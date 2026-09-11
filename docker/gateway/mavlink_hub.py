#!/usr/bin/env python3
"""Single-link MAVLink hub for QGroundControl.

Aggregates every vehicle stream onto one TCP port while keeping AERPAW's link
isolation: a vehicle's traffic goes only to ground clients and never into
another vehicle's link, GCS heartbeats are dropped, and targeted GCS traffic
is routed only to the vehicle it addresses. Without this isolation MAVLink
clients inside an E-VM bind to a neighboring vehicle's heartbeats and fail.
"""

from __future__ import annotations

import argparse
import socket
import sys
import threading
import time

HEARTBEAT_MSGID = 0
RECONNECT_DELAY = 2.0


def load_parser():
    try:
        from pymavlink.dialects.v20 import common
    except ImportError:
        return None
    return common.MAVLink


class Backend:
    def __init__(self, host: str, port: int, sysid: int):
        self.host = host
        self.port = port
        self.sysid = sysid
        self.sock: socket.socket | None = None

    def send(self, data: bytes) -> None:
        if self.sock is not None:
            try:
                self.sock.sendall(data)
            except OSError:
                pass  # the owning thread reconnects


class Client:
    def __init__(self, sock: socket.socket):
        self.sock = sock


class Hub:
    def __init__(self, listen_port: int, backends: list[Backend], parser_factory):
        self.listen_port = listen_port
        self.backends = backends
        self.by_sysid = {backend.sysid: backend for backend in backends}
        self.parser_factory = parser_factory
        self.clients: list[Client] = []
        self._send_lock = threading.Lock()
        self._stop = threading.Event()

    def message_id(self, msg) -> int:
        get_msg_id = getattr(msg, "get_msgId", None)
        if get_msg_id is not None:
            return get_msg_id()
        return getattr(msg, "msgid", -1)

    def forward_to_clients(self, raw: bytes) -> None:
        with self._send_lock:
            for client in list(self.clients):
                try:
                    client.sock.sendall(raw)
                except OSError:
                    self.clients.remove(client)
                    try:
                        client.sock.close()
                    except OSError:
                        pass

    def route_from_client(self, msg) -> None:
        raw = getattr(msg, "_msgbuf", None)
        if raw is None:
            return
        if self.message_id(msg) == HEARTBEAT_MSGID:
            return  # never leak GCS heartbeats into vehicle links
        target = getattr(msg, "target_system", None)
        if target in (None, 0):
            destinations = self.backends
        else:
            backend = self.by_sysid.get(target)
            destinations = [backend] if backend is not None else []
        with self._send_lock:
            for backend in destinations:
                backend.send(raw)

    def _pump(self, sock: socket.socket, handle) -> None:
        parser = self.parser_factory(None)
        while not self._stop.is_set():
            chunk = sock.recv(65536)
            if not chunk:
                return
            try:
                messages = parser.parse_buffer(chunk) or []
            except Exception:
                # mavlink-router prefixes non-MAVLink bytes on new TCP links;
                # drop the bad parser state and resync on the byte stream
                parser = self.parser_factory(None)
                continue
            for msg in messages:
                handle(msg)

    def backend_loop(self, backend: Backend) -> None:
        while not self._stop.is_set():
            try:
                sock = socket.create_connection((backend.host, backend.port), timeout=10)
            except OSError:
                time.sleep(RECONNECT_DELAY)
                continue
            backend.sock = sock
            try:
                self._pump(sock, lambda msg: self.forward_to_clients(msg._msgbuf))
            except OSError:
                pass
            finally:
                backend.sock = None
                try:
                    sock.close()
                except OSError:
                    pass
            time.sleep(RECONNECT_DELAY)

    def client_loop(self, client: Client) -> None:
        try:
            self._pump(client.sock, lambda msg: self.route_from_client(msg))
        except OSError:
            pass
        finally:
            with self._send_lock:
                if client in self.clients:
                    self.clients.remove(client)
            try:
                client.sock.close()
            except OSError:
                pass

    def run(self) -> None:
        for backend in self.backends:
            threading.Thread(target=self.backend_loop, args=(backend,), daemon=True).start()

        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind(("0.0.0.0", self.listen_port))
        listener.listen()
        while not self._stop.is_set():
            sock, _ = listener.accept()
            client = Client(sock)
            self.clients.append(client)
            threading.Thread(target=self.client_loop, args=(client,), daemon=True).start()


def parse_backend(spec: str) -> Backend:
    host, port, sysid = spec.rsplit(":", 2)
    return Backend(host, int(port), int(sysid))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--listen", type=int, default=5760)
    parser.add_argument("backends", nargs="+", metavar="HOST:PORT:SYSID")
    args = parser.parse_args()

    parser_factory = load_parser()
    if parser_factory is None:
        print("mavlink_hub needs pymavlink", file=sys.stderr)
        return 1

    hub = Hub(args.listen, [parse_backend(spec) for spec in args.backends], parser_factory)
    hub.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

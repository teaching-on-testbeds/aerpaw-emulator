#!/usr/bin/env python3
"""Bridge one raw MAVLink TCP client to a local UDP endpoint."""

from __future__ import annotations

import argparse
import selectors
import socket


def run(tcp_port: int, udp_port: int) -> None:
    selector = selectors.DefaultSelector()
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(("0.0.0.0", tcp_port))
    listener.listen()
    listener.setblocking(False)
    selector.register(listener, selectors.EVENT_READ)

    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.connect(("127.0.0.1", udp_port))
    udp.setblocking(False)
    selector.register(udp, selectors.EVENT_READ)

    clients = {}

    def close_client(connection: socket.socket) -> None:
        selector.unregister(connection)
        connection.close()
        clients.pop(connection, None)

    try:
        while True:
            for key, events in selector.select():
                if key.fileobj is listener:
                    connection, _ = listener.accept()
                    connection.setblocking(False)
                    clients[connection] = bytearray()
                    selector.register(connection, selectors.EVENT_READ)
                elif key.fileobj is udp:
                    try:
                        packet = udp.recv(65535)
                    except BlockingIOError:
                        continue
                    for connection, pending in clients.items():
                        pending.extend(packet)
                        selector.modify(connection, selectors.EVENT_READ | selectors.EVENT_WRITE)
                else:
                    connection = key.fileobj
                    pending = clients.get(connection)
                    if pending is None:
                        continue
                    if events & selectors.EVENT_READ:
                        try:
                            packet = connection.recv(65535)
                        except BlockingIOError:
                            packet = None
                        except OSError:
                            packet = b""
                        if packet == b"":
                            close_client(connection)
                            continue
                        if packet is not None:
                            try:
                                udp.send(packet)
                            except OSError:
                                pass
                    if events & selectors.EVENT_WRITE and pending:
                        try:
                            sent = connection.send(pending)
                        except BlockingIOError:
                            continue
                        except OSError:
                            close_client(connection)
                            continue
                        del pending[:sent]
                        if not pending:
                            selector.modify(connection, selectors.EVENT_READ)
    finally:
        for connection in clients:
            connection.close()
        selector.close()
        udp.close()
        listener.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tcp-port", type=int, default=5760)
    parser.add_argument("--udp-port", type=int, default=14560)
    args = parser.parse_args()
    run(args.tcp_port, args.udp_port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Generate a small mavlink-router configuration for one simulated vehicle."""

from __future__ import annotations

import argparse
from pathlib import Path


def render(source_host: str, source_port: int, endpoints: list[tuple[str, int]]) -> str:
    lines = [
        "[General]",
        "TcpServerPort = 5762",
        "ReportStats = true",
        "",
        "[TcpEndpoint sitl]",
        "Mode = Normal",
        f"Address = {source_host}",
        f"Port = {source_port}",
        "",
    ]
    for index, (host, port) in enumerate(endpoints, start=1):
        lines.extend(
            [
                f"[UdpEndpoint evm_{index}]",
                "Mode = Normal",
                f"Address = {host}",
                f"Port = {port}",
                "Group = evm",
                "",
            ]
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-host", default="127.0.0.1")
    parser.add_argument("--source-port", type=int, default=5760)
    parser.add_argument("--endpoint", action="append", required=True, metavar="HOST:PORT")
    args = parser.parse_args()

    endpoints = []
    for value in args.endpoint:
        host, separator, port = value.rpartition(":")
        if not separator or not host or not port:
            parser.error(f"invalid endpoint: {value!r}")
        endpoints.append((host, int(port)))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(args.source_host, args.source_port, endpoints), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

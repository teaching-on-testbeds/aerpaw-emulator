#!/usr/bin/env bash
set -Eeuo pipefail

: "${CVM_ENDPOINTS:?CVM_ENDPOINTS is required}"

mkdir -p /etc/mavlink-router
{
    printf '%s\n' '[General]' 'TcpServerPort = 0' 'ReportStats = true' 'SnifferSysid = 255' ''
    endpoint_number=0
    for endpoint in ${CVM_ENDPOINTS}; do
        host=${endpoint%:*}
        port=${endpoint##*:}
        address=$(python3 -c 'import socket, sys; print(socket.gethostbyname(sys.argv[1]))' "$host")
        endpoint_number=$((endpoint_number + 1))
        printf '[TcpEndpoint cvm_%d]\nMode = Normal\nAddress = %s\nPort = %s\n\n' \
            "$endpoint_number" "$address" "$port"
    done
    printf '%s\n' '[UdpEndpoint qgc]' 'Mode = Server' 'Address = 127.0.0.1' 'Port = 14560' ''
} > /etc/mavlink-router/main.conf

mavlink-routerd -c /etc/mavlink-router/main.conf &
router_pid=$!

cleanup() {
    kill "$router_pid" 2>/dev/null || true
    wait "$router_pid" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

python3 /opt/standalone/docker/gateway/tcp_udp_bridge.py \
    --tcp-port 5760 \
    --udp-port 14560

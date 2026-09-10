#!/usr/bin/env bash
set -Eeuo pipefail

: "${EVM_SERVICE:?EVM_SERVICE is required}"
: "${SITL_HOME:?SITL_HOME is required}"
: "${SITL_SYSID:?SITL_SYSID is required}"

case "${VEHICLE_TYPE:-uav}" in
    uav)
        sitl_binary="${SITL_BINARY:-arducopter}"
        sitl_model="${SITL_MODEL:-+}"
        parameter_file=/opt/standalone/docker/cvm/params/uav.parm
        ;;
    ugv)
        sitl_binary="${SITL_BINARY:-ardurover}"
        sitl_model="${SITL_MODEL:-rover}"
        parameter_file=/opt/standalone/docker/cvm/params/ugv.parm
        ;;
    *)
        echo "VEHICLE_TYPE must be uav or ugv" >&2
        exit 2
        ;;
esac

resolve_binary() {
    if command -v "$1" >/dev/null 2>&1; then
        command -v "$1"
        return
    fi
    for candidate in \
        "/ardupilot/build/sitl/bin/$1" \
        "/root/ardupilot/build/sitl/bin/$1" \
        "/root/workarea/ardupilot/build/sitl/bin/$1" \
        "/opt/ardupilot/build/sitl/bin/$1"; do
        if [ -x "$candidate" ]; then
            printf '%s\n' "$candidate"
            return
        fi
    done
    echo "could not find $1 in the ArduPilot image" >&2
    exit 127
}

sitl_path=$(resolve_binary "$sitl_binary")
mkdir -p /etc/mavlink-router

"$sitl_path" -S -w --model "$sitl_model" --speedup "${SPEEDUP:-1}" \
    --defaults "$parameter_file" --home "$SITL_HOME" --sysid "$SITL_SYSID" &
sitl_pid=$!
printf '%s\n' "$sitl_pid" > /run/standalone-sitl.pid
router_pid=""

cleanup() {
    if [ -n "$router_pid" ]; then
        kill "$router_pid" 2>/dev/null || true
    fi
    kill "$sitl_pid" 2>/dev/null || true
    if [ -n "$router_pid" ]; then
        wait "$router_pid" 2>/dev/null || true
    fi
    wait "$sitl_pid" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

until nc -z 127.0.0.1 5760; do
    if ! kill -0 "$sitl_pid" 2>/dev/null; then
        exit 1
    fi
    sleep 1
done

until evm_address=$(python3 -c 'import socket, sys; print(socket.gethostbyname(sys.argv[1]))' "$EVM_SERVICE" 2>/dev/null); do
    if ! kill -0 "$sitl_pid" 2>/dev/null; then
        exit 1
    fi
    sleep 1
done

python3 /opt/standalone/tools/generate_router_config.py \
    --output /etc/mavlink-router/main.conf \
    --source-host 127.0.0.1 \
    --source-port 5760 \
    --endpoint "$evm_address:14550" \
    --endpoint "$evm_address:14551"

mavlink-routerd -c /etc/mavlink-router/main.conf &
router_pid=$!
printf '%s\n' "$router_pid" > /run/standalone-mavlink-router.pid
wait "$router_pid"

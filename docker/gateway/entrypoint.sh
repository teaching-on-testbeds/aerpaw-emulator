#!/usr/bin/env bash
set -Eeuo pipefail

: "${CVM_ENDPOINTS:?CVM_ENDPOINTS is required}"

exec python3 /opt/standalone/docker/gateway/mavlink_hub.py --listen 5760 ${CVM_ENDPOINTS}

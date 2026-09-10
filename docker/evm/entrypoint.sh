#!/usr/bin/env bash
set -Eeuo pipefail

"/opt/standalone/docker/evm/setup-aerpaw-profile.sh"

if [ "$#" -gt 0 ]; then
    exec "$@"
fi

exec sleep infinity

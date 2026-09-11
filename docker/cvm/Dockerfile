FROM ubuntu:22.04

ARG ARDUPILOT_COMMIT=5b597044263bd8e8eecf9376678cf9fba218897c
ARG MAVLINK_ROUTER_REF=v4

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        git \
        libglib2.0-dev \
        libsystemd-dev \
        lsb-release \
        meson \
        netcat-openbsd \
        ninja-build \
        pkg-config \
        python3 \
        python3-pip \
        sudo

RUN useradd --create-home --shell /bin/bash ardupilot \
    && printf 'ardupilot ALL=(ALL) NOPASSWD:ALL\n' > /etc/sudoers.d/ardupilot \
    && chmod 0440 /etc/sudoers.d/ardupilot

RUN git clone --branch aerpaw-4.3.6 --single-branch --recurse-submodules \
        https://github.com/morzack/ardupilot.git /opt/ardupilot \
    && cd /opt/ardupilot \
    && git checkout "$ARDUPILOT_COMMIT" \
    && git submodule update --init --recursive \
    && chown -R ardupilot:ardupilot /opt/ardupilot

RUN sudo --user ardupilot --set-home bash -lc \
    'cd /opt/ardupilot \
    && SKIP_AP_EXT_ENV=1 SKIP_AP_GRAPHIC_ENV=1 SKIP_AP_COV_ENV=1 \
        Tools/environment_install/install-prereqs-ubuntu.sh -y \
    && source "$HOME/.profile" \
    && ./waf configure --board sitl \
    && ./waf copter rover'

RUN git clone --branch "$MAVLINK_ROUTER_REF" --depth 1 --recurse-submodules \
        https://github.com/mavlink-router/mavlink-router.git /tmp/mavlink-router \
    && meson setup -Dsystemdsystemunitdir=/usr/lib/systemd/system \
        /tmp/mavlink-router/build /tmp/mavlink-router \
    && ninja -C /tmp/mavlink-router/build install \
    && rm -rf /tmp/mavlink-router /var/lib/apt/lists/*

RUN python3 -m pip install --no-cache-dir "pymavlink>=2.4.41,<3"

COPY tools/generate_router_config.py /opt/standalone/tools/generate_router_config.py
COPY docker/cvm/entrypoint.sh /opt/standalone/docker/cvm/entrypoint.sh
COPY docker/gateway/entrypoint.sh /opt/standalone/docker/gateway/entrypoint.sh
COPY docker/gateway/mavlink_hub.py /opt/standalone/docker/gateway/mavlink_hub.py
COPY docker/cvm/params /opt/standalone/docker/cvm/params

RUN chmod +x /opt/standalone/docker/cvm/entrypoint.sh \
    /opt/standalone/docker/gateway/entrypoint.sh \
    /opt/standalone/docker/gateway/mavlink_hub.py

ENTRYPOINT ["/opt/standalone/docker/cvm/entrypoint.sh"]

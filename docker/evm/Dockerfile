FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/opt/standalone/experiments:/opt/standalone/vendor/aerpawlib \
    AERPAW_REPO=/root/AERPAW-Dev \
    PROFILE_DIR=/root/AERPAW-Dev/AHN/E-VM/Profile_software \
    PATH=/root/AERPAW-Dev/AHN/E-VM/bin:$PATH

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        git \
        iproute2 \
        python3 \
        python3-pip \
        screen \
        moreutils \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /opt/standalone/requirements.txt
RUN python3 -m pip install --no-cache-dir -r /opt/standalone/requirements.txt

COPY vendor/aerpawlib /opt/standalone/vendor/aerpawlib
RUN python3 -m pip install --no-cache-dir --no-deps /opt/standalone/vendor/aerpawlib

COPY experiments /opt/standalone/experiments
COPY tools/auto_arm.py /opt/standalone/tools/auto_arm.py
COPY tools/experiment_runner.py /opt/standalone/tools/experiment_runner.py
COPY tools/run-aerpawlib /usr/local/bin/run-aerpawlib
COPY docker/evm/entrypoint.sh /opt/standalone/docker/evm/entrypoint.sh
COPY docker/evm/setup-aerpaw-profile.sh /opt/standalone/docker/evm/setup-aerpaw-profile.sh
COPY vendor/aerpaw-profile/AHN/E-VM/Profile_software /root/AERPAW-Dev/AHN/E-VM/Profile_software
COPY vendor/aerpaw-profile/AHN/E-VM/bin /root/AERPAW-Dev/AHN/E-VM/bin
COPY vendor/aerpaw-profile/AHN/C-VM/MAVLink_Filter/Geofences /root/AERPAW-Dev/AHN/C-VM/MAVLink_Filter/Geofences

RUN ln -s /root/AERPAW-Dev/AHN/E-VM/Profile_software /root/Profiles \
    && ln -s /root/Profiles/ProfileScripts/startAll.sh /root/startexperiment.sh \
    && ln -s /root/Profiles/ProfileScripts/stopAll.sh /root/stopexperiment.sh \
    && ln -s /root/Profiles/ProfileScripts/reset.sh /root/reset.sh \
    && mkdir -p /results \
    && ln -s /results /root/Results \
    && printf '\nexport AERPAW_REPO="${AERPAW_REPO:-/root/AERPAW-Dev}"\nexport PROFILE_DIR="$AERPAW_REPO/AHN/E-VM/Profile_software"\nexport PATH="$PATH:${AERPAW_REPO}/AHN/E-VM/bin"\n' >> /root/.bashrc

RUN bash -lc 'shopt -s globstar nullglob; chmod +x \
    /root/AERPAW-Dev/AHN/E-VM/Profile_software/ProfileScripts/**/*.sh \
    /root/AERPAW-Dev/AHN/E-VM/bin/*' \
    && chmod +x /opt/standalone/docker/evm/entrypoint.sh \
    /opt/standalone/docker/evm/setup-aerpaw-profile.sh \
    /usr/local/bin/run-aerpawlib

WORKDIR /opt/standalone
ENTRYPOINT ["/opt/standalone/docker/evm/entrypoint.sh"]

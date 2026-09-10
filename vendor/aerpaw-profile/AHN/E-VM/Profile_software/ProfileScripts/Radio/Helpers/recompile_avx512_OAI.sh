#!/bin/bash

cd /opt/openairinterface-AERPAW/cmake_targets
./build_oai -w USRP --ninja --eNB --nrUE --gNB --build-lib "nrscope" -C --cmake-opt "-DCMAKE_CXX_FLAGS='-march=cascadelake -mtune=cascadelake'"
if ! grep "march=cascadelake" ./ran_build/build/build.ninja; then
	echo "Failed to recompile Architecture"
	exit 1
elif ! grep "mtune=cascadelake" ./ran_build/build/build.ninja; then
	echo "Failed to recompile Tune"
	exit 1
fi
echo "Recompile successful"

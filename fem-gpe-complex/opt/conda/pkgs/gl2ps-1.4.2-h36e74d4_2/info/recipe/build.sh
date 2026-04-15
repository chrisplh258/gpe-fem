#!/usr/bin/env bash

set -o xtrace -o nounset -o pipefail -o errexit

cmake -S ./source -B build -G Ninja \
    -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
    ${CMAKE_ARGS} -LAH
cmake --build build --target install -j${CPU_COUNT}

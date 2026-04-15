#!/bin/bash

export CMAKE_CONFIG="Release"

mkdir "build_${CMAKE_CONFIG}"
pushd "build_${CMAKE_CONFIG}"

cmake ${CMAKE_ARGS} \
      -G Ninja \
      -D CMAKE_BUILD_TYPE:STRING="${CMAKE_CONFIG}" \
      -D CMAKE_PREFIX_PATH:PATH="${PREFIX}" \
      -D CMAKE_INSTALL_PREFIX:PATH="${PREFIX}" \
      "${SRC_DIR}" \
;
cmake --build . --parallel ${CPU_COUNT}
cmake --install .

popd

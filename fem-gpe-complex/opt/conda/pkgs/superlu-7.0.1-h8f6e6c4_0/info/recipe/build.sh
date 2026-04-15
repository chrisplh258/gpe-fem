#!/usr/bin/env bash

mkdir build
cd build

cmake ${CMAKE_ARGS} .. \
    -DCMAKE_INSTALL_PREFIX="${PREFIX}" \
    -DCMAKE_INSTALL_LIBDIR="${PREFIX}/lib" \
    -DBUILD_SHARED_LIBS=ON \
    -DTPL_BLAS_LIBRARIES="blas;cblas" \
    -Denable_internal_blaslib=OFF \
    -Denable_tests=ON \
    -Denable_examples=OFF \
    -Denable_doc=OFF

make -j"${CPU_COUNT:-1}"
if [[ "${CONDA_BUILD_CROSS_COMPILATION}" != "1" ]]; then
  ctest --output-on-failure
fi
make install

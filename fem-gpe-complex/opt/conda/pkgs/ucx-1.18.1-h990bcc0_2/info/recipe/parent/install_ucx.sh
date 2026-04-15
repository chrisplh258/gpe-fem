#!/bin/bash

set -xeuo pipefail

EXTRA_ARGS=" --with-rdmacm=${PREFIX} --with-verbs=${PREFIX}"

if [[ "${cuda_compiler_version}" =~ 12.* ]]; then
  EXTRA_ARGS="${EXTRA_ARGS} --with-cuda=${PREFIX}"
elif [[ "${cuda_compiler_version}" != "None" ]]; then
  if [[ "${CONDA_BUILD_CROSS_COMPILATION:-}" == "1" ]]; then
    if [[ "${target_platform}" == "linux-aarch64" ]]; then
        CUDA_HOME="${CUDA_HOME}/targets/sbsa-linux"
    elif [[ "${target_platform}" == "linux-ppc64le" ]]; then
        CUDA_HOME="${CUDA_HOME}/targets/ppc64le-linux"
    else
        echo "Unsupported target_platform: ${target_platform}"
        exit 1
    fi
  fi
  EXTRA_ARGS="${EXTRA_ARGS} --with-cuda=${CUDA_HOME}"
fi

./contrib/configure-release \
    --build="${BUILD}" \
    --host="${HOST}" \
    --prefix="${PREFIX}" \
    --with-sysroot \
    --disable-static \
    --enable-openmp \
    --enable-cma \
    --enable-mt \
    --with-gnu-ld \
    ${EXTRA_ARGS} || { cat config.log; exit 1; }


make -j${CPU_COUNT}
make install

cp "${RECIPE_DIR}/ucx-post-link.sh" "${PREFIX}/bin/.ucx-post-link.sh"

mkdir -p "${PREFIX}/etc/conda/activate.d"
cp -v "${RECIPE_DIR}/ucx-activate.sh" "${PREFIX}/etc/conda/activate.d/"

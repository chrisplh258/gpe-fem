#!/bin/bash
set -ex
cd python

# cross-compiled linux produces wrong wheel tags
# causing pip check to fail
if [[ "${target_platform}" == "linux-aarch64" ]]; then
  export _PYTHON_HOST_PLATFORM=linux_aarch64
elif [[ "${target_platform}" == "linux-ppc64le" ]]; then
  export _PYTHON_HOST_PLATFORM=linux_ppc64le
fi

$PYTHON -m pip install --no-build-isolation --no-deps -vv .

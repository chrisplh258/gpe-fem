#!/bin/bash

if [[ "${target_platform}" == osx-* ]]; then
  export glu_gl_provider="gl"
else
  export glu_gl_provider="glvnd"
fi

mkdir -p build
meson setup build ${MESON_ARGS} -Dgl_provider=${glu_gl_provider} --prefix=${PREFIX}

# Build and install
meson compile -C build
meson install -C build

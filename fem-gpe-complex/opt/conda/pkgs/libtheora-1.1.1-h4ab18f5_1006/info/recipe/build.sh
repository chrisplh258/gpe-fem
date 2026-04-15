#!/bin/bash

export C_INCLUDE_PATH=${PREFIX}/include
export LDFLAGS="-L${PREFIX}/lib"
export PKG_CONFIG_PATH=${PREFIX}/lib/pkgconfig

rm ./config.sub
./autogen.sh

# -fforce-addr is not supported in clang
if [ `uname` == Darwin ]; then
    sed -i.bak 's/-fforce-addr //g' ./configure
    sed -i.bak 's/-fforce-addr //g' ./configure.ac
    export LDFLAGS="${LDFLAGS} -Wl,-rpath,$PREFIX/lib"
fi

./configure --prefix=${PREFIX} --disable-examples --disable-spec
make

if [[ "$CONDA_BUILD_CROSS_COMPILATION" != "1" ]]; then
    make check
fi

make install

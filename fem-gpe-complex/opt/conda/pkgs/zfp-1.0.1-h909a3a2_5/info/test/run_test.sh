

set -ex



test -f $PREFIX/include/zfp.h
test -f ${PREFIX}/lib/cmake/zfp/zfp-config.cmake
test -f $PREFIX/lib/libzfp.so.1.0.1
test -f $PREFIX/lib/libzfp${SHLIB_EXT}
which zfp
exit 0

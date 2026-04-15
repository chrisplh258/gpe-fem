

set -ex



test -f $PREFIX/lib/libpciaccess.so
test -f $PREFIX/lib/libpciaccess.so.0
test -f $PREFIX/lib/pkgconfig/pciaccess.pc
test -f $PREFIX/include/pciaccess.h
exit 0

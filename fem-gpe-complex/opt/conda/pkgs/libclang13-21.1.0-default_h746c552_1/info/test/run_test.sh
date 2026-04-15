

set -ex



test -f $PREFIX/lib/libclang.so.13
test ! -f $PREFIX/lib/libclang.so
test ! -f $PREFIX/lib/libclang.so.21
test ! -f $PREFIX/lib/libclang.so.21.1.0
exit 0



set -ex



test -f $PREFIX/lib/libclang-cpp.so.20.1
test ! -f $PREFIX/lib/libclang-cpp.so
exit 0

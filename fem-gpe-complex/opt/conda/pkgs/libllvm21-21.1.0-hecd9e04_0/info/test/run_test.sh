

set -ex



test -f $PREFIX/lib/libLLVM-21.so
test -f $PREFIX/lib/libLLVM.so.21.1
exit 0

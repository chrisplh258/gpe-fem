

set -ex



test -f $PREFIX/lib/libLLVM-20.so
test -f $PREFIX/lib/libLLVM.so.20.1
exit 0

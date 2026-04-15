

set -ex



test -h $PREFIX/lib/libudev.so.1
test -f $PREFIX/lib/libudev.so.1
exit 0

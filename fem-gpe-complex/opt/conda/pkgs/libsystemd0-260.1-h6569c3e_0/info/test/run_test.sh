

set -ex



test -h $PREFIX/lib/libsystemd.so.0
test -f $PREFIX/lib/libsystemd.so.0
exit 0

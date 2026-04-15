

set -ex



test -f $PREFIX/lib/libfabric.so.1
test ! -f $PREFIX/lib/libfabric${SHLIB_EXT}
if [ "$FI_PROVIDER" != "tcp" ]; then exit 1; fi
exit 0

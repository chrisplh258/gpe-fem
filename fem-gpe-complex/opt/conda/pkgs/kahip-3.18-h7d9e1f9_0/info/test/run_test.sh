

set -ex



test -f $PREFIX/lib/libkahip${SHLIB_EXT}
test -f $PREFIX/lib/libkahip_static${SHLIB_EXT}
kaffpa examples/delaunay_n15.graph --k 2 --preconfiguration=strong
exit 0



set -ex



test -f ${PREFIX}/lib/libproj${SHLIB_EXT}
test ! -f ${PREFIX}/lib/libproj.a
exit 0

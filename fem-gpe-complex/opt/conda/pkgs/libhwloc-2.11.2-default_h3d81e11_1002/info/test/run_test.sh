

set -ex



hwloc-ls
test -f ${PREFIX}/lib/libhwloc${SHLIB_EXT}
exit 0

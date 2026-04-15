

set -ex



test -f "${PREFIX}/lib/libucp${SHLIB_EXT}"
test ! -f "${PREFIX}/lib/libucp.a"
test -f "${PREFIX}/lib/libucm${SHLIB_EXT}"
test ! -f "${PREFIX}/lib/libucm.a"
test -f "${PREFIX}/lib/libucs${SHLIB_EXT}"
test ! -f "${PREFIX}/lib/libucs.a"
test -f "${PREFIX}/lib/libuct${SHLIB_EXT}"
test ! -f "${PREFIX}/lib/libuct.a"
test -f "${PREFIX}/bin/.ucx-post-link.sh"
test -f "${PREFIX}/bin/ucx_info"
ucx_info -v
exit 0

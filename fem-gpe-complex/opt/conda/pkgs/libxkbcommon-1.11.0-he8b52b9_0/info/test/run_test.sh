

set -ex



test -f "${PREFIX}/lib/libxkbcommon${SHLIB_EXT}"
xkbcli --help
exit 0

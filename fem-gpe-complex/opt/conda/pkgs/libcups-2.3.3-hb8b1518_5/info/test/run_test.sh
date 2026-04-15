

set -ex



test -f ${PREFIX}/lib/libcups${SHLIB_EXT}
test -f ${PREFIX}/include/cups/cups.h
exit 0

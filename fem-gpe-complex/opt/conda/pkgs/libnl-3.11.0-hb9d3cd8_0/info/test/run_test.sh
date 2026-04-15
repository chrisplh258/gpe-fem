

set -ex



test -f "$PREFIX/lib/libnl-3.so"
test -f "$PREFIX/lib/libnl-cli-3.so"
test -f "$PREFIX/lib/libnl-genl-3.so"
test -f "$PREFIX/lib/libnl-idiag-3.so"
test -f "$PREFIX/lib/libnl-nf-3.so"
test -f "$PREFIX/lib/libnl-route-3.so"
test -f "$PREFIX/include/libnl3/netlink/types.h"
exit 0



set -ex



test ! -f "${PREFIX}/lib/libpugixml.a"
test -f "${PREFIX}/include/pugixml.hpp"
test -f "${PREFIX}/lib/libpugixml${SHLIB_EXT}"
exit 0

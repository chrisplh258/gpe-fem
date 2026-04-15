

set -ex



test -f "${PREFIX}/include/json/json.h"
test -f "${PREFIX}/lib/pkgconfig/jsoncpp.pc"
test ! -f "${PREFIX}/lib/libjsoncpp.a"
python -c "import ctypes; ctypes.cdll[r'${PREFIX}/lib/libjsoncpp${SHLIB_EXT}']"
cmake-package-check jsoncpp
exit 0

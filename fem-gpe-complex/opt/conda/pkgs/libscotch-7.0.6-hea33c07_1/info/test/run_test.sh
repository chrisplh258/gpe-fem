#!/bin/bash
set -xeuo pipefail

python3 -c "import ctypes; ctypes.CDLL('${PREFIX}/lib/libscotch${SHLIB_EXT}')"

$CC $CFLAGS $LDFLAGS test/test_scotch.c -o test_scotch -lscotch
./test_scotch

# build tests from repo
for test in test_scotch_graph_color; do
  $CC $CFLAGS $LDFLAGS src/check/${test}.c -o ${test} -lscotch -lscotcherr
done
# run tests
./test_scotch_graph_color src/check/data/m4x4.grf


set -ex



test -f "${PREFIX}/lib/libscotch${SHLIB_EXT}"
test -f "${PREFIX}/lib/libscotcherr${SHLIB_EXT}"
test -f "${PREFIX}/lib/libscotcherrexit${SHLIB_EXT}"
test -f "${PREFIX}/lib/libesmumps${SHLIB_EXT}"
test -f "${PREFIX}/include/scotch.h"
test -f "${PREFIX}/include/scotchf.h"
test -f "${PREFIX}/include/esmumps.h"
test ! -f "${PREFIX}/include/metis.h"
test -f "${PREFIX}/include/scotch/metis.h"
test ! -f "${PREFIX}/bin/gord"
test -f "$PREFIX/lib/cmake/scotch/SCOTCHConfig.cmake"
exit 0

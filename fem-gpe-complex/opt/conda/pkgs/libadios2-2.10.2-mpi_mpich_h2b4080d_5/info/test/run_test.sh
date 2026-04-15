

set -ex



test -f ${PREFIX}/lib/cmake/adios2/adios2-config.cmake
test -f ${PREFIX}/lib/cmake/adios2/adios2-c-targets.cmake
test -f ${PREFIX}/lib/cmake/adios2/adios2-cxx11-targets.cmake
test -f ${PREFIX}/lib/libadios2_cxx11${SHLIB_EXT}
test -f ${PREFIX}/lib/libadios2_c${SHLIB_EXT}
test ! -d ${SP_DIR}/adios2
test ! -f ${PREFIX}/bin/bp5dbg
bash test-libadios.sh
exit 0

#!/bin/sh
set -ex

# Test shared library
${CXX} ${CXXFLAGS} -I${PREFIX}/include -c test.cc -o test.o
${CXX} ${LDFLAGS} -L${PREFIX}/lib test.o -ldouble-conversion -o test.exe
./test.exe

# Test static library
${CXX} ${CXXFLAGS} -I${PREFIX}/include -c test.cc -o test_static.o
${CXX} ${LDFLAGS} -L${PREFIX}/lib test_static.o ${PREFIX}/lib/libdouble-conversion.a -o test_static.exe
./test_static.exe


set -ex



test -f $PREFIX/lib/libdouble-conversion.a
test -f $PREFIX/lib/libdouble-conversion${SHLIB_EXT}
exit 0

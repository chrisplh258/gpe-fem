set -eux

cmake -B build \
  -DCMAKE_INSTALL_PREFIX=$PREFIX \
  test-ufcx

cmake --build build --verbose
cmake --install build
test-ufcx


set -ex



test -f ${PREFIX}/include/ufcx.h
pkg-config --cflags ufcx
exit 0

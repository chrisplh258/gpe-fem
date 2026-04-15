cmake \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX="${PREFIX}" \
  -B build-dir \
  -S cmake/
cmake --build build-dir
cmake --install build-dir

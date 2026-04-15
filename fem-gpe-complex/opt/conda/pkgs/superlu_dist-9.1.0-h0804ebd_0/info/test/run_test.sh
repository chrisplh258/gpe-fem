set -exuo pipefail

pushd EXAMPLE
mpicc pddrive.c dcreate_matrix.c -o pddrive \
  $CFLAGS \
  $LDFLAGS \
  $(pkg-config --cflags --libs superlu_dist)
mpiexec -n 2 ./pddrive g20.rua
popd

pushd FORTRAN
mpifort f_pddrive.F90 -o f_pddrive \
  $FFLAGS \
  $LDFLAGS \
  $(pkg-config --cflags superlu_dist) -lsuperlu_dist_fortran
mpiexec -n 4 ./f_pddrive ../EXAMPLE/g20.rua
popd


set -ex



pkg-config --cflags --libs superlu_dist
test ! -f ${PREFIX}/lib/libsuperlu_dist.a
test -f ${PREFIX}/lib/libsuperlu_dist${SHLIB_EXT}
test -f ${PREFIX}/include/superlu-dist/superlu_defs.h
test ! -f ${PREFIX}/include/colamd.h
test ! -f ${PREFIX}/include/supermatrix.h
test ! -f ${PREFIX}/lib/libsuperlu_dist_fortran.a
test -f ${PREFIX}/lib/libsuperlu_dist_fortran${SHLIB_EXT}
test -f ${PREFIX}/include/superlu-dist/superlu_dist_config.fh
test -f ${PREFIX}/include/superlu-dist/superlu_mod.mod
test ! -d ${PREFIX}/lib/EXAMPLE
test ! -f ${PREFIX}/lib/libsuperlu_dist_python.so
exit 0

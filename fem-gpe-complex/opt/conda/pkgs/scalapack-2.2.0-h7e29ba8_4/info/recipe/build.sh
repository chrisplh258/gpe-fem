#!/bin/sh

# see https://github.com/Reference-ScaLAPACK/scalapack/issues/31
export CFLAGS="${CFLAGS} -Wno-error=implicit-function-declaration"

if [[ "$target_platform" == "osx-64" ]]; then
  TOOLS_DIR=$(dirname $($FC --print-libgcc-file-name))
  if [[ ! -f "$TOOLS_DIR/ld" ]]; then
    ln -sf $LD $TOOLS_DIR/ld
    ln -sf $LD $BUILD_PREFIX/bin/ld
  fi
fi

# Workaround for https://github.com/conda-forge/scalapack-feedstock/pull/30#issuecomment-1061196317
export FFLAGS="${FFLAGS} -fallow-argument-mismatch"
# compiler adds $PREFIX/include via isystem, but this doesn't always have an effect
# only seems relevant working with openmpi for some reason
# https://github.com/conda-forge/gfortran_osx-64-feedstock/issues/57
export OMPI_FCFLAGS="${FFLAGS} -I$PREFIX/include"
export OMPI_LDFLAGS=${LDFLAGS}


if [[ "$CONDA_BUILD_CROSS_COMPILATION" == "1" ]]; then
  # This is only used by open-mpi's mpicc
  # ignored in other cases
  export OMPI_CC=$CC
  export OMPI_CXX=$CXX
  export OMPI_FC=$FC
  export OPAL_PREFIX=$PREFIX
  export EXTRA_CMAKE="-DCDEFS=Add_"
  export EXTRA_CMAKE="${EXTRA_CMAKE} --debug-output --debug-trycompile"
fi

# As mpi libraries are not correctly linked in CMake scripts, use mpi wrappers for the compilers
export CC=mpicc
export CXX=mpic++
export FC=mpifort

mkdir build && cd build
cmake ${CMAKE_ARGS} \
    $EXTRA_CMAKE \
    -DBLAS_LIBRARIES="blas" \
    -DLAPACK_LIBRARIES="lapack" \
    -DBUILD_SHARED_LIBS=ON \
    -DCMAKE_INSTALL_PREFIX="$PREFIX" \
    -DCMAKE_PREFIX_PATH="$PREFIX" \
    -DCMAKE_BUILD_TYPE=Release \
    .. || (
      cat CMakeFiles/CMakeConfigureLog.yaml;
      exit 1
    )

make install -j${CPU_COUNT}

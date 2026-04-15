

set -ex



test ! -f ${PREFIX}/lib/libfftw3f.a
test ! -f ${PREFIX}/lib/libfftw3.a
test ! -f ${PREFIX}/lib/libfftw3l.a
test ! -f ${PREFIX}/lib/libfftw3f_threads.a
test ! -f ${PREFIX}/lib/libfftw3_threads.a
test ! -f ${PREFIX}/lib/libfftw3l_threads.a
test ! -f ${PREFIX}/lib/libfftw3f_omp.a
test ! -f ${PREFIX}/lib/libfftw3_omp.a
test ! -f ${PREFIX}/lib/libfftw3l_omp.a
test -f ${PREFIX}/include/fftw3.h
python -c "import ctypes; ctypes.cdll[r'${PREFIX}/lib/libfftw3${SHLIB_EXT}']"
python -c "import ctypes; ctypes.cdll[r'${PREFIX}/lib/libfftw3_threads${SHLIB_EXT}']"
python -c "import ctypes; ctypes.cdll[r'${PREFIX}/lib/libfftw3f${SHLIB_EXT}']"
python -c "import ctypes; ctypes.cdll[r'${PREFIX}/lib/libfftw3f_threads${SHLIB_EXT}']"
python -c "import ctypes; ctypes.cdll[r'${PREFIX}/lib/libfftw3l${SHLIB_EXT}']"
python -c "import ctypes; ctypes.cdll[r'${PREFIX}/lib/libfftw3l_threads${SHLIB_EXT}']"
python -c "import ctypes; ctypes.cdll[r'${PREFIX}/lib/libfftw3_omp${SHLIB_EXT}']"
python -c "import ctypes; ctypes.cdll[r'${PREFIX}/lib/libfftw3f_omp${SHLIB_EXT}']"
python -c "import ctypes; ctypes.cdll[r'${PREFIX}/lib/libfftw3l_omp${SHLIB_EXT}']"
test -f ${PREFIX}/lib/libfftw3_mpi${SHLIB_EXT} || exit 1
test -f ${PREFIX}/lib/libfftw3f_mpi${SHLIB_EXT} || exit 1
test -f ${PREFIX}/lib/libfftw3l_mpi${SHLIB_EXT} || exit 1
bash test_cmake.sh
exit 0

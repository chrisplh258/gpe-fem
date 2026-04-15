

set -ex



specdir=$PREFIX/lib/gcc/x86_64-conda-linux-gnu/13.4.0
test -f $specdir/conda.specs
CC=$(${PREFIX}/bin/*-gcc -dumpmachine)-gcc
echo | ${CC} -E -v -x c - |& grep '^Reading specs from' | awk '{print $NF}' | xargs readlink -e | awk -v ORS= '{print $1":"}' | grep "${specdir}/specs:${specdir}/conda.specs:"
cp tests/libhowdy.h $PREFIX/include/
${CC} -shared -fpic -o $PREFIX/lib/libhowdy.so tests/libhowdy.c
${CC} -o howdy-dso tests/howdy-dso.c -lhowdy
./howdy-dso
grep RPATH   <(x86_64-conda-linux-gnu-readelf -d howdy-dso)
! grep RUNPATH <(x86_64-conda-linux-gnu-readelf -d howdy-dso)
${CC} -Wl,-enable-new-dtags -o howdy-dso-runpath tests/howdy-dso.c -lhowdy
./howdy-dso-runpath
! grep RPATH   <(x86_64-conda-linux-gnu-readelf -d howdy-dso-runpath)
grep RUNPATH <(x86_64-conda-linux-gnu-readelf -d howdy-dso-runpath)
echo | ${CC} -E -Wp,-v -x c - |& awk '/include <\.\.\.> search starts/,/^End of search/ {print}' | tail -n2 | head -n1 | grep "$PREFIX/include"
echo | ${CC} -isystem "$PREFIX/include" -E -Wp,-v -x c - |& awk '/include <\.\.\.> search starts/, /^End of search/ {print}' | head -n2 | tail -n1 | grep "$PREFIX/include"
exit 0

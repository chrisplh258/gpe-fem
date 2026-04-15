

set -ex



echo 2.17
test -f ${PREFIX}/lib/gcc/x86_64-conda-linux-gnu/13.4.0/crtbegin.o
test -f ${PREFIX}/lib/gcc/x86_64-conda-linux-gnu/13.4.0/libgcc_eh.a
test -f ${PREFIX}/lib/gcc/x86_64-conda-linux-gnu/13.4.0/libgcc.a
test -f ${PREFIX}/lib/gcc/x86_64-conda-linux-gnu/13.4.0/libgcc_s.so
exit 0

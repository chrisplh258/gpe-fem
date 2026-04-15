

set -ex



echo sysroot
echo 2.17
test -f ${PREFIX}/lib/gcc/x86_64-conda-linux-gnu/13.4.0/libgomp.so
test `readlink ${PREFIX}/lib/gcc/x86_64-conda-linux-gnu/13.4.0/libgomp.so` == "../../../libgomp.so"
test -f ${PREFIX}/bin/x86_64-conda-linux-gnu-gcc
test -f ${PREFIX}/bin/x86_64-conda-linux-gnu-cpp
test ! -f ${PREFIX}/bin/gcc
test ! -f ${PREFIX}/bin/cpp
CC=$(${PREFIX}/bin/*-gcc -dumpmachine)-gcc
${CC} -Wall tests/aligned_alloc.c -c -o c_aligned.o -v -Wl,-v -march=native
${CC} -Wall tests/aligned_alloc.c -c -o c_aligned.o -v -fsanitize=address
${CC} -Wall tests/aligned_alloc.c -c -o c_aligned.o -v
${CC} -Wall c_aligned.o -o c_aligned -v && ./c_aligned
${CC} -Wall c_aligned.o -o c_aligned -Wl,-rpath,/foo && x86_64-conda-linux-gnu-readelf -d c_aligned | grep RPATH | grep "/foo:${PREFIX}/lib"
${CC} -Wall tests/hello_world.c -c -o hello_world.o -v
${CC} -Wall hello_world.o -o hello_world -v
test -f ${PREFIX}/lib/gcc/x86_64-conda-linux-gnu/13.4.0/libgcc_s.so
test -f ${PREFIX}/lib/gcc/x86_64-conda-linux-gnu/13.4.0/libsanitizer.spec
test -f ${PREFIX}/lib/gcc/x86_64-conda-linux-gnu/13.4.0/libasan_preinit.o
test -f ${PREFIX}/lib/gcc/x86_64-conda-linux-gnu/13.4.0/libgomp.spec
exit 0

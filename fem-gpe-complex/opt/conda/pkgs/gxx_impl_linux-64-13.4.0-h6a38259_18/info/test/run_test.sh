

set -ex



test -f ${PREFIX}/bin/x86_64-conda-linux-gnu-g++
CXX=$(${PREFIX}/bin/*-gcc -dumpmachine)-g++
${CXX} -Wall tests/aligned_alloc.cpp -c -o cpp_aligned.o --std=c++17
${CXX} -Wall cpp_aligned.o -o cpp_aligned --std=c++17 && ./cpp_aligned
${CXX} -Wall tests/hello_world.cpp -c -o hello_world.o --std=c++17 -v
${CXX} -Wall hello_world.o -o hello_world --std=c++17 -v
exit 0

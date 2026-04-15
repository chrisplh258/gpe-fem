

set -ex



test -f ${PREFIX}/lib/gcc/x86_64-conda-linux-gnu/13.4.0/libstdc++.a
test -f ${PREFIX}/lib/gcc/x86_64-conda-linux-gnu/13.4.0/libstdc++fs.a
test -f ${PREFIX}/lib/gcc/x86_64-conda-linux-gnu/13.4.0/libsupc++.a
test -f ${PREFIX}/lib/gcc/x86_64-conda-linux-gnu/13.4.0/include/c++/cstdio
test -f ${PREFIX}/lib/gcc/x86_64-conda-linux-gnu/13.4.0/libstdc++.so
exit 0



set -ex



test -f $PREFIX/x86_64-conda-linux-gnu/sysroot/lib/libc.so.6
test -f $PREFIX/x86_64-conda-linux-gnu/sysroot/sbin/ldconfig
test -f $PREFIX/x86_64-conda-linux-gnu/sysroot/usr/lib/crt1.o
test -f $PREFIX/x86_64-conda-linux-gnu/sysroot/usr/include/limits.h
test -f $PREFIX/x86_64-conda-linux-gnu/sysroot/usr/include/gnu/stubs-64.h
test -d $PREFIX/x86_64-conda-linux-gnu/sysroot/usr/share/locale
test -f $PREFIX/x86_64-conda-linux-gnu/sysroot/usr/bin/ldd
test -f $PREFIX/x86_64-conda-linux-gnu/sysroot/lib/libc.so.6
find "${PREFIX}" \( -name 'libnsl*' -o -path '*/rpcsvc/yp*' \) | { ! grep . ; }
find "${PREFIX}" \( -name 'libcrypt*' -o -name 'crypt.*' \) | { ! grep . ; }
exit 0

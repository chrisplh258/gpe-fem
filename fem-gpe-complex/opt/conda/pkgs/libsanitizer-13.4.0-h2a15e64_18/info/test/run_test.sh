

set -ex



test -f ${PREFIX}/lib/libasan.so
test -f ${PREFIX}/lib/libhwasan.so
file ${PREFIX}/bin/x86_64-conda-linux-gnu-gcc
echo 'void main(){}' | x86_64-conda-linux-gnu-gcc -fsanitize=address -Wl,--fatal-warnings -x c -
exit 0

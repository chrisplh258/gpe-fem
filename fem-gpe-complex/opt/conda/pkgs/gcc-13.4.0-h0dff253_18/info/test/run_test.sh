

set -ex



echo "int main (void) {return 0;}" > conftest.c
${PREFIX}/bin/gcc -v
${PREFIX}/bin/gcc conftest.c -c -v
${PREFIX}/bin/gcov -v
exit 0

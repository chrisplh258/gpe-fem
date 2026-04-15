

set -ex



test -f ${PREFIX}/lib/libtheora.a
test -f ${PREFIX}/lib/libtheora.so
test -f ${PREFIX}/lib/libtheoradec.a
test -f ${PREFIX}/lib/libtheoradec.so
test -f ${PREFIX}/lib/libtheoraenc.a
test -f ${PREFIX}/lib/libtheoraenc.so
exit 0

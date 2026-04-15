

set -ex



${PREFIX}/bin/freetype-config --version
test -f ${PREFIX}/lib/libfreetype.so
test -f ${PREFIX}/lib/libfreetype.so.6
test -f ${PREFIX}/lib/libfreetype.so.6.20.6
test -f ${PREFIX}/include/freetype2/freetype/freetype.h
test -f ${PREFIX}/lib/pkgconfig/freetype2.pc
test -f ${PREFIX}/bin/freetype-config
test ! -f ${PREFIX}/lib/libfreetype.a
exit 0



set -ex



test -f $PREFIX/include/ntlm.h
test -f $PREFIX/lib/libntlm.a
test -f $PREFIX/lib/libntlm.so
test -f $PREFIX/lib/pkgconfig/libntlm.pc
exit 0

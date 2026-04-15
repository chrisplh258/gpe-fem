

set -ex



test -f $PREFIX/include/HYPRE.h
test -f $PREFIX/lib/libHYPRE.so
exit 0

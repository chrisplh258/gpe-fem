

set -ex



test -f ${PREFIX}/lib/libGLU.a
test -f ${PREFIX}/lib/libGLU${SHLIB_EXT}
exit 0

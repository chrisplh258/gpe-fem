

set -ex



test -f ${PREFIX}/include/xf86drm.h
test -f ${PREFIX}/include/xf86drmMode.h
test -f ${PREFIX}/include/libsync.h
test -d ${PREFIX}/include/libdrm
test -f ${PREFIX}/lib/libdrm.so
test -f ${PREFIX}/lib/libdrm.so.2
test -f ${PREFIX}/include/libdrm/intel_bufmgr.h
exit 0

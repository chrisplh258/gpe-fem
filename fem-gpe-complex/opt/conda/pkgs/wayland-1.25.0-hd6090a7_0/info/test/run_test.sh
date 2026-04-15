

set -ex



wayland-scanner --help
test -f ${PREFIX}/lib/libwayland-egl.so
test -f ${PREFIX}/lib/libwayland-client.so
test -f ${PREFIX}/lib/libwayland-cursor.so
test -f ${PREFIX}/lib/libwayland-server.so
test -f ${PREFIX}/lib/pkgconfig/wayland-egl.pc
test -f ${PREFIX}/lib/pkgconfig/wayland-client.pc
test -f ${PREFIX}/lib/pkgconfig/wayland-cursor.pc
test -f ${PREFIX}/lib/pkgconfig/wayland-server.pc
test -f ${PREFIX}/include/wayland-egl.h
test -f ${PREFIX}/include/wayland-client.h
test -f ${PREFIX}/include/wayland-cursor.h
test -f ${PREFIX}/include/wayland-server.h
exit 0

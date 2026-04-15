

set -ex



pip check
test $(pip list | grep vtk | tr -s " " | grep $PKG_VERSION | wc -l) -eq 1
test -f $PREFIX/lib/libvtkGUISupportQt-9.3${SHLIB_EXT}
test -f $PREFIX/lib/libvtkRenderingQt-9.3${SHLIB_EXT}
exit 0

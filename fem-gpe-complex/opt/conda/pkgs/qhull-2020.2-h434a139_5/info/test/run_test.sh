

set -ex



test ! -f $PREFIX/lib/libqhullcpp.a
test ! -f $PREFIX/lib/libqhullstatic.a
test ! -f $PREFIX/lib/libqhullstatic_r.a
test -f $PREFIX/lib/libqhull_r${SHLIB_EXT}
rbox c P0 D2 | qvoronoi s o
rbox c | qconvex FQ FV n | qhalf Fp
rbox 1000 D3 | qhull C-1e-4 FO Ts
exit 0

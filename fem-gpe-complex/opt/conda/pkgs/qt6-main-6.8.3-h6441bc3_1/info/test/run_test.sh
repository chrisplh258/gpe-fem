#!/bin/bash

set -ex


# If qt6.conf is not part of the package, it won't work when installed side by side with Qt5.
# See https://github.com/conda-forge/qt-main-feedstock/issues/99
test -f ${PREFIX}/bin/qt6.conf

test "${HOST}" = "aarch64-conda-linux-gnu" && exit 0

ls
cd test
cmake .
make
ctest --output-on-failure
make clean


set -ex



test -d $PREFIX/include/qt6/QtCore
test -f $PREFIX/lib/libQt6Core${SHLIB_EXT}
test -d $PREFIX/include/qt6/QtGui
test -f $PREFIX/lib/libQt6Gui${SHLIB_EXT}
test -d $PREFIX/include/qt6/QtNetwork
test -f $PREFIX/lib/libQt6Network${SHLIB_EXT}
test -d $PREFIX/include/qt6/QtOpenGL
test -f $PREFIX/lib/libQt6OpenGL${SHLIB_EXT}
test -d $PREFIX/include/qt6/QtOpenGLWidgets
test -f $PREFIX/lib/libQt6OpenGLWidgets${SHLIB_EXT}
test -d $PREFIX/include/qt6/QtPrintSupport
test -f $PREFIX/lib/libQt6PrintSupport${SHLIB_EXT}
test -d $PREFIX/include/qt6/QtShaderTools
test -f $PREFIX/lib/libQt6ShaderTools${SHLIB_EXT}
test -d $PREFIX/include/qt6/QtSvg
test -f $PREFIX/lib/libQt6Svg${SHLIB_EXT}
test -d $PREFIX/include/qt6/QtTest
test -f $PREFIX/lib/libQt6Test${SHLIB_EXT}
test -d $PREFIX/include/qt6/QtQml
test -f $PREFIX/lib/libQt6Qml${SHLIB_EXT}
test -d $PREFIX/include/qt6/QtQuick
test -f $PREFIX/lib/libQt6Quick${SHLIB_EXT}
test -d $PREFIX/include/qt6/QtWidgets
test -f $PREFIX/lib/libQt6Widgets${SHLIB_EXT}
test -d $PREFIX/include/qt6/QtXml
test -f $PREFIX/lib/libQt6Xml${SHLIB_EXT}
test -f $PREFIX/lib/qt6/plugins/platforms/libqxcb.so
test -f $PREFIX/lib/qt6/plugins/platforms/libqeglfs.so
test -f $PREFIX/lib/qt6/plugins/sqldrivers/libqsqlite${SHLIB_EXT}
test -f $PREFIX/lib/qt6/plugins/imageformats/libqtiff${SHLIB_EXT}
test ! -f $PREFIX/lib/libQt6WaylandClient${SHLIB_EXT}
test ! -f $PREFIX/lib/libQt6WaylandCompositor${SHLIB_EXT}
qmake6 --version
exit 0

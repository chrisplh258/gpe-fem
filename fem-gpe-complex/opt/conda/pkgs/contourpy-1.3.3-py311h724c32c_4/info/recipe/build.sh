#!/bin/bash
set -ex

echo $MESON_ARGS

if [[ -f "$BUILD_PREFIX/meson_cross_file.txt" ]];
then
    # HACK: extend meson_cross_file to use host python;
    # requires that [binaries] section is last in meson_cross_file
    echo "python = '${PREFIX}/bin/python'" >> $BUILD_PREFIX/meson_cross_file.txt
    cat $BUILD_PREFIX/meson_cross_file.txt
fi

$PYTHON -m pip install . -vv --no-build-isolation --no-deps \
    -Cbuilddir=builddir \
    -Csetup-args=${MESON_ARGS// / -Csetup-args=} \
    || (cat builddir/meson-logs/meson-log.txt && exit 1)

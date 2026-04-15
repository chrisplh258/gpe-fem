set -ex

meson setup builddir ${MESON_ARGS} -Dintel=enabled

meson install -C builddir

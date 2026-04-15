# Get an updated config.sub and config.guess
cp $BUILD_PREFIX/share/gnuconfig/config.* ./build
cp $BUILD_PREFIX/share/gnuconfig/config.* ./contrib/ldapc++
set -x
# export CPPFLAGS="${CPPFLAGS} -isystem $PREFIX/include "
export ac_cv_func_memcmp_working=yes

# disable server components
./configure \
    --prefix=$PREFIX  \
    --disable-slapd \
    --disable-slurpd \
    --with-yielding_select=yes || { cat config.log; exit 1; }
make -j${CPU_COUNT}
make install

#!/bin/bash
set -x

# ++awful .. broken configure script here, it does not look in include/openssl
# cp -f ${PREFIX}/include/openssl/des.h ${PREFIX}/include

if [[ ${target_platform} == osx-* ]]; then
  DISABLE_MACOS_FRAMEWORK=--disable-macos-framework
fi

if [[ ${target_platform} =~ .*ppc.* ]]; then
  # We should probably run autoreconf here instead, but I am tired of this software.
  BUILD_FLAG="--build=${HOST}"
  GSSAPI="--disable-gssapi"
  if [[ 0 == 1 ]]; then
    echo libtoolize
    libtoolize
    echo aclocal -I cmulocal -I config
    aclocal -I cmulocal -I config
    echo autoheader
    autoheader
    echo autoconf
    autoconf
    echo automake --add-missing --include-deps
    automake --add-missing --include-deps
  fi
fi

# Cyrus sasl REALLY wants something called gcc to exist.  Desperately
ln -s ${CC} ${BUILD_PREFIX}/bin/gcc

autoreconf -vfi
# --disable-dependency-tracking works around:
# https://forums.gentoo.org/viewtopic-t-366917-start-0.html
./configure --prefix=${PREFIX}                    \
            --host=${HOST}                        \
            ${BUILD_FLAG}                         \
            ${GSSAPI}                             \
            --enable-digest                       \
            --with-des=${PREFIX}                  \
            --with-plugindir=${PREFIX}/lib/sasl2  \
            --with-configdir=${PREFIX}/etc/sasl2  \
            --with-openssl=${PREFIX}              \
            --disable-dependency-tracking         \
            ${DISABLE_MACOS_FRAMEWORK} || { cat config.log; exit 1; }
cat config.log
# Parallel builds fail frequently.
make -j1 ${VERBOSE_AT}
make install

# awful--
rm -f ${PREFIX}/include/des.h

# ++awful
if [[ ${target_platform} == osx-* ]]; then
  # Some older versions of sasl had strange names.
  if [ -f ${PREFIX}/sbin/${HOST}-pluginviewer ]; then
    mv ${PREFIX}/sbin/${HOST}-pluginviewer ${PREFIX}/sbin/pluginviewer
  fi
  if [ -f ${PREFIX}/sbin/${HOST}-pluginviewer ]; then
    mv ${PREFIX}/sbin/${HOST}-saslpasswd2 ${PREFIX}/sbin/saslpasswd2
  fi
  if [ -f ${PREFIX}/sbin/${HOST}-sasldblistusers2 ]; then
    mv ${PREFIX}/sbin/${HOST}-sasldblistusers2 ${PREFIX}/sbin/sasldblistusers2
  fi
  ${INSTALL_NAME_TOOL:-install_name_tool} -id @rpath/libsasl2.dylib ${PREFIX}/lib/libsasl2.dylib
  ${INSTALL_NAME_TOOL:-install_name_tool} -change /libsasl2.dylib @rpath/libsasl2.dylib ${PREFIX}/sbin/pluginviewer
  ${INSTALL_NAME_TOOL:-install_name_tool} -change /libsasl2.dylib ${PREFIX}/lib/libsasl2.dylib ${PREFIX}/sbin/saslpasswd2
  ${INSTALL_NAME_TOOL:-install_name_tool} -change /libsasl2.dylib ${PREFIX}/lib/libsasl2.dylib ${PREFIX}/sbin/sasldblistusers2
fi

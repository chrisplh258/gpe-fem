



test -f $PREFIX/x86_64-conda-linux-gnu/sysroot/lib/libc.so.6
IF %ERRORLEVEL% NEQ 0 exit /B 1
test -f $PREFIX/x86_64-conda-linux-gnu/sysroot/sbin/ldconfig
IF %ERRORLEVEL% NEQ 0 exit /B 1
test -f $PREFIX/x86_64-conda-linux-gnu/sysroot/usr/lib/crt1.o
IF %ERRORLEVEL% NEQ 0 exit /B 1
test -f $PREFIX/x86_64-conda-linux-gnu/sysroot/usr/include/limits.h
IF %ERRORLEVEL% NEQ 0 exit /B 1
test -f $PREFIX/x86_64-conda-linux-gnu/sysroot/usr/include/gnu/stubs-64.h
IF %ERRORLEVEL% NEQ 0 exit /B 1
test -d $PREFIX/x86_64-conda-linux-gnu/sysroot/usr/share/locale
IF %ERRORLEVEL% NEQ 0 exit /B 1
test -f $PREFIX/x86_64-conda-linux-gnu/sysroot/usr/bin/ldd
IF %ERRORLEVEL% NEQ 0 exit /B 1
test -f $PREFIX/x86_64-conda-linux-gnu/sysroot/lib/libc.so.6
IF %ERRORLEVEL% NEQ 0 exit /B 1
find "${PREFIX}" \( -name 'libnsl*' -o -path '*/rpcsvc/yp*' \) | { ! grep . ; }
IF %ERRORLEVEL% NEQ 0 exit /B 1
find "${PREFIX}" \( -name 'libcrypt*' -o -name 'crypt.*' \) | { ! grep . ; }
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0





test -f $PREFIX/x86_64-conda-linux-gnu/sysroot/usr/include/linux/version.h
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0

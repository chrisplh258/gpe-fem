



test -f ${PREFIX}/include/ufcx.h
IF %ERRORLEVEL% NEQ 0 exit /B 1
pkg-config --cflags ufcx
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0

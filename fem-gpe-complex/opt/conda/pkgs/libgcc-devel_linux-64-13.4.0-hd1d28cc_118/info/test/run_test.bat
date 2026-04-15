

@echo on

echo 2.17
IF %ERRORLEVEL% NEQ 0 exit /B 1
test -f ${PREFIX}/lib/gcc/x86_64-conda-linux-gnu/13.4.0/crtbegin.o
IF %ERRORLEVEL% NEQ 0 exit /B 1
test -f ${PREFIX}/lib/gcc/x86_64-conda-linux-gnu/13.4.0/libgcc_eh.a
IF %ERRORLEVEL% NEQ 0 exit /B 1
test -f ${PREFIX}/lib/gcc/x86_64-conda-linux-gnu/13.4.0/libgcc.a
IF %ERRORLEVEL% NEQ 0 exit /B 1
test -f ${PREFIX}/lib/gcc/x86_64-conda-linux-gnu/13.4.0/libgcc_s.so
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0

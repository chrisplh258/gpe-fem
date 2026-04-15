

@echo on

test -f ${PREFIX}/lib/gcc/x86_64-conda-linux-gnu/13.4.0/libstdc++.a
IF %ERRORLEVEL% NEQ 0 exit /B 1
test -f ${PREFIX}/lib/gcc/x86_64-conda-linux-gnu/13.4.0/libstdc++fs.a
IF %ERRORLEVEL% NEQ 0 exit /B 1
test -f ${PREFIX}/lib/gcc/x86_64-conda-linux-gnu/13.4.0/libsupc++.a
IF %ERRORLEVEL% NEQ 0 exit /B 1
test -f ${PREFIX}/lib/gcc/x86_64-conda-linux-gnu/13.4.0/include/c++/cstdio
IF %ERRORLEVEL% NEQ 0 exit /B 1
test -f ${PREFIX}/lib/gcc/x86_64-conda-linux-gnu/13.4.0/libstdc++.so
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0

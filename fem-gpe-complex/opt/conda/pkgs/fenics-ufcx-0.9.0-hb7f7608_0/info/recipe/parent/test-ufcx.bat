setlocal EnableDelayedExpansion

cmake -G "NMake Makefiles" ^
  -B build-dir ^
  -DCMAKE_BUILD_TYPE=Release ^
  -DCMAKE_INSTALL_PREFIX="%PREFIX%" ^
  -DCMAKE_PREFIX_PATH:PATH="%LIBRARY_PREFIX%" ^
  test-ufcx

if errorlevel 1 exit 1

cmake --build build-dir --verbose
if errorlevel 1 exit 1

cmake --install build-dir
if errorlevel 1 exit 1

test-ufcx
if errorlevel 1 exit 1

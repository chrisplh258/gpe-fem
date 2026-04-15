setlocal EnableDelayedExpansion

cd cpp

:: Make a build folder and change to it.
mkdir build
cd build

cmake -G "NMake Makefiles" ^
      -DCMAKE_INSTALL_PREFIX:PATH="%LIBRARY_PREFIX%" ^
      -DCMAKE_PREFIX_PATH:PATH="%LIBRARY_PREFIX%" ^
      %CMAKE_ARGS% ^
      ..
if errorlevel 1 exit 1

cmake --build . --verbose
if errorlevel 1 exit 1

cmake --install . --verbose
if errorlevel 1 exit 1

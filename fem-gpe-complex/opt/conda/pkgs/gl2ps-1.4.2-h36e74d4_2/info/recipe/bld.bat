@echo on

cmake -GNinja ^
    -DCMAKE_POLICY_VERSION_MINIMUM=3.5 ^
    -DCMAKE_BUILD_TYPE=Release ^
    %CMAKE_ARGS% ^
    -S source -B build
if errorlevel 1 exit 1

cmake --build build --target install
if errorlevel 1 exit 1



set -ex



test -d $PREFIX/lib/cmake/Boost-1.86.0
test -d $PREFIX/lib/cmake/boost_atomic-1.86.0
test -d $PREFIX/lib/cmake/boost_charconv-1.86.0
test -d $PREFIX/lib/cmake/boost_chrono-1.86.0
test -d $PREFIX/lib/cmake/boost_cobalt-1.86.0
test -d $PREFIX/lib/cmake/boost_container-1.86.0
test -d $PREFIX/lib/cmake/boost_context-1.86.0
test -d $PREFIX/lib/cmake/boost_contract-1.86.0
test -d $PREFIX/lib/cmake/boost_coroutine-1.86.0
test -d $PREFIX/lib/cmake/boost_date_time-1.86.0
test -d $PREFIX/lib/cmake/boost_filesystem-1.86.0
test -d $PREFIX/lib/cmake/boost_graph-1.86.0
test -d $PREFIX/lib/cmake/boost_iostreams-1.86.0
test -d $PREFIX/lib/cmake/boost_locale-1.86.0
test -d $PREFIX/lib/cmake/boost_log-1.86.0
test -d $PREFIX/lib/cmake/boost_log_setup-1.86.0
test -d $PREFIX/lib/cmake/boost_math_c99-1.86.0
test -d $PREFIX/lib/cmake/boost_math_c99f-1.86.0
test -d $PREFIX/lib/cmake/boost_math_tr1-1.86.0
test -d $PREFIX/lib/cmake/boost_math_tr1f-1.86.0
test -d $PREFIX/lib/cmake/boost_prg_exec_monitor-1.86.0
test -d $PREFIX/lib/cmake/boost_program_options-1.86.0
test -d $PREFIX/lib/cmake/boost_random-1.86.0
test -d $PREFIX/lib/cmake/boost_regex-1.86.0
test -d $PREFIX/lib/cmake/boost_serialization-1.86.0
test -d $PREFIX/lib/cmake/boost_system-1.86.0
test -d $PREFIX/lib/cmake/boost_thread-1.86.0
test -d $PREFIX/lib/cmake/boost_timer-1.86.0
test -d $PREFIX/lib/cmake/boost_type_erasure-1.86.0
test -d $PREFIX/lib/cmake/boost_unit_test_framework-1.86.0
test -d $PREFIX/lib/cmake/boost_wave-1.86.0
test -d $PREFIX/lib/cmake/boost_wserialization-1.86.0
test -d $PREFIX/lib/cmake/boost_math_c99l-1.86.0
test -d $PREFIX/lib/cmake/boost_math_tr1l-1.86.0
test -d $PREFIX/lib/cmake/boost_exception-1.86.0
test -d $PREFIX/lib/cmake/boost_test_exec_monitor-1.86.0
test ! -d $PREFIX/lib/cmake/boost_python-1.86.0
test ! -d $PREFIX/lib/cmake/boost_numpy-1.86.0
./test_lib.sh
exit 0

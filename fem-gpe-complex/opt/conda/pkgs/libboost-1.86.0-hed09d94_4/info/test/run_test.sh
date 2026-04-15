

set -ex



test ! -d $PREFIX/include/boost
test ! -d $PREFIX/lib/cmake/Boost-1.86.0
test -f $PREFIX/lib/libboost_atomic.so
test ! -f $PREFIX/lib/libboost_atomic.a
test ! -d $PREFIX/lib/cmake/boost_atomic-1.86.0
test -f $PREFIX/lib/libboost_charconv.so
test ! -f $PREFIX/lib/libboost_charconv.a
test ! -d $PREFIX/lib/cmake/boost_charconv-1.86.0
test -f $PREFIX/lib/libboost_chrono.so
test ! -f $PREFIX/lib/libboost_chrono.a
test ! -d $PREFIX/lib/cmake/boost_chrono-1.86.0
test -f $PREFIX/lib/libboost_cobalt.so
test ! -f $PREFIX/lib/libboost_cobalt.a
test ! -d $PREFIX/lib/cmake/boost_cobalt-1.86.0
test -f $PREFIX/lib/libboost_container.so
test ! -f $PREFIX/lib/libboost_container.a
test ! -d $PREFIX/lib/cmake/boost_container-1.86.0
test -f $PREFIX/lib/libboost_context.so
test ! -f $PREFIX/lib/libboost_context.a
test ! -d $PREFIX/lib/cmake/boost_context-1.86.0
test -f $PREFIX/lib/libboost_contract.so
test ! -f $PREFIX/lib/libboost_contract.a
test ! -d $PREFIX/lib/cmake/boost_contract-1.86.0
test -f $PREFIX/lib/libboost_coroutine.so
test ! -f $PREFIX/lib/libboost_coroutine.a
test ! -d $PREFIX/lib/cmake/boost_coroutine-1.86.0
test -f $PREFIX/lib/libboost_date_time.so
test ! -f $PREFIX/lib/libboost_date_time.a
test ! -d $PREFIX/lib/cmake/boost_date_time-1.86.0
test -f $PREFIX/lib/libboost_filesystem.so
test ! -f $PREFIX/lib/libboost_filesystem.a
test ! -d $PREFIX/lib/cmake/boost_filesystem-1.86.0
test -f $PREFIX/lib/libboost_graph.so
test ! -f $PREFIX/lib/libboost_graph.a
test ! -d $PREFIX/lib/cmake/boost_graph-1.86.0
test -f $PREFIX/lib/libboost_iostreams.so
test ! -f $PREFIX/lib/libboost_iostreams.a
test ! -d $PREFIX/lib/cmake/boost_iostreams-1.86.0
test -f $PREFIX/lib/libboost_locale.so
test ! -f $PREFIX/lib/libboost_locale.a
test ! -d $PREFIX/lib/cmake/boost_locale-1.86.0
test -f $PREFIX/lib/libboost_log.so
test ! -f $PREFIX/lib/libboost_log.a
test ! -d $PREFIX/lib/cmake/boost_log-1.86.0
test -f $PREFIX/lib/libboost_log_setup.so
test ! -f $PREFIX/lib/libboost_log_setup.a
test ! -d $PREFIX/lib/cmake/boost_log_setup-1.86.0
test -f $PREFIX/lib/libboost_math_c99.so
test ! -f $PREFIX/lib/libboost_math_c99.a
test ! -d $PREFIX/lib/cmake/boost_math_c99-1.86.0
test -f $PREFIX/lib/libboost_math_c99f.so
test ! -f $PREFIX/lib/libboost_math_c99f.a
test ! -d $PREFIX/lib/cmake/boost_math_c99f-1.86.0
test -f $PREFIX/lib/libboost_math_tr1.so
test ! -f $PREFIX/lib/libboost_math_tr1.a
test ! -d $PREFIX/lib/cmake/boost_math_tr1-1.86.0
test -f $PREFIX/lib/libboost_math_tr1f.so
test ! -f $PREFIX/lib/libboost_math_tr1f.a
test ! -d $PREFIX/lib/cmake/boost_math_tr1f-1.86.0
test -f $PREFIX/lib/libboost_prg_exec_monitor.so
test ! -f $PREFIX/lib/libboost_prg_exec_monitor.a
test ! -d $PREFIX/lib/cmake/boost_prg_exec_monitor-1.86.0
test -f $PREFIX/lib/libboost_program_options.so
test ! -f $PREFIX/lib/libboost_program_options.a
test ! -d $PREFIX/lib/cmake/boost_program_options-1.86.0
test -f $PREFIX/lib/libboost_random.so
test ! -f $PREFIX/lib/libboost_random.a
test ! -d $PREFIX/lib/cmake/boost_random-1.86.0
test -f $PREFIX/lib/libboost_regex.so
test ! -f $PREFIX/lib/libboost_regex.a
test ! -d $PREFIX/lib/cmake/boost_regex-1.86.0
test -f $PREFIX/lib/libboost_serialization.so
test ! -f $PREFIX/lib/libboost_serialization.a
test ! -d $PREFIX/lib/cmake/boost_serialization-1.86.0
test -f $PREFIX/lib/libboost_system.so
test ! -f $PREFIX/lib/libboost_system.a
test ! -d $PREFIX/lib/cmake/boost_system-1.86.0
test -f $PREFIX/lib/libboost_thread.so
test ! -f $PREFIX/lib/libboost_thread.a
test ! -d $PREFIX/lib/cmake/boost_thread-1.86.0
test -f $PREFIX/lib/libboost_timer.so
test ! -f $PREFIX/lib/libboost_timer.a
test ! -d $PREFIX/lib/cmake/boost_timer-1.86.0
test -f $PREFIX/lib/libboost_type_erasure.so
test ! -f $PREFIX/lib/libboost_type_erasure.a
test ! -d $PREFIX/lib/cmake/boost_type_erasure-1.86.0
test -f $PREFIX/lib/libboost_unit_test_framework.so
test ! -f $PREFIX/lib/libboost_unit_test_framework.a
test ! -d $PREFIX/lib/cmake/boost_unit_test_framework-1.86.0
test -f $PREFIX/lib/libboost_wave.so
test ! -f $PREFIX/lib/libboost_wave.a
test ! -d $PREFIX/lib/cmake/boost_wave-1.86.0
test -f $PREFIX/lib/libboost_wserialization.so
test ! -f $PREFIX/lib/libboost_wserialization.a
test ! -d $PREFIX/lib/cmake/boost_wserialization-1.86.0
test -f $PREFIX/lib/libboost_math_c99l.so
test ! -f $PREFIX/lib/libboost_math_c99l.a
test ! -d $PREFIX/lib/cmake/boost_math_c99l-1.86.0
test -f $PREFIX/lib/libboost_math_tr1l.so
test ! -f $PREFIX/lib/libboost_math_tr1l.a
test ! -d $PREFIX/lib/cmake/boost_math_tr1l-1.86.0
test ! -f $PREFIX/lib/libboost_exception.so
test -f $PREFIX/lib/libboost_exception.a
test ! -d $PREFIX/lib/cmake/boost_exception-1.86.0
test ! -f $PREFIX/lib/libboost_test_exec_monitor.so
test -f $PREFIX/lib/libboost_test_exec_monitor.a
test ! -d $PREFIX/lib/cmake/boost_test_exec_monitor-1.86.0
test ! -f $PREFIX/lib/libboost_python310.so
test ! -f $PREFIX/lib/libboost_python310.a
test ! -d $PREFIX/lib/cmake/boost_python310-1.86.0
test ! -f $PREFIX/lib/libboost_numpy310.so
test ! -f $PREFIX/lib/libboost_numpy310.a
test ! -d $PREFIX/lib/cmake/boost_numpy310-1.86.0
exit 0

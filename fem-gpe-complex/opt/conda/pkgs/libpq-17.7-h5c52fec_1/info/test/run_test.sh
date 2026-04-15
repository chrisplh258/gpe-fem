

set -ex



pg_config
test -f $PREFIX/lib/libpq.so.5.17
test -f $PREFIX/lib/libpq.so.5
test -f $PREFIX/lib/libpq.so
exit 0

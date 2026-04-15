

set -ex



test -f $PREFIX/share/mysql/english/errmsg.sys
test -f $PREFIX/share/mysql/charsets/ascii.xml
exit 0

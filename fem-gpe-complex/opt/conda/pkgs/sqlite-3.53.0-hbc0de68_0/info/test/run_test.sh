

set -ex



sqlite3 --version
echo "PRAGMA compile_options;" | sqlite3
exit 0



set -ex



py.test tests --c-extensions
pip check
exit 0



set -ex



pip check
pytest -v test/test_create.py
exit 0

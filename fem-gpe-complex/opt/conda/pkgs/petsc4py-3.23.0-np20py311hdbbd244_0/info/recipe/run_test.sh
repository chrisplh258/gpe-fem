# aarch64 failing tests
# /lib64/libm.so.6: version `GLIBC_2.27' not found
if [[ "$target_platform" == linux-aarch64 && "$device" != host ]]; then
  echo "skipping test"
else
  python -c "import petsc4py"
  python -c "import petsc4py.PETSc"
fi

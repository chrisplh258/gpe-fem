export HYDRA_LAUNCHER=fork
export OMPI_MCA_plm=isolated
export OMPI_MCA_rmaps_base_oversubscribe=yes
export OMPI_MCA_btl_vader_single_copy_mechanism=none

# aarch64 failing tests
# /lib64/libm.so.6: version `GLIBC_2.27' not found
if [[ "$target_platform" == linux-aarch64 && "$device" != host ]]; then
  echo "skipping test"
else
  python -c "import slepc4py"
  python -c "import slepc4py.SLEPc"
fi

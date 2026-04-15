#!/bin/sh
#
# This simple script will collect outputs of ibroute for all switches
# on the subnet and drop it on stdout. It can be used for MFTs dump
# generation.
#

/home/conda/feedstock_root/build_artifacts/rdma-core_1769154678374/_h_env_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_placehold_p/sbin/dump_fts -M $@
echo ""
echo "*** WARNING ***: this command has been replaced by dump_fts -M"
echo ""
echo ""

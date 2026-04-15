#!/bin/sh
#
# This simple script will collect outputs of ibroute for all switches
# on the subnet and drop it on stdout. It can be used for LFTs dump
# generation.
#

/opt/conda/envs/fem-gpe/sbin/dump_fts $@
echo ""
echo "*** WARNING ***: this command has been replaced by dump_fts"
echo ""
echo ""

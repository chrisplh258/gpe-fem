#!/bin/bash

cat << EOF >> "${PREFIX}/.messages.txt"

To enable CUDA support, UCX requires the CUDA Runtime library (libcudart).
The library can be installed with the appropriate command below:

* For CUDA 11, run:    conda install cudatoolkit cuda-version=11
* For CUDA 12, run:    conda install cuda-cudart cuda-version=12

If any of the packages you requested use CUDA then CUDA should already
have been installed for you.

EOF

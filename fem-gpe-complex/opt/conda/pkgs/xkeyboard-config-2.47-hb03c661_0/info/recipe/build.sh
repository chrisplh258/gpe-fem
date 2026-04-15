#!/bin/bash
set -ex

meson setup builddir --prefix="${PREFIX}"

cd builddir
meson compile
meson test
meson  install

#!/usr/bin/env bash

set -ex

mkdir forgebuild

meson_config_args=(
    -Dmode=release
    -Dsplit-bin=false
    -Dsysconfdir=etc
    -Dsysvinit-path=""
    -Dversion-tag=condaforge
    # general toggles
    -Dcreate-log-dirs=false
    -Dinstall-sysconfdir=false
    -Dtests=false
    # component toggles
    -Danalyze=false
    -Dbacklight=false
    -Dbinfmt=false
    -Dbpf-framework=disabled
    -Dcoredump=false
    -Defi=false
    -Denvironment-d=false
    -Dfirstboot=false
    -Dhibernate=false
    -Dhomed=disabled
    -Dhostnamed=false
    -Dhwdb=false
    -Dimportd=disabled
    -Dinitrd=false
    -Dkernel-install=false
    -Dlocaled=false
    -Dlogind=false
    -Dmachined=false
    -Dmountfsd=false
    -Dnetworkd=false
    -Dnsresourced=false
    -Dnss-myhostname=false
    -Dnss-mymachines=disabled
    -Dnss-resolve=disabled
    -Dnss-systemd=false
    -Doomd=false
    -Dportabled=false
    -Dpstore=false
    -Dquotacheck=false
    -Drandomseed=False
    -Drepart=disabled
    -Dresolve=false
    -Drfkill=false
    -Dsysext=false
    -Dsysusers=false
    -Dtimedated=false
    -Dtimesyncd=false
    -Dtmpfiles=false
    -Duserdb=false
    -Dvconsole=false
    -Dxdg-autostart=false
)

# Set DESTDIR so that the installation knows that we are packaging for a
# distribution and not installing to the local machine, but actual destination
# is still handled by setting the prefix/rootprefix.
# This avoids doing things like building the catalog database under /var
export DESTDIR="/"

meson setup forgebuild \
    ${MESON_ARGS} \
    "${meson_config_args[@]}" \
    --wrap-mode=nofallback
meson compile -v -C forgebuild -j ${CPU_COUNT}
meson install -C forgebuild --no-rebuild

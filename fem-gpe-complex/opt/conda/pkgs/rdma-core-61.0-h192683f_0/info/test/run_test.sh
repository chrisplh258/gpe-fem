

set -ex



test -f "${PREFIX}/bin/ibv_devices"
${PREFIX}/bin/ibv_devices
exit 0

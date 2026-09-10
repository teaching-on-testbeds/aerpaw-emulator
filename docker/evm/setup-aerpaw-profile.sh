#!/usr/bin/env bash
set -Eeuo pipefail

node_id=${NODE_ID:-0}
vehicle=${AP_EXPENV_THIS_CONTAINER_NODE_VEHICLE:-NONE}
vehicle_name=${vehicle#vehicle_}
cvm_service=${CVM_SERVICE:-node${node_id}-${vehicle_name}-cvm}
evm_address=$(hostname -I | cut -d ' ' -f 1)
cvm_address=$(getent hosts "$cvm_service" | cut -d ' ' -f 1 || true)
cvm_address=${cvm_address:-$cvm_service}

cat > /root/.ap-set-experiment-env.sh <<EOF
#!/usr/bin/env bash
export AP_EXPENV_EXP_NUM=${AP_EXPENV_EXP_NUM:-1}
export AP_EXPENV_NUM_NODES=${AP_EXPENV_NUM_NODES:-1}
export AP_EXPENV_SESSION_ENV=${AP_EXPENV_SESSION_ENV:-Virtual}
export AP_EXPENV_SET_NODES="${AP_EXPENV_SET_NODES:-0}"
export AP_EXPENV_CVM_${node_id}_XE=${cvm_address}
export AP_EXPENV_CVM_${node_id}_XV=NONE
export AP_EXPENV_EVM_${node_id}_XM=${evm_address}
export AP_EXPENV_EVM_${node_id}_XD=NONE
export AP_EXPENV_EVM_${node_id}_XE1=${evm_address}
export AP_EXPENV_EVM_${node_id}_XE2=NONE
export AP_EXPENV_EVM_${node_id}_XV=NONE
export AP_EXPENV_CHEMVM_XE=NONE
export AP_EXPENV_CHEMVM_AD=NONE
export AP_EXPENV_OEOSVM_AD=NONE
export AP_EXPENV_OEOSVM_XW=NONE
export AP_EXPENV_OEOCVM_XW=NONE
export AP_EXPENV_THIS_CONTAINER_ROLE=${AP_EXPENV_THIS_CONTAINER_ROLE:-E-VM}
export AP_EXPENV_THIS_CONTAINER_EXP_NODE_NUM=${AP_EXPENV_THIS_CONTAINER_EXP_NODE_NUM:-${node_id}}
export AP_EXPENV_THIS_CONTAINER_NAME=${AP_EXPENV_THIS_CONTAINER_NAME:-E-VM}
export AP_EXPENV_THIS_CONTAINER_NODE_TYPE=${AP_EXPENV_THIS_CONTAINER_NODE_TYPE:-Portable}
export AP_EXPENV_THIS_CONTAINER_NODE_AHN_NUM=${AP_EXPENV_THIS_CONTAINER_NODE_AHN_NUM:-NONE}
export AP_EXPENV_THIS_CONTAINER_NODE_VEHICLE=${vehicle}
export AP_EXPENV_THIS_CONTAINER_NODE_UHD=${AP_EXPENV_THIS_CONTAINER_NODE_UHD:-NONE}
EOF
chmod 0644 /root/.ap-set-experiment-env.sh

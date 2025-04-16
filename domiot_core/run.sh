#!/usr/bin/with-contenv bashio
echo "SUPERVISOR_TOKEN: ${SUPERVISOR_TOKEN}"

echo "----------------------------------------------------------------------"
echo
curl -sSL -H "Authorization: Bearer $SUPERVISOR_TOKEN" http://supervisor/auth/list
echo
echo "----------------------------------------------------------------------"

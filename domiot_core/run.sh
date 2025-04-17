#!/usr/bin/with-contenv bashio
echo "SUPERVISOR_TOKEN: ${SUPERVISOR_TOKEN}"
echo
echo
ls
echo
echo


echo "----------------------------------------------------------------------"
echo
curl -sSL -H "Authorization: Bearer $SUPERVISOR_TOKEN" http://supervisor/auth/list
echo
echo "----------------------------------------------------------------------"

uvicorn main:app --host 0.0.0.0 --port 8888
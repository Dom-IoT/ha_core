#!/usr/bin/with-contenv bashio

set -e

bashio::log.info "Starting DomIoT Core"
echo "Starting DomIoT Core"

cd backend && uvicorn main:app --host 0.0.0.0 --port 8888
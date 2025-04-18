#!/usr/bin/with-contenv bashio

set -e

# Run uvicorn for backend and nginx for frontend
uvicorn main:app --host 0.0.0.0 --port 8099 --log-level debug
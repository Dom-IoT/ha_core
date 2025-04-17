#!/usr/bin/with-contenv bashio

set -e

# Run uvicorn for backend and nginx for frontend
run_backend() {
    pushd backend
    echo "Running backend..."
    univorn main:app --host 0.0.0.0 --port 8888
    popd
}

run_frontend() {
    pushd frontend
    echo "Running frontend..."
    # redirect nginx logs to stdout
    nginx -g 'daemon off; error_log /dev/stdout debug;'
    popd
}
# Run both backend and frontend in the background
run_backend & run_frontend & wait
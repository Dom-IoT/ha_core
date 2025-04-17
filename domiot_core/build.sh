#!/usr/bin/with-contenv bashio

set -e


build_backend() {
    pushd backend
    echo "Building backend..."
    pip3 install --break-system-packages -r requirements.txt
    echo "Running backend..."
    univorn main:app --host 0.0.0.0 --port 8888
    popd
}

build_frontend() {
    pushd frontend
    echo "Building frontend..."
    echo "Running frontend..."
    popd
}

build_backend &
build_frontend &
wait
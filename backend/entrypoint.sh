#!/bin/bash

set -e
echo "Starting backend"
gunicorn app:app -k uvicorn.workers.UvicornWorker --workers 4 --bind unix:/var/run/honeysuckle/uvicorn.sock
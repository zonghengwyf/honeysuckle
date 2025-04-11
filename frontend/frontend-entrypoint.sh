#!/bin/bash

set -e
echo "Starting frontend"
cd $WORK_DIR
if [ "$APP_ENV" = "development" ]; then
    echo "Starting in development ENV..."
    pnpm run dev
else
    echo "Building for production ENV..."
    pnpm run generate
    mkdir -p /var/www/html/
    cp -r .output/public/* /var/www/html/
fi

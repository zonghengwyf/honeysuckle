#!/bin/bash

set -e

cd /etc/nginx/conf.d;
if [ "$APP_ENV" = "development" ]; then
    echo "Nginx Starting in development ENV..."
    [ -f default.conf ] && mv default.conf default.conf.disabled
    [ -f dev.conf.disabled ] && mv dev.conf.disabled dev.conf
else
    echo "Nginx Building for production ENV..."
    [ -f dev.conf ] && mv dev.conf dev.conf.disabled
    [ -f default.conf.disabled ] && mv default.conf.disabled default.conf
fi

nginx -g "daemon off;"
#!/bin/bash

# Create nginx log directories
mkdir -p logs/nginx

# Start nginx
nginx -c ${PWD}/nginxProxy.conf
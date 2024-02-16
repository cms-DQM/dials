#!/bin/bash

docker stop redis_local

docker rm redis_local

docker run -d \
    --restart always \
    --name redis_local \
    -p 6379:6379 \
    redis

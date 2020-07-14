#!/usr/bin/env bash

value=${1:-production}

echo Selected mode: $value

cd ..

if [ "$value" == "production" ];then
    export ENV=prod.env

elif [ "$value" == "dev" ];then
    export ENV=dev.env
fi

docker-compose up -d
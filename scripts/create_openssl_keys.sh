#!/usr/bin/env bash

echo "Check private and public key..."

if [[ ! -f "backup_key.pem" || ! -f "backup_key.pem.pub" ]]; then

  echo "Create public and private key..."

  openssl req -x509 -nodes -days 1000000 -newkey rsa:4096 -keyout backup_key.pem\
 -subj "/C=US/ST=Illinois/L=Chicago/O=IT/CN=api.privet-obed.ru" \
 -out backup_key.pem.pub

 echo "Keys are created, save the private key to decrypt dump";  else echo "The file already exists"
fi


#!/usr/bin/env bash

ssh-keygen -t rsa -b 4096 -C "zakharpetukhov@protonmail.com"
cat ~/.ssh/id_rsa.pub

echo "Paste the above copied output to the form at https://github.com/settings/ssh/new"
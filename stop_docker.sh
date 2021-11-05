#!/bin/bash
cd /home/ec2-user/email_templates
/usr/local/bin/docker-compose down
cp token.json ../

rm -rf *.*
rm -rf .gitignore
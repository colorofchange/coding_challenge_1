#!/bin/bash
cd /home/ec2-user
sudo cp -a stout.colorofchange.org email_templates
sudo cp credentials.json token.json email_templates
cd /home/ec2-user/email_templates
/usr/local/bin/docker-compose up --build -d
cd /home/ec2-user
sudo cp -a stout.colorofchange.org email_templates

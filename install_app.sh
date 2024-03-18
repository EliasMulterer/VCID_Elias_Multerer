#!/bin/bash

sudo apt update


sudo apt install -y python3-pip python3.11-venv

#Script ausführbar machen
chmod +x ./app_start.sh
chmod +x ./app.py
chmod +x ./db.py


python3 -m venv venv
source venv/bin/activate
pip install gunicorn flask
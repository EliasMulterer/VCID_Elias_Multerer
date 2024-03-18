#!/bin/bash

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

#Starten der Applikation via gunicorn über Port 8080
gunicorn -b :8080 app:app &
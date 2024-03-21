#!/bin/bash

python3 -m venv venv
source venv/bin/activate
pip install -r /home/elias_multerer/VCID_Elias_Multerer/requirements.txt

#Starten der Applikation via gunicorn über Port 8080
gunicorn -b :8080 app:app &
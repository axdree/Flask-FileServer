#!/bin/bash
echo Starting Flask example app.
cd /home/azureuser/fileserver
source .venv/bin/activate
cd .venv
gunicorn -w 2 -b 0.0.0.0:443 app:app
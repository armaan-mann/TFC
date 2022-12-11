#!/bin/bash
sudo lsof -t -i tcp:8000 | xargs kill -9
sudo lsof -t -i tcp:3000 | xargs kill -9

cd PB

cd Backend-TFC
python3 -m pip install virtualenv
python3 -m virtualenv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python3 manage.py runserver &


cd ../Frontend_TFC
npm start
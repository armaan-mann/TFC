#!/bin/bash
cd PB

cd Backend-TFC
python3 -m virtualenv venv
python3 -m pip install virtualenv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python3 manage.py runserver --noreload &

cd ../Frontend_TFC
npm run start






@echo off
cd "C:\Users\samrasto\OneDrive - Nokia\Desktop\email forwarding\jobmailer"
call venv\Scripts\activate
python manage.py runserver 127.0.0.1:2712

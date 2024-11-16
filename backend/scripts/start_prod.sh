#!/bin/bash

cd backend
#python3 manage.py makemigrations
#python3 manage.py migrate --no-input
gunicorn dproject.wsgi -b 0.0.0.0:8003
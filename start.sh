#! /usr/bin/env bash

echo "Initialization..."
python ./app/prestart.py

echo "Starting development server..."
exec uvicorn "app.main:app" --reload --host "0.0.0.0" --port 8000 --proxy-headers --workers 4
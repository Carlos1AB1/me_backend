#!/usr/bin/env bash
# Build script for Render

set -o errexit  # Exit on error

pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate

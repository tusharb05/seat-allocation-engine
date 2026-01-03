#!/bin/sh
set -e

# echo "Waiting for Postgres at localhost:6379 ..."

# while ! nc -z "localhost" "6379"; do
#   sleep 1
# done


echo "Starting Booking Service..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
#!/bin/sh
set -e

echo "Waiting for Postgres at $DB_HOST:$DB_PORT..."

while ! nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 1
done

echo "Postgres is up."

echo "Running migrations..."
python -m app.migration
echo "Migrations complete."

echo "Seeding database..."
python -m app.db.seed
echo "Seeding complete."

echo "Starting Booking Service..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000


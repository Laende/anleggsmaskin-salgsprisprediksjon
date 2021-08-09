#!/bin/sh

# The web service is dependent not only on the container being up and running but also the actual 
# Postgres instance being up and healthy. The loop continues until a message verifying a connection to the DB is returned.

echo "Waiting for postgres..."

while ! nc -z web-db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

exec "$@"
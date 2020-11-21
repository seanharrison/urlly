#!/bin/sh
set -e

until psql $DATABASE_URL -c '\l'; do
    >&2 echo "Waiting for postgres..."
    sleep 1
done

alembic upgrade head

exec "$@"
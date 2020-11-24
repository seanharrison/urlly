#!/bin/bash
set -eux

# linting check, exit 1 if any errors
black --check app tests
flake8 app tests

# create the test database and migrate it
export POSTGRES_DB=${POSTGRES_DB}_test
psql -c "DROP DATABASE IF EXISTS $POSTGRES_DB" $DATABASE_URL
psql -c "CREATE DATABASE $POSTGRES_DB" $DATABASE_URL

export DATABASE_URL=${DATABASE_URL}_test
alembic upgrade head

# run the pytests (using the test database)
export TESTING=true  # flag to force database rollback per test case in the api app
pytest "$@"

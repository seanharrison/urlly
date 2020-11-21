#!/bin/bash
PATHS="app tests alembic"
isort -q -rc $PATHS
black -q $PATHS
flake8 $PATHS

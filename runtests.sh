#!/bin/bash
set -eux

# linting check, exit 1 if any errors
black --check app tests
flake8 app tests

pytest

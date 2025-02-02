#!/bin/bash

set -e
set -x

# pip install -U pip setuptools && pip install -r /rekrutka/requirements.txt

if [ "$DEVELOPMENT" = "YES" ]; then
    python -m flask run --debug --host 0.0.0.0
else
    python -m flask run --host 0.0.0.0
fi
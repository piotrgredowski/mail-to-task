#!/bin/bash

set -o allexport
[[ -f .env ]] && source .env
set +o allexport

source .venv/bin/activate
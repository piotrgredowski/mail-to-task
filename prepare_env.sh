#!/bin/bash

set -o allexport
[[ -f .env ]] && source .env
set +o allexport

export $(cat .env | xargs)

source .venv/bin/activate

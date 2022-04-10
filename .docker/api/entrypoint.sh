#!/bin/sh

set -eo pipefail

python manage.py migrate

exec $@
#!/bin/sh

set -eo pipefail

if [[ "$DEBUG" == "1" ]]; then npm run dev; else node .output/server/index.mjs; fi

exec $@
#!/bin/bash
# Build le wheel tchat-client depuis dist/tchat-client/.
# Usage: make build-client

set -e

python3 -m pip install --quiet hatch
cd dist/tchat-client
hatch build --clean

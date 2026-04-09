#!/bin/bash
# Deploy sur le Pi : git pull + restart service.
# Usage: make deploy-pi

set -e

source .env

echo "Deploying to Pi..."
ssh ${PIUSER}@${PI} "cd tchat && git fetch origin && git reset --hard origin/main && uv sync && sudo systemctl restart tchat"
echo "Done."

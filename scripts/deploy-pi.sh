#!/bin/bash
# Deploy sur le Pi : git pull + restart service.
# Usage: make deploy-pi

set -e

source .env

echo "Deploying to Pi..."
ssh ${PIUSER}@${PI} "cd tchat && git pull origin main && sudo systemctl restart tchat"
echo "Done."

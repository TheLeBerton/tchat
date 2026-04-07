#!/bin/bash

set -e

source .env

echo "Pushing to GitHub..."
git push origin main

echo "Deploying to Pi..."
ssh ${PIUSER}@${PI} "cd tchat && git pull origin main && sudo systemctl restart tchat"

echo "Done."

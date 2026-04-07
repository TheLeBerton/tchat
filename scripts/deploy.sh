#!/bin/bash

set -e

source .env

echo "Pushing to GitHub..."
git push origin main

echo "Deploying to Pi..."
ssh ${PIUSER}@${PI} "cd tchat && git pull origin main && tmux kill-server 2>/dev/null; tmux new-session -d -s server 'make watch'"

echo "Done."

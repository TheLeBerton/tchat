#!/bin/bash

set -e

source .env

echo "Pushing to GitHub..."
git push origin main

echo "Deploying to Pi..."
ssh ${PIUSER}@${PI} "
	cd tchat &&
	git pull origin main &&
	tmux send-keys -t server '/restart 10' Enter &&
	sleep 12 &&
	tmux kill-session -t server 2>/dev/null || true &&
	tmux new-session -d -s server 'make watch'
"

echo "Deploy done."

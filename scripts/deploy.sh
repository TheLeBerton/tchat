#!/bin/bash

set -e

source .env

echo "Pushing to GitHub..."
git push origin main

echo "Deploying to Pi..."
ssh ${PIUSER}@${PI} "
	cd tchat &&
	git pull origin main &&
	kill -USR1 \$(pgrep -f 'main.py serv') 2>/dev/null || true &&
	sleep 12 &&
	tmux kill-session -t server 2>/dev/null || true &&
	tmux new-session -d -s server 'make watch'
"

echo "Deploy done."

#!/bin/bash

set -e

source .env

echo "Pushing to GitHub..."
git push origin main

echo "Deploying to Pi..."
ssh ${PIUSER}@${PI} "cd tchat && git pull origin main && nohup bash -c 'kill -USR1 \$(pgrep -f main.py) 2>/dev/null; sleep 12; tmux kill-session -t server 2>/dev/null; tmux new-session -d -s server \"make watch\"' &>/dev/null &"

echo "Deploy done. Server restarting in ~12s..."

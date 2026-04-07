PYTHON = venv/bin/python3

dev:
	@tmux split-window -h
	@tmux split-window -v -t 1
	@$(PYTHON) main.py serv

kill:
	@tmux kill-pane -a

serv:
	@clear
	@$(PYTHON) main.py serv

cli:
	@rm -f $(HOME)/.tchat_username
	@clear
	@$(PYTHON) main.py cli

watch:
	@echo "Starting server in watch mode ( auto-restart )..."
	@trap 'exit 0' INT; while true; do \
		$(PYTHON) main.py serv || true; \
		echo "Server stopped. Restarting is 3s... ( CTRL-C to quit )"; \
		sleep 3; \
	done

PYTHON = venv/bin/python3

dev:
	tmux split-window -h 'sleep 1 && make cli'
	tmux split-window -v -t 1 'sleep 1 && make cli'
	$(PYTHON) main.py serv

kill:
	tmux kill-pane -a

serv:
	$(PYTHON) main.py serv

cli:
	$(PYTHON) main.py cli

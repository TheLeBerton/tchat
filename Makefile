PYTHON = venv/bin/python3

dev:
	tmux split-window -h
	tmux split-window -v -t 1
	$(PYTHON) main.py serv

kill:
	tmux kill-pane -a

serv:
	$(PYTHON) main.py serv

cli:
	$(PYTHON) main.py cli

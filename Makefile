-include .env
export PYTHON_KEYRING_BACKEND

PYTHON = venv/bin/python3

serv:
	@clear
	@$(PYTHON) main.py serv

cli:
	@clear
	@$(PYTHON) main.py cli

watch:
	@echo "Starting server in watch mode ( auto-restart )..."
	@trap 'exit 0' INT; while true; do \
		$(PYTHON) main.py serv || true; \
		echo "Server stopped. Restarting is 3s... ( CTRL-C to quit )"; \
		sleep 3; \
	done

test-serv:
	$(PYTHON) main.py serv

test-cli:
	@rm -f $(HOME)/.tchat_username
	$(PYTHON) main.py cli --host 127.0.0.1

test-pip:
	python -m venv /tmp/test-tchat && /tmp/test-tchat/bin/pip install tchat-client && /tmp/test-tchat/bin/tchat

sync-client:
	@bash scripts/sync-client.sh

build-client:
	@bash scripts/build-client.sh

publish-client:
	@bash scripts/sync-client.sh
	@bash scripts/build-client.sh
	@bash scripts/publish-client.sh

deploy-pi:
	@bash scripts/deploy-pi.sh

deploy:
	@git push origin main
	@bash scripts/deploy-pi.sh

version:
	./scripts/bump_version.py

log:
	@ssh admin@ftpi.local "cat /home/admin/.local/share/tchat/server.log | tail -20"

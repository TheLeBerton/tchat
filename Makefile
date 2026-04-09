-include .env
export PYTHON_KEYRING_BACKEND

# ── Dev ───────────────────────────────────────────────────────────────────────

serv:
	@clear
	@uv run tchat-server

cli:
	@clear
	@uv run tchat

watch:
	@echo "Starting server in watch mode ( auto-restart )..."
	@trap 'exit 0' INT; while true; do \
		uv run tchat-server || true; \
		echo "Server stopped. Restarting in 3s... ( CTRL-C to quit )"; \
		sleep 3; \
	done

test-cli:
	@rm -f $(HOME)/.tchat_username
	@uv run tchat --host 127.0.0.1

# ── Release ───────────────────────────────────────────────────────────────────

version:
	./scripts/bump_version.py

build-client:
	uv build packages/tchat-client

build-shared:
	uv build packages/tchat-shared

publish-client:
	rm -f dist/tchat_client-*
	uv build packages/tchat-client
	uv publish dist/tchat_client-*

publish-shared:
	rm -f dist/tchat_shared-*
	uv build packages/tchat-shared
	uv publish dist/tchat_shared-*

# ── Check ─────────────────────────────────────────────────────────────────────

check:
	@LOCAL=$$(grep -oP '(?<=")[^"]+(?=")' packages/tchat-shared/tchat_shared/version.py); \
	PYPI=$$(python3 -c "import urllib.request,json; print('v'+json.loads(urllib.request.urlopen('https://pypi.org/pypi/tchat-client/json',timeout=3).read())['info']['version'])" 2>/dev/null || echo "?"); \
	PI=$$(ssh admin@$(PI) "grep -oP '(?<=\")[^\"]+(?=\")' ~/tchat/packages/tchat-shared/tchat_shared/version.py" 2>/dev/null || echo "?"); \
	echo "Local  : $$LOCAL"; \
	echo "PyPI   : $$PYPI"; \
	echo "Pi     : $$PI"

# ── Deploy ────────────────────────────────────────────────────────────────────

deploy:
	@git push origin main
	@bash scripts/deploy-pi.sh

log:
	@ssh admin@$(PI) "cat /home/admin/.local/share/tchat/server.log | tail -20"

server-status:
	@ssh admin@$(PI) "journalctl -u tchat -n 30"

# ── Test PyPI ─────────────────────────────────────────────────────────────────

test-pip:
	@rm -rf /tmp/test-tchat
	@python -m venv /tmp/test-tchat && /tmp/test-tchat/bin/pip install tchat-client && /tmp/test-tchat/bin/tchat

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
	@python3 - "$(PI)" "$(PIUSER)" <<'EOF'
import sys, re, json, threading, subprocess, urllib.request

pi, piuser = sys.argv[1], sys.argv[2]
results = {}

def get_local():
    content = open("packages/tchat-shared/tchat_shared/version.py").read()
    results["local"] = re.search(r'"(v[\d.]+)"', content).group(1)

def get_pypi():
    try:
        data = json.loads(urllib.request.urlopen("https://pypi.org/pypi/tchat-client/json", timeout=5).read())
        results["pypi"] = "v" + data["info"]["version"]
    except Exception:
        results["pypi"] = "?"

def get_pi():
    try:
        out = subprocess.check_output(
            ["ssh", f"{piuser}@{pi}", "grep -oP '(?<=\")v[^\"]+(?=\")' ~/tchat/packages/tchat-shared/tchat_shared/version.py"],
            timeout=10, stderr=subprocess.DEVNULL,
        ).decode().strip()
        results["pi"] = out or "?"
    except Exception:
        results["pi"] = "?"

threads = [threading.Thread(target=f) for f in [get_local, get_pypi, get_pi]]
for t in threads: t.start()
for t in threads: t.join()

local, pypi, pi_v = results["local"], results["pypi"], results["pi"]
ok   = lambda v: "✓" if v == local else "✗"
print(f"Local  : {local}")
print(f"PyPI   : {pypi}  {ok(pypi)}")
print(f"Pi     : {pi_v}  {ok(pi_v)}")
EOF

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

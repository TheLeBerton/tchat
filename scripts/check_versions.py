#!/usr/bin/env python3
import re
import json
import sys
import threading
import subprocess
import urllib.request

pi = sys.argv[1]
piuser = sys.argv[2]
results: dict = {}


def get_local() -> None:
    content = open("packages/tchat-shared/tchat_shared/version.py").read()
    results["local"] = re.search(r'"(v[\d.]+)"', content).group(1)


def get_pypi() -> None:
    try:
        data = json.loads(
            urllib.request.urlopen(
                "https://pypi.org/pypi/tchat-client/json", timeout=5
            ).read()
        )
        results["pypi"] = "v" + data["info"]["version"]
    except Exception:
        results["pypi"] = "?"


def get_pi() -> None:
    try:
        out = subprocess.check_output(
            [
                "ssh",
                f"{piuser}@{pi}",
                "grep -oP '(?<=\")v[^\"]+(?=\")' ~/tchat/packages/tchat-shared/tchat_shared/version.py",
            ],
            timeout=10,
            stderr=subprocess.DEVNULL,
        ).decode().strip()
        results["pi"] = out or "?"
    except Exception:
        results["pi"] = "?"


threads = [threading.Thread(target=f) for f in [get_local, get_pypi, get_pi]]
for t in threads:
    t.start()
for t in threads:
    t.join()

local = results["local"]
pypi = results["pypi"]
pi_v = results["pi"]

ok = lambda v: "✓" if v == local else "✗"
print(f"Local  : {local}")
print(f"PyPI   : {pypi}  {ok(pypi)}")
print(f"Pi     : {pi_v}  {ok(pi_v)}")

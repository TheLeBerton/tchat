#!/bin/bash
# Sync les fichiers client dans dist/tchat-client/.
# Usage: make sync-client

set -e

DIST_DIR="dist/tchat-client"
VERSION=$(grep '^VERSION' tchat/version.py | sed 's/.*"v\(.*\)"/\1/')

echo "=== Sync client package (v$VERSION) ==="

rm -rf "$DIST_DIR/tchat"
mkdir -p "$DIST_DIR/tchat"
cp -r tchat/client    "$DIST_DIR/tchat/"
cp -r tchat/message   "$DIST_DIR/tchat/"
cp -r tchat/config    "$DIST_DIR/tchat/"
cp -r tchat/logger    "$DIST_DIR/tchat/"
cp    tchat/exceptions.py "$DIST_DIR/tchat/"
cp    tchat/version.py    "$DIST_DIR/tchat/"
cp    tchat/__init__.py   "$DIST_DIR/tchat/"

cat > "$DIST_DIR/pyproject.toml" <<EOF
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "tchat-client"
version = "$VERSION"
description = "tchat — client"
requires-python = ">=3.11"
dependencies = [
    "typer>=0.24.1",
    "prompt_toolkit>=3.0.52",
]

[project.scripts]
tchat = "tchat.client.runner:run"

[tool.hatch.build.targets.wheel]
packages = ["tchat"]
include = ["tchat/**/*.toml"]
EOF

echo "Fichiers générés dans $DIST_DIR/"

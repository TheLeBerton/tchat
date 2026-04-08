#!/bin/bash
# Génère dist/tchat-client/, build le wheel et publie sur PyPI.
# Usage: make publish-client
# Prérequis: avoir un compte PyPI et un token configuré (hatch publish le demande la 1ère fois).

set -e

DIST_DIR="dist/tchat-client"
VERSION=$(grep '^version' pyproject.toml | head -1 | sed 's/.*= "\(.*\)"/\1/')

echo "=== Sync client package (v$VERSION) ==="

# Sync des fichiers client
rm -rf "$DIST_DIR/tchat"
mkdir -p "$DIST_DIR/tchat"
cp -r tchat/client    "$DIST_DIR/tchat/"
cp -r tchat/message   "$DIST_DIR/tchat/"
cp -r tchat/config    "$DIST_DIR/tchat/"
cp -r tchat/logger    "$DIST_DIR/tchat/"
cp    tchat/exceptions.py "$DIST_DIR/tchat/"
cp    tchat/version.py    "$DIST_DIR/tchat/"
cp    tchat/__init__.py   "$DIST_DIR/tchat/"

# Script d'install pour les users
cp scripts/client-install.sh "$DIST_DIR/install.sh"

# pyproject.toml client-only
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

# Build + publish sur PyPI
echo "Build du package..."
python3 -m pip install --quiet hatch
cd "$DIST_DIR"
hatch build --clean
echo "Publication sur PyPI..."
hatch publish
echo ""
echo "Publié ! Les users installeront avec:"
echo "  curl -sSL https://raw.githubusercontent.com/TheLeBerton/tchat-client/main/install.sh | bash"

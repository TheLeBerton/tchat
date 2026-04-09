#!/bin/bash
# Publie tchat-client sur PyPI depuis dist/tchat-client/.
# Usage: make publish-client

set -e

cd dist/tchat-client
hatch publish
echo ""
echo "Publié ! Les users installeront avec:"
echo "  curl -sSL https://raw.githubusercontent.com/TheLeBerton/tchat/main/scripts/client-install.sh | bash"

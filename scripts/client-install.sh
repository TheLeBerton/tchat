#!/bin/bash
# Script d'installation de tchat pour les users.
# Usage: curl -sSL https://raw.githubusercontent.com/TheLeBerton/tchat/main/scripts/client-install.sh | bash

set -e

echo "=== Installation de tchat ==="

# Vérifie python3
if ! command -v python3 &>/dev/null; then
    echo "Erreur : python3 non trouvé."
    echo "Installe Python 3.11+ depuis https://www.python.org/downloads/"
    exit 1
fi

# Vérifie version >= 3.11
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)" 2>/dev/null; then
    version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    echo "Erreur : Python 3.11+ requis (tu as $version)."
    echo "Mets à jour Python depuis https://www.python.org/downloads/"
    exit 1
fi

# Assure que pip est disponible
python3 -m ensurepip --upgrade 2>/dev/null || true

# Installe / met à jour tchat-client
echo "Installation de tchat-client..."
python3 -m pip install --upgrade tchat-client --quiet

# Trouve le binaire installé
TCHAT_BIN=$(python3 -c "import sysconfig; print(sysconfig.get_path('scripts'))")/tchat
USER_BIN=$(python3 -m site --user-base 2>/dev/null)/bin/tchat

if command -v tchat &>/dev/null; then
    echo ""
    echo "Terminé ! Lance : tchat"
elif [ -f "$TCHAT_BIN" ]; then
    echo ""
    echo "Terminé ! Lance : $TCHAT_BIN"
    echo ""
    echo "Astuce — pour utiliser juste 'tchat', ajoute cette ligne à ton ~/.zshrc ou ~/.bashrc :"
    echo "  export PATH=\"$(dirname $TCHAT_BIN):\$PATH\""
elif [ -f "$USER_BIN" ]; then
    echo ""
    echo "Terminé ! Lance : $USER_BIN"
    echo ""
    echo "Astuce — pour utiliser juste 'tchat', ajoute cette ligne à ton ~/.zshrc ou ~/.bashrc :"
    echo "  export PATH=\"$(dirname $USER_BIN):\$PATH\""
else
    echo ""
    echo "Terminé ! Lance : python3 -m tchat"
fi

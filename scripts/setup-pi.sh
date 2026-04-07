#!/bin/bash
# À exécuter UNE SEULE FOIS sur le Pi depuis le dossier tchat :
#   bash scripts/setup-pi.sh
set -e

PI_USER=$(whoami)
PI_WORKDIR=$(pwd)

sudo tee /etc/systemd/system/tchat.service > /dev/null <<EOF
[Unit]
Description=Tchat Server
After=network.target

[Service]
Type=simple
User=${PI_USER}
WorkingDirectory=${PI_WORKDIR}
ExecStart=${PI_WORKDIR}/venv/bin/python main.py serv
Restart=on-failure
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable tchat
sudo systemctl start tchat
echo "Service tchat installé et démarré."
echo "Logs : journalctl -u tchat -f"

#!/bin/bash

set -e

MIN_PYTHON="3.11"

check_python() {
	if ! command -v python3 &>/dev/null; then
		echo "Python3 not found. Please install python $MIN_PYTHON or higher."
		exit 1
	fi

	version=$(python3 -c "import sys; print( f'{sys.version_info.major}.{sys.version_info.minor}')")
	required="3.11"
	if python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1 )"; then
		echo "Python $version found."
	else
		echo "Python $version found but $MIN_PYTHON+ is required."
		read -p "Would you like to update Python now ? (y/n): " choice
		if [[ "$choice" == "y" ]]; then
			echo "Please update python manually and re-run this script."
		fi
		exit 1
	fi
}

setup_venv() {
	if [ ! -d "venv" ]; then
		echo "Creating virtaul environment..."
		python3 -m venv venv
	else
		echo "Virtual environment already exists, skipping."
	fi
	echo "Installing dependencies..."
	venv/bin/pip install -q -r requirements.txt
	echo "Dependencies installed."
}

setup_config() {
	if [ -f "config/config.toml" ]; then
		echo "config.toml already exists, skipping."
	else
		cp config/config.example.toml config/config.toml
		echo "config.toml created from examlpe"
		echo "--> Edit config/config.toml to set you client's IP."
	fi
}


echo "=== tchat installer ==="
check_python
setup_venv
setup_config
echo "=== Done. Run 'make cli' to start the client or 'make serv' to start the server ==="


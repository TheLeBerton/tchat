"""Auto-updater: checks PyPI for a newer tchat-client version and upgrades if needed."""
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from importlib.metadata import PackageNotFoundError, version as pkg_version

from tchat_shared.version import VERSION

_PYPI_URL = "https://pypi.org/pypi/tchat-client/json"


def _fetch_remote_version() -> str | None:
    """Query PyPI and return the latest tchat-client version string, or None on failure."""
    try:
        with urllib.request.urlopen( _PYPI_URL, timeout=3 ) as resp:
            data = json.loads( resp.read() )
            return data[ "info" ][ "version" ]
    except ( OSError, urllib.error.URLError, json.JSONDecodeError, KeyError, ValueError ):
        pass
    return None


def check_and_update() -> None:
    """If a newer version exists on PyPI, upgrade the package and re-exec the process."""
    try:
        pkg_version( "tchat-client" )
    except PackageNotFoundError:
        return  # running from source (dev), skip

    remote = _fetch_remote_version()
    if remote is None or remote == VERSION.lstrip( "v" ):
        return

    print( f"Mise à jour disponible ({ VERSION } → v{ remote }). Installation..." )
    subprocess.run(
        [ sys.executable, "-m", "pip", "install", "--upgrade", "--quiet", "tchat-client" ],
        check=True,
    )
    print( "Mise à jour terminée. Redémarrage..." )
    os.execv( sys.executable, [ sys.executable ] + sys.argv )

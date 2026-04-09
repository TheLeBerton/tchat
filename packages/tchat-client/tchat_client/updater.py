import json
import os
import subprocess
import sys
import urllib.request
from importlib.metadata import PackageNotFoundError, version as pkg_version

from tchat_shared.version import VERSION

_PYPI_URL = "https://pypi.org/pypi/tchat-client/json"


def _fetch_remote_version() -> str | None:
    try:
        with urllib.request.urlopen( _PYPI_URL, timeout=3 ) as resp:
            data = json.loads( resp.read() )
            return data[ "info" ][ "version" ]
    except Exception:
        pass
    return None


def check_and_update() -> None:
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

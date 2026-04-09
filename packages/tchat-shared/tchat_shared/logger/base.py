import threading
from datetime import datetime

from .colors import Colors
from . import typewriter
from tchat_shared.config import config as _config


_lock = threading.Lock()
_user_colors: dict[ str, Colors ] = {}
_available_colors = [ Colors.BLUE, Colors.GREEN, Colors.YELLOW, Colors.RED, Colors.WHITE ]

def get_user_color( user: str ) -> Colors:
    if user not in _user_colors:
        _user_colors[ user ] = _available_colors[ len( _user_colors ) % len( _available_colors ) ]
    return _user_colors[ user ]

def log( msg: str, server_mode: bool = False ) -> None:
    with _lock:
        if not server_mode and _config.logger.typewriter:
            typewriter.write( msg, _config.logger.typewriter_delay )
        else:
            print( msg )


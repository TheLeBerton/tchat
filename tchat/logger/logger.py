from datetime import datetime
import threading

from .colors import Colors
from . import typewriter
from tchat.message.message import Message, MessageType
from tchat.config import config as _config


_user_colors: dict[ str, Colors ] = {}
_available_colors = [ Colors.BLUE, Colors.GREEN, Colors.YELLOW, Colors.RED, Colors.WHITE ]

_typewriter_enabled: bool = _config.logger.typewriter
_server_mode: bool = False
_lock = threading.Lock()

def set_server_mode( enabled: bool ) -> None:
    global _server_mode
    _server_mode = enabled

def _get_user_color( user: str ) -> Colors:
    if user not in _user_colors:
        _user_colors[ user ] = _available_colors[ len( _user_colors ) % len( _available_colors ) ]
    return _user_colors[ user ]

def message( msg: Message ) -> None:
    timestamp = f"{ Colors.WHITE.value }[{ msg.timestamp }]{ Colors.RESET.value }"
    if msg.type == MessageType.JOIN:
        _log( f"{ timestamp } { Colors.YELLOW.value }--> { msg.sender } joined{ Colors.RESET.value }" )
    elif msg.type == MessageType.LEAVE:
        _log( f"{ timestamp } { Colors.RED.value }<-- { msg.sender } left{ Colors.RESET.value }" )
    elif msg.type == MessageType.CHAT:
        color = _get_user_color( msg.sender ).value
        _log( f"{ timestamp } { color }{ Colors.BOLD.value }<{ msg.sender }>{ Colors.RESET.value } { msg.content }" )
    elif msg.type == MessageType.COMMAND:
        _log( f"{ timestamp } { Colors.BLUE.value }<server>{ Colors.RESET.value } { msg.content }" )

def info( msg: str ) -> None:
    _log( f"{ Colors.YELLOW.value }{ msg }{ Colors.RESET.value }" )

def error( msg: str ) -> None:
    _log( f"{ Colors.RED.value }{ msg }{ Colors.RESET.value }" )

def connected( address: tuple ) -> None:
    _log( f"{ Colors.GREEN.value }--> connected { address }{ Colors.RESET.value }" )

def disconnected( address: tuple ) -> None:
    _log( f"{ Colors.RED.value }<-- disconnected { address }{ Colors.RESET.value }" )

def banner() -> None:
    chat = r"""
 _____ _   _  _____   _     _____ _____ _   _ _ _____   _____  _   _   ___ _____
|_   _| | | ||  ___| | |   |_   _|  _  | \ | ( )  ___| /  __ \| | | | / _ \_   _|
  | | | |_| || |__   | |     | | | | | |  \| |/\ `--.  | /  \/| |_| |/ /_\ \| |
  | | |  _  ||  __|  | |     | | | | | | . ` |  `--. \ | |    |  _  ||  _  || |
  | | | | | || |___  | |_____| |_\ \_/ / |\  | /\__/ / | \__/\| | | || | | || |
  \_/ \_| |_/\____/  \_____/\___/ \___/\_| \_/ \____/   \____/\_| |_/\_| |_/\_/

"""
    print( f"{ Colors.BLUE.value }{ chat }{ Colors.RESET.value }" )

def _log( msg: str ) -> None:
    with _lock:
        if _server_mode:
            timestamp = datetime.now().strftime( "%H:%M:%S" )
            print( f"[{ timestamp }] { msg }" )
        elif _typewriter_enabled:
            typewriter.write( msg, _config.logger.typewriter_delay )
        else:
            print( msg )

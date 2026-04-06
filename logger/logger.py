from datetime import datetime
import threading

from .colors import Colors
from . import typewriter
from chat.message.message import Message, MessageType

_lock = threading.Lock()

_user_colors: dict[ str, Colors ] = {}
_available_colors = [ Colors.BLUE, Colors.GREEN, Colors.YELLOW, Colors.RED, Colors.WHITE ]

_typewriter_enabled: bool = True
_server_mode: bool = False

def set_server_mode( enabled: bool ) -> None:
    global _server_mode
    _server_mode = enabled

def set_typewriter( enabled: bool ) -> None:
    global _typewriter_enabled
    _typewriter_enabled = enabled

def _get_user_color( user: str ) -> Colors:
    if user not in _user_colors:
        _user_colors[ user ] = _available_colors[ len( _user_colors ) % len( _available_colors ) ]
    return _user_colors[ user ]


def message( msg: Message ) -> None:
    if msg.type == MessageType.JOIN:
        _log( f"[ { msg.timestamp } ] { msg.sender } joined the chat", Colors.GREEN )
    elif msg.type == MessageType.LEAVE:
        _log( f"[ { msg.timestamp } ] { msg.sender } leaved the chat", Colors.RED )
    elif msg.type == MessageType.CHAT:
        _log( f"[ { msg.timestamp } ][ { msg.sender } ]: { msg.content }", _get_user_color( msg.sender ) )
    elif msg.type == MessageType.COMMAND:
        _log( f"[ { msg.timestamp } ][ { msg.sender } ]: { msg.content }", Colors.BLUE )
    else:
        _log( msg.to_json(), Colors.WHITE )

def log( msg: str ) -> None:
    _log( f"{ msg }", Colors.WHITE, 0.1 )

def info( msg: str ) -> None:
    _log( f"{ msg }", Colors.YELLOW )

def error( msg: str ) -> None:
    _log( f"{ msg }", Colors.RED )

def success( msg: str ) -> None:
    _log( f"{ msg }", Colors.GREEN )

def info_user( msg: str, user: str ) -> None:
    _log( f"[ { user } ]: { msg }", Colors.YELLOW )

def error_user( msg: str, user: str ) -> None:
    _log( f"[ { user } ]: { msg }", Colors.RED )

def success_user( msg: str, user: str ) -> None:
    _log( f"[ { user } ]: { msg }", Colors.GREEN )

def connected( address: tuple ) -> None:
    _log( f"Connected to { address }", Colors.GREEN )

def disconnected( address: tuple ) -> None:
    _log( f"Disconnected from { address }", Colors.RED )

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

def _log( msg: str, color: Colors, delay: float = 0.1 ) -> None:
    with _lock:
        formatted = f"{ color.value }{ msg }{ Colors.RESET.value }"
        if _server_mode:
            timestamp = datetime.now().strftime( "%H:%M:%S" )
            print( f"[{ timestamp }] { msg }" )
        elif _typewriter_enabled:
            typewriter.write( formatted, delay )
        else:
            print( formatted )

    

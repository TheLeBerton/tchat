from .colors import Colors
from . import typewriter

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

def _log( msg: str, color: Colors, delay: float = 0.1 ) -> None:
    typewriter.write( f"{ color.value }{ msg }{ Colors.RESET.value }", delay )


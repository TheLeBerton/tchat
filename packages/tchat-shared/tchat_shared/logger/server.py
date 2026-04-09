import os
from datetime import datetime
from pathlib import Path

from . import base
from tchat_shared.message.message import Message, MessageType
from tchat_shared.config import config as _config


def _prefix( level: str ) -> str:
    timestamp = datetime.now().strftime( "%b %d %H:%M:%S" )
    return f"{ timestamp } tchat[{ os.getpid() }]: { level:^7}"

def _emit( msg: str ) -> None:
    base.log( msg, server_mode=True )
    _log_to_file( msg )

def info( msg: str ) -> None:
    _emit( f"{ _prefix('INFO') } { msg }" )

def warning( msg: str ) -> None:
    _emit( f"{ _prefix('WARN') } { msg }" )

def error( msg: str ) -> None:
    _emit( f"{ _prefix('ERROR') } { msg }" )

def message( msg: Message ) -> None:
    if msg.type == MessageType.JOIN:
        _emit( f"{ _prefix('JOIN') } { msg.sender } joined" )
    elif msg.type == MessageType.LEAVE:
        _emit( f"{ _prefix('LEAVE') } { msg.sender } left" )
    elif msg.type == MessageType.CHAT:
        _emit( f"{ _prefix('CHAT') } { msg.sender }: { msg.content }" )
    elif msg.type == MessageType.COMMAND:
        _emit( f"{ _prefix('CMD') } { msg.content }" )

def connected( address: tuple ) -> None:
    _emit( f"{ _prefix('CONN') } { address }" )

def disconnected( address: tuple ) -> None:
    _emit( f"{ _prefix('DISC') } { address }" )

def _log_to_file( msg: str ) -> None:
    if _config.logger.log_to_file:
        log_path = Path( _config.logger.log_file ).expanduser()
        log_path.parent.mkdir( parents=True, exist_ok=True )
        with open( log_path, "a" ) as f:
            f.write( msg + "\n" )

import os
from datetime import datetime

from . import base
from tchat.message.message import Message, MessageType


def _prefix( level: str ) -> str:
    timestamp = datetime.now().strftime( "%b %d %H:%M:%S" )
    return f"{ timestamp } tchat[{ os.getpid() }]: { level:^7}"

def _emit( msg: str ) -> None:
    base.log( msg, server_mode=True )

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

import socket

from . import commands
import logger
from message import Message


def handle( connection: socket.socket, msg: Message ) -> None:
    if msg.content == "whoonline":
        commands.whoonline( connection )
    elif msg.content == "help":
        commands.help( connection )
    logger.message( msg )

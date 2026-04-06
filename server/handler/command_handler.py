import socket

from . import commands
import logger
from message import Message


def handle( connection: socket.socket, msg: Message ) -> None:
    if msg.content == "whoonline":
        commands.whoonline( connection )
    logger.message( msg )

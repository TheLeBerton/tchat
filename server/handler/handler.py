import socket

from .. import state
import logger
from message import Message, MessageType
from . import join_handler
from . import chat_handler
from . import command_handler


def recieve( connection: socket.socket, address: tuple ) -> None:
    while True:
        try:
            data = connection.recv( 1024 )
            if not data:
                break
            _handle_data( data, connection, address )
        except Exception as e:
            logger.error( f"{ e }" )
            break
    connection.close()
    logger.disconnected( address )

def _handle_data( data: bytes, connection: socket.socket, address: tuple ) -> None:
    msg = Message.from_json( data.decode() )
    if msg.type == MessageType.JOIN:
        join_handler.handle( address, msg )
    if _is_unknown_user( address ):
        return
    if msg.type == MessageType.CHAT:
        chat_handler.handle( address, msg )
    elif msg.type == MessageType.COMMAND:
        command_handler.handle( connection, msg )

def _is_unknown_user( address: tuple ) -> bool:
    with state.lock:
        return address not in state.users

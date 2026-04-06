import socket

import logger
from chat.message.message import Message
from chat.message.types import MessageType
from chat.message.framing import receive_framed
from chat.handlers.base import HandlerRegistry
from chat.state.server_state import ServerState
from exceptions import MessageFramingError, InvalidMessageError


class ClientSession:
    def __init__ ( self, connection: socket.socket, address: tuple, state: ServerState, registry: HandlerRegistry ) -> None:
        self._connection = connection
        self._address = address
        self._state = state
        self._registry = registry

    def run( self ) -> None:
        try:
            while True:
                try:
                    raw = receive_framed( self._connection )
                except MessageFramingError:
                    break
                try:
                    msg = Message.from_json( raw )
                except InvalidMessageError as e:
                    logger.error( str( e ) )
                    continue
                self._registry.dispatch( self._address, msg, self._state )
        finally:
            leave_msg = Message.make( MessageType.LEAVE, "", "" )
            self._registry.dispatch( self._address, leave_msg, self._state )
            self._connection.close()
            logger.disconnected( self._address )

import socket

from tchat import logger
from tchat.version import VERSION
from tchat.message.message import Message
from tchat.message.types import MessageType
from tchat.message.framing import receive_framed, send_framed
from tchat.handlers.base import HandlerRegistry
from tchat.state.server_state import ServerState
from tchat.exceptions import MessageFramingError, InvalidMessageError


class ClientSession:
    def __init__ ( self, connection: socket.socket, address: tuple, state: ServerState, registry: HandlerRegistry ) -> None:
        self._connection = connection
        self._address = address
        self._state = state
        self._registry = registry

    def run( self ) -> None:
        version_msg = Message.make( MessageType.VERSION, "server", VERSION )
        send_framed( self._connection, version_msg.to_json() )
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

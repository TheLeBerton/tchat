from typing import Protocol

from tchat_shared.message.message import Message
from tchat_shared.message.types import MessageType
from tchat_server.state.server_state import ServerState
from tchat_shared.exceptions import CommandError


class MessageHandler( Protocol ):
    def handle( self, address: tuple, msg: Message, state: ServerState ) -> None: ...


class HandlerRegistry:
    def __init__( self ) -> None:
        self._handlers: dict[ MessageType, MessageHandler ] = {}

    def register( self, type: MessageType, handler: MessageHandler ) -> None:
        self._handlers[ type ] = handler

    def dispatch( self, address: tuple, msg: Message, state: ServerState ) -> None:
        handler = self._handlers.get( msg.type )
        if handler is None:
            raise CommandError( f"No handler for message type: { msg.type }" )
        handler.handle( address, msg, state )

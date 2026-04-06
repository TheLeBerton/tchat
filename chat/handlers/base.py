from typing import Protocol

from chat.message.message import Message
from chat.message.types import MessageType
from chat.state.server_state import ServerState
from exceptions import CommandError


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

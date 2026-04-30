"""Protocol and registry for message handlers."""
from typing import Protocol

from tchat_shared.message.message import Message
from tchat_shared.message.types import MessageType
from tchat_server.state.server_state import ServerState
from tchat_shared.exceptions import CommandError


class MessageHandler( Protocol ):
    """Interface that every message handler must satisfy."""

    def handle( self, address: tuple[str, int], msg: Message, state: ServerState ) -> None:
        """Process the message received from address using the shared server state."""
        ...


class HandlerRegistry:
    """Maps MessageType values to their corresponding MessageHandler."""

    def __init__( self ) -> None:
        self._handlers: dict[ MessageType, MessageHandler ] = {}

    def register( self, type: MessageType, handler: MessageHandler ) -> None:
        self._handlers[ type ] = handler

    def dispatch( self, address: tuple[str, int], msg: Message, state: ServerState ) -> None:
        """Look up and call the handler for msg.type; raises CommandError if none registered."""
        handler = self._handlers.get( msg.type )
        if handler is None:
            raise CommandError( f"No handler for message type: { msg.type }" )
        handler.handle( address, msg, state )

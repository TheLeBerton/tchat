"""Manages the lifecycle of a single client connection."""
from collections.abc import Iterator
import socket

from tchat_shared import logger
from tchat_shared.version import VERSION
from tchat_shared.message.message import Message, LeaveMessage, VersionMessage
from tchat_shared.message.framing import receive_framed, send_framed
from tchat_server.handlers.base import HandlerRegistry
from tchat_server.state.server_state import ServerState
from tchat_shared.exceptions import MessageFramingError, InvalidMessageError, CommandError, JoinError


class ClientSession:
    """Handles the full message loop for one connected client."""

    def __init__ ( self, connection: socket.socket, address: tuple, state: ServerState, registry: HandlerRegistry ) -> None:
        """Store the connection, address, shared state, and handler registry."""
        self._connection = connection
        self._address = address
        self._state = state
        self._registry = registry

    def run( self ) -> None:
        """Send the version handshake, process incoming messages, then clean up."""
        version_msg = VersionMessage.make( "server", VERSION )
        send_framed( self._connection, version_msg.to_json() )
        try:
            for raw in self._messages():
                self._handle( raw )
        finally:
            leave_msg = LeaveMessage.make( "", "" )
            self._registry.dispatch( self._address, leave_msg, self._state )
            self._connection.close()
            logger.server.disconnected( self._address )

    def _messages( self ) -> Iterator[ str ]:
        """Yield raw framed strings from the socket until the connection closes."""
        while True:
            try:
                yield receive_framed( self._connection )
            except MessageFramingError:
                break

    def _handle( self, raw: str ) -> None:
        """Parse a raw JSON string and dispatch it to the appropriate handler."""
        try:
            msg = Message.from_json( raw )
            self._registry.dispatch( self._address, msg, self._state )
        except ( InvalidMessageError, CommandError, JoinError ) as e:
            logger.server.error( str( e ) )

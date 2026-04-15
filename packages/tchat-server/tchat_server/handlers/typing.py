"""Handler for TYPING messages — broadcasts typing status to other users."""
from tchat_shared.message.message import TypingMessage
from tchat_server.state.server_state import ServerState


class TypingHandler:
    """Forwards typing-status events to all users except the sender."""

    def handle( self, address: tuple, msg: TypingMessage, state: ServerState ) -> None:
        """Look up the sender's username and broadcast the typing status."""
        username = state.accounts.get_username( address )
        if username is None:
            return
        self._broadcast_user_is_typing( username, address, msg, state )

    def _broadcast_user_is_typing( self, username: str, address: tuple, msg: TypingMessage, state: ServerState ) -> None:
        """Broadcast the typing event to all users except the sender."""
        tp_msg = TypingMessage.make( username, msg.status )
        state.broadcaster.cast( tp_msg.to_json(), exclude=address )

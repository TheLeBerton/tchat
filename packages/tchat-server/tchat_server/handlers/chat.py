"""Handler for incoming chat messages."""
from tchat_shared import logger
from tchat_shared.config import config as _config
from tchat_shared.message.message import ChatMessage, CommandMessage
from tchat_server.state.server_state import ServerState
from tchat_shared.exceptions import UnknowUserError


class ChatHandler:
    """Validates and broadcasts chat messages from registered users."""

    def handle( self, address: tuple, msg: ChatMessage, state: ServerState ) -> None:
        """Validate the sender is registered, then broadcast the message."""
        username = self._require_username( address, state )
        self._broadcast_chat( address, msg, state, username )

    def _require_username( self, address: tuple, state: ServerState ) -> str:
        """Return the username for address; raises UnknowUserError if not found."""
        username = state.accounts.get_username( address )
        if username is None:
            raise UnknowUserError( f"No user registered for { address }" )
        return username

    def _broadcast_chat( self, address: tuple, msg: ChatMessage, state: ServerState, username: str ) -> None:
        """Validate content, then broadcast the message and add it to history."""
        if not self._validate_content( address, msg.text, state ):
            return
        chat_msg = ChatMessage.make( username, msg.text )
        state.broadcaster.cast( chat_msg.to_json(), exclude=address )
        state.history.add_to_history( chat_msg.to_json() )
        logger.server.message( chat_msg )

    def _validate_content( self, address: tuple, content: str , state: ServerState ) -> bool:
        """Return False and notify the sender if content is empty or too long."""
        if not content.strip():
            error_msg = CommandMessage.make( "server", "Messages content cannot be empty" )
            state.broadcaster.send_to( address, error_msg.to_json() )
            return False
        if len( content ) > _config.chat.max_message_length:
            error_msg = CommandMessage.make( "server", "Messages content exceeded max length" )
            state.broadcaster.send_to( address, error_msg.to_json() )
            return False
        return True


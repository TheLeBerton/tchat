from tchat_shared import logger
from tchat_shared.config import config as _config
from tchat_shared.message.message import Message
from tchat_shared.message.types import MessageType
from tchat_server.state.server_state import ServerState
from tchat_shared.exceptions import UnknowUserError


class ChatHandler:
    def handle( self, address: tuple, msg: Message, state: ServerState ) -> None:
        username = self._require_username( address, state )
        self._broadcast_chat( address, msg, state, username )

    def _require_username( self, address: tuple, state: ServerState ) -> str:
        username = state.accounts.get_username( address )
        if username is None:
            raise UnknowUserError( f"No user registered for { address }" )
        return username

    def _broadcast_chat( self, address: tuple, msg: Message, state: ServerState, username: str ) -> None:
        if not self._validate_content( address, msg.content, state ):
            return
        chat_msg = Message.make( MessageType.CHAT, username, msg.content)
        state.broadcaster.cast( chat_msg.to_json(), exclude=address )
        state.history.add_to_history( chat_msg.to_json() )
        logger.server.message( chat_msg )

    def _validate_content( self, address: tuple, content: str , state: ServerState ) -> bool:
        if not content.strip():
            error_msg = Message.make( MessageType.CHAT, "server", "Messages content cannot be empty" )
            state.broadcaster.send_to( address, error_msg.to_json() )
            return False
        if len( content ) > _config.chat.max_message_length:
            error_msg = Message.make( MessageType.CHAT, "server", "Messages content exceeded max length" )
            state.broadcaster.send_to( address, error_msg.to_json() )
            return False
        return True


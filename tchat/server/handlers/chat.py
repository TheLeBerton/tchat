from tchat import logger
from tchat.message.message import Message
from tchat.message.types import MessageType
from tchat.server.state.server_state import ServerState
from tchat.exceptions import UnknowUserError


class ChatHandler:
    def handle( self, address: tuple, msg: Message, state: ServerState ) -> None:
        username = self._require_username( address, state )
        self._broadcast_chat( address, msg, state, username )

    def _require_username( self, address: tuple, state: ServerState ) -> str:
        username = state.get_username( address )
        if username is None:
            raise UnknowUserError( f"No user registered for { address }" )
        return username

    def _broadcast_chat( self, address: tuple, msg: Message, state: ServerState, username: str ) -> None:
        chat_msg = Message.make( MessageType.CHAT, username, msg.content)
        state.broadcast( chat_msg.to_json(), exclude=address )
        state.add_to_history( chat_msg.to_json() )
        logger.message( chat_msg )

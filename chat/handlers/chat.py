import logger
from chat.message.message import Message
from chat.message.types import MessageType
from chat.state.server_state import ServerState
from exceptions import UnknowUserError


class ChatHandler:
    def handle( self, address: tuple, msg: Message, state: ServerState ) -> None:
        username = state.get_username( address )
        if username is None:
            raise UnknowUserError( f"No user registered for { address }" )
        state.add_user( address, msg.sender )
        chat_msg = Message.make( MessageType.CHAT, username, msg.content)
        state.broadcast( chat_msg.to_json(), exclude=address )
        logger.message( chat_msg )

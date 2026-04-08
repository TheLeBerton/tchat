from tchat.message.message import Message
from tchat.message.types import MessageType
from tchat.state.server_state import ServerState


class TypingHandler:
    def handle( self, address: tuple, msg: Message, state: ServerState ) -> None:
        username = state.get_username( address )
        if username is None:
            return
        self._broadcast_user_is_typing( username, address, msg, state )

    def _broadcast_user_is_typing( self, username: str, address: tuple, msg: Message, state: ServerState ) -> None:
        tp_msg = Message.make( MessageType.TYPING, username, msg.content )
        state.broadcast( tp_msg.to_json(), exclude=address )

from tchat.message.message import Message
from tchat.message.types import MessageType
from tchat.state.server_state import ServerState


class TypingHandler:
    def handle( self, address: tuple, msg: Message, state: ServerState ) -> None:
        username = state.get_username( address )
        if username is None:
            return
        payload = Message.make( MessageType.TYPING, username, msg.content ).to_json()
        state.broadcast( payload, exclude=address )

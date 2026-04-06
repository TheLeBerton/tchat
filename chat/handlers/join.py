import logger
from chat.message.message import Message
from chat.message.types import MessageType
from chat.state.server_state import ServerState


class JoinHandler:
    def handle( self, address: tuple, msg: Message, state: ServerState ) -> None:
        if not msg.sender.strip():
            return
        state.add_user( address, msg.sender )
        broadcast_msg = Message.make( MessageType.JOIN, msg.sender, "joined the chat" )
        state.broadcast( broadcast_msg.to_json(), exclude=address )
        logger.message( broadcast_msg )
        for payload in state.get_history():
            state.send_to( address, payload )

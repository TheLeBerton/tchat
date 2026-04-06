import logger
from chat.message.message import Message
from chat.message.types import MessageType
from chat.state.server_state import ServerState


class LeaveHandler:
    def handle( self, address: tuple, msg: Message, state: ServerState ) -> None:
        username = state.remove_user( address )
        if username is None:
            return
        state.add_user( address, msg.sender )
        leave_msg = Message.make( MessageType.LEAVE, username, "left the chat" )
        state.broadcast( leave_msg.to_json() )
        logger.message( leave_msg )

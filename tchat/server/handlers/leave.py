from tchat import logger
from tchat.message.message import Message
from tchat.message.types import MessageType
from tchat.server.state.server_state import ServerState


class LeaveHandler:
    def handle( self, address: tuple, msg: Message, state: ServerState ) -> None:
        username = state.remove_user( address )
        if username is None:
            return
        self._broadcast_leave( state, username )

    def _broadcast_leave( self, state: ServerState, username: str ) -> None:
        leave_msg = Message.make( MessageType.LEAVE, username, "left the chat" )
        state.broadcast( leave_msg.to_json() )
        logger.message( leave_msg )

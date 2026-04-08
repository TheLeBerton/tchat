from tchat import logger
from tchat.message.message import Message
from tchat.message.types import MessageType
from tchat.state.server_state import ServerState


class JoinHandler:
    def handle( self, address: tuple, msg: Message, state: ServerState ) -> None:
        if not msg.sender.strip():
            return
        if state.is_username_taken( msg.sender ):
            error_msg = Message.make( MessageType.COMMAND, "server", f"Username '{ msg.sender }' is already taken." )
            state.send_to( address, error_msg.to_json() )
            state.kick( address )
            return
        state.add_user( address, msg.sender )
        broadcast_msg = Message.make( MessageType.JOIN, msg.sender, "joined the chat" )
        state.broadcast( broadcast_msg.to_json(), exclude=address )
        logger.message( broadcast_msg )
        for payload in state.get_history():
            state.send_to( address, payload )
        if state.check_and_clear_restart_flag():
            msg = Message.make( MessageType.COMMAND, "server", "Server is back online." )
            state.broadcast( msg.to_json() )

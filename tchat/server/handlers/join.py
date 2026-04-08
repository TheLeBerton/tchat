from tchat import logger
from tchat.message.message import Message
from tchat.message.types import MessageType
from tchat.server.state.server_state import ServerState
from tchat.exceptions import JoinError


class JoinHandler:
    def handle( self, address: tuple, msg: Message, state: ServerState ) -> None:
        self._validate_username( address, msg, state )
        self._register_user( state, msg, address )
        self._handle_server_restart( state )

    def _validate_username( self, address: tuple, msg: Message, state: ServerState ) -> None:
        if not msg.sender.strip():
            raise JoinError( "empty username" )
        if state.is_username_taken( msg.sender ):
            error_msg = Message.make( MessageType.COMMAND, "server", f"Username '{ msg.sender }' is already taken." )
            state.send_to( address, error_msg.to_json() )
            state.kick( address )
            raise JoinError( f"username taken: { msg.sender }" )

    def _register_user( self, state: ServerState, msg: Message, address: tuple ) -> None:
        state.add_user( address, msg.sender )
        self._broadcast_join_message( state, msg, address )
        self._send_history_to_user( state, address )

    def _broadcast_join_message( self, state: ServerState, msg: Message, address: tuple ) -> None:
        broadcast_msg = Message.make( MessageType.JOIN, msg.sender, "joined the chat" )
        state.broadcast( broadcast_msg.to_json(), exclude=address )
        logger.server.message( broadcast_msg )

    def _send_history_to_user( self, state: ServerState, address: tuple ) -> None:
        for payload in state.get_history():
            state.send_to( address, payload )

    def _handle_server_restart( self, state: ServerState ) -> None:
        if state.check_and_clear_restart_flag():
            msg = Message.make( MessageType.COMMAND, "server", "Server is back online." )
            state.broadcast( msg.to_json() )

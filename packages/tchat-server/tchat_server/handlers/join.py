from tchat_shared import logger
from tchat_shared.config import config as _config
from tchat_shared.message.message import Message
from tchat_shared.message.types import MessageType
from tchat_server.state.server_state import ServerState
from tchat_shared.exceptions import JoinError


class JoinHandler:
    def handle( self, address: tuple, msg: Message, state: ServerState ) -> None:
        self._validate_username( address, msg, state )
        self._register_user( state, msg, address )
        self._handle_server_restart( state )

    def _validate_username( self, address: tuple, msg: Message, state: ServerState ) -> None:
        if state.ban.is_banned( address ):
            msg = Message.make( MessageType.KICK, "server", "You are banned from this server." )
            state.broadcaster.send_to( address, msg.to_json() )
            state.accounts.kick( address )
            raise JoinError( "banned username" )
        if not msg.sender.strip():
            raise JoinError( "empty username" )
        if state.accounts.is_username_taken( msg.sender ):
            error_msg = Message.make( MessageType.COMMAND, "server", _config.messages.username_taken.format( msg.sender ) )
            state.broadcaster.send_to( address, error_msg.to_json() )
            state.accounts.kick( address )
            raise JoinError( f"username taken: { msg.sender }" )
        if msg.sender in _config.admin.usernames and address[ 0 ] not in _config.admin.ips:
            error_msg = Message.make( MessageType.COMMAND, "server", "Admin access not configured for your IP" )
            state.broadcaster.send_to( address, error_msg.to_json() )
            state.accounts.kick( address )
            logger.server.warning( f"( { address[ 0] } ) tried to connect as admin" )
            raise JoinError( f"reserved username: { msg.sender }" )

    def _register_user( self, state: ServerState, msg: Message, address: tuple ) -> None:
        state.accounts.add_user( address, msg.sender )
        if msg.sender in _config.admin.usernames and address[ 0 ] in _config.admin.ips:
            state.accounts.set_admin( address )
        self._broadcast_join_message( state, msg, address )
        self._send_history_to_user( state, address )
        self._send_welcome_to_user( state, address, msg.sender )

    def _broadcast_join_message( self, state: ServerState, msg: Message, address: tuple ) -> None:
        broadcast_msg = Message.make( MessageType.JOIN, msg.sender, _config.messages.broadcast_joined )
        state.broadcaster.cast( broadcast_msg.to_json(), exclude=address )
        logger.server.message( broadcast_msg )

    def _send_history_to_user( self, state: ServerState, address: tuple ) -> None:
        for payload in state.history.get_history():
            state.broadcaster.send_to( address, payload )

    def _send_welcome_to_user( self, state: ServerState, address: tuple, username: str ) -> None:
        try:
            text = _config.messages.welcome_text.format( username )
        except ( KeyError, IndexError ) as e:
            logger.server.error( f"Invalid welcome_text template in JoinHandler._send_welcome_to_user. { e }" )
            text = "Hi, welcome to the tchat server."
        welcome_msg = Message.make( MessageType.COMMAND, "server", text )
        state.broadcaster.send_to( address, welcome_msg.to_json() )

    def _handle_server_restart( self, state: ServerState ) -> None:
        if state.server.check_and_clear_restart_flag():
            msg = Message.make( MessageType.COMMAND, "server", _config.messages.server_online )
            state.broadcaster.cast( msg.to_json() )

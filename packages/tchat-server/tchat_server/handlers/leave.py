"""Handler for LEAVE messages — removes the user and notifies the room."""
from tchat_shared import logger
from tchat_shared.config import config as _config
from tchat_shared.message.message import LeaveMessage
from tchat_server.state.server_state import ServerState


class LeaveHandler:
    """Removes a disconnecting user from state and broadcasts their departure."""

    def handle( self, address: tuple[str, int], msg: LeaveMessage, state: ServerState ) -> None:
        """Remove the user; if they were registered, broadcast a leave message."""
        username = state.accounts.remove_user( address )
        if username is None:
            return
        self._broadcast_leave( state, username )

    def _broadcast_leave( self, state: ServerState, username: str ) -> None:
        leave_msg = LeaveMessage.make( username, _config.messages.broadcast_left )
        state.broadcaster.cast( leave_msg.to_json() )
        logger.server.message( leave_msg )

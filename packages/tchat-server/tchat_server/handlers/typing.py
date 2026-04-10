from tchat_shared.message.message import TypingMessage
from tchat_server.state.server_state import ServerState


class TypingHandler:
    def handle( self, address: tuple, msg: TypingMessage, state: ServerState ) -> None:
        username = state.accounts.get_username( address )
        if username is None:
            return
        self._broadcast_user_is_typing( username, address, msg, state )

    def _broadcast_user_is_typing( self, username: str, address: tuple, msg: TypingMessage, state: ServerState ) -> None:
        tp_msg = TypingMessage.make( username, msg.status )
        state.broadcaster.cast( tp_msg.to_json(), exclude=address )

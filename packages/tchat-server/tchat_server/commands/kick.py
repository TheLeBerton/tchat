from tchat_shared.message.message import Message
from tchat_shared.message.types import MessageType
from tchat_server.state.server_state import ServerState


class KickCommand:
    def execute( self, address: tuple, args: str, state: ServerState ) -> None:
        if not state.is_admin( address ):
            msg = Message.make( MessageType.COMMAND, "server", "Unauthorized: admin only." )
            state.send_to( address, msg.to_json() )
            return
        target = args.strip()
        if not target:
            msg = Message.make( MessageType.COMMAND, "server", "Usage: /kick <username>." )
            state.send_to( address, msg.to_json() )
            return
        target_account = state.find_by_username( target )
        if target_account is None:
            msg = Message.make( MessageType.COMMAND, "server", f"User '{ target }' not found." )
            state.send_to( address, msg.to_json() )
            return
        kicked_msg = Message.make( MessageType.KICK, "server", "You have been kicked." )
        state.send_to( target_account.address, kicked_msg.to_json() )
        state.ban( target_account.address )
        state.kick( target_account.address )
        confirm = Message.make( MessageType.COMMAND, "server", f"{ target } has been kicked." )
        state.send_to( address, confirm.to_json() )

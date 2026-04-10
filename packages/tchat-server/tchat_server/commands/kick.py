from tchat_shared.message.message import CommandMessage, KickMessage
from tchat_server.state.server_state import ServerState


class KickCommand:
    def execute( self, address: tuple, args: str, state: ServerState ) -> None:
        if not state.accounts.is_admin( address ):
            msg = CommandMessage.make( "server", "Unauthorized: admin only." )
            state.broadcaster.send_to( address, msg.to_json() )
            return
        target = args.strip()
        if not target:
            msg = CommandMessage.make( "server", "Usage: /kick <username>." )
            state.broadcaster.send_to( address, msg.to_json() )
            return
        target_account = state.accounts.find_by_username( target )
        if target_account is None:
            msg = CommandMessage.make( "server", f"User '{ target }' not found." )
            state.broadcaster.send_to( address, msg.to_json() )
            return
        kicked_msg = KickMessage.make( "server", "You have been kicked." )
        state.broadcaster.send_to( target_account.address, kicked_msg.to_json() )
        state.ban.ban( target_account.address )
        state.accounts.kick( target_account.address )
        confirm = CommandMessage.make( "server", f"{ target } has been kicked." )
        state.broadcaster.send_to( address, confirm.to_json() )

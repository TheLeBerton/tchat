from tchat_shared.config import config as _config
from tchat_shared.message.message import CommandMessage
from tchat_server.state.server_state import ServerState


class WhoOnlineCommand:
    def execute( self, address: tuple, args: str, state: ServerState ) -> None:
        usernames = state.accounts.get_all_usernames()
        online = ", ".join( usernames ) if usernames else _config.messages.nobody_online
        response = CommandMessage.make( "server", _config.messages.online_format.format( online ) )
        state.broadcaster.send_to( address, response.to_json() )

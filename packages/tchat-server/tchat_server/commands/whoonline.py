from tchat_shared.config import config as _config
from tchat_shared.message.message import Message
from tchat_shared.message.types import MessageType
from tchat_server.state.server_state import ServerState


class WhoOnlineCommand:
    def execute( self, address: tuple, args: str, state: ServerState ) -> None:
        usernames = state.get_all_usernames()
        online = ", ".join( usernames ) if usernames else _config.messages.nobody_online
        response = Message.make( MessageType.COMMAND, "server", _config.messages.online_format.format( online ) )
        state.send_to( address, response.to_json() )

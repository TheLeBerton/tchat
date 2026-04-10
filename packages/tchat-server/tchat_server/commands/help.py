from tchat_shared.config import config as _config
from tchat_shared.message.message import CommandMessage
from tchat_server.state.server_state import ServerState


class HelpCommand:

    def execute( self, address: tuple, args: str, state: ServerState ) -> None:
        response = CommandMessage.make( "server", _config.messages.help_text )
        state.broadcaster.send_to( address, response.to_json() )

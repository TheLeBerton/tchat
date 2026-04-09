from tchat_shared.config import config as _config
from tchat_shared.message.message import Message
from tchat_shared.message.types import MessageType
from tchat_server.state.server_state import ServerState


class HelpCommand:

    def execute( self, address: tuple, state: ServerState ) -> None:
        response = Message.make( MessageType.COMMAND, "server", _config.messages.help_text )
        state.send_to( address, response.to_json() )

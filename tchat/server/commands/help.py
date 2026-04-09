from tchat.config import config as _config
from tchat.message.message import Message
from tchat.message.types import MessageType
from tchat.server.state.server_state import ServerState


class HelpCommand:

    def execute( self, address: tuple, state: ServerState ) -> None:
        response = Message.make( MessageType.COMMAND, "server", _config.messages.help_text )
        state.send_to( address, response.to_json() )

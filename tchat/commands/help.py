from tchat.message.message import Message
from tchat.message.types import MessageType
from tchat.state.server_state import ServerState


class HelpCommand:
    HELP_TEXT = "/whoonline - who is online\n/status - server status\n/help - list commands\n/quit - disconnect"

    def execute( self, address: tuple, state: ServerState ) -> None:
        response = Message.make( MessageType.COMMAND, "server", self.HELP_TEXT )
        state.send_to( address, response.to_json() )

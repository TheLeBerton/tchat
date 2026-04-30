"""The /help command — sends the configured help text to the requesting user."""
from tchat_shared.config import config as _config
from tchat_shared.message.message import CommandMessage
from tchat_server.state.server_state import ServerState


class HelpCommand:
    """Replies with the help text from configuration."""

    def execute( self, address: tuple[str, int], args: str, state: ServerState ) -> None:
        """Send the help text to the user who issued the command."""
        response = CommandMessage.make( "server", _config.messages.help_text )
        state.broadcaster.send_to( address, response.to_json() )

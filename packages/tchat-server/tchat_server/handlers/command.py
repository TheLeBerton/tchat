"""Handler for COMMAND messages — delegates to the CommandRegistry."""
from tchat_shared import logger
from tchat_shared.message.message import Message, CommandMessage
from tchat_server.state.server_state import ServerState
from tchat_server.commands.base import CommandRegistry


class CommandHandler:
    """Dispatches command-type messages to the appropriate Command."""

    def __init__( self, commands: CommandRegistry ) -> None:
        self._commands = commands

    def handle( self, address: tuple[str, int], msg: Message, state: ServerState ) -> None:
        """Extract the command text and dispatch it via the command registry."""
        assert isinstance( msg, CommandMessage )
        self._commands.dispatch( address, msg.text, state )
        logger.server.message( msg )

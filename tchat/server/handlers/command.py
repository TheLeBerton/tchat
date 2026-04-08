from tchat import logger
from tchat.message.message import Message
from tchat.server.state.server_state import ServerState
from tchat.server.commands.base import CommandRegistry


class CommandHandler:
    def __init__( self, commands: CommandRegistry ) -> None:
        self._commands = commands

    def handle( self, address: tuple, msg: Message, state: ServerState ) -> None:
        self._commands.dispatch( address, msg.content, state )
        logger.message( msg )

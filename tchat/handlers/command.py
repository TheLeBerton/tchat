from tchat import logger
from tchat.message.message import Message
from tchat.message.types import MessageType
from tchat.state.server_state import ServerState
from tchat.commands.base import CommandRegistry
from tchat.exceptions import CommandError


class CommandHandler:
    def __init__( self, commands: CommandRegistry ) -> None:
        self._commands = commands

    def handle( self, address: tuple, msg: Message, state: ServerState ) -> None:
        try:
            self._commands.dispatch( address, msg.content, state )
        except CommandError as e:
            logger.error( str( e ) )
        logger.message( msg )

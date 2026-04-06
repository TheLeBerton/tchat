import logger
from chat.message.message import Message
from chat.message.types import MessageType
from chat.state.server_state import ServerState
from chat.commands.base import CommandRegistry
from exceptions import CommandError


class CommandHandler:
    def __init__( self, commands: CommandRegistry ) -> None:
        self._commands = commands

    def handle( self, address: tuple, msg: Message, state: ServerState ) -> None:
        try:
            self._commands.dispatch( address, msg.content, state )
        except CommandError as e:
            logger.error( str( e ) )
        logger.message( msg )

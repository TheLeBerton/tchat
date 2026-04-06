from chat.message.types import MessageType
from chat.state.server_state import ServerState
from chat.handlers.base import HandlerRegistry
from chat.handlers.join import JoinHandler
from chat.handlers.leave import LeaveHandler
from chat.handlers.chat import ChatHandler
from chat.handlers.command import CommandHandler
from chat.commands.base import CommandRegistry
from chat.commands.whoonline import WhoOnlineCommand
from chat.commands.help import HelpCommand


def build_registry() -> HandlerRegistry:
    commands = CommandRegistry()
    commands.register( "whoonline", WhoOnlineCommand() )
    commands.register( "help", HelpCommand() )
    registry = HandlerRegistry()
    registry.register( MessageType.JOIN, JoinHandler() )
    registry.register( MessageType.LEAVE, LeaveHandler() )
    registry.register( MessageType.CHAT, ChatHandler() )
    registry.register( MessageType.COMMAND, CommandHandler( commands ) )
    return registry


from tchat.message.types import MessageType
from tchat.state.server_state import ServerState
from tchat.handlers.base import HandlerRegistry
from tchat.handlers.join import JoinHandler
from tchat.handlers.leave import LeaveHandler
from tchat.handlers.chat import ChatHandler
from tchat.handlers.command import CommandHandler
from tchat.commands.base import CommandRegistry
from tchat.commands.whoonline import WhoOnlineCommand
from tchat.commands.help import HelpCommand
from tchat.commands.status import StatusCommand
from tchat.handlers.typing import TypingHandler


def build_registry() -> HandlerRegistry:
    commands = CommandRegistry()
    commands.register( "whoonline", WhoOnlineCommand() )
    commands.register( "help", HelpCommand() )
    commands.register( "status", StatusCommand() )
    registry = HandlerRegistry()
    registry.register( MessageType.JOIN, JoinHandler() )
    registry.register( MessageType.LEAVE, LeaveHandler() )
    registry.register( MessageType.CHAT, ChatHandler() )
    registry.register( MessageType.COMMAND, CommandHandler( commands ) )
    registry.register( MessageType.TYPING, TypingHandler() )
    return registry

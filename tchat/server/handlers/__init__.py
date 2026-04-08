from tchat.message.types import MessageType
from tchat.server.state.server_state import ServerState
from tchat.server.handlers.base import HandlerRegistry
from tchat.server.handlers.join import JoinHandler
from tchat.server.handlers.leave import LeaveHandler
from tchat.server.handlers.chat import ChatHandler
from tchat.server.handlers.command import CommandHandler
from tchat.server.commands.base import CommandRegistry
from tchat.server.commands.whoonline import WhoOnlineCommand
from tchat.server.commands.help import HelpCommand
from tchat.server.commands.status import StatusCommand
from tchat.server.handlers.typing import TypingHandler


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

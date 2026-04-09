from tchat_shared.message.types import MessageType
from tchat_server.state.server_state import ServerState
from tchat_server.handlers.base import HandlerRegistry
from tchat_server.handlers.join import JoinHandler
from tchat_server.handlers.leave import LeaveHandler
from tchat_server.handlers.chat import ChatHandler
from tchat_server.handlers.command import CommandHandler
from tchat_server.commands.base import CommandRegistry
from tchat_server.commands.whoonline import WhoOnlineCommand
from tchat_server.commands.help import HelpCommand
from tchat_server.commands.status import StatusCommand
from tchat_server.commands.kick import KickCommand
from tchat_server.handlers.typing import TypingHandler


def build_registry() -> HandlerRegistry:
    commands = CommandRegistry()
    commands.register( "whoonline", WhoOnlineCommand() )
    commands.register( "help", HelpCommand() )
    commands.register( "status", StatusCommand() )
    commands.register( "kick", KickCommand() )
    registry = HandlerRegistry()
    registry.register( MessageType.JOIN, JoinHandler() )
    registry.register( MessageType.LEAVE, LeaveHandler() )
    registry.register( MessageType.CHAT, ChatHandler() )
    registry.register( MessageType.COMMAND, CommandHandler( commands ) )
    registry.register( MessageType.TYPING, TypingHandler() )
    return registry

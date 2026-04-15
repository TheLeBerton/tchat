"""Client-side logger — formats and prints messages for the chat UI."""
from . import base
from .colors import Colors
from tchat_shared.config import config as _config
from tchat_shared.message.message import Message, MessageType, ChatMessage, CommandMessage

from tchat_shared import logger


def _tag( label: str, color: str ) -> str:
    """Build a colored tag string like ` > [LABEL]` for the left margin."""
    return f"{ Colors.WHITE.value }>{ Colors.RESET.value } { color }[{ label:^5}]{ Colors.RESET.value }"

def _emit( msg: str ) -> None:
    """Send a formatted string to the base logger in client mode."""
    base.log( msg, server_mode=False )

def info( msg: str ) -> None:
    """Print a system info line."""
    _emit( f"{ _tag('SYS', Colors.WHITE.value) } { msg }" )

def warning( msg: str ) -> None:
    """Print a warning line."""
    _emit( f"{ _tag('WARN', Colors.YELLOW.value) } { msg }" )

def error( msg: str ) -> None:
    """Print an error line."""
    _emit( f"{ _tag('ERR', Colors.RED.value) } { msg }" )

def message( msg: Message ) -> None:
    """Format and print a chat message based on its type."""
    if msg.type == MessageType.JOIN:
        _emit( f"{ _tag('JOIN', Colors.GREEN.value) } { msg.sender } { _config.messages.user_joined }" )
    elif msg.type == MessageType.LEAVE:
        _emit( f"{ _tag('LEAVE', Colors.YELLOW.value) } { msg.sender } { _config.messages.user_left }" )
    elif msg.type == MessageType.CHAT:
        color = base.get_user_color( msg.sender ).value
        assert isinstance( msg, ChatMessage )
        _emit( f"{ _tag('MSG', Colors.WHITE.value) } { color }{ Colors.BOLD.value }{ msg.sender }{ Colors.RESET.value }: { msg.text }" )
    elif msg.type == MessageType.COMMAND:
        assert isinstance( msg, CommandMessage )
        _emit( f"{ _tag( 'SERVER', Colors.MAGENTA.value ) } { msg.text }" )

def banner() -> None:
    """Print the tchat ASCII art banner."""
    chat = r"""
 _____ _   _  _____   _     _____ _____ _   _ _ _____   _____  _   _   ___ _____
|_   _| | | ||  ___| | |   |_   _|  _  | \ | ( )  ___| /  __ \| | | | / _ \_   _|
  | | | |_| || |__   | |     | | | | | |  \| |/\ `--.  | /  \/| |_| |/ /_\ \| |
  | | |  _  ||  __|  | |     | | | | | | . ` |  `--. \ | |    |  _  ||  _  || |
  | | | | | || |___  | |_____| |_\ \_/ / |\  | /\__/ / | \__/\| | | || | | || |
  \_/ \_| |_/\____/  \_____/\___/ \___/\_| \_/ \____/   \____/\_| |_/\_| |_/\_/

"""
    print( f"{ Colors.BLUE.value }{ chat }{ Colors.RESET.value }" )

def remove_line() -> None:
    """Erase the last printed line in the terminal (used after the user sends a message)."""
    print( "\033[1A\033[2K", end="", flush=True )

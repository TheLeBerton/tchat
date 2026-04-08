from . import base
from .colors import Colors
from tchat.message.message import Message, MessageType


def _tag( label: str, color: str ) -> str:
    return f"{ Colors.WHITE.value }>{ Colors.RESET.value } { color }[{ label:^5}]{ Colors.RESET.value }"

def _emit( msg: str ) -> None:
    base.log( msg, server_mode=False )

def info( msg: str ) -> None:
    _emit( f"{ _tag('SYS', Colors.WHITE.value) } { msg }" )

def warning( msg: str ) -> None:
    _emit( f"{ _tag('WARN', Colors.YELLOW.value) } { msg }" )

def error( msg: str ) -> None:
    _emit( f"{ _tag('ERR', Colors.RED.value) } { msg }" )

def message( msg: Message ) -> None:
    if msg.type == MessageType.JOIN:
        _emit( f"{ _tag('JOIN', Colors.GREEN.value) } { msg.sender } has entered the chat" )
    elif msg.type == MessageType.LEAVE:
        _emit( f"{ _tag('LEAVE', Colors.YELLOW.value) } { msg.sender } has left the chat" )
    elif msg.type == MessageType.CHAT:
        color = base.get_user_color( msg.sender ).value
        _emit( f"{ _tag('MSG', Colors.WHITE.value) } { color }{ Colors.BOLD.value }{ msg.sender }{ Colors.RESET.value }: { msg.content }" )
    elif msg.type == MessageType.COMMAND:
        _emit( f"{ _tag('CMD', Colors.BLUE.value) } { msg.content }" )

def banner() -> None:
    chat = r"""
 _____ _   _  _____   _     _____ _____ _   _ _ _____   _____  _   _   ___ _____
|_   _| | | ||  ___| | |   |_   _|  _  | \ | ( )  ___| /  __ \| | | | / _ \_   _|
  | | | |_| || |__   | |     | | | | | |  \| |/\ `--.  | /  \/| |_| |/ /_\ \| |
  | | |  _  ||  __|  | |     | | | | | | . ` |  `--. \ | |    |  _  ||  _  || |
  | | | | | || |___  | |_____| |_\ \_/ / |\  | /\__/ / | \__/\| | | || | | || |
  \_/ \_| |_/\____/  \_____/\___/ \___/\_| \_/ \____/   \____/\_| |_/\_| |_/\_/

"""
    print( f"{ Colors.BLUE.value }{ chat }{ Colors.RESET.value }" )

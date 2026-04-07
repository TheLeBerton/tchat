from pathlib import Path

from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import Completer, Completion

from chat.message.message import Message
from chat.message.types import MessageType
from chat.client.connection import Connection
from chat.client.receiver import ReceiveLoop


COMMANDS = [ "/whoonline", "/status", "/help", "/quit" ]


class CommandCompleter( Completer ):
    def get_completions( self, document, complete_event ):
        text = document.text_before_cursor
        if not text.startswith( "/" ):
            return
        for cmd in COMMANDS:
            if cmd.startswith( text ):
                yield Completion( cmd, start_position=-len( text ) )


class InputLoop:
    def __init__( self, connection: Connection, username: str ) -> None:
        self._connection = connection
        self._username = username

    def run( self, receiver: ReceiveLoop ) -> bool:
        history_file = Path.home() / ".tchat_history"
        session = PromptSession( f"[{ self._username }] > ", history=FileHistory( str( history_file ) ), completer=CommandCompleter(), complete_while_typing=True )
        with patch_stdout( raw=True ):
            while not receiver.connection_lost:
                try:
                    text = session.prompt()
                except ( EOFError, KeyboardInterrupt ):
                    if receiver.connection_lost:
                        return True
                    return False
                if text == "/quit":
                    return False
                elif text.startswith( "/" ):
                    self._connection.send( Message.make( MessageType.COMMAND, self._username, text[ 1: ] ) )
                else:
                    self._connection.send( Message.make( MessageType.CHAT, self._username, text ) )
        return True


import threading
import time
from pathlib import Path

from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import Completer, Completion

from tchat.message.message import Message
from tchat.message.types import MessageType
from tchat.client.connection import Connection
from tchat.client.receiver import ReceiveLoop


COMMANDS = [ "/whoonline", "/status", "/help", "/quit" ]


class CommandCompleter( Completer ):
    def get_completions( self, document, complete_event ):
        text = document.text_before_cursor
        if not text.startswith( "/" ):
            return
        for cmd in COMMANDS:
            if cmd.startswith( text ):
                yield Completion( cmd, start_position=-len( text ) )


class TypingNotifier:
    THROTTLE = 2.5
    IDLE_TIMEOUT = 4.0

    def __init__( self, connection: Connection, username: str ) -> None:
        self._connection = connection
        self._username = username
        self._last_sent = 0.0
        self._is_typing = False
        self._timer: threading.Timer | None = None
        self._lock = threading.Lock()

    def on_text_changed( self, _buffer ) -> None:
        now = time.monotonic()
        with self._lock:
            if self._timer:
                self._timer.cancel()
            if now - self._last_sent >= self.THROTTLE:
                self._send( "start" )
                self._last_sent = now
                self._is_typing = True
            self._timer = threading.Timer( self.IDLE_TIMEOUT, self._send_stop )
            self._timer.daemon = True
            self._timer.start()

    def on_message_sent( self ) -> None:
        with self._lock:
            if self._timer:
                self._timer.cancel()
                self._timer = None
            if self._is_typing:
                self._send( "stop" )
                self._is_typing = False
                self._last_sent = 0.0

    def _send_stop( self ) -> None:
        with self._lock:
            if self._is_typing:
                self._send( "stop" )
                self._is_typing = False
                self._last_sent = 0.0

    def _send( self, state: str ) -> None:
        try:
            self._connection.send( Message.make( MessageType.TYPING, self._username, state ) )
        except OSError:
            pass


class InputLoop:
    def __init__( self, connection: Connection, username: str ) -> None:
        self._connection = connection
        self._username = username

    def run( self, receiver: ReceiveLoop ) -> bool:
        history_file = Path.home() / ".tchat_history"
        notifier = TypingNotifier( self._connection, self._username )

        def bottom_toolbar():
            users = receiver.typing_tracker.get_typing_users()
            if not users:
                return ""
            names = ", ".join( users )
            return f" { names } est en train d'écrire..."

        session = PromptSession(
            f"[{ self._username }] > ",
            history=FileHistory( str( history_file ) ),
            completer=CommandCompleter(),
            complete_while_typing=True,
            bottom_toolbar=bottom_toolbar,
            refresh_interval=0.5,
        )

        def pre_run():
            session.app.current_buffer.on_text_changed += notifier.on_text_changed

        with patch_stdout( raw=True ):
            while not receiver.connection_lost:
                try:
                    text = session.prompt( pre_run=pre_run )
                except ( EOFError, KeyboardInterrupt ):
                    if receiver.connection_lost:
                        return True
                    return False
                notifier.on_message_sent()
                if text == "/quit":
                    return False
                elif text.startswith( "/" ):
                    self._connection.send( Message.make( MessageType.COMMAND, self._username, text[ 1: ] ) )
                else:
                    self._connection.send( Message.make( MessageType.CHAT, self._username, text ) )
        return True

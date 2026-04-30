"""Interactive input loop, typing notifications, and command completion for the client."""
import threading
import time
from pathlib import Path

from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import Completer, Completion


from tchat_shared import logger
from tchat_shared.message.message import ChatMessage, CommandMessage, TypingMessage
from tchat_client.connection import Connection
from tchat_client.receiver import ReceiveLoop


COMMANDS = [ "/whoonline", "/kick", "/status", "/help", "/quit" ]


class CommandCompleter( Completer ):
    """Tab-completes slash commands in the prompt_toolkit input."""

    def get_completions( self, document, complete_event ):
        """Yield completions for any input that starts with '/'."""
        text = document.text_before_cursor
        if not text.startswith( "/" ):
            return
        for cmd in COMMANDS:
            if cmd.startswith( text ):
                yield Completion( cmd, start_position=-len( text ) )


class TypingNotifier:
    """Sends throttled typing-start/stop events to the server as the user types."""

    THROTTLE = 2.5
    IDLE_TIMEOUT = 4.0

    def __init__( self, connection: Connection, username: str ) -> None:
        """Initialise with the connection, username, and internal timing state."""
        self._connection = connection
        self._username = username
        self._last_sent = 0.0
        self._is_typing = False
        self._timer: threading.Timer | None = None
        self._lock = threading.Lock()

    def on_text_changed( self, _buffer ) -> None:
        """Called on every keystroke; sends a throttled typing-start event."""
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
        """Cancel the idle timer and send a typing-stop event when a message is submitted."""
        with self._lock:
            if self._timer:
                self._timer.cancel()
                self._timer = None
            self._stop_typing()

    def _send_stop( self ) -> None:
        """Idle-timeout callback — send a typing-stop event if still marked as typing."""
        with self._lock:
            self._stop_typing()

    def _stop_typing( self ) -> None:
        # Caller must hold self._lock.
        if self._is_typing:
            self._send( "stop" )
            self._is_typing = False
            self._last_sent = 0.0

    def _send( self, state: str ) -> None:
        """Send a TypingMessage with the given state ('start' or 'stop'), silencing OS errors."""
        try:
            self._connection.send( TypingMessage.make( self._username, state ) )
        except OSError:
            pass


class InputLoop:
    """Prompt-toolkit based input loop that reads user input and sends messages."""

    def __init__( self, connection: Connection, username: str ) -> None:
        """Store the connection and username for use during the loop."""
        self._connection = connection
        self._username = username

    def run( self, receiver: ReceiveLoop ) -> bool:
        """Run the prompt loop; return True if the client should reconnect, False to exit."""
        history_file = Path.home() / ".tchat_history"
        notifier = TypingNotifier( self._connection, self._username )

        def bottom_toolbar() -> str:
            users = receiver.typing_tracker.get_typing_users()
            if not users:
                return ""
            names = ", ".join( users )
            return f" { names } is typing..."
        try:
            session = PromptSession(
                f"[{ self._username }] > ",
                history=FileHistory( str( history_file ) ),
                completer=CommandCompleter(),
                complete_while_typing=True,
                bottom_toolbar=bottom_toolbar,
                refresh_interval=0.5,
            )
        except KeyboardInterrupt:
            return receiver.connection_lost

        def pre_run() -> None:
            """Wire the typing notifier to the buffer's on_text_changed event before each prompt."""
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
                    self._connection.send( CommandMessage.make( self._username, text[ 1: ] ) )
                else:
                    msg = ChatMessage.make( self._username, text )
                    self._connection.send( msg )
                    logger.client.remove_line()
                    logger.client.message( msg )
        return True

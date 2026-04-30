"""Admin console that handles operator commands and restart signals."""
import os
import json
import threading
import time
import signal as _signal
from collections.abc import Callable
from datetime import datetime

from tchat_shared import logger
from tchat_shared.config import config as _config
from tchat_shared.message.message import CommandMessage
from tchat_server.state.server_state import ServerState
from tchat_server.commands.status import _STATUS_FILE


class AdminConsole:
    """Reads operator commands from stdin and handles server lifecycle actions."""

    def __init__( self, state: ServerState, stop_callback: Callable[[], None] ) -> None:
        self._state = state
        self._stop = stop_callback
        _signal.signal( _signal.SIGUSR1, self._on_signal_restart )

    def start( self ) -> None:
        thread = threading.Thread( target=self._loop, daemon=True )
        thread.start()

    def _loop( self ) -> None:
        while True:
            try:
                cmd = input()
            except ( EOFError, KeyboardInterrupt ):
                break
            self._handle( cmd.strip() )

    def _handle( self, cmd: str ) -> None:
        if cmd == "/quit":
            logger.server.info( "Server shutting down..." )
            msg = CommandMessage.make( "server", "Server shutting down..." )
            self._state.broadcaster.cast( msg.to_json() )
            time.sleep( 1 )
            self._stop()
            os._exit( 0 )
        elif cmd.startswith( "/restart" ):
            parts = cmd.split()
            delay = int( parts[ 1 ] ) if len( parts ) > 1 else 5
            self._restart( delay )
        else:
            logger.server.error( f"Unknown command: { cmd }" )

    def _restart( self, delay: int ) -> None:
        """Broadcast a restart warning and schedule a stop after delay seconds."""
        _STATUS_FILE.write_text( json.dumps( { "last_restart": datetime.now().isoformat() } ) )
        msg = CommandMessage.make( "server", _config.messages.server_restart.format( delay ) )
        self._state.broadcaster.cast( msg.to_json() )
        logger.server.info( f"Restarting in { delay }s..." )
        threading.Thread( target=self._delayed_stop, args=( delay, ), daemon=True ).start()

    def _delayed_stop( self, delay: int ) -> None:
        """Wait delay seconds, then broadcast and execute a server stop."""
        time.sleep( delay )
        msg = CommandMessage.make( "server", "Server restarting now." )
        self._state.broadcaster.cast( msg.to_json() )
        logger.server.info( "Restarting now." )
        time.sleep( 1 )
        self._stop()
        os._exit( 0 )

    def _on_signal_restart( self, sig, frame ) -> None:
        """SIGUSR1 handler — triggers a 10-second restart."""
        self._restart( 10 )

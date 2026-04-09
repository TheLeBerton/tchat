import os
import json
import threading
import time
import signal as _signal
from datetime import datetime
from pathlib import Path

from tchat import logger
from tchat.config import config as _config
from tchat.message.message import Message
from tchat.message.types import MessageType
from tchat.server.state.server_state import ServerState


class AdminConsole:
    def __init__( self, state: ServerState, stop_callback ) -> None:
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
            self._stop()
            os._exit( 0 )
        elif cmd.startswith( "/restart" ):
            parts = cmd.split()
            delay = int( parts[ 1 ] ) if len( parts ) > 1 else 5
            self._restart( delay )
        else:
            logger.server.error( f"Unknown command: { cmd }" )

    def _restart( self, delay: int ) -> None:
        status_file = Path( __file__ ).parents[ 3 ] / "server.status.json"
        status_file.write_text( json.dumps( { "last_restart": datetime.now().isoformat() } ) )
        msg = Message.make( MessageType.COMMAND, "server", _config.messages.server_restart.format( delay ) )
        self._state.broadcast( msg.to_json() )
        logger.server.info( f"Restarting in { delay }s..." )
        threading.Thread( target=self._delayed_stop, args=( delay, ), daemon=True ).start()

    def _delayed_stop( self, delay: int ) -> None:
        time.sleep( delay )
        msg = Message.make( MessageType.COMMAND, "server", "Server restarting now." )
        self._state.broadcast( msg.to_json() )
        logger.server.info( "Restarting now." )
        time.sleep( 1 )
        self._stop()
        os._exit( 0 )

    def _on_signal_restart( self, sig, frame ) -> None:
        self._restart( 10 )

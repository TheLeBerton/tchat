import os
import signal
import threading

from prompt_toolkit.patch_stdout import patch_stdout

from tchat import logger
from tchat.message.message import Message
from tchat.client.connection import Connection
from tchat.exceptions import MessageFramingError, InvalidMessageError


class ReceiveLoop:
    def __init__( self, connection: Connection ) -> None:
        self._connection = connection
        self._connection_lost = False

    @property
    def connection_lost( self ) -> bool:
        return self._connection_lost

    def start( self ) -> None:
        thread = threading.Thread( target=self._loop, daemon=True )
        thread.start()

    def _loop( self ) -> None:
        while True:
            try:
                raw = self._connection.receive()
                msg = Message.from_json( raw )
                logger.message( msg )
            except ( MessageFramingError, InvalidMessageError ):
                break
        print( "\n[ Connection closed ]" )
        self._connection_lost = True
        os.kill( os.getpid(), signal.SIGINT )

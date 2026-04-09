import os
import signal
import threading

from tchat_shared import logger
from tchat_shared.config import config as _config
from tchat_shared.message.message import Message
from tchat_shared.message.types import MessageType
from tchat_client.connection import Connection
from tchat_shared.exceptions import MessageFramingError, InvalidMessageError


class TypingTracker:
    EXPIRY = 2.0

    def __init__( self ) -> None:
        self._typing: dict[ str, threading.Timer ] = {}
        self._lock = threading.Lock()

    def set_typing( self, username: str, state: str ) -> None:
        with self._lock:
            if username in self._typing:
                self._typing[ username ].cancel()
            if state == "start":
                t = threading.Timer( self.EXPIRY, self._expire, args=[ username ] )
                t.daemon = True
                t.start()
                self._typing[ username ] = t
            else:
                self._typing.pop( username, None )

    def _expire( self, username: str ) -> None:
        with self._lock:
            self._typing.pop( username, None )

    def get_typing_users( self ) -> list[ str ]:
        with self._lock:
            return list( self._typing.keys() )


class ReceiveLoop:
    def __init__( self, connection: Connection ) -> None:
        self._connection = connection
        self._connection_lost = False
        self.typing_tracker = TypingTracker()

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
                if msg.type == MessageType.TYPING:
                    self.typing_tracker.set_typing( msg.sender, msg.content )
                else:
                    logger.client.message( msg )
            except ( MessageFramingError, InvalidMessageError ):
                break
        logger.client.warning( _config.messages.connection_closed )
        self._connection_lost = True
        os.kill( os.getpid(), signal.SIGINT )

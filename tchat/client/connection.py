import socket

from tchat.config import config
from tchat.message.message import Message
from tchat.message.framing import send_framed, receive_framed


class Connection:
    def __init__( self, host: str | None = None ) -> None:
        self._host = host or config.client.ip
        self._socket: socket.socket | None = None

    def connect( self ) -> None:
        self._socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        self._socket.connect( ( self._host, config.client.port ) )

    def close( self ) -> None:
        if self._socket:
            self._socket.close()

    def send( self, msg: Message ) -> None:
        assert self._socket is not None
        send_framed( self._socket, msg.to_json() )

    def receive( self ) -> str:
        assert self._socket is not None
        return receive_framed( self._socket )

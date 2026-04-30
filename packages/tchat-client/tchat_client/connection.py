"""TCP connection wrapper used by the client to communicate with the server."""
import socket

from tchat_shared.config import config
from tchat_shared.message.message import Message
from tchat_shared.message.framing import send_framed, receive_framed


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
        if self._socket is None:
            raise RuntimeError( "Not connected" )
        send_framed( self._socket, msg.to_json() )

    def receive( self ) -> str:
        if self._socket is None:
            raise RuntimeError( "Not connected" )
        return receive_framed( self._socket )

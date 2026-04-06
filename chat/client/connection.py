import socket

from config import config
from chat.message.message import Message
from chat.message.framing import send_framed, receive_framed


class Connection:
    def __init__( self ) -> None:
        self._socket: socket.socket | None = None


    def connect( self ) -> None:
        self._socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        self._socket.connect( ( config.client.ip, config.client.port ) )

    def close( self ) -> None:
        if self._socket:
            self._socket.close()

    def send( self, msg: Message ) -> None:
        assert self._socket is not None
        send_framed( self._socket, msg.to_json() )

    def receive( self ) -> str:
        assert self._socket is not None
        return receive_framed( self._socket )

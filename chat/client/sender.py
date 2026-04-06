from chat.message.message import Message
from chat.message.types import MessageType
from chat.client.connection import Connection
from chat.client.receiver import ReceiveLoop


class InputLoop:
    def __init__( self, connection: Connection, username: str ) -> None:
        self._connection = connection
        self._username = username

    def run( self, receiver: ReceiveLoop ) -> bool:
        while not receiver.connection_lost:
            try:
                text = input( "> " )
            except ( EOFError, KeyboardInterrupt ):
                return False
            if text == "/quit":
                return False
            elif text.startswith( "/" ):
                self._connection.send( Message.make( MessageType.COMMAND, self._username, text[ 1: ] ) )
            else:
                self._connection.send( Message.make( MessageType.CHAT, self._username, text ) )
        return True


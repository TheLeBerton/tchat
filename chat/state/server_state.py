import socket
import threading

from config import config as _config
from exceptions import UnknowUserError
from chat.message.framing import send_framed


class ServerState:
    def __init__( self ) -> None:
        self._users: dict[ tuple, str ] = {}
        self._connections: dict[ tuple, socket.socket ] = {}
        self._lock = threading.Lock()
        self._history: list[ str ] = []


    def add_connection( self, address: tuple, conn: socket.socket ) -> None:
        with self._lock:
            self._connections[ address ] = conn

    def add_user( self, address: tuple, username: str ) -> None:
        with self._lock:
            self._users[ address ] = username

    def remove_user( self, address: tuple ) -> str | None:
        with self._lock:
            self._connections.pop( address, None )
            return self._users.pop( address, None )

    def is_registered( self, address: tuple ) -> bool:
        with self._lock:
            return address in self._users

    def get_username( self, address: tuple ) -> str | None:
        with self._lock:
            return self._users.get( address )

    def get_all_usernames( self ) -> list[ str ]:
        with self._lock:
            users = []
            for user in self._users.values():
                if user.strip():
                    users.append( user )
            return users

    def broadcast( self, payload: str, exclude: tuple | None = None ) -> None:
        with self._lock:
            targets = list( self._connections.items() )
        for address, conn in targets:
            if address == exclude:
                continue
            try:
                send_framed( conn, payload )
            except OSError:
                pass

    def send_to( self, address: tuple, payload: str ) -> None:
        with self._lock:
            conn = self._connections.get( address )
        if conn is None:
            raise UnknowUserError( f"No connection for { address }" )
        send_framed( conn, payload )

    def add_to_history( self, payload: str ) -> None:
        with self._lock:
            self._history.append( payload )
            if len( self._history ) > _config.chat.history_size:
                self._history.pop( 0 )

    def get_history( self ) -> list[ str ]:
        with self._lock:
            return list( self._history )

    def is_username_taken( self, username: str ) -> bool:
        with self._lock:
            return username in self._users.values()

    def kick( self, address: tuple ) -> None:
        with self._lock:
            conn = self._connections.pop( address, None )
            self._users.pop( address, None)
        if conn:
            conn.close()

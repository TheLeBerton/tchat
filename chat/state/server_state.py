import socket
import threading
from datetime import datetime

from config import config as _config
from exceptions import UnknowUserError
from chat.message.framing import send_framed


class ServerState:
    def __init__( self ) -> None:
        self._users: dict[ tuple, str ] = {}
        self._connections: dict[ tuple, socket.socket ] = {}
        self._lock = threading.Lock()
        self._history: list[ str ] = []
        self._first_join_after_restart: bool = True
        self._start_time: datetime = datetime.now()
        self._message_count: int = 0


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
            self._message_count += 1
            if len( self._history ) > _config.chat.history_size:
                self._history.pop( 0 )

    def get_start_time( self ) -> datetime:
        return self._start_time

    def get_message_count( self ) -> int:
        with self._lock:
            return self._message_count

    def get_uptime( self ) -> str:
        delta = datetime.now() - self._start_time
        total = int( delta.total_seconds() )
        h, rem = divmod( total, 3600 )
        m, s = divmod( rem, 60 )
        return f"{ h }h { m }m { s }s"

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

    def check_and_clear_restart_flag( self ) -> bool:
        with self._lock:
            if self._first_join_after_restart:
                self._first_join_after_restart = False
                return True
            return False
        

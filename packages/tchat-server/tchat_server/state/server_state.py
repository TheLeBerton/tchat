import socket
import threading
from datetime import datetime

from tchat_shared import logger
from tchat_shared.config import config as _config
from tchat_shared.exceptions import UnknowUserError
from tchat_shared.message.framing import send_framed
from tchat_server.account import Account


class ServerState:
    def __init__( self ) -> None:
        self._accounts: list[ Account ] = []
        self._lock = threading.Lock()
        self._history: list[ str ] = []
        self._first_join_after_restart: bool = True
        self._start_time: datetime = datetime.now()
        self._message_count: int = 0
        self._banned: set[ str ] = set()

    def _find( self, address: tuple ) -> Account | None:
        for account in self._accounts:
            if account.address == address:
                return account
        return None

    def add_connection( self, address: tuple, conn: socket.socket ) -> None:
        with self._lock:
            self._accounts.append( Account( address, conn ) )

    def add_user( self, address: tuple, username: str ) -> None:
        with self._lock:
            account = self._find( address )
            if account:
                account.username = username

    def remove_user( self, address: tuple ) -> str | None:
        with self._lock:
            account = self._find( address )
            if account:
                self._accounts.remove( account )
                return account.username or None
            return None 

    def is_registered( self, address: tuple ) -> bool:
        with self._lock:
            account = self._find( address )
            return bool( account and account.username.strip() )

    def get_username( self, address: tuple ) -> str | None:
        with self._lock:
            account = self._find( address )
            if account:
                return account.username
            return None

    def get_all_usernames( self ) -> list[ str ]:
        with self._lock:
            usernames = []
            for account in self._accounts:
                if account.username.strip():
                    usernames.append( account.username )
            return usernames

    def broadcast( self, payload: str, exclude: tuple | None = None ) -> None:
        with self._lock:
            targets = [ a for a in self._accounts if a.address != exclude ]
        for account in targets:
            try:
                send_framed( account.connection, payload )
            except OSError:
                logger.server.error( f"Error broadcasting payload to account. address={ account.address } payload={ payload }" )

    def send_to( self, address: tuple, payload: str ) -> None:
        with self._lock:
            user = self._find( address )
        if user is None or user.connection is None:
            raise UnknowUserError( f"No connection for { address }" )
        send_framed( user.connection, payload )

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
            return any( a.username == username for a in self._accounts )

    def kick( self, address: tuple ) -> None:
        with self._lock:
            account = self._find( address )
            if account:
                self._accounts.remove( account )
        if account:
            account.connection.close()

    def check_and_clear_restart_flag( self ) -> bool:
        with self._lock:
            if self._first_join_after_restart:
                self._first_join_after_restart = False
                return True
            return False

    def set_admin( self, address: tuple ) -> None:
        with self._lock:
            account = self._find( address )
            if account:
                account.is_admin = True

    def is_admin( self, address: tuple ) -> bool:
        with self._lock:
            account = self._find( address )
            if account:
                return account.is_admin
            return False

    def find_by_username( self, username: str ) -> Account | None:
        with self._lock:
            for account in self._accounts:
                if account.username == username:
                    return account
        return None

    def ban( self, address: tuple ) -> None:
        with self._lock:
            self._banned.add( address[ 0 ] )

    def is_banned( self, address: tuple ) -> bool:
        with self._lock:
            return address[ 0 ] in self._banned

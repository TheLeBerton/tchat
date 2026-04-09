import socket
import threading


from tchat_server.account import Account


class AccountManager:
    def __init__( self ) -> None:
        self._lock: threading.Lock = threading.Lock()
        self._accounts: list[ Account ] = []


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

    def _find( self, address: tuple ) -> Account | None:
        for account in self._accounts:
            if account.address == address:
                return account
        return None

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

    def get_all( self ) -> list[ Account ]:
        with self._lock:
            return list( self._accounts )

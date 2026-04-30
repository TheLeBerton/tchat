"""Thread-safe registry of connected accounts."""
import socket
import threading


from tchat_server.account import Account


class AccountManager:
    """Stores and manages the list of connected Account objects."""

    def __init__( self ) -> None:
        """Initialise the lock and empty accounts list."""
        self._lock: threading.Lock = threading.Lock()
        self._accounts: list[ Account ] = []


    def add_connection( self, address: tuple[str, int], conn: socket.socket ) -> None:
        """Register a new socket connection before a username is known."""
        with self._lock:
            self._accounts.append( Account( address, conn ) )

    def add_user( self, address: tuple[str, int], username: str ) -> None:
        """Assign a username to an existing connection."""
        with self._lock:
            account = self._find( address )
            if account:
                account.username = username

    def remove_user( self, address: tuple[str, int] ) -> str | None:
        """Remove an account and return its username, or None if not found."""
        with self._lock:
            account = self._find( address )
            if account:
                self._accounts.remove( account )
                return account.username or None
            return None 

    def get_username( self, address: tuple[str, int] ) -> str | None:
        """Return the username for an address, or None if not found."""
        with self._lock:
            account = self._find( address )
            if account:
                return account.username
            return None

    def get_all_usernames( self ) -> list[ str ]:
        """Return a list of all non-empty usernames currently connected."""
        with self._lock:
            usernames = []
            for account in self._accounts:
                if account.username.strip():
                    usernames.append( account.username )
            return usernames

    def _find( self, address: tuple[str, int] ) -> Account | None:
        """Return the Account for an address, or None (caller must hold the lock)."""
        for account in self._accounts:
            if account.address == address:
                return account
        return None

    def is_username_taken( self, username: str ) -> bool:
        """Return True if username is already in use by a connected account."""
        with self._lock:
            return any( a.username == username for a in self._accounts )

    def kick( self, address: tuple[str, int] ) -> None:
        """Remove the account and close its socket."""
        with self._lock:
            account = self._find( address )
            if account:
                self._accounts.remove( account )
        if account:
            account.connection.close()

    def set_admin( self, address: tuple[str, int] ) -> None:
        """Grant admin privileges to the account at address."""
        with self._lock:
            account = self._find( address )
            if account:
                account.is_admin = True

    def is_admin( self, address: tuple[str, int] ) -> bool:
        """Return True if the account at address has admin privileges."""
        with self._lock:
            account = self._find( address )
            if account:
                return account.is_admin
            return False

    def find_by_username( self, username: str ) -> Account | None:
        """Return the Account with the given username, or None if not found."""
        with self._lock:
            for account in self._accounts:
                if account.username == username:
                    return account
        return None

    def get_all( self ) -> list[ Account ]:
        """Return a snapshot of all current accounts."""
        with self._lock:
            return list( self._accounts )

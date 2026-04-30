"""Thread-safe set of banned IP addresses."""
import threading


class BanManager:
    """Tracks banned IP addresses and answers ban-check queries."""

    def __init__( self ) -> None:
        """Initialise the lock and empty banned-IP set."""
        self._lock = threading.Lock()
        self._banned: set[ str ] = set()

    def ban( self, address: tuple[str, int] ) -> None:
        """Add the IP from address to the ban list."""
        with self._lock:
            self._banned.add( address[ 0 ] )

    def is_banned( self, address: tuple[str, int] ) -> bool:
        """Return True if the IP from address is banned."""
        with self._lock:
            return address[ 0 ] in self._banned

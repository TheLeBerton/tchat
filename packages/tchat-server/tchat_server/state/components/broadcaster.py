"""Sends framed payloads to one or all connected accounts."""
import threading

from tchat_shared import logger
from tchat_shared.exceptions import UnknowUserError
from tchat_shared.message.framing import send_framed
from tchat_server.state.components.account_manager import AccountManager

class Broadcaster:
    """Broadcasts or unicasts JSON payloads to connected clients."""

    def __init__( self, account_manager: AccountManager ) -> None:
        """Initialise with a reference to the AccountManager and a send lock."""
        self.accounts = account_manager
        self._lock: threading.Lock = threading.Lock()

    def cast( self, payload: str, exclude: tuple | None = None ) -> None:
        """Send payload to all connected accounts, optionally excluding one address."""
        with self._lock:
            targets = [ a for a in self.accounts.get_all() if a.address != exclude ]
        for account in targets:
            try:
                send_framed( account.connection, payload )
            except OSError:
                logger.server.error( f"Error broadcasting payload to account. address={ account.address } payload={ payload }" )

    def send_to( self, address: tuple, payload: str ) -> None:
        """Send payload to a single account by address; raises UnknowUserError if not found."""
        with self._lock:
            user = next( ( a for a in self.accounts.get_all() if a.address == address ), None )
        if user is None:
            raise UnknowUserError( f"No connection for { address }" )
        send_framed( user.connection, payload )

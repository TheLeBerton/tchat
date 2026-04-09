import threading

from tchat_shared import logger
from tchat_shared.exceptions import UnknowUserError
from tchat_shared.message.framing import send_framed
from tchat_server.state.components.account_manager import AccountManager

class Broadcaster:
    def __init__( self, account_manager: AccountManager ) -> None:
        self.accounts = account_manager
        self._lock: threading.Lock = threading.Lock()

    def cast( self, payload: str, exclude: tuple | None = None ) -> None:
        with self._lock:
            targets = [ a for a in self.accounts.get_all() if a.address != exclude ]
        for account in targets:
            try:
                send_framed( account.connection, payload )
            except OSError:
                logger.server.error( f"Error broadcasting payload to account. address={ account.address } payload={ payload }" )

    def send_to( self, address: tuple, payload: str ) -> None:
        user = next( ( a for a in self.accounts.get_all() if a.address == address ), None )
        if user is None:
            raise UnknowUserError( f"No connection for { address }" )
        send_framed( user.connection, payload )

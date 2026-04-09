import socket
import threading

from tchat_shared import logger
from tchat_shared.config import config
from tchat_server.state.server_state import ServerState
from tchat_server.handlers import build_registry
from tchat_server.session import ClientSession
from tchat_server.admin import AdminConsole


class ChatServer:
    def __init__( self ) -> None:
        self._state = ServerState()
        self._registry = build_registry()
        self._socket: socket.socket | None = None

    def start( self ) -> None:
        self._socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        self._socket.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
        self._socket.bind( ( config.server.ip, config.server.port ) )
        self._socket.listen( config.server.waiting_list_size )
        AdminConsole( self._state, self.stop ).start()
        logger.server.info( f"Listening on { config.server.ip }:{ config.server.port }" )
        self._accept_loop()

    def stop( self ) -> None:
        if self._socket:
            self._socket.close()

    def _accept_loop( self ) -> None:
        while True:
            try:
                if not self._socket:
                    break
                conn, address = self._socket.accept()
            except OSError:
                break
            self._state.accounts.add_connection( address, conn )
            logger.server.connected( address )
            session = ClientSession( conn, address, self._state, self._registry )
            thread = threading.Thread( target=session.run, daemon=True )
            thread.start()


def main() -> None:
    try:
        ChatServer().start()
    except Exception as e:
        print( f"[ SERVER ERROR ]: { e }" )

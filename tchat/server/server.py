import socket
import threading

from tchat import logger
from tchat.config import config
from tchat.state.server_state import ServerState
from tchat.handlers import build_registry
from tchat.server.session import ClientSession
from tchat.server.admin import AdminConsole


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
        logger.set_server_mode( True )
        logger.info( f"Listening on { config.server.ip }:{ config.server.port }" )
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
            self._state.add_connection( address, conn )
            logger.connected( address )
            session = ClientSession( conn, address, self._state, self._registry )
            thread = threading.Thread( target=session.run, daemon=True )
            thread.start()

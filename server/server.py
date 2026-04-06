import socket
import threading

from config import config
import logger

from . import state
from . import handler


def run() -> None:
    logger.set_server_mode( True )
    server = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    _connect_server( server )
    _start_connection_thread( server )
    server.close()

def _start_connection_thread( server: socket.socket ) -> None:
    thread = threading.Thread( target=_check_connections, args=( server, ), daemon=True )
    thread.start()
    thread.join()

def _check_connections( server: socket.socket ) -> None:
    while True:
        try:
            connection, address = server.accept()
            state.connections[ address ] = connection
            logger.connected( address )
            _start_thread( connection, address )
        except:
            break

def _connect_server( server: socket.socket ) -> None:
    server.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
    server.bind( ( config.server.ip, config.server.port ) )
    server.listen( config.server.waiting_list_size )
    logger.info( f"Waiting for connection on port { config.server.port }" )

def _start_thread( connection: socket.socket, address: tuple ) -> None:
    thread = threading.Thread( target=handler.recieve, args=( connection, address ), daemon = True )
    thread.start()



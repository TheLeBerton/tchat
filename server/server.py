import socket
import threading

from config import config
import logger


users: dict[ tuple, str ] = {}
connections: dict[ tuple, socket.socket ] = {}

def run() -> None:
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
            connections[ address ] = connection
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
    thread = threading.Thread( target=_recieve, args=( connection, address ), daemon = True )
    thread.start()

def _recieve( connection: socket.socket, address: tuple ) -> None:
    while True:
        try:
            data = connection.recv( 1024 )
            if not data:
                break
            _try_add_user( data, address )
            if address not in users:
                continue
            if "USER_NAME" in data.decode():
                continue
            _broadcast( data.decode(), address )
            logger.log( f"[ { users[ address ] } ]: { data.decode() }" )
        except:
            break
    connection.close()
    logger.disconnected( address )

def _try_add_user( data: bytes, address: tuple ) -> None:
    if address in users:
        return
    msg = data.decode()
    if "USER_NAME" in msg:
        parts = msg.split( ":" )
        user_name = parts[ 1 ][ 1: ]
        users[ address ] = user_name

def _broadcast( msg: str, sender_address: tuple ) -> None:
    for address, connection in connections.items():
        if address == sender_address:
            continue
        message = f"[ { users[ sender_address ] } ]: { msg }"
        connection.send( message.encode() )


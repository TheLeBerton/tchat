import socket
import threading

from config import config

users: dict[ tuple, str ] = {}

def run() -> None:
    server = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    _connect_server( server )
    connection, address = server.accept()
    print( f"Connected to { address }" )
    _start_thread( connection, address )
    while True:
        msg = input()
        if msg.lower() == "quit":
            break
        connection.send( msg.encode() )
    connection.close()
    server.close()

def _connect_server( server: socket.socket ) -> None:
    server.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
    server.bind( ( config.server.ip, config.server.port ) )
    server.listen( config.server.waiting_list_size )
    print( f"Waiting for connection on port { config.server.port }" )

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
            print( f"\n[ { users[ address ] } ] { data.decode() }" )
        except:
            break
    print( f"[ Connection closed ]" )

def _try_add_user( data: bytes, address: tuple ) -> None:
    if address in users:
        return
    msg = data.decode()
    if "USER_NAME" in msg:
        parts = msg.split( ":" )
        user_name = parts[ 1 ][ 1: ]
        users[ address ] = user_name

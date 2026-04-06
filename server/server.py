import socket
import threading

from config import config


def run() -> None:
    server = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    _connect_server( server )
    connection, address = server.accept()
    print( f"Connected to { address }" )
    _start_thread( connection )
    while True:
        msg = input()
        if msg.lower() == "quit":
            break
        connection.send( msg.encode() )
    connection.close()
    server.close()

def _connect_server( server: socket.socket ) -> None:
    server.bind( ( config.server.ip, config.server.port ) )
    server.listen( config.server.waiting_list_size )
    print( f"Waiting for connection on port { config.server.port }" )

def _start_thread( connection: socket.socket ) -> None:
    thread = threading.Thread( target=_recieve, args=( connection, ), daemon = True )
    thread.start()

def _recieve( connection: socket.socket ) -> None:
    while True:
        try:
            data = connection.recv( 1024 )
            if not data:
                break
            print( f"\n[ Ami ] { data.decode() }" )
        except:
            break
    print( f"[ Connection closed ]" )


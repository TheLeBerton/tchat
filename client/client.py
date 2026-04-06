import socket
import threading

from config import config


def run() -> None:
    client = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    client.connect( ( config.client.ip, config.client.port ) )
    _start_thread( client )
    user_name = input( "Enter user name: " )
    user_info: str = f"USER_NAME: { user_name }"
    client.send( user_info.encode() )
    while True:
        msg = input()
        if msg.lower() == "quit":
            break
        client.send( msg.encode() )
    client.close()

def _start_thread( connection: socket.socket ) -> None:
    thread = threading.Thread( target=_recieve, args=( connection, ), daemon = True )
    thread.start()

def _recieve( connection: socket.socket ) -> None:
    while True:
        try:
            data = connection.recv( 1024 )
            if not data:
                break
            print( f"\n[ Server ] { data.decode() }" )
        except:
            break
    print( f"[ Connection closed ]" )

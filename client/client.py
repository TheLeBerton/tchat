import sys
import socket
import threading
from datetime import datetime

from config import config
import logger
from message import Message, MessageType


def run() -> None:
    logger.banner()
    client = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    client.connect( ( config.client.ip, config.client.port ) )
    user_name = input( "Enter user name: " )
    _send_user_name( client, user_name )
    _start_thread( client )
    while True:
        msg = input( "> " )
        if msg.startswith( "/" ):
            if msg == "/quit":
                break
            _send_command( client, msg, user_name )
        else:
            _send_chat( client, msg, user_name )
    client.close()

def _send_command( client: socket.socket, msg: str, user_name: str ) -> None:
    cmd_msg = Message( type=MessageType.COMMAND, sender=user_name, content=msg[ 1: ], timestamp=datetime.now().strftime( "%H:%M" ) )
    client.send( cmd_msg.to_json().encode() )

def _send_chat( client: socket.socket, msg: str, user_name: str ) -> None:
    chat_msg = Message( type=MessageType.CHAT, sender=user_name, content=msg, timestamp=datetime.now().strftime( "%H:%M" ) )
    client.send( chat_msg.to_json().encode() )

def _send_user_name( client: socket.socket, user_name: str ) -> None:
    join_msg = Message( type=MessageType.JOIN, sender=user_name, content="", timestamp=datetime.now().strftime( "%H:%M" ) )
    client.send( join_msg.to_json().encode() )


def _start_thread( connection: socket.socket ) -> None:
    thread = threading.Thread( target=_recieve, args=( connection, ), daemon = True )
    thread.start()

def _recieve( connection: socket.socket ) -> None:
    while True:
        try:
            data = connection.recv( 1024 )
            if not data:
                break
            msg = Message.from_json( data.decode() )
            sys.stdout.write( "\r" )
            logger.message( msg )
            sys.stdout.write( "> " )
            sys.stdout.flush()
        except:
            break
    print( f"[ Connection closed ]" )


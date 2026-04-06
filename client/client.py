import os
import sys
import socket
import signal
import time
import threading
from datetime import datetime

from config import config
import logger
from message import Message, MessageType

_reconnect = False


def run() -> None:
    global _reconnect
    logger.banner()
    user_name = _get_username()
    while True:
        try:
            client = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            client.connect( ( config.client.ip, config.client.port ) )
            _send_user_name( client, user_name )
            _start_thread( client )
            while True:
                try:
                    msg = input( "> " )
                except ( EOFError, KeyboardInterrupt ):
                    break
                if msg.startswith( "/" ):
                    if msg == "/quit":
                        client.close()
                        return
                    _send_command( client, msg, user_name )
                else:
                    _send_chat( client, msg, user_name )
            client.close()
            if _reconnect:
                _reconnect = False
                logger.info( "Connection lost. Recconecting in 5s..." )
                time.sleep( 5 )
                continue
            return
        except OSError:
            logger.info( "Connection lost. Recconecting in 5s..." )
            time.sleep( 5 )

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
    global _reconnect
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
    _reconnect = True
    os.kill( os.getpid(), signal.SIGINT )

def _get_username() -> str:
    if os.path.exists( ".username" ):
        with open( ".username", "r" ) as f:
            return f.read().strip()
    name = input( "Enter user name: " )
    with open( ".username", "w") as f:
        f.write( name )
    return name


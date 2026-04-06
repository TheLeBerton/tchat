from datetime import datetime
import socket
import threading

from config import config
from message import Message, MessageType
import logger


users: dict[ tuple, str ] = {}
connections: dict[ tuple, socket.socket ] = {}

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
            msg = Message.from_json( data.decode() )
            if msg.type == MessageType.JOIN:
                users[ address ] = msg.sender
                join_broadcast = Message( type=MessageType.JOIN, sender=msg.sender, content="joined the chat", timestamp=datetime.now().strftime( "%H:%M" ) )
                logger.message( join_broadcast )
                _broadcast( join_broadcast.to_json(), address )
            if address not in users:
                continue
            if msg.type == MessageType.CHAT:
                chat_broadcast = Message(                                                                                                                                                                             
                    type=MessageType.CHAT,                                                                                                                                                                      
                    sender=users[ address ],                                                                                                                                                                    
                    content=msg.content,                                                                                                                                                                      
                    timestamp=datetime.now().strftime( "%H:%M" )                                                                                                                                                
                ) 
                logger.message( chat_broadcast )
                _broadcast( chat_broadcast.to_json(), address )
            elif msg.type == MessageType.COMMAND:
                if msg.content == "whoonline":
                    online = ", ".join( users.values() )
                    response = Message(
                        type=MessageType.COMMAND,
                        sender="server",
                        content=f"Online: { online }",
                        timestamp=datetime.now().strftime( "%H:%M" )                                                                                                                                                
                    )
                    connection.send( response.to_json().encode() )
                logger.message( msg )
        except Exception as e:
            print( e )
            break
    connection.close()
    logger.disconnected( address )

def _broadcast( msg: str, sender_address: tuple ) -> None:
    for address, connection in connections.items():
        if address == sender_address:
            continue
        connection.send( msg.encode() )


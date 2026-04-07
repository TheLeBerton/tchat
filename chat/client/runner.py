import time

import logger
from config import config as _config
from chat.version import VERSION
from chat.message.message import Message
from chat.message.types import MessageType
from chat.client.connection import Connection
from chat.client.identity import load_username, prompt_username
from chat.client.receiver import ReceiveLoop
from chat.client.sender import InputLoop


def run() -> None:
    logger.banner()
    username = prompt_username( load_username() )
    while True:
        conn = Connection()
        try:
            conn.connect()
        except OSError:
            logger.info( "Cannot connect. Retrying in 5s..." )
            time.sleep( 5 )
            continue
        version_msg = Message.from_json( conn.receive() )
        if version_msg.content != VERSION:
            logger.info( f"Version mismatch — serveur: { version_msg.content }, client: { VERSION }. Telecharge la derniere version." )
            conn.close()
            return
        conn.send( Message.make( MessageType.JOIN, username, "" ) )
        receiver = ReceiveLoop( conn )
        receiver.start()
        should_reconnect = InputLoop( conn, username ).run( receiver )
        conn.close()
        if should_reconnect:
            logger.info( "Connection lost. Reconnecting in 5s..." )
            time.sleep( _config.client.reconnect_delay )
            continue
        return

import time

from tchat import logger
from tchat.client.updater import check_and_update
from tchat.config import config as _config
from tchat.version import VERSION
from tchat.message.message import Message
from tchat.message.types import MessageType
from tchat.client.connection import Connection
from tchat.client.identity import load_username, prompt_username
from tchat.client.receiver import ReceiveLoop
from tchat.client.sender import InputLoop


def run( host: str | None = None ) -> None:
    check_and_update()
    logger.banner()
    username = prompt_username( load_username() )
    while True:
        conn = Connection( host=host )
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

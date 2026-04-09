import time

from tchat_shared import logger
from tchat_client.updater import check_and_update
from tchat_shared.config import config as _config
from tchat_shared.version import VERSION
from tchat_shared.message.message import Message
from tchat_shared.message.types import MessageType
from tchat_client.connection import Connection
from tchat_client.identity import load_username, prompt_username
from tchat_client.receiver import ReceiveLoop
from tchat_client.sender import InputLoop


def run( host: str | None = None ) -> None:
    check_and_update()
    logger.client.banner()
    username = prompt_username( load_username() )
    while True:
        conn = Connection( host=host )
        try:
            conn.connect()
        except OSError:
            logger.client.info( "Cannot connect. Retrying in 5s..." )
            time.sleep( 5 )
            continue
        version_msg = Message.from_json( conn.receive() )
        if version_msg.content != VERSION:
            logger.client.info( f"Version mismatch — serveur: { version_msg.content }, client: { VERSION }. Telecharge la derniere version." )
            conn.close()
            return
        conn.send( Message.make( MessageType.JOIN, username, "" ) )
        receiver = ReceiveLoop( conn )
        receiver.start()
        should_reconnect = InputLoop( conn, username ).run( receiver )
        if receiver.was_kicked:
            return
        conn.close()
        if should_reconnect:
            logger.client.info( "Connection lost. Reconnecting in 5s..." )
            time.sleep( _config.client.reconnect_delay )
            continue
        return

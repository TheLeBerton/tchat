from datetime import datetime

from .. import state
from . import broadcast
import logger
from message import Message, MessageType

def handle( address: tuple, msg: Message ) -> None:
    with state.lock:
        state.users[ address ] = msg.sender
    join_broadcast = Message( type=MessageType.JOIN, sender=msg.sender, content="joined the chat", timestamp=datetime.now().strftime( "%H:%M" ) )
    logger.message( join_broadcast )
    broadcast.cast( join_broadcast.to_json(), address )

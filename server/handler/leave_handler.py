from datetime import datetime

from .. import state
from . import broadcast
import logger
from message import Message, MessageType

def handle( address: tuple ) -> None:
    with state.lock:
        if address not in state.users:
            return
        leave_broadcast = Message( type=MessageType.LEAVE, sender=state.users[ address ], content="left the chat", timestamp=datetime.now().strftime( "%H:%M" ) )
        del state.users[ address ]
        del state.connections[ address ]
    logger.message( leave_broadcast )
    broadcast.cast( leave_broadcast.to_json(), address )

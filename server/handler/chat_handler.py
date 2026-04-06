from datetime import datetime

from .. import state
from . import broadcast
import logger
from message import Message, MessageType


def handle( address: tuple, msg: Message ) -> None:
    with state.lock:
        sender = state.users[ address ]
    chat_broadcast = Message(                                                                                                                                                                             
        type=MessageType.CHAT,                                                                                                                                                                      
        sender=sender,
        content=msg.content,                                                                                                                                                                      
        timestamp=datetime.now().strftime( "%H:%M" )                                                                                                                                                
    ) 
    logger.message( chat_broadcast )
    broadcast.cast( chat_broadcast.to_json(), address )

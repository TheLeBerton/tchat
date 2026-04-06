from datetime import datetime
import socket

from message import Message, MessageType
from .. import state


def whoonline( connection: socket.socket ) -> None:
    with state.lock:
        online = ", ".join( state.users.values() )
    response = Message(
        type=MessageType.COMMAND,
        sender="server",
        content=f"Online: { online }",
        timestamp=datetime.now().strftime( "%H:%M" )                                                                                                                                                
    )
    connection.send( response.to_json().encode() )


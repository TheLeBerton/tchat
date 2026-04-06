from .. import state
import logger


def cast( msg: str, sender_address: tuple ) -> None:
    with state.lock:
        connections = dict( state.connections )
    for address, connection in connections.items():
        if address == sender_address:
            continue
        try:
            connection.send( msg.encode() )
        except OSError as e:
            logger.error( f"Failed to send to { address }: { e }" )


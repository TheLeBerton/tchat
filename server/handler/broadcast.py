from .. import state


def cast( msg: str, sender_address: tuple ) -> None:
    with state.lock:
        connections = dict( state.connections )
    for address, connection in connections.items():
        if address == sender_address:
            continue
        connection.send( msg.encode() )

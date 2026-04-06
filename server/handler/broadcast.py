from .. import state


def cast( msg: str, sender_address: tuple ) -> None:
    for address, connection in state.connections.items():
        if address == sender_address:
            continue
        connection.send( msg.encode() )

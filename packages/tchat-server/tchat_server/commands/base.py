from typing import Protocol

from tchat_server.state.server_state import ServerState
from tchat_shared.exceptions import CommandError


class Command( Protocol ):
    def execute( self, address: tuple, args: str, state: ServerState ) -> None: ...


class CommandRegistry:
    def __init__( self ) -> None:
        self._commands: dict[ str, Command ] = {}

    def register( self, name: str, command: Command ) -> None:
        self._commands[ name ] = command

    def dispatch( self, address: tuple, content: str, state: ServerState ) -> None:
        name, _, args = content.partition( " " )
        command = self._commands.get( name )
        if command is None:
            raise CommandError( f"Unknown command: { name }" )
        command.execute( address, args, state )

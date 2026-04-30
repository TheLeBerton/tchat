"""Protocol and registry for server-side chat commands."""
from typing import Protocol

from tchat_server.state.server_state import ServerState
from tchat_shared.exceptions import CommandError


class Command( Protocol ):
    """Interface that every chat command must satisfy."""

    def execute( self, address: tuple[str, int], args: str, state: ServerState ) -> None:
        """Execute the command for the given user with the provided argument string."""
        ...


class CommandRegistry:
    """Maps command names to their Command implementations."""

    def __init__( self ) -> None:
        self._commands: dict[ str, Command ] = {}

    def register( self, name: str, command: Command ) -> None:
        self._commands[ name ] = command

    def dispatch( self, address: tuple[str, int], content: str, state: ServerState ) -> None:
        """Parse content as `name [args]` and execute the matching command; raises CommandError if unknown."""
        name, _, args = content.partition( " " )
        command = self._commands.get( name )
        if command is None:
            raise CommandError( f"Unknown command: { name }" )
        command.execute( address, args, state )

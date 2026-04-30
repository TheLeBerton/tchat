"""The /status command — reports server uptime, connected users, and message count."""
import json
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime

from tchat_shared import logger
from tchat_shared.config import config as _config
from tchat_shared.version import VERSION
from tchat_shared.message.message import CommandMessage
from tchat_server.state.server_state import ServerState


_STATUS_FILE = Path( __file__ ).parents[ 3 ] / "server.status.json"


@dataclass
class StatusData:
    """Plain data bag used to pass status fields between helper methods."""

    started: str = ""
    uptime: str = ""
    last_restart: str = "N/A"
    users: list[ str ] = field( default_factory=list )
    total_messages: int = 0


class StatusCommand:
    """Collects and formats server status, then replies to the requesting user."""

    def execute( self, address: tuple[str, int], args: str, state: ServerState ) -> None:
        """Gather status data and send the formatted report to the user."""
        data = self._get_data( state )
        lines = "\n".join( self._get_lines( data ) )
        msg = CommandMessage.make( "server", lines )
        state.broadcaster.send_to( address, msg.to_json() )

    def _get_data( self, state: ServerState ) -> StatusData:
        """Build a StatusData object from live server state and the status file."""
        data = StatusData()
        data.started = state.server.get_start_time().strftime( "%d %b %Y, %H:%M:%S" )
        data.uptime = state.server.get_uptime()
        data.users = state.accounts.get_all_usernames()
        data.total_messages = state.history.get_message_count()
        data.last_restart = "N/A"
        self._try_get_last_restart( data )
        return data

    def _try_get_last_restart( self, data: StatusData ) -> None:
        """Read the last restart timestamp from the status file into data, if available."""
        if _STATUS_FILE.exists():
            try:
                status_data = json.loads( _STATUS_FILE.read_text() )
                data.last_restart = datetime.fromisoformat( status_data[ "last_restart" ] ).strftime( "%d %b %Y, %H:%M:%S" )
            except ( KeyError, ValueError ) as e:
                logger.server.warning( f"Malformed server.status.json: { e }" )

    def _get_lines( self, data: StatusData ) -> list[ str ]:
        """Format the StatusData fields into a list of display lines."""
        lines = []
        lines.append( "[ SERVER STATUS ]" )
        lines.append( f"Version         : { VERSION }" )
        lines.append( f"Status          : Online" )
        lines.append( f"Address         : ( { _config.server.ip }, { _config.server.port } )" )
        lines.append( f"Started at      : { data.started }" )
        lines.append( f"Uptime          : { data.uptime }" )
        lines.append( f"Last restart    : { data.last_restart }" )
        users_len = len( data.users )
        users_names = f"( { ', '.join( data.users ) if data.users else 'none' } )"
        lines.append( f"Users online    : { users_len } { users_names }" )
        lines.append( f"Total messages  : [ { data.total_messages } / { _config.chat.history_size } ]" )
        return lines


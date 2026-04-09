import json
from pathlib import Path
from datetime import datetime

from tchat_shared.config import config as _config
from tchat_shared.version import VERSION
from tchat_shared.message.message import Message
from tchat_shared.message.types import MessageType
from tchat_server.state.server_state import ServerState


_STATUS_FILE = Path( __file__ ).parents[ 3 ] / "server.status.json"


class StatusData:
    started: str
    uptime: str
    last_restart: str
    users: list[ str ]
    total_messages: int


class StatusCommand:
    def execute( self, address: tuple, args: str, state: ServerState ) -> None:
        data = self._get_data( state )
        lines = "\n".join( self._get_lines( data ) )
        msg = Message.make( MessageType.COMMAND, "server", lines )
        state.broadcaster.send_to( address, msg.to_json() )

    def _get_data( self, state: ServerState ) -> StatusData:
        data = StatusData()
        data.started = state.server.get_start_time().strftime( "%d %b %Y, %H:%M:%S" )
        data.uptime = state.server.get_uptime()
        data.users = state.accounts.get_all_usernames()
        data.total_messages = state.history.get_message_count()
        data.last_restart = "N/A"
        self._try_get_last_restart( data )
        return data

    def _try_get_last_restart( self, data: StatusData ) -> None:
        if _STATUS_FILE.exists():
            try:
                status_data = json.loads( _STATUS_FILE.read_text() )
                data.last_restart = datetime.fromisoformat( status_data[ "last_restart" ] ).strftime( "%d %b %Y, %H:%M:%S" )
            except ( KeyError, ValueError ):
                pass

    def _get_lines( self, data: StatusData ) -> list[ str ]:
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


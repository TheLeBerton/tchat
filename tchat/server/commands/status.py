import json
from pathlib import Path

from tchat.message.message import Message
from tchat.message.types import MessageType
from tchat.server.state.server_state import ServerState

_STATUS_FILE = Path( __file__ ).parents[ 3 ] / "server.status.json"


class StatusCommand:
    def execute( self, address: tuple, state: ServerState ) -> None:
        started = state.get_start_time().strftime( "%d %b %Y, %H:%M:%S" )
        uptime = state.get_uptime()
        users = state.get_all_usernames()
        total_messages = state.get_message_count()

        last_restart = "N/A"
        if _STATUS_FILE.exists():
            try:
                data = json.loads( _STATUS_FILE.read_text() )
                from datetime import datetime
                last_restart = datetime.fromisoformat( data[ "last_restart" ] ).strftime( "%d %b %Y, %H:%M:%S" )
            except ( KeyError, ValueError ):
                pass

        lines = [
            "[ SERVER STATUS ]",
            f"Status        : Online",
            f"Started at    : { started }",
            f"Uptime        : { uptime }",
            f"Last restart  : { last_restart }",
            f"Users online  : { len( users ) }",
            f"Total messages: { total_messages }",
        ]
        response = Message.make( MessageType.COMMAND, "server", "\n".join( lines ) )
        state.send_to( address, response.to_json() )

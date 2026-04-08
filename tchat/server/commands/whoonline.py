from tchat.message.message import Message
from tchat.message.types import MessageType
from tchat.server.state.server_state import ServerState


class WhoOnlineCommand:
    def execute( self, address: tuple, state: ServerState ) -> None:
        usernames = state.get_all_usernames()
        online = ", ".join( usernames ) if usernames else "nobody"
        response = Message.make( MessageType.COMMAND, "server", f"Online: { online }" )
        state.send_to( address, response.to_json() )

from dataclasses import dataclass, asdict
import json

from .types import MessageType


@dataclass
class Message:
    type: MessageType
    sender: str
    content: str
    timestamp: str

    def to_json( self ) -> str:
        self_dict = asdict( self )
        self_dict[ "type" ] = self.type.value
        return json.dumps( self_dict )
    
    @classmethod
    def from_json( cls, data: str ) -> "Message":
        self_dict = json.loads( data )
        self_dict[ "type" ] = MessageType( self_dict[ "type" ] )
        return cls( **self_dict )

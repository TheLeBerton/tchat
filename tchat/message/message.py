from dataclasses import dataclass, asdict
from datetime import datetime
import json

from .types import MessageType
from tchat.exceptions import InvalidMessageError
from tchat.config import config as _config


@dataclass
class Message:
    type: MessageType
    sender: str
    content: str
    timestamp: str

    @classmethod
    def make( cls, type: MessageType, sender: str, content: str ) -> "Message":
        return cls(
            type=type,
            sender=sender,
            content=content,
            timestamp=datetime.now().strftime( _config.logger.timestamp_format )
        )

    def to_json( self ) -> str:
        self_dict = asdict( self )
        self_dict[ "type" ] = self.type.value
        return json.dumps( self_dict )

    @classmethod
    def from_json( cls, data: str ) -> "Message":
        try:
            self_dict = json.loads( data )
            self_dict[ "type" ] = MessageType( self_dict[ "type" ] )
            return cls( **self_dict )
        except ( json.JSONDecodeError, KeyError, ValueError ) as e:
            raise InvalidMessageError( f"Cannot parse message: { e }" ) from e

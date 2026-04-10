from dataclasses import dataclass, asdict
from datetime import datetime
import json

from .types import MessageType
from tchat_shared.exceptions import InvalidMessageError
from tchat_shared.config import config as _config


@dataclass
class Message:
    """Base class for all messages exchanged between client and server."""
    type: MessageType
    sender: str
    timestamp: str

    def to_json( self ) -> str:
        """Serialize the message to a JSON string"""
        self_dict = asdict( self )
        self_dict[ "type" ] = self.type.value
        return json.dumps( self_dict )

    @classmethod
    def from_json( cls, data: str ) -> "Message":
        """Deserialize a JSON string and return the appropriate message subclass."""
        try:
            _dict =  json.loads( data )
            msg_type = MessageType( _dict[ "type" ] )
            _dict[ "type" ] = msg_type
            if msg_type == MessageType.CHAT:
                return ChatMessage( **_dict )
            elif msg_type == MessageType.COMMAND:
                return CommandMessage( **_dict )
            elif msg_type == MessageType.JOIN:
                return JoinMessage( **_dict )
            elif msg_type == MessageType.KICK:
                return KickMessage( **_dict )
            elif msg_type == MessageType.LEAVE:
                return LeaveMessage( **_dict )
            elif msg_type == MessageType.TYPING:
                return TypingMessage( **_dict )
            elif msg_type == MessageType.VERSION:
                return VersionMessage( **_dict )
            raise InvalidMessageError( f"Cannot parse message." )
        except ( json.JSONDecodeError, KeyError, ValueError ) as e:
            raise InvalidMessageError( f"Cannot parse message: { e }" ) from e

    @staticmethod
    def _now() -> str:
        """Return the current time as a formatted string."""
        return datetime.now().strftime( _config.logger.timestamp_format )


@dataclass
class ChatMessage( Message ):
    """A chat message sent by a user."""
    text: str

    @classmethod
    def make( cls, sender: str, text: str ) -> "ChatMessage":
        """Create a new chat message with the current timestamp."""
        return cls( type=MessageType.CHAT, sender=sender, text=text, timestamp=Message._now() )


@dataclass
class CommandMessage( Message ):
    """A command response sent by the server."""
    text: str

    @classmethod
    def make( cls, sender: str, text: str ) -> "CommandMessage":
        """Create a new command message with the current timestamp."""
        return cls( type=MessageType.COMMAND, sender=sender, text=text, timestamp=Message._now() )


@dataclass
class JoinMessage( Message ):
    """Broadcast message sent when a user joins."""
    text: str

    @classmethod
    def make( cls, sender: str, text: str ) -> "JoinMessage":
        """Create a new join message with the current timestamp."""
        return cls( type=MessageType.JOIN, sender=sender, text=text, timestamp=Message._now() )


@dataclass
class LeaveMessage( Message ):
    """Broadcast message sent when a user leaves."""
    text: str

    @classmethod
    def make( cls, sender: str, text: str ) -> "LeaveMessage":
        """Create a new leave message with the current timestamp."""
        return cls( type=MessageType.LEAVE, sender=sender, text=text, timestamp=Message._now() )


@dataclass
class KickMessage( Message ):
    """A kick notification sent to a banned user."""
    reason: str

    @classmethod
    def make( cls, sender: str, reason: str ) -> "KickMessage":
        """Create a new kick message with the current timestamp."""
        return cls( type=MessageType.KICK, sender=sender, reason=reason, timestamp=Message._now() )


@dataclass
class TypingMessage( Message ):
    """A typing status notification ( start/stop )."""
    status: str

    @classmethod
    def make( cls, sender: str, status: str ) -> "TypingMessage":
        """Create a new typing message with the current timestamp."""
        return cls( type=MessageType.TYPING, sender=sender, status=status, timestamp=Message._now() )


@dataclass
class VersionMessage( Message ):
    """A version handshake message sent by the server on connect."""
    version: str

    @classmethod
    def make( cls, sender: str, version: str ) -> "VersionMessage":
        """Create a new version message with the current timestamp."""
        return cls( type=MessageType.VERSION, sender=sender, version=version, timestamp=Message._now() )


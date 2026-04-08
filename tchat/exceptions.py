class ChatError( Exception ):
    """Base class for all chat application errors."""


class MessageFramingError( ChatError ):
    """Raised when a framed message cannot be read ( connection closed mid-frame )."""


class InvalidMessageError( ChatError ):
    """Raised when a message cannot be parsed ( invalid JSON or unknown type )."""


class UnknowUserError( ChatError ):
    """Raised when an address is not registered in the server state."""


class CommandError( ChatError ):
    """Raised when a command is unknow or malformed."""


class ConfigError( ChatError ):
    """Raised when configuration is missing or invalid."""

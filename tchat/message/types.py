from enum import Enum


class MessageType( Enum ):
    CHAT = "chat"
    COMMAND = "command"
    JOIN = "join"
    LEAVE = "leave"
    VERSION = "version"

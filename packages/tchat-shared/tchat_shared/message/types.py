"""Defines the message types used in the tchat protocoll"""

from enum import Enum


class MessageType( Enum ):
    """
    Helps routing the messages on the server side.
    Helps formatting display on client/server side.
    """
    CHAT = "chat"
    COMMAND = "command"
    JOIN = "join"
    LEAVE = "leave"
    VERSION = "version"
    TYPING = "typing"
    KICK = "kick"

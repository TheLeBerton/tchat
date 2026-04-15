"""Defines the Account dataclass representing a connected client."""
import socket
from dataclasses import dataclass


@dataclass
class Account:
    """Holds the connection state for a single connected client."""
    address: tuple[ str, int ]
    connection: socket.socket
    username: str = ""
    is_admin: bool = False


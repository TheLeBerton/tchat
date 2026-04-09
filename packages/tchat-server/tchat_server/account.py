import socket
from dataclasses import dataclass


@dataclass
class Account:
    address: tuple[ str, int ]
    connection: socket.socket
    username: str = ""
    is_admin: bool = False


import socket


users: dict[ tuple, str ] = {}
connections: dict[ tuple, socket.socket ] = {}

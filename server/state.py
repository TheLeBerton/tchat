import socket
import threading

lock = threading.Lock()

users: dict[ tuple, str ] = {}
connections: dict[ tuple, socket.socket ] = {}

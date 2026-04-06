import struct
import socket

from exceptions import MessageFramingError


def send_framed( sock: socket.socket, payload: str ) -> None:
    data = payload.encode( "utf-8" )
    sock.sendall( struct.pack( ">I", len( data ) ) + data )

def receive_framed( sock: socket.socket ) -> str:
    header = _receive_exact( sock, 4 )
    length = struct.unpack( ">I", header )[ 0 ]
    body = _receive_exact( sock, length )
    return body.decode( "utf-8" )

def _receive_exact( sock: socket.socket, n: int ) -> bytes:
    buf = b""
    while len( buf ) < n:
        try:
            chunk = sock.recv( n - len( buf ) )
        except OSError:
            raise MessageFramingError( "Socket error or connection closed" )
        if not chunk:
            raise MessageFramingError( "Connection closed mid-frame" )
        buf += chunk
    return buf

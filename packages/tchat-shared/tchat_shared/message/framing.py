import struct
import socket

from tchat_shared.exceptions import MessageFramingError


def send_framed( sock: socket.socket, payload: str ) -> None:
    """
    Send a framed message through a socket.
    """
    data = payload.encode( "utf-8" )
    sock.sendall( struct.pack( ">I", len( data ) ) + data )

def receive_framed( sock: socket.socket ) -> str:
    """
    Receive a framed message from a socket.

    The message format is:
        [ 4 bytes length ][ payload ]

    The first 4 bytes indicate the size of the payload (big-endian).
    Then the exact number of bytes is read and decoded as UTF-8.
    """
    header = _receive_exact( sock, 4 )
    length = struct.unpack( ">I", header )[ 0 ]
    body = _receive_exact( sock, length )
    return body.decode( "utf-8" )

def _receive_exact( sock: socket.socket, n: int ) -> bytes:
    """
    This function keeps reading from the socket until n bytes are received.
    If the connection is closed or an error occurs before that, an 'MessageFramingError'
    is raised. Else the received data of length n is returned.
    """
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

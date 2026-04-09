import threading


class BanManager:
    def __init__( self ) -> None:
        self._lock = threading.Lock()
        self._banned: set[ str ] = set()

    def ban( self, address: tuple ) -> None:
        with self._lock:
            self._banned.add( address[ 0 ] )

    def is_banned( self, address: tuple ) -> bool:
        with self._lock:
            return address[ 0 ] in self._banned

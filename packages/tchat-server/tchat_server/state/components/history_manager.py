import threading

from tchat_shared.config import config as _config

class HistoryManager:
    def __init__( self ) -> None:
        self._history: list[ str ] = []
        self._message_count: int = 0
        self._lock = threading.Lock()

    def add_to_history( self, payload: str ) -> None:
        with self._lock:
            self._history.append( payload )
            self._message_count += 1
            if len( self._history ) > _config.chat.history_size:
                self._history.pop( 0 )

    def get_history( self ) -> list[ str ]:
        with self._lock:
            return list( self._history )

    def get_message_count( self ) -> int:
        with self._lock:
            return self._message_count

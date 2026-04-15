"""Keeps a rolling buffer of recent chat payloads and a total message counter."""
import threading

from tchat_shared.config import config as _config

class HistoryManager:
    """Thread-safe rolling history of serialised message payloads."""

    def __init__( self ) -> None:
        """Initialise the history list, message counter, and lock."""
        self._history: list[ str ] = []
        self._message_count: int = 0
        self._lock = threading.Lock()

    def add_to_history( self, payload: str ) -> None:
        """Append a payload and drop the oldest entry if history is full."""
        with self._lock:
            self._history.append( payload )
            self._message_count += 1
            if len( self._history ) > _config.chat.history_size:
                self._history.pop( 0 )

    def get_history( self ) -> list[ str ]:
        """Return a snapshot of the current history buffer."""
        with self._lock:
            return list( self._history )

    def get_message_count( self ) -> int:
        """Return the total number of messages received since server start."""
        with self._lock:
            return self._message_count

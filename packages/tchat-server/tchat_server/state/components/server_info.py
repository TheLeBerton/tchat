"""Tracks server start time and the first-join-after-restart flag."""
from datetime import datetime
import threading


class ServerInfo:
    """Stores uptime data and a one-shot flag for post-restart behaviour."""

    def __init__( self ) -> None:
        """Record the start time and initialise the restart flag."""
        self._lock: threading.Lock = threading.Lock()
        self._start_time: datetime = datetime.now()
        self._first_join_after_restart: bool = True

    def get_start_time( self ) -> datetime:
        """Return the datetime when the server started."""
        return self._start_time

    def get_uptime( self ) -> str:
        """Return a human-readable uptime string like '2h 15m 30s'."""
        delta = datetime.now() - self._start_time
        total = int( delta.total_seconds() )
        h, rem = divmod( total, 3600 )
        m, s = divmod( rem, 60 )
        return f"{ h }h { m }m { s }s"

    def check_and_clear_restart_flag( self ) -> bool:
        """Return True once after a restart, then False on all subsequent calls."""
        with self._lock:
            if self._first_join_after_restart:
                self._first_join_after_restart = False
                return True
            return False

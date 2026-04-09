from datetime import datetime
import threading


class ServerInfo:
    def __init__( self ) -> None:
        self._lock: threading.Lock = threading.Lock()
        self._start_time: datetime = datetime.now()
        self._first_join_after_restart: bool = True

    def get_start_time( self ) -> datetime:
        return self._start_time

    def get_uptime( self ) -> str:
        delta = datetime.now() - self._start_time
        total = int( delta.total_seconds() )
        h, rem = divmod( total, 3600 )
        m, s = divmod( rem, 60 )
        return f"{ h }h { m }m { s }s"

    def check_and_clear_restart_flag( self ) -> bool:
        with self._lock:
            if self._first_join_after_restart:
                self._first_join_after_restart = False
                return True
            return False

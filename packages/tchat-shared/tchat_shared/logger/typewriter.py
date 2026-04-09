import time
import sys


def write( msg: str, delay: float = 0.1 ) -> None:
    for char in msg:
        sys.stdout.write( char )
        sys.stdout.flush()
        time.sleep( delay )
    print()

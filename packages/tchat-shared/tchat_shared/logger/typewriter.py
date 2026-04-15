"""Typewriter effect for terminal output."""
import time
import sys


def write( msg: str, delay: float = 0.1 ) -> None:
    """Print msg character by character with a delay between each one."""
    for char in msg:
        sys.stdout.write( char )
        sys.stdout.flush()
        time.sleep( delay )
    print()

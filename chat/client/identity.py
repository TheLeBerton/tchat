import re
from pathlib import Path

USERNAME_FILE = Path.home() / ".tchat_username"
_USERNAME_PATTERN = re.compile( r"^[a-zA-Z0-9_]{2,20}$" )


def _validate( name: str ) -> str | None:
    """Returns an error message if invalid, None if valid."""
    if len( name ) < 2:
        return "Username must be at least 2 characters."
    if len( name ) > 20:
        return "Username must be at most 20 characters."
    if not _USERNAME_PATTERN.match( name ):
        return "Username can only contain letters, digits, and underscores."
    return None


def load_username() -> str | None:
    if USERNAME_FILE.exists():
        return USERNAME_FILE.read_text().strip()
    return None

def save_username( name: str ) -> None:
    USERNAME_FILE.write_text( name )

def prompt_username( saved: str | None = None ) -> str:
    if saved:
        print( f"Saved username: \033[1m{ saved }\033[0m — press Enter to use it, or type a new one." )
    while True:
        raw = input( "Username: " ).strip()
        if raw == "" and saved:
            return saved
        name = raw or saved or ""
        error = _validate( name )
        if error:
            print( f"\033[31m{ error }\033[0m" )
            continue
        save_username( name )
        return name

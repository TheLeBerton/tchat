from pathlib import Path

USERNAME_FILE = Path.home() / ".tchat_username"


def load_username() -> str | None:
    if USERNAME_FILE.exists():
        return USERNAME_FILE.read_text().strip()
    return None

def save_username( name: str ) -> None:
    USERNAME_FILE.write_text( name )

def prompt_username() -> str:
    name = input( "Enter username: " )
    save_username( name )
    return name

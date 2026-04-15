"""Loads and exposes the application configuration from ~/.config/tchat/config.toml."""
import shutil
import tomllib
from dataclasses import dataclass
from pathlib import Path

from tchat_shared.exceptions import ConfigError


_CONFIG_DIR = Path.home() / ".config" / "tchat"
_CONFIG_PATH = _CONFIG_DIR / "config.toml"
_TEMPLATE_PATH = Path( __file__ ).parent / "config.toml"


@dataclass
class ServerConfig:
    """Network settings for the server."""
    ip: str
    port: int
    waiting_list_size: int


@dataclass
class ClientConfig:
    """Network settings for the client."""
    ip: str
    port: int
    reconnect_delay: int

@dataclass
class LoggerConfig:
    """Controls logging behaviour — typewriter effect and file output."""
    typewriter: bool
    typewriter_delay: float
    timestamp_format: str
    log_to_file: bool
    log_file: str

@dataclass
class ChatConfig:
    """Limits applied to chat messages."""
    max_message_length: int
    history_size: int

@dataclass
class ColorsConfig:
    """ANSI color codes used by the logger."""
    join: str
    leave: str
    server: str
    timestamp: str
    error: str
    info: str


@dataclass
class MessagesConfig:
    """Configurable user-facing strings."""
    server_restart: str
    user_joined: str
    user_left: str
    username_taken: str
    server_online: str
    broadcast_joined: str
    broadcast_left: str
    help_text: str
    online_format: str
    nobody_online: str
    connection_closed: str
    welcome_text: str


@dataclass
class AdminConfig:
    """Whitelisted admin usernames and IP addresses."""
    usernames: list[ str ]
    ips: list[ str ]


@dataclass
class Config:
    """Root configuration object aggregating all sub-sections."""
    server: ServerConfig
    client: ClientConfig
    logger: LoggerConfig
    chat: ChatConfig
    colors: ColorsConfig
    messages: MessagesConfig
    admin: AdminConfig


def _ensure_config() -> None:
    """Copy the bundled config template to ~/.config/tchat/ if it does not exist yet."""
    if not _CONFIG_PATH.exists():
        _CONFIG_DIR.mkdir( parents=True, exist_ok=True )
        shutil.copy( _TEMPLATE_PATH, _CONFIG_PATH )
        print( f"Config created at { _CONFIG_PATH }" )
        print( f"--> Edit it to set your server IP ( client.ip )." )


def _load_config() -> Config:
    """Read config.toml and return a fully populated Config instance."""
    _ensure_config()
    try:
        with open( _CONFIG_PATH, "rb" ) as f:
            data = tomllib.load( f )
    except OSError as e:
        raise ConfigError( f"Cannot read config: { e }" ) from e
    data[ "messages" ].setdefault( "welcome_text", "Welcome to the system." )
    admin_data = data.get( "admin", { "usernames": [], "ips": [] } )
    return Config(
            server=ServerConfig( **data[ "server" ] ),
            client=ClientConfig( **data[ "client" ] ),
            logger=LoggerConfig( **data[ "logger" ] ),
            chat=ChatConfig( **data[ "chat" ] ),
            colors=ColorsConfig( **data[ "colors" ] ),
            messages=MessagesConfig( **data[ "messages" ] ),
            admin=AdminConfig( **admin_data )
    )

config = _load_config()

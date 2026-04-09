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
    ip: str
    port: int
    waiting_list_size: int


@dataclass
class ClientConfig:
    ip: str
    port: int
    reconnect_delay: int

@dataclass
class LoggerConfig:
    typewriter: bool
    typewriter_delay: float
    timestamp_format: str
    log_to_file: bool
    log_file: str

@dataclass
class ChatConfig:
    max_message_length: int
    history_size: int

@dataclass
class ColorsConfig:
    join: str
    leave: str
    server: str
    timestamp: str
    error: str
    info: str


@dataclass
class MessagesConfig:
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


@dataclass
class Config:
    server: ServerConfig
    client: ClientConfig
    logger: LoggerConfig
    chat: ChatConfig
    colors: ColorsConfig
    messages: MessagesConfig


def _ensure_config() -> None:
    if not _CONFIG_PATH.exists():
        _CONFIG_DIR.mkdir( parents=True, exist_ok=True )
        shutil.copy( _TEMPLATE_PATH, _CONFIG_PATH )
        print( f"Config created at { _CONFIG_PATH }" )
        print( f"--> Edit it to set your server IP ( client.ip )." )


def _load_config() -> Config:
    _ensure_config()
    try:
        with open( _CONFIG_PATH, "rb" ) as f:
            data = tomllib.load( f )
    except OSError as e:
        raise ConfigError( f"Cannot read config: { e }" ) from e
    return Config(
            server=ServerConfig( **data[ "server" ] ),
            client=ClientConfig( **data[ "client" ] ),
            logger=LoggerConfig( **data[ "logger" ] ),
            chat=ChatConfig( **data[ "chat" ] ),
            colors=ColorsConfig( **data[ "colors" ] ),
            messages=MessagesConfig( **data[ "messages" ] )
    )

config = _load_config()

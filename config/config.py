from dataclasses import dataclass
import tomllib


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
class Config:
    server: ServerConfig
    client: ClientConfig
    logger: LoggerConfig
    chat: ChatConfig
    colors: ColorsConfig

def _load_config( path: str="config/config.toml" ) -> Config:
    with open( path, "rb" ) as f:
        data = tomllib.load( f )
    return Config(
            server=ServerConfig( **data[ "server" ] ),
            client=ClientConfig( **data[ "client" ] ),
            logger=LoggerConfig( **data[ "logger" ] ),
            chat=ChatConfig( **data[ "chat" ] ),
            colors=ColorsConfig( **data[ "colors" ] ),
    )

config = _load_config()

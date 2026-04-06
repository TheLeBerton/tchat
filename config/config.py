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


@dataclass
class Config:
    server: ServerConfig
    client: ClientConfig

def _load_config( path: str="config/config.toml" ) -> Config:
    with open( path, "rb" ) as f:
        data = tomllib.load( f )
    return Config(
            server=ServerConfig( **data[ "server" ] ),
            client=ClientConfig( **data[ "client" ] )
    )

config = _load_config()

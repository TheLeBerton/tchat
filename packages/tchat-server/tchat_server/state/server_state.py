"""Aggregates all server-state components into a single object."""
from tchat_server.state.components import BanManager, HistoryManager, ServerInfo, AccountManager, Broadcaster


class ServerState:
    """Central state passed to every handler — holds accounts, history, bans, and broadcaster."""

    def __init__( self ) -> None:
        self.ban: BanManager = BanManager()
        self.history: HistoryManager = HistoryManager()
        self.server: ServerInfo = ServerInfo()
        self.accounts: AccountManager = AccountManager()
        self.broadcaster: Broadcaster = Broadcaster( self.accounts )


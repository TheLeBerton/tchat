from tchat_server.state.components import BanManager, HistoryManager, ServerInfo, AccountManager, Broadcaster


class ServerState:
    def __init__( self ) -> None:
        self.ban: BanManager = BanManager()
        self.history: HistoryManager = HistoryManager()
        self.server: ServerInfo = ServerInfo()
        self.accounts: AccountManager = AccountManager()
        self.broadcaster: Broadcaster = Broadcaster( self.accounts )


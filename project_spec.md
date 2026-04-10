# tchat — Project Structure

```
packages/
├── tchat-shared/               ← protocol, config, logger, exceptions
│   └── tchat_shared/
│       ├── message/
│       │   ├── framing.py      ← length-prefixed TCP framing
│       │   ├── message.py      ← Message dataclass, to_json / from_json
│       │   └── types.py        ← MessageType enum
│       ├── logger/             ← client + server loggers, colors, typewriter
│       ├── config/             ← config.toml loader
│       ├── exceptions.py
│       └── version.py
│
├── tchat-server/
│   └── tchat_server/
│       ├── handlers/           ← one handler per message type (join, chat, leave…)
│       ├── commands/           ← one command per file (whoonline, kick, help…)
│       ├── state/              ← ServerState
│       │   └── components/     ← AccountManager, Broadcaster, BanManager…
│       ├── server.py           ← ChatServer, accept loop
│       ├── session.py          ← ClientSession, per-client message loop
│       ├── admin.py            ← AdminConsole (server-side terminal)
│       └── account.py          ← Account dataclass
│
└── tchat-client/
    └── tchat_client/
        ├── runner.py           ← entry point, connect + reconnect loop
        ├── connection.py       ← TCP Connection wrapper
        ├── receiver.py         ← ReceiveLoop + TypingTracker (background thread)
        ├── sender.py           ← InputLoop + TypingNotifier + CommandCompleter
        ├── identity.py         ← load / save username
        └── updater.py          ← auto-update on launch
```

---

# tchat — Data Flow (MVP)

```
Client                              Server
  │                                   │
  │── TCP connect ──────────────────► │
  │◄─ VERSION(server_version) ────────│
  │                                   │
  │── JOIN(username) ───────────────► JoinHandler
  │                                   └── AccountManager.add_user()
  │                                   └── Broadcaster.cast(JOIN) ──► all clients
  │                                   │
  │── CHAT(text) ───────────────────► ChatHandler
  │                                   └── Broadcaster.cast(CHAT) ──► all clients
  │                                   │
  │── COMMAND(/whoonline) ──────────► CommandHandler
  │◄─ COMMAND(response) ──────────────│
  │                                   │
  │── TYPING(start/stop) ───────────► TypingHandler
  │                                   └── Broadcaster.cast(TYPING) ► all clients
  │                                   │
  │── disconnect ───────────────────► LeaveHandler
  │                                   └── AccountManager.remove_user()
  │                                   └── Broadcaster.cast(LEAVE) ─► all clients
```

# Architecture

## System

Raspberry Pi (Tailscale) runs the server. Clients connect over TCP.

```
[client] ──TCP── [ChatServer on RPi]
[client] ──TCP──┘
```

## Packages

- `tchat-shared` — protocol (Message, framing, types), config, logger, exceptions
- `tchat-server` — server logic
- `tchat-client` — client logic

## Server

```
ChatServer          accept loop, one thread per client
ClientSession       per-client message loop → dispatches to handlers
handlers/           one file per message type (join, chat, leave, command, typing)
commands/           one file per /command (whoonline, kick, help, status)
ServerState         holds all state, composed of:
  AccountManager    list of connected users (address → username, socket)
  Broadcaster       send a message to all / one
  BanManager        banned IPs
  HistoryManager    recent messages
  ServerInfo        server metadata (start time, etc.)
AdminConsole        server-side terminal (/quit, /restart)
Account             Account dataclass (address, socket, username, is_admin)
```

## Client

```
runner.py       entry point — connect, version check, reconnect loop
Connection      TCP socket wrapper
ReceiveLoop     background thread — reads messages, prints them
TypingTracker   tracks who is currently typing (used by ReceiveLoop)
InputLoop       main thread — prompt_toolkit input, sends messages
TypingNotifier  fires TYPING start/stop while user types
```

## Data flow

```
client sends JOIN(username)
  → JoinHandler → AccountManager.add_user() → Broadcaster.cast(JOIN)

client sends CHAT(text)
  → ChatHandler → Broadcaster.cast(CHAT)

client sends COMMAND(/whoonline)
  → CommandHandler → WhoonlineCommand → Broadcaster.send_to(response)

client disconnects
  → MessageFramingError → LeaveHandler → AccountManager.remove_user() → Broadcaster.cast(LEAVE)
```

## Message format

```json
{ "type": "chat", "sender": "leberton", "content": "hello", "timestamp": "14:32" }
```

Types: `join` `leave` `chat` `command` `typing` `kick` `version`

Framing: 4-byte big-endian length prefix + UTF-8 JSON payload.

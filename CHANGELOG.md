# Changelog

## v0.18.5
- Refactor: split `ServerState` into components (`AccountManager`, `BanManager`, `HistoryManager`, `ServerInfo`, `Broadcaster`)

## v0.18.4
- Fix: `JoinError` in `ClientSession`, ban by IP, add `authorized` check

## v0.18.3
- Fix: display kick message to kicked user

## v0.18.2
- Fix: catch `KeyboardInterrupt` in `PromptSession` (sender)

## v0.18.1
- Fix: ban system — kicked users cannot reconnect

## v0.18.0
- Feat: admin user support with `/kick` command

## v0.17.0
- Refactor: replace `users`/`connections` dicts with `Account` list in `ServerState`

## v0.16.3 — v0.16.0
- Feat: welcome message on join
- Fix: systemd service uses `uv run`
- Fix: version push sets upstream
- Feat: easy install via PyPI (`pip install tchat-client`)

## v0.15.x and below
- Feat: typing indicator
- Feat: input history and tab completion
- Feat: `/status`, `/help`, `/whoonline` commands
- Feat: message history replayed to new clients
- Feat: duplicate username rejection
- Feat: auto-reconnect on connection loss
- Feat: versioning + version handshake between client and server
- Feat: admin console (`/quit`, `/restart`)
- Refactor: migrate to `uv` workspace with separate `server`/`client`/`shared` packages
- Refactor: handler modules, structured messages, config system
- Feat: basic server + client working together

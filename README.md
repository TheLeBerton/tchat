# tchat — The family chat

Welcome! This program lets you chat live with the whole family, straight from your computer. No ads, just type and talk.

---

## What you need before starting

- A Mac or a PC running Linux ( or Windows with WSL )
- Python 3.11 or newer *( ask leberton if you're not sure )*

That's it.

---

## Install — only once

Open a terminal and run:

```
python3 -m pip install https://github.com/TheLeBerton/tchat/archive/refs/heads/main.tar.gz
```

Then launch it:

```
tchat
```

The first time it runs, it will create a config file and ask you to set the server IP *(leberton will give it to you — it looks like `100.x.x.x`)*.

> **If `tchat` is not found**, find where it was installed:
> ```
> python3 -c "import sysconfig; print(sysconfig.get_path('scripts'))"
> ```
> And run it with the full path shown.

---

## Update

```
python3 -m pip install --upgrade https://github.com/TheLeBerton/tchat/archive/refs/heads/main.tar.gz
```

---

## Start chatting

Every time you want to chat, just open a terminal and type:

```
tchat
```

A big logo appears, then it asks for your name. Type it, press Enter, and you're in!

---

## How to use it

| What you type | What it does |
|---|---|
| Any message + Enter | Sends it to everyone |
| `/whoonline` + Enter | Shows who is currently connected |
| `/help` + Enter | Lists all available commands |
| `/quit` + Enter | Leaves the chat |
| `Ctrl + C` | Also leaves the chat |

---

## Something's not working?

**It keeps saying "Cannot connect"?**
The server might be off. Send a message to leberton and he'll start it back up.

**You forgot which name you used last time?**
No worries — it shows up at the start and you can pick a new one if you want.

---

*Made with love by leberton*

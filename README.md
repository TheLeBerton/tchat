# tchat — The family chat

Welcome! This program lets you chat live with the whole family, straight from your computer. No ads, just type and talk.

---

## What you need before starting

- A Mac or a PC running Linux ( or Windows with WSL )
- Tailscale installed and connected *( ask leberton if you're not sure )*
- Python 3.11 or newer *( ask leberton if you don't know )*
- An established SSH connection *( ask leberton if you don't know )*
- git installed *( ask leberton if you don't know )*

---

## Install — only once

Open a terminal and type these two commands, one after the other:

```
cd tchat
bash install.sh
```

You'll see `Done.` at the end if everything worked.

**Then**, open the file `config/config.toml` with any text editor and replace:

```
ip = "TAILSCALE_IP"
```

with the Tailscale IP address of the server *(leberton will give it to you — it looks like `100.x.x.x`)*.

---

## Start chatting

Every time you want to chat, just open a terminal and type:

```
make cli
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

**Nothing happens when you type `make cli`?**
Make sure you're in the right folder. Type `cd tchat` first, then try again.

**It keeps saying "Cannot connect"?**
The server might be off. Send a message to leberton and he'll start it back up.

**You forgot which name you used last time?**
No worries — it shows up at the start and you can pick a new one if you want.

---

*Made with love by leberton*

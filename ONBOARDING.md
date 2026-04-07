# Onboarding — How to set up a new family member

This is your checklist. Go through it top to bottom on their machine (or guide them over a call).

---

## Step 1 — Download the project

1. Go to https://github.com/TheLeBerton/tchat
2. Click the green **Code** button
3. Click **Download ZIP**
4. Unzip the file — you'll get a folder called `tchat-main`
5. Rename it to `tchat` (optional, just cleaner)

---

## Step 2 — Install Python

Open a terminal and check if Python is already there:

```
python3 --version
```

If you see `Python 3.11.x` or higher, skip to Step 3.

Otherwise, follow the instructions for their system:

### Mac

1. Go to https://www.python.org/downloads/
2. Click the big yellow **Download Python** button
3. Open the downloaded file and follow the installer
4. Once done, close and reopen the terminal, then run `python3 --version` to confirm

### Linux (Ubuntu / Debian)

```
sudo apt update && sudo apt install -y python3
```

### Windows

Windows needs WSL (a Linux layer) first — Python runs inside it.

1. Open **PowerShell as administrator** (right-click the Start menu > "Windows PowerShell (Admin)")
2. Run:
   ```
   wsl --install
   ```
3. Restart the machine
4. Open the **Ubuntu** app from the Start menu
5. Inside Ubuntu, run:
   ```
   sudo apt update && sudo apt install -y python3
   ```

From now on, all commands are typed in the **Ubuntu** app, not PowerShell.

---

## Step 3 — Install Tailscale

1. Go to https://tailscale.com/download and install Tailscale
2. Have them sign in (Google or Apple account works fine)
3. On your Tailscale admin panel, invite them: **Settings > Users > Invite**
4. Wait until their machine shows up as **Connected** in your dashboard before moving on

---

## Step 4 — Install the project

Open a terminal, go into the project folder, and run:

```
cd tchat
bash install.sh
```

You'll see `Done.` at the end if everything worked.

---

## Step 5 — Set the server IP

Open `config/config.toml` with any text editor and update the `ip` line under `[client]`:

```toml
[client]
ip = "100.81.188.25"   # your Pi's Tailscale IP
port = 9999
```

Save the file.

---

## Step 6 — Test it

Make sure the server is running on your end (`make serv` or `make watch`), then on their machine:

```
make cli
```

If the banner appears and they can send a message — you're done.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `make: command not found` | Run `sudo apt install make` (Linux/WSL) or `brew install make` (Mac) |
| `Cannot connect` in a loop | Check the server is running and the IP in `config.toml` is correct |
| Tailscale says "not connected" | Have them click the Tailscale icon and hit Connect |
| `python3: command not found` | Go back to Step 2 |

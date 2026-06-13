# gh-notify — Agent instructions

## Overview

Python 3 script that polls GitHub notifications and shows KDE desktop notifications with clickable links. Uses `gh api /notifications` for data, `gdbus call` for rich HTML notifications with `body-markup`, `paplay` for sound.

## Key commands

- `python3 -m src.gh_notify` — check and notify (live mode, fetches from GitHub)
- `python3 -m src.gh_notify --test` / `-t` — show 3 test notifications (no API call)
- `./install.sh` — install package + systemd timer
- After `pipx install .` or `./install.sh`, `gh-notify` is available globally

## Architecture

- **Runtime:** Python 3.10+, no external dependencies (stdlib only)
- **Schedule:** systemd --user timer (`OnCalendar=*:0/10`)
- **Notification:** D-Bus `org.freedesktop.Notifications.Notify` via `gdbus call`
- **Sound:** Built-in `notification.wav` (bundled via `importlib.resources`), played with `paplay`
- **Logs:** `~/.local/share/gh-notify/logs/` (JSON, kept configurable days, default 7)
- **Config:** `~/.config/gh-notify/config.toml` (TOML, XDG-compliant)

## Gotchas

- `gh auth login` must be done before the script can work
- The script only shows unread notifications that exist at poll time
- System dependencies: `python3`, `gh`, `gdbus`, `paplay`

## ADRs

Key technical decisions are documented in `docs/adr/`:

- [001](docs/adr/001-use-gh-api-for-notifications.md) — GitHub API polling
- [002](docs/adr/002-use-dbus-notifications-with-body-markup.md) — D-Bus with body-markup
- [003](docs/adr/003-batch-multiple-notifications.md) — Batch notifications
- [004](docs/adr/004-use-systemd-user-timer.md) — Systemd user timer
- [006](docs/adr/006-use-python-pipx.md) — Python with pipx

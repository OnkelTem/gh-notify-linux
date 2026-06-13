# gh-notify

GitHub notification monitor for Linux desktops. Shows desktop notifications with clickable links to PRs, Issues, and Discussions. Plays a sound. Runs every 10 minutes.

## Dependencies

- Python 3.10+
- [pipx](https://pipx.pypa.io/) (recommended) or pip
- [GitHub CLI](https://cli.github.com) (`gh`) – API access
- `gdbus` (`glib-utils`) – D-Bus notifications
- `paplay` (`pulseaudio-utils`) – sound playback

## Local run (without installation)

```bash
# From the project root:
python3 -m src.gh_notify --test

# With custom flags:
python3 -m src.gh_notify --test --sound "" --timeout 5000 --urgency 1
```

After `pipx install .` or `./install.sh`, the `gh-notify` command is available globally.

## Quick start

```bash
# 1. Authenticate with GitHub
gh auth login

# 2. Deploy script, install package, and set up timer
./install.sh

# 3. Test it
gh-notify --test
```

A notification will appear within 10 minutes. Click a link to open the PR/Issue in your browser.

## Files

| Path | Purpose |
|------|---------|
| `src/gh_notify/` | Python package |
| `pyproject.toml` | Package metadata & entry point |
| `systemd/` | Systemd user service & timer |
| `docs/adr/` | Architecture Decision Records |
| `install.sh` | Deployment script |

## Logs

Raw API responses are saved to `~/.local/share/gh-notify/logs/`. Logs older than 7 days are automatically cleaned.

## Test mode

```bash
gh-notify --test
```

Shows 3 fake notifications (PR, Issue, Discussion) without calling the GitHub API. Useful for verifying the notification pipeline.

## Desktop environments

Notifications use the standard D-Bus `org.freedesktop.Notifications` protocol,
compatible with KDE Plasma, GNOME, Xfce, sway, and most Linux desktops.
Clickable links (`body-markup`) are supported on KDE Plasma and GNOME.

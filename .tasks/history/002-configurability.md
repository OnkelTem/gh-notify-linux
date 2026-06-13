# Task: 002-configurability

**Status:** completed
**Created:** 2026-06-13
**Completed:** 2026-06-13

## Goal

Make all hardcoded values in gh-notify configurable via config file, environment variables, and CLI flags.

## Plan

### Hardcoded values to externalize

| Value | Current | Config key | Env var |
|-------|---------|------------|---------|
| Log directory | `~/.local/share/gh-notify/logs` | `logging.dir` | `GH_NOTIFY_LOG_DIR` |
| Sound file | `/usr/share/sounds/Oxygen-Im-New-Mail.ogg` | `notifications.sound` | `GH_NOTIFY_SOUND` |
| Notification timeout | `10000` ms | `notifications.timeout` | `GH_NOTIFY_TIMEOUT` |
| Notification urgency | `2` (critical) | `notifications.urgency` | `GH_NOTIFY_URGENCY` |
| Emoji map | hardcoded dict | `display.emoji` | — (too complex for env) |
| API URL transform | hardcoded function | — | — |

### Config file format: TOML

Path: `~/.config/gh-notify/config.toml` (XDG compliant via `platformdirs` or manual `$XDG_CONFIG_HOME`)

```toml
[logging]
dir = "~/.local/share/gh-notify/logs"
retention_days = 7

[notifications]
sound = "/usr/share/sounds/Oxygen-Im-New-Mail.ogg"
timeout_ms = 10000
urgency = 2

[display]
emoji.PullRequest = "🔀"
emoji.Issue = "🐛"
emoji.Discussion = "💬"
emoji.Release = "🚀"
emoji.RepositoryInvitation = "📩"
emoji.Commit = "📝"
```

### Priority (highest to lowest)

1. CLI flags (`--log-dir`, `--sound`, `--timeout`, `--config`)
2. Environment variables (`GH_NOTIFY_*`)
3. Config file (`~/.config/gh-notify/config.toml`)
4. Built-in defaults

### CLI flags to add

- `--config PATH` — custom config file path
- `--log-dir PATH` — override log directory
- `--sound PATH` — override sound file (empty string = no sound)
- `--timeout MS` — notification timeout in milliseconds
- `--urgency BYTE` — D-Bus urgency level (0=low, 1=normal, 2=critical)

### Not in scope (this task is planning only)

- No implementation — this task only documents the plan
- Implementation will be a separate task after 001-migrate-to-python is complete

## Implementation notes

- Config file: `~/.config/gh-notify/config.toml` (XDG compliant)
- Config format: TOML via `tomllib` (stdlib 3.11+) with `tomli` fallback
- CLI via `argparse`
- Env vars: `GH_NOTIFY_*` prefix
- Priority: CLI > env > config > defaults
- Items 1-6 implemented; items 7-9 (emoji, API endpoint, base URL) deferred

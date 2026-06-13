#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib

_BUNDLED_SOUND: str | None = None
try:
    from importlib.resources import files as _res_files
    _sound_path = _res_files("gh_notify") / "sounds" / "notification.wav"
    if _sound_path.exists():
        _BUNDLED_SOUND = str(_sound_path)
except Exception:
    pass


@dataclass
class Config:
    log_dir: str = "~/.local/share/gh-notify/logs"
    retention_days: int = 7
    sound: str = field(default_factory=lambda: _BUNDLED_SOUND or "")
    timeout_ms: int = 10000
    urgency: int = 2
    app_name: str = "GitHub Monitor"


EMOJI = {
    "PullRequest": "\U0001f500",
    "Issue": "\U0001f41b",
    "Discussion": "\U0001f4ac",
    "Release": "\U0001f680",
    "RepositoryInvitation": "\U0001f4e9",
    "Commit": "\U0001f4dd",
}


def get_config_path() -> Path:
    xdg_config = os.environ.get("XDG_CONFIG_HOME")
    if xdg_config:
        base = Path(xdg_config)
    else:
        base = Path.home() / ".config"
    return base / "gh-notify" / "config.toml"


def load_config_file(path: Path) -> dict:
    if not path.exists():
        return {}
    with open(path, "rb") as f:
        return tomllib.load(f)


def load_config(cli_args: argparse.Namespace) -> Config:
    cfg = Config()

    config_path = Path(cli_args.config) if cli_args.config else get_config_path()
    raw = load_config_file(config_path)

    if "logging" in raw:
        lc = raw["logging"]
        if "dir" in lc:
            cfg.log_dir = lc["dir"]
        if "retention_days" in lc:
            cfg.retention_days = lc["retention_days"]

    if "notifications" in raw:
        nc = raw["notifications"]
        if "sound" in nc:
            cfg.sound = nc["sound"]
        if "timeout_ms" in nc:
            cfg.timeout_ms = nc["timeout_ms"]
        if "urgency" in nc:
            cfg.urgency = nc["urgency"]
        if "app_name" in nc:
            cfg.app_name = nc["app_name"]

    env_map = {
        "GH_NOTIFY_LOG_DIR": ("log_dir", str),
        "GH_NOTIFY_RETENTION_DAYS": ("retention_days", int),
        "GH_NOTIFY_SOUND": ("sound", str),
        "GH_NOTIFY_TIMEOUT": ("timeout_ms", int),
        "GH_NOTIFY_URGENCY": ("urgency", int),
        "GH_NOTIFY_APP_NAME": ("app_name", str),
    }
    for env_key, (attr, typ) in env_map.items():
        val = os.environ.get(env_key)
        if val is not None:
            if typ is int:
                setattr(cfg, attr, int(val))
            else:
                setattr(cfg, attr, val)

    cli_overrides = {
        "log_dir": cli_args.log_dir,
        "retention_days": cli_args.retention,
        "sound": cli_args.sound,
        "timeout_ms": cli_args.timeout,
        "urgency": cli_args.urgency,
        "app_name": cli_args.app_name,
    }
    for attr, val in cli_overrides.items():
        if val is not None:
            setattr(cfg, attr, val)

    return cfg


def api_url_to_html(api_url: str) -> str:
    return (
        api_url.replace("api.github.com/repos", "github.com")
        .replace("/pulls/", "/pull/")
    )


def build_notification(items: list[dict]) -> tuple[str, str]:
    if not items:
        return "", ""

    lines = []
    for n in items:
        emoji = EMOJI.get(n["type"], "\U0001f514")
        html_url = api_url_to_html(n["url"])
        lines.append(f'<a href="{html_url}">{emoji} {n["repo"]} \u2014 {n["title"]}</a>')

    body = "<br>".join(lines)
    total = len(items)
    if total == 1:
        summary = "\U0001f514 GitHub \u2014 1 \u0443\u0432\u0435\u0434\u043e\u043c\u043b\u0435\u043d\u0438\u0435"
    elif total < 5:
        summary = f"\U0001f514 GitHub \u2014 {total} \u0443\u0432\u0435\u0434\u043e\u043c\u043b\u0435\u043d\u0438\u044f"
    else:
        summary = f"\U0001f514 GitHub \u2014 {total} \u0443\u0432\u0435\u0434\u043e\u043c\u043b\u0435\u043d\u0438\u0439"

    return summary, body


def send_notif(summary: str, body: str, cfg: Config) -> None:
    subprocess.run(
        [
            "gdbus", "call", "--session",
            "--dest", "org.freedesktop.Notifications",
            "--object-path", "/org/freedesktop/Notifications",
            "--method", "org.freedesktop.Notifications.Notify",
            cfg.app_name, "0", "",
            summary, body,
            "[]",
            f"{{'body-markup': <true>, 'urgency': <byte {cfg.urgency}>}}",
            str(cfg.timeout_ms),
        ],
        check=True,
    )


def play_sound(sound_path: str) -> None:
    if sound_path:
        subprocess.run(["paplay", sound_path])


def clean_old_logs(log_dir: str, retention_days: int) -> None:
    subprocess.run(
        ["find", log_dir, "-name", "*.json", "-mtime", f"+{retention_days}", "-delete"],
        check=True,
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="gh-notify")
    parser.add_argument("--config", help="Path to config file")
    parser.add_argument("--log-dir", help="Log directory")
    parser.add_argument("--sound", help="Sound file path (empty = no sound)")
    parser.add_argument("--timeout", type=int, help="Notification timeout in ms")
    parser.add_argument("--urgency", type=int, help="D-Bus urgency (0=low, 1=normal, 2=critical)")
    parser.add_argument("--app-name", help="Notification app name")
    parser.add_argument("--retention", type=int, help="Log retention in days")
    parser.add_argument("--test", "-t", action="store_true", help="Show test notifications")
    return parser.parse_args(argv)


def main() -> None:
    cli_args = parse_args()
    cfg = load_config(cli_args)

    if cli_args.test:
        test_items = [
            {"type": "PullRequest", "repo": "test-repo", "title": "Add amazing feature", "url": "https://api.github.com/repos/owner/test-repo/pulls/42"},
            {"type": "Issue", "repo": "test-repo", "title": "Bug: login fails on Sunday", "url": "https://api.github.com/repos/owner/test-repo/issues/7"},
            {"type": "Discussion", "repo": "another-repo", "title": "RFC: new architecture", "url": "https://api.github.com/repos/owner/another-repo/discussions/3"},
        ]
        summary, body = build_notification(test_items)
        send_notif(summary, body, cfg)
        play_sound(cfg.sound)
        return

    result = subprocess.run(
        ["gh", "api", "/notifications"],
        capture_output=True, text=True, check=True,
    )
    raw = json.loads(result.stdout)

    log_dir = os.path.expanduser(cfg.log_dir)
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f"notifications-{int(time.time() * 1000)}.json")
    with open(log_path, "w") as f:
        json.dump(raw, f, indent=2)

    if not raw:
        return

    items = [
        {
            "type": n["subject"]["type"],
            "repo": n["repository"]["name"],
            "title": n["subject"]["title"],
            "url": n["subject"]["url"],
        }
        for n in raw
    ]

    summary, body = build_notification(items)
    send_notif(summary, body, cfg)
    play_sound(cfg.sound)

    clean_old_logs(log_dir, cfg.retention_days)


if __name__ == "__main__":
    main()

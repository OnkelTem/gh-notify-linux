#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SYSTEMD_DIR="$HOME/.config/systemd/user"
SERVICE_SRC="$SCRIPT_DIR/systemd/gh-notify.service"
TIMER_SRC="$SCRIPT_DIR/systemd/gh-notify.timer"

# Check dependencies
for cmd in python3 gh gdbus paplay; do
  if ! command -v "$cmd" &>/dev/null; then
    echo "ERROR: $cmd not found. Install it first."
    exit 1
  fi
done

# Check gh auth
gh auth status &>/dev/null || {
  echo "ERROR: gh is not authenticated. Run 'gh auth login' first."
  exit 1
}

# Install Python package
if command -v pipx &>/dev/null; then
  pipx install "$SCRIPT_DIR" --force
  echo "✓ Installed via pipx"
else
  pip install --user -e "$SCRIPT_DIR"
  echo "✓ Installed via pip (pipx not found, used pip --user)"
fi

# Deploy systemd files
mkdir -p "$SYSTEMD_DIR"
cp "$SERVICE_SRC" "$TIMER_SRC" "$SYSTEMD_DIR/"
echo "✓ Systemd files deployed"

# Enable timer
systemctl --user daemon-reload
systemctl --user enable --now gh-notify.timer
systemctl --user status gh-notify.timer --no-pager
echo "✓ Timer enabled and started"

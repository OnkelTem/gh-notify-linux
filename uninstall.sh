#!/usr/bin/env bash
set -euo pipefail

SYSTEMD_DIR="$HOME/.config/systemd/user"

echo "==> Stopping and disabling gh-notify timer..."
systemctl --user disable --now gh-notify.timer || true

echo "==> Removing systemd unit files..."
rm -f "$SYSTEMD_DIR/gh-notify.service" "$SYSTEMD_DIR/gh-notify.timer"

echo "==> Reloading systemd daemon..."
systemctl --user daemon-reload

echo "==> Uninstalling Python package..."
if command -v pipx &>/dev/null; then
  pipx uninstall gh-notify
  echo "    Uninstalled via pipx"
else
  pip uninstall -y gh-notify --user
  echo "    Uninstalled via pip"
fi

echo "==> Done. Configuration and logs in ~/.config/gh-notify/ and ~/.local/share/gh-notify/ were kept."

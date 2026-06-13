# ADR 004: Use systemd --user timer

## Context

Need to run the script periodically. Options: cron or systemd --user timer.

## Decision

Use systemd --user timer instead of cron.

## Rationale

- systemd --user inherits `DBUS_SESSION_BUS_ADDRESS` and `PULSE_SERVER` from the desktop session
- No need for workarounds to set these environment variables in cron
- `OnCalendar=*:0/10` is straightforward to read and maintain
- Better integration with the desktop session lifecycle

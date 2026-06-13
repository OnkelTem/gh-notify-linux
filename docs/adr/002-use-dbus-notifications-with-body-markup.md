# ADR 002: Use D-Bus notifications with body-markup

## Context

Need to show clickable links in KDE notifications. `notify-send` only supports plain text.

## Decision

Send notifications via D-Bus `org.freedesktop.Notifications.Notify` using `gdbus call` with `body-markup: true`.

## Rationale

- KDE supports HTML in notification body when `body-markup` hint is set
- `<a href="...">` links are rendered clickable by KDE's notification widget
- `gdbus` ships with glib (Ubuntu default) — no extra dependencies

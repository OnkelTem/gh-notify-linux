# ADR 001: Use GitHub API for notifications

## Context

Several options were considered: email notifications, browser Service Worker, GitHub Desktop, and polling `gh api /notifications`.

## Decision

Use `gh api /notifications` (GitHub REST API) via a systemd-triggered script.

## Rationale

- GitHub does not implement Web Push API for browser notifications
- Browser Service Workers are throttled when tab is backgrounded
- Email requires IMAP client setup on the desktop
- CLI-based approach does not require an open browser

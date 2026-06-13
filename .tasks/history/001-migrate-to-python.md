# Task: 001-migrate-to-python

**Status:** active
**Created:** 2026-06-13

## Goal

Migrate `gh-notify` from TypeScript/Bun to Python 3 with `pyproject.toml` and `pipx` installation.

## Steps

1. Rewrite `gh-notify` as Python package under `src/gh_notify/`
2. Create `pyproject.toml` with `[project.scripts]` entry point
3. Update `install.sh` to use `pipx` instead of `cp`
4. Update `README.md` with new dependencies and install instructions
5. Supersede ADR 005 with a new ADR 006
6. Keep all hardcoded values as-is (configurability is a separate task)

## Acceptance criteria

- [ ] `python3 -m gh_notify` works (live mode)
- [ ] `python3 -m gh_notify --test` shows 3 test notifications
- [ ] `pipx install .` makes `gh-notify` available in PATH
- [ ] `install.sh` deploys via pipx and sets up systemd timer
- [ ] All existing functionality preserved: D-Bus notify, paplay sound, JSON logging, 7-day log cleanup

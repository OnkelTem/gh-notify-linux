# ADR 006: Use Python 3 with pipx

## Status

Supersedes [ADR 005](005-use-typescript-bun.md).

## Context

The original TypeScript/Bun implementation required installing Bun, a non-standard runtime. Python 3 is pre-installed on virtually all Linux distributions, making the script more portable.

## Decision

Rewrite in Python 3, distribute via `pyproject.toml` with `pipx install`.

## Rationale

- Python 3 is available on every Linux system without additional installation
- `pipx` provides isolated environments for CLI tools (best practice for Python utilities)
- `pyproject.toml` with `[project.scripts]` creates a proper entry point
- The script has no external Python dependencies — pure stdlib
- `subprocess.run()` replaces Bun's `$` template literal with equivalent functionality

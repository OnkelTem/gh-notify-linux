# Task: 003-gen-sound

**Status:** completed
**Created:** 2026-06-13
**Completed:** 2026-06-13

## Goal

Generate a custom notification sound WAV file and bundle it with the Python package. Use `importlib.resources` to locate the sound file at runtime.

## Steps

1. Create `scripts/gen-sound` — a Python script that generates `src/gh_notify/sounds/notification.wav`
2. Create `src/gh_notify/sounds/` directory
3. Run `scripts/gen-sound` to generate the WAV
4. Update `Config` defaults in `__main__.py` to use `importlib.resources` to find the bundled sound
5. Update `pyproject.toml` to include the sound file in the package (via `package-data` or `include`)
6. Update `.gitignore` to NOT ignore `.wav` in `src/gh_notify/sounds/`
7. Adjust gen-sound: sample rate 16 kHz, volume 20%
8. Rewrite to numpy with harmonics and ADSR envelope
9. Final frequency tuning: C5 (523 Hz) / G5 (784 Hz)

## Sound design

Two-tone chime (like a doorbell), generated with numpy:
- Tone 1: 523 Hz (C5), 0.1 sec — harmonics at 1×, 2×, 3×, 4×
- Pause: 0.05 sec
- Tone 2: 784 Hz (G5), 0.15 sec — harmonics at 1×, 2×, 3×, 5×
- ADSR envelope: attack/decay/sustain/release per tone
- Format: WAV, 16000 Hz, 16-bit, mono
- Total length: ~0.30 sec
- Volume: 20% of max

## Acceptance criteria

- [ ] `./scripts/gen-sound` creates `src/gh_notify/sounds/notification.wav`
- [ ] `notification.wav` is included in the package (visible after `pip install`)
- [ ] `python3 -m src.gh_notify --test` plays the bundled sound
- [ ] If sound file is missing from the package, falls back to silence (no crash)
- [ ] Sound is short, pleasant, and distinct from the Oxygen theme

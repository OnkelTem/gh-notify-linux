# ADR 003: Batch multiple notifications into one

## Context

Multiple simultaneous notifications (e.g., several PRs) would flood the desktop with separate popups.

## Decision

Collect all items into a single notification with `<br>`-separated HTML list.

## Rationale

- Prevents notification spam
- One sound per batch instead of per item
- Each line remains individually clickable

---
name: scaffold-app
description: Scaffold a new web app repo based on docs/architecture/HANDOFF.json and ARCHITECTURE.md. Creates folder structure, baseline config, scripts, CI, and starter modules without implementing full features.
argument-hint: "[optional: stack override] [repo name]"
---

# Scaffold App Skill

## Preconditions
- Must read: docs/architecture/HANDOFF.json and docs/architecture/ARCHITECTURE.md
- If those files do not exist, run /architecture-pack first.

## Goal
Create a clean starting codebase that matches the chosen architecture.

## Steps
1. Read HANDOFF.json and choose exact tech (frontend/backend/db).
2. Create repo layout (folders) as specified.
3. Add baseline tooling:
   - formatting, linting
   - unit test runner
   - env var handling
   - logging
4. Add CI pipeline that runs lint + tests.
5. Add starter "health" endpoint and minimal web page to prove end-to-end wiring.
6. Write docs/runbooks/LOCAL_DEV.md with commands from HANDOFF.json.

## Rules
- Do not implement multiple features. Only the skeleton + health check + one minimal screen.
- No large refactors. Keep diffs small.
- Prefer industry-standard defaults.

## Definition of done
- `lint` passes
- `test` passes
- `dev` starts successfully
- health endpoint responds

## Output
Update:
- docs/runbooks/LOCAL_DEV.md
- Add minimal README with run instructions

---
name: release-deploy
description: Create deployment pipeline and release runbooks for web now and a clear future path for iOS/Android (wrapper or native). Adds environment config, build artifacts, and rollback strategy.
argument-hint: "[target: vercel|netlify|aws|azure|gcp] [mobile path: capacitor|react-native|flutter]"
---

# Release & Deploy Skill

## Preconditions
- Must read HANDOFF.json + ARCHITECTURE.md deployment section.

## Steps
1. Web deployment:
   - define env vars and secrets strategy
   - configure CI/CD pipeline
   - add staging + prod guidance
2. Mobile-ready plan:
   - document chosen approach (Capacitor/React Native/Flutter)
   - define what must remain stable (API contract, auth flows)
3. Write runbooks:
   - docs/runbooks/RELEASE.md
   - docs/runbooks/ROLLBACK.md

## Definition of done
- A fresh clone can deploy by following docs (no tribal knowledge)

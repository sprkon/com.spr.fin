---
name: release-deploy
description: Prepare app for production release. Manages versioning, final integration tests, deploy scripts, rollback runbooks, and post-deploy health checks.
argument-hint: "[version number] [target environment]"
---

# Release & Deploy Skill

## Steps
1. Read docs/architecture/HANDOFF.json and current deployment config.
2. Verify:
   - Version bump (tag or version file)
   - All tests pass
   - No secrets in build artifacts
   - Build/docker image is clean
3. Create:
   - docs/runbooks/DEPLOY.md (deployment steps)
   - docs/runbooks/ROLLBACK.md (rollback procedure)
   - Smoke test checklist
4. Execute deploy to staging (if available).
5. Smoke test post-deployment (health, core flow).

## Output
- docs/runbooks/DEPLOY.md
- docs/runbooks/ROLLBACK.md
- Release tag
- Deployment verification checklist

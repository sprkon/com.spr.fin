---
name: observability
description: Add production-grade observability: structured logs, request correlation IDs, metrics, health checks, and error reporting hooks. Produces runbook notes and verification steps.
argument-hint: "[scope: backend|frontend|full]"
---

# Observability Skill

## Steps
1. Read ARCHITECTURE.md observability section.
2. Implement:
   - structured logging
   - correlation/request IDs
   - health endpoint + readiness checks
   - baseline metrics (if stack supports)
3. Write docs/runbooks/OBSERVABILITY.md with:
   - what to look for
   - common failure modes
   - sample queries

## Output
- docs/runbooks/OBSERVABILITY.md
- health/readiness endpoints

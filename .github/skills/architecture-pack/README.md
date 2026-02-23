---
name: architecture-pack
description: Create a complete Architecture Pack (ARCHITECTURE.md + Mermaid diagrams + ADRs + OpenAPI draft + data model + NFRs + HANDOFF.json) from a requirement. Use this BEFORE implementation for any new app or major feature. Output is used by other skills.
argument-hint: "[requirement] [constraints] [platform targets]"
---

# Architecture Pack Skill

## Goal
Given a product requirement and constraints, produce a consistent architecture + design package that is ready for implementation and future mobile deployment.

## When to use
- Starting a new project
- Adding a large feature
- Re-architecting for scale, security, offline, or mobile readiness

## Inputs required (ask only if missing)
- Target platforms: Web now; future iOS/Android
- Users + core flows (2–5 bullets)
- Constraints: timeline, budget, preferred stack, hosting preference, auth requirements
- Data requirements (if any): main entities
- Non-functional requirements: performance, privacy, compliance, offline

If details are missing, make reasonable assumptions and clearly write them in the "Assumptions" section.

## Output contract (MUST create/overwrite these files)
Create/update:
- docs/architecture/ARCHITECTURE.md
- docs/architecture/HANDOFF.json
- docs/architecture/ADR/ADR-0001-stack.md (and more if needed)
- docs/architecture/diagrams/system-context.mmd
- docs/architecture/diagrams/containers.mmd
- docs/architecture/diagrams/sequence-core-flow.mmd
- docs/api/openapi.yaml (draft is ok but must be syntactically valid)
- docs/data/schema.md
- docs/quality/NFR.md
- docs/runbooks/LOCAL_DEV.md

## Required sections in ARCHITECTURE.md
1. Problem summary
2. Users and core user journeys
3. Constraints & assumptions
4. Proposed architecture (high level)
5. Frontend architecture (web now)
6. Backend architecture (API-first)
7. Data model overview
8. API design overview
9. Security model (authn/authz)
10. Observability (logs/metrics/traces)
11. Deployment architecture (web now; mobile later plan)
12. Risks & mitigations
13. Open questions

## Architecture rules (mobile-ready)
- Design API-first. Mobile and web must share the same API contract.
- Keep the domain model clean and separated from UI.
- Prefer modular boundaries: frontend / backend / shared contracts.
- Prefer stateless backend services.
- Plan for future mobile wrapper or shared UI code path:
  - If using web tech: consider Capacitor later
  - If using native: keep API contract stable and versioned

## Mermaid diagrams
Write Mermaid code in .mmd files. Keep them simple:
- system-context: actors + systems
- containers: client/web, API, DB, external services
- sequence-core-flow: one key journey end-to-end

## HANDOFF.json (must be strict)
Write a JSON object with:
- "stack": { "frontend": "...", "backend": "...", "db": "...", "mobile_path": "..." }
- "repo_layout": [list of top-level folders]
- "commands": { "setup": "...", "dev": "...", "test": "...", "lint": "...", "build": "..." }
- "quality_gates": ["tests_pass", "lint_pass", "no_secrets", "api_contract_updated"]
- "api_contract": { "openapi_path": "docs/api/openapi.yaml", "versioning": "..." }
- "nfr_summary": { "security": "...", "performance": "...", "privacy": "...", "offline": "..." }
- "feature_slices": [3-7 slice names in build order]

## Final step
End with:
- "How to run locally" in docs/runbooks/LOCAL_DEV.md
- A short "Next actions" list referencing the Feature Slice skill.

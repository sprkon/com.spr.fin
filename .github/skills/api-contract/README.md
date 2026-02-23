---
name: api-contract
description: Create or update docs/api/openapi.yaml and keep it consistent with backend handlers and client usage. Use before or alongside any backend work to keep the API stable and mobile-ready.
argument-hint: "[feature] [endpoints] [auth requirements]"
---

# API Contract Skill

## Goal
Keep OpenAPI as the source of truth for clients (web now, mobile later).

## Steps
1. Read ARCHITECTURE.md + existing openapi.yaml.
2. For requested feature:
   - define endpoints, request/response schemas, error responses
   - include auth/security schemes
3. Ensure versioning strategy is respected (document in openapi).
4. Provide examples for key endpoints.
5. If backend code exists, cross-check for drift and propose fixes.

## Output
- Update docs/api/openapi.yaml (must remain valid YAML)
- Add notes in docs/architecture/ADR if contract changes are significant

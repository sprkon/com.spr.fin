---
name: feature-slice
description: Implement one vertical feature slice end-to-end (UI -> API -> DB -> tests) based on HANDOFF.json and OpenAPI. Produces small, reviewable diffs and verification steps.
argument-hint: "[slice name from HANDOFF.json]"
---

# Feature Slice Skill

## Preconditions
- Must read docs/architecture/HANDOFF.json
- Must read docs/api/openapi.yaml
- Must read docs/quality/NFR.md

## Steps (strict)
1. Confirm scope for ONE slice only.
2. Update OpenAPI first if needed (or run /api-contract).
3. Implement backend endpoint(s) + validation + error handling.
4. Implement data persistence (migrations if applicable).
5. Implement frontend UI for the slice.
6. Add tests:
   - backend unit/integration
   - minimal frontend tests if applicable
7. Run commands from HANDOFF.json: lint + test + build (if available).
8. Provide:
   - changed files list
   - manual verification steps
   - rollback notes if risky

## Rules
- Keep public contracts stable unless requirement says otherwise.
- No unrelated formatting.
- Prefer small commits (if your environment supports it).

## Definition of done
- quality gates from HANDOFF.json are satisfied

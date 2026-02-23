---
name: test-quality
description: Improve test coverage and quality gates. Adds unit/integration/e2e scaffolding, makes CI enforce lint+tests, and creates a pragmatic test strategy for the repo.
argument-hint: "[focus area: backend|frontend|e2e]"
---

# Test & Quality Skill

## Goal
Make quality measurable and repeatable.

## Steps
1. Read HANDOFF.json commands and current CI.
2. Add/strengthen:
   - unit tests for core modules
   - integration tests for API + DB (if applicable)
   - basic e2e smoke (optional)
3. Ensure CI runs:
   - lint
   - tests
   - build (optional)
4. Write docs/quality/TEST_STRATEGY.md

## Output
- docs/quality/TEST_STRATEGY.md
- CI updates
- Example tests

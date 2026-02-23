---
name: security-review
description: Perform a security design + code review for a feature or entire app. Enforces authn/authz, input validation, secrets handling, OWASP basics, and adds security-focused tests/checklists.
argument-hint: "[feature or module]"
---

# Security Review Skill

## Steps
1. Read NFR.md + ARCHITECTURE.md security section.
2. Identify threats for:
   - auth/session/token handling
   - injection (SQL/NoSQL), XSS, CSRF
   - insecure direct object references (IDOR)
   - secrets leakage
3. Recommend mitigations and implement low-risk fixes.
4. Add tests for auth/validation/error behavior.
5. Write docs/quality/SECURITY_CHECKLIST.md

## Output
- docs/quality/SECURITY_CHECKLIST.md
- Optional ADR if major security decision

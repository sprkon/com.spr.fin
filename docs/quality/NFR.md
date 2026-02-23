# Non-Functional Requirements (NFRs)

## Performance

- **PDF Processing:** P95 < 5 seconds per file (< 50MB)
- **Text Extraction:** < 1 second for typical 10-page PDF
- **API Response Time:** < 200ms for metadata queries
- **Concurrent Users:** Support 100 simultaneous users initially
- **Throughput:** 10–50 PDFs processed per minute (depends on size)

---

## Scalability

- **Horizontal Scaling:** Backend can scale to N instances (stateless)
- **Database:** PostgreSQL with connection pooling (max 20 connections)
- **File Storage:** S3 scales transparently
- **Queue:** Use Celery + Redis for large file processing (future)

---

## Security

- **Authentication:** JWT with 1-hour expiry; refresh tokens supported
- **Authorization:** User isolation (users can only see/modify their own documents)
- **Transport:** TLS 1.2+ enforced; HTTPS only
- **Data at Rest:** S3 server-side encryption (AES-256)
- **Logging:** No PDF content logged; only metadata + timing
- **Secrets:** All tokens, DB credentials in environment variables (never in code)
- **CORS:** Restrict to known frontend domain
- **Input Validation:** Reject malformed PDFs, oversized files (> 50MB)

---

## Privacy & Compliance

- **GDPR:** 
  - User consent before data collection
  - Right to deletion: soft delete documents after 30 days of deletion request
  - Data export: provide JSON dump of user's documents + metadata
  - Privacy Policy linked in UI
- **Data Retention:** Keep change logs 90 days; archive old PDFs to cold storage
- **Audit Trail:** Log all document access + modifications with timestamps
- **No Analytics Tracking:** No third-party analytics on document content

---

## Reliability & Availability

- **Uptime SLA:** 99.5% (no more than 3.6 hours/month)
- **Backup:** Automated daily backups of PostgreSQL to S3
- **Disaster Recovery:** RTO < 4 hours, RPO < 1 hour
- **Error Handling:** Graceful degradation; failed replacements are rolled back
- **Monitoring:** Health checks every 30 seconds; alert on > 2 consecutive failures

---

## Maintainability

- **Code Coverage:** Minimum 70% unit test coverage
- **Documentation:** README + API docs (Swagger) + Architecture ADRs
- **Deployment:** CI/CD pipeline (GitHub Actions) with automated testing before deploy
- **Staging Environment:** Test all changes in staging before production
- **Rollback Plan:** Blue/green deployment for zero-downtime updates

---

## Offline & Mobile Readiness

- **Web:** Progressive Web App (PWA) for offline viewing of processed PDFs
- **Mobile:** Capacitor wrapper with local file picker; sync when online
- **Data Sync:** Track unsync'd changes locally; retry on reconnect

---

## Testing

- **Unit Tests:** Core logic (text extraction, PDF editing)
- **Integration Tests:** End-to-end PDF upload → replacement → download
- **E2E Tests:** User workflows in Playwright/Cypress
- **Mutation Tests:** Verify replacement logic doesn't break edge cases
- **Regression Tests:** 50+ sample PDFs covering diverse formats

---

## Accessibility (WCAG 2.1 AA)

- Keyboard navigation for all UI controls
- Screen reader support for document metadata
- Color contrast ratio ≥ 4.5:1 for text
- Alt text for all images in UI

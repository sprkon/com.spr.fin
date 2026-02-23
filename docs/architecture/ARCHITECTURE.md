# Architecture - PDF Content Replacement Engine

## 1. Problem summary

Users need to modify specific text content in PDF documents while preserving exact formatting, alignment, spacing, and visual layout. The replacement must be surgical—only the specified text changes; everything else remains byte-level identical. Primary use case: Replace names, codes, or values in templated PDFs while maintaining document integrity.

## 2. Users and core journeys

**Users:**
- Content managers processing bulk PDF documents
- Legal/HR professionals updating templates
- Automated workflows needing PDF text replacement

**Core journeys:**
1. Upload PDF → Preview content → Map old text to new text → Execute replacement → Download modified PDF
2. Track change history → Compare before/after → Verify integrity → Archive version
3. Create reusable mapping templates for repeated replacements

## 3. Constraints & assumptions
- **Constraints:**
  - Must preserve PDF formatting byte-level (no re-rendering)
  - Response time < 5 seconds per PDF (< 50MB)
  - Support 100 concurrent users initially
  - GDPR compliance required (document encryption, audit logs)
  
- **Assumptions:**
  - PDFs are text-based (not scanned images)
  - Replacement text is exact ASCII/Unicode match (no regex initially)
  - Small document set initially (< 100MB per file)
  - Python ecosystem preferred for PDF precision

## 4. Proposed architecture (high level)

**Three-tier architecture:**
1. **Frontend (React + TypeScript)** → PDF upload, preview, diff viewer, change mapping UI
2. **Backend (Python FastAPI)** → Text extraction, surgical PDF editing, validation
3. **Database (PostgreSQL)** → Document metadata, change history, version control
4. **Storage (S3/Blob)** → Original + modified PDFs, audit trail

**Data flow:**
```
User Upload PDF
    ↓
Extract text + metadata (pdfplumber)
    ↓
Store document + create version
    ↓
User specifies mappings (AB → DE)
    ↓
Apply replacement (pikepdf - surgical edit)
    ↓
Validate (compare checksums, diffs)
    ↓
User downloads modified PDF
    ↓
Store change log + archive versions
```

## 5. Frontend architecture (web)

**Tech:** React 18 + TypeScript + TailwindCSS
**State:** Zustand or Redux Toolkit
**PDF Viewer:** PDF.js powered viewer

**Components:**
- `DocumentUpload` - Drag-and-drop PDF upload
- `TextMappingEditor` - Create AB → DE mappings (table UI)
- `PDFPreview` - Side-by-side original/preview with highlights
- `DiffView` - Show exact changes (character-level diff)
- `DocumentHistory` - Version timeline and audit log

**Key flows:**
- Upload triggers backend extraction
- Display extracted text in editable table
- Preview shows changes in real-time
- Diff highlights only changed text

## 6. Backend architecture (API)

**Tech:** Python 3.11 + FastAPI + pydantic

**Modules:**
- **Document Service** - Upload, store metadata, versioning
- **PDF Parser** (pdfplumber) - Extract text + coordinates
- **PDF Editor** (pikepdf) - Surgical text replacement in PDF stream
- **Validator** - Checksum comparison, diff analysis
- **Storage Service** - S3/Blob operations

**Key endpoints:**
- `POST /documents/upload` - Accept PDF, extract, store
- `GET /documents/{id}/content` - Return extracted text
- `POST /documents/{id}/replace` - Apply mappings, return modified PDF
- `GET /documents/{id}/versions` - List change history
- `GET /documents/{id}/diff` - Compare two versions

**Processing flow:**
1. Receive PDF → store with UUID
2. Extract text + coordinates (pdfplumber)
3. Return text mapping UI to frontend
4. Receive mappings → validate
5. Use pikepdf to edit PDF content stream directly
6. Verify output (no format changes, only text)
7. Store modified PDF + changelog

## 7. Data model overview

**Core entities:**

**Document**
- `id` (UUID)
- `filename` (original name)
- `original_pdf_url` (S3 path)
- `content_hash` (SHA256 of original)
- `upload_timestamp`
- `status` (pending, ready, processing, completed)

**TextMapping**
- `id` (UUID)
- `document_id` (FK)
- `original_text` (search term, e.g., "AB")
- `replacement_text` (new value, e.g., "DE")
- `page_hints` (optional: pages where to replace)
- `created_at`

**ChangeLog**
- `id` (UUID)
- `document_id` (FK)
- `mapping_id` (FK)
- `original_checksum`
- `modified_checksum`
- `byte_diff_count` (validation: should be small)
- `timestamp`
- `applied_by` (user/system)

## 8. API design overview

**Authentication:** JWT bearer token (future: OAuth 2.0)

**Error responses:**
```
400 Bad Request - Invalid PDF or mapping
413 Payload Too Large - PDF > 50MB
422 Unprocessable Entity - Text not found in PDF
500 Server Error - Processing failure with partial rollback
```

**Example flow:**
```
POST /api/documents/upload
  File: document.pdf
  →
  {
    "document_id": "uuid-123",
    "content": "This is AB report",
    "pages": 1
  }

POST /api/documents/uuid-123/replace
  {
    "mappings": [
      {"original": "AB", "replacement": "DE"}
    ]
  }
  →
  {
    "status": "completed",
    "modified_pdf_url": "s3://...",
    "changes": [
      {"type": "text_replacement", "old": "AB", "new": "DE", "count": 1}
    ]
  }
```

## 9. Security model (authn/authz)

**Authentication:**
- JWT tokens (issued by FastAPI with 1-hour expiry)
- Future: OAuth 2.0 for SSO

**Authorization:**
- User can only access their own documents
- Role-based: Admin can audit others' changes

**Data Security:**
- TLS/HTTPS enforced
- Uploaded PDFs encrypted at rest (S3 server-side encryption)
- Change logs immutable (soft delete only)
- No PDF content logged (only metadata)
- GDPR: Implement data retention policy, document deletion

## 10. Observability

**Logging:**
- Structured logs (JSON) with correlation IDs
- Log: upload events, extraction time, replacement time, validation results
- Exclude PDF content; log only metadata + timing

**Metrics:**
- Processing time per PDF (histogram)
- Success/failure rates by document type
- S3 storage usage
- Concurrent users (Prometheus)

**Traces:**
- End-to-end trace ID for each document upload → completion
- Span: extraction, editing, validation, storage

**Health Checks:**
- `/health` - App running
- `/ready` - DB connected, S3 accessible, pikepdf available

## 11. Deployment architecture
- **Web now:**
  - Frontend: Vercel / Netlify (SPA)
  - Backend: AWS ECS + Fargate or Heroku (Python container)
  - Database: AWS RDS PostgreSQL (managed)
  - Storage: AWS S3 (PDFs, versions)
  - CDN: CloudFront (if needed)

- **Mobile later:**
  - Capacitor wrapper around React web app OR
  - Native mobile with shared API contract (same endpoints)
  - File picker integration for mobile document selection

## 12. Risks & mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Pikepdf corrupts PDFs | High | Unit test with 100+ sample PDFs; byte-level checksum validation |
| Concurrent edits overwrite | High | Implement document locks; queue replacements |
| PDF too large (> 100MB) | Medium | Stream processing or reject with clear error |
| Text encoding issues (UTF-8) | Medium | Normalize text on ingress; test with multiple encodings |
| User deletes important document | Medium | Soft delete + 30-day recovery window |
| S3 outage | Medium | Local temp storage with retry; graceful degradation |
| Performance degradation | Medium | Queue long jobs; async processing with webhooks |

## 13. Open questions

1. Should we support batch replacements (multiple files at once)?
2. Do we need OCR for scanned PDFs (future enhancement)?
3. What's the retention policy for archived PDFs?
4. Should users be able to undo replacements or only view history?
5. Do we need API rate limiting or pay-per-use billing?
6. Should we support scheduled/automated replacements via API?

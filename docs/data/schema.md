# Data Model & Schema

## Core Entities

### **documents** table
Stores uploaded PDF metadata and versions.

```sql
CREATE TABLE documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  filename VARCHAR(255) NOT NULL,
  original_pdf_url VARCHAR(500) NOT NULL,
  modified_pdf_url VARCHAR(500),
  content_hash VARCHAR(64) NOT NULL,
  status VARCHAR(20) DEFAULT 'pending',
  page_count INT,
  file_size_bytes INT,
  upload_timestamp TIMESTAMP DEFAULT NOW(),
  last_modified TIMESTAMP DEFAULT NOW(),
  deleted_at TIMESTAMP,
  UNIQUE(user_id, filename, upload_timestamp)
);
```

**Status values:** pending, ready, processing, completed, error

---

### **text_mappings** table
Defines text replacements for a document.

```sql
CREATE TABLE text_mappings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
  original_text TEXT NOT NULL,
  replacement_text TEXT NOT NULL,
  page_hints TEXT,
  match_count INT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

**page_hints:** Optional JSON array of page numbers or null for all pages.

---

### **change_logs** table
Immutable record of every replacement applied.

```sql
CREATE TABLE change_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
  mapping_id UUID NOT NULL REFERENCES text_mappings(id),
  original_checksum VARCHAR(64) NOT NULL,
  modified_checksum VARCHAR(64) NOT NULL,
  byte_diff_count INT,
  replacement_count INT,
  processing_time_ms INT,
  timestamp TIMESTAMP DEFAULT NOW(),
  applied_by VARCHAR(100) DEFAULT 'system',
  status VARCHAR(20) DEFAULT 'completed',
  error_message TEXT
);
```

**status values:** pending, completed, failed, rolled_back

---

### **users** table
Application users.

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  last_login TIMESTAMP,
  role VARCHAR(20) DEFAULT 'user',
  deleted_at TIMESTAMP
);
```

**role values:** user, admin

---

## Relationships

```
users (1) ---> (*) documents
documents (1) ---> (*) text_mappings
documents (1) ---> (*) change_logs
text_mappings (1) ---> (*) change_logs
```

---

## Indexes

For performance:
- `documents(user_id, deleted_at)` - Efficient user document list
- `change_logs(document_id, timestamp)` - Version history
- `text_mappings(document_id)` - Lookup by document
- `documents(content_hash)` - Detect duplicates

---

## API Response Models (Pydantic)

```python
class Document(BaseModel):
    id: UUID
    filename: str
    status: str
    page_count: int
    upload_timestamp: datetime

class TextMapping(BaseModel):
    id: UUID
    original_text: str
    replacement_text: str
    match_count: int

class ChangeLog(BaseModel):
    id: UUID
    replacement_count: int
    byte_diff_count: int
    timestamp: datetime
    status: str
```

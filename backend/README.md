# Backend (PDF Replacement Engine)

## Run locally

Create a Python 3.11+ virtual environment and install dependencies:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
pip install -r requirements.txt
```

Run the app (development):

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API endpoints:
- `GET /health` - Liveness
- `GET /ready` - Readiness
- `POST /documents/upload` - Upload PDF (multipart/form-data)
- `POST /documents/{id}/replace` - Apply replacement mappings (JSON)
- `GET /documents/{id}/download` - Download stored PDF

Notes: The replace endpoint is a placeholder; full PDF stream editing will be implemented in feature slices.

# Local Development Setup

This file contains commands to run the scaffolded backend and (placeholder) frontend locally.

Prerequisites:
- Python 3.11+
- Node.js 18+ (for frontend)
- Docker & Docker Compose (optional)

Backend (FastAPI)

```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Run backend tests:

```bash
cd backend
.venv\Scripts\activate  # or `source .venv/bin/activate`
pytest
```

Docker Compose (optional)

```bash
docker-compose up --build
```

Frontend (placeholder):

```bash
cd frontend
# initialize React app here in a feature slice
```

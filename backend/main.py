from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
import uuid
import os

app = FastAPI(title="PDF Replacement Engine API")

STORAGE_DIR = os.path.join(os.path.dirname(__file__), "storage")
os.makedirs(STORAGE_DIR, exist_ok=True)

class ReplacementMapping(BaseModel):
    original_text: str
    replacement_text: str
    page_hints: list[int] | None = None

class ReplacementRequest(BaseModel):
    mappings: list[ReplacementMapping]


@app.get("/health")
async def health():
    return JSONResponse({"status": "ok"})


@app.get("/ready")
async def ready():
    # Basic readiness: ensure storage dir writable
    try:
        test_path = os.path.join(STORAGE_DIR, ".ready_test")
        with open(test_path, "w") as f:
            f.write("ok")
        os.remove(test_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return JSONResponse({"status": "ready"})


@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")
    doc_id = str(uuid.uuid4())
    save_path = os.path.join(STORAGE_DIR, f"{doc_id}.pdf")
    with open(save_path, "wb") as out:
        content = await file.read()
        out.write(content)
    # In real flow: extract text and return metadata
    return {"document_id": doc_id, "filename": file.filename}


@app.post("/documents/{document_id}/replace")
async def replace_text(document_id: str, req: ReplacementRequest):
    # Placeholder: in real implementation call pikepdf/pdfplumber logic
    src = os.path.join(STORAGE_DIR, f"{document_id}.pdf")
    if not os.path.exists(src):
        raise HTTPException(status_code=404, detail="Document not found")
    # For now, just return success and echo mappings
    return {"status": "accepted", "mappings": [m.dict() for m in req.mappings]}


@app.get("/documents/{document_id}/download")
async def download(document_id: str):
    path = os.path.join(STORAGE_DIR, f"{document_id}.pdf")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Not found")
    return FileResponse(path, media_type="application/pdf", filename=os.path.basename(path))

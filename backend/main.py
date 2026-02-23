from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse, FileResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
import uuid
import os
import json
from datetime import datetime, timedelta

app = FastAPI(title="PDF Replacement Engine API")

STORAGE_DIR = os.path.join(os.path.dirname(__file__), "storage")
USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")
os.makedirs(STORAGE_DIR, exist_ok=True)

# Auth config
SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-prod")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def load_users() -> dict:
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(users: dict):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


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
    try:
        test_path = os.path.join(STORAGE_DIR, ".ready_test")
        with open(test_path, "w") as f:
            f.write("ok")
        os.remove(test_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return JSONResponse({"status": "ready"})


@app.post("/auth/register")
async def register(form: OAuth2PasswordRequestForm = Depends()):
    users = load_users()
    username = form.username.lower()
    if username in users:
        raise HTTPException(status_code=400, detail="User already exists")
    users[username] = {
        "username": username,
        "password_hash": get_password_hash(form.password),
        "created_at": datetime.utcnow().isoformat(),
    }
    save_users(users)
    return {"msg": "user created"}


@app.post("/auth/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    users = load_users()
    username = form_data.username.lower()
    user = users.get(username)
    if not user or not verify_password(form_data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_username(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401, detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    users = load_users()
    if username not in users:
        raise credentials_exception
    return username


@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...), username: str = Depends(get_current_username)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")
    doc_id = str(uuid.uuid4())
    save_path = os.path.join(STORAGE_DIR, f"{doc_id}.pdf")
    with open(save_path, "wb") as out:
        content = await file.read()
        out.write(content)
    return {"document_id": doc_id, "filename": file.filename, "uploaded_by": username}


@app.post("/documents/{document_id}/replace")
async def replace_text(document_id: str, req: ReplacementRequest, username: str = Depends(get_current_username)):
    src = os.path.join(STORAGE_DIR, f"{document_id}.pdf")
    if not os.path.exists(src):
        raise HTTPException(status_code=404, detail="Document not found")
    # Placeholder: in real implementation call pikepdf/pdfplumber logic
    return {"status": "accepted", "mappings": [m.dict() for m in req.mappings], "applied_by": username}


@app.get("/documents/{document_id}/download")
async def download(document_id: str, username: str = Depends(get_current_username)):
    path = os.path.join(STORAGE_DIR, f"{document_id}.pdf")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Not found")
    return FileResponse(path, media_type="application/pdf", filename=os.path.basename(path))

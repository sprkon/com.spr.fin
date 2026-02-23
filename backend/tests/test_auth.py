from fastapi.testclient import TestClient
from main import app
import io

client = TestClient(app)


def test_register_and_login_and_upload():
    # Register
    r = client.post("/auth/register", data={"username": "testuser", "password": "secret"})
    assert r.status_code == 200
    # Login
    r = client.post("/auth/token", data={"username": "testuser", "password": "secret"})
    assert r.status_code == 200
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    # Upload a small fake PDF
    pdf_bytes = b"%PDF-1.4\n%FakePDF\n1 0 obj<</Type /Catalog>>endobj\ntrailer<</Root 1 0 R>>\n%%EOF\n"
    files = {"file": ("sample.pdf", io.BytesIO(pdf_bytes), "application/pdf")}
    r = client.post("/documents/upload", files=files, headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert "document_id" in data

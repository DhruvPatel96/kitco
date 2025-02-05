from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_editorial_endpoint():
    response = client.post(
        "/api/v1/generate/editorial",
        headers={"X-API-Key": "kitco-secret-2024"},
        json={"event": "Gold prices surge 5% after Fed meeting"}
    )
    assert response.status_code == 200
    assert "%" in response.json()["content"]
    assert "US$" in response.json()["content"]
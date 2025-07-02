from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_moderate_smoke() -> None:
    resp = client.post(
        "/v1/moderate/",
        files={"file": ("dummy.jpg", b"bytes", "image/jpeg")},
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "OK"

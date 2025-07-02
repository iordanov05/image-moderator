from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_moderate_smoke(monkeypatch) -> None:
    async def fake_moderate(self, _: bytes) -> float:
        return 0.0

    monkeypatch.setattr(
        "app.services.deepai_client.DeepAIClient.moderate",
        fake_moderate,
    )

    resp = client.post(
        "/v1/moderate/",
        files={"file": ("dummy.jpg", b"bytes", "image/jpeg")},
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "OK"

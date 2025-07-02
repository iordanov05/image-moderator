import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.mark.parametrize("score, expected", [(0.3, "OK"), (0.9, "REJECTED")])
def test_moderate_deepai(monkeypatch, score, expected):
    async def fake_moderate(self, _: bytes) -> float:  # noqa: D401
        return score

    monkeypatch.setattr("app.services.deepai_client.DeepAIClient.moderate", fake_moderate)

    resp = client.post("/v1/moderate/", files={"file": ("x.jpg", b"abc", "image/jpeg")})
    assert resp.status_code == 200
    assert resp.json()["status"] == expected

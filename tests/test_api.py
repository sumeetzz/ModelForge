import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_predict():
    response = client.post(
        "/predict",
        json={"features": [35, 70000, 1, 0, 0, 1]},
        headers={"Authorization": "Bearer dummy-token"}
    )
    assert response.status_code == 200
    assert "prediction" in response.json()

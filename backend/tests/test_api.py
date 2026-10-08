import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, Base, engine

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "name" in response.json()
    assert "claim-review-assistant" in response.json()["name"].lower()


def test_list_claims_empty(client):
    response = client.get("/api/claims")
    assert response.status_code == 200
    assert response.json() == []


def test_get_nonexistent_claim(client):
    response = client.get("/api/claims/nonexistent-id")
    assert response.status_code == 404


def test_get_pending_claims(client):
    response = client.get("/api/claims/pending")
    assert response.status_code == 200
    assert response.json() == []

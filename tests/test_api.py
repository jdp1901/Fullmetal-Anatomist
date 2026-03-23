"""Integration tests for the FastAPI API endpoints."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from backend.main import app
from backend.database import get_session


# ── In-memory DB fixture ───────────────────────────────────────

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    app.dependency_overrides[get_session] = lambda: session
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# ── Settings tests ──────────────────────────────────────────────

def test_get_settings_default(client: TestClient):
    res = client.get("/api/settings")
    assert res.status_code == 200
    data = res.json()
    assert data["llm_provider"] == "gemini"
    assert data["has_api_key"] is False


def test_update_settings(client: TestClient):
    res = client.put("/api/settings", json={
        "llm_provider": "openai",
        "api_key": "sk-testkey123",
        "model_name": "gpt-4o-mini",
    })
    assert res.status_code == 200
    data = res.json()
    assert data["llm_provider"] == "openai"
    assert data["has_api_key"] is True


# ── Subjects tests ──────────────────────────────────────────────

def test_list_subjects_empty(client: TestClient):
    res = client.get("/api/subjects")
    assert res.status_code == 200
    assert res.json() == []


def test_create_subject(client: TestClient):
    res = client.post("/api/subjects", json={"name": "Pathology"})
    assert res.status_code == 201
    data = res.json()
    assert data["name"] == "Pathology"
    assert "id" in data


def test_list_subjects_after_create(client: TestClient):
    client.post("/api/subjects", json={"name": "Pharmacology"})
    res = client.get("/api/subjects")
    assert len(res.json()) == 1
    assert res.json()[0]["name"] == "Pharmacology"


# ── Chapters tests ──────────────────────────────────────────────

@pytest.fixture(name="subject_id")
def subject_id_fixture(client: TestClient) -> int:
    res = client.post("/api/subjects", json={"name": "Anatomy"})
    return res.json()["id"]


def test_create_chapter(client: TestClient, subject_id: int):
    res = client.post("/api/chapters", json={
        "subject_id": subject_id,
        "title": "Chapter 1: The Heart",
        "raw_content": "The heart is a muscular organ that pumps blood.",
        "chapter_number": 1,
    })
    assert res.status_code == 201
    data = res.json()
    assert data["title"] == "Chapter 1: The Heart"
    assert data["subject_id"] == subject_id


def test_get_chapter(client: TestClient, subject_id: int):
    create_res = client.post("/api/chapters", json={
        "subject_id": subject_id,
        "title": "Chapter 2: The Lungs",
        "raw_content": "The lungs facilitate gas exchange.",
    })
    chapter_id = create_res.json()["id"]
    res = client.get(f"/api/chapters/{chapter_id}")
    assert res.status_code == 200
    assert res.json()["id"] == chapter_id


def test_get_chapter_not_found(client: TestClient):
    res = client.get("/api/chapters/99999")
    assert res.status_code == 404


def test_delete_chapter(client: TestClient, subject_id: int):
    create_res = client.post("/api/chapters", json={
        "subject_id": subject_id,
        "title": "Chapter 3: The Liver",
        "raw_content": "The liver metabolizes drugs.",
    })
    chapter_id = create_res.json()["id"]
    del_res = client.delete(f"/api/chapters/{chapter_id}")
    assert del_res.status_code == 200
    # Confirm it's gone
    assert client.get(f"/api/chapters/{chapter_id}").status_code == 404


# ── Worksheets tests ───────────────────────────────────────────

def test_list_worksheets_empty(client: TestClient):
    res = client.get("/api/worksheets")
    assert res.status_code == 200
    assert res.json() == []


def test_get_worksheet_not_found(client: TestClient):
    res = client.get("/api/worksheets/99999")
    assert res.status_code == 404

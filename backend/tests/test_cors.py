"""CORS tests: a browser may read API responses only for configured origins."""

from fastapi.testclient import TestClient

from app.config import Settings, get_settings
from app.main import app

client = TestClient(app)

ALLOWED_ORIGIN = get_settings().cors_origins[0]
OTHER_ORIGIN = "https://not-allowed.example"


def test_allowed_origin_is_echoed_back():
    response = client.get("/health", headers={"Origin": ALLOWED_ORIGIN})
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == ALLOWED_ORIGIN


def test_other_origin_gets_no_cors_header():
    response = client.get("/health", headers={"Origin": OTHER_ORIGIN})
    assert response.status_code == 200
    assert "access-control-allow-origin" not in response.headers


def test_preflight_for_allowed_origin_succeeds():
    response = client.options(
        "/health",
        headers={"Origin": ALLOWED_ORIGIN, "Access-Control-Request-Method": "GET"},
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == ALLOWED_ORIGIN


def test_preflight_for_other_origin_is_rejected():
    response = client.options(
        "/health",
        headers={"Origin": OTHER_ORIGIN, "Access-Control-Request-Method": "GET"},
    )
    assert response.status_code == 400
    assert "access-control-allow-origin" not in response.headers


def test_origins_come_from_the_environment(monkeypatch):
    monkeypatch.setenv("CORS_ALLOWED_ORIGINS", "https://app.example, https://other.example")
    assert Settings().cors_origins == ["https://app.example", "https://other.example"]


def test_blank_entries_in_the_origin_list_are_ignored():
    settings = Settings(cors_allowed_origins=" http://a.test , ,http://b.test ")
    assert settings.cors_origins == ["http://a.test", "http://b.test"]
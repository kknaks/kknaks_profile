"""TDD — FastAPI 앱 부팅 + /api/me 통합 테스트 (TestClient — 실제 lifespan 발동)."""

import os

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def client():
    """TestClient는 lifespan을 발동시킴 → load_all() 자동.

    모듈 스코프 — lifespan 이 1.1초라 매 테스트 재기동할 이유가 없다.
    로그인·쿠키를 쓰지 않아 공유해도 client 에 상태가 남지 않는다.
    """
    from main import app

    with TestClient(app) as c:
        yield c


class TestLifespanGuards:
    def test_multi_worker_rejected(self, monkeypatch):
        monkeypatch.setenv("WEB_CONCURRENCY", "2")
        with pytest.raises(RuntimeError, match="Multi-worker"):
            from fastapi.testclient import TestClient

            from main import app

            with TestClient(app):
                pass


class TestApiMe:
    def test_returns_200(self, client):
        r = client.get("/api/me")
        assert r.status_code == 200

    def test_has_handle(self, client):
        data = client.get("/api/me").json()
        assert data["user"]["handle"] == "kknaks"
        assert data["user"]["name"] == "이건학"

    def test_lang_ko_returns_korean(self, client):
        data = client.get("/api/me?lang=ko").json()
        assert "호기심" in data["user"]["tagline"]
        assert data["about"]["subtitle"] == "만드는 사람"

    def test_lang_en_returns_english(self, client):
        data = client.get("/api/me?lang=en").json()
        assert "curiosity" in data["user"]["tagline"].lower()
        assert data["about"]["subtitle"] == "the maker"

    def test_invalid_lang_rejected(self, client):
        r = client.get("/api/me?lang=jp")
        assert r.status_code == 422

    def test_stack_is_list_not_i18n(self, client):
        # stack은 단일 언어 X — list 그대로
        data = client.get("/api/me").json()
        assert isinstance(data["user"]["stack"], list)
        assert "Python" in data["user"]["stack"]

    def test_email_unchanged_by_i18n(self, client):
        # email 은 단일 언어 X — string 그대로 (i18n 분기 안 됨)
        data = client.get("/api/me").json()
        email = data["user"]["email"]
        assert isinstance(email, str)
        assert "@" in email

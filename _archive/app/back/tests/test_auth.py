"""관리자 인증 라우터 테스트 (KDEV-SPEC-006 / WORK-011).

라이브 Postgres 가 필요하다 — 미가용이면 모듈 전체 skip (CI/무-DB 환경 안전).
docker compose -f docker-compose.local.yml up -d postgres 후 실행.
"""

from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

import config

# DB 연결 확인 — 안 되면 모듈 skip. (앱 엔진은 async 라 프로브는 별도 sync 엔진으로.)
try:
    _probe = create_engine(config.database_url())
    with _probe.connect() as conn:
        conn.execute(text("SELECT 1"))
    _probe.dispose()
    _DB_OK = True
except SQLAlchemyError:
    _DB_OK = False

pytestmark = pytest.mark.skipif(not _DB_OK, reason="Postgres 미가용 — auth 테스트 skip")


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("ADMIN_USERNAME", "admin")
    monkeypatch.setenv("ADMIN_PASSWORD", "changeme")
    monkeypatch.setenv("JWT_SECRET", "test-jwt-secret-at-least-32-bytes-long!!")
    with TestClient(__import__("main").app) as c:  # lifespan → seed_admin
        yield c


def test_me_without_session_401(client):
    r = client.get("/api/auth/me")
    assert r.status_code == 401
    assert r.json()["detail"] == "not authenticated"


def test_login_bad_credentials_401(client):
    r = client.post("/api/auth/login", json={"username": "admin", "password": "wrong"})
    assert r.status_code == 401
    assert r.json()["detail"] == "invalid credentials"


def test_login_missing_field_422(client):
    r = client.post("/api/auth/login", json={"username": "admin"})
    assert r.status_code == 422


def test_login_sets_httponly_cookie_and_me(client):
    r = client.post("/api/auth/login", json={"username": "admin", "password": "changeme"})
    assert r.status_code == 200
    assert r.json()["user"] == {"username": "admin", "role": "admin"}
    setc = r.headers.get("set-cookie", "")
    assert f"{config.auth_cookie_name()}=" in setc
    assert "HttpOnly" in setc
    # 비밀번호/해시 미노출
    assert "password" not in str(r.json()).lower()

    r = client.get("/api/auth/me")
    assert r.status_code == 200
    assert r.json()["user"]["username"] == "admin"


def test_logout_clears_session(client):
    client.post("/api/auth/login", json={"username": "admin", "password": "changeme"})
    r = client.post("/api/auth/logout")
    assert r.status_code == 200
    client.cookies.clear()
    r = client.get("/api/auth/me")
    assert r.status_code == 401

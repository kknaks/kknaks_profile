"""승인 큐 API (KDEV-WORK-014 P2 / KDEV-SPEC-007 §4).

이 테스트들은 실 Postgres 에 **실제로 커밋한다** — 라우터가 자기 세션을 열고 커밋하는
경로를 그대로 태워야 의미가 있기 때문이다. 대신 만든 행은 전용 `source_kind` 로
표시하고 끝나면 지운다(자식 행은 CASCADE).
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

import config

MARK = "apitest"

try:
    _probe = create_engine(config.database_url())
    with _probe.connect() as conn:
        conn.execute(text("SELECT 1"))
    _probe.dispose()
    _DB_OK = True
except SQLAlchemyError:
    _DB_OK = False

pytestmark = pytest.mark.skipif(not _DB_OK, reason="Postgres 미가용")


@pytest.fixture(scope="module")
def _cleanup():
    yield
    engine = create_engine(config.database_url())
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM queue_items WHERE source_kind = :k"), {"k": MARK})
    engine.dispose()


@pytest.fixture
def anon(monkeypatch):
    monkeypatch.setenv("ADMIN_USERNAME", "admin")
    monkeypatch.setenv("ADMIN_PASSWORD", "changeme")
    monkeypatch.setenv("JWT_SECRET", "test-jwt-secret-at-least-32-bytes-long!!")
    with TestClient(__import__("main").app) as c:
        yield c


@pytest.fixture
def client(anon, _cleanup):
    r = anon.post("/api/auth/login", json={"username": "admin", "password": "changeme"})
    assert r.status_code == 200, r.text
    return anon


def _create(client, **body):
    body.setdefault("source_kind", MARK)
    return client.post("/api/admin/queue/items", json=body)


class TestAuthGate:
    """큐 표면 전체가 admin 뒤에 있다 — 승인 전 초안이 여기 있기 때문이다."""

    @pytest.mark.parametrize(
        "method, path",
        [
            ("get", "/api/admin/queue/items"),
            ("post", "/api/admin/queue/items"),
            ("get", "/api/admin/queue/items/1"),
            ("patch", "/api/admin/queue/items/1"),
            ("post", "/api/admin/queue/items/1/prepare"),
            ("delete", "/api/admin/queue/items/1"),
        ],
    )
    def test_anonymous_is_rejected(self, anon, method, path):
        kwargs = {"json": {}} if method in ("post", "patch") else {}
        response = getattr(anon, method)(path, **kwargs)
        assert response.status_code == 401


class TestCreate:
    def test_creates_and_lists(self, client):
        created = _create(client, source_url="https://youtu.be/apicreate01", note="메모")
        assert created.status_code == 201, created.text
        assert created.json()["outcome"] == "created"
        item_id = created.json()["item_id"]

        listed = client.get("/api/admin/queue/items")
        assert listed.status_code == 200
        assert item_id in [i["id"] for i in listed.json()["items"]]

    def test_second_submission_joins(self, client):
        first = _create(client, source_url="https://youtu.be/apijoin0001", note="첫")
        second = _create(
            client, source_url="https://www.youtube.com/watch?v=apijoin0001&t=5s", note="둘"
        )
        assert second.json()["outcome"] == "joined"
        assert second.json()["item_id"] == first.json()["item_id"]

    def test_empty_submission_rejected(self, client):
        assert _create(client).status_code == 422

    def test_published_duplicate_returns_409(self, client):
        created = _create(client, source_url="https://youtu.be/apidup00001")
        item_id = created.json()["item_id"]
        engine = create_engine(config.database_url())
        with engine.begin() as conn:
            conn.execute(
                text("UPDATE queue_items SET status='published' WHERE id=:i"), {"i": item_id}
            )
        engine.dispose()

        again = _create(client, source_url="https://youtu.be/apidup00001")
        assert again.status_code == 409
        assert again.json()["detail"]["code"] == "DUPLICATE_PUBLISHED"
        assert again.json()["detail"]["existing_item_id"] == item_id

        forced = _create(client, source_url="https://youtu.be/apidup00001", allow_republish=True)
        assert forced.status_code == 201
        assert forced.json()["outcome"] == "created"


class TestDetailAndNote:
    def test_detail_exposes_history(self, client):
        item_id = _create(client, source_url="https://youtu.be/apidetail01").json()["item_id"]
        detail = client.get(f"/api/admin/queue/items/{item_id}")
        assert detail.status_code == 200
        body = detail.json()
        # 실패한 실행까지 보여야 재시도 판단이 선다.
        assert "preparations" in body and "ai_tasks" in body
        assert body["status"] == "received"

    def test_note_update(self, client):
        item_id = _create(client, source_url="https://youtu.be/apinote0001").json()["item_id"]
        patched = client.patch(f"/api/admin/queue/items/{item_id}", json={"note": "고친 메모"})
        assert patched.status_code == 200
        assert patched.json()["note"] == "고친 메모"

    def test_missing_item_is_404(self, client):
        assert client.get("/api/admin/queue/items/99999999").status_code == 404


class TestDelete:
    def test_soft_delete_hides_but_keeps_row(self, client):
        item_id = _create(client, source_url="https://youtu.be/apidelete01").json()["item_id"]
        assert client.delete(f"/api/admin/queue/items/{item_id}").status_code == 200

        listed = client.get("/api/admin/queue/items")
        assert item_id not in [i["id"] for i in listed.json()["items"]]
        assert client.get(f"/api/admin/queue/items/{item_id}").status_code == 404

        engine = create_engine(config.database_url())
        with engine.connect() as conn:
            row = conn.execute(
                text("SELECT status, deleted_at FROM queue_items WHERE id=:i"), {"i": item_id}
            ).one()
        engine.dispose()
        assert row[0] == "deleted" and row[1] is not None

    def test_cannot_delete_while_publishing(self, client):
        item_id = _create(client, source_url="https://youtu.be/apipublish1").json()["item_id"]
        engine = create_engine(config.database_url())
        with engine.begin() as conn:
            conn.execute(
                text("UPDATE queue_items SET status='publishing' WHERE id=:i"), {"i": item_id}
            )
        engine.dispose()

        response = client.delete(f"/api/admin/queue/items/{item_id}")
        assert response.status_code == 409
        assert response.json()["detail"]["code"] == "DELETE_WHILE_PUBLISHING"


class TestRetryPrepare:
    def test_rejected_when_state_disallows(self, client):
        item_id = _create(client, source_url="https://youtu.be/apiretry001").json()["item_id"]
        engine = create_engine(config.database_url())
        with engine.begin() as conn:
            conn.execute(
                text("UPDATE queue_items SET status='in_review' WHERE id=:i"), {"i": item_id}
            )
        engine.dispose()

        response = client.post(f"/api/admin/queue/items/{item_id}/prepare")
        assert response.status_code == 409
        assert response.json()["detail"]["code"] == "PREPARE_RETRY_NOT_ALLOWED"

    def test_unavailable_summarizer_is_reported_not_faked(self, client, monkeypatch):
        """캡처가 꺼져 있으면 재시도도 불가능한 게 사실이다 — 조용히 대체하지 않는다."""
        monkeypatch.setattr("api.routers.queue._summarizer_factory", lambda: None)
        item_id = _create(client, source_url="https://youtu.be/apinoai0001").json()["item_id"]
        response = client.post(f"/api/admin/queue/items/{item_id}/prepare")
        assert response.status_code == 503
        assert response.json()["detail"]["code"] == "SUMMARIZER_UNAVAILABLE"

    def test_retry_uses_note_when_source_unreachable(self, client, monkeypatch):
        """막힌 항목이 메모 한 줄로 풀리는 경로가 API 로도 열려 있어야 한다."""

        async def fake_summarize(*, material, note):
            from service.pipeline import SummaryResult

            return SummaryResult(summary=f"요약({note})")

        async def fetch_fail(url):
            raise RuntimeError("no transcript")

        monkeypatch.setattr("api.routers.queue._summarizer_factory", lambda: fake_summarize)
        monkeypatch.setattr("service.knowledge_capture.source.fetch_source", fetch_fail)

        item_id = _create(
            client, source_url="https://youtu.be/apirescue01", note="자막 없어 직접 요약: X"
        ).json()["item_id"]

        response = client.post(f"/api/admin/queue/items/{item_id}/prepare")
        assert response.status_code == 200, response.text
        assert response.json()["status"] == "in_review"

        detail = client.get(f"/api/admin/queue/items/{item_id}").json()
        assert detail["preparations"][-1]["payload"]["material_source"] == "note"

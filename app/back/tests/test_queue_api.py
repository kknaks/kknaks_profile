"""승인 큐 API (KDEV-WORK-014 P2 / KDEV-SPEC-007 §4).

이 테스트들은 실 Postgres 에 **실제로 커밋한다** — 라우터가 자기 세션을 열고 커밋하는
경로를 그대로 태워야 의미가 있기 때문이다. 대신 만든 행은 전용 `source_kind` 로
표시하고 끝나면 지운다(자식 행은 CASCADE).
"""

from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

import config

try:
    _probe = create_engine(config.database_url())
    with _probe.connect() as conn:
        conn.execute(text("SELECT 1"))
    _probe.dispose()
    _DB_OK = True
except SQLAlchemyError:
    _DB_OK = False

pytestmark = pytest.mark.skipif(not _DB_OK, reason="Postgres 미가용")


#: 이 파일이 만든 항목 id. `source_kind` 를 정리용 마커로 쓰면 안 된다 —
#: 같은 컬럼이 **파이프라인 정의 조회 키**라 게이트가 안 열린다.
_CREATED: set[int] = set()


@pytest.fixture(scope="module")
def _cleanup():
    yield
    if not _CREATED:
        return
    engine = create_engine(config.database_url())
    with engine.begin() as conn:
        conn.execute(
            text("DELETE FROM queue_items WHERE id = ANY(:ids)"), {"ids": list(_CREATED)}
        )
    engine.dispose()


@pytest.fixture(scope="module")
def app_client():
    """모듈당 한 번만 띄운다 — lifespan(load_all + seed_admin)이 1초를 넘는다.

    인증 상태는 client 에 남는 **쿠키**뿐이라, 테스트마다 쿠키만 비우면 공유해도 안전하다.
    """
    os.environ["ADMIN_USERNAME"] = "admin"
    os.environ["ADMIN_PASSWORD"] = "changeme"
    os.environ["JWT_SECRET"] = "test-jwt-secret-at-least-32-bytes-long!!"
    with TestClient(__import__("main").app) as c:
        yield c


@pytest.fixture
def anon(app_client):
    app_client.cookies.clear()
    return app_client


@pytest.fixture
def client(anon, _cleanup):
    r = anon.post("/api/auth/login", json={"username": "admin", "password": "changeme"})
    assert r.status_code == 200, r.text
    return anon


def _create(client, **body):
    response = client.post("/api/admin/queue/items", json=body)
    if response.status_code == 201:
        _CREATED.add(response.json()["item_id"])
    return response


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
        """막힌 항목이 메모 한 줄로 풀리는 경로가 API 로도 열려 있어야 한다.

        준비 응답은 **요약을 기다리지 않는다** — 제출까지만 하고 `preparing` 으로
        돌아오며, 상세 조회가 수확한다 (WORK-016 P2).
        """
        from tests.fakes import FakeSummarizer

        summarizer = FakeSummarizer(summary="요약(메모)")

        async def fetch_fail(url):
            raise RuntimeError("no transcript")

        monkeypatch.setattr("api.routers.queue._summarizer_factory", lambda: summarizer)
        monkeypatch.setattr("service.knowledge_capture.source.fetch_source", fetch_fail)

        item_id = _create(
            client, source_url="https://youtu.be/apirescue01", note="자막 없어 직접 요약: X"
        ).json()["item_id"]

        response = client.post(f"/api/admin/queue/items/{item_id}/prepare")
        assert response.status_code == 200, response.text
        assert response.json()["status"] == "preparing"

        detail = client.get(f"/api/admin/queue/items/{item_id}").json()
        assert detail["status"] == "in_review"
        assert detail["preparations"][-1]["payload"]["material_source"] == "note"
        assert detail["preparations"][-1]["payload"]["summary"] == "요약(메모)"


class TestGates:
    """route 게이트 표면 (KDEV-WORK-014 P3 / SPEC-008·009)."""

    @staticmethod
    def _payload(**over):
        destinations = {
            "reference": {"enabled": over.get("reference", True)},
            "concept": {"enabled": over.get("concept", True)},
            "derived": {"enabled": over.get("derived", False)},
        }
        return {
            "destinations": destinations,
            "exclusive": over.get("exclusive"),
            "rationale": "근거",
        }

    @pytest.fixture
    def gated(self, client, monkeypatch, request):
        """준비까지 끝내 route 게이트가 열린 항목을 만든다.

        URL 은 테스트마다 고유해야 한다 — 같으면 두 번째부터 **기존 항목에 합류**해
        (S-4) 이미 `in_review` 인 항목에 준비를 재시도하게 되고 409 가 난다.
        """
        import hashlib

        video_id = hashlib.sha1(request.node.name.encode()).hexdigest()[:11]
        from tests.fakes import FakeRunner, FakeSummarizer

        summarize = FakeSummarizer(summary="요약본", session_ref="s1")

        async def fetch_ok(url):
            return {"url": url, "content": "본문"}

        runner = FakeRunner(payload=self._payload(), session_ref="gate-sess")

        monkeypatch.setattr("api.routers.queue._summarizer_factory", lambda: summarize)
        monkeypatch.setattr("api.routers.queue._runner_for", lambda stage: runner)
        monkeypatch.setattr("service.knowledge_capture.source.fetch_source", fetch_ok)

        item_id = _create(client, source_url=f"https://youtu.be/{video_id}").json()["item_id"]
        assert client.post(f"/api/admin/queue/items/{item_id}/prepare").status_code == 200
        gates = client.get(f"/api/admin/queue/items/{item_id}/gates").json()["gates"]
        assert len(gates) == 1 and gates[0]["stage_name"] == "route"
        return item_id, gates[0]["id"]

    def test_gate_is_exposed_with_revisions(self, client, gated):
        item_id, gate_id = gated
        gates = client.get(f"/api/admin/queue/items/{item_id}/gates").json()["gates"]
        gate = gates[0]
        assert gate["status"] == "review_pending"
        assert len(gate["revisions"]) == 1
        assert gate["revisions"][0]["payload"]["destinations"]["concept"]["enabled"] is True

    def test_short_feedback_is_422(self, client, gated):
        _, gate_id = gated
        response = client.post(f"/api/admin/queue/gates/{gate_id}/feedback", json={"body": "응"})
        assert response.status_code == 422
        assert response.json()["detail"]["code"] == "FEEDBACK_TOO_SHORT"

    def test_approve_confirms_destinations(self, client, gated):
        item_id, gate_id = gated
        response = client.post(f"/api/admin/queue/gates/{gate_id}/approve", json={})
        assert response.status_code == 200, response.text
        body = response.json()
        assert body["gate_status"] == "approved"
        assert body["route_outcome"] == "publishable"
        # 승인해도 항목은 아직 발행되지 않는다 — 발행은 WORK-015.
        assert body["item_status"] == "in_review"

    def test_approved_gate_rejects_feedback(self, client, gated):
        _, gate_id = gated
        client.post(f"/api/admin/queue/gates/{gate_id}/approve", json={})
        response = client.post(
            f"/api/admin/queue/gates/{gate_id}/feedback", json={"body": "역시 아닌 것 같다"}
        )
        assert response.status_code == 409
        assert response.json()["detail"]["code"] == "GATE_ALREADY_APPROVED"

    def test_human_edit_must_pass_the_same_validation(self, client, gated):
        """사람이 고친 값도 AI 출력과 같은 검사를 통과해야 한다."""
        _, gate_id = gated
        bad = self._payload(reference=False, concept=False, exclusive="discard")
        bad["destinations"]["reference"]["enabled"] = True  # exclusive 와 동시 — 금지 조합
        response = client.post(
            f"/api/admin/queue/gates/{gate_id}/approve", json={"payload": bad}
        )
        assert response.status_code == 422
        assert response.json()["detail"]["code"] == "INVALID_ROUTE_RESULT"

    def test_discard_approval_ends_item_without_files(self, client, gated, tmp_path):
        """폐기 승인은 항목을 끝낸다. 파일은 만들어지지 않는다."""
        item_id, gate_id = gated
        discard = self._payload(reference=False, concept=False, exclusive="discard")
        response = client.post(
            f"/api/admin/queue/gates/{gate_id}/approve", json={"payload": discard}
        )
        assert response.status_code == 200, response.text
        assert response.json()["route_outcome"] == "discarded"
        assert response.json()["item_status"] == "discarded"

        # 목록에서도 빠진다.
        listed = client.get("/api/admin/queue/items").json()
        assert item_id not in [i["id"] for i in listed["items"]]

    def test_regenerate_without_ai_path_is_503(self, client, gated, monkeypatch):
        _, gate_id = gated
        client.post(f"/api/admin/queue/gates/{gate_id}/feedback", json={"body": "다시 판단해 달라"})
        monkeypatch.setattr("api.routers.queue._runner_for", lambda stage: None)
        response = client.post(f"/api/admin/queue/gates/{gate_id}/regenerate")
        assert response.status_code == 503
        assert response.json()["detail"]["code"] == "GENERATOR_UNAVAILABLE"

    def test_gate_endpoints_require_auth(self, anon):
        for method, path in [
            ("get", "/api/admin/queue/items/1/gates"),
            ("post", "/api/admin/queue/gates/1/feedback"),
            ("post", "/api/admin/queue/gates/1/regenerate"),
            ("post", "/api/admin/queue/gates/1/retry"),
            ("post", "/api/admin/queue/gates/1/approve"),
        ]:
            kwargs = {"json": {}} if method == "post" else {}
            assert getattr(anon, method)(path, **kwargs).status_code == 401


class TestMeta:
    """화면 선택지는 서버가 준다 — 프론트에 목록을 복사해 두면 SoT 가 둘이 된다."""

    def test_pipeline_definition_is_exposed(self, client):
        stages = client.get("/api/admin/queue/meta").json()["pipelines"]["youtube"]
        assert [s["name"] for s in stages] == [
            "collect",
            "summarize",
            "route",
            "source_note",
            "concept",
            "derived",
        ]
        assert [s["name"] for s in stages if s["kind"] == "gate"][0] == "route"

    def test_meta_requires_auth(self, anon):
        assert anon.get("/api/admin/queue/meta").status_code == 401


class TestPublishTrigger:
    """마지막 게이트 승인이 발행 트리거다 — **다만 정말 마지막일 때만.**"""

    def test_blocked_chain_does_not_publish(self, client, monkeypatch):
        """생성기가 없어 다음 게이트를 못 열었는데 발행되면, reference 만 있고
        concept 는 없는 미완성 체인이 origin 에 나간다.
        """
        from tests.fakes import FakeRunner, FakeSummarizer

        summarize = FakeSummarizer(summary="요약")

        async def fetch_ok(url):
            return {"url": url, "content": "본문"}

        route_runner = FakeRunner(
            payload={
                "destinations": {
                    "reference": {"enabled": True, "group": "study"},
                    "concept": {"enabled": True},
                    "derived": {"enabled": False},
                },
                "exclusive": None,
            }
        )

        monkeypatch.setattr("api.routers.queue._summarizer_factory", lambda: summarize)
        # route 만 있고 source_note 실행기는 없다.
        monkeypatch.setattr("api.routers.queue._runners", lambda: {"route": route_runner})
        monkeypatch.setattr(
            "api.routers.queue._runner_for", lambda stage: route_runner if stage == "route" else None
        )
        monkeypatch.setattr("service.knowledge_capture.source.fetch_source", fetch_ok)

        item_id = _create(client, source_url="https://youtu.be/blockchain1").json()["item_id"]
        client.post(f"/api/admin/queue/items/{item_id}/prepare")
        gate_id = client.get(f"/api/admin/queue/items/{item_id}/gates").json()["gates"][0]["id"]

        body = client.post(f"/api/admin/queue/gates/{gate_id}/approve", json={}).json()

        assert body["blocked"] is True
        assert body["next_stage"] == "source_note"
        # **발행이 돌지 않았다** — 이게 핵심이다.
        assert body["published"] is None
        assert body["item_status"] == "in_review"

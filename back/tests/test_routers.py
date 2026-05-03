"""TDD — M3 라우터 11개 통합 테스트."""

import hashlib
import hmac

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    from main import app

    with TestClient(app) as c:
        yield c


class TestSite:
    def test_returns_200(self, client):
        r = client.get("/api/site")
        assert r.status_code == 200

    def test_lang_ko(self, client):
        d = client.get("/api/site").json()
        assert "홈서버" in d["site"]["footerTagline"]

    def test_lang_en(self, client):
        d = client.get("/api/site?lang=en").json()
        assert "homelab" in d["site"]["footerTagline"].lower()


class TestActivity:
    def test_returns_200_even_when_empty(self, client):
        # activity.yaml 미존재 시에도 200 + 빈 응답
        r = client.get("/api/activity")
        assert r.status_code == 200
        d = r.json()
        assert "activity" in d
        assert d["activity[]"] == []


class TestCareer:
    def test_lists_careers(self, client):
        d = client.get("/api/career").json()
        assert len(d["career[]"]) >= 1
        assert d["career[]"][0]["org"] == "Stealth AI Co."


class TestProjects:
    def test_returns_categories_with_counts(self, client):
        d = client.get("/api/projects").json()
        cats = {c["id"]: c["count"] for c in d["projects"]["categories"]}
        assert cats["web"] == 1  # homelab-console = web

    def test_total_count(self, client):
        d = client.get("/api/projects").json()
        assert d["projects"]["totalCount"] == 1


class TestNotesGraph:
    def test_includes_clusters(self, client):
        d = client.get("/api/notes/graph").json()
        cluster_ids = {c["id"] for c in d["notes"]["graph"]["clusters"]}
        assert "py" in cluster_ids and "ai" in cluster_ids

    def test_nodes_have_title(self, client):
        d = client.get("/api/notes/graph").json()
        nodes = d["notes"]["graph"]["nodes"]
        assert len(nodes) >= 1
        assert any(n["id"] == "python-asyncio" for n in nodes)

    def test_edges_from_wikilinks(self, client):
        d = client.get("/api/notes/graph").json()
        edges = d["notes"]["graph"]["edges"]
        # python-asyncio.md → [[fastapi-di]], [[uvicorn-workers]]
        assert {"source": "python-asyncio", "target": "fastapi-di"} in edges


class TestNotesRecent:
    def test_returns_recent_notes(self, client):
        d = client.get("/api/notes/recent?limit=5").json()
        assert len(d["notes.recent[]"]) >= 1


class TestNotesDetail:
    def test_returns_existing_note(self, client):
        d = client.get("/api/notes/python-asyncio").json()
        assert d["notes.detail"]["id"] == "python-asyncio"
        assert "Event Loop" in d["notes.detail"]["body"]

    def test_404_for_unknown_note(self, client):
        r = client.get("/api/notes/nonexistent")
        assert r.status_code == 404


class TestNotesSearch:
    def test_finds_by_title_keyword(self, client):
        d = client.get("/api/notes/search?q=asyncio").json()
        ids = [n["id"] for n in d["notes.recent[]"]]
        assert "python-asyncio" in ids

    def test_empty_query_rejected(self, client):
        r = client.get("/api/notes/search?q=")
        assert r.status_code == 422


class TestContents:
    def test_lists_contents(self, client):
        # spec-06 — status: published 만 노출 (status 미명시는 default published)
        d = client.get("/api/contents").json()
        assert d["contents"]["totalCount"] >= 1
        assert "contents[]" in d
        assert len(d["contents[]"]) >= 1


class TestContentsDetail:
    def test_returns_concept_and_body(self, client):
        # spec-06 §3.3 — concept (frontmatter 직접) + body (markdown 8섹션) 응답.
        # C-001 mock 은 frontmatter concept 없을 수 있어 빈 list 도 OK.
        d = client.get("/api/contents/C-001").json()
        detail = d["contents.detail"]
        assert "concept" in detail and isinstance(detail["concept"], list)
        assert "body" in detail and isinstance(detail["body"], str)

    def test_404_for_unknown_id(self, client):
        r = client.get("/api/contents/C-999")
        assert r.status_code == 404


class TestAdminReload:
    def test_requires_token(self, client, monkeypatch):
        monkeypatch.setenv("RELOAD_TOKEN", "secret")
        r = client.post("/admin/reload")
        assert r.status_code == 403

    def test_reloads_with_correct_token(self, client, monkeypatch):
        monkeypatch.setenv("RELOAD_TOKEN", "secret")
        r = client.post("/admin/reload", headers={"X-Reload-Token": "secret"})
        assert r.status_code == 200
        assert r.json()["status"] == "reloaded"


def _hmac_sig(secret: bytes, body: bytes) -> str:
    return "sha256=" + hmac.new(secret, body, hashlib.sha256).hexdigest()


class TestAdminReloadWebhook:
    def test_hmac_valid_signature_passes(self, client, monkeypatch):
        monkeypatch.setenv("GITHUB_WEBHOOK_SECRET", "wsecret")
        # push event 시 _git_pull_rebase 호출됨 → 테스트 환경에선 no-op mock
        from api.admin import reload as reload_mod
        monkeypatch.setattr(reload_mod, "_git_pull_rebase", lambda: None)
        body = b'{"ref":"refs/heads/main"}'
        r = client.post(
            "/admin/reload",
            content=body,
            headers={
                "X-Hub-Signature-256": _hmac_sig(b"wsecret", body),
                "X-GitHub-Event": "push",
            },
        )
        assert r.status_code == 200
        assert r.json()["status"] == "reloaded"

    def test_hmac_invalid_signature_403(self, client, monkeypatch):
        monkeypatch.setenv("GITHUB_WEBHOOK_SECRET", "wsecret")
        r = client.post(
            "/admin/reload",
            content=b"{}",
            headers={"X-Hub-Signature-256": "sha256=wrong"},
        )
        assert r.status_code == 403

    def test_ping_event_returns_pong(self, client, monkeypatch):
        monkeypatch.setenv("GITHUB_WEBHOOK_SECRET", "wsecret")
        body = b""
        r = client.post(
            "/admin/reload",
            content=body,
            headers={
                "X-Hub-Signature-256": _hmac_sig(b"wsecret", body),
                "X-GitHub-Event": "ping",
            },
        )
        assert r.status_code == 200
        assert r.json()["status"] == "pong"

    def test_no_secret_configured_falls_back_to_token(self, client, monkeypatch):
        # webhook secret 안 박혀도 토큰으로 통과 가능
        monkeypatch.delenv("GITHUB_WEBHOOK_SECRET", raising=False)
        monkeypatch.setenv("RELOAD_TOKEN", "tok")
        r = client.post("/admin/reload", headers={"X-Reload-Token": "tok"})
        assert r.status_code == 200

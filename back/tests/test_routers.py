"""TDD — M3 라우터 11개 통합 테스트."""

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
        d = client.get("/api/contents").json()
        assert d["contents"]["totalCount"] >= 1
        assert d["contents[]"][0]["id"] == "C-001"


class TestContentsDetail:
    def test_extracts_concept_section(self, client):
        d = client.get("/api/contents/C-001").json()
        # contents/C-001-fastapi-di.md 본문에 ## 개념 + bullet 박힘
        assert len(d["contents.detail"]["concept"]) > 0

    def test_extracts_example_section(self, client):
        d = client.get("/api/contents/C-001").json()
        assert len(d["contents.detail"]["example"]) > 0

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

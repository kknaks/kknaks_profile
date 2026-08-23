"""TDD — M3 라우터 11개 통합 테스트."""

import hashlib
import hmac

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def client():
    """모듈당 한 번만 띄운다 — lifespan(=load_all) 이 1.1초라 38건이면 40초를 쓴다.

    공유해도 안전한 이유: 이 파일은 로그인·쿠키를 쓰지 않아 client 에 남는 상태가 없고,
    `main._data` 는 conftest 의 autouse fixture 가 테스트마다 스냅샷에서 되돌린다.
    (쿠키를 다루는 test_auth 는 함수 스코프를 유지한다 — 공유하면 세션이 샌다.)
    """
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
    def test_returns_list_shape(self, client):
        # /api/activity — 200 + list shape (실 데이터 의존 X)
        r = client.get("/api/activity")
        assert r.status_code == 200
        d = r.json()
        assert "activity" in d
        assert isinstance(d["activity[]"], list)


class TestCareer:
    def test_lists_careers(self, client):
        d = client.get("/api/career").json()
        assert len(d["career[]"]) >= 1
        assert "org" in d["career[]"][0]


class TestProjects:
    def test_returns_categories_with_counts(self, client):
        d = client.get("/api/projects").json()
        cats = {c["id"]: c["count"] for c in d["projects"]["categories"]}
        assert isinstance(cats, dict)
        assert all(isinstance(v, int) for v in cats.values())

    def test_total_count(self, client):
        d = client.get("/api/projects").json()
        assert d["projects"]["totalCount"] >= 1


class TestNotesRemoved:
    """`/api/notes/*` 는 없앴다 — `resources/` 는 R(개인 지식)이고 공개 표면이 아니다.

    화면이 안 쓰는데 열려 있으면 **다음 사람이 그것을 보고 다시 붙인다.** 없는 것이
    닫힌 것보다 확실하다.
    """

    @pytest.mark.parametrize(
        "path",
        ["/api/notes/graph", "/api/notes/recent", "/api/notes/search?q=x", "/api/notes/x"],
    )
    def test_gone(self, client, path):
        assert client.get(path).status_code == 404


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
        _noop_reload_background(monkeypatch)
        r = client.post("/admin/reload", headers={"X-Reload-Token": "secret"})
        assert r.status_code == 200
        assert r.json()["status"] == "reloaded"


def _hmac_sig(secret: bytes, body: bytes) -> str:
    return "sha256=" + hmac.new(secret, body, hashlib.sha256).hexdigest()


def _noop_reload_background(monkeypatch):
    from api.admin import reload as reload_mod

    async def noop():
        return None

    monkeypatch.setattr(reload_mod, "_run_enrich_safe", noop)
    monkeypatch.setattr(reload_mod, "_run_pdf_safe", noop)


class TestAdminReloadWebhook:
    def test_hmac_valid_signature_passes(self, client, monkeypatch):
        monkeypatch.setenv("GITHUB_WEBHOOK_SECRET", "wsecret")
        _noop_reload_background(monkeypatch)
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
        _noop_reload_background(monkeypatch)
        r = client.post("/admin/reload", headers={"X-Reload-Token": "tok"})
        assert r.status_code == 200


class TestAlgorithms:
    """spec-07 — /api/algorithms + /api/algorithms/{id}."""

    def test_list_returns_200(self, client):
        r = client.get("/api/algorithms")
        assert r.status_code == 200

    def test_list_shape(self, client):
        d = client.get("/api/algorithms").json()
        assert "algorithms" in d
        assert "algorithms[]" in d
        assert "totalCount" in d["algorithms"]
        assert "today" in d["algorithms"]

    def test_list_includes_seed(self, client):
        d = client.get("/api/algorithms").json()
        ids = [a["id"] for a in d["algorithms[]"]]
        assert "A-001" in ids

    def test_list_today_pick(self, client):
        d = client.get("/api/algorithms").json()
        today = d["algorithms"]["today"]
        ids = [a["id"] for a in d["algorithms[]"]]
        assert today is not None
        assert today["id"] in ids

    def test_list_lang_ko(self, client):
        d = client.get("/api/algorithms?lang=ko").json()
        assert "neetcode" in d["algorithms"]["subtitle"].lower()
        # 한글 평탄화 — title 이 string
        assert isinstance(d["algorithms[]"][0]["title"], str)

    def test_list_lang_en(self, client):
        d = client.get("/api/algorithms?lang=en").json()
        assert isinstance(d["algorithms[]"][0]["title"], str)

    def test_detail_returns_existing(self, client):
        r = client.get("/api/algorithms/A-001")
        assert r.status_code == 200
        d = r.json()
        det = d["algorithms.detail"]
        assert det["id"] == "A-001"
        # 6 data 키
        for k in ("problem", "clarifying", "approach", "logic", "trace", "solution"):
            assert k in det

    def test_detail_logic_slot_format(self, client):
        d = client.get("/api/algorithms/A-001").json()
        assert d["algorithms.detail"]["logic"]["format"] == "slot"

    def test_detail_trace_simple_shape(self, client):
        # adr-09: code + cases + worked_example
        d = client.get("/api/algorithms/A-001").json()
        trace = d["algorithms.detail"]["trace"]
        assert "code" in trace
        assert "cases" in trace
        assert "worked_example" in trace
        # step-by-step 폐기 — old 'steps' 키 없음
        assert "steps" not in trace

    def test_detail_404(self, client):
        r = client.get("/api/algorithms/A-999")
        assert r.status_code == 404

    def test_detail_i18n_flatten(self, client):
        # ko 응답에 영어만 들어있는 필드 X — distractor.why 같은 nested {ko, en} 도 평탄화
        d = client.get("/api/algorithms/A-001?lang=ko").json()
        clarifying = d["algorithms.detail"]["clarifying"]["items"]
        assert len(clarifying) > 0
        # 첫 항목의 q 가 string 으로 평탄화
        assert isinstance(clarifying[0]["q"], str)
        # why 도 string
        assert isinstance(clarifying[0]["why"], str)

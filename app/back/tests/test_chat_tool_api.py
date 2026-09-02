"""P2 — chat-tool API · 노출 경계 · turn 토큰 (SPEC-017 §3 S-9 · §4 Tool Contract).

지키는 것 셋: **토큰 없는 호출은 못 들어온다** · **미노출은 없는 것과 같다** ·
**어드민 토글이 다음 호출부터 먹는다**(캐시·export 없음 — DEC-027 D4).
"""

from __future__ import annotations

from datetime import date

import pytest
from sqlalchemy import select

from config import get_settings
from core.security import create_access_token
from models import (
    Algorithm,
    Career,
    Company,
    Content,
    Note,
    Problem,
    Product,
    Profile,
    Project,
    User,
)
from service.chat.turn_token import turn_token_service


@pytest.fixture
async def ledger(db):
    """이력 데이터 한 벌. **전부 chat_exposed=False 로 시작한다**(옵트인이 기본)."""
    profile = Profile(
        handle="kknaks",
        name="이건학",
        role="백엔드 엔지니어",
        years="1년차",
        location="서울",
        focus="AI · Python",
        email="kknaks@kknaks.dev",
        stack=["Python", "FastAPI"],
    )
    company = Company(slug="medisolve-ai", name="메디솔브 AI", location="서울")
    db.add_all([profile, company])
    await db.flush()

    career = Career(
        profile_id=profile.id,
        company_id=company.id,
        title="백엔드 개발자",
        started_on=date(2026, 2, 1),
        summary="AI 파이프라인을 만들었습니다",
        description="상세: 워커·큐·게이트를 세웠습니다",
        stack=["Python"],
    )
    project = Project(
        profile_id=profile.id,
        slug="wine-log",
        title="와인 로그",
        summary="마신 와인을 기록하는 앱",
        detail_path="para/projects/summer-star/wine-log/showcase.md",
        status="live",
    )
    note = Note(
        profile_id=profile.id,
        slug="fastapi-di",
        title="FastAPI 의존성 주입",
        summary="Depends 가 하는 일",
        detail_path="para/resources/note/fastapi-di.md",
        tags=["fastapi"],
    )
    db.add_all([career, project, note])
    await db.flush()

    problem = Problem(
        career_id=career.id, title="큐가 밀리던 문제", body="전용 큐로 갈랐습니다"
    )
    # 회사 제품 — `career` 에 매달린다(개인 `project` 와 다른 표다).
    product = Product(
        career_id=career.id,
        slug="mediness",
        title="Mediness",
        summary="사내 AX 워크스페이스",
        detail_path="para/projects/company/mediness/showcase.md",
        status="live",
        stack=["FastAPI"],
    )
    db.add_all([problem, product])
    await db.commit()
    return {
        "career": career.id,
        "career_slug": f"medisolve-ai-{career.id}",
        "project": project.id,
        "problem": problem.id,
        "problem_slug": f"problem-{problem.id}",
        "product": product.id,
        "profile": profile.id,
    }


@pytest.fixture
async def turn(client, db):
    """살아 있는 turn 토큰 하나 — 대화를 만들고 그 pending 답변에 매단다."""
    created = await client.post("/api/chat/conversations", json={"question": "질문"})
    message_id = created.json()["messages"][1]["id"]
    token = await turn_token_service.issue(db, message_id)
    await db.commit()
    return {"token": token, "message_id": message_id}


def _auth(turn) -> dict:
    return {"Authorization": f"Bearer {turn['token']}"}


@pytest.fixture
async def admin(client, db):
    """어드민 쿠키 — 노출 토글은 기존 인증 방식을 그대로 쓴다."""
    profile = Profile(handle="a", name="a", role="a", email="a@a.a")
    db.add(profile)
    await db.flush()
    user = User(
        username="admin",
        password_hash="x",
        system_role="admin",
        profile_id=profile.id,
    )
    db.add(user)
    await db.commit()
    client.cookies.set(
        get_settings().auth_cookie_name,
        create_access_token(username="admin", uid=user.id, role="admin"),
    )
    return user


# ── turn 토큰 (DEC-027 D5) ──────────────────────────────
async def test_no_token_is_401(client, ledger):
    res = await client.get("/api/chat-tool/careers")

    assert res.status_code == 401


async def test_garbage_token_is_401(client, ledger):
    res = await client.get(
        "/api/chat-tool/careers", headers={"Authorization": "Bearer nope"}
    )

    assert res.status_code == 401


async def test_revoked_token_is_401(client, db, ledger, turn):
    """폐기 = 해시를 지우는 것. 그 뒤로는 구조적으로 못 찾는다."""
    ok = await client.get("/api/chat-tool/careers", headers=_auth(turn))
    assert ok.status_code == 200

    await turn_token_service.revoke(db, turn["message_id"])
    await db.commit()

    res = await client.get("/api/chat-tool/careers", headers=_auth(turn))
    assert res.status_code == 401


async def test_expired_token_is_401(client, db, ledger, turn):
    from datetime import UTC, datetime, timedelta

    from models.chat import ChatMessage

    message = await db.get(ChatMessage, turn["message_id"])
    message.turn_token_expires_at = datetime.now(UTC) - timedelta(seconds=1)
    await db.commit()

    res = await client.get("/api/chat-tool/careers", headers=_auth(turn))
    assert res.status_code == 401


# ── 노출 경계 (DEC-027 D4 · §3 S-9) ─────────────────────
async def test_unexposed_is_absent_from_list(client, ledger, turn):
    """기본은 false — 승인 전에는 목록이 비어 있다."""
    res = await client.get("/api/chat-tool/careers", headers=_auth(turn))

    assert res.status_code == 200
    assert res.json() == {"items": [], "count": 0}


async def test_unexposed_detail_is_404(client, ledger, turn):
    """미노출 상세는 404 — AI 에게는 존재하지 않는 문서다."""
    res = await client.get(
        f"/api/chat-tool/careers/{ledger['career_slug']}", headers=_auth(turn)
    )

    assert res.status_code == 404


@pytest.mark.parametrize(
    ("kind", "key", "list_path"),
    [
        ("career", "career", "/api/chat-tool/careers"),
        ("project", "project", "/api/chat-tool/projects"),
        ("problem", "problem", "/api/chat-tool/problems"),
        # 회사 제품도 **같은 축**이다 — 새 기계가 아니라 kind 확장(spec v0.0.8).
        ("product", "product", "/api/chat-tool/company-products"),
    ],
)
async def test_admin_toggle_takes_effect_immediately(
    client, ledger, turn, admin, kind, key, list_path
):
    """토글 직후의 호출부터 반영된다 — export · 재시작 · 캐시가 없다(U-7)."""
    before = await client.get(list_path, headers=_auth(turn))
    assert before.json()["count"] == 0

    patched = await client.patch(
        f"/api/admin/chat-exposure/{kind}/{ledger[key]}", json={"chatExposed": True}
    )
    assert patched.status_code == 200
    assert patched.json() == {"kind": kind, "id": ledger[key], "chatExposed": True}

    after = await client.get(list_path, headers=_auth(turn))
    assert after.json()["count"] == 1

    # 다시 끄면 다시 사라진다 — 경계가 한 방향이 아니다.
    await client.patch(
        f"/api/admin/chat-exposure/{kind}/{ledger[key]}", json={"chatExposed": False}
    )
    assert (await client.get(list_path, headers=_auth(turn))).json()["count"] == 0


async def test_toggle_requires_admin(client, ledger):
    res = await client.patch(
        "/api/admin/chat-exposure/career/1", json={"chatExposed": True}
    )

    assert res.status_code == 401


async def test_toggle_rejects_unknown_kind(client, ledger, admin):
    """`{kind}` 로 아무 표나 건드릴 수 없다 — 허용 목록이 셋뿐이다."""
    res = await client.patch(
        "/api/admin/chat-exposure/user/1", json={"chatExposed": True}
    )

    assert res.status_code == 422


async def test_toggle_unknown_id_is_404(client, ledger, admin):
    res = await client.patch(
        "/api/admin/chat-exposure/career/999999", json={"chatExposed": True}
    )

    assert res.status_code == 404


# ── 합성 slug (코디 승인 조건 ①) ────────────────────────
async def test_exposed_detail_returns_body(client, db, ledger, turn, admin):
    """career 의 상세는 DB 컬럼(description)이다 — 원장 md 가 없다."""
    await client.patch(
        f"/api/admin/chat-exposure/career/{ledger['career']}", json={"chatExposed": True}
    )

    res = await client.get(
        f"/api/chat-tool/careers/{ledger['career_slug']}", headers=_auth(turn)
    )

    assert res.status_code == 200
    item = res.json()["item"]
    assert item["slug"] == ledger["career_slug"]
    assert item["body"] == "상세: 워커·큐·게이트를 세웠습니다"
    # 근거 카드가 걸 링크 — career 는 전용 페이지가 없어 공개 표면을 가리킨다.
    assert item["url"] == "/career"


@pytest.mark.parametrize(
    "slug",
    [
        "not-a-slug",              # 숫자 꼬리가 없다 — 파싱 실패
        "medisolve-ai-999999",     # 형식은 맞고 id 가 없다
        "wrong-company-1",         # id 는 맞지만 정본 slug 와 다르다
    ],
)
async def test_bad_career_slug_is_always_404(client, ledger, turn, admin, slug):
    """파싱 실패 · 없는 id · 접두사 불일치가 **전부 같은 404** 다."""
    await client.patch(
        f"/api/admin/chat-exposure/career/{ledger['career']}", json={"chatExposed": True}
    )

    res = await client.get(f"/api/chat-tool/careers/{slug}", headers=_auth(turn))

    assert res.status_code == 404


async def test_problem_slug_roundtrip(client, ledger, turn, admin):
    await client.patch(
        f"/api/admin/chat-exposure/problem/{ledger['problem']}",
        json={"chatExposed": True},
    )

    listed = await client.get("/api/chat-tool/problems", headers=_auth(turn))
    slug = listed.json()["items"][0]["slug"]
    assert slug == ledger["problem_slug"]

    detail = await client.get(f"/api/chat-tool/problems/{slug}", headers=_auth(turn))
    assert detail.status_code == 200
    assert detail.json()["item"]["body"] == "전용 큐로 갈랐습니다"
    assert detail.json()["item"]["url"] == "/career"


@pytest.mark.parametrize(
    "slug",
    [
        "12",                # 접두사가 없다 — 파싱 실패
        "problem-999999",    # 형식은 맞고 id 가 없다
        "problem-0000001",   # id 는 같은 행에 닿지만 정본 slug 가 아니다
    ],
)
async def test_bad_problem_slug_is_always_404(client, ledger, turn, admin, slug):
    """career 와 **같은 규약**이다 — 정본 slug 불일치도 404(리뷰 W4).

    `problem-007` 류가 200 을 받으면 응답·근거 카드의 slug 가 요청과 달라져 같은
    문서에 손잡이가 둘 생긴다.
    """
    await client.patch(
        f"/api/admin/chat-exposure/problem/{ledger['problem']}",
        json={"chatExposed": True},
    )

    res = await client.get(f"/api/chat-tool/problems/{slug}", headers=_auth(turn))

    assert res.status_code == 404


# ── 판정식: 공개 조건 ∧ chat_exposed (spec v0.0.14 §4) ──
#
# DEC-027 D3 「공개 API 가 보여 주는 것 = tool 의 상한」이 식으로 내려온 것이다.
# 공개 표면에서 내린 항목이 tool 에 실리면 근거 카드가 404 페이지를 가리킨다.
# 유형별 공개 조건 표는 `repository/chat_tool_repo.py` 머리 주석에 있다.
async def test_hidden_project_is_absent_even_when_chat_exposed(client, db, ledger, turn, admin):
    """**`chat_exposed` 만으로는 부족하다** — `visible=false` 면 tool 에서 빠진다.

    이 조합(공개 표면에서 내렸는데 chat 노출은 켜져 있음)이 실측 결함의 모양이다.
    """
    await client.patch(
        f"/api/admin/chat-exposure/project/{ledger['project']}",
        json={"chatExposed": True},
    )
    project = await db.get(Project, ledger["project"])
    project.visible = False
    await db.commit()

    listed = await client.get("/api/chat-tool/projects", headers=_auth(turn))
    detail = await client.get("/api/chat-tool/projects/wine-log", headers=_auth(turn))

    assert listed.json()["count"] == 0
    assert detail.status_code == 404


async def test_visible_project_still_needs_chat_exposed(client, ledger, turn):
    """반대 방향도 그대로다 — 사이트에 떠 있어도 승인 전에는 AI 에게 없다."""
    listed = await client.get("/api/chat-tool/projects", headers=_auth(turn))
    detail = await client.get("/api/chat-tool/projects/wine-log", headers=_auth(turn))

    assert listed.json()["count"] == 0      # visible=true 인데 chat_exposed=false
    assert detail.status_code == 404


async def test_hidden_note_detail_is_404(client, db, ledger, turn):
    """note 는 `chat_exposed` 축이 없다 — `visible` 이 곧 공개 조건이고 상세도 그걸 본다."""
    note = (await db.execute(select(Note))).scalars().one()
    note.visible = False
    await db.commit()

    res = await client.get("/api/chat-tool/notes/fastapi-di", headers=_auth(turn))

    assert res.status_code == 404


@pytest.mark.parametrize(
    ("model", "path"),
    [(Content, "/api/chat-tool/contents"), (Algorithm, "/api/chat-tool/algorithms")],
)
async def test_hidden_content_and_algorithm_are_absent(
    client, db, ledger, turn, model, path
):
    """content · algorithm 도 `visible` 이 공개 조건이다(목록 전용 tool)."""
    row = model(
        profile_id=ledger["profile"],
        slug="hidden-one",
        title="숨긴 것",
        detail_path="para/resources/x.md",
        visible=False,
        **(
            {"youtube_id": "abc"}
            if model is Content
            else {"difficulty": "easy", "source_platform": "leetcode"}
        ),
    )
    db.add(row)
    await db.commit()

    res = await client.get(path, headers=_auth(turn))

    assert [i["slug"] for i in res.json()["items"]] == []


# ── 회사 제품 (spec v0.0.8) ─────────────────────────────
async def test_company_product_detail_reads_showcase(client, ledger, turn, admin):
    """노출을 켜면 showcase.md 본문이 실린다 — 이것이 fix3 에서 막혀 있던 자리다."""
    await client.patch(
        f"/api/admin/chat-exposure/product/{ledger['product']}",
        json={"chatExposed": True},
    )

    res = await client.get(
        "/api/chat-tool/company-products/mediness", headers=_auth(turn)
    )

    assert res.status_code == 200
    item = res.json()["item"]
    # 문서 유형은 표 이름(`product`)이 아니라 `company_product` 다 — 근거 카드에서
    # 개인 프로젝트와 구분돼야 한다(spec v0.0.9 · FE `ChatSourceType`).
    assert item["type"] == "company_product"
    assert item["slug"] == "mediness"
    # 어느 회사·어느 역할에서 만들었나가 앞자리에 온다.
    assert "메디솔브 AI" in item["subtitle"]
    assert item["meta"]["role"] == "백엔드 개발자"
    # 제품 전용 페이지는 없지만 **그 제품의 회사 경력이 그려지는 표면**으로 보낸다 —
    # 화살표가 있는 카드는 눌려야 한다(owner 판정 · spec v0.0.9 §4).
    assert item["url"] == "/career"


async def test_unexposed_company_product_detail_is_404(client, ledger, turn):
    """기본은 false — 승인 전에는 AI 에게 존재하지 않는 제품이다."""
    res = await client.get(
        "/api/chat-tool/company-products/mediness", headers=_auth(turn)
    )

    assert res.status_code == 404


async def test_unknown_company_product_slug_is_404(client, ledger, turn, admin):
    await client.patch(
        f"/api/admin/chat-exposure/product/{ledger['product']}",
        json={"chatExposed": True},
    )

    res = await client.get(
        "/api/chat-tool/company-products/nope", headers=_auth(turn)
    )

    assert res.status_code == 404


async def test_invisible_company_product_is_hidden(client, db, ledger, turn, admin):
    """`visible` 과 `chat_exposed` 는 다른 축이고 **둘 다** 켜져야 한다."""
    await client.patch(
        f"/api/admin/chat-exposure/product/{ledger['product']}",
        json={"chatExposed": True},
    )
    product = await db.get(Product, ledger["product"])
    product.visible = False
    await db.commit()

    listed = await client.get("/api/chat-tool/company-products", headers=_auth(turn))
    detail = await client.get(
        "/api/chat-tool/company-products/mediness", headers=_auth(turn)
    )

    assert listed.json()["count"] == 0
    assert detail.status_code == 404


async def test_company_products_and_personal_projects_are_separate(
    client, ledger, turn, admin
):
    """회사 제품과 개인 프로젝트가 **서로의 목록에 섞이지 않는다**.

    표가 갈리고 tool 이 갈린다 — 「회사 일」과 「혼자 만든 것」이 섞이면 이력이 흐려진다.
    """
    for kind, key in (("product", "product"), ("project", "project")):
        await client.patch(
            f"/api/admin/chat-exposure/{kind}/{ledger[key]}", json={"chatExposed": True}
        )

    products = await client.get("/api/chat-tool/company-products", headers=_auth(turn))
    projects = await client.get("/api/chat-tool/projects", headers=_auth(turn))

    assert [i["slug"] for i in products.json()["items"]] == ["mediness"]
    assert [i["slug"] for i in projects.json()["items"]] == ["wine-log"]


async def test_archived_company_product_reads_showcase(client, db, ledger, turn, admin):
    """전 회사 제품(`para/archive/company/`)도 같은 tool 로 읽힌다(v0.0.8)."""
    product = await db.get(Product, ledger["product"])
    product.detail_path = "para/archive/company/linky/showcase.md"
    await db.commit()
    await client.patch(
        f"/api/admin/chat-exposure/product/{ledger['product']}",
        json={"chatExposed": True},
    )

    res = await client.get(
        "/api/chat-tool/company-products/mediness", headers=_auth(turn)
    )

    assert res.status_code == 200
    # 실원장에 그 파일이 있다면 본문이 실린다 — 없어도 404 는 아니다(요약까지는 준다).
    assert res.json()["item"]["slug"] == "mediness"


@pytest.mark.parametrize(
    "detail_path",
    [
        "para/projects/company/mediness/log/SUMMARY.md",   # 작업 회고
        "para/archive/company/linky/README.md",            # 내부 안내
        "para/resources/persona/secret.md",                # 개인 지식
    ],
)
async def test_company_product_body_is_absent_outside_public_root(
    client, db, ledger, turn, admin, detail_path
):
    """showcase.md 밖이면 본문을 안 읽는다 — 그래도 404 가 아니라 「요약까지만」이다."""
    product = await db.get(Product, ledger["product"])
    product.detail_path = detail_path
    await db.commit()
    await client.patch(
        f"/api/admin/chat-exposure/product/{ledger['product']}",
        json={"chatExposed": True},
    )

    res = await client.get(
        "/api/chat-tool/company-products/mediness", headers=_auth(turn)
    )

    assert res.status_code == 200
    assert "body" not in res.json()["item"]


# ── 나머지 tool 표면 ────────────────────────────────────
async def test_profile_tool(client, ledger, turn):
    res = await client.get("/api/chat-tool/profile", headers=_auth(turn))

    assert res.status_code == 200
    assert res.json()["item"]["name"] == "이건학"
    assert res.json()["item"]["email"] == "kknaks@kknaks.dev"


async def test_notes_are_gated_by_visible_only(client, ledger, turn):
    """note · content · algorithm 은 `chat_exposed` 축이 없다 — 이미 공개 페이지가 있다."""
    res = await client.get("/api/chat-tool/notes", headers=_auth(turn))

    assert res.json()["count"] == 1
    assert res.json()["items"][0]["slug"] == "fastapi-di"
    assert res.json()["items"][0]["url"] == "/notes/fastapi-di"


async def test_note_search_filters(client, ledger, turn):
    hit = await client.get(
        "/api/chat-tool/notes", params={"query": "의존성"}, headers=_auth(turn)
    )
    miss = await client.get(
        "/api/chat-tool/notes", params={"query": "쿠버네티스"}, headers=_auth(turn)
    )

    assert hit.json()["count"] == 1
    assert miss.json()["count"] == 0


async def test_hidden_note_is_absent(client, db, ledger, turn):
    note = (await db.execute(select(Note))).scalars().first()
    note.visible = False
    await db.commit()

    res = await client.get("/api/chat-tool/notes", headers=_auth(turn))
    assert res.json()["count"] == 0


@pytest.mark.parametrize(
    "detail_path",
    [
        "para/resources/persona/secret.md",   # 개인 지식 — 공개 루트 밖
        "para/projects/company/x/spec.md",    # 회사 기록 — 공개 루트 밖
        "para/projects/summer-star/none.md",  # 공개 루트 안이지만 끊긴 경로
    ],
)
async def test_project_body_is_absent_outside_public_root(
    client, db, ledger, turn, admin, detail_path
):
    """공개 루트 밖이면 본문을 읽지 않는다 — 그래도 **404 가 아니다**.

    행은 실재하고 요약은 줄 수 있다. 거부와 「파일 없음」을 구분하지 않는 것도 계약이다
    (`core/chat_detail.py`) — 구분하면 AI 에게 「있는데 못 준다」가 보인다.
    """
    project = await db.get(Project, ledger["project"])
    project.detail_path = detail_path
    await db.commit()

    await client.patch(
        f"/api/admin/chat-exposure/project/{ledger['project']}",
        json={"chatExposed": True},
    )
    res = await client.get("/api/chat-tool/projects/wine-log", headers=_auth(turn))

    assert res.status_code == 200
    assert "body" not in res.json()["item"]
    assert res.json()["item"]["url"] == "/projects/wine-log"


async def test_contents_and_algorithms_are_empty_lists(client, ledger, turn):
    for path in ("/api/chat-tool/contents", "/api/chat-tool/algorithms"):
        res = await client.get(path, headers=_auth(turn))
        assert res.status_code == 200
        assert res.json() == {"items": [], "count": 0}

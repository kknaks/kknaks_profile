"""공개 문서 루트 밖은 읽지 않는다 (SPEC-017 §5 · `core/chat_detail.py`).

원장을 건드리지 않으려고 임시 디렉토리를 리포 루트로 세워 검사한다 — 실제 `para/` 의
파일 유무에 결과가 흔들리면 이 테스트는 원장의 상태를 재는 것이지 가드를 재는 것이
아니게 된다.
"""

from __future__ import annotations

import pytest

from config import get_settings
from core.chat_detail import is_public_path, read_public_detail


@pytest.fixture
def ledger(tmp_path, monkeypatch):
    """`para/` 를 흉내 낸 임시 원장. 공개 자리 하나와 비공개 자리 하나를 둔다."""
    showcase = tmp_path / "para" / "projects" / "summer-star" / "wine-log"
    showcase.mkdir(parents=True)
    (showcase / "showcase.md").write_text("# 와인 로그\n\n본문", encoding="utf-8")

    persona = tmp_path / "para" / "resources" / "persona"
    persona.mkdir(parents=True)
    (persona / "secret.md").write_text("개인 지식", encoding="utf-8")

    # 회사 제품 — **한 디렉토리 안에 공개(showcase.md)와 내부 기록이 섞여 있다.**
    company = tmp_path / "para" / "projects" / "company" / "mediness"
    company.mkdir(parents=True)
    (company / "showcase.md").write_text("# Mediness\n\n제품 소개", encoding="utf-8")
    (company / "spec.md").write_text("회사 기록", encoding="utf-8")
    (company / "README.md").write_text("내부 안내", encoding="utf-8")
    (company / "log").mkdir()
    (company / "log" / "SUMMARY.md").write_text("작업 회고", encoding="utf-8")
    # 하위 디렉토리의 **동명 파일** — 파일명만 보면 새는 자리다.
    (company / "log" / "showcase.md").write_text("회고 안의 동명 파일", encoding="utf-8")

    # 전 회사 제품 — 채용담당자 질문의 핵심이라 v0.0.8 이 같은 규칙으로 열었다.
    archive = tmp_path / "para" / "archive" / "company" / "linky"
    archive.mkdir(parents=True)
    (archive / "showcase.md").write_text("# Linky\n\n전 회사 제품", encoding="utf-8")
    (archive / "README.md").write_text("내부 안내", encoding="utf-8")
    (archive / "log").mkdir()
    (archive / "log" / "showcase.md").write_text("회고 안의 동명 파일", encoding="utf-8")

    monkeypatch.setenv("REPO_ROOT", str(tmp_path))
    get_settings.cache_clear()
    yield tmp_path
    get_settings.cache_clear()


def test_reads_inside_public_root(ledger):
    body = read_public_detail(
        "project", "para/projects/summer-star/wine-log/showcase.md"
    )

    assert body is not None
    assert "와인 로그" in body


def test_rejects_private_sibling(ledger):
    """`para/resources/persona/` 는 개인 지식이다 — note 루트가 아니다(DEC-027 D3)."""
    assert is_public_path("note", "para/resources/persona/secret.md") is False
    assert read_public_detail("note", "para/resources/persona/secret.md") is None


# ── 회사 제품 — showcase.md **한 파일만** (spec v0.0.7 §4 · v0.0.8 로 archive 추가) ──
def test_reads_company_product_showcase(ledger):
    """사이트가 이미 공개로 그리는 상세다 — chat 만 못 읽을 이유가 없다(owner 피드백)."""
    body = read_public_detail(
        "company_product", "para/projects/company/mediness/showcase.md"
    )

    assert body is not None
    assert "Mediness" in body


@pytest.mark.parametrize(
    "relative",
    [
        "spec.md",            # 회사 내부 기록
        "README.md",          # 내부 안내
        "log/SUMMARY.md",     # 작업 회고 — 이력의 원료지 공개 자료가 아니다
        "log/showcase.md",    # **하위 디렉토리의 동명 파일** — 파일명만 보면 샌다
    ],
)
def test_rejects_everything_else_in_the_company_product(ledger, relative):
    """같은 디렉토리 안에서 공개는 `showcase.md` **하나**뿐이다.

    `para/projects/` 를 통째로 열지 않는 이유가 여기 있다 — 회사 제품 디렉토리는
    공개 자료와 내부 기록이 섞여 있어서 디렉토리 단위로는 가를 수 없다.
    """
    path = f"para/projects/company/mediness/{relative}"

    assert is_public_path("company_product", path) is False
    assert read_public_detail("company_product", path) is None


def test_company_root_itself_is_not_a_document(ledger):
    """제품 디렉토리 바로 아래가 아닌 자리(루트 자신·중간 디렉토리)는 문서가 아니다."""
    assert is_public_path("company_product", "para/projects/company/") is False
    assert is_public_path("company_product", "para/projects/company/mediness") is False


def test_reads_archived_company_product_showcase(ledger):
    """**전 회사 제품**도 같은 규칙으로 읽는다 — 채용담당자가 실제로 묻는 자리다(v0.0.8)."""
    body = read_public_detail(
        "company_product", "para/archive/company/linky/showcase.md"
    )

    assert body is not None
    assert "Linky" in body


@pytest.mark.parametrize("relative", ["README.md", "log/showcase.md"])
def test_rejects_everything_else_in_the_archived_product(ledger, relative):
    """archive 도 **showcase.md 한 파일만** — projects/company 와 같은 규칙이다."""
    path = f"para/archive/company/linky/{relative}"

    assert is_public_path("company_product", path) is False
    assert read_public_detail("company_product", path) is None


def test_project_and_product_roots_do_not_cross(ledger):
    """개인 프로젝트 tool 과 회사 제품 tool 은 **서로의 자리를 못 읽는다**.

    표가 갈리고(`project` · `product`) tool 이 갈리므로 루트도 갈린다 — 한쪽 행의
    `detail_path` 가 잘못 꽂혀도 다른 쪽 원장으로 넘어가지 않는다.
    """
    personal = "para/projects/summer-star/wine-log/showcase.md"
    company = "para/projects/company/mediness/showcase.md"
    archived = "para/archive/company/linky/showcase.md"

    assert is_public_path("project", company) is False
    assert is_public_path("project", archived) is False
    assert is_public_path("company_product", personal) is False


def test_company_rule_does_not_leak_to_other_types(ledger):
    """note·content·algorithm 은 회사 제품 자리를 못 읽는다 — 유형별 루트는 그대로다."""
    path = "para/projects/company/mediness/showcase.md"

    for doc_type in ("note", "content", "algorithm"):
        assert is_public_path(doc_type, path) is False


def test_rejects_traversal_escape(ledger):
    """문자열 prefix 검사만이면 통과하는 모양 — 실경로로 편 뒤 본다."""
    escape = "para/projects/summer-star/../company/mediness/spec.md"

    assert is_public_path("project", escape) is False
    assert read_public_detail("project", escape) is None


def test_traversal_out_of_every_root_is_rejected(ledger):
    """회사 자리를 발판 삼아 개인 지식으로 빠져나가지 못한다."""
    escape = "para/projects/company/mediness/../../../resources/persona/secret.md"

    assert is_public_path("company_product", escape) is False
    assert read_public_detail("company_product", escape) is None


def test_judgement_is_on_the_resolved_destination(ledger):
    """`..` 를 편 **결과**가 공개 자리면 통과한다 — 판정 대상은 문자열이 아니라 실경로다.

    회사 제품의 `log/` 를 거쳐 돌아와도 도착지가 showcase.md 면 그것은 공개 자료다.
    """
    detour = "para/projects/company/mediness/log/../showcase.md"

    assert is_public_path("company_product", detour) is True


def test_rejects_wrong_type_root(ledger):
    """유형마다 자기 루트만 읽는다 — note 가 project 의 자리를 읽지 않는다."""
    assert (
        is_public_path("note", "para/projects/summer-star/wine-log/showcase.md")
        is False
    )


def test_unknown_type_and_empty_path(ledger):
    assert is_public_path("career", "para/anything.md") is False   # career 는 md 가 없다
    assert is_public_path("project", None) is False
    assert read_public_detail("project", "") is None


def test_missing_file_is_none_not_error(ledger):
    """공개 루트 안이지만 파일이 없다 — 끊긴 detail_path 는 상세 없음이다."""
    assert (
        read_public_detail("project", "para/projects/summer-star/none/showcase.md")
        is None
    )

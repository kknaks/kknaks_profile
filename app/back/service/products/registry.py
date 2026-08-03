"""제품 등록·수정 오케스트레이션 (KDEV-WORK-018 P3 / KDEV-SPEC-014).

계층은 `40-architecture/system` 「백엔드 계층 규약」을 따른다 — DB 는 `repository/` 가
만지고, HTTP 는 알지 않으며(`ProductError` 를 올린다), 계층을 넘는 데이터는 DTO 다.

등록의 순서가 계약이다.

    검증(전량) → 파일 생성 → 커밋 1개 → 레지스트리 행 → 클론 예약

**검증이 맨 앞인 이유**는 실패했을 때 아무것도 만들어지지 않은 상태여야 하기 때문이고,
**커밋이 행보다 먼저인 이유**는 파일이 나가지 못했는데 행만 남는 상태를 피하기
위해서다. 반대 순서(행 먼저)면 커밋 실패 시 "추적은 하는데 제품 문서가 없는" 행이
남는다 — 그건 화면에서 `⚠ 제품 폴더 없음` 으로만 보여 원인을 알 수 없다.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

import config
import repository.tracked_repos as tracked_repos_repo
from service.apply import git as apply_git
from service.jobs.repo_registry import account_for
from service.products import scaffold, validate
from service.products.dto import RepoCreate, RepoPatch, TrackedRepoDTO
from service.products.errors import ProductError, ProductNotFound, ScaffoldError
from utils.slug import product_dir

logger = logging.getLogger("kknaks-back.products.registry")


async def list_rows(db: AsyncSession) -> list[TrackedRepoDTO]:
    """전체. **꺼진 것도 준다** — 안 보이면 다시 켤 방법이 없다."""
    return await tracked_repos_repo.list_all(db)


def product_exists(slug: str | None, repo_root: Path) -> bool:
    """`product_slug` 가 실재하는 디렉토리인가.

    **응답 시점에 판정하고 저장하지 않는다.** 저장하면 디렉토리를 지운 순간부터 값이
    거짓말을 한다(KDEV-DEC-017 D7).
    """
    return bool(slug) and (repo_root / product_dir(slug)).is_dir()


def card_visible(slug: str | None, repo_root: Path) -> bool | None:
    """공개 카드의 노출 값. **읽기만 한다** — 파일이 SoT 다(D14).

    카드가 없으면 `None` 이다. `False` 와 구분해야 화면이 "숨김" 과 "카드 없음" 을
    다르게 보여줄 수 있다.
    """
    if not slug:
        return None
    path = repo_root / product_dir(slug) / "showcase.md"
    if not path.exists():
        return None
    try:
        import frontmatter

        return bool(frontmatter.load(path).metadata.get("visible", True))
    except Exception:  # noqa: BLE001
        return None


async def register(
    db: AsyncSession,
    *,
    repo: str,
    kind: str,
    detail: str | None = None,
    product_slug: str | None = None,
    card: dict[str, Any] | None = None,
    repo_root: Path | None = None,
    dry_run: bool | None = None,
) -> TrackedRepoDTO:
    """제품/레포를 등록한다.

    `kind="company"` 면 **파일을 만들지 않는다**(KDEV-DEC-017 D9) — 회사 레포는 문서
    트리도 공개 카드도 없이 레지스트리에만 산다. 그래서 커밋도 없다.

    Raises:
        ProductError: 검증 실패. **아무것도 만들어지지 않았다.**
        ScaffoldError: 파일 생성이나 커밋 실패. 롤백 후 올라온다.
    """
    root = repo_root or config.repo_root()
    dry = config.job_git_push_dry_run() if dry_run is None else dry_run

    # --- 1. 검증 — 파일을 쓰기 전에 전부 --------------------------------------
    slug = validate.normalize_repo_slug(repo)
    validate.check_slug_available(slug, await tracked_repos_repo.existing_slugs(db))

    if kind not in ("company", "studio"):
        raise ProductError("INVALID_TYPE", "구분은 company 또는 studio 다", field="type")

    if kind == "company":
        validate.check_career(detail, root)
        product_slug = None  # 회사 레포는 제품 문서를 갖지 않는다
    else:
        detail = None  # studio 는 career 귀속이 없다 — DB CHECK 가 강제한다
        if not product_slug:
            raise ProductError(
                "INVALID_PRODUCT_SLUG", "제품 slug 가 필요하다", field="product_slug"
            )
        validate.check_product_slug_shape(product_slug)
        validate.check_product_dir_free(product_slug, root)
        if not card:
            raise ProductError("CARD_FIELD_MISSING", "카드 정보가 필요하다", field="card")
        validate.check_card(card, root)

    # --- 2. 파일 + 커밋 1개 (studio 만) ---------------------------------------
    if kind == "studio":
        _write_and_commit(product_slug, card or {}, root, dry_run=dry)

    # --- 3. 레지스트리 행 ------------------------------------------------------
    row = await tracked_repos_repo.create(
        db,
        RepoCreate(
            slug=slug,
            type=kind,
            detail=detail,
            product_slug=product_slug,
            account=account_for(slug),
        ),
    )
    logger.info("제품 등록 — %s (%s, product=%s)", slug, kind, product_slug)
    return row


def _write_and_commit(
    slug: str, card: dict[str, Any], root: Path, *, dry_run: bool
) -> None:
    """골격 + 카드 + 목록을 만들고 **한 커밋**으로 낸다.

    나눠 커밋하면 중간 커밋에 검증 실패 상태가 origin 에 남는다(DEC-012 D3 과 같은
    이유). 실패하면 `publish_atomic` 이 되돌린다 — `commit_and_push_with_retry` 를
    쓰지 않는 이유가 그 함수에 롤백이 없어서다.
    """
    before = apply_git.head_ref(root)
    try:
        paths = scaffold.write_scaffold(slug, root)
        card_path, content = scaffold.render_card(slug=slug, card=card, repo_root=root)
        (root / card_path).write_text(content, encoding="utf-8")
        paths.append(card_path)

        index_path = scaffold.append_product_index(slug, root)
        if index_path:
            paths.append(index_path)
    except ScaffoldError:
        apply_git.rollback(root, before)
        raise
    except Exception as exc:  # noqa: BLE001
        apply_git.rollback(root, before)
        raise ScaffoldError("WRITE_FAILED", f"파일 생성에 실패했다 — {exc}") from exc

    outcome = apply_git.publish_atomic(
        paths, f"feat(products): {slug} 제품 등록", repo_root=root, dry_run=dry_run
    )
    if not outcome.ok:
        # `publish_atomic` 이 이미 되돌렸다. 여기서 또 하지 않는다.
        raise ScaffoldError(
            outcome.error_code or "GIT_FAILED",
            outcome.error_message or "커밋·푸시에 실패했다",
        )


async def update(
    db: AsyncSession,
    repo_id: int,
    *,
    detail: str | None = None,
    product_slug: str | None = None,
    enabled: bool | None = None,
    fields_set: set[str],
    repo_root: Path | None = None,
) -> TrackedRepoDTO:
    """행 수정. **파일을 옮기지 않는다** — 연결만 바뀐다.

    `fields_set` 은 요청이 실제로 보낸 필드다. 이것이 없으면 `detail` 을 안 보낸
    요청과 `detail=null` 을 보낸 요청이 같아져 **company 행의 career 귀속이 조용히
    지워진다.**
    """
    root = repo_root or config.repo_root()
    row = await tracked_repos_repo.get_by_id(db, repo_id)
    if row is None:
        raise ProductNotFound(f"레지스트리 행이 없다 — id={repo_id}")

    if "detail" in fields_set and detail:
        validate.check_career(detail, root)
    if "product_slug" in fields_set and product_slug:
        validate.check_product_slug_shape(product_slug)

    patch = RepoPatch()
    if "detail" in fields_set:
        patch = patch.model_copy(update={"detail": detail})
        patch.model_fields_set.add("detail")
    if "product_slug" in fields_set:
        patch = patch.model_copy(update={"product_slug": product_slug})
        patch.model_fields_set.add("product_slug")
    if "enabled" in fields_set and enabled is not None:
        patch = patch.model_copy(update={"enabled": enabled})
        patch.model_fields_set.add("enabled")

    updated = await tracked_repos_repo.patch(db, repo_id, patch)
    if updated is None:
        raise ProductNotFound(f"레지스트리 행이 없다 — id={repo_id}")
    return updated


async def resync(
    db: AsyncSession, repo_id: int, *, root: Path | None = None
) -> TrackedRepoDTO:
    """수동 재동기화. 클론이 없으면 받고, 있으면 fetch 한다.

    결과를 예외로 올리지 않는다 — 실패도 행에 남는 정상적인 상태이고, 화면이 사유
    코드와 재시도 버튼을 보여준다(SPEC-014 §4 State).
    """
    row = await tracked_repos_repo.get_by_id(db, repo_id)
    if row is None:
        raise ProductNotFound(f"레지스트리 행이 없다 — id={repo_id}")

    result = await _sync_one(row, root=root)
    now = datetime.now(timezone.utc)
    if result.ok:
        await tracked_repos_repo.mark_synced(db, repo_id, now)
    else:
        await tracked_repos_repo.mark_failed(
            db, repo_id, result.code or "FETCH_FAILED", result.message
        )
    refreshed = await tracked_repos_repo.get_by_id(db, repo_id)
    assert refreshed is not None  # 방금 읽은 행이다
    return refreshed


async def _sync_one(row: TrackedRepoDTO, *, root: Path | None):
    import asyncio

    from service.jobs import repos as repo_sync

    return await asyncio.to_thread(repo_sync.sync_repo, row.slug, row.account, root=root)

"""잔디 수집기 — 케이스 6·7. GitHub REST 로 커밋을 긁어 commit 표에 쌓는다.

승인 게이트 없음 · md 안 씀 — 읽는 곳은 GitHub, 쓰는 곳은 DB 뿐(케이스 6
「잔디는 자동이어도 된다」). summary 는 우선 커밋 메시지 첫 줄 — 수집 완료 뒤
summarize_service 가 연쇄되어 최근 7일 창을 AI 한 줄로 덮는다.

잔디는 「내가 한 일」이다 — **내 커밋만 담는다**(케이스 6). 신원 집합은
git_token 표의 (account, email) 전부(enabled 무관 — 신원은 신원이다)를 수집
시작 때 한 번 읽고, GitHub item 의 author.login 이나 commit.author.email 이
집합에 있어야(대소문자 무시) 통과한다. 회사 레포의 팀원 커밋은 여기서 걸린다.

기본 브랜치만 보지 않는다 — **브랜치 전부**를 훑는다: /branches 로 목록을 받아
브랜치마다 /commits?sha= 로 긁는다. 브랜치 간 중복은 tree 로 한 실행 안에서
걸러 넣고, DB 의 (repo_id, tree) UNIQUE + insert_ignore 가 실행 간 중복을 막는다.

요청 밖(백그라운드·스케줄)에서 돌아서 get_db 를 못 쓴다 — 세션을 직접 연다.
트랜잭션 경계는 **레포 하나**다: 한 레포가 실패해도 나머지는 계속 가고,
실패는 그 레포의 last_error 에 남는다(성공하면 비운다).

증분 기준은 repo.last_fetched_at 재사용(발주 확정 — 잡 상태 표를 안 만든다).
첫 수집(NULL)은 전체 이력 소급, 이후는 since=last_fetched_at — 브랜치별로
같은 since 를 쓴다.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta, timezone
from typing import Any
from zoneinfo import ZoneInfo

import httpx

from core.crypto import decrypt_token
from core.db import SessionLocal
from dto.repo import RepoDTO
from repository.commit_repo import CommitRepository
from repository.git_token_repo import GitTokenRepository
from repository.repo_repo import RepoRepository

logger = logging.getLogger(__name__)

_API = "https://api.github.com"
_PER_PAGE = 100
_MAX_PAGES = 100          # 폭주 방지 — **브랜치당** 100 * 100 = 커밋 1만이면 충분하다
_MAX_BRANCHES = 100       # 브랜치가 아주 많은 레포 대비 상한 — 초과분은 로그만 남기고 버린다
_KST = ZoneInfo("Asia/Seoul")
_SCHEDULE_HOUR = 8        # 매일 KST 08:00


def _summary(message: str | None) -> str | None:
    """커밋 메시지 첫 줄 — 잔디에 뜨는 한 줄(확정 — AI 요약은 나중에 교체)."""
    if not message:
        return None
    return message.splitlines()[0].strip() or None


def _is_mine(
    item: dict[str, Any], accounts: frozenset[str], emails: frozenset[str]
) -> bool:
    """내 커밋 판정 — author.login ∈ accounts 이거나 commit.author.email ∈ emails.

    집합은 전부 소문자 — 비교도 소문자로(대소문자 무시). 집합이 비어 있으면
    (토큰 미등록) 아무것도 통과하지 못한다.
    """
    login = ((item.get("author") or {}).get("login") or "").lower()
    if login and login in accounts:
        return True
    email = (((item.get("commit") or {}).get("author") or {}).get("email") or "").lower()
    return bool(email) and email in emails


class CollectService:
    def __init__(
        self,
        repo_repo: RepoRepository,
        commit_repo: CommitRepository,
        git_token_repo: GitTokenRepository,
    ) -> None:
        self._repo_repo = repo_repo
        self._commit_repo = commit_repo
        self._git_token_repo = git_token_repo
        self._running = False

    # ── 트리거 ──────────────────────────────────────────────────────────
    def start(self) -> bool:
        """백그라운드로 전체 수집을 건다. 이미 돌고 있으면 안 겹치고 False."""
        if self._running:
            return False
        asyncio.get_running_loop().create_task(self.collect_all())
        return True

    async def collect_all(self) -> dict[str, int]:
        """enabled 레포 전부 수집. 레포별 격리 — 반환은 {slug: 넣은 커밋 수}."""
        if self._running:
            logger.info("collect: already running — skip")
            return {}
        self._running = True
        try:
            async with SessionLocal() as session:
                repos = await self._repo_repo.list_enabled(session)
            results: dict[str, int] = {}
            headers = {
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            }
            # 토큰은 레포에 연결된 git_token 행 — DB 의 암호문을 복호해 쓴다.
            # 연결 없으면 무토큰(공개 레포만 읽힌다). 복호 실패는 그 레포만 실패로.
            # **비활성(enabled=false) 토큰도 무토큰 취급** — cipher_map 이 활성 행만
            # 담으므로 아래 ciphers.get() 이 None 을 주고, 레포는 계속 수집하되
            # 공개 범위만 읽힌다.
            async with SessionLocal() as session:
                ciphers = await self._git_token_repo.cipher_map(session)
                # 신원 집합 — git_token 의 (account, email) 전부. enabled 무관:
                # 토큰이 꺼져도 신원은 신원이다. 수집 시작 때 한 번 읽는다.
                tokens = await self._git_token_repo.list_all(session)
            accounts = frozenset(t.account.lower() for t in tokens if t.account)
            emails = frozenset(t.email.lower() for t in tokens if t.email)
            if not accounts and not emails:
                logger.warning(
                    "collect: git_token 미등록 — 신원 집합이 비어 모든 커밋이 걸러진다"
                )
            async with httpx.AsyncClient(headers=headers, timeout=30.0) as client:
                for repo in repos:
                    try:
                        token = None
                        if repo.git_token_id is not None:
                            cipher = ciphers.get(repo.git_token_id)
                            token = decrypt_token(cipher) if cipher else None
                        results[repo.slug] = await self._collect_one(
                            client, repo, token, accounts, emails
                        )
                    except Exception as exc:  # 레포 하나가 죽어도 나머지는 계속
                        logger.exception("collect: %s failed", repo.slug)
                        await self._mark_error(repo.id, str(exc)[:1000])
            logger.info("collect: done — %s", results)
            # 수집 뒤 AI 요약 연쇄 — 최근 7일 창의 미요약 날짜만(케이스 6 —
            # 잔디는 자동이어도 된다). 스케줄·수동 「지금 수집」 공통 경로다.
            # 요약이 죽어도 수집 결과는 그대로 — 실패는 daily.error 몫이다.
            try:
                from service.summarize_service import summarize_service

                await summarize_service.summarize_recent()
            except Exception:
                logger.exception("collect: summarize_recent failed")
            return results
        finally:
            self._running = False

    # ── 레포 하나 ───────────────────────────────────────────────────────
    async def _collect_one(
        self,
        client: httpx.AsyncClient,
        repo: RepoDTO,
        token: str | None,
        accounts: frozenset[str],
        emails: frozenset[str],
    ) -> int:
        # 새 last_fetched_at 은 수집 시작 시각 — 도는 동안 푸시된 것을 다음 판이 줍는다.
        started = datetime.now(timezone.utc)
        auth = {"Authorization": f"Bearer {token}"} if token else {}
        branches = await self._fetch_branches(client, repo, auth)
        # 브랜치 간 중복은 tree 로 한 실행 안에서 걸러 insert 양을 줄인다.
        # DB 의 (repo_id, tree) UNIQUE + insert_ignore 가 실행 간 중복을 막는다.
        rows_by_tree: dict[str, dict[str, Any]] = {}
        for branch in branches:
            for row in await self._fetch_commits(
                client, repo, auth, branch, accounts, emails
            ):
                rows_by_tree.setdefault(row["tree"], row)
        rows = list(rows_by_tree.values())
        async with SessionLocal() as session:
            inserted = await self._commit_repo.insert_ignore(session, rows)
            await self._repo_repo.update(
                session,
                repo.id,
                {"last_fetched_at": started, "last_error": None},
            )
            await session.commit()
        logger.info(
            "collect: %s — %d branches, fetched %d (mine, deduped), inserted %d",
            repo.slug,
            len(branches),
            len(rows),
            inserted,
        )
        return inserted

    async def _fetch_branches(
        self, client: httpx.AsyncClient, repo: RepoDTO, auth: dict[str, str]
    ) -> list[str]:
        """GET /repos/{slug}/branches — pagination. 상한 _MAX_BRANCHES, 초과는 로그."""
        names: list[str] = []
        for page in range(1, (_MAX_BRANCHES // _PER_PAGE) + 2):
            res = await client.get(
                f"{_API}/repos/{repo.slug}/branches",
                params={"per_page": _PER_PAGE, "page": page},
                headers=auth,
            )
            if res.status_code == 409:
                return []  # 빈 레포 — 브랜치 0 이 정상이다
            if res.status_code != 200:
                detail = ""
                try:
                    detail = res.json().get("message", "")
                except Exception:
                    pass
                raise RuntimeError(f"GitHub {res.status_code} — {detail or res.text[:200]}")
            batch = res.json()
            names.extend(b["name"] for b in batch if b.get("name"))
            if len(batch) < _PER_PAGE:
                break
            if len(names) >= _MAX_BRANCHES:
                logger.warning(
                    "collect: %s — 브랜치 %d개 이상, 상한 %d개까지만 훑는다",
                    repo.slug,
                    len(names),
                    _MAX_BRANCHES,
                )
                break
        return names[:_MAX_BRANCHES]

    async def _fetch_commits(
        self,
        client: httpx.AsyncClient,
        repo: RepoDTO,
        auth: dict[str, str],
        branch: str,
        accounts: frozenset[str],
        emails: frozenset[str],
    ) -> list[dict[str, Any]]:
        """GET /repos/{slug}/commits?sha={branch} — pagination. 증분은 since=last_fetched_at.

        내 커밋만 남긴다(_is_mine) — 잔디는 「내가 한 일」이다(케이스 6).
        """
        params: dict[str, Any] = {"per_page": _PER_PAGE, "sha": branch}
        if repo.last_fetched_at is not None:
            params["since"] = repo.last_fetched_at.astimezone(timezone.utc).isoformat()
        rows: list[dict[str, Any]] = []
        for page in range(1, _MAX_PAGES + 1):
            res = await client.get(
                f"{_API}/repos/{repo.slug}/commits",
                params={**params, "page": page},
                headers=auth,
            )
            if res.status_code == 409:
                break  # 빈 레포 — 커밋 0 이 정상이다
            if res.status_code != 200:
                detail = ""
                try:
                    detail = res.json().get("message", "")
                except Exception:
                    pass
                raise RuntimeError(f"GitHub {res.status_code} — {detail or res.text[:200]}")
            batch = res.json()
            for item in batch:
                if not _is_mine(item, accounts, emails):
                    continue  # 남의 커밋 — 잔디에 안 담는다
                commit = item.get("commit") or {}
                author = commit.get("author") or {}
                authored_at = author.get("date")
                if not authored_at:
                    continue  # author 날짜 없는 커밋은 잔디에 놓을 자리가 없다
                message = commit.get("message")
                rows.append(
                    {
                        "repo_id": repo.id,
                        "sha": item["sha"],
                        "tree": (commit.get("tree") or {}).get("sha") or item["sha"],
                        "author": author.get("name"),
                        "authored_at": datetime.fromisoformat(
                            authored_at.replace("Z", "+00:00")
                        ),
                        "message": message,
                        "summary": _summary(message),
                    }
                )
            if len(batch) < _PER_PAGE:
                break
        return rows

    async def _mark_error(self, repo_id: int, error: str) -> None:
        async with SessionLocal() as session:
            await self._repo_repo.update(session, repo_id, {"last_error": error})
            await session.commit()

    # ── 스케줄 — 매일 KST 08:00 ─────────────────────────────────────────
    async def run_scheduler(self) -> None:
        """가벼운 asyncio 루프 — 프레임워크 없이 다음 08:00 까지 자고 돈다."""
        while True:
            now = datetime.now(_KST)
            next_run = now.replace(
                hour=_SCHEDULE_HOUR, minute=0, second=0, microsecond=0
            )
            if next_run <= now:
                next_run += timedelta(days=1)
            wait = (next_run - now).total_seconds()
            logger.info("collect scheduler: next run %s (in %.0fs)", next_run, wait)
            await asyncio.sleep(wait)
            try:
                await self.collect_all()
            except Exception:  # 스케줄 루프는 죽지 않는다
                logger.exception("collect scheduler: run failed")


collect_service = CollectService(
    RepoRepository(), CommitRepository(), GitTokenRepository()
)

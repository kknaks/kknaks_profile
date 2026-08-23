"""진짜 `collect` 스테이지 — 레지스트리·클론·git 조사를 하나로 묶는다.

KDEV-WORK-017 P5 / KDEV-SPEC-011 S-1.

**더미와 계약이 같다.** `investigate_payload` 가 내던 키를 하나도 더하거나 빼지 않으므로
하류(`investigate`·`daily` 게이트·발행부)는 한 줄도 바뀌지 않는다 — P2 가 더미 경계를
그렇게 그어 둔 값을 여기서 받는다.

`DummyCollect` 를 지우지 않는다. 시나리오 일곱(일부 실패·전부 실패·상한 적중·활동 0…)은
진짜 git 으로 재현하기 어렵고, 한 바퀴 테스트가 그 분기들을 타고 있다.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

import config
from core.models import QueueItem
from service.jobs import repo_registry, repos
from service.jobs.collect_commits import collect_repo, identities
from service.jobs.inputs import read_changed_files_today
from service.notify import notify_slack

from .collect_common import (
    context_attribution,
    decompose,
    has_activity,
    rules_for,
    target_date,
)
from .prepare import StageSubmission

logger = logging.getLogger("kknaks-back.pipeline.collect-git")


def career_attribution(
    commits: list[dict[str, Any]], detail_by_repo: dict[str, str]
) -> dict[str, list[str]]:
    """`type=company` 인 레포의 커밋만 career 로 귀속된다 (SPEC-012).

    `studio` 는 career 를 만들지 않는다 — 다닌 적 없는 조직을 이력에 넣지 않는다.
    더미와 같은 규칙이고, 다른 것은 대응표의 출처뿐이다(코드 상수 → 레지스트리).
    """
    mapping: dict[str, list[str]] = {}
    for commit in commits:
        detail = detail_by_repo.get(str(commit.get("repo") or ""))
        if not detail:
            continue
        repos_for = mapping.setdefault(detail, [])
        if commit["repo"] not in repos_for:
            repos_for.append(commit["repo"])
    return mapping


def drift(found: dict[str, list[str]]) -> list[str]:
    """등록되지 않은 identity (SPEC-011 S-2). 조사는 멈추지 않는다."""
    known = config.known_commit_identities()
    return sorted({i for ids in found.values() for i in ids} - known)


class GitCollect:
    """`collect` auto 스테이지 — **LLM 을 부르지 않는다.**

    제출 건수가 0이라 `AITask` 가 생기지 않는다. 조사는 git 을 읽는 일이지 생성이
    아니므로 실행기 큐에 넣을 대상이 아니다. 더미에서 물려받은 성질 그대로다.

    DB 세션을 **팩토리로** 받는다. 스테이지 인터페이스에 세션이 없고(`submit(item,
    prior)`), 여기서 여는 세션은 요청/드라이버의 트랜잭션과 생명주기가 달라야 한다 —
    fetch 13회가 도는 동안 남의 트랜잭션을 붙잡고 있으면 안 된다.
    """

    stages = ("collect",)
    #: **이 실행기가 어느 파이프라인의 것인가** — 진짜 git 조사 — 잔디 전용이다.
    #: 스테이지 이름만 보면 유튜브·블로그의 `collect` 가 여기로 샌다
    #: (실제로 샜다 — 유튜브 항목이 커밋 33건을 수집했다).
    source_kinds = ("daily_commit",)

    def __init__(self, *, session_factory, repo_root: Path | None = None) -> None:
        self.session_factory = session_factory
        self.repo_root = repo_root or config.repo_root()

    async def submit(self, *, item: QueueItem, prior: dict[str, Any]) -> StageSubmission:
        target = target_date(item.normalized_url)
        payload = await self._investigate(target)

        if not has_activity(payload):
            return StageSubmission(
                [],
                {"collect": payload},
                error_code="NO_ACTIVITY",
                error_message=f"{payload['date']} 활동이 없다 — 만들 것이 없다",
            )
        return StageSubmission([], {"collect": payload})

    async def _investigate(self, target: date) -> dict[str, Any]:
        async with self.session_factory() as db:
            rows = await repo_registry.enabled_repos(db)
            sync = await repos.sync_all(db, rows)
            # 레지스트리 값을 **세션 밖으로 들고 나온다.** 아래 git 작업은 오래 걸리고
            # 그동안 세션을 열어 둘 이유가 없다.
            plan = [
                {
                    "slug": r.slug,
                    "detail": r.detail if r.type == "company" else None,
                    # `## 진행 중` 귀속에 쓴다 (KDEV-DEC-022 D1). `detail` 과 달리
                    # `type` 에 묶지 않는다 — 회사 레포도 제품 문서를 가질 수 있다.
                    "type": r.type,
                    "product_slug": r.product_slug,
                    "rules": rules_for(r.path_rules),
                }
                for r in rows
            ]
            await db.commit()

        ok = {r.slug for r in sync if r.ok}
        failures = [
            {"repo": r.slug, "code": r.code or "FETCH_FAILED", "message": r.message}
            for r in sync
            if not r.ok
        ]

        commits: list[dict[str, Any]] = []
        truncated: dict[str, dict[str, int]] = {}
        found_identities: dict[str, list[str]] = {}
        rules_by_repo = {p["slug"]: p["rules"] for p in plan}

        for entry in plan:
            slug = entry["slug"]
            if slug not in ok:
                continue  # 클론이 실패한 레포는 읽을 것이 없다. 실패는 이미 기록됐다.
            path = repos.clone_dir(slug)
            got, hit = await asyncio.to_thread(
                collect_repo, path, slug, target, rules=entry["rules"]
            )
            commits.extend(got)
            if hit:
                truncated[slug] = hit
            found = await asyncio.to_thread(identities, path, target)
            if found:
                found_identities[slug] = found

        await self._notify_drift(found_identities)

        detail_by_repo = {p["slug"]: p["detail"] for p in plan if p["detail"]}
        meta_by_repo = {
            p["slug"]: {"type": p["type"], "product_slug": p["product_slug"]} for p in plan
        }
        notes, study = self._counts_from_repo(target)
        return {
            "date": target.isoformat(),
            "commits": commits,
            "areas": decompose(commits, rules_by_repo),
            "career_map": career_attribution(commits, detail_by_repo),
            "context_map": context_attribution(commits, meta_by_repo),
            "counts": {
                # **코드가 센다.** AI 출력의 숫자를 쓰지 않는다(SPEC-012 §5).
                "commit": len(commits),
                "note": notes,
                "study": study,
            },
            "truncated": truncated,
            "failures": failures,
            "identities": found_identities,
        }

    def _counts_from_repo(self, target: date) -> tuple[int, int]:
        """노트·교안 변경 수. **커밋만 활동이 아니다**(SPEC-011 S-5 3항).

        프로필 레포 자신의 작업트리에서 읽는다 — 그날 `resources/source/` 와
        `persona/contents/` 에 무엇이 바뀌었는지는 여기 있고, bare 클론에는 없다.
        """
        notes = read_changed_files_today("resources/source/", target, self.repo_root)
        contents = read_changed_files_today("persona/contents/", target, self.repo_root)
        return len(notes), len(contents)

    async def _notify_drift(self, found: dict[str, list[str]]) -> None:
        """U-2 — 미등록 identity. **조사는 계속한다.**

        그 커밋들은 이미 패턴에 걸려 결과에 들어 있다. 알림은 "등록하거나 패턴을
        좁혀라" 는 요청이지 실패 통지가 아니다.
        """
        unknown = drift(found)
        if not unknown:
            return
        where = {
            i: sorted(s for s, ids in found.items() if i in ids) for i in unknown
        }
        lines = [f":mag: 새 커밋 identity 발견 — {len(unknown)}종"]
        lines += [f"• `{i}` ({', '.join(where[i])})" for i in unknown]
        lines.append("등록하거나 패턴을 좁혀야 한다.")
        await notify_slack("\n".join(lines))

    async def wait(self, task_ref: str) -> None:  # pragma: no cover - 제출이 0건이다
        return None

    async def poll(self, task_ref: str):  # pragma: no cover - 제출이 0건이다
        raise RuntimeError("collect 는 실행기를 쓰지 않는다")

    def parse(
        self, results: dict[str, str], *, item: QueueItem, prior: dict[str, Any]
    ) -> dict[str, Any]:
        # 산출물은 이미 `submit` 이 확정했다. 여기서 더할 것이 없다.
        return {}

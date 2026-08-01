"""더미 커밋 조사 — 레일을 태우기 위한 가짜 입력 (KDEV-WORK-017 P2 / KDEV-SPEC-011).

**지어내는 것은 커밋뿐이다.** 영역 분해·`counts` 산출·`career_map` 귀속은 진짜 코드이고
P5 가 그대로 물려받는다. 갈아 끼울 자리는 "git 을 읽어 `commits[]` 를 만드는" 한 곳이다.

그 경계를 지키는 이유가 이 모듈의 존재 이유다. 더미가 SPEC-011 §4 조사 산출물 계약을
**통째로** 내기 때문에 하류(`investigate`·`compose`·발행)는 진짜인지 가짜인지 구분하지
못한다. 계약을 줄이면 그 보장이 깨지고 P5 교체가 여러 곳으로 번진다.

시나리오를 고를 수 있는 것도 목적이다. 한 바퀴의 값어치는 정상 경로가 아니라 **일부 실패·
전부 실패·상한 적중·활동 0** 에서 나온다 — 그 분기들이 게이트 화면과 발행부까지 이어진다.
"""

from __future__ import annotations

import fnmatch
import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from typing import Any

from core.models import QueueItem

from .prepare import StageSubmission

KST = timezone(timedelta(hours=9))

#: 전역 기본 영역 규칙 (SPEC-011 「기술 영역 분해」). 레포별 예외는 P5 의 `path_rules`.
#: 순서가 의미를 갖는다 — 먼저 맞는 규칙이 이긴다.
AREA_RULES: tuple[tuple[str, str], ...] = (
    ("app/back/*", "backend"),
    ("*/backend/*", "backend"),
    ("app/front/*", "frontend"),
    ("*/frontend/*", "frontend"),
    ("products/*", "docs"),
    ("docs/*", "docs"),
    ("*.md", "docs"),
    ("*.yml", "infra"),
    ("*.yaml", "infra"),
    ("Dockerfile*", "infra"),
)

#: 추적 대상 — P5 에서 `tracked_repos` 테이블로 옮긴다. 지금 테이블을 만들면
#: P5 전에 되돌릴 것이 생기므로 코드 안에 둔다(WORK-017 P2 더미 경계).
#: `detail` 은 career 파일 stem 이고 **실재해야 한다** — `is_current: true` 는
#: `medisolve-ai` 하나뿐이라 company 귀속은 전부 그리로 간다.
TRACKED = (
    ("MediSolveAIDev/mediness", "company", "medisolve-ai"),
    ("MediSolveAIDev/Linky", "company", "medisolve-ai"),
    ("kknaks/kknaks_profile", "studio", None),
    ("kknaks/open_kknaks", "studio", None),
)


def area_for(path: str) -> str:
    """파일 경로 → 기술 영역. 어디에도 안 걸리면 `other`."""
    for pattern, area in AREA_RULES:
        if fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(path, f"*/{pattern}"):
            return area
    return "other"


def decompose(commits: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    """커밋들 → 영역별 집계.

    **한 커밋이 여러 영역에 걸치면 영역마다 계상한다**(SPEC-011). 그래서
    `counts["commit"]` 과 영역별 `commits` 합계는 일치하지 않는다 — 영역별 활동을
    보려는 값이지 커밋을 세려는 값이 아니다.
    """
    areas: dict[str, dict[str, int]] = {}
    for commit in commits:
        seen: set[str] = set()
        for f in commit.get("files") or []:
            area = area_for(str(f.get("path") or ""))
            bucket = areas.setdefault(area, {"commits": 0, "added": 0, "deleted": 0})
            bucket["added"] += int(f.get("added") or 0)
            bucket["deleted"] += int(f.get("deleted") or 0)
            if area not in seen:
                bucket["commits"] += 1
                seen.add(area)
    return areas


def career_attribution(commits: list[dict[str, Any]]) -> dict[str, list[str]]:
    """`type=company` 인 레포의 커밋만 career 로 귀속된다 (SPEC-012).

    `studio` 는 career 를 만들지 않는다 — 다닌 적 없는 조직을 이력에 넣지 않는다.
    """
    detail_by_repo = {slug: detail for slug, kind, detail in TRACKED if kind == "company"}
    mapping: dict[str, list[str]] = {}
    for commit in commits:
        detail = detail_by_repo.get(str(commit.get("repo") or ""))
        if not detail:
            continue
        repos = mapping.setdefault(detail, [])
        if commit["repo"] not in repos:
            repos.append(commit["repo"])
    return mapping


def _commit(repo: str, sha: str, message: str, files: list[tuple[str, int, int]]) -> dict:
    entries = [{"path": p, "added": a, "deleted": d} for p, a, d in files]
    return {
        "repo": repo,
        "sha": sha,
        # tree 해시는 중복 제거 키다(SPEC-011). 더미도 자리를 비우지 않는다 —
        # 하류가 계약을 온전히 받아야 P5 교체가 여기 한 곳으로 끝난다.
        "tree": f"tree-{sha}",
        "message": message,
        "files": entries,
        "areas": sorted({area_for(p) for p, _, _ in files}),
    }


# --- 시나리오 -----------------------------------------------------------------


@dataclass(frozen=True)
class Scenario:
    commits: list[dict[str, Any]]
    notes: int = 0
    study: int = 0
    truncated: dict[str, dict[str, int]] | None = None
    failures: list[dict[str, str]] | None = None


def _normal() -> Scenario:
    return Scenario(
        commits=[
            _commit(
                "MediSolveAIDev/mediness",
                "a1b2c3d",
                "차트 요약 API 응답 스키마 정리",
                [("app/back/api/charts.py", 84, 21), ("app/back/tests/test_charts.py", 40, 0)],
            ),
            _commit(
                "MediSolveAIDev/Linky",
                "e4f5a6b",
                "예약 알림 재시도 백오프 도입",
                [("app/back/service/notify.py", 33, 8), ("docker-compose.yml", 4, 1)],
            ),
            _commit(
                "kknaks/kknaks_profile",
                "c7d8e9f",
                "잔디 파이프라인 레일 일반화",
                [
                    ("app/back/service/pipeline/prepare.py", 120, 6),
                    ("products/kknaks-dev/30-work/work-017.md", 30, 12),
                ],
            ),
        ],
        notes=1,
        study=1,
    )


def _studio_only() -> Scenario:
    return Scenario(
        commits=[
            _commit(
                "kknaks/open_kknaks",
                "b1c2d3e",
                "브로커 재연결 백오프",
                [("app/back/broker.py", 45, 12)],
            )
        ],
        notes=1,
    )


def _career_unchanged() -> Scenario:
    """company 커밋이 있지만 문서 손질뿐 — `compose` 가 `changed:false` 로 돌아갈 재료."""
    return Scenario(
        commits=[
            _commit(
                "MediSolveAIDev/mediness",
                "f0e1d2c",
                "오탈자 수정",
                [("README.md", 2, 2)],
            )
        ]
    )


def _partial_failure() -> Scenario:
    scenario = _normal()
    return Scenario(
        commits=scenario.commits,
        notes=scenario.notes,
        study=scenario.study,
        failures=[
            {
                "repo": "MediSolveAIDev/NEXUS",
                "code": "FETCH_FAILED",
                "message": "remote hung up unexpectedly",
            }
        ],
    )


def _all_failed() -> Scenario:
    return Scenario(
        commits=[],
        notes=1,
        failures=[
            {"repo": slug, "code": "FETCH_FAILED", "message": "network unreachable"}
            for slug, _, _ in TRACKED
        ],
    )


def _truncated() -> Scenario:
    scenario = _normal()
    return Scenario(
        commits=scenario.commits,
        notes=scenario.notes,
        study=scenario.study,
        truncated={"MediSolveAIDev/mediness": {"diff_bytes": 32768, "commits": 30}},
    )


def _empty() -> Scenario:
    return Scenario(commits=[])


SCENARIOS = {
    "normal": _normal,
    "studio_only": _studio_only,
    "career_unchanged": _career_unchanged,
    "partial_failure": _partial_failure,
    "all_failed": _all_failed,
    "truncated": _truncated,
    "empty": _empty,
}

_SCENARIO_RE = re.compile(r"scenario:([a-z_]+)")
_DATE_RE = re.compile(r"daily:(\d{4}-\d{2}-\d{2})")


def target_date(item: QueueItem) -> str:
    """조사 대상 날짜. 합성 키(`daily:{date}`)가 있으면 거기서, 없으면 어제(KST).

    합성 키를 심는 접수부는 아직 P2 의 뒤쪽 작업이라, 그때까지는 어제로 떨어진다.
    """
    match = _DATE_RE.search(item.normalized_url or "")
    if match:
        return match.group(1)
    return (datetime.now(KST).date() - timedelta(days=1)).isoformat()


def pick_scenario(item: QueueItem) -> str:
    """메모에 `scenario:<이름>` 이 있으면 그것, 없으면 `normal`.

    수동 접수(`POST /api/admin/queue/items`)로 분기를 하나씩 태워 보기 위한 손잡이다 —
    P2 에는 스케줄러가 없으므로 접수가 곧 사람의 조작이다.
    """
    match = _SCENARIO_RE.search(item.note or "")
    name = match.group(1) if match else "normal"
    return name if name in SCENARIOS else "normal"


def investigate_payload(item: QueueItem) -> dict[str, Any]:
    """SPEC-011 §4 조사 산출물 — 키를 하나도 빠뜨리지 않는다."""
    scenario = SCENARIOS[pick_scenario(item)]()
    commits = scenario.commits
    return {
        "date": target_date(item),
        "commits": commits,
        "areas": decompose(commits),
        "career_map": career_attribution(commits),
        "counts": {
            # **코드가 센다.** AI 출력의 숫자를 쓰지 않는다(SPEC-012 §5).
            "commit": len(commits),
            "note": scenario.notes,
            "study": scenario.study,
        },
        "truncated": scenario.truncated or {},
        "failures": scenario.failures or [],
        "identities": {
            slug: ["kknaksss <kknaks@medisolveai.com>"] for slug, _, _ in TRACKED
        },
    }


def has_activity(payload: dict[str, Any]) -> bool:
    """활동 0이면 이후 단계를 부르지 않는다 (SPEC-011 §5).

    커밋만 보지 않는다 — 노트·교안 변경도 활동이다. 전 레포 조사가 실패해도 그 둘이
    있으면 커밋 없이 진행한다(S-5).
    """
    counts = payload.get("counts") or {}
    return any(int(counts.get(k) or 0) > 0 for k in ("commit", "note", "study"))


class DummyCollect:
    """`collect` auto 스테이지 — **LLM 을 부르지 않는다.**

    제출 건수가 0이라 `AITask` 가 생기지 않는다. 조사는 git 을 읽는 일이지 생성이
    아니므로, 실행기 큐에 넣을 대상이 아니다. P5 에서 진짜 git 조사로 바뀌어도
    이 성질은 그대로다.
    """

    stages = ("collect",)

    async def submit(self, *, item: QueueItem, prior: dict[str, Any]) -> StageSubmission:
        payload = investigate_payload(item)
        if not has_activity(payload):
            return StageSubmission(
                [],
                {"collect": payload},
                error_code="NO_ACTIVITY",
                error_message=f"{payload['date']} 활동이 없다 — 만들 것이 없다",
            )
        return StageSubmission([], {"collect": payload})

    async def wait(self, task_ref: str) -> None:  # pragma: no cover - 제출이 0건이다
        return None

    async def poll(self, task_ref: str):  # pragma: no cover - 제출이 0건이다
        raise RuntimeError("collect 는 실행기를 쓰지 않는다")

    def parse(
        self, results: dict[str, str], *, item: QueueItem, prior: dict[str, Any]
    ) -> dict[str, Any]:
        # 산출물은 이미 `submit` 이 확정했다. 여기서 더할 것이 없다.
        return {}

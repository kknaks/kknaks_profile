"""조사 산출물의 **계산** 부분 — 더미와 진짜가 함께 쓴다 (KDEV-SPEC-011 §4).

P2 는 이 함수들을 `collect_dummy` 안에 두고 "지어내는 것은 커밋뿐이고 영역 분해·
`counts` 산출은 진짜 코드다" 라고 적었다. P5 에서 진짜 수집이 들어오면서 **그 말이
문자 그대로 성립하도록** 여기로 옮긴다 — 더미와 진짜가 같은 함수를 부르지 않으면
"하류는 진짜인지 가짜인지 구분하지 못한다" 는 보장이 말뿐인 것이 된다.

여기 있는 것은 전부 **git 을 읽지 않는다.** 입력이 같으면 결과가 같다.
"""

from __future__ import annotations

import fnmatch
import re
from datetime import date, datetime, timedelta, timezone
from typing import Any

KST = timezone(timedelta(hours=9))

#: 접수부가 심는 합성 키. daily 는 URL 이 없어서 날짜가 그 자리를 대신한다.
DATE_KEY_RE = re.compile(r"daily:(\d{4}-\d{2}-\d{2})")


def target_date(normalized_url: str | None) -> date:
    """조사 대상 날짜. 합성 키(`daily:{date}`)가 있으면 거기서, 없으면 어제(KST).

    어제로 떨어지는 이유는 스케줄러가 **하루가 끝난 뒤** 도는 잡이기 때문이다.
    """
    match = DATE_KEY_RE.search(normalized_url or "")
    if match:
        return date.fromisoformat(match.group(1))
    return datetime.now(KST).date() - timedelta(days=1)

#: 전역 기본 영역 규칙 (SPEC-011 「기술 영역 분해」). 레포별 예외는 레지스트리의
#: `path_rules` 가 앞에 붙는다. 순서가 의미를 갖는다 — 먼저 맞는 규칙이 이긴다.
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


def area_for(path: str, rules: tuple[tuple[str, str], ...] | None = None) -> str:
    """파일 경로 → 기술 영역. 어디에도 안 걸리면 `other`.

    `rules` 는 레포별 예외(`path_rules`)를 **전역 규칙 앞에** 붙인 것이다. 뒤에 붙이면
    전역이 먼저 이겨서 예외가 예외 노릇을 못 한다.
    """
    for pattern, area in rules or AREA_RULES:
        if fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(path, f"*/{pattern}"):
            return area
    return "other"


def rules_for(path_rules: Any) -> tuple[tuple[str, str], ...]:
    """레지스트리의 `path_rules`(`[{glob, area}]`) → `area_for` 가 받는 모양.

    비면 전역 기본만 쓴다. 잘못 생긴 항목은 **조용히 버린다** — 규칙 하나가 깨졌다고
    그날 조사를 통째로 실패시킬 이유가 없고, 어차피 `other` 로 떨어질 뿐이다.
    """
    extra: list[tuple[str, str]] = []
    for rule in path_rules or []:
        if not isinstance(rule, dict):
            continue
        glob, area = rule.get("glob"), rule.get("area")
        if glob and area:
            extra.append((str(glob), str(area)))
    return (*extra, *AREA_RULES)


def decompose(
    commits: list[dict[str, Any]], rules_by_repo: dict[str, Any] | None = None
) -> dict[str, dict[str, int]]:
    """커밋들 → 영역별 집계.

    **한 커밋이 여러 영역에 걸치면 영역마다 계상한다**(SPEC-011). 그래서
    `counts["commit"]` 과 영역별 `commits` 합계는 일치하지 않는다 — 영역별 활동을
    보려는 값이지 커밋을 세려는 값이 아니다.
    """
    areas: dict[str, dict[str, int]] = {}
    for commit in commits:
        rules = (rules_by_repo or {}).get(str(commit.get("repo") or ""))
        seen: set[str] = set()
        for f in commit.get("files") or []:
            area = area_for(str(f.get("path") or ""), rules)
            bucket = areas.setdefault(area, {"commits": 0, "added": 0, "deleted": 0})
            bucket["added"] += int(f.get("added") or 0)
            bucket["deleted"] += int(f.get("deleted") or 0)
            if area not in seen:
                bucket["commits"] += 1
                seen.add(area)
    return areas


def has_activity(payload: dict[str, Any]) -> bool:
    """활동 0이면 이후 단계를 부르지 않는다 (SPEC-011 §5).

    커밋만 보지 않는다 — 노트·교안 변경도 활동이다. 전 레포 조사가 실패해도 그 둘이
    있으면 커밋 없이 진행한다(S-5).
    """
    counts = payload.get("counts") or {}
    return any(int(counts.get(k) or 0) > 0 for k in ("commit", "note", "study"))


#: `context/` 아래 현황 문서를 갖는 영역. `tracked_repos.type` 의 값이자 디렉토리명이다.
#: **`personal` 은 없다** — 개인 영역은 커밋 축이 아니라 배움 축이라 사람이 쓴다
#: (`templates/context/current.md`).
CONTEXT_AREAS = ("company", "studio")


def context_attribution(
    commits: list[dict[str, Any]], meta_by_repo: dict[str, dict[str, Any]]
) -> dict[str, dict[str, list[str]]]:
    """커밋 → `context/{영역}/current.md` 귀속 (KDEV-DEC-022 D1).

    `career_attribution` 과 **같은 자리에 있지만 축이 다르다.** 저쪽은 회사 커밋만
    골라 이력으로 보내고, 이쪽은 회사·개인사업자 **양쪽**을 각자의 현황 문서로 보낸다.
    귀속 기준은 둘 다 `tracked_repos.type` 이다.

    안쪽 키는 **제품**이다 — `## 진행 중` 표의 `Project` 열이 그것이다. 제품에 안
    묶인 레포는 slug 를 그대로 쓴다. 없는 제품명을 지어내지 않는다.

        {"studio": {"kknaks.dev": ["kknaks/kknaks_profile"]}}
    """
    out: dict[str, dict[str, list[str]]] = {}
    for commit in commits:
        repo = str(commit.get("repo") or "")
        meta = meta_by_repo.get(repo) or {}
        area = str(meta.get("type") or "")
        if area not in CONTEXT_AREAS:
            continue
        project = str(meta.get("product_slug") or "").strip() or repo
        repos = out.setdefault(area, {}).setdefault(project, [])
        if repo not in repos:
            repos.append(repo)
    return out

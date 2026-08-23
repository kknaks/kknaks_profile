"""조사 스테이지 — 레포마다 하나씩 (KDEV-WORK-017 P2 / KDEV-SPEC-011·013).

**한 스테이지가 N 건을 제출하는 유일한 자리다.** 레포를 한 프롬프트에 몰아넣지 않는
이유는 둘이다. 하나는 입력 상한 — 하루치 diff 를 다 합치면 레포 하나가 다른 레포의
서술을 밀어낸다. 다른 하나는 부분 실패 — 몰아넣으면 레포 하나 때문에 그날 조사 전체가
날아간다.

여기서 만드는 것은 **문서가 아니다.** `compose` 가 daily·career·concept 초안을 쓸 때
읽을 레포별 재료다. 그래서 형식 규칙(`templates/persona/`)을 참조하지 않는다 — 형식이
필요한 단계는 다음이다.

회사 레포와 개인 레포를 구분하지 않는다. 조사 깊이는 균일하고 **공개 통제는 게이트가**
한다(SPEC-011). 여기서 미리 걸러 두면 사람이 화면에서 판단할 재료가 사라진다.

AI 호출은 open-kknaks 를 거친다. Anthropic SDK 를 직접 import 하지 않는다(OKK ADR-04).
"""

from __future__ import annotations

import json
import logging
from typing import Any

from core.models import QueueItem

from ..executor import Execution, await_execution, poll_execution
from ..prepare import StageSubmission

logger = logging.getLogger("kknaks-back.pipeline.investigate")

PROMPT = """다음은 하루치 커밋 조사 결과 중 **레포 하나**의 몫이다. 이 레포에서 그날
무엇을 왜 했는지 정리하라.

문서를 쓰는 것이 아니다. 다음 단계가 읽을 재료이므로 아래 넷만 한국어로 쓴다.

1. 한 일 — 커밋 메시지를 나열하지 말고 **묶어서** 서술한다. 무엇을 했는지보다
   왜 그렇게 했는지가 중요하다
2. 기술 영역 — 어느 쪽 작업이었는지 서술로. 숫자를 쓰지 않는다
3. 막힌 것·판단 — 커밋에서 읽히는 문제와 선택. 없으면 "없음"
4. 개념 후보 — 재사용 가능한 개념이 보이면 이름 + 한 줄. 없으면 "없음".
   **억지로 만들지 않는다**

의존성 파일(pyproject.toml·package.json·requirements.txt·go.mod)이 변경 목록에 있으면
추가된 패키지를 명시하라. 없으면 스택을 추측하지 않는다.

마크다운 산문으로 답한다. JSON 이나 코드펜스로 감싸지 않는다."""


def group_by_repo(commits: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """레포별로 커밋을 모은다. 순서는 처음 나타난 순."""
    grouped: dict[str, list[dict[str, Any]]] = {}
    for commit in commits:
        grouped.setdefault(str(commit.get("repo") or ""), []).append(commit)
    grouped.pop("", None)
    return grouped


def repo_prompt(repo: str, commits: list[dict[str, Any]], *, meta: dict[str, Any]) -> str:
    payload = {
        "repo": repo,
        "date": meta.get("date"),
        "commits": commits,
        # 상한에 걸려 diff 본문이 빠졌다면 알려 준다 — 서술이 얕은 이유가 자료 부족
        # 때문인지 그날 일이 적어서인지 구분되어야 한다(SPEC-011 S-3).
        "truncated": (meta.get("truncated") or {}).get(repo),
    }
    return PROMPT + "\n\n" + json.dumps(payload, ensure_ascii=False)


class AgentInvestigate:
    """레포별 조사 — `AutoStage` 중 유일하게 **N 건**을 제출한다."""

    stages = ("investigate",)
    #: **이 실행기가 어느 파이프라인의 것인가** — 레포별 조사 — 잔디 전용이다.
    #: 스테이지 이름만 보면 유튜브·블로그의 `collect` 가 여기로 샌다
    #: (실제로 샜다 — 유튜브 항목이 커밋 33건을 수집했다).
    source_kinds = ("daily_commit",)

    def __init__(
        self,
        client,
        *,
        provider: str,
        model: str | None,
        work_dir: str | None,
        timeout_seconds: float = 600,
    ) -> None:
        self.client = client
        self.provider = provider
        self.model = model
        self.work_dir = work_dir
        self.timeout_seconds = timeout_seconds

    async def submit(self, *, item: QueueItem, prior: dict[str, Any]) -> StageSubmission:
        collect = prior.get("collect") or {}
        grouped = group_by_repo(collect.get("commits") or [])
        if not grouped:
            # 커밋이 없어도 노트·교안 변경으로 여기까지 올 수 있다(SPEC-011 S-5 3항).
            # 부를 것이 없으니 조용히 0건으로 지나간다 — 스테이지 실패가 아니다.
            logger.info("조사할 커밋이 없다 item=%s — investigate 를 건너뛴다", item.id)
            return StageSubmission([], {"investigate": {"repos": {}, "skipped": True}})

        options = {"cwd": self.work_dir} if self.work_dir else None
        refs: list[str] = []
        ref_to_repo: dict[str, str] = {}
        for repo, commits in grouped.items():
            ref = await self.client.submit(
                repo_prompt(repo, commits, meta=collect),
                provider=self.provider,
                model=self.model,
                options=options,
                max_retries=2,
                metadata={"source": "pipeline-investigate", "repo": repo},
            )
            refs.append(str(ref))
            ref_to_repo[str(ref)] = repo

        # **대응표를 남긴다.** 수확은 성공한 것만 돌려주므로, 이게 없으면 어느 레포가
        # 빠졌는지 알 수 없다 — 화면의 "조사 중 (3/13)" 과 실패 표시가 여기서 나온다.
        return StageSubmission(refs, {"investigate_refs": ref_to_repo})

    async def wait(self, task_ref: str) -> Execution:
        return await await_execution(
            self.client, task_ref, timeout_seconds=self.timeout_seconds
        )

    async def poll(self, task_ref: str) -> Execution:
        return await poll_execution(
            self.client, task_ref, timeout_seconds=self.timeout_seconds
        )

    def parse(
        self, results: dict[str, str], *, item: QueueItem, prior: dict[str, Any]
    ) -> dict[str, Any]:
        """레포별 조사문. **실패한 레포는 빠진 채로 넘어간다.**

        빈 자리를 지어내지 않는다 — `compose` 가 없는 레포를 서술하면 그날 daily 가
        거짓이 된다. 무엇이 빠졌는지는 `missing` 이 들고 간다.
        """
        ref_to_repo: dict[str, str] = prior.get("investigate_refs") or {}
        repos: dict[str, str] = {}
        for ref, text in results.items():
            repo = ref_to_repo.get(ref)
            body = (text or "").strip()
            if not repo or not body:
                continue
            repos[repo] = body

        missing = sorted(set(ref_to_repo.values()) - set(repos))
        if missing:
            logger.info("조사가 빠진 레포 item=%s: %s", item.id, ", ".join(missing))
        return {"investigate": {"repos": repos, "missing": missing}}

"""취합 스테이지 — daily·career·concept 초안 (KDEV-WORK-017 P2 / KDEV-SPEC-012).

`investigate` 가 만든 레포별 재료를 문서 초안으로 바꾼다. 여기서 처음으로 **형식**이
등장하고, 그 형식은 프롬프트에 적혀 있지 않고 `templates/persona/` 에서 실려 온다.
규칙을 파이썬 문자열에 복사하면 교안에서 없앤 이중 SoT 를 daily·career 에서 다시
만드는 것이 된다(SPEC-012 「형식 SoT」).

세 산출물의 성격이 다르다.

    daily     매일 만든다. 본문은 사이트에 노출되지 않고 다음 단계의 입력이다
    career    **조건부다.** company 귀속 커밋이 0이면 AI 를 부르지도 않는다
    concept   후보가 있을 때만. 억지로 만들지 않는다

`counts` 는 코드가 채운다. AI 출력의 숫자를 믿지 않는다(SPEC-012 §5).

AI 호출은 open-kknaks 를 거친다. Anthropic SDK 를 직접 import 하지 않는다(OKK ADR-04).
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import frontmatter

from core.models import QueueItem
from service.content_format import career_format, daily_format

from ..executor import Execution, await_execution, poll_execution
from ..prepare import StageSubmission

logger = logging.getLogger("kknaks-back.pipeline.compose")

#: 본문 하드 상한 (SPEC-012). 1200자가 목표이고 이 값을 넘으면 자른다.
BODY_HARD_LIMIT = 1500

PROMPT = """다음은 하루치 커밋 조사와 레포별 정리다. 이것으로 문서 초안을 만든다.

아래 **형식 명세를 그대로 따른다.** 명세에 없는 필드를 만들지 않는다.

=== daily 형식 ===
{daily_format}

=== career 형식 ===
{career_format}

## 만들 것

JSON 하나로 답한다. 코드펜스로 감싸지 않는다.

{{
  "daily": {{
    "summary": {{"ko": ["[owner/repo] ...", "[notes] ..."], "en": [...]}},
    "body": "마크다운 본문"
  }},
  "career": {career_shape},
  "concepts": [
    {{"stem": "kebab-case", "title": "제목", "content": "노트 전문", "mode": "new"}}
  ]
}}

- `counts` 를 만들지 마라. 코드가 채운다
- `summary` 는 활동 단위마다 한 줄이고, **활동이 0인 카테고리는 줄을 만들지 않는다**
- `concepts` 는 재사용 가능한 개념이 보일 때만. 없으면 빈 배열. **억지로 만들지 않는다**
"""

CAREER_SHAPE_ACTIVE = """{
    "changed": true,
    "stem": "<대상 stem>",
    "content": "본문 전문 (frontmatter 없이 ## 섹션들만)"
  }"""

CAREER_SHAPE_NONE = """null   (이번엔 career 대상이 없다. null 로 둔다)"""


def career_targets(collect: dict[str, Any], repo_root: Path) -> list[dict[str, Any]]:
    """갱신 대상 career. **결정적으로 고른다 — AI 를 부르기 전에.**

    빠지는 조건이 셋이다(SPEC-012 S-2).

        귀속 커밋 0      `type=studio` 만 커밋한 날. career 를 만들지 않는다
        `is_current` 아님 끝난 재직 기간을 오늘 커밋으로 고치지 않는다
        파일 없음        `detail` 이 가리키는 문서가 사라졌다

    셋 중 하나면 **AI 를 부르지 않는다.** 불러 놓고 버리면 그만큼이 낭비이고,
    "변경 없음" 과 "대상 없음" 이 구분되지 않는다.
    """
    targets: list[dict[str, Any]] = []
    for stem, repos in (collect.get("career_map") or {}).items():
        if not repos:
            continue
        path = repo_root / "persona" / "career" / f"{stem}.md"
        if not path.exists():
            logger.info("career 대상 없음 — %s (DETAIL_NOT_FOUND)", stem)
            continue
        try:
            post = frontmatter.load(path)
        except Exception:  # noqa: BLE001
            logger.warning("career 문서를 읽지 못했다 — %s", stem)
            continue
        if not post.metadata.get("is_current"):
            continue
        targets.append({"stem": stem, "repos": repos, "body": post.content})
    return targets


def build_prompt(
    *, collect: dict[str, Any], investigate: dict[str, Any], targets: list[dict[str, Any]],
    repo_root: Path,
) -> str:
    payload = {
        "date": collect.get("date"),
        "counts": collect.get("counts"),
        "areas": collect.get("areas"),
        "repo_reports": (investigate or {}).get("repos") or {},
        # 조사가 빠진 레포와 상한 적중을 알려 준다 — 서술이 얕은 이유가 자료 부족
        # 때문인지 구분되어야 한다.
        "missing_repos": (investigate or {}).get("missing") or [],
        "truncated": collect.get("truncated") or {},
        "failed_repos": collect.get("failures") or [],
        "career_targets": [
            {"stem": t["stem"], "repos": t["repos"], "current_body": t["body"]}
            for t in targets
        ],
    }
    return PROMPT.format(
        daily_format=daily_format(repo_root),
        career_format=career_format(repo_root),
        career_shape=CAREER_SHAPE_ACTIVE if targets else CAREER_SHAPE_NONE,
    ) + "\n\n" + json.dumps(payload, ensure_ascii=False)


def _strip_fence(raw: str) -> str:
    text = (raw or "").strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1]
        if text.endswith("```"):
            text = text[: -3]
    return text.strip()


def _summary(value: Any) -> dict[str, list[str]]:
    """`{ko: [], en: []}` 로 정규화. 로더가 이 모양을 강제한다."""
    if not isinstance(value, dict):
        raise ValueError("summary 가 {ko, en} 이 아니다")
    out: dict[str, list[str]] = {}
    for key in ("ko", "en"):
        items = value.get(key)
        if not isinstance(items, list) or not all(isinstance(i, str) for i in items):
            raise ValueError(f"summary.{key} 가 list[str] 이 아니다")
        # 활동이 0인 카테고리는 줄이 없어야 한다. 빈 줄이 오면 걸러낸다 —
        # 잔디 셀 카드에 빈 줄이 뜨는 것이 사용자에게 보이는 증상이다.
        out[key] = [i.strip() for i in items if i.strip()]
    return out


class AgentCompose:
    """조사 결과 → daily·career·concept 초안."""

    stages = ("compose",)

    def __init__(
        self,
        client,
        *,
        provider: str,
        model: str | None,
        work_dir: str | None,
        repo_root: Path,
        timeout_seconds: float = 600,
    ) -> None:
        self.client = client
        self.provider = provider
        self.model = model
        self.work_dir = work_dir
        self.repo_root = repo_root
        self.timeout_seconds = timeout_seconds

    async def submit(self, *, item: QueueItem, prior: dict[str, Any]) -> StageSubmission:
        collect = prior.get("collect") or {}
        investigate = prior.get("investigate") or {}
        targets = career_targets(collect, self.repo_root)

        options = {"cwd": self.work_dir} if self.work_dir else None
        ref = await self.client.submit(
            build_prompt(
                collect=collect,
                investigate=investigate,
                targets=targets,
                repo_root=self.repo_root,
            ),
            provider=self.provider,
            model=self.model,
            options=options,
            max_retries=2,
            metadata={"source": "pipeline-compose"},
        )
        return StageSubmission(
            [str(ref)],
            # 대상이 없었다는 사실 자체가 수확의 판단 근거다 — AI 가 career 를 지어내도
            # 대상이 없으면 버린다.
            {"compose_targets": [t["stem"] for t in targets]},
        )

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
        raw = next(iter(results.values()), "")
        try:
            data = json.loads(_strip_fence(raw))
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(f"compose 응답이 JSON 이 아니다: {exc}") from exc
        if not isinstance(data, dict):
            raise RuntimeError("compose 응답이 객체가 아니다")

        daily = data.get("daily") or {}
        body = str(daily.get("body") or "")
        if len(body) > BODY_HARD_LIMIT:
            logger.info("daily 본문 %d자 — %d자로 자른다", len(body), BODY_HARD_LIMIT)
            body = body[:BODY_HARD_LIMIT]

        collect = prior.get("collect") or {}
        composed: dict[str, Any] = {
            "daily": {
                "date": collect.get("date"),
                # **코드가 넣는다.** AI 가 센 숫자를 쓰지 않는다.
                "counts": collect.get("counts") or {},
                "summary": _summary(daily.get("summary")),
                "body": body,
            },
            "career": self._career(data.get("career"), prior),
            "concepts": self._concepts(data.get("concepts")),
        }
        return {"compose": composed}

    def _career(self, value: Any, prior: dict[str, Any]) -> dict[str, Any]:
        """대상이 없으면 무엇이 오든 `changed: false` 다."""
        allowed = set(prior.get("compose_targets") or [])
        if not allowed or not isinstance(value, dict):
            return {"changed": False}
        stem = str(value.get("stem") or "")
        content = str(value.get("content") or "").strip()
        if stem not in allowed or not content or not value.get("changed"):
            return {"changed": False}
        return {"changed": True, "stem": stem, "content": content}

    def _concepts(self, value: Any) -> list[dict[str, Any]]:
        if not isinstance(value, list):
            return []
        out: list[dict[str, Any]] = []
        for entry in value:
            if not isinstance(entry, dict):
                continue
            stem = str(entry.get("stem") or "").strip()
            content = str(entry.get("content") or "").strip()
            if not stem or not content:
                continue
            out.append(
                {
                    "stem": stem,
                    "title": str(entry.get("title") or stem),
                    "content": content,
                    "mode": "supplement" if entry.get("mode") == "supplement" else "new",
                }
            )
        return out

"""`daily` 게이트 스테이지 — 잔디 산출물 작성 (KDEV-WORK-017 P2 / KDEV-SPEC-012·013).

`investigate` 가 만든 레포별 재료를 daily·career·concept 초안으로 바꾼다. 여기서 처음
**형식**이 등장하고, 그 형식은 프롬프트에 적혀 있지 않고 `templates/persona/` 에서
실려 온다(SPEC-012 「형식 SoT」).

**작성 주체가 게이트인 이유.** 처음에는 `compose` 라는 auto 스테이지가 초안을 만들고
게이트는 그것을 보여 주기만 하는 모양이었다. 그런데 재생성(SPEC-013 S-3)은 "조사는
다시 돌지 않고 서술만 다시 만든다" 이므로 **게이트가 작성 능력을 갖고 있어야 한다.**
그러면 auto 쪽 작성은 첫 회에만 쓰이고 재생성마다 게이트가 다시 만드는 중복이 된다.
그래서 작성을 게이트 한 곳으로 모았다. 유튜브도 같은 모양이다 — `summarize`(auto)는
route 판단 재료를 만들 뿐이고 노트 **작성**은 게이트 스테이지가 한다.

세 산출물의 성격이 다르다.

    daily     매일 만든다. 본문은 사이트에 노출되지 않고 다음 단계의 입력이다
    career    **조건부다.** company 귀속 커밋이 0이면 대상에서 아예 빠진다
    concept   후보가 있을 때만. 억지로 만들지 않는다

`counts` 는 코드가 채운다. AI 출력의 숫자를 믿지 않는다(SPEC-012 §5).
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import frontmatter

from service.content_format import career_format, daily_format

from ..executor import AgentStage
from ..gates import GateError, GenerationInput

logger = logging.getLogger("kknaks-back.pipeline.daily")

#: 본문 하드 상한 (SPEC-012). 1200자가 목표이고 이 값을 넘으면 자른다.
BODY_HARD_LIMIT = 1500

PROMPT = """하루치 커밋 조사와 레포별 정리를 읽고 문서 초안을 만든다.

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
- `feedback` 이 있으면 그 지적을 반영해 다시 쓴다. 조사 결과는 바뀌지 않았다
"""

CAREER_SHAPE_ACTIVE = """{
    "changed": true,
    "stem": "<대상 stem>",
    "content": "본문 전문 (frontmatter 없이 ## 섹션들만)"
  }"""

CAREER_SHAPE_NONE = """null   (이번엔 career 대상이 없다. null 로 둔다)"""


def career_targets(collect: dict[str, Any], repo_root: Path) -> list[dict[str, Any]]:
    """갱신 대상 career. **결정적으로 고른다 — 모델에게 묻지 않는다.**

    빠지는 조건이 셋이다(SPEC-012 S-2).

        귀속 커밋 0       `type=studio` 만 커밋한 날. career 를 만들지 않는다
        `is_current` 아님  끝난 재직 기간을 오늘 커밋으로 고치지 않는다
        파일 없음          `detail` 이 가리키는 문서가 사라졌다

    제출과 수확 양쪽에서 같은 값이 나와야 하므로 **저장하지 않고 다시 계산한다** —
    입력이 같으면 결과가 같다. 제출 시점의 지역 변수를 붙잡아 두면 back 재시작 뒤에
    수확이 다른 판단을 하게 된다.
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


def _prep(request: GenerationInput) -> dict[str, Any]:
    return (request.preparation.payload or {}) if request.preparation else {}


def _strip_fence(raw: str) -> str:
    text = (raw or "").strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
        if text.startswith("json"):
            text = text[4:].strip()
    return text


def _summary(value: Any) -> dict[str, list[str]]:
    """`{ko: [], en: []}` 로 정규화. **로더가 이 모양을 하드 검증한다.**

    여기서 막지 않으면 발행 뒤 persona 로드 전체가 실패해 사이트가 옛 데이터를
    계속 서빙한다.
    """
    if not isinstance(value, dict):
        raise GateError("INVALID_DAILY_OUTPUT", "summary 가 {ko, en} 이 아니다")
    out: dict[str, list[str]] = {}
    for key in ("ko", "en"):
        items = value.get(key)
        if not isinstance(items, list) or not all(isinstance(i, str) for i in items):
            raise GateError("INVALID_DAILY_OUTPUT", f"summary.{key} 가 list[str] 이 아니다")
        # 활동이 0인 카테고리는 줄이 없어야 한다. 빈 줄이 오면 잔디 셀 카드에 그대로 뜬다.
        out[key] = [i.strip() for i in items if i.strip()]
    return out


def _career(value: Any, allowed: set[str]) -> dict[str, Any]:
    """대상이 아니면 무엇이 오든 `changed: false` 다.

    모델이 대상 밖 career 를 지어내는 경우를 여기서 버린다 — 대상 판정은 코드가
    결정적으로 했고, 그 판단이 모델 출력보다 우선한다.
    """
    if not allowed or not isinstance(value, dict):
        return {"changed": False}
    stem = str(value.get("stem") or "")
    content = str(value.get("content") or "").strip()
    if stem not in allowed or not content or not value.get("changed"):
        return {"changed": False}
    return {
        "changed": True,
        "stem": stem,
        "content": content,
        "target_path": f"persona/career/{stem}.md",
    }


def _concepts(value: Any) -> list[dict[str, Any]]:
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
                "target_path": f"permanent/concept/{stem}.md",
            }
        )
    return out


class DailyStage(AgentStage):
    """잔디 게이트 — daily·career·concept 초안을 만들고 사람에게 넘긴다."""

    source = "pipeline-daily"

    def prompt(self, request: GenerationInput) -> str:
        targets = career_targets(_prep(request).get("collect") or {}, self.repo_root)
        return PROMPT.format(
            daily_format=daily_format(self.repo_root),
            career_format=career_format(self.repo_root),
            career_shape=CAREER_SHAPE_ACTIVE if targets else CAREER_SHAPE_NONE,
        )

    def payload(self, request: GenerationInput) -> dict[str, Any]:
        prep = _prep(request)
        collect = prep.get("collect") or {}
        investigate = prep.get("investigate") or {}
        targets = career_targets(collect, self.repo_root)
        payload: dict[str, Any] = {
            "date": collect.get("date"),
            "counts": collect.get("counts"),
            "areas": collect.get("areas"),
            "repo_reports": investigate.get("repos") or {},
            # 조사가 빠진 레포와 상한 적중을 알려 준다 — 서술이 얕은 이유가 자료 부족
            # 때문인지 그날 일이 적어서인지 구분되어야 한다.
            "missing_repos": investigate.get("missing") or [],
            "truncated": collect.get("truncated") or {},
            "failed_repos": collect.get("failures") or [],
            # career 는 **전문 교체**라 기존 본문을 함께 준다. 안 주면 모델이 append 할
            # 수밖에 없고, 그러면 career 가 daily 의 복사본이 된다.
            "career_targets": [
                {"stem": t["stem"], "repos": t["repos"], "current_body": t["body"]}
                for t in targets
            ],
        }
        if request.previous_payload is not None:
            payload["previous_draft"] = request.previous_payload
        if request.feedback:
            payload["feedback"] = request.feedback
        return payload

    def parse(self, raw: str, request: GenerationInput) -> dict[str, Any]:
        try:
            data = json.loads(_strip_fence(raw))
        except ValueError as exc:
            raise GateError("INVALID_DAILY_OUTPUT", f"JSON 파싱 실패: {exc}") from exc
        if not isinstance(data, dict):
            raise GateError("INVALID_DAILY_OUTPUT", "출력이 객체가 아니다")

        collect = _prep(request).get("collect") or {}
        daily = data.get("daily") or {}
        body = str(daily.get("body") or "")
        if len(body) > BODY_HARD_LIMIT:
            logger.info("daily 본문 %d자 — %d자로 자른다", len(body), BODY_HARD_LIMIT)
            body = body[:BODY_HARD_LIMIT]

        allowed = {t["stem"] for t in career_targets(collect, self.repo_root)}
        return {
            "daily": {
                "date": collect.get("date"),
                # **코드가 넣는다.** AI 가 센 숫자를 쓰지 않는다.
                "counts": collect.get("counts") or {},
                "summary": _summary(daily.get("summary")),
                "body": body,
                "target_path": f"persona/daily/{collect.get('date')}.md",
            },
            "career": _career(data.get("career"), allowed),
            "concepts": _concepts(data.get("concepts")),
        }

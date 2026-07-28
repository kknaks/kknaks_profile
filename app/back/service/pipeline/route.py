"""route 게이트 — 이 자료를 어디로 보낼지 (KDEV-WORK-014 P3 / KDEV-SPEC-008 stage 3).

route 는 **체인 길이를 결정하는 유일한 게이트**다. 여기서 끈 산출물의 스테이지는
아예 생성되지 않는다. 그래서 route 만 역방향 재오픈이 허용된다(KDEV-DEC-011 D5) —
목적지를 잘못 정하면 뒤가 전부 헛돌기 때문이다.

route 는 본문을 만들지 않는다. 무엇을 만들지만 정한다.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any


from .gates import GateError, GenerationInput, GenerationResult

logger = logging.getLogger("kknaks-back.pipeline.route")

DESTINATIONS = ("reference", "concept", "derived")
#: 목적지를 하나도 안 만드는 선택. 둘은 성격이 다르다 —
#: `inbox_hold` 는 "지금은 정제 못 하지만 버리긴 아깝다", `discard` 는 "안 남긴다".
EXCLUSIVES = ("inbox_hold", "discard")

PROMPT = """이 자료를 어디로 보낼지 판단하라. **본문은 쓰지 않는다** — 목적지만 정한다.

먼저 레포의 규칙을 읽어라. 프롬프트에 복사돼 있지 않다.

1. `rules/knowledge-note-pipeline.md` — 4층 모델, 개념의 입도, SoT 위임
2. `templates/knowledge/reference.md` 와 `concept.md` — 각 층이 무엇을 담는지

그다음 아래 JSON 하나만 출력한다. 코드펜스나 설명 문장을 붙이지 않는다.

{
  "destinations": {
    "reference": {"enabled": true},
    "concept":   {"enabled": true},
    "derived":   {"enabled": false}
  },
  "exclusive": null,
  "rationale": "<왜 이렇게 판단했는지 2~4문장. 특히 concept 를 켜거나 끈 이유>"
}

판단 기준:
- `reference` — 자료를 기록해 둘 가치가 있는가. 대개 켠다. `reference/` 는 **flat** 이라
  하위 폴더를 고르지 않는다 — 분류는 개념 링크가 한다.
- `concept` — **다른 자료·다른 맥락에서 독립적으로 재등장할 개념**이 있는가.
  자료에만 붙어 있는 설명은 개념이 아니다. 없으면 끈다. 억지로 만들지 않는다.
- `derived` — 교안(`persona/contents/`)으로 만들 만한가. 대개 끈다.
- `exclusive` — 위 셋을 전부 끄는 경우에만 쓴다.
  `"inbox_hold"` = 지금은 정제 못 하지만 버리긴 아깝다.
  `"discard"` = 남길 가치가 없다.
  목적지를 하나라도 켰으면 반드시 `null` 이다."""


def validate_route_result(raw: Any) -> dict[str, Any]:
    """route 결과를 정규화한다. 어긋나면 `GateError`.

    AI 출력과 사람이 화면에서 고친 값 **양쪽**이 여기를 통과한다 — 승인 시점에도
    검사해야 토글을 이상하게 조합한 채로 확정되는 것을 막는다.
    """
    if not isinstance(raw, dict):
        raise GateError("INVALID_ROUTE_RESULT", "route 결과가 객체가 아니다")

    incoming = raw.get("destinations")
    if not isinstance(incoming, dict):
        raise GateError("INVALID_ROUTE_RESULT", "destinations 가 없다")

    destinations: dict[str, Any] = {}
    for name in DESTINATIONS:
        entry = incoming.get(name) or {}
        if not isinstance(entry, dict):
            raise GateError("INVALID_ROUTE_RESULT", f"destinations.{name} 이 객체가 아니다")
        destinations[name] = {"enabled": bool(entry.get("enabled"))}

    exclusive = raw.get("exclusive")
    if exclusive is not None and exclusive not in EXCLUSIVES:
        raise GateError("INVALID_ROUTE_RESULT", f"알 수 없는 exclusive: {exclusive}")

    any_enabled = any(destinations[name]["enabled"] for name in DESTINATIONS)
    if exclusive is not None and any_enabled:
        # 둘 다면 무엇이 우선인지 알 수 없다. 조용히 한쪽을 고르지 않는다.
        raise GateError(
            "INVALID_ROUTE_RESULT", "exclusive 와 목적지를 동시에 켤 수 없다"
        )
    if exclusive is None and not any_enabled:
        raise GateError(
            "INVALID_ROUTE_RESULT", "목적지를 하나도 켜지 않았으면 exclusive 를 정해야 한다"
        )

    result: dict[str, Any] = {"destinations": destinations, "exclusive": exclusive}
    rationale = raw.get("rationale")
    if isinstance(rationale, str) and rationale.strip():
        result["rationale"] = rationale.strip()
    return result


def _parse(text: str) -> Any:
    """모델이 코드펜스를 붙이는 경우가 있어 한 겹 벗겨 본다."""
    cleaned = (text or "").strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[-1]
        if cleaned.endswith("```"):
            cleaned = cleaned[: -3]
        cleaned = cleaned.strip()
        if cleaned.startswith("json"):
            cleaned = cleaned[4:].strip()
    try:
        return json.loads(cleaned)
    except ValueError as exc:
        raise GateError("INVALID_ROUTE_RESULT", f"JSON 파싱 실패: {exc}") from exc


class RouteProposer:
    """open-kknaks 로 목적지 제안을 만든다.

    프롬프트는 "무엇을 판단하라"만 지시하고, **4층 모델과 개념 입도 기준은 레포에서 읽게**
    한다(`rules/knowledge-note-pipeline.md`). 규칙을 프롬프트에 복사하면 SoT 가 둘이 되고
    한쪽만 고쳐지는 날 조용히 어긋난다 — WORK-013 에서 세운 원칙이다.
    """

    def __init__(
        self,
        client,
        *,
        repo_root: Path,
        provider: str,
        model: str | None,
        work_dir: str | None,
        timeout_seconds: float = 600,
    ) -> None:
        self.client = client
        self.repo_root = repo_root
        self.provider = provider
        self.model = model
        self.work_dir = work_dir
        self.timeout_seconds = timeout_seconds

    async def __call__(self, request: GenerationInput) -> GenerationResult:
        payload = {
            "source_url": request.item.source_url,
            "source_kind": request.item.source_kind,
            "note": request.item.note,
            "summary": (request.preparation.payload or {}).get("summary")
            if request.preparation
            else None,
            "material_source": (request.preparation.payload or {}).get("material_source")
            if request.preparation
            else None,
        }
        if request.previous_payload is not None:
            payload["previous_proposal"] = request.previous_payload
        if request.feedback:
            payload["feedback"] = request.feedback

        options: dict[str, Any] = {"cwd": self.work_dir} if self.work_dir else {}
        if request.session_ref:
            # 세션을 이어받으면 원문·지침을 다시 보내지 않아도 된다 (SPEC-009 S-1 5항).
            options["resume"] = {"mode": "session", "session_id": request.session_ref}

        task_id = await self.client.submit(
            PROMPT + "\n\n" + json.dumps(payload, ensure_ascii=False),
            provider=self.provider,
            model=self.model,
            options=options or None,
            max_retries=2,
            metadata={"source": "pipeline-route", "item_id": request.item.id},
        )
        task = await self.client.result(task_id, timeout=self.timeout_seconds)
        if task is None or not task.result:
            raise RuntimeError(getattr(task, "error", None) or "open_kknaks returned no result")

        result = validate_route_result(_parse(str(task.result)))
        return GenerationResult(
            payload=result,
            session_ref=getattr(task, "result_session_id", None),
            external_task_ref=str(task_id),
        )


def route_outcome(payload: dict[str, Any]) -> str:
    """승인된 route 가 항목을 어디로 보내는가.

    `discard` 만 항목을 끝낸다. `inbox_hold` 는 **끝이 아니다** — `inbox/` 에 idea 노트를
    남기는 발행이 남아 있어 여전히 발행 대상이다(KDEV-DEC-011 D1).
    """
    return "discarded" if payload.get("exclusive") == "discard" else "publishable"

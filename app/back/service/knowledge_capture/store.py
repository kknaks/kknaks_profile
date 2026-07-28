"""Capture store 계약 — 캡처 노트를 어디에 어떻게 남기고 어떻게 다시 읽을지 (KDEV-WORK-012).

runner 는 "무엇을 만들지"(원문 수집·AI 호출·파싱·경로 결정·렌더)까지만 하고,
**영속화는 store 가 양방향으로 소유한다**.

- 현재 store: 레포에 md 를 쓰고 commit/push (`service.slack_bridge.stores.FileCaptureStore`)
- 후속 store: 승인 큐에 draft 적재 (KDEV-WORK-014) — 파일도 push 도 하지 않는다

**양방향인 이유**: 스레드 후속 대화는 "이전 초안"을 AI 에 다시 넘겨야 하는데, 그 초안이
어디 있는지는 저장한 쪽만 안다. 쓰기만 추상화하고 읽기를 runner 에 남겨두면 (파일을
직접 `read_text` 하는 식) 큐 store 로 갈아끼울 때 runner 를 또 고쳐야 한다.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol


@dataclass(frozen=True)
class CaptureArtifact:
    """store 에 넘기는 캡처 산출물 한 건."""

    path: Path
    """시스템이 조립한 목적지 경로 (레포 루트 기준 절대경로).

    큐 store 에서는 아직 파일을 만들지 않으므로 **발행 예정 목적지**를 뜻한다.
    """

    rendered: str
    """렌더된 markdown 전문."""

    document: Any
    """`CaptureDocument` — kind/title/slug/tags/connection_candidates 등."""

    replace: bool = False
    """기존 산출물 갱신 여부. 스레드 후속(follow-up)이면 True."""

    request: Any = None
    """`CaptureRequest` — 큐 store 가 채널/스레드/제출자를 기록할 때 쓴다."""


@dataclass(frozen=True)
class StoreResult:
    """store 실행 결과 — Slack 회신과 세션 기록에 필요한 정보."""

    location: str
    """사용자에게 보여줄 위치. 파일 store 면 레포 상대 경로, 큐 store 면 큐 항목 참조."""

    stored_ref: str | None = None
    """다음 후속 대화에서 `load_previous` 에 넘어올 **불투명 참조**.

    이 값을 해석하는 것은 store 자신뿐이다. 파일 store 는 상대 경로를,
    큐 store 는 `queue:<id>` 같은 참조를 넣는다. 저장하지 않는 store 면 None.
    (세션에는 `CaptureSession.output_path` 필드로 실린다 — 이름은 파일 시절의 잔재이며
    의미는 "store 참조"다.)
    """

    warnings: tuple[str, ...] = field(default_factory=tuple)
    """치명적이지 않은 경고 (push 실패, reload 거부 등)."""


@dataclass(frozen=True)
class PreviousCapture:
    """스레드 후속 대화에서 이어 쓸 직전 상태."""

    markdown: str | None = None
    """직전 산출물 전문. AI 에 "이전 초안"으로 넘어간다. 없으면 None."""

    output_override: Path | None = None
    """같은 목적지로 다시 쓰기 위한 경로(레포 루트 기준 상대). 없으면 새로 조립한다."""


EMPTY_PREVIOUS = PreviousCapture()


class CaptureStore(Protocol):
    """캡처 산출물의 영속화 계약. 쓰기와 읽기를 한 구현이 함께 소유한다."""

    async def load_previous(self, session: Any) -> PreviousCapture:
        """`CaptureSession` 으로부터 직전 산출물을 복원한다.

        참조가 없거나 대상이 사라졌으면 `EMPTY_PREVIOUS` 를 돌려준다 — 후속 대화가
        실패하는 대신 새로 쓰는 쪽으로 흐르게 한다.
        """
        ...

    async def store(self, artifact: CaptureArtifact) -> StoreResult:
        """산출물을 영속화한다."""
        ...

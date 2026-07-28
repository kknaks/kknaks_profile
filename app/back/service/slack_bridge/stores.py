"""Capture store 구현 — 현재는 파일 store 하나 (KDEV-WORK-012).

`FileCaptureStore` 는 흡수 이전 동작(atomic_write → commit/push → reload + 후속 시 파일
재읽기)을 그대로 옮긴 것이다. KDEV-WORK-014 가 이 자리에 큐 store 를 끼우면 캡처가
파일 대신 승인 큐로 간다 — 그때 `runner.py` 는 건드리지 않는다.
"""

from __future__ import annotations

import inspect
from pathlib import Path
from typing import Awaitable, Callable

from service.knowledge_capture import (
    EMPTY_PREVIOUS,
    CaptureArtifact,
    PreviousCapture,
    StoreResult,
    atomic_write,
)


async def _maybe_await(value):
    return await value if inspect.isawaitable(value) else value


class FileCaptureStore:
    """레포에 md 를 쓰고 commit/push 한 뒤 메모리 reload 를 요청한다.

    `publish` 와 `reload_data` 는 주입받는다 — 테스트가 fake 를 넣고, 운영은
    `commit_and_push_with_retry` / `reload_data` 를 넣는다.
    """

    def __init__(
        self,
        *,
        repo_root: Path,
        publish: Callable[[Path], bool | Awaitable[bool]],
        reload_data: Callable[[], bool | Awaitable[bool]],
    ) -> None:
        self.repo_root = repo_root.resolve()
        self.publish = publish
        self.reload_data = reload_data

    async def load_previous(self, session) -> PreviousCapture:
        """직전 산출물을 파일에서 복원한다.

        참조는 레포 상대 경로다. 레포 밖을 가리키면 빈 결과를 돌려준다(경로 이탈 차단).
        파일이 사라졌으면 본문만 비우고 **목적지는 유지한다** — 같은 노트를 계속
        갱신하는 것이 스레드 후속의 의도이기 때문이다.
        """
        ref = getattr(session, "output_path", None) if session else None
        if not ref:
            return EMPTY_PREVIOUS

        relative = Path(ref)
        path = (self.repo_root / relative).resolve()
        if not path.is_relative_to(self.repo_root):
            return EMPTY_PREVIOUS

        markdown = path.read_text(encoding="utf-8") if path.is_file() else None
        return PreviousCapture(markdown=markdown, output_override=relative)

    async def store(self, artifact: CaptureArtifact) -> StoreResult:
        atomic_write(artifact.path, artifact.rendered, replace=artifact.replace)

        publish_ok = await _maybe_await(self.publish(artifact.path))
        reload_ok = await _maybe_await(self.reload_data())

        warnings: list[str] = []
        if not publish_ok:
            warnings.append("⚠ 파일은 저장됐지만 Git push에 실패했습니다.")
        if not reload_ok:
            warnings.append("⚠ 파일은 저장됐지만 그래프 reload가 거부됐습니다.")

        relative = artifact.path.relative_to(self.repo_root).as_posix()
        return StoreResult(
            location=relative,
            stored_ref=relative,
            warnings=tuple(warnings),
        )

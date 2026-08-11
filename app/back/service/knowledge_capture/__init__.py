"""Slack knowledge capture domain primitives.

**파일 쓰기 계열은 제거됐다** (KDEV-DEC-013 D2). 슬랙은 URL 을 큐에 적재하는
입구이고, 파일 쓰기·커밋은 승인 뒤 Apply Executor 가 단독으로 한다.
지워진 것: `render`·`writer`·`store`(그리고 `slack_bridge/runner`·`stores`) —
게이트 이전에 슬랙이 바로 레포에 쓰던 경로다.
"""

from .models import CaptureDocument, CaptureValidationError, parse_document
from .session import CaptureSession, CaptureSessionStore, ThreadBusyError

__all__ = [
    "CaptureDocument",
    "CaptureValidationError",
    "CaptureSession",
    "CaptureSessionStore",
    "ThreadBusyError",
    "parse_document",
]

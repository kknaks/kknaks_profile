"""mcp 도메인 에러.

에러 문구는 **모델이 읽는다**. 그래서 「무엇을 하라/하지 마라」까지 적는다 —
`NOT_FOUND` 에 「다른 slug 를 추측하지 마라」가 들어 있는 것이 그 이유다. 코드가 읽는
에러라면 필요 없었을 문장이다.
"""

from __future__ import annotations


class McpError(Exception):
    code = "INTERNAL_ERROR"
    message = "서버 내부 오류입니다"

    def __init__(self, message: str | None = None) -> None:
        self.message = message or self.message
        super().__init__(self.message)


class UnauthorizedError(McpError):
    code = "UNAUTHORIZED"
    message = "이 turn 의 토큰이 유효하지 않습니다 — tool 을 부를 수 없습니다"


class NotFoundError(McpError):
    """미노출과 없음을 구분하지 않는다(DEC-027 D4) — 모델에게는 없는 문서다."""

    code = "NOT_FOUND"
    message = (
        "그런 문서가 없습니다. 다른 slug 를 추측해 다시 부르지 말고, "
        "기록에 없다고 답하세요."
    )


class UpstreamError(McpError):
    code = "UPSTREAM_ERROR"
    message = "이력 데이터를 읽지 못했습니다"

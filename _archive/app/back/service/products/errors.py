"""제품 레지스트리 도메인 예외 (KDEV-WORK-018 P3).

**`HTTPException` 을 쓰지 않는다.** service 가 HTTP 를 알면 CLI·잡·테스트에서 같은
코드를 못 쓴다. 라우터가 `code` 를 보고 상태코드로 바꾼다 —
`service/pipeline/gates.py` 의 `GateError` → `api/routers/queue.py:414 _gate_error()`
가 이미 같은 형태다.

`code` 는 KDEV-SPEC-014 §4 Validation 의 사유 코드 그대로다. 화면이 그 문자열로 필드를
찾아 오류를 붙이므로 **임의로 바꾸면 화면이 조용히 못 찾는다.**
"""

from __future__ import annotations


class ProductError(ValueError):
    """등록·수정이 거부된 이유.

    `field` 는 화면이 어느 입력 아래에 메시지를 붙일지 정한다. 전체에 해당하면 비운다.
    """

    def __init__(self, code: str, message: str, *, field: str | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.field = field

    def as_dict(self) -> dict[str, str | None]:
        return {"code": self.code, "message": self.message, "field": self.field}


class ProductNotFound(LookupError):
    """레지스트리 행이 없다. 라우터가 404 로 바꾼다."""


class ScaffoldError(RuntimeError):
    """파일을 만들거나 커밋하는 데 실패했다.

    검증과 구분한다 — 검증 실패는 **아무것도 만들지 않은** 상태이고, 이것은 **일부를
    만들었을 수 있는** 상태다. 그래서 이쪽은 롤백이 따라붙는다.
    """

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message

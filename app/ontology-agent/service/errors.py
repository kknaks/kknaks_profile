"""조회 표면의 에러 코드 — SPEC-002 §4 Case Matrix · SPEC-003 Case Matrix 단일 표.

도구는 `{"error": <코드>, "detail": …}` 로, API 는 `{"detail": <코드>}` 로 낸다.
**코드는 한 곳에서만 정의한다** — 두 표면이 다른 이름을 쓰면 같은 실패가 두 이름을 갖는다.

거부 응답에는 **허용 목록을 동봉**한다(SPEC-002 AC-2) — 에이전트가 무엇을 고를 수 있는지
모른 채 재시도를 반복하지 않게 한다.
"""

from __future__ import annotations


class QueryError(Exception):
    """조회 거부. `code` 가 Case Matrix 의 코드, `http_status` 가 API 응답 코드다."""

    code = "QUERY_ERROR"
    http_status = 400

    def __init__(self, detail: str = "", allowed: list | None = None) -> None:
        super().__init__(detail or self.code)
        self.detail = detail or self.code
        self.allowed = allowed

    def to_tool_payload(self) -> dict:
        payload: dict = {"error": self.code, "detail": self.detail}
        if self.allowed is not None:
            payload["allowed"] = self.allowed
        return payload


class UnknownMetric(QueryError):
    code = "UNKNOWN_METRIC"


class UnknownTable(QueryError):
    code = "UNKNOWN_TABLE"
    http_status = 404


class UnknownField(QueryError):
    """허용 필드 목록 밖의 이름. 목록은 **뷰의 실제 컬럼**이다.

    **PII 원 컬럼명은 이 예외로 막히지 않는다.** 마스킹 뷰가 별칭을 원본과 같게 주므로
    `patientName`·`phone`·`birthday` 는 목록 안에 있고 `filters`·`order_by` 를 통과한다.
    원값 우회가 성립하지 않는 이유는 값이 마스킹본이라 원값으로 조회하면 0건이기 때문이다.
    SPEC-002 AC-3 의 문언(「어디에 넣어도 거부된다」)과는 이 지점에서 갈리며,
    편차는 테스트 독스트링에 명시돼 있다.
    """

    code = "UNKNOWN_FIELD"


class UnknownTerm(QueryError):
    code = "UNKNOWN_TERM"
    http_status = 404


class UnknownNode(QueryError):
    code = "UNKNOWN_NODE"
    http_status = 404


class InvalidRange(QueryError):
    code = "INVALID_RANGE"


class LimitExceeded(QueryError):
    """상한 초과는 **절단이 아니라 거부**다 — 소리 없는 절단 금지(SPEC-002 §5)."""

    code = "LIMIT_EXCEEDED"


class TooManyFilters(QueryError):
    code = "TOO_MANY_FILTERS"


class SourceUnavailable(QueryError):
    code = "SOURCE_UNAVAILABLE"
    http_status = 503


#: 빈 결과는 **에러가 아니다** — 200 + 빈 배열이다(SPEC-002 §4). 코드는 문서상 표기용으로만
#: 존재하고 예외 클래스를 두지 않는다. 예외를 두면 언젠가 누가 그것을 던진다.
EMPTY_RESULT = "EMPTY_RESULT"

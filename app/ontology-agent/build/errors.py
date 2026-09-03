"""빌드 실패 코드 — SPEC-001 §4 Case Matrix 그대로.

게이트 실패는 exit code ≠ 0 이고, 코드와 기대·실측값을 로그로 남긴다.
로그에 PII 원값을 쓰지 않는다 — 행수·합계·식별자만.
"""

from __future__ import annotations


class BuildError(Exception):
    """빌드 중단. `code` 는 SPEC-001 Case Matrix 의 코드다."""

    code = "BUILD_ERROR"

    def __init__(self, message: str, detail: list[str] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.detail = detail or []

    def render(self) -> str:
        lines = [f"{self.code}: {self.message}"]
        lines += [f"  {d}" for d in self.detail]
        return "\n".join(lines)


class BronzeRowcountMismatch(BuildError):
    code = "BRONZE_ROWCOUNT_MISMATCH"


class EnumViolation(BuildError):
    code = "ENUM_VIOLATION"


class NegativeAmount(BuildError):
    code = "NEGATIVE_AMOUNT"


class ClosedListViolation(BuildError):
    code = "CLOSED_LIST_VIOLATION"


class RebuildMismatch(BuildError):
    code = "REBUILD_MISMATCH"


class OrphanEdge(BuildError):
    code = "ORPHAN_EDGE"


class PiiLeak(BuildError):
    code = "PII_LEAK"


class NodeIdMismatch(BuildError):
    """SPEC-001 §4 25종 표와 `ontology_nodes` 의 1:1 대조 실패 (AC-6)."""

    code = "NODE_ID_MISMATCH"


# --- WORK-001 신설 코드 5종 (SPEC-001 v0.0.7 Case Matrix 등재 완료) --------
# `ENUM_VIOLATION` 은 spec 상 `visit_status` 전용이라 다른 원인을 그 코드로 올리면
# 로그가 원인을 가리키지 못한다. 그래서 아래로 갈랐다.


class ReviewScoreViolation(BuildError):
    """리뷰 채점 System 검증 위반 — 점수 범위·0.5 단위·근거 미실존·채점 누락 (기록 04 게이트 4·5)."""

    code = "REVIEW_SCORE_VIOLATION"


class MaskingResidue(BuildError):
    """마스킹 잔존 — `body_masked` 에 직원 실명 토큰이 남았다 (기록 04 게이트 7)."""

    code = "MASKING_RESIDUE"


class AgreementBelowThreshold(BuildError):
    """강남언니 평점 정합률 미달 (기록 04 게이트 6 — ±0.5 이내 80% 이상).

    이식 원본 `reviews_finalize.py:117` 의 `sys.exit(2)` 동등물이다.
    """

    code = "AGREEMENT_BELOW_THRESHOLD"


class UnknownBranch(BuildError):
    """지점 alias 매핑에 없는 표기 — 정본 코드로 치환할 수 없다 (기록 03 1장 지점)."""

    code = "UNKNOWN_BRANCH"


class RowcountMismatch(BuildError):
    """실버 행수 대사 불일치 — 브론즈 ≠ 실버 + 필터 제외 + 중복 제거 (기록 04 게이트 1)."""

    code = "SILVER_ROWCOUNT_MISMATCH"

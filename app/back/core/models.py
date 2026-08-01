"""ORM 모델 (auth-01 — DB화 토대 / KDEV-WORK-014 — 승인 파이프라인).

첫 모델은 User(관리자 인증). 이어서 승인 큐·게이트 체인 테이블이 붙는다.

**md 파일과 DB 의 경계**(40-architecture/database): 발행된 노트 본문의 SoT 는
Markdown 이고, DB 는 운영 상태·승인 워크플로·**승인 전 초안**을 소유한다.
초안이 DB 에 있어야 하는 것은 취향이 아니라 강제 조건이다 —
`POST /admin/reload` 가 `git reset --hard origin/main` 을 돌려 미커밋 md 를 지운다.

설계 규약:
- 상태는 **텍스트 + CHECK**. DB enum 타입을 쓰지 않는다(값 추가마다 마이그레이션).
- `stage_name`·`kind` 처럼 **파이프라인 정의에서 오는 값은 제약하지 않는다** —
  정의가 데이터이므로(KDEV-DEC-011 D2) 입력 종류가 늘어도 스키마를 안 건드린다.
- 이력 테이블(`ItemPreparation`·`GateRevision`·`AITask`)은 **불변**이다.
  재시도·재생성은 UPDATE 가 아니라 새 행 + 원 행 참조다.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from core.db import Base

# --- 상태값 -----------------------------------------------------------------
# 넷은 서로 다른 상태다. 게이트가 `검토 대기` 인데 실행은 `succeeded` 이고
# 버전은 `reviewable` 인 것이 정상이다 — 합치면 "AI 가 실패한 것" 과
# "사람이 아직 안 본 것" 이 구분되지 않는다.

ITEM_STATUSES = (
    "received",
    "preparing",
    "in_review",
    "prepare_failed",
    "publishing",
    "published",
    "publish_failed",
    "discarded",
    "deleted",
)
#: 아직 발행되지 않아 같은 URL 재투입 시 **합류 대상**이 되는 상태 (SPEC-007 S-4).
ITEM_PENDING_STATUSES = (
    "received",
    "preparing",
    "in_review",
    "prepare_failed",
    "publishing",
    "publish_failed",
)
#: `running` 은 게이트 버전의 `drafting` 과 같은 자리다 — 수집은 끝났고 요약이
#: 아직 실행기 큐에 있는 구간 (KDEV-WORK-016 P2).
PREPARATION_STATUSES = ("running", "succeeded", "failed")
AI_TASK_STATUSES = ("queued", "running", "succeeded", "failed")
GATE_STATUSES = (
    "not_started",
    "generating",
    "review_pending",
    "failed",
    "feedback_pending",
    "regenerating",
    "approved",
    "cancelled",
)
REVISION_STATUSES = ("drafting", "reviewable", "approved", "superseded", "failed")
FEEDBACK_STATUSES = ("submitted", "consumed")
PLAN_VALIDATION_STATUSES = ("pending", "passed", "rejected")
APPLY_RESULT_STATUSES = ("succeeded", "rejected", "failed")


def _in(column: str, values: tuple[str, ...]) -> str:
    joined = ", ".join(f"'{v}'" for v in values)
    return f"{column} IN ({joined})"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(32), nullable=False, default="admin")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class QueueItem(Base):
    """승인 큐 항목 — 접수부터 발행까지의 lifecycle 소유자 (KDEV-SPEC-007).

    `in_review` 동안의 진행 상태는 항목이 아니라 **게이트가 소유**한다.
    항목 status 는 스테이지마다 바뀌지 않는다.
    """

    __tablename__ = "queue_items"
    __table_args__ = (
        CheckConstraint(_in("status", ITEM_STATUSES), name="ck_queue_items_status"),
        # 발행 전 같은 URL 은 새 항목을 만들지 않고 기존 항목에 합류한다(S-4).
        # 발행 뒤에는 같은 자료의 재정리가 정당하므로 제약을 걸지 않는다.
        Index(
            "uq_queue_items_pending_url",
            "normalized_url",
            unique=True,
            postgresql_where=text(
                "normalized_url IS NOT NULL AND deleted_at IS NULL AND "
                + _in("status", ITEM_PENDING_STATUSES)
            ),
        ),
        Index("ix_queue_items_status", "status"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    #: 파이프라인 정의를 고르는 키. 정의가 데이터라 CHECK 를 걸지 않는다.
    source_kind: Mapped[str] = mapped_column(String(32), nullable=False)
    source_url: Mapped[str | None] = mapped_column(Text)
    #: 중복 판정 기준. 텍스트 입력 항목은 null.
    normalized_url: Mapped[str | None] = mapped_column(Text)
    #: 메모. 수집 성공·실패와 무관하게 항상 요약 입력에 동반되고, 수집이 막히면 원문을 대체한다.
    note: Mapped[str | None] = mapped_column(Text)
    channel: Mapped[str] = mapped_column(String(32), nullable=False, default="manual")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="received")
    #: Slack 사용자 식별자를 담을 수 있어 문자열 — `users` 와 FK 로 잇지 않는다(단일 관리자).
    submitted_by: Mapped[str | None] = mapped_column(String(128))
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    commit_ref: Mapped[str | None] = mapped_column(String(64))
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class AITask(Base):
    """AI 실행 이력 — 실패와 재시도를 포함한 **불변** 기록 (KDEV-SPEC-009).

    재시도는 이 행을 고치지 않고 `retry_of_task_id` 로 원 행을 가리키는 새 행을 만든다.
    실패를 지우면 "왜 이 결과가 나왔는지" 를 잃는다.
    """

    __tablename__ = "ai_tasks"
    __table_args__ = (
        CheckConstraint(_in("status", AI_TASK_STATUSES), name="ck_ai_tasks_status"),
        Index("ix_ai_tasks_item_id", "item_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(
        ForeignKey("queue_items.id", ondelete="CASCADE"), nullable=False
    )
    #: 어느 스테이지의 생성/재생성인가. 스테이지는 정의에서 오므로 CHECK 를 걸지 않는다.
    kind: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="queued")
    retry_of_task_id: Mapped[int | None] = mapped_column(
        ForeignKey("ai_tasks.id", ondelete="SET NULL")
    )
    #: 실행이 반환한 세션 참조 — 다음 재생성의 resume 원천.
    session_ref: Mapped[str | None] = mapped_column(String(128))
    external_task_ref: Mapped[str | None] = mapped_column(String(128))
    error_code: Mapped[str | None] = mapped_column(String(64))
    error_message: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class ItemPreparation(Base):
    """자동 준비(수집·요약) 산출물 — 버전마다 **박제**한다 (KDEV-SPEC-007).

    준비 재시도는 덮어쓰지 않고 새 버전을 남긴다. 실패한 준비도 행으로 남아
    "무엇이 막혔는지" 를 상세 화면이 보여줄 수 있다.
    """

    __tablename__ = "item_preparations"
    __table_args__ = (
        CheckConstraint(
            _in("status", PREPARATION_STATUSES), name="ck_item_preparations_status"
        ),
        Index("uq_item_preparations_version", "item_id", "version", unique=True),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(
        ForeignKey("queue_items.id", ondelete="CASCADE"), nullable=False
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    #: 수집 원문·요약. 조회 키가 되는 값이 생기면 컬럼으로 승격한다.
    payload: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    ai_task_id: Mapped[int | None] = mapped_column(
        ForeignKey("ai_tasks.id", ondelete="SET NULL")
    )
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class Gate(Base):
    """스테이지별 게이트 컨테이너 — 사용자가 보는 단계의 상태 (KDEV-SPEC-008).

    승인 대상 내용은 게이트가 아니라 `GateRevision` 이 들고 있다.
    """

    __tablename__ = "gates"
    __table_args__ = (
        CheckConstraint(_in("status", GATE_STATUSES), name="ck_gates_status"),
        # 항목·스테이지당 살아 있는 게이트는 하나. route 재오픈으로 무효화된
        # `cancelled` 게이트는 이력으로 남아야 하므로 제약에서 뺀다.
        Index(
            "uq_gates_live_stage",
            "item_id",
            "stage_name",
            unique=True,
            postgresql_where=text("status <> 'cancelled'"),
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(
        ForeignKey("queue_items.id", ondelete="CASCADE"), nullable=False
    )
    #: `route`·`source_note`·`concept`·`derived`… 정의에서 온다 — CHECK 없음.
    stage_name: Mapped[str] = mapped_column(String(32), nullable=False)
    stage_no: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(24), nullable=False, default="not_started")
    active_revision_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "gate_revisions.id",
            use_alter=True,
            name="fk_gates_active_revision",
            ondelete="SET NULL",
        )
    )
    approved_revision_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "gate_revisions.id",
            use_alter=True,
            name="fk_gates_approved_revision",
            ondelete="SET NULL",
        )
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class GateRevision(Base):
    """AI 제안 버전 — 실제 승인 대상 (KDEV-SPEC-009).

    피드백을 받으면 v1 을 고치지 않고 v2 를 만든다. v1 은 read-only 로 남아
    "무엇을 보고 무슨 지시를 했는지" 가 보존된다.
    """

    __tablename__ = "gate_revisions"
    __table_args__ = (
        CheckConstraint(_in("status", REVISION_STATUSES), name="ck_gate_revisions_status"),
        Index("uq_gate_revisions_version", "gate_id", "version", unique=True),
        # 게이트당 승인 버전은 하나. 이건 DB 가 강제한다.
        # (반면 "검토 가능 버전 하나" 는 전이 순간의 경합 때문에 앱 sweep 소관 — SPEC-009 §5)
        Index(
            "uq_gate_revisions_approved",
            "gate_id",
            unique=True,
            postgresql_where=text("status = 'approved'"),
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    gate_id: Mapped[int] = mapped_column(
        ForeignKey("gates.id", ondelete="CASCADE"), nullable=False
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="drafting")
    payload: Mapped[dict[str, Any] | None] = mapped_column(JSONB)
    parent_revision_id: Mapped[int | None] = mapped_column(
        ForeignKey("gate_revisions.id", ondelete="SET NULL")
    )
    feedback_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "gate_feedbacks.id",
            use_alter=True,
            name="fk_gate_revisions_feedback",
            ondelete="SET NULL",
        )
    )
    ai_task_id: Mapped[int | None] = mapped_column(
        ForeignKey("ai_tasks.id", ondelete="SET NULL")
    )
    session_ref: Mapped[str | None] = mapped_column(String(128))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class GateFeedback(Base):
    """재생성을 유발한 사용자 지시 (KDEV-SPEC-009)."""

    __tablename__ = "gate_feedbacks"
    __table_args__ = (
        CheckConstraint(_in("status", FEEDBACK_STATUSES), name="ck_gate_feedbacks_status"),
        Index("ix_gate_feedbacks_gate_id", "gate_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    gate_id: Mapped[int] = mapped_column(
        ForeignKey("gates.id", ondelete="CASCADE"), nullable=False
    )
    target_revision_id: Mapped[int | None] = mapped_column(
        ForeignKey("gate_revisions.id", ondelete="SET NULL")
    )
    body: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="submitted")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class ApplyPlan(Base):
    """발행 계획 — 무엇을 어디에 쓸지 (KDEV-SPEC-010).

    **AI 가 파일을 직접 건드리지 않는다.** AI 는 내용만 내고, 무엇을 어느 경로에 쓸지는
    이 계획이 들고 있으며 Executor 만 실행한다(KDEV-DEC-012 D2).
    """

    __tablename__ = "apply_plans"
    __table_args__ = (
        CheckConstraint(
            _in("validation_status", PLAN_VALIDATION_STATUSES),
            name="ck_apply_plans_validation_status",
        ),
        Index("ix_apply_plans_item_id", "item_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(
        ForeignKey("queue_items.id", ondelete="CASCADE"), nullable=False
    )
    #: `[{action, path, content, stem, layer, source_gate}]` — 경로는 시스템이 조립한 값이다.
    file_actions: Mapped[list[Any]] = mapped_column(JSONB, nullable=False)
    validation_status: Mapped[str] = mapped_column(
        String(16), nullable=False, default="pending"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class ApplyResult(Base):
    """발행 결과 — 성공·거부·실패를 모두 남긴다 (KDEV-SPEC-010).

    재시도는 이 행을 고치지 않고 **새 행**을 만든다. 실패를 지우면 왜 안 나갔는지를 잃는다.
    """

    __tablename__ = "apply_results"
    __table_args__ = (
        CheckConstraint(
            _in("status", APPLY_RESULT_STATUSES), name="ck_apply_results_status"
        ),
        Index("ix_apply_results_item_id", "item_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    plan_id: Mapped[int] = mapped_column(
        ForeignKey("apply_plans.id", ondelete="CASCADE"), nullable=False
    )
    item_id: Mapped[int] = mapped_column(
        ForeignKey("queue_items.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    commit_ref: Mapped[str | None] = mapped_column(String(64))
    #: 검증 위반 목록. 거부 사유를 사람이 읽을 수 있어야 재시도 판단이 선다.
    violations: Mapped[list[Any] | None] = mapped_column(JSONB)
    error_code: Mapped[str | None] = mapped_column(String(64))
    error_message: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


#: 추적 레포의 성격. `company` 만 career 로 귀속된다 (KDEV-SPEC-011).
TRACKED_REPO_TYPES = ("company", "studio")
#: 클론·fetch 에 쓸 토큰.
TRACKED_REPO_ACCOUNTS = ("personal", "company")


class TrackedRepo(Base):
    """잔디가 추적할 레포 (KDEV-WORK-017 P5 / KDEV-SPEC-011).

    **"보여줄 레포" 와 "긁을 레포" 를 분리한다.** 종전에는 추적 대상이
    `products/*/showcase.md` 에 묶여 있었는데, 그 파일은 공개 표시용이라 둘을 따로
    정할 수 없었다 — 사이트에 안 보이지만 커밋은 세고 싶은 레포를 표현할 방법이 없다.

    삭제 대신 `enabled` 를 끈다. 지우면 과거 조사 이력의 참조가 끊긴다(S-4 3항).
    """

    __tablename__ = "tracked_repos"
    __table_args__ = (
        CheckConstraint(_in("type", TRACKED_REPO_TYPES), name="ck_tracked_repos_type"),
        CheckConstraint(
            _in("account", TRACKED_REPO_ACCOUNTS), name="ck_tracked_repos_account"
        ),
        # `type=company` 면 `detail` 이 있어야 하고 `studio` 면 없어야 한다.
        # 앱이 아니라 DB 가 강제한다 — 이 불변이 깨지면 career 귀속이 조용히 틀린다.
        CheckConstraint(
            "(type = 'company' AND detail IS NOT NULL)"
            " OR (type = 'studio' AND detail IS NULL)",
            name="ck_tracked_repos_detail",
        ),
        Index("uq_tracked_repos_slug", "slug", unique=True),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    #: `owner/name`. 클론 URL 과 조사 결과의 키가 된다.
    slug: Mapped[str] = mapped_column(String(160), nullable=False)
    type: Mapped[str] = mapped_column(String(16), nullable=False)
    #: career 파일 stem. `company` 일 때만. 실재하는 문서를 가리켜야 한다.
    detail: Mapped[str | None] = mapped_column(String(80))
    account: Mapped[str] = mapped_column(String(16), nullable=False, default="personal")
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    #: `{glob, area}` 목록. 비면 전역 기본 규칙이 적용된다.
    path_rules: Mapped[list[Any] | None] = mapped_column(JSONB)
    last_fetched_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    #: 마지막 실패 사유. 성공하면 비운다 — 남아 있으면 지금 막혀 있다는 뜻이다.
    last_error: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

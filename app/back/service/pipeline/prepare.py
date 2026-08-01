"""자동 준비 — 수집 + 요약 (KDEV-WORK-014 P2 / KDEV-SPEC-007 §3 S-3).

준비는 **게이트가 아니다.** 승인 대상이 아니고, 실패하면 재시도한다.
여기서 만드는 요약은 노트 본문이 아니라 **route 판단의 근거**다 — 무엇을 만들지
정하기 전에 노트 전문을 쓰면, 폐기할 자료의 노트까지 쓰게 된다.

세 가지 원칙이 이 모듈의 모양을 결정한다.

1. **메모는 원문을 대체할 수 있다.** 수집이 막혀도(자막 없음·봇 차단) 사람이 메모를
   남겼으면 준비가 성립한다. 수집 실패가 항목을 죽이지 않는다.
2. **재시도는 덮어쓰지 않는다.** 새 준비 버전과 새 실행 행을 만들고 이전 실패를
   감사 이력으로 남긴다. 실패를 지우면 "왜 이렇게 됐는지"를 잃는다.
3. **요약을 기다리지 않는다** (KDEV-WORK-016 P2). 제출하고 돌아온다. 수집 결과는
   `running` 준비 버전에 이미 저장돼 있어, back 이 재시작해도 수확할 재료가 남는다.

   수집(`fetch`)은 여전히 제출 경로 안에서 돈다. AI 가 아니라 HTTP 이고 상한이
   15초라, 실행기 큐에 넣을 대상이 아니다.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Awaitable, Callable, Protocol

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import AITask, ItemPreparation, QueueItem

from .executor import Execution

logger = logging.getLogger("kknaks-back.pipeline.prepare")

#: 준비를 시작할 수 있는 항목 상태. 이미 검토 중이거나 발행된 항목을 다시 준비하면
#: 사람이 보고 있던 근거가 발밑에서 바뀐다.
PREPARABLE_STATUSES = ("received", "prepare_failed")


class Summarizer(Protocol):
    """요약 실행기 — 게이트 스테이지와 같이 **제출과 수확이 나뉘어 있다**.

    `parse` 는 완료된 원문에서 요약 본문을 꺼낸다. 비어 있으면 예외 — 빈 요약을
    성공으로 넘기면 route 게이트가 근거 없이 판단한다.
    """

    async def submit(self, *, material: Any, note: str | None) -> str: ...

    async def poll(self, task_id: str) -> Execution: ...

    #: 실행 완료까지 블록한다 — 워커가 깨워 주므로 폴링이 아니다. 선언이 빠져 있었는데
    #: `driver` 가 계속 부르고 있었다(KDEV-WORK-017 P2 에서 실사용에 맞춰 채웠다).
    async def wait(self, task_id: str) -> Any: ...

    def parse(self, raw: str) -> str: ...


#: 원문 수집기. 실패는 예외.
Fetcher = Callable[[str], Awaitable[Any]]


@dataclass(frozen=True)
class StageSubmission:
    """auto 스테이지가 제출을 마치고 돌려주는 것 (KDEV-WORK-017 P2).

    `task_refs` 가 비어 있어도 정상이다 — `collect` 처럼 **LLM 을 부르지 않는**
    스테이지가 있다. 그 경우 기다릴 것이 없으니 곧바로 수확된다.

    `investigate` 는 반대로 레포마다 하나씩 **N 건**을 낸다. 제출 건수를 0·1·N 으로
    함께 다루는 것이 이 계약의 요점이다 — 종전 준비부는 1 만 가정했다.
    """

    task_refs: list[str]
    #: 제출 시점에 이미 확정된 payload 조각(수집 원문 등). 실행 결과가 아니다.
    payload: dict[str, Any]
    #: 제출 전에 막힌 경우. 채워지면 준비가 실패로 닫힌다.
    error_code: str | None = None
    error_message: str | None = None


class AutoStage(Protocol):
    """auto 스테이지 실행기 — 게이트가 아니라 `ItemPreparation` 을 남긴다.

    게이트 실행기(`gates.StageRunner`)와 계약이 다르다. 승인 리비전을 만들지 않고,
    사람의 검토를 받지 않으며, 실패하면 재시도한다.

    **`stages` 가 이 프로토콜의 핵심이다.** 실행기 하나가 정의상 스테이지 **여럿을
    덮을 수 있다.** 유튜브의 수집+요약이 그렇다 — 정의에는 `collect`·`summarize` 로
    둘이지만 코드에서는 한 덩어리이고, 그걸 굳이 쪼개면 얻는 것 없이 회귀면만 넓어진다.
    잔디는 셋을 각각 따로 덮는다.
    """

    #: 이 실행기가 덮는 정의상 스테이지 이름들. 성공하면 전부 완료로 기록된다.
    stages: tuple[str, ...]

    async def submit(self, *, item: QueueItem, prior: dict[str, Any]) -> StageSubmission: ...

    async def wait(self, task_ref: str) -> Any: ...

    async def poll(self, task_ref: str) -> Execution: ...

    def parse(
        self, results: list[str], *, item: QueueItem, prior: dict[str, Any]
    ) -> dict[str, Any]:
        """실행 결과들 → 이 스테이지가 payload 에 더할 조각.

        `results` 는 제출 순서대로다. 비어 있으면 LLM 을 부르지 않은 스테이지다.
        """
        ...


async def completed_auto_stages(db: AsyncSession, item_id: int) -> set[str]:
    """이 항목에서 **이미 끝난** auto 스테이지 이름들.

    성공한 준비 버전에만 기록된다 — 실패한 버전은 재시도 대상이라 완료로 세지 않는다.
    """
    rows = (
        await db.scalars(
            select(ItemPreparation.payload).where(
                ItemPreparation.item_id == item_id,
                ItemPreparation.status == "succeeded",
            )
        )
    ).all()
    done: set[str] = set()
    for payload in rows:
        for name in (payload or {}).get("stages") or []:
            done.add(str(name))
    return done


def next_auto_stage(pipeline, completed: set[str]) -> str | None:
    """정의 순서에서 아직 안 끝난 첫 auto 스테이지. 없으면 `None`(= 게이트 차례).

    **정의가 순서의 SoT다.** 종전에는 "수집 1회 + 요약 1회" 가 코드에 굳어 있어
    `Stage(..., "auto")` 선언을 아무도 읽지 않았다(WORK-017 P2).
    """
    if pipeline is None:
        return None
    for stage in pipeline.auto_stages():
        if stage.name not in completed:
            return stage.name
    return None


@dataclass(frozen=True)
class PrepareResult:
    item_id: int
    status: str  # preparing · in_review · prepare_failed · not_allowed
    preparation_id: int | None = None
    version: int | None = None
    error_code: str | None = None
    error_message: str | None = None

    @property
    def ok(self) -> bool:
        """준비가 **끝났는가.** 제출만 된 상태는 아직 아니다."""
        return self.status == "in_review"

    @property
    def running(self) -> bool:
        """요약이 실행기 큐에 있다 — 화면이 폴링해 수확한다."""
        return self.status == "preparing"


def _now() -> datetime:
    return datetime.now(timezone.utc)


async def _next_version(db: AsyncSession, item_id: int) -> int:
    current = await db.scalar(
        select(func.max(ItemPreparation.version)).where(ItemPreparation.item_id == item_id)
    )
    return (current or 0) + 1


async def _last_failed_task(db: AsyncSession, item_id: int) -> AITask | None:
    return await db.scalar(
        select(AITask)
        .where(AITask.item_id == item_id, AITask.kind == "summarize", AITask.status == "failed")
        .order_by(AITask.id.desc())
        .limit(1)
    )


def _material_dict(material: Any) -> dict[str, Any] | None:
    if material is None:
        return None
    if isinstance(material, dict):
        return material
    to_dict = getattr(material, "to_dict", None)
    return to_dict() if callable(to_dict) else {"content": str(material)}


async def submit_preparation(
    db: AsyncSession,
    item_id: int,
    *,
    fetch: Fetcher,
    summarize: Summarizer,
) -> PrepareResult:
    """항목 하나의 준비를 **시작한다.** 커밋은 호출자가 한다.

    수집까지 하고 요약은 제출만 한 뒤 돌아온다. 반환값으로 결과를 알린다 —
    준비 실패는 **예외가 아니라 상태**다. 사람이 메모를 보태 재시도하는 정상
    경로의 일부이기 때문이다.
    """
    item = await db.get(QueueItem, item_id)
    if item is None or item.deleted_at is not None:
        return PrepareResult(item_id=item_id, status="not_allowed", error_code="ITEM_NOT_FOUND")
    if item.status not in PREPARABLE_STATUSES:
        return PrepareResult(
            item_id=item_id,
            status="not_allowed",
            error_code="PREPARE_RETRY_NOT_ALLOWED",
            error_message=f"상태가 {item.status} 라 준비할 수 없다",
        )

    retry_of = await _last_failed_task(db, item_id) if item.status == "prepare_failed" else None
    item.status = "preparing"
    await db.flush()

    # --- 수집 -------------------------------------------------------------
    material: dict[str, Any] | None = None
    collect_error: str | None = None
    if item.source_url:
        try:
            # **여기서 한 번만 dict 로 만든다.** 수집기는 dataclass 를 돌려주는데,
            # 그걸 그대로 아래로 흘리면 요약 프롬프트를 조립할 때
            # `Object of type SourceMaterial is not JSON serializable` 로 터진다.
            material = _material_dict(await fetch(item.source_url))
        except Exception as exc:  # noqa: BLE001 — 수집 실패는 정상 분기다
            collect_error = f"{type(exc).__name__}: {exc}"[:500]
            logger.info("수집 실패 item=%s: %s", item_id, collect_error)

    note = (item.note or "").strip()
    if material is None and not note:
        # 원문도 못 받고 메모도 없으면 요약할 것이 없다. AI 를 부르지 않는다.
        return await _fail(
            db,
            item,
            version=await _next_version(db, item_id),
            error_code="NO_SOURCE_MATERIAL",
            error_message=collect_error or "원문 수집에 실패했고 메모도 없다",
            payload={"collect_error": collect_error},
        )

    # --- 요약 제출 ---------------------------------------------------------
    task = AITask(
        item_id=item_id,
        kind="summarize",
        status="running",
        retry_of_task_id=retry_of.id if retry_of else None,
    )
    db.add(task)
    await db.flush()

    try:
        task_id = await summarize.submit(material=material, note=note or None)
    except Exception as exc:  # noqa: BLE001
        task.status = "failed"
        task.error_code = type(exc).__name__
        task.error_message = str(exc)[:1000]
        task.finished_at = _now()
        await db.flush()
        return await _fail(
            db,
            item,
            version=await _next_version(db, item_id),
            error_code="SUMMARIZE_SUBMIT_FAILED",
            error_message=str(exc)[:500],
            payload={"collect_error": collect_error},
            ai_task_id=task.id,
        )

    task.external_task_ref = str(task_id)

    version = await _next_version(db, item_id)
    preparation = ItemPreparation(
        item_id=item_id,
        version=version,
        status="running",
        ai_task_id=task.id,
        payload={
            # 이 준비가 덮은 정의상 스테이지들(WORK-017 P2). 수집과 요약은 코드에서
            # 한 덩어리지만 정의에서는 둘이고, 레일은 정의 기준으로 "다음이 남았나"를
            # 판단한다. 둘 다 여기 적히므로 유튜브는 준비 한 번으로 auto 가 끝난다.
            "stages": ["collect", "summarize"],
            "source": material,
            "note": note or None,
            # 수집이 막혀 메모로 대체했는지는 route 판단의 재료다 —
            # 근거가 원문인지 사람 기억인지에 따라 신뢰도가 다르다.
            "material_source": "fetched" if material is not None else "note",
            "collect_error": collect_error,
            "summary": None,
        },
    )
    db.add(preparation)
    await db.flush()

    return PrepareResult(
        item_id=item_id,
        status="preparing",
        preparation_id=preparation.id,
        version=version,
    )


async def harvest_preparation(
    db: AsyncSession, item: QueueItem, *, summarize: Summarizer
) -> PrepareResult:
    """제출해 둔 요약을 확인해 끝났으면 준비를 닫는다. **멱등이다.**

    게이트 수확과 같은 규율이다 — `running` 행을 `FOR UPDATE` 로 잡아, 폴링이
    겹쳐도 요약이 두 번 채워지지 않는다.
    """
    if item.status != "preparing":
        return PrepareResult(item_id=item.id, status=item.status)

    preparation = await db.scalar(
        select(ItemPreparation)
        .where(ItemPreparation.item_id == item.id, ItemPreparation.status == "running")
        .order_by(ItemPreparation.version.desc())
        .limit(1)
        .with_for_update()
    )
    if preparation is None:
        # 준비 중인데 진행 행이 없다. 제출이 커밋 전에 끊긴 흔적이므로
        # 사람이 재시도할 수 있게 실패로 닫는다.
        logger.warning("항목 %s 가 preparing 인데 running 준비가 없다", item.id)
        item.status = "prepare_failed"
        await db.flush()
        return PrepareResult(
            item_id=item.id, status="prepare_failed", error_code="PREPARATION_MISSING"
        )

    task = await db.get(AITask, preparation.ai_task_id) if preparation.ai_task_id else None
    if task is None or not task.external_task_ref:
        return await _close_failed(
            db,
            item,
            preparation,
            task,
            error_code="TASK_REF_MISSING",
            error_message="제출 기록에 실행기 작업 참조가 없다",
        )

    execution = await summarize.poll(task.external_task_ref)
    if execution.running:
        return PrepareResult(
            item_id=item.id,
            status="preparing",
            preparation_id=preparation.id,
            version=preparation.version,
        )
    if execution.status == "failed":
        return await _close_failed(
            db,
            item,
            preparation,
            task,
            error_code=execution.error_code or "SUMMARIZE_FAILED",
            error_message=execution.error_message or "요약 실행이 실패했다",
        )

    try:
        summary = summarize.parse(execution.result or "")
    except Exception as exc:  # noqa: BLE001
        return await _close_failed(
            db,
            item,
            preparation,
            task,
            error_code="SUMMARIZE_FAILED",
            error_message=str(exc)[:500],
        )

    task.status = "succeeded"
    task.session_ref = execution.session_ref
    task.finished_at = _now()

    # **새 dict 로 갈아 끼운다.** JSONB 는 제자리 수정으로는 변경을 감지하지 못해
    # 요약이 조용히 저장되지 않는다.
    preparation.payload = {**(preparation.payload or {}), "summary": summary}
    preparation.status = "succeeded"
    item.status = "in_review"
    await db.flush()

    return PrepareResult(
        item_id=item.id,
        status="in_review",
        preparation_id=preparation.id,
        version=preparation.version,
    )


async def _close_failed(
    db: AsyncSession,
    item: QueueItem,
    preparation: ItemPreparation,
    task: AITask | None,
    *,
    error_code: str,
    error_message: str,
) -> PrepareResult:
    """진행 중이던 준비를 실패로 닫는다 — 행을 새로 만들지 않는다.

    이미 있는 버전이 그 실행의 기록이다. 또 만들면 같은 시도가 두 줄이 된다.
    """
    if task is not None and task.status == "running":
        task.status = "failed"
        task.error_code = error_code
        task.error_message = error_message[:1000]
        task.finished_at = _now()
    preparation.payload = {
        **(preparation.payload or {}),
        "error_code": error_code,
        "error_message": error_message,
    }
    preparation.status = "failed"
    item.status = "prepare_failed"
    await db.flush()
    return PrepareResult(
        item_id=item.id,
        status="prepare_failed",
        preparation_id=preparation.id,
        version=preparation.version,
        error_code=error_code,
        error_message=error_message,
    )


async def _fail(
    db: AsyncSession,
    item: QueueItem,
    *,
    version: int,
    error_code: str,
    error_message: str,
    payload: dict[str, Any],
    ai_task_id: int | None = None,
) -> PrepareResult:
    """제출 전에 막힌 경우 — 실패도 **버전으로 남긴다.**

    무엇이 막혔는지 상세 화면이 보여줘야 한다.
    """
    preparation = ItemPreparation(
        item_id=item.id,
        version=version,
        status="failed",
        ai_task_id=ai_task_id,
        payload={**payload, "error_code": error_code, "error_message": error_message},
    )
    db.add(preparation)
    item.status = "prepare_failed"
    await db.flush()
    return PrepareResult(
        item_id=item.id,
        status="prepare_failed",
        preparation_id=preparation.id,
        version=version,
        error_code=error_code,
        error_message=error_message,
    )

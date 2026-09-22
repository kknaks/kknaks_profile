"""제출과 소비자 기동의 배선.

라우터는 **저장이 끝난 뒤** `start_turn` 하나만 부른다. 순서가 곧 계약이다:

1. 제출 한 벌을 조립해 `ontology` 큐에 넣는다.
2. 제출이 성공하면 **그 태스크 전용 소비자**를 백그라운드로 띄운다.
3. 실패하면 답변을 `failed` 로 마감하고 소비자는 뜨지 않는다.

## 왜 저장 뒤인가

태스크가 저장보다 먼저 큐에 들어가면 워커가 즉시 집어 소비자가 **아직 보이지 않는
메시지**를 찾다가 실패한다. 접수(201)는 이미 확정된 사실이므로 제출 실패는 응답을
뒤집지 않고 답변 상태로만 표현된다.

## 백그라운드 태스크 참조 보관

`asyncio.create_task` 의 반환을 붙들지 않으면 GC 가 가져가 **조용히 사라진다.**
모듈 레벨 집합에 담고 끝나면 뺀다.

**ADR-04** — LLM SDK 를 직접 import 하지 않는다. 실행은 open-kknaks 경유이고
그 import 도 lazy 라 의존 미설치 환경(단위 테스트)에서 이 모듈이 그대로 로드된다.
"""

from __future__ import annotations

import asyncio
import logging

from config import settings

from . import store
from .consumer import run_consumer
from .prompt import build_prompt, build_repair_prompt
from .submission import SubmissionPlan, build_submission

logger = logging.getLogger(__name__)

_background_tasks: set[asyncio.Task] = set()


def _track(task: asyncio.Task) -> None:
    _background_tasks.add(task)
    task.add_done_callback(_background_tasks.discard)


def build_plan_for(conn, message_id: str, question: str) -> SubmissionPlan | None:
    """이 답변 한 건의 제출 계획. 이미 끝난 메시지면 None.

    **테스트가 여기서 닫힌다** — 큐 없이 조립만 검증할 수 있다.
    """
    row = store.get_message(conn, message_id)
    if row is None or row["status"] != store.STATUS_PENDING:
        return None
    return build_submission(
        prompt=build_prompt(question),
        resume_session_id=store.get_session_id(conn, row["conversation_id"]),
        conversation_id=row["conversation_id"],
        message_id=message_id,
    )


async def _submit(plan: SubmissionPlan) -> str:
    """open-kknaks 제출 — lazy import 로 의존 미설치 환경을 보호한다."""
    from open_kknaks import AgentClient, RedisBroker

    broker = RedisBroker(url=settings.redis_url, namespace=settings.ai_namespace)
    await broker.connect()
    try:
        return await AgentClient(broker=broker).submit(
            plan.prompt,
            queue=plan.queue,
            provider=plan.provider,
            # model=None 이면 어댑터가 `--model` 자체를 안 붙인다 — CLI 기본이 쓰인다
            model=plan.model,
            options=plan.options,
            provider_options=plan.provider_options,
            metadata=plan.metadata,
        )
    finally:
        await broker.close()


async def resubmit_for_repair(
    *, message_id: str, conversation_id: str, violations: str
) -> str | None:
    """스키마·근거 위반 뒤 **같은 세션으로** 다시 제출한다 (SPEC-005 OQ-5).

    같은 텍스트를 다시 파싱하는 것은 결정적이라 의미가 없다 — 재시도는 **재제출**이어야
    한다. codex 세션을 resume 해 직전 맥락(무엇을 물었고 어떤 도구를 불렀는지)을 그대로
    들고 가고, 위반 목록만 새 발화로 얹는다.

    세션이 아직 없으면(첫 이벤트 전에 죽었다) 재시도할 맥락이 없으므로 None 을 돌려준다.
    """
    with store.connect() as conn:
        session_id = store.get_session_id(conn, conversation_id)
    if not session_id:
        logger.warning("chat: message %s 세션이 없어 재시도하지 않는다", message_id)
        return None

    plan = build_submission(
        prompt=build_repair_prompt(violations),
        resume_session_id=session_id,
        conversation_id=conversation_id,
        message_id=message_id,
    )
    try:
        task_id = await _submit(plan)
    except Exception:  # noqa: BLE001 — 재제출 실패도 답변 상태로만 표현한다
        logger.exception("chat 재시도 제출 실패 message=%s", message_id)
        return None
    with store.connect() as conn:
        store.update_message(conn, message_id, {"task_id": task_id})
    return task_id


def spawn_consumer(*, message_id: str, conversation_id: str, task_id: str) -> None:
    task = asyncio.create_task(
        run_consumer(message_id=message_id, conversation_id=conversation_id, task_id=task_id))
    _track(task)


async def start_turn(*, message_id: str, conversation_id: str, question: str) -> None:
    """제출하고 소비자를 띄운다. 예외를 밖으로 내보내지 않는다."""
    with store.connect() as conn:
        plan = build_plan_for(conn, message_id, question)
    if plan is None:
        return
    try:
        task_id = await _submit(plan)
    except Exception:  # noqa: BLE001 — 제출 실패는 답변 상태로만 표현한다
        logger.exception("chat 제출 실패 message=%s", message_id)
        with store.connect() as conn:
            store.update_message(conn, message_id, {
                "status": store.STATUS_FAILED, "error_code": store.CODE_AI_FAILED})
        return
    with store.connect() as conn:
        store.update_message(conn, message_id, {"task_id": task_id})
    spawn_consumer(message_id=message_id, conversation_id=conversation_id, task_id=task_id)

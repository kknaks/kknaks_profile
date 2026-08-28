"""제출과 소비자 기동의 배선 (SPEC-017 §4 Flow).

라우터는 **요청 트랜잭션이 커밋된 뒤** `start_turn(message_id)` 하나만 부른다
(`BackgroundTasks` — FastAPI 는 `get_db` 의 commit 을 background task 보다 먼저 끝낸다).
그 안에서 일어나는 일은 셋이다:

1. turn 토큰을 발급하고 제출 한 벌을 조립해 `chat` 큐에 넣는다.
2. 제출이 성공하면 **그 태스크 전용 소비자**를 백그라운드로 띄운다.
3. 실패하면 답변을 `failed` 로 마감하고 소비자는 뜨지 않는다.

## 왜 커밋 뒤인가

태스크가 커밋보다 먼저 큐에 들어가면 워커가 즉시 집어 소비자가 **아직 보이지 않는
메시지**를 찾다가 실패한다. 접수(201)는 이미 확정된 사실이므로 제출 실패는 응답을
뒤집지 않고 답변 상태로만 표현된다.

## 백그라운드 task 참조 보관

`asyncio.create_task` 의 반환을 붙들지 않으면 GC 가 가져가 **조용히 사라진다**.
그래서 모듈 레벨 집합에 담고 끝나면 뺀다.
"""

from __future__ import annotations

import asyncio
import logging

from core.db import SessionLocal
from models.chat import ROLE_USER, STATUS_FAILED, STATUS_PENDING
from repository.chat_repo import chat_repository
from service.chat.consumer import CODE_AI_FAILED, run_turn_consumer
from service.chat.prompt import (
    build_question_block,
    build_recent_context,
    build_system_prompt,
)
from service.chat.submission import SubmissionPlan, build_submission
from service.chat.turn_token import turn_token_service

logger = logging.getLogger(__name__)

_background_tasks: set[asyncio.Task] = set()


def _track(task: asyncio.Task) -> None:
    _background_tasks.add(task)
    task.add_done_callback(_background_tasks.discard)


async def _agent_submit(plan: SubmissionPlan) -> str:
    """open-kknaks 제출 — lazy import 로 의존 미설치 환경(테스트)을 보호한다."""
    from open_kknaks import AgentClient, RedisBroker

    from config import get_settings

    settings = get_settings()
    broker = RedisBroker(url=settings.redis_url, namespace=settings.ai_namespace)
    await broker.connect()
    try:
        return await AgentClient(broker=broker).submit(
            plan.prompt,
            queue=plan.queue,
            provider=plan.provider,
            # model=None 이면 어댑터가 `--model` 자체를 안 붙인다 — CLI 기본이 쓰인다.
            model=plan.model,
            options=plan.options,
            provider_options=plan.provider_options,
            metadata=plan.metadata,
        )
    finally:
        await broker.close()


async def build_plan_for(db, message_id: int) -> SubmissionPlan | None:
    """이 답변 한 건의 제출 계획. 이미 끝난 메시지면 None.

    **테스트가 여기서 닫힌다** — 큐 없이 조립만 검증할 수 있다.
    """
    message = await chat_repository.get_message(db, message_id)
    if message is None or message.status != STATUS_PENDING:
        return None
    conversation = await chat_repository.get_conversation(db, message.conversation_id)
    if conversation is None:
        return None

    # 이번 턴의 질문과 「지난 기록」을 가른다. 자르지 않으면 방금 한 질문이 지난
    # 기록에도 한 번 더 실려 프롬프트에 같은 문장이 두 번 들어간다.
    history = await chat_repository.list_messages(db, conversation.id)
    prior = [m for m in history if m.id < message.id]
    question = ""
    for index in range(len(prior) - 1, -1, -1):
        if prior[index].role == ROLE_USER and prior[index].content.strip():
            question = prior[index].content
            prior = prior[:index]   # 그 앞까지가 지난 기록이다
            break

    from repository.chat_tool_repo import chat_tool_repository

    profile = await chat_tool_repository.get_profile(db)
    careers = await chat_tool_repository.list_careers(db)
    career_lines = [
        f"{c.title} — {c.subtitle}" if c.subtitle else c.title for c in careers
    ]

    resume_session_id = conversation.ai_session_id
    # 세션이 살아 있으면 codex 가 문맥을 갖고 있다 — 같은 것을 두 번 싣지 않는다(D2).
    recent = "" if resume_session_id else build_recent_context(prior)

    token = await turn_token_service.issue(db, message.id)
    return build_submission(
        system_prompt=build_system_prompt(profile, career_lines),
        question_block=build_question_block(question),
        mcp_token=token,
        recent_context=recent,
        resume_session_id=resume_session_id,
        conversation_id=conversation.id,
        message_id=message.id,
    )


async def _log_skip(db, message_id: int) -> None:
    """제출을 건너뛴 **이유가 로그에서 보이게** 한다.

    「제출 대상이 아니다」는 두 가지 아주 다른 상황을 한 문장으로 덮고 있었다:

    - **정상**: 그 사이 답변이 마감됐다(다른 경로가 이미 처리). 그냥 건너뛰면 된다.
    - **이상**: row 가 안 보이거나, pending 인데 계획을 못 세웠다. 이때 그 답변은
      **영구 pending** 이 된다 — 폴링에 재큐잉 경로가 없어 방문자가 컴포저 잠금에
      갇힌다. 2026-08-28 실측 사고(커밋 전 큐잉)가 정확히 이 갈래였는데 info 한 줄로
      묻혀 있었다.

    `start_turn` 은 **라우터가 방금 만든 id** 로만 불린다. 그래서 「못 찾았다」는 그
    자체로 정상 경로가 아니다.
    """
    message = await chat_repository.get_message(db, message_id)
    if message is None:
        logger.warning(
            "chat: message %s 를 찾지 못해 제출을 건너뛴다 — 라우터가 방금 만든 id 라"
            " 정상 경로가 아니다(커밋 전 큐잉 의심). 이 답변은 영구 pending 으로 남는다",
            message_id,
        )
    elif message.status == STATUS_PENDING:
        logger.warning(
            "chat: message %s 가 pending 인데 제출 계획을 못 세웠다(대화 행이 없다)"
            " — 이 답변은 영구 pending 으로 남는다",
            message_id,
        )
    else:
        logger.info(
            "chat: message %s 는 제출 대상이 아니다(status=%s) — 건너뛴다",
            message_id,
            message.status,
        )


async def start_turn(message_id: int, *, submitter=None) -> str | None:
    """제출하고 소비자를 띄운다. 반환 = task_id(제출 실패면 None).

    `submitter` 주입은 테스트용 seam 이다 — 실제 큐 없이 이 배선만 검증할 수 있다.
    """
    submit = submitter or _agent_submit
    try:
        async with SessionLocal() as db:
            plan = await build_plan_for(db, message_id)
            if plan is None:
                await db.commit()
                await _log_skip(db, message_id)
                return None
            # 토큰 발급이 커밋돼야 MCP 가 그 토큰을 검증할 수 있다 — 제출보다 먼저.
            await db.commit()

        task_id = await submit(plan)

        async with SessionLocal() as db:
            await chat_repository.update_message(db, message_id, {"task_id": task_id})
            await db.commit()
    except Exception:  # noqa: BLE001 — 제출 실패가 접수 응답을 뒤집지 않는다
        # ⚠ **`plan` 을 이 문자열에 넣지 마라.** `plan.provider_options["config"]` 의
        #   `-c` 목록에는 MCP Bearer 원문이 들어 있다. 여기는 message_id 만 찍는다.
        logger.exception("chat: message %s 제출 실패 — failed 로 마감", message_id)
        await _fail(message_id)
        return None

    # 같은 이유로 여기도 토큰이 닿는 값(plan.prompt · provider_options)을 싣지 않는다.
    logger.info(
        "chat: message %s 제출 완료 task=%s queue=%s model=%s",
        message_id,
        task_id,
        plan.queue,
        plan.model,
    )
    _track(asyncio.create_task(run_turn_consumer(message_id=message_id, task_id=task_id)))
    return task_id


def spawn_consumer(*, message_id: int, task_id: str) -> None:
    """복구 경로(기동 스윕)가 쓰는 진입점 — 제출 없이 소비자만 붙인다."""
    _track(
        asyncio.create_task(
            run_turn_consumer(message_id=message_id, task_id=task_id, replay=True)
        )
    )


async def _fail(message_id: int) -> None:
    async with SessionLocal() as db:
        await chat_repository.update_message(
            db,
            message_id,
            {
                "status": STATUS_FAILED,
                "error_code": CODE_AI_FAILED,
                "turn_token_hash": None,
                "turn_token_expires_at": None,
            },
        )
        await db.commit()

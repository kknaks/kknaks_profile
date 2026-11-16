"""이벤트 폴딩 — open-kknaks 스트림을 메시지 행으로 접는다.

`pending` 동안 화면이 볼 것이 자라야 한다(SPEC-003 AC-8). 스피너만 도는 구간을 만들지
않으려고 부분 텍스트와 도구 단계를 이벤트마다 적재하고, 폴링이 그것을 읽는다.

## 멱등이 요구사항이다

**같은 이벤트를 두 번 받아도 결과가 같아야 한다.** 중복 수신은 예외가 아니라 정상
경로다(재부착 재생). 짝짓기 키는 `tool_use_id` 이고, 같은 id 가 다시 오면 새 단계를
만들지 않고 그 자리를 갱신한다.

## 스키마 위반 재시도는 turn 예산 안에서 돈다

`ai_schema_retry` 만큼 **재제출**한다(SPEC-005 OQ-5). 재시도까지 포함한 전체가
`run_consumer` 의 `asyncio.wait_for(ai_timeout_sec)` 안에 있다 — 사용자가 기다리는
시간을 재시도가 두 배로 늘리지 않게 하려는 것이다(SPEC-003 「180초 초과 → failed」는
turn 전체의 상한이다). 첫 시도가 예산을 다 쓰면 재시도는 `AI_TIMEOUT` 으로 끝난다.

## steps 의 기록 주체는 백엔드다

모든 도구 호출이 도구 서버를 지나므로 AI 의 신고 없이 서버가 잰다.
`args_summary` 도 서버가 만들고 길이를 제한한다 — 인자 원문을 그대로 실으면
필터 값이 응답으로 흘러 나간다(SPEC-003 Data Contract).
"""

from __future__ import annotations

import asyncio
import contextlib
import datetime
import logging
import time
from typing import Any

from config import settings

from . import store
from .answer import AnswerSchemaError, extract_answer_object, validate

logger = logging.getLogger(__name__)

#: 소비 중인 태스크 — 같은 태스크에 소비자를 두 번 띄우지 않는다
_running: set[str] = set()

#: `args_summary` 길이 상한. 인자 원문을 그대로 싣지 않는다.
_ARGS_SUMMARY_MAX = 120


def _now() -> str:
    return datetime.datetime.now(datetime.UTC).isoformat(timespec="seconds")


def _unwrap_arguments(tool_input: Any) -> dict:
    """codex 어댑터는 실제 인자를 `tool_input["arguments"]` 안에 넣는다.

    바깥 껍데기는 `{id, type, server, tool, arguments, result, error, status}` 이고
    우리가 볼 것은 `arguments` 뿐이다(2.1.2 실측). 껍데기가 없으면 그대로 쓴다 —
    어댑터가 모양을 바꿔도 요약이 통째로 죽지 않게.
    """
    if not isinstance(tool_input, dict):
        return {}
    inner = tool_input.get("arguments")
    if isinstance(inner, dict):
        return inner
    return tool_input


def summarize_args(tool_name: str, tool_input: Any) -> str:
    """서버가 만드는 인자 요약 — 값이 아니라 **무엇을 물었는지**만 남긴다.

    필터 값·기간 원문을 그대로 실으면 응답으로 새어 나간다. 키와 지표명까지가 상한이다.
    """
    tool_input = _unwrap_arguments(tool_input)
    if not tool_input:
        return tool_name
    parts: list[str] = []
    metrics = tool_input.get("metrics")
    if isinstance(metrics, list) and metrics:
        parts.append(" · ".join(str(m) for m in metrics[:4]))
    for key in ("grain", "layer", "table", "node", "direction", "term"):
        value = tool_input.get(key)
        if isinstance(value, str) and value:
            parts.append(value)
    if isinstance(tool_input.get("filters"), list):
        # 값은 싣지 않는다 — 개수만
        parts.append(f"필터 {len(tool_input['filters'])}개")
    summary = " · ".join(parts) if parts else tool_name
    return summary[:_ARGS_SUMMARY_MAX]


class TurnFolder:
    """메시지 한 건의 폴딩 상태. 이벤트를 받아 행으로 접는다."""

    def __init__(self, message_id: str, conversation_id: str) -> None:
        self.message_id = message_id
        self.conversation_id = conversation_id
        self._text: list[str] = []
        self._steps: list[dict] = []
        self._step_index: dict[str, int] = {}
        self._started: dict[str, float] = {}

    # --- 이벤트 ---

    def on_init(self, conn, session_id: str | None) -> None:
        if session_id:
            store.set_session_id(conn, self.conversation_id, session_id)

    def on_text(self, conn, delta: str) -> None:
        """부분 텍스트 누적. `text` 는 델타라 이어 붙인다."""
        if not delta:
            return
        self._text.append(delta)
        store.update_message(conn, self.message_id, {"content": "".join(self._text)})

    def on_tool_use(self, conn, *, tool_use_id: str | None, tool_name: str,
                    tool_input: Any) -> None:
        if not tool_use_id:
            return
        step = {
            "tool": tool_name,
            "args_summary": summarize_args(tool_name, tool_input),
            "duration_ms": None,
            "called_at": _now(),
        }
        self._upsert(tool_use_id, step)
        self._started.setdefault(tool_use_id, time.monotonic())
        self._flush(conn)

    def on_tool_result(self, conn, *, tool_use_id: str | None, result: Any,
                       is_error: Any) -> None:
        if not tool_use_id:
            return
        idx = self._step_index.get(tool_use_id)
        if idx is None:
            # result 가 use 보다 먼저 온 경우 — 자리를 만들고 채운다
            self._upsert(tool_use_id, {"tool": "", "args_summary": "",
                                       "duration_ms": None, "called_at": _now()})
            idx = self._step_index[tool_use_id]
        started = self._started.get(tool_use_id)
        if started is not None:
            self._steps[idx]["duration_ms"] = int((time.monotonic() - started) * 1000)
        self._steps[idx]["is_error"] = bool(is_error)
        self._flush(conn)

    def _upsert(self, tool_use_id: str, step: dict) -> None:
        """`tool_use_id` 멱등 — 같은 id 가 다시 오면 자리를 갱신한다."""
        idx = self._step_index.get(tool_use_id)
        if idx is None:
            self._step_index[tool_use_id] = len(self._steps)
            self._steps.append(step)
            return
        merged = {**self._steps[idx]}
        for key, value in step.items():
            if value not in (None, ""):
                merged[key] = value
        self._steps[idx] = merged

    def _flush(self, conn) -> None:
        store.update_message(conn, self.message_id, {"steps": list(self._steps)})

    # --- 마감 ---

    @property
    def partial_text(self) -> str:
        return "".join(self._text)

    def begin_retry(self, conn) -> None:
        """재제출 직전 상태를 고른다 — 본문만 비우고 **단계는 남긴다**.

        새 답변이 통째로 다시 오므로 이전 본문에 이어 붙이면 두 답변이 섞인다.
        반대로 도구 호출 기록은 **실제로 일어난 일**이라 지우면 `steps` 가 사실과 어긋난다.
        """
        self._text.clear()
        store.update_message(conn, self.message_id, {"content": ""})

    def finalize_done(self, conn, ontology_conn, result_text: str | None) -> dict:
        """최종 result 로 본문을 교체하고 답변 객체를 검증한다.

        검증 실패는 예외로 올린다 — 소비자가 `ai_schema_retry` 만큼 재제출하고,
        그래도 안 되면 `failed` + `AI_FAILED` 로 마감한다(SPEC-005 OQ-5).
        """
        text = result_text or self.partial_text
        obj = extract_answer_object(text)
        validate(ontology_conn, obj)
        store.update_message(conn, self.message_id, {
            "status": store.STATUS_DONE,
            "error_code": None,
            "content": obj["answer"],
            "result": obj,
            "steps": list(self._steps),
        })
        return obj

    def finalize_failed(self, conn, code: str) -> None:
        """실패 마감. **부분 텍스트는 지우지 않는다** — 어디까지 갔는지가 근거다."""
        store.update_message(conn, self.message_id, {
            "status": store.STATUS_FAILED,
            "error_code": code,
            "steps": list(self._steps),
        })


# --- 구동 -------------------------------------------------------------------


async def run_consumer(*, message_id: str, conversation_id: str, task_id: str) -> None:
    """태스크 하나를 끝까지 소비한다. 예외를 밖으로 내보내지 않는다(백그라운드 태스크)."""
    if task_id in _running:
        logger.info("chat: task %s 는 이미 소비 중 — 건너뛴다", task_id)
        return
    _running.add(task_id)
    timeout = settings.ai_timeout_sec
    try:
        await asyncio.wait_for(
            _consume(message_id=message_id, conversation_id=conversation_id, task_id=task_id),
            # 전체 상한 = turn 시간 상한. 이벤트가 아예 안 와도 여기서 끊긴다.
            timeout=timeout,
        )
    except TimeoutError:
        logger.warning("chat: message %s 시간 상한(%ds) 초과 — failed", message_id, timeout)
        _finalize_out_of_band(message_id, conversation_id, store.CODE_AI_TIMEOUT)
    except Exception:  # noqa: BLE001 — 백그라운드 태스크는 조용히 죽지 않는다
        logger.exception("chat 소비자 예외 message=%s", message_id)
        _finalize_out_of_band(message_id, conversation_id, store.CODE_AI_FAILED)
    finally:
        _running.discard(task_id)


async def _consume(*, message_id: str, conversation_id: str, task_id: str) -> None:
    from open_kknaks import AgentClient, RedisBroker

    from db.connection import connect_ro

    broker = RedisBroker(url=settings.redis_url, namespace=settings.ai_namespace)
    await broker.connect()
    client = AgentClient(broker=broker)
    try:
        folder = TurnFolder(message_id, conversation_id)
        with store.connect() as conn:
            row = store.get_message(conn, message_id)
            if row is None or row["status"] != store.STATUS_PENDING:
                return  # 이미 끝난 메시지 — 완료 이벤트 재수신은 무시한다

            # 스키마·근거 위반이면 **재제출**로 한 번 더 본다(SPEC-005 OQ-5).
            # `ai_schema_retry` 가 그 횟수다 — 0 이면 첫 실패에서 바로 마감한다.
            attempts_left = max(0, settings.ai_schema_retry)
            current_task_id = task_id
            while True:
                async for event in client.stream(current_task_id, timeout=settings.ai_timeout_sec):
                    fold_one(conn, folder, event)

                task = await broker.get_task(current_task_id)
                status = getattr(task, "status", None) if task is not None else None
                exit_code = getattr(task, "exit_code", 0) if task is not None else None
                if status != "done" or (exit_code or 0) != 0:
                    # 태스크가 사라졌으면 시간 초과로 본다 — 워커가 실패를 남겼으면 그건 실패다
                    code = store.CODE_AI_TIMEOUT if task is None else store.CODE_AI_FAILED
                    logger.warning("chat: message %s 마감 실패 status=%s exit=%s",
                                   message_id, status, exit_code)
                    folder.finalize_failed(conn, code)
                    return

                ontology = connect_ro()
                try:
                    folder.finalize_done(conn, ontology, getattr(task, "result", None))
                    return
                except AnswerSchemaError as exc:
                    # `except ... as exc` 는 블록을 벗어나면 이름이 지워진다 —
                    # 재제출에 실어 보낼 문구를 여기서 붙들어 둔다.
                    violations = exc.render()
                    logger.warning("chat: message %s 답변 검증 실패(남은 재시도 %d)\n%s",
                                   message_id, attempts_left, violations)
                    if attempts_left <= 0:
                        folder.finalize_failed(conn, store.CODE_AI_FAILED)
                        return
                finally:
                    ontology.close()

                attempts_left -= 1
                # 순환 import 회피 — `runtime` 이 이 모듈의 `run_consumer` 를 쓴다
                from .runtime import resubmit_for_repair

                retry_task_id = await resubmit_for_repair(
                    message_id=message_id, conversation_id=conversation_id,
                    violations=violations)
                if retry_task_id is None:
                    folder.finalize_failed(conn, store.CODE_AI_FAILED)
                    return
                # 새 답변이 통째로 다시 오므로 본문은 비우고 단계는 이어 붙인다 —
                # 도구 호출은 실제로 일어난 일이라 지우면 기록이 사실과 어긋난다.
                folder.begin_retry(conn)
                current_task_id = retry_task_id
    finally:
        with contextlib.suppress(Exception):
            await broker.close()


def fold_one(conn, folder: TurnFolder, event: Any) -> None:
    """이벤트 하나를 접는다. `thinking`·`cost`·`progress` 는 버린다 — 화면에 자리가 없다."""
    kind = getattr(event, "type", None)
    if kind == "init":
        folder.on_init(conn, getattr(event, "session_id", None))
    elif kind == "text":
        folder.on_text(conn, getattr(event, "text", None) or "")
    elif kind == "tool_use":
        folder.on_tool_use(
            conn,
            tool_use_id=getattr(event, "tool_use_id", None),
            tool_name=getattr(event, "tool_name", "") or "",
            tool_input=getattr(event, "tool_input", None),
        )
    elif kind == "tool_result":
        folder.on_tool_result(
            conn,
            tool_use_id=getattr(event, "tool_use_id", None),
            result=getattr(event, "tool_result", None),
            is_error=getattr(event, "tool_is_error", None),
        )


def _finalize_out_of_band(message_id: str, conversation_id: str, code: str) -> None:
    """소비자 바깥에서 실패로 마감한다(상한 초과·예외)."""
    with contextlib.suppress(Exception):
        with store.connect() as conn:
            row = store.get_message(conn, message_id)
            if row is None or row["status"] != store.STATUS_PENDING:
                return
            # 이미 적재된 부분 텍스트·단계는 건드리지 않는다 — 어디까지 갔는지가 근거다
            store.update_message(conn, message_id, {
                "status": store.STATUS_FAILED, "error_code": code})


def recover_pending() -> int:
    """기동 스윕 — 진행 중이던 답변을 정리한다. 반환 = 손댄 메시지 수.

    `task_id` 가 있으면 재부착 재생, 없으면(제출 전에 죽었다) 실패로 마감한다.
    """
    from .runtime import spawn_consumer

    with store.connect() as conn:
        pending = [(r["id"], r["conversation_id"], r["task_id"]) for r in store.list_pending(conn)]
    for message_id, conversation_id, task_id in pending:
        if task_id:
            spawn_consumer(message_id=message_id, conversation_id=conversation_id,
                           task_id=task_id)
        else:
            _finalize_out_of_band(message_id, conversation_id, store.CODE_AI_FAILED)
    if pending:
        logger.info("chat 기동 복구: 진행 중이던 답변 %d건 처리", len(pending))
    return len(pending)

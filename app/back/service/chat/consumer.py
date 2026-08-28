"""상주 소비자 — 이벤트 폴딩 (SPEC-017 §5 · DEC-027 D6).

제출 직후 태스크 전용 소비자가 이벤트 스트림(`init` · `text` · `tool_use` ·
`tool_result` · `result`)을 구독해 DB 에 접는다. 원시 이벤트 로그 표를 두지 않는다 —
FE 가 2초 폴링으로 읽는 것은 접힌 결과 그 자체다.

| 이벤트 | 저장 |
|---|---|
| `init` | `conversation.ai_session_id` 확정 (D2 와 연결) |
| `text` | assistant `content` 부분 누적 |
| `tool_use` | `steps` 에 한 줄 INSERT — `tool_use_id` 멱등 |
| `tool_result` | 같은 줄 UPDATE(+`durationMs`) + 문서 계열이면 `sources` 추출 |
| `thinking`·`cost`·`progress` | 버린다 — 화면에 자리가 없다 |
| 최종 `result` | `content` 를 최종 본문으로 **교체** + `done` |

## 중복 수신이 정상 경로다

브로커가 Redis Stream 이라 다시 붙으면 **처음부터 전부 다시 온다**(cursor 가 없다).
그래서 폴딩은 「같은 이벤트를 두 번 받아도 같은 결과」여야 한다:

- `text` 는 재생 시작 때 **초기화한 뒤** 다시 쌓는다(누적이라 그냥 두면 두 배가 된다).
- `tool_use`/`tool_result` 는 `tool_use_id` 로 멱등 upsert 한다.
- 이미 끝난 메시지의 완료 이벤트는 무시한다.

## idle 상한은 바깥에서 건다

`AgentClient.stream(timeout=)` 의 deadline 검사는 `async for` **본문 안**에 있다 —
이벤트가 하나도 안 오면 발동하지 않는다(설치본 확인). 워커가 조용히 죽었을 때 소비자가
영원히 사는 것을 막는 유일한 안전망이 바깥의 `asyncio.wait_for` 다.

## 소비자 1개 보장은 in-process 로 충분하다

레퍼런스는 Redis `SET NX EX` 를 썼다 — 배포 단위가 여러 pod 이라서다. 이 사이트의 back 은
**컨테이너 하나**이므로 모듈 레벨 집합이면 같은 보장을 준다. 프로세스가 죽으면 집합도
사라지는데, 그게 정확히 원하는 것이다 — 기동 스윕이 다시 붙어야 한다.
"""

from __future__ import annotations

import ast
import asyncio
import contextlib
import json
import logging
import time
from datetime import UTC, datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from config import get_settings
from core.chat_slugs import public_url
from core.db import SessionLocal
from dto.chat import ChatMessageDTO
from models.chat import STATUS_DONE, STATUS_FAILED, STATUS_PENDING
from repository.chat_repo import chat_repository

logger = logging.getLogger(__name__)

# 폐기(turn 토큰 해시 지우기)는 **마감 한 곳**에서만 한다 — `TurnFolder.finalize` 가
# done/failed 양쪽에서 지우고, 상한 초과·예외 경로도 `_finalize_out_of_band` 를 거쳐
# 같은 자리로 모인다. 별도 폐기 함수를 두면 「어느 쪽이 지웠나」가 생긴다.

# §4 Case Matrix — status 는 둘 다 failed 이고 code 만 구분한다.
CODE_AI_FAILED = "AI_FAILED"
CODE_AI_TIMEOUT = "AI_TIMEOUT"

#: 단계 한 줄의 인자 요약 상한. 인자 원문을 그대로 노출하지 않는다(§5).
_ARG_SUMMARY_MAX = 120
#: 인자 **하나**의 상한 — 첫 인자가 줄을 다 먹지 않게 각 값을 먼저 자른다.
_ARG_VALUE_MAX = 60

#: 한 답변이 실을 근거 카드 상한. 넘으면 로그를 남긴다 — 조용한 절단을 만들지 않는다.
_MAX_SOURCES = 12

#: MCP 봉투를 여는 깊이. 실측상 한 겹이다 — 더 파면 엉뚱한 깊이의 값을 줍는다.
_MAX_ENVELOPE_DEPTH = 1

#: **문서 계열 tool** — 근거 카드는 여기서만 나온다(§3 S-9 2항 「실제로 읽은 것」).
#: 목록 tool 은 훑기만 한 것이라 카드로 올리지 않는다.
#:
#: `get_company_product` 도 문서다(spec v0.0.9) — 회사 제품 showcase 를 읽은 것 역시
#: 「실제로 읽은 것」이다. 그 카드의 `url` 은 **null** 이다(공개 페이지가 없다) — 값은
#: tool 응답이 싣고 오고, 없으면 `public_url` 이 유형으로 파생하는데 회사 제품은 그쪽도
#: None 을 준다(`core/chat_slugs.py`). 화면은 링크 없이 카드만 그린다.
_DOC_TOOLS = frozenset(
    {
        "get_career",
        "get_project",
        "get_problem",
        "get_note",
        "get_company_product",
    }
)

#: 태스크당 소비자 1개 — 위 머리 주석 참조.
_running: set[str] = set()


# ── 이벤트 값 해석 ───────────────────────────────────────
def _decode(raw: Any) -> Any:
    """tool payload 문자열 → 객체. **구조적 해석만** 한다(정규식 없음).

    두 모양을 다 받는다: JSON 문자열, 그리고 파이썬 repr(작은따옴표 — codex 어댑터가
    파싱된 dict 를 `str()` 로 넘겨 생긴다). repr 은 `ast.literal_eval` 로 읽는다 —
    리터럴만 평가하므로 tool 응답이 코드가 될 여지가 없다. 둘 다 실패하면 None 이고,
    그때는 아무것도 하지 않는다.
    """
    if not isinstance(raw, str):
        return raw
    try:
        return json.loads(raw)
    except (ValueError, TypeError):
        pass
    try:
        return ast.literal_eval(raw)
    except (ValueError, SyntaxError, MemoryError, RecursionError):
        return None


def _layers(raw: Any, *, depth: int = _MAX_ENVELOPE_DEPTH) -> list[Any]:
    """payload 층 목록 — 바깥이 먼저, MCP 봉투 안쪽이 뒤.

    MCP 는 한 겹 더 감싸 온다: `{"content":[{"type":"text","text":"<JSON 문자열>"}]}`.
    즉 tool 의 `structured` 가 text 안에 **이중 인코딩**돼 있다.
    """
    payload = _decode(raw)
    out: list[Any] = [payload]
    if depth >= 1 and isinstance(payload, dict):
        for block in payload.get("content") or []:
            if not isinstance(block, dict):
                continue
            inner = _decode(block.get("text"))
            if inner is not None:
                out.extend(_layers(inner, depth=depth - 1))
    return out


def _render_arg(value: Any) -> str:
    if isinstance(value, str):
        text = value
    elif isinstance(value, bool | int | float) or value is None:
        text = json.dumps(value, ensure_ascii=False)
    else:
        text = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return " ".join(text.split())[:_ARG_VALUE_MAX]


def summarize_args(tool_input: Any) -> str:
    """`tool_use` 의 **인자만** 요약한다 — 이벤트 item 봉투를 싣지 않는다.

    codex 어댑터의 `tool_input` 은 item dict 통째다(`{id, type, server, tool,
    arguments, …}`). 그걸 그대로 요약하면 화면에 `id=item_4 · type=mcp_tool_call …` 이
    찍힌다 — 방문자가 볼 것은 「무엇을 인자로 줬나」지 봉투가 아니다.

    인자가 하나면 값만, 여럿이면 `키=값` 을 ` · ` 로 잇는다. None 인 인자는 에이전트가
    주지 않은 것이라 뺀다. 못 읽으면 빈 문자열이다.
    """
    if tool_input is None:
        return ""
    for layer in _layers(tool_input):
        if not isinstance(layer, dict):
            continue
        raw_args = layer["arguments"] if "arguments" in layer else layer
        # 봉투인데 arguments 가 없으면 봉투를 인자로 싣지 않는다.
        if raw_args is layer and layer.get("type") == "mcp_tool_call":
            continue
        args = _decode(raw_args)
        if not isinstance(args, dict):
            continue
        pairs = [(k, v) for k, v in args.items() if v is not None]
        if not pairs:
            continue
        if len(pairs) == 1:
            return _render_arg(pairs[0][1])[:_ARG_SUMMARY_MAX]
        return " · ".join(f"{k}={_render_arg(v)}" for k, v in pairs)[:_ARG_SUMMARY_MAX]
    return ""


def _tool_key(tool_name: str) -> str:
    """`kknaks__get_career` · `mcp__kknaks__get_career` → `get_career`.

    codex 가 MCP tool 이름 앞에 서버 접두사를 붙인다. 근거 카드 판정(`_DOC_TOOLS`)과
    화면 표시가 접두사에 흔들리지 않게 마지막 조각만 본다.
    """
    return (tool_name or "").rsplit("__", 1)[-1]


def extract_sources(tool_name: str, result: Any) -> list[dict[str, Any]]:
    """문서 계열 tool_result 에서 근거 카드를 **구조 필드로만** 뽑는다.

    본문 텍스트를 정규식으로 훑는 경로를 두지 않는다 — 문구가 바뀌면 조용히 깨지고,
    「읽지 않은 것」이 근거로 올라온다. 못 읽으면 빈 리스트다.
    """
    if _tool_key(tool_name) not in _DOC_TOOLS or result is None:
        return []
    for layer in _layers(result):
        if not isinstance(layer, dict):
            continue
        structured = layer.get("structured")
        item = structured.get("item") if isinstance(structured, dict) else None
        if not isinstance(item, dict):
            continue
        doc_type, slug = item.get("type"), item.get("slug")
        if not doc_type or not slug:
            continue
        return [
            {
                "type": str(doc_type),
                "slug": str(slug),
                "title": str(item.get("title") or slug),
                # tool 이 url 을 안 실었으면 유형으로 파생한다 — 카드가 링크를 잃지 않게.
                "url": item.get("url") or public_url(str(doc_type), str(slug)),
            }
        ]
    return []


# ── 폴딩 ────────────────────────────────────────────────
class TurnFolder:
    """이벤트 → chat_message. 한 assistant 메시지만 만진다."""

    def __init__(self, message: ChatMessageDTO) -> None:
        self._message_id = message.id
        self._conversation_id = message.conversation_id
        self._text = message.content or ""
        self._steps: list[dict[str, Any]] = list(message.steps or [])
        self._sources: list[dict[str, Any]] = list(message.sources or [])
        #: tool_use_id → 그 호출을 본 시각(monotonic). **프로세스 안에서만** 산다.
        self._started: dict[str, float] = {}
        #: 재생 중인가. 재생에서 두 이벤트의 시간차는 「툴이 걸린 시간」이 아니라
        #: 「스트림을 읽은 시간」이라 durationMs 로 적을 수 없다.
        self._replay = False
        #: 아직 안 치른 재생 초기화가 있는가 — `begin_replay` 참조.
        self._reset_pending = False

    @property
    def message_id(self) -> int:
        return self._message_id

    def begin_replay(self) -> None:
        """재부착을 표시한다. **여기서는 아직 지우지 않는다.**

        재생은 스트림을 처음부터 다시 받으므로 부분 텍스트를 비우고 다시 쌓아야 한다
        (안 비우면 두 배가 된다). 그런데 **비우는 시점이 붙는 시점이면** 스트림이 이미
        만료돼 이벤트가 하나도 안 오는 경우에 기존 텍스트만 날아간다 — 그리고 그대로
        failed 로 마감돼 「실패 마감은 부분 텍스트를 지우지 않는다」(`finalize`)는
        불변식과 정면으로 어긋난다(리뷰 W10).

        그래서 초기화를 **첫 재생 text 를 받는 순간**으로 미룬다. 다시 쌓을 것이
        실제로 왔을 때만 지우므로, 이벤트가 0건이면 기존 기록이 그대로 남는다.
        steps 는 애초에 지우지 않는다 — `tool_use_id` 멱등 upsert 라 지우면 그 사이
        도착한 결과가 사라진다.
        """
        self._replay = True
        self._reset_pending = True

    async def on_init(self, db: AsyncSession, session_id: str | None) -> None:
        """codex 세션 확정 — 이 대화의 다음 질문이 resume 으로 쓴다(DEC-027 D2)."""
        if not session_id:
            return
        await chat_repository.set_ai_session_id(
            db, self._conversation_id, session_id
        )

    async def on_text(self, db: AsyncSession, delta: str) -> None:
        if not delta:
            return
        if self._reset_pending:
            # 재생의 첫 글자가 실제로 왔다 — 이제 비우고 다시 쌓는다(`begin_replay`).
            self._text = ""
            self._reset_pending = False
        self._text += delta
        await chat_repository.update_message(
            db, self._message_id, {"content": self._text}
        )

    async def on_tool_use(
        self, db: AsyncSession, *, tool_use_id: str | None, tool_name: str, tool_input: Any
    ) -> None:
        """단계 한 줄 INSERT — `tool_use_id` 로 멱등. 재생에서 같은 id 는 덮지 않는다.

        ⚠ id 가 없는 경로가 남아 있다(구 어댑터). 그때는 `tool 이름 + 순서`로 대신
        키를 만든다 — 병렬 호출이 섞이면 짝이 어긋날 수 있는 임시 대응이다.
        """
        key = tool_use_id or f"seq:{_tool_key(tool_name)}:{len(self._steps)}"
        if any(step.get("toolUseId") == key for step in self._steps):
            return
        self._started.setdefault(key, time.monotonic())
        self._steps.append(
            {
                "toolUseId": key,
                "tool": _tool_key(tool_name),
                "argsSummary": summarize_args(tool_input),
                "durationMs": None,
                "calledAt": datetime.now(UTC).isoformat(),
                "status": "running",
            }
        )
        await self._flush_steps(db)

    async def on_tool_result(
        self, db: AsyncSession, *, tool_use_id: str | None, result: Any, is_error: bool | None
    ) -> None:
        """같은 줄을 UPDATE(새 줄 X) + 문서 계열이면 근거 카드를 더한다."""
        step = self._find_step(tool_use_id)
        if step is None:
            return
        step["status"] = "failed" if is_error else "done"
        duration = self._duration_for(step)
        if duration is not None:
            step["durationMs"] = duration

        patch: dict[str, Any] = {"steps": list(self._steps)}
        for source in extract_sources(step.get("tool", ""), result):
            if self._add_source(source):
                patch["sources"] = list(self._sources)
        await chat_repository.update_message(db, self._message_id, patch)

    async def finalize(
        self,
        db: AsyncSession,
        *,
        result_text: str | None,
        status: str,
        error_code: str | None = None,
    ) -> None:
        """최종 본문으로 **교체**하고 마감한다.

        실패 마감에서는 부분 텍스트를 지우지 않는다 — 방문자가 이미 읽은 글자를 사후에
        뺏지 않는다. 토큰 폐기도 여기서 같이 한다(마감 = 폐기 시점).
        """
        content = result_text if (status == STATUS_DONE and result_text) else self._text
        await chat_repository.update_message(
            db,
            self._message_id,
            {
                "content": content,
                "status": status,
                "error_code": error_code,
                "steps": list(self._steps),
                "sources": list(self._sources),
                # 폐기 — 해시를 지우면 그 토큰으로는 아무것도 못 찾는다.
                "turn_token_hash": None,
                "turn_token_expires_at": None,
            },
        )

    # ── helpers ─────────────────────────────────────────
    def _find_step(self, tool_use_id: str | None) -> dict[str, Any] | None:
        if tool_use_id:
            for step in self._steps:
                if step.get("toolUseId") == tool_use_id:
                    return step
            return None
        # id 없는 tool_result 의 짝 — 아직 running 인 마지막 줄(임시 대응).
        for step in reversed(self._steps):
            if step.get("status") == "running":
                return step
        return None

    def _duration_for(self, step: dict[str, Any]) -> int | None:
        """이 짝의 소요 ms. 이미 적혀 있거나 재생 중이면 재지 않는다 —
        **없는 것보다 틀린 수치가 나쁘다.**"""
        if isinstance(step.get("durationMs"), int):
            return None
        if self._replay:
            return None
        started = self._started.get(step.get("toolUseId", ""))
        if started is None:
            return None
        return max(0, round((time.monotonic() - started) * 1000))

    def _add_source(self, source: dict[str, Any]) -> bool:
        """(type, slug) 로 접는다. 같은 문서를 두 번 읽어도 카드는 하나다."""
        key = (source["type"], source["slug"])
        if any((s.get("type"), s.get("slug")) == key for s in self._sources):
            return False
        if len(self._sources) >= _MAX_SOURCES:
            logger.info(
                "chat: 근거 카드 상한(%d) 초과 — %s 는 싣지 않는다",
                _MAX_SOURCES,
                source["slug"],
            )
            return False
        self._sources.append(source)
        return True

    async def _flush_steps(self, db: AsyncSession) -> None:
        await chat_repository.update_message(
            db, self._message_id, {"steps": list(self._steps)}
        )


# ── 구동 ────────────────────────────────────────────────
async def run_turn_consumer(*, message_id: int, task_id: str, replay: bool = False) -> None:
    """태스크 하나를 끝까지 소비한다. 예외를 밖으로 내보내지 않는다(백그라운드 task)."""
    if task_id in _running:
        logger.info("chat: task %s 는 이미 소비 중 — 건너뛴다", task_id)
        return
    _running.add(task_id)
    timeout = get_settings().chat_timeout_sec
    try:
        await asyncio.wait_for(
            _consume(message_id=message_id, task_id=task_id, replay=replay),
            # 전체 상한 = turn 시간 상한. 이벤트가 아예 안 와도 여기서 끊긴다.
            timeout=timeout,
        )
    except TimeoutError:
        logger.warning("chat: message %s 시간 상한(%ds) 초과 — failed", message_id, timeout)
        await _finalize_out_of_band(message_id, CODE_AI_TIMEOUT)
    except Exception:  # noqa: BLE001 — 백그라운드 task 는 조용히 죽지 않는다
        logger.exception("chat 소비자 예외 message=%s task=%s", message_id, task_id)
        await _finalize_out_of_band(message_id, CODE_AI_FAILED)
    finally:
        _running.discard(task_id)


async def _consume(*, message_id: int, task_id: str, replay: bool) -> None:
    from open_kknaks import AgentClient, RedisBroker

    settings = get_settings()
    broker = RedisBroker(url=settings.redis_url, namespace=settings.ai_namespace)
    await broker.connect()
    client = AgentClient(broker=broker)
    try:
        async with SessionLocal() as db:
            message = await chat_repository.get_message(db, message_id)
            if message is None or message.status != STATUS_PENDING:
                # 이미 끝난 메시지 — 완료 이벤트 재수신은 무시한다.
                return
            folder = TurnFolder(message)
            if replay:
                # DB 를 건드리지 않는다 — 초기화는 첫 재생 text 때 일어난다.
                folder.begin_replay()

            async for event in client.stream(task_id, timeout=settings.chat_timeout_sec):
                await _fold_one(db, folder, event)
                # 이벤트마다 커밋한다 — 폴링이 2초마다 읽으므로 트랜잭션을 오래 열면
                # 「자라나는 답변」이 통째로 늦게 보인다.
                await db.commit()

            # 스트림이 끝났다 = 태스크가 종료 상태다. 최종 result 로 마감한다.
            await _close_from_task(db, folder, await broker.get_task(task_id))
            await db.commit()
    finally:
        with contextlib.suppress(Exception):
            await broker.close()


async def _fold_one(db: AsyncSession, folder: TurnFolder, event: Any) -> None:
    kind = getattr(event, "type", None)
    if kind == "init":
        await folder.on_init(db, getattr(event, "session_id", None))
    elif kind == "text":
        await folder.on_text(db, getattr(event, "text", None) or "")
    elif kind == "tool_use":
        await folder.on_tool_use(
            db,
            tool_use_id=getattr(event, "tool_use_id", None),
            tool_name=getattr(event, "tool_name", "") or "",
            tool_input=getattr(event, "tool_input", None),
        )
    elif kind == "tool_result":
        await folder.on_tool_result(
            db,
            tool_use_id=getattr(event, "tool_use_id", None),
            result=getattr(event, "tool_result", None),
            is_error=getattr(event, "tool_is_error", None),
        )
    # thinking · cost · progress · retry 는 버린다 — 화면에 자리가 없다.


async def _close_from_task(db: AsyncSession, folder: TurnFolder, task: Any) -> None:
    """스트림 종료 후 최종 마감 — `task.result` 회수가 2차 안전망이기도 하다."""
    current = await chat_repository.get_message(db, folder.message_id)
    if current is None or current.status != STATUS_PENDING:
        return
    status = getattr(task, "status", None) if task is not None else None
    exit_code = getattr(task, "exit_code", 0) if task is not None else None
    if status == "done" and (exit_code or 0) == 0:
        await folder.finalize(
            db, result_text=getattr(task, "result", None), status=STATUS_DONE
        )
        return
    # 태스크가 사라졌으면(스트림 만료·소멸) 시간 초과로 본다 — 워커가 실패를 남겼으면
    # 그건 실패다. 둘 다 status=failed 이고 code 만 갈린다(§4 Case Matrix).
    code = CODE_AI_TIMEOUT if task is None else CODE_AI_FAILED
    logger.warning(
        "chat: message %s 마감 실패 status=%s exit=%s", folder.message_id, status, exit_code
    )
    await folder.finalize(db, result_text=None, status=STATUS_FAILED, error_code=code)


async def _finalize_out_of_band(message_id: int, code: str) -> None:
    """소비자 바깥에서 실패로 마감한다(상한 초과·예외). 부분 텍스트는 지우지 않는다."""
    with contextlib.suppress(Exception):
        async with SessionLocal() as db:
            message = await chat_repository.get_message(db, message_id)
            if message is None or message.status != STATUS_PENDING:
                return
            await TurnFolder(message).finalize(
                db, result_text=None, status=STATUS_FAILED, error_code=code
            )
            await db.commit()


async def recover_pending_turns() -> int:
    """back 기동 시 스윕 — 2단 복구(WORK-023 P4). 반환 = 손댄 메시지 수.

    ① `task_id` 가 있으면 **재부착 재생**으로 기록을 다시 세운다(스트림이 살아 있으면
       처음부터 다시 오고, 죽었으면 `_close_from_task` 의 result 회수가 마감한다).
    ② `task_id` 가 없으면(제출 전에 죽었다) 재생할 스트림 자체가 없으므로 실패로 마감한다.
    """
    from service.chat.runtime import spawn_consumer

    async with SessionLocal() as db:
        pending = await chat_repository.list_pending_messages(db)
        stale = [(m.id, m.task_id) for m in pending]
    for message_id, task_id in stale:
        if task_id:
            spawn_consumer(message_id=message_id, task_id=task_id)
        else:
            await _finalize_out_of_band(message_id, CODE_AI_FAILED)
    if stale:
        logger.info("chat 기동 복구: 진행 중이던 답변 %d건 처리", len(stale))
    return len(stale)

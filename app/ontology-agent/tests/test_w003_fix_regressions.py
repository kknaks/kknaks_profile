"""WORK-003 검수 지적의 회귀 — 「다시 풀리면 여기서 잡힌다」.

각 테스트가 리포트 항목 번호를 달고 있다.
"""

from __future__ import annotations

import asyncio
import sqlite3
import types

import pytest

from agent import store
from agent.answer import (
    AnswerSchemaError,
    EvidenceError,
    ValidationReport,
    validate_evidence,
)
from agent.consumer import TurnFolder, _consume
from agent.prompt import SYSTEM_PROMPT, build_repair_prompt
from config import settings
from tests.conftest import requires_source


def _minimal(**overrides) -> dict:
    obj = {
        "answer": "본문",
        "premise_correction": {"corrected": False},
        "used_edges": [],
        "citations": [],
    }
    obj.update(overrides)
    return obj


# --- W1. 스키마 위반 시 1회 재시도 (SPEC-005 OQ-5) ---------------------------


class _FakeTask:
    def __init__(self, result: str) -> None:
        self.status = "done"
        self.exit_code = 0
        self.result = result


class _FakeBroker:
    """`get_task` 가 제출 순서대로 결과를 돌려준다."""

    def __init__(self, results: list[str]) -> None:
        self._results = list(results)
        self.closed = False

    async def connect(self) -> None:  # pragma: no cover — 인터페이스 맞춤
        pass

    async def get_task(self, task_id: str):
        return _FakeTask(self._results.pop(0))

    async def close(self) -> None:
        self.closed = True


class _FakeClient:
    def __init__(self, broker: _FakeBroker) -> None:
        self.broker = broker

    async def stream(self, task_id: str, timeout: int | None = None):
        # 이벤트는 없어도 된다 — 마감은 `get_task` 의 result 로 이뤄진다
        for event in ():  # pragma: no cover
            yield event


def _install_fakes(monkeypatch, results: list[str], *, submits: list[str | None]):
    """open-kknaks 와 재제출을 가짜로 갈아 끼운다. 큐 없이 재시도 경로가 돈다."""
    broker = _FakeBroker(results)
    fake_module = types.SimpleNamespace(
        AgentClient=lambda broker: _FakeClient(broker),
        RedisBroker=lambda url, namespace: broker,
    )
    monkeypatch.setitem(__import__("sys").modules, "open_kknaks", fake_module)

    calls: list[str] = []
    pending = list(submits)

    async def _fake_resubmit(*, message_id, conversation_id, violations):
        calls.append(violations)
        return pending.pop(0)

    from agent import runtime

    monkeypatch.setattr(runtime, "resubmit_for_repair", _fake_resubmit)
    return broker, calls


def _good_answer(built_db) -> str:
    row = built_db.execute(
        "SELECT sales_total FROM gold_kpi_monthly WHERE month = '2026-08'").fetchone()
    return (
        '```json\n{"answer": "8월 매출입니다.", "premise_correction": {"corrected": false}, '
        '"used_edges": [], "citations": [{"claim": "8월 매출", "value": '
        f'{row["sales_total"]}, "row_count": 1, '
        '"period": {"start": "2026-08-01", "end": "2026-08-31"}, '
        '"source": {"tool": "query_kpi", "table": "gold_kpi_monthly", '
        '"column": "sales_total"}}]}\n```')


_BAD_ANSWER = '```json\n{"answer": "본문만 있고 필수 필드가 없다"}\n```'


@requires_source
def test_W1_1차_위반이면_재제출해서_살린다(built_db, built_db_path, monkeypatch, tmp_path):
    """SPEC-005 OQ-5 — 스키마 위반 시 **1회 재시도**. 재시도가 통과하면 `done` 이다."""
    monkeypatch.setattr(settings, "db_path", built_db_path)
    monkeypatch.setattr(settings, "chat_db_path", tmp_path / "chat.db")
    monkeypatch.setattr(settings, "ai_schema_retry", 1)
    _install_fakes(monkeypatch, [_BAD_ANSWER, _good_answer(built_db)], submits=["task-2"])

    with store.connect() as conn:
        cid = store.create_conversation(conn, question="q")
        mid = store.add_message(conn, conversation_id=cid, role=store.ROLE_ASSISTANT,
                                status=store.STATUS_PENDING)

    asyncio.run(_consume(message_id=mid, conversation_id=cid, task_id="task-1"))

    with store.connect() as conn:
        row = store.get_message(conn, mid)
    assert row["status"] == store.STATUS_DONE, "재시도가 통과했는데 failed 다"
    assert row["error_code"] is None


@requires_source
def test_W1_2연속_위반이면_failed_로_마감한다(built_db_path, monkeypatch, tmp_path):
    """재시도도 실패하면 `failed` + `AI_FAILED` — 무한 재시도하지 않는다."""
    monkeypatch.setattr(settings, "db_path", built_db_path)
    monkeypatch.setattr(settings, "chat_db_path", tmp_path / "chat.db")
    monkeypatch.setattr(settings, "ai_schema_retry", 1)
    _, calls = _install_fakes(monkeypatch, [_BAD_ANSWER, _BAD_ANSWER], submits=["task-2"])

    with store.connect() as conn:
        cid = store.create_conversation(conn, question="q")
        mid = store.add_message(conn, conversation_id=cid, role=store.ROLE_ASSISTANT,
                                status=store.STATUS_PENDING)

    asyncio.run(_consume(message_id=mid, conversation_id=cid, task_id="task-1"))

    with store.connect() as conn:
        row = store.get_message(conn, mid)
    assert row["status"] == store.STATUS_FAILED
    assert row["error_code"] == store.CODE_AI_FAILED
    assert len(calls) == 1, f"재시도는 1회여야 한다(실제 {len(calls)}회)"


@requires_source
def test_W1_재시도_0이면_첫_실패에서_바로_마감한다(built_db_path, monkeypatch, tmp_path):
    """`ai_schema_retry` 가 **실제로 읽힌다** — 죽은 설정이 아니다."""
    monkeypatch.setattr(settings, "db_path", built_db_path)
    monkeypatch.setattr(settings, "chat_db_path", tmp_path / "chat.db")
    monkeypatch.setattr(settings, "ai_schema_retry", 0)
    _, calls = _install_fakes(monkeypatch, [_BAD_ANSWER], submits=[])

    with store.connect() as conn:
        cid = store.create_conversation(conn, question="q")
        mid = store.add_message(conn, conversation_id=cid, role=store.ROLE_ASSISTANT,
                                status=store.STATUS_PENDING)

    asyncio.run(_consume(message_id=mid, conversation_id=cid, task_id="task-1"))

    with store.connect() as conn:
        row = store.get_message(conn, mid)
    assert row["status"] == store.STATUS_FAILED
    assert calls == [], "재시도 0인데 재제출했다"


@requires_source
def test_W1_재제출이_실패하면_failed_다(built_db_path, monkeypatch, tmp_path):
    """세션이 없거나 제출이 죽으면 살릴 방법이 없다 — 조용히 pending 으로 두지 않는다."""
    monkeypatch.setattr(settings, "db_path", built_db_path)
    monkeypatch.setattr(settings, "chat_db_path", tmp_path / "chat.db")
    monkeypatch.setattr(settings, "ai_schema_retry", 1)
    _install_fakes(monkeypatch, [_BAD_ANSWER], submits=[None])

    with store.connect() as conn:
        cid = store.create_conversation(conn, question="q")
        mid = store.add_message(conn, conversation_id=cid, role=store.ROLE_ASSISTANT,
                                status=store.STATUS_PENDING)

    asyncio.run(_consume(message_id=mid, conversation_id=cid, task_id="task-1"))

    with store.connect() as conn:
        row = store.get_message(conn, mid)
    assert row["status"] == store.STATUS_FAILED
    assert row["error_code"] == store.CODE_AI_FAILED


def test_W1_재시도_프롬프트에_도메인_지식이_없다():
    """위반 목록만 실어 보낸다 — 「무엇이 옳은지」를 알려 주지 않는다(S-001)."""
    repair = build_repair_prompt("EVIDENCE_VIOLATION: 근거 무결성 위반 1건")
    for needle in ("cancel_rate", "sales_total", "채택", "자동 확정", "취소율", "→"):
        assert needle not in repair.replace("{violations}", ""), needle
    assert "EVIDENCE_VIOLATION" in repair


def test_W1_재시도_설정이_실제로_읽힌다():
    """리포트가 지적한 「죽은 설정」이 되지 않게 참조를 고정한다."""
    from pathlib import Path

    consumer_src = (Path(__file__).resolve().parents[1] / "agent" / "consumer.py").read_text(
        encoding="utf-8")
    assert "settings.ai_schema_retry" in consumer_src


def test_W1_독스트링이_실동작과_일치한다():
    """문서가 없는 동작을 있다고 말하지 않는다 — 리포트 W1 의 절반이 이것이었다."""
    from pathlib import Path

    app = Path(__file__).resolve().parents[1]
    answer_src = (app / "agent" / "answer.py").read_text(encoding="utf-8")
    consumer_src = (app / "agent" / "consumer.py").read_text(encoding="utf-8")
    # 「재제출」이라고 적어야 한다 — 같은 텍스트 재파싱은 결정적이라 의미가 없다
    assert "재제출" in answer_src
    assert "ai_schema_retry" in answer_src
    assert "재제출" in consumer_src


# --- W2. period 누락이 더 느슨한 검사를 받지 않는다 ---------------------------


@requires_source
def test_W2_기간_테이블_인용에_period_가_없으면_거부한다(built_db):
    """지시를 어긴 응답이 **더 넓은 창**으로 검사받는 역전을 없앤다."""
    row = built_db.execute(
        "SELECT sales_total FROM gold_kpi_daily ORDER BY date LIMIT 1").fetchone()
    obj = _minimal(citations=[{
        "claim": "어느 하루 매출", "value": row["sales_total"], "row_count": 1,
        # period 없음 — 예전에는 컬럼 전체(235행)를 훑어 우연 일치가 통과했다
        "source": {"tool": "query_kpi", "table": "gold_kpi_daily", "column": "sales_total"}}])
    with pytest.raises(EvidenceError) as exc:
        validate_evidence(built_db, obj)
    assert "period.start·period.end 가 필수" in exc.value.render()


@requires_source
def test_W2_period_가_반쪽이어도_거부한다(built_db):
    row = built_db.execute(
        "SELECT sales_total FROM gold_kpi_daily ORDER BY date LIMIT 1").fetchone()
    for period in ({"start": "2026-01-07"}, {"end": "2026-08-30"}, {}, None, "2026-08"):
        obj = _minimal(citations=[{
            "claim": "매출", "value": row["sales_total"], "row_count": 1, "period": period,
            "source": {"tool": "query_kpi", "table": "gold_kpi_daily",
                       "column": "sales_total"}}])
        with pytest.raises(EvidenceError):
            validate_evidence(built_db, obj)


@requires_source
def test_W2_period_를_주면_통과하고_창을_리포트에_남긴다(built_db):
    row = built_db.execute(
        "SELECT date, sales_total FROM gold_kpi_daily ORDER BY date LIMIT 1").fetchone()
    obj = _minimal(citations=[{
        "claim": "첫날 매출", "value": row["sales_total"], "row_count": 1,
        "period": {"start": row["date"], "end": row["date"]},
        "source": {"tool": "query_kpi", "table": "gold_kpi_daily", "column": "sales_total"}}])
    report = validate_evidence(built_db, obj)
    match = report.citation_matches[0]
    assert match["rule"] == "single_row"
    assert match["window"] == "period", "창을 좁혀 검사했다는 사실이 리포트에 남아야 한다"


@requires_source
def test_W2_기간_없는_테이블은_명시적_면제다(built_db):
    """면제는 모델의 선택이 아니라 **테이블의 성질**로 정한다 — 그레인 키가 없으면 좁힐 창이 없다."""
    row = built_db.execute(
        "SELECT n_products FROM gold_promo_calendar WHERE n_products IS NOT NULL LIMIT 1"
    ).fetchone()
    obj = _minimal(citations=[{
        "claim": "구성 상품 수", "value": row["n_products"], "row_count": 1,
        "source": {"tool": "query_kpi", "table": "gold_promo_calendar",
                   "column": "n_products"}}])
    report = validate_evidence(built_db, obj)
    assert report.citation_matches[0]["window"] == "table"


@requires_source
def test_W2_period_누락이_더_느슨한_검사를_받지_않는다(built_db):
    """역전의 핵심 — 같은 값이 창을 주면 실패, 안 주면 통과하는 경로가 있으면 안 된다.

    창을 좁히면 안 맞는 값(다른 날의 값)을 골라, period 를 빼면 통과하던 경로가
    지금은 **거부**되는지 본다.
    """
    rows = built_db.execute(
        "SELECT date, sales_total FROM gold_kpi_daily ORDER BY date LIMIT 40").fetchall()
    first, other = rows[0], rows[30]
    assert first["sales_total"] != other["sales_total"]

    # 첫날 창인데 값은 30일 뒤의 것 — 창을 주면 당연히 거부다
    windowed = _minimal(citations=[{
        "claim": "첫날 매출", "value": other["sales_total"], "row_count": 1,
        "period": {"start": first["date"], "end": first["date"]},
        "source": {"tool": "query_kpi", "table": "gold_kpi_daily", "column": "sales_total"}}])
    with pytest.raises(EvidenceError):
        validate_evidence(built_db, windowed)

    # 같은 값에서 period 만 빼면 예전에는 row_value 로 통과했다 — 지금은 거부여야 한다
    unwindowed = _minimal(citations=[{
        "claim": "첫날 매출", "value": other["sales_total"], "row_count": 1,
        "source": {"tool": "query_kpi", "table": "gold_kpi_daily", "column": "sales_total"}}])
    with pytest.raises(EvidenceError):
        validate_evidence(built_db, unwindowed)


@requires_source
def test_nit3_row_count_가_1이_아니면_row_value_를_인정하지_않는다(built_db):
    """「30행에서 나왔다」고 적어 놓고 그중 한 행과 우연히 같은 경우를 통과시키지 않는다."""
    rows = built_db.execute(
        "SELECT date, sales_total FROM gold_kpi_daily ORDER BY date LIMIT 10").fetchall()
    period = {"start": rows[0]["date"], "end": rows[-1]["date"]}
    value = rows[5]["sales_total"]

    loose = _minimal(citations=[{
        "claim": "구간 매출", "value": value, "row_count": 10, "period": period,
        "source": {"tool": "query_kpi", "table": "gold_kpi_daily", "column": "sales_total"}}])
    with pytest.raises(EvidenceError):
        validate_evidence(built_db, loose)

    tight = _minimal(citations=[{
        "claim": "그날 매출", "value": value, "row_count": 1, "period": period,
        "source": {"tool": "query_kpi", "table": "gold_kpi_daily", "column": "sales_total"}}])
    assert validate_evidence(built_db, tight).citation_matches[0]["rule"] == "row_value"


# --- W3. PII 대조를 건너뛰면 리포트에 남는다 ----------------------------------


def test_W3_브론즈가_없으면_스캔_0과_사유를_남긴다(tmp_path):
    """예외를 삼키면 리포트만 보고 「검사했다」로 오독한다."""
    path = tmp_path / "empty.db"
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE ontology_edges (cause, effect, verdict)")
    report = validate_evidence(conn, _minimal(), ValidationReport())
    conn.close()

    assert report.pii_scanned_fields == 0
    assert report.pii_skipped, "건너뛴 사유가 리포트에 없다"


@requires_source
def test_W3_브론즈가_있으면_실제로_스캔하고_사유가_비어_있다(built_db):
    report = validate_evidence(built_db, _minimal())
    assert report.pii_scanned_fields >= 1
    assert report.pii_skipped is None


# --- W4. 검사와 삽입이 원자적이다 ---------------------------------------------


def test_W4_exclusive_가_쓰기_락을_먼저_잡는다(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "chat_db_path", tmp_path / "chat.db")
    with store.connect() as conn:
        cid = store.create_conversation(conn, question="q")
        with store.exclusive(conn):
            assert store.has_pending(conn, cid) is False
            store.add_message(conn, conversation_id=cid, role=store.ROLE_ASSISTANT,
                              status=store.STATUS_PENDING)
        assert store.has_pending(conn, cid) is True


def test_W4_exclusive_는_예외에_되감는다(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "chat_db_path", tmp_path / "chat.db")
    with store.connect() as conn:
        cid = store.create_conversation(conn, question="q")
        with pytest.raises(RuntimeError):
            with store.exclusive(conn):
                store.add_message(conn, conversation_id=cid, role=store.ROLE_ASSISTANT,
                                  status=store.STATUS_PENDING)
                raise RuntimeError("중간에 터진다")
        assert store.has_pending(conn, cid) is False, "롤백되지 않았다"


# --- nit 5. update_message 컬럼 화이트리스트 ----------------------------------


def test_nit5_허용_밖_컬럼은_거부한다(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "chat_db_path", tmp_path / "chat.db")
    with store.connect() as conn:
        cid = store.create_conversation(conn, question="q")
        mid = store.add_message(conn, conversation_id=cid, role=store.ROLE_ASSISTANT,
                                status=store.STATUS_PENDING)
        with pytest.raises(ValueError, match="쓸 수 없는 컬럼"):
            store.update_message(conn, mid, {"conversation_id": "다른대화"})
        store.update_message(conn, mid, {"status": store.STATUS_DONE})


# --- nit 1. 독스트링이 실재하는 테스트를 가리킨다 ------------------------------


def test_nit1_프롬프트_독스트링이_실재_파일을_가리킨다():
    from pathlib import Path

    app = Path(__file__).resolve().parents[1]
    src = (app / "agent" / "prompt.py").read_text(encoding="utf-8")
    assert "test_w003_prompt.py" not in src, "없는 파일을 가리킨다"
    assert (app / "tests" / "test_w003_submission.py").exists()
    assert SYSTEM_PROMPT

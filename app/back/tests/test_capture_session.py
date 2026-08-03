from __future__ import annotations

import json
from datetime import datetime
from types import SimpleNamespace

import pytest

from service.knowledge_capture.session import (
    CaptureSession,
    CaptureSessionStore,
    ThreadBusyError,
)
from service.knowledge_capture import EMPTY_PREVIOUS, PreviousCapture, StoreResult
from service.slack_bridge.app import normalize_event
from service.slack_bridge.runner import KnowledgeCaptureRunner
from service.slack_bridge.stores import FileCaptureStore


class FakeRedis:
    def __init__(self):
        self.data: dict[str, str] = {}

    async def get(self, key):
        return self.data.get(key)

    async def set(self, key, value, *, ex=None, nx=False):
        if nx and key in self.data:
            return False
        self.data[key] = value
        return True

    async def eval(self, script, count, key, token):
        if self.data.get(key) == token:
            del self.data[key]
            return 1
        return 0


@pytest.mark.asyncio
async def test_session_round_trip_and_event_deduplication():
    redis = FakeRedis()
    store = CaptureSessionStore(redis)
    session = CaptureSession(
        channel_id="C1",
        root_thread_ts="100.1",
        session_id="provider-1",
        kind="idea",
        output_path="inbox/note.md",
        first_prompt="idea",
        created_at="2026-07-02T12:00:00+09:00",
        last_seen_at="2026-07-02T12:00:00+09:00",
    )
    await store.set(session)
    assert await store.get("C1", "100.1") == session
    assert await store.claim_event("Ev1") is True
    assert await store.claim_event("Ev1") is False


@pytest.mark.asyncio
async def test_thread_lock_is_exclusive_and_released():
    store = CaptureSessionStore(FakeRedis())
    async with store.lock("C1", "100.1"):
        with pytest.raises(ThreadBusyError):
            async with store.lock("C1", "100.1"):
                pass
    async with store.lock("C1", "100.1"):
        pass


def test_normalize_root_mention_and_followup():
    root = normalize_event(
        {"channel": "C1", "user": "U1", "ts": "100.1", "text": "<@UBOT> idea"},
        {"event_id": "Ev1", "team_id": "T1"},
        entrypoint="app_mention",
    )
    assert root.root_thread_ts == "100.1"
    assert root.text == "idea"
    followup = normalize_event(
        {"channel": "C1", "user": "U1", "ts": "100.2", "thread_ts": "100.1", "text": "보완"},
        {"event_id": "Ev2", "team_id": "T1"},
        entrypoint="thread_message",
    )
    assert followup.root_thread_ts == "100.1"
    assert followup.request_id == "Ev2"


class FakeAgentClient:
    def __init__(self, results):
        self.results = list(results)
        self.submits = []

    async def submit(self, prompt, **kwargs):
        self.submits.append((prompt, kwargs))
        return f"task-{len(self.submits)}"

    async def result(self, task_id, *, timeout):
        result, session_id = self.results.pop(0)
        return SimpleNamespace(result=json.dumps(result, ensure_ascii=False), result_session_id=session_id)


class FakeSlack:
    def __init__(self):
        self.messages = []
        self.updates = []

    async def chat_postMessage(self, **kwargs):
        self.messages.append(kwargs)
        return {"ts": f"bot.{len(self.messages)}"}

    async def chat_update(self, **kwargs):
        self.updates.append(kwargs)


def _idea_result(refined="첫 아이디어"):
    return {
        "schema_version": "1.0",
        "kind": "idea",
        "title": "Thread 아이디어",
        "slug": "thread-idea",
        "summary": "Thread에서 아이디어를 정리한다.",
        "tags": ["slack"],
        "intent": None,
        "source": None,
        "idea": {
            "original": "아이디어",
            "refined": refined,
            "problem": "기록이 어렵다.",
            "expected_value": "기록이 쉬워진다.",
            "open_questions": ["어떻게 검증할까?"],
        },
        "reference": None,
        "connection_candidates": [],
    }


def _reference_result():
    return {
        "schema_version": "1.0",
        "kind": "reference",
        "title": "지식 그래프 자료",
        "slug": "knowledge-graph-source",
        "summary": "지식 그래프를 설명한다.",
        "tags": ["knowledge-graph"],
        "intent": None,
        "source": {
            "url": "https://example.com/source",
            "type": "blog",
            "title": "Knowledge Graph",
            "author": "Author",
            "publisher": None,
            "published_at": None,
            "accessed_at": "2026-07-02T12:00:00+09:00",
            "external_id": None,
        },
        "idea": None,
        "reference": {
            "overview": "지식 그래프 개요",
            "context": "기술 블로그",
            "key_claims": ["링크가 관계를 표현한다."],
            "concepts": [{"name": "노드", "description": "지식 단위"}],
            "evidence": ["예시 그래프를 제시한다."],
            "applications": ["개인 지식 관리에 적용 가능하다."],
            "limitations": ["정량 검증은 없다."],
            "notes": "추가 자료 없음",
        },
        "connection_candidates": [],
    }


@pytest.mark.asyncio
async def test_runner_reuses_session_and_output_path(tmp_path):
    redis = FakeRedis()
    sessions = CaptureSessionStore(redis)
    client = FakeAgentClient([
        (_idea_result(), "session-1"),
        (_idea_result("보완된 아이디어"), "session-1"),
    ])
    slack = FakeSlack()
    runner = KnowledgeCaptureRunner(
        client,
        sessions,
        repo_root=tmp_path,
        provider="codex",
        model="gpt-test",
        work_dir=str(tmp_path),
        known_stems=set,
        allowed_groups=lambda: {"study"},
        store=FileCaptureStore(
            repo_root=tmp_path,
            publish=lambda _path: True,
            reload_data=lambda: True,
        ),
        now=lambda: datetime.fromisoformat("2026-07-02T12:00:00+09:00"),
    )
    root = normalize_event(
        {"channel": "C1", "user": "U1", "ts": "100.1", "text": "<@UBOT> 아이디어"},
        {"event_id": "Ev1", "team_id": "T1"},
        entrypoint="app_mention",
    )
    await runner.handle(root, slack)
    session = await sessions.get("C1", "100.1")
    assert session and session.output_path == "inbox/2026-07-02-thread-idea.md"
    followup = normalize_event(
        {"channel": "C1", "user": "U1", "ts": "100.2", "thread_ts": "100.1", "text": "보완"},
        {"event_id": "Ev2", "team_id": "T1"},
        entrypoint="thread_message",
    )
    await runner.handle(followup, slack)
    assert client.submits[1][1]["options"] == {
        "cwd": str(tmp_path),
        "resume": {"mode": "session", "session_id": "session-1"}
    }
    path = tmp_path / "inbox/2026-07-02-thread-idea.md"
    assert "보완된 아이디어" in path.read_text()
    assert len(list((tmp_path / "inbox").glob("*.md"))) == 1


@pytest.mark.asyncio
async def test_runner_writes_reference_and_requests_reload(tmp_path):
    sessions = CaptureSessionStore(FakeRedis())
    client = FakeAgentClient([(_reference_result(), "session-ref")])
    published = []
    reloaded = []
    runner = KnowledgeCaptureRunner(
        client,
        sessions,
        repo_root=tmp_path,
        provider="codex",
        model=None,
        work_dir=str(tmp_path),
        known_stems=set,
        allowed_groups=lambda: {"study"},
        store=FileCaptureStore(
            repo_root=tmp_path,
            publish=lambda path: published.append(path.relative_to(tmp_path).as_posix()) or True,
            reload_data=lambda: reloaded.append(True) or True,
        ),
        now=lambda: datetime.fromisoformat("2026-07-02T12:00:00+09:00"),
    )
    request = normalize_event(
        {"channel": "C1", "user": "U1", "ts": "200.1", "text": "<@UBOT> reference"},
        {"event_id": "EvRef", "team_id": "T1"},
        entrypoint="app_mention",
    )
    await runner.handle(request, FakeSlack())
    assert (tmp_path / "resources/source/2026-07-02-knowledge-graph-source.md").is_file()
    assert published == ["resources/source/2026-07-02-knowledge-graph-source.md"]
    assert reloaded == [True]


class QueueStore:
    """WORK-014 의 큐 store 를 흉내내는 fake — 파일도 push 도 하지 않는다.

    draft(본문 + 발행 예정 목적지)를 메모리에 들고 있다가 후속 대화에 돌려준다.
    실제 구현에서는 이 자리가 DB 큐 항목이 된다.
    """

    def __init__(self, repo_root):
        self.repo_root = repo_root.resolve()
        self.stored = []
        self.drafts = {}

    async def load_previous(self, session):
        ref = getattr(session, "output_path", None) if session else None
        if not ref or ref not in self.drafts:
            return EMPTY_PREVIOUS
        markdown, destination = self.drafts[ref]
        return PreviousCapture(markdown=markdown, output_override=destination)

    async def store(self, artifact):
        self.stored.append(artifact)
        ref = f"queue:{len(self.stored)}"
        destination = artifact.path.relative_to(self.repo_root)
        self.drafts[ref] = (artifact.rendered, destination)
        return StoreResult(location=ref, stored_ref=ref)


@pytest.mark.asyncio
async def test_runner_with_queue_store_writes_nothing(tmp_path):
    """store 교체만으로 '파일 쓰기' 를 끌 수 있어야 한다 (KDEV-WORK-014 가 갈아끼울 지점)."""
    sessions = CaptureSessionStore(FakeRedis())
    client = FakeAgentClient([(_idea_result(), "session-noop")])
    store = QueueStore(tmp_path)

    runner = KnowledgeCaptureRunner(
        client,
        sessions,
        repo_root=tmp_path,
        provider="codex",
        model=None,
        work_dir=str(tmp_path),
        known_stems=set,
        allowed_groups=lambda: {"study"},
        store=store,
        now=lambda: datetime.fromisoformat("2026-07-02T12:00:00+09:00"),
    )
    slack = FakeSlack()
    request = normalize_event(
        {"channel": "C1", "user": "U1", "ts": "300.1", "text": "<@UBOT> 아이디어"},
        {"event_id": "EvQueue", "team_id": "T1"},
        entrypoint="app_mention",
    )
    await runner.handle(request, slack)

    # 파일이 하나도 생기지 않는다
    assert list(tmp_path.rglob("*.md")) == []
    # store 는 렌더 결과와 목적지 경로를 그대로 받는다
    assert len(store.stored) == 1
    assert store.stored[0].path == tmp_path / "inbox/2026-07-02-thread-idea.md"
    assert store.stored[0].rendered.startswith("---")
    assert store.stored[0].request.channel_id == "C1"
    # 세션에는 store 가 준 불투명 참조가 실린다
    session = await sessions.get("C1", "300.1")
    assert session and session.output_path == "queue:1"
    assert "queue:1" in slack.updates[-1]["text"]


@pytest.mark.asyncio
async def test_queue_store_follow_up_reads_previous_from_store(tmp_path):
    """후속 대화의 '이전 초안' 을 store 가 공급한다 — runner 는 파일을 읽지 않는다."""
    sessions = CaptureSessionStore(FakeRedis())
    client = FakeAgentClient([
        (_idea_result(), "session-q"),
        (_idea_result("보완된 아이디어"), "session-q"),
    ])
    store = QueueStore(tmp_path)
    runner = KnowledgeCaptureRunner(
        client,
        sessions,
        repo_root=tmp_path,
        provider="codex",
        model=None,
        work_dir=str(tmp_path),
        known_stems=set,
        allowed_groups=lambda: {"study"},
        store=store,
        now=lambda: datetime.fromisoformat("2026-07-02T12:00:00+09:00"),
    )
    slack = FakeSlack()
    root = normalize_event(
        {"channel": "C1", "user": "U1", "ts": "400.1", "text": "<@UBOT> 아이디어"},
        {"event_id": "EvQ1", "team_id": "T1"},
        entrypoint="app_mention",
    )
    await runner.handle(root, slack)
    followup = normalize_event(
        {"channel": "C1", "user": "U1", "ts": "400.2", "thread_ts": "400.1", "text": "보완"},
        {"event_id": "EvQ2", "team_id": "T1"},
        entrypoint="thread_message",
    )
    await runner.handle(followup, slack)

    # 두 번째 프롬프트에 store 가 준 이전 초안이 실려 있다
    second_prompt = client.submits[1][0]
    assert "첫 아이디어" in second_prompt
    # 여전히 파일은 없고, 같은 목적지로 갱신된다
    assert list(tmp_path.rglob("*.md")) == []
    assert len(store.stored) == 2
    assert store.stored[1].replace is True
    assert store.stored[1].path == store.stored[0].path

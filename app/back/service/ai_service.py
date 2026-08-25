"""AI 실행 — open-kknaks 경유 codex (inbox.md Step 6). SDK 직접 호출 금지(ADR-04).

back 은 `AgentClient` 로 redis 에 제출만 하고, 실행은 호스트 워커가 한다
(`scripts/run-worker.sh`). 같은 세션을 이어서 두 번 부른다 —
문서 생성(새 세션)이 session_id 를 남기고, 개념 생성이 resume 으로 이어받는다.

- 격리는 워커 컨테이너 + /ledger ro 마운트가 맡는다 — codex 자체 sandbox(bwrap)는
  컨테이너 안에서 안 뜬다(아래 _build_run_options 주석). md 는 서버 검증 통과 시점에
  back 이 쓴다(문서 자동 착지 — 케이스 1, 2026-08-25 개정)
- output_schema(파일 경로 — codex_adapter 가 --output-schema 로 넘긴다)로
  출력 모양을 강제한다 — 파싱 없이 gate.payload 에 꽂힌다
- 템플릿은 back 이 kind 로 고른다 — cwd 가 원장 레포라 codex 가 직접 읽는다
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from config import get_settings
from service.fetch_service import FetchedSource

# 프롬프트에 넣는 원료(자막·본문) 상한 — codex 컨텍스트 보호.
_SOURCE_CAP = 60_000

_CONCEPT_AREAS = "ai · back · cs · db · design · front · infra · pm · qa"


class AIError(Exception):
    """제출·실행·파싱 실패 — queue.failed + error 한 줄로 끝난다."""


@dataclass(frozen=True)
class AIDocument:
    payload: dict          # gate(document).payload — {stem, body, meta?}
    session_id: str | None # queue.ai_session_id — 개념 생성이 resume 한다


_client = None
_broker = None


async def _get_client():
    """AgentClient 싱글턴 — broker 연결은 첫 제출 때 한 번."""
    global _client, _broker
    if _client is None:
        from open_kknaks import AgentClient, RedisBroker

        settings = get_settings()
        _broker = RedisBroker(
            url=settings.redis_url, namespace=settings.ai_namespace
        )
        await _broker.connect()
        _client = AgentClient(broker=_broker)
    return _client


def _build_run_options(
    settings, schema_file: str, resume_session_id: str | None
) -> tuple[dict, dict]:
    """문서·개념(resume) 두 호출의 실행 옵션 — **여기 하나로만 만든다**.

    개념 턴이 문서 턴과 다른 옵션으로 나가 bwrap 사고가 재발하는 것을 막는
    공용 빌더다(2026-08-25 실사고 — 개념 resume 턴만 sandbox·cwd 가 빠져
    exec 전부 실패 + workdir /app).

    resume 의 함정(codex-cli 0.147 실측): `codex exec resume` 은 `--sandbox`·`--cd` 를
    안 받는다 — codex_adapter 가 resume 모드에서 두 값을 떨궈서, 옵션에 넣어도
    새 세션과 같은 플래그로는 안 나간다. 그래서:
    - sandbox 는 `-c sandbox_mode=…`(config)로도 싣는다 — resume 서브커맨드가 받는
      유일한 통로다(--strict-config 로 검증). 새 세션에선 --sandbox 와 중복이지만
      같은 값이라 무해하다.
    - cwd 는 config 로도 못 넣는다(`-c cwd=…` 는 unknown field — 실측). resume 턴의
      workdir 는 워커 프로세스 cwd(/app)로 남으므로, 프롬프트가 원장 루트 기준
      **절대 경로**를 쓰는 것으로 보완한다(_concept_prompt).
    """
    options: dict = {"cwd": settings.ai_cwd, "timeout_sec": settings.ai_timeout_sec}
    if resume_session_id:
        options["resume"] = {"mode": "session", "session_id": resume_session_id}

    provider_options: dict = {
        # "read-only" 가 아닌 이유(2026-08-25 실측): 워커가 도커 컨테이너로 가면서
        # codex 의 리눅스 sandbox(bwrap)가 매 exec_command 에서
        #   「bwrap: No permissions to create a new namespace, likely because the
        #    kernel does not allow non-privileged user namespaces.」
        # 로 죽었다(도커 기본 seccomp 이 unprivileged userns 를 막는다 — 세션 로그
        # rollout-2026-08-25T09-20-08-*.jsonl). codex 는 셸이 전부 막힌 채 웹 검색으로
        # 표류해 「작업 중단 사유문」을 초안으로 냈다(queue 6·7 실사고).
        # 격리는 이미 컨테이너 자체 + /ledger ro 마운트가 맡는다(docker-compose.yml)
        # — codex 겹사포는 끄고 컨테이너 경계를 격리로 삼는다.
        "sandbox": "danger-full-access",
        # resume 경로 — 위 머리 주석. adapter 가 "sandbox" 를 떨궈도 이 config 는 남는다.
        "config": ['sandbox_mode="danger-full-access"'],
        "color": "never",
        "output_schema": str(Path(settings.ai_schema_dir) / schema_file),
        # 워커 컨테이너의 /ledger 는 이 맥에선 linked worktree 라 .git 이 컨테이너
        # 밖을 가리킨다 — codex 의 git repo 신뢰 검사가 resume 에서 실패한다(실측).
        # sandbox 가 read-only 라 검사의 보호 대상(쓰기)이 없으므로 끈다.
        "skip_git_repo_check": True,
    }
    return options, provider_options


async def _run_codex(
    prompt: str, schema_file: str, resume_session_id: str | None = None
) -> tuple[dict, str | None]:
    """제출 → 완료 대기 → JSON 파싱. (payload, session_id) 를 돌려준다."""
    settings = get_settings()
    client = await _get_client()

    options, provider_options = _build_run_options(
        settings, schema_file, resume_session_id
    )
    task_id = await client.submit(
        prompt,
        queue=settings.ai_queue,
        provider="codex",
        model=settings.ai_model,
        options=options,
        provider_options=provider_options,
    )
    task = await client.result(task_id, timeout=settings.ai_timeout_sec + 60)
    if task is None:
        raise AIError("AI 태스크를 못 찾음 — 워커가 떠 있는지 확인")
    if task.status != "done" or (task.exit_code or 0) != 0:
        detail = (task.error or "").strip().splitlines()
        raise AIError(
            f"AI 실행 실패(status={task.status}): {detail[-1] if detail else 'exit_code=' + str(task.exit_code)}"
        )
    if not task.result:
        raise AIError("AI 가 빈 결과를 냄")
    try:
        payload = json.loads(task.result)
    except json.JSONDecodeError as exc:
        raise AIError(f"AI 출력이 schema JSON 이 아님: {exc}") from exc
    if not isinstance(payload, dict):
        raise AIError("AI 출력이 JSON object 가 아님")
    return payload, task.result_session_id


def _clip(text: str) -> str:
    return text if len(text) <= _SOURCE_CAP else text[:_SOURCE_CAP] + "\n…(잘림)"


def _document_prompt(
    kind: str, url: str, note: str | None, source: FetchedSource
) -> str:
    lines = [
        f"자료 캡처 파이프라인의 문서 초안을 만든다. 종류는 `{kind}` 다.",
        "",
        f"1. 먼저 `templates/resources/{kind}.md` 를 읽어라. 초안은 그 양식의 절 구성"
        " **그대로** 따른다 — 머리(H1 + 출처 줄)부터 본문 절 순서·제목까지. 섹션을"
        " 비워 두지 않는다.",
    ]
    if kind == "youtube":
        lines += [
            # 채번 지시는 남기지만 **신뢰하지 않는다** — codex 가 원장을 못 읽고 엉터리
            # 번호를 낸 실사고(C-000·C-001, 2026-08-25) 이후 번호는 서버가 강제한다
            # (inbox_service._force_youtube_number). 여기 지시는 slug 품질용일 뿐이다.
            "2. 파일명 stem 은 `C-NNN-<slug>` — `para/resources/youtube/` 의 기존 파일명을"
            " 보고 NNN 은 최대값 + 1, slug 는 내용을 요약한 영문 kebab-case 로 정한다.",
            "3. meta 는 DB content 행의 카드 메타다 — 아래 「원료 메타」를 쓰되 비어 있으면"
            " 자막에서 합리적으로 추론해 채운다. summary 는 카드에 실릴 1~2문장.",
        ]
    else:
        lines += [
            "2. 파일명 stem 은 내용을 요약한 영문 kebab-case slug 로 정한다 —"
            " 한국어·대문자·날짜 없이. `para/resources/" + kind + "/` 의 기존 파일과"
            " 겹치지 않게 한다.",
        ]
    lines += [
        "",
        "출력은 강제된 JSON schema 를 따른다. body 는 md 전문이다.",
        "",
        "## 캡처 정보",
        f"- URL: {url}",
        f"- 사용자 메모: {note or '(없음)'}",
    ]
    if kind == "youtube":
        lines += [
            "",
            "## 원료 메타",
            f"- 제목: {source.title or '(모름)'}",
            f"- 채널: {source.channel or '(모름)'}",
            f"- 길이: {source.duration or '(모름)'}",
            f"- 게시일: {source.published_on or '(모름)'}",
            f"- youtubeId: {source.youtube_id}",
            "",
            "## 자막 전문",
        ]
    else:
        lines += ["", "## 크롤링 본문"]
    lines += ["", "```", _clip(source.text), "```"]
    return "\n".join(lines)


def _concept_prompt(kind: str, stem: str, body: str, root: str) -> str:
    # root(원장 루트, 워커 기준 = settings.ai_cwd)를 모든 경로에 박는 이유:
    # resume 턴은 `--cd` 가 안 먹혀 workdir 가 복원되지 않는다(_build_run_options).
    return "\n".join(
        [
            "방금 만든 문서 초안이 서버 검증을 거쳐 원장에 착지 확정됐다."
            " **기준은 아래 착지 확정본이다** — 세션에서 만든 초안과 다르면 확정본을 따른다.",
            "",
            "이제 이 문서에서 자란 개념의 신규/보강안을 만든다.",
            "",
            f"이 턴은 작업 디렉토리가 원장 레포가 아닐 수 있다. 원장 루트는 `{root}` 다 —"
            " 아래 경로는 전부 이 루트 기준 절대 경로로 접근하라.",
            "",
            f"1. `{root}/para/areas/area.md` 의 3.3 절(개념 규약)을 읽고 판정 기준을 따른다.",
            f"2. `{root}/para/areas/concept/` ({_CONCEPT_AREAS}) 를 탐색해 이미 있는 개념인지"
            " 먼저 찾는다. 한국어·약어는 영문 stem 에 안 걸리므로"
            f" `grep -rn \"aliases:\" -A6 {root}/para/areas/concept/` 로 aliases 도 본다.",
            "3. **이미 있으면 mode=supplement** — 새 파일을 만들지 않는다. 기존 파일에"
            " `up:` 출처(이 문서 stem)를 더하고 더해진 내용을 본문에 녹인 **파일 전체**를"
            " body 로, 기존 파일 대비 unified diff 를 diff 로 낸다.",
            f"4. **없으면 mode=create** — `{root}/templates/areas/concept.md` 양식으로 새 본문을"
            " body 에 낸다(안내문 줄은 지운다). `up:` 은 이 문서 stem. diff 는 빈 문자열.",
            "5. stem 은 영문 kebab-case, area 는 아홉 영역 중 하나. 개념이 없으면"
            " concepts 를 빈 배열로 낸다 — 억지로 만들지 않는다.",
            "",
            "출력은 강제된 JSON schema 를 따른다.",
            "",
            f"## 착지 확정본 — `para/resources/{kind}/{stem}.md`",
            "",
            "```markdown",
            body,
            "```",
        ]
    )


async def generate_document(
    kind: str, url: str, note: str | None, source: FetchedSource
) -> AIDocument:
    """문서 초안 — 새 codex 세션. payload 는 {stem, body}(+ youtube 는 meta)."""
    schema = "document_youtube.json" if kind == "youtube" else "document.json"
    payload, session_id = await _run_codex(
        _document_prompt(kind, url, note, source), schema
    )
    if not payload.get("stem") or not payload.get("body"):
        raise AIError("AI 문서 초안에 stem/body 가 비어 있음")
    return AIDocument(payload=payload, session_id=session_id)


async def generate_concepts(
    kind: str, stem: str, body: str, session_id: str | None
) -> dict:
    """개념 보강안 — 문서 생성 세션을 resume 하고 착지 확정본을 동봉한다."""
    if not session_id:
        raise AIError("ai_session_id 가 없음 — 문서 생성 세션을 resume 할 수 없다")
    settings = get_settings()
    payload, _ = await _run_codex(
        _concept_prompt(kind, stem, body, settings.ai_cwd),
        "concept.json",
        resume_session_id=session_id,
    )
    if not isinstance(payload.get("concepts"), list):
        raise AIError("AI 개념안에 concepts 배열이 없음")
    return payload

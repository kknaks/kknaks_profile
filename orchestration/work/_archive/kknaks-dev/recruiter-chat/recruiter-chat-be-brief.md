
# [backend] 채용담당자 채팅 서버 — 세션·대화 API · MCP 서버 · 제출·소비자 (KDEV-WORK-023)

너는 **kknaks-dev `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/agent/orchestration/roles/kknaks-dev/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/recruiter-chat`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

⚠ **FE 워커가 같은 워크트리의 `app/front/` 에서 병렬 작업 중** — `app/front/` 는 읽기만 하고 절대 수정하지 마라.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/agent/para/projects/summer-star/kknaks-dev/20-spec/spec-017-recruiter-chat.md` ← **계약의 SoT. 여기 없는 건 발명하지 마라.** (§3 서버 시나리오 · §4 API/폴링/쿠키/Tool Contract · §5 구현 규칙)
- `/Users/kknaks/orca/workspaces/kknaks_profile/agent/para/projects/summer-star/kknaks-dev/30-work/work-023-recruiter-chat-backend.md` ← 이번 작업의 빌드 계획 (Phase 1~4 · Code Surface · Pre-deploy Check)
- `/Users/kknaks/orca/workspaces/kknaks_profile/agent/para/projects/summer-star/kknaks-dev/10-decision/decision-027-chat-ai-execution-and-tool-boundary.md` ← 왜 이 구조인지 (D1~D6)
- `/Users/kknaks/orca/workspaces/kknaks_profile/agent/para/projects/summer-star/kknaks-dev/10-decision/decision-026-anonymous-visitor-session.md` ← 세션 결정 (D1~D3)

**기대는 개념** — 이 작업이 따를 판단 기준:

- `/Users/kknaks/orca/workspaces/kknaks_profile/agent/para/areas/concept/ai/ai-agent.md` — tool 은 「용도가 새겨진 손」이다. tool 이름·설명·스키마가 모델의 선택 품질을 정한다 — MCP tool 설명을 성의 있게 써라
- `/Users/kknaks/orca/workspaces/kknaks_profile/agent/para/areas/concept/back/http-session.md` — 익명 세션의 구조가 정확히 이것이다. 상태는 서버, 클라이언트는 열쇠(쿠키)만

## 2. 배경 / 무엇을 바꾸나

포트폴리오 사이트(kknaks.dev) 홈을 채팅 퍼스트로 재구성한다. 로그인 없는 채용담당자가
질문하면 codex 가 MCP tool 로 공개 이력 데이터(career·projects·problem)를 읽고 1인칭으로
대답한다. 이 레포에는 이미 open-kknaks 워커 파이프라인(`service/ai_service.py` — submit→result,
resume)이 돌고 있다 — 채팅은 그 인프라를 **전용 `chat` 큐**로 재사용하되, 이벤트 스트림
구독(상주 소비자) 방식으로 실시간 폴딩한다.

**검증된 레퍼런스가 있다**: `/Users/kknaks/git/harness_works/mediness-app` (읽기 전용) —
같은 스택(open-kknaks + codex + MCP)의 사내 구현. 특히:
- `back/app/services/landing_chat/consumer.py` — 이벤트 폴딩·중복수신 멱등·2단 복구·Redis lock
- `back/app/services/landing_chat/submission.py` — `-c` 오버라이드 조립 (모델 정식표기·resume 함정·shell off 전부 주석에 실측 근거)
- `back/app/services/landing_chat/runtime.py` — 커밋 뒤 제출·백그라운드 task 참조 보관
- `mcp/app/` — HTTP MCP 서버 구조 (server.py·auth.py·back_client.py·tool_access.py)
이식하되 **얇게** — 저긴 사용자 JWT·조직권한이 얽혀 있지만 여긴 익명 + 공개 데이터다.
turn 토큰은 우리 스스로 발급·검증하는 불투명 토큰이면 된다(JWT family 기계 불필요).

## 3. 계약 (FE 와 합의됨 — 이대로 제공. 필드명 임의 변경 금지)

SPEC-017 §4 가 전문이다. 요지:

- `GET /api/chat/conversations` — 쿠키 없으면 **세션 만들지 말고** 빈 목록
- `POST /api/chat/conversations` `{question}` → 201 `{conversation:{id,title,createdAt}, messages:[user, assistant(pending)]}` + 세션 없으면 `Set-Cookie chat_sid`(httpOnly·Lax·Secure·30일 sliding)
- `GET /api/chat/conversations/{id}` → `{conversation, messages}` — message = `{id, role, status(pending|done|failed), content, sources:[{type,slug,title,url}], steps:[{tool,argsSummary,durationMs,calledAt}], createdAt}`. **pending 중에도 content(부분 누적)·steps 가 채워진다**
- `POST /api/chat/conversations/{id}/messages` `{question}` → 201. pending 있으면 409 `CONVERSATION_BUSY`
- `PATCH /api/admin/chat-exposure/{kind}/{id}` — admin 인증(기존 방식), `chat_exposed` 토글
- validation: question trim 1~1000자(422 `EMPTY_QUESTION`/`QUESTION_TOO_LONG`) · 남의 세션 대화 404
- MCP tool 10종: `get_profile`·`list_career`·`get_career`·`list_projects`·`get_project`·`list_problems`·`get_problem`·`search_notes`·`get_note`·`list_contents`·`list_algorithms` — 전부 read-only·slug 인자만, `chat_exposed=false` 는 목록 제외·상세 404

## 4. 먼저 읽을 핵심 파일 (워크트리 안)

- `app/back/service/ai_service.py` — 기존 제출 패턴 + resume·sandbox 함정이 주석에 있다. 채팅 제출부는 이 옆에 새로 만든다(기존 파이프라인 무변경)
- `app/back/Dockerfile.worker` · `app/back/docker-compose*.yml` — 워커 기동 계약(codex 런타임 마운트·CODEX_HOME)
- `app/back/api/deps.py` + admin 계열 라우터 1개 — 인증·계층 관례
- `app/back/models/` 아무 모델 1개 + `app/back/alembic/versions/` 최근 1개 — 모델·마이그레이션 관례
- `app/back/config.py` — 설정 추가 위치

## 5. allowed_paths — 이 밖은 건드리지 마라

- `app/back/`
- `app/mcp/`

## 6. 구현 단계 (work-023 의 Phase 그대로)

1. **P1 스키마·세션·대화 API**: 모델 3(`chat_session` 1:N `conversation` 1:N `chat_message`) + migration(+ career·project·problem 에 `chat_exposed` boolean 기본 false) → 쿠키 발급/검증 → 공개 API 4종 + admin 토글 (AI 는 스텁 — pending 만 만든다)
2. **P2 chat-tool API + MCP 서버**: 노출 판정 조회 API → `app/mcp/` HTTP MCP 서버(tool 10종 + turn Bearer 검증)
3. **P3 제출부**: SubmissionPlan 조립(`gpt-5.6-terra`·queue=chat·timeout 180·resume·MCP url/토큰/allowlist/approval_mode·`features.shell_tool=false`·`web_search="disabled"`·`features.apps=false`·`sandbox=read-only`·`skip_git_repo_check`) + turn 토큰 발급/폐기 + 시스템 프롬프트(§5 프롬프트 계약)
4. **P4 소비자 + compose**: 상주 소비자(이벤트 폴딩 — text 누적/재생 초기화·tool_use_id 멱등 upsert·문서 계열 tool_result 에서 sources 추출·init→ai_session_id·result 교체 done·실패/timeout→failed·기동 시 pending 스윕) + compose 에 chat 워커(전용 CODEX_HOME·마운트 없음)와 mcp 서비스 추가
5. work-023 문서의 Phase Status·완료 증거는 **네가 갱신하지 않는다**(코디네이터 몫) — 보고에 Phase 별 결과만 적어라

## 7. 범위 제약 — 하지 말 것

- `app/front/`·`para/`·`orchestration/` 수정 금지
- 기존 파이프라인(`ai_service.py`·기존 워커 compose 서비스·queue=default) 변경 금지
- open-kknaks 라이브러리 수정 금지 · LLM SDK 직접 import 금지(ADR-04)
- spec 에 없는 엔드포인트·필드 발명 금지. 어긋남 발견 시 질문 채널로 보고
- 레이트리밋·WS·어드민 대화 열람 화면은 범위 밖
- `.env` 실값 커밋 금지(예시 파일만)

## 8. 검증

```
cd app/back && uv run pytest -q <네가 만들거나 고친 테스트 파일만> (전체 스위트 금지 — 사용자 방침). 검증은 1회만 — 통과하면 반복하지 마라
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_53806a6d-ced5-4948-88bd-4181b7ba4323 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_53806a6d-ced5-4948-88bd-4181b7ba4323 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_53806a6d-ced5-4948-88bd-4181b7ba4323 --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)

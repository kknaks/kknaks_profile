---
type: work
id: KDEV-WORK-023
title: "채용담당자 채팅 BE — 세션·대화 API · MCP 서버 · 제출·소비자"
status: done
product: kknaks-dev
work_type: new-feature
owner: kknaks
roles:
  pm: "kknaks"
  design: "—"
  fe: "—"
  be: "worker:backend"
  qa: "coordinator"
  ops: "kknaks"
progress: 100
created_at: 2026-08-28
updated_at: 2026-08-28
tags:
  - product/kknaks-dev
  - doc/work
  - status/done
links:
  baselines:
    - "[[baseline-008-recruiter-chat|KDEV-BL-008]]"
  decisions:
    - "[[decision-026-anonymous-visitor-session|KDEV-DEC-026]]"
    - "[[decision-027-chat-ai-execution-and-tool-boundary|KDEV-DEC-027]]"
  specs:
    - "[[spec-017-recruiter-chat|KDEV-SPEC-017]]"
  works: []
  releases: []
  related: []
---

# 채용담당자 채팅 BE — 세션·대화 API · MCP 서버 · 제출·소비자

SPEC-017 의 서버 전부 — 익명 세션 쿠키, conversation/message API, `chat_exposed`
플래그 + chat-tool API, HTTP MCP 서버, codex 제출(-c 오버라이드)과 상주 소비자(이벤트
폴딩). **비목표**: 프론트 화면(WORK-024) · 레이트리밋(DEC-026 OQ-1) · WS 푸시.

## Meta

- Baseline: KDEV-BL-008
- Covers spec: KDEV-SPEC-017 (§3 S-1~S-9 서버 측 · §4 전체 · §5)
- Depends on work: 없음
- Parallel work: WORK-024 (FE — API 계약은 spec 으로 고정, mock 으로 병행)
- Follow-up work: 레이트리밋 · 어드민 대화 열람
- External dependency: open-kknaks 2.1.2(설치본 그대로) · codex CLI 런타임 마운트
  (기존 Dockerfile.worker 체계) · **레퍼런스 구현**
  `/Users/kknaks/git/harness_works/mediness-app` (읽기 전용 — landing_chat 서비스 ·
  mcp/ 서버 · submission/-c 오버라이드. 이식하되 익명·공개 데이터 규모로 얇게)

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | kknaks |
| Status | done |
| Progress | 100% |
| Branch/PR |  |
| Blocker |  |
| Next | PR (코디네이터) |

## Scope

포함:

- `chat_session` · `conversation` · `chat_message` 모델 + alembic migration
- 익명 세션 쿠키(`chat_sid`, httpOnly · Lax · Secure · 30일 sliding) 발급/검증
- 공개 chat API 4종 + admin `chat_exposed` 토글 1종 (SPEC-017 §4 계약 그대로)
- career · project · problem 에 `chat_exposed` 컬럼(기본 false) + chat-tool 조회 API
- HTTP MCP 서버(`app/mcp/`) — tool 10종, turn Bearer 토큰 검증
- 제출부(-c 오버라이드: MCP url·토큰·allowlist·approval_mode·shell off,
  모델 `gpt-5.6-terra`, `queue=chat`, timeout 180초, resume) + turn 토큰 발급/폐기
- 상주 소비자 — 이벤트 폴딩(text 누적 · tool_use_id 멱등 · init 세션 확정 ·
  result 마감 · failed 마감), 기동 시 pending 스윕 복구
- compose: 채팅 워커(`queue=chat`, CODEX_HOME 분리, 마운트 없음) + mcp 서비스

제외:

- 프론트(WORK-024) · 레이트리밋 · WS/SSE · 어드민 대화 열람 화면

## Code Surface

- Repo / module: `kknaks_profile` — `app/back/` · `app/mcp/`(신설)
- 만질 파일 후보:

| 경로 후보 | 설명 |
|---|---|
| `app/back/models/chat.py` | chat_session · conversation · chat_message |
| `app/back/alembic/versions/*` | 신규 테이블 + chat_exposed 컬럼 |
| `app/back/api/chat_router.py` | 공개 chat API 4종 |
| `app/back/api/chat_tool_router.py` | MCP 가 부르는 chat-tool 조회 API |
| `app/back/api/admin(기존 라우터)` | chat_exposed 토글 |
| `app/back/service/chat/` | 세션 · 대화 · 제출 · 소비자 · turn 토큰 |
| `app/back/config.py` | chat 설정(모델 · 큐 · timeout · MCP url) |
| `app/mcp/` | HTTP MCP 서버 (신설 — mediness `mcp/` 축소 이식) |
| `app/back/docker-compose*.yml` | chat 워커 · mcp 서비스 |

- Domain / schema note: migration 필요. 컬럼 전문은 migration 이 SoT.

## Domain / Schema

| Entity | 역할 |
|---|---|
| `chat_session` | 익명 방문자 1명 (쿠키 토큰 해시, last_seen) |
| `conversation` | 대화 1건 — 제목 · `ai_session_id` · 소속 세션 |
| `chat_message` | 메시지 — role · status(pending/done/failed) · content · sources · steps |

- 상태 / invariant: 한 conversation 에 pending assistant 최대 1 (직렬화 — DB 로 강제)
- Migration 필요 여부: 필요 (신규 3 테이블 + 기존 3 테이블 chat_exposed)
- SPEC 환류: steps/sources 필드 모양이 spec §4 와 어긋나면 spec 개정 필요 — 임의
  변경 금지, 코디네이터에 보고

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| WORK-024 (FE) | SPEC-017 §4 API | FE 는 이 계약만 본다 — 응답 필드명 임의 변경 금지 |
| chat 워커(codex) | MCP tool 10종 | 이름·인자 = SPEC-017 §4 Tool Contract |

## Execution

### Phase 1 — 스키마 · 세션 · 대화 API (AI 스텁)

- **Status**: DONE
- **설명**: FE 와 소비자가 딛는 토대. AI 는 아직 없다 — assistant 메시지는 pending
  으로 만들어만 둔다.
- **작업**:
  - [ ] 모델 3 + migration, `chat_exposed` 컬럼 migration
  - [ ] 세션 쿠키 발급/검증(deps) — 발급은 POST conversations 에서만
  - [ ] chat API 4종 + Case Matrix 에러(422/404/409) — router→service→repository 계층 준수
  - [ ] admin chat_exposed 토글
- **검증**:
  - [ ] 새 테스트: 쿠키 발급 시점 · 소유권 404 · busy 409 · validation 422
  - [ ] `uv run pytest -q <새 테스트 파일>` 통과
- **완료 증거**: 2026-08-28 — 워커 구현 + fix1(리뷰 W1~W7)·fix2(제출-커밋 순서) 반영. back 133 · mcp 24 passed(코디 재현), 로컬 compose e2e 완주(15~20초, tool 폴딩·근거·resume·retry 실동작). 상세는 orchestration/work/recruiter-chat/

### Phase 2 — chat-tool API + MCP 서버

- **Status**: DONE
- **설명**: AI 의 손. 노출 판정이 매 호출 DB 에서 돈다.
- **작업**:
  - [ ] chat-tool 조회 API — 목록은 chat_exposed 만, 상세는 미노출 404, slug 는
        `detail_path` 해석 + 공개 루트 밖 거부
  - [ ] `app/mcp/` HTTP MCP 서버 — tool 10종(SPEC-017 §4 표), turn Bearer 검증,
        back 호출 클라이언트 (mediness `mcp/app/` 구조 이식·축소)
- **검증**:
  - [ ] 새 테스트: 노출 토글 반영 · 미노출 404 · 경로 이탈 거부 · 무토큰 거부
- **완료 증거**: 2026-08-28 — 워커 구현 + fix1(리뷰 W1~W7)·fix2(제출-커밋 순서) 반영. back 133 · mcp 24 passed(코디 재현), 로컬 compose e2e 완주(15~20초, tool 폴딩·근거·resume·retry 실동작). 상세는 orchestration/work/recruiter-chat/

### Phase 3 — 제출부 + turn 토큰

- **Status**: DONE
- **설명**: 질문 → codex 태스크. mediness `submission.py` 의 검증된 -c 계약을 그대로.
- **작업**:
  - [ ] SubmissionPlan 조립 — 모델 `gpt-5.6-terra` · `queue=chat` · timeout 180 ·
        resume(conversation.ai_session_id) · MCP url/토큰/allowlist/approval_mode ·
        `features.shell_tool=false` · `web_search="disabled"` · `features.apps=false` ·
        `sandbox=read-only` · `skip_git_repo_check`
  - [ ] turn 토큰 발급(제출 시)/폐기(마감 시 best-effort) — MCP 서버와 검증 계약 공유
  - [ ] 시스템 프롬프트(§5 프롬프트 계약 — 1인칭 · 기록에 없으면 없다고 · 거절 규칙)
- **검증**:
  - [ ] 새 테스트: 제출 옵션 조립(-c 목록 · resume 유/무) · 토큰 로그 마스킹
- **완료 증거**: 2026-08-28 — 워커 구현 + fix1(리뷰 W1~W7)·fix2(제출-커밋 순서) 반영. back 133 · mcp 24 passed(코디 재현), 로컬 compose e2e 완주(15~20초, tool 폴딩·근거·resume·retry 실동작). 상세는 orchestration/work/recruiter-chat/

### Phase 4 — 상주 소비자 + compose

- **Status**: DONE
- **설명**: 이벤트 폴딩. mediness `consumer.py` 의 folding·중복수신·복구 패턴 이식.
- **작업**:
  - [ ] 태스크 전용 소비자 — text 누적(재생 시 초기화) · tool_use/tool_result
        `tool_use_id` 멱등 upsert(+durationMs·argsSummary 서버 생성) · 문서 계열
        tool_result 에서 sources 추출 · init → ai_session_id · result 교체+done ·
        실패/timeout → failed · asyncio task 참조 보관
  - [ ] 기동 시 pending 스윕(재생 복구 → 안 되면 result 회수 마감)
  - [ ] compose: chat 워커 서비스(전용 CODEX_HOME · 마운트 없음 · queue=chat) +
        mcp 서비스. 기존 워커·서비스 무변경
- **검증**:
  - [ ] 새 테스트: 폴딩 멱등(같은 이벤트 2회 = 같은 결과) · 재생 초기화 · failed 마감
  - [ ] `uv run pytest -q <이 work 의 새 테스트 전부>` 통과
- **완료 증거**: 2026-08-28 — 워커 구현 + fix1(리뷰 W1~W7)·fix2(제출-커밋 순서) 반영. back 133 · mcp 24 passed(코디 재현), 로컬 compose e2e 완주(15~20초, tool 폴딩·근거·resume·retry 실동작). 상세는 orchestration/work/recruiter-chat/

## Pre-deploy Check

- [ ] 기존 파이프라인 워커(`queue=default`) 계약 무변경 — diff 로 확인
- [ ] chat-tool·MCP 응답에 비공개 필드(내부 경로 · 게이트 · 토큰) 없음
- [ ] turn 토큰이 로그에 원문으로 남지 않음
- [ ] `.env` 신규 키는 예시 파일에만, 실값 커밋 없음

## Rollback

- 라우터 미등록 + compose 서비스 제거로 표면이 사라진다. migration revert 는
  alembic downgrade 1스텝(신규 테이블 drop + 컬럼 drop).

## Done Criteria

- [ ] 모든 Phase DONE
- [ ] SPEC-017 AC 중 서버 측 항목이 테스트로 커버
- [ ] product `log.md` · `30-work/README.md` 갱신 (코디네이터)

## Open Issues

- MCP 서버 프레임워크(FastMCP vs mediness 방식 그대로)는 코드 조사 후 워커가 정하고
  브리프 완료 보고에 근거를 남긴다.

## Related

- SPEC: KDEV-SPEC-017 · Work: WORK-024(FE, 병렬)

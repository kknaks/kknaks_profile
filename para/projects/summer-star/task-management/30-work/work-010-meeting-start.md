---
type: work
id: WORK-010
title: "회의 시작 — `/start` 는 전이만 · 웜스타트는 컨텍스트 없이 백그라운드"
status: done
product: "task-management"
work_type: refactor
owner: ""
roles:
  pm: ""
  design: ""
  fe: ""
  be: ""
  qa: ""
  ops: ""
progress: 100
created_at: 2026-09-07
updated_at: 2026-09-07
tags:
  - product/task-management
  - doc/work
  - status/done
links:
  baselines: [BASE-003]
  decisions: [DEC-003]
  specs: [SPEC-006, SPEC-007]
  works: [WORK-006, WORK-007, WORK-009]
  releases: []
  related: [WORK-011, WORK-012]
---

# 회의 시작 — `/start` 는 전이만 · 웜스타트는 컨텍스트 없이 백그라운드

**「회의 시작」이 13초 도는 것을 끝낸다.** 지금 `start()` 는 컨텍스트를 모아 commit 하고 **codex 웜스타트를 요청 안에서 기다린다**(`meeting_service.py` L515~). 이 work 가 끝나면 `/start` 는 **전이 + 토큰 INSERT 한 트랜잭션**뿐이고, 웜스타트는 **commit 뒤 백그라운드 태스크**가 던지며 **컨텍스트를 싣지 않는다** — 역할 · 흐름 · 요약 원칙 · 용어 다섯 · 도구 목록뿐이다. **실패 처리를 만들지 않는다**(MF-70).

> 1 파일 = 1 work = **빌드 계획**. dev 가 이 문서만 보고 PR 분리 / 일정 / 작업 시작이 가능해야 한다.
> SPEC 의 외부 계약 본문은 복제하지 않고 frontmatter `links.specs` 와 index 에서 연결한다.
> **결정 원본은 `reference/2026-09-06-task-management-app/Meeting flow.md`** — **MF-1 · MF-55 · MF-70**(그리고 웜스타트가 컨텍스트를 안 싣는 근거 MF-50). 계약과 부딪히면 그쪽이 이긴다.

## Meta

- Baseline: BASE-003 §Raw L37(시작 전 AI 는 아무것도 하지 않는다) · #5(회의 시작)
- Covers spec
  - **SPEC-006 §4 `POST /api/meetings/{id}/start`**(→ `200 MeetingDetail` · 전이 + `recordingStartedAt` · 즉시 응답) · **§4 「상태별 허용 표」 `/start` 행** · **§4 구현 규칙 L647**(외부 호출을 요청 안에서 하지 않는다) · **U-4 CTA 「회의 시작」**
  - **SPEC-007 §4 「AI 배치 계약」 → 「웜스타트」 표 5행 전부**(시점 · 세션 · 주는 것 · 싣지 않는 것 · 실패) · **§5 「웜스타트는 `/start` 밖에서 돈다」 · 「배치 트리거 … `ai_session_id` 가 없으면 제출하지 않는다」** · **§4 Case Matrix 「웜스타트 미완료·실패(`ai_session_id` 없음)」 행** · **§6 AC 「워커를 내린 채 「회의 시작」을 눌러도 **즉시** 회의 중 화면이 되고 …」**
  - **DEC-003 §4**(상태 흐름 · 회의 시작) · **§7**(웜스타트 미완료·실패 — 처리 없음) · **§8**(AI 도구 연결 — 용어 다섯의 뜻)
- Depends on work: **WORK-009**(`build_codex_options(meeting_token=)` · `auth_service.get_meeting_token()` · `issue_meeting_token()` — `/start` 안의 토큰 INSERT 는 **WORK-009 가 이미 넣었다**. 이 work 는 그 줄을 유지한 채 그 뒤를 걷어낸다) · WORK-006(`/start` 표면) · WORK-007(`meeting_batch_service`)
- Parallel work: 없음 — **코드 워커는 한 번에 하나**
- Follow-up work: **WORK-011**(같은 파일 `meeting_batch_service.py` 의 배치 쪽 · `_agenda_rows` 의 남은 호출자) → WORK-012
- **External dependency**
  - **코드 레포는 별도다** — `github.com/kknaks/task_management`, 워크트리 `/Users/kknaks/orca/workspaces/task_management/docs-v1`
  - open-kknaks 워커 · codex 설정은 **WORK-009 가 세운다.** 이 work 는 프롬프트와 호출 시점만 바꾼다
  - **화면 변경 없음** — 프론트는 `/start` 응답이 빨라지는 것 말고 달라지는 것이 없다(SPEC-006 U-4 CTA 그대로)

## Work Summary

| Field | Value |
|---|---|
| Type | refactor |
| Owner |  |
| Status | done |
| Progress | 100% |
| Branch/PR | `kknaksss/docs-v1` |
| Blocker | 없음 |
| Next | 없음 — WORK-011 로. 앱 창 실측 캡처(§6 AC)는 아침에 사용자가 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM |  | SPEC-007 §6 AC 「워커를 내린 채 회의 시작」 1항목 대조 | todo |
| Design |  | 해당 없음 — 화면 변경 없음 | — |
| FE |  | 해당 없음 | — |
| BE |  | Phase 1~2 전부 | todo |
| QA |  | `/start` 응답 시간 · 워커 없이 시작 · 웜스타트 페이로드에 컨텍스트 0건 · 실패 갈래 코드 0건 | todo |
| Ops |  | 해당 없음 — env · compose 변경 없음 | — |

## Scope

포함:

- **`/start` 를 전이만으로 되돌린다** — `status` + `recording_started_at` 한 UPDATE(기존) + WORK-009 의 회의 토큰 INSERT. **서비스가 `commit()` 을 부르지 않는다**(BE §7 — `get_db` 가 요청 끝에서 커밋). 응답은 지금처럼 `MeetingDetail`
- **웜스타트를 백그라운드로** — `register_after_commit`(`core/db.py`, 이미 있다)로 commit 뒤에 태스크 하나를 띄운다. 태스크는 ① 제출(새 세션 · `output_schema` 없음) ② 돌아온 `session_id` 를 **새 세션에서** `meeting.ai_session_id` 에 UPDATE. **결과 본문은 버린다**
- **웜스타트 프롬프트 재작성** — 컨텍스트 0. 역할 · 회의 흐름 · 만들 것(용어 다섯의 뜻 — 안건이 뼈대) · 요약 원칙 · 지켜야 할 것 · **도구 7개 목록** · 쓰면 안 되는 것. 본문은 `reference/2026-09-06-task-management-app/ai-prompt-draft.md` **§A** 가 초안이다
- **컨텍스트 적재 코드 폐기** — `WarmStartContext` · `load_warm_start_context()` · `_task_rows()` · `_date()`
- **실패 처리를 만들지 않는다**(MF-70) — 태스크 예외는 **로그 한 줄**. 재시도 · 재웜스타트 · 별도 기록 테이블 · 화면 표시 어느 것도 없다. 결과는 이미 있는 두 경로다(회의 중 = 배치 미제출 · 종료 후 = ② `final_failed`)
- 테스트 — BE §12 **8-a**(워커 어댑터를 막아 둔 채 `/start` → 응답 · `recording` · `ai_session_id IS NULL` · 그 상태에서 트리거가 와도 제출 없음) + 웜스타트 프롬프트 정적 검사

제외:

- **배치 입력 · `build_batch_prompt` · `_persist` 전량 교체 · 프론트** → WORK-011. 이 work 는 `build_batch_prompt` 를 **건드리지 않는다**
- **최종 회의록 · 재전사 · `run_final`** → WORK-012
- **MCP 도구 · 토큰 · allow list** → WORK-009(이미 있다). 이 work 는 `get_meeting_token()` 을 **읽어 넘기기만** 한다
- **`_agenda_rows()` 폐기** — 남은 호출자가 `build_batch_prompt`(WORK-011) · `build_final_prompt`(WORK-012)다. **마지막 호출자를 지우는 WORK-012 가 폐기한다**(아래 §Code Surface 주)
- 배치 트리거 수치 · 상태 바 · WS — 바뀌지 않는다

## Code Surface

- Repo / module: `github.com/kknaks/task_management` — `app/back` 만. **프론트 · compose · env 변경 없음**

| 경로 | 신규 / 수정 / 폐기 | 설명 |
|---|---|---|
| `app/back/service/meeting_service.py` `start()` (L515~) | 수정 | 전이 UPDATE + `auth_service.issue_meeting_token()`(WORK-009) 까지만 남기고 **`load_warm_start_context()` 호출 · `await session.commit()` · `warm_start()` 대기 · `set_ai_session_id()` 를 걷어낸다.** 대신 `register_after_commit(session, lambda: meeting_batch_service.launch_warm_start(meeting_id))`. 마지막은 `build_detail(...)` 그대로 |
| `app/back/service/meeting_batch_service.py` `launch_warm_start()` | **신규** | `asyncio.create_task(_warm_start_once(meeting_id))` + done 콜백으로 예외 로그(기존 `_on_batch_task_done` 과 같은 모양). **await 하지 않는다** |
| 〃 `_warm_start_once()` | **신규** | ① `auth_service.get_meeting_token(meeting_id)`(없으면 로그 후 반환 — 제출하지 않는다) ② `gateway.run(prompt=build_warm_start_prompt(), session_id=None, output_schema=None, timeout_sec=settings.ai_timeout_sec, meeting_token=…)` ③ `session_id` 가 있으면 **새 세션**에서 `meeting_repository.set_ai_session_id()`. **본문은 버린다.** 예외는 전파(태스크 콜백이 로그) |
| 〃 `warm_start(context)` | **폐기** | `_warm_start_once` 가 대신한다 — 컨텍스트 인자가 없어졌다 |
| 〃 `load_warm_start_context()` · `WarmStartContext` | **폐기** | 컨텍스트를 싣지 않는다(MF-50). 대체 = MCP 도구 7개(WORK-009) |
| 〃 `_task_rows()` · `_date()` | **폐기** | 유일한 호출자가 `build_warm_start_prompt` 였다(grep 확인). `build_batch_prompt`·`build_final_prompt` 는 `taskWhitelist` 만 쓴다 |
| 〃 `_agenda_rows()` | 수정 없음(폐기는 WORK-012) | 이 work 가 호출자 하나를 지우지만 `build_batch_prompt`(011) · `build_final_prompt`(012)가 남는다. **여기서 지우면 011 이 깨진다** |
| 〃 `build_warm_start_prompt()` | 수정(전면) | 인자 없음 → `str` 상수 조립. 본문은 §Internal Interface 의 여섯 절. **`_dumps` 를 부르지 않는다**(실을 데이터가 없다) |
| `app/back/service/meeting_service.py` import | 수정 | `meeting_batch_service.load_warm_start_context` 참조 제거. `core.db.register_after_commit` 은 이미 import 돼 있다(L25) |
| `app/back/tests/meeting_live_fixtures.py` · `test_meeting_live_api.py` | 수정 | `/start` 가 웜스타트를 기다리지 않는 것으로 바뀐다 — 대역 게이트웨이 호출 시점 단언을 고친다(실물은 이 둘이었다 — 검수 D-2. `test_meeting.py` · `test_meeting_batch.py` 는 손댈 필요 없었다) |
| `app/back/tests/test_meeting_start_warm.py` | **신규** | §Execution 검증 항목(8-a 포함) |

- Domain / schema note: **리비전 0건.** `meeting.ai_session_id` 는 이미 NULL 허용이고 `/start` 가 채우지 않는 것이 정상 상태다(M-12 · meeting.md 컬럼 표)

## Domain / Schema

| Entity | 역할 |
|---|---|
| `meeting` | `status` · `recording_started_at` 은 `/start` 트랜잭션에서, **`ai_session_id` 는 백그라운드 태스크가 나중에** 쓴다 |
| `auth_session(kind='meeting')` | WORK-009 가 `/start` 에 넣은 행. 이 work 의 제출부가 원문을 **읽는다** |

- 상태 / invariant: **M-1-a**(`start_at` 예정 / `recording_started_at` 실적) · **M-12**(`ai_session_id` 는 회의 하나에 하나 · `/start` 가 채우지 않는다 · `NULL` 동안 배치 미제출) · **M-3**(상태 4종 한 방향)
- Migration 필요 여부: **없음**
- SPEC 에 환류해야 하는 변경: 없음

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| **WORK-011 회의 중** | `meeting.ai_session_id` · `_agenda_rows`(아직 살아 있다) | 배치는 이 값이 찬 뒤에만 제출된다(기존 `evaluate` 규칙 그대로) |
| **WORK-012 회의 종료** | 같은 세션(`resume`) | ② 가 `ai_session_id` 를 `resume` 한다. `NULL` 이면 `final_failed`(MF-70) |
| 프론트 | 없음 | `/start` 응답 형태가 그대로다 |

## Internal Interface Contract

외부 계약(`/start` 응답 · 웜스타트가 주는 것)은 **SPEC-006 §4 · SPEC-007 §4 「웜스타트」 표**가 정본이다. 여기는 Phase 사이 · 후속 WP 가 기대는 접점만 고정한다.

| 접점 | 계약 |
|---|---|
| **`start()` 의 트랜잭션** | 전이 UPDATE + 토큰 INSERT **하나**. **`session.commit()` 을 부르지 않는다** — 이 파일에서 `commit()` 호출 0건이 정적 검사다(BE §7 「`/start` 도 예외가 아니다」) |
| **`launch_warm_start(meeting_id: int) -> None`** | **동기 함수처럼 즉시 돌아온다**(내부에서 `create_task`). 예외를 밖으로 내지 않는다 — done 콜백이 로그만 남긴다. `register_after_commit` 에 등록되므로 **커밋이 안 되면 돌지 않는다** |
| **제출 파라미터** | `session_id=None`(새 세션) · `output_schema=None`(웜스타트는 JSON 을 받지 않는다) · `timeout_sec=settings.ai_timeout_sec` · `meeting_token=auth_service.get_meeting_token(meeting_id)`. **토큰이 `None` 이면 제출하지 않는다**(WORK-009 §Execution Phase 3 규칙과 같다) |
| **`session_id` 저장** | 제출이 끝난 뒤 **새 세션**에서 `set_ai_session_id`. 제출 대기 중 트랜잭션 0(BE §7) |
| **실패의 결과** | `ai_session_id` 가 `NULL` 로 남는다. **그것이 전부다** — `meeting_batch_service.evaluate()` 는 지금도 `NULL` 이면 제출하지 않고(기존 규칙), 종료 후는 WORK-012 의 ② 가 `final_failed` 로 간다. **`warm_start_failed` 같은 상태·컬럼·에러코드를 만들지 않는다** |
| **`build_warm_start_prompt() -> str`** | 인자 없음. 여섯 절 고정 — ① 역할(「회의에 참가하는 두 명 중 하나」) ② 회의는 이렇게 흐른다(발화가 배치로 · 종료 후 최종 회의록 · 사람 트랙은 읽기 전용) ③ 무엇을 만드나(**안건이 뼈대 · 논의 · 결정 · 액션 · 업무가 거기서 파생** — MF-55 · DEC-003 §8) ④ 어떻게 요약하나(압축 · 이름 안 씀 · 숫자 그대로 · 말 안 한 건 안 채움 · 확실치 않으면 한 단계 낮춤) ⑤ 쓸 수 있는 도구 **7개**(WORK-009 §Internal Interface 의 이름 그대로) ⑥ 쓰면 안 되는 것(셸 · 웹 · 이미지 · 쓰기). 끝에 「이번 요청에는 아무것도 만들지 말고 「준비됨」이라고만 답하라」 |
| **프롬프트에 없는 것** | 프로젝트 · 업무 목록 · 안건 · 유형 · **화이트리스트**. 문자열 안에 `humanAgendas` · `taskWhitelist` · `project` · JSON 블록(`{` `}`) 이 **0건**(정적 검사). `tasks` 는 도구 이름 `list_tasks` 에 들어 있어 needle 로 못 쓴다 — 「업무 제목·업무 목록 데이터」 0 으로 본다(검수 D-1) |

## Execution

### Phase 1 — `/start` 는 전이만 · 웜스타트는 커밋 뒤 태스크 (백엔드)

- **Status**: DONE
- **설명**: MF-1 이 코드가 되는 자리. 「회의 시작」이 즉시 끝나고, 워커가 죽어 있어도 회의가 시작된다.
- **작업**:
  - [ ] `meeting_service.start()` — `load_warm_start_context` · `commit()` · `warm_start` · `set_ai_session_id` 제거 · `register_after_commit` 등록
  - [ ] `meeting_batch_service.launch_warm_start()` · `_warm_start_once()` 신규 · `warm_start(context)` 폐기
  - [ ] `_warm_start_once` 안에서 `get_meeting_token` → 없으면 제출하지 않고 로그(WORK-009)
  - [ ] `tests/test_meeting_start_warm.py` · 기존 `test_meeting.py` · `test_meeting_batch.py` 의 시점 단언 수정
- **검증**:
  - [ ] **BE §12 8-a** — 워커 어댑터를 막아 둔 채 `POST /start` → **응답이 온다** · `status='recording'` · `recording_started_at` 이 찼고 · `ai_session_id IS NULL`. 그 상태에서 배치 트리거를 밀어도 **제출이 나가지 않는다**
  - [ ] 대역 게이트웨이가 **응답 반환 뒤에** 불린다(요청 처리 중 호출 0건). `run_after_commit_hooks` 를 돌리지 않으면 호출이 **0건**이다 — 커밋이 안 되면 웜스타트도 없다
  - [ ] 웜스타트가 성공하면 `ai_session_id` 가 **새 세션에서** 찬다. 그 뒤 배치 트리거가 정상 제출된다
  - [ ] 웜스타트가 예외로 죽어도 **회의는 `recording`** 이고 응답은 이미 나갔다. **DB 어디에도 실패 기록이 없다**(`meeting_batch_run` 행 0건 · job 행 0건)
  - [ ] **정적 검사**: `meeting_service.py` 에 `session.commit(` 0건 · `load_warm_start_context` 0건 · `WarmStartContext` 0건 · `_task_rows` 0건(grep 결과를 완료 증거에)
  - [ ] `make test` 전체 통과
- **완료 증거**: 커밋 `WORK-010` · `make test` 595 · `/start` 7ms(옛 5.6초) · 검수 `work010-review-report.md` FAIL 0 · WARN 6(WORK-011 에서 정리) · **앱 창 캡처 미완(아침)**

### Phase 2 — 웜스타트 프롬프트 · 컨텍스트 0 (백엔드)

- **Status**: DONE
- **설명**: MF-50 · MF-55. **「안건이 무엇인가」가 프롬프트에 들어가는 자리** — 지금 프롬프트에는 스키마 규칙만 있고 뜻이 없다(F-10 의 원인).
- **작업**:
  - [ ] `build_warm_start_prompt()` 전면 재작성(§Internal Interface 여섯 절 · 초안 `ai-prompt-draft.md` §A)
  - [ ] 도구 이름 7개를 WORK-009 의 `enabled_tools` 와 **글자 그대로** 맞춘다
  - [ ] `tests/test_meeting_start_warm.py` 에 프롬프트 정적 단언
- **검증**:
  - [ ] 제출된 프롬프트 문자열에 **`humanAgendas` · `tasks` · `taskWhitelist` · `project` · `{` JSON 블록이 0건**(grep · 테스트 단언)
  - [ ] 프롬프트에 **도구 7개 이름이 전부** 있고 그 밖의 도구 이름이 없다
  - [ ] 프롬프트에 **용어 다섯**(안건 · 논의 · 결정 · 액션 · 업무)의 뜻이 각각 한 절씩 있고 「안건이 뼈대」라는 문장이 있다
  - [ ] `output_schema=None` 으로 나간다(웜스타트는 JSON 을 강제하지 않는다)
  - [ ] 워커 로그에서 웜스타트 요청 본문이 **1페이지 안**이고 회의 데이터가 없다(실측 캡처)
  - [ ] `make test` 전체 통과
- **완료 증거**: 커밋 `WORK-010` · `make test` 595 · `/start` 7ms(옛 5.6초) · 검수 `work010-review-report.md` FAIL 0 · WARN 6(WORK-011 에서 정리) · **앱 창 캡처 미완(아침)**

## Pre-deploy Check

- [ ] env · compose 변경 없음 — WORK-009 의 `MCP_SERVER_URL` · `MEETING_TOKEN_TTL_MIN` 이 이미 있어야 한다
- [ ] 리비전 없음 — `alembic upgrade head` 결과가 WORK-009 와 같다(`0007`)
- [ ] 배포 뒤 첫 회의에서 `/start` 응답이 **1초 안**인지 본다(실측 13초의 원인이 이 work 다)

## Rollback

- **백엔드 단독 revert 로 끝난다** — 스키마 · env · 프론트가 없다
- 되돌리면 `/start` 가 다시 웜스타트를 기다리고 컨텍스트를 싣는다. **WORK-011 이 이미 들어간 뒤에는 되돌리지 않는다** — 011 의 배치가 도구로 읽는 것을 전제로 하는데 웜스타트만 옛 컨텍스트로 돌아가면 프롬프트 두 벌이 어긋난다
- 부분 revert 시: Phase 2 만 되돌리면 프롬프트가 옛것이 되고 동작은 그대로(느려지지 않는다). Phase 1 만 되돌리면 `/start` 가 다시 느려진다

## Done Criteria

- [ ] 모든 Phase 가 `DONE` 또는 `SUPERSEDED` 다
- [ ] **SPEC-007 §6 AC 「워커를 내린 채 「회의 시작」을 눌러도 즉시 회의 중 화면이 되고 받아쓰기가 된다. `ai_session_id` 가 비어 있어 배치는 돌지 않고 AI 탭은 「첫 배치를 기다리는 중」 그대로다」 — 앱 창 실측 캡처가 완료 증거에 있다**
- [ ] BE §12 **8-a** 테스트가 있다
- [ ] 정적 검사 4종(`commit(` 0 · `load_warm_start_context` 0 · `WarmStartContext` 0 · 프롬프트 안 컨텍스트 키 0) 결과가 붙어 있다
- [ ] **실패 갈래가 코드에 없다**(MF-70) — `warm_start` 근처에 `retry` · `attempt` · `except` 후 재제출이 0건이라는 grep 결과
- [ ] `make test` 전체 통과 · `Errors` 줄 0
- [ ] `30-work/README.md` 갱신

## Open Issues

- **`_agenda_rows()` 의 폐기 시점** — 이 work 가 아니라 **WORK-012**(마지막 호출자 `build_final_prompt` 를 지우는 WP). 이 work 에서 지우면 WORK-011 이 깨진다. 결정이 아니라 **순서 사실**이다
- **웜스타트 태스크의 수명** — `asyncio.create_task` 는 프로세스가 죽으면 사라진다. 그 회의는 `ai_session_id` 가 `NULL` 로 남고 **MF-70 대로 아무 처리를 하지 않는다**(기동 스윕 대상이 아니다 — job 행이 없다). 이것이 MF-70 의 뜻이고 새 결정이 아니다
- OQ-10 · 11 · 12 는 이 work 와 무관하다(재전사 `context` · 유형 시드 · 유형 `null`)

## Related

- SPEC: SPEC-006 §4 · U-4 · SPEC-007 §4 「웜스타트」 · §5 · §6 AC · DEC-003 §4 · §7 · §8
- Architecture: `backend/README.md` §5-2 · §5-3 · §7 · §8-3(웜스타트 미완료·실패 행) · §12 8-a · `database/domains/meeting.md` M-1-a · M-3 · M-12
- 프롬프트 초안: `reference/2026-09-06-task-management-app/ai-prompt-draft.md` §A
- Work: WORK-009(선행) · WORK-011 · WORK-012(소비)

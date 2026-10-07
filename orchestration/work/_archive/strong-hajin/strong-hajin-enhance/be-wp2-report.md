# WP2-BE 결과 보고 — 회의록 생성 고도화

## 상태: done (커밋하지 않음 · WP1 커밋 `e51fe3b` 위 워크트리 변경)

- 기준: WORK-012 「Phase WP2-BE」 · SPEC-010 §4.5 · §4.6 · §4.7 · DEC-009 · 코디 판정(보정 표 = 회의 상세 **최상위** `term_corrections`, 상세 모양 응답 전부)
- 기준선: `be-baseline.md` 의 「WP2-BE 기준선」 — 고치기 전 **기존 실패 0건**(unit 491 · contract 1268+128 · postgres 107)
- 경로 약어: `B/` = `backend/src/ax_workspace/` · `T/` = `backend/tests/`
- **외부 서비스 실물**: 정정 pass·다시 쓰기·새 세션 재시도는 Codex/Claude 를 부른다. 시험은 모두 대역으로 했고 실물 Codex 는 부르지 않았다 → **실물 1회 확인은 코디 E2E 몫**이다(10-07 주간 회의 원문 재합성 · 900초 안 · 「캐스티」 류가 표에 · 안건 시간 순 / 30분+ 회의가 90초를 넘겨도 「종료」)

## 1. 계약 체크박스 7/7

| # | 계약 | 구현 위치 |
|---|---|---|
| 1 | **timeout env 넷**(`AX_AI_TIMEOUT_BATCH_SECONDS` 240 · `…_WARMSTART_SECONDS` 240 · `…_FINAL_SECONDS` 900 · `…_CONVERSATION_SECONDS` 180) · Codex·Claude 같은 값 · 숫자 아님·0·음수면 시작 오류 | 기본값 상수 `B/bootstrap/settings.py:9-16` 부근 · `_positive_seconds` `:39`(빈 값=기본 · 정수 아님/0/음수 → `ValueError(이름 포함)`) · 필드 `:126-129` · `__post_init__` 재검증 `:178` · `from_environment` `:260-267` |
| 2 | **단계 값을 내려보내는 길 = 단계별 프로필** — 공장이 단계 timeout 을 받아 그 단계 프로필을 만든다 · 호출 넷이 자기 값 · 배치/웜스타트 분리 · `AiProviderProfileRequest.timeout_seconds` 안 씀 | 공장 `create_conversation_provider(…, timeout_seconds=)` `B/bootstrap/application.py:4834`(안 주면 대화 값) → `create_codex_cli_provider` `:4804`(`CodexCliProfile(timeout_seconds=…)`) · `create_claude_cli_provider` `:4817`(`ClaudeCliProfile(timeout_seconds=…)`). 호출 넷: **최종** `_CodexFinalizeAgent` `:527`(final) · **배치/웜스타트** `_CodexBatchAgent` — `open_session` `:636`(warmstart) · `run_batch` `:643`(batch) · `run_batch_in_new_session` `:652`(batch) — `meeting_batch_provider(tools, timeout_seconds=)` `:2155` · **보고서** `:1049`(conversation) · **대화 워커** `B/bootstrap/conversation_worker.py:62`(conversation). 요청 필드 `ai.py:23` 은 손대지 않았다(읽는 곳도 채우는 곳도 없음 그대로) |
| 3 | **timeout 재시도 = 새 세션 1회 — 배치·웜스타트·최종** · 배치는 회의마다 한 줄 · 재시도 중 도착분은 다음 배치 · 새 세션 참조는 성공 때 교체 · 그 밖 실패는 지금 규칙 · 워커 재배달 수와 맞춤 | **분류**: `ProviderTimedOut(ProviderRequestFailed)` `B/modules/ax_execution/ai.py:176` — Codex `platform/codex_cli.py:145,228` · Claude `platform/claude_cli.py:111,185` 가 던진다(하위 클래스라 기존 처리부는 그대로). 회의 경계 예외 `AiCallTimedOut`·`AiSessionLost` `B/modules/meetings/batch.py:26,34` — agent 가 옮긴다 `bootstrap/application.py:543,682,684`. **배치**: `B/modules/meetings/batch_service.py:299`(같은 세션 timeout·유실 → 새 세션) · `_run_in_new_session` `:337`(웜스타트 맥락 + 맥락 목록 + 지금까지의 AI 벌 + 그 배치 구간 → 성공하면 `record_session` 으로 교체, 실패면 `failed` 기록·옛 참조 유지) · 회의당 락 안이라 겹치지 않고 `to_seq` 는 읽을 때 고정 → 그 사이 도착분은 다음 배치. **웜스타트**: `:190-201`(timeout 이면 1회 다시 연다). **세션이 아예 없는 회의**: `batch_input` 이 `session_ref=None` 으로 내고(`mtg/application.py:1509`) 그 배치가 새 세션으로 연다(아래 §6-1). **최종**: `B/modules/meetings/finalize_service.py:166-199` — timeout 이면 `session_ref=None` 으로 **새 세션 1회**(시도 상한과 무관하게 보장), 그 1회의 실패는 무엇이든 「실패」 · timeout 이 아닌 실패는 지금처럼 시도 3회·세션 유실이면 콜드. **워커 lease**: `Settings.effective_meeting_finalize_lease_seconds` `settings.py:205` = max(설정값, 재전사 1200 + 최종×2 + 300) → `meeting_worker.py:84`(기본 900 이면 3300초). `MAX_DELIVERIES=FINAL_ATTEMPTS` 는 그대로(서비스가 timeout 을 안에서 다루므로 예외로 새는 배달 수는 변하지 않는다) |
| 4 | **AI 맥락 목록 조립 함수 하나** — 프로젝트 전부 · 완료·취소 안 된 업무 · 구성원 전부 · 호출 때 DB 조회 · 조직 전체 · 상한 없음 · 세션을 새로 열 때마다 | 모양·글자 `B/modules/ax_execution/context_catalog.py`(`render_ai_context_catalog` `:83` · 세 표 `{id,name,status}` · `{id,title,project_id,state,due_date}` · `{id,name,unit,position}`) · 조회 `B/platform/ai_context.py:33`(쿼리 넷 — 프로젝트 · `state NOT IN (done, cancelled)` 업무 · 활성 구성원 · 주 소속/주 보직) · 하나의 입구 `WorkflowApplication.ai_context_catalog()` `bootstrap/application.py:2140`(크기 로그 — I-6). **WP3 는 이 메서드를 대화에 부르면 된다**. 실리는 자리: 웜스타트 · 배치 새 세션 · 최종 합성(시도마다, 회차당 한 번 조회 `finalize_service.py:161`) |
| 5 | 웜스타트·최종 프롬프트에 맥락 목록 · **최종에 재전사 전체 발화 매번** | 웜스타트 `build_warm_start_prompt(context, tools, catalog)` `B/modules/meetings/batch.py:205`(+ 「구성원 표로 화자를 짐작하지 마라」) · 새 세션 배치 `build_fresh_batch_prompt` `:302` · 최종 `build_final_prompt(…, transcript, catalog)` `B/modules/meetings/finalize.py:460-493`(`transcript` 필수 인자) · 서비스 `finalize_service.py:265`(`if cold_start else None` 삭제) |
| 6 | **정정 pass + 보정 표** — 최종 프롬프트 두 단계 · 출력 스키마 `term_corrections[{heard,corrected,grade}]` · 파서·검증(형식 오류 항목만 버림) · 저장(행 + `term_corrected_at` 같은 트랜잭션) · 상세 응답(`null`/`[]`/행) · 배치 출력에 오면 버림 · 원문 안 바꿈 | 프롬프트 「두 단계로 한다 — ① 정정 → ② 다시 쓰기」 `finalize.py:390-405`(등급 auto/presumed · 화자 라벨 불변 · 원문 불변) · 스키마 `schemas/ai_final_output.json` `term_corrections`(provider 에는 **필수**로 건다) · 서버 검증은 그 칸을 뺀 스키마(`_without_term_corrections` `finalize.py:29`) + 항목 파서 `parse_term_corrections` `:140`(1~100자 · 등급 둘 · 같은 `heard` 첫 것만 · 칸이 없거나 배열 아니면 빈 표) · `TermCorrection`/`FinalNotes.term_corrections` `:107` · 적재 `mtg/application.py:951`(`commit_finalized` 안 — 같은 트랜잭션, 0개여도 시각을 찍는다) · 저장소 `platform/meetings.py:820,839` · 표 `MeetingTermCorrectionRecord` `platform/persistence.py:331` · 칸 `meetings.term_corrected_at` `:325` · 응답 `_term_corrections_view` `mtg/application.py:1858` · 배치 `parse_output` 이 그 칸만 버림 `batch.py:135` · [회의록만 삭제] 저장소가 표·시각을 걷음 `platform/meetings.py:807-814` |
| 7 | **안건 순서** — 최종 적재가 가장 이른 근거 시각으로 `order_index` | `order_agendas_by_evidence` `finalize.py:244`(줄들의 최소 `from_ms` · 줄 없는 안건은 끝 · 같은 시각은 모델 순서 — 안정 정렬) · `_prepare_final_notes_in_place` 에서 **출처 도장(「안건 N 에서」) 전에** 매긴다 `:339` → `commit_finalized` 의 `next_agenda_order` 가 그 순서대로 1부터 |

**코디 지시 — 보정 표를 실은 「상세 모양」 응답 전부**: `term_corrections` 는 상세를 만드는 **한 자리** `MeetingApplication._detail`(`mtg/application.py:1855`)에 실었다. 그 결과를 그대로 돌려주는 자리는 전부 11곳이다.
- `get` `:296`
- `create` `:337`
- `quick_start` `:477`
- `update_info`(= PATCH) `:538`
- `apply_legacy_note` `:587`
- `start` `:629`
- `end` `:643`
- `retry_finalize` `:993`
- `apply_legacy_visibility` `:1152`·`:1172`
- (`export` `:1059` 는 상세를 읽어 `{meeting, agendas}` 만 다시 엮는다 — **내보내기는 바꾸지 않는다** · OQ-1006)

HTTP·MCP 의 생성·조회·수정·시작·종료·재시도 응답이 모두 이 길을 지난다(`meeting_get` MCP 포함). 합성 잡의 투영 `_detail_for_owner` `:1075` 에도 같은 값을 실었다. 시험: PATCH 응답 `test_responses_that_return_the_detail_shape_carry_the_same_term_table`.

## 2. WARN 함께

- **W-5**: 계약 시험 앱의 연동 사건 묶음 타이머를 0 으로 주입했다.
  - `UserEventHub(coalesce_seconds=None)` 이 만들 때 모듈 값을 읽는다(`platform/user_event_hub.py:56`).
  - 새 `T/contract/conftest.py` 가 autouse 로 `COALESCE_SECONDS=0` 을 넣는다 — 계약 시험에서 진짜 1초 타이머 스레드가 돌지 않는다.
  - 묶어 내기 자체는 `T/unit/test_user_event_hub.py` 가 타이머 대역으로 잰다.
- **W-7**: `external_inbox_upstream.py` 의 죽은 상수 `REMOTE_IMAGE_TYPES` 를 지웠다. 쓰는 곳이 0이었다(grep).

## 3. Code Surface WP2 대비 닿은 자리

| 행 | 재계수(`e51fe3b`) | 닿은 자리 |
|---|---|---|
| timeout 값(codex·claude·cli_process) | 16줄 / 3파일 (표와 같음) | 박힌 값 둘(`codex_cli.py:95` 90 · `claude_cli.py:74` 180)은 **프로필 기본값으로 남겼다**. 공장이 늘 단계 값을 넘기므로 제품 경로에서는 쓰이지 않는다(어댑터를 직접 만드는 시험만 쓴다). 쓰는 곳 넷(`codex_cli.py:141,222` · `claude_cli.py:108,179`)은 프로필 값을 읽으므로 그대로 두었다. timeout 예외 넷은 `ProviderTimedOut` 으로 바꿨다. 러너 `cli_process.py` 는 그대로다. `ai.py:23` 요청 필드도 그대로(쓰지 않음). `bootstrap/application.py` 의 회의실·자료·영수증 timeout 도 그대로 |
| provider 를 만드는 곳 | 10줄 | 공장 셋 + 호출 넷(최종 · 배치/웜스타트(셋으로 갈림) · 보고서 · 대화 워커) + `meeting_batch_provider` 전부 |
| 최종 재시도 `FINAL_ATTEMPTS\|FinalizeSessionLost\|cold_start\|session_ref` | 112줄 (src 전체) | `finalize_service.py` 루프·`_compose` · `_CodexFinalizeAgent` · 워커 lease. `FINAL_ATTEMPTS`·`MAX_DELIVERIES` 값은 그대로 |
| 재전사 전체 발화 매번 | — | `finalize_service.py:265` · `finalize.py` docstring·`build_final_prompt` |
| 맥락 목록이 들어갈 프롬프트 | 21줄 | 웜스타트(`batch.py:205`) · 새 세션 배치(`:302`) · 최종(`finalize.py:460`) · 재료(`mtg/application.py` `warm_start_context` 그대로 + `batch_input.ai_track` · `finalize_input` 그대로). 대화(`codex_cli.py:529-564` · `claude_cli.py`)는 **WP3 몫이라 두었다**. 도구 레지스트리 `settings.py:13` 등은 그대로 |
| 정정·보정 표 | — | 스키마 · 파서 · `_bind_evidence`(그대로) · 프롬프트 · 배치 파서 · 적재 · 응답 · persistence · 저장소. 내보내기 `export.py` 는 그대로(OQ-1006) |
| 안건 순서 `order_index` | 37줄 | 최종 적재 순서만(도메인에서 정렬 → 기존 `next_agenda_order`). 읽기 `platform/meetings.py` `order_by(order_index, created_at)` 는 그대로 |
| **표 밖** | — | 웜스타트가 회의 정보에 참석자 실명을 싣지 않는 규칙은 그대로다. 다만 맥락 목록의 구성원 표(D-13)에는 이름이 실린다 → 프롬프트에 「구성원 표로 화자를 짐작하지 마라」 를 넣었고, 기존 시험을 「이 회의」 구간 한정으로 고쳤다(§4) · `batch_input` 이 세션 없는 회의도 입력을 낸다(§6-1) · `delete_note_content` 가 보정 표·시각을 걷는다 |

**스키마 변경 경로**(코드 레포 규칙): 일반 API 시작은 DDL 을 하지 않는다.
- 로컬: `make sync-demo-schema`(schema_sync additive)가 새 표와 nullable 칸을 만든다 — postgres 시험으로 확인
- 운영: `backend/migrations/manual/2026-10-07-meeting-term-corrections.sql`(`IF NOT EXISTS` · 이미지보다 먼저 적용)
- `docs/domain-model.md` 대조표에 한 줄을 더했다

⚠ **allowed_paths 밖 1파일**: `docs/domain-model.md`. 역할 규칙 「새 모듈·새 표는 domain-model.md 대조표에 한 줄 추가」 를 따랐다. 인벤토리 json 은 이번에 drift 가 없어 바꾸지 않았다(HTTP·MCP 시그니처 변화 없음).

## 4. 새 시험 · 고친 시험

**새 파일 6개**

`T/unit/test_ai_stage_timeouts.py`(25)
- 기본값 넷
- env 넷이 각자 읽힘
- `abc`·`0`·`-5`·`1.5` × 넷 → 시작 오류
- Codex·Claude 공장이 단계 값으로 프로필을 만듦(안 주면 대화 값)
- lease 바닥

`T/unit/test_ai_context_catalog.py`(1) — 세 표 모양 · 머리 · 「목록에서 먼저」

`T/unit/test_user_event_hub.py` — WP1 에서 만든 파일(W-5 와 함께 동작 확인)

`T/contract/test_meeting_minutes_enhance.py`(12)
- **배치 재시도 시험**
  - 배치 timeout → 새 세션 1회 → 성공 때만 세션 교체
  - 새 세션도 실패 → 옛 세션 유지 · 같은 구간이 다음 배치에
  - 재시도 중 도착한 발화는 다음 배치로 · 재시도 중 트리거는 새 배치를 세우지 않음(겹침 0) · 다음 배치는 새 세션을 이어 씀
- 웜스타트 timeout → 1회 다시 열기
- 세션 없는 회의 → 다음 배치가 새 세션으로 엶
- 맥락 목록 = 프로젝트 전부·열린 업무·활성 구성원(DB 와 대조)
- 새 프로젝트가 다음 호출에 들어감
- 보정 표
  - 정정 안 돈 회의 `null`
  - 바로잡을 것 없음 `[]`
  - 최상위 · 순서 · 틀린 행만 버림
  - PATCH 응답에도 같은 표
  - 회의록 삭제 저장소가 `null` 로 되돌림

`T/integration/postgres/test_meeting_term_corrections_postgres.py`(2) — PostgreSQL 왕복 · `null`→행→`[]` · `schema_sync` 가 새 표·인덱스·칸을 계획함

**기존 파일에 더함**

`T/unit/test_meeting_finalize_service.py` +5
- timeout → 새 세션 1회
- 두 번째 timeout → 「실패」 — 같은 세션 resume 3회 없음(운영 3abe9f9b 모양)
- timeout 뒤 다른 실패도 「실패」
- 시도마다 전사 전량·맥락 목록·정정 지시
- timeout 아닌 실패는 3회

`T/unit/test_meeting_domain.py` +5
- 보정 표 항목별 버림·중복·순서
- 칸 없음/깨짐 = 빈 표
- provider 스키마가 표를 필수로 건다
- **안건 순서**(가장 이른 근거 · 줄 없는 것 끝)
- 배치에 온 보정 표는 그 칸만 버림

`T/contract/test_codex_cli.py` +1 — 상한 초과 = `ProviderTimedOut`(하위 클래스) · 프로필 900 이 러너에 감

**계약이 바뀌어 고친 기존 시험 5**
- `test_meeting_finalize_service.py::test_finalize_falls_back_to_cold_start…` — 이어 쓰는 시도에도 전사가 실린다(OQ-904)
- `test_meeting_domain.py::test_final_prompt_carries_the_meeting_day…` — `transcript` 필수 인자
- `test_meeting_finalize.py::test_a_merge_that_succeeds…` — resume 프롬프트에 전사가 있다
- `test_meeting_memo_batch.py::test_starting_a_meeting_opens_one_provider_session…` — 회의 정보 구간에는 여전히 참석자 실명이 없고, 맥락 목록이 따로 실린다
- `test_codex_cli.py::test_a_conversation_that_asked_for_the_final_notes_schema…` — provider 스키마의 필수 칸에 `term_corrections` 가 더해졌다

**대역 확장**: `FakeBatchAgent.run_batch_in_new_session` · `_Gateway.ai_context_catalog`

## 5. 검증 수치

| 시험 | 기준선(`e51fe3b`) | 이번 |
|---|---|---|
| `make test-unit`(architecture · 인벤토리 drift 포함) | 491 passed | **526 passed** · 0 failed |
| `make test-contract` | 1268 + 직렬 128 | **1281 + 직렬 128 passed** · 0 failed |
| `make test-postgres`(격리 `127.0.0.1:55439`) | 107 | **109 passed** · 0 failed |
| 운영 인벤토리 drift | 통과 | 통과 — HTTP·MCP 시그니처 변화 없음, json 미변경 |
| `make test`(전체 병렬 + 직렬) | — | **1807 + 직렬 130 passed** · 0 failed |

- 첫 회차 `make test-contract` 에서 1건이 실패했다: `test_codex_cli.py::test_a_conversation_that_asked_for_the_final_notes_schema…` — provider 스키마의 필수 칸이 셋이 되어서다. 계약 변경으로 시험을 고친 뒤 위 수치로 다시 돌렸다
- **기존 실패(기준선) 0건** — 남은 실패 없음
- frontend 시험은 이번 Phase 범위 밖이라 돌리지 않았다(BE 는 `frontend/` 를 바꾸지 않았다)

## 6. 미결 · 주의점

1. **세션 없는 회의도 배치를 낸다** — 옛 규칙은 「세션이 없으면 제출하지 않는다」 였다. SPEC-010 §4.6 의 「웜스타트 새 세션 1회도 실패하면 다음 배치에 합친다」 를 지키려면 다음 배치가 세션을 열 수 있어야 해서, 세션이 없으면 그 배치가 새 세션 1회로 연다. 웜스타트가 세션 없이 끝나는 경우(timeout 아닌 실패 포함)도 같은 길을 탄다. 다르게 원하면 알려 달라
2. **배치 세션 유실(`ProviderSessionUnavailable`)도 timeout 과 같이 새 세션**으로 간다(§4.5 「세션 유실로 다시 시작할 때 다시 싣는다」). 옛 규칙은 `failed` 뒤 다음 배치도 같은 죽은 세션을 다시 시도했다
3. **새 세션 배치는 지금까지의 AI 벌(안건·줄·근거)을 함께 싣는다** — 배치가 AI 벌을 통째로 갈아 끼우므로, 싣지 않으면 새 세션의 첫 출력이 앞 구간 요약을 지운다. SPEC 의 「웜스타트 맥락 + 맥락 목록 + 그 배치 미처리 구간」 에 이 하나를 더했다(모양 상세는 구현 몫으로 봤다)
4. **맥락 목록에 구성원 실명이 실린다**(D-13 「구성원은 다」). 옛 웜스타트의 「실명을 프롬프트에 흘리지 않는다」(WP Pre-deploy Check)와 부딪친다 — 회의 정보 구간은 그대로 실명 없음 + 「화자 짐작에 쓰지 마라」 한 줄로 갈랐다. 운영 반영 전에 Pre-deploy Check 문구를 갱신해야 할 수 있다(planner)
5. **맥락 목록 크기 상한 없음**(I-6) — 호출마다 `AI 맥락 목록: 프로젝트 n · 업무 n · 구성원 n · n자` 로그를 남긴다. 운영 크기는 코디 E2E 에서 본다. Codex 는 프롬프트를 인자로 넘기므로 매우 크면 `E2BIG` 위험이 있다(메디니스 115KB 실측 주석 참고)
6. **최종 timeout 이 여러 번이면 최대 약 30분 「정리 중」**(H-9). 워커 lease 는 재전사 1200 + 900×2 + 300 = 3300초로 올라가게 했다(`AX_MEETING_FINALIZE_LEASE_SECONDS` 가 더 크면 그 값)
7. 「참석 N명」·화자 라벨은 손대지 않았다(OQ-905). `auto` 치환을 원문(스크립트)에 적용하지 않는다(OQ-1003 — 원문 불변)
8. 격리 PostgreSQL 컨테이너 `sh-enhance-be-pgtest`(127.0.0.1:55439)는 다음 Phase 를 위해 띄워 둔 채로 두었다

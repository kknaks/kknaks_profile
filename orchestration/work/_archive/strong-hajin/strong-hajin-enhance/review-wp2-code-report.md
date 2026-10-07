# 코드 검수 — WORK-012 WP2 (BE + FE)

- 검수자: reviewer(read-only) · 2026-10-07
- 대상: 코드 워크트리 `strong-hajin-enhance` 의 **WP1 커밋 `e51fe3b` 뒤 미커밋 변경 전부** — 수정 28파일(+914/−100) · 새 파일 9
- 계약
  - WORK-012 「Phase WP2-BE」·「Phase WP2-FE」 · Code Surface WP2 표
  - SPEC-010 §2.5 · §4.5~§4.7
  - 코디 판정: `term_corrections` = 상세 응답 **최상위** · `null`/`[]`/행
- 워커 리포트: `be-wp2-report.md` · `fe-wp2-report.md`
- 한 일: `git diff` 전부 읽음 · 호출자·쓰는 곳을 `rg` 로 다시 셈. **시험·빌드·서버는 돌리지 않았다** — 수치는 워커 값이다
- 지시서 물음 2~4 는 WP1 문구가 그대로 와 있다. WP2 의 같은 축(Code Surface WP2 · BE↔FE `term_corrections` · WP2 회귀)으로 답하고, WP1 영역은 「WP2 가 건드렸는가」 만 본다(§4).
- 약어: `B/` = `backend/src/ax_workspace/` · `F/` = `frontend/src/` · `T/` = `backend/tests/`

---

## 0. 판정 — **FAIL**(BE 2건 · 고칠 곳은 좁다)

계약 체크박스는 BE 7/7 · FE 2/2 모두 구현됐다. 스키마 경로와 운영 SQL↔ORM 도 맞다. BE↔FE 의 `term_corrections` 모양도 일치한다.

FAIL 2건은 둘 다 **동시성·시간 예산** 문제다.

1. **합성 잡 lease 바닥 3300초가 실제 최악 시간보다 짧다.** 한 배달에서 최종 호출은 2번이 아니라 **최대 4번**(시도 3 + timeout 뒤 새 세션 1)이다. lease 가 끝나면 다른 워커가 같은 회의 합성을 겹쳐 돈다.
2. **「세션 없는 회의도 배치를 낸다」(BE 미결 1)가 웜스타트와 경주한다.** 웜스타트는 회의 락 밖에서 최대 480초 돈다. 그 사이 첫 배치가 자기 새 세션을 열고, 뒤늦게 끝난 웜스타트가 그 세션 참조를 덮어쓴다.

그 밖은 WARN 8건이다. 하나가 운영 전 실측 필수다 — 매번 싣는 전사 전량 + 맥락 목록이 **Codex·Claude 의 argv 한 칸**으로 넘어간다(리눅스 한 인자 128KiB 한도).

---

## 1. 계약 체크박스 — 구현 위치

### WP2-BE (7/7)

| 계약 | 구현 | 판정 |
|---|---|---|
| timeout env 넷 · 시작 오류 | `B/bootstrap/settings.py` 기본값 상수 · `_positive_seconds`(빈 값=기본 · 정수 아님/0/음수 → `ValueError`) · `__post_init__` 재검증 · `from_environment` | PASS |
| 단계별 프로필 · 호출 넷 · `ai.py:23` 안 씀 | 아래 다섯 자리가 각자 단계 값을 받는다. `meeting_batch_provider(…, *, timeout_seconds)` 는 키워드 필수라 빠진 호출자가 있으면 깨진다(다시 셈: 호출 둘 `:526` · `:666`)<br>— 최종 `bootstrap/application.py:526`<br>— 웜스타트 `_converse(…warmstart)`<br>— 배치·새 세션 배치 `batch`<br>— 보고서 `:1048`<br>— 대화 워커 `conversation_worker.py:61` | PASS |
| timeout 재시도 = 새 세션 1회(배치·웜스타트·최종) | 예외: `ProviderTimedOut` `B/modules/ax_execution/ai.py:176`(하위 클래스라 기존 처리부 무변) — 던지는 자리 넷 `codex_cli.py:145,228` · `claude_cli.py:111,185`(다시 셈: `TimeoutExpired` 잡는 곳 전부)<br>배치 `batch_service.py:290-307,337-358`<br>웜스타트 `:190-201`<br>최종 `finalize_service.py:160-197` | PASS(§4 F-1·F-2) |
| AI 맥락 목록 함수 하나 | 조회 `B/platform/ai_context.py`<br>— 프로젝트 전부 · 업무 `state NOT IN (done, cancelled)` · 활성 구성원 + 주 소속·주 보직<br>모양 `context_catalog.py:83-136`<br>입구 `WorkflowApplication.ai_context_catalog()` `bootstrap/application.py:2140`(크기 로그) | PASS — 조직 전체(OQ-1002 ① 정정)대로, 호출자 권한을 걸지 않는다 |
| 웜스타트·최종에 목록 · 최종 전사 매번 | `build_warm_start_prompt(…, catalog)` `batch.py:205` · `build_fresh_batch_prompt` `:302` · `build_final_prompt(transcript 필수, catalog)` `finalize.py:460-493` · `finalize_service.py:265` | PASS |
| 정정 pass + 보정 표 | 프롬프트 두 단계 `finalize.py:390-405`<br>스키마: provider 쪽 필수 · 서버 검증은 그 칸을 뺀 사본 `:29-37`<br>항목 파서 `:140-163`(1~100자 · 등급 둘 · 같은 `heard` 첫 것)<br>적재 `mtg/application.py:949-958`(같은 트랜잭션 · 0개여도 시각)<br>저장소 `platform/meetings.py:819-846`<br>배치에 오면 그 칸만 버림 `batch.py:135`<br>[회의록만 삭제]가 걷음 `platform/meetings.py:810-814` | PASS(§5 W-3) |
| 안건 순서 | `order_agendas_by_evidence` `finalize.py:244-254` — 출처 도장 **전에** `:339` · 안정 정렬 · 줄 없는 안건 끝 | PASS |

### WP2-FE (2/2)

| 계약 | 구현 | 판정 |
|---|---|---|
| 회의록 끝 「용어 보정」 표 · 읽기 전용 · `[]` 한 줄 · `null` 자리 없음 | 부품 `F/features/meetings/TermCorrections.tsx`(DS `DataTable`)<br>놓는 자리 `MeetingDetailPage.tsx:1310-1314`(최종 탭 · 「종료」·「실패」 · 정리 중 아님)<br>배열 판정 `:718-719`<br>타입 `viewModels.ts:1297-1304`<br>문구 `labels.ts:922-930` | PASS |
| 안건 순서는 서버 `order` 그대로 | 코드 변경 없음 · 시험으로 잠금 | PASS |
| (덤) 제목 PATCH 응답이 칸을 안 실을 때 표 보존 | `MeetingDetailPage.tsx:568-570` | PASS — BE 가 PATCH(`update_info`)도 `_detail` 을 지나 같은 값을 낸다(`mtg/application.py:1853-1864` 한 자리) → FE 리포트 §5-2 걱정은 해소 |

---

## 2. Code Surface WP2 — 다시 센 것

| 표의 행 | 다시 센 것 | 판정 |
|---|---|---|
| timeout 값(codex·claude·cli_process 16/3) | 박힌 기본값 둘(`codex_cli.py:95` 90 · `claude_cli.py:74` 180)은 프로필 기본값으로 남았다. 제품 경로는 늘 공장이 단계 값을 넘긴다 · 러너 그대로 · `ai.py:23` 그대로 | PASS |
| provider 만드는 곳 | `create_conversation_provider(` 호출 셋(`conversation_worker.py:61` · `application.py:1048` · `:2162`) — 모두 `timeout_seconds` 를 넘긴다 · `meeting_batch_provider(` 둘 | PASS |
| 최종 재시도 | `finalize_service.py` 루프 · 워커 lease(`meeting_worker.py:84`) — **lease 셈이 루프와 안 맞음**(F-1) | **FAIL** |
| 재전사 전체 발화 매번 | `finalize_service.py:265` · `build_final_prompt` | PASS |
| 맥락 목록 프롬프트 | 웜스타트 · 새 세션 배치 · 최종. 대화(`codex_cli.py:529-564` · `claude_cli.py`)는 WP3 몫으로 남겼다 — WORK 와 같음 | PASS |
| 정정·보정 표 | 스키마 · 파서 · 프롬프트 · 배치 파서 · 적재 · 응답(`_detail` · 합성 투영 `_detail_for_owner` `:1074-1075`) · persistence · 저장소 · `export.py` 무변(OQ-1006) | PASS |
| 안건 순서 `order_index` | 최종 적재만 — 읽기 `order_by(order_index, created_at)` 그대로 | PASS |

---

## 3. BE↔FE 계약 · 스키마 경로

| 항목 | 본 것 | 판정 |
|---|---|---|
| `term_corrections` 위치·모양 | BE `_term_corrections_view` = `term_corrected_at` 없으면 `None` · 있으면 `[{heard,corrected,grade}]`(order_index 순)<br>FE 타입 `MeetingTermCorrection[] \| null` · 없는 칸은 `null` 취급 | PASS |
| 상세 모양을 돌려주는 응답 전부 | 상세를 짓는 자리가 `_detail` 한 곳 → get·create·quick_start·PATCH·start·end·retry·legacy 둘이 다 지난다(워커 셈 11 — 코드 확인) | PASS |
| 스키마 경로(일반 API 시작 DDL 금지) | ORM `MeetingTermCorrectionRecord` · `MeetingRecord.term_corrected_at`<br>로컬은 `schema_sync`(additive) · 운영은 `backend/migrations/manual/2026-10-07-meeting-term-corrections.sql`<br>API 시작에 `create_all` 없음(diff 에 없다) | PASS |
| 운영 SQL ↔ ORM | 표·칸·타입(UUID · INTEGER · VARCHAR(100)×2 · VARCHAR(10) · timestamptz) · NOT NULL · FK `meetings(id)` · 인덱스 이름·칸 모두 같다<br>`id` 기본값은 ORM 쪽(`uuid4`)이라 SQL 에 DEFAULT 없음 — 기존 표들과 같은 결<br>회의는 하드 삭제 경로가 없어(`delete(MeetingRecord)` 0) FK 에 `ON DELETE` 가 없어도 막히지 않는다 | PASS |
| `docs/domain-model.md` 대조표 | 한 줄 추가(allowed_paths 밖이지만 역할 규칙이 시킨 자리) | PASS |
| 로컬 스택 | 새 표·칸 때문에 `make local-stack` 이 「스키마가 최신이 아님」 으로 멈춘다 — 코디가 재시작 전에 `make sync-demo-schema` 를 돌려야 한다(AGENTS · P-4) | 참고 |

---

## 4. 회귀 · 동시성 — FAIL 둘

### F-1 (FAIL · BE) — 합성 잡 lease 바닥이 최악 시간보다 짧다

- **바닥 셈**: `effective_meeting_finalize_lease_seconds`(`B/bootstrap/settings.py:205-212`) = 재전사 1200 + **최종 × 2** + 300 = **3300초**. 워커는 lease 를 연장하지 않는다 — `meeting_worker.py` 에 heartbeat·extend 가 없다(대화 워커는 `extend_visibility` 로 연장한다).
- **루프가 실제로 부르는 횟수**: 최대 **4번**이다(`finalize_service.py:160-197`) — 시도 `FINAL_ATTEMPTS = 3` + timeout 뒤 새 세션 1회. 새 세션 1회는 시도 상한과 무관하게 보장된다.
- **최악 시나리오**:
  - timeout 이 아닌 실패(스키마 위반·근거 없는 줄)는 provider 가 **답을 다 낸 뒤** 난다 → 그 시도도 최대 900초를 쓴다.
  - 그래서 스키마 실패 × 2 → timeout → 새 세션이면 1200 + 900×4 = **4800초**.
  - timeout 이 아예 없어도 시도 3회 = 1200 + 2700 = **3900초**.
- **lease 가 끝나면**: 같은 회의 잡을 다른 워커가 다시 집는다(`claim`) → 재전사·합성이 **겹쳐 돈다** → 두 번 적재·두 번 provider 비용. 옛 90초 시대에는 3×90 이 넉넉히 들어가서 드러나지 않던 문제다.
- **시험 쪽**: `T/unit/test_ai_stage_timeouts.py` 의 lease 시험은 이 셈식 자체(3300)를 단언한다 — 루프 최대 횟수와 맞춰 보지 않는다.
- **고칠 것**(하나를 고른다):
  - ① 바닥 = 1200 + 900 × (`FINAL_ATTEMPTS` + 1) + 300(= 5100초)
  - ② 합성 루프에 lease 연장(heartbeat)을 단다 — 대화 워커와 같은 방식
  - ③ 한 배달의 최종 시도 시간 합에 상한을 두어 lease 안에서 끊는다

  시험은 「루프의 최대 호출 수 × 단계 상한 ≤ lease」 를 단언하도록 고친다.

### F-2 (FAIL · BE) — 세션 없는 배치가 웜스타트와 경주한다(BE 미결 1)

- **바뀐 것**: `batch_input` 이 세션이 없어도 입력을 낸다(`mtg/application.py:1496-1512`, 옛 `if session is None: return None` 삭제). 그러면 배치가 `_run_in_new_session` 으로 **자기 세션**을 열고 `record_session` 한다(`batch_service.py:337-358`).
- **문제**: 웜스타트(`warm_start` `batch_service.py:182-201`)는 「회의 시작」 커밋 뒤 **별도 스레드**로 돌고, 배치가 잡는 **회의당 락을 잡지 않는다**. 걸리는 시간은 240초, timeout 이면 1회 더 → 최대 480초. 배치 트리거는 미처리 600자 또는 **90초**다.
- **시나리오**: 웜스타트가 90초 넘게 걸리는 날 →
  1. 첫 배치가 세션 없음으로 보고 새 세션 S2 를 연다
  2. S2 로 AI 벌을 낸 뒤 S2 를 기록한다
  3. 웜스타트가 끝나 S1(배치 내용을 모름)을 기록해 **S2 를 덮어쓴다**
  4. 다음 배치는 S1 을 이어 쓴다 → S1 이 낸 「네 벌 전체」 가 AI 벌을 통째로 갈아 끼워 **첫 배치 구간의 요약이 AI 탭에서 사라진다**
  - provider 호출도 두 벌로 돈다.
  - 옛 규칙(세션 없으면 제출 안 함)에는 없던 경주다.
- **최종 합성 영향은 작다**: 전사 전량을 매번 싣기 때문이다. 하지만 회의 중 AI 탭은 사용자가 보는 화면이다.
- **고칠 것**(하나를 고른다):
  - ① 웜스타트를 회의당 락 안에서 돌린다(배치가 기다린다)
  - ② 「웜스타트 진행 중」 표지를 두고, 그동안은 세션 없는 배치를 내지 않는다(웜스타트가 끝내 실패·timeout 2회일 때만 배치가 새 세션을 연다)
  - ③ `record_session` 을 「없을 때만 기록」(compare-and-set)으로 바꾸고, 진 쪽 세션은 버린다

  시험 하나: 웜스타트를 붙잡은 채 배치를 돌려 세션이 하나로 남는지.

### WP1 영역을 건드렸나

| 자리 | WP2 변경 | 판정 |
|---|---|---|
| `external_inbox_upstream.py` | 죽은 상수 `REMOTE_IMAGE_TYPES` 삭제(WP1 W-7) — 쓰는 곳 0 재확인 | PASS |
| `user_event_hub.py` | `coalesce_seconds=None` → 만들 때 모듈 값 · 계약 시험 `T/contract/conftest.py` 가 0 주입(WP1 W-5) — 운영 기본 1초 그대로 | PASS |
| 기한·`download=1`·SVG·「빠른 회의」 | WP2 diff 에 없음 | 해당 없음 |
| 옛 `next_meeting_after` 등 WP1 계약 | WP2 가 `finalize_input`·`_prepare_final_notes_in_place` 를 열었지만 하한(`floor_due`)·`meeting_starts_on` 경로는 그대로 | PASS |

---

## 5. BE 리포트 「미결」 판정

| # | 워커가 적은 것 | 판정 |
|---|---|---|
| 1 | 세션 없는 회의도 배치를 낸다 | **결함 → F-2.** 의도(SPEC §4.6 「웜스타트 실패면 다음 배치가 연다」)는 맞지만, 웜스타트가 아직 도는 중과 실패를 가르지 않는다 |
| 2 | 배치 세션 유실도 새 세션 | **계약대로** — SPEC-010 §4.5 「세션 유실로 다시 시작할 때 다시 싣는다」 |
| 3 | 새 세션 배치가 지금까지의 AI 벌을 싣는다 | **계약 보완(필요한 것)** — 배치가 AI 벌 전량 교체라 없으면 앞 구간이 지워진다. SPEC §4.6 문장에 「지금까지의 AI 벌」 을 더하는 것은 planner 몫(WARN W-6) |
| 4 | 맥락 목록에 구성원 실명 | **계약대로**(D-13 「구성원은 다」). 회의 정보 구간은 실명 없음 + 「화자 짐작 금지」 한 줄로 갈랐다. WORK Pre-deploy Check 의 「실명 미유출」 문구는 갱신 필요(planner · W-7) |
| 5 | 맥락 목록 크기 상한 없음 · Codex `E2BIG` 위험 | **계약대로지만 운영 전 실측 필수 — W-1.** 프롬프트를 argv 한 칸으로 넘긴다(`codex_cli.py:327` `[..., prompt]` · `claude_cli.py:282`). 리눅스는 인자 하나에 **128KiB**(`MAX_ARG_STRLEN`) 상한이 있다. 이제 최종 프롬프트가 **매번** 전사 전량 + 맥락 목록 + 두 벌을 싣는다. 넘으면 `OSError` → `ProviderUnavailable` → timeout 이 아닌 실패 3회 → 「실패」 다 — 긴 회의일수록 회의록이 안 선다 |
| 6 | 최종 timeout 여러 번이면 약 30분 · lease 3300 | **결함 → F-1**(셈이 4회를 담지 못한다) |

---

## 6. 시험이 계약을 잡나

| 시험 | 판정 | 비고 |
|---|---|---|
| `T/unit/test_meeting_finalize_service.py` +5 | 강함 | timeout → 새 세션 1회 · 둘째 timeout 「실패」 · 같은 세션 resume 3회 없음(운영 3abe9f9b 모양) · 시도마다 전사·목록·정정 지시 |
| `T/contract/test_meeting_minutes_enhance.py`(12) | 강함 | 배치 재시도 성공 때만 교체 · 실패 때 옛 세션 유지 · 재시도 중 도착분 다음 배치 · 겹침 0 · `null`/`[]`/행 · PATCH 응답 같은 표 · 삭제 시 `null` |
| | **빈틈** | **웜스타트와 배치의 경주(F-2) 시험 없음** |
| `T/unit/test_ai_stage_timeouts.py`(25) | 보통 | env·공장은 강함. **lease 시험은 셈식만 단언** — 루프 최대 호출 수와 대조하지 않아 F-1 을 못 잡는다 |
| `T/integration/postgres/test_meeting_term_corrections_postgres.py`(2) | 강함 | 왕복 · `schema_sync` 계획 |
| `T/unit/test_ai_context_catalog.py`(1) | 약함 | 글자 모양만 · 제외 규칙은 계약 시험이 DB 대조로 본다(괜찮음) |
| `F/features/meetings/MeetingAfter.test.tsx` +6 | 강함 | 표 위치(본문 마지막 블록) · `[]`/`null`/칸 없음 · 상태별 · 서버 `order` 를 일부러 근거 시각과 반대로 줘서 확인 |
| **빠진 시험** | WARN | ① 프롬프트 크기(전사+목록) 상한 근처에서의 동작 ② 모델이 `term_corrections` 칸을 아예 안 냈을 때(§7 H-4) |

FE 실패 9건 = 기준선 8 + `App.test.tsx` 1(워커가 단독 3회 통과 확인 — 흔들리는 시험으로 보임). 내가 돌려 보지는 않았다.

---

## 7. 사람 눈에 이상해 보일 자리

| # | 자리 | 무엇이 걸리나 |
|---|---|---|
| H-1 | **회의 중 AI 탭이 앞부분을 잃는다** | F-2 — 웜스타트가 느린 날, 회의 초반 요약이 다음 배치에서 사라진다 |
| H-2 | **긴 회의의 「실패」** | W-1 — 1시간 넘는 회의 + 큰 조직이면 argv 한도로 합성이 시작조차 못 하고 3회 만에 「실패」. 사용자는 이유를 모른다 |
| H-3 | **「정리 중」 이 길다** | 최종 900초 × 최대 4회 + 재전사 — 진행 표시 없이 최대 1시간 넘게 「정리 중」(SPEC H-9 는 30분으로 적었다 — 실제 상한은 더 길다) |
| H-4 | **「바로잡은 용어 없음」 이 거짓일 수 있다** | 파서는 모델이 `term_corrections` 칸을 **안 냈거나 배열이 아니어도** 빈 표로 보고 시각을 찍는다(`finalize.py:146-147` · 적재 `:949-958`). 정정 pass 를 건너뛴 회의도 「바로잡은 용어 없음」(`[]`)으로 보인다 — `null`(안 돎)과 `[]`(돌았는데 없음)를 가르려던 H-3 의 뜻과 어긋난다. provider 스키마가 칸을 필수로 걸어 드물긴 하다 |
| H-5 | **배치 timeout 뒤 AI 탭이 출렁인다** | 새 세션이 「앞 배치까지 네 벌」 을 받아 다시 쓰므로 안건 제목·묶음이 바뀔 수 있다 — 계약 범위 안이지만 회의 중 화면이 크게 바뀐다 |
| H-6 | **「표에만」 의 인명** | `presumed` 행에 사람 이름 쌍(「김민수 님 → 김민서 님」)이 표로 선다 — 회의록을 공유받은 사람도 본다. 의도대로지만 처음 보면 놀랄 자리 |
| H-7 | **재합성 실패 뒤의 표** | 예전 성공의 보정 표가 「실패」 화면에 그대로 선다 — 최종 벌도 예전 것이라 서로는 맞다. 다만 「이번 합성」 이 아닌 표다 |

---

## 8. FAIL / WARN 목록(재발주용)

### FAIL (2) — BE

| # | 자리 | 무엇 | 고칠 것 |
|---|---|---|---|
| F-1 | `B/bootstrap/settings.py:205-212` · `B/bootstrap/meeting_worker.py:84` · `T/unit/test_ai_stage_timeouts.py`(lease 시험) | lease 바닥 3300초가 한 배달의 최악(최종 호출 최대 4회 · 4800초)을 못 담는다 · 연장 없음 → 합성 이중 실행 | 바닥을 `FINAL_ATTEMPTS + 1` 회로 셈하거나 lease 연장을 단다 · 시험이 루프 최대 호출 수와 대조 |
| F-2 | `B/modules/meetings/batch_service.py:182-201`(웜스타트 락 밖) · `:337-358` · `B/modules/meetings/application.py:1496-1512` | 세션 없는 배치가 진행 중인 웜스타트와 경주 → 세션 덮어쓰기 · AI 벌 앞부분 유실 · provider 이중 호출 | 웜스타트를 회의 락 안에서 · 또는 「웜스타트 중」 동안 세션 없는 배치 보류 · 또는 `record_session` CAS · 경주 시험 1 |

### WARN (8)

| # | 팀 | 자리 | 무엇 | 권장 |
|---|---|---|---|---|
| W-1 | BE(+코디 실측) | `B/platform/codex_cli.py:327` · `claude_cli.py:282` | 프롬프트가 argv 한 칸 — 매번 전사 전량+목록이라 리눅스 128KiB 한도에 닿을 수 있다(미결 5) | 운영 반영 전 「1시간 회의 + 운영 조직 규모」 프롬프트 바이트 실측 · 넘으면 stdin/파일 전달로(별도 결정) |
| W-2 | BE | `B/modules/meetings/finalize.py:146-147` | 모델이 표 칸을 빼도 `[]` 로 기록(H-4) | 칸이 없거나 배열이 아니면 `term_corrected_at` 을 찍지 않는다(→ `null`) — 한 줄 |
| W-3 | BE | `T/unit/test_ai_stage_timeouts.py` | lease 시험이 셈식만 단언 | F-1 과 함께 |
| W-4 | BE | `B/modules/meetings/application.py` `batch_input` | 배치마다 `_ai_track_material` 을 조립(새 세션이 아닐 때도) — 회의 중 조회가 는다 | 새 세션 갈래에서만 읽기(경미) |
| W-5 | BE | 맥락 목록 | 조직 전체라 호출자가 도구로는 못 읽는 업무 제목도 실린다(코디 판정 · D-13 정본) — WP3 에서 AX 대화에 붙을 때 노출 범위가 넓어진다 | 판정대로 두되 WP3 검수 때 다시 본다(참고) |
| W-6 | 문서(planner) | SPEC-010 §4.6 · §4.7-4 | 새 세션 배치에 「지금까지의 AI 벌」 을 싣는 것(미결 3) · 보정 표 위치 「최종 벌에」 → 「상세 최상위」(코디 판정) — SPEC 문장 갱신 | planner |
| W-7 | 문서(planner) | WORK-012 Pre-deploy Check | 「웜스타트에 실명 미유출」 문구가 맥락 목록(구성원 실명)과 어긋난다(미결 4) | planner |
| W-8 | 코디 | 로컬 스택 | 새 표·칸 → `make sync-demo-schema` 뒤 `make local-stack` 재시작(P-4) | 운영 SQL 은 이미지보다 먼저(파일 머리 주석대로) |

### 확인한 것 / 확인 안 한 것

- **확인한 것**
  - diff 전부(BE 20 · FE 5 · 시험 · SQL · domain-model)
  - 호출자 재계수: `meeting_batch_provider` · `create_conversation_provider` · `TimeoutExpired` · `_detail` 경로 · `delete(MeetingRecord)`
  - 운영 SQL↔ORM 칸별 대조 · lease 셈 대 루프 횟수 · 웜스타트 락
- **확인 안 한 것**
  - 시험·빌드·실물 Codex — 금지 · 코디 몫
  - 운영 조직 규모의 맥락 목록 실제 바이트
  - 운영 파드 OS 의 인자 한도 실측

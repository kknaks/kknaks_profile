# WP1-BE 결과 보고 — 운영 버그(서버)

## 상태: done (커밋하지 않음 · 변경은 워크트리 `strong-hajin-enhance` 에만 있다)

- 기준: WORK-012 「Phase WP1-BE」 · SPEC-010 §2.1 · §2.3 · §4.2 · §4.3(참석자) · §4.8 · SPEC-008 §2.2 · §4.4 · §5(원격 이미지 프록시)
- 기준선: `be-baseline.md` — 고치기 전 **기존 실패 0건**. 아래 실패가 있다면 모두 「이번 실패」 다
- 경로 약어: `B/` = `backend/src/ax_workspace/` · `T/` = `backend/tests/`

## 1. 계약 체크박스 7/7

| # | 계약 | 구현 위치 |
|---|---|---|
| 1 | **005 안건 출처(안건별)** — 생성 전용 안건 입력 `{title, source?}` · 안건마다 저장(없으면 `manual`) · `carried` 인데 이어온 회의가 없으면 `422 AGENDA_SOURCE_INVALID` · 회의 중 안건 추가 입구는 옛 모델(제목만) · AX `meeting_create` 도 같은 모양 | 새 모델 `MeetingReservationAgendaInput` `B/modules/meetings/commands.py:138`, `MeetingReservationInput.agendas` 가 이것을 씀 `:155` · 옛 `MeetingAgendaDraftInput` 은 그대로(제목만 · `extra=forbid`) · 규칙 `ensure_reservation_agenda_sources` `B/modules/meetings/domain.py:155` + 예외 `MeetingAgendaSourceInvalid`(`code="AGENDA_SOURCE_INVALID"`) `:58` · 생성 `B/modules/meetings/application.py:418`(판정) `:330`(안건마다 저장 — 옛 회의 단위 `source = "carried" if carried …` 를 지움) · HTTP 422 매핑 `{code, message}` `B/entrypoints/http.py:560` · HTTP 라우트가 `source` 를 넘김 `:930` · AX 제안을 저장할 때 같은 규칙으로 거절 `B/platform/actions.py:321`(`_freeze_meeting_proposal`). MCP `McpMeetingReservationInput` 은 `MeetingReservationInput` 을 상속하므로 같은 모양을 받는다 |
| 2 | **002 수정 참석자 합치기** — `MeetingInfoPatch` 의 `attendee_ids`·`external_attendees` 를 순서 유지 중복 제거 | `B/modules/meetings/commands.py:208,210`(`validate_times` 안, 생성 `:165-166` 과 같은 규칙). 옛 `meeting.update`(`MeetingUpdateCommand`)에는 참석자 칸이 없다 |
| 3 | **006 기한** — 「다음 회의」 = 이월 회의만 · 취소 제외 · 뒤에 시작 · 모든 날짜 KST · 회의일보다 이른 기한은 비움(① 포함) · 프롬프트·스키마 동기화 | 다음 회의 쿼리 `B/platform/meetings.py:786`(같은 owner 의 아무 다음 예약 갈래 삭제 · `status != cancelled` · `starts_at > 이 회의`) · KST `_office_day` `B/modules/meetings/application.py:2001`(`rooms.OFFICE_TIMEZONE` 재사용 — 새 상수 없음) → `starts_on` `:819` · `next_meeting_on` `:821` · `next_meeting_starts_on` `:839` · 새 `meeting_starts_on` `:840` · 하한 `floor_due` `B/modules/meetings/finalize.py:205` · `resolve_due` `:215` · `FinalizationContext.meeting_starts_on` `:104` · 서비스가 넘김 `finalize_service.py:262` · **배치 잠정 후보도 같은 하한**(OQ-1014) `application.py:1555` · 프롬프트 「다음 회의 전날을 네가 셈해 넣지 마라 … 회의일보다 이른 날짜는 서버가 비운다」 `finalize.py:350` · 「이월된 다음 회의」 `:396` · 스키마 설명 `schemas/ai_final_output.json`·`ai_batch_output.json`(`due_candidate`) |
| 4 | **014 받기** — 메일·방 첨부가 `?download=1` 이면 언제나 `attachment`, 없으면 지금 규칙 | `B/entrypoints/http_inbox.py:121`(`_download(force_attachment)`) · 메일 첨부 `:254` · 방 첨부 `:270`(`download: bool = Query(False)`). 머리(nosniff·CSP·CORP)·캐시는 그대로 |
| 5 | **018 원격 SVG** — 바이트로 SVG 판정 → `image/svg+xml` + 지금 머리 · HTML 거절 유지 · docstring 셋 정정 | `sniff_svg` `B/platform/external_inbox_upstream.py:77`(BOM·공백·XML 선언·처리 지시·주석·`<!DOCTYPE svg>` 뒤 `<svg`) · 판정 `:383`(래스터 → SVG 순, 둘 다 아니면 「이미지가 아닙니다」 400 유지) · `SVG_MEDIA_TYPE` `:90`. docstring 정정 셋: 모듈 머리(옛 「리다이렉트는 따라가지 않는다 · SVG 거절」) `external_inbox_upstream.py:9-12` · `sniff_raster` `:52` · `B/modules/external_channels/inbox_html.py:8-10`(옛 「기본 차단 · 이미지 보기」) + 라우트 docstring `http_inbox.py`(「이미지 보기」) |
| 6 | **018 응답 disposition** — 원격 이미지 경로는 래스터·SVG 모두 `inline` | 새 `_remote_image` `B/entrypoints/http_inbox.py:141`(`inline` + 상류가 바이트로 판정한 type + `RELAY_HEADERS` = `default-src 'none'; … sandbox` · nosniff · CORP) · 라우트 `:282`. `_download` 의 「허용 목록 밖은 `attachment`」 를 이 경로는 쓰지 않는다 |
| 7 | **010 사건** — 적재 건수·마지막 수집·백필 진행(커서 포함)이 바뀌는 저장마다 `integration.changed` · 같은 연동은 1초에 한 번 | 실시간 저장(20건 이하)도 `message_arrived` 뒤에 연동 변경 한 건 `B/platform/external_channels_sync_store.py:217` · `update_integration`·`update_room` 이 `_PROGRESS_FIELDS={status, backfill_cursor, backfill_done_at}` 중 하나라도 바뀌면 냄 `:42,258-264,276-282`(옛: 상태가 바뀔 때만) · 카톡 수신 `accepted>0` 이면 냄 `B/modules/external_channels/kakao_ingest.py:267` · **묶어 내기 = 듣는 쪽** `B/platform/user_event_hub.py:30,93,107` — 같은 (회원, 연동)의 첫 사건은 곧바로, 1초 창 안의 나머지는 마지막 하나를 창이 닫힐 때(방이 여럿이면 `room_id=None`). 다른 사건 종류는 묶지 않는다 |

## 2. Code Surface 대비 닿은 자리

표의 줄 수는 FE 를 포함한 값이다. 아래는 같은 패턴을 **`backend/src` 기준선(`f0ad522`)** 에서 다시 센 값과, 그중 바꾼 자리다.

| 행 | 기준선 재계수(backend/src) | 바꾼 자리 / 그대로 둔 자리 |
|---|---|---|
| 002 참석자 | `MeetingInfoPatch` 1곳 | 합침 추가(위 #2) |
| 005 ② `carried_from_meeting_id` | 22줄 / 6파일 | 출처 판정은 `mtg/application.py` 한 곳만 바꿨다. 상세 응답·합성·웜스타트·승인 편집기는 그대로 두었고, `platform/meetings.py` 다음 회의는 006 몫으로 바꿨다 |
| 005 ② 출처 값 `"carried"…\|AGENDA_SOURCES` | 4줄 / 2파일 | 회의 단위 판정 줄을 지웠다. `AGENDA_SOURCES`(넷)는 그대로 두고, 생성용 `RESERVATION_AGENDA_SOURCES`(둘)를 더했다 |
| 005 ② `manual` 자리 넷 | `:467`·`:564`·`:1225`(서버 셋) | 값은 그대로 `manual` 이다. 문구 변경은 FE 몫 |
| 005 ② 안건 입력 모델 `MeetingAgendaDraftInput\|agendas.map(` | 8줄 / 4파일 | 생성(`commands.py`)만 새 모델로 바꿨다. 추가 입구 셋 `mcp.py:905,1779` · `http.py:87` · `bootstrap/application.py:3889` 은 옛 모델 그대로다. **표 밖**: `bootstrap/scenario.py:260`(시드 생성, `source` 없음 → `manual`)은 그대로 둬도 계약에 맞는다 |
| 006 기한 `next_meeting_*\|resolve_due` | 15줄 / 4파일 | 전부 닿았다 — 규칙 · 하한 · 날짜 변환 셋 · 프롬프트 · 서비스 · 스키마 설명 |
| 006 `due_candidate` | 26줄 / 9파일 | 최종 결과(`finalize.py` `_prepare_final_notes_in_place`)와 배치 잠정 후보(`application.py` `replace_ai_track`)에 하한을 걸었다. 승격 `bootstrap/application.py:2015,3867` 은 그대로다 |
| 006 KST `OFFICE_TIMEZONE =` | 3줄 / 3파일 | 새 상수 없이 이미 import 된 `rooms.OFFICE_TIMEZONE` 을 썼다. **표 밖 재검사**: `modules/meetings` 안의 `.date()` 는 `rooms.py:277`(이미 KST) 하나만 남았다 |
| 014 서버 disposition | 21줄 / 5파일 | `_download` 쓰는 곳 셋 중 메일·방 첨부는 `download=1`, 원격 이미지는 `_remote_image` 로 갈랐다. `http.py` 회의 자료·업무 첨부 disposition 은 그대로다 |
| 018 SVG | 7줄 / 2파일 | 판정 · 거절 · docstring 셋 + 라우트 docstring. `inbox_html.py` 의 인라인 `<svg>` 삭제와 `data:` 래스터 규칙은 그대로다(시험으로 고정) |
| 010 사건 | 11줄 / 5파일(사건을 내는 곳 여섯) | 실시간 저장 · `update_integration` · `update_room` · 카톡 수신에 사건을 더하고, 듣는 쪽에 묶어 내기를 더했다. 이미 내던 곳(끊김·OAuth·방 구성·handshake·상태 보고)은 그대로 두었고 묶어 내기의 대상이 된다 |
| 운영 인벤토리 | — | `docs/unified-operations-inventory.json` 에서 **diff 난 3항목만** 패치했다 — MCP `meeting_create` 입력 스키마(안건 `$defs` 이름·`source`) · `GET /api/inbox/mail/{message_id}/attachments/{aid}` · `GET /api/inbox/rooms/{room_id}/attachments/{aid}` 시그니처(`download: bool`). `meeting_agenda_add` 스키마는 바뀌지 않게 했다(옛 모델에 docstring 을 달지 않음) |

⚠ **allowed_paths 밖 1파일**: `docs/unified-operations-inventory.json`. 코드 레포 `AGENTS.md` 와 WORK-012 「운영 인벤토리」 가 「시그니처를 바꾸면 diff 난 항목만 패치」 하라고 정한 파일이다 — 안 고치면 `make test-unit` 의 drift 시험이 실패한다. 코디가 확인해 달라.

## 3. 새 시험 · 고친 시험

**새 시험 파일 3개**
- `T/contract/test_meeting_agenda_source.py`(10)
  - 불러오기 = 미결 `carried` + 손 안건 `manual`
  - [다음 회의 예약] 새 안건만 = 전부 `manual`
  - `carried` + 이어온 회의 없음 = 422 `AGENDA_SOURCE_INVALID`
  - 출처 값 `set`·`derived`·`ai`·`""` = 422(4)
  - 안건 추가 입구 HTTP·MCP 가 `source` 를 거절하고 추가된 안건은 `manual`
  - AX `meeting_create` 직접 생성은 안건별 출처, 위임 제안은 이어온 회의 없는 `carried` 를 거절
  - 수정 참석자 중복 합치기
- `T/contract/test_meeting_due_dates.py`(5) — 이월 회의 1주 뒤 = 전날 · 경로 (b) 같은 owner 다른 예약 = `null` · 경로 (a) 앞 날짜 이월 = `null` · 취소된 이월 제외 · 경로 (c) 다음 날 KST 08:00 → 기한 = 회의일
- `T/unit/test_user_event_hub.py`(2) — 1초 창 · 마지막 하나 유지 · 방이 여럿이면 연동 전체 · 다른 연동·다른 회원·다른 사건은 묶지 않음(타이머 대역 — 스레드 없음)

**기존 파일에 더한 시험**
- `T/contract/test_meeting_finalize.py` — 경로 (d) 「말의 날짜가 회의일보다 이르면 비움」
- `T/contract/test_meeting_memo_batch.py` — 잠정 후보 하한
- `T/unit/test_meeting_domain.py` — `resolve_due`·`floor_due` 하한(같은 날 허용)
- `T/contract/test_external_inbox.py`
  - `download=1` × 이미지/PDF/기타(3) — 미리보기 규칙 유지 · 머리 셋 유지
  - 메일 첨부 `download=1` · 남의 것 404
  - 원격 SVG = `inline` + `image/svg+xml` + 샌드박스 CSP · nosniff · CORP
- `T/unit/test_inbox_rules.py`
  - SVG 바이트 판정(8)
  - 원격 SVG 는 SVG 그대로(GitHub camo 모양)
  - `image/svg+xml` 이라고 선언한 HTML 은 거절
  - 본문 인라인 `<svg>`·`data:image/svg+xml` 은 여전히 삭제
- `T/contract/test_kakao_ingest_and_profile.py` — 카톡 1건 저장에 `inbox.message_arrived` 뒤 `integration.changed`
- `T/integration/postgres/test_external_channels_postgres.py` — 실시간 1건 저장 NOTIFY = `message_arrived` + `integration.changed` · `update_room` 커서만 → 사건 · `update_integration` 커서만 → 사건 · 무관한 칸(`watch_expires_at`) → 사건 없음

**계약이 바뀌어 고친 기존 시험 4**
- `test_meeting_core.py` 둘 — 이어온 회의 안건이 `carried` 가 되려면 이제 안건에 `source:"carried"` 를 실어야 한다
- `test_meeting_finalize.py::test_a_spoken_date_survives…` · `test_meeting_memo_batch.py::test_the_batch_brings_follow_up…` — 고정 날짜(2026-09-18/20)가 「지금」 연 회의보다 이르러 하한에 걸린다. 회의일 뒤 날짜(2099-…)로 바꿨다

## 4. 검증 수치

| 시험 | 기준선 | 이번 |
|---|---|---|
| `make test-unit` | 477 passed | **491 passed** · 0 failed |
| `make test-contract` | 1245 + 직렬 128 passed | **1268 + 직렬 128 passed** · 0 failed |
| `make test-postgres`(격리 `127.0.0.1:55439`) | 106 passed | **107 passed** · 0 failed |
| 운영 인벤토리 drift(`tests/architecture`, test-unit 안) | 통과 | 통과(3항목 패치 뒤) |
| `make verify` 의 나머지 | — | §4-1 |

### 4-1. `make verify` 나머지

| 단계 | 결과 |
|---|---|
| `make test`(전체 병렬 + 직렬) | **1759 + 직렬 130 passed** · 0 failed |
| `make test-scale` | 13 passed |
| `make test-release` | 1 passed |
| frontend 시험 — `cd frontend && npx vitest run --no-file-parallelism`(P-9 · 병렬 vitest 금지 메모) | **8 failed** / 1385 passed (3파일: `features/work/CreateWork.test.tsx` · `CreateWorkLayout.test.tsx` · `TaskDetailDates.test.tsx`) |
| `make frontend-assets` | 통과 |
| `make frontend-build`(tsc + vite) | 통과 |

**frontend 실패 8건은 이번 BE 변경 때문이 아니다.** 이 판에서 BE 는 `frontend/` 를 한 줄도 바꾸지 않았고, vitest 는 서버를 부르지 않는다. 같은 워크트리에서 frontend 워커가 `frontend/src/lib/labels.ts` · `api.ts` 등을 고치는 중이며(`git status`), 실패는 업무 생성·업무 상세의 날짜·메타 격자 문구 비교다. frontend 기준선은 잰 적이 없어서(`be-baseline.md`) 「기존 실패냐 FE 변경이냐」 는 frontend 워커와 코디가 가려야 한다

## 5. 실물 확인 (완료 조건)

- **원격 SVG**: 운영 로그의 camo 주소 원문이 없어서 **같은 주소** 1회는 하지 못했다. 대신 공개 SVG 배지 두 개를 고친 `SafeImageFetcher` 로 실제로 받았고, 둘 다 `image/svg+xml` 로 통과했다 — `https://img.shields.io/badge/build-passing-brightgreen.svg`(1282B) · `https://github.com/actions/checkout/actions/workflows/test.yml/badge.svg`(2303B, 리다이렉트 경유). 옛 코드는 이 둘을 「이미지가 아닙니다」 400 으로 거절했다. 운영 로그의 같은 주소 1회 확인은 **코디 몫**이다
- **Gmail `download=1`**: 로컬 스택을 띄우지 않았다(P-7). 계약 시험으로 메일 첨부 `attachment` 를 확인했다 — 실물은 코디 몫
- **10-07 모양 기한**: 「같은 owner 같은 날 오후 다른 예약」 은 계약 시험 `test_another_booking_of_the_same_owner_is_not_the_next_meeting` 으로 `null` 임을 확인했다(예전에는 회의 전날이었다)

## 6. 다른 팀 영향 (FE)

- `POST /api/meetings` 의 `agendas[]` = `{title, source?: "manual"|"carried"}`. 화면은 불러온 미결 안건에 `"carried"` 를 실어야 한다. 이어온 회의 없이 `carried` 를 보내면 `422 {detail:{code:"AGENDA_SOURCE_INVALID"}}`
- 첨부 받기 = 같은 주소에 `?download=1`. 미리보기·썸네일(`variant=thumb`)은 그대로다
- 원격 이미지 SVG 는 이제 200 `image/svg+xml` `inline` 이다
- `integration.changed` 가 실시간 1건 저장·백필 커서 걸음에도 온다(같은 연동 1초에 한 번). 설정·메시지함 화면은 이미 구독하고 있다

## 7. 미결 · 주의점

1. **묶어 내기는 듣는 쪽(back 의 `UserEventHub`)에서 한다.** 워커의 NOTIFY 는 저장마다 나간다(같은 트랜잭션 원칙 유지). back 프로세스가 여럿이면 프로세스마다 따로 묶는다. 운영은 back 한 벌이라 영향 없음(I-7 실측 뒤 조정)
2. 「진행 칸」 은 `status`·`backfill_cursor`·`backfill_done_at` 셋이다. Gmail 의 `sync_cursor`·`watch_expires_at` 처럼 화면 숫자와 무관한 칸은 사건을 내지 않는다. 방 `name`·`member_count` 변경도 사건 대상이 아니다(SPEC 의 「건수·마지막 수집·백필 진행」 밖)
3. 기한 하한은 `meeting_starts_on` 을 모르면(옛 입력·시험 대역) 걸지 않는다(`FinalizationContext` 기본값 None)
4. SVG 판정은 앞 4096바이트만 본다. `<!DOCTYPE svg …>` 는 허용했다 — SPEC 은 「XML 선언·주석·공백」 만 적었는데, 실제 SVG 파일에 흔한 머리라 더했다. 다르게 원하면 알려 달라
5. 격리 PostgreSQL 컨테이너 `sh-enhance-be-pgtest`(127.0.0.1:55439)는 다음 Phase 시험에 다시 쓰려고 띄워 둔 채로 두었다 — 필요 없으면 `docker rm -f sh-enhance-be-pgtest`

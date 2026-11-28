# day-reservations-fix WP-1 backend (#300) 결과 보고

## 상태: done (A7 실물 e2e 와 KOS 실물 읽기 1회는 pending — 아래 「이슈」)

워크트리 `CENTURION_DAY/day-reservations-fix` · base `65506f35` · 커밋 · push 없음.

## 수행 — 파일 · 모듈

### P1 F6 origin (A1)
- `day/session.py` — `public_origin(request)` **하나**(두 벌 `routers/reservation_displays.py:46` · `routers/api/displays.py:55` 없앰 → import).
- `services/reservation_detail.py` `detail_view(..., origin: str)` 필수 · `services/displays.py` `visit_displays(..., origin: str)` 필수(mypy 가 origin 없는 호출을 잡음).
- 4곳 origin 넘김: `routers/reservation_detail.py` GET 상세 · 동행 저장 · 신분확인, `routers/api/reservations.py` 앱 상세(+ `request: Request`).
- `schemas/reservation_detail.py` 앱 `DisplayProgress.qrUrl` 추가(SPEC-007 §547 · 케이스 763 「앱 상세 `displays[].qrUrl` 채움」 — 그전 앱 JSON 엔 칸 자체가 없었음).
- **두 router 파일에서 고친 줄**(코디 지정 backend 몫):
  - `routers/reservation_detail.py`: import `public_origin`(:33 ~ 40) · `:186-188`(GET 상세) · `:336-338`(동행 저장) · `:418-420`(신분확인) — `detail_view(..., public_origin(request))`.
  - `routers/reservation_displays.py`: import `public_origin`(:31 ~ 38) · 로컬 `def public_origin` 삭제(옛 :46-47). 팝오버 라우트는 그대로 두고 동작은 service 에서 바꿈.

### P2 배치 값 Rule 15 (A2)
- `policies/reservation_layout.py` 다시 씀: `ROW_MINUTES = 60`(배치) · `COMPANION_SLOT_MINUTES = 30`(R71) + `companion_slot()` — `can_join` · `valid_members` 는 30분 그대로.
  - `row_starts(open_min, earliest)` ⓐ ⓘ ⓙ(1시간씩 · 오픈 전 예약이면 1시간씩 앞으로 · 자정 앞 안 늘림 · 24:00 자름).
  - `seat(visits, ends, memberships, grid)` ⓑ ⓖ — 열마다 시작 순 → 같은 시작 R73(닫힘 뒤 · 그룹 먼저(생긴 순) · 생성 순) · 겹치지 않는 가장 앞 자리 · 5 자리 넘으면 그 행 아래 줄 · 동행 = 이어진 빈 자리 첫 묶음(5명씩 줄마다) · 첫 줄 카드가 행을 넘으면 다음 행 첫 줄 자리 셈에 들고 지나는 행의 아래 줄 같은 자리를 덮음(찬 자리) · 아래 줄 카드는 행 끝에서 자름(자리 셈만 · `end_min` 값은 실제 끝).
  - `rows(grid, …)` ⓒ `lines` = 그 행에서 시작한 카드 가장 큰 line + 1(전 열).
  - `Band.end_min`(멤버 가장 늦은 끝) · `start_min` = 멤버 가장 이른 시작.
- `policies/reservations.py`: `axis.start_min` = 첫 행 · `open_min` 없으면 08:00 기준(앞 판 기본값 그대로) · **「최소 30분」 없앰**(Rule 15 ⓓ · 끝 ≤ 시작이면 그 열 간격).
- `dtos` · `presentation` · `schemas/reservations.py` — band `end_min` / 앱 `Band.endMin`. 열 `title` · `interval_minutes` / `title` · `intervalMinutes` 는 이미 있음(새 칸 없음).
- 「볼 것」 `open_min = 0`: `start_time` 없는 시간표는 `_hours` 가 이미 셈에서 뺌(`policies/reservations.py:149` 은 열 회색 면 계산일 뿐) → 행은 00:00 에서 시작하지 않음 — 테스트로 고정. SPEC 은 안 바꿈.

### P3 문진 6개월 · 제출 id (A4)
- `common/config.py` `day_questionnaire_valid_months`(env `DAY_QUESTIONNAIRE_VALID_MONTHS` · 기본 6).
- `policies/questionnaire.py` `add_months`(말일 맞춤) · `is_expired`(KST 날짜 + n 달력 개월 < 오늘 KST) · `health_lines(read=True)` = INPUT_BOX 판정을 `inputText` 유무로(OQ-D46 ①).
- `services/questionnaire_reads.py` `last_of(customer_id, submitted_only=)` — 고객 단위 마지막 살아 있는 행(출처 · 방문 무관) · `expired()` · `summary()` 에 `questionnaire.expired`.
- `services/reservation_detail.py` — 고객 마지막 행 · `questionnaire_done = 행 있음 ∧ 기간 안`(→ [문진 QR] `actions.questionnaireQr` 같은 조건).
- `schemas/reservation_detail.py` 앱 `questionnaire.expired`.
- `services/questionnaire_kos.py` 다시 보내기 대상 = 그 고객 마지막 **제출** 행(`source != read`) · 보내기 성공 시 KOS `questionnaireId` → `external_ref(entity_type = questionnaire_history)`(ON CONFLICT DO NOTHING · 업체 = 그 고객 연결의 vendor).

### P4 KOS 문진 읽기 (A3)
- `emr/kos/identity.py` `PATH_Q_READ = visitor/questionnaire/v1/queries/get-questionnaire-submit/legacy`(내부) · `read_questionnaire`(400 → None) · `submit_questionnaire` → 제출 id 반환(공개 제출 경로 자체는 안 바꿈).
- `emr/kos/mapper_questionnaire.py`(새) — 키 4개 이름 바꿈 · `memo` → `inputText` · `inputType` · `subText` 비움 · `seq` · `phoneNumber` · `phoneticName` 버림 · `visitorName` → `name`.
- `emr/base.py` `read_questionnaire` 기본 = `WriteNotSupportedError` · `normalized_identity.QuestionnaireSubmitData`.
- `services/emr_questionnaire_sync.py`(새) — 대상 = 연결 고객 ∧ (문진 없음 ∨ 기간 지남)(묶음 조회 2번) → 고객마다 읽기(transaction 밖 · 실패 = 그 고객만 · 경고 로그) → `source = read` · `visit_id` null · `fetched_at` · `crm_status` null 행 + `external_ref` · 이미 있는 제출 id 건너뜀 · savepoint 로 동시 회차 유일 위반 흡수 · 행 안 지움.
- `tasks/emr.py` 새 태스크 `day.emr.sync_questionnaires_hospital(hospital_id, customers)` — 일정 회차 `done` ∧ 일정 응답 있을 때 같은 응답 고객(정렬 · 겹침 없음)으로 **따로 발행**(일정 태스크 결과 영향 없음). `emr_sync.Job` 에 `questionnaires`(잠금 TTL = sales 와 같음).
- migration `0032_questionnaire_customer`(head `0031_reservation_request` 다음) — `ix_questionnaire_history_customer_id_submitted_at WHERE deleted_at IS NULL`(고객 단위 판정 · 10초 회차 대상 고르기용 인덱스만 · 새 칸 없음). revision id 는 `alembic_version` 32자 제한으로 짧게.

### P5 팝오버 요청 흐름 (A5)
- `services/displays.py` `create` — 기기 없는 문진 요청 + 그 방문에 기기 없는 열린(pending · opened · 시한 안) 문진 요청 있으면 **그 행 다시 씀**(새 행 · 취소 없음 · OQ-D44) · 기기 줄 = 앞 열린 요청 canceled → 새 요청(그대로) · 스캔 기기 필수(그대로).
- `qr_url_of` · `visit_displays` — `qrUrl` 을 열린(pending · **opened**) 문진 요청에 싣음(다시 쓰는 링크가 opened 일 수 있어서 · cc 는 pending 만이었음 — 아래 「주의」).
- GET `display-targets` 는 요청을 만들지 않음(테스트로 고정). 웹 템플릿 · day.js 는 frontend 가 이미 응답 모달의 `[data-day-res-dp-link]`(= 기기 없는 열린 요청 `qrUrl`)를 읽음 — 계약 맞음.

## 검증 — 명령과 수치
- `./scripts/test.sh -q`(전체 · 격리 인프라): **3344 passed** · 0 failed (7분).
- `./scripts/test.sh --pure -q`(마지막 수정 뒤): **2454 passed** · 890 deselected.
- 새 · 고친 infra 파일 재실행: 32 passed(popover · origin · KOS 문진 읽기 · 앱 띄우기 · 고객 문진).
- `backend/tests/migrations` + `backend/tests/architecture`: 457 passed.
- ruff check · format --check: 통과. taut audit / check: complete · diagnostics 0.
- mypy(전체): **1 error — `backend/tests/day/test_reservation_request_rules.py:191`**(TypeAdapter UnionType · 이 작업이 안 건드린 파일 · 기존). 그래서 `check.sh --pure` 는 mypy 단계에서 멈춤 → 뒤 단계(taut)는 따로 돌려 통과 · frontend npm check 는 frontend 몫이라 안 돌림.
- 새 테스트: `test_reservation_layout.py`(16 · Rule 15 경우 전부 + R71 12:10 · 12:40 안 묶임 · 자동 빠짐 30분) · `test_reservation_rules.py`(웹 view = 앱 JSON 배치 값 같음 · 오픈 전 · start_time 없음) · `test_questionnaire_period_rules.py`(경계 · 말일 · KST) · `emr/test_kos_questionnaire_read.py`(내부 경로만 · 400 · 500 · mapper · 제출 id) · `emr/test_questionnaire_sync_rules.py`(별도 발행 · 실패 격리 · 태스크 이름 · 새 코드 공개 호출 0) · `board/test_reservation_detail_origin.py`(실제 service · 4경로 qrUrl = POST · origin 함수 하나) · `board/test_kos_questionnaire_sync.py`(200 → read 1 · 다시 읽어도 1 · 기간 안 건너뜀 · 지남 다시 · 400 · 오류 · 웹 제출 id 와 같으면 새 행 없음 · 웹 · 앱 expired 같음 · QR 보이기 · 다시 보내기 read 제외) · `board/test_reservation_display_popover.py`(누름 0 · 링크 다시 씀 · 기기 줄 취소 + 새 요청 · 스캔 기기만).
- 고친 기존 테스트(새 계약으로): `test_display_rules.py`(앱 상세 qrUrl 싣음 · expired) · `board/test_public_questionnaire.py`(두 번째 링크 = 다시 씀 · 취소는 기기 줄로) · `board/test_reservation_app_displays.py`(스캔 `qrUrl` = null 키 있음) · `display_support.FakeIdentityKos.submit_questionnaire` 제출 id 반환 · `migrations/test_alembic.py` HEAD.

## 계약 대조
| 계약 | 결과 |
|---|---|
| ① rows · cards · bands(start_min ~ end_min) · camelCase · Band `endMin` | 같음 — 웹 view · 앱 JSON 같은 함수(`board_view`) · 테스트로 같은 값 고정 |
| ② 열 title · interval_minutes / title · intervalMinutes | 같음(이미 있음 · 새 칸 없음) |
| ③ questionnaire.expired · 고객 단위 · KST + n 달력 개월 · [문진 QR] 같은 조건 | 같음 |
| ④ display-targets GET · display-requests POST(kind · device_id) · 링크 다시 씀 · 기기 줄 취소 → 새 · 스캔 기기만 | 같음 |
| ⑤ 모든 경로 같은 origin · displays[].qrUrl | 같음 |
| R71 30분 그대로(함수 · 상수 분리) | 같음 |
| KOS 내부 API 만 · 공개 새 호출 0 | 같음(테스트 고정 · 기존 공개 제출 경로는 안 바꿈) |
| 문구 새로 짓기 없음 | 같음(서버는 글자 없음) |

## 이슈 · 코디가 확인할 것
1. **KOS 실물 읽기 1회 = 실패(pending)** — 데모 지점 · 내부 경로만 · `KOS_CLIENT_TAG` 를 비워(남의 로그인 자동 해제 없음) 실행 → 시스템 계정 sign-in 이 `HTTP 401 InvalidRequestException`(be-kos 때와 같은 5기기 한도로 보임) · 문진 호출 전 멈춤 · 다시 안 함. 태그를 켜면 같은 태그 가장 오래된 로그인 1개를 해제(dev 서버가 끊길 수 있음)하므로 **코디 허용이 필요**. 스크립트: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-CENTURION-DAY-day-reservations-fix/215d09b4-784a-4030-a661-d571fd34c6df/scratchpad/live/qread.py`(출력 = id 앞 8자 · 개수만).
2. **A7 로컬 e2e(KOS 에 문진 제출 → 다음 회차 같은 제출 · D46 ②)는 안 함** — KOS 쓰기라 브리프 「읽기만」 밖. 특히 **제출 응답의 `questionnaireId` 위치를 실물로 본 적 없음**(최상위 → 없으면 `data.questionnaireId` 순으로 읽음 · 없으면 external_ref 를 안 남겨 다음 읽기에서 read 행이 하나 더 생길 수 있음 — SPEC 이 e2e 확인 항목으로 둠).
3. `qrUrl` 을 `opened` 문진 요청에도 실음(D44 「pending · opened 링크 다시 씀」을 하려면 필요 · cc 는 pending 만). 고객 웹 토큰 판정은 그대로. 앱 「이 기기 QR」(기기 없는 문진)도 같은 service 라 열린 요청이 있으면 다시 씀.
4. `open_min` 없음(켜진 시간표 · start_time 모두 없음) = 08:00 기준 행(앞 판 축 기본값 유지) — SPEC 에 정의 없음.
5. KOS 문진 읽기 회차에 고객 수 상한은 안 둠(SPEC 에 없음) — 잠금 TTL(sales 와 같음 · 60초 − 여유) 안에서 끝나지 않으면 회차 전체가 되돌아가고 다음 회차가 다시 읽음.
6. mypy 기존 오류 1건(`test_reservation_request_rules.py:191`)으로 `check.sh` 가 mypy 단계에서 멈춤 — 이 작업 밖.
7. 배포 전: `DAY_QUESTIONNAIRE_VALID_MONTHS`(기본 6) · `DAY_PUBLIC_API_BASE` 확인 · migration `0032` 적용(인덱스만).

# be-fix-2 리포트 — review-code-2 F1 · BW1 ~ BW8 (+ 코디 추가: 여권 스캔 칸 서버 검사)

대상 = 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app-re1` HEAD `fb08fe4e` 위 변경(커밋 안 함 · `app/` 안 만짐).

## 0. 계약 차이(mobile · 코디가 볼 것)

- **고객 POST 순서가 바뀜(BW5)**: IP 속도 제한(5/분) → 토큰 없음 400 `q_token_missing` → 본문 검사 400 `invalid_request` → 토큰 제한(3/분) → 토큰 판정. 전에는 본문 검사가 먼저였다. 틀린 본문도 IP 5번에 들어간다.
- **고객 POST 200 = DAY 저장까지만(BW2)**: KOS 보내기는 응답 뒤(`BackgroundTasks` → `questionnaire_kos.send_detached`, 자기 세션). 응답 시점의 행은 `crm_status = sending`. 결과는 행에만 남는다(`sent` · `failed`).
- **공개 API 의 뜻밖의 실패 = 500 `{detail, code: "internal_error", field: null}` + no-store · no-referrer(BW1)**: 전에는 머리 없는 Starlette 500이었다.
- **여권 스캔 저장 `fields` 400 이 늘어남(코디 추가)**: `nationality` = `[A-Z]{2}` · `passportNumber` = `[A-Z0-9]{1,9}` · 날짜 = `YYYY-MM-DD` 만(전에는 `YYYYMMDD` 도 통과). `field = fields.<칸>`. 앱 `scanValueOk` 와 같은 규칙이다.
- 고객 웹 토큰: 읽은 뒤 주소창에서 `#토큰` 을 지운다. 새로고침용 사본은 그 탭 `sessionStorage` 에만 둔다(BW7).

## 1. 처분표

| # | 처분 | 무엇을 했나 | 바꾼 곳 |
|---|---|---|---|
| **F1** | 고침 | 요청 `done` 넘김 = 원자적 `UPDATE … WHERE id ∧ 살아 있음 ∧ (pending ∧ 여는 시한 안 ∨ opened ∧ 쓰는 시한 안) RETURNING id`. 못 잡으면 rollback 뒤 다시 읽어 409 `q_submitted` · 410 `q_canceled` · `q_expired`. 넘김을 먼저 하고 그다음 답 행을 쓴다(같은 트랜잭션). 마지막 보장 = `questionnaire_history(display_request_id) WHERE deleted_at IS NULL` 부분 유일(공용 `live_unique` — 저장소 규칙 「유일 = 살아 있는 행끼리」 · `test_constraints.py` 가 강제 · null 은 PostgreSQL 에서 겹쳐도 됨) → `IntegrityError` = 409. `expire_open` 은 `populate_existing`(세션의 낡은 값으로 판정하지 않음). 여권 스캔 저장도 같은 `finish` 를 쓴다. | `services/displays.py:452`(`finish`) · `:207`(`expire_open`) · `services/questionnaire_public.py:306`(`submit`) · `:337`(`_save` · `:383` IntegrityError) · `services/passport_scan.py:402` · `models/reception.py:107` · `migrations/versions/20261125_0029_display_questionnaire_kos.py:50` · `:60` · `tests/day/test_constraints.py`(`_questionnaire_request` · `UNIQUE` 사례 추가) |
| BW1 | 고침 | Redis 잠금을 못 잡으면(`RedisError`) 잠금 없이 간다. 1회 보장은 F1 의 DB 몫이다. `PublicRoute` 가 `Exception` 도 잡아 500 `internal_error` + 공개 머리를 단다(로그 = 예외 타입만). | `questionnaire_public.py:321-330` · `routers/api/public_questionnaire.py:62` |
| BW2 | 고침 | 커밋 · 신호 뒤 바로 200. KOS 는 `BackgroundTasks` 로 응답 뒤에 보낸다. 프로세스가 그 사이 죽으면 행은 `sending` 으로 남고, 기존 멈춤 판정(OQ-D41)이 「실패」 + [다시 보내기]로 보인다. 새 정책은 없다(SPEC-007 「DAY 먼저 → KOS」 · 결정 5 안). taskiq 는 쓰지 않았다 — 새 task name 은 외부 계약이 되고, 같은 결과를 멈춤 판정이 이미 덮기 때문이다. | `routers/api/public_questionnaire.py:118-133` · `services/questionnaire_kos.py:128`(`send_detached`) |
| BW3 | 고침 | `send` 는 행을 `populate_existing` 으로 읽는다. `sending` 이 아니면 보내지 않는다. 결과 쓰기 = `WHERE crm_status='sending' ∧ updated_at = 그 회차가 읽은 값`. 다른 회차가 다시 잡았으면 버리고 로그만 남긴다. KOS 호출 전체 = `asyncio.timeout(send_limit())`. `send_limit` = HTTP 한도 + 멈춤 여유/2 로, 멈춤 판정보다 짧다. 넘기면 `failed`(`TimeoutError`). | `services/questionnaire_kos.py:73-125` · `services/questionnaire_reads.py:26` |
| BW4 | 고침 | 불러오기에서 KOS 를 받은 뒤 `expire_open` → `get(..., with_for_update, populate_existing)`. 닫혔으면 410 / 409. | `questionnaire_public.py:245-256` |
| BW5 | 고침 | 라우터가 `gate_post`(IP 5/분 · 토큰 없음)를 본문 검사 전에 부른다. | `questionnaire_public.py:299` · `routers/api/public_questionnaire.py:120` |
| BW6 | **기록만(코드 그대로)** | Redis 장애 = 속도 제한 · 거절 로그 간격이 모두 꺼진다(be-2 §5 결정). 남는 보호는 43자 HMAC 토큰 + (이번부터) DB 의 1회 보장이다. 결정을 유지한다면 SPEC-007 OQ-D40 에 「Redis 장애 = 제한 끔」을 적어야 한다(spec-sync 몫). 거절 로그 폭주(장애 때 거절마다 `event_log` 1행)는 그대로 두었다. 정책 문제라 손대지 않는다. | — |
| BW7 | 고침 | 토큰을 읽은 뒤 `history.replaceState` 로 주소의 `#` 을 지운다. 새로고침이 깨지지 않게 그 탭 `sessionStorage` 에 사본을 둔다(try/catch · 막힌 브라우저 = 주소 값만 씀). | `static/day.js:5473-5487` |
| BW8 | 고침 | 아래 §3 시험. 기존의 비어 있던 속도 시험을 지웠다(갈래별 새 시험으로 대체). `:241` 의 항상 참인 단언 → 「다시 시도」가 틀에 없음. | `tests/day/board/test_public_questionnaire.py:218` · `:228` |
| 코디 추가 | 고침 | 날짜 · 성별 검사는 이미 있었다. 국적 · 여권번호 검사가 없어서 넣었다. 날짜 `YYYYMMDD` 가 통과하던 구멍도 막았다. 근거 = U-27 자리 글 「예: KR」 + 앱 MRZ alpha-3 → alpha-2 · MRZ 문서번호 칸(TD3 9자). | `services/passport_scan.py:83-89` · `:116` · `:126-128` |

## 2. migration 0029 를 고친 이유

0029(`0029_display_questionnaire_kos`)는 이번 WORK-002 묶음에서 처음 생겼고, 아직 dev · prod 어디에도 올라가지 않았다(push 전). 그래서 새 revision 을 잇지 않고 0029 의 upgrade 에 부분 유일 인덱스 `uq_questionnaire_history_display_request_id`(`WHERE deleted_at IS NULL`)를, downgrade 머리에 지우기를 넣었다. 모델 `__table_args__` 와 같은 정의라 `alembic check` 차이 0이다(`tests/migrations/test_alembic.py` 왕복 · check 통과).

## 3. 시험

새 파일:
- `backend/tests/day/board/test_public_questionnaire_guard.py`(infra · 16개):
  - F1 동시 제출 2 → 답 1행 + 409 `q_submitted`(두 세션을 같은 자리에서 세운 뒤 놓음 · Redis 잠금 끔)
  - F1 제출 중 [취소] 커밋 → 410 `q_canceled` · 답 0 · KOS 0 · `canceled` 유지
  - F1 같은 요청 답 2행 INSERT = `IntegrityError`
  - 60분 시한(`fillUntil` = opened + 60분 · 61분 지남 → 410 `q_expired` · 답 0)
  - 속도 제한: GET 30/IP · POST IP 5(본문보다 먼저) · 토큰 3(토큰마다 — 다른 토큰은 통과)과 IP 6번째의 갈래 · 틀린 토큰 10 → 맞는 토큰도 429
  - `X-Day-Client-IP`: 앞단 설정이 없으면 무시 · 믿는 앞단이면 머리 IP 로 셈 · 다른 IP 는 통과 · IP 꼴이 아니면 소켓 주소
  - `phoneticName` · `registrationNumber` · 모르는 최상위 키 = 400 + 그 칸
  - BW1: 잠금 Redis 장애여도 저장 1회 · 두 번째 409. 뜻밖의 예외 = 500 `internal_error` + 머리
  - BW2: 응답 시점 `sending` · KOS 0 · 응답 뒤 일 1건
  - BW3: 다시 잡힌 행의 결과를 덮지 않음 · 전체 시한 넘김 = `failed`/`TimeoutError`
  - BW4: 양식을 받는 중 취소 → 410
- `backend/tests/day/board/test_reservation_app_display_scope.py`(infra · 3개):
  - 대상 기기 거르기: 폰 · 코디 아닌 직무 · 끊긴 세션 · 만료된 세션 · 다른 병원 → 목록 밖 · 만들기 404 · 요청 0
  - 다른 병원: 만들기 · 닫기 404(상태 안 바뀜) · 메우기 = 빈 목록
  - 스캔 저장 `displayRequestId` 가 다른 기기 · 문진 종류 · 다른 병원 방문이면 404 · 어느 요청도 `done` 이 되지 않음
- `backend/tests/day/test_passport_scan_fields.py`(DB 없음 · 2개 / 11개 경우): 국적 · 여권번호 · 성별 · 날짜 꼴 400 + `fields.<칸>` · 맞는 값 통과

수치:
- F1 회귀 증명: 같은 F1 시험 3개를 HEAD 서비스 · 모델 · migration 으로 돌림 → **3 failed**(`['ok','ok']` · 취소 뒤 200 · 제약 없음). 고친 코드 → 통과.
- `./scripts/test.sh` 로 4 파일(`test_public_questionnaire.py` · `_guard.py` · `test_reservation_app_displays.py` · `_display_scope.py`) → **38 passed**. `test_passport_scan_fields.py` → **11 passed**. `test_alembic.py` 포함 앞 회차 → 29 passed.
- `scripts/check.sh` 3회:
  - 1회차: ruff E501(긴 줄 7개)로 실패 → 고침.
  - 2회차: 정적 검사(ruff · mypy · taut · frontend) 전부 통과. 시험 **3023 passed · 1 failed** — `test_constraints.py::test_유일_사례는_모델의_부분_유일_인덱스_전부다`(유일 = `deleted_at IS NULL` 만 허용 · `UNIQUE` 사례 등록 강제). 인덱스를 `live_unique` 로 바꾸고 사례를 등록했다. 그 뒤 `test_constraints.py` + `test_alembic.py` + `_guard.py` → **81 passed**.
  - 3회차(최종 · 맥이 잠들었다 깬 직후): 정적 검사 전부 통과. 시험 **3024 passed · 2 failed** — `backend/tests/day/chat/test_devices_push.py` 의 `test_늦게_온_이전_세션_등록은_결속_토큰을_바꾸지_않는다` · `test_해제는_요청_세션_결속일_때만_늦은_로그아웃이_새_등록을_지우지_않는다`.
    - **이번 변경과 무관으로 판단**: 이 파일과 기기 등록 경로는 손대지 않았다. 2회차 전체 실행에서는 통과했다. 단독으로 두 번 돌리면 **12 passed · 12 passed**. 두 시험은 `now - 5분` 처럼 시각에 기대는 세션 순서 시험이라, 잠자기 · 깨기의 시계 흔들림을 의심한다(원인을 확인하지는 않았다). 기록 = `.local/checks/20261126-003256-49895`.
    - 브리프 「check.sh 1회」를 넘겨 3회 돌렸다. 4회째는 돌리지 않았다 — 코디가 PR 전에 한 번 더 돌릴 것.

## 4. 남은 것 · 질문

1. **(질문 · 정책)** 국적을 alpha-2 로 강제한 근거는 U-27 자리 글 「예: KR」과 앱 MRZ 변환이다. KOS 고객 수정의 `nationality` 가 alpha-2 만 받는지는 KOS 문서로 확인하지 않았다(SPEC-003 OQ-A9 「KOS 국적 값이 두 글자 코드가 아닐 때」 · SPEC-000 OQ-02-1 alpha-2 승인 대기와 이어짐). alpha-3 도 받아야 한다면 서버 · 앱 규칙을 같이 넓혀야 한다.
2. BW6 = SPEC OQ-D40 에 「Redis 장애 = 제한 끔」을 적을지(spec-sync · 사용자).
3. BW8 중 「같은 계정 다른 기기 = 실제 스트림 두 개」 시험은 넣지 않았다. 이번 지시 목록 밖이고, 거르개(`own_device`) 단위 시험이 이미 있다.
4. BW2: 응답 뒤 보내기는 프로세스 안 일이다. 배포 · 재시작으로 죽으면 그 행은 멈춤 한도(기본 75초) 뒤 「실패」 + [다시 보내기]로 보인다(자동 재전송 없음 — 기존 OQ-D41 그대로).

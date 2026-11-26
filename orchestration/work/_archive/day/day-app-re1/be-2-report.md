# be-2 결과 보고 — WORK-002 backend+web (Delivery CENTURION_DAY#287)

## 상태: done (코드 · 테스트 · check.sh — 실물 A6 = 코디 몫) · 커밋 없음(워크트리 변경만 · 기준 `96036397`)

## 0. 계약 차이 — mobile · 코디가 먼저 볼 것

| # | 자리 | 계약(이름 제안) | 구현 | 이유 |
|---|---|---|---|---|
| D1 | DB 칸 이름 | `questionnaire_history.kos_status` · `kos_error` · `kos_sent_at` · enum 이름 BE | **`crm_status` · `crm_error` · `crm_sent_at`** · enum `questionnaire_crm_status` | 레포 구조 검사 `tests/day/test_models.py` `VENDOR_COLUMNS` 가 핵심 테이블의 `kos_status` 칸을 막는다(업체 전용 칸 금지 · AGENTS). 값 · 뜻 같음. spec-sync 때 DAY-SPEC-000 칸 이름 고침 필요 |
| D2 | 앱 상세 JSON 초진 문진 상태 키 | 이름 없음 | `questionnaire.sendStatus`(sending · sent · failed — 멈춘 sending = failed) · `time` · `submittedAt` · `canResend`(웹만) · 건강정보 = 따로 `health[]{question, answer}` · 행 없음 = 둘 다 `null` | mobile 은 둘 다 읽게 해 둠(app-2 §5-3) |
| D3 | KOS 고객 연결 없음(워크인) 409 코드 | 이름 WORK(OQ-D29) | **`customer_not_linked`** | 스캔 저장 · 여권 값 읽기 둘 다 |
| D4 | 닫기 「이미 닫힘」 409 코드 | 이름 없음 | **`display_closed`**(cc 이름) · 다시 보내기 「실패 아님」 409 = **`questionnaire_not_failed`** | |
| D5 | 앱 상세 `reservation.companions` | (W2 「동행 이름」) | **`[{visitId, name}]`** | 코디 지시(app-2 §5-2 · A-63 동행 누름 = 그 상세) — 반영함 |
| D6 | iOS 띄우기 푸시 본문 | W5 는 Android data 칸만 | APNs 본문 = `aps.alert{title, body}`(sound 없음) **+ 최상위 `kind: display` · `requestId` · `environment` · `hospitalId`**(Android data 와 같은 칸 — FCM 은 같은 본문을 `data_of` 로 바꿈) | 코디 지시(app-2 §5-6) — 처음부터 그렇게 지음 · 시험 고정 |
| D7 | 여권 스캔 저장 응답 `identity` | 모양 없음 | `{status: "confirmed", method: "app_scan"\|"app_manual", checkedAt}` | |
| D8 | 띄우기 만들기 응답 | `{requestId, kind, status, expiresAt, deviceName?, qrUrl?}` | 그대로 — `deviceName` · `qrUrl` 는 없으면 `null`(키는 늘 있음) | |
| D9 | 상세 `displays[]` 칸 | 종류 · 상태 · 기기 이름 · 시각 | `{requestId, kind, status, deviceName, createdAt, openedAt, closedAt, expiresAt}` · 시한은 **읽을 때** 판정(`expired` 로 보임 · 행은 다음 쓰기 때 바뀜 — OQ-D30) · `qrUrl` 은 웹만 | |
| D10 | 저장소 꺼짐 | 「저장소 실패 = 503 photo_disabled · 앞 단계(KOS 고객 수정)는 남음」 | 저장소가 **설정 안 됨**이면 KOS 를 부르기 **전에** 503 `photo_disabled`(고객 수정도 안 함) · 쓰는 중 실패면 계약대로 앞 단계 남음 | 설정 꺼짐은 미리 알 수 있어 부작용을 남기지 않음 |
| D11 | 고객 문진 KOS 실패 코드 | 502(OQ-D39 기본값) | 불러오기 KOS 실패 = **502 `kos_unavailable`**(직원 경로 503 과 다름 · cc 와 같음) | |
| D12 | `qweb_denied` 기록 | 이유 · IP 안 남김 · 1분 1줄 | 그 요청의 **병원을 아는 거절만** `event_log`(canceled · expired · submitted · submitting) — 틀린 토큰 · 속도 제한은 병원을 몰라(`event_log.hospital_id` not null) 서버 로그만 | |
| D13 | 쓰는 시한 | 문진 = 처음 연 뒤 60분 | **스캔 `opened` 도 같은 60분**으로 `expired`(열린 스캔 화면이 끝없이 남지 않게) | 계약에 스캔 opened 시한 없음 → 기본값 |
| D14 | 앱 목록 JSON | 칸 이름 WORK | 웹 값 camelCase(`today · date · weekday · isToday · nowMin · openMin · axis{startMin, endMin, timeGraySpans} · columns · cards · rows · bands · filter{total, counts} · notice{content, date} · inhouse{chips, items}`) · `filter.counts` 키 = 단계 이름 그대로(snake) | |
| D15 | 앱 상세 날짜 · 시각 | — | 웹과 같은 글자(`reservation.date` = `2026.11.25` · `start`/`end` = `HH:MM` · 없으면 null) | |
| D16 | 고객 문진 웹 HMAC 키 | 「서버 비밀」 | 새 env 없음 — `ENCRYPTION_KEY` 에서 `sha256("day-qweb\|"+키)` 로 따로 뽑음 | deploy env 금지 · 새 비밀 칸 없음 |
| D17 | `qrUrl` origin | `{DAY 공개 origin}` · 설정 이름 WORK | `DAY_PUBLIC_API_BASE`(있음) · 없으면(로컬) 그 요청 주소 | 로컬 시뮬레이터 E2E 용 |

새 설정(env · 기본값 · 배포 env 안 건드림): `DAY_DISPLAY_TTL_MINUTES=10` · `DAY_QWEB_FILL_MINUTES=60` · `DAY_QWEB_STUCK_MARGIN_SECONDS=60`(멈춘 sending = `EMR_HTTP_TIMEOUT_SECONDS` + 이 값 · OQ-D41).

## 1. 경로 표

인증 = `/api` 공통(Bearer · 쿠키 — 쿠키 쓰기는 CSRF) · 오류 `{detail, code, field}` · 검사 401 → 403 → 400 → 404 → 409.

| 메서드 · 경로 | 인증 · 권한 | 응답 | 오류 |
|---|---|---|---|
| GET `/api/reservations?date=&poll=` | `reservation` view | 목록 JSON(D14 · 쓰기 칸 · KOS id 없음) | 400 date · 401 · 403 |
| GET `/api/reservations/stream` | `reservation` view | SSE `reservation`(version) · `display`(방문 id) · `session_expired` | 401 · 403 |
| GET `/api/reservations/visits/{v}` | `reservation` view | 상세 JSON + `displays[]` + `actions{questionnaireQr, passportScan, sendToTablet}`(여권 칸 · 쓰기 칸 · 링크 · KOS id 없음) | 400 · 404 |
| GET `/api/reservations/visits/{v}/passport` | `reservation.detail` edit | 7칸(DAY 사본 · 빈 고객 = null) | 403 · 404 · 409 `visit_not_today` · `visit_stage_changed` · `customer_not_linked` |
| GET `/api/display-targets` | `reservation.detail` edit | `{targets[{deviceId, name, online}]}` | 403 |
| POST `/api/visits/{v}/display-requests` `{kind, deviceId?}` | edit | `{requestId, kind, status, expiresAt, deviceName, qrUrl}` | 400 kind · scan 에 deviceId 없음 · 404 방문 · 기기(목록 밖) · 409 `reservation_past_date` · `visit_not_today` · `visit_stage_changed` |
| POST `/api/display-requests/{id}/close` `{status: canceled}` | edit | `{ok}` | 400(다른 값) · 404 · 409 `display_closed` |
| GET `/api/display-requests/pending` | 로그인 세션(자기 기기 · 기기 없으면 빈 목록) | `{requests[{requestId, kind, visitId, expiresAt, qrUrl}]}` · 스캔을 돌려주면 `opened` | 401 |
| POST `/api/visits/{v}/passport-scan` multipart `fields`(JSON) · `photo`(JPEG ≤5MB) · `manual` · `displayRequestId` | edit | `{identity, photo{id, kosSynced}\|null, kos{customer ok\|unchanged, photo ok\|failed\|skipped\|null}}` | 400(칸 · 모르는 키 · 사진 형식 `photo_type` · 사진 없음) · 413 `photo_too_large` · 404(방문 · displayRequestId 가 이 방문 · 이 기기 · scan 아님) · 409(D3 포함) · 503 `kos_unavailable`(고객 수정 실패 = 아무것도 안 남김) · `photo_disabled` · 401(직원 KOS 토큰 거절 = 세션 끝냄) |
| POST `/api/id-photos/{id}/kos-retry` | edit | `{photo{id, kosSynced}, kos{photo}}` | 400 · 404 · 409 · 503 |
| PUT `/api/devices/{install_id}/name` `{name}` | 로그인 세션(자기 기기) | `{ok}`(등록 전이면 바꾸지 않음) | 400 빈 값 · 40자 넘음 |
| PUT `/api/devices/{install_id}` + `name?` | 기존 | 등록 때 이름도 둠 | |
| GET `/api/notifications/stream` | 기존 | + `display {requestId, kind, visitId}` — **그 세션 기기 연결만**(같은 계정 다른 기기 · 기기 없는 연결 = 안 받음) | |
| GET `/api/public/questionnaire?lang=` | **로그인 없음** · 헤더 `X-Questionnaire-Token` 만 · `Authorization` 무시 | `{customerName, language{code, source, options}, form{pages}, agreements, prefill, fillUntil}` · 첫 성공 = opened | 400 `q_token_missing` · 404 `q_not_found` · 409 `q_submitted` · 410 `q_expired` · `q_canceled` · 429 · 502 `kos_unavailable` — 응답마다 no-store · no-referrer |
| POST `/api/public/questionnaire` | 같음 | `{ok}`(DAY 저장되면 200) | 위 + 400 `invalid_request`(최상위 모르는 키 · `registrationNumber` · `phoneticName`) · 409 `q_submitting` |
| GET `/q` | 로그인 없음 | Jinja 페이지(no-store · no-referrer · CSP 그대로) | |
| 웹 GET `/reservations/visits/{v}/display-targets?kind=` | 쿠키 · edit | 기기 고르기 조각 | 400 kind |
| 웹 POST `/reservations/visits/{v}/display-requests`(form kind · device_id) | 쿠키 + CSRF · edit | 최신 모달 조각(`#modal-root` · 진행 칸 · 문진 QR) | 위와 같음 |
| 웹 POST `/reservations/display-requests/{id}/close`(form status=canceled) | 같음 | 최신 모달 조각 | 400 · 404 · 409 |
| 웹 POST `/reservations/visits/{v}/questionnaire/resend` | 같음 | 최신 모달 조각 | 409 `questionnaire_not_failed`(원자적 갱신 — 같은 행 동시 두 번 = 한 번) |
| 웹 SSE `/reservations/stream` | 기존 | + `display`(방문 id) → 열린 모달이 그 방문이면 다시 받기 | |

## 2. 구현 요약 — 파일

- **DB · migration** `migrations/versions/20261125_0029_display_questionnaire_kos.py`(0028 뒤 · up/down): `display_request.qr_token_hash` · `qr_nonce` null 허용 · enum `questionnaire_crm_status` + `questionnaire_history.crm_status · crm_error · crm_sent_at`. 모델 `models/reception.py` · enum `enums/reception.py`(`DisplayKind` · `IdentityMethod` · `QuestionnaireCrmStatus`).
- **규칙(순수)** `policies/displays.py`(HMAC 토큰 43자 · sha256 · 시한 · 멈춘 sending) · `policies/questionnaire.py`(cc 언어 표 · 금지 칸 · 건강정보 줄) · `policies/reservation_detail.py`(`qr` · `scan` = D55 + 문진 안 함 · 신분 미확인 + `reservation.detail` edit).
- **EMR** `emr/normalized_identity.py` · `emr/base.py`(기본 = `WriteNotSupportedError`) · `emr/kos/identity.py`(여권 = 직원 토큰 `get-visitor` → `PERSONAL_KEYS` + 바뀐 칸 → `update-visitor-personal-information` → 다시 읽기 · 문진 = 공개 양식 · 약관 · 제출 + 내부 `get-visitor`(시스템) · 같은 `KosClient` timeout).
- **서비스** `services/displays.py`(목록 · 만들기 · 닫기 · 메우기 · 진행 · 닿기) · `display_push.py`(+ 태스크 `day.notifications.display_push` · `tasks/notifications.py`) · `passport_scan.py` · `id_photo_kos.py`(시술전후 KOS 경로 재사용 · 분류 「여권」 · 장비 「태블릿」 · 메모 비움) · `questionnaire_public.py`(Redis 속도 제한 · 잠금) · `questionnaire_kos.py`(보내기 · 다시 보내기) · `questionnaire_reads.py` · `reservation_detail.py`(문진 · 건강 · `displays` · `can_detail`) · `push.py`(`device_id` 한 행 · `display_request_id` 기록) · `notification_events.py`(`display` 발행 · 「접속 중」 Redis 표시 25초) · `live.py` · `board_events.display_changed` · `devices.rename`.
- **라우터** `routers/api/reservations.py` · `api/displays.py` · `api/public_questionnaire.py`(route class 로 오류에도 머리) · `api/devices.py` · `api/notifications.py`(자기 기기 거르기) · `api/streams.py`(`accept`) · `api/ext_peer.py`(`client_address` 분리 — 같은 믿는 앞단 규칙) · `routers/reservation_displays.py` · `reservations_streams.py`(`display` · 앱 `app=True`) · `public_pages.py`(`/q`).
- **스키마** `schemas/reservations.py` · `reservation_detail.py` · `displays.py` · `public_questionnaire.py` · `devices.py`(`name`) · `events.py`(`DisplayEvent`).
- **웹** `templates/partials/reservations_display.html`(버튼 · 진행 칸 · 초진 문진 · 건강정보) · `reservations_display_targets.html` · `reservations_detail.html`(외국인 신분확인 「O」 + `data-day-res-id-ok`) · `templates/questionnaire.html` · `reservations.html`(sse-swap `display`) · `presentation/qr.py`(서버 QR SVG) · `presentation/questionnaire_text.py`(cc `text.ts` 6언어 그대로 · cc `fake` 글자만 뺌) · `static/day.js`(남은 시간 · QR 닫기 · SSE `display` · [상담 대기] 외국인 신분확인 · 고객 문진 화면 전체 · `runtime.exchange`) · `styles/app.css` → 빌드 `static/day.css`.
- **저장소** `adapters/storage/contracts.py` — 용도 폴더 `identity/{병원}/{32hex}.jpg`.
- **의존성** `pyproject.toml` · `uv.lock` — **`segno>=1.6,<2`**(순수 Python · 의존 없음 · 타입 있음): 웹 [문진 QR] 「이 화면 QR」을 서버에서 SVG 로 그림 — CSP · 「JS 는 day.js 하나」 규칙 때문에 브라우저 QR 라이브러리를 벤더링하지 않음.
- **Caddyfile** 안 바꿈 — 스캔 multipart(≤5MB + 칸)는 지금 6MiB 상한 안 · 문진 공개 경로 머리는 앱이 단다. `X-Day-Client-IP` 는 이미 `{remote_host}` 를 싣고 `DAY_EXT_PROXY_HOST` 설정일 때만 믿는다.

## 3. 검증

- `scripts/check.sh` 전부 통과 — 2995 passed(§3-1).
- 중간: `scripts/test.sh --pure` 2199 passed(새 규칙 전) · 새 infra 파일 `test_reservation_app_displays.py` 13 passed · `test_public_questionnaire.py` 7 passed · `tests/day/web` 251 passed · `test_alembic.py` + enum 11 passed · `test_display_rules.py` 14 passed.
- 새 시험: 경로 계약(성공 · 400 · 401 · 403 · 404 · 409 · Bearer · 쿠키 CSRF) · 기기 하나 닿기(채널 메시지 대상 세션 · 연결 거르기 · 푸시 = 그 기기 하나 · 두 번 안 감) · 스캔 저장(직원 토큰 · 고객 수정 실패 = 아무것도 안 남김 · 분류 없음 skipped → 다시 올리기 · 손 입력 · 413 · 형식) · 문진(허용 키 · Authorization 무시 · 머리 · 토큰 없음 / 틀림 / 닫힘 / 지남 · 1회 · 금지 칸 · DAY 먼저 → KOS sent / failed · 멈춘 sending → 다시 보내기 · 속도 제한 429) · 웹 Jinja(QR · 진행 줄 · 초진 문진 · 건강정보 · 신분확인 O · 기기 조각) · migration 0029 왕복.
- 기존 시험 고친 것(새 동작 · 레포 규칙): 상세 화면 [문진 QR] · [여권 스캔] 켬 · sse-swap · 고정본 다시 씀 · 칸 스냅샷 · enum 수 52 · 저장소 키(`identity/` 이제 jpg 허용) · 화면 문구 근거 표 · head 0029 · 상세 화면 시험 700줄 넘어 고침 5 시험을 새 파일로.

### 3-1. check.sh — **전부 통과**

`scripts/check.sh` = 구조 · Jinja(680 소스) · ruff · format · mypy · taut-audit · taut-check · frontend(ESLint · Stylelint · Prettier · CSS 재현) · tests(격리 PostgreSQL · Redis) → **2995 passed in 361s** · 증거 `.local/checks/20261125-175310-95709`. 중간에 Taut 가 잡은 것(응답 스키마 수동 매핑 SCHEMA003 · 요청 스키마 extra 금지 SCHEMA001 · 업무 예외 코드) · 파일 700줄 · 의미 id 타입은 모두 코드로 고침(제외 · baseline 없음).

## 4. 코디 실물 확인 순서(A6 — 로컬 KOS 데모 · 각 1회)

1. migrate(0029) → 웹 로그인(간호 · `reservation.detail` edit) · 앱(태블릿)은 **직무 코디** 계정으로 로그인 + 푸시 등록(기기 `kind = tablet`) · 설정 「이 기기 이름」.
2. 웹 예약 현황 → 오늘 · 접수 · **외국인** 고객 상세 → [여권 스캔] → 기기 목록에 그 태블릿(「 · 접속 중」) → 고르기 → 진행 줄 「{기기}에 보냈어요 · 여는 중…」 · 태블릿에 즉시(SSE) 또는 알림 → 열면 「스캔 중 · 촬영 대기 중…」.
3. 태블릿 스캔 저장 → **KOS 고객 여권 칸 바뀜**(KOS 웹 고객 상세 · 기록 = 코디 계정) · **KOS 일정 사진 탭에 분류 「여권」**(데모에 분류 없으면 `skipped` — 그때는 데모 분류 추가 후 [사진 다시 올리기]) · 웹 모달 신분확인 「O」 · [상담 대기] 신분확인 칸 채움.
4. 웹 [문진 QR] → 이 화면 QR(남은 시간) → 휴대폰으로 찍기 → `/q#…` 언어 칩 · 기본 정보 · 양식 · 동의 → 제출 → **KOS 문진 제출본 생김**(KOS 고객 문진) · 웹 「제출됨 · HH:MM」 + 「보냄」 · 건강정보 줄. (KOS 실패 확인은 선택 — 실패면 「실패」 + [다시 보내기])
5. 앱 예약현황 목록 · 상세 · 「태블릿에 보내기」(문진) → 태블릿 QR 전체 화면.

## 5. 미결 · 주의

- 고객 문진 공개 POST 본문의 `answers[]` · `agreements[]` 항목 = 자유 JSON(KOS 키 그대로 넘김) · 필수 키(`parentQuestionId` · `parentQuestionTitle` · `id` · `title` / `agreed` bool)만 검사 — Taut SCHEMA001 이 `extra="allow"` 모델을 막아서.
- **SPEC 고칠 것(spec-sync)**: D1 칸 이름 · D3/D4 코드 · D10 · D12 · D13 · D16 · D17.
- `online` = 그 세션 알림 스트림 연결이 10초마다 세우는 Redis 표시(25초) — 끊김 뒤 최대 25초 「접속 중」이 남을 수 있음(푸시는 늘 보내므로 닿기에는 영향 없음).
- 문진 답 저장 = 고객이 보낸 본문 전체(이름 · 생년월일 · 휴대폰 · 주소 · 약관 · 답 — `language` 만 뺌)를 `answers` JSONB 에 — [다시 보내기]가 같은 본문을 KOS 에 다시 보내야 해서. 법적 검토 DAY-ESC-001 참조(비차단).
- 공개 경로 속도 제한은 Redis 가 안 되면 **열어 둔다**(고객이 막히지 않게 · 로그만).
- 앱 「국적/통역」 글자 차이(app-2 §5-8) · 오류 코드 글자(§5-10)는 backend 몫 아님.
- 웹 진행 칸 · 고객 문진 화면 모양은 시안 없음(OQ-D37 · 2루프).

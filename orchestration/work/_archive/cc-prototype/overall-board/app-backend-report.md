# WORK-009 backend(WP-BE1 ~ BE5) 결과 보고

## 상태: done (BE1 ~ BE5)

작업 위치: `/Users/kknaks/orca/workspaces/cc-prototype/overall-board` · branch `kknaksss/overall-board-2`(base `95c64bc`) · 범위 `procedure/back/**` 만 · 커밋 없음.

---

## WP-BE1 — 계정 · 기기 · 알림 바탕 (done)

### 수행
- `app/repository/db.py` — `PUSH_LOG` 0.4.0 모양(`call_id` · `visit_id` null 가능 · `kind` · `reservation_id` · `display_request_id` · `notification_id`) · `APP_SCHEMA`(새 표 `notification` · `notification_setting` · `display_request` · `id_photo` — 머리 주석 「법적 검토 필요」) · `MIGRATIONS` 열 더함(`device.name·kind·last_seen_at` · `questionnaire_history.source·language·device_id·display_request_id` · `identity_check.photo_id`) · **`_rebuild_push_log()`** — `PRAGMA table_info` 로 `call_id.notnull=1` 일 때만 한 트랜잭션에서 새 표 → 옛 행 복사(`kind='doctor_call'`) → DROP → RENAME(멱등)
- `app/domain/models.py` — `ROLES`(다섯) · `MANAGER_ROLES`(admin · coordinator · counselor) · `Device`
- `app/schemas/actions.py` — `Role` 에 `counselor` · `DeviceRequest{token, name?(1~40), kind?(phone|tablet)}` · `DeviceResponse{ok, deviceId}` · 알림 · 설정 스키마
- `app/service/actions.py` `accept()` — 분기를 `MANAGER_ROLES` 로(상담사 = doctorId 필수)
- `app/service/accounts.py` — `_doctors` 를 `_linked()` 로 일반화 + **`_counselors`**(상담사 목록 = `service/reservations._counselors` 같은 함수 · 시스템 계정 · `KOS_EXCLUDE_ACCOUNT_IDS` 뺌) · 카드 1명 `CCC_COUNSELOR_ID` · 내부 `counselor-<staffId>` · 빠지면 `active=false` · `_passwords` 에 counselor
- `app/config.py` — `ccc_counselor_id · _password · _kos_account_id` · `proc_photo_dir` · `proc_display_ttl_min`(기본 10)
- `app/service/stream.py` — 허브 연결마다 `(account_id, device_id?)` · `send_to_account` · `send_to_device` · `online()` · 새 이벤트 프레임 `id:` 없음 · version 그대로
- `app/service/devices.py`(새) — 등록(이름 없으면 「iPhone」/「iPad」) · `check()` = 남의 계정 · 없는 id → 404 `device_not_found` + `last_seen_at` 갱신 · `own()` = SSE 용(무시)
- `app/service/notifications.py`(새) — 목록(그 계정 · 오늘 KST · 50 · 새것 위 · `unread`) · 읽음(ids / 전부 / `callId` · `reservationId`) · 설정(역할별 종류 · 받지 않는 종류 400 `setting_not_allowed`) · 새 행 → SSE `notification {unread}`(그 계정만)
- `app/service/push.py` — `Delivery` 일반화(`kind` · `reservation_id` · `notification_id` · `display_request_id`) · 원장 호출 = 받는 계정마다 `notification` 1행(기기 없어도 · 설정 끔이면 행 · push_log 둘 다 없음) · payload `kind:"doctor_call"` · 발송 루틴 `deliver()` 공용
- `app/api/devices.py`(응답 `deviceId`) · `app/api/notifications.py`(새 — 4경로) · `app/api/board.py`(stream `deviceId` 쿼리 → 계정 · 기기 붙임) · `app/container.py` · `app/main.py`
- tests: `tests/test_app_be1.py`(새 25) · `conftest.py`(상담사 비밀번호) · `test_auth_roles.py`(역할 행렬 5) · `test_push.py`(payload `kind` · `deviceId`) · `test_order.py`(경로 수 = 35 + 그 WP 까지 생긴 새 경로)

### 검증
- `uv run ruff check .` → All checks passed
- `uv run pytest -q -k "role or account or push or notification or migrat or stream"` → **69 passed**
- 전체 `uv run pytest -q` → **393 passed**(시작 361)

### 계약 대조(§8.6)
| 항목 | 결과 |
|---|---|
| 역할 다섯 — 행렬 × coordinator · counselor = admin · 수락 doctorId 필수 · 새 API 다섯 역할 ○ · grep | 같음(`role in (` / `role == "admin"` 남은 곳 = `push.py` 원장 호출 받는 사람 1곳뿐 — 계약상 관리자만) |
| 상담사 계정 | 같음 |
| 마이그레이션 — 옛 모양 DB 파일에서 시작 · 값 · 멱등 · call_id 없는 행 INSERT | 같음 |
| 원장 호출 회귀 — `kind:"doctor_call"` · 계정마다 1행 · coordinator · counselor 0 | 같음 |
| 알림 — 오늘 · 50 · 둘만 · 읽음 · 남의 것 · 역할별 설정 · 400 · SSE 그 계정만 | 같음 |
| SSE 허브 — board 전부 · notification 계정 · display 기기 · `id:` 없음 · version · online | 같음 |

### 코디 확인
- **(요청 모양 · 더함)** `POST /api/notifications/read` 본문에 `ids?` 외 **`callId?` · `reservationId?`** 를 받는다 — SPEC §5-4 「푸시를 눌러 열 때 back 이 callId · reservationId + 계정으로 찾음」을 위한 자리(SPEC 에 필드 이름이 없어 이 이름으로). 응답 = `{ok:true, read:N}`(SPEC 에 응답 모양 없음 → `read` 수를 더함). mobile 에 알려 주세요.
- `GET /api/notifications` `items[].target` = `{visitId?, callId?, reservationId?}` — SPEC 의 `{visitId?, reservationId?}` 에 `callId` 를 더 실음(앱 원장 호출 누름 → 읽음에 씀).
- 「전부 읽음」은 오늘 밖(어제) 안 읽은 행도 읽음으로 바꾼다(`unread` 는 오늘만 셈).

---

## WP-BE2 — 상담사 호출 푸시 (done)

### 수행
- `app/service/push.py` — `counselor_message()`(그 상담사 `counselor` 계정 active 만 · 본문 「<방> · 상담 대기」 / 「상담 대기」 · 방 = 예약 사본 `room_title`(「방 배정」 작업 방) · category 없음 · payload `{aps, kind:"counselor_call", reservationId}`) · `schedule_counselor` · `notify_counselor` · `push_log.kind = counselor_call` · `notification` 1행
- `app/service/reception.py` `counselor_call()` — KOS 200 + `event_log(counselor_call)` 커밋 **뒤** `on_counselor_call(reservationId, staffId)` · 컨테이너가 `push.schedule_counselor` 를 끼움
- tests: `tests/test_app_be2.py`(새 6)

### 검증
- `uv run pytest -q -k counselor` → **18 passed**

### 계약 대조(§8.6 「상담사 호출 푸시」)
KOS 200 뒤에만 · 거절 0 · 받는 사람 그 상담사만 · 다시 누름 = 다시 · 다른 상담사 = 새 상담사만 · 본문 둘 · 고객 이름 0 · payload · `push_log.kind` · 설정 끔 = 발송 0 · notification 0 → **전부 같음**.

---

## WP-BE3 — 띄우기 요청 (done)

### 수행
- `app/service/display.py`(새) — `targets()`(코디 계정 기기 · `last_seen_at` 24시간 · 최근 순 · `online` = 허브) · `create()`(같은 예약 · 종류 pending → canceled · `secrets.token_urlsafe(32)` · DB 엔 sha256 만 · `PROC_DISPLAY_TTL_MIN` · `event_log(display_request)`) · `reach()`(그 기기 SSE 열림 → `send_to_device` `display {requestId, deviceId, kind, reservationId}` · 아니면 띄우기 푸시) · `pending()`(deviceId 필수 400 · 기기 확인 404 · 그 기기 pending + 이미 opened · 돌려주며 opened) · `claim()`(1회 409 `display_closed` · 만료 409 `display_expired` · 없음 404 `display_not_found` · deviceId 로 기기 바꿈 · 없으면 그대로) · `close()`(done|canceled · 닫힌 것 409) · `finish()`(문진 · 스캔이 대신 done — BE4 · BE5 가 씀) · `of_reservation()`(상세 `displays[]` — 오늘 그 예약 것)
- 만료 = 읽을 때 pending 중 `expires_at` 지난 것 → expired(**열린 것은 그대로** — 고객이 쓰는 중) · 409 를 던져도 expired 가 남게 따로 커밋
- `app/service/push.py` — `display_message()`(그 기기 하나 · `aps.alert` 만 · `sound` 없음 · payload `{aps, kind:"display", requestId}` · `push_log.kind = display` · `display_request_id` · notification 없음) · `schedule_display` · `notify_display`
- `app/api/display.py`(새 5경로) · `app/schemas/actions.py`(띄우기 스키마) · `app/schemas/reservations.py`(`ReservationDetail.displays[]` · `Identity.device` · `photoId`) · `app/service/reservations.py`(상세에 `displays` · identity `device` · `photoId`) · `app/repository/repo.py`(display 함수 · identity_check `method` · `device` · `photo_id`) · `app/domain/models.py`(`DisplayRequest`) · `app/container.py` · `app/main.py`
- tests: `tests/test_app_be3.py`(새 12)

### 검증
- `uv run pytest -q -k display` → **13 passed** · 전체 **405 passed**

### 계약 대조(§8.6 「띄우기」)
만들기 · 앞 pending canceled · 10분 뒤 expired · SSE `display` · 앞에 없으면 푸시 1(`display` · 목록 0 · `sound` 없음 · `alert` 있음) · pending 그 기기 것만 · claim 1회 · 만료 · 남의 계정 404 · 해시만 · targets 코디 24시간 · 같은 코디 계정 태블릿 · 폰 가르기 · deviceId 없는 pending 400 · claim deviceId 로 기기 바뀜 → **같음**.

### 코디 확인
- pending · claim 응답 모양 = 코디 결정(2026-10-27) 그대로: 항목 `{requestId, kind, reservationId, customerId, deviceId, status, expiresAt}` · pending `{items}` · claim 항목 하나.
- 만들기 `deviceId` 는 기기 행이 있기만 보면 된다(코디 계정 기기인지는 안 막음 — SPEC 에 없음). 없는 id = 404 `device_not_found`.
- `close` 는 누가 불러도 됨(웹 [닫기] · 기기 둘 다) — 역할 다섯 ○.

---

## WP-BE4 — 문진 · unlock (done)

### 수행
- `app/domain/languages.py`(새) — 출처 주석(`app-kos-report.md` §3.2 ~ §3.4) · `FORM_LANGS`(6 · 칩 순서) · `normalize`(zh-CN → zh-Hans · zh-yue → zh-Hant · 17 enum 밖 = 없음) · `NATIONALITY`(KOS 웹앱 표 그대로) · `resolve()` → `(code, source)` · `AGREEMENT_KEY`(ja · en · zh)
- `app/service/questionnaire.py`(새) — `load()`: 기기 확인 → 내부 `get-visitor` · 공개 `get-visitor-questionnaire` · `get-questionnaire-agreements` · `get-questionnaire-submit` 동시 · 응답 §6.15 ① 모양 · `submit()`: 주민번호 · 발음 = 400 `questionnaire_field`(KOS 전) · 받은 본문 + `visitorId`(언어 · 기기 · 요청 id 는 KOS 로 안 보냄) → 공개 `submit-visitor-questionnaire` · KOS 400 = 409 `questionnaire_rejected` · 그 밖 502 · 둘 다 `event_log(kos_rejected)` · 성공 → 제출본 다시 읽어 `questionnaire_history`(같은 제출본 read 행이면 그 행을 `app_submit` 으로 고침) · 띄우기 요청 done · `event_log(questionnaire_submit)` · 그날 캐시 비움
- `app/repository/repo.py` `put_app_questionnaire()` — 읽기 쪽 `add_questionnaire`(INSERT OR IGNORE)는 그대로
- `app/service/auth.py` `unlock()` — `(계정, deviceId|None)` 마다 실패 수 · 5회 → 그 기기만 1분 429 「여러 번 틀렸어요. 1분 뒤 다시 시도해 주세요」 · 로그인 실패 수와 따로 · bcrypt 상수 시간 · 가짜 해시
- `app/api/auth.py` `POST /api/auth/unlock`(기기 확인 404 먼저) · `app/api/questionnaire.py`(새 2경로 · POST 는 `require_real_board`) · `app/schemas/actions.py`(문진 · unlock 스키마) · 컨테이너 · main
- tests: `tests/test_app_be4.py`(새 24) · `tests/fake_kos.py`(공개 약관 · 제출 — 휴대폰 앞 0 빼기 흉내)

### 검증
- `uv run pytest -q -k "questionnaire or unlock"` → **24 passed** · 전체 **429 passed**

### 데모 실호출(2026-10-27 · 완료 조건 「문진 제출 1」)
- 스크립트 = 스크래치(레포 밖) · DB = 스크래치 파일(사용자 DB · 포트 안 건드림) · **데모 테넌트 assert**: `.env` 공개 키 = ax-clinic-project dev 키 · ≠ 운영 키 · sign-in `tenantIds` 에 `.env` 테넌트 — 값 출력 없음
- 대상 = `[ccc 시험]` 고객 1명(이름 접두 assert) · ccc 서비스 함수 그대로(`QuestionnaireService.load` → `submit`)
- 결과: 불러오기 = 4쪽 · 15질문 · 약관 1 · 언어 `ko`(source `nationality`) · **제출 KOS 200** · 답 15줄(질문마다 첫 선택지 · 이메일 칸 `ccc-test@example.com` · 기타 칸 `[ccc 시험]`) · 이력 1행 `app_submit` · 다시 불러오기 `todaySubmitted = true`
- **데모 흔적**: 그 시험 고객 KOS 문진 제출본 1건 덮어씀 · 개인정보 동의 true · (미리 채운 값 그대로 보냄 — 비어 있던 주소 · 휴대폰 칸이 있었다면 `[ccc 시험]` 문구 · 시험 번호로 채워짐). 되돌리지 않음

### 계약 대조(§8.6 「문진」)
언어 표(zh-CN · zh-yue · TW · VN · th) · source · 제출 본문 = 받은 값 + visitorId · 400 · KOS 400 → 409 · 이력 1행(app_submit · language · 기기) · 띄우기 done · read 행 고침(행 1) · 읽기가 뒤에 와도 app_submit · 휴대폰 = 앞 0 빠진 값 · unlock(200 · 기기별 5회 429 · 1분 뒤 · 다른 기기 · 로그인 그대로 · 기기 없음 칸) → **같음**.

### 코디 확인
- `prefill.dateOfBirth` 는 **`yyyyMMdd`**(제출 꼴과 같게 · KOS 고객 값에서 바꿈) — mobile 에 알려 주세요. `prefill.phone` 키 = `{countryCode, phoneNumber}`(제출 본문과 같음).
- `?lang=` 은 6개 중 하나면 `language.code` 를 그 값으로(source 는 원래 정한 근거 그대로) · 모르는 값은 무시.
- `form` = `{pages:[…]}`(KOS 양식 페이지 그대로 · translsMap 포함) · `agreements` = KOS 약관 그대로.
- 답 · 약관 항목의 그 밖 키(`inputType` · `translsMap` 등)는 받아 그대로 KOS 로 넘긴다.

---

## WP-BE5 — 여권 스캔 · 사진 (done)

### 수행
- `app/service/passport_scan.py`(새) — 기기 확인 → 5MB(413 `photo_too_large`) → ④-a **`ReservationService.personal()` 그대로**(저장 직전 내부 `get-visitor` 다시 읽기 · `PERSONAL_KEYS` 중 응답에 있는 키 전부 + 바뀐 칸 · `passportExpiryDate` `yyyy-MM-dd` 보냄 · `skipped` 늘 빈 목록) · 실패(409 · 502)면 사진 · 신분 확인 0 → ④-b → ④-c → ④-d `identity_check`(confirmed · `app_scan` / `app_manual` · `device` = 기기 이름 · `photo_id`) + `event_log(passport_scan)`(칸 이름 · photoId · kos 결과 · 값 없음) + 띄우기 done · `fields` 는 7칸만(`name` 등 그 밖 = 400)
- `app/service/id_photo.py`(새) — **법적 검토 주석 ①②③ + 종류 고정 자리** · `save()` = `PROC_PHOTO_DIR/<32자 16진>.jpg` 바로 쓰기 + `id_photo` 1행 · 폴더 비면 `disabled` · `upload()` = 내부 `get-codes{IMAGE_EQUIPMENT}` 에서 이름 「태블릿」 객체 → 공개 `generate-uploading-url{fileName}` → presigned PUT(`image/jpeg` · 인증 없음) → 공개 `register-visitor-images{images:[{fileName, visitorId, source:"HOSPITAL", shootingDateTimeUtc, equipment, memo:"ccc 여권 스캔"}]}`(`category` · `scheduleId` · `path` 없음) · 「태블릿」 없음 = 올리기 0 · `failed` · `equipment_code_missing` · `read()` 열람(+ `event_log(id_photo_view)`) · `retry()`(kos-retry · 이미 ok 면 그대로)
- `app/kos/client.py` `put_presigned()` · `app/api/photos.py`(새 3경로 · multipart 는 Content-Length 로 5MB 먼저 거르고 spool 한도를 올려 **임시 파일 없이 메모리에서만** · 열람 = Bearer 헤더만 · `Cache-Control: no-store`) · `app/schemas/actions.py` · 컨테이너(`PROC_PHOTO_DIR` 비면 시작 경고 1줄) · main
- `pyproject.toml` · `uv.lock` — `python-multipart`(multipart 받기)
- **`Dockerfile` 17행 — `mkdir -p /data /photos && chown app:app /data /photos`**(코디 지시 · `app-infra-report.md` §5) + 머리 주석 한 줄
- tests: `tests/test_app_be5.py`(새 15) · `tests/fake_kos.py`(장비 코드 · URL 발급 · S3 PUT · 등록) · `tests/test_order.py` **`test_route_count_50`**(앞 35 + 새 HTTP 15 — 목록으로 단언)

### 검증
- `uv run pytest -q -k "scan or photo or route_count"` → **15 passed**
- `grep -rn "법적 검토 필요" procedure/back/app` → **9곳**(≥ 3 · ① 저장 ② KOS 올리기 ③ 열람 · 보관 + 종류 고정 · `id_photo` 표 머리 · 저장소 · API · 스캔 서비스)
- 레포 `app/` 에 24자 16진(KOS id) **0**(시험이 grep)
- **전체 `uv run ruff check . && uv run pytest -q` → All checks passed · 443 passed**(시작 361)

### 데모 실호출(2026-10-27 · 완료 조건 「여권 수정 + 이미지 올리기 1」)
- 같은 스크래치 스크립트 · 데모 테넌트 assert 통과 · 대상 `[ccc 시험]` 고객 1명(BE4 와 다른 사람 · 접두 assert)
- `PassportScanService.save()` 그대로 — 칸 = `passportNumber`(지어낸 9자) · `passportExpiryDate`(지어낸 날짜) · 사진 = **지어낸 TEST 그림 JPEG**(1250 × 880 · 파란 바탕 흰 「TEST」 · 27KB · 실제 신분증 아님) · `manual = true`
- 결과: `personal:"ok"` · `skipped:[]` · `photo:{ccc:"ok", kos:"ok"}` · `id_photo.kos_status = ok` · 다시 읽은 KOS 고객 = 여권번호 · 만료일 보낸 값과 같음 · 이름 그대로 · 내부 `get-visitor-images` 에 올린 파일 이름 보임(1건)
- 호출: 내부 get-visitor 2 · update-visitor-personal-information 1(쓰기) · get-codes 1 · 공개 generate-uploading-url 1 · presigned PUT 1(쓰기) · register-visitor-images 1(쓰기) · get-visitor-images 1 · 운영 키 0
- **데모 흔적**(되돌리지 않음): 그 시험 고객 여권번호 · 만료일 = 지어낸 값 · KOS 고객 이미지 1장(TEST 그림 · 메모 「ccc 여권 스캔」 · 장비 「태블릿」). ccc 쪽 사진 파일은 스크래치 폴더에만(레포 · 사용자 볼륨 아님)

### 계약 대조(§8.6 「스캔」 · 「경로 수」)
다시 읽기 · 있는 키 전부(고정 수 단언 없음) · `name` 안 바뀜 · 만료일 보냄 · `skipped` 빔 · KOS 이미지 본문 키 · 「태블릿」 없음 = 업로드 0 · `failed` · `equipment_code_missing` · 코드 id 0 · 고객 수정 실패 = 사진 0 · identity 0 · 파일 1 + 행 1 · 이름에 고객 값 0 · KOS 사진 실패 = 앞은 남고 `failed` · kos-retry · `PROC_PHOTO_DIR` 빔 = `disabled` · 413 · `app_scan` / `app_manual` · Bearer(헤더 없음 · `?token=` = 401) · `id_photo_view` · 로그에 값 0 · 경로 50 → **같음**.

### 코디 확인
- `PROC_PHOTO_DIR` 이 비면 응답 `photo = {ccc:"disabled", kos:"skipped"}` · `photoId: null` — SPEC 응답 enum(`kos: ok|failed`)에 **`skipped` 를 더함**(ccc 파일이 없으면 kos-retry 를 못 하므로 KOS 로도 안 올림). mobile 에 알려 주세요.
- 열람 · kos-retry 오류: 없는 사진 = 404 `photo_not_found` · 폴더 꺼짐 = 409 `photo_disabled`.
- multipart 칸: `fields`(JSON 문자열) · `photo`(파일) · `reservationId` · `displayRequestId` · `deviceId` · `manual`(`true`/`1`) — 숫자 칸은 문자열로 와도 받음.

---

## 전체 요약
- 경로 **50 = HTTP 49 + WS 1**(`test_route_count_50`) · 전체 **443 passed** · ruff 0
- 바뀐 파일(전부 `procedure/back/**`): `Dockerfile` · `pyproject.toml` · `uv.lock` · `app/{config,container,main}.py` · `app/api/{auth,board,devices}.py` + 새 `app/api/{display,notifications,photos,questionnaire}.py` · `app/domain/models.py` + 새 `app/domain/languages.py` · `app/kos/client.py` · `app/repository/{db,repo}.py` · `app/schemas/{actions,reservations}.py` · `app/service/{accounts,actions,auth,push,reception,reservations,stream}.py` + 새 `app/service/{devices,display,id_photo,notifications,passport_scan,questionnaire}.py` · `tests/{conftest,fake_kos,test_auth_roles,test_order,test_push}.py` + 새 `tests/test_app_be{1..5}.py`
- compose · `.env.example` 은 건드리지 않음(WP-INFRA 몫). `.env.example` 에 `CCC_COUNSELOR_*` · `PROC_PHOTO_DIR` 이름이 있는지는 infra 쪽 확인
- 미결(코디): ① 알림 읽음 본문 `callId` · `reservationId` · 응답 `read` 수 ② `target.callId` 더함 ③ pending · claim 모양(코디 결정 반영됨) ④ `prefill.dateOfBirth = yyyyMMdd` ⑤ 스캔 `photo.kos = skipped` — ①②④⑤ 는 SPEC 반영 · mobile 전달 필요

---

## 추가 1 — 예약 상세 `customer.identity.photoKos` (done)

### 수행
- `app/schemas/reservations.py` `Identity` — `photoKos: "ok" | "failed" | "skipped" | null`(기본 null)
- `app/service/reservations.py` `detail()` — 마지막 신분 확인의 `photo_id` 가 있으면 그 `id_photo.kos_status` · 없으면(확인 기록 없음 · 웹 수동 확인 · 사진 저장 꺼짐) null
- tests: `tests/test_app_be5.py` `test_scan_detail_photo_kos`(기록 없음 null · 웹 수동 null · KOS 실패 `failed` · kos-retry 뒤 `ok` · `skipped`)

### 검증
- `uv run ruff check .` → All checks passed · `uv run pytest -q -k "scan or photo"` → 15 passed · 전체 **444 passed**

---

## 리뷰 r1 수정 (backend 몫 FAIL-1 · FAIL-2 · W2) — done

### 수행
- **FAIL-1** `app/api/display.py` `create` → `async def`(sync 면 스레드풀에서 돌아 이벤트 루프가 없어 띄우기 푸시가 「건너뜀」 로그만 남았다). 시험 `test_display_api_create_push_log_row`(API 만들기 · 기기 SSE 없음 → push_log `display` 1행 · `sent` · 그 기기 토큰) — **옛 `def` 로 되돌리면 실패 · `async def` 면 통과 확인**
- **FAIL-2**(코디 기본값) `app/service/passport_scan.py` · `app/api/photos.py` · `app/schemas/actions.py` — `manual = true` 면 사진 없이 저장: 고객 수정 → `identity_check`(confirmed · `app_manual` · `photo_id` null) · 이벤트(`photoId` null · `kos.photo` null) · 띄우기 done · ccc · KOS 사진 0 · 응답 `photo: null` · `photoId: null`(그 밖 모양 SPEC 그대로). 카메라 길(`manual` 아님)은 사진 필수(없으면 400 `invalid_request`). 시험 `test_scan_manual_without_photo` · `test_scan_api_manual_without_photo`
- **W2** `procedure/.env.example` — 코디 줄 아래 `CCC_COUNSELOR_ID=` · `CCC_COUNSELOR_PASSWORD=` · `CCC_COUNSELOR_KOS_ACCOUNT_ID=`(이름만 · 주석 1줄)

### 검증
- `uv run ruff check .` → All checks passed · `uv run pytest -q -k "display or scan or photo"` → 32 passed · 전체 **447 passed**

### 바뀐 파일
`procedure/.env.example` · `procedure/back/app/api/{display,photos}.py` · `app/service/passport_scan.py` · `app/schemas/actions.py` · `tests/test_app_be3.py` · `tests/test_app_be5.py`

---

## E2E batch 1 (2026-10-28 · branch `kknaksss/overall-board-3` · base `f8a3751`) — backend #1 · #3 · #4 done

### #1 installId — 기기 행 하나
- `device.install_id` 열(`MIGRATIONS` · 옛 DB 에 ADD COLUMN · 옛 행 null) · `Device.install_id`
- `POST /api/devices {token, name?, kind?, installId?}`(1 ~ 100자 · 빈 문자열 400 — 없으면 키를 뺀다) — `repo.put_device()`:
  ① 같은 `install_id` 행이 있으면 **그 행에 새 토큰 · 계정 · 시각**(이름 · 종류는 보낸 것만 고침 → 사용자가 정한 이름 유지) · 새 토큰이 다른 행에 있으면 그 행은 지움 → **`deviceId` 그대로** ② 없으면 토큰 행(옛 규칙 + install_id 기록) ③ 둘 다 없으면 새 행
- `targets` — 계정 · installId 당 하나(가장 최근). installId 없는 옛 행은 행마다(옛 빌드 호환)
- **운영 옛 행 8 · 9**: 새 빌드가 지금 토큰(행 9)으로 등록하면 행 9 에 installId 가 붙는다. 행 8 은 아무도 그 id 로 부르지 않으니 `last_seen_at` 이 멈춰 **24시간 뒤 targets 에서 빠진다**(지우진 않음). 바로 없애려면 운영 DB 에서 행 8 삭제(코디 · 사용자 판단)

### #3 SSE display — back 은 그 기기 스트림으로 보낸다(고칠 곳 없음 · 시험 더함)
- 시험 `test_sse_display_reaches_device_stream_via_route` — **실제 route 함수 `GET /api/board/stream?token=&deviceId=`** 로 연 스트림에 `c.display.create(…, deviceId)` → `event: display` `{requestId, deviceId, kind, reservationId}` 1프레임(`id:` 없음) · 푸시 0 · 웹 연결(deviceId 없음) 0 · 연결 없는 다른 기기 = 푸시 1 · targets `online` 이 스트림 따라 바뀜 · 남의 계정 deviceId = 무시(`test_sse_foreign_device_id_ignored`)
- 운영 #10 해석: `reach()` 는 `hub.online(9)` 가 참일 때만 푸시를 건너뛴다 → **기기 9 스트림이 deviceId 9 로 붙어 있었고 back 은 그 스트림에 display 를 실었다**. 폰이 안 연 것은 앱 쪽(받은 `display` 처리 · 화면 열기)으로 본다 — mobile #3 몫. (프록시가 `id:` 없는 프레임을 버리는 일은 없음 — 같은 스트림의 `board` 가 닿고 있었다)

### #4 휴대폰 표시 — **back 응답에 `display` 를 더함**(규칙 한 곳 `app/domain/phone.py` `phone_display()`)
- 예약 상세 `customer.personal.phone` · `additionalPhone` = `{countryCode, number, display}` — `number` 는 KOS 값 그대로 · **보낼 때도 그대로**
- 규칙(front · app 이 직접 그릴 일이 생기면 같은 것): 숫자만 → 비면 null / 국가번호(앞 `+` 무시) `82` 면 맨 앞이 0 이 아니면 0 붙임 → 11자리 `3-4-4`(`010-5511-3764`) · 10자리 `02` 로 시작 `2-4-4` · 그 밖 10자리 `3-3-4` · 9자리 `02` `2-3-4` · 그 밖 길이 = 숫자 그대로 / 그 밖 국가번호 · 없음 = 숫자 그대로(국가번호는 화면이 따로)
- **front · app 은 `phone.display` 를 쓰면 된다**(없으면 `number`). 문진 `prefill.phone` 은 입력 칸 값이라 그대로 둠(KOS 값)

### 검증
- `uv run ruff check .` → All checks passed · `tests/test_app_e2e1.py`(새 19) · 전체 **466 passed**

### 바뀐 파일
`procedure/back/app/{api/devices.py, domain/models.py, domain/phone.py(새), repository/db.py, repository/repo.py, schemas/actions.py, schemas/reservations.py, service/devices.py, service/display.py, service/reservations.py}` · `tests/test_app_e2e1.py`(새)

- **(2026-10-28 · 결정 바뀜) #4 되돌림** — 휴대폰 = KOS 그대로(사용자). `app/domain/phone.py` 삭제 · `personal.phone` · `additionalPhone` 의 `display` 제거(응답 모양 batch 1 전과 같음 · 두 파일 diff 0) · `#4` 시험 12개 제거. #1 · #3 그대로 · ruff 0 · 전체 **454 passed**

---

## E2E batch 2 (2026-10-28 · branch `kknaksss/overall-board-4` · base `333f30f`) — done

### #1 아이폰 2대 — 옛 기기 행 가리기
- `app/repository/repo.py` `live_devices()`(새 · 한 곳): 어떤 계정에 installId 있는 행이 있으면 그 계정의 **installId 없는 옛 행 중 같은 kind**(옛 행 kind 가 비었으면 어느 kind 든)는 뺀다 — **지우지 않음**
  - `targets`(`service/display.py`) · 푸시 대상(`repo.devices_of` — 원장 · 상담사 호출)이 이 목록을 쓴다
- 등록: `installId` 와 함께 온 토큰이 옛 행(installId 없음) 토큰과 같으면 **그 행에 installId 를 붙인다**(새 행 없음 — batch 1 `put_device` 의 토큰 행 분기 그대로 · 이번에 시험으로 고정)
- 운영 행 8 · 9: 새 빌드가 지금 토큰(행 9)으로 `installId` 를 보내면 행 9 에 붙고 · 행 8(같은 kind 또는 kind 없음)은 targets · 푸시에서 바로 빠진다(24시간 기다림 없음)

### 띄우기 = SSE + 푸시 둘 다
- `DisplayService.reach()` — 그 기기 스트림이 열려 있으면 `event: display` 를 보내고 **늘** 띄우기 푸시도 보낸다(허브가 죽은 연결을 ping 전까지 online 으로 봐 잠긴 · 뒤 폰을 놓치던 위험) · 반환 `"sse+push"` / `"push"` · 앱은 requestId 로 한 번만 연다(batch 1 W1)
- 앞 판 시험 2곳(「SSE 면 푸시 0」)을 새 규칙으로 고침(`test_app_be3.py` · `test_app_e2e1.py`)

### #3 짝 — back 변경 없음
- 등록 `name` 은 보낸 값으로 고치고 · 안 보내면 그대로(처음 행만 「iPhone」/「iPad」) — 앱이 기종 이름을 `name` 으로 보내면 그대로 쓴다
- **주의(mobile)**: 등록 때마다 기종 이름을 `name` 으로 보내면 설정에서 바꾼 이름을 덮는다(back 은 설정 저장과 자동 등록을 가르지 못한다 — 둘 다 `POST /api/devices`). 「이미 이름 넣은 기기는 그대로」 를 지키려면 앱이 **처음 등록(받아 둔 deviceId 없음) · 설정 저장 때만 `name` 을 싣는다**

### 검증
- `uv run ruff check .` → All checks passed · `tests/test_app_e2e2.py`(새 5) · 전체 **459 passed**

### 바뀐 파일
`procedure/back/app/repository/repo.py` · `app/service/display.py` · `tests/test_app_be3.py` · `tests/test_app_e2e1.py` · `tests/test_app_e2e2.py`(새)

---

## E2E batch 2 #5 — 여권 사진이 KOS 일정 「사진 · 펜차트」에 안 보임 (2026-10-28 · branch `kknaksss/overall-board-5` · base `affac41`) — done

### 원인 (HAR · 데모로 확인)
- KOS 일정 상세 사진 탭이 부르는 것 = 내부 **`image/visitor-image/v1/queries/get-visitor-images {visitorId, scheduleId, deleted:false}`**(HAR `처방전상세` · `수납필요 추가` · `app.kos-solution.com2` — 사진 조회는 모두 이 꼴 · `scheduleId` 없는 조회는 HAR 에 없음)
- KOS 자체 여권 스캔(HAR `여권스캔`)도 등록 본문에 **`scheduleId` 를 싣는다**(`{fileName, visitorId, source, scheduleId, shootingDateTimeUtc}`) → 같은 꼴로 바로 다시 읽음
- ccc 는 Q-156 기본값으로 `scheduleId` 를 안 보냈다 → KOS 는 200 · 저장(`scheduleId:""`)했지만 일정 탭 조회에는 안 걸린다. 운영 `id_photo` #1 `kos_status=ok` 와 맞다

### 데모 실호출 (데모 테넌트 assert · 운영 키 0 · `[ccc 시험]` · TEST 그림)
- 대상 = BE5 때 사진을 올린 같은 시험 고객 · 그 고객의 KOS 일정 1건
- 전: 일정 없이 조회 = 1건(BE5 사진 · `scheduleId` 빈 값) · **일정 탭 조회 = 0건**
- ccc `PhotoService.save` → `upload`(이번 수정 코드 · `scheduleId` 실음) 1회 → `ok`
- 뒤: **일정 탭 조회 = 1건 · 이번 사진 보임 · 그 항목 `scheduleId` = 그 일정** · 일정 없이 조회 = 2건(옛 것 + 이번 것)
- `scheduleId` 없는 이미지가 KOS 웹 어디에 보이는지: HAR 의 사진 조회는 모두 `scheduleId` 를 실어 **화면을 찾지 못함**(고객 상세에 이미지 탭이 있는지는 사용자 눈 확인 자리). API 로는 일정 없이 조회하면 보인다
- 호출: 내부 get-codes 1 · 공개 getSchedulesByVisitor ≤ 2 · 공개 generate-uploading-url 1 · presigned PUT 1(쓰기) · 공개 register-visitor-images 1(쓰기) · 내부 get-visitor-images 4
- **남긴 흔적**: 그 시험 고객 KOS 이미지 1장 더(TEST 그림 · 메모 「ccc 여권 스캔」 · 장비 「태블릿」 · 그 일정에 묶임). 되돌리지 않음

### 수정
- `app/service/id_photo.py` `upload()` — 사진 행의 `reservation_id` → 그 예약 `kos_id` 를 **`scheduleId`** 로 싣는다(예약이 없으면 뺌). kos-retry 도 같은 함수라 같이 실린다. `category` · `path` 는 그대로 안 보냄(데모 지점 분류 = 「시술 전 / 시술 후」 뿐 — 「여권」 같은 맞는 코드 없음)
- tests: `test_app_be5.py` — 이미지 본문 키에 `scheduleId`(= 그 예약 일정) · `test_scan_photo_kos_schedule_id`(예약 없음 = 키 없음 · kos-retry 도 실음)

### 검증
- `uv run ruff check .` → All checks passed · 전체 **460 passed**

### 코디 확인
- 운영 `id_photo` #1(이미 `ok` · `scheduleId` 없음)은 이 수정으로 바뀌지 않는다 — 일정 탭에 띄우려면 그 고객을 **다시 스캔**(새 사진 · 일정 실림)하거나, KOS 내부 `update-visitor-image`(HAR 에 있음 · 허가 밖이라 안 함)로 일정을 붙여야 한다
- 운영 지점에 「여권」 같은 이미지 분류 코드가 있으면(HAR `처방전상세` 에는 다른 지점 응답에 「여권」 분류가 보임) 분류도 실을 수 있다 — 지금은 안 보냄(지시대로)

### 바뀐 파일
`procedure/back/app/service/id_photo.py` · `tests/test_app_be5.py`

---

## 여권 사진 분류 (2026-10-28 · branch `kknaksss/overall-board-6` · base `fad8b56`) — done · **이 절만 따로 커밋 · 배포 가능**

### 바뀐 파일 (이 수정만)
`procedure/back/app/service/id_photo.py` · `procedure/back/tests/fake_kos.py` · `procedure/back/tests/test_app_be5.py`

### HAR 해부 (`reference/2026-10-23-cc-overall-board/har/여권스캔.har` · 데모 테넌트 · 모양만)
| 순서 | KOS 웹 | ccc(지금) |
|---|---|---|
| 코드 | 내부 `get-codes {category:"IMAGE_CATEGORY"}` · `{category:"IMAGE_EQUIPMENT"}` 둘 | 둘 다(이번에 IMAGE_CATEGORY 더함) |
| URL 발급 | **내부** `image/v1/commands/generate-presigned-url {fileName}` → `{data:{url}}` | **공개** `image/open/v1/commands/generate-uploading-url {fileName}` → `{data:"url"}` |
| 올리기 | S3 `PUT`(`Content-Type: image/jpeg` · 인증 없음) | 같음 |
| 등록 | **내부** `image/visitor-image/v1/commands/register-visitor-images {registerVisitorImageConfigurations:[…]}` | **공개** `image/open/v1/commands/register-visitor-images {images:[…]}` |
| 등록 항목 키 | `fileName · visitorId · source:"HOSPITAL" · scheduleId · shootingDateTimeUtc` **(5개 — equipment · category · memo 없음)** | `fileName · visitorId · source:"HOSPITAL" · scheduleId(그 예약 · batch 2 #5) · shootingDateTimeUtc · equipment(「태블릿」) · memo` + **category(「여권」 있으면)** |
| 파일 이름 | `<고객 이름>_<yyyyMMdd>_<uuid>.jpeg` | 무작위 32자 16진 `.jpg`(고객 정보 없음 — §6.16 그대로) |
| 다시 읽기 | 내부 `get-visitor-images {visitorId, scheduleId, deleted:false}` → 썸네일 `generate-signed-urls-with-param {fileNames, query:{w,h}}` | (확인용 · 아래 데모) |

- **경로 판단 = 공개 경로 그대로**: 데모에서 공개 경로로 올린 사진이 KOS 웹과 같은 일정 탭 조회에 나오고, **KOS 웹이 쓰는 썸네일 길(`generate-signed-urls-with-param` → GET)로 200 · `image/webp` 로 그려진다** → 같은 이미지 저장소 · 같은 행. 내부 경로로 바꿀 근거 없음(공개 API = 문서화된 계약). ccc 가 더 싣는 `equipment` · `memo` 는 KOS 가 받아 저장(K3 · 이번 응답에 그대로)
- 사용자 「여전히 안 보임」: 운영 `id_photo` 는 `scheduleId` 수정(fad8b56) **배포 전 1장뿐**이라 일정 탭에 안 걸린다 — 배포 뒤 **다시 스캔**해야 보인다(코디 확인과 같음)

### 분류 「여권」
- `id_photo.py` — `CATEGORY_NAME = "여권"`(이름 판정 이 한 곳) · 업로드 때마다 내부 `get-codes {IMAGE_CATEGORY}` 에서 그 이름 코드 객체를 그대로 `category` 로 · **없으면 `category` 키를 안 보냄**(데모 지점 = 「시술 전 · 시술 후」 뿐 — 이번 데모 조회로 다시 확인)
- 시험 `test_scan_photo_kos_category_passport` — 데모 꼴(없음) = 키 없음 · 운영 꼴(「여권」 있음) = 그 객체 그대로 + `scheduleId` · `equipment` 함께

### 데모 실호출 1회 (데모 테넌트 assert · 운영 키 0 · `[ccc 시험]` · TEST 그림)
- 지점 코드: IMAGE_CATEGORY = 「시술 전 · 시술 후」(「여권」 없음) · IMAGE_EQUIPMENT = DSLR · APE · ETC · 태블릿 · 피부진단기
- 같은 시험 고객 · 그 일정 → `PhotoService.save` + `upload`(이번 코드) = **ok** · 일정 탭 조회 2건(앞 판 1 + 이번 1) · 이번 사진 보임 · `category` 키 없음(분류 없음 · 맞음) · 썸네일 GET 200
- 호출: 내부 get-codes 4 · 공개 getSchedulesByVisitor 1 · 공개 generate-uploading-url 1 · S3 PUT 1(쓰기) · 공개 register-visitor-images 1(쓰기) · 내부 get-visitor-images 1 · generate-signed-urls-with-param 1 · 썸네일 GET 1
- **남긴 흔적**: 그 시험 고객 KOS 이미지 1장 더(TEST 그림 · 그 일정에 묶임). 되돌리지 않음

### 검증
- `uv run ruff check .` → All checks passed · 전체 **461 passed**

---

## WORK-010 WP-BE — 고객 문진 웹 back (2026-10-28 · branch `kknaksss/overall-board-6` · 「여권 사진 분류」 커밋 `7e39bd3` 위) — done

### 수행 (SPEC-006 0.1.0 · DEC-008 · `_RESUME` 10-28 OQ = 추천대로)
- **토큰(§3.1)**: `display_request.qr_nonce` 열(MIGRATIONS · 스캔 · 옛 행 null) · 문진 종류 = `base64url(HMAC-SHA256(PROC_SESSION_SECRET, "q|{id}|{nonce}"))` 43자 · DB 엔 nonce · `sha256(token)` 만 · `service/display.py` `qweb_token` · `token_of` · `qr_url`
- **직원 쪽 링크(§6.6)**: `POST /api/display-requests` 응답 `qrUrl`(문진) · `qrToken` = 스캔만(문진 null) · SSE `display` 에 `qrUrl`(그 기기 스트림) · `pending` 항목 `qrUrl`(문진 · pending 만) · **문진 pending 은 돌려줘도 `opened` 로 안 바꿈**(스캔은 그대로) · 상세 `displays[]` 에 `qrUrl`(pending 만) · `openedAt` · claim 에 문진 토큰 = 404 `display_not_found` · 띄우기 푸시 payload 그대로(링크 안 실음)
- **상태(§3.2 · §3.3)**: 새 문진 요청이 같은 예약의 `pending` · `opened` 둘 다 `canceled` · 쓰는 시한 = `opened_at` + `PROC_QWEB_FILL_MIN`(기본 60) 지나면 `expired`(`repo.expire_displays(now, fill_min)` · 문진 opened 만)
- **공개 API(§6.1)** `app/api/public_questionnaire.py`(새 · **법적 검토 주석 ①**): `GET` · `POST /api/public/questionnaire` · 헤더 `X-Questionnaire-Token` · `Authorization` 안 봄 · 가짜 판 `POST` 403 · 응답 = 허용 키 모델(`extra` 금지 — `customerName · language · form{pages} · agreements · prefill · fillUntil`) · `Cache-Control: no-store` · `Referrer-Policy: no-referrer`(main 미들웨어 · 오류 응답 포함)
- **서비스(§6.2 · §9)** `service/questionnaire.py` 다시 씀: `public_target(token)`(해시로 찾기 → HMAC 다시 계산 `compare_digest` → 만료 먼저 커밋 → 404 `q_not_found` · 410 `q_expired` / `q_canceled` · 409 `q_submitted`) · `load_for` · `submit_for` · **원천 세 함수 `read_form` · `read_prefill` · `submit_answers`**(지금 KOS · 나중 갈래 자리) · 첫 GET = `opened` · 겹친 제출 = 요청 id 별 `asyncio.Lock` → 409 `q_submitting` · 이력 `web_submit`(`put_app_questionnaire(source=…)` — 같은 제출본 read 행 고침) · 요청 `done` · `event_log` `qweb_open` · `qweb_denied`(IP · 이유 1분 1행) · `questionnaire_submit {…, historyId, channel:"web"}` · `kos_rejected` — actor 모두 `customer`
- **속도 제한(§7.3)** 메모리 1분 창: IP GET 30 · IP POST 5 · IP 404/410 10(넘으면 그 IP 모든 공개 요청 429) · 토큰 POST 3 → 429 `too_many_requests` · 직원 API 안 걸림
- **IP 헤더(한 곳 · `public_questionnaire.client_ip`)**: 운영 = Cloudflare 엣지 → Tunnel(cloudflared) → ingress-nginx → 파드(infra `CLAUDE.md` ⑨ — **설정 문서로 확인 · 운영 클러스터 직접 조회 안 함**) → ingress 의 `X-Forwarded-For` 는 cloudflared 파드 주소라 **`CF-Connecting-IP` 먼저** · 없으면 `X-Forwarded-For` 첫 값 · 소켓 주소. LAN(MetalLB)에서 ingress 로 바로 오면 헤더를 꾸밀 수 있음(병원 안 · PoC 수용)
- **없앰(§6.2 · OQ-802)**: `api/questionnaire.py`(직원 문진 `GET` · `POST /api/questionnaires/{id}`) · `POST /api/auth/unlock` · `AuthService.unlock` · `UnlockRequest` · 옛 문진 스키마
- **법적 검토 주석 ③** `repository/db.py` `questionnaire_history` 정의 위(`web_submit` · 보관 기간 미정) + `read_prefill` 한 줄(OQ-807)
- `config.py` `proc_qweb_fill_min` · `domain/errors.py` `Gone`(410) · `TooManyRequests`(429) · CORS `allow_headers=["*"]` 가 `X-Questionnaire-Token` 을 이미 덮음(주석만) · `procedure/.env.example` `PROC_QWEB_FILL_MIN=` 한 줄
- **경로 49**(`test_route_count_49` — 없앤 3 = 404 · 공개 2 더함)

### 검증
- `uv run ruff check .` → All checks passed · `uv run pytest -q -k "questionnaire or display or route_count or rate"` → **49 passed** · 전체 **467 passed**
- `grep -rn "법적 검토 필요" procedure/back` 이 판 몫 = **3곳**(① API 머리 · ③ db · 미리 채움) — ② 는 front
- 새 시험 `tests/test_app_qweb.py`(18) — SPEC-006 §10.1 묶음 전부(토큰 · 공개 GET · POST · 다시 띄우기 · pending · 상세 · claim · 속도 제한 · 로그에 토큰 0 · 없앤 경로 404). 옛 시험 고침: `test_app_be3.py`(문진 = `qrUrl` · claim 시험은 스캔 종류로) · `test_app_be4.py`(언어 표만 남김) · `test_order.py`(49)

### 데모 실호출 (코디 허가 · 데모 테넌트 assert · 운영 키 0)
- 대상 `[ccc 시험]` 고객 1명(이름 접두 assert) · 스크래치 DB 에 띄우기 요청 1(KOS 일정 쓰기 없음) · **실제 공개 route 를 앱 안에서(ASGI)** 부름
- 만들기: `qrToken` null · `qrUrl` = `{PROC_FRONT_ORIGIN}/q#` + 43자
- 공개 `GET` 200 · 키 6개(허용 목록) · 언어 `en`(source `default` — 이 고객은 KOS language · 국적 표 둘 다 없음) · 4쪽 · 약관 1 · `no-store`
- 공개 `POST` **200 `{ok:true}`**(답 15줄 · 미리 채운 값 그대로) → 다시 `GET` = 409 `q_submitted` · 요청 `done` · 이력 `web_submit` 1행(`en`)
- 호출: 내부 get-visitor 1 · 공개 get-visitor-questionnaire 1 · get-questionnaire-agreements 1 · **submit-visitor-questionnaire 1(쓰기)** · get-questionnaire-submit 1
- **남긴 흔적**: 그 시험 고객 KOS 문진 제출본 1건 덮어씀(성별 · 생년월일 · 주소 · 휴대폰 · 동의 = 미리 채운 값 그대로 다시 씀 · 비어 있던 칸은 `[ccc 시험]` 문구 · 시험 번호로). 되돌리지 않음

### 코디 확인
- front · app 은 문진 요청에서 `qrToken` 대신 **`qrUrl`** 을 쓴다(문진 `qrToken` = null). 공개 오류 본문 = `{error:{code, message}}` 만(`requestId` 안 실음)
- 공개 `GET` 은 고객이 제출 전에 여러 번 열 수 있다(`opened` 안 · 쓰는 시한 안)
- 「여권 사진 분류」 는 이미 `7e39bd3` 로 커밋됨 — 이 절 파일과 겹치지 않음

### 바뀐 파일
`procedure/.env.example` · `procedure/back/app/{api/auth.py, api/public_questionnaire.py(새), api/questionnaire.py(지움), config.py, container.py, domain/errors.py, domain/models.py, main.py, repository/db.py, repository/repo.py, schemas/actions.py, schemas/reservations.py, service/auth.py, service/display.py, service/questionnaire.py}` · `tests/{test_app_be3.py, test_app_be4.py, test_order.py, test_app_qweb.py(새)}`

---

## WORK-010 건강 정보 반영 (2026-10-28 · branch `kknaksss/overall-board-6`) — done

증상(frontend 실 back 확인): 공개 POST 200 뒤 데스크 상세 `health` = `ok` · **items 0** · `submittedAt` = 어제 값.

### 원인 — 둘 (데모 테넌트 **읽기만**으로 확인 · 쓰기 0)
1. **items 0 = 매핑**: `domain/reservation_rules.health_items` 가 쪽 제목이 **정확히** 「건강 정보」인 쪽을 찾는데, 실 KOS 양식 쪽 제목은 **「건강 정보 >> 안전한 시술을 위해 …」** 꼴(4쪽 모두 `이름 >> 안내`). 실 양식 × 실 제출본으로 옛 판정 = 맞는 쪽 0 → 고친 판정 = **7칸 · 7칸 답 있음**. (가짜 KOS 양식 제목이 「건강 정보」 그대로라 시험이 못 잡았다 — SPEC-005 때부터 실 화면 items 는 늘 0 이었을 것)
2. **submittedAt 어제 = KOS 읽기가 첫 제출본**: 오늘 데모 POST(KOS 200 `{questionnaireId}`)를 받은 시험 고객의 제출본 읽기 = **어제(10-27) 제출본 · 15줄 그대로** — 공개 `get-questionnaire-submit` 과 **KOS 웹이 쓰는 내부 `visitor/questionnaire/v1/queries/get-questionnaire-submit/legacy`** 둘 다 같은 행(같은 id). 즉 **다시 제출은 받지만 제출본 읽기는 첫 제출본을 준다**(Q-27 의 답 · KOS 웹 화면도 옛 답일 것). 그래서 ccc 는 제출 뒤 다시 읽어 **어제 행을 `web_submit` 으로 고쳐 쓰고**(같은 `kos_submitted_at`) 새 답은 어디에도 없었다. 캐시 · 최상위 객체 매핑은 문제 아님(최상위 객체 · `answers` 키 맞음)

### 고침
- `domain/reservation_rules.py` — `page_name()`(제목의 `>>` 앞) · `health_items` 가 그것으로 「건강 정보」 쪽을 찾음
- `service/questionnaire.py` `submit_for` — 제출 확인의 `createdDateTimeUtc` 가 **제출 시작보다 60초 넘게 앞이면(또는 없으면) 옛 제출본**으로 보고, **받은 답을 KOS 제출본 꼴**(`{seq, questionId, questionTitle, answerId, answerTitle, memo}` · `submitted_answers()`)로 `questionnaire_history` 새 행(`web_submit` · `kos_submitted_at` = ccc 제출 시각 `…000Z`)에 둔다 — 옛 행은 그대로. 새 제출본을 주면 지금처럼 그 키로. `questionnaire_submit` 이벤트에 `kosReadStale` 더함
- `service/reservations.py` `_health` — 그 고객의 가장 늦은 `web_submit` 행(`repo.latest_web_questionnaire`)이 KOS 제출본보다 **새로우면 그것으로** 「건강 정보」(`submittedAt` · 항목)를 그린다 · KOS 가 더 새 제출본을 주면(예: KOS 웹에서 제출) KOS 가 이긴다 · KOS 제출본 읽기 오류여도 ccc 행이 있으면 그린다. (SPEC-006 §9 「ccc 가 SoT」 를 읽는 쪽만 앞당김 — KOS 제출은 그대로 함)
- tests: `tests/fake_kos.py` `keep_first_submit`(실 KOS 꼴) · `tests/test_app_qweb.py` 2개 더함 — 실 꼴 쪽 제목 · 「다시 제출 → 상세에 방금 답 · 제출 시각 · 이력 옛 행 그대로 + 새 행 · KOS 가 더 새면 KOS」 · 앞 시험 1곳(`kosReadStale`)

### 검증
- `uv run ruff check .` → All checks passed · 전체 **469 passed**
- 실 데모(읽기만): 실 양식 × 실 제출본 → `health_items` 7칸(고치기 전 0)

### 코디 확인
- **KOS 쪽 사실(사용자 · planner 에)**: 같은 고객이 두 번째로 낸 문진은 KOS 제출본 조회(공개 · KOS 웹 legacy)에 안 보인다 — **KOS 웹 「설문」 화면은 계속 첫 답**일 것. ccc 데스크 · 앱 상세는 이번 고침으로 새 답을 보인다. 다만 KOS 고객 값(성별 · 생년월일 · 주소 · 휴대폰 · 동의)이 두 번째 제출로 바뀌는지는 이번에 확인하지 않음(쓰기 허가 밖)
- 스크래치 데모 DB 의 어제 행은 오늘 데모에서 `web_submit` 으로 잘못 고쳐졌다(스크래치만 · 운영 · 레포 영향 없음)

### 바뀐 파일
`procedure/back/app/domain/reservation_rules.py` · `app/repository/repo.py` · `app/service/questionnaire.py` · `app/service/reservations.py` · `tests/fake_kos.py` · `tests/test_app_qweb.py`

---

## E2E batch 3 — 웹 예약 상세 (2026-10-28 · branch `kknaksss/overall-board-8` · base `113c5e1`) — done

### #1 사진 삭제 — `DELETE /api/id-photos/{photoId}` → `{ok:true, kos:"deleted"|"not_found"|"skipped"}`
- **KOS 경로(KOS 웹 [삭제]와 같음)**: KOS 웹 JS `image-manage-client` — `this.delete = e => fetcher("/tenants/:t/image/visitor-image/v1/commands/delete-visitor-images", xt.toJSON(e))` · 메시지 `xt` = `{ids:[string]}` · 화면 [삭제] = `delete({ids: 고른 이미지.map(id)})`(HAR `예약그룹.har` 의 JS 번들 · 실제 요청 기록은 없음 — 아래 데모로 확인). 이미지 id 는 내부 `get-visitor-images{visitorId, deleted:false}` 항목 `id`
- `service/id_photo.py` `PhotoService.delete()`(**법적 검토 주석**): ① KOS — 같은 `fileName` 의 이미지 id 를 찾아 `delete-visitor-images{ids}` · 못 찾으면 `not_found`(올리기 실패 · 이미 지움) · ccc 가 KOS 로 안 올린 사진(`skipped`)은 안 부름 · **KOS 오류면 409 `kos_rejected` / 502 + `event_log(kos_rejected)` · ccc 는 그대로**(다시 누르면 됨) ② ccc — 파일 · `id_photo` 행 지움 · 신분 확인 행의 `photo_id` 비움 · **마지막 신분 확인이 이 사진으로 한 「확인 완료」면 「미확인」 1행**(뒤에 웹에서 따로 확인했으면 그대로) ③ `event_log(id_photo_delete){photoId, customerId, kos}` · 고객 값(여권번호 등)은 그대로
- `api/photos.py` 경로 · `require_real_board` · CORS `allow_methods` 에 `DELETE`(로컬 3700 ↔ 8700)

### #2 유입 채널 — `PUT /api/customers/{customerId}/funnel {funnelId: int|null, funnelDetail?}` → `{ok:true}`
- KOS 고객 칸 = 관리 묶음 `visitorFunnel{funnelCategoryId, funnelId, funnelDetail}`(데모 읽기 50명: `funnelCategoryId` 늘 빈 값 · `funnelId` = FUNNEL 코드 `id` — 31명 모두 코드 목록에 있음)
- `ReservationService.funnel()` — 특이사항(`remark`)과 같은 길: **직전 내부 `get-visitor` 다시 읽기 → 관리 묶음 그대로(빈 배열 뺌) + `visitorFunnel` 만 바꿈 → `update-visitor-management-information`** · `funnelId` = ccc `funnel_code` id(예약 등록이 쓰는 FUNNEL 코드 그대로 · 닫힌 코드 · 없는 id = 400) · `null` = 비움 · `funnelDetail` 은 보낼 때만 고침 · `funnelCategoryId` 는 읽은 값 그대로 · **같은 값이면 KOS 안 부름** · `event_log(visitor_funnel)`
- 상세 응답 더함: `customer.funnel = {funnelId, name, detail} | null`(KOS 고객 값 · 코드 목록에 없는 id 면 `funnelId`·`name` null) · `funnelCodes = [{funnelId, name}]`(닫힌 것 뺌). 지금 있는 `reservation.funnel`(예약의 유입)은 그대로 — 화면은 고객 칸(`customer.funnel`)을 쓴다

### #3 ~ #5 자동 저장 — 지금 API 그대로 쓰면 됨 + 같은 값이면 KOS 안 부름
- `PUT …/remark`(주의사항) · `PUT /api/reservations/{id}/memo`(예약 메모) · `PUT …/personal`(고객 기본 정보 칸마다) — 응답 모양 그대로 `{ok:true}`
- **같은 값 건너뜀**: remark = 다시 읽은 `memo` 와 같으면 · memo = 사본 `reservation.memo` 와 같으면 · personal = 다시 읽은 값과 바꿀 칸이 모두 같으면(빈 값끼리 포함) → KOS 쓰기 0 · 이벤트 0. **직전 다시 읽기는 그대로**(remark · personal · funnel)
- 칸마다 저장(personal 에 그 칸 하나만 보내기)도 지금 함수로 된다 — 다시 읽은 묶음 전체 + 그 칸

### 검증
- `uv run ruff check .` → All checks passed · 전체 **474 passed** · 경로 **`test_route_count_51`**(HTTP 50 + WS 1 — 사진 삭제 · 유입 채널 더함)
- 새 시험 `tests/test_app_e2e3.py`(5): 사진 삭제(ccc · KOS id · 미확인 · 고객 값 그대로 · 두 번째 404) · KOS 실패 = ccc 그대로 · KOS 에 없음 + 뒤 확인 = 그대로 · 유입 채널(상세 · 묶음 그대로 · 같은 값 0 · 설명 · 닫힌 코드 400 · 비움) · 자동 저장 같은 값 0. `tests/fake_kos.py` 이미지 조회 · 삭제

### 데모 실호출 (데모 테넌트 assert · 운영 키 0 · `[ccc 시험]` 고객 1 · 스크래치 DB)
- ① **사진 삭제 1**: 앞 판(「여권 사진 분류」 데모)에서 올린 TEST 그림 1장 — `PhotoService.delete` → KOS 이미지 3 → **2** · 그 사진 없음 · ccc 행 · 파일 없음 · 결과 `deleted` (= 앞 판 흔적 1장을 지움)
- ② **유입 채널 쓰기 1**: 같은 고객(전: 유입 비어 있음) → 코드 「강남언니」 → 다시 읽기: `funnelId` = 그 코드 · `funnelDetail` 그대로 · 다른 관리 칸(memo · 유형 · 분류 · 담당 의사 · 상담사 · 사용자 속성 · 동의) **그대로**
- 호출: 내부 get-visitor-images 2 · **delete-visitor-images 1(쓰기)** · get-visitor 3 · **update-visitor-management-information 1(쓰기)**
- **남긴 흔적**: 그 시험 고객 유입 채널 = 「강남언니」(비어 있던 칸). 되돌리지 않음. KOS 이미지 1장은 지워짐(TEST 그림)

### 코디 확인 (front 에)
- 사진 삭제 응답 `kos` 로 「KOS 사진도 지움 / KOS 에 없었음」 정도만 · 실패(409 · 502)면 아무것도 안 지워졌으니 다시 누르기
- 유입 채널 드롭다운 = `funnelCodes` · 지금 값 = `customer.funnel.funnelId` · 비우기 = `{funnelId:null}`
- 신분 확인 「미확인」은 그 사진으로 한 확인일 때만 바뀐다(접수 뒤에도 — 사진을 지우면 확인 근거가 없어지므로 `[미확인으로]` 잠금을 따르지 않음)

### 바뀐 파일
`procedure/back/app/{api/photos.py, api/reservations.py, main.py, repository/repo.py, schemas/actions.py, schemas/reservations.py, service/id_photo.py, service/reservations.py}` · `tests/{fake_kos.py, test_order.py, test_app_e2e3.py(새)}`

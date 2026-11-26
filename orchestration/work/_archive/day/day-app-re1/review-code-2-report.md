# 리뷰 리포트 — day-app-re1 WORK-002 / code (2026-11-25)

대상 = `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app-re1` 커밋 `fb08fe4e`(`git diff 96036397..fb08fe4e` · 119 파일).
읽은 SSOT = `delivery-2-report.md` §5 A·B(W0 ~ W9) · `_RESUME.md` §2 WORK-002 행 · `be-2-report.md` §0 · `app-2-report.md` §5 · §6 · cc-prototype `0553173`(`/Users/kknaks/git/toy_pr2/cc-prototype`).
실행한 것(읽기 전용 · 로컬 스택 · KOS · 시뮬레이터 없음):
- `fvm flutter test test/model/reservation_model_test.dart test/state/reservation_state_test.dart test/ui/reservation_ui_test.dart test/scan` → **All tests passed (+45)**
- `uv run pytest backend/tests/day/test_display_rules.py backend/tests/day/test_reservation_detail_rules.py` → **33 passed**
- 문진 글자 기계 대조: `presentation/questionnaire_text.py` `TEXT` 204개 글자(6언어) 전부가 cc `procedure/front/lib/q/text.ts` 안에 있음 → **빠진 것 0**
- SQLAlchemy identity map 재현 스크립트(SQLite, `scratchpad/idmap.py`): 다른 세션이 `done` 으로 커밋한 뒤에도 같은 세션의 `select` · `get(with_for_update=True)` 가 `opened` 를 돌려줌

## 판정: FAIL

FAIL 1(backend) · WARN 15(backend 8 · app 7) · 사용자 확인 3. 앱 ↔ backend 계약(경로 · 칸 · 상태 · 코드 · SSE · 푸시)은 **모두 PASS**다. FAIL 은 고객 문진 「제출 1회」를 DB 가 보장하지 않는다는 것 하나다.

---

## FAIL

### F1. 「제출 1회」가 Redis 잠금 + 낡은 값으로 다시 확인하는 것에만 기대고, DB 보장이 없다 — **backend**
- 자리: `backend/day/services/questionnaire_public.py:281` · `:287` · `:296` · `:310` / `backend/day/services/displays.py:449-455`(`finish`) / `backend/day/models/reception.py:114`(`questionnaire_history.display_request_id` = 그냥 FK · unique 없음) / `backend/common/db/session.py:124`(`expire_on_commit=False`)
- 근거:
  - 처음 `_target_or_deny`(:281)가 `DisplayRequest` 를 세션에 올린다.
  - 잠금 안에서 다시 확인하는 `_target_or_deny`(:287)와 `session.get(DisplayRequest, id, with_for_update=True)`(:296)는 FOR UPDATE 잠금은 잡는다. 그러나 `populate_existing` 이 없어 **이미 올라온 객체의 속성을 새로 채우지 않는다**(재현 스크립트로 확인).
  - `displays.finish()` 는 낡은 `status` 를 보고 `DONE` 을 쓴다. 반환값 `False` 도 submit 이 버린다(:310).
- 재현(경합):
  - ① 고객 제출의 첫 읽기와 `get … FOR UPDATE` 사이에 직원이 웹 [취소]를 누르거나 새 링크를 만든다 → `CANCELED` 가 커밋된다 → 제출이 그 위에 `DONE` 을 덮고 답을 저장한 뒤 KOS 에 보낸다(닫기 = canceled 계약 위반).
  - ② 같은 링크로 제출 둘(B 가 A 커밋 전에 읽고, A 가 잠금을 푼 뒤 잠금을 잡음) → `questionnaire_history` 2행 · KOS 제출 2번.
- 규칙: AGENTS.md 「공유 상태의 불변식은 사전 조회만으로 보호하지 않는다 — DB constraint · 원자적 갱신 · row lock · 멱등 키」. 지금은 Redis 잠금이 유일한 보호다.
- 고칠 방향:
  - 넘김을 원자적 갱신으로 바꾼다 — `UPDATE display_request SET status='done', closed_at=:now WHERE id=:id AND status IN ('pending','opened') RETURNING id`. 행이 안 오면 409 `q_submitted` 또는 410 `q_canceled` · `q_expired`. 최소한 `get(..., with_for_update=True, populate_existing=True)` 를 쓰고 `finish()` 의 False 를 오류로 바꾼다.
  - `questionnaire_history(display_request_id) WHERE display_request_id IS NOT NULL` partial unique index(새 migration 또는 0029 안 — push 전이라 0029 를 고쳐도 된다).
  - 실제 PostgreSQL infra 시험: 동시 제출 2 → 1행 · 제출 중 [취소] → 답 없음.

---

## WARN — backend

### BW1. Redis 가 안 되면 고객 제출이 500 이고, 그 응답에 no-store · no-referrer 머리가 없다
- 자리: `services/questionnaire_public.py:283`(`try_lock`) → `common/redis.py:82`(`redis.set` 예외 처리 없음) · `routers/api/public_questionnaire.py:52-56`(`PublicRoute` 는 `ServiceError` 만 잡음)
- 근거:
  - 속도 제한은 Redis 실패 때 열어 두는데(`:92-94`), 제출 잠금은 `RedisError` 가 그대로 올라간다. Starlette 500 이 되고 `PUBLIC_HEADERS` 를 달지 않는다.
  - 계약은 「응답마다 `Cache-Control: no-store` · `Referrer-Policy: no-referrer`」(W7)다. 그리고 be-2 §5 「Redis 가 안 되면 열어 둔다(고객이 막히지 않게)」 의도와 반대로 Redis 장애 때 고객이 아예 제출하지 못한다.
  - 500 본문에 정보는 없어 노출 위험은 낮다 → WARN.
- 고칠 방향: `PublicRoute` 에서 `Exception` 도 잡아 코드가 있는 5xx 로 돌려주고 머리를 단다. 잠금 실패의 갈래(열어 둠 · 503)를 정한다. F1 의 DB 보장이 들어가면 열어 둬도 안전하다.

### BW2. 고객 200 이 KOS 제출을 기다린다 — 브라우저가 30초에 끊으면 DAY 에 저장됐는데도 「실패」가 보인다(「15초 넘김」 자리)
- 자리: `services/questionnaire_public.py:329-330`(`await questionnaire_kos.send` 뒤 return) · `static/day.js:221`(`exchange` 30000 ms abort) · `common/config.py:212`(`emr_http_timeout_seconds=15`)
- 근거:
  - 계약 W7 ④ 는 「고객 200 = DAY 저장되면(KOS 결과 안 보임)」이다. 구현은 커밋한 뒤 같은 요청 안에서 KOS 공개 토큰 + 제출을 부른다(401 이면 한 번 더 → 최악 약 60초).
  - 30초가 넘으면 고객은 오류를 본다. 다시 누르면 409 `q_submitted` 다.
  - 「조용히 통과」는 아니지만, 고객이 본 것과 DAY 가 남긴 것이 갈린다.
- 고칠 방향: 커밋 뒤 바로 200 을 돌려주고 KOS 보내기는 taskiq 태스크(또는 응답 뒤 background)로 옮긴다. 멈춘 `sending` 판정(OQ-D41)이 이미 있어 행이 멈추지 않는다.

### BW3. [다시 보내기]가 아직 진행 중인 보내기와 겹칠 수 있다
- 자리: `services/questionnaire_kos.py:92-96`(마지막 `UPDATE` 에 `WHERE crm_status='sending'` 이 없음) · `services/questionnaire_reads.py:19-23`(멈춤 = timeout + 60초)
- 근거: 보내기가 멈춤 한도를 넘기면 [다시 보내기]가 같은 행을 다시 잡는다. 그러면 KOS 제출 2번이 되고, 늦게 끝난 쪽이 결과를 덮는다. httpx timeout 은 요청 전체가 아니라 동작 하나마다 걸린다.
- 고칠 방향: 결과 쓰기에 `AND crm_status='sending'`(가능하면 시도 번호 칸 또는 `updated_at` 비교)을 넣고, KOS 호출 전체를 `asyncio.timeout` 으로 감싼다.

### BW4. KOS 양식을 받는 동안 취소된 링크에도 양식이 200 으로 간다
- 자리: `services/questionnaire_public.py:230-236`(KOS 를 부른 뒤 다시 읽을 때 `PENDING` 인지만 봄)
- 근거: 그 사이 `canceled` 가 되면 그 상태를 거르지 않고 양식을 돌려준다(제출은 410 이라 저장되지는 않음).
- 고칠 방향: 다시 읽은 상태가 닫힘이면 410 `q_canceled` · `q_expired`.

### BW5. 형식이 틀린 본문은 속도 제한 전에 400 이 된다
- 자리: `routers/api/public_questionnaire.py:101-109`(본문 검사) → `services/questionnaire_public.py:278`(`_gate`) · 시험 `tests/day/board/test_public_questionnaire.py:226` 이 이 순서를 굳힘
- 근거: 형식이 틀린 POST 는 IP 당 5 제한을 받지 않는다(DB 는 안 닿아 비용은 낮음). 토큰이 없는 틀린 본문도 `q_token_missing` 이 아니라 `invalid_request` 다.
- 고칠 방향: IP 제한 `_gate` 를 본문 검사 앞으로 옮긴다(라우터에서 서비스의 gate 를 먼저 부르기).

### BW6. 속도 제한 · 거절 로그 간격이 Redis 장애 때 모두 꺼진다(의도된 열어 둠 — 기록만)
- 자리: `services/questionnaire_public.py:92-94` · `:119-120`
- 근거: GET 30 · POST 5 · 토큰 3 · 틀린 토큰 10 이 모두 꺼진다. `qweb_denied` 1분 1줄 간격도 꺼져 거절마다 `event_log` 가 쌓인다. 남는 보호는 43자 HMAC 토큰 하나다. be-2 §5 에 적힌 결정이라 WARN 으로만 둔다.
- 고칠 방향: 결정 유지라면 SPEC(OQ-D40)에 「Redis 장애 = 제한 끔」을 적고, 거절 로그는 Redis 장애 때 서버 로그만 남긴다.

### BW7. 토큰이 주소창 · 방문 기록에 남는다
- 자리: `static/day.js:5473`(`location.hash` 를 읽기만 함 · `history.replaceState` 없음)
- 근거: 서버 · Referer · 로그로는 새지 않는다(`#` 뒤 · 헤더로만 보냄 — PASS). 그러나 고객 폰 방문 기록 · 주소창 화면 캡처에는 남는다. 1회 · 60분 시한이라 위험은 낮다.
- 고칠 방향: 토큰을 읽은 뒤 `history.replaceState(null, "", location.pathname)`.

### BW8. 시험이 계약의 핵심을 다 지키지 않는다(초록이지만 비어 있음)
- `tests/day/board/test_public_questionnaire.py:218-232`: 「같은 토큰 POST 3」 시험은 틀린 토큰(`"B"*43`)만 쓰고 `429 in statuses` 만 본다. 토큰 · IP · 틀린 토큰 막음 중 무엇이 걸렸는지 가르지 못한다.
- `:241`: 항상 참인 단언이다.
- 시험이 없는 것: GET 30/IP · 틀린 토큰 10번 막음 · `X-Day-Client-IP` 믿는 규칙 · `phoneticName` · 최상위 모르는 키 · 60분 시한(HTTP) · 동시 제출(F1).
- `tests/day/board/test_reservation_app_displays.py`:
  - 대상 기기 거르기(폰 · 코디 아닌 직무 · 끝난 세션 · 다른 병원)가 없다.
  - 다른 병원 create · close · pending 이 없다.
  - `displayRequestId` 는 무작위 uuid 만 본다(:458). 다른 기기 · 다른 방문 · 문진 종류 요청으로 하는 시험이 없다.
  - 「같은 계정 다른 기기」는 `own_device` 거르개를 가짜 세션 id 로 부를 뿐이다(:256-258). 실제 스트림 두 개로 보지 않는다.
- 고칠 방향: 위 빈칸을 PostgreSQL infra 시험으로 채운다(특히 F1 동시 제출 · 기기 거르기 · 다른 병원 404).

## WARN — app

### AW1. Android 스캔 화면에 FLAG_SECURE 가 없고, `excludeFromRecents` 는 효과가 없다(app-2 §4 「최근 앱 목록 제외」 주장과 다름)
- 자리: `app/android/app/src/main/AndroidManifest.xml:54`(`excludeFromRecents="true"`) · `app/android/app/src/main/kotlin/day/medisolveai/ScanChannel.kt:96-101`(`FLAG_ACTIVITY_NEW_TASK` 없이 `startActivity` → MainActivity task 의 위에 쌓여 root 가 아님) · FLAG_SECURE 0건(grep)
- 근거: 최근 앱 썸네일 · 화면 캡처에 여권 미리보기가 남는다. Flutter 확인 화면(7칸)도 두 OS 모두 막지 않는다.
- 고칠 방향: `PassportScanActivity.onCreate` 에 `window.addFlags(WindowManager.LayoutParams.FLAG_SECURE)` 를 넣는다. 확인 화면이 떠 있는 동안 MainActivity 창에도 secure 를 켰다가 끈다(채널 하나 추가). app-2 리포트의 주장도 고친다.

### AW2. Android 카메라 시작 실패 = [닫기]와 같은 처리 → 받은 요청이 조용히 canceled 되고 [손으로 입력]도 안 나온다
- 자리: `PassportScanActivity.kt:205-209` · `:226-228`(`ProcessCameraProvider` · `bindToLifecycle` 예외 → `finishWith(null)`) → `app/lib/ui/scan_screen.dart:154`(`shot == null` → `_close()` → `closeDisplay`)
- 재현: 다른 앱이 카메라를 쥐고 있는 갤럭시 탭에 웹에서 [여권 스캔]을 보낸다 → 태블릿 화면이 바로 닫히고 웹 진행 줄이 사라진다. 직원에게 이유가 안 보인다. iOS 는 같은 경우 실패 → 손 입력으로 간다.
- 고칠 방향: 카메라 시작 실패는 `no_camera` 오류(또는 `{failed: true}`)로 돌려 `ScanStage.noCamera` → [손으로 입력] 으로 보낸다.

### AW3. 손 입력 칸이 형식 없는 자유 글자다 — 잘못된 값이 KOS 로 간다
- 자리: `app/lib/ui/scan_screen.dart:391-405`(일반 `TextField` 7개) · `backend/day/services/passport_scan.py:88-116`(날짜 · 성별만 400)
- 근거:
  - 성별은 `MALE` / `FEMALE` 를 정확히 쳐야 한다. 국적(alpha-2) · 여권번호는 앱 · 서버 어느 쪽도 검사하지 않는다.
  - 칸이 모두 비어도 [저장]이 켜진다(`fieldsToSend` → `{}`).
  - 서버 400 은 「저장하지 못했어요 · 요청이 올바르지 않습니다」로만 보이고 어느 칸인지 알 수 없다.
- 고칠 방향: 앱은 성별 고르기 · 날짜 형식 검사 · 여권번호 `[A-Z0-9]{1,9}` · 보낼 칸이 없으면 [저장] 끔 · 400 `field` 로 그 칸 강조. 서버는 국적 코드(alpha-2) · 여권번호 형식 검사 — **backend 몫 일부**. 글자는 새로 짓지 말고 SPEC 에 없으면 비운다.

### AW4. MRZ 여권번호 「고치기」가 체크숫자를 맞추는 다른 번호를 만들 수 있다
- 자리: `app/lib/scan/mrz.dart:85-100`(`_docNumber` — 닮은 글자 바꾸기를 최대 63가지 시도해 mod-10 이 맞으면 채택) · 종합 체크숫자는 의도적으로 안 봄(`:133-134`)
- 근거: 체크숫자는 한 자리(10가지)라, 잘못 읽은 번호가 바꾼 조합 중 하나로 통과할 확률이 작지 않다. 같은 오독이 두 번 반복되면 자동 촬영 확인(두 번 일치)도 지난다. 남는 보호는 직원 확인 화면뿐이다. cc 원천을 그대로 옮긴 것이라 출처 동작이다.
- 고칠 방향: 바꾸기를 1 ~ 2자리로 줄이거나, 바꾸기를 썼으면 종합 체크숫자를 필수로 본다. 바꾼 값이면 확인 화면에서 그 칸을 노랑으로 보인다.

### AW5. 받은 스캔의 상세 읽기가 실패하면 그 요청이 다시 열리지도 닫히지도 않는다
- 자리: `app/lib/ui/display_flows.dart:250-256`(실패 → 토스트만) · `app/lib/state/display_inbox.dart:71-76`(`take()` 가 이미 `_opened` 에 넣음)
- 근거: 서버는 `pending` 응답 때 이미 `opened` 로 바꿨다. 웹에는 「{기기}에서 스캔 중 · 촬영 대기 중…」이 시한(60분 · be-2 D13)까지 남는다. 태블릿은 다시 받지 않는다.
- 고칠 방향: 상세 읽기에 실패하면 `_opened` 에서 빼고 다음 메우기 때 다시 열거나, `closeDisplay(canceled)` 를 보낸다.

### AW6. Android 분석 프레임마다 1080p 비트맵을 만든다(메모리 · 버벅임)
- 자리: `PassportScanActivity.kt:281`(`upright()` 가 `busy` / 100 ms 검사 `:285` 보다 앞) · `:236`(회전 때 하나 더)
- 근거: 프레임마다 약 8 MB ARGB 를 만들고 GC 에 맡긴다. 낮은 사양 탭에서 버벅임 · OOM 위험이 있다.
- 고칠 방향: 간격 검사를 `toBitmap` 앞으로 옮기고, 앞 `lastFrame` 을 쓰지 않으면 `recycle()` 한다.

### AW7. 의존성 · 개인정보 표기(정보)
- `app/android/app/build.gradle.kts` 새 의존성:
  - CameraX 1.4.2 · androidx.activity 1.10.1 · ZXing core 3.5.3 = Apache-2.0 → 앱 오픈소스 고지에 넣어야 한다.
  - `com.google.mlkit:text-recognition:16.0.1` = 오픈소스가 아니고 ML Kit 약관이다. 번들 모델이라 기기 안에서 판독하지만, ML Kit 은 사용 · 성능 지표를 Google 에 보낸다고 공개한다(이미지 · 인식 글자는 안 보냄 — 이번 검수에서 Google 문서와 대조하지는 않음) → Play 데이터 보안 양식 · 개인정보 안내(OQ-A89).
- backend `segno>=1.6,<2`(`pyproject.toml`) = 순수 Python · MIT 계열 · 이유(CSP · day.js 하나 규칙 때문에 서버 SVG) 타당 → PASS.
- 고칠 방향: 출시 전 고지 · 데이터 보안 양식 항목에 넣는다(사용자 · 코디 몫).

---

## PASS — 볼 것 1 ~ 6 대조

### 1. backend ↔ app 계약 맞물림 — PASS
| 항목 | 앱 | backend | 판정 |
|---|---|---|---|
| 경로 11개 | `app/lib/data/reservation_api.dart:21-77` | `routers/api/reservations.py:34-108` · `api/displays.py:75-198` · `api/devices.py:73` | PASS — 글자 같음 · Bearer |
| 목록 칸(camel) `today · date · weekday · isToday · nowMin · openMin · axis{startMin,endMin,timeGraySpans} · columns{groupId,title,capacity,intervalMinutes,graySpans} · cards{visitId,groupId,startMin,endMin,lane,line,name,nationality,isNew,state,paymentDue,staff{role,name},companionGroupId} · rows{startMin,endMin,lines} · bands{groupId,columnId,startMin,line,laneFrom,laneTo} · filter{total,counts} · notice{content}` | `model/reservation.dart:35-202`(`_v` = snake → camel) | `schemas/reservations.py:15-154` | PASS(`inhouse` 는 앱이 안 그림 — OQ-A80 · app-2 §6) |
| 상세 칸 `visitId · stage · dateKind · isNew · customer{name,passportName,contact,birth,age,gender,nationality,isDomestic,notes} · identity{confirmed} · questionnaire{submittedAt,time,sendStatus} · health[{question,answer}] · reservation{…,doctor(글자),companions[{visitId,name}]} · consult{orderMemo} · treatments · dischargeReason · payment · previousVisits · displays[] · actions{questionnaireQr,passportScan,sendToTablet}` | `model/reservation.dart:269-527` | `schemas/reservation_detail.py:16-215` | PASS — be-2 D2 `sendStatus` · D5 `companions{visitId,name}` · D9 `displays[]` 따라감. `procedureInfo` · `paymentRequired` · `consult.counselor/room` 은 앱이 안 읽음(웹에서 쓰기 바닥 줄 전용 `reservations_detail.html:33,261` — 읽기 전용 앱엔 해당 없음) |
| W3 여권 7칸 · W6 응답 `identity{status,method,checkedAt} · photo{id,kosSynced} · kos{customer,photo}` · retry · W4 `targets{deviceId,name,online}` · 만들기 `{requestId,kind,status,expiresAt,deviceName,qrUrl}` · pending `requests{requestId,kind,visitId,expiresAt,qrUrl}` | `model/reservation.dart:558-640` | `schemas/displays.py:33-193` | PASS(be-2 D7 · D8) |
| 닫기 본문 `{status: canceled}` · 기기 이름 `PUT …/name {name}` | `reservation_api.dart:44` · `:77` · `state/push_coordinator.dart`(등록 뒤 `PUT …/name`) | `schemas/displays.py:21-30` | PASS(app-2 §5-5 · be-2 D 등록 `name` 도 받음 — 둘 다 맞음) |
| 예약 SSE `reservation`(version) · `display`(방문 id 글자) · `session_expired` · 앱 = `write_confirmed` · `kos_failed` 뺌 | `state/reservation_controller.dart:101` · `:138` · `data/event_stream.dart`(JSON 아님 → `{value}`) | `routers/reservations_streams.py:117-123`(`app=True`) | PASS |
| 알림 SSE `display {requestId,kind,visitId}` = 그 세션 연결만 | `notify/notification_controller.dart:59-71`(신호 → 메우기) | `routers/api/notifications.py:136-143`(`own_device`) · `services/notification_events.py`(`publish_display` 에 `session` 실음) · `schemas/events.py:94-102` | PASS |
| 푸시 iOS `aps.alert{title,body}` 소리 없음 + 최상위 `kind:display · requestId · environment · hospitalId` · Android data = `data_of` 로 `title · body` + 같은 칸 | iOS `AppDelegate.swift` · `AcceptLogic.swift`(`tapKeys`+`requestId`) · Android `PushLogic.kt`(`KIND_DISPLAY` · 채널 id `display` · 이름 「고객 입력 요청」 · `silent` · tag `display:{requestId}`) · Dart `push_coordinator.dart`(환경 · 병원 같을 때만 `onDisplay`) | `services/display_push.py:39-56` · `adapters/fcm.py:60-72` | PASS(be-2 D6) |
| 오류 코드 `customer_not_linked` · `display_closed` · `visit_not_today` · `visit_stage_changed` · `reservation_past_date` · `kos_unavailable` · `photo_disabled` | `core/copy.dart:60`(`actionMessage` → 표에 없으면 코드만 · OQ-A7) | `common/error_codes.py` · `day/errors.py` | PASS(글자 미정 = 코드만 — app-2 §5-10 · 기존 규칙) |
| `crm_status`(be-2 D1) | 앱은 DB 칸을 모름 · `sendStatus` 만 | `models/reception.py` · migration 0029 | PASS — spec-sync 몫 |

### 2. 결정 위반 — PASS
- 앱 상세 쓰기 0: 누르는 것은 [문진 QR] · [여권 스캔] · [태블릿에 보내기](`ui/display_flows.dart:44-60`)와 닫기 · 이전 방문 접기 · 동행 이동뿐이다. 웹 쓰기 11개는 없고, 보이기는 서버 `actions` 만 따른다.
- 기기 하나로만: SSE 거르개(`notifications.py:136-143`) · 푸시 한 행(`display_push.py:83-85` · `push.py` `device_id`) · pending = 자기 기기 · 그 병원(`displays.py:407-427`).
- 문진 DAY 먼저 → 요청 done · 신호 → KOS · 실패여도 답이 남음(`questionnaire_public.py:296-330` · `questionnaire_kos.py:70-100`). 멈춘 `sending` = 읽을 때 failed(`policies/displays.py:85-99`). [다시 보내기] = 원자적 `UPDATE … RETURNING`(`questionnaire_kos.py:113-128`) · 웹만(앱 없음).
- 외국인 스캔 = `identity_check confirmed`(`passport_scan.py:377-386`) → `queries/reservation_treatments.py:52` → [상담 대기] · [시술 대기](`reservation_care_writes.py:338` · `:445`) · 웹 「O」 + `data-day-res-id-ok`(`reservations_detail.html:117` · `day.js:3453-3456`).
- 여권번호 상세 JSON 에 없음: `DetailCustomer` 는 `passportName` 만(`schemas/reservation_detail.py:16-27`). 여권 7칸은 W3 를 확인 화면에서만 부른다(`scan_screen.dart:190-200`).
- 공용 코디 계정 판정: 그 병원 · tablet · 살아 있는 세션 · 활성 직원 · 직무 `coordinator` 태그(`displays.py:140-179`). 목록 밖 기기 = 404(`:262-272`).
- 「태블릿에 보내기」 글자: 앱 `core/reservation_copy.dart:166` = 웹 `reservations_display.html`(「태블릿에 보내기」) 같음.
- 웹과 닮게: 단계 이름 · 진행 줄 글자 · 칸 순서가 웹 템플릿과 같다(`reservation_copy.dart` 줄마다 출처).

### 3. 보안 — PASS(F1 · BW1 ~ BW7 빼고)
- 토큰 = 헤더 `X-Questionnaire-Token` 만 · `Authorization` 안 봄 · 세션 / CSRF 의존성 없음(`public_questionnaire.py:69-98`).
- 응답 머리(성공 · `ServiceError`) · `/q`(`public_pages.py:105` · `web.py:263`) · CSP `script-src 'self'` · 인라인 스크립트 0(`templates/questionnaire.html`).
- 응답 허용 키 6 · KOS id 없음(`schemas/public_questionnaire.py:50-100`) · 제출 본문 extra 금지 + `FORBIDDEN_FIELDS` 한 번 더(`:109-113` · `questionnaire_public.py:288-290`).
- 수명 10분 / 60분 · 새 링크가 앞 것을 canceled(`policies/displays.py:50-68` · `displays.py:276-285`).
- 속도 제한 값 · Lua 미끄럼 창 · 틀린 토큰 10 → IP 막음(`questionnaire_public.py:48-99` · `:170-171`).
- IP = 소켓 · 믿는 앞단(`DAY_EXT_PROXY_HOST`)일 때만 `X-Day-Client-IP`(`ext_peer.py:32-43`).
- 닫기 = canceled 만 · 409 `display_closed` · 행 잠금(`displays.py:346-379`).
- `displayRequestId` = 이 방문 · 이 기기 · scan(`displays.py:458-469`).
- 로그 · 토스트에 여권 · 문진 값 0:
  - 서버는 예외 타입 · id 만 남기고, 스캔 event 는 칸 이름만 남긴다(`passport_scan.py:375-381`).
  - 앱 `lib/scan` · `scan_screen` · `qr_screen` · `display_*` · `ScanChannel.kt` · `PassportScanActivity.kt` · `TextScanner.swift` 에 print · Log · NSLog 0. MRZ 줄은 `kDebugMode` 화면 글자만 쓴다.
  - qrUrl 을 토스트 · 저장에 안 씀(`display_flows.dart:7`).
- 원본 사진 = 메모리만 · 저장 · 다시 찍기 · 닫기 때 버림.

### 4. 조용히 통과하는 자리
- KOS 실패: 여권 고객 수정 실패 = 아무것도 안 남김 503(`passport_scan.py:8-11`) · KOS 사진 실패 = `kosSynced false` + [사진 다시 올리기] · 문진 KOS 실패 = `failed` + [다시 보내기] → PASS.
- 15초 넘김: BW2 · BW3 → **WARN**.
- 푸시 실패: 신호 실패는 로그만, 메우기가 채운다(`notification_events.py` `publish_display`) · 같은 요청 두 번 발송 0(`display_push.py:74-78` · `:96`) → PASS.
- SSE 끊김: 다시 붙으면 메우기(`notification_controller.dart:71`) · QR 화면은 끊긴 동안만 5초 폴링(`qr_screen.dart:107-110`) → PASS.
- 손 입력 · MRZ 체크숫자: 문서번호 · 생년월일 · 만료일 체크숫자가 틀리면 null(「읽지 못함」)이라 조용히 받지 않음(`mrz.dart:135-148`) → PASS. 고치기 · 손 입력은 AW3 · AW4 → **WARN**.
- Android 카메라 권한 거절: 실행 중 요청 → 거절(다시 묻지 않음 포함) = `no_camera` → 손 입력(`ScanChannel.kt:77-91`) → PASS. 카메라 시작 실패는 AW2 → **WARN**.
- **CAMERA 선언 → 차트 · 채팅 카메라(OQ-A91) — PASS(코드 근거)**:
  - `pubspec.lock` image_picker 1.2.4 / image_picker_android 0.8.13+25 는 manifest 에 CAMERA 가 선언돼 있으면 `ACTION_IMAGE_CAPTURE` 전에 권한을 묻는다. 거절은 `camera_access_denied` 다.
  - `app/lib/chat/photo_pick.dart:49` 가 `access_denied` 를 `PhotoDenied` 로 바꾸고, 채팅(`chat_room_screen.dart:158`) · 차트(`chart_photos.dart:135` · `:157`)가 처리한다.
  - 남는 것: 카메라 거절에도 `photoDeniedMessage`(사진 보관함 글자)가 보이는지는 실물에서 볼 것.

### 5. 지은 글자 — PASS
- 앱 `core/reservation_copy.dart` 줄은 모두 웹 템플릿 · SPEC · cc(`launchers.dart` · `qr_show_screen.dart` · `scan_screen.dart` · `settings_screen.dart` · `app_state.dart` · cc 웹 `Display.tsx`)에 있다. 표본 17개를 grep 으로 확인했고(「꺼짐」 = `launchers.dart:53`), 빠진 것은 0이다.
- 문진 6언어 204개 = cc `text.ts` 전부 있음(기계 대조).
- 푸시 「고객 입력 요청」 · 「여권 스캔 요청」 · 「데스크에서 보냈어요」 = cc `back/app/service/push.py` · `api/display.py`.
- app-2 §6 의 비운 자리(종류 고르기 머리 · 스캔 부제 · 사진 줄 · 자리 글)는 짓지 않았다.

### 6. migration · 계층 · 의존성 — PASS
- `migrations/versions/20261125_0029_display_questionnaire_kos.py`: up = 두 칸 null 허용 + enum 만들기 + 칸 3 · down = 칸 지움 → enum 지움 → 빈 글자 채움 → not null 로 되돌림. 대칭이고 `test_alembic` 왕복이 있다.
- 계층: 새 라우터에 `select` · `session.execute` 0(router → service 직접 · repository 층 없음 = AGENTS 규칙). ORM 은 `day` 밖으로 나가지 않는다(`public.py` 는 DTO). 정책 `policies/displays.py` · `questionnaire.py` 는 순수 함수다.
- async 경로에 `time.sleep` · 동기 I/O 0.
- 의존성: AW7 참고.

---

## 사용자 확인 필요(결정 · SPEC 을 다시 열지 않음 — 열려 있는 것)

1. **「국적/통역」**(app-2 §5-8): 웹 템플릿은 `{국적} / 통역필요` 를 그리고, DAY-SPEC-007 U-3 은 「통역필요 안 보임」(OQ-D06)이다. 앱은 템플릿을 따랐다(`reservation_copy.dart:73-74`). 어느 쪽이 정본인지 정해야 웹 · 앱을 같이 맞출 수 있다.
2. **iOS 카메라 문구 여권 용도**(U5 · OQ-A79): `ios/Runner/Info.plist:52-53` 은 D15 문구(채팅 · 차트)뿐이다. 여권 스캔이 들어가면 App Review 에서 「목적 문구 불완전」으로 걸릴 수 있다(이번 E2E 는 시뮬레이터라 막히지 않음).
3. **ML Kit 지표 전송 · 오픈소스 고지**(AW7 · OQ-A89): 출시 전 Play 데이터 보안 · 개인정보 안내.

## 직원이 실물에서 만날 자리

- 고객이 문진 [제출] 뒤 KOS 가 느리면, 30초 뒤 고객 폰에 오류가 뜨는데 웹에는 「제출됨 · 보냄」이 보인다(BW2). 다시 누르면 「이미 제출됨」.
- 갤럭시 탭에서 다른 앱이 카메라를 쥐고 있으면, 받은 [여권 스캔] 화면이 뜨자마자 닫히고 웹 진행 줄이 사라진다(AW2).
- 손 입력 성별에 「남」 · 「male」을 치면 「저장하지 못했어요 · 요청이 올바르지 않습니다」만 나오고 어느 칸인지 모른다(AW3).
- 받은 스캔을 여는 중 네트워크가 끊기면, 웹에는 「{기기}에서 스캔 중 · 촬영 대기 중…」이 오래 남는다(AW5).
- 기기 목록 「접속 중」은 태블릿 연결이 끊긴 뒤 최대 25초 남는다(be-2 §5 — 닿기에는 영향 없음).
- 저장 실패 글자 중 KOS · 저장소 코드(`kos_unavailable` · `photo_disabled` · `customer_not_linked`)는 코드 글자 그대로 보인다(OQ-A7 · 글자 미정).
- Android 최근 앱 화면에 여권 미리보기 썸네일이 남는다(AW1).

## 참고(기존 부채 · 이번 범위 밖)

- `kos_unavailable` 은 앱 `loginMessages` 에만 글자가 있고 `actionMessages` 에는 없다. 그래서 조작 실패에서는 코드만 보인다(`core/copy.dart:8` · `:60`). 로그인 글자가 잘못 섞여 나오지는 않는다(정상).
- QR 화면 1.5초 자동 닫힘 `Timer` 를 `dispose` 에서 끄지 않는다(`qr_screen.dart:129-131` — `mounted` 가 대부분 막음).

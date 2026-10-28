# 리뷰 리포트 — overall-board 앱 판(WORK-009) / code (2026-10-27)

대상: `cc-prototype/overall-board` branch `kknaksss/overall-board-2` 커밋 안 된 변경 전체(`95c64bc` 이후 · 수정 58 + 새 파일) · infra `k8s_infra_mac/overall-board` branch `kknaksss/cc-prototype-app-photo` diff.
기준: SPEC-004 0.4.1 · DEC-007 · WORK-009 · `app-spec-followups.md` #1~#7 · `_RESUME` §2 10-27 앱 줄.

## 판정: FAIL (2건 · 둘 다 한 줄~몇 줄 고침)

## 직접 돌린 검증 수치
| 명령 | 결과 |
|---|---|
| `cd procedure/back && uv run pytest -q` | **444 passed**, 1 warning(starlette httpx 권고) · 26.5s |
| `cd procedure/app && flutter analyze` (fvm 3.44.8) | **No issues found** |
| `cd procedure/app && flutter test` | **97 passed** (All tests passed) |
| `cd procedure/front && npx tsc --noEmit` | 0 오류 |
| `cd procedure/front && npm run lint` | 0 문제 |

> 확인용 프로브 1회: FAIL-1 재현을 위해 `back/tests/` 에 임시 시험 파일 1개를 넣어 돌리고 **곧바로 지웠다**(git status 변화 0 · 원본은 스크래치에 둠). 그 밖 파일 수정 · 사용자 포트 · 시뮬레이터 창 손댄 것 없음.

## FAIL

### FAIL-1 띄우기 푸시가 아예 안 나간다 — `POST /api/display-requests` 가 sync `def` → **고칠 사람: backend**
- `back/app/api/display.py:27` `def create(...)` (sync) → FastAPI 가 threadpool 에서 돌림 → `DisplayService.reach()` → `push.schedule_display()` → `PushService._dispatch()` 의 `asyncio.get_running_loop()` 가 `RuntimeError` → **「띄우기 request=N 푸시 건너뜀(이벤트 루프 없음)」 경고만 · APNs 0 · push_log 0** (`back/app/service/push.py:175-187`).
- 재현(프로브 · APNs 키 있는 설정 · 컨테이너 연결 그대로): 응답 200 · `PUSH_LOGS []` · `APNS_SENT 0` · 경고 1줄. 기존 시험이 못 잡은 이유: `test_app_be3.py:38` 이 `c.display.push` 를 가짜로 바꿔 끼우고, `test_display_wired_push_without_key` 는 키 없음(`_skip` 길 — 루프 필요 없음)만 본다.
- 계약: SPEC-004 §5-3 「기기에 닿기 ②」(SSE 가 닫힌 기기 = 띄우기 푸시). 기존 조작 API 는 전부 `async def`(`api/actions.py` · `api/reservations.py`)라 원장 · 상담사 호출은 문제없음 — 새 경로만.
- E2E 영향: 앱이 뒤에 있거나 SSE 가 끊긴 태블릿에 [태블릿에 띄우기] → 아무것도 안 뜸(앞으로 올 때 pending 으로만 늦게 열림). 같은 이유로 SSE `display` 도 threadpool 에서 `asyncio.Queue.put_nowait` 를 부른다(루프 밖 스레드 — 1초 heartbeat 때까지 늦게 깨는 정도지만 같은 고침으로 함께 사라짐).
- 고침: `display.py` 의 `create` 를 `async def` 로(본문은 그대로 — 동기 DB 호출은 기존 async 경로들과 같은 꼴). 시험: `c.display.push` 를 바꾸지 않고 키 있는 설정에서 `POST /api/display-requests{deviceId}` → `push_log.kind=display` 1행 단언.

### FAIL-2 「카메라 없음 → [손으로 입력] → [저장]」 이 늘 400 — 시뮬레이터에서 여권 저장 길이 없다 → **고칠 사람: 코디 결정 → backend 또는 mobile**
- 앱 `app/lib/screens/scan_screen.dart:110-112 · 145-150 · 163-170`: 카메라 없음(`NoCamera`) → [손으로 입력] → `_photo == null` 인 채 multipart 저장. back `back/app/api/photos.py:40-42` 는 `photo` 없으면 **400 `photo: 사진 파일이 필요해요`**(SPEC §6.16 ④ = `photo` 필수). 앱 · back 이 서로 다른 계약을 보고 있다(mobile 보고서 「이슈」 끝 줄에 적혀만 있고 닫히지 않음).
- 또 카메라 [취소] = 스캔 닫기(`scan_screen.dart:116`)라, 시뮬레이터가 카메라 「있음」으로 열리면(mobile 보고: iPhone 17 시뮬레이터) 손 입력 길로도 못 간다.
- `_RESUME` 10-27 「E2E 먼저 iPhone 시뮬레이터 · 여권 = 손 입력 길 · 견본 사진 주입」 → 지금 코드로는 시뮬레이터 E2E 에서 [여권 스캔] 저장(고객 수정 · identity `app_manual` · 띄우기 done · 웹 「{기기}에서 수신」)을 한 번도 볼 수 없다. 견본 사진을 넣는 길도 앱에 없다.
- 고칠 길(하나 골라 주세요): (a) back — `manual=true` 이고 사진 없으면 허용 · `photo={ccc:"skipped", kos:"skipped"}` · `photoId:null`(followups #6 처럼 enum 하나 더함 · SPEC 후속) / (b) mobile — debug 빌드에만 「견본 사진 넣기」(번들 지어낸 TEST JPEG) + 카메라 취소 → [손으로 입력] 으로 / (c) 코디가 「스캔 저장 E2E = 실기기만」으로 정하고 시뮬레이터 범위에서 뺌(그러면 FAIL 아님 · 앱 [저장] 은 사진 없으면 꺼 두는 게 맞음).

## WARN

- **W1 띄우기 같은 요청이 두 번 열릴 수 있다** — `app/lib/app_state.dart:351-354` `resumed` 마다 `refreshDisplays()` · back `pending` 은 **이미 opened 도 돌려줌**(followups #1) · `enqueueDisplays` 는 지금 큐에 있는 id 만 거름(`app_state.dart:96-100`) — 지금 화면에 떠 있는 요청은 이미 `takeDisplay()` 로 빠져 있어 다시 들어간다. 카메라 권한 창 · 알림 센터 내림 · 잠깐 백그라운드 → 화면이 끝난 뒤(이미 done) **같은 스캔/문진 화면이 한 번 더 열림**. 고침: 열고 있는 `requestId` 를 기억해 거르거나, `openDisplay` 직전에 상태를 다시 확인. (mobile)
- **W2 `procedure/.env.example` 에 `CCC_COUNSELOR_ID · _PASSWORD · _KOS_ACCOUNT_ID` 이름 없음** — SPEC-004 §2.3 표 · WORK-009 WP-INFRA. infra 는 BE1 몫으로 넘기고 BE1 은 「infra 쪽 확인」으로 넘겨 둘 다 안 넣음(`app-infra-report.md` §1 · `app-backend-report.md` 전체 요약). infra Secret 예시에는 있음. 로컬 compose E2E 에서 상담사 계정을 쓰려면 코디가 `.env` 에 넣어야 함. (backend 또는 코디 · 한 줄)
- **W3 알림 목록 항목 누름 = `ids` 아닌 `reservationId`/`callId` 로 읽음** — `app_state.dart:179-181` 이 목록 항목도 `PushTap` 으로 바꿔 `readNotificationOf` 를 부름. SPEC §5-4 「목록 항목을 누르면 그 id 를 읽음」. 결과는 같은 발송 행을 읽으니 화면상 차이 거의 없음(같은 예약에 상담사 호출이 여러 번이면 한꺼번에 읽음). (mobile · 낮음)
- **W4 front `npm audit` critical 1 · Next 16.4.0 보안 권고**(`app-fe-report.md` 이슈 4) — 이 판 범위 밖 · 기존 부채로 넘김 결정 필요.

## 볼 것별 결과

### 1. 계약 일치(back ↔ app ↔ front)
| 항목 | 결과 |
|---|---|
| 경로 50 = HTTP 49 + WS 1 | 같음(`back/tests/test_order.py:246` `test_route_count_50` 통과) |
| 새 경로 15 — app `lib/api/api.dart` · front `lib/api.ts` 가 부르는 경로 · 메서드 | 같음(devices · targets · display-requests 4 · notifications 4 · questionnaires 2 · unlock · passport-scan · id-photos 2) |
| SSE — `board` 만 `id:` + version · `notification`/`display` 는 `id:` 없음 · 계정/기기 단위 | 같음(`back/app/service/stream.py:20-75` · app `sse/board_stream.dart` · `display_test`) |
| 푸시 payload — `doctor_call{visitId,callId}` · `counselor_call{reservationId}` · `display{requestId}`(sound 없음) | 같음(`back/app/service/push.py:113-147` · `app/lib/push/push.dart:23-41` · `AppDelegate.swift` onTap 키 5) — 단 display 는 FAIL-1 로 안 나감 |
| followups #1 pending · claim 항목 | 같음(`service/display.py:39-42` ↔ `model/display.dart`) |
| #3 읽음 본문 `ids?·callId?·reservationId?` · `{ok,read}` | 같음 |
| #4 `target.callId` | 같음 |
| #6 스캔 `photo.kos = skipped` | 같음(`scan_screen.dart:373`) |
| #7 `identity.photoKos` | 같음(back `schemas/reservations.py` · front `Display.tsx`) |
| #2 · #5 문진 prefill | 보류 코드(아래 「다음 판 정리 목록」) |
| QR 내용 `ccc://display?t=` | 같음(front `lib/api.ts:148` ↔ app `model/display.dart:40-46`) |

### 2. 회귀
- 시술 현황: board 이벤트는 모든 연결 그대로 · 앱 시술 현황 탭 = 기존 화면 + 2계층(시험 통과). 웹 시술 현황 · 예약 현황: front 변경은 `DetailModal.tsx` 12줄 + 새 `Display.tsx` · `lib/api.ts` · `types.ts` · `session.ts`(역할 하나) — 다른 화면 안 건드림.
- 원장 호출 푸시: payload 에 `kind:"doctor_call"` 만 더함 · 받는 사람 규칙 그대로(`push.py:89-121`) · 옛 앱 빌드는 `kind` 없음 = doctor_call.
- `push_log` 다시 만들기: `back/app/repository/db.py:233-250` — `PRAGMA table_info` 로 `call_id NOT NULL` 일 때만 · 한 트랜잭션(새 표 → 옛 행 복사 `kind=doctor_call` → DROP → RENAME) · 멱등. 시험 `test_app_be1.py:162` 옛 모양 DB 에서 행 보존 확인. **운영 DB 데이터 보존 = OK**(배포 직후 1회 `push_log` 행 수 비교 권장).

### 3. 보안 · 개인정보
- 사진 열람 = Bearer 헤더만(`api/deps.py:17-21` · 쿼리/쿠키 없음) · `Cache-Control: no-store` · 열람마다 `event_log(id_photo_view)`. 파일 이름 = `secrets.token_hex(16).jpg`(고객 값 0).
- 사진첩 저장 0: 앱 · Swift 에 사진첩 · 임시 파일 · path_provider 쓰기 없음(grep) · `NSPhotoLibrary*` 키 없음 · `NSCameraUsageDescription` 만. back multipart 는 spool 한도를 올려 메모리에서만.
- 주민번호 0: 앱 문진 제출 본문에 `registrationNumber` 없음 · back 400 `questionnaire_field`.
- 법적 검토 주석: back 9 · app 6 · front 1 = 16곳(① ~ ⑤ 자리 다 있음) + infra PVC 머리 · back.yaml · compose.
- 띄우기: QR = `token_urlsafe(32)` · DB 엔 sha256 만 · claim 1회(409 `display_closed`) · 만료 10분(409 `display_expired`) · `deviceId` 남의 계정/없는 id = 404 `device_not_found`(pending · claim · unlock · 문진 · 스캔) · SSE 는 무시.
- 로그: 새 로그 줄에 값(이름 · 여권 · 토큰) 없음 · 토큰은 끝 6자리만. 레포 새 코드에 24자 16진(KOS id) 0. 워커 리포트 실값 없음(지어낸 견본 · `[ccc 시험]` 만).

### 4. 앱 상태 · 알림 · 버튼
- `app/lib/view/state.dart` = 웹 `reservations/view.tsx` `MAIN_NAME · SUB_NAME · MAIN_TONE · phaseStyle · barStyle · headOf` 값 하나씩 대조 — 같음(귀가 대기 gray-600 / 완료 gray-300 막대 · 머리 gray-400 · 부도 외곽선 · done/none 칩 회색).
- 알림 종류 둘만(`doctor_call` · `counselor_call`) · display 는 목록 · 설정 밖.
- [수납하기] · [처방전 출력] · [리포트 QR 전송] 버튼 없음 — 정산은 글자만(`reservation_detail_screen.dart` grep).

### 5. infra
- PVC `procedure-photos` 1Gi RWO local-path · `resource-policy: keep` · 머리 주석에 법적 검토 + 암호화 안 되는 근거 · `enabled=false` 면 PVC · 마운트 · env 다 빠짐.
- env: `PROC_PHOTO_DIR=/photos` = ConfigMap(Secret 예시 「NOT here」 목록에 추가) · Secret 예시에 `CCC_COUNSELOR_*` 3개 이름만.
- compose: `PROC_PHOTO_DIR: /photos` · 이름 있는 볼륨 `procedure-photos`.
- Dockerfile: `mkdir -p /data /photos && chown app:app /data /photos`(uid 10001 쓰기) — k8s 는 `fsGroup: 10001` 로도 됨. OK.
- `kubectl apply --dry-run` 은 아직(infra 워커 머신에 kubeconfig 없음) — 배포 전 코디 · 사용자.

## 고객이 실물에서 만날 자리
- 데스크가 [태블릿에 띄우기] 를 눌렀는데 태블릿 앱이 뒤에 있으면 아무 알림도 안 옴(FAIL-1).
- 스캔/문진 화면이 끝났는데 같은 화면이 한 번 더 열림(W1) — 고객 앞 태블릿에서 「또 뜬다」.
- 시뮬레이터 · 카메라 없는 iPad 에서 [손으로 입력] → [저장] = 「저장하지 못했어요 · photo: 사진 파일이 필요해요」(FAIL-2).

## 다음 판 정리 목록(문진 → 고객 웹 페이지 · 10-27 — FAIL 아님)
- APP5 앱 문진 화면 전체(`screens/questionnaire_screen.dart` · `model/questionnaire.dart` · `l10n/questionnaire_text.dart` · `test/questionnaire_test.dart`) · `launchers.dart` [이 기기에서 열기] · `kind:"questionnaire"` 띄우기 길 → 앱은 QR 만 보여 주는 화면으로.
- BE4 `api/questionnaire.py` · `service/questionnaire.py` · `POST /api/auth/unlock` · `domain/languages.py` — 고객 웹 페이지(로그인 없는 토큰 링크)에서 재사용할 부분(KOS 양식 · 제출 · 언어 표)과 지울 부분(unlock · 앱 `deviceId` 확인) 가르기. 경로 수 50 이 바뀜.
- followups #2(`prefill.dateOfBirth = yyyyMMdd`) · #5(`prefill.phone`) 는 고객 웹 계약으로 옮김.
- 문진 질문 「필수」 키 이름(`required`·`isRequired`·`essential` 추정) — 실제 KOS 양식으로 확인.

## 참고(기존 부채)
- 동기 엔드포인트에서 `hub.publish()` 등 asyncio 큐를 다른 스레드에서 건드리는 꼴은 이번 새 경로(`display.create`)에서만 보임 — 기존 조작 API 는 async.
- `MultiPartParser.spool_max_size` 를 모듈 전역으로 바꿈(`api/photos.py:21`) — 앱 안 multipart 경로가 이것 하나라 지금은 무해.

# 리뷰 리포트 — day-app-re1 / doc (2026-11-25)

- 워커: day `reviewer_doc` · task `task_374b6f37d593` · dispatch `ctx_60077edbb60b` · read-only
- 대상: `/Users/kknaks/orca/workspaces/mediness-mediness/day-app-re1-spec` 미커밋 변경(`git diff origin/main` · base `b152d463`) — `products/day/20-spec/spec-003-mobile-app.md`(개정 ㉑) · `spec-002-procedure-board.md`(개정 ㉚) · `20-spec.md` · `10-decision.md` · `log.md`(5 파일 +271 −30)
- 대조 기준: 코디 `day-app-re1/_RESUME.md` §2(범위 = 차트만 · D1 ~ D11) · `research-1-report.md` §2 28행 · `chart-photo-decisions.md` C1 ~ C36 · 코드 CENTURION_DAY `55e60aa4`(`git show` 만)
- 줄 번호 = 작업 트리 파일 기준(SPEC-003 = `S3:` · SPEC-002 = `S2:`)

## 판정: WARN

FAIL 없음. 결정 D1 ~ D11 · 범위 · 28행 처분 · 웹 결정 C 번호 · 코드 사실은 맞는다. 범위 밖 항목(여권 스캐너 · 문진 QR · 예약 탭 · 사진 대상 확장 · 웹 동작 / 권한 변경 · migration)은 하나도 안 들어왔다. lint `--strict` = **exit 0 · 0 error · 263 warning · `products/day/` 0 / 0**(263 은 전부 다른 제품 기존 WARN — 무관).

WARN 7건 — 그중 **W1(iOS 뒤로 가기 밀기)** 과 **W2(JSON 요청 null 칸)** 는 mobile · backend 워커가 되물을 자리라 WORK 전에 고치는 편이 낫다. 나머지는 표기 · 잔재.

---

## FAIL

없음.

## WARN

### W1. iOS 가장자리 밀기 = 「확인 창」은 Flutter 기본 동작으로는 안 된다 — 구현 가능성

- 위치: `S3:576`(닫기 표 「뒤로 가기(iOS 가장자리 밀기 · Android 뒤로) | 닫힘 | 확인 창」) · `S3:1219` A-55 「미저장이면 [✕] · 뒤로 가기 = 확인 창 … 미저장 없으면 [✕] · 뒤로 가기 = 바로 닫힘」
- 근거: Flutter 의 iOS 뒤로 밀기(`CupertinoPageRoute` 계열)는 route 의 `popDisposition == doNotPop`(= `PopScope(canPop: false)`) 이거나 `fullscreenDialog` 이면 **제스처 자체가 꺼진다** — 밀어도 `onPopInvoked` 가 오지 않아 확인 창을 띄울 시점이 없다. Android 뒤로는 `onPopInvokedWithResult` 로 확인 창을 띄울 수 있다. 아이패드 가운데 창(dialog)엔 밀기 제스처가 없다. (프레임워크 동작 기준 판단 · 앱 코드에 이 패턴의 선례 없음 — 채팅 `showAppSheet(busy:)` 는 `PopScope(canPop: !busy)` 로 **막기만** 한다 · `app/lib/chat/chat_kit.dart:403-438`)
- 결과: A-55 의 iOS 몫이 TestFlight 에서 그대로는 통과 못 하고, mobile 워커가 「밀면 확인 창을 직접 만든 제스처로 띄울지 · 막기만 할지」를 되묻는다.
- 고칠 방향: 닫기 표를 「Android 뒤로 = 확인 창 · iOS 가장자리 밀기 = 미저장이면 막힘(아무 일 없음) · 미저장 없으면 닫힘(폰 전체 화면을 밀 수 있는 route 로 띄울 때)」로 나누거나, iOS 몫을 OQ(기본값 = 막힘)로 둔다. A-55 문장도 같이. D6 의 「확인 창」은 ✕ · Android 뒤로에 그대로 살아 있어 결정은 안 열림.

### W2. 탭 저장 JSON 요청 — null · 빈 값 칸이 안 닫힘 — 구현 가능성

- 위치: `S2:690`(JSON 짝 표 「요청」 = `{chart, rows: [{taskId, body, staffId, baseLogId, baseBody, baseDoctorStaffId}]}`(칸 뜻 = 위 표 웹 폼 칸))
- 근거: 웹 폼은 빈 문자열로 「없음」을 보낸다(`routers/board.py:440-462` `_chart_rows` — `staffId` · `baseLogId` · `baseDoctorStaffId` 가 빈 값이면 `None`). JSON 에선 `null` 인지 `""` 인지 · 칸 생략을 받는지가 안 적혀 있다. `staffId` 없음은 서비스가 409 `chart_staff_required` 로 내야 하므로(`services/board_charts.py:240-242`) 400 `invalid_request` 로 먼저 튕기면 계약이 어긋난다.
- 고칠 방향: 한 줄 — 「`staffId` · `baseLogId` · `baseDoctorStaffId` = uuid 또는 `null`(빈 값 대신) · `baseBody` = 문자열(빈 문자열 허용) · 칸 생략 = 400 `invalid_request`(앱 `/api` `extra=forbid` 관례)」 같은 꼴. 이름 제안 수준이면 OQ-99 기본값에 넣어도 된다.

### W3. 「읽기 전용」 잔재 — 살아 있는 문장 2곳

grep 전수(「읽기 전용 · 읽기만 · 차트 API 를 부르지 않 · 차트 경로를 부르지 않 · 앱 경로 없음 · 웹만 · 차트(읽기) · 차트 = 읽기 · 부르지 않는다」): SPEC-003 15곳 · SPEC-002 22곳. 대부분은 취소선 안 · 역사 기록 · 보기 권한 뜻(「보기 권한이면 읽기만」 `S3:562` · `S3:991` · `S3:1114` · `S2:449`) · 다른 기능(귀가 대기 취소 「웹만」 `S2:647` 등)이라 문제없다. 남은 것:

- **`S3:677`** 소비 기준 — 「그 브랜치가 더한 `GET /api/board/search` · `GET /api/visits/{id}/chart` · `POST /api/tasks/{id}/doctor` 는 1차 앱이 부르지 않는다(§1 「뺌」) — ~~`POST …/doctor`~~(0.2.0) · ~~`GET …/chart`~~(개정 ㉑ 로 부름)」. 「부르지 않는다」 문장 본문은 살아 있고 취소선은 **뒤에 덧붙인 경로 이름**에 걸려 있어, 이 SPEC 관례(뒤집은 문장 자체를 긋고 날짜 · 사유)와 반대로 읽힌다. → 문장 안의 `GET /api/visits/{id}/chart` 를 그어 「~~…~~(2026-11-25 개정 ㉑ — 부름)」으로.
- **`S3:1299`** OQ-A34 질문 칸 「앱은 차트 API 를 부르지 않으므로 …」 — 답 칸이 「닫음」이라 뜻은 닫혔지만 질문 칸이 지금 사실처럼 남는다. 같은 표의 OQ-A35 는 질문 칸까지 그었다. → 질문 칸도 취소선 또는 「(개정 ㉑ 전 사실)」 꼬리.

### W4. `chart_too_long` 을 JSON 짝 오류 코드로 「나가는 것」처럼 적음

- 위치: `S2:698`(400 `… · chart_too_long`(제안)) · `S3:567`(「`chart_too_long` = 글자 미정(SPEC-002 OQ-90)」)
- 근거: 웹 매트릭스 `S2:833` 은 「**자리만 · 한도가 정해지면 연다** … 그때까지 DAY 는 길이 검사를 하지 않는다」. 코드에도 `CHART_TOO_LONG` 코드가 없다(`backend/common/error_codes.py` · `services/board_charts.py` grep 0).
- 고칠 방향: 두 곳에 「(자리만 — 지금 서버는 보내지 않음 · `S2:833`)」 꼬리. backend 워커가 새 코드를 만들지 않게.

### W5. 「최근 저장」 시각 = 「기기 시간대」 — 원천 없음 · 웹과 다름

- 위치: `S3:558`(「시각만 · **기기 시간대** · 없으면 안 보임」)
- 근거: 웹 E58 은 `day_hm` = **병원 시간대** `HH:MM`(`backend/day/web.py:103-106` `hm` · `board_chart_parts.html:36`). 결정 · 웹 SPEC 어디에도 「기기 시간대」가 없다. 병원 · 기기가 같은 KST 라 실물에서 다를 일은 드물지만 「웹과 같은 기능」이 목표인 개정에서 근거 없는 갈래다.
- 고칠 방향: 앱의 다른 시각 표시(「마지막 종료 HH:MM」 U-4)와 같은 규칙을 가리키거나, 「기본값(planner 제안)」 표시를 붙인다.

### W6. 사진 올리기 흐름 「카메라 · 앨범 중 고름 · 카메라 = 한 장 찍어 바로 올림」 — 기본값 표시 없음

- 위치: `S3:586`
- 근거: 결정 D1 · C28 은 「여러 장 올리기」까지만 정한다. 웹은 파일 고르기 하나(`board_photos.html:39-43`). 고르기 화면 모양은 OQ-A73 으로 열어 뒀는데, 「카메라 / 앨범 두 갈래 · 카메라는 바로 올림(확인 단계 없음)」은 계약 문장으로 들어가 있다. 화면 글자 발명은 아니어서 FAIL 아님(카메라 / 앨범 글자는 OQ-A78 로 비움).
- 고칠 방향: 이 문장을 OQ-A73 기본값으로 옮기거나 문장 끝에 「기본값(planner 제안 · OQ-A73)」.

### W7. A-38 고친 문장이 여전히 틀린 사실을 품음(기존 부채가 이번 편집으로 다시 살아남)

- 위치: `S3:1202` — 고친 결과 = 「… · 담당 원장 바꾸기 · 서버 검색 ~~· 차트 API 호출 0건~~(…) 호출 0건」
- 근거: 0.2.0 개정 ⑲ U-22 로 앱은 `POST /api/tasks/{id}/doctor` 를 부른다. planner 는 OQ-A62(다음 cut 정리)로 남겼다고 보고(planner-1 「못 고친 앞 판 문장」). 그러나 이번 편집으로 문장 꼬리가 「담당 원장 바꾸기 · 서버 검색 … 호출 0건」으로 재조립돼 TestFlight 검수자가 그대로 읽으면 U-22 와 부딪친다.
- 고칠 방향: 「담당 원장 바꾸기」도 같은 자리에서 「~~담당 원장 바꾸기~~(0.2.0 개정 ⑲ U-22 로 부름)」 한 번 긋기(한 단어 · 범위 안 정리). 그대로 두려면 「참고(기존 부채)」로 코디 판단.

---

## 1. 결정 D1 ~ D11 · 범위 → SPEC 반영

| 결정 | SPEC 자리 | 판정 |
|---|---|---|
| 범위 = 차트만 · 여권 스캐너 · 문진 QR · 예약 탭 = WORK-002 | `S3:236`(넣음 표 차트 행) · `S3:254-255`(뺌) · `20-spec.md:52` · 개정 머리글 `S3:83` | 반영 |
| D1 사진 탭 | `S3:557` 탭 셋 · `S3:583-593` 사진 탭 · A-57 ~ A-59 · `S2:455` | 반영 |
| D2 탭별 [저장] + 「최근 저장」(C2 ~ C4) | `S3:558` · `S3:563-569` · A-53 | 반영(시간대 = W5) |
| D3(「시안 없음」 행) 폰 전체 화면 · 아이패드 가운데 창 | `S3:146` · `S3:222-237` Wireframe(예시 표시) · `S3:555` · A-51 · OQ-A66 | 반영 |
| D4 세션 Navigator | `S3:146` · `S3:554` · A-51 | 반영 — `_sessionNav` 실재(`app/lib/ui/shell.dart:106`) |
| D5 담당자 = `doctor_picker.dart` 재사용 | `S3:560` · A-56 · OQ-A67 | 반영 |
| D6 미저장 확인 창 · 끌어 내림 · 바깥 누름 안 닫힘 | `S3:571-582` 닫기 표 · 매트릭스 · A-55 · OQ-A70 · A71 | 반영 — iOS 밀기 몫 구현 불가(W1). 「미저장 없을 때도 늘 안 닫힘」 해석은 OQ-A71 로 기록됨 |
| D7 새 `/api` JSON(웹 HTML 경로 안 넓힘) | `S3:683` §3 · `S3:686-702` · D-7 `S3:1151` · `S2:653-670` 표 앱 칸 · `S2:686-704` | 반영 — 요청 null 칸(W2) |
| D8 사진 대상 = 웹 그대로 | `S3:592` · `S2:686` · `S2:1385` 표 · 10-decision | 반영 |
| D9 까만 줄 = 테마 · 탭바 겹침 = 같은 탭 Navigator 시트도 | `S3:597-598` · A-52 · OQ-A76 · A77 | 반영 — 줄 근거 맞음(`doctor_picker.dart:83` 팝오버 · `:93` 시트 · `room_screen.dart:742` 창 · `:753` 시트 · `interpret_widgets.dart:160 · 194`) |
| D10 iOS 권한 문구 그대로 | `S3:1043` · A-17 `S3:1180` · OQ-A64 · 10-decision | 반영 — 문구 발명 없음 |
| D11 값 원천 = `GET /api/visits/{id}/chart` | `S3:594` · `S3:686-702` · A-38 · A-51 · OQ-A30 · A34 | 반영 — 경로 · 인증 실재(`routers/api/board.py:149-161` `current_session` · `board` view · `ChartResponse` 에 `base` 있음 `schemas/board_responses.py:554`) |
| C7 권한 그대로 | `S3:595` · 매트릭스 · A-60 · `S2:1385` | 반영 — A-60 「코디 · 상담 = 보기만」은 `S2:724` 직무 표와 맞음 |

## 2. 웹 기능 28행 처분 (`S3:1104-1133`)

28행 전부 있음 · 빠진 행 0. 27 넣음 · 1 웹 전용(#4 [고객 차트] — 앱에 고객 차트 화면 없음 · 범위 = 차트만) + #1 의 누른 시술 강조(`sec`)만 웹 전용(OQ-A63). 둘 다 결정과 어긋나지 않는다(범위 = 차트만 · 강조는 결정 없음 → OQ). 연구 표 #1 ~ #28 과 행 번호 · 기능 이름 1:1 확인.

## 3. 「읽기 전용」 잔재 — W3

살아 있는 문장 2곳(`S3:677` · `S3:1299`). 나머지는 취소선 · 역사 · 다른 뜻.

## 4. 발명 검사

- 화면 글자: 쓴 글자는 전부 원천 있음 — 「최근 저장 : 」 · 「저장」(E57 · E58) · 「저장하지 않고 닫을까요?」 · [계속 쓰기] · [버리고 닫기](E59 — SPEC-002 U-14 · OQ-79 「웹도 사용자 확인 전」을 그대로 적음) · 「사진을 삭제할까요?」 [취소] [삭제](C26) · C27 · C29 · C36 글자(코드 `routers/board_messages.py` 와 일치) · 「시술 전」 · 「시술 후」(`policies/photos.py` `TITLES`) · 직군 「간호」 · 「피부관리」 · 「원장」(`board_chart_parts.html:20` `JOBS`) · ✕ 접근성 「닫기」(`chart_sheet.dart:51`). 탭 글자 · 드로어 머리 · 사진 버튼 · 카메라/앨범 글자는 비우고 OQ(A65 · A67 · A78) — 맞음.
- iOS 권한 문구: 없음(D10 · OQ-A64) — 맞음.
- 정책: 「앱 백그라운드 = 10초 확인 멈춤」 · 「고르는 · 올리는 중 회차 건너뜀」은 웹 `day.js` `photosShown`(`document.hidden`) · `photosBusy` 와 같아 근거 있음. 「세션 끝 = 확인 창 없이 닫힘」은 지금 셸 규칙(`shell.dart:165` `popUntil`). OQ-A63 ~ A78 기본값은 전부 「기본값(planner 제안 · 코디 확인 전)」 표시 — 허용.
- 근거 약한 계약 문장 2건: W5(기기 시간대) · W6(카메라 / 앨범 갈래).

## 5. 범위 검사 — 통과

여권 스캐너 · 문진 QR · 예약 탭 = 뺌 표로만(`S3:255`). 사진 대상 규칙 = 규칙 23 그대로. 웹 경로 · 웹 동작 · 권한 키 · 직무 표 무수정(`S2` 의 웹 칸 · 규칙 23 · 31 · 39 본문 diff 없음). migration = 없음(`S2:1407` · `S3:1134`) — 같은 service · 같은 칸이라 맞음. Caddy 한 줄은 배포 설정(D-7 · `S2:699`) — 「같은 동작의 두 번째 경로」로 C33 을 넓히지 않음.

## 6. 구현 가능성 — 앱 `/api` 짝 · 코드 사실

| 스펙이 기대는 사실 | 코드(`55e60aa4`) | 판정 |
|---|---|---|
| 같은 service — `board.save_chart_tab` · `visit_photos.list_photos/upload/delete/retry/open_file/open_tab` · `visit_photo_import.request_import/wait_imported` | `services/board_charts.py:189` · `visit_photos.py:114 · 164 · 362 · 463 · 501 · 593` · `visit_photo_import.py:107 · 133` · 웹 라우터가 `board.save_chart_tab` 로 부름(`routers/board.py:489`) | 맞음 · 세션 종류 무관(`CurrentSessionData` 만) |
| 충돌 = 409 + `details.conflicts` | 서비스는 충돌을 예외가 아닌 `status = "conflict"` 결과로 돌려줌(`board_charts.py:236-238`) · 공용 본문에 `details` 칸 있음(`common/http_contracts.py:18-20` · `errors.py` `public_details`) | 가능 — JSON 라우트가 409 본문을 직접 만들면 됨 |
| 오류 코드 `chart_staff_required` · `staff_not_listed` · `doctor_not_listed` · `photo_type` · `photo_too_large` · `photo_disabled`(409 · 503) · `session_expired`(직원 토큰 없음) | `error_codes.py` 실재 · `board_charts.py:240-250` · `errors.py:313-316` · `visit_photos.py:87-94 · 123-134` | 맞음 · `chart_too_long` 만 없음(W4) |
| 사진 오류가 `/api` 에서 공용 모양 | `PhotoError` = `ServiceError` → 전역 `_service_error_handler`(`runtime/main.py:47-49 · 65`) | OQ-100 기본값과 같은 방향(코드 읽기 기준 · 확인은 WORK) |
| 사진 목록 값 = `photos_view` · `title` = `TITLES` · 빈 묶음도 늘 | `presentation/photos.py:10-33` | 맞음 |
| 토스트 「 · 」 이어 붙임 | `routers/board_photos.py:77-84` `_message` | 맞음 |
| 100MiB 서버 쪽 `BODY_MAX_BYTES` | `routers/board_photos.py:51` | 맞음 |
| 파일 머리 `no-store` · `inline` · `nosniff` | `routers/board_photos.py:52-56` | 맞음 |
| 앱 위젯 — `doctor_picker.dart` · `room_screen.dart:583-587` · `chart_sheet.dart:57` TabBar · `chat/photo_pick.dart` · `chat/screens/chat_photo_screen.dart` · `chat/widgets/chat_media.dart` · `core/copy.dart`(`chart_conflict` 뺌 · `unsetActionCodes` 에 `chart_staff_required` · `staff_not_listed`) · `test/core/board_messages_contract_test.dart` · `ui/theme.dart` | 전부 실재 · 줄 번호 맞음 | 맞음 |

남은 빈칸: W1(iOS 밀기) · W2(null 칸). 착수를 막는 OQ 는 없음 — OQ-A63 ~ A78 · OQ-99 · 100 모두 기본값 있음 · 「막는 것」 칸 = OQ-A64(정식 출시 심사)만.

## 7. 인수 조건 A-51 ~ A-60 · 미저장 닫기 경로

- A-51 ~ A-60 은 「누가(단위 ✓ / iPhone · iPad · dev · KOS 데모) · 무엇으로」가 칸으로 있어 실기기 · TestFlight 에서 확인 가능한 문장이다. A-57 「앱 백그라운드 = 요청 0」은 서버 로그로 확인 가능.
- 닫기 경로 4개(✕ · 뒤로 가기 · 끌어 내림 · 바깥 누름)는 D6 과 맞다. 단 iOS 가장자리 밀기 몫이 구현 불가 — W1.
- 폰 = 전체 화면이라 「끌어 내림」은 시트로 띄울 때만 생기는 길이다(전체 화면 route 엔 기본으로 없음) — 표에 있어도 해롭지 않음.

## 8. 지도 · 결정 · 로그 · 번호 · lint

- 개정 번호: SPEC-003 앞 판 마지막 ⑳ → ㉑ · SPEC-002 앞 판 마지막 ㉙ → ㉚. SPEC-002 머리글 순서(①~⑦ 오름 · 그 뒤 최신이 위)에 맞게 ㉚ 이 ㉙ 위(`S2:49`).
- `20-spec.md:41 · 42 · 51 · 52` · `10-decision.md:39` · `log.md:17` — 셋 다 「SPEC-003 개정 ㉑ · SPEC-002 개정 ㉚ · D1 ~ D11 · migration 없음 · escalation 없음」으로 서로 맞음. 10-decision 이 가리키는 DAY-ESC-001 · SPEC-002 OQ-95 실재. 참조 OQ(SPEC-002 OQ-79 · 80 · 82 · 87 · 88 · 90 · 97 · SPEC-003 OQ-A7 · A12) 전부 실재.
- frontmatter `last_updated` 둘 다 2026-11-25 · `status: stable` 그대로(앞 개정 관례 · 머리글에 「코드 미반영」 기준선 주의 있음).
- `python3 scripts/lint-pipeline.py --strict` → **exit 0 · 0 error · 263 warning** · `products/day` 줄 0. 263 은 전부 다른 제품(selly 등) — 무관.
- 참고(사소): 같은 결정 파일을 SPEC-003 frontmatter 는 `day-app/reference/2026-11-24-day-picture/chart-photo-decisions.md`, SPEC-002 는 `시술현황-차트/reference/…` 로 가리킨다. 실제 파일은 `kknaks_profile/day-app/reference/…`. 링크 깨짐은 아니나(외부 경로 · lint 대상 아님) 한쪽으로 맞추면 찾기 쉽다.

---

## 사용자 확인 필요 (결정을 다시 열지 않고 따로 묶음)

1. **D6 해석** — 미저장이 **없을 때**도 바깥 누름(아이패드) · 끌어 내림으로 닫히지 않게 했다(웹은 미저장 없으면 바깥 누름으로 닫힘 · U-14). planner 가 OQ-A71 에 차이를 기록. 의도대로인지 한 번 확인.
2. **W1 과 묶어** — iOS 에서 미저장일 때 가장자리 밀기는 「막힘(아무 일 없음)」으로 두는 것이 Flutter 기본이다. 「밀면 확인 창」이 꼭 필요하면 직접 만든 제스처라 공수가 든다.
3. **OQ-A65 탭 글자** — 기본값 = 웹 글자 셋(「간호관리차트」 · 「의사차트」 · 「시술전후사진」). 앱 지금 글자(띄어 씀)와 다르다.
4. **OQ-A76** — D9 는 폰 시트 둘만 말했는데 기본값이 아이패드 팝오버 · 창까지 세션 Navigator 로 옮긴다. 아이패드 원장 고르기 팝오버는 지금 「덮개 없음 — 판이 보인다(F1)」(`doctor_picker.dart:88`)라 옮겨도 덮개는 투명 그대로인지 함께 확인.
5. **OQ-A64 · D10** — 정식(prod) 심사 전에 시술 사진 용도 권한 문구가 필요하다(지금 문구는 「채팅으로 보낼 …」).

## 직원이 실물에서 만날 자리

- 폰 차트가 전체 화면이 되면서 하단 탭바가 가려진다 — 「차트에서 다른 메뉴로 바로 못 간다」는 첫 반응이 나올 수 있다(D3 · D4 의도대로).
- 미저장이 없어도 아이패드 창 바깥을 눌러 닫히지 않는다(웹과 다름 — 위 1).
- 보기 권한 직무(코디 · 상담)는 차트를 열어도 글 칸이 읽기만 · 사진 올리기 없음 — 「왜 못 써요」 문의 예상(C7 그대로).
- 「최근 저장」 시각은 병원 · 기기가 다른 시간대일 때만 웹과 달라질 수 있다(W5).

## 참고(기존 부채)

- A-38 「담당 원장 바꾸기 … 호출 0건」(0.2.0 이후 사실과 다름) — W7 · OQ-A62(다음 cut 정리).
- `chart_sheet.dart:19` · `doctor_picker.dart:85` 주석 「세션 Navigator 에 묶는다」는 실제로 탭 Navigator(`useRootNavigator: false`) — 코드 주석 몫(WORK 에서 같이 정리).

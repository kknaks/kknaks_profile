# 리뷰 리포트 — day-app-re1 / code (2026-11-25)

대상: CENTURION_DAY `kknaksss/day-app-re1` 커밋 `43ba40a3`(= `git diff 55e60aa4..43ba40a3` · 35 파일 +3410 −119) — #281 backend · #282 mobile.
방법: read-only 정적 대조다. 테스트·시뮬레이터는 돌리지 않았고, 실행 수치는 워커 보고(be-1 · app-1)를 인용한다. 원천은 delivery-1-report 계약 C0 ~ C3, SPEC-002 ㉚, SPEC-003 ㉑ U-23 · A-51 ~ A-60, `_RESUME.md` §2 D1 ~ D15 · D6′.

## 판정: WARN (FAIL 0 · WARN 9 · 사용자 확인 필요 2)

막는 것은 없다. C2 · C3 경로 · 요청 · 응답 · 오류 코드 · 권한은 백과 앱이 같은 이름 · 같은 모양이다. 새 라우터는 웹과 같은 service 를 부르고, 웹 쿠키 전용 GET 도 그대로다. 닫기 표 다섯 길, Info.plist(D15 바이트 일치), 까만 줄(D9)도 SPEC 과 같다. 남은 것은 아래 세 갈래다.

- 시뮬레이터에서 사람 눈에 걸릴 자리
- 「조용히 통과」에 가까운 테스트 몇 곳
- 사용자 확인이 필요한 길 둘: 푸시 · 채팅 배너가 미저장 차트를 확인 없이 닫는 길, 카드가 판에서 빠진 뒤 남는 시트

---

## 1. 계약 대조 (C0 ~ C3) — 줄 단위

| 항목 | 백 | 앱 | 결과 |
|---|---|---|---|
| C2 경로 · 권한 | `POST /api/visits/{id}/chart` · `board` edit (`backend/day/routers/api/board.py:187-212`) | `'$_base/chart'` POST (`app/lib/state/chart_controller.dart:164-166`) | 같음 |
| C2 요청 | `ChartTabBody{chart: Literal, rows}` · `ChartRowBody` 6칸 필수 · uuid 칸 `None` 허용 · extra=forbid (`backend/day/schemas/board.py:76-115`) | `{taskId, body, staffId, baseLogId, baseBody, baseDoctorStaffId}` 6칸을 늘 보냄 · 간호관리 탭 `baseDoctorStaffId=null` · `baseBody = base.body ?? ''` (`chart_controller.dart:148-159`) | 같음 |
| C2 `staffId=null` → 409 | 서비스까지 감 → `CHART_STAFF_REQUIRED` (`services/board_charts.py` save_chart_tab) · 테스트 `test_board_api_chart_photos.py:157` | 빈 담당자도 그대로 보냄 → `chartSaveMessage` 「담당자를 선택해 주세요」 | 같음 |
| C2 200 | `{saved, lastSavedAt, tasks[{id,title,<kind>}]}` · `exclude_unset` 이라 다른 종류 칸은 안 실림 (`schemas/board_charts.py:18-62`) | `ChartSaved.parse` · `t.cells[k]` 만 반영 (`model/chart.dart:98-108` · `chart_controller.dart:168-172`) | 같음 |
| C2 409 | `ChartConflict({"conflicts": …})` → 공용 본문 + `details.conflicts[{taskId, body, staffId, base{body,doctorStaffId}, baseLogId}]` (`board.py:207-208` · `presentation/board_chart_reads.py:69-81`) | `ApiError.details` → `ChartConflict.parseAll` (`data/day_api.dart:267-269` · `model/chart.dart:111-122`) | 같음 |
| C2 409 반영 | 걸린 줄만 · 안 걸린 보낸 줄은 그대로(웹 `chart_tab_view` 와 같음) | 걸린 줄 = 서버 글 · KOS 담당자 · `logId=baseLogId` · `base` · 「바뀐 줄」 유지, 안 걸린 줄은 draft 그대로 (`chart_controller.dart:184-193`) | 같음(SPEC U-23 「충돌」) |
| C3 ① 목록 | `{visitId, reread, groups[{category,title,items[{photoId,shotAt,kosSynced}]}]}` · `edit` 없음 · 두 묶음 늘 (`schemas/photos.py:57-76` · `presentation/photos.py:36-49`) | `PhotoList.parse` · 서버 `title` · 서버 순서 (`model/chart.dart:140-159`) | 같음 |
| C3 ① `poll` · `tick` | `tick=="1"` 작업만 · `poll!="1"` 이면 작업 + 3초 대기 (`routers/api/board_photos.py:74-79`) — 웹 `routers/board_photos.py:153-157` 과 같은 줄 | 탭 고름 = 쿼리 없음 · `reread` → 5초 뒤 `?poll=1` · 10초 `?tick=1` (`chart_controller.dart:244-282`) | 같음 |
| C3 ② 올리기 | multipart `category` + `file`×N · 웹 `_form`(100MiB) 재사용 · `+kosError +rejected` (`board_photos.py:85-112`) | `postMultipart` 가 `category` + `file`×N(늘 JPEG)을 보냄 · `Content-Length` 먼저 (`day_api.dart:175-200`) | 같음 |
| C3 ③ ④ | `…/{photo_id}/delete` · `…/kos-retry` → 목록 + `kosError` | `'$_base/photos/$photoId/$action'` 본문 `{}` (`chart_controller.dart:310-326`) | 같음 |
| C3 ⑤ 파일 | `current_session`(Bearer) · `FILE_HEADERS` 셋 · 웹 GET 둘은 `required_web_view` 그대로 (`board_photos.py:155-178` · 웹 `routers/board_photos.py:142,259`) | `getBytes` 에 `Authorization: Bearer` · 메모리 캐시 (`day_api.dart:204-213` · `chart_controller.dart:335-343`) | 같음 |
| C0 오류 코드 | 413 `photo_too_large` · 400 `photo_type` · 409/503 `photo_disabled` → 공용 모양(기존 `photo_error_handler`) | 413 = 본문 모양과 상관없이 100MB 글자 · `photo_disabled` 글자 · 401 `unauthorized`·`session_expired` 둘 다 세션 끝 (`chart_controller.dart:345-369` · `day_api.dart:23`) | 같음 |
| C0 권한 | `require_permission` → `is_admin` = 전부 | `me.canEditBoard` = `allows('board', edit:true)` · `isAdmin` = 전부 (`day_api.dart:66-75` · `room_screen.dart:588`) | 같음 |
| 옛 `/api/tasks/{id}/chart` | 없음 · `/tasks/{id}/{action}` 이 400 · 저장 0 (`test_board_chart_api.py:489` · `test_board_api_chart_photos.py:247`) | 부르지 않음 | 같음 |
| Caddy | `@photo_upload` · `@other_body` 둘 다 `path /board/visits/*/photos /api/visits/*/photos` (`deploy/caddy/Caddyfile:9-18`) — 가운데 `*` 는 한 마디만 받아 delete · retry 는 6MiB 그대로 · 두 matcher 는 겹치지 않음 | — | 같음(C33 · ㉚) |

서비스 재사용(브리프 6-2)은 다음과 같다.

- 차트 저장: `board.save_chart_tab` 을 그대로 부른다. `baseBody` 를 `board.chart_body` 로 정리하는 것은 웹 `_chart_rows`(`routers/board.py:444-463`)와 같은 변환이다.
- 사진: `open_tab` · `request_import` · `wait_imported` · `list_photos` · `upload` · `delete` · `retry` · `open_file` 을 웹과 같은 순서로 부른다.
- 웹 라우트 · 템플릿 · static 은 diff 에 변경이 없다. 웹 차트 저장 회귀 테스트도 있다(`test_board_api_chart_photos.py:238`).

## 2. FAIL

없음.

## 3. WARN

### W1. 사진 탭 10초 tick 이 삭제 · 다시 시도 중에도 돈다 → 지운 사진이 잠깐 다시 보일 수 있음
- `app/lib/state/chart_controller.dart:247-249` — tick 이 건너뛰는 조건은 `picking || _uploading.isNotEmpty || _fetching` 뿐이다. `_photoBusy`(삭제 · 다시 시도 중)는 보지 않는다.
- 흐름: tick GET 이 삭제 POST 보다 먼저 서버에서 읽히고 늦게 도착할 수 있다. 그러면 `photos = l`(`:267`)이 삭제 응답 목록을 덮어쓴다. 지운 사진이 다음 tick(10초)까지 다시 보이고, 다시 시도한 사진은 「KOS 미반영」으로 되돌아 보인다.
- 근거: SPEC-003 U-23 「사진을 고르는 중 · 올리는 중이면 그 회차 건너뜀」은 웹 기본값이다. 삭제 · 다시 시도 중에 대한 문장은 없지만, 올리는 중과 같은 이유로 건너뛰는 것이 맞다.
- 고칠 방향: 건너뛰는 조건에 `_photoBusy.isNotEmpty` 를 넣는다. 또는 조작 응답이 반영된 뒤에 시작한 GET 응답만 쓴다(세대 번호).

### W2. 받기 실패한 사진은 화면이 다시 그려질 때마다 다시 받는다 · 깨진 그림이 깜빡임
- `app/lib/state/chart_controller.dart:335-343` + `app/lib/ui/chart_photos.dart:190-191` — `ApiError` 이면 캐시에서 지우고 null 을 돌려준다. 그런데 `FutureBuilder(future: controller.file(photoId))` 가 build 마다 새 future 를 받는다.
- 결과: 글 한 자 입력이나 10초 tick 으로 rebuild 가 일어날 때마다 실패한 사진을 다시 요청한다. 그동안 그림은 「받는 중」 회색과 「깨진 그림」 사이를 오간다.
- 근거: 「같은 바이트 1회」(A-59 · app-1 보고 「메모리 캐시」).
- 고칠 방향: 실패도 캐시한다(예: 실패 표시를 남기고 목록이 바뀔 때만 다시 받기). 또는 `ChartPhotoImage` 를 StatefulWidget 으로 바꿔 future 를 한 번만 잡는다.

### W3. 크게 보기 = 채팅 화면 재사용이 아니라 새 화면 (SPEC 과 다름 — 워커가 알림)
- `app/lib/ui/chart_photos.dart:206-231` — SPEC-003 U-23 「크게 보기 … 채팅 사진 크게 보기 `chat/screens/chat_photo_screen.dart` 재사용」이다. 구현은 검정 화면 + [닫기]를 따로 만들었다.
- 이유(app-1 다름 ②): 채팅 화면이 `ChatMessage` 에 묶여 있다. 새 글자는 없다(`closeLabel` 기존). 확대 · 이동(핀치)은 없다 — 채팅 화면에 있다면 기능 차이다.
- 고칠 방향: spec-sync 때 SPEC 문장을 「같은 꼴」로 고치거나, 채팅 화면에서 사진 표시 부분을 꺼내 함께 쓴다. 2루프에서 핀치 확대가 필요한지 사용자에게 묻는다.

### W4. 「최근 저장」 · [저장] 자리 = 탭 줄 아래 띠 (SPEC 「탭 줄 오른쪽」과 다름 — 워커가 알림)
- `app/lib/ui/chart_sheet.dart:236-268` — SPEC-003 U-23 「탭 줄 오른쪽 … 「최근 저장 : HH:MM」 바로 오른쪽에 [저장]」이다. 폭이 모자라 아래 띠에 두었다(app-1 다름 ①).
- 배치는 2루프 몫이라 FAIL 로 잡지 않았다. 다만 spec-sync 에서 SPEC 문장을 고칠지, 2루프에서 배치를 고칠지 정해야 한다.

### W5. 웹 라우터의 비공개 함수를 앱 라우터가 import
- `backend/day/routers/api/board_photos.py:33-35` — `from day.routers.board_photos import _form as photo_form` · `_photo_id as photo_id_of`.
- 복사하지 않고 한 곳(`BODY_MAX_BYTES`)으로 묶은 것은 맞다. 하지만 `_` 이름을 모듈 밖에서 쓴다. 앞으로 웹 쪽에서 이름을 바꾸면 앱 경로가 깨지는데, 웹 변경자는 이 사용처를 모른다.
- 근거: `docs/development/refactoring-conventions.md`(구조 · 이름).
- 고칠 방향: `_form` · `_photo_id` 를 공개 이름(예: `routers/board_photos.py` 의 `read_photo_form` · `photo_id_of`)으로 올리거나, `routers/photo_forms.py` 같은 공용 모듈로 옮긴다. 동작은 바뀌지 않는다.

### W6. `ChartConflict` docstring 이 예전 모양을 설명함
- `backend/day/errors.py:199-209` — 「`public_details` = 그 줄 · 그 차트의 새 값(`{taskId, chart, body, staffId, author, savedAt, logId}`)」이라고 적혀 있다.
- 지금 유일한 호출(`routers/api/board.py:208`)은 `{"conflicts": [...]}` 를 싣는다. 문서와 계약이 어긋난다.
- 고칠 방향: docstring 을 C2 `details.conflicts[]` 로 고친다.

### W7. 웹 사진 파일 GET 의 Bearer 거절 단언이 넓음 (조용히 통과)
- `backend/tests/day/board/test_board_api_chart_photos.py:429` — `assert web.status_code != 200`.
- 쿠키 전용 확인이 목적인데 500 이나 404 로 깨져도 통과한다.
- 고칠 방향: `required_web_view` 의 실제 결과(리다이렉트 303 또는 401)로 좁힌다.

### W8. 셸에 더한 `NavigatorPopHandler` 이후 「탭 스택 뒤로」 회귀 테스트 없음
- `app/lib/ui/shell.dart:236-237` — 세션 Navigator 바깥에 `NavigatorPopHandler` 를 더했다. 안쪽 탭 스택용 `NavigatorPopHandler`(`:270`)와 겹쳐 있다.
- 차트 위 Android 뒤로는 테스트가 있다(`app/test/ui/chart_test.dart:299-302`). 그런데 차트가 없을 때 룸 상세에서 Android 뒤로 → 목록으로 돌아가는 경우를 지키는 테스트는 찾지 못했다(`handlePopRoute` 는 `m2_actions_test.dart` 의 로그인 화면 하나뿐).
- iOS 앱이 대상이라 실물 영향은 작다. 그래도 바뀐 경로이니 테스트로 잡아 두는 것이 맞다(AGENTS 「테스트」).
- 고칠 방향: 「룸 상세 · Android 뒤로 = 목록」 위젯 테스트를 하나 더한다.

### W9. `copy.dart` 미정 코드 표에 예약 화면 코드 8개 추가 (범위 경계)
- `app/lib/core/copy.dart:116-130` — `companion_condition` … `reception_missing` 이다. 앱은 이 코드를 받지 않는다. 웹 `UNSET_MESSAGES` 와 맞추는 계약 테스트(`test/core/board_messages_contract_test.dart`)가 시작 전부터 −1 로 깨져 있었고, 이를 고치려고 넣은 것이다(app-1 「기준선 −1」).
- 동작 영향은 없다. 범위 밖 변경으로 기록만 남긴다. 범위를 넓힌 것은 아니다. 손 복제 표를 웹과 맞춘 것이라 허용 범위로 본다.

## 4. 사용자 확인 필요 (결정 · SPEC 을 다시 열지 않음 — 표에 없는 길)

### Q1. 푸시 · 알림 · 채팅 배너 [보기]가 미저장 차트를 확인 없이 닫는다
- `app/lib/ui/shell.dart:165`(`_toVisit` — 알림 행 · 원장 호출 푸시) · `:173`(`_toChat` — 채팅 푸시 · 배너 [보기]) · `:182`(채팅 거절) — `_sessionNav.currentState?.popUntil((r) => r.isFirst)` 는 차트의 `PopScope` 를 거치지 않는다. 쓴 글이 확인 창 없이 버려진다.
- SPEC-003 U-23 닫기 표(D6′ · D12)에 있는 길은 다섯(✕ · Android 뒤로 · iOS 밀기 · 끌어 내림 · 바깥 누름)과 「세션 끝 = 확인 없이 버림」이다. 이 세 길은 표에 없다.
- app-1 은 푸시만 알렸다. **채팅 배너 [보기]도 같은 길**이다. 시술실에서 차트를 쓰는 중에 채팅 배너가 뜨고 그것을 누르면 글이 사라진다.
- 선택지(사용자): (a) 지금대로 버림 · SPEC 에 한 줄 추가 (b) 미저장이면 확인 창 (c) 미저장이면 이동을 미루고 토스트.

### Q2. 카드가 판에서 빠질 때 세션 Navigator 에 남는 시트 · 팝오버
- `app/lib/ui/room_screen.dart:743`(확인 시트 · 창) · `app/lib/ui/doctor_picker.dart:84`(원장 고르기 · 방 옮기기 U-21 도 같은 함수 — `room_move.dart:37`). D9 · D14 에 따라 세션 Navigator 로 옮겼기 때문에, 룸 상세가 목록으로 돌아가도 시트는 남는다. 전에는 탭 Navigator 에 있어서 함께 닫혔다.
- 남은 시트로 [확인]을 누르면 서버 `not_found` 토스트 「대상을 찾을 수 없습니다. 화면을 새로 고칩니다」가 뜬다. 차트 창은 OQ-A69 대로 남는 것이 맞다. 확인 시트 · 원장 고르기에는 정한 문장이 없다.
- 선택지(사용자): 룸 상세가 닫힐 때 그 방문 시트도 닫을지(앱이 route 를 기억해 지움), 지금대로 서버 거절에 맡길지.

## 5. 앱 동작 점검 (브리프 6-3) — 통과한 것

| 점검 | 결과 · 근거 |
|---|---|
| 닫기 표 다섯 길 × 미저장 있음/없음 | `chart_sheet.dart:129`(`canPop = !anyDirty && !busy`) · `:138`(✕ = `maybePop` → PopScope 확인 창) · `:141-143`(끌어 내림 · 바깥 누름 = 미저장이면 무시) · `:186-187`(아이패드 덮개) · `MaterialPageRoute` + `canPop false` → iOS 밀기 꺼짐(D12). 테스트 `chart_test.dart:290-376`(iOS 밀기는 `debugDefaultTargetPlatformOverride`) |
| [버리고 닫기] | `c.discard()` → `Navigator.pop`(PopScope 우회 · 요청 0) · 테스트 `:309-328` |
| 보내는 중 닫기 꺼짐(OQ-A70) | ✕ `onPressed: c.busy ? null` (`:229`) · `_confirmClose` 가 busy 면 return (`:146`) · 테스트 `:377` |
| 충돌 409 반영 | §1 표. 다시 저장하면 응답 `base` · `baseLogId` 로 보냄(테스트 `chart_controller_test.dart:129`) |
| 저장 실패 때 쓴 글 유지 | 그 밖 거절 · 끊김 · 넘김 = `_fail` 만(draft 그대로) · `finally` 에서 잠금 풂 (`chart_controller.dart:173-180`) |
| 보내는 동안 잠금 | `setBody` · `setStaff` 무시 + `TextField.readOnly` · 담당자 누름 null (`chart_sheet.dart:279,306,340`) |
| 보기 권한 = 쓰기 UI 없음 | [저장] 숨김(`:259`) · 담당자 ▾ · 누름 없음 · 글 칸 readOnly · 사진 +/✕/↻ 숨김(`chart_photos.dart:50,77,83`) · 컨트롤러도 막음 · 테스트 `chart_test.dart:540` |
| 10초 tick 정지 | 탭 바꿈(`chart_sheet.dart:98-99`) · 닫히는 순간(`:162-164` · `_popped`) · dispose(`chart_controller.dart:371-377`) · 백그라운드(`AppLifecycleListener` `:85`) · 테스트 `chart_test.dart:426-453` |
| 세션 Navigator 시트가 세션 끝에 같이 사라짐 | 차트 · 고르기 · 확인 · 첨부 시트 · 크게 보기는 모두 `_sessionNav` 위 → 셸이 사라지면 함께 사라짐 · 테스트 `session_race_test.dart:129-141`(차트) |
| 사진 파일 Bearer | `day_api.dart:207` · 테스트 `chart_controller_test.dart:281-288` |
| 토스트가 차트 위 | `ToastHost` = `MaterialApp.builder`(`lib/app.dart:279`) — 세션 Navigator 보다 위(U-13) |
| 받기 실패 = 토스트 + 닫힘(OQ-A75) | `chart_sheet.dart:89-96` · 테스트 `chart_test.dart:106` |

## 6. Info.plist · 테마 (브리프 6-4)

- `app/ios/Runner/Info.plist:53,57` 의 카메라 · 사진 보관함 문구는 `_RESUME.md` D15 「…」 안 글자와 **바이트 일치**한다(파이썬으로 두 문자열을 비교해 True · True). 마이크 문구는 그대로이고, 새 권한 키는 없다(`test/build/info_plist_test.dart` 가 지킴).
- 까만 줄: `theme.dart` `outlineVariant` · `tabBarTheme.dividerColor` = `Ms.gray300`(D9). 앱 안 `TabBar` 는 차트 하나뿐이다(SPEC U-23).

## 7. 테스트가 동작을 실제로 지키나 (브리프 6-5)

- 앱 위젯 테스트는 실제 `DayApp` 트리 + 가짜 HTTP 서버 · SSE 로 돈다. 더블은 서버 경계에만 있고, 요청 경로 · 쿼리 · 본문 · Bearer 를 단언한다. 너무 넓은 더블은 보지 못했다.
- 백 테스트는 실제 PostgreSQL · Redis · disk 저장소를 쓰고, KOS client 경계만 가짜다. 저장 0(이력 · outbox) · 응답 키 집합(`set(got) == {...}`) · 머리 셋 · CSRF · 다른 병원 404 를 단언한다.
- 조용히 통과에 가까운 곳: W7(`!= 200`) · W8(탭 스택 뒤로 회귀 없음).
- 덧붙임: `detail_polish_test.dart:50-55` · `room_move_test.dart:125-130` 는 「꺼진 [시작] · 담당의 글자 누름 = 조작 요청 0」을 `/chart` 경로를 빼고 센다. 누르면 차트 GET 이 나가는 것은 SPEC 「여는 곳 = 시술 줄 누름」과 맞다. 단언을 좁힌 것이지 비운 것이 아니다.
- 실행 수치(워커 보고 인용 · 리뷰어는 실행 안 함): BE `./scripts/test.sh -q` 2902 passed · `check.sh` 의 frontend 단계는 npm 미설치로 pending / APP `flutter analyze` 0 · `flutter test` +460 ~81 −0 · `build ios --no-codesign` 통과.

## 8. 범위 밖 · 새 글자 · 새 패키지 (브리프 6-6)

- 새 패키지 없음(`pubspec.*` · `pyproject` · `uv.lock` 변경 없음).
- 새 화면 글자 없음. 앱 글자는 모두 웹 템플릿 · `board_messages.py` · 채팅 기존 글자(`photoDisabledMessage` = `chat_copy.dart:39` · `photoDeniedMessage` = `chat_room_screen.dart:159`)다. 계약 테스트가 웹 파일을 읽어 지킨다.
- migration 없음. 웹 라우트 · 템플릿 · static 변경 없음.
- 범위 경계 두 곳은 기록만 남긴다. (1) W9 예약 코드 동기화. (2) 방 옮기기 시트(U-21)도 `showPickerSurface` 를 같이 써서 세션 Navigator 로 올라감 — D9 「같은 탭 Navigator 시트」 취지와 맞는다.

## 9. 사용자가 시뮬레이터에서 만날 자리 (막히진 않는데 이상해 보일 곳)

1. **채팅 배너 [보기] · 푸시를 누르면 쓰던 차트가 경고 없이 닫히고 글이 사라진다**(Q1).
2. **「최근 저장」 · [저장]이 탭 줄 아래 따로 놓인 띠에 있다** — 웹과 자리가 다르다(W4). 저장한 적이 없는 탭에서 보기 권한이면 띠 자체가 없어서, 탭마다 위아래 높이가 달라 보일 수 있다(`chart_sheet.dart:252`).
3. **사진을 지운 직후 몇 초 동안 그 사진이 다시 나타났다가 사라질 수 있다**(W1, 10초 tick 과 겹칠 때).
4. **받지 못한 사진 썸네일이 회색 ↔ 깨진 그림으로 깜빡인다**(W2, 글 입력 · tick 마다).
5. **크게 보기에서 손가락으로 확대가 안 된다**(W3, 채팅 화면과 다른 꼴 · 보낸 사람 · 시각 줄 없음).
6. 사진 탭 버튼이 모두 아이콘(＋ · ✕ · ↻ · 경고)뿐이고 글자가 없다. 「KOS 미반영」도 빨간 경고 아이콘 하나다(웹도 미정 · OQ-A78).
7. 담당자 칸이 빈칸이면 빈 테두리 상자와 ▾ 만 보인다. 보기 권한이면 ▾ 도 없어 빈 회색 상자만 남는다(웹 빈 값과 같음).
8. 담당자 고르기 목록이 서버 순서로 나온다(이름순 아님 · `doctor_picker.dart:120` 의 `sorted` 는 아바타 색에만 쓰임). 원장 고르기 드로어(이름순 · `:243`)와 순서 규칙이 달라 보일 수 있다.
9. 저장 200 뒤 같은 탭 글 칸 커서가 끝으로 튄다. 서버가 앞뒤 빈칸을 뺀 글로 바꿔 넣는 경우다(`chart_sheet.dart:106-111` — `text` 를 통째로 바꿈).
10. 사진 올리는 동안(최대 120초 · 원천 없음 · app-1 애매 1) ✕ · 뒤로가 꺼진다. 진행 표시가 없어 「창이 안 닫힌다」로 보일 수 있다(OQ-A70 기본값대로).
11. 카드가 판에서 빠진 뒤에도 확인 시트 · 원장 고르기가 떠 있고, 누르면 「대상을 찾을 수 없습니다. 화면을 새로 고칩니다」가 뜬다(Q2).
12. 꺼진 [시작] 버튼이나 담당의 글자를 누르면 차트가 열린다(줄 누름으로 떨어짐 · 기존 동작이지만 이제 서버 요청 + 로딩 원이 보임).
13. 폰 차트는 오른쪽에서 밀려 들어오는 페이지 전환이다(iOS 기본). 「끌어 내림」은 머리 줄에서만 받는다.

## 10. 참고 (기존 부채 · 무관)

- BE `check.sh` frontend 단계 pending — 워크트리에 npm 의존이 없다(be-1 보고). 변경과 무관하지만 PR 전에 코디가 한 번 돌려야 한다.
- 앱 `board_messages_contract_test` 는 시작 전부터 −1 로 깨져 있었고, 이번에 고쳐졌다(app-1 기준선).

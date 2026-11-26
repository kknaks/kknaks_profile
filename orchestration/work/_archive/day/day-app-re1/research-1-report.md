# research-1 — 앱 시술현황 차트 현황 조사 (웹 차트와 같은 기능으로 올리기 전)

- 워커: day `researcher` · 2026-11-25 · read-only
- 코드 기준: `MediSolveAIDev/CENTURION_DAY` `55e60aa4`(origin/dev) — 근거 표기 `파일:줄` 은 모두 이 커밋
- 스펙 기준: `MediSolveAIDev/mediness` `origin/main` = `b152d463` — `products/day/20-spec/…`
- 결정 정본: `reference/2026-11-24-day-picture/chart-photo-decisions.md`(profile main · C1 ~ C36)
- 사용자 스크린샷 `~/.config/day/reference/app-chart-2026-11-25.png` 은 보기만 했다(복사 안 함)

---

## 0. 한 화면 요약

| 구분 | 내용 |
|---|---|
| **앱에 있음** | 차트 시트 하나 — 탭 2(간호 관리 차트 · 의사 차트) · 시술마다 글 칸 · **읽기 전용**(`SelectableText`). 값 = 판 스냅샷 `tasks[].assigneeNote` · `doctorNote`(KOS 사본). 차트 API 호출 0건 |
| **앱에 빠짐** | 탭 3번째(시술전후사진) · 담당자 고르기 · 글 편집 · 탭별 [저장] · 「최근 저장 : HH:MM」 · 저장 전 KOS 확인 / 충돌 이어 붙이기 결과 반영 · 미저장 닫기 확인 · 사진 목록 · 올리기(여러 장) · 삭제(확인 창) · 「KOS 미반영」 + [다시 시도] · 원본 크게 보기 · 사진 탭 10초 가져오기 · 저장 거절 / 사진 토스트 글자 · 고객 바이탈 줄(성별 · 나이 · 국적) · [고객 차트] 버튼 · 시술 전 의사차트(DAY 이력에만 있는 글) |
| **디자인 이상 원인** | ① 까만 가로줄 = M3 `TabBar` 기본 구분선 — `dayTheme()` 이 `outlineVariant` 를 안 줘서 `onSurface`(= `#000000`) 로 그려짐 ② 「탭바 밑에 깔림」 = 시트가 **시술현황 탭 Navigator**(탭바 위 영역)에 떠서 시트 아래 끝이 탭바 윗선에 붙고 탭바는 dim 없이 그대로 보이고 눌림. 탭바 「밑으로」 들어가는 것은 아니다(코드 근거 §1-3) |
| **백엔드 추가 필요?** | **예.** 서비스(저장 · 사진 로직)는 세션 종류와 무관하게 앱 세션으로 돌 수 있지만, **앱이 부를 JSON 경로가 없다**: 차트 탭 저장 · 사진 목록 · 올리기 · 삭제 · 다시 시도 · 파일 다섯 갈래 전부 웹 HTML 조각 라우트뿐이고, 그중 GET 두 개(사진 목록 · 파일)는 **쿠키 전용**이라 앱 Bearer 로는 401. 차트 읽기 JSON(`GET /api/visits/{id}/chart`)은 **이미 있다**(앱이 안 부를 뿐) |
| **스펙** | SPEC-003 은 앱 차트 = 읽기 전용 · 차트 API 0건을 인수 조건(A-38)으로 박아 둠. SPEC-002 는 차트 저장 · 사진 「앱 경로 없음 — 웹만(C15)」. 고칠 절 = SPEC-003 §1 「뺌」 표 · §2 차트 줄 · §3 API 계약 · §4 권한 / A-17 · A-38 · OQ-A30 · OQ-A34 + SPEC-002 API 계약 표 차트 · 사진 행 · U-16 마지막 줄 · C15 |
| **정할 것** | **11건**(§6) |

---

## 1. 앱 현재 상태

### 1-1. 여는 흐름

- 룸 상세(`RoomScreen`)의 시술 줄 하나를 누르면(줄 전체 `GestureDetector` · `onTap`) `showChart(...)` — `app/lib/ui/room_screen.dart:584-587`.
  - 넘기는 값 = 고객 이름 · 한글 발음 + **그 카드 시술 전부**의 `ChartEntry(title, assigneeNote, doctorNote)` — `room_screen.dart:586-587`.
  - 누른 시술로 스크롤 · 강조하지 않는다(웹은 `flash` = 누른 시술 섹션 깜빡임 — `routers/board.py:297-314` · `board_chart_parts.html:62`).
- 룸 상세 자체는 시술현황 탭 Navigator 에 `MaterialPageRoute` 로 쌓인다 — `app/lib/ui/board_screen.dart:93-95`.
- 다른 곳에서 차트를 여는 곳 없음(`git grep showChart` = `room_screen.dart:586` 하나). 앱엔 「시술 완료」 탭이 없어 완료 방문 차트는 못 연다(SPEC-003 :402).

### 1-2. 보여 주는 것 · 부르는 API · 편집

- `app/lib/ui/chart_sheet.dart` 전체 89줄. 1줄 주석 = 「읽기 전용(DAY-SPEC-002 U11 · 웹 ui.html `chart_modal` 글자). 작성 · 저장 · 작성자 · 시각 없음」.
- 머리 = `CustomerName`(이름 · 발음) + [✕] — `chart_sheet.dart:46-56`. 바이탈(성별 · 나이 · 국적) · [고객 차트] 없음.
- 탭 = `TabBar(tabs: [Tab('간호 관리 차트'), Tab('의사 차트')])` — `chart_sheet.dart:57`(웹 글자는 「간호관리차트」 · 「의사차트」 · 「시술전후사진」 — `board_chart_parts.html:15-16`. 앱 글자는 띄어쓰기가 다르다).
- 칸 = 시술마다 제목 + 회색 상자 안 `SelectableText` — `chart_sheet.dart:68-88`. **편집 가능한 곳 0.** 담당자 · 작성자 · 저장 시각 표시 없음.
- **API 호출 없음.** 값은 판 스냅샷(`GET /api/board` · SSE)에서 이미 받은 `tasks[].assigneeNote` · `doctorNote` — `app/lib/model/board.dart:85-86 · 124-125`. 앱 `data/day_api.dart` 의 경로는 auth · devices · 판 조작 POST 뿐(`day_api.dart:112-148`) · `git grep "/chart"` app = 0.
  - 결과: 시술 전(준비중 · 호출 중) 의사차트처럼 **DAY 이력에만 있는 글은 앱에 안 보인다**(SPEC-003 OQ-A34 「1차 그대로」).
- 폰 = `showModalBottomSheet(isScrollControlled, useSafeArea, heightFactor 0.8)` · 아이패드 = `showDialog`(최대 410×640) — `chart_sheet.dart:14-34`. 둘 다 `barrierColor` 지정 없음(다른 앱 시트는 `Ms.dim` — `doctor_picker.dart:99` · `chat_kit.dart:409`).
- 시험: `app/test` 에 `showChart` · `ChartEntry` · `chart_sheet` 를 부르는 시험 0건(`git grep` 결과 없음).

### 1-3. 디자인 이상 원인 (코드 근거)

**① 탭 아래 까만 가로줄**

- `chart_sheet.dart:57` `TabBar` 에 `dividerColor` 를 주지 않고, `app/lib/ui/theme.dart:110-158` `dayTheme()` 에 `tabBarTheme` 이 없다.
- Flutter 3.44.8(`.fvmrc` @55e60aa4) M3 기본: `_TabsPrimaryDefaultsM3.dividerColor => _colors.outlineVariant` · `dividerHeight => 1.0`(`~/fvm/versions/3.44.8/packages/flutter/lib/src/material/tabs.dart:2806 · 2810`).
- `ColorScheme.outlineVariant => _outlineVariant ?? onBackground` · `onBackground => _onBackground ?? onSurface`(`color_scheme.dart:1299 · 1360`).
- `dayTheme()` 의 `ColorScheme.light(... onSurface: Day.textPrimary ...)` = `#000000`(`theme.dart:117 · 40`), `outlineVariant` 미지정 → **1px 검정 구분선.** 스크린샷의 탭 아래 전체 폭 검정 줄과 일치.
- 앱 안에 `TabBar(` 는 이것 하나뿐(`git grep` — 셸 `_TabBar` 는 자체 위젯). 다른 화면에 같은 증상은 없다.

**② 시트가 하단 탭바에 깔림**

- `showModalBottomSheet` 의 `useRootNavigator` 기본값 = false → **가장 가까운 Navigator = 시술현황 탭 Navigator**(`_navs[AppTab.board]`).
  - 폰 셸 = `Scaffold` → `Column[ Expanded(탭 IndexedStack · 탭마다 Navigator) , _TabBar ]` — `app/lib/ui/shell.dart:248-265 · 295-307`.
  - 탭 Navigator 영역은 탭바 **위까지**이고 그 영역은 아래 안전 영역도 지워져 있다(`shell.dart:304-305` `removePadding(removeBottom: true)`).
  - 그래서 시트(그 영역의 80%)는 아래 끝이 탭바 윗선에 딱 붙고, dim 은 탭 영역만 덮어 **탭바는 밝게 남고 눌린다.** 스크린샷: 룸 상세는 어둡고 하단 3메뉴는 밝음 · 시트 흰 바탕이 탭바 흰 바탕과 이어져 마지막 「쥬베룩」 칸이 탭바 선에서 끊겨 보임.
- 시트의 `ListView` 아래 여백은 `16 + listEndInset`(iOS 0) — `chart_sheet.dart:69`. 끝까지 스크롤하면 마지막 칸이 보이는지는 **실기기 확인 안 됨**(빌드 · 실행 금지).
- `chart_sheet.dart:19` 주석은 「세션 Navigator 에 묶는다」인데 실제로는 탭 Navigator 다(아이패드 `showDialog(useRootNavigator: false)` 도 같은 탭 Navigator). 셸에는 탭바까지 덮는 **세션 Navigator** `_sessionNav` 가 따로 있다 — `shell.dart:104-106 · 234`. 채팅의 창 · 시트는 `chatOverlayContext` 로 그 세션 Navigator 를 쓴다(`app/lib/chat/chat_kit.dart:55 · 58` · `chat_ui.dart:111` 등).
- 같은 탭 Navigator 에 뜨는 다른 시술현황 시트: 원장 고르기(`doctor_picker.dart:93`) · 확인 시트(`room_screen.dart:753`). 고치는 범위를 차트만으로 할지 함께 할지는 정할 것(§6 Q9).

---

## 2. 웹 차트 기능 전수표

열 = 기능 · 웹 코드 위치 · 백엔드 경로(메서드 · 인증 · 응답) · 앱 지금. 인증 표기: **쿠키 전용** = `required_web_view`(`backend/day/session.py:151-156` — 쿠키 `day_session` 만 읽음) · **쿠키 / Bearer** = `writable_session`(`session.py:46-74` — Bearer 가 있으면 Bearer · CSRF 는 쿠키 세션에만).

| # | 기능 | 웹 코드 | 백엔드 경로 · 인증 · 응답 | 앱 |
|---|---|---|---|---|
| 1 | 차트 모달 열기 · 값 | `partials/board_chart.html` · `board_chart_parts.html:121-154`(modal) | `GET /board/visits/{id}/chart?sec=` — 쿠키 전용 · `board` view · HTMX 아니면 `/board` 로 redirect · HTML(`routers/board.py:297-314`). 같은 값 JSON = `GET /api/visits/{id}/chart` — 쿠키 / Bearer(`current_session`) · `board` view(`routers/api/board.py:148-161`) | **일부** — 읽기만 · 스냅샷 노트 사용 · JSON 안 부름 |
| 2 | 탭 셋(간호관리 · 의사 · 시술전후사진) · 처음 탭 `firstTab` | `board_chart_parts.html:15-16 · 137` | #1 응답 `firstTab`(`schemas/board_responses.py:640`) | **일부** — 탭 2 · 늘 첫 탭 · 사진 탭 없음 |
| 3 | 머리 = 이름 · 발음 + 바이탈(성별 · 만 나이 · 국적) | `board_chart_parts.html:128-131` | #1 `customer{name, phoneticName, gender, birthDate, nationality, isNew}`(`board_responses.py:626-638`) | **일부** — 이름 · 발음만 |
| 4 | [고객 차트] 버튼 | `board_chart_parts.html:133`(`data-cc-from-board` → `/board/visits/{id}/customer-chart`) | 고객 차트 화면(웹 · `routers/customers.py:75 · 190`) | **없음** |
| 5 | 칸 = 시술마다 「시술명 · 담당자 · 차트 내용」 | `board_chart_parts.html:51-78` | #1 `tasks[].{assignee, doctor}.{body, staffId, author, savedAt, logId, base}` · `staffOptions{assignee[], doctor[]}`(`board_responses.py:545-656`) | **일부** — 시술명 · 글만(담당자 없음) |
| 6 | 담당자 고르기(직군 표시 · 목록 밖 값은 빈칸) | `board_chart_parts.html:59-72`(`ui.staff_picker`) | #1 `staffOptions` | **없음** |
| 7 | 글 편집 · 보기 권한이면 readonly | `board_chart_parts.html:75` · `edit` = admin 또는 `board` edit(`routers/board.py:316-322`) | 권한 = `board` edit(SPEC-002 권한 표 :689) | **없음**(편집 0) |
| 8 | 저장 단위 = 탭(차트 종류) × 그 방문 바뀐 줄 전부 · 한 transaction | 탭 form `board_chart_parts.html:80-87` · `day.js:1423-1479`(바뀐 줄만 보냄 · 안 바뀐 줄 칸 disabled) | `POST /board/visits/{id}/chart` — **쿠키 / Bearer** · `board` edit · **form-urlencoded** `chart` + 줄마다 `taskId · body · staffId · baseLogId · baseBody · baseDoctorStaffId` · 응답 **HTML 조각**(`partials/board_chart_tab.html`) · HTMX 아니면 **저장한 뒤** `/board` redirect(`routers/board.py:466-524` — :161 저장 → :162-163 redirect) · 서비스 `services/board_charts.py:189-279` | **없음** |
| 9 | [저장] 자리 · 켜짐(바뀐 줄 있을 때만) · 보기 권한이면 없음 | `board_chart_parts.html:40-48` · `day.js:1438-1459` | — | **없음** |
| 10 | 「최근 저장 : HH:MM」(탭마다 savedAt 최댓값) | `board_chart_parts.html:29-37` · 응답 OOB `board_chart_tab.html:9` | #1 `savedAt` | **없음** |
| 11 | 저장 전 KOS 지금 값 확인 · 하나라도 다르면 탭 전체 거절(409 `chart_conflict`) | — | `board_charts.py:189-245`(`_kos_now` → `judge_row`) · 규칙 `policies/board_chart_tabs.py:26-31 kos_differs` · C17 | **없음** |
| 12 | 걸린 줄 = KOS 글 + 줄바꿈 + 내 글 · 담당자는 KOS 값 · 그 상태로 다시 저장 | `day.js:1428-1433`(409 로 다시 그린 줄은 늘 「바뀐 줄」) | `board_chart_tabs.py:15-23 joined_text` · `presentation/board_chart_reads.py:27-` `chart_tab_view` · 409 응답 본문 = 같은 탭 조각 | **없음** |
| 13 | 응답 유실 뒤 같은 저장 = 성공(C19) · 줄바꿈 정규화(C20) | — | `board_chart_tabs.py:11-13 · 34-` | **없음** |
| 14 | 저장 중 칸 잠금(C21-기본값) · 15초 시간 초과 | `day.js:1452 chartLock` · `hx-request timeout 15000`(`board_chart_parts.html:82`) | — | **없음** |
| 15 | 집도의를 바꾼 저장 = 카드 · 원장 상태 갱신 | — | 응답 `X-Day-Action` · `X-Day-Version` + OOB(`routers/board.py:167-194`) | **없음** |
| 16 | 미저장 닫기 확인 창(「저장하지 않고 닫을까요?」 · [계속 쓰기] · [버리고 닫기]) · ✕ · Esc · 바깥 누름 무시 | `board_chart_parts.html:89-101` · `day.js:1517-1591` | — | **없음** |
| 17 | 저장 거절 토스트 글자 | `board_chart_tab.html:10` | `routers/board_messages.py:25-29`(`chart_conflict` · `chart_staff_required` · `staff_not_listed` · `chart_staff_not_listed`) · C29 | **일부** — 앱 `core/copy.dart:22-23` 이 웹 표를 복제하되 `chart_conflict` 만 뺀다 · `chart_staff_required` · `staff_not_listed` 는 앱에서 「빈 글자」(`copy.dart:109-118` `unsetActionCodes`) |
| 18 | 사진 탭 — 두 묶음(시술 전 · 시술 후) · DAY 행만 | `board_photos.html:15-47` | `GET /board/visits/{id}/photos` — **쿠키 전용** · `board` view · HTML(`routers/board_photos.py:126-147`) · 서비스 `services/visit_photos.py:164` | **없음** |
| 19 | 사진 올리기 — 묶음마다 · 여러 장 한 요청 · JPEG · PNG · 장당 5MB · 본문 100MiB | `board_photos.html:39-43`(`input type=file multiple accept=image/jpeg,image/png`) · `day.js:1669 photosPickDone` | `POST /board/visits/{id}/photos` — **쿠키 / Bearer** · `board` edit · multipart `category` + `file` 여러 개 · 응답 HTML 조각 · HTMX 아니면 **처리한 뒤** redirect(`board_photos.py:185-208` · `_render :97-98`) · 형식 판정 `policies/photos.py:7 · 18-31` · 앞단 `deploy/caddy/Caddyfile:4-22`(이 경로만 100MiB) | **없음** |
| 20 | 사진 삭제 + 확인 창(「사진을 삭제할까요?」 · [취소] [삭제]) | `board_photos.html:32-34` · `board_chart_parts.html:105-118` | `POST /board/visits/{id}/photos/{photo_id}/delete` — 쿠키 / Bearer · `board` edit · HTML(`board_photos.py:211-226`) | **없음** |
| 21 | 「KOS 미반영」 표시 + [다시 시도] | `board_photos.html:24-31` | `POST …/photos/{photo_id}/kos-retry` — 쿠키 / Bearer · `board` edit · HTML(`board_photos.py:229-244`) | **없음** |
| 22 | 썸네일 · 원본 보기(새 창) | `board_photos.html:23-25`(`<a target=_blank><img src=…/file>`) | `GET …/photos/{photo_id}/file` — **쿠키 전용** · `board` view · 바이트 스트림 `no-store` · `inline`(`board_photos.py:247-274`) | **없음** |
| 23 | 탭을 열 때 KOS 사진 가져오기(최대 3초 대기 · 못 끝나면 5초 뒤 `poll=1`) | `board_chart_parts.html:147` · `board_photos.html:48-49` | #18 `poll` 없음 → `visit_photo_import.request_import` + `wait_imported`(`board_photos.py:142-146` · `services/visit_photo_import.py` 머리 주석) · C23 | **없음** |
| 24 | 사진 탭 보이는 동안 10초마다 `?tick=1` · 다른 탭 · 닫힘 = 멈춤 | `day.js:28 · 1618-1660 photosTick` | #18 `tick=1`(`board_photos.py:142-143`) · C30 | **없음** |
| 25 | 사진 토스트 글자 | `board_photos.html:52` | `board_messages.py:54-58`(「KOS 반영에 실패했습니다」 · 「올리지 못한 사진이 있습니다 (JPEG · PNG, 5MB 이하만)」 · 「한 번에 올릴 수 있는 용량(100MB)을 넘었습니다」) · C27 · C36 | **없음** |
| 26 | 사진 KOS 쪽 = 로그인 직원 토큰(시스템 계정 아님) · 없으면 401 `session_expired` | — | `visit_photos.py:123-134 staff_token`(그 세션의 `ExternalSession`) · C10 | 해당 없음(아래 §3-3) |
| 27 | 권한 | 보기 = `board` view(모든 직군 기본) · 쓰기(차트 작성 · 사진 올리기 · 삭제) = `board` edit(SPEC-002 :688-689 · C7) | 라우트마다 `require_permission` | 앱은 `/me` 의 `canEditBoard` 로 판 조작 버튼만 가린다(`room_screen.dart:543`) — 차트엔 안 씀 |
| 28 | 대상 방문 = 오늘 판 카드 · 「시술 완료」 탭 방문만, 그 밖 404 | — | `visit_photos.py:104-112 chartable` · `board_charts.py:68-83 _rows_of`(규칙 23) — 사진 다섯 경로 전부 `chartable` 를 먼저 부름(`visit_photos.py:119 · 167 · 375 · 473 · 512 · 601`) | 해당 없음 |

참고: 차트 저장 규칙의 정형 명세는 `.agents/skills/verify-day-chart/`(`SKILL.md` · `specs/ChartSave.tla` · `ChartGuard.lean` · `GuardContract.lean` · `source-map.json`)에 있다 — 읽기만 했고 내용은 위 #8 ~ #15 와 같은 규칙을 가리킨다.

---

## 3. API 재사용성 — 앱이 웹 차트 API 를 그대로 부를 수 있나

### 3-1. 경로별 결론

| 경로 | 앱 Bearer 로 통과? | 앱이 쓸 수 있는 응답? | 결론 |
|---|---|---|---|
| `GET /api/visits/{id}/chart`(JSON) | 예 — `current_session`(`api/board.py:155-161`) | 예 — `ChartResponse` JSON(담당자 · `logId` · `base` · `savedAt` · `staffOptions` 포함) | **그대로 쓸 수 있음.** 단 SPEC-003 A-38 이 「차트 API 호출 0건」을 인수 조건으로 둠 |
| `GET /board/visits/{id}/chart`(HTML) | 아니오 — 쿠키 전용(`board.py:297-303` · `session.py:151-156`) | HTML · HTMX 아니면 redirect | 못 씀 |
| `POST /board/visits/{id}/chart`(탭 저장) | 예 — `writable_session` · Bearer 면 CSRF 안 봄(`session.py:63-74`) | **아니오** — form-urlencoded 요청 · HTML 조각 응답 · `HX-Request` 없으면 **저장은 하고** 303 redirect 만 돌려줌 → 저장됨 / 충돌(409) 결과 · 걸린 줄 이어 붙인 값 · 새 `logId` 를 앱이 못 받음(`board.py:161-163`) | 실질적으로 못 씀(앱이 `HX-Request` 를 흉내 내 HTML 을 파싱하는 길은 남아 있으나 AGENTS.md 「API 경로 · 오류 계약 = 외부 계약」 · 「JSON = 앱 전용」(SPEC-002 개정 ② OQ-01)과 어긋남) |
| `GET /board/visits/{id}/photos` | 아니오 — 쿠키 전용(`board_photos.py:132`) | HTML | 못 씀 |
| `POST /board/visits/{id}/photos` | 예 — `writable_session`(`board_photos.py:189`) | 아니오 — HTML 조각 / 처리 뒤 redirect(`:97-98`) · KOS 실패(`kos_error`) · 빠진 장(`rejected`) 결과를 앱이 못 받음 | 실질적으로 못 씀 |
| `POST …/photos/{id}/delete` · `…/kos-retry` | 예 | 아니오 — 위와 같음 | 실질적으로 못 씀 |
| `GET …/photos/{id}/file` | 아니오 — 쿠키 전용(`board_photos.py:255`) | 바이트(형식은 앱이 쓸 수 있는 모양) | 인증 때문에 못 씀 |

- 웹 · `/api` 라우터는 **같은 FastAPI 앱 · 같은 호스트**에 붙는다(`backend/runtime/main.py:68-73` · `day/public.py:26-33`). 앱의 `api_base_url` 로 웹 경로에 닿는 것 자체는 가능.
- Caddy 본문 상한 100MiB 는 경로 `/board/visits/*/photos` 에만(`Caddyfile:8-22`) — 앱용 새 경로를 만들면 그 경로도 Caddy 에 더해야 6MiB 를 넘는다(그 밖 6MiB).

### 3-2. 앱 전용 JSON 짝 — 지금 있는 것 / 없는 것 (목록만)

- 있음: `GET /api/visits/{visit_id}/chart`(읽기). 옛 줄 저장 `POST /api/tasks/{task_id}/chart` 는 이미 지워짐(`api/board.py` 경로 목록 :149 · 165 · 185 · 244 · 264 · 282 · 302 · 323 · 344 — chart POST 없음 · SPEC-002 :648 「지우는 대상」과 일치). 모듈 주석이 「차트 저장 JSON 짝은 없다(개정 ㉘ · 검수 W8)」 — `api/board.py:13`.
- 없음(앱이 웹 기능을 쓰려면 빠진 것):
  1. 차트 탭 저장 JSON(요청 = `chart` + `rows[]` · 응답 = 저장됨 / 409 `chart_conflict` + 걸린 줄 값 · 새 `logId` · `savedAt` · 집도의 변경 여부 · `version`)
  2. 사진 목록 JSON(`poll` · `tick` 뜻 포함 · 두 묶음 · `photo_id` · `shot_at` · `kos_synced` · `reread`)
  3. 사진 올리기 JSON 응답(목록 + `kos_error` + `rejected`)
  4. 사진 삭제 · 다시 시도 JSON 응답
  5. 사진 파일 Bearer 열기(채팅 첨부 열기와 같은 꼴 — `routers/api/chat.py:14` 주석 「서버가 직접 바이트를 보낸다(Bearer · no-store)」)
  6. 오류 = 공용 `{detail, code, field}`(앱 `/api` 공통 — `api/board.py:14-17`) — 사진 쪽 `PhotoError`(413 · 코드 `photo_too_large` 등)가 `/api` 에서도 같은 모양으로 나가는지는 **확인 안 됨**
- 서비스 층은 재사용 가능: `board.save_chart_tab` · `visit_photos.upload/delete/retry/list_photos/open_file` · `visit_photo_import.request_import/wait_imported` 은 `CurrentSessionData` 만 받고 쿠키 / Bearer 를 모른다(`board_charts.py:189-198` · `visit_photos.py` 시그니처). 웹 라우터가 HTML 로 바꾸는 부분(`presentation/photos.photos_view` · `chart_tab_view`)만 화면 쪽이다.

### 3-3. 앱 세션의 KOS 토큰

- 앱 · 웹 로그인은 같은 서비스에서 `LoginSession` + `ExternalSession(access_token = KOS 직원 토큰)` 을 만든다 — `backend/day/services/auth.py:577-597`(세션 만료 = KOS 토큰 만료). 클라이언트 종류로 갈라지지 않는다(`auth.py` 에 `client` 분기는 로그인 거절 규칙뿐 — :27 · :253).
- 따라서 차트 저장의 KOS 확인(`_kos_now`) · 사진 KOS 등록의 `staff_token`(`visit_photos.py:123-134`)은 앱 세션으로도 같은 직원 토큰을 찾는다(코드 읽기 기준 · 실물 확인 안 함).

### 3-4. 예약 탭(WORK-002)에서 사진 흐름을 부를 수 있나

- **지금 코드로는 아니다.** 사진 다섯 경로 전부 첫 단계가 `chartable` — 「오늘 판 카드 · 『시술 완료』 탭」 방문이 아니면 404(`visit_photos.py:104-112`). 예약 탭 방문(아직 판에 안 오른 예약 · 다른 날짜)은 여기서 걸린다.
- 경로도 `/board/visits/{id}/photos` 로 판 아래에 있고 권한 키는 `board` view / edit(`board_photos.py:46-47`).
- 예약 화면 라우터 · 템플릿에 사진 경로 없음(`routers/reservations.py` · `reservation_detail.py` `git grep photo` = 0).
- 앱 쪽 고르기 · 올리기 부품(§4)은 화면에 묶여 있지 않아 예약 탭에서도 부를 수 있는 모양이다. 서버 대상 방문 규칙 · 권한 키 · 경로 위치가 정할 것(§6 Q8).

---

## 4. 앱 네이티브 · 패키지 — 재사용 후보

| 무엇 | 있는 것 | 근거 |
|---|---|---|
| 패키지 | `image_picker ^1.2.4` · `flutter_image_compress ^2.5.1` · `photo_manager ^3.12.0` · `video_player` · `http ^1.6.0` | `app/pubspec.yaml:13-25` |
| 사진 찍기 · 고르기 | `chat/photo_pick.dart` — `pickChatPhoto(PhotoSource.camera / album)` · 고른 파일을 **늘 JPEG(긴 변 2048 · 품질 85)로 다시 인코딩** · 권한 거부 = `PhotoDenied` · 카메라 사진 사진첩 저장 안 함 · 임시 파일 바로 지움 | `photo_pick.dart:1-60`. 서버 웹 경로는 JPEG · PNG 만 받는다(`policies/photos.py:18-31` — HEIC 거절) → JPEG 변환이 그대로 맞는다 |
| 여러 장 고르기 | 첨부 시트 「최근 사진」 줄(최대 10 · `photo_manager` · limited 접근 [더 고르기]) · 「사진」 메뉴 = `pickMultipleMedia(limit: 10)` | `chat/screens/chat_attach_sheet.dart:1-6`(주석) · `photo_pick.dart:5`. 웹 사진은 「장 수 한도 없음」(C28) — 10 한도는 채팅 값 |
| 첨부 시트 | `openAttachSheet(context, media, onCamera)` — 폰 시트 / 아이패드 가운데 창 · 결과 `AttachSend(items, thumbs)` · `AttachGallery` | `chat_attach_sheet.dart:17-56`. 채팅 모델(`RecentItem` · `RecentMedia` · 동영상 칸)에 묶여 있어 그대로 쓰면 동영상도 고를 수 있다 — 사진만으로 좁힐지는 정할 것 |
| multipart 올리기(진행률 · 되밀기 · `Content-Length` 고정 · 시간 초과) | `ChatApi._upload` — `http.StreamedRequest` · Bearer · `Accept: application/json` · 응답 JSON 기대 | `chat/chat_api.dart:145-185` |
| Bearer 로 이미지 받아 그리기 | 채팅 사진 = Bearer 로 받아 메모리 캐시 · `Image.memory`(`Image.network` 안 씀) | `chat/widgets/chat_media.dart:11` |
| 크게 보기 | `chat/screens/chat_photo_screen.dart` · `chat_media_screen.dart` | 파일 목록(@55e60aa4) — 내부는 읽지 않음 |
| 시트 닫기 막기(올리는 중) | `showAppSheet(busy:)` → `PopScope(canPop: !busy)` · 끌어 닫기 끔 | `chat/chat_kit.dart:403-438` — 미저장 닫기 확인(#16)에 쓸 수 있는 꼴 |
| iOS 권한 | `NSCameraUsageDescription` · `NSPhotoLibraryUsageDescription` · `PHPhotoLibraryPreventAutomaticLimitedAccessAlert` 있음. **문구가 채팅 목적**(「채팅으로 보낼 사진을 찍기 위해…」 · 「채팅으로 보낼 사진 · 동영상을 고르고…」) | `app/ios/Runner/Info.plist:52-57`. 시술 사진 용도를 더하면 문구 수정이 필요한지 · 심사 영향은 정할 것(§6 Q10) |
| Android 권한 | `READ_MEDIA_IMAGES` · `READ_MEDIA_VIDEO` · `READ_MEDIA_VISUAL_USER_SELECTED` · `READ_EXTERNAL_STORAGE(maxSdk 32)` · `CAMERA` 선언 없음(image_picker 카메라는 시스템 카메라 앱 인텐트) | `app/android/app/src/main/AndroidManifest.xml:5-13` |
| 스펙상 권한 | SPEC-003 §4 「알림 · 마이크만 … 카메라 · 사진은 DAY-SPEC-004 §4(직원 채팅)가 정한다」 · A-17 「알림 · 마이크 외 권한 없음(채팅 구현 뒤 DAY-SPEC-004 §4 의 카메라 · 사진 보관함만 더함)」 | SPEC-003 :933 · :1014 |

---

## 5. 스펙 대조 — 앱 차트가 지금 어떻게 적혀 있나 · 바꾸려면 어느 절

### SPEC-003 (`spec-003-mobile-app.md` @origin/main)

| 줄 | 지금 적힌 것 | 바꿀 때 닿는 곳 |
|---|---|---|
| :115 · :120 | §1 「1차 범위」 뺌 표 — 차트 작성 · 차트 API `GET /api/visits/{id}/chart` 를 뺀 목록 | 넣음으로 옮김 |
| :324 | §2 UX — 「차트 — 시술 카드를 누르면 **읽기 전용** 차트(간호 관리 차트 · 의사 차트 글 = 스냅샷 `assigneeNote` · `doctorNote` — KOS 사본). 작성 · 저장 없음 … 시술 전 의사차트는 … 안 보인다」 | 차트 U 절 다시 씀(탭 3 · 저장 · 사진) |
| :137 | Android 하단 영역 — 「폰 차트 시트」 목록 끝 여백 | 시트 → 전체 화면이면 같이 고침 |
| :596 | §3 API 계약 — `GET /api/visits/{id}/chart` 등은 「1차 앱이 부르지 않는다」 | 부르는 경로 · 새 JSON 짝 추가 |
| :930 | §4 화면 목록 — 「차트(읽기)」 | 고침 |
| :933 · A-17 :1014 | 권한 = 알림 · 마이크 + 채팅 카메라 · 사진 | 시술 사진 용도 추가 여부 |
| A-38 :1035 | 인수 조건 — 「… 차트 API 호출 0건」 | 지움 / 바꿈 |
| OQ-A30 :1113 | 웹 차트 API 를 앱에 넣을지 → 「넣지 않음」 | 다시 엶 |
| OQ-A34 :1122 | 차트 작성을 앱에서 쓸지 → 「1차 그대로」 · 「차트 작성 · 방 이동은 정해지지 않음」 | 닫음 |

### SPEC-002 (`spec-002-procedure-board.md` @origin/main)

| 줄 | 지금 적힌 것 | 바꿀 때 닿는 곳 |
|---|---|---|
| :51 개정 ㉘ ⑧ · C15 | 「범위 = 웹 차트 모달만(직원 앱 차트 · 사진은 다음 스펙)」 | 이번 작업이 그 「다음 스펙」 |
| :95 | 「직원 앱 화면은 이 SPEC 범위 밖 — DAY-SPEC-003」 | 그대로(앱 화면은 SPEC-003) |
| :450 U-16 끝 | 「직원 앱 차트 화면(DAY-SPEC-003 — 읽기 전용)에는 사진 탭이 없다 — 다음 스펙」 | 고침 |
| :646 차트 행 | 웹 `GET /board/…/chart` · 앱 `GET /api/visits/{id}/chart` | 그대로 |
| :648 차트 탭 저장 행 | 앱 짝 「**없음 — 웹만**(검수 W8 · C15 — 앱은 차트 경로를 부르지 않는다 · DAY-SPEC-003 차트 = 읽기)」 · `POST /api/visits/{id}/chart` 는 취소선 | 앱 짝 추가 |
| :650 · :652 · :654 · :656 · :657 사진 행 | 앱 짝 「없음 — 웹만(C15)」 · 「없음」 | 앱 짝 추가 |
| :688-689 권한 표 | `board` view / edit 가 차트 · 사진을 덮음(C7) | 그대로일 가능성(앱도 같은 키) |
| 규칙 23 · 31 · 39 (:1231 · :1238 · :1259) | 대상 방문 · 저장 · 사진 규칙 | 업무 규칙은 그대로 · 예약 탭 재사용이면 규칙 23(대상 방문) · 39 가 닿음 |

### SPEC-000 (`spec-000-data-model.md`)

- `visit_photo`(:1198-1217) · `external_ref.entity_type = visit_photo`(:410) — 앱이 같은 행을 쓰면 데이터 모델 변경은 없다(앱용 칸 · 테이블 언급 없음). 예약 탭에서 방문 아닌 대상에 사진을 달면 닿을 수 있음 — 확인 안 됨(WORK-002 범위).

---

## 6. 정할 것 (사용자 결정 · 추천은 한 줄)

| # | 질문 | 추천 · 근거 |
|---|---|---|
| Q1 | 앱 차트에 **시술전후사진 탭**을 둘지 | 둔다 — 목표가 「웹과 같은 기능」이고 WORK-002 가 이 사진 흐름을 다시 쓴다(브리프 §2) |
| Q2 | 차트 **저장 단위 · 버튼 자리** — 웹처럼 탭마다 [저장](탭 줄 오른쪽) · 「최근 저장」 옆 | 웹과 같게(C2 · C3 · C4) — 업무 규칙(규칙 31)이 탭 단위라 다르게 하면 서버 계약이 갈린다 |
| Q3 | **시트 vs 전체 화면**(폰) · 아이패드 가운데 창 유지 여부 | 판단 근거만: 편집 · 키보드 · 담당자 고르기 · 사진 격자가 들어가면 80% 시트 안 공간이 좁다 · 지금 시트는 탭 Navigator 에 떠서 탭바가 남는다(§1-3 ②). 추천 없음 — 시안이 정함 |
| Q4 | 시트 / 창을 **어느 Navigator** 에 띄울지 — 세션 Navigator(탭바까지 덮음 · 채팅 창과 같음) vs 지금 탭 Navigator | 세션 Navigator — 채팅이 이미 그 길(`chat_kit.dart:55-58`)이고 탭바 겹침이 없어진다 |
| Q5 | 담당자 고르기 UI(웹 `ui.staff_picker` 목록 모양) — 앱 원장 고르기 드로어(`doctor_picker.dart`) 재사용 여부 | 재사용 — 같은 「목록에서 한 명」 꼴 · 앱 DS 에 이미 있음. 시안 확인 필요 |
| Q6 | 미저장 닫기 경고 — 앱에서 닫는 길(✕ · 끌어 내림 · 뒤로 가기 제스처 · 바깥 누름)마다 어떻게 | 웹 E59 와 같은 확인 창 · 끌어 내림 / 바깥 누름은 막음(웹 「바깥 누르기는 아무 일 없음」과 같게) |
| Q7 | 백엔드 — 앱용 **새 JSON 경로**를 만들지(§3-2 의 1 ~ 5) vs 웹 HTML 경로를 Bearer · JSON 협상으로 넓힐지 | 새 `/api` 짝 — SPEC-002 개정 ② OQ-01 「웹 = HTML 조각 · JSON = 앱 전용」 · 판 조작이 이미 그 꼴(`api/board.py`) |
| Q8 | 사진 경로를 **예약 탭(WORK-002)도 부를 수 있게** 지금 설계할지 — 대상 방문(`chartable` = 오늘 판 · 시술 완료만) · 경로 위치(`/board/…` vs 방문 공통) · 권한 키(`board` vs 예약 키) | 이번 작업에서 「방문 사진」 경로를 판에 묶지 않을지만 먼저 정하고 대상 방문 확장은 WORK-002 에서 — 근거: 지금 대상 규칙은 규칙 23 에 묶여 있고(§3-4) 예약 쪽 규칙은 아직 조사 안 함 |
| Q9 | 까만 줄 · 탭바 겹침을 **차트만** 고칠지 · 같은 탭 Navigator 시트(원장 고르기 `doctor_picker.dart:93` · 확인 시트 `room_screen.dart:753`)도 같이 | 판단 근거만: 원장 고르기 · 확인 시트는 내용이 짧아 탭바 겹침이 눈에 안 띌 수 있음 — 실기기 확인 안 됨 |
| Q10 | iOS 권한 문구(카메라 · 사진 보관함)를 **시술 사진 용도까지** 넓힐지 · 심사 영향 | 넓힌다 — 지금 문구가 「채팅으로 보낼…」로 목적을 한정(`Info.plist:52-57`). 글자는 사용자 몫(문구 발명 금지) |
| Q11 | 앱 차트 **값 원천**을 스냅샷 노트 → `GET /api/visits/{id}/chart` 로 바꿀지(시술 전 의사차트 · 담당자 · `savedAt` · `base` 가 생김) · 그에 따라 SPEC-003 OQ-A34 · A-38 닫기 | 바꾼다 — 저장(충돌 판정)에 `logId` · `base` 가 필요해 스냅샷 노트만으로는 저장 요청을 못 만든다(`board_chart_parts.html:63-68`) |

그 밖에 사용자 결정은 아니나 스펙 쓸 때 맞출 사실:

- 앱 탭 글자 「간호 관리 차트」 · 「의사 차트」 ↔ 웹 「간호관리차트」 · 「의사차트」 — 다르다(`chart_sheet.dart:57` vs `board_chart_parts.html:15`).
- 앱 `copy.dart` 는 `chart_conflict` 를 「웹 전용」으로 빼 두었다(`copy.dart:22-23` · `test/core/board_messages_contract_test.dart:19`) — 앱 저장이 생기면 그 계약 시험도 닿는다.
- 사진 쪽 웹 글자 중 빈 묶음 · 크게 보기 · 「KOS 미반영」 · 버튼 이름 · aria 는 웹도 비워 둠(아이콘만 — `board_photos.html:8-10` · OQ-87 · OQ-88).
- 웹 차트 GET 이 템플릿에 넘기는 `stored_staff`(`routers/board.py:309-311`)는 `board_chart*.html` · `day.js` 에서 쓰는 곳 0(`git grep stored_staff` templates · static = 0) — JSON 에 없어도 앱 기능에 빠지는 것은 없어 보임(확인 범위는 grep 까지).

## 7. 확인 안 됨

- 실기기에서 차트 시트 마지막 칸이 끝까지 스크롤되는지(빌드 · 실행 금지).
- `/api` 경로에서 사진 쪽 `PhotoError`(413 등)가 공용 오류 모양으로 나가는지.
- 앱 로그인 세션의 KOS 토큰으로 사진 KOS 등록이 실제로 되는지(코드 읽기로는 같은 `ExternalSession` — 실물 호출 안 함 · 서버 · DB 접속 금지).
- 예약 탭 방문에 사진을 다는 데이터 모양(WORK-002 범위 · 조사 제외).

# research-1 — 예약 현황판 피드백 F1 ~ F6 원인 · 지금 동작 · 고칠 자리

- 워커: day researcher (읽기 전용) · 2026-11-27
- 코드 기준: CENTURION_DAY `origin/dev` `65506f35`(워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservations-fix` · 깨끗함). 아래 `파일:줄` 은 이 sha 의 `backend/day/` · `app/lib/` 기준
- 스펙 기준: mediness `origin/main` `d0fcc23a`(`products/day/20-spec/` 파일 9개 + `.gitkeep` — `git ls-tree` 로 셈 · 이번에 읽은 것 = spec-006 · spec-007 · spec-003(grep) · spec-000(grep) · `10-decision.md`)
- 참고: ax-clinic-project `9409e11`(CC 기획안 `130fd83`) · cc-prototype `origin/main` `0553173`
- 로컬 DB: **확인 못 함** — `docker ps` 에 떠 있는 컨테이너 없음 · 접속 값은 `deploy/local.env` 에만 있어 읽지 않음(브리프 §5). dev · prod 는 접속 안 함
- 고객 이름 · 전화 · 메모 원문은 적지 않았다

## 0. 한 줄 답

| # | F | 답 한 줄 |
|---|---|---|
| 1 | F1 | 빈 칸 클릭은 `day.js` `resSlotClick`(카드 · 띠 밖이면 그 열 · 30분 칸으로 등록 창) · 호버 점선 [+] 도 **이미 있다**(`resHintMove` · `.day-res-hint`). 카드가 칸을 꽉 채우는 원인 = 열 최소 폭이 「카드 수 × 140 + 왼쪽 10 + 오른쪽 **4px**」뿐이라, 열이 많아 `1fr` 이 안 남으면 카드 오른쪽 빈 곳이 4px → [+] 폭 계산이 0 이 되어 안 보이고 누를 자리도 없다. 툴팁 재료: 그룹 이름 = 열 머리 글자(DOM 에만 · 열 요소엔 id 만) · 칸 시작 = `slot.at` · 끝 = 지금 칸 단위 30분(그룹 간격은 숫자 칸으로 안 실림) |
| 2 | F2 | 카드 높이 = **한 줄 고정 66px**(스펙 R70 이 일부러 정함 · `day.js:2261`). 서버는 끝 분(`end_min`)을 이미 실어 보내지만 화면이 안 씀. 그룹 간격 설정 = **KOS 예약 그룹 `intervalMinutes` → `reservation_group.interval_minutes`**(DAY 에 설정 화면 없음 · 열 머리 「n명 / m분」에만 보임) — 높이에는 안 씀. KOS 끝 시각은 매퍼가 담는다(`emr/kos/mapper.py:570`). 60분인지 DB 값은 **확인 못 함** |
| 3 | F3 | [문진 QR] 은 **비활성이 아니다** — 보일 때는 늘 눌린다(`ed.qr` 이 거짓이면 아예 안 그림). 회색 바탕 버튼 모양(`.day-res-dt__ss2` · 예약 변경 · 취소와 같은 꼴)이라 꺼진 것처럼 보임. day-reservation2 「비활성」은 **day-app-re1 #295(`8fe0095a` · 11-26)에서 켜짐**(spec-007 고침 6). 누르면 메뉴 없이 바로 이 화면 QR 을 만든다. 문진 링크 = `display_request` 토큰 URL(`qrUrl`) — 웹 템플릿이 이미 받아 QR 그림으로만 씀 → 링크 복사 · 열기에 쓸 URL 은 **열린(pending) 요청이 있을 때만** 얻을 수 있다. 앱은 [문진 QR](이 기기 QR) · [태블릿에 보내기](종류 → 기기 고르기 → 바로 보냄)로 나뉨 |
| 4 | F5 | 「데스크 · 접속 중」 카드 = 기기 고르기 목록 조각 `partials/reservations_display_targets.html:5-15` 가 모달 안 빈 자리(`data-day-res-dp-targets`)에 hx 로 끼워짐. #295 에서 생김. 스펙(spec-007 §3 규칙 7)은 「**기기 팝오버**」라고 적었는데 구현이 모달 안 칸으로 넣음. 목록 = `services/displays.py:140-179` `targets()`(코디 직무 · 태블릿 · 살아 있는 세션) · 접속 = 알림 스트림 Redis 표시(25초). 여러 대면 목록에 다 뜨고 줄 = 버튼(고를 수 있음). 「미연결」 기기도 목록엔 나오지만 글자가 없을 뿐(점 없음) |
| 5 | F6 | 웹 → 서버 → 기기 → 앱 수신 코드가 **끝까지 다 있다**(앱 「태블릿 보내기」와 같은 service `displays.create` → `reach`). 코드만으로 끊긴 곳은 못 찾음. 단 **태블릿 보내기 / 받기는 앞 작업 e2e 에서 실물 확인을 안 했다**(`day-app-re1/e2e-a6-report.md:22`). 후보 = ① 목록 줄을 눌러야 보내지는데 줄이 버튼처럼 안 보임 ② QR 이 「만료」면 [태블릿에 보내기]가 안 보임(pending 일 때만) ③ 태블릿 앱이 문진 화면을 못 엶(앱 빌드 · 떠 있는 띄우기 화면 · 세션) ④ 신호 · 푸시가 안 닿음 — 실물로 확인할 것 §3.5 |
| 6 | F4 | 문진 = `questionnaire_history`(고객 id + 방문 id + `submitted_at` 제출 시각 · 작성 시작 칸 없음). 예약 상세 「초진 문진」은 **그 방문** 행이 있나로만 정함(없으면 「작성 필요」) → 재진 고객도 이번 방문에 안 냈으면 「작성 필요」 · [문진 QR] 이 다시 보임(초진 / 재진 구분 없이 줄이 늘 보임). 고객 차트는 **고객 단위**(마지막 행)로 따로 읽음 — 두 화면 기준이 다름. KOS = 고객 단위 「초진설문 n시간 전 제출」(DAY 로 동기화하는 칸 없음). cc 코드엔 유효 기간 없음 · **CC 기획안엔 「재진 기준 기간(처음 값 1년) 넘은 재진 = 다시 받기」**가 있음(기준 = 마지막 방문일) |
| 7 | 빠진 것 | §4 표 — 새 칼럼은 F4 에서도 필요 없음(고객 id · 제출 시각 이미 있음). 필요한 것 = 배치 규칙 바꿈(F2) · 열 오른쪽 여백 토큰(F1) · 툴팁에 그룹 이름 · 간격 싣기(F1) · 웹 문진 메뉴 + 링크를 내주는 길(F3) · 기기 팝오버(F5) · 6개월 판정 규칙 · 설정 값(F4) · 태블릿 실물 확인(F6) |

## 1. 정할 것 (사용자에게)

| # | 물을 것 | 선택지 | 근거 | 추천 |
|---|---|---|---|---|
| Q1 | F2 카드 높이 = 예약 길이만큼(스펙 **R70 뒤집기**)? | (a) 시작 ~ 끝 길이만큼(끝 없으면 그룹 간격) (b) 지금대로 한 줄 | R70(spec-006 :66 · :204)은 「줄 접기 R64 와 충돌」해서 높이를 고정했다. 길이만큼 늘이면 **같은 열 12:00 60분 카드와 12:30 카드가 겹친다** — 지금 자리 판정이 30분 행 하나 안에서만 lane 을 정하기 때문(`policies/reservation_layout.py:119-150`). (a) 면 자리 판정을 「시간이 겹치는 카드끼리 lane」으로 바꿔야 하고 R64 「6번째부터 아래 줄」 · 행 높이 `lines` 도 다시 정해야 함 | 사용자 피드백이 (a) — 다만 배치 규칙(R64 · R70 · R71)을 SPEC 에서 다시 정한 뒤 코드 |
| Q2 | F2 (a)일 때 한 행에 5장 넘는 경우 | (a1) 열 폭을 늘려 옆으로(lane 제한 풂) (a2) 지금처럼 아래 줄로 접고 긴 카드는 잘라 보임 | R64 가 열 폭 상한 5 를 둔 이유 = 열이 넓어지는 것 막기(spec-006 :68) | 결정 필요(추천 없음 — 실제 데이터에서 한 칸 5장 넘는 빈도 확인 안 됨) |
| Q3 | F1 툴팁의 「끝」 = 무엇? | (a) 30분(지금 칸 단위 `RES_SLOT_MIN`) (b) 그 열 그룹 간격(`interval_minutes` — 등록하면 실제로 이 길이로 만들어짐 · `services/reservation_book.py:239`) | KOS 예시 「기타 \| 12:00 ~ 12:30」은 그 그룹 간격이 30 일 때와 구별 안 됨 | (b) — 등록 결과와 툴팁이 같아짐 |
| Q4 | F1 오른쪽 여백 크기 | 카드 한 장 폭(140) 만큼 늘 남김 / 더 작은 고정 폭(KOS 처럼 점선 칸만) | 지금 `[+]` 폭 = 남은 폭과 카드 폭 중 작은 것(`day.js:3758`) · 남는 폭 4px | 결정 필요 — 시안 기준이 있으면 시안(모달 디자인 단계와 같이) |
| Q5 | F3 [문진 QR] 을 누르면 | (a) 메뉴(링크 복사하기 · 태블릿에 띄우기 · 링크 열기 — 사용자 말 그대로)만 뜨고, 고른 뒤에 요청을 만든다 (b) 지금처럼 바로 QR 을 만들고 메뉴를 붙인다 | 지금은 누르는 순간 `display_request` 1행 생성 · 같은 방문 열린 요청은 취소(`services/displays.py:279-288`). 링크는 **요청마다 새 토큰** · 10분 시한(`DAY_DISPLAY_TTL_MINUTES`) — 링크 복사 뒤 10분 지나면 고객 링크 410 | (a) — 사용자가 꼽은 세 줄에 「이 화면 QR」이 없음. 단 **이 화면 QR 을 없앨지는 따로 확인**(사용자 말에 없음) |
| Q6 | F3 「링크 복사」 링크의 수명 | 지금 10분 그대로 / 링크 복사 · 열기는 더 길게 | 문자로 보낸 링크는 10분 안에 안 열 수 있다 · 열면 쓰는 시한 60분(`DAY_QWEB_FILL_MINUTES`) | 결정 필요 |
| Q7 | F5 팝오버 줄 「미연결」 기기도 보이나 · 누를 수 있나 | (a) 보이고 누름(푸시로 닿음) (b) 보이되 못 누름 (c) 안 보임 | 지금: 미연결도 목록에 나오고 누를 수 있음 · 서버는 늘 푸시를 보냄(spec-007 규칙 3 「죽은 연결을 열린 것으로 볼 수 있어서」) · 「접속 중」 표시는 끊긴 뒤 25초까지 남음 | (a) — 지금 서버 동작 그대로 · 점 색만 |
| Q8 | F5 [여권 스캔] 의 기기 고르기도 같은 팝오버로? | 같이 / 문진만 | 두 버튼이 같은 조각 · 같은 빈 자리 꼴을 씀(`reservations_display.html:13-15 · :61 · :77`) | 같이 |
| Q9 | F4 6개월 기준일 | (a) 마지막 문진 **제출일**(`submitted_at`) (b) 마지막 **방문일**(CC 기획안 「재진 기준 기간」 방식) | DAY 에 「작성일」 칸은 없고 제출 시각만 있다. 사용자 말 「문진 작성하면 6개월 지났으면」 = 문진 날짜 기준으로 읽힘 · CC 기획안은 방문일 기준 · 처음 값 1년 | (a) 제출일 — 사용자 말과 맞고 DAY 에 칸이 있음 |
| Q10 | F4 판정 단위 | (a) 고객 단위(그 고객 마지막 문진) (b) 지금처럼 방문 단위 | 지금 예약 상세 = 방문 단위(`services/questionnaire_reads.py:35-41`) · 고객 차트 = 고객 단위(`queries/customers.py:448-456`) · KOS = 고객 단위 | (a) — 6개월 정책은 방문을 건너 이어지는 개념 |
| Q11 | F4 지난 경우 화면 | 「초진 문진」 줄 글자 · [문진 QR] 다시 보임 · 재진에도 적용 | 지금 줄 이름 「초진 문진」 · 재진에도 줄 · 버튼이 그대로 보임. 화면 글자는 지어 쓰지 않음 — 사용자 · 시안 몫 | 결정 필요(글자) · 재진 적용 = 예(6개월 정책 취지) |
| Q12 | F4 KOS 에서 낸 문진(DAY 밖)도 셀지 | 셈(KOS 에서 제출 시각을 읽어 와야 함) / DAY 저장분만 | DAY 는 KOS 문진 제출 시각을 안 읽는다(매퍼 · 픽스처에 칸 없음). KOS 응답에 그런 칸이 있는지 **확인 안 됨** | 조사 필요(KOS 호출 금지라 이번엔 못 봄) |
| Q13 | F4 6개월 값을 어디에 | 코드 상수 / 설정(env) / 병원 설정 화면 | CC 기획안은 「설정에서 정한다」 | 설정(env) — 화면은 범위 밖 |

## 2. 범위 겹침 메모

- `_RESUME` §1 의 `day-reservation3` 는 11-27 마감 · dev `65506f35`(#299 「예약 요청 스레드」)로 이미 들어감 — 이번 조사 기준 sha 가 그 뒤다. `git diff 3543d8b2 65506f35`: `reservations_parts.html` 은 오른쪽 패널 `side` 매크로만(`:137-155`) · `day.js` 바뀐 줄에 `resHint` · `resSlot` · `resLayout` · 카드 높이 관련 줄 없음 · `reservations_display*.html` · `reservations_detail.html` · `reservation_layout.py` 는 안 바뀜 → F1 ~ F6 자리와 겹치지 않음(`app.css` 는 732줄 늘었지만 예약 요청 화면 몫 — 줄 단위 대조는 안 함).

## 3. 물음별 근거

### 3.1 F1 — 예약 추가 자리

**클릭 핸들러**

- `static/day.js:3474-3490` `resSlotClick` — 누른 곳이 카드 · 띠(`[data-day-res-card], .day-res-band`) 안이면 무시 · 표에 `data-day-res-bookable` 이 있어야 함 · `resSlotAt(x, y)` 로 열 · 30분 칸을 찾아 `GET /reservations/book?date&group_id&start` 등록 창.
- `static/day.js:3054-3075` `resSlotAt` — 그 지점 아래 `[data-day-res-col]` · 30분(`RES_SLOT_MIN = 30` · `:2347`) 칸 · 회색 면이면 null. **카드 영역이 아닌 열 안 아무 곳**이면 등록이 열린다.
- `templates/partials/reservations_parts.html:98-100` — `data-day-res-bookable` = 서버 `detail_editable`(오늘 · 앞날 ∧ `reservation.detail` edit · `services/reservations.py:107`).

**이미 있는 호버 [+]**

- `templates/reservations.html:30` `<template data-day-res-hint>` · `styles/app.css:3584-3615` `.day-res-hint`(primary 점선 · 연한 바탕 · `pointer-events: none` · 글자 없음) · `static/day.js:3729-3763` `resHintMove`(mousemove).
- 자리: `lane` = 그 열에서 **시작 분이 칸 시작과 정확히 같은** 카드 수(`:3757-3759`) · `left = 10 + lane × 144` · `width = min(140, 열 폭 − 10 − 4 − lane × 144)`(`:3760-3762`) — 남은 폭이 0 이하면 폭 0(안 보임).
- 덤: 12:10 처럼 칸 중간 시작 카드는 lane 수에 안 잡혀 [+] 가 그 카드 위에 겹쳐 놓일 수 있다(같은 줄).

**카드가 칸을 꽉 채우는 원인**

- 열 폭: `static/day.js:2313-2314` `w = max(128, most × 140 + (most − 1) × 4 + 10 + 4)` → `minmax(w px, 1fr)`. 카드 1장 열 = 154px · 카드가 10 ~ 150 을 차지 → 오른쪽 4px.
- `1fr` 은 화면이 남을 때만 늘어남(`styles/app.css:3280-3285` `inline-grid` · `min-width: 100%`). 열이 많아 가로 스크롤이 생기면 모든 열이 최소 폭 → 빈 곳 4px · [+] 폭 0 · 누를 자리 없음(카드 위 클릭 = 상세 열기).
- 세로도: 카드 높이 66 + 위 2 · 행 70 → 아래 2px.
- 토큰: `styles/app.css:188-200`(`--day-res-card-w 140` · `--day-res-card-gap 4` · `--day-res-col-pad 10` · `--day-res-col-min 128` · `--day-res-card-h 66`) · 스펙 R64(spec-006 :68 · :176) 「열 폭 = 카드 수 × 폭 + 사이 · 왼쪽 여백」— 오른쪽 여백은 스펙에 없음.

**툴팁 재료**

- 그룹 이름: 열 머리 `reservations_parts.html:104` `col.title` 글자로만 있음. 열 요소(`:115`)엔 `data-day-res-col="{group_id}"` 만 → 툴팁에 쓰려면 열에 이름을 싣거나 JS 가 같은 순서의 머리를 찾아야 함.
- 그룹 간격: 머리 글자 「{정원}명 / {간격}분」(`:104`)에만 — 숫자 data 칸 없음.
- 칸 시작: `slot.at`(분) · 끝: 칸 단위 30분 가정이면 `at + 30`. 실제 등록 길이는 그룹 간격(`services/reservation_book.py:239` `end = start + interval_minutes`).
- 툴팁 장치: `day.js:335-382`(`[data-tip]` 호버 · 0.3초 지연 `data-tip-delay`). [+] 는 `pointer-events: none` 이라 이 장치로는 안 뜸 — 직접 띄우거나 이벤트를 받게 바꿔야 함.

**닿는 파일(grep 셈)**

| 찾은 이름 | 파일 수 | 파일 |
|---|---|---|
| `resHintMove` · `data-day-res-hint` · `day-res-hint` · `resHint` | 2(+ CSS 2) | `static/day.js`(3) · `templates/reservations.html`(1) · `styles/app.css` · 빌드 `static/day.css` |
| `resSlotClick` · `resSlotAt` · `data-day-res-bookable` | 3 | `static/day.js`(12) · `templates/partials/reservations_parts.html`(2) · `tests/day/web/test_reservation_detail_screen.py`(2) |
| `--day-res-card-w` · `-card-h` · `-col-pad` · `-card-gap` | 3 | `static/day.js`(12) · `styles/app.css`(7) · `static/day.css`(7 · 빌드 산출) |

### 3.2 F2 — 카드 높이

- 서버: `policies/reservations.py:199-208` `_card_span` — 끝 = `reserved_end_at`, 없으면 그 열 `interval_minutes`, 최소 30분 → `end_min` 을 카드에 실음(`:272`) · 템플릿 `reservations_parts.html:73` `data-day-res-end`.
- 화면: `static/day.js:2255-2268` — 「R70 — 높이 = 한 줄 고정(--day-res-card-h)」 · `top = 행 top + line × 70 + 2` · **`data-day-res-end` 를 안 읽음**.
- 스펙: spec-006 개정 ⑩ 보충 **R70**(:66 · U-5 :204) 「높이 = 한 줄 고정 66 · 시작 ~ 끝 길이로 늘이지 않는다(줄 접기 R64 와 충돌)」 — 앞 판(cc `spanOf` 처럼 시작 ~ 끝)을 일부러 뒤집은 결정. 결정 원천 = `reservation-board-decisions.md` R70(검수 11 뒤 · 코디 기본값).
- 자리 판정: `policies/reservation_layout.py:119-150` `seat` — 열 × **30분 행** 한 칸 안에서만 순번 → `lane = i % 5` · `line = i // 5`. `:152-164` `rows` — 행마다 `lines`. 시간 겹침(12:00 ~ 13:00 와 12:30 시작)은 판정하지 않음 → 높이만 늘이면 겹친다.
- 그룹 간격 설정: KOS 예약 그룹 `intervalMinutes`(`emr/kos/mapper.py:209`) → `reservation_group.interval_minutes`(`models/room.py:81` · 동기화 `emr/sync_master.py:163`). DAY 에 고치는 화면 없음. 화면이 쓰는 곳 = 열 머리 글자(`reservations_parts.html:104`) · 끝 없는 예약의 기본 끝(`_card_span`) · 등록 / 옮기기 끝 시각(`services/reservation_book.py:239` · `services/reservation_writes.py:182`). **카드 높이에는 안 씀.** → 사용자 질문 답: 설정(KOS 그룹 간격)은 있지만 높이는 R70 때문에 늘 한 칸.
- KOS 끝 시각: `emr/kos/mapper.py:570` `reserved_end_at = utc(reservation.endDateTime)`(없으면 null) → `emr/sync_schedules.py:295` → `models/visit.py:86`. 매퍼는 그대로 담는다.
- 60분 실제 값: **확인 못 함**(로컬 DB 안 떠 있음 · dev 금지). 사용자 화면으로 확인하는 길: 그 카드 예약 상세 「예약 일시」 끝 = `reserved_end_at` 그대로(`services/reservation_detail.py:218` · 템플릿 `reservations_detail.html:137`) — 「12:00-13:00」이면 DB 60분.

**닿는 파일(grep 셈)** — `_card_span` · `layout_rows` · `reservation_layout` · `ROW_MINUTES` · `LANES`: 4 파일(`policies/reservation_layout.py` 11 · `policies/reservations.py` 6 · `services/reservation_companions.py` 1 · `tests/day/test_reservation_layout.py` 1) + 화면 `static/day.js`(카드 높이 · 띠 · ghost `:3110-3115` · hint) · CSS 토큰. 동행 띠(`day.js:2270-2312`)는 카드 상자 위아래를 감싸므로 높이가 바뀌면 같이 바뀜 · 동행 「같은 30분 행」 규칙(R71 · `reservation_companions.py`)도 영향 확인 필요.

### 3.3 F3 — [문진 QR]

- 그리기: `templates/partials/reservations_detail.html:102` → `templates/partials/reservations_display.html:18-26` `display_buttons` — `ed.qr` 이면 `<form hx-post="/reservations/visits/{id}/display-requests" kind=questionnaire>` + `<button type=submit class="day-res-dt__ss2">문진 QR</button>` · **disabled 속성 없음**.
- 보이는 조건: `policies/reservation_detail.py:115` `qr = can_detail ∧ 오늘 ∧ 예약 · 접수 단계 ∧ 그 방문 문진 행 없음`(D55 · spec-007 :218). 조건이 거짓이면 버튼을 안 그림.
- 왜 꺼져 보이나: `styles/app.css:6174-6195` `.day-res-dt__ss2` = 회색 바탕(`--ms-gray-200`) · 회색 글자 — [예약 변경] · [예약 취소] · [여권 스캔] 도 같은 꼴(스크린샷 `f3-day-detail-modal.png` 네 버튼 같은 모양). 꺼짐 상태(`:disabled`)는 글자색만 더 흐림.
- 켜진 경위: day-reservation2 결정(11-24 「버튼 자리만 · 비활성」 · `_archive/day/day-reservation2/_RESUME.md:43`) → spec-007 **고침 6**(11-25 · :51 「D13 · D20 을 뒤집는다」) → 코드 #295 `8fe0095a`(2026-11-26 「문진 QR · 여권 스캔 · 태블릿에 보내기」 — `git log` 에서 `reservations_display.html` · `reservation_displays.py` 의 첫 커밋).
- 지금 흐름(웹): [문진 QR] → `POST display-requests`(기기 없음) → `services/displays.py:248-330` `create` 가 `display_request` 1행(10분 시한 · HMAC 토큰) → 모달 다시 그림 → `reservations_display.html:43-63` 진행 칸 = 배지 · 「고객 휴대폰 카메라로 찍어 주세요 · 남은 시간」 · QR 그림(`qr_svg(q.qrUrl)` `:56`) · [태블릿에 보내기](`:59` · pending 일 때만) · 「QR 닫기」. 메뉴는 없다.
- 링크 만드는 서버: 라우터 `routers/reservation_displays.py:102-125`(웹) · `routers/api/displays.py`(앱) → `services/displays.py:222-227` `qr_url_of`(pending 일 때만) → `policies/displays.py` `qr_url` = `{공개 origin}/q#<토큰>`(spec-007 규칙 2). 공개 페이지 · API = `routers/api/public_questionnaire.py` · `services/questionnaire_public.py`.
- 웹이 URL 을 얻나: 상세 값 `detail.displays[].qrUrl`(`services/displays.py:492-` `visit_displays` · origin 이 있고 pending 일 때) — 템플릿이 이미 갖고 있음 · 지금은 QR 그림에만 쓰고 글자 / 속성으로는 안 냄. **pending 요청이 없으면 URL 이 없다**(만료 · 취소 · 제출 뒤엔 null). 토큰은 저장 안 하고 nonce 로 다시 만든다(`:216-219`).
- 앱: `app/lib/ui/display_flows.dart:27-60` 버튼 셋 — [문진 QR](이 기기 QR 화면 · `:100-113` `createDisplay(kind)` → `showQrScreen`) · [여권 스캔](이 기기 카메라) · **[태블릿에 보내기]**(`:120-` 종류 고르기 → 기기 고르기 바텀시트 → `createDisplay(kind, deviceId)` 로 바로). 웹은 「먼저 이 화면 QR → 그 안에서 태블릿에 보내기」, 앱은 「보내기 버튼 따로 · 바로 보냄」 — 같은 service · 다른 꼴.
- KOS 메뉴(사용자 기준): `f3-kos-survey-menu.png` · KOS 사용 캡처(ax-clinic-project `para/archive/inbox_archive/2026-10-01-kos-usage-capture-raw.md:239-241`) 「[작성하기]에서 링크 보내기 · 링크 복사 · 링크 바로 열기 · QR 코드」.

**닿는 파일(grep 셈)** — `display-requests` · `displays.create` · `display_buttons` · `_targets_button`: 18 파일(코드 9 = `routers/api/displays.py` · `routers/reservation_displays.py` · `templates/partials/reservations_detail.html` · `reservations_display.html` · `reservations_display_targets.html` · `app/lib/data/reservation_api.dart` · `app/lib/model/reservation.dart` · `app/lib/state/display_inbox.dart` · `app/lib/ui/display_flows.dart` / 시험 9 = `tests/day/board/test_public_questionnaire.py` · `test_reservation_app_display_scope.py` · `test_reservation_app_displays.py` · `tests/day/web/test_reservation_detail_display_screen.py` · `test_reservation_detail_screen.py` · `app/test/state/reservation_state_test.dart` · `app/test/support/ui_harness.dart` · `app/test/ui/reservation_ui_test.dart` · `app/test/ui/scan_fix_test.dart`). 모달 디자인 단계 메모: [문진 QR] · [여권 스캔] 버튼 = `reservations_display.html` `display_buttons` · 진행 칸 = 같은 파일 `display_progress` · 「초진 문진」 · 「건강정보」 값 = 같은 파일 `questionnaire_value` · `health_value` · 줄 자리 = `reservations_detail.html:95-125`.

### 3.4 F5 — 기기 상태 카드

- 그리는 곳: `templates/partials/reservations_display_targets.html:5-15` — `<div class="day-res-dp__targets">` 안에 기기마다 `<form>` + `<button class="day-res-dp__target">{이름}{ · 접속 중}</button>` · 없으면 「띄울 수 있는 기기가 없어요 — 코디 계정으로 로그인한 기기가 보여요」.
- 끼우는 곳: `reservations_display.html:13-15` `_targets_button` = `hx-get /reservations/visits/{id}/display-targets?kind=` → `hx-target="[data-day-res-dp-targets='{kind}']"`. 빈 자리 = 문진 `:61`(진행 칸 안 · QR 아래) · 스캔 `:77`(진행 칸 밖 · 고객 정보 줄 바로 위). 라우터 `routers/reservation_displays.py:74-99`.
- 카드 모양: `styles/app.css:7405-7431` — 흰 바탕 · 회색 테두리 · 둥근 모서리 상자(카드) · 줄 버튼은 투명 바탕(호버 때만 회색). 스크린샷 `f5-day-device-card.png` 의 안쪽 회색 = 호버된 줄. 스크린샷에서 상자가 회색 진행 칸 **밖**·성명 줄 바로 위 → 모양으로는 [여권 스캔] 빈 자리(`:77`)일 가능성이 큼 — **확인 안 됨**(문진 [태블릿에 보내기]로 연 것이면 진행 칸 안에 들어간다).
- 언제 · 왜: #295 `8fe0095a`(11-26). 스펙 spec-007 §3 규칙 7(:559 · :561)은 「[태블릿에 보내기] → **기기 팝오버**」 · API 표(:510) 「200 기기 팝오버 조각」 — **스펙은 팝오버, 구현은 모달 안 칸**. 구현 쪽 결정 기록은 찾지 못함(day-app-re1 `_RESUME` §2 에 없음 · be-2 / app-2 리포트는 안 읽음 — 확인 안 됨).
- 기기 목록 원천: `services/displays.py:140-179` `targets()` — `device`(kind = tablet · 안 지움) ⋈ `login_session`(그 병원 · 안 끊김 · 안 만료) ⋈ `staff`(활성) ⋈ `job_role`(tags ∋ `coordinator`) ⋈ `account`(활성) · 이름 순. 이름 = `device.name` 비면 「태블릿」(`:136-137`). 기기 행은 앱 푸시 등록(`PUT /api/devices/{install_id}`) 때 생김 · 이름은 앱 설정 「이 기기 이름」(`PUT .../name` · #295).
- 연결 상태: `services/notification_events.py:69-96` — 앱 알림 스트림 연결이 세우는 Redis 표시(`mark_online`) · `online_sessions()` 로 읽음 · spec-007 :552 「10초마다 · 25초 표시 · 끊긴 뒤 최대 25초 남음」. 웹이 받는 값 = `{deviceId, name, online}`(`:182-183`) · 화면은 `online` 이면 「 · 접속 중」, 아니면 글자 없음.
- 여러 대: 목록에 전부 · 줄마다 form(`device_id`) → 고를 수 있음. 「미연결」 기기도 목록에 나오고 누를 수 있음(푸시로 닿을 수 있어서 · 규칙 3).
- 팝오버 부품: DAY 에 이미 팝오버 매크로가 있다 — 예: 상담사 · 관리실 고르기 `reservations_detail.html:49` `ui.pop_trigger(id)` · 필터 `reservations_parts.html:60-63`. 같은 부품을 쓸 수 있는지는 구현 판단.

**닿는 파일(grep 셈)** — `day-res-dp__targets` · `day-res-dp__target` · `data-day-res-dp-targets`: 템플릿 2(`reservations_display.html` 3 · `reservations_display_targets.html` 4) + CSS(`styles/app.css` · 빌드 `static/day.css`). `display-targets` · `displays.targets` · `DisplayTarget`: 15 파일(코드 8 · 시험 7 — 웹 1 라우터 · 앱 3 파일이 같은 목록을 씀).

### 3.5 F6 — 태블릿 전송

경로(모두 코드에 있음):

1. 웹: [문진 QR] → pending 요청 → [태블릿에 보내기](`reservations_display.html:59` · **pending ∧ qrUrl 일 때만**) → 목록 → 기기 줄 누름 = `POST /reservations/visits/{id}/display-requests`(form `kind=questionnaire` · `device_id`) (`reservations_display_targets.html:7-11`).
2. 서버: `routers/reservation_displays.py:102-125` → `services/displays.py:248-330` `create` — 기기가 목록 안이어야(아니면 404) · 오늘 ∧ 예약 · 접수(아니면 409) · 같은 방문 문진 열린 요청 취소 → 새 pending(기기 있음) → 커밋 → `signal`(웹 · 앱 예약 스트림 `display`) → `reach`(`:338-346`).
3. 닿기: `services/notification_events.py:49-66` `publish_display` — 그 계정 채널에 `session` 을 붙여 냄(그 세션 연결만) + `push.kick_task("day.notifications.display_push")` → `tasks/notifications.py:33-35` → `services/display_push.py`(APNs/FCM · kind `display`).
4. 앱 수신: 알림 스트림 이벤트 `display`(`app/lib/notify/notification_controller.dart:59-71` → `displayPing`) · 푸시(`app/lib/state/push_coordinator.dart:215-217 · 252-255` — 환경 · 병원 같을 때) → `app/lib/app.dart:105 · 206` `inbox.refill()` → `GET /api/display-requests/pending`(`services/displays.py:410-448` — **요청 세션에 이어진 기기** 앞 열린 요청) → `app/lib/state/display_inbox.dart:59-68`(문진은 qrUrl 있을 때만 큐) → `app/lib/ui/shell.dart:233-247` `_pumpDisplays`(떠 있는 띄우기 화면이 없을 때 하나씩) → `app/lib/ui/display_flows.dart:242-247` QR 전체 화면.
5. 앱 「태블릿 보내기」와 같은가: 같은 service(`displays.create` · `reach`) · 앱은 `POST /api/visits/{v}/display-requests`(`routers/api/displays.py:106`). 받는 쪽은 하나.

끊길 수 있는 후보(코드로 확정 못 함):

| 후보 | 코드 근거 | 실물로 확인할 것 |
|---|---|---|
| A. 기기 줄을 안 누름 — 목록이 떴을 뿐 아직 안 보냄 · 줄이 버튼처럼 안 보임(투명 바탕) | `reservations_display_targets.html:10` · `styles/app.css:7418-7431` | 누른 뒤 진행 칸에 「{기기}에 표시 중」(`reservations_display.html:58`)이 뜨는지 · `event_log` `display_request` 에 `deviceId` 가 있는지 |
| B. QR 이 만료 · 취소면 [태블릿에 보내기]가 없음 — 스크린샷 상세는 「만료」 | `reservations_display.html:55-60` · 시한 10분 | [문진 QR] 을 다시 누른 뒤 10분 안에 보내기 |
| C. 스캔 칸 목록을 누름(스크린샷 카드 위치가 스캔 자리 모양) — 그러면 문진이 아니라 여권 스캔 요청이 감 | `reservations_display.html:25 · :77` | 그 요청의 `display_request.kind` |
| D. 태블릿 앱이 안 엶 — 앱 빌드가 #295 앞이면 받는 코드(`display_inbox.dart`)가 없음 · 띄우기 화면이 이미 떠 있으면(`screens > 0`) 대기 · 셸 Navigator 없으면 안 엶 | `shell.dart:236-238` · `display_inbox.dart` 첫 커밋 = #295. 단 「데스크」 이름은 `PUT .../name`(#295 앱 코드)로만 붙으므로 그 태블릿은 #295 이후 빌드일 가능성 큼 | 태블릿 앱 버전 · 앱을 앞으로 가져왔을 때(`app.dart:281` 메우기) 뜨는지 |
| E. 받는 세션 불일치 — 목록은 `device.login_session_id` 세션 기준, 메우기는 **요청 세션에 이어진 기기**(`own_device`) 기준 | `services/displays.py:146-158 · 400-407` | 태블릿이 다시 로그인한 뒤 기기 행이 새 세션을 가리키는지(`device.login_session_id`) |
| F. 신호 · 푸시 둘 다 안 닿음(Redis 발행 실패는 로그만 · 푸시 환경 다름) | `notification_events.py:63-65` · `push_coordinator.dart:216`(환경 같을 때만) | dev 서버 로그 `display signal failed` · 푸시 태스크 결과 |

- 앞 작업 기록: `_archive/day/day-app-re1/e2e-a6-report.md:22` 「남은 것: … **태블릿 보내기 / 받기** — 코디 직무 계정 로그인 기기 필요」 — 실물 확인 없이 마감됨. 웹 → 태블릿 경로는 **처음 실물로 써 본 것**이 이번 피드백.

### 3.6 F4 — 문진 6개월

- 저장: `models/reception.py:96-121` `questionnaire_history` — `customer_id`(필수) · `visit_id`(null 허용) · **`submitted_at`**(제출 시각 · 필수) · `source`(`read` · `app_submit` · `web_submit` — `enums/reception.py:12-15`) · `answers` · `device_id` · `display_request_id` · KOS 보냄 상태(`crm_status` 등). 「작성 시작」 · 「작성일」 칸은 없음(제출 시각만). 쓰는 곳 = `services/questionnaire_public.py:359`(`web_submit`) — `read` 로 쓰는 코드는 이번 grep 에서 못 찾음.
- 단위: 행은 고객 + 방문 둘 다 가짐. 읽는 쪽이 갈림 — 예약 상세 = **방문**(`services/questionnaire_reads.py:35-41` `last_of(visit_id)` · `services/reservation_detail.py:166 · 177`) / 고객 차트 = **고객**(`queries/customers.py:448-456` · 화면 `templates/partials/customer_info.html:47` 「초진 설문 {제출일}」).
- 「작성 필요」 판정: `reservations_display.html:81-94` `questionnaire_value` — 그 방문 행 없음 → 「작성 필요」 · 있음 → 「제출됨 · HH:MM」. `reservations_detail.html:120` 줄 「초진 문진」은 **초진 / 재진 조건 없이 늘** 그림. [문진 QR] 도 `is_new` 를 안 봄(`policies/reservation_detail.py:115`) → 재진도 이번 방문에 안 냈으면 「작성 필요」 · 버튼 보임. 앱도 같은 값(`app/lib/ui/reservation_detail.dart:323-351`).
- KOS: 고객 차트에 「초진설문 n시간 전 제출 [보기]」 · 초진이면 「작성 안함」 + [작성하기](KOS 캡처 `:73` · `:239-241`) — **고객 단위**. DAY 는 KOS 문진 제출 여부 · 시각을 동기화하지 않는다(`emr/kos/` 매퍼 · `tests/` 픽스처에 해당 칸 없음 · 문진 KOS 경로는 공개 양식 읽기 · 제출만 `emr/kos/identity.py:29-31 · 131-165`).
- cc-prototype: 문진 유효 기간 개념 없음(`git grep` — 띄우기 시한 · QR 시한만).
- CC 기획안(ax-clinic-project `cc-기획안-예약현황-접수귀가.md:22 · 36-48` · `cc-기획안-고객.md:72 · 99 · 800 · 808`): 「초진 설문 작성 여부」 = 미작성 / **다시 받기**(마지막 방문이 재진 기준 기간을 넘은 재진 · 이번 예약에 안 냄) / 완료 · 「재진 기준 기간」 = 설정 · 처음 값 **1년** · 기준 = **마지막 방문일**. 화면 글자 「마지막 작성 {작성일}」 + 「초진 설문 QR생성」. — 사용자 말(6개월 · 문진 작성 기준)과 기간 · 기준이 다름 → Q9.
- 닿는 자리: `services/questionnaire_reads.py`(고객 단위 마지막 행 + 기한 판정) · `policies/reservation_detail.py:84-130`(`qr` 조건 · 새 「지남」 값) · `services/reservation_detail.py:166-187` · `reservations_display.html:81-104`(글자) · `reservations_detail.html:120` · 앱 `reservation_detail.dart:323-351` · 앱 JSON 짝(같은 `detail_view`) · 설정 `common/config.py`(값) · spec-007 U-3 · D55.
- 재작성 = 새 문진 링크인가: 지금 링크는 요청마다 새 토큰(문진 행은 `display_request_id` 하나에 한 행) → 다시 받기도 [문진 QR] 로 새 요청을 만들면 됨 · 새 칸 불필요.

**닿는 파일(grep 셈)** — `questionnaire_reads` · `questionnaire_done` · `questionnaire_value` · `QuestionnaireHistory`: 16 파일(코드 11 = `identifiers.py` · `models/__init__.py` · `models/reception.py` · `policies/reservation_detail.py` · `queries/customers.py` · `services/questionnaire_kos.py` · `questionnaire_public.py` · `questionnaire_reads.py` · `reservation_detail.py` · 템플릿 2 / 시험 5 = `tests/day/board/test_public_questionnaire.py` · `test_public_questionnaire_guard.py` · `tests/day/test_constraints.py` · `test_reservation_detail_rules.py` · `tests/verification/customer_scenario.py`).

## 4. 빠진 것 (고치려면 새로 필요한 것)

| F | 새로 필요한 것 | 종류 | 새 칼럼 · migration |
|---|---|---|---|
| F1 | 열 오른쪽 여백(토큰 · 열 최소 폭 식 `day.js:2313` · 스펙 R64 열 폭 식) | 화면 · 스펙 | 없음 |
| F1 | 열 요소에 그룹 이름 · 간격 싣기(`reservations_parts.html:115`) · [+] 툴팁(지금 `pointer-events: none`) | 화면 | 없음 |
| F1 | [+] lane 셈을 「같은 행 카드 수」로(지금 「시작 분 같은 카드 수」 · `day.js:3757`) | 화면 | 없음 |
| F2 | 자리 판정을 시간 겹침 기준으로(`reservation_layout.seat` · `rows`) · 카드 높이 = 길이(`day.js:2261-2266`) · 띠 · ghost · hint 높이 | 서버 정책 · 화면 · **스펙 R64 · R70 · R71 뒤집기** | 없음 |
| F3 | [문진 QR] 메뉴(팝오버 — 링크 복사하기 · 태블릿에 띄우기 · 링크 열기) | 화면 | 없음 |
| F3 | 링크 복사 · 열기용 URL 을 화면에 내기(지금 QR 그림에만) · 요청 없을 때 메뉴 고르면 요청을 만들고 URL 을 돌려주는 길(지금 `POST display-requests` 응답 = 모달 조각) | 화면 · 라우터 응답 | 없음 |
| F3 | (Q6 따라) 링크 수명 설정 | 설정 | 없음 |
| F5 | 기기 고르기 = 팝오버(스펙대로) · 줄 = 이름 + 점(초록 연결 / 빨강 미연결) · 카드 빼기 | 화면 | 없음(`online` 값 이미 있음) |
| F6 | 태블릿 실물 e2e(코디 직무 계정 · 태블릿 · dev) · 후보 A ~ F 확인 | 확인 | — |
| F4 | 고객 단위 마지막 문진 + 6개월 판정 · 「지남」 상태 값 · 화면 글자 · [문진 QR] 조건 · 재진 적용 | 서버 정책 · 화면 · 앱 · 스펙(spec-007 U-3 · D55) | **없음**(`customer_id` · `submitted_at` 있음 · 인덱스 필요 여부는 확인 안 됨) |
| F4 | (Q12 따라) KOS 문진 제출 시각 동기화 | 동기화 · 매퍼 | 아마 있음(KOS 칸 확인 뒤) |
| F4 | 6개월 값 설정 | 설정 | 없음 |

## 5. 확인 안 된 것

- F2 60분 카드의 DB `reserved_start_at` · `reserved_end_at`(로컬 DB 안 떠 있음 · dev 금지) — 사용자가 그 카드 상세 「예약 일시」 끝으로 볼 수 있음.
- F5 스크린샷 카드가 문진 칸인지 스캔 칸인지.
- F5 구현이 스펙 「팝오버」 대신 모달 안 칸을 고른 기록(be-2 · app-2 리포트 안 읽음).
- F6 실제 끊긴 곳(코드로는 경로가 다 있음).
- F4 KOS 응답에 문진 제출 시각 칸이 있는지 · `source = read` 행을 쓰는 코드가 있는지.
- `app.css` 의 day-reservation3 변경과 F1 · F5 CSS 자리 줄 단위 겹침.
- mediness `origin/main` 을 보려고 `git fetch origin main` 을 한 번 돌렸다(읽기용 ref 갱신 · checkout · pull 아님).

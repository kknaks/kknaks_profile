# research-1 — 웹 피드백 W1~W10 바꿀 표면 전수조사 · 앱 영향 (read-only)

- 기준: CENTURION_DAY `HEAD = c5045a99`(#248 · dev) — `git show HEAD:` / `git grep HEAD` 로만 읽음(작업 트리 변경 없음 · `.claude/` 미추적 1건만)
- 스펙: mediness `origin/main = de59fe3f`(2026-11-12) — `git show origin/main:`
- 피드백 원천: `orchestration/work/fix-web/e2e-feedback.md`(W1~W9 + 보충 · W10)
- 줄 번호 표기: 코드 = `경로:줄`(전부 `c5045a99` 기준), 스펙 = `spec-002:줄` = `products/day/20-spec/spec-002-procedure-board.md`, `기획-시술현황:줄` = `products/day/00-baseline/planning/데이(CC)-기획안-·-시술-현황.md`, `기획-설정:줄` = `…-·-설정.md`, `기획-개요:줄` = `데이(CC)-개요.md`, `spec-003:줄` = `spec-003-mobile-app.md`
- 결정하지 않았다. 고칠 방향은 후보로만 적고, 정할 것은 맨 끝 §정할 것에 모았다.

---

## 0. 한 장 요약

| 변경 | 판정 | 한 줄 |
|---|---|---|
| W5 확인 필요에서 accept 빼기 | **API 같이(앱 수정 불필요)** 또는 **웹만** — 고르기 | `needs()` 에서 빼면 API `cards[].needs[]` · `cards[].inbox.section` 이 같이 바뀐다. 깔린 앱은 깨지지 않지만 **앱의 「확인 필요」 칩 · 빨강 상자에서도 accept 가 사라진다**(앱 동작이 바뀜). 웹 템플릿/`inbox()` 에서만 거르면 앱은 그대로 |
| W6 시작 가능 · 시술 대기 아코디언 제거 | **웹만** | `rules.inbox()` 의 `startable`·`waiting` 목록은 웹 라우터만 쓴다. 앱은 카드별 `inbox.section` 을 쓰므로 **`inbox_section()`·`urgency` 는 지우면 앱 칩이 깨진다** |
| W7 수락함 목록 제거 | **웹만** | 템플릿 `accepted_calls` 만. API `calls[]` 에서 수락된 호출을 빼면 앱 방 상세 「수락」 이름이 비어 질 수 있다 |
| W8 방 카드 시술 줄 [수락] 제거 | **웹만** | 템플릿 `proc()` 한 곳. 사이드바 [수락]과 같은 팝오버·같은 엔드포인트 |
| W10 사이드바 need 카드 [귀가 대기] 제거 | **웹만** | 템플릿 `need_card()` 한 곳. 방 카드의 [귀가 대기](같은 엔드포인트)는 남음 |
| W2·W3 탭 이름·개수 | **웹만** | `board_regions.html:21`. 앱엔 이 탭이 없다(spec-003 개정 ⑤) |
| W4 카드 구조 | **웹만** | `need_card` · `call_card`(+`inbox_card` 를 지우지 않으면) · CSS |
| W1 오더 메모 글자 | **웹만** | `app.css:448`(+ `:161` 최대 높이) · 빌드 산출 `static/day.css` |
| W9 포커스 해제 | **웹만** | `day.js` |

푸시·알림: **확인 필요는 푸시·알림 행이 없다**(규칙 16 「알리지 않는다」). 푸시 종류는 `doctor_call`·`counselor_call`·`display`·`chat` 뿐 — accept 를 빼도 푸시 payload 영향 0.

---

## 1. 확인 필요 `accept`(수락 뒤 미시작) — 만드는 곳 · 쓰는 곳 전부

grep: `accept_min|acceptMin|"accept"|'accept'|why == "accept"|수락 뒤|BOARD_ACCEPT_MIN` (HEAD 전체)

### 만드는 곳(백엔드)
| 곳 | 무엇 |
|---|---|
| `backend/day/services/board_rules.py:38` | `NeedWhy = Literal["wait","anes","call","accept","home"]` |
| `backend/day/services/board_rules.py:381-385` | `needs()` docstring 「상황 5개」 |
| `backend/day/services/board_rules.py:408-411` | accept 상황 만들기 — `_accepted_unstarted()` + `lim.accept_min` |
| `backend/day/services/board_rules.py:420-458` | `_accepted_unstarted()`(accept 전용 헬퍼 — 다른 호출자 없음 · grep 확인) |
| `backend/day/services/board_rules.py:460-477` | `_need()` — `doctorName` 은 accept 만 채움(docstring 「doctorName 은 accept 만」) |
| `backend/day/services/board_rules.py:1063` | 스냅샷 `limits.acceptMin` |
| `backend/day/dtos/board.py:126,134,156` | `BoardLimits.accept_min = 5` · 주석 |
| `backend/day/queries/board.py:94` | `accept_min=settings.board_accept_min` |
| `backend/day/queries/board.py:318` | `doctor_changed_at` 조회 주석 「수락 뒤 미시작은 그때부터 다시 센다」(값은 accept 에만 쓰임) |
| `backend/common/config.py:181-186` | `board_accept_min`(env `BOARD_ACCEPT_MIN` · 기본 5) · 주석 |
| `backend/day/services/board.py:1003,1064` | 원장 변경 docstring 「수락 뒤 미시작은 이 시각부터 다시 센다」(동작 = `event_log task.doctor_change` 기록 — accept 를 빼도 기록은 남음) |
| `backend/day/routers/kit_board.py:51,258` | dev 견본 world — 「확인 필요 5상황」 · `w.accepts = [... m(6)]  # 수락 뒤 미시작` |

### 쓰는 곳(웹)
| 곳 | 무엇 |
|---|---|
| `backend/day/templates/partials/board_parts.html:245` | need_card 문구 `{{ item.doctorName }} 수락 {{ n }}분째` |
| `backend/day/templates/partials/board_main.html:1-2` | 조각 계약 주석(inbox{need, startable, waiting}) |
| 정렬 | `board_rules.py:479-480 _need_key` · `:1043-1047 inbox().hit_at` — why 무관 공통(accept 전용 코드 없음) |
| urgency | `board_rules.py:481-490` — **accept need 와 무관**, 대신 `has_accepted(v)` 면 2.0(`:488-489`). accept 를 needs 에서 빼도 urgency 는 그대로 |
| 섹션 | `board_rules.py:492-503 inbox_section()` — needs 가 있으면 `need`. accept 만 걸린 카드는 accept 를 빼면 **`startable`** 로 내려간다(`has_accepted`) |

### 쓰는 곳(앱)
| 곳 | 무엇 |
|---|---|
| `app/lib/model/board.dart:141` | `Need` 주석(wait·anes·call·accept·home) · `:148-156` 파서는 why 문자열 그대로(값 목록 검사 없음) |
| `app/lib/ui/format.dart:100` | `'accept' => '${n.doctorName} 수락 $m분째'` · `:102 _ => n.why`(모르는 값은 원문) |
| `app/lib/model/board.dart:158-163` | `Limits` 는 `anesMin`·`callMin` 만 읽음 — **`acceptMin` 안 읽음** |

### 테스트
| 곳 | 단언 |
|---|---|
| `backend/tests/day/board/test_board_rules.py:490-525` | accept 상황 생김/원장 변경 시 다시 셈(`:501 "why": "accept"`, `:511`, `:522`) |
| `backend/tests/day/board/test_board_rules.py:575-580` | `limits` 에 `acceptMin` |
| `backend/tests/day/board/test_board_api.py:1103-1116` | 「수락 뒤 5분 지난 카드는 원장을 바꾸면 사라진다」 · `("accept", call_id, "가원장")` |
| `backend/tests/day/web/test_board_page.py:496-512` | `whys == ["accept","anes","call","home","wait"]` · `count(...is-late) == 5` · `김도윤 수락 \d+분째` |
| `app/test/data/board_stream_test.dart:369,378` | `['wait','anes','call','accept','home']` 파싱 |
| `app/test/ui/status_box_test.dart:199-207` · `app/test/ui/app_flow_test.dart:149` · `app/test/capture/visual_capture_test.dart:168-181` · `app/test/support/fixtures.dart:307` | 앱 fixture 에 accept need · `acceptMin` |

### 알림 문구 · 설정 화면 · 시드
- 알림/푸시: **없음**. `backend/day/enums/misc.py:22-31` NotificationKind = doctor_call·counselor_call / PushKind = doctor_call·counselor_call·display·chat. `services/notifications.py:1-20` 는 원장 호출 알림만.
- 설정 화면: **없음**(env 만 · `config.py:181` 「설정 화면 없음」). 배포 env 파일(`deploy/`)에 `BOARD_*` 없음 — grep 0.
- 시드: `scripts/seed_demo_board.py` 의 `accept` 는 KOS `accept-purchase`(수납) — 무관(`:167,662`).

---

## 2. `inbox_section` 의 `startable`·`waiting` 과 스냅샷의 해당 칸 — 쓰는 곳 전부

두 층이 있다. **둘을 구분해야 한다.**

| 층 | 정의 | 누가 씀 |
|---|---|---|
| ① 카드별 `cards[].inbox = {section, urgency}` | `board_rules.py:492-503`(section) · `:481-490`(urgency) · 스냅샷 `:874` | **웹 + 앱 둘 다** (API `/api/board` · `/api/board/stream` 스냅샷에 실림) |
| ② 웹 전용 `inbox = {need, startable, waiting}` 목록 | `board_rules.py:1031-1051 inbox()` | **웹만** — `routers/board.py:154-156 board_context()`(호출 `:184,247,590`) · `routers/kit_board.py:283`. API 라우터(`routers/api/board.py:113-118`)는 `snapshot()` 만 돌려줌 |

②를 쓰는 곳: `templates/partials/board_regions.html:28-29`(아코디언) · `board_main.html:1-2`(주석) · 테스트 `test_board_api.py:91-95`(세 칸 개수 단언) · `test_board_page.py:242,427,499,954,1019` · `test_board_rules.py:559,709`(need 만).

①을 쓰는 곳:
- 앱 `app/lib/model/board.dart:178,223`(`section` 파싱) · `app/lib/ui/board_screen.dart:22-29,125,145`(칩 「전체·확인 필요·시작 가능·시술 대기」가 `section` 으로 거름) · 테스트 `app/test/ui/app_flow_test.dart:28,78,454-470` · `visual_capture_test.dart:61,110-121,193,374-377` · `fixtures.dart:214-215`
- 백엔드 테스트 `test_board_rules.py:450,592,603,609,611,694`
- 웹 템플릿에서 카드별 `inbox.section` 직접 참조: **없음**(grep `inbox.section|\.section` templates = 0). 웹은 ②만 본다.

`inbox_card` 매크로(`board_parts.html:212-227`)의 호출처 = `board_regions.html:28-29` 두 곳뿐 → W6 뒤 웹에서 쓰는 곳 0.

## 3. 수락함(`acceptedBy` 있는 call) 목록 — 웹 외에 쓰는 곳

- 웹 「수락함」: `board_regions.html:9`(`accepted_calls`) · `:37`(아코디언) · `board_parts.html:269-270`(call_card 의 수락 원장 줄 — `acceptedBy` 있을 때만 그려짐 = 수락함 칸 전용 분기) · `:277-279`(`not call.acceptedBy` 분기).
- API `calls[]`(스냅샷 `board_rules.py:880-` `calls_view()` · `acceptedBy` `:912`)는 **수락 대기 + 수락함을 같이** 싣는다.
- 앱: 「수락함」 목록 화면 **없음**(`board_screen.dart:1-2` 「호출 탭 · 시술 완료 탭 없음」). 앱이 `calls[].acceptedBy` 를 쓰는 곳 = `app/lib/ui/room_screen.dart:242`(방 상세 호출 박스 「{원장} 수락」 이름 대체값 `snap.doctorName(c.acceptedBy)`) · `app/lib/model/board.dart:352 waitingCallCount`(정의만 — lib 안 호출 0, grep 확인) · 카드 task 의 `call.acceptedBy`(`board.dart:48-71` · `board_rules.py:777`).
- 그 밖(알림·푸시·시드): 없음.
- 결론: 웹 템플릿에서만 빼면 앱 무영향. API `calls[]` 에서 수락된 호출을 빼면 앱 `room_screen.dart:242` 대체값이 비게 됨(task 쪽 `doctorName` 이 있으면 그걸 먼저 씀).

## 4. 방 카드 [수락] · 사이드바 need_card [귀가 대기](W10)

### W8 방 카드 시술 줄 [수락]
- 템플릿: `board_parts.html:91-94` — `t.state == "called"` 이고 `ACCEPT` 면 `action="수락"` · `data-day-pop="accept-{call.id}"` → `ui.proc_row(p)`(`:107`). 주석 `:95`.
- 같은 팝오버인가: **예**. 사이드바 call_card [수락] `board_parts.html:279` 도 `ui.pop_trigger("accept-" ~ call.callId)`. 팝오버 본체는 `board_regions.html:58-63`(모든 `snapshot.calls` 마다 하나) → action `/board/calls/{callId}/accept`.
- 엔드포인트: 웹 `routers/board.py:501-512`(권한 `ACCEPT_KEY = board.accept` EDIT `:508`) · 앱 `routers/api/board.py:210-219`(같은 권한).
- 권한 플래그: `board_parts.html:22 ACCEPT = _edit_of("board.accept")`.
- day.js: `static/day.js:772-773` 주석 「줄의 더보기 · [수락]」(정착 중 막기 — `.day-proc` 안 pop 트리거 일반 처리, [수락] 전용 코드 아님).
- 테스트(바뀌면 깨질 단언):
  - `test_board_page.py:96` `data-day-pop="accept-…">수락` (페이지 전체 — 사이드바 call_card 에도 있으므로 **견본 world 에 수락 대기 호출이 있으면 통과할 수 있음** · 확인 안 됨, 돌려 봐야 함)
  - `test_board_page.py:530-535` `test_판_카드_호출_줄에는_재호출이_없다` — **시술 줄 안에 [수락] 단언 → 깨짐**
  - `test_board_page.py:248-279` 권한 표 `data-day-pop="accept-"` 유무(사이드바에도 있어 영향 여부 확인 안 됨)
  - `test_board_api.py:714,729` 호출 응답(조작 응답 OOB 에 호출 탭이 포함되면 사이드바 쪽으로 통과 — 확인 안 됨)
- 스펙과 문구표: `backend/tests/architecture/test_screen_copy.py:52` 「수락」(사이드바에 남으므로 유지).

### W10 사이드바 need_card [귀가 대기]
- 템플릿: `board_parts.html:254-256` — `EDIT and item.why == "home" and card.canHome` → `hx-post="/board/visits/{visitId}/home"`.
- 같은 엔드포인트: 방 카드 액션바 [귀가 대기] `board_parts.html:178-179` 와 **같은** `/board/visits/{id}/home`(`routers/board.py:669-678`, 권한 `board` EDIT). 앱은 `routers/api/board.py:291-299`.
- 빼도 서버·권한 변경 0. 방 카드 버튼은 남음.
- 테스트: `test_board_page.py:521` `hx-post="/board/visits/{V8}/home">귀가 대기</button>' in need` → **깨짐**. `:515-516` 주석.
- 남는 사이드바 카드 버튼 = [재호출](`board_parts.html:250-253`, `why == "call"` 일 때만). wait·anes·home 카드는 버튼 없음이 된다.

## 5. 받은함 탭 이름 · 개수

- 정의: `board_regions.html:21` — `ui.tabs("inbox", [("now","현황"), ("call","호출 " ~ waiting_calls|length), ("done","시술 완료 " ~ home_count)], "now", "inbox", "인박스")`.
  - 「현황」 = **개수 없음**.
  - 「호출 n」 = `waiting_calls`(`:8` — `acceptedBy` 없는 calls) 수.
  - 「시술 완료 n」 = `home_count`(`:10` — `doneTab` 중 `state == "home"`).
- 탭 id: `ui.html:168-174 tabs()` → `id="inbox-tab-now|call|done"`. 패널 id `inbox-panel-*`. 탭 값(`now`/`call`)을 바꾸면 패널(`tab_panel`) · day.js 상태 저장(`day.js:430-431` 탭 기억) 키도 같이 바뀜 — **글자만 바꾸면 id 그대로**.
- 탭 개수의 OOB 갱신: `inbox_tabs(oob)`(`board_regions.html:20-22`) — 조작 응답에 `inbox-tabbar` 로 실림(테스트 `test_board_page.py:969,982` · `test_board_api.py:1402`).
- 테스트 단언: `test_board_page.py:64-74`(「현황」 「호출 1」 「시술 완료 1」 「확인 필요」 「시작 가능」 「시술 대기」 「수락 대기」 「수락함」 in html).
- 문구 허용표: `test_screen_copy.py:32-39`(「현황」 「호출」 「시술 완료」 「확인 필요」 「시작 가능」 「시술 대기」 「수락 대기」 「수락함」 — 근거 칸 있음). 「확인 필요」·「수락 대기」 는 이미 있다 → 새 글자 추가 불필요. 안 쓰게 되는 글자(현황·시작 가능·시술 대기·수락함)는 표에 남아도 실패하지 않음 — 테스트는 「표에 없는 글자」(`test_screen_copy.py:156-159`)와 「지운 문구 목록」(`:164-179`)만 본다. 「없앤 문구」로 막으려면 `:164` 목록에 더한다.
- dev 견본: `templates/partials/kit_page.html:142-145,441-492`(아코디언 견본) — 화면 문구 검사 대상 밖(`test_screen_copy.py:7`).

## 6. 카드 구조(W4)

### 지금 줄 구성
| 매크로 | 머리 | 본문 | 버튼 칸 |
|---|---|---|---|
| `need_card` `board_parts.html:232-259` | `ui.card_head(방 이름)`(`:238`) — 방 이름만 | ① 이름 줄 `:240`(아이콘 user-round · 이름 · 발음) ② 상태 줄 `:241-247`(`.day-line__note.is-late` 「대기 n분째」 등) | `:250-257` `.day-card__actions`([재호출] / [귀가 대기]) |
| `call_card` `board_parts.html:262-282` | `card_head(방 이름)` `:265` | ① 이름 줄 `:267` ② 시술 점 목록 `.day-dots` `:268` ③ 원장 줄 `:269-273`(수락됨 「{원장} 수락」 / 아니면 「{원장 또는 전체 의사} 호출 +mm:ss」) | `:277-280` [재호출] + [수락] |
| `inbox_card` `:213-227`(W6 뒤 미사용) | `card_head(방)` + 마취 칩 · 수납 필요 | 이름 줄 + `call_lines()`(`:194-210`) | [재호출] |

### 바뀐 구조로 갈 때 손댈 곳
- 매크로: `need_card`(`:236-249` 머리에 상태·경과를 넣고 상태 줄 삭제) · `call_card`(`:263-275` — 수락 대기 카드 머리에 「호출 · 경과」 · 시술 점 목록 · 원장 줄을 둘지 = 정할 것) · `ui.card_head`(`ui.html:194-196` — `caller()` 로 머리 오른쪽에 넣을 수 있음 · 이미 `inbox_card`·`done_card` 가 caller 로 배지를 넣음 `board_parts.html:216,289`).
- 사용자 말 「[사람이름] [재호출]」(이름 줄 오른쪽) vs 보충 「버튼은 이름 줄 한 칸 아래(지금 위치 그대로)」 — 보충이 나중 말이므로 **버튼 칸 `.day-card__actions` 위치 유지**로 읽힘(브리프 §2 도 「버튼 한 칸 아래」).
- 상태 문구 정의 위치:
  - 웹: `board_parts.html:242-246`(need: 대기/마취/호출/{원장} 수락/귀가 대기 전) · `:272`(call_card 「호출 +mm:ss」) · `:204`(call_lines 「호출 +mm:ss」 · 「재호출 +mm:ss」) · 경과 숫자 `ui.elapsed`(`ui.html:212-214`) — fmt `min`(need · 「n」) / `mmss`(call) — 1초마다 `day.js:221-224`(`data-day-since` · `data-day-format` → `fmtElapsed`).
  - 앱(참고 · 웹 변경과 무관): `app/lib/ui/format.dart:94-104 needText()`.
- W5 「상태값 = 대기 · 호출 · 귀가대기(+마취)」: 지금 need 문구 5종(`:242-246`). accept 를 빼면 `:245` 분기 삭제. 「귀가 대기 전」→「귀가대기」 로 글자를 바꿀지 = 정할 것(스펙·기획 원문은 「귀가 대기 전」 — spec-002:282 · 기획-시술현황:283).
- CSS: `styles/app.css:375-376`(`.day-card__head` · 방 카드용) · `:385`(`.day-card__body`) · `:387-388`(`.day-card__actions` — `margin-top:-4px` · 버튼 flex:1) · `:400-401`(`.day-line__note` · `.is-late` 빨강). 머리에 상태 글자를 넣으면 `.day-card__head` 안 간격·말줄임 처리 필요 여부 = 확인 안 됨(카드 폭 280 인박스).
- 테스트: `test_board_page.py:496-512`(`data-day-need-why="…">(.*?)</span></span>` 정규식이 **상태 줄 마크업 구조에 묶여 있음** — 머리로 옮기면 깨짐) · `:497-498 count('class="day-card day-card--inbox is-late"') == 5`(accept 빼면 4) · `day.js:438,474-475`(`data-day-need` 키로 새로 늦음 깜빡임 — 속성 유지하면 무영향).

## 7. W1 오더 메모 글자 · W9 카드 포커스

### W1
- 글자: `backend/day/styles/app.css:448` `.day-memo__box { … font-size: 10px; line-height: 1.3; … max-height: var(--day-memo-max-h) }` → 2pt↑ 면 12px(단위 px · 「pt」 해석 = 정할 것 아님, 피드백 「2pt 정도」).
- 최대 높이 토큰: `app.css:161` `--day-memo-max-h: 67px`(10px × 1.3 × 5줄 ≈ 65 + 여유로 보임 — 근거 주석은 확인 안 됨). 글자를 키우면 **5줄 접힘 높이가 4줄 남짓으로 줄어듦** → 같이 바꿀지 = 정할 것. 5줄 판정은 서버 `ui.html:228-235 memo()` `text.split('\n')|length > 5`(줄바꿈 수 기준 · 화면 줄 수 아님).
- 공유: `ui.memo` 호출처 = `board_parts.html:172`(방 카드) + `kit_page.html:217,285-287,529,542`(dev 견본). **다른 업무 화면 공유 없음.** 앱(Flutter)은 별도 — 무영향.
- 빌드: `static/day.css` 는 커밋된 빌드 산출(`styles/build.mjs:1-6,27` · `scripts/build-css.sh:2` 「app.css 를 바꿨으면 다시 돌리고 static/day.css 를 같이 커밋」) — `static/day.css:223,1431-1438` 에 같은 값.

### W9
- 잡는 곳: `static/day.js:775-783` — `[data-day-goto]`(인박스 카드) 클릭 → `selectCard(root, id, true)`(`:616-626` — 고른 카드 `is-selected`, 나머지 `is-dimmed`).
- 지금 풀리는 조건 **하나뿐**: 이미 고른 카드를 다시 누름(`:780-781 already → clearCards`) — 인박스 카드 재클릭 또는 고른 판 카드의 빈 곳(`:776 boardCard` = `.day-card--room.is-selected` 이고 버튼·체크·줄·팝오버 밖).
- 안 풀리는 곳: 탭 바꾸기(`selectTab` `:236-251` — `day:tab` 이벤트만 발생, 선택 해제 없음) · 카드 밖 빈 곳 클릭(처리 없음) · Escape(`:898` 은 팝오버만).
- 다시 그려도 유지: `:437`(swap 전 `state.selected` 저장) · `:472`(swap 뒤 `selectCard` 복원) — 해제 규칙을 넣으면 이 복원과 충돌하지 않게 해야 함.
- 테스트: day.js 클릭 동작 테스트는 없음(`test_board_page.py` 의 js 검사는 문자열 존재만 — `:290 근처 motionMs…`). 확인 범위: grep `is-selected` tests = 0.

## 8. 「귀가 대기 전」(home)이 확인 필요 **개수**에 세지는가

- 코드상 **세진다**:
  - 생성: `board_rules.py:412-415` — `all_done(v)`(`:130-132` 카드 시술 ≥1 · 전부 done)이면 `home` need(`limitMin 0`). 단 `needs()` 첫 줄 `:386-387` 이 `is_home(v)`(= flow_step `PROCEDURE_DONE`, `:85-86`)이면 `[]`.
  - 웹 개수 = 아코디언 「확인 필요」 `count=inbox.need|length`(`board_regions.html:27`) — `inbox.need` 는 모든 카드 `needs` 를 펼친 목록(`board_rules.py:1039`)이라 **home 포함**. 테스트 `test_board_page.py:499-502,511,521` 이 home 카드가 need 목록에 있음을 단언.
  - 앱 개수 = 칩 「확인 필요」 = `section == "need"` **카드 수**(`board_screen.dart:125` · `inbox_section` `:494-495` — needs 가 있으면 need). home 만 있는 카드도 need.
- 탭 개수와 need 목록이 같은 원천인가: **탭 「현황」에는 개수가 아예 없다**(`board_regions.html:21`). 지금 「확인 필요」 숫자는 아코디언 머리에만 있다. → 사용자가 본 「계산 안 된다」가 탭 숫자를 본 것이라면 원인은 「탭에 숫자 없음」. W3 에서 탭 숫자를 새로 만들 때 원천을 `inbox.need|length`(상황 수)로 할지 카드 수로 할지 = 정할 것(웹 아코디언 = 상황 수 · 앱 칩 = 카드 수 — **이미 웹·앱 셈 단위가 다르다**).
- 그 밖 가능성(확인 안 됨 — 실물 확인 필요):
  - [종료] 뒤 KOS 동기화가 고객 단계를 `PROCEDURE_DONE` 으로 바꾸면(`is_home`) home need 없이 판에서 빠짐. DAY [종료](`services/board.py:855-880`)는 flow_step 을 바꾸지 않음 — KOS 쪽이 자동으로 단계를 넘기는지는 확인 안 됨.
  - 「방 배정」만 남은 카드: `tasks()` 가 방 배정 작업을 빼므로(`:101-112`) 시술 0 이면 `all_done` false → home need 없음.
  - 로컬 화면 상태(사용자 본 카드의 실제 값)는 사용자 포트 금지라 확인하지 않음.

---

## 9. 앱이 쓰는 백엔드 값 (파일:줄)

API: `GET /api/board` = `snapshot()`(`routers/api/board.py:113-118`) · `GET /api/board/stream` SSE 같은 스냅샷(`:121-140`). **웹 전용 `inbox{need,startable,waiting}` 은 API 에 없다.**

| 값 | 앱 사용처 |
|---|---|
| `cards[].needs[]`(why·since·limitMin·callId·doctorName) | 파싱 `app/lib/model/board.dart:141-156,177,195,222` · 표시 `app/lib/ui/format.dart:94-104,147-148`(`callIsLate` — why=='call') · `app/lib/ui/board_screen.dart:261,332-335,400`(빨강 상자 = needs 하나라도) · `app/lib/ui/room_screen.dart:193-228`(머리 「확인할 일」 · home 은 모두 완료면 숨김 `:197-198`) |
| `cards[].inbox.section` | `board.dart:178,223` · `board_screen.dart:22-29,125`(칩 거르기·개수) |
| `cards[].inbox.urgency` | 앱 사용 0(grep `urgency` app/lib = 0) |
| `calls[]` · `acceptedBy` · `canRecall` | `board.dart:236-261,302,325,331`(`callCanRecall`) · `:352 waitingCallCount`(정의만, 사용 0) · `room_screen.dart:22,242` |
| `limits` | `board.dart:158-163`(anesMin·callMin 만) · `room_screen.dart:244,379` |
| 탭 개수 | 앱엔 탭 없음(spec-003:233-234 · `board_screen.dart:1-2`). `homeCount` `board.dart:355` 정의 |
| 푸시 payload | 원장 호출만(`services/notifications.py:63-85` TITLE 「원장 호출」 · body = 방 · 시술 n건 · 지정/전체). 확인 필요 관련 payload 없음 |
| 수락 호출 | `app/lib/state/board_controller.dart:181` `POST /api/calls/{id}/accept` |

## 10. 변경별 판정

| 변경 | 판정 | 이유 · 근거 | 「API 두고 웹에서만 감추기」 가능? |
|---|---|---|---|
| **W5 accept 빼기** | `needs()` 에서 빼면 **API 같이** · 앱 코드 수정 **불필요**(깨지지 않음) · 앱 **동작은 바뀜** | `needs()` 는 웹·API 공통 원천(`board_rules.py:380-416`). 빼면 API `needs[]` 에 accept 없음 → 앱 「확인 필요」 칩·빨강 상자·방 상세 「확인할 일」에서 accept 사라지고, accept 만 걸린 카드는 section `need`→`startable`(앱 칩 이동). 앱 파서는 값 목록을 검사하지 않음(`board.dart:148-156`) → 크래시 없음. 앱 테스트 fixture 의 accept 는 그대로 통과(서버 안 봄) | **가능.** `rules.inbox()`(`:1039`) 또는 `board_regions.html:27`/`need_card` 에서 `why == "accept"` 를 거르면 웹만 바뀌고 API·앱은 그대로. 단 그러면 **웹·앱의 확인 필요 정의가 갈라진다**(규칙 16 은 둘 공통 — spec-003:235 「앱이 다시 계산하지 않음」) |
| **W5 accept_min 설정** | API 같이(선택) | `limits.acceptMin`(`:1063`) 은 앱이 안 읽음(`board.dart:158-163`) → 지워도 앱 무영향. env `BOARD_ACCEPT_MIN`(`config.py:186`) | 남겨도 무해 |
| **W6 시작 가능·시술 대기 제거** | **웹만** | 목록 ②는 웹 라우터 전용(§2). `inbox()` 의 `startable`·`waiting` 을 지우거나 템플릿만 지우면 됨 | — (애초에 웹만) |
| W6 의 `inbox_section`·`urgency` | **건드리면 앱 수정 필요** | 앱 칩이 `section` 의 `startable`·`waiting` 으로 거름(`board_screen.dart:22-29`) | 지우지 말 것(후보) |
| **W7 수락함 제거** | **웹만** | `board_regions.html:9,37` · `call_card` 의 `acceptedBy` 분기(`:269-270`) | API `calls[]` 는 두기(앱 `room_screen.dart:242`) |
| **W8 방 카드 [수락] 제거** | **웹만** | `board_parts.html:91-94` 한 곳. 팝오버·엔드포인트·권한은 사이드바가 계속 씀 | — |
| **W10 need [귀가 대기] 제거** | **웹만** | `board_parts.html:254-256`. 엔드포인트는 방 카드·앱이 계속 씀 | — |
| W2·W3 탭 | 웹만 | `board_regions.html:21` | — |
| W4 카드 | 웹만 | 템플릿·CSS | — |
| W1 | 웹만 | CSS | — |
| W9 | 웹만 | day.js | — |

## 11. 이미 배포된 앱이 옛 API 값을 기대하는 곳

- 앱 빌드가 어느 커밋에서 나왔는지(TestFlight DAY Dev · 심사 중 0.1.0 (2))는 레포에서 확인 안 됨. `app/pubspec.yaml:5` = `0.1.0+1`(빌드 번호는 빌드 때 올린 것으로 보임 — 확인 안 됨). 아래는 HEAD 앱 코드 기준이며, 그 뒤 앱 변경이 `aa7853cd`(#238) 이후 있었는지 `git log -- app/pubspec.yaml` 로는 #238 이 마지막.
- **값을 빼는 변경(accept need 없앰 · acceptMin 없앰)**: 앱은 깨지지 않음 — `Need.parse` 는 문자열 그대로(`board.dart:149-155`) · `needText` 기본 분기 `format.dart:102` · `Limits` 는 acceptMin 안 읽음. 결과는 「accept 상황이 앱에서도 안 보임」.
- **값 모양을 바꾸는 변경은 깨짐**: `cards[].inbox.section` 의 값 이름(`need`/`startable`/`waiting`)을 바꾸거나 없애면 칩이 비거나 「전체」만 남음(`board_screen.dart:25,29`). `needs[]` 키 이름 변경도 마찬가지. `calls[]` 에서 수락된 호출을 빼면 방 상세 「{원장} 수락」 이름 대체값이 빔(`room_screen.dart:242` — 첫 대체는 task `doctorName`).
- **새 why 값을 더하면**(이번엔 해당 없음) 깔린 앱은 원문(`'xxx'`)을 그대로 보임(`format.dart:102`).
- 서버 dev·prod 배포와 앱 심사본이 같은 API 를 봄(`DAY` 메모: prod 첫 배포 · 정식 앱 심사) — prod API 에서 accept 를 빼면 **심사 중 앱 화면에서도 accept 카드가 사라진다**(크래시는 아님).

## 12. 스펙 · 기획안 정의 위치 + 이미 어긋난 곳

| 변경 | 정의 위치 |
|---|---|
| 규칙 16 확인 필요(accept 포함 5상황) | `spec-002:821-830`(규칙 16 · `:825` 수락 뒤 미시작 · `:828` 기준 분 env 「수락 분 5」) · `spec-002:859` 차이표 「상황 5개」 |
| U-10 「확인할 상황」 표 | `spec-002:262-288` — `:266` 「확인할 상황 5개」 · `:274-282` 표(`:281` 수락 뒤 미시작 행 · `:282` 귀가 대기 전 행 「카드 버튼 [귀가 대기]」 = **W10 대상**) · `:285` 카드 와이어 「방 이름 · 고객 이름 · 「확인할 일」 · 카드 버튼」 = **W4 대상** |
| 아코디언(현황 탭 세 칸) | `spec-002:264-272`(U-10 칸 표 — 확인 필요 · 시작 가능 · 시술 대기 · urgency 정의 `:270`) · `spec-002:609` 인박스 칸 분류 |
| 호출 탭 두 칸 · 「호출 n」 | `spec-002:290-293`(U-11 — 「수락 대기 n」 · 「수락함 n」 · 탭 숫자) |
| 받은함 탭 | `spec-002:163`(E16 탭 「현황 / 호출 n / 시술 완료 n」 · E17 접는 칸 머리) |
| 방 카드 [수락] | `spec-002:198`(U-3 줄 버튼 「호출 → [수락]」) · `:227`(「인박스 호출 탭의 [수락] 또는 시술 줄 [수락]」) · `:361`(흐름 예시 「인박스 시작 가능」) |
| 스냅샷 모양 | `spec-002:582`(`limits … acceptMin: 5`) · `:597`(`needs[].why` 5값 · doctorName 은 accept 만) · `:598`(`inbox.section` 3값) |
| 「확인 필요 기준 분」(설정) | `spec-002:122`(기획 CC-20-3 화면은 「안 함」 — 서버 설정) · 기획-설정 `:440-469`(CC-20-3 · `:454` 「마취 전 대기 · 마취 초과 · 받지 않은 호출 · 수락 뒤 미시작 기준 분 … 5 · 40 · 5 · 5」) · `:210,356` |
| 기획 「확인할 상황」 | 기획-시술현황 `:245-290`(1-3 · 표 `:276-283` — 기획은 **6상황**: + 「시술 변경」 · 수락 뒤 미시작 버튼 「다시 알림」 `:281` · `:267`) |
| 알림 표 | 기획-개요 `:541`(「시술 현황 확인 필요 — 「확인할 상황」 여섯」 · 알림을 띄움) · 기획-시술현황 `:253,289`(확인 필요 알림 글자) · `:171`(정책 7) |
| 앱 칩 | `spec-003:235-238`(칩 = `inbox.section` 값으로만 · 「확인 필요 카드 수」 빨강) · `:233-234`(앱엔 인박스 탭 없음) |
| W1 메모 | `spec-002:181`(E39 카드 메모 = 오더 메모) — 글자 크기 정의 없음(DS 값) |

### 스펙과 지금 코드가 이미 어긋난 곳(이번 변경과 별개로)
1. **규칙 16 「env 이름은 … 40-architecture/deployment.md env 표에 더한다」**(`spec-002:828`) — mediness `products/day/40-architecture/deployment.md` 에 `BOARD_*_MIN` 없음(grep 0). CENTURION_DAY `deploy/` 에도 없음(기본값으로만 돎).
2. **카드 셈 단위**: 웹 아코디언 「확인 필요 n」 = 상황 수(`board_regions.html:27`), 앱 칩 = 카드 수(`board_screen.dart:125`). spec-003:238 「확인 필요 카드 수」 · spec-002 는 「상황 1개 = 카드 1장」(웹 카드 = 상황). 같은 「확인 필요 n」 이 웹·앱에서 다른 수.
3. **기획 ↔ 스펙 차이(의도된 것)**: 기획은 6상황 · 알림을 띄움 · 마취 기준 40분 · 「다시 알림」 버튼 — 스펙은 5상황 · 알리지 않음 · 20분 · 버튼 없음(`spec-002:120,122,252,281,829`). 이번 W5 는 스펙에서 수락 뒤 미시작을 또 빼는 것이라 기획과 더 멀어진다.
4. 코드 주석 「확인 필요 5상황」 등 `kit_board.py:51` · `board_rules.py:381` — 스펙과는 지금 맞음.

---

## 고칠 방향 후보 (결정 아님)

- **W5**: (A) `needs()` 에서 accept 제거 + `_accepted_unstarted`·`accept_min`·`acceptMin`·env·테스트 정리 → API·앱 동작 같이 바뀜(앱 코드 수정 0, 앱 테스트 fixture 정리는 선택). (B) 서버는 두고 웹에서만 거름(`inbox()` 또는 템플릿). (C) (A) + `limits.acceptMin` 만 당분간 남김(호환).
- **W6**: 템플릿 `board_regions.html:28-29` 삭제 · `inbox()` 에서 `startable`·`waiting` 제거(또는 둠) · `inbox_card` 매크로 삭제(또는 둠). **`inbox_section`·`urgency` 는 앱용으로 유지.**
- **W7**: `board_regions.html:9,37` 삭제 · `call_card` 의 `acceptedBy` 분기 정리. API `calls[]` 유지.
- **W2·W3**: 탭 글자 `("now","확인 필요 " ~ N)` · `("call","수락 대기 " ~ waiting_calls|length)`. 아코디언이 없어지므로 목록은 `tab_panel` 바로 아래 카드 나열.
- **W4**: `need_card`·`call_card` 머리 = `card_head(방)` + caller 로 상태·경과 · 본문 = 이름 줄 · 버튼 칸 유지.
- **W8 · W10**: 템플릿 분기만 삭제 + 테스트 단언 갱신.
- **W1**: `app.css:448` 10px→12px · `:161` max-h 조정 여부 · `build-css.sh` 로 `static/day.css` 재빌드.
- **W9**: `day.js` — 탭 클릭(`selectTab` 또는 `day:tab` 이벤트)에서 `clearCards` · 문서 클릭에서 고른 카드·인박스 카드 밖이면 `clearCards`(팝오버·dialog 안 클릭은 제외) · `:437/:472` 복원 유지.
- 스펙 갱신: spec-002 규칙 16 · U-10(칸 표 · 상황 표 · 카드 와이어 · 귀가 대기 전 버튼) · U-11 · E16 · U-3 · 스냅샷 `limits`/`needs.why` · 차이표 `:859` · spec-003 칩(:235 — W6 와 무관하게 앱 칩은 그대로인지 명시).

## 정할 것

1. **W5 accept 를 앱에서도 빼나?** 서버 `needs()` 에서 빼면(API 같이) 깔린 앱·심사본에서도 accept 카드가 사라진다(크래시 없음). 웹만 거르면 웹·앱 확인 필요 정의가 갈라진다.
2. accept 를 서버에서 뺀다면 `limits.acceptMin` · env `BOARD_ACCEPT_MIN` · `_accepted_unstarted` · `doctor_changed_at` 조회(`queries/board.py:318`)도 지우나, 호환으로 남기나.
3. **W3 「확인 필요 n」 의 n = 상황 수(웹 지금 아코디언) vs 카드(고객) 수(앱 칩)?** 지금 둘이 다르다.
4. W6: `rules.inbox()` 의 `startable`·`waiting` 계산과 `inbox_card` 매크로를 코드에서 지우나, 템플릿만 지우나. (`inbox_section`·`urgency` 는 앱용 — 지우면 앱 수정 필요)
5. W5 「상태값 = 대기 · 호출 · 귀가대기」: need 카드 글자 「귀가 대기 전」(스펙·기획 원문)을 「귀가대기」로 바꾸나 그대로 두나. 마취(「마취 n분째」)는 4가지에 들어감(보충).
6. W4 `call_card`(수락 대기 카드): 머리 「룸 · 상태(호출) · 경과」로 갈 때 지금 있는 **시술 점 목록(`.day-dots`)과 원장 줄(지정 원장/전체 의사)**을 남기나 뺀나. 수락 대기 카드 버튼은 [재호출] + [수락] 둘(사이드바 [수락]은 W8 전제상 남음).
7. W4 머리 「경과값」 형식: need 카드는 지금 「n분째」(분), call 카드는 「+mm:ss」 — 하나로 맞추나.
8. W1 「2pt」: 10px→12px 로 읽나. 메모 접힘 높이(`--day-memo-max-h: 67px`)를 같이 키우나(안 키우면 4줄 남짓에서 잘림).
9. W9 「카드 밖 클릭」 범위: 판 빈 곳만인가, 인박스 빈 곳 · 헤더 등 문서 전체인가. 팝오버·창 안 클릭은 해제하지 않는 것으로 볼지.
10. 「귀가 대기가 확인 필요에 계산 안 된다」: 코드상 세짐(§8). 탭에 숫자가 없어서인지, 실물에서 home need 가 안 생겼는지(KOS 단계 자동 변경 등)는 **실물 확인 필요** — W3 구현 뒤 사용자 E2E 로 볼지, 그 전에 확인할지.
11. 스펙 갱신 범위: spec-002 만인가, spec-003(앱 칩 · `needs.why` 목록)도 같이 고치나. 기획(6상황 · 알림)과의 차이표(`spec-002:859`)에 「수락 뒤 미시작 뺌(사용자 2026-11-12)」을 남기나.

## 확인 안 됨

- 깔린 앱(TestFlight DAY Dev · 심사 0.1.0 (2))의 정확한 빌드 커밋.
- `test_board_page.py:96,279` · `test_board_api.py:714,729` 가 W8 뒤에도 사이드바 [수락] 덕에 통과하는지(돌려 봐야 함).
- KOS 가 모든 시술 완료 시 고객 단계를 자동으로 `PROCEDURE_DONE` 으로 넘기는지(§8 가능성).
- `--day-memo-max-h: 67px` 의 근거 주석.

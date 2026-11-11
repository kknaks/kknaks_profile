# 리뷰 리포트 — day-procedure-board-2 / code — CENTURION_DAY#236 v3 (2026-11-10)

대상: `CENTURION_DAY/day-procedure-board-2` 미커밋 전부(a1c90b9d 이후 · 20파일 + 새 `partials/board_action.html` · `board_regions.html`) — F1 확인 창 · F5 원장 이름 · F6 시드 생년월일 · v3 구현.
SSOT: Delivery #236 v3 ①~⑲ · A1 ~ A13 · SPEC-002 개정 ⑮(bd029f3c) · `_RESUME.md` §2 11-10 · `e2e-feedback.md` F1 ~ F8 · `code-236v3-brief.md`.
파일 경로는 `backend/` 기준(시드는 레포 루트 `scripts/`).

## 판정: WARN (FAIL 0)

v3 의 바뀐 것 ①(호출 중 줄 새 호출) · ②(재호출) · ⑰(카드 순서) · ⑱(「⋯」) · ⑲(갱신 범위)이 스펙 ⑮ · Delivery 대로 들어갔다. 서버 쪽은 API · infra 테스트가 실제로 막는다. 남은 위험은 version 신호를 건너뛰는 규칙에 있는 짧은 경쟁 창(W1)과 테스트가 문자열 단언뿐인 day.js 동작이다. 둘 다 10초 신호가 메워 오래 가지 않는다.

검증(직접 1회):
- `DAY_ENV_FILE=…/local.env scripts/test.sh -q` → **680 passed**(브리프 기준 679 + 1 · 실패 0 · 앞 단계 migration 0006 실패도 해소됨).
- `uv run ruff check` → All checks passed.
- templates 인라인 `<script>`(src 없음) 0 · `style="` 0.

## FAIL

없음.

## WARN

### W1. 조작 응답의 version 이 「다른 카드까지 봤다」로 쓰여, 바로 앞 다른 사람 변경의 신호를 건너뛸 수 있다(조용히 통과하는 자리 · 10초 안에 풀림)
- 흐름:
  - `services/board.py:321` `_finish` → 조작 뒤 `board_changed` 가 V_A 를 돌려준다.
  - `routers/board.py:203-` `_after` 는 그 값을 `version=` 으로 넘기고, 응답은 **누른 카드 + OOB 자리만** 그린다(`partials/board_action.html`).
  - `#board-version` 도 V_A 로 OOB 된다(`board_regions.html` `version(oob=true)`).
  - 화면은 그 뒤 `version <= haveVersion()` 인 신호를 GET 없이 건너뛴다(`static/day.js:503` · `:513`).
- 깨지는 경우: 다른 직원 B 가 다른 카드를 바꿔 V_B(< V_A)로 신호를 냈는데, 그 신호가 A 화면에 **A 의 조작 응답보다 늦게** 닿는 경우다. 서로 다른 연결(SSE · HTTP)이고 api 프로세스가 여럿이면 순서가 보장되지 않는다. 그러면 A 화면은 V_B ≤ V_A 라 건너뛴다. 그런데 A 의 응답은 B 의 카드를 다시 그리지 않았으므로 **B 카드 변경이 A 화면에 안 보인다.** 인박스 세 칸 · 호출 탭 · 원장 상태는 응답 OOB 가 최신 값으로 그리므로 맞다. 판의 다른 카드만 늦는다.
- 크기: SSE 10초 신호는 본문이 비어(`routers/board.py:391-` `_board_event` · 빈 값 = 늘 다시 받기) 다음 10초 안에 판 전체를 다시 받는다. 그래서 늦어도 10초다. 데이터가 틀린 채 오래 남지는 않으므로 WARN. 다만 브리프가 1순위로 본 「신호 건너뛰기가 다른 화면 갱신을 놓치는 자리」에 해당한다.
- 고치는 길(택일):
  - (가) 화면은 **자기 조작 응답의 version 과 같은 신호만** 건너뛴다(조작 응답 version 들을 따로 두고, `#board-version` 은 GET /board 로 받은 값만 올림).
  - (나) 서버가 조작 시작 때 읽은 version 과 bump 직전 값이 다르면(사이에 다른 변경이 있었으면) 응답 version 을 싣지 않는다. 그러면 자기 신호도 다시 받아 판 전체로 맞춘다.
  - 어느 쪽이든 「누른 카드만」은 지켜진다.
- 테스트 빈칸: A13 화면 쪽(가진 version 이하 신호 건너뛰기 · OOB 상태 지키기)은 `tests/day/web/test_board_page.py::test_day_js_는_가진_version_이하_신호를_건너뛰고_OOB_자리_상태를_지킨다` 의 소스 문자열 단언뿐이라 위 순서를 막지 못한다. 브라우저 확인(수동) 몫으로 적어 둘 것.

### W2. 10초 신호는 여전히 판 전체를 다시 그린다 — F8 「다른 카드가 새로고침된다」가 클릭 때는 사라지지만 10초마다는 남는다(OQ-37 범위 · 기록)
- `routers/board.py:391-` — 10초 신호 = 빈 본문 → `GET /board` → `#board-main` 통째 교체. 확인 필요 n분 · 마취 늦음 같이 시간이 지나 바뀌는 값을 위해서다(스펙 ⑮ · Delivery ⑲ 「다른 화면 … 이번엔 판 전체 다시 받기 그대로」와 맞음).
- 사용자가 F8 을 「클릭 때」로 말했으므로 범위 안이다. 다만 진행 중 카드가 10초마다 다시 그려지는 것은 남는다. 로컬 확인 때 사용자가 같은 말을 할 수 있다 — 코디가 미리 알려 둘 거리.

### W3. 끌기(PUT /board/order)가 오래된 화면 목록으로 저장되면 그 화면에 없던 카드가 맨 뒤로 간다(⑰ 「자동으로 안 바뀜」의 경쟁 예외)
- `services/board.py:978-` `order` — 보낸 `visitIds` 에 없는 저장 행은 지운다(`:1021` `stale.append(…notin_(kept))`). 그 카드는 다음 그리기 때 `_append_new_cards`(`:397-`)가 **맨 뒤로** 다시 붙인다(`on_conflict … where deleted_at is not null`).
- 화면 A 가 카드 X 가 오르기 전 판을 보고 있다가 끌어 저장하면, 이미 자리(중간 · 끝)가 저장된 X 가 맨 뒤로 간다. 대개 X 는 이미 맨 뒤라 티가 안 나지만, 그 사이 다른 사람이 X 를 앞으로 끌었다면 그 자리가 풀린다. 스펙 규칙 18 ② 「통째 바꾸기(마지막 쓰기가 이긴다)」가 이 결과를 허용하므로 WARN(기록). 줄이려면 `order` 가 「보낸 목록에 없는 살아 있는 카드」를 지우지 않고 그 뒤에 원래 순서대로 남기는 방법이 있다.

### W4. 「시작 취소」 반영 중 거절의 토스트가 「요청이 올바르지 않습니다」 — OQ-36(막기만)에 맞지만 잘못 알린다
- 서버 409 `task_start_reflecting`(제안) → `routers/board.py:110` 에 MESSAGES 행이 없어 `web_errors.py:113` 공용 폴백 「요청이 올바르지 않습니다」가 나온다. 새 글자는 0이다. 화면은 메뉴 줄을 `disabled` 로 그려(`partials/board_parts.html` `proc_menu`) 보통은 이 토스트까지 가지 않는다. 화면이 낡았거나 앱에서 보낼 때만 보인다. OQ-36 글자가 정해지면 한 줄 넣을 것.

### W5. GET(판 그리기)이 DB 에 쓴다(워커 미결 ④) — 의도이고 안전하지만 부작용 범위를 적어 둘 것
- `services/board.py:372-` `board()` → `_append_new_cards`(`:397-`): 판에 처음 오른 카드가 있으면 병원 잠금(`_lock_order` · PUT /order 와 같은 advisory xact lock) 안에서 다시 읽고 `board_card_order` 에 붙이고 commit 한다. 동시 GET 두 개는 잠금으로 줄을 서고, 둘째는 다시 읽어 붙일 것이 없으면 그냥 끝난다 → 자리 겹침 없음. 같은 날(`board_date`) 경계 · 귀가 대기 제외도 맞다.
- 부작용:
  - ① `board` view 만 있는 계정 · 앱 `GET /api/board` · 앱 SSE 스냅샷도 쓴다.
  - ② 붙인 뒤 `board_changed` 를 내지 않는다. 다른 화면은 각자 그릴 때 저장된 자리를 읽으니 순서는 같다(같은 정렬 키).
  - ③ 아무도 판을 열지 않은 동안 오른 카드들은 「같이 오른」 것으로 묶여 입실 순이 된다 — 스펙 「어느 단계(동기화 · 그리기)에서 저장하는지는 구현」이 허용한다.
  - spec-sync 때 「그리기 때 저장(GET 이 쓴다)」 한 줄을 남기기를 권한다.
- 동시 GET 둘째 쪽은 잠금 뒤 다시 읽은 결과를 버리고 앞서 읽은 world 로 그린다(`board()` 가 `False` 면 다시 읽지 않음). 정렬 키가 같아 화면 순서는 같다. 낮음.

## PASS — Acceptance(이번에 바뀐 것)

| A | 볼 것 | 코드 | 테스트 |
|---|---|---|---|
| A1 ① | pickable = 준비중 · 호출(수락 전) · 섞이면 409 `task_not_pickable` · 호출 중 줄 새 호출 → 새 호출로 옮김(사슬 아님 · `reassigned_from` 없음) · 빈 앞 호출 `closed_at` · KOS 3단계를 호출 중 작업에도(방 → 담당자 → 처음분 `call_doctors` · 다시분 `call_doctors recall=True`) | `board_rules.py` `pickable` · `services/board.py` `call`(`moved` · `_close_moved` · `_call_intents(again=moved)`) | rules `test_호출은_준비중과_호출중_재호출_수락은_닫힘_받을것없음` · `test_전체_선택은_켜진_줄이_없으면_꺼진다` · API `test_수락_진행중_완료가_섞인_호출은_task_not_pickable` · `test_호출_중_줄을_새로_호출하면_새_호출로_옮기고_앞_호출은_닫힘` · web `test_체크박스는_준비중_호출중_완료는_체크된_채_꺼짐` |
| A4 ⑩ | [재호출] = 처음 대상(사슬 맨 처음 `kind` · `target`) · 창 없음 · 호출 통째 · API `target` 안 받음(빈 본문 · `{}`만) · 판 카드 줄에 없음 · `tasks[].canRecall` 없음 · `calls[].canRecall` = 열린 · 수락 안 된 · 받을 시술 있는 호출(경과 무관) · 받지 않은 호출은 줄을 새로 호출하면 풀림 | `board_rules.py:181-193` · `services/board.py` `recall` · `routers/api/board.py` `recall` · `routers/board.py` `recall`(`_fields()` 칸 없음) | rules `test_재호출은_판_줄에_없고_수락_안_된_호출에_경과_무관` · `test_재호출_대상은_처음_호출_대상_그대로` · `test_받지_않은_호출은_그_줄을_새로_호출해_앞_호출이_닫히면_풀린다` · API `test_재호출은_대상_없이_처음_대상으로_5분_전에도` · web `test_판_카드_호출_줄에는_재호출이_없다` |
| A7 (글자 · F5) | 「원장 변경」(툴팁 · 머리 · 버튼) · 거절 「원장을 변경할 수 없습니다.」 · 원장 이름 = 평소 글자 · 호버 · 포커스 때만 옅은 배경 | `routers/board.py` MESSAGES · `ui.html` · `app.css` | `test_원장_이름_버튼은_평소_줄_글자와_같고_호버만_표시` 등 |
| A9 (F1) | 확인 창 = medikit ConfirmModal 경고형(경고 아이콘 · 가운데 제목 · [닫기] 테두리 · 빨강 채움 · DAY 크기) | `ui.html` `confirm_modal` · `app.css` | `test_확인_창은_medikit_ConfirmModal_모양` |
| A11 ⑰ | 처음 오른 카드 = 목록 맨 뒤 저장 · 같이 오르면 입실 순 · 입실 빈 카드 그 뒤 · 같으면 id · 저장 뒤 입실이 바뀌어도 · 다시 그려도 그대로 · 끌기 = 통째 · 입실 빈 카드 since = `board_card_order.created_at` · 그리는 시각(`now`)으로 자리 정하기 없앰 | `services/board.py:372-460` · `board_rules.py:495-530` · `queries/board.py`(순서 행 `created_at`) | rules `test_처음_오른_카드는_저장된_목록_뒤에_입실_순_입실_빈_카드는_그_뒤` · `test_저장된_자리는_입실_시각이_바뀌어도_그대로` · API `test_판에_처음_오른_순으로_자리를_저장하고_바뀌지_않는다`(행 · position · created_at 단언) — 동시 GET 경쟁은 테스트 없음(잠금으로 막힘 · W5) |
| A12 ⑱ | 첫 [시작] KOS op(pending · sent · `event_log task.start` 의 taskId)이 반영 중이면 `canUndoStart` false · 서버 409 `task_start_reflecting`(제안) · 반영 끝나면 켜짐 · 「⋯」는 진행 중 줄에 늘(반영 중이어도) · 메뉴 줄만 `disabled` | `queries/board.py`(`starting`) · `board_rules.py:292-301` · `board_parts.html` `proc` · `proc_menu` | rules `test_시작_쓰기가_반영_중이면_시작_취소를_막는다` · API 409(`test_board_api.py:1261`) · web `test_진행중_줄의_더보기는_반영_중에도_보이고_시작_취소만_막힌다` |
| A13 ⑲ | 조작 응답 = 누른 카드(`#card-{방문}` innerHTML · 판에서 빠지면 delete) + OOB(탭 숫자 · 현황 세 칸 · 호출 탭 · 시술 완료 목록 · 창 · version) · `HX-Reswap: none` · 권한 다시 읽음 · board 신호 본문 = version(Redis 단조 증가 · ms 기반 · 앞 값 이하면 +1 · 여러 api 프로세스는 같은 키 · Redis 없으면 본문 없음 = 늘 다시 받기) · GET 은 version 을 **읽기 전에** 정함 · 연결 첫 신호 = 지금 version · 10초 = 빈 본문 | `board_events.py:55-99` · `routers/board.py:200-` · `board_action.html` · `board_regions.html` · `day.js:470-530` | web `test_조작_응답_조각은_누른_카드와_OOB_자리뿐` · `test_판_조각은_자리_id_와_version_을_싣는다` · infra `test_웹_조작_응답은_누른_카드와_OOB_자리와_version` · SSE `test_웹_board_신호_본문은_version` · rules `test_스냅샷_version_은_판의_판` — 화면의 건너뛰기 · 상태 지키기는 문자열 단언(W1) |
| A2 · A3 글자 | E35 · 빨강 테두리 없음 · 검색 칸 「고객 · 원장 · 관리실」(placeholder · label 둘 다 결정 글자) | `board_main.html` | 기존 + copy 테스트 |

## 브리프 3 — OOB 조각 · 화면 상태 · 권한

- 상태 지키기: `htmx:oobBeforeSwap` 에서 바뀌는 자리 안의 체크 · 탭(`[data-day-tabs]` → `selectTab`) · 접힘(`aria-expanded`) · 메모 열림 · 입력 · 스크롤(카드 `data-day-keep-scroll="card-{방문}"` · 인박스)을 `keepState` 로 담고 `oobAfterSwap` 에서 돌린다(`day.js:470-497`). 호출 · 재호출이 나간 카드의 체크만 푼다(`clearOnOob`). 열린 팝오버가 그 자리 안이면 먼저 닫는다.
- 검색 중이면 「시술 완료」 목록 OOB 를 끼우지 않고 검색을 다시 청한다 — 앞 리뷰 W3(깜빡임)도 같은 방법으로 `keepState.lists` 에서 해소됐다.
- 판에서 빠지는 카드([귀가 대기]): `hx-swap-oob="delete"` 로 그 자리를 지운다. 판에 새로 오르는 카드는 조작 응답이 그리지 않는다 — 조작으로는 새 카드가 생기지 않고(동기화 몫), 동기화는 `board_changed` 신호 → 판 전체.
- 권한: `_after` 가 `sessions.grants` 를 다시 읽고 응답 조각을 같은 `EDIT` · `ACCEPT` 로 그린다. 조작 라우트 권한(view/edit · board.accept)은 그대로다.

## 브리프 4 — 시드 생년월일(F6)

- `scripts/seed_demo_board.py` `fake_birth_date`: 20 ~ 59세 · 한 실행 안에서 순번마다 다른 나이 · 월일은 순번으로 흩음 · 「실제 사람 값 아님」. 공개 API `visitorBirthDayUtc` 로 그날 자정 UTC 를 보낸다.
- 출력: 독스트링 「이름 · 전화 · 생년월일은 출력하지 않는다」 + 테스트 `test_reserve_body_carries_fake_birth_and_run_does_not_print_it`.
- 가드: `DEMO_TENANT_ID` · 데모 지점 아니면 아무것도 안 보냄 — diff 가 손대지 않았다(그대로).

## 브리프 5 · 워커 미결

- 새로 지은 화면 글자 0. 「원장 변경」 · 「원장을 변경할 수 없습니다.」 · 「고객 · 원장 · 관리실」 = 결정 58. `task_start_reflecting` 글자는 비움(OQ-36 · W4).
- 손 CSS: `app.css` 는 기존 규칙 안에서 F1 확인 창 · F5 원장 이름 · 더보기를 고쳤다(medikit · DS 토큰). `day.css` 는 빌드 결과물.
- 미결 ③(10초 신호 본문 없음): 맞는 처리다 — 시간이 지나 바뀌는 값(확인 필요 n분 · 마취 늦음)은 version 이 안 바뀌므로 본문을 비워 늘 다시 받게 했다. 덕분에 W1 의 늦음이 10초로 묶인다. 대신 W2.
- 미결 ④(GET 이 쓴다): W5.

## 직원이 실물에서 만날 자리

- 다른 사람이 막 바꾼 카드가 내 조작 직후에 최대 10초 늦게 바뀔 수 있다(W1).
- 가만히 보고 있으면 10초마다 판 전체가 다시 그려진다(W2 — 클릭 때만 사라짐).
- KOS 반영 중 진행 줄 「⋯」 → 「시작 취소」가 회색으로 눌리지 않는다. 설명 글자는 없다(OQ-36).
- 오래 열어 둔 화면에서 카드를 끌면, 그 사이 새로 오른 카드가 맨 뒤로 간다(W3).
- [재호출]은 판 카드에 없고 왼쪽 인박스 카드에만 있다(결정대로). 누르면 창 없이 바로 처음 대상에게 간다.

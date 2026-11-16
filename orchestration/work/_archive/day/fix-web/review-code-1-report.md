# 리뷰 리포트 — fix-web / code (2026-11-12)

대상: `CENTURION_DAY/fix-web` 미커밋 변경 20파일(base `origin/dev` `c5045a99`) · backend W5 + frontend W1 ~ W11.
대조: 결정 표(코디 브리프 §1 · `e2e-feedback.md` W1 ~ W11 · 결정 A) · DAY-SPEC-002 개정 ⑳(미커밋 · U-10 · U-11 · 규칙 16) · DAY-SPEC-003 개정 ⑬.
리뷰어 검증: `uv run pytest -q -m "not infra"` → **930 passed · 318 deselected** · `uv run ruff check backend` → **All checks passed**. infra 는 돌리지 않았다(아래 §6 에 영향 받는 테스트).

## 판정: FAIL (1건 — 스펙 ⑳ 과 코드 불일치 · 사용자 결정으로 어느 쪽을 맞출지만 정하면 끝)

나머지 W1 ~ W11 · 결정 A · 앱 호환은 PASS. WARN 3건.

## FAIL

### F1. 「귀가대기」 확인 필요 카드 머리에 경과(n분째)를 붙였다 — 스펙 ⑳ 은 「경과 없음」
- 코드: `backend/day/templates/partials/board_parts.html:201` — `why` 에 상관없이 `ui.elapsed(item.since, …, "min")분째` 를 배지 안에 붙인다 → 화면 「귀가대기 n분째」(since = 마지막 시술 완료 시각).
- 테스트도 이 동작을 고정: `backend/tests/day/web/test_board_page.py` `test_확인_필요_4상황_카드는_인박스에만_빨강` — `re.fullmatch(r"귀가대기\d+분째", by_why["home"])`.
- 근거: SPEC-002 U-10 「확인할 상황」 표 `home` 행(spec-002 :289) **「귀가대기(경과 없음 — 지금처럼 n 없음)」** · 결정 W4 「경과 형식은 지금 그대로」(전에는 `home` 만 n 없이 「귀가 대기 전」).
- 프론트 워커가 알고 갈랐다(`fe-1-report.md` 미결 1 — 「4상황 모두 같게 적용 · 사용자 확인 권장」). 스펙과 코드가 다르므로 FAIL.
- 고칠 방법(택 1 — 사용자 결정):
  - (a) 스펙대로: `home` 이면 배지에 경과를 빼고(`{% if item.why != "home" %}…분째{% endif %}`) 테스트를 `by_why["home"] == "귀가대기"` 로.
  - (b) 코드대로: SPEC-002 U-10 표 `home` 행 · 개정 ⑳ ③ 을 「귀가대기 · n분째(완료 뒤 분)」로 고친다.

## WARN

### W1. W9 — 다른(흐린) 카드를 누르면 고르기가 안 풀린다
- `backend/day/static/day.js:783` 제외 조건이 `[data-day-card]` 전체라서, 고르지 **않은** 판 카드(선택 중엔 `is-dimmed`)의 빈 곳 · 버튼을 눌러도 해제가 안 된다. 판 카드 빈 곳 처리(`:776` `boardCard`)는 `.is-selected` 인 카드만 보므로 흐린 카드 빈 곳 클릭은 아무 일도 없다.
- 근거: SPEC-002 U-10 「고른 카드 강조가 풀리는 때 ③ **고른 카드 밖**(문서 어디든)을 누름」 · 결정 W9 「카드 밖 클릭(문서 어디든)」. 「다른 카드 = 고른 카드 밖」으로 읽으면 빠짐이다.
- 직원 체감: 흐린 카드를 눌러 풀려고 하면 안 풀린다 → 판 바깥 여백이나 탭을 눌러야 한다.
- 제안(필요하면): 제외 조건을 `[data-day-card].is-selected`(+ 인박스 카드의 `data-day-goto` 경로는 이미 위 분기)로 좁히거나, 흐린 카드 빈 곳 클릭도 `clearCards` 로. 결정이 「아무 카드도 아닌 곳」이었다면 PASS — 코디 판단.

### W2. 화면 문구 근거 표에 지운 문구가 남아 「허용」과 「금지」에 동시에 있다
- `backend/tests/architecture/test_screen_copy.py:36` 「시작 가능」 · `:40` 「수락함」이 `VISIBLE`(근거 표)에 그대로 있고, 같은 파일 `:179-180` 지운 문구 목록에도 들어갔다. `:32` 「현황」 · `:37` 「시술 대기」도 웹 템플릿에서 사라졌는데 근거 표에 남음.
- 지금은 금지 목록이 이겨서 계약이 깨지진 않지만, 근거 표가 사실과 다르다(조용히 통과하는 자리 후보). 근거 표에서 빼는 것이 맞다(「시술 대기」는 앱 · 다른 화면 쓰임 확인 후).

### W3. 테스트 주석과 실제 확인 범위가 어긋난 자리 · 중복 줄
- `backend/tests/day/web/test_board_page.py:96-97` — 주석은 「[수락]은 인박스 수락 대기 카드에만」인데 단언은 문서 전체에서 `data-day-pop="accept-…">수락` 을 찾는다(인박스에 있어서 통과). 판에 없다는 확인은 `test_판_카드_호출_줄에는_재호출이_없다` 쪽(`'data-day-pop="accept-' not in board`)이 해서 계약은 지켜진다 — 위 단언을 `calls` 구간으로 좁히면 명확.
- 같은 테스트 끝 `board = html[...]` 줄이 두 번(무해 · 정리 거리).

## 항목별 대조 (결정 표 · 스펙 ⑳)

| 항목 | 코드 | 판정 |
|---|---|---|
| W5 / 결정 A — `needs()` 4상황 · accept 제거 | `services/board_rules.py:38`(`NeedWhy` 4값) · `:380-414`(accept 분기 · `_accepted_unstarted` 삭제) · `_need` 에서 `doctorName` 삭제 `:419-433` | PASS |
| W5 — `accept_min` · `limits.acceptMin` · env | `common/config.py:182-185`(`board_accept_min` 삭제) · `dtos/board.py:126-133` · `queries/board.py:71-75` · `board_rules.py:1011-1015`. env 파일 · deploy · scripts 에 `BOARD_ACCEPT_MIN` 없음(grep 0) | PASS |
| W5 — 원장 바꾼 시각 조회 삭제 | `queries/board.py`(`doctor_changes` · `world.doctor_changed_at` 삭제) · `dtos/board.py` `BoardWorld.doctor_changed_at` 삭제. `event_log task.doctor_change` 쓰기는 이력으로 유지(`services/board.py:1003`) | PASS(결정에 직접 없지만 accept 전용 입력이라 같이 지움이 맞음 · 넘침 아님) |
| W5 — `inbox.section` · `urgency` 유지 | `board_rules.py:439-463` 변경 없음 — accept 만 걸렸던 카드는 `startable`(SPEC-002 U-10 표 · 테스트 `test_수락_뒤_미시작은_확인_필요가_아니다`) | PASS |
| W2 탭 「수락 대기 n」 | `templates/partials/board_regions.html:23` — n = `waiting_calls|length`(지금 그대로) | PASS |
| W3 탭 「확인 필요 n」 | 같은 줄 — n = `inbox.need|length`(= 목록 카드 수) · 탭 값 now/call/done 유지 | PASS |
| W6 확인 필요 탭 목록 하나 | `board_regions.html:25-29` 아코디언 제거 · `rules.inbox()` → `{"need"}` 만(`board_rules.py:990-1003`) · `inbox_card` · `call_lines` 매크로 삭제 | PASS |
| W7 수락 대기 탭 목록 하나 | `board_regions.html:32-36` · `accepted_calls` 삭제 · API `calls[]` 그대로(`snapshot.calls` 무변경) | PASS |
| W4 need_card 구조 | `board_parts.html:195-212` — 머리 = 방 이름 + 빨강 배지(상태 글자 + n분째) / 본문 = 이름 줄 / 버튼 칸 | PASS(단 home 경과 → F1) |
| W4 상태 글자 | `board_parts.html:199` 대기 · 마취 · 호출 · 귀가대기 | PASS |
| W10 [귀가 대기] 삭제 | `board_parts.html` need_card 의 `/home` 버튼 삭제 · 버튼 = `why=="call"` [재호출] 하나 | PASS |
| W11 call_card [재호출] 삭제 | `board_parts.html:214-229` — 구조 그대로 · 버튼 [수락](ACCEPT 권한) 하나 · `acceptedBy` 분기 제거(수락된 호출은 안 오므로 맞음) | PASS |
| W8 판 시술 줄 [수락] 삭제 | `board_parts.html:91-93` — `called` 분기는 남겨 다른 버튼이 안 붙게 · 수락 팝오버는 `board_regions.html:59` 에서 그대로 그려짐(인박스 트리거가 씀) · 엔드포인트 · 권한 무변경 | PASS |
| W9 선택 해제 | `static/day.js:783-788`(문서 click) · `:912`(인박스 탭 ←→ 키) | PASS(+W1) |
| W1 오더 메모 12px · 5줄 | `styles/app.css:161`(67→80px = 12×1.3×5 + 2) · `:448`(10→12px) | PASS |
| 그대로 둠 — 시술 완료 탭 · 판 [귀가 대기] · 엔드포인트 · 권한 · migration | 변경 없음 · migration 파일 없음 | PASS |

## 앱 호환 (깔린 앱이 깨질 자리) — PASS

- `app/lib/model/board.dart:149-155` `Need.parse` — `why` 를 문자열로만 읽고 값 목록 검사 없음 · `doctorName` 은 `_s()` 로 없으면 null. 깨지지 않음.
- `board.dart:158-163` `Limits.parse` — `anesMin` · `callMin` 만 읽음(`acceptMin` 원래 안 읽음).
- `app/lib/ui/board_screen.dart:22-29` 칩 = `inbox.section` 값(`need`/`startable`/`waiting`) — 값 이름 · 모양 그대로.
- `calls[]` 모양 무변경(웹 템플릿에서만 거름).
- `app/lib/ui/format.dart:100` `'accept'` 분기는 죽은 코드가 됨(SPEC-003 ⑬ 이 명시 · 무수정 결정) — 참고.

## 「조용히 통과하는 자리」 grep 전수 — 지운 키를 아직 읽는 곳

`startable` · `waiting` · `acceptMin` · `accept_min` · `BOARD_ACCEPT_MIN` · `doctorName` · `doctor_changed_at` · `doctor_changes` · `_accepted_unstarted` · `"accept"` · `inbox_card` · `call_lines` · `inbox-startable|waiting|need` · `calls-accepted|waiting` 를 `backend` · `deploy` · `scripts` · `docs` · `.github` 전체에서 찾음:

- 남은 `startable`/`waiting` = `inbox_section()`(앱용 · 의도) · 무관한 `TaskStatus.WAITING` · outbox `waiting` · 테스트의 부재 단언(`test_board_api.py:92`)뿐.
- 남은 `"accept"` = 수락 창 모드(`ui.html:373/432` · `kit.py:199` · `board_parts.html:46`) — need why 와 무관.
- `doctorName` · `acceptMin` · `doctor_changed_at` · `inbox_card` · `call_lines` = 0건(단언용 `"acceptMin" not in` 1건 제외).
- 템플릿에서 `inbox.startable` · `inbox.waiting` 을 읽는 곳 0 — `rules.inbox()` 가 `need` 만 돌려줘도 Jinja undefined 로 조용히 비는 자리 없음.
- 남은 dead CSS: `.day-line__ok` · `.day-line--prev`(`styles/app.css:399/402`) — 견본(`kit_page.html:200/331`)이 아직 써서 dead 아님.
- 유일한 지적 = W2(근거 표) · W3(주석 범위).

## W9 day.js 상세 — PASS

- 팝오버: 트리거 클릭은 `:767-771` 에서 먼저 return · 팝오버 안은 `.day-pop` 제외 · 창: `dialog`(배경 클릭 target = dialog 자신 → 제외) · `#modal-root` 제외. 팝오버 바깥 클릭은 mousedown 에서 팝오버를 닫고 click 에서 고르기도 푼다 — 「카드 밖 클릭」이라 스펙과 맞음.
- 복원 충돌: `keepState` 는 `htmx:beforeSwap` · `oobBeforeSwap` 시점(동기)에 DOM 의 `.is-selected` 를 읽으므로(`:440` · `:503` · `:573`), 푼 뒤 오는 SSE · 조작 응답이 고르기를 되살리지 않음. `restoreState → selectTab`(`:453-454`) 경로에는 해제를 넣지 않고(`selectTab` 안이 아니라 click · keydown 에서만) OOB 탭 줄 재그림이 고르기를 풀지 않음 — 맞게 피했다.
- 탭 클릭: 탭은 카드 밖이므로 click 분기에서 풀림(인박스 외 탭 — 시술 완료 탭 등 — 클릭도 풀림 · 「문서 어디든」과 맞음). ←→ 키는 인박스 탭만 풂.
- 위임 누수: 새 리스너 없음(기존 document click · keydown 위임 안에 분기만 추가).

## W1 CSS 빌드 — PASS

- `static/day.css` 배너 `source-sha256:4f332af6…` = `shasum -a 256 backend/day/styles/app.css` 와 일치. 산출물 diff 는 sha · 80px · 12px 세 곳뿐(손 편집 흔적 없음). `tests/architecture/test_web_rules.py` 가 sha 를 지킴(non-infra 통과).

## 스펙 ⑳ 과 코드가 다른 곳

| 자리 | 스펙 ⑳ | 코드 | 판정 |
|---|---|---|---|
| 귀가대기 머리 경과 | U-10 표 `home` = 「귀가대기(경과 없음)」 | 「귀가대기 n분째」(`board_parts.html:201`) | **FAIL F1** |
| 고른 카드 밖 클릭 | 「고른 카드 밖(문서 어디든)」 | 다른 카드 위 클릭은 제외(`day.js:783`) | WARN W1 |
| 그 밖(탭 이름 · 목록 하나 · 버튼 정리 · 4상황 · 스냅샷 키 · 메모 12px) | — | 같음 | PASS |

## §6 infra 테스트 — 영향 받는 것(코디가 `scripts/test.sh` 로 확인)

- `backend/tests/day/board/test_board_api.py::test_웹_판_조각_계약` — 아코디언 개수 → 「inbox-startable/waiting 없음」으로 바뀜.
- `backend/tests/day/board/test_board_api.py::test_수락_뒤_오래_시작하지_않아도_확인_필요가_없다`(옛 `…원장을_바꾸면_수락_뒤_미시작_카드가_닫히고…` 대체).
- `backend/tests/day/board/test_board_queries.py::test_방문_1개와_10개의_쿼리_수가_같다` — 기대 16 → 15(원장 바꾼 시각 조회 삭제).
- 삭제: `test_board_queries.py::test_원장_바꾼_시각_조회는_event_log_인덱스를_탄다` — `ix_event_log_visit_id_type` 를 판이 더 안 쓰므로 맞는 삭제(인덱스 · migration 은 그대로).
- be-1-report 기준 위 세 파일 infra 포함 111/111(프론트 변경 들어간 뒤 2건 재실행) — 전체 `scripts/test.sh` 는 아직 아무도 안 돌림.

## 직원이 실물에서 만날 자리

1. 확인 필요 탭에 「귀가대기 n분째」가 보인다(F1 결정 전까지).
2. 수락 뒤 오래 시작 안 한 고객이 웹 확인 필요 · 앱 「확인 필요」 칩에서 사라지고 앱 「시작 가능」 칩으로 간다(결정 A · 의도).
3. 판 카드 호출 줄에 [수락]이 없어 수락하려면 왼쪽 「수락 대기」 탭으로 가야 한다(W8 · 의도).
4. 카드를 고른 뒤 다른(흐린) 카드를 눌러도 안 풀린다(W1).
5. 확인 필요 카드의 「귀가대기」에는 버튼이 없어 판 카드 [귀가 대기]로 가야 한다(W10 · 의도).

## 참고(기존 부채 · 무관)

- OOB 로 인박스 목록만 다시 그릴 때 `keepState(target)` 이 그 자리 안의 `.is-selected` 만 보므로, 판 카드를 고른 상태에서 인박스 카드의 흐림(`is-dimmed`)이 풀린 채 그려질 수 있다 — 이번 변경 전부터의 동작(`day.js:440` · `:510`).
- 계층 규칙(router 의 DB 직접 접근 · 모델 감추기) · 인라인 스크립트 · CDN · 비밀값: 이번 diff 에 해당 변경 없음 · 위반 없음.

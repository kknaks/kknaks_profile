# fix-web fe-1 결과 보고 — 웹 피드백 W1~W11 화면 (frontend)

## 상태: done (infra 테스트만 pending — 사유 아래)

워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix-web` · 커밋 · push 안 함. backend 워커 파일(services · queries · dtos · common · `tests/day/board/*`)은 건드리지 않았다.

## 수행 — 변경 파일

| 파일 | 무엇 |
|---|---|
| `backend/day/templates/partials/board_regions.html` | **W2 · W3** 탭 `("now", "확인 필요 " ~ inbox.need\|length)` · `("call", "수락 대기 " ~ waiting_calls\|length)` (탭 id · 값 그대로 · OOB `inbox_tabs(oob)` 도 같은 매크로라 n 일치). **W6 · W7** 아코디언 삭제 → `inbox_now` = `need_card` 나열 · `inbox_calls` = 수락 안 된 `call_card` 나열(둘 다 `.day-acc__cards` 래퍼 — 「시술 완료」 탭 `done-list` 와 같은 방식). `accepted_calls` 삭제. 빈 목록 = 빈 래퍼(새 문구 없음) |
| `backend/day/templates/partials/board_parts.html` | **W8** 시술 줄 `called` 분기에서 [수락] 삭제(분기 자체는 둬서 호출 줄에 [시작] 등이 안 붙게). **W4 · W5 · W10** `need_card` 재구성 — 머리 = `ui.card_head(방 이름)` + caller `ui.sq_badge(상태, "red", data-day-need-why)` 안에 `<span>{elapsed min}분째</span>` / 본문 = 이름 줄 / 버튼 칸 = `why == "call"` 의 [재호출] 하나. 상태 글자 대기 · 마취 · 호출 · 귀가대기. accept 분기 · [귀가 대기] 삭제. `data-day-need` · `data-day-need-why` 유지. **W11** `call_card` 구조 그대로 · [재호출] 삭제 · `acceptedBy` 분기 정리 → 버튼 [수락](ACCEPT 권한) 하나. **W6** `inbox_card` · `call_lines` 매크로 삭제(호출처 0 — grep 확인) |
| `backend/day/templates/partials/board_main.html` | 조각 계약 주석 `inbox{need}` |
| `backend/day/static/day.js` | **W9** 문서 click 위임: 인박스 · 판 카드(`[data-day-card]`) · `.day-pop` · `dialog` · `#modal-root` 밖을 누르면 `clearCards(document)` (탭 클릭 포함). 인박스 탭 ←→ 키 전환도 해제. 팝오버 트리거는 앞에서 return 이라 해제 안 됨 |
| `backend/day/styles/app.css` → `static/day.css`(재빌드) | **W1** `.day-memo__box` 10px → 12px · `--day-memo-max-h` 67 → 80px(12 × 1.3 × 5 = 78 + 여유 2 — 10px 때 65 + 2 와 같은 여유) |
| `backend/day/routers/board.py` | 모듈 docstring `inbox = {need}` |
| `backend/day/routers/kit_board.py` | 견본 world docstring 「확인 필요 4상황」 · accept 주석(수락 기록 자체는 수락된 호출 견본이라 유지) |
| `backend/day/routers/kit.py` · `templates/partials/kit_page.html` | 시술 줄 견본 호출 줄 [수락] 삭제 · 「조합 — 인박스」 견본을 새 탭 글자 · 아코디언 없는 목록 · 새 need 카드 · [수락]만 있는 수락 대기 카드로 |
| `backend/tests/day/web/test_board_page.py` | 탭 글자 · 개수(확인 필요 4 · 수락 대기 1 · 시술 완료 1) · 아코디언 없음 · 사라진 글자 · 4상황 need 카드 구조(머리 정규식 · 이름 줄 · [재호출] 1개 · [귀가 대기] 없음) · 수락 대기 카드 [수락]만 · 판 시술 줄 [수락] 없음 · 빈 inbox fixture `{"need": []}` |
| `backend/tests/architecture/test_screen_copy.py` | 근거 표에 「귀가대기」(개정 ⑳ W4) 추가 · 「확인 필요」·「수락 대기」 근거에 탭 추가 · 지운 문구 목록에 「수락함」·「시작 가능」·「귀가 대기 전」 |

## W9 — 선택 복원과 충돌 검토
- 처음엔 `selectTab` 안에서 해제했으나, 조작 응답 OOB 로 `#inbox-tabbar` 를 다시 그리면 `restoreState(tabbar)` → `selectTab` 이 불려 **판 카드 선택까지 풀리고 tabbar 안엔 카드가 없어 복원이 안 됨** → 사람이 바꿀 때(클릭 · ←→ 키)만 해제하도록 옮김.
- 다시 그릴 때 복원(`keepState` :437 → `restoreState` :472)은 DOM 의 `.is-selected` 를 읽으므로, 해제된 선택은 swap 뒤 되살아나지 않는다.

## 검증
- `uv run pytest -q backend/tests/day/web backend/tests/architecture` → **121 passed**
- `uv run pytest -q -m "not infra" backend/tests` → **930 passed, 318 deselected**(backend 워커 변경 포함 현재 워크트리)
- `uv run ruff check backend` → All checks passed · `ruff format --check` 변경 파일 OK · `node --check day.js` OK
- `scripts/build-css.sh` 1회(템플릿 변경 뒤 1회 더) → `static/day.css` diff = 메모 2값 + 원본 해시만
- 인라인 스크립트 · `style=` · `onclick` · `eval(` grep (추가된 줄 기준) → **0**. 손 CSS 0 — app.css 기존 규칙 값 2개만 바꾸고 빌드 산출물로 반영
- 견본: `/dev/kit/board`(sample_world) 전체 페이지 · HX 조각 렌더는 TestClient 테스트로 확인(4상황 · 수락 대기 1 · 시술 완료 1). 브라우저 눈 확인은 안 함(사용자 포트 금지)
- **pending**: `scripts/test.sh`(infra · PostgreSQL) — 로컬 PostgreSQL 이 사용자 `day-local` compose(127.0.0.1:11042)뿐이라 돌리지 않음. 웹 조각을 보는 infra 테스트 `test_board_api.py:711,726,1395` 는 grep 으로 새 마크업과 맞는지 확인(사이드바 수락 대기 카드 [수락]으로 통과 예상) — 코디 검증 때 실행 필요

## 계약 대조
| 항목 | 결과 |
|---|---|
| 웹 `inbox = {"need": [...]}` 만 소비 | 같음 — 템플릿은 `inbox.need` 만 읽음 |
| why ∈ {wait, anes, call, home} · doctorName 없음 | 같음 — 매핑 dict 4키(모르는 why 면 렌더 오류로 드러남) |
| 확인 필요 n = `inbox.need\|length` · 수락 대기 n = `waiting_calls\|length` | 같음 |
| 탭 id now · call · done 유지 | 같음 |
| 결정 표 W1~W11 | 전부 반영 |
| spec-002 | 개정 ⑳ 머리글은 결정 표와 같음. **본문 U-10 표(「확인할 상황 5개」 · 수락 뒤 미시작 행 · 귀가 대기 전 행 [귀가 대기] 버튼 · 「귀가 대기 전」 글자 · 시작 가능 · 시술 대기 칸) · U-11(「수락함 n」 · 탭 「호출 n」)은 아직 옛 내용**(fix-web-spec 작업 트리 기준 :264-293) — 결정 표를 따름 |

## 이슈 · 코디가 확인할 것
1. **「귀가대기」 경과**: 결정 표 「머리 = 룸 이름 · 상태 · 경과」를 4상황 모두 같게 적용 → 귀가대기도 「귀가대기 n분째」(since = 마지막 시술 완료 시각 · 서버 값). 전에는 경과 없이 「귀가 대기 전」만 있었다 — 사용자 확인 권장.
2. 머리 상태 · 경과는 `ui.sq_badge(red, solid)` 배지로 넣음(견본 kit 의 「마취」 배지 머리 패턴과 같은 클래스). 시안 없음 — 배치만 결정 표대로.
3. kit 「G4 아코디언」 컴포넌트 견본(`kit_page.html` kit-acc-1~4 · 「시작 가능」 등 라벨)은 시술 완료 탭이 아직 아코디언을 쓰므로 컴포넌트 견본으로 그대로 둠(화면 문구 검사 대상 밖).
4. `test_screen_copy.py`(architecture)는 allowed_paths 에 명시가 없지만 「귀가대기」 근거 등록 없이는 실패하므로 표만 고침.

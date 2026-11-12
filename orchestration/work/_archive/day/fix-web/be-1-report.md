# fix-web backend W5 · W6(rules.inbox) 결과 보고

## 상태: done (커밋 · push 안 함 — 워크트리에 변경만)

## 수행 — 파일

| 파일 | 변경 |
|---|---|
| `backend/day/services/board_rules.py` | `NeedWhy` 에서 `"accept"` 삭제 · `needs()` 의 수락 뒤 미시작 분기 삭제(docstring 「상황 4개」) · `_accepted_unstarted()` 삭제 · `_need()` 의 `doctor` 인자와 `doctorName` 칸 삭제 · `inbox()` → `{"need": [...]}` 만(startable · waiting 계산 삭제) · `snapshot().limits.acceptMin` 삭제 |
| `backend/day/dtos/board.py` | `BoardLimits.accept_min` 삭제 · `BoardWorld.doctor_changed_at` 삭제 |
| `backend/day/queries/board.py` | `accept_min=settings.board_accept_min` 삭제 · `doctor_changes()` 쿼리 함수 + `load_world` 의 원장 바꾼 시각 조회 삭제(판 읽기 쿼리 16 → 15) · 쓰지 않게 된 import(`Any` · `Select` · `func`) 정리. `DOCTOR_CHANGE_EVENT` 상수는 남김(`services/board.py:62,1016` 가 event_log 쓰기에 씀) |
| `backend/common/config.py` | `board_accept_min`(env `BOARD_ACCEPT_MIN`) 삭제 · 주석 정리 |
| `backend/day/services/board.py` | 주석 2곳(:1003 · :1064)에서 「수락 뒤 미시작은 이 시각부터 다시 센다」 삭제 — 동작 변경 없음(`task.doctor_change` event_log 쓰기는 그대로) |
| `backend/tests/day/board/test_board_rules.py` | `doctorName` 단언 삭제(anes · wait · home) · `test_확인_필요_수락_뒤_미시작` → `test_수락_뒤_미시작은_확인_필요가_아니다`(수락 50분 뒤에도 needs 비어 있고 section 은 `startable` · `acceptMin` 없음) · `test_원장을_바꾸면_수락_뒤_미시작은_닫히고_다시_센다` 삭제 · limits 단언 3칸 · `inbox()` 키가 `["need"]` 뿐인지 단언 추가 |
| `backend/tests/day/board/test_board_api.py` | `test_웹_판_조각_계약` — 아코디언 세 칸 개수 단언 → `inbox-startable` · `inbox-waiting` 이 없음 · `test_원장을_바꾸면_수락_뒤_미시작_카드가_닫히고_다시_센다` → `test_수락_뒤_오래_시작하지_않아도_확인_필요가_없다`(실제 DB · 수락 60분 전 → needs `[]` · section `startable`) |
| `backend/tests/day/board/test_board_queries.py` | 쿼리 수 16 → 15 · `doctor_changed_at` 단언과 seed 의 `task.doctor_change` event_log 행 삭제 · `test_원장_바꾼_시각_조회는_event_log_인덱스를_탄다` 삭제(조회 함수가 없어짐) |

## grep 전수 (손대기 전 · `git grep`)

- `accept_min` / `acceptMin` / `board_accept_min`: `config.py:186` · `dtos/board.py:134` · `queries/board.py:94` · `board_rules.py:410,411,1063` · 테스트 `test_board_rules.py:575-580` → 전부 정리. 앱 `app/test/support/fixtures.dart:307` 에도 있으나 앱 = 범위 밖(수정 안 함).
- env `BOARD_ACCEPT_MIN`: `deploy/` · `scripts/` · `*.env*` 어디에도 없음(pydantic 기본값만 썼음) → 지울 env 파일 없음.
- `_accepted_unstarted`: `board_rules.py:409,421` 만.
- `doctor_changed_at`: `dtos/board.py:159` · `queries/board.py:320` · `board_rules.py:445,447`(= `_accepted_unstarted` 안) · 테스트 `test_board_rules.py:525,528` · `test_board_queries.py:163` → **accept 에만 쓰였으므로 삭제**. `doctor_changes()` 는 `queries/board.py:319` 와 인덱스 테스트에서만 쓰였음 → 삭제.
- `"accept"` need: `board_rules.py:411` · 테스트 · 템플릿 `board_parts.html:245`(frontend 몫) · `test_board_page.py:502,509`(frontend 몫).
- `rules.inbox(` 호출부: `routers/board.py:156` · `routers/kit_board.py:283` · `tests/day/web/test_board_page.py:242,954,1019` — 셋 다 반환을 통째로 템플릿에 넘길 뿐 startable/waiting 을 직접 꺼내지 않음. 꺼내 쓰는 곳은 템플릿 `board_regions.html:28-29`(frontend 몫 — 이미 frontend 워커가 고치는 중).

## 검증

- `uv run ruff check backend/day backend/common backend/tests/day/board` → All checks passed · `ruff format --check` 통과.
- `uv run pytest -q -m "not infra" test_board_rules.py test_board_api.py test_board_queries.py` → **55 passed, 56 deselected**.
- `scripts/test.sh -q`(같은 세 파일 · infra 포함 · `DAY_ENV_FILE=~/git/CENTURION_DAY/deploy/local.env` — 이 워크트리엔 `deploy/local.env` 가 없음 · 로컬 compose postgres/redis · 테스트 스키마 · redis db 15) → 첫 실행 **109 passed · 2 failed**: ① 쿼리 수 15 ≠ 16(예상된 감소 — 기대값 고침) ② `test_웹_판_조각_계약`(그때 frontend 템플릿이 아직 아코디언을 그리고 있었음). 고친 뒤 두 테스트만 다시 돌림 → **2 passed**(frontend 의 `board_regions.html` 변경이 들어간 상태). 합계 111/111.
- 전체 스위트(`scripts/test.sh` 전부)는 돌리지 않음 — 브리프 §8 은 고친 파일만. `tests/day/web/test_board_page.py` 의 accept · 인박스 단언은 frontend 몫이라 그쪽 결과에 달림.

## 계약 대조

| 항목 | 결과 |
|---|---|
| `cards[].needs[].why` ∈ {wait, anes, call, home} | 같음 |
| `limits` 에서 `acceptMin` 삭제 | 같음 — `{waitMin, anesMin, callMin}` |
| `_need()` 의 `doctorName` 삭제 | 같음 — needs 한 장 = `{why, since, limitMin, callId}` |
| `cards[].inbox.section` · `urgency` · `calls[]` | 그대로(손대지 않음). 수락 뒤 미시작만 걸렸던 카드는 이제 `startable`(스펙 :269 와 같음) |
| 웹 `rules.inbox()` = `{"need": [...]}` 만 | 같음 |
| migration · 엔드포인트 · 권한 | 변경 없음 |

**앱 호환 근거**(`app/lib/model/board.dart`): `Need.parse`(:149-155)는 `doctorName: _s(m['doctorName'])` — `_s`(:6)는 String 이 아니면 null 이라 칸이 없어도 null. `Limits.parse`(:163)는 `anesMin` · `callMin` 만 읽고 `acceptMin` 은 원래 안 읽음. `format.dart:100` 의 `'accept'` 분기는 그 값이 안 와서 안 쓰임(죽은 코드 · 앱 수정 금지라 그대로).

## 스펙과 다른 곳(결정 표가 맞음 — planner 확인용)

- `spec-002` :611 — `needs[]` 에 `doctorName` 을 아직 적고 「칸을 남길지 뺄지 OQ-55」라고 열어 둠. 브리프 계약대로 **뺐다** → OQ-55 닫고 :611 에서 `doctorName` 지울 것.
- 개정 ⑳ 을 반영하지 않은 옛 문구: :839(규칙 16 의 「수락 뒤 미시작」 bullet 이 취소선 없이 남음) · :854(규칙 27 「수락 뒤 미시작 카드는 닫히고 다시 센다」) · :858(규칙 31 「「수락 뒤 미시작」 다시 셈」) · :873(cc 와 다른 곳 「상황 5개」).

## frontend 몫으로 넘긴 것 · 주의점

- `templates/partials/board_parts.html:245`(`item.why == "accept"` 글자) · `board_regions.html` 인박스 칸 · `routers/kit_board.py`(dev 견본 accept 데이터) · `tests/day/web/test_board_page.py:427`(`inbox={"need":[], "startable":[], "waiting":[]}`) · `:502,509`(accept 문구 단언) — 모두 frontend 몫, 건드리지 않음.
- migration 0006 의 `ix_event_log_visit_id_type` 인덱스는 이제 판 읽기에서 쓰지 않는다(쓰기만 남음). migration 금지라 그대로 둠 — 지울지는 나중 판단.
- `task.doctor_change` event_log 쓰기는 그대로(원장 변경 이력).

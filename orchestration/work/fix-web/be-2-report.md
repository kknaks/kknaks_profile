# fix-web backend E3 — 판 스냅샷 `cards[].counselors` 결과 보고

## 상태: done (커밋 · push 안 함 — 1차 변경 위에 워크트리 변경만)

## 수행 — 파일

| 파일 | 변경 |
|---|---|
| `backend/day/dtos/board.py` | `BVisit.counselor_ids: tuple[uuid.UUID, ...] = ()` (`order_memo` 옆) |
| `backend/day/queries/board.py` | `load_world` — 방문 id 들의 상담을 **쿼리 1번**으로 읽음: `consultation` 에서 `visit_id IN (...)` · `deleted_at IS NULL` · `counselor_id IS NOT NULL` · `ORDER BY started_at ASC NULLS LAST, created_at, id` → 방문별로 처음 나온 순서대로 중복을 뺀 tuple 을 `BVisit` 에 넣음. 방문이 없으면 쿼리 안 함. `Consultation` import 추가 |
| `backend/day/services/board_rules.py` | `card_view` — `"orderMemo"` 바로 뒤에 `"counselors": [{"staffId", "name"}]`. 이름은 이미 읽는 `world.staff` 에서 가져옴(병원 직원 · `deleted_at IS NULL` · **비활성 포함**). 판 직원 목록에 없는(지운) 직원은 뺌 = 지금 판 규칙. 없으면 `[]` |
| `backend/tests/day/board/test_board_rules.py` | 단위 1건 — 순서 그대로 이름 붙임 · 모르는 직원 id 는 뺌 · 상담사 없으면 `[]` |
| `backend/tests/day/board/test_board_api.py` | infra 1건 `test_카드_상담사는_방문의_상담_전부_시작_순_중복_없이` — 실제 DB · `/api/board`: 처음엔 `[]` → 상담 7개(같은 상담사 2번 · 지운 상담 · started_at 없음 · counselor 없음 · 지운 직원 · 비활성 직원)를 넣으면 `[가상담(60분 전), 나상담(비활성 · 30분 전), 라상담(시작 없음 → 뒤)]` |
| `backend/tests/day/board/test_board_queries.py` | `add_full_visits` 방문마다 상담 1개 · 쿼리 수 15 → **16** (방문 1개 · 10개 같음 단언은 그대로 — N+1 없음) |

손대지 않음: `emr/`(동기화) · 모델 · migration · 앱 · 템플릿 · static · styles · routers.

## 검증

- `uv run ruff check backend/day backend/tests/day/board` → All checks passed · `ruff format` 통과.
- `DAY_ENV_FILE=/Users/kknaks/git/CENTURION_DAY/deploy/local.env scripts/test.sh -q test_board_rules.py test_board_api.py test_board_queries.py`(로컬 compose · 테스트 스키마) → 첫 실행 **112 passed · 1 failed**(새 infra 테스트의 테스트 코드 실수 — `Staff(**over)` 키 중복). 고친 뒤 그 테스트만 다시 → **1 passed**. 합계 113/113.

## 계약 대조

| 항목 | 결과 |
|---|---|
| `cards[].counselors: [{"staffId": str, "name": str}]` · 없으면 `[]` · `orderMemo` 옆 | 같음 |
| 상담(삭제 안 됨) 전부의 `counselor_id` · 중복 제거 · 상담 시작 순 | 같음 — 같은 시각이면 `created_at` → `id`. **`started_at` 이 없는 상담은 맨 뒤**(브리프가 정하지 않아서 고름 — 다르면 알려 달라) |
| 희망 상담사(`requested_counselor_id`) 안 씀 · 상담 의사 안 씀 | 같음 |
| 비활성 직원도 이름 | 같음(`world.staff` 는 `is_active` 와 상관없이 읽음) |
| 지운 직원 | 뺌 — 판 직원 조회(`Staff.deleted_at IS NULL`) 규칙 그대로 |
| 쿼리 수가 방문 수와 무관 | 같음 — 상담 쿼리 1번 · 16(방문 1 = 10) |
| 앱 | 변경 0 — 모르는 키 무시(research-2 §5 `board.dart:210-224`) |
| migration · 동기화 | 변경 없음 |

## frontend 몫

- E1 · E2 · E4 화면(제목 줄 「오더 메모」 + 배지 · 펼치기/접기 · 14px)은 frontend 가 `card.counselors` 로 그림. 메모가 없으면 메모 칸 자체를 그리지 않는 것도 템플릿 쪽.
- kit 견본 world(`routers/kit_board.py`)에 상담사 견본이 필요하면 `BVisit(counselor_ids=...)` + `world.staff` 에 그 직원을 넣으면 된다.

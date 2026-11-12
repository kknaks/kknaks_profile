# 리뷰 리포트 — fix-web / code 4차 · review-code-3 WARN 반영분 (2026-11-12)

대상: `be-3-report.md`(W1 — migration 0009 · 모델 · `counselor_rows` · 가드 테스트) · `fe-4-report.md`(W2 — 「펼치기」 화면 높이 기준 · `ui.html` · `day.js`). 3차 W3(스펙 공백)은 코드가 아니라 스펙 몫이라 이번 범위 밖.
리뷰어 검증: `uv run pytest -q -m "not infra"` → **936 passed · 320 deselected** · `ruff check backend` 통과 · `node --check day.js` 통과 · `static/day.css` 배너 sha = `app.css` sha256(`69880f5d…` · CSS 변경 없음). infra 는 돌리지 않음(be-3 리포트: migrations · 판 테스트 포함 131 passed).

## 판정: PASS

3차 W1 · W2 해소. 새 FAIL · WARN 없음. 참고 2건.

## W1 — migration 0009 `ix_consultation_visit_id`

| 볼 것 | 근거 | 판정 |
|---|---|---|
| 이름 규칙 | 파일 `backend/migrations/versions/20261112_0009_consultation_visit.py` · revision `0009_consultation_visit` · down `0008_chart_room` — 기존 `YYYYMMDD_NNNN_slug` · revision `NNNN_slug` 관례(0006 `20261110_0006_event_log_visit_type.py` · `0006_event_log_visit_type`)와 같음. 체인 head 하나(`backend/tests/migrations/test_alembic.py:22` `HEAD = "0009_consultation_visit"`) | PASS |
| upgrade / downgrade | upgrade = `op.create_index(…, postgresql_where=sa.text("deleted_at IS NULL"))` 하나 · downgrade = 같은 이름 `op.drop_index(…, table_name="consultation")` — 짝이 맞음 · 데이터 변경 · `op.execute` 없음. 0006 과 같은 모양 | PASS |
| 모델 일치 | `backend/day/models/visit.py:97-104` `Consultation.__table_args__ = (Index("ix_consultation_visit_id", "visit_id", postgresql_where=text("deleted_at IS NULL")),)` — 이름 · 칼럼 · 조건이 migration 과 같음. be-3: infra `alembic check` 차이 없음 | PASS |
| 부분 인덱스 조건 ↔ 쿼리 조건 | `backend/day/queries/board.py:59-76` `counselor_rows` — `WHERE visit_id IN (…) AND deleted_at IS NULL AND counselor_id IS NOT NULL`. 쿼리가 인덱스 술어 `deleted_at IS NULL` 을 그대로 포함하므로 플래너가 부분 인덱스를 쓸 수 있음(나머지 `counselor_id IS NOT NULL` 은 필터). `load_world` 는 같은 함수를 부름(`:131`) — 가드 테스트가 EXPLAIN 하는 문장 = 실제 문장 | PASS |
| 가드 테스트 | `backend/tests/day/board/test_board_queries.py:294-305` — `SET LOCAL enable_seqscan = off` 에서 EXPLAIN 에 `ix_consultation_visit_id`(0006 가드와 같은 방식 · infra). 인덱스가 지워지거나 쿼리 조건이 술어와 어긋나면 실패 | PASS |
| 운영 잠금(CONCURRENTLY) | 일반 `CREATE INDEX` 는 그 표에 SHARE 잠금 — 만드는 동안 **상담 쓰기(동기화 upsert)만** 기다리고 읽기는 막지 않는다. `consultation` 은 병원별 방문의 상담(대개 방문당 0 ~ 몇 건 · KOS 동기화 · DAY 운영 시작 2026-11 이후 누적)이라 지금 규모는 수천 ~ 수만 행 수준 → btree 한 칼럼 생성은 1초 안쪽. `CONCURRENTLY` 는 트랜잭션 밖(`autocommit_block`)이 필요하고 실패 시 INVALID 인덱스 정리 부담이 있어 이 규모에선 득이 없음 · 0006(쌓기만 하는 `event_log`)도 같은 판단. **CONCURRENTLY 불필요** — 다만 배포 직전에 prod 행 수가 수백만이면 다시 볼 것(리뷰어는 실제 DB 를 보지 않음) | PASS |
| 그 밖 | `backend/day/models/task.py:187` `EventLog` 인덱스 주석만 사실에 맞게 고침(스키마 무변경) · `backend/tests/day/test_chat_device_schema.py` 인덱스 목록에 새 인덱스 추가 | PASS |

## W2 — 「펼치기」 화면 높이 기준

| 볼 것 | 근거 | 판정 |
|---|---|---|
| 서버 줄 수 판정 제거 | `backend/day/templates/ui.html:229-240` — `split('\n')` 판정 삭제 · 버튼은 늘 두고 `hidden` · 펼친 견본은 「접기」 | PASS |
| 화면 높이로 판정 | `backend/day/static/day.js:737-744` `fitMemos` — `is-open` 이거나 `box.scrollHeight > box.clientHeight + 1` 이면 보임. 긴 한 줄이 접혀 5줄을 넘는 경우도 잡힘(3차 W2 해소) | PASS |
| `hidden` 이 CSS 에 덮이지 않음 | `.day-memo__more`(`app.css:453`)에 `display` 지정 없음 → UA `[hidden]{display:none}` 그대로 | PASS |
| 언제 재나 | `init(root)` 맨 앞(`:748`) — 처음(`:982`) · `htmx:afterSwap`(`:972`) · `htmx:oobAfterSwap`(`:980`). 조작 응답의 카드 OOB 는 `#card-<id>` innerHTML(`board_action.html:11`)이라 target 안에 `.day-memo` 가 있어 `querySelectorAll` 로 잡힘. 창 크기 바뀔 때도(`:745`) | PASS |
| 펼침 복원과의 순서 | 복원 리스너(`htmx:afterSwap` `:~580` · `oobAfterSwap` `:~507`)가 `init` 리스너보다 먼저 등록 → `is-open` 복원 뒤에 잰다. 펼친 메모는 잴 수 없어 「접기」를 그대로 둠 — 펼쳤던 메모는 넘쳤던 메모라 맞음. 복원 · 토글 모두 글자(`textContent`)와 `aria-expanded` 를 맞춤(`:462-464` · `:819-826`) | PASS |
| 웹 규칙 | 인라인 스크립트 · `style=` · `onclick` · `eval` 없음 · 새 리스너는 `resize` 1개(document 위임 아님이지만 창 이벤트라 누수 없음) · 손 CSS 없음 | PASS |
| 테스트 | `backend/tests/day/web/test_board_page.py` — 버튼이 늘 있고 `hidden` · 글자 · `ui.html` 에 split 없음 · `day.js` 에 판정 있음(문자열 확인). 실제 높이 판정은 브라우저에서만 — E2E 확인 몫(fe-4 리포트도 같은 권고) | PASS(정적 확인 한계는 참고) |

## 「조용히 통과하는 자리」

- `backend/tests/migrations/test_consultation_visit_migration.py` 는 migration 파일 **글자**를 찾는 non-infra 테스트라, 실제로 인덱스가 생기는지는 증명하지 않는다. 실제 보증은 infra 쪽(`test_alembic.py` upgrade/downgrade · `alembic check` · `test_상담사_조회는_consultation_인덱스를_탄다`) — 그 infra 가 돌아야 W1 이 닫힌다. 빈 단언은 아님(이름 · 술어 · 짝을 고정) — 참고.
- 메모 버튼 판정은 JS 라 서버 테스트는 「판정 코드가 있다」만 확인 — E2E 에서 6줄 메모 · 줄바꿈 없는 긴 메모 · 짧은 메모 세 가지를 눈으로 확인 필요.

## infra 테스트 — 영향 받는 것(코디가 `scripts/test.sh` 전체로 확인)

- 새: `backend/tests/day/board/test_board_queries.py::test_상담사_조회는_consultation_인덱스를_탄다`
- 바뀜: `backend/tests/migrations/test_alembic.py`(HEAD 0009 · upgrade/downgrade/`alembic check`) · `backend/tests/day/test_chat_device_schema.py`(인덱스 목록)
- 앞 차수분: `test_board_api.py::test_웹_판_조각_계약` · `::test_수락_뒤_오래_시작하지_않아도_확인_필요가_없다` · `::test_카드_상담사는_방문의_상담_전부_시작_순_중복_없이` · `test_board_queries.py::test_방문_1개와_10개의_쿼리_수가_같다`(16)
- be-3 가 위 파일들 131 passed 를 냈으나 전체 `scripts/test.sh` 는 아직 아무도 안 돌림.

## 직원이 실물에서 만날 자리

1. 줄바꿈 없는 긴 메모도 5줄 높이를 넘으면 「펼치기」가 보인다. 짧은 메모는 버튼 없음.
2. 배포 때 migration 0009 가 돌아야 인덱스가 생긴다 — 안 돌아도 판은 그대로 동작하고 느려지기만 한다. dev · prod 배포 흐름(`deploy-*` · `migrate-prod`)에서 migration 단계 확인.

## 참고

- **웹폰트 늦게 붙는 경우**: `@font-face Pretendard` 가 `font-display: swap`(`app.css:19-24`) · preload 없음 → 처음 `init(document)` 가 대체 글꼴로 잴 수 있다. 경계 근처 메모(딱 5줄 안팎)는 첫 화면에서 버튼이 틀릴 수 있고, 다음 판 갱신(SSE · 조작 응답)이나 창 크기 변경 때 바로잡힌다. 신경 쓰이면 `document.fonts.ready.then(() => fitMemos(document))` 한 줄 — 이번 판정엔 넣지 않음.
- 판 카드 폭이 창 크기 말고 다른 이유로 바뀌면(레이아웃 전환 등) 다음 갱신까지 판정이 남는다 — 지금 판은 카드 폭이 창 크기로만 바뀌어 해당 없음.

# 리뷰 리포트 — fix-web / code 3차 · E2E 1회차 수정 E1 ~ E4 (2026-11-12)

대상: `CENTURION_DAY/fix-web` 미커밋 변경 중 E2E 1회차분(`be-2-report.md` E3 · `fe-3-report.md` E1 · E2 · E4). 1 · 2차 리뷰 범위(W1 ~ W11 · 결정 A)는 그대로라 변경 없음만 확인.
기준: 결정 `e2-common.md`(E1 ~ E4 · 계약 `cards[].counselors`) · DAY-SPEC-002 개정 ⑳ U-1 「오더 메모 모양」 · 「상담사 배지」(spec-002 :184-188) · 스냅샷(:609) · 레포 `AGENTS.md`.
리뷰어 검증: `uv run pytest -q -m "not infra"` → **933 passed · 319 deselected** · `ruff check backend` 통과 · `node --check day.js` 통과 · `static/day.css` 배너 `source-sha256:69880f5d…` = `app.css` sha256(일치). infra 는 돌리지 않음.

## 판정: WARN (FAIL 없음 · WARN 3)

## FAIL

없음.

## WARN

### W1. 상담 조회가 `consultation.visit_id` 인덱스 없이 돈다 — 판을 다시 받을 때마다 상담 표 전체 seq scan
- 코드: `backend/day/queries/board.py:108-126` — `WHERE visit_id IN (...) AND deleted_at IS NULL AND counselor_id IS NOT NULL ORDER BY started_at, created_at, id`.
- `consultation` 표에는 `visit_id` 인덱스가 없다(모델 `backend/day/models/visit.py:93-102` · migration `20261105_0002…:1177-` — FK 만 있고 `Index` · `index=True` 없음 · migrations 전체 grep 0).
- 쿼리 수는 방문 수와 무관(1번 · N+1 아님 — `test_board_queries.py` 16 = 방문 1 · 10 같음)이지만, 행 수는 **병원 누적 상담 전부**에 비례해 판 GET · SSE 갱신 · 조작 응답마다 읽는다. 날이 갈수록 느려지는 자리.
- 이번 결정은 「migration 없음」(e2-common E3)이라 지금 고칠 수 없다 → **후속 migration 으로 `ix_consultation_visit_id`(부분 `WHERE deleted_at IS NULL` 가능) 권장**. 1차에서 판 쿼리가 인덱스를 타는지 지키던 테스트(`test_원장_바꾼_시각_조회는_event_log_인덱스를_탄다`)와 같은 종류의 가드도 그때 같이.
- 근거: AGENTS.md 「백엔드 안전 기준」(centurion backend-reliability) · 판은 SSE 로 자주 다시 읽힌다(SPEC-002 실시간 갱신).

### W2. 「펼치기」가 줄바꿈(`\n`) 수로만 정해져 14px 에서 긴 한 줄 메모가 잘린 채 버튼이 없다
- 코드: `backend/day/templates/ui.html:234` — `text.split('\n')|length > 5` 일 때만 「펼치기」. 내용 칸은 `max-height: var(--day-memo-max-h)`(93px) · `overflow: hidden`(`styles/app.css:451`).
- 줄바꿈이 5개 이하라도 한 줄이 길면 카드 폭에서 접혀 5줄을 넘고, 넘친 부분이 **아무 표시 없이 잘린다** — 펼칠 수단이 없음. 판정 방식은 앞 판부터 같지만(기존 부채), 글자를 10 → 12 → 14px 로 키우며 한 줄이 접힐 확률이 크게 늘었다.
- 근거: SPEC-002 U-1 「오더 메모 모양」 ① 「5줄 넘을 때」 펼치기(:185) — 화면에 보이는 줄 기준으로 읽으면 빠짐. 고치려면 day.js 가 `scrollHeight > clientHeight` 로 버튼을 켜는 방식(템플릿은 늘 버튼을 두고 `hidden`) — 이번 결정 범위를 넘으면 후속으로.

### W3. 스펙에 없는 정렬 · 제외 규칙 두 가지를 백엔드가 골랐다
- `started_at` 이 없는 상담은 **맨 뒤**(`queries/board.py:118` `nulls_last`) · 같으면 `created_at` → `id`. be-2 리포트도 「브리프가 정하지 않아 고름」이라 적음. 스펙 :188 은 「상담 시작(`started_at`) 순」까지만.
- **지운 직원**(`staff.deleted_at`)의 상담사는 배지에서 뺀다(`services/board_rules.py:816-820` — `world.staff` 는 `Staff.deleted_at IS NULL` 만 읽음 `queries/board.py:323-325`). 스펙은 「비활성 직원도 보인다」만 있고 지운 직원은 말이 없다.
- 둘 다 합리적이고 판의 기존 규칙(지운 직원은 판에 없음)과 맞지만, 「외부 응답에 없는 값을 추정해 채우지 않는다」 계열은 아니어서 FAIL 은 아님 — **SPEC-002 :188 에 한 줄씩 적어 닫기 권장**.

## 결정 E1 ~ E4 대조

| 항목 | 코드 | 판정 |
|---|---|---|
| E1 펼침 아이콘 → 파란 글자 「펼치기」/「접기」 · 제목 줄 오른쪽 끝 | `ui.html:229-240`(`.day-memo__head` 안 `button.day-memo__more` · `margin-left: auto` `app.css:453`) · 글자 색 `--day-text-brand` 토큰 · 토글 글자 전환 `day.js:812` · 다시 그릴 때 복원 `day.js:462-464` | PASS(+W2) |
| E2 12 → 14px · 접힌 높이 14px 기준 5줄 | `app.css:451` 14px · `:161` 93px(14 × 1.3 × 5 = 91 + 2 · 1차의 여유 2 와 같은 셈) | PASS |
| E4 제목 줄 「오더 메모」 + 상담사 배지(작은 글씨 · 여러 개) · 구분선 없음 · 내용은 아래 | `ui.html:231-238` — `sq_badge(name, "gray")`(기존 배지 매크로 · `--day-font-badge`) · `.day-memo` 세로 배치 gap 4 · 제목 줄 · 내용 사이 border 없음(`app.css:447-451`) · 상담사 0명이면 「오더 메모」만 | PASS |
| E4 메모 없으면 칸 없음 | `board_parts.html:170` `{% if card.orderMemo %}` 그대로 | PASS |
| E3 `cards[].counselors: [{staffId, name}]` · 없으면 `[]` · `orderMemo` 옆 | `services/board_rules.py:814-820` | PASS |
| E3 그 방문 상담(삭제 안 됨) 전부 · 중복 제거 · 시작 순 | `queries/board.py:108-126`(삭제 · `counselor_id` null 제외 · 처음 나온 순서 유지 중복 제거) · `dtos/board.py:65-66` `counselor_ids` | PASS(+W3) |
| E3 희망 상담사 · 상담 의사 안 씀 | `requested_counselor_id` · `doctor_id` 안 읽음 | PASS |
| E3 비활성 직원도 이름 | `world.staff` 는 `is_active` 상관없이 담음(`queries/board.py:323-331` — `is_active` 는 원장 · 간호 목록 판정에만) | PASS |
| E3 migration · 동기화 변경 없음 | `migrations/` · `emr/` 변경 없음 | PASS |
| 앱 변경 0 | `app/` 변경 없음 | PASS |

## 앱 호환 — PASS

- 새 키 `cards[].counselors` 만 더해짐 · 기존 키 모양 무변경. 앱 `app/lib/model/board.dart:210-224` 카드 파서는 필요한 키만 `m['…']` 로 읽어 모르는 키를 무시(`orderMemo` `:217` 등 그대로). 깔린 앱이 깨질 자리 없음.

## 화면 문구 발명 — PASS

- 새 문구 「오더 메모」 · 「펼치기」 · 「접기」 = 사용자 E1 · E4 원문(e2-common) · SPEC-002 :185. 근거 표 `backend/tests/architecture/test_screen_copy.py` 에 출처와 함께 등록 · 앞 판 aria 문구(「메모 크게 보기」 · 「메모 접기」 · 「크게 보기」)는 지운 문구 목록으로. 「메모」 단독 근거 삭제 — 남은 쓰임 없음(테스트 통과).
- 배지 색(회색) · 제목 12px/500 은 시안 없음 — 문구가 아니라 모양 선택(fe-3 리포트 「코디가 확인할 것」). 기존 토큰 · 기존 배지 매크로만 썼다.

## 「조용히 통과하는 자리」 — PASS

- 템플릿 `counselors=card.counselors or []`(`board_parts.html:170`) — 키가 빠진 견본 · 옛 스냅샷에도 안전. 서버는 늘 리스트를 싣고(`[]` 포함) 단위 테스트(`test_board_rules.py`) · infra 테스트(`test_board_api.py` `test_카드_상담사는_방문의_상담_전부_시작_순_중복_없이`)가 순서 · 중복 · 지운 상담 · 비활성 · 지운 직원 · 시작 없음까지 실제 값으로 단언 — 빈 단언 없음.
- 지운 aria 문구 · `icon('maximize')` 를 아직 읽는 곳: `day.js` 는 `aria-label` 대신 `textContent` 로 바뀜 · 다른 읽는 곳 grep 0.
- `day.js` 복원(`restoreState`)과 클릭 토글 둘 다 글자를 맞춤 — 다시 그린 뒤 「펼치기」인데 펼쳐진 상태가 되는 어긋남 없음.

## N+1 — PASS(쿼리 수) / WARN W1(인덱스)

- 상담 쿼리 1번 · 방문 0개면 안 함. `test_board_queries.py::test_방문_1개와_10개의_쿼리_수가_같다` 기대 15 → 16(방문마다 상담 1개 넣고 같음 단언 유지).

## 손 CSS — PASS

- `static/day.css` 는 빌드 산출물 — 배너 sha = `app.css` sha. 새 규칙은 `app.css` 의 `.day-memo*` 클래스 규칙뿐 · 색은 기존 토큰(`--day-text-secondary` · `--day-text-brand` · `--ms-primary-100` · `--ms-gray-500`). 템플릿 · JS 에 `style=` · 인라인 스크립트 · `onclick` · `eval` 없음.

## 계층 규칙 — PASS

- DB 접근은 `queries/board.py` 에만 · 라우터 무변경 · ORM 은 `day` 밖으로 안 나감(`counselor_ids` 는 DTO 의 uuid tuple). 병원 범위: 상담 조회는 그 병원 판 방문 id 로만 거름(`visit_ids` 가 이미 병원 범위).

## infra 테스트 — 영향 받는 것(코디가 `scripts/test.sh` 로 확인)

- 새: `backend/tests/day/board/test_board_api.py::test_카드_상담사는_방문의_상담_전부_시작_순_중복_없이`
- 바뀜: `backend/tests/day/board/test_board_queries.py::test_방문_1개와_10개의_쿼리_수가_같다`(15 → 16 · `add_full_visits` 에 상담 1개)
- 1 · 2차분: `test_board_api.py::test_웹_판_조각_계약` · `::test_수락_뒤_오래_시작하지_않아도_확인_필요가_없다`
- be-2 리포트: 세 파일 113/113(새 테스트 1건은 고친 뒤 단독 재실행). 프론트 fe-3 변경이 들어간 상태의 전체 `scripts/test.sh` 는 아직 아무도 안 돌림.

## 직원이 실물에서 만날 자리

1. 방 카드 오더 메모가 14px 로 커지고 위에 「오더 메모」 + 상담사 이름 배지(회색)가 붙는다. 상담이 없거나 상담사가 비면 「오더 메모」만.
2. 줄바꿈 없는 긴 메모는 5줄 높이에서 잘리는데 「펼치기」가 안 나온다(W2).
3. 상담사가 많으면 제목 줄이 두 줄로 접히고 「펼치기」는 마지막 줄 오른쪽 끝(fe-3 리포트).
4. 날이 갈수록 판 갱신이 조금씩 느려질 수 있다(상담 표 전체 읽기 · W1) — 오늘 데모 규모에서는 체감 없음.

## 참고(기존 부채 · 무관)

- 메모 「5줄」 판정이 줄바꿈 수 기준인 것은 앞 판부터(W2 의 뿌리).
- OOB 로 인박스 목록만 다시 그릴 때 판 카드 고르기의 흐림이 인박스에서 풀린 채 그려질 수 있음 — 2차 리포트 참고 그대로.

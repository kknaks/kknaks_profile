# be-fix-1 결과 보고 — review-code-1 반영 (C18 · C19 · C20 · C21 · W6 · W7)

## 상태: done (커밋 안 함 · day.js · 템플릿 안 건드림)

## 수행
| 항목 | 위치 | 내용 |
|---|---|---|
| C18 (W1) | `backend/day/policies/board_chart_tabs.py` `day_differs` | `baseLogId` ≠ 마지막 이력이어도, 뒤 이력이 전부 `source=kos` 이고 마지막 글(의사 + 집도의)이 요청 `base` 와 같으면 안 걸림 · `baseLogId` 없음 = 그 줄 이력 전부가 뒤 이력 · 모르는 `baseLogId` = 걸림 |
| C19 (W2) | 같은 파일 `already_saved` · `judge_row` 첫 단계 | 마지막 이력 = 세션 직원 · `source=day` · 같은 글(C20 정규화) · 같은 담당자 → DAY · KOS 판정 안 함 · 바뀐 것 없음으로 건너뜀(저장 0 · 200) |
| C20 (W4) | `chart_text` | `\r\n` · `\r` → `\n` 뒤 앞뒤 빈칸 빼기(기준값 · KOS 값 · 요청 · 이력 비교 모두 이 함수) · 저장 글도 같은 함수라 LF 로 저장됨 |
| C21 (W5) | `services/board_charts.py` `_kos_values` | 코디 답 ⓐ — 매핑 먼저 → 매핑된 DAY 직원이 한 명일 때만 · `chart_base` 그대로(DAY 사본 = 매핑된 직원만 · `sync_tasks.py:378-381`) |
| W7 | `backend/common/error_codes.py` | `STAFF_NOT_LISTED` 상수 · `board_charts.py` 가 씀 |
| W6 | `README.md:197` | 「경로 없어져 지웠다」→ 커밋 뒤 응답 유실은 남고 C19 로 200 · 테스트 위치 |
| 판정 입력 | `services/board_charts.py` `_history` | 보낸 줄 · 그 차트 이력 전부(DB 순번 `revision`)를 잠금 안에서 읽어 `judge_row(history=…, viewer=…)` 로 |
| 정형 결속 | `scripts/devtools/verification_binding.py` · `.agents/skills/verify-day-chart/specs/source-map.json` | 기준 ID 비교가 `day_differs` 로 옮겨감 → GUARD = `row.base_log_id != last_id`(같은 극성 · 대조군 `!=`→`==` 그대로) · `day_differs` 결속 추가 · 해시 재계산 · abstraction/exclusions 에 C18 · C19 를 TLA 모델 밖 수락 경로로 적음 · TLA · Lean 원문 안 바꿈 |

## 테스트
- 순수 `backend/tests/day/test_board_chart_tabs_policy.py`(15): C20 CRLF · CR · KOS CRLF 동일 글 · C18(동기화만 · baseLogId 없음 · 뒤에 DAY 저장 · 마지막 KOS 글 다름 · 의사 집도의 다름) · C19(같은 직원/글/담당자 · CRLF · 다른 직원 · 다른 담당자 · 다른 글)
- 실제 DB `backend/tests/day/board/test_board_chart_conflicts.py`(test_board_chart_api.py 가 700줄을 넘어 충돌 묶음을 나눔): `test_C18_…` 409 → `source=kos` 이력 + 사본 추가 → 걸린 응답 값 그대로 다시 저장 = 200 · 이력 = [KOS 글, KOS 글\n내 글](글 한 번) · `test_C19_…` 두 줄 저장 200 → 같은 요청 다시 = 200 · 이력 각 1 · event 1 · outbox 그대로 · 다른 글이면 409

## 검증
- `scripts/test.sh -q backend/tests/day/board` — 233 passed
- `scripts/test.sh --pure -q` architecture · devtools · policy — 536 passed
- ruff check · format --check(backend · scripts) OK · mypy(repo 설정) Success 585 files

## 계약 대조
- 규칙 31 ⓑ 새 순서(planner-fix-3): 이미 저장됨(C19) → DAY 쪽(C18 단서) → KOS 쪽 — 같음
- C21: 결정 「매핑 전 개수」 → 코디 답 ⓐ(매핑 뒤 · 두 쪽 같은 단계)로 구현 — SPEC 문구는 planner 가 맞춤

## 코디가 확인할 것
- C19 는 정형 동시성 평가(`verification_concurrency` — 편집자 = 같은 계정의 다른 세션)에서 편집자가 서로 다른 글을 보내므로 수락되지 않는다(stale retry 글도 다름). 실행은 안 함(TLC · 브라우저 필요) · pending.
- C20 로 저장 글도 CRLF → LF 가 된다(비교와 저장이 한 함수). KOS 로 나가는 메모도 LF.
- W3(보내는 동안 칸 잠금)은 frontend 몫 — 안 건드림.

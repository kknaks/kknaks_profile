# planner-fix-4 결과 보고 — C21 집도의 「한 명」 기준 바로잡기

## 상태: done

워크트리 `mediness-mediness/day-chart-photo-spec` · `d98c5a28` 위 · 미커밋. 바꾼 파일 = `products/day/20-spec/spec-002-procedure-board.md` · `products/day/log.md`.

## 바꾼 곳 (spec-002 줄)

| 자리 | 반영 |
|---|---|
| :45 개정 ㉘ 머리글 보충 3 ⑮ | ~~매핑 전 KOS 외부 id 개수~~(→ fix-4) **DAY 기준값 · KOS 지금 값 둘 다 매핑 뒤 DAY 직원 수** + 날짜 · 사유 |
| :1157 규칙 31 「비교 =」 | 집도의 괄호(`mapper.single` 과 같은 규칙) ~~취소선~~ → 「한 명」 기준을 따름(`mapper.single` 은 매핑 전 개수라 맞지 않음) |
| :1157 규칙 31 「(C21-기본값) 집도의 「한 명」」 | 앞 문장 ~~취소선~~ + 사유 → 매핑 뒤 DAY 직원 수 · 정확히 한 명이면 그 직원 · 0명 · 둘 이상 = 「없음」 · KOS 집도의 둘 중 하나만 DAY 직원이면 양쪽 다 그 한 명 |
| :1260 §4 결정 짝 표 C18 ~ C21 행 | ~~매핑 전 KOS id 개수~~ → 매핑 뒤 DAY 직원 수 |
| OQ-91 | 보충 문구 같게 고침 |

- 사유(문서에 적음): DAY 사본 `visit_task_staff` 는 매핑된 집도의만 저장(CENTURION_DAY `emr/sync_tasks.py:378-381`) → 매핑 전 개수를 알 수 없음 · 새 칸 = migration = 범위 밖.
- `log.md` spec-change 1행(앞 fix-3 행은 이력이라 그대로). `10-decision.md` 는 「한 명」 기준을 적지 않아 바꿀 것 없음. U-14 에는 「한 명」 문장이 없음.

## 검증

`python3 scripts/lint-pipeline.py --strict` → **0 error · 263 warning** · `products/day/` 0건(전부 타 제품 — 무관).

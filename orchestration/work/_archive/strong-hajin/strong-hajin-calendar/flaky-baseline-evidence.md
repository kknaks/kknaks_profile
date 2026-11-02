# `test-contract` 실패의 기준선 분리 — 근거 (2026-09-21, 코디 실측)

BE-3 검수의 **WARN-1** 이 요구한 기록이다. 「이번 계약이 초록이다」를 닫으려면
실패가 우리 것이 아님을 보여야 한다.

## 관측

| 언제 | 누가 | 결과 |
|---|---|---|
| BE-1 착수 **전**(기준선) | backend 워커 | 1078 passed / **2 failed** — `test_material_identity` 1 · `test_material_worker_recovery` 1 |
| BE-1 직후 | backend 워커 | 1104 passed / **2 failed** — `material_worker_recovery` 2 |
| BE-2 직후 | backend 워커 | 1117 passed / **2 failed** — 같은 계열 |
| BE-3 직후 | backend 워커 | 1135 passed / **3 failed** — `recovery` 2 + `material_search` 1 |
| BE-3 직후 | **코디 실측** | 1133 passed / **5 failed** — `material_search` **3** + `recovery` 2 |

**실패하는 테스트의 집합이 회차마다 바뀐다.** 워커 1차는 `material_search` 중
`test_naming_the_work_still_scopes_the_search_to_it`, 2차는
`test_search_returns_bounded_excerpts_only_for_authorized_live_bindings` 였고,
코디 실측은 그 둘에 `test_searching_without_naming_the_work_finds_what_this_person_may_read` 가 더해졌다.
**고정 실패가 아니다.**

## 결정적 증거 — 직렬로 돌리면 전부 통과한다

```
$ uv run pytest tests/contract/test_material_search.py \
                tests/contract/test_material_worker_recovery.py -p no:randomly -q
20 passed, 2 warnings in 49.42s
```

## 판정

**기존 flaky 다. 이번 작업과 인과가 없다.**

- **기준선(착수 전)에 이미 같은 계열이 실패했다** — 우리 코드가 한 줄도 없을 때.
- 두 파일은 **material 파서 워커의 lease·timeout** 계열이고, 실패 단언이 job 상태
  (`['failed','running']` vs `['failed','completed']`)다 — **시간에 민감한 경합**이다.
- 두 파일은 **배정·회의·캘린더 표면을 전혀 부르지 않는다.** `overlapping_blocks` 는
  `create_schedule`·`retime_schedule` 두 곳에서만 불린다.

## 다만 정직하게 — 우리가 악화시켰을 수 있다

**2f → 3f → 5f 의 증가는 부하로 읽는 것이 맞다.** BE-1~BE-3 이 계약 테스트를 **58건**
더했고(19+13+7 외 계약 19), `-n auto` 병렬의 부하가 올라가면 시간에 민감한 그 계열이
**더 자주** 흔들린다. 워커도 같은 말을 먼저 보고했다.

**이번 작업의 계약이 깨진 것은 아니다** — 우리가 더한 테스트는 전부 통과한다.
하지만 **그 계열의 격리 문제는 남는다.**

## 남기는 것

`material_search`·`material_worker_recovery` 의 **병렬 격리**는 이 작업의 범위 밖이다.
별건으로 볼 자리다 — 부하가 더 오르면 CI 가 붉어지는 빈도가 는다.

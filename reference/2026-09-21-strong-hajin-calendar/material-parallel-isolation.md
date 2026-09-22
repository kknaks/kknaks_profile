# `material_*` 계열의 병렬 격리 — 다음 작업 재료

**2026-09-21 · 캘린더 시간 배정 작업(`strong-hajin-calendar`)에서 관측.**
운영 사고는 같은 폴더 [`README.md`](README.md) 에 있다.
이 작업 탓이 아니지만 **이 작업이 악화시켰다.** 고치는 것은 별건이다.

## 증상

`make test-contract` 가 `-n auto` 병렬로 도는데, **`material` 파서 워커 계열이 흔들린다.**
**실패하는 테스트의 집합이 회차마다 바뀐다** — 고정 실패가 아니다.

| 언제 | 결과 |
|---|---|
| 캘린더 작업 **착수 전**(기준선) | 1078 passed / **2 failed** |
| BE-1 직후 | 1104 / **2** |
| BE-2 직후 | 1117 / **2** |
| BE-3 직후 (워커) | 1135 / **3** |
| BE-3 직후 (**코디 실측**) | 1133 / **5** |
| BE-4 직후 | 1158 / **2** → 수정 뒤 1157 / **3** |

돌아가며 들고 나는 파일: `test_material_worker_recovery` · `test_material_search` ·
`test_material_search_owners` · `test_material_action_evidence` · `test_conversation_lifecycle`.

## 결정적 관측 — 직렬로 돌리면 전부 통과한다

```bash
$ uv run pytest tests/contract/test_material_search.py \
                tests/contract/test_material_worker_recovery.py -p no:randomly -q
20 passed
```

한 라운드에서 실패한 **다섯 파일 전부**를 직렬로 → **44 passed / 0 failed**.

## 왜 기존 것인가

- **착수 전 기준선에 이미 2건 실패**했다 — 캘린더 코드가 한 줄도 없을 때.
- 실패 단언이 **job 상태**다 (`['failed','running']` vs `['failed','completed']`) —
  **시간에 민감한 경합**이다. lease·heartbeat·timeout 계열.
- 그 파일들은 **배정·회의·캘린더 표면을 전혀 부르지 않는다.**

## 왜 이 작업이 악화시켰나

**계약 테스트를 58건 더했다.** `-n auto` 의 병렬 부하가 올라가면 시간에 민감한 그 계열이
**더 자주** 흔들린다. `2f → 3f → 5f` 의 증가는 그것으로 읽는 것이 맞다.

**부하가 실제로 눌려 있었다** — 측정 중 `load average 19.39` 를 봤고, 그때 **E2E 스택**
(API + 대화·자료·회의·보고 워커 4개)이 함께 떠 있었다. 그 스택은 나중에 **메모리 부족으로 두 번
죽었다.** 기계가 빡빡하면 이 계열이 먼저 무너진다.

## 왜 문제인가

- **`make verify` 가 exit 2 로 끝난다.** 초록을 못 본다.
- **새 계약의 증명이 흐려진다** — 「우리가 더한 테스트가 통과한다」를 보이려면 매번 직렬 재실행으로
  기준선을 갈라야 한다. 그 분리를 안 하면 「이번 계약이 초록이다」가 안 닫힌다
  (실제로 BE-3 검수가 그 근거가 없다고 지적했고, 코디가 실측으로 닫았다).
- 앞으로 **테스트가 더 늘수록 빈도가 는다.**

## 다음에 볼 자리

1. **무엇이 공유되는가** — 그 계열이 무엇을 두고 다투는지. 파일? DB? 시계?
   `durable_jobs` 원장과 lease 시각이 후보다.
2. **격리 수단** — `pytest-xdist` 의 `--dist loadgroup` 으로 그 파일들을 한 워커에 묶거나,
   그 계열만 직렬 마커를 주거나, lease/timeout 을 실시간이 아닌 주입 시계로 바꾸거나.
3. **`make verify` 의 계약** — 지금은 한 명령이 전부를 돌린다. 그 계열만 갈라 도는 타겟이
   필요한지.

## 근거 파일

- `orchestration/work/_archive/strong-hajin/strong-hajin-calendar/flaky-baseline-evidence.md`
  — 회차별 관측과 직렬 재실행 결과
- 같은 디렉토리의 `review-be3-report.md`(WARN-1 이 이 분리를 요구했다) · `be2-report.md`

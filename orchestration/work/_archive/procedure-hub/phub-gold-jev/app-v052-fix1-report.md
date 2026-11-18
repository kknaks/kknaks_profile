# app 0.5.2 수정 1 보고 — 덮인 조각 · (다) 끝 상태 · 코드 검수 W-1 ~ W-4

상태: 끝. 커밋 안 함. F-2 는 코디 답 (a)대로 처리함.

## F-1 덮인 조각(결정 — _RESUME §2 11-17)
- `walk/front.py`: 판정 순서는 overlap → yes `target` → **덮인 조각(`covered_by` ≠ null)이면 `dropped`**(사이 값이든 no 든 · noul 과 함께 `front.dropped[]`) → 덮이지 않은 사이 값은 `uncertain_kept`(TG2) → 덮이지 않은 no 는 `named`(TG3). 이제 TG2 는 덮이지 않은 조각에만 붙는다. 쓸 일이 없어진 `else dropped` 갈래는 지웠다.
- `walk/calls.py`: `Entry` 에 `span` · `covered_by` 를 더했다(B 단계 ① 만 채움 · 키 · 깊이 입구는 None 이라 동작 그대로). `covers()` · `filter_entries(owner, entries, table)` 를 새로 둠. **덮은 대상의 조회에는 그 안에 든 조각을 거르개로 쓰지 않는다** — 부위(`site_name` · `concern_candidates.site`) · 사건(`adverse_code`) · 조건(`condition_code`)에 다 적용. 서로 떨어진 이름은 지금처럼 거르개로 쓴다.
- 시험(`tests/test_covered.py`): 긴 이름 꼴(덮인 고민 0.56 · 덮인 부위 0.37 → 둘 다 dropped · 거르지 않은 `concern_candidates` 하나 · 거르개 0) · 덮인 조각 yes 꼴(대상이 되지만 덮은 고민 조회는 거르지 않음. 덮지 않은 다른 고민 조회는 그 부위로 거름) · 떨어진 이름 회귀(부위로 거른 조회 하나뿐). `test_walk_front::test_covered_piece_dropped_or_kept` 는 새 규칙에 맞춰 고쳤다(사이 값 → dropped · yes → target). 덮이지 않은 사이 값 → TG2 를 보는 시험 하나를 더했다.

## F-2 (다) 끝 상태 — 코디 답 (a)
- 원인: 필터로 쓴 사건 입구(ADV-051)가 required 셈에서 대상과 이어지지 않았다 → `met_by None` → 「후보 소진」. W-1 을 고친 뒤 Q12 B 는 **근거 충족**으로 끝난다. 「원천 미확정 (다)」 는 B 가 물은 칸을 알아야 판정할 수 있어서 SPEC §5 600행(O-5 ②)이 말한 대로 알고 가는 어긋남이다. 물은 칸 판정 (b) 는 이번에 하지 않았다.

## 코드 검수 덧붙임
- **W-1**: `walk/required.call_side(q, node)` 를 새로 둠. node · a · b · concern_code 에 더해 `filters.{adverse,condition}_code` 도 그 입구의 조회로 센다. B `target_rows` 와 키 `answer_key.kinds_met` 가 **같은 함수**를 쓴다. 필터 조회는 좁힌 조회라 coverage 대조는 그대로 건너뛴다. 주의: 키를 다시 뽑으면 Q12 `kinds_met` 에 `adverse:ADV-051.adverse` 줄이 새로 선다(이번에 다시 뽑지 않음).
- **W-2**: 지시서 F-1 을 따랐다. 덮이지 않은 사이 값(TG2) 거르개 입구는 **거른 조회 + 안 거른 조회**를 함께 낸다(부위 · 사건 · 조건 — `filter_entries` 의 plain 표지). 시험은 부위 · 사건 두 꼴.
- **W-3**: `ReadAll.summary()` 에 `ledger_check` 를 더했다 → runs 의 `breadth[]` 줄마다 남는다. 실물 볼 주름 run 에 LCK 1건이 찍혔다.
- **W-4**: `Verified.add_response` 에서 같은 gid 가 다시 오면 `_merge_marks` 로 `inherited_from` · `site_match` 를 합친다. 읽은 차례와 무관하고, 두 차례로 확인하는 시험이 있다.

## 확인
- `uv run ruff check .` 통과 · `uv run pytest -q` **190 passed · 1 skipped**(이전 181 · 1 + 9: test_covered 8 · test_walk_front 1).
- 실물 — 18221 속도 탭 API(effort b=low c=low · 동시 · 허브 18105). 18221 은 띄웠다가 내렸다(LISTEN 0). 18105 · 18106 · 18220 은 손대지 않았다.

| | run | B 종료 | B 읽기 조회 · 묶음 | C 대비 | B / C ms |
|---|---|---|---|---|---:|
| 볼 주름에 뭐 해? | 0ca349f1d5fc | 근거 충족 | 주름 0.55 · 볼 0.36 → dropped · `concern_candidates(CON-012)`(site 없음) **65 묶음** · 윗고민 CON-008 inherited 181 · ledger_check 1 | C 도 깊은 주름 윗고민 · 하위 고민으로 같은 폭(전엔 B 2 / C 65) | 37047 / 13907 |
| Q12 필러 혈관 폐색 | e6d733edcdac | **근거 충족**(a — 기대 (다)와 알고 가는 어긋남) | ADV-051 adverse self 1 · lower 22(필터 조회로 셈 — W-1) | B · C 모두 발현 · 지속 「자료에 없음」 · 효과 기간과 안 섞음 | 23021 / 24454 |
| 이마에 주름이 많아서 걱정이에요 | 55e856071af8 | 근거 충족 | `concern_candidates(CON-001, site=이마)` **16 묶음 그대로**(회귀 없음) | 같은 계열 목록 | 29997 / 10389 |

- 단건이라 ms 편차가 크다. 볼 주름 B 가 느린 것은 묶음이 65 로 늘어 followup profile 65 회를 부르기 때문으로 보인다.

## 커밋 후보 grep
- 실제 코드 · 이름 · 질문 문장 · 홈 경로 0. 코드 docstring 에 넣었던 실제 이름을 일반 말로 바꿨다. 시험은 가짜 코드(ZZ…) · 가짜 이름(「가짜…」)만 쓴다. 기존의 가짜 gid(9xxxx)는 그대로.
- 바뀐 파일: clinic_chat/walk/{front,calls,required,verified}.py · clinic_chat/evalset/answer_key.py · clinic_chat/clients/hub_rest.py · tests/test_walk_front.py · tests/test_covered.py(새). 로컬: runs/runs.jsonl 에 3 줄이 늘었다.

## 되적기 후보(SPEC-002 0.6)
1. TG2 · TG3: 덮인 조각은 yes 일 때만 대상(사이 값도 dropped).
2. BR1: 덮은 대상의 조회에 그 안의 조각을 거르개로 쓰지 않음 · 사이 값 거르개 입구는 거른 조회 + 안 거른 조회.
3. RQ1 셈: 필터로 쓴 사건 · 조건 입구도 필터 조회로 센다(B · 키 같은 `call_side`).

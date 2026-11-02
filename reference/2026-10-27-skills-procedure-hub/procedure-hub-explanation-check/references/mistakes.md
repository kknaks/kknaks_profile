# 9단계에서 틀린 것

| # | 틀린 것 | 어떻게 드러났나 | 고친 것 |
|---|---|---|---|
| 1 | 칸 이름(slot) 을 경로 꼴마다 다르게 만듦 — `extracted.M10.indications.primary[0]` 은 `primary`, `taxonomy.modality[9].extracted.indications.primary[0]` 은 `indications.primary` | 조사 중 「extracted.json 에만 있는 값 209」 · 계열 충돌 6 이 엉터리 | extracted 아래는 그 뒤 경로 하나로(`slot_key`) — 다시 세니 대조본 다름 7 |
| 2 | 고민 CC 대응을 CC 이름만으로 찾음 — 7단계 대응표 글자는 `cc [cc_detail]` | 고민 쪽 붙음 11/125 | `cc [상세]` 로 먼저 찾고 없으면 이름 |
| 3 | 고민 노드 집합을 `node` 표시만으로 셈 — 7단계 items 는 `kind == 고민` 이 노드(시맨틱 정본과 같은 기준) | 반영 첫 판 open 33 | items[kind=고민] 을 넣음 |
| 4 | 배열 칸(적응증 목록)을 원소 단위로 비교해 「목록이 다르면 충돌」로 셈 | 충돌 996 | 원천 레코드마다 값 집합으로 비교 → 606 · 배열 칸엔 ② 를 쓰지 않음 |
| 5 | 「지속 = 짧은 쪽」을 하한으로 비교 — 「완전 효과 1개월, 유지 3-4개월」의 시작 숫자가 하한이 됨 | ② 처분 표본 확인 | 지속은 상한 → 하한 순 |
| 6 | 고정 시험 기대값을 조사 md 의 잘린 목록(노드 앞 2)에서 옮김 | R9-1 시험 FAIL(U5-012 빠짐) | 기대값은 실물 출력에서 |
| 7 | 새 실버 정본(step9-explanations)을 semantic-build 입력에 넣고 semantic-check 입력 목록을 안 고침 | semantic-check build 실패 · selftest 14/15 | check_semantic 입력 목록(DECISIONS 쪽)에 더함 — 실버 8 풀기 줄은 건드리지 않음 |
| 8 | 스펙 문구(「severity_levels 는 실버에 칸이 없다」)를 믿고 대상에 넣을 뻔 | 조사 때 골드 fact 덮임 24/24 | 대상 전에 골드 · 실버 덮임을 먼저 셈(K10 대상 밖) |
| 9 | 발주서의 A 수(v5a 27)를 셈 식 없이 받음 | 같은 배치 gold_match 무히트 30 | 셈 식(recheck2 gold_match)을 같이 적고 30 으로 보고 |

## 되풀이하지 않은 것

- 골드 export 노드로 붙는 자리를 정하지 않음(반영은 실버 id 만 — 실버에 없으면 open)
- 설명 문장을 요약 · 다시 쓰기 하지 않음(원문 그대로 · 숫자 정규화 없음)
- 원문 보관 행선지(5단계 결정)를 9단계가 바꾸지 않음

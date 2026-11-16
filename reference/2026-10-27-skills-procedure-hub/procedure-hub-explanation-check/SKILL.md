---
name: procedure-hub-explanation-check
description: 설명 사실(효과 시작 · 지속 · 작용 원리 · 개요 · 적응증 · 제품 메모 · 대안 · 관련 기법 · 고민 상세 · 반응 · 중증도 단계 값 사전 · 합병증 관리 · 예방 section) 원천이 들어오거나 바뀌거나, 앞 단계(5단계 extracted · taxonomy_products attach · 7단계 고민 항목 · 8단계 합병증)가 바뀌었을 때 Procedure Hub 실버 설명 사실 원장(step9-explanations)을 갱신한다. 사람 확인 게이트 없이 규칙으로만 — 붙는 자리는 5 · 7 · 8단계가 이미 정한 대응(R9-1~R9-8)으로, 같은 노드 · 같은 칸 충돌은 D9-3(① 포함 관계 = 긴 쪽 하나 · ② 숫자 다름 = resolved 하나(지속 짧은 · 시작 늦은 · 간격 긴 · 그 밖 원천 우선순위) + alternatives · ③ 숫자 없는 다른 문장 = 둘 다)으로, 대조본(extracted.json · products.json)은 정본과 같으면 same_as · 다르면 source_conflict 로 판정한다. 결정 파일 한 줄만 고친 뒤 step9-apply.py 로 결정론 반영하고, 끝 조건은 open 0 · 두 번 실행 cmp 같음 · 고정 시험 전부 PASS · check_explanations errors 0 · semantic-check errors 0. 트리거 예 — 「원장 항목 효과 지속 문장 바뀌었어」「적응증이 골드에 없대」「같은 시술에 지속 기간이 둘이야」「extracted.json 이 taxonomy 랑 달라」「새 section 이 필요해」「step9-apply 가 open 을 냈어」「step9-explanations 갱신」「설명 사실 원장 점검」.
---

# Procedure Hub 설명 사실 판정 · 실버 설명 사실 원장 갱신

실버 9단계(설명 사실, 2026-11-01)에서 실제로 한 방법을 옮긴 것이다. 새로 지어낸 절차가 아니다.
8단계(관계 · 안전 — `procedure-hub-relation-check`) 다음 단계다. 1~8단계가 추천 · 안전 위주라 끌어올리지 않던 **설명 문장**(「언제부터 효과가 나나 · 얼마나 가나 · 어떻게 작용하나 · 어디에 쓰나」)을
**원천에 적힌 그대로** 이미 있는 노드의 속성으로 붙인다. 노드 · 엣지 종류는 늘지 않는다.

- 정본 원장: `orchestration/work/phub-recommend/step9-explanations.json` · `.md` — 현재 값 = `scripts/check_explanations.py` 출력. 숫자를 여기 박지 않는다
- 결정(사람이 고치는 곳): `step9-decisions.json` — 종류 식 `kinds` · 규칙 `rules`(R9-1~R9-8 · R9-2b · R9-5b · G9-1) · section 표 `section_map` · 새 section `new_sections` · 붙이지 않는 행선지 `attach_status_unattached` · `concern_item_unattached_kinds` · 충돌 처리 `conflict_resolution`(D9-3) · 대조본 규칙 `extracted_json_rule` · `products_json_rule` · 값 사전 `value_dictionary` · 사용자 판단 `user_decisions`(D9-1~D9-9)
- 결정론 반영: `step9-apply.py`(입력 = 결정 · 원천 7파일 · 실버 정본 step1 · 2 · 5 · 7 · 8 → 출력 `step9-explanations.json` · `.md`) · 가드 시험 `step9-fixture-test.py` + `step9-fixtures/cases.json` · 효과 재셈 `step9-effect.py`(A 행 닫힘 · 읽기만)
- 결정 정본: `_RESUME.md` §2 2026-11-01 「9단계 — 추천으로 데이터 결정하자」 · 조사 `step9-research.md` · `.json`(조사 판 · 셈은 조사 때 값)
- 원천: `step9-decisions.json source.path`

**원장 · 결정 파일은 승인 없이 고치지 않는다.** 판정 → 결정 목록(사람) → 결정 한 줄 → 반영(스크립트) → 점검 고리를 그대로 돈다. 1~8단계 산출 · 원천은 고치지 않는다(앞 단계 값이 틀려 보이면 보고). 골드 빌드 · 허브 코드는 이 스킬 밖(section 반영은 허브 발주).

## 1. 언제

| 경우 | 시작점 |
|---|---|
| ① 원천 새 스냅샷(taxonomy items · products extracted · 계열 extracted · products.json · procedure-profiles · problem-packages · complications · post-procedure-timeline) | `step9-apply.py --out <scratchpad> --source <폴더>` 의 open → §2 |
| ② 앞 단계가 바뀜(5단계 attach · 단위 시술 · 7단계 고민 항목 · CC 대응 · 8단계 합병증) | `step9-apply.py` 재실행 — open 「붙는 노드 없음」 이면 그 단계부터(unit-check · concern-check · relation-check) |
| ③ 새 설명 칸(종류 식 밖) | `kinds` 한 줄 + `section_map` 한 줄(최종 판단) — 규칙이 닿는 원천 칸 전부를 먼저 센다 |
| ④ 같은 노드 · 같은 칸에 값이 둘 | D9-3 — §2-3. 규칙 바꾸기는 최종 판단(사용자) |
| ⑤ 정기 점검 · 결정을 고친 뒤 | `scripts/check_explanations.py --selftest` — errors 0 · selftest 전부 잡힘 · 그다음 semantic-check |

```bash
python3 <스킬>/scripts/check_explanations.py --work orchestration/work/phub-recommend --out <scratchpad>/explanation-check.json --selftest
```

`errors[]` = 원장 낡음(재생성과 바이트 다름) · 결정론 아님 · open · 사람 확인 남음 · summary 셈 불일치 · 붙음인데 노드 없음 · **붙는 노드가 실버에 없음** · section 이 허용 집합 밖 · 붙이지 않음 · 대조본인데 노드 있음 · emit 이 그 노드에 안 붙음 · **② 인데 숫자 값이 하나가 아님 · alternatives 가 emit 에 섞임** · ③ 인데 multi_source 없음 · same_as 로 접힌 것이 emit 에 · fact_ids 꼴(G9-1) · 값 사전 수 ≠ 원천 · section_map 이 8단계 실버 밖 · 고정 시험 FAIL.
`--selftest` 는 원장 사본에 틀린 값 10가지를 넣어 각각 잡히는지 본다.

## 2. 판정 순서

원천 잎 하나마다 위에서부터. 앞에서 끝나면 뒤로 가지 않는다. 상세 `references/rules.md`.

### 2-1. 설명 사실인가(종류 식)

`kinds` 정규식(K1 효과 시작 · 지속 ~ K11 고민 상세)에 걸리면 대상. **A 실패에 나온 필드만이 아니라 같은 종류 필드 전부**(onset_duration 은 items · products · 계열 · extracted.json 네 자리). K10(최적화 중증도 단계)은 7단계 조합에 이미 있어 대상 밖. 규칙이 없는 대상 칸 = open.

### 2-2. 붙는 자리 = 앞 단계가 정한 대응(새 대응표 없음)

1. 원장 항목(taxonomy items) → 5단계 `extracted[].attach`(제품 · 단위 시술 · 후보 전부 + candidates · 원문 보관 = 붙이지 않음)(R9-1)
2. taxonomy products → 5단계 `taxonomy_products`(제품 · S8 단위 시술)(R9-2) · products.json 은 이름으로 대조(R9-2a — 같은 칸 있으면 same_as/source_conflict · 없는 칸만 싣기) · 이름이 없으면 원장 항목 이름이 전부 같은 제품일 때만(R9-2b)
3. 계열 extracted = taxonomy 정본만(R9-3) · extracted.json 은 대조(D9-4) · 프로파일 moa_summary(R9-4) · 하위 분류 description = 계열 + sub_family(R9-8 · D9-9)
4. 고민 쪽 = 7단계 항목(고민 노드 · 항목의 concern · 시술 이름이면 resolve 단위 시술 + `cc:` 조건 · 단위 시술 없으면 resolve 계열)(R9-5 · R9-5b · D9-5) · 부위 · 시술 아님 항목 = 붙이지 않음
5. 합병증 · 부작용 설명 = 8단계 실버 그대로 · section 만(R9-6 · D9-1 management · prevention → `safety.management`) — 실버 값과 원천이 다르면 open
6. 반응 · 중증도 단계 = 값 사전(R9-7 · D9-7 → semantic.json value_dictionary · 골드 globals)
7. **노드는 실버에 있는 id 만** — 골드 export 를 읽지 않는다. 없으면 open(앞 단계부터)

### 2-3. 같은 노드 · 같은 칸(D9-3 — D-13b 방향)

| 분류 | 조건 | 처분 |
|---|---|---|
| 같음 | 원천 여럿 · 정규화 같음 | 한 행 · same_as |
| ① 포함 관계 | 한쪽이 다른 쪽을 정규화 포함 · 또는 숫자 집합이 같고 문장만 다름 | 긴 쪽 하나 · 짧은 쪽 same_as |
| ② 숫자 다름 | 포함으로 안 접힌 대표가 둘 이상 · 숫자 집합이 서로 다른 대표가 둘 이상 | **resolved 하나** — 지속 · 유지 = 상한이 짧은 쪽 · 시작 = 하한이 늦은 쪽 · 간격 · 회복 · 대기 = 긴 쪽 · 그 밖 · 기간을 못 읽음 = 원천 우선순위 · 나머지는 alternatives(골드엔 안 나감) |
| ③ 숫자 없는 다른 문장 | 숫자 있는 대표가 하나 이하 | 둘 다 실음 · multi_source |

배열 칸(indications · related_techniques · alternatives)은 원소마다 한 사실 — ② 를 쓰지 않는다. 「직후 · 즉시 · 즉각 · 당일 · 바로」 = 0일.

## 3. 갱신 방법

1. 판정 → 결정 목록(사람 승인) → `step9-decisions.json` 한 줄
2. `python3 step9-apply.py` 두 번 → `cmp` 같음 · open 0
3. `python3 step9-fixture-test.py` 전부 PASS(규칙마다 실물 기대값 — 조사 md 의 잘린 목록에서 옮기지 않는다)
4. `scripts/check_explanations.py --selftest` errors 0
5. `semantic-build.py` 재생성 → semantic-check errors 0(값 사전 · 설명 사실 셈이 시맨틱에 들어간다)
6. `python3 step9-effect.py` — A 행 닫힘 재셈(보고)

## 4. 끝 조건

open 0 · 사람 확인 0 · 두 번 cmp 같음 · 고정 시험 전부 PASS · check_explanations errors 0 · selftest 전부 잡힘 · semantic-check errors 0.

## 5. 변경 보고 형식

```text
9단계 갱신 — <원천 · 결정 한 줄>
레코드 N(붙음 · 붙이지 않음 · 대조본 · source_conflict) · node_slots · fact
D9-3: 한 원천 · 같음 · ① · ② (짧은 · 늦은 · 우선순위) · ③ · alternatives
open 0 · 고정 시험 n/n · check errors 0 · semantic errors 0
A 행 닫힘(step9-effect) — 실버로 · 골드 section 으로 · alternatives 에만 · 안 닫힘
```

참고: `references/rules.md`(규칙 · 셈) · `references/record-schema.md`(칸) · `references/mistakes.md`(틀린 것).

# 기록 형식 — step6-decisions.json · step6-packages.json

출처: `orchestration/work/phub-recommend/step6-decisions.json` · `step6-packages.json` · `step6-apply.py`. 칸은 실제 파일에서 옮겼다. 셈은 `scripts/check_packages.py` 출력에서 본다.

## 1. step6-decisions.json — 사람이 고치는 곳

| 칸 | 무엇 |
|---|---|
| `source.path` | 원천 스냅샷 폴더(taxonomy · market-pricing · synergy) |
| `canon.step5` | 읽는 5단계 정본(`step5-units.json`) |
| `rules` | R1~R11 규칙 문장(정본 — `references/package-rules.md` 는 요약) · `R2` = 구성 낱말 → 키 대응표 |
| `kinds` | kind 값 — 「일반 패키지」 · 「회차 묶음」 · 「병원 시그니처」. 밖이면 open |
| `recommend_rule` | 시그니처 = 추천 노출 기본 제외 |
| `backport_step5[]` | 패키지 아님 → 5단계 단위 시술로 돌린 행 `{id, ledger_id, name, to}` — apply 가 5단계 정본에서 그 행이 `to` 키를 가리키는지 확인 |
| `packages[]` | 패키지 한 줄 — 아래 |
| `non_packages[]` | 묶음 이름 `{id(taxonomy 하위 id), label, verdict, to}` — `to` 에 「menu_group(P6-NN~NN)」이 있으면 apply 가 그 번호와 `packages[].menu_group` 을 대조 |
| `handoffs[]` | 5단계 handoffs 「2단계 deferred」 의 6단계 행 → `{source, covered_by[non_packages id], note}` |
| `origin_questions[]` | `{id: Qnn, question, packages[], target?}` |
| `source_fix[]` | 원천 수정 후보 `{ledger_id, name, field, now, proposal}` — 원천은 고치지 않는다 |

### 1-1. packages[] 한 줄

```json
{
 "id": "P6-05", "research_id": "P6-05", "name": "꿀광토닝",
 "kind": "일반 패키지", "shape": "일반 패키지(다른 계열)",
 "source": "ledger", "ledger_id": "auto-M8-1775402572157",
 "menu_group": null,
 "same_day_raw": "명시 없음 — overview 「결합하여 … 동시에 제공하는 복합 시술」(「동시에」는 효과 문장)",
 "recommendable": true,
 "components": [
  {"text": "레이저토닝", "basis": "detail · 5단계 U5-023 동의어 「레이저토닝」", "unit": "U5-023"},
  {"text": "스킨부스터", "basis": "detail · mechanism 「스킨부스터의 히알루론산 주입」 · 부위 J2 얼굴 전체", "unit": "U5-018"}
 ],
 "notes": ["…"],
 "step8_notes": [{"pair": ["U5-023", "U5-018"], "links": [56], "verdict": "다름 — synergy 「스킨부스터 2주 후 레이저토닝」 …"}],
 "decided_by": "step6-research 추천 · R1~R11 · U3 · U4(10-29 사용자 「추천으로 가자」)"
}
```

- `source: "market"` 이면 `ledger_id` 대신 `market_names[]`(시장가 행 이름 원문 — 둘 이상이면 한 패키지로 합친 행 · R6)
- 시그니처: `"kind": "병원 시그니처"` · `"menu_group": "M9-SIG 「시그니처 프로그램」"` · `"recommendable": false` · `"price_raw": "950만원"`(detail 안 글자)
- `menu_group` 형식 = `<taxonomy 하위 id> 「<라벨>」` — `check_packages.py` 가 원장 행이 그 라벨 하위에 있는지 본다

### 1-2. components[] 한 줄

| 칸 | 엣지 | 슬롯 | 뜻 |
|---|---|---|---|
| `text` | ○ | ○ | 원문 낱말(원천 칸에서 다시 찾을 수 있어야 — 엣지) |
| `basis` | ○ | ○ | 원천 칸 · 문구 · 키 근거 |
| `unit` | ○ | — | 5단계 키 |
| `candidates[]` | 선택 | ○ | 후보 키 |
| `origin_question` | 근거 약이면 필수 | **필수** | Qnn |
| `evidence_level` | 「약」 | — | 정체 · 투여 방식 미상 |
| `quantity_raw` · `sessions` | 선택 | 선택 | 수량 원문 · 회차 수 |
| `missing_unit` | — | 선택 | 5단계에 없는 키 서술 |

슬롯 예(5단계에 키 없음):

```json
{"text": "인모드바디", "basis": "detail — 1단계 「인모드」는 얼굴 RF 키뿐 …", "missing_unit": "M9 RF × 바디 부위 × K05 — 5단계에 없음 …", "origin_question": "Q07"}
```

회차 엣지 예:

```json
{"text": "얼굴 전체 콜라겐부스터 × 3회", "basis": "시장가 이름 · 5단계 market units · sessions 3", "unit": "U5-090", "quantity_raw": "3회", "sessions": 3}
```

## 2. step6-packages.json — 산출(손으로 고치지 않음)

| 칸 | 무엇 |
|---|---|
| `summary` | packages · by_kind · recommendable · source_rows(ledger · market) · edges · edges_weak · slots · slots_missing_unit · packages_full · packages_no_edge · non_packages · handoffs · step8_notes · step8_verdicts · origin_questions · source_fix · open · stale_decisions |
| `packages[]` | 노드 — id · name · kind · menu_group · same_day_raw · recommendable · synonyms(원장 이름 · 시장가 이름) · price(원장 detail raw / 시장가 low · mid · high · unit_raw) · description(extracted overview · mechanism · onset_duration) · components(셈) |
| `contains[]` | 엣지 — package · order · text · basis · unit · unit_name · quantity_raw · sessions · evidence_level · origin_question |
| `slots[]` | 슬롯 — package · order · text · candidates · candidate_names · origin_question · missing_unit |
| `non_packages[]` | 묶음 이름 + family · items(그 하위 항목 수) |
| `step6-to-step8-notes[]` | 8단계 메모 — pair · links(synergy from · to · type · timing) · verdict |
| `open[]` · `stale_decisions[]` | 0 이어야 |

## 3. open · 오류 — 어느 스크립트가 무엇을

| 무엇 | `step6-apply.py` open | `check_packages.py` |
|---|---|---|
| 결정 없는 패키지 원천 행 · 이름 바뀜 · 시장가 행 원천에 없음 | ○ | open |
| 구성 키도 질문도 없음 · 근거 약인데 질문 없음 | ○ | open |
| 패키지인데 구성 없음 | ○ | open(+ 「구성도 질문도 없는 패키지」) |
| 시그니처인데 추천 노출 · kind 값 밖 | ○ | 오류 |
| 결정이 가리키는 키 · 원천 질문 없음 | ○ | 오류 |
| 가격 원문이 detail 에 없음 | ○ | 오류 |
| 묶음 이름 행선지 번호 ↔ menu_group 대조 | ○ | — |
| menu_group ↔ 원천 하위 라벨 · non_packages 에 그 하위 | — | 오류 |
| **구성 원문이 원천 칸에 없음 · 적응증에만 있음** | — | 오류 |
| 회차 ↔ 5단계 시장가 sessions | — | 오류 |
| 넘겨받은 것 행선지 없음 · 키 없음 | ○ | open · 오류 |
| synergy 링크 번호 없음 · 5단계 보강 안 됨 | ○ | — |
| 5단계 정본 ↔ 5단계 결정 행선지 어긋남 · 원장 낡음 · summary 불일치 | — | 오류 |

# step9-explanations.json 칸

| 칸 | 뜻 |
|---|---|
| `summary` | 셈(레코드 · 붙음 · node_slots · facts_out · d93 · d93_resolved_by · alternatives · source_conflicts · value_dictionary · section_map · facts_by_section · nodes_by_kind · human_check · open) |
| `records[]` | 원천 잎 하나 = 레코드 하나 |
| `node_slots[]` | (노드, 칸) 하나 — D9-3 처분 · 골드로 나갈 fact |
| `source_conflicts[]` | 대조본이 정본과 다른 칸(싣지 않음) |
| `value_dictionary[]` | 값 사전(D9-7) |
| `section_map[]` | 8단계 실버 합병증 · 부작용 칸 → section(R9-6) |
| `new_sections[]` | 새 section(safety.management) |
| `open[]` | 비어야 끝 |

## records[]

```json
{"id": "S9:taxonomy.modality[0].subcategories[2].items[5].extracted.onset_duration.duration",
 "rule": "R9-1", "kind": "K1", "slot": "onset_duration.duration", "text": "<원천 원문 그대로>",
 "source": {"file": "taxonomy", "path": "<원천 경로>", "record": "<원장 항목 · taxonomy products id>"},
 "attach": {"nodes": ["unit_procedure:U5-010", "unit_procedure:U5-011", "unit_procedure:U5-012"], "status": "단위 시술", "flags": [], "rank": 0},
 "section": "recovery", "status": "붙음"}
```

- `status` = 붙음 · 붙이지 않음(<행선지>) · 대조본 같음(same_as …) · source_conflict(싣지 않음)
- `attach.flags` = `candidates`(5단계 후보 전부) · `cc:<CC [상세]>`(D9-5) · `sub_family:<하위 라벨>`(D9-9)
- `attach.rank` = D9-3 원천 우선순위(0 그 노드 자신의 원장 항목 · 1 taxonomy products · 2 후보 · 3 계열 · 4 고민)
- `text` 는 요약 · 번역 · 숫자 정규화 없음

## node_slots[]

```json
{"node": "product:M10-1-1", "slot": "onset_duration.duration", "section": "recovery", "sources": 2, "records": ["S9:…", "S9:…"],
 "class": "②", "resolved": "S9:…", "resolved_by": "짧은 쪽", "alternatives": ["S9:…"],
 "emit": ["S9:…"], "same_as": {}, "fact_ids": ["product:M10-1-1#recovery#step9[taxonomy.modality[…]…]"]}
```

- `class` = 한 원천 · 같음 · ① · ② · ③
- `emit` = 골드로 나갈 레코드(② 는 resolved + 숫자 없는 대표) · `alternatives` = ② 의 나머지(골드엔 안 나감 · 보관)
- `same_as{대표: [접힌 레코드]}` · `multi_source: true` = ③ 또는 원천 여럿 배열 칸

## section_map[]

`{"path": "complications.categories[1].complications[0].management", "silver_id": "SE-M2-01", "silver_where": "side_effect", "field": "management", "section": "safety.management", "node": "family:M2"}`

## 실제 행(반영 판)

- ① `product:M1-1-1` onset_duration.duration — taxonomy products 문장(긴 쪽 · 「…발현, 3-4개월 지속」) 하나 · 원장 항목 「3-4개월 지속」 same_as
- ② `product:M10-1-1` onset_duration.duration — resolved 「3-6개월 유지 …」(짧은 쪽) · alternatives 「6-9개월」
- ② `product:M1-2-3` onset_duration.onset — resolved 「3-7일」(늦은 쪽) · alternatives 「2-3일」
- ③ `product:M1-1-1` overview — taxonomy products · 원장 항목 두 문장 둘 다
- R9-2b `products.energy_device.products[4].type` → `product:M9-2-3`
- R9-5b `taxonomy.problem[3].subcategories[2].items[1].detail`(줄기세포치료 · 전신) → `family:M17`

# silver-v3 — ERD v3.1(동결) 실버 빌더

동결 ERD **v3.1**(`../ERD-FROZEN.md` v3.1 절 · 2026-11-05)대로 브론즈 22(원장 21 + `../step1-products.json`)를 실버 레코드로 만드는 결정론 빌더. Python 3 표준 라이브러리만. 1차~4차는 ERD v2.4, 5차 v3, **6차부터 v3.1**(아래 「6차 빌드」).

## 실행

```bash
cd silver-v3
python3 build.py --bronze ../bronze/phub-ledger \
  --erd ../erd-v3.1.json --dict ../erd-v3.1-dictionaries.json --decisions decisions/ --out out/
python3 check.py            # 검산 ①~⑨ + V3-1~V3-10 + V3.1-1~V3.1-10 (④ 는 빌드를 두 번 새로 돌려 out/ 과 바이트 대조)
```

인자는 전부 기본값이 위 경로다(`python3 build.py` 만으로 같다). 더 받는 인자:

| 인자 | 뜻 |
|---|---|
| `--step1` | 22번째 브론즈(기본 `../step1-products.json`) |
| `--colmap` | 잎 키 행선지 표(기본 `../erd-v3.1-column-map.md`) — 개체 속성 출처 보조 · 커버리지 대조 |
| `--tuples` | ERD 실측(기본 `../erd-v3.1-tuples.json`) — report §5 · check ③ 대조 |
| `--tuples-prev` | 이전 판 실측(기본 `../erd-v3-tuples.json`) — 참조 구현 adverse summary 의 v3 대조 키(v3_comparison · 수식어 표 v3_unregistered)를 같은 값으로 만든다 |
| `--bootstrap` | `decisions/_bootstrap/` 을 ERD 의 approved 결정 19 로 (다시) 쓴다 |
| `--propose` | `decisions/proposed/` 에 결정 묶음 1 제안을 쓴다. status 가 proposed 가 아닌 파일(사람이 바꾼 것)은 덮지 않는다 |
| `--propose4` | `decisions/batch4-proposed/` 에 결정 묶음 4(동의어) 제안을 쓴다 — 게이트 `out/gate/batch4.json` 옵션마다 결정 파일 하나(같은 항목 옵션은 배타 · 같은 규칙으로 덮지 않음) |

브론즈 검증(exit 2 로 거부): `--bronze` 폴더에 `HASHES.txt` 가 있으면 원장 21 을 그 해시로(2판~ · manifest `bronze_version` = 폴더명 + CHANGELOG 최신 판), 없으면 `erd-v2.4.json → source_files` 해시로(1판). step1 은 늘 ERD 해시. 기본 `--bronze` = `../bronze/phub-ledger`(원장의 집 · 2판) · 1판 = `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26`(1판으로 돌리면 3차와 바이트 동일). check.py ① 도 같은 규칙.
`out/` 은 매번 지우고 다시 쓴다. 빌드 시각은 표준 출력에만 — 재실행하면 `out/` 이 바이트 동일하다.

## 빌더 완성 조건 — 적합성 시험(`tests/`) + 검산(`check.py`)

**빌더 완성 = `python3 tests/run_tests.py` 전부 PASS + `python3 check.py` 전부 PASS.** 빌더는 ERD 가 바뀔 때만 고친다 — 새 원장 판·새 결정은 시험이 이미 덮은 경우의 수 안에서 돈다.

```bash
cd silver-v3
python3 tests/run_tests.py            # 경우 목록(erd-v3.1.json 에서 기계로 · 2,514) → unittest 전부 → 모든 경우에 시험이 있는지(없으면 FAIL)
python3 tests/run_tests.py -v -k Edge # 이름 부분 일치만(이때 커버리지 검사는 건너뛴다)
python3 tests/enumerate_cases.py --out /tmp/cases.json   # 경우 목록만
python3 build.py && python3 check.py  # 실제 원장(브론즈 2판) 빌드 · 검산 29
```

| 파일 | 하는 일 |
|---|---|
| `tests/enumerate_cases.py` | `erd-v3.1.json`(+ 사전 이름)에서 경우를 뽑는다 — 결정 kind 20 × target/new_value 분기 · ref 구조체 5 × 관계 31(R29 없음 · R32) 양끝(허용 = accept · 허용 밖·만들 수 없는 관계 = reject) · 분해 규칙 잎 키마다 양성·음성(목록은 원소마다 — 수식어 138 · 패턴 5 · shape · class 포함) · 결과 열거형 값 · 충돌 ④⑥⑦⑧⑨ 생애 · 적용 순서 ⓪①~⑦·안정 키 · 브론즈·출처·재실행 |
| `tests/run_tests.py` | 러너 — 시험 FAIL · 시험 없는 경우 · ERD 에 없는 경우를 가리키는 시험 → exit 1 |
| `tests/synth.py` | 합성 원장 21 + step1(실제 원장의 키 경로·레코드 모양만 따르는 가짜 데이터) · 합성 사전 · 합성 결정 · 작업 폴더(HASHES.txt · CHANGELOG) |
| `tests/test_rules_procedure.py` · `test_rules_adverse.py` | §1.3·§1.4·§1.5·§1.6 분해 규칙(stopwords 단어마다 · 회·차 자리 · 겹침 · 조합 기호마다 · 조직층·수식 값마다 · 세 칸 단위 · 경과 엣지 · 수식어 단어·패턴마다 · phrase_shape · fragment_classes · 문구 사전 · 고지 · 조건 단위) |
| `tests/test_decisions.py` | 결정 kind 20 · 분기 · 적용 순서(이웃 단계 의존 · ① 안 kind 순서 · 같은 단계 decided_at → id) · 안정 키(허용 · 파생 id 거부) · 옛 네 칸·옛 표현 지정의 v3.1 변환 |
| `tests/test_edge_refs.py` | edge_create ref 구조체 × 관계 31 — 합성 빌드 한 번에 경우마다 결정 하나(R32 · 조건 단위 dict_value 포함) |
| `tests/test_conflicts.py` · `test_bronze.py` | 충돌 생성·override·close·fold 닫힘 · 브론즈 판 교체·거부 · 출처 필수 · 재실행 바이트 동일(`tests/_core_build.py` 두 번) |

시험은 합성 데이터만 쓴다(실제 원장·실제 결정은 `check.py` 몫). 경우 id 는 `@covers(...)`(정적) · `mark(...)`(데이터 주도 시험이 경우를 실제로 돌렸을 때) 로 시험에 대응시킨다.
ERD 가 바뀌면(관계·kind·규칙 키·열거형 값이 늘거나 줄면) 경우 목록이 바뀌고 러너가 빠진 시험을 FAIL 로 드러낸다.

## 빌드 순서

1. 입력 검증(해시 22) → 결정 저장소 읽기(검증 · approved 만 적용 대상)
2. 사전 단계 ① `dictionary_add` · ④ `event_split` → 사전을 바꾸고 분해를 다시 돌린다(ERD 사전 그대로의 분해도 같이 돌려 ERD 실측과 대조)
3. 분해 `lib/decompose.py` — `erd-v2.4-tuples.py` 상속 사슬의 최종 로직을 한 모듈로(같은 튜플 · 같은 id · 같은 등록 순서)
4. 개체 21 · 원장 메모 결정(질문 23 · 원장 작성자 · approved) 적재 · ⓪ `reclassification`(R2 만)
5. anchor 지도에 ② `canonical_mapping` → ③ `tuple_assign` / `tuple_assign_multi` / `adverse_tuple_assign` → ④ `fold_approve`
6. 관계 31 (anchor 끝을 최종 튜플 id 로) → ⑤ `edge_create`
7. 충돌 ④⑥⑦⑧⑨ → ⑥ `conflict_override` / `conflict_close` → ⑦ `exclude`
8. 기록만 kind(`ledger_correction_note` · `verification_hold` · `conflict_resolution` · `scope_review`)는 적용 로그에 recorded

같은 단계 안은 `decided_at` 순(같으면 id 순).

## 결정 파일 형식

`decisions/` 아래 아무 폴더의 `*.json` 하나 = 결정 하나(`_` 로 시작하는 파일은 목록·색인이라 읽지 않는다).

```json
{
  "id": "DEC-2026-11-05-01",
  "kind": "adverse_tuple_assign",
  "target": {"locator": "complications.json:categories[].complications[].name@M2/5", "kind": "raw_name"},
  "new_value": {"tuples": [{"event_id": "DIC-…", "site_id": "none", "qualifier_id": "none"}], "courses": ["지연"]},
  "reason": "왜",
  "decided_by": "사람",
  "decided_at": "2026-11-05",
  "status": "approved",
  "source_refs": [{"kind": "ledger", "ref": "file:path@rec"}]
}
```

- `status`: `approved` 만 적용 · `proposed`·`rejected` 는 목록만(manifest `listed_not_read`)
- `target` 은 안정 키만 — CAT- · REF-(…#m<i>) · 원장 locator · MOD-/SUB-/PRD-/SIT-/TEC- · 사전 값 · conflict.stable_key. **PRC-/ADV-/CFL- 를 쓰면 거부**(manifest `invalid`)
- kind 별 target·new_value 모양은 `erd-v3.1.md §5.2`(kind 20). 덧붙인 것: product_name 의 `dictionary_add` 는 `new_value.code`(계열)를 읽는다 · person_condition 의 `dictionary_add` 는 `new_value.kind` · ⑧ conflict 의 stable_key 에는 `value`(조각)가 있다 · edge_create dict_value person_condition 은 `dict.kind` 로 kind 를 가를 수 있다
- `conflict_override`·`conflict_close` 의 `target.conflict_key` 는 `out/conflicts.jsonl` 의 `stable_key` 를 그대로 복사한다
- `adverse_tuple_assign` 의 locator 는 ERD 꼴 complications 이름(`…name@M2/5`) — `out/entities/adverse_effect.jsonl` 의 `anchor`. 문구는 `phrase_map`(target `phrase_id` PHR- 또는 `normalized` — `out/dictionaries.json` phrase_dictionary · `out/gate/unlinked_phrases.json`)

`decisions/_bootstrap/` = ERD 가 approved 로 둔 19(전부 기록만 kind). `decisions/proposed/` = 결정 묶음 1 제안(`_INDEX.md` 참고) + `templates/`(ERD-FROZEN 「결정으로 넘긴 것」 빈 템플릿).

## 재빌드 절차(2차)

1. `decisions/proposed/*.json` 중 승인할 파일의 `status` → `approved`, `decided_by`·`decided_at` 채우기(그대로 두거나 다른 폴더로 옮겨도 된다)
2. `python3 build.py` → `python3 check.py`
3. `out/manifest.json → decisions.apply_log` 에 결정마다 단계·결과(applied / no_target / rejected)
4. check ③ 은 ①~④ 단계 결정이 적용되면 「ERD 사전 그대로 분해 = ERD 실측」만 본다(실버 산출물은 결정만큼 달라진다)

## 3차 빌드 · 결정 묶음 2A / 게이트 2B

- `decisions/batch2a/` — 사용자 승인(2026-11-04 「진행」) 추천 매핑 8: ① dictionary_add 7(크라이오·수액·줄기세포 → 계열 · 혈관레이저·다이오드 → M8 하위분류 · CO2·Nd:YAG → M8 계열) · ② canonical_mapping 1(「HA」 — 계열 힌트 M2 참조 자리만).
- ② canonical_mapping 중 **from_ref 가 라벨(조각)이고 scope 가 REF- 목록**인 것은 미해결 참조라 튜플이 없으므로, 분해 때 그 anchor 안에서만 조각을 to_id 로 읽는다(`lib/decompose.py scoped_label_spans`). 적용 로그는 ② 단계에 남는다.
- `baseline/manifest-2차.json` = 2A 전 2차 manifest → report §10(1차→2차) · §11(2차→3차).
- 게이트 2B: 빌드가 `out/gate/batch2b.json`·`.md` 를 쓴다(`lib/gate2b.py` — 템플릿 11 항목을 하위 항목까지 펼친 선택지 · 옵션마다 결정 파일 본문). 고른 답 → 결정 파일:
  `python3 apply_gate.py --answers answers.json [--recommended] [--dry-run]` → `decisions/batch2b/`(answers = {항목 id|하위 id: 옵션 key} · `{}` + `--recommended` = 전부 추천대로).
- ⚠ 현재 빌더는 tuple_assign(_multi) 를 미해결·조합 참조 anchor 에 적용하지 못한다(apply_log rejected) — 게이트의 해당 옵션에 `builder_applies_now=false` 로 표시.

## 4차 빌드 · 브론즈 2판 + 결정 묶음 2B

- 사용자 답 67(`decisions/batch2b-answers/answers/`) → `_answers.json`(64 · note 는 reason 에) → `apply_gate.py --gate decisions/batch2b-answers/_gate-batch2b-3차.json`(사용자가 본 3차 게이트 고정본) → `decisions/batch2b/` 57. 결정 안 만든 3 = `_not_applied.json`(slash 03·08·12 — 2판에서 anchor 가 사라짐).
- `baseline/manifest-3차.json` · `baseline/unresolved_references-3차.json` → report §12.
- 결정 provenance: source_refs 의 ERD 꼴 locator 는 원장 위치로 옮겨 derived_from 에 넣는다 · scope_review target.erd_ref 가 ERD 결정 erd_ref 가 아니면 R24 erd 엣지를 만들지 않는다(해석 보류에 기록).

## 산출물

```
out/
  manifest.json            입력 해시 22 · ERD/사전/잎 키 표 해시 · 결정 적용 로그 · 산출 파일 해시 · 결정론 키
  entities/<type>.jsonl    20종(v3.1). {id, type, status, attrs{이름: [칸]}, aliases[칸], provenance[{file,path,rec}], derived_from[]}
                           칸 = {value, prov:[{file,path,rec}]}(원장 잎) 또는 {value, derived_from:[locator]}(파생)
  relations/R1..R32.jsonl  31(R29 없음 · v3.1). {relation, from{type,id}, to{type,id}, attrs{이름: 칸}, provenance[], derived_from[]}
  dictionaries.json        적용된 사전(⓪① 반영 · ⑦ 제외 표시 · 문구 사전 phrase_dictionary = 결정 뒤 항목 · ledger_locators)
  conflicts.jsonl          ④⑥⑦⑧⑨ — stable_key · values[] · status
  erd_comparison.json      결정 전 분해 요약 vs erd-v2.4-tuples.json (키마다)
  gate/                    unresolved_references · unregistered_fragments · unlinked_phrases · catalog_partial (.md/.json) · conflicts.md · batch3 · batch4 (.json/.md)
                           (6차부터 batch2b 는 만들지 않는다 — 답이 끝났고 3차 고정본은 decisions/batch2b-answers/_gate-batch2b-3차.json)
  report.md                수치 · ERD 대조 · 제안 · ERD 개정 후보 · 잎 키 커버리지 · 해석 보류
```

locator = `<파일>:<잎 키 경로>@<rec>` — 경로는 컬럼 스캔과 같은 접기(배열 `[]` · 코드 키 `{code}`), rec 는 `[]`·`{code}` 마다 실제 위치·키를 `/` 로(파일 루트 잎은 `-`).
파생 값의 `derived_from` 은 원장 locator · `erd-v2.4.json#/…` · `erd-v2.4-dictionaries.json#/…` · `DEC-…` · `decisions/<파일>` 중 하나다(check ② 가 전부 해석한다).

## 모듈

| 모듈 | 하는 일 |
|---|---|
| `lib/load.py` | 브론즈 적재·해시 검증 · 잎 키 행선지 표 파싱 |
| `lib/provenance.py` | 잎 순회 · locator 만들기/해석 |
| `lib/decompose.py` | §1.3 참조 분해 · §1.4 시술 튜플(v3.1 회·차 자리 · stopwords 겹침) · v3 부작용 분해(멤버 · 원칙 B·C · 조립 — v3.1 단위가 그대로 쓴다) · 엣지 끝 분포 |
| `lib/adverse31.py` | v3.1 §1.5 부작용 단위(세 칸) · 수식어 목록 · 문구 사전 · R15 경과 · 필수 고지 문구 · §1.6 조건 단위 — 참조 구현 `erd-v3.1-tuples.py` 의 v3.1 부분 |
| `lib/units31.py` | 실버 부작용 단위·문구 사전 지도(결정 ① phrase_map · ③ adverse_tuple_assign · ⑤ 이 바꾸는 곳) · 조건 단위(문장 자리 → 단위) |
| `lib/refs.py` | 참조 자리의 원장 위치(엣지 provenance) |
| `lib/anchors.py` | anchor → 튜플 지도(결정 ②③④ 가 바꾸는 곳) |
| `lib/entities.py` | 개체 20(adverse_expression 없음) |
| `lib/relations.py` | 관계 31(R29 없음 · R32) · anchor 끝 확정 |
| `lib/conflicts.py` | 충돌 ④⑥⑦⑧⑨ |
| `lib/decisions.py` | 결정 저장소 · 원장 메모 결정 · 적용 ⓪~⑦ |
| `lib/proposals.py` | 결정 묶음 1 제안 · 빈 템플릿 |
| `lib/report.py` · `lib/reportmd.py` | out/ 쓰기 · gate · report · manifest |
| `lib/gate2b.py` · `apply_gate.py` | 결정 묶음 2B 게이트 자료 · 고른 답 → 결정 파일 |
| `lib/gate3.py` | 결정 묶음 3 게이트 자료(`out/gate/batch3.json`·`.md` — `decisions/batch3-proposed/` · 2B 와 같은 스키마) → `apply_gate.py --gate out/gate/batch3.json --out decisions/batch3b/ --answers …` |
| `lib/gate4.py` | 결정 묶음 4(동의어) 게이트 자료(`out/gate/batch4.json`·`.md` · 2B 스키마 · effect = 그 결정으로 다시 분해해 센 닫히는 문구·참조 수) · `--propose4` 제안 파일 → `apply_gate.py --gate out/gate/batch4.json --out decisions/batch4/ --answers …` |
| `lib/report6.py` | report §14(6차 · 5차 대비) |
| `tests/` | ERD v3 적합성 시험(위 「빌더 완성 조건」) |

## 5차 빌드 · ERD v3 + 결정 묶음 3 (2026-11-05 · 발주서 `../silver-build-5-brief.md`)

입력 기본값이 v3 로 바뀌었다(`erd-v3.json` · `erd-v3-dictionaries.json` · `erd-v3-column-map.md` · `erd-v3-tuples.json`). 분해 `lib/decompose.py` = `erd-v3-tuples.py` 상속 사슬의 최종 로직(결정 전 요약 166 키 · 튜플 등록 순서 · 표현 연결 · 분류 항목 → 튜플 차이 0 — check ③).

| V3 | 어디 |
|---|---|
| V3-1 수식 칸 | `decompose.AdverseTuples`(qualifier 사전 순서 · 접두 수식 가름 · 네 칸 id `adverse_unit_id`) · `anchors.AdverseUnits.unit_for(qualifier_id)` · `entities.build_adverse/build_expressions` |
| V3-2 회사·제품 괄호 | `decompose.Ids`(manufacturer_surface · product_company) · `Resolver.classify3`(inner 만) · `ProcedureTuples.assemble` V3-2 블록 |
| V3-3 stopwords | `Ids.stopwords` · `Resolver.decompose`(stopwords → qualifier_text) · `_annotate`(session_index) · 엣지 속성 `relations.Ends._v3` |
| V3-4 `+`/`/` | `Resolver.decompose`(sep) · `assemble` 괄호 안 대안 · 「무엇을 하나 × 부위 여럿」(multi_tuple · `#s<i>` · 부위 둘 이상일 때만) · combo member_mode · `anchors.build_anchor_map`(multi) · `relations.Ends.of` |
| V3-5 site.kind | `decompose.site_kind_of` · `classify3`(layer_site) · `entities.build_sites`(kind) · `decisions.apply_tuples`(layer site 지정 거부) |
| V3-6 canonical_rename | `decisions.apply_rename`(① · DIC id 재계산 · renamed_from · 옛 정준값 동의어) |
| V3-7 description·media_refs | 값은 등록된 새 원천이 있을 때만(지금 0) — check V3-7 |
| V3-8 R5 하위분류 | `decisions.apply_tuples` canonical_mapping `R5:<하위분류 id>` · `relations` R5(basis ledger/canonical_mapping) |
| V3-9 anchor 확장 | `anchors.AnchorMap.establish/reassign_base` · `decisions.apply_tuples`(tuple_assign · _multi) · `conflicts.reference_conflicts`(세운 ⑨ 는 resolved) · `relations.Ends.of` |
| V3-10 ⑦ 닫음 | `conflicts.close_duplicates_by_fold`(쌍의 ⑦ → resolved · decision_id) |

- 결정 kind 17(+`canonical_rename` · ① 단계). `canonical_rename.new_value.synonyms`(dictionary_add 와 같은 모양 · `{value, is_marketing_name}`)는 빌더 확장. `dictionary_add` 의 site 값은 `new_value.kind`(V3-5)를 읽는다.
- ⑤ `edge_create` 의 `adverse_tuple` 끝(사전 값 네 쌍)이 기존 단위에 없으면 결정이 단위를 세운다(`decisions.prepare_edge_units` · 개체 적재 전).
- `decisions/batch3/` = 묶음 3 approved(`_INDEX.md`) · `decisions/batch3-proposed/` = 제안(status=proposed · 읽지 않음 · `_INDEX.md`).
- `baseline/manifest-4차.json` · `unresolved_references-4차.json` · `report-12-4차.md`(4차 report §12 그대로) → report §13(4차 대비 · v3 규칙만의 효과는 묶음 3 을 뺀 사전으로 한 번 더 분해해 가른다 · `lib/report5.py`).

## 적합성 시험으로 고친 구멍(2026-11-05 · 발주서 `../silver-conformance-brief.md`)

| 구멍 | 어디 | 실제 5차 빌드 영향 |
|---|---|---|
| edge_create `dict_value` 가 계열·하위분류·제품만 — 기법·부위·고민·고민 하위분류·분류 항목 사전 값과 고정 id(SIT-/TEC-/…) 거부 · 계열은 taxonomy 이름으로만 찾아 canonical_rename 뒤 새 정준값을 못 찾음 | `decisions.dict_entities` · `dict_value_end` | 없음(묶음 3 의 edge_create 5 그대로) |
| 관계 끝 문자열 파싱 — `(모든 개체·엣지·속성값)`(R25)·`person_condition(age_group)`(R17)·`adverse_expression(evidence_statement)`(R20) 을 개체로 못 읽어 그 끝 전부 거부 | `decisions.allowed_ends` | 없음 |
| 「무엇을 하나 × 부위 여럿」의 primary 멤버가 분류 항목(그 튜플에 site)에 닿으면 그 site 를 부위로 안 세어 multi_site(⑨) | `decompose.ProcedureTuples.assemble` | 없음(원장에 그 꼴 0) |
| 회사 사전 조각을 괄호 안 조각 하나(V3-2 scope) 밖에서도 읽고 규칙이 안 맞으면 조각을 버림(튜플이 됨) | `decompose.ProcedureTuples._manufacturer_scope` | 없음 |
| 항목 자신(ambiguous multi_site·multi_technique)의 site/기법 — 닿은 분류 항목 튜플의 값을 빼고 셈(site=그 값 하나 · extra_sites 누락) | `decompose.ProcedureTuples._self` | 없음 |
| 자유 텍스트 자리의 코드(M 코드만 · 하위분류 id · 분류 항목 id · synergy 「M9」)를 분해(튜플·⑨)함 — §1.4 code_references 는 노드·그 항목 튜플 | `decompose.ProcedureTuples.run_reference` · `relations.Ends.of`(via) | 없음(원장에 그 꼴 0) |
| 부작용 부위 나열(바로 앞 멤버)에서 온 부위의 site_basis 가 늘 member(site_list 를 못 냄 · member 문자열도 나열을 잃음) | `decompose.AdverseTuples.assemble` | 표현 1(「이마/눈가 당김감」 AEX-e022d617d7 candidates: 이마 site_basis member→site_list · member 「눈가 당김감」→「이마 / 눈가 당김감」) — 그 밖 바이트 동일 · check 19/19 |

ERD 공백(빌더는 그대로 둠 · 열린 것): `회`(횟수)는 「count 로 간다」(§1.3 stopwords) 지만 §3 관계 표에 count 속성 자리가 없다 — 지금은 참조 qualifiers 의 규격 조각으로만 남는다. stopwords 「관리」는 사전 값(분해가 읽지 않는 사전)과 겹친다 — ERD 「겹치는 단어 없음」 문장과 다르다(분해 사전 7 과는 안 겹친다).



## 6차 빌드 · ERD v3.1 + 엑소좀 approved + 결정 묶음 4 제안 (2026-11-05 · 발주서 `../silver-build-6-brief.md`)

입력 기본값이 v3.1 로 바뀌었다(`erd-v3.1.json` · `erd-v3.1-dictionaries.json` · `erd-v3.1-column-map.md` · `erd-v3.1-tuples.json` · 이전 판 실측 `erd-v3-tuples.json`).
결정 적용 전 분해 = `erd-v3.1-tuples.json` 요약(시술 73 · 부작용 117 · 조건 36 키) + 행 대조(튜플·단위 순서 · 이름 → 단위 · 문구 사전 항목 · R15 · 조건 단위 · 분류 항목) 차이 0 — check ③.

| V3.1 | 어디 |
|---|---|
| V3.1-1 product_reclassify(⓪) | `decisions.apply_product_reclassify`(product_name code 교체 · 같은 (계열|제품명) 있으면 합침) · `entities.build_products`(reclassified_from alias) · `relations` R4 이동 |
| V3.1-2 R32 | `relations`(고지 basis=ledger) · `decisions.ensure_product_note_rule`(locator 가 제품 note 문장이면 clinical_rule(product_note)) · `allowed_ends` |
| V3.1-3 dictionary_remove(①) | `decisions.apply_remove`(동의어 · 값 — 값은 in_use 판정: 지금 사전으로 분해해 쓰는 자리 · 개체 식별 사전은 늘 거부) · 이력 removed_synonyms/removed_entries |
| V3.1-4 조건 단위 | `adverse31.run_condition` · `units31.CondUnits` · `entities.build_conditions`(사전 단위 · raw_name · phrases 부록) · R16/R17 끝 = 단위 · source_phrases |
| V3.1-5 회·차 | `decompose.ProcedureTuples.run_reference`(R12 자리 session_index/count · 그 밖 qualifier_text) · `relations.Ends._v3`(session_count) |
| V3.1-6 겹침 | `decompose.stopword_overlap`(값 사전 전수 · 문구 사전 제외) |
| V3.1-7 필수 고지 | `entities.build_rules`(clinical_rule disclosure · 정규화 문장 하나 · phrase_ids) · R32 ledger · 문구 사전 kind=disclosure → R15 disclosure |
| V3.1-8 수식어 | `adverse31.AdverseUnits31.split`(단어 138 · 패턴 5 → parsed · 정규화형에서 뺀다) |
| V3.1-9 단위 세 칸 · 경과 엣지 | `adverse31`(단위 id = ADV-sha(event|site|qualifier) · 상대 부위 none) · `units31.AdverseUnits`(이름·문구 → 단위 · (이름|항목, 단위) → 경과) · `relations` R15.course(원칙 C) · R31 site 만 |
| V3.1-10 문구 사전 | `adverse31.run_adverse31`(항목 · auto 면 단위 생성) · `decisions.apply_phrase_maps`(①) · `report.phrase_dictionary_json`(out/dictionaries.json) · 게이트 `unlinked_phrases` · adverse_expression·R29 없음 |

- 결정 kind 20 · ① 안 kind 순서 dictionary_add → canonical_rename → dictionary_remove → phrase_map(decided_at 보다 앞선다).
- 옛 결정의 v3.1 변환(거부 아님 · apply_log note): adverse_tuple_assign 옛 네 칸(course_id) → 세 칸 + 그 이름 R15 경과 · 상대 부위 site_id → none · 옛 kind=expression → 그 locator 의 문구 사전 항목 지도(phrase_map 과 같은 효과) · edge_create adverse_tuple 의 옛 course → R15 면 attrs.course(R30 은 자리 없음).
- 엑소좀 EXO-02·05·06 → `decisions/batch3/DEC-2026-11-05-B3-EXO-*`(product_reclassify 2 · R32 edge_create 3 · dictionary_remove 1) · 제안 셋은 `batch3-proposed/` 에서 뺐다.
- `baseline/manifest-5차.json` · `unresolved_references-5차.json` · `report-13-5차.md`(5차 report §13 그대로) → report §14(`lib/report6.py`).
- 결정 묶음 4(동의어 · proposed): `out/gate/batch4.json`·`.md` + `decisions/batch4-proposed/`(`python3 build.py --propose4`) → `python3 apply_gate.py --gate out/gate/batch4.json --out decisions/batch4/ --answers answers.json`.
- 적합성 시험: 2,514 경우 전부(열거기는 v3.1 json 을 읽는다 · tuple_rules.condition 은 열거기 정적 목록 밖이라 경우가 아니다 — 조건 단위는 `test_rules_adverse.Conditions` 가 따로 본다).

## 7차 빌드 · ERD v3.2 + 노드 단위 게이트 5 (2026-11-05 · 발주서 `../silver-build-7-brief.md`)

입력 기본값이 v3.2 로 바뀌었다(`erd-v3.2.json` · `erd-v3.2-dictionaries.json` · `erd-v3.2-column-map.md` · `erd-v3.2-tuples.json` · 이전 판 실측 `erd-v3.1-tuples.json` · 씨앗 `--seeds ../erd-v3.2-seed-candidates.json`).
v3.2 사전 파일의 파생 항목(원장 사건 노드 origin=ledger · 장비 제품 origin=taxonomy)은 빼고(`lib/v32.base_dictionary`) 결정 ① 뒤 분해가 다시 세운다.
결정 적용 전 분해 = `erd-v3.2-tuples.json` 요약 164 키 + 행 대조 19 차이 0 — check ③.

| v3.2 | 어디 |
|---|---|
| 분해(V3.2-0~9) | `lib/v32.py` — 참조 구현 `erd-v3.2-tuples.py` 의 분해·실측 부분(Tokenizer · 병기 · AdverseUnits32 노드 원칙 · V32Resolver/ProcedureTuples32 성분 what · ConditionTuples32 · judge_phrase · ⑦ dup_rules · run_adverse32 · 장비 자동 등록 · R33 행) · `run_v32` · `silver_dictionary` |
| 단위·자기 테이블 | `lib/units32.py`(메모·설명문 · 타임라인 줄 · 응급 징후 · 고지 · 문헌 · 일반값 참조 · 옛 타임라인 지정 → 줄 참조) |
| 개체 | `lib/entities32.py`(장비 제품 · 문헌 adverse_effects · 고지 adverse_ref · post_procedure_timeline · emergency_sign) · `entities.build_adverse`(event_kind dict\|ledger · general_* · side_fragments) · site.parent · procedure grammar_tokens/ingredient_fragments |
| 관계 | `lib/relations32.py`(R15 (출발, 단위) 하나 · inheritance · layer · timeline_refs · emergency_sign_refs · R33 · R34 · R35 · R20 · R4 장비) · R27 은 성분 what 끝 없음 |
| 충돌 | `conflicts.ledger_duplicates`(⑦ 노드 쌍 strong/weak · 안정 키 pair · 장비 ↔ 기존 제품 접두) |
| 결정 | 노드 결정 — `fold_approve` target {dictionary: adverse_event_type, canonical, into} · `exclude` dictionary_value(부작용 아님 → 메모)는 분해 단계에서 · `adverse_tuple_assign` target.kind name\|phrase(옛 raw_name · expression 은 같은 locator 로 · 타임라인 줄은 줄 참조로) · conflict_close 는 노드 쌍 pair 키로도 찾는다 |
| 게이트 5 | `lib/gate5.py` → `out/gate/batch5.json`·`.md` · `batch5-weak.json` — `python3 apply_gate.py --gate out/gate/batch5.json --answers answers.json`(→ decisions/batch5/ · 한 노드에 처분 둘이면 거부) |
| 보고 | `lib/report7.py` → report §15(6차 = `baseline/manifest-6차.json` · §14 는 `baseline/report-14-6차.md` 그대로) |
| 시험 | 열거기 v3.2(3,065 경우 · 토큰화 · 문구 종류 · 장비 규칙 · 새 열거형 · R33~R35) · `tests/test_v32.py` · `test_edge_refs` 는 v3.2 합성 빌드 |

## 8차 빌드 · ERD v3.3 + 원장 3판 + 결정 묶음 6-A + 형태소 분석기 (2026-11-06 · 발주서 `../silver-build-8-brief.md`)

입력 기본값이 v3.3 로 바뀌었다(`erd-v3.3.json` · `erd-v3.3-dictionaries.json` · `erd-v3.3-column-map.md` · `erd-v3.3-tuples.json` · 이전 판 실측 `erd-v3.2-tuples.json` · 원장 `../bronze/phub-ledger/` 3판).
v3.3 은 v3.2 경로(`lib/v32.py`) 위에 분기한다 — `erd_version` 으로 가른다(`pipeline.is33`). v3.2 ERD + 2판으로 돌리면 7차와 바이트가 같다(`baseline/manifest-7차-repro.json` · 아래).

| v3.3 | 어디 |
|---|---|
| V3.3-A 제품 구성품(구조만 · 값 0) | `entities32.products_v33`(product.kind=product · component_of/component_kind null) · `relations.finalize` R27 끝 component → product · `report.relations_of`(R36 파일 · 엣지 0) |
| V3.3-B 토큰화 = 형태소 분석기 | `lib/kiwi_worker.py`(`.venv-kiwi/bin/python` 로만 · kiwipiepy 0.24.1) · `lib/analyzer.py`(서브프로세스 · 캐시 정본 `cache/kiwi-cache.json` · 산출 `out/kiwi-cache.json` · 키 = 판 + 등록 사전 해시 + 문구 NFC) · `lib/adverse33.py`(`AdverseUnits33._apply_cores` — T3·T4·N2·T1·N1·R2·R1 · dryrun3 규칙 · R1/R2 보조 목록 상수) · `v32.run_v32(analyzer=…)`(사전 표면형 전부 사용자 단어 등록 · `_analyzer_prepass` 가 부작용 축 문자열 전부를 미리 캐시) |
| V3.3-C R2 사전 값 · 부위 | 사전 파일(폐색 · decomposed_from · 동맥·정맥·안동맥) 그대로 분해 · `decompose.Ids.event_decomposed` + `units31.labels_to_ids`(옛 값 「혈관 폐색」을 가리킨 결정 → (폐색, 혈관)) · 승인 씨앗 21 = `decisions/batch6a/` |
| V3.3-D 접미사 표기 꼴 | `decisions/batch6a/` fold_approve 19 + canonical_rename 1(자극감 → 자극) |
| V3.3-E category 삭제 | `decompose.Ids.v33`(사전 erd_version) · `adverse31.register_unit/register_raw` · `units31.unit_for` · `entities.ADV_ATTRS_V33` · `v32.silver_dictionary(v33=)`(사건 노드 status·category 없음) · `decisions.apply_dictionary`(new_value category 무시) — v≤3.2 분기는 7차 재현용으로 남아 있다 |
| 게이트 6 | `lib/gate6.py` → `out/gate/batch6.json`·`.md`·`batch6-weak.json`(새 노드 목록만 · ⑦ strong · 문장꼴(b) · 애매 · 폐색/색전 · R30 후보 · 묶음 3 · R1 후보 · Mxx-) → `python3 apply_gate.py --gate out/gate/batch6.json --out decisions/batch6/ --answers …` |
| 보고 | `lib/report8.py` → report §16(7차 = `baseline/manifest-7차.json` · §15 는 `baseline/report-15-7차.md` 그대로) |
| 검산 | `check.py` ③ 은 분석기 없는 목록 규칙 분해로 ERD 실측과 대조(ERD 실측이 분석기 없이 돈다) · ④ 재실행은 venv 경로를 없는 곳으로 주어 캐시만으로 · V3.3-A~E · V3.3-B2 |
| 시험 | 열거기 v3.3(3,243 경우) · `tests/test_v33.py` · `test_edge_refs` 는 v3.3 합성 빌드(R36) · 합성 v3.3 빌드의 분석기 캐시는 워크스페이스 안(`Workspace.args kiwi_cache`) |

```bash
cd silver-v3
python3 build.py && python3 check.py && python3 tests/run_tests.py           # 8차(v3.3 · 3판 · 6-A)
# 7차 재현(8차 lib · v3.2 · 2판 · 6-A 를 뺀 결정 저장소 사본 · 2판 폴더 이름은 phub-ledger 여야 report.md 한 줄(원장 라벨)까지 같다)
python3 build.py --erd ../erd-v3.2.json --dict ../erd-v3.2-dictionaries.json --colmap ../erd-v3.2-column-map.md --tuples ../erd-v3.2-tuples.json \
  --tuples-prev ../erd-v3.1-tuples.json --bronze <2판 사본>/phub-ledger --seeds ../erd-v3.2-seed-candidates.json --decisions <batch6a 뺀 사본> --out <임시>
```

- 결정 묶음 6-A(`decisions/batch6a/` · `_INDEX.md`): site 15 · ingredient_material 6 · 접미사 쌍 20(fold 19 + rename 1) · product_name 동의어 7 = 48 · approved · decided_by 사용자.
- 분석기가 없을 때: `cache/kiwi-cache.json` 에 문구가 전부 있으면 빌드·검산이 venv 없이 돈다. 새 원장·새 사전 값이 생기면 venv 가 한 번 필요하다(`--kiwi-python`).
- `baseline/manifest-8차.json` = 8차 manifest · `baseline/manifest-7차-repro.json` = 8차 lib 로 재현한 7차 manifest(determinism_key 동일).

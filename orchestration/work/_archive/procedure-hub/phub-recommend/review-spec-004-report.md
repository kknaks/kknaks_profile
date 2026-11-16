# 검수 — SPEC-004 · WORK-002 (그래프 v2 구현 전 게이트)

**판정: FAIL** — FAIL 3 · WARN 9

- FAIL 은 모두 **입력 계약**(SPEC-004 §3.1.2 · §3.1.3 · §3.3.4 조인 키) 하나에서 나온다. SPEC 을 쓴 16:55 뒤 `procedure-master-v3.json`(16:57) · `gate-answers/*.json`(16:58)이 실물로 생겼고, 둘 다 계약과 **구조가** 다르다. 키 이름만 다른 정도가 아니라서 WORK-002 Phase 0 의 「어댑터 한 곳에서 맞춘다」로는 흡수되지 않는다. 문서대로 짜면 `curation_shape_error` · `dangling_reference`(error)에 걸려 발행이 막힌다. 그러면 E-5 「error 0」 이 성립하지 않는다
- 규칙 골격(메달리온 4층 · 노드 16 · 엣지 16 · 내림 A~D · v1 교체 · 마이그레이션 0 · LLM 0)은 결정과 맞고, 기존 코드 위에 올릴 수 있다. **§3.1 계약을 실물 모양으로 고치면(코디 30분 안팎) FAIL 은 전부 풀린다**
- 대조 시점: 2026-10-27 17:00. `procedure-master-v3.json` 은 아직 고쳐지는 중이다(17:00 사이에 단위 시술 151 → 236 · UP-M9-038 추가). 아래 수치는 이 시점 값이다

---

## FAIL

### F-1. `curation:procedure-master` 계약(§3.1.2)이 실물 v3 와 구조가 다르다

근거: `procedure-master-v3.json` 최상위 = `version · generated_at · source_snapshot · basis · rules · summary · site_tree · site_special · site_out_of_tree · families · techniques · unit_procedures · ledger_map · provisional · market_rows · market_rows_skipped`

| SPEC §3.1.2 | 실물 v3 | 문서대로 만들면 |
|---|---|---|
| `purposes[]` 배열(필수) | **없음.** 목적은 `unit_procedures[].purposes`(이름 문자열, 예 「주름」 · 「자갈턱」)와 `ledger_map[].destinations[] {type:"purpose", purposes:[이름]}` 에만 있다. 목적 id 가 없다 | 필수 배열 없음 → `curation_shape_error` → 빌드 차단 |
| `packages[]` 배열(필수) | **없음.** 패키지는 `ledger_map` 행선지 `{type:"package", components:[{family, site, unit_procedure_ids}]}` 17건뿐이다 | 같음 |
| `items[]` · `destination` 6종 · `target_ids[]` | `ledger_map[]`(521) · `destinations[]`(행 하나에 1~8개) · **11종**: unit_procedure 403 · product 184 · device 154 · hold 21 · not_procedure 21 · package 17 · purpose 10 · technique 8 · family 6 · material 2 · device_attribute 1. 타입마다 칸이 다르다(`unit_procedure_id` · `product_master_id` · `purposes` · `components` …) | `hold` · `family` · `technique` · `material` · `device_attribute` 를 처리하는 규칙이 없다(§3.3.2-2 도 6종만 다룬다). 제품 행선지에는 `family_id` 가 없고, 같은 행의 `ledger_map[].family` 에 있다 |
| `families[].modality_codes[]`(필수 · 하나 이상) | 없음. `id` 가 곧 M 코드다(M1~M17). **X1~X6**(사용자 답에서 온 계열 6 — 지방분해주사 · 카복시 · 국소 메조 · 성장호르몬 · 태반 · RF 지방감소, 단위 시술 10)에는 M 코드가 없다 | X 계열에서 `curation_shape_error`. 이걸 피해도 F(M) 에 걸리지 않아 X 계열의 금기 · 부작용 · `treats` 가 0 이 된다. 또 M9 → HIFU · RF 는 **계열이 아니라 `sub_family`(속성)** 이다. 그래서 OQ-G04 의 「코드 하나 → 계열 여럿」 가정은 실물에서 일어나지 않는다(F(M) 은 1:1) |
| `sites[]` `id · name · parent_id` · `synonyms[]` | `site_tree[]` = `name · parent`(이름이 곧 열쇠) · 동의어 칸 없음. 묶음은 「턱(묶음)」 처럼 이름에 접미가 붙는다 | 이름 → id 규칙은 어댑터로 맞출 수 있다. 다만 W-3 |
| `unit_procedures[].site_id`(필수 · 무결) | `site` 이름. **트리 밖 값 54**: `"해당 없음"` 27(수액 — `site_special`, DEC-003 OQ-306 처리) · `null` 25(`site_status=missing`) · 「옆구리」 · 「등」(`out_of_tree`) | §3.4 대로면 `dangling_reference`(error) 54 → 발행 차단. 「해당 없음」 부위 노드를 둘지, 부위 없는 단위 시술을 어떻게 다룰지(`unit_without_site` 로 낼지) SPEC 에 규칙이 없다. §3.2.4 · 부위 일치(§3.3.3 B)도 「해당 없음」 을 모른다 |
| `unit_procedures[].gate`(분류표 상태: approved · regate · question · waiting_mfds) | `approval` = **source_only 123** · regate_pending 40 · approved 30 · provisional 27 · waiting_mfds 16 | 가장 많은 `source_only` 가 §3.2.2 표 어디에도 없다. E-2 · E-3 의 단위 시술(UP-M2-* · UP-M9-* · UP-M11-*)이 전부 여기 속한다. `gate_status` 를 정할 수 없다 |
| `product_item_ids[]` | `devices[]`(장비 원장 id만 — 21개 링크, 전부 `kind=device`). 약제 · 필러 제품은 단위 시술에 id 로 이어지지 않고, `synonyms[{text, type:"product"}]` 텍스트로만 있다 | 칸 이름은 어댑터로 맞출 수 있다. 다만 약제 · 필러의 `uses_product` 가 0 이 되는 점을 SPEC 이 알고 있어야 한다(E-4 「보톡스」 경로는 `has_product` 로 가므로 성립한다) |
| `synonyms[]`(문자열) | `[{text, type}]` — type: product 149 · device 127 · ledger_item 125 · problem_tree 61 · market 50 · technique_expression 13 · device_accessory 1 | 어댑터로 맞출 수 있다. 다만 W-2 |

**고칠 것**: §3.1.2 표를 실물 v3 의 칸으로 다시 쓴다. 최소한 정해야 할 것은 다섯이다. ① 목적 = 이름으로 노드 세우기(`purpose:<normalize(name)>`) ② 패키지 = 행선지 `components` 로 노드 세우기 ③ 행선지 11종 각각의 처리(hold · not_procedure · material · device_attribute = 엣지 없음 + 집계 / family · technique = 무엇에 잇는지) ④ X 계열의 `modality_codes=[]` 허용과 그 결과(안전 `gaps`) ⑤ 「해당 없음」 · `null` · 트리 밖 부위의 처리(error 가 아니라 warning)와 `source_only` · `regate_pending` · `market` 의 `gate_status`.

### F-2. `gate:product-match` 계약(§3.1.3)이 실물 파일과 다르다

근거: `gate-answers/product-match.json`(16:58) = `{"items": [ {ledger_id, name, status, license_keys[], source, note} … 340 ], "new_devices": [35]}`

| SPEC | 실물 |
|---|---|
| `items` = 원장 id 를 키로 둔 dict | `items` = **list**(`ledger_id` 칸) |
| `decision` ∈ pick · none · na · unconfirmed | `status` ∈ **auto 127 · unconfirmed 148 · not_applicable 45 · pending 20** |
| `basis` ∈ auto · user · preset | `source` ∈ auto · none. `user` 는 **0건**이다(사용자 답이 아직 하나도 없다) |
| `picks[]` | `license_keys[]` |

- **`pending` 20(「이름 맞고 업체 다름」 — 직접 확인 대상) 이 계약에 없다.** E-3 의 `M11-1-1` 포텐자가 여기 속한다(`status=pending`, `license_keys=[]`). 문서대로면 알 수 없는 값이라 셈에서 빠지거나 shape error 가 난다. 결정 취지(「직접 확인」 = 답 전)로 보면 `unconfirmed` 로 읽는 게 맞다. 다만 SPEC 에 한 줄로 적어야 한다
- 이 결과로 오늘 `approved` 제품은 0 이고, `license_status=unlicensed`(`decision=none`)도 0 이다. §3.2.2 · Phase 2 테스트 「`license_status` 다섯 값」 · fixture 「제품 4(auto · user pick · none · unconfirmed)」 가운데 user pick · none 은 **실물에서 잘라 낼 행이 없다**. WORK-002 Phase 2 는 「손으로 지어내지 말고 실물에서 잘라 내라」 고 하는데, 그 규칙과 부딪친다
- `gate:source-fix` 도 `{"items": …}` 껍데기 없이 최상위가 `{A1-001: {decision, note, proposed, updated_at}}` 이다(이건 이름만 다른 것 — 어댑터로 맞출 수 있다)

**고칠 것**: §3.1.3 을 실물 모양으로 바꾸고 값 대응표를 둔다(auto → pick/auto · not_applicable → na/preset · unconfirmed · **pending → unconfirmed**). Phase 2 의 「다섯 값」 테스트는 실물에 있는 셋(licensed · not_applicable · unconfirmed — cancelled 가 있으면 넷)으로 줄인다.

### F-3. `manufactured_by` · `licensed_to` 의 조인 키(§3.3.4 · §3.2.4 manufacturer)가 입력에 없다

근거: `product-master-draft.json` `manufacturers[]`(219) → `products[]` = 문자열 179 · `{product_id, link}` 258. **`link` 는 허가 key 가 아니라 매칭 상태다**(`candidate` 253 · `auto` 5)

- SPEC 은 「`manufacturers[].products[]` 중 `link` 가 그 허가의 것」 으로 품목 → 제조사를 잇는다. 그런데 `link` 에는 허가 정보가 없고, 원소 절반 가까이가 dict 가 아닌 문자열이다. 문서대로 짜면 엣지가 0 이거나, 제품의 후보 허가 전체에 제조사를 붙이는 틀린 엣지가 나온다
- 게이트가 고른 허가 key 366 가운데 제조사 `sources` 문자열에서 찾아지는 것은 **172**뿐이다. 「보톡스」(`drug:200901660` · 허가 업체 한국애브비)는 **제조사 노드가 아예 없다** — 원장에는 `manufacturer:src:엘러간` · `앨러간애브비`(origin `source_only`, 역할 빈칸)만 있다
- 「만든 `product_item` 에 이어진 제조사만」(§3.2.4) 규칙도 이 조인에 기대므로 같이 무너진다

**고칠 것(둘 중 하나)**: (a) 품목의 `licenses[]`(고른 후보)의 `company` · `manufacturer_original` 을 열쇠로 삼는다. 제조사 노드는 `sources` 에 그 허가 key 가 든 것과 잇고, 없으면 후보 값으로 세운다. 이렇게 할 때는 정규화 규칙을 SPEC 에 적는다. (b) 오늘은 제조사 노드 · 두 엣지를 미루고(OQ 로), 품목 `attributes.licenses[].company` 로만 둔다. 오늘 범위로는 **(b) 를 권한다**(아래 「오늘 범위」).

---

## WARN

### W-1. `unconfirmed` 발행(OQ-G06 임시값)이 결정된 승인 게이트 규칙과 부딪친다

`_RESUME` §2 10-27 「분류표 · 원천 수정 목록은 승인 게이트 … **승인된 것만 다음 단계, 미결은 진행 안 함**」 과 DEC-003 D-03(「승인된 것만 다음 단계로」)은 **정해진 것**이다. 실물 단위 시술 236 가운데 `approved` 는 30 이고, 나머지 206(source_only · regate_pending · provisional · waiting_mfds)이 그래프에 실린다. SPEC 은 이걸 「표시하고 내보낸다」 로 열린 질문(OQ-G06)으로만 두었다. 정해진 규칙을 임시값으로 뒤집은 모양이다. 「오늘 골드까지」 지시가 이 규칙보다 앞서는지를 **발주 전에 사용자에게 한 줄로 확인**해야 한다. 그러지 않으면 「정해진 것을 다시 논의하지 않는다」를 어긴다. (확인되면 그대로 PASS. 이 범위가 E2E 를 성립시키는 전제다 — approved 만 실으면 E-2 · E-3 이 사라진다.)

### W-2. 동의어 해석(§3.3.2)이 공유 동의어 때문에 아무 단위 시술로나 간다

- 단위 시술 동의어 가운데 장비 · 제품 · 고민 트리 텍스트는 80개이고, 그중 **40개가 단위 시술 여럿에 걸린다.** 예: 「팔뚝/복부/허벅지」 10 · 「목주름」 7 · 「슈링크유니버스」 · 「써마지FLX」 6 · 「울쎄라」 5
- §3.3.2 는 사전 순서가 단위 시술 → 계열 → 제품이고, 동점이면 `node_id` 사전순 첫째를 고른다. 그래서 synergy · minimum_intervals · optimization 의 「울쎄라」 끝점이 **UP-M9-002(얼굴 전체 HIFU)로 우연히** 가고, `lowering=direct` · `gate_status=auto` 가 붙는다. 장비 이름이 단위 시술 동의어로 먼저 잡히므로 제품 노드에는 닿지 않는다(「이브아르」 등)
- 고민 트리 동의어(`problem_tree`)에는 **치환 전 표기 「쳐짐」** 이 남아 있다(UP-M7-009 · UP-M9-018 · UP-M9-027 「볼쳐짐/불독살」, UP-M9-038 · UP-M7-014 「눈꺼풀쳐짐」). §3.2.3 치환표는 stg 원천에만 걸린다
- 제안: 해석 사전에는 `ledger_item` · `market` 동의어와 이름만 넣는다. 장비 · 제품 · 고민 트리 동의어는 **검색 전용**으로 둔다. 단위 시술이 여럿 맞으면 「못 풂 → 원천 시술군 코드의 계열(`modality`)」로 보낸다. 오늘 범위에서는 C 의 이름 끝점을 **전부 계열로** 내리면 이 문제를 통째로 피한다(아래)

### W-3. 부위 이름 「(묶음)」 처리가 정해지지 않았다 — E-2 1단계가 깨진다

`site_tree` 이름은 「턱(묶음)」 · 「이마(묶음)」 … 이고, `normalize` 를 거치면 「턱묶음」 이 된다. 그러면 `search?q=턱` 은 묶음 노드를 `exact` 1.0 이 아니라 `prefix` 로 낸다. E-2 1단계 기대(「`site:<턱 묶음>` exact 1.0」)가 성립하지 않는다. 반대로 접미를 떼면 이마 · 눈가 · 코 · 볼 · 목이 묶음과 하위로 같은 이름 둘이 된다(§3.2.5 의 「`parent_id` 로 가른다」 는 이쪽을 가정한다). 둘 중 하나로 정한다. 제안: `name` 은 접미를 뗀 값, `node_id` 는 원문(「(묶음)」 포함), 원문은 동의어에 넣지 않는다. 검색 동점은 타입 순서 다음에 `node_id` 로 가른다.

### W-4. E2E 기대값 가운데 실물과 어긋나는 문장

| 곳 | SPEC 문장 | 실물 |
|---|---|---|
| E-2 2단계 | 「필러」 → 동의어를 가진 M2 계열, HA · 비HA 로 나뉘면 둘 다 0.9 | M2 계열 **이름이 「필러」** 다(`exact` 1.0). HA · 비HA 는 `sub_family` 속성이라 계열은 하나다 |
| E-2 4단계 · OQ-G07 | 턱선 필러는 원천 근거가 없어 나오지 않는 게 맞다 | **UP-M2-011 「턱선 필러」 가 있다**(`source_only` · 동의어 더채움 · 아띠에르 …). 「없어야 함」 으로 쓰면 E2E 가 FAIL 난다. 사각턱 필러는 없다(맞음) |
| R-1 | M2 · M9 · M11 단위 시술 0 | **충족**: UP-M2-004 턱끝 필러 · UP-M11-001 얼굴 전체 니들RF(동의어 포텐자 · `devices` ∋ M11-1-1). Phase 0 escalation 은 필요 없다 |
| E-1 · 규칙 A 「이중턱」 | 턱밑 동의어에 있으면 턱밑 | `site_tree` 에 동의어 칸이 없으므로 **계열로 간다**(`concern_without_site`). 이 갈래로 확정해 적는다 |
| E-3 3단계 | `pick` 이면 / `unconfirmed` 이면 | `M11-1-1` = `pending` → **unconfirmed 갈래로 확정**. licensed 갈래는 오늘 E2E 에서 확인할 수 없다 — 「licensed 확인」 은 `M1-2-1` 보톡스(auto · `drug:200901660` · `drug:200804190`)로 옮긴다 |
| E-1 · E-4 stg 사실 | P3 「쳐짐」 · 하위 3 · 고민 항목 5 · `modality_ref`(M9 · M7 / M7 · M9 / M9 · M14 / M9 · M7 / M9 · M10) | **일치**(`phub-stg-2026-10-26/taxonomy.json`). E-4 3단계 UP-M1-006 「사각턱 보톡스」 approved 있음 |

### W-5. Phase 0 의 독립 기대값 계산(§6.2)은 30분 안에 못 끝낸다

`graph_v2_expected.py` 는 §3.2 · §3.3 규칙(노드 16 · 엣지 16 · 내림 A~D · 검증 코드 20여 개)을 빌드 코드 없이 **한 번 더** 구현하는 일이다. 사실상 두 번째 구현이라 Phase 2~4 와 같은 크기다. 오늘 안에 하려면 범위를 「노드 타입별 수 + E-1~E-4 의 반드시 있음 · 없어야 함 id」로 줄이고, 엣지 · 이슈 수 대조는 뒤로 미룬다.

### W-6. 규격 노드가 두 길에서 겹친다

`specs[]` 40 은 이미 `source=mfds-license` 32(`license_key` · `PACK_UNIT` 파싱 결과 포함)와 `market-pricing` 8 로 되어 있다. §3.2.4 ②(「품목 허가의 `spec.PACK_UNIT`」)를 따로 읽으면 같은 규격이 다른 원문으로 한 번 더 생긴다. ② 를 지우고 `specs[]` 만 쓴다(그중 `license_key` 가 고른 허가에 든 것만).

### W-7. 제품 원장 「4차 판」 은 아직 없다

`product-master-draft.json` 과 `-v3-frozen.json` 은 바이트까지 같다(`cmp` 동일). §3.1.1 의 「4차가 끝나면 그 판」 은 지금은 frozen 과 같은 내용이다. 4차가 오늘 안에 오면 F-3 · F-1 칸이 또 바뀔 수 있다. Phase 0 대조는 **4차 도착 뒤 한 번 더** 돌린다고 WORK 에 적는다.

### W-8. 테스트 범위 — 빠진 파일 하나

WORK-002 는 `test_graph_{ingest,domain,sources,build,api,mcp,boundary}` 일곱을 다룬다(코드 실물과 맞다). 다만 v1 stg fixture 를 만드는 `tests/graph_support.py` 가 Scope 표에 없다. v1 단언(build 59/79/49 · api 59/24/49/15 · `missing_bronze` 10 → 14 · sources `treats` 26)은 전부 이 fixture 에 기대므로 Phase 2~3 에서 같이 고쳐야 한다. `test_graph_sources.py` 는 Phase 3 검증 명령에만 있고, 「v1 단언 → v2」 고칠 목록에는 없다.

### W-9. 「같은 입력」 판정에 `counts.schema` 를 넣는 건 필요 없다

`application.py:204` 는 `set(bronze_hashes) == set(BUILD_ENDPOINTS)` 일 때만 기존 발행본을 찾는다. v2 의 키(14)는 v1 발행본의 키(10)와 겹칠 수 없어서 v1 과 「같은 입력」 이 될 일이 없다. `counts.schema="v2"` 표기 자체는 둬도 좋다. 다만 Phase 4 의 「판정에 schema 포함」 은 할 일에서 빼도 된다.

---

## 볼 것 1~5 요약

| # | 항목 | 결과 |
|---|---|---|
| 1 | DEC 이탈 | LLM 0 ○(어디에도 모델 호출 없음 · D-12) · 레거시 · canonical 미접촉 ○(graph 밖 변경 0 · stg 호출 0 · alembic 0) · D-03 엣지 하나 ○ · D-04 주장 메타 ○ · D-06 safety 동반(family · unit) ○ · 자동 확정 범위: 제품 `auto` → `gate_status=auto`(approved 아님) ○. **승인 게이트 규칙과의 충돌 W-1** |
| 2 | 결정론 계산 가능성 | 규칙 자체는 결정론이다. 다만 입력 모양 가정이 틀렸다 → F-1 · F-2 · F-3. 공유 동의어 동점 W-2 · 묶음 이름 W-3 |
| 3 | v1 교체 · 테스트 | 교체 판단 타당(소비자 없음 · 테이블 일반형 — `graph_node.node_id` 255 · `edge_id` sha256 · `endpoint` 64자, `curation:procedure-master` 25자). 지난 발행본 보존 ○. 테스트 범위 W-8 |
| 4 | E2E 정직성 | 입력 의존을 숨기지 않고(R-1 · OQ-G07 · unconfirmed 갈래) 잘 드러냈다. 실물 기준으로 고칠 문장 W-4. E-5 「error 0」 은 F-1 이 고쳐져야 성립한다 |
| 5 | 오늘 안 | 합계 6시간 45분 + Phase 0 과소평가(W-5) → 지금(17시) 시작이면 자정을 넘긴다. 아래처럼 줄인다 |

## 오늘 범위 제안 — 뒤로 미룰 것

**발주 전(코디, 30분)**: F-1 · F-2 표를 실물 칸으로 고친다. F-3 은 (b). W-1 은 사용자 한 줄 확인. W-3 · W-4 는 문장만 고친다.

| 남길 것(오늘) | 미룰 것(OQ 로) |
|---|---|
| 큐레이션 적재(Phase 1 그대로) | `graph_v2_expected.py` 의 엣지 · 이슈 수 독립 재계산(W-5) — 노드 수 + E2E id 목록만 |
| 노드: 계열 · 단위 시술 · 부위 · 기법 · 목적 · 패키지 · 제품 · 품목 · 고민 트리 · 어휘 · 부작용 | **제조사 노드 · `manufactured_by` · `licensed_to`**(F-3 b) · 규격 ②(W-6) · `danger_level` |
| `treats` ① ② ③ ⑤(규칙 A + 부위 일치) | `treats` ④ optimization 의 「제품 → 단위 시술 하나면 device」 갈래 — 계열로만 내림 |
| `procedure_relation` 은 **계열 단위만**(contraindications · sequence · synergy · intervals 의 이름 끝점도 원천 시술군 코드의 계열로) | 이름 끝점의 단위 시술 해석(C 셋째 줄 · OQ-G05) — W-2 를 고치고 나서 |
| `has_unit` · `at_site` · `uses_technique` · `includes` · `has_child`(부위) · `has_complication` · `site_caution` · `has_product` · `uses_product`(devices) · `has_item` · `has_spec`(① 만) · `synonym` | `coverage_gap` v2 종류 재정의 — v1 종류 이름만 바꿔 그대로 |
| 조회: 허용 타입 · `Edge.gate_status` · Safety v2 · 검색 synonym 열 · tool 설명 문장 | — |
| E-1 · E-2 · E-4 전부 + E-3(unconfirmed 갈래) · E-5 | E-3 licensed 갈래(→ 보톡스로 대신 확인) |

이렇게 줄이면 Phase 3 이 절반 가까이 줄어(1시간 30분 → 약 50분) 전체가 약 5시간 안쪽이 된다.

---
type: review
target:
  - "orchestration/work/phub-recommend/SPEC-002-mfds-mcp.md"
  - "orchestration/work/phub-recommend/SPEC-003-mfds-ingest.md"
basis:
  - "orchestration/work/phub-recommend/DEC-003.md"
  - "orchestration/work/phub-recommend/DEC-001.md (D-12)"
  - "orchestration/work/phub-recommend/_RESUME.md §2 2026-10-27"
reviewer: reviewer_doc (task_ef6dfef05144)
created_at: 2026-10-27
---

# SPEC-002 · SPEC-003 검수 리포트

## 종합: **FAIL** (FAIL 2 · WARN 13)

- SPEC-002(작업용 MCP)만 놓고 보면 **WARN**(FAIL 0)이다. 바로 만들 수 있다. 다만 응답 모양 1건과 S-1 기대값 1건은 고쳐야 한다(W-1 · W-2).
- SPEC-003(Hub 적재 · 매칭)에서 **FAIL 2** 가 나왔다. 둘 다 문서대로 만들면 결과가 틀린다.
  - F-1 · 옛 답 걸러내기가 문서대로는 동작하지 않는다 → 후보가 바뀐 카드의 옛 승인이 원장에 들어간다
  - F-2 · 질의 규칙 Q-M ② 가 코드에 없는 관계를 가리킨다 → 영문명 질의가 모든 항목에서 조용히 빠진다
- DEC 이탈은 없다. 모델 호출 0 · 부분 일치나 편집 거리로 자동 확정하는 곳 0 · 레거시와 canonical 접촉 0. 「정규화 후 완전 일치 = 자동」은 해석이 필요한 자리라 W-3 에서 사용자 확인을 권한다.

### 실물 대조 (2026-10-27, 이 검수에서 부른 횟수 8회 · 키 값은 기록하지 않음)

| # | 호출 | 결과 | SPEC 과 대조 |
|---|---|---|---|
| R1 | 의료기기 상세 `getMdlpPrdlstPrmisnItem05` · `TYPE_NAME=Thermage` · `numOfRows=100` | 200 · total 3 · 그중 2건이 취소(`RTRCN_DSCTN_DIVS_CD` 「2」 · 「5」) | total 3 일치. **유효 허가는 1건**이다 → W-2. `numOfRows=100` 은 받아들인다(SPEC-002 `rows≤100` 일치). `MANUF_NM` 표기가 셋째로 하나 더 나왔다: 「SOLTA Medical, Inc」 — 정규화하면 같다(SPEC-003 §3.3 예 유지) |
| R1' | (같은 응답의 모양) | `body.items` 는 **`[{"item": {...}}]`** 이다. 한 겹 더 싸여 있다 | SPEC-002 · SPEC-003 둘 다 적혀 있지 않다 → W-1 |
| R2 | 상세 · `ENTRPS=솔타` | 200 · total **20** = 솔타메디칼코리아 18 + **한국솔타(주) 2**(관계없는 국내 제조사) | 부분 일치가 관계없는 업체까지 끌어온다 → W-6. `BRNO` 는 행마다 **허가 보유 업체(ENTRPS)의 사업자번호**다(같은 업체 18행이 모두 같은 값이고 `MANUF_NM` 과 관계없다) → W-5 |
| R3 | 업체 `getMdeqMnftPrmsnDtlInq01` · `BSSH_NM=솔타` | 200 · total 2(한국솔타(주) 「제조업」 포함) · `items` 는 **평평한 dict**(싸여 있지 않음) | 필드 목록은 SPEC-002 T-3 과 일치한다(`ENTP_ADDR` · `SRVC_TRGT_ADD_INFO` · `SRVC_TRGT_INFO` 포함). 대표자 이름 같은 사람 실명 필드는 없다. 서비스마다 items 모양이 다르다 → W-1 |
| R4 | 상세 · `PRDUCT_PRMISN_NO=<허가번호>` | 200 · total 1 | **SPEC-002 OQ-M03 은 「받는다」로 답이 난다.** T-2 의 캐시 대체 경로는 필요 없다 → W-8 |
| R5 | 상세 · `PRDUCT=조직수복용생체재료` | 200 · total 606 | **상세 오퍼레이션도 `PRDUCT` 를 받는다.** SPEC-002 T-1 의 「받으면 상세로 옮긴다」 조건이 채워졌다 → W-8 |
| R6 | 목록 `getMdlpPrdlstPrmisnList05` · `entrps=솔타`(소문자) | 200 · total 20 · items 는 `[{"item":…}]` | 소문자 `entrps` 일치(SPEC-002 #2) |
| R7 | 상세 · `TYPE_NAME=써마지FLX` | 200 · total 0 · `items` 키 없음 | 빈 결과 모양 일치(SPEC-002 공통 「빈 결과」). 한글 상담 이름은 모델명에 거의 걸리지 않는다 → F-2 의 영향 |
| R8 | 상세 · `TYPE_NAME=리쥬란` | 200 · total 1 | 한글 모델명으로 등록된 제품도 있다(Q-M ① 이 쓸모없지는 않다) |

- 의약품(`DrugPrdtPrmsnInfoService07`) · DUR 은 부르지 않았다. SPEC 이 이미 403 을 기록해 두었다. 「응답 미확인」 표시는 정직하다. SPEC-002 T-4 표(:169-175)와 SPEC-003 Q-D(:112) · OQ-I03(:400)이 서로 같은 칸을 가리키고, 의약품 필드를 짐작해 적은 곳은 없다.
- 코드 대조(`PROCEDURE-HUB/phub-recommend/backend`, read-only): `mcp>=2.3,<3`(pyproject:12) ○ · `normalize` = `[^0-9A-Za-z가-힣]+` 제거 + casefold(domain.py:49 · 56) ○ · `GraphSettings`(config.py:15) ○ · revision `b202610260001`(alembic/versions/b202610260001_graph_schema.py) ○ · `graph_bronze_snapshot` 유일 키 (endpoint, content_hash)(model/graph.py:38) ○ — SPEC-003 §5.2 에 브론즈를 따로 두는 이유로 적은 것과 같다 · 조회 tool 6종(`graph_search` · `graph_get_node` · `graph_neighbors` · `graph_subgraph` · `graph_list_nodes` · `graph_schema`) ○
- 대상 수 대조(`taxonomy-classify.json`): 제품 183(M1 18 · M2 29 · M3 24 · M4 30 · M7 24 · M15 43 · M16 13 · M17 2) + 장비 157 = **340** ○(SPEC-003 :103). 업체 문자열(`product.maker`)이 있는 것은 168 이고 **172 는 없다** → §5 사용자 표면

---

## FAIL

### F-1 · 옛 답 걸러내기가 문서대로는 동작하지 않는다 — SPEC-003 §3.4 · §3.5 · S-3

- 위치: `SPEC-003-mfds-ingest.md:210`(되들이기 때 카드 해시 대조) · `:214`(「같은 파일을 두 번 넣으면 `unchanged`」) · `:221`(「현재 답이 `approve` 인 것」) · `:364-367`(S-3)
- 근거: 문서는 카드 해시를 **답을 되들일 때(`graph_mfds_answers.py`)만** 대조한다. 순서를 따라가면 이렇다.
  1. 답 파일 A 를 넣는다 → 그때 카드 해시가 같으니 「적용」으로 저장된다
  2. 다시 적재 · 매칭 → 후보가 늘어 카드 해시가 바뀐다
  3. S-3-2 는 「옛 답 파일을 다시 넣음 → `mfds_answer_stale` 1」을 기대한다. 하지만 :214 에 따르면 같은 파일 A 는 **`unchanged`** 로 끝난다. 대조가 다시 일어나지 않는다
  4. 빌드는 :221 「현재 답이 `approve`」를 읽는다. A 는 이미 「적용」 상태로 DB 에 있다 → **바뀐 후보를 사람이 보지 않았는데 옛 승인이 원장에 들어간다**
- 결과: S-3 수용 시나리오는 문서대로 만들면 통과할 수 없다. 통과하도록 고치지 않으면 승인 게이트를 우회하는 길이 생긴다(`_RESUME` 「승인된 것만 다음 단계」 위반).
- 고칠 것(하나만 고르면 된다): **빌드(§3.5)가 원장을 만들 때, 저장된 답마다 그 빌드가 읽은 매칭 런의 `card_hash` 와 다시 대조한다.** 다르면 적용하지 않고 `mfds_answer_stale` 로 센다(§3.6 표의 코드도 이미 빌드 검사다). 되들이기 때의 대조는 즉시 알리는 용도로만 남긴다. S-3-2 를 「옛 답 파일을 다시 넣지 않아도 빌드에서 `stale` 1」로 바꾼다. 「현재 매칭 런」이 무엇인지(최신 `graph_mfds_match_run`인가, 빌드가 고른 런인가)도 :210 · :218 에 한 줄로 못박는다.

### F-2 · Q-M ② 가 코드에 없는 관계를 가리킨다 — SPEC-003 §3.1

- 위치: `SPEC-003-mfds-ingest.md:109`(「그 항목과 SPEC-001 `synonym` 으로 이어진 products.json 제품의 `name_en`」) · 같은 가정 `:189` · `:228`(synonyms · country 원천) · `:258`
- 근거: SPEC-001 의 `synonym` 엣지는 `opt_concern` · `synergy_target` · `product` ↔ `concern` 계열 · `product` 사이에만 있다(`backend/app/modules/graph/domain.py:230-236`). 「products 사전 제품 ↔ taxonomy 제품」이 그 예다. 그런데 매칭 대상의 키는 분류표 `items[].id` 이고, 이것은 SPEC-001 에서 **`procedure:<id>`(시술 항목) 노드**다(domain.py:106 · SPEC-001 :563 `procedure:M1-2-1`「보톡스(엘러간)」). `procedure` 와 products.json `product` 를 잇는 `synonym` 은 없다.
- 결과: 문서대로 만들면 **340 항목 모두 Q-M ② 질의가 0개**가 된다. 에러도 나지 않는다. 그런데 taxonomy `name` 은 대부분 한글이다. 그래서 라틴 모델명(`TYPE_NAME`)에 걸 수 있는 질의는 ② 뿐이다(R7: 「써마지FLX」 0건). ② 가 빠지면 자동 확정이 사실상 0 이 되고, 업체 문자열이 없는 172 항목은 질의 자체가 한글 이름 하나뿐이다. `country`(:227)와 제조사 국문명의 products.json 원천(:227 · OQ-I07)도 같은 이유로 비게 된다.
- 고칠 것: 대상 항목 ↔ products.json 제품을 잇는 **결정론 키를 하나 정한다.** 예를 들면 분류표 `items[].product.name` 의 `normalize` 가 products.json `name` 의 `normalize` 와 같은 것이다. 분류표에는 이미 `product.maker_products_json` 이 있어서 연결을 한 번 거쳤다는 흔적이 있다. 이 키를 대상 항목 파일(§3.1 :97-100)의 필드로 넣는 것이 가장 단순하다. 예: `"products_json_name": "…"` · `"name_en": "…"`(코디가 만들 때 채움). 이 키는 정규화 후 완전 일치여야 한다(DEC-001 D-12).

---

## WARN

### W-1 · 응답 items 모양이 서비스마다 다른데 SPEC 에 없다 — SPEC-002 §4 공통 · SPEC-003 §3.3

- 위치: `SPEC-002-mfds-mcp.md:63`(「`body{…, items[]}`」) · `:125`(「원본 항목의 필드 이름 · 값 그대로」) · `SPEC-003-mfds-ingest.md:141`
- 근거: R1' · R6 — 의료기기 품목허가(목록 · 상세)는 `items: [{"item": {…}}]`, R3 — 업체 상세는 `items: [{…}]`(싸여 있지 않음). 0건이면 `items` 키 자체가 없다(R7 · SPEC 에 있음).
- 영향: `is_cancelled` 판정 · 허가 키 `MDEQ_PRDLST_SN` 추출 · 카드 후보 필드가 모두 이 한 겹을 거친다. 워커가 실호출로 금방 알아채겠지만, `--from-dir` 테스트 픽스처를 손으로 만들면 모양이 틀린 채로 통과할 수 있다.
- 고칠 것: SPEC-002 「응답에서 본 것」에 서비스별 items 모양 한 줄. MCP 출력 `items[]` 은 **한 겹 벗긴 항목**으로 낸다고 적는다(캐시는 원본 그대로). SPEC-003 테스트 픽스처는 실호출 저장본(`--save-dir`)에서 만든다고 적는다.

### W-2 · S-1 의 「3건(유효만, 기본값)」이 실제와 다르다 — SPEC-002 §3

- 위치: `SPEC-002-mfds-mcp.md:97` · AC `:300`
- 근거: R1 — `TYPE_NAME=Thermage` 3건 가운데 2건이 취소다(코드 「2」 · 「5」). 기본값(`include_cancelled=false`)이면 `returned=1` · `filtered_out_cancelled=2` 이고 `total_count=3` 이다.
- 영향: AC(:300)는 total 만 봐서 맞는다. 그런데 S-1-2 문장대로 「유효만 3건」을 기대하면 걸러내기를 잘못 만든 쪽이 통과한다.
- 고칠 것: S-1-2 를 「`total_count` 3 · `returned` 1 · `filtered_out_cancelled` 2」로 고친다. AC 에 `returned` · `filtered_out_cancelled` 를 더한다.

### W-3 · 「정규화 후 완전 일치 = 자동(게이트 밖)」이 사용자 결정의 해석이다 — SPEC-003 §3.3

- 위치: `SPEC-003-mfds-ingest.md:143-147` · `:155` · AC `:388`(「대소문자만 다른 모델명은 정규화 뒤 같아 자동」) · OQ-I08 `:405`
- 근거: `_RESUME` §2 10-27 「외국어 이름(원어명 · 모델명)은 오타가 섞일 수 있다 → 식약처 매칭이 **정확히 일치하지 않는 것은** 승인 게이트로」. DEC-003 D-03 은 「매칭 결과는 … 승인 게이트에 올린다」. SPEC 은 casefold + 기호·공백 제거 뒤 같은 것을 「정확히 일치」로 읽었다. SPEC-001 synonym 규칙과 같은 선이라 DEC-001 D-12 와는 어긋나지 않는다. 하지만 「Thermage FLX」 = 「thermageflx」 = 「THERMAGE-FLX」 를 사람이 보지 않고 확정한다.
- 판단: 모델명 + 업체 두 조건 + 유일성이 함께 걸려 있어 위험은 낮다. 그래도 이것은 사용자 결정의 범위를 정하는 문제다. OQ-I08 이 「자동도 확인 카드로?」만 묻고 있는데, 「정규화한 일치를 정확한 일치로 보는가」까지 OQ 에 명시해 사용자 확인을 받는다. 기본값은 지금 SPEC 그대로 두면 된다.

### W-4 · 넓은 질의로 `query_failed` 가 된 항목은 빠져나갈 길이 없다 — SPEC-003 §3.1 · §3.3

- 위치: `SPEC-003-mfds-ingest.md:115` · `:158`(「다시 적재한 뒤 다시 매칭」) · Case Matrix `:313`
- 근거: 넓은 질의 판정은 결정론이다(같은 토막 → 같은 totalCount). 그래서 다시 적재해도 다시 `too_broad` 이고, 그 항목은 영영 카드로 나오지 않는다. 그 항목의 다른 질의(Q-M)가 정상이어도 마찬가지다.
- 고칠 것: 넓은 질의 하나 때문에 항목 전체를 막지 말고, **그 질의만 빼고 나머지 질의로 매칭해 카드로 내보낸다.** `query_notes` 에 「제외됨(too_broad)」을 보이면 된다. 아니면 `query_failed` 의 「다음」 칸을 「OQ-I06 값을 바꾸거나 대상 항목의 업체 문자열을 고친 뒤」로 정직하게 고친다.

### W-5 · `brno` 가 어느 쪽 업체 값인지 정해져 있지 않다 → `manufacturer_brno_split` 오탐 — SPEC-003 §3.5 · §3.6

- 위치: `SPEC-003-mfds-ingest.md:227`(`brno` — 같은 업체 판별용) · `:275`
- 근거: R2 — 품목허가의 `BRNO` 는 **허가 보유 업체(`ENTRPS`)의 사업자번호**다. 솔타메디칼코리아의 18행이 모두 같은 값인데, 그 행들의 `MANUF_NM` 은 Solta Medical · Parker Laboratories · Sanmina · Pharmaceutical Innovations 로 갈린다. 이 값을 `MANUF_NM` 쪽 제조사 노드에도 붙이면, 수입 제품 하나마다 「같은 brno · 다른 이름」이 생긴다. 그러면 `manufacturer_brno_split` 이 수입품 전부에서 울린다.
- 고칠 것: `brno` 는 **`licensed_to` 쪽(ENTRPS) 노드에만** 붙인다고 적는다. 해외 제조원 노드는 `brno` 가 비어 있다.

### W-6 · 역할(제조업 / 수입업)을 잇는 키가 없다 · 부분 일치가 관계없는 업체를 끌어온다 — SPEC-003 §3.1 Q-C · §3.4

- 위치: `SPEC-003-mfds-ingest.md:111` · `:191`(「역할(Q-C 결과의 제조업 / 수입업)」) · `:227` `roles`
- 근거: R2 · R3 — `ENTRPS=솔타` · `BSSH_NM=솔타` 둘 다 관계없는 국내 제조사 「한국솔타(주)」를 함께 낸다. Q-C 결과를 허가 행에 이름으로 붙이면 잘못 붙을 수 있다. 업체 응답과 품목 응답이 함께 가진 것은 **`BRNO`** 다(R3 필드 목록 · SPEC-002 :159).
- 고칠 것: 「역할은 허가 행 `BRNO` = 업체 행 `BRNO` 로 잇는다. 없으면 빈칸」을 한 줄로 적는다. 카드에는 부분 일치로 잡힌 업체가 섞인다는 점을 S-1-2 에 적는다(실제 20건).

### W-7 · 취소 · 미허가가 조회 표면에서 안 보인다 — SPEC-003 §3.5 · §4

- 위치: `SPEC-003-mfds-ingest.md:231-239`(「추천에서 빼는 일 자체는 조회 · 추천 쪽이 한다. 이 SPEC 은 값을 보장할 뿐」) · `:304`
- 근거:
  - ① `graph_search` 의 결과 항목은 `node_id · name · names · synonyms` 뿐이다(`application.py:911` `ListItemView`). `attributes.status` 가 없다. 외부 에이전트가 「써마지」로 검색하면 `cancelled` 인 `product_entry` 도 같은 모양으로 나온다. 상태는 `graph_get_node` 까지 가야 보인다.
  - ② SPEC-001 의 기존 `product` 노드(products.json `mfds` False 6 포함)는 이 SPEC 이 손대지 않는다(:258). 「쓰는 제품」 쪽 길은 지금도 허가 상태 없이 열려 있다.
- DEC 이탈은 아니다. Hub 는 추천하지 않는다(DEC-001 경계). 그래도 `_RESUME` 「미허가 · 취소는 상태로 남기고 추천 제외」를 받는 쪽이 지킬 수 있으려면 표면 계약이 있어야 한다.
- 고칠 것: tool description(`graph_search` · `graph_get_node`)에 「`product_entry.attributes.status` 가 `licensed` 가 아니면 추천하지 않는다」를 넣는다. 그리고 검색 결과 항목에 `status` 를 실을지를 OQ 로 남긴다. 기존 `product` 노드의 허가 상태는 SPEC-001 개정(DEC-002 D-08) 쪽 OQ 로 넘긴다고 한 줄 적는다.

### W-8 · OQ-M03 은 실호출로 답이 났다 — SPEC-002 T-1 · T-2

- 위치: `SPEC-002-mfds-mcp.md:142`(「상세가 `PRDUCT` 를 받는지 미확인」) · `:151`(T-2 캐시 대체) · `:316` OQ-M03
- 근거: R4(`PRDUCT_PRMISN_NO` → total 1) · R5(상세 `PRDUCT` → total 606)
- 고칠 것: T-2 는 상세 오퍼레이션에 `PRDUCT_PRMISN_NO` 를 직접 보낸다. `not_in_cache` 경로는 없앤다. `MDEQ_PRDLST_SN` 필터는 여전히 미확인이다. T-1 의 `prduct` 도 상세로 보낸다. 그러면 목록 오퍼레이션과 소문자 `entrps` 를 쓰는 곳은 **없어진다.** :143 · AC :303 의 회귀 방지 항목도 함께 정리한다(목록 오퍼레이션을 남길 이유가 없으면 남기지 않는다).

### W-9 · T-1 입력 조합 하나가 정의되지 않았다 — SPEC-002 T-1

- 위치: `SPEC-002-mfds-mcp.md:139-143`
- 근거: `type_name` + `prduct`(또는 셋 다)일 때 표의 첫 행(상세 · `TYPE_NAME` · `ENTRPS`)이 걸리고 `prduct` 는 조용히 버려진다. W-8 대로 상세 하나로 합치면 세 파라미터를 함께 보내면 된다. 다만 AND 로 걸리는지는 1회 확인이 필요하다.

### W-10 · 대상 항목의 `service` 배정 규칙에 빈칸 — SPEC-003 §3.1

- 위치: `SPEC-003-mfds-ingest.md:102`
- 근거: 실제 분포(위 「대상 수 대조」)에 대 보았다.
  - 「M15 필링 제품 → `undecided`」라고 적었는데, M15 제품 43 가운데 「물톡스」 · 「라라닥터」는 필링이 아니다 → 규칙 밖
  - 「약」이 무엇인지(kind · 시술군) 정의가 없다
  - kind `device` 인 M16 1건은 「kind device 전부 → device」와 「M16 → drug」 두 규칙에 동시에 걸린다
- 고칠 것: 시술군 × kind 표로 바꾸고 어긋나는 항목은 대상 항목 파일에서 명시적으로 지정한다(이미 `service` 필드가 있다).

### W-11 · 의약품 대상에도 의료기기 질의가 「항상」 나간다 — SPEC-003 §3.1 · §3.3

- 위치: `SPEC-003-mfds-ingest.md:109`(Q-M 「항상」) · `:110-111` · `:141`(후보 = 가리킨 질의 전부)
- 근거: `service=drug` 항목(M1 18 · M16 13)도 의료기기 상세 · 업체 질의를 받는다. 의약품 키가 반영된 뒤에는 의약품 후보와 의료기기 후보가 한 카드에 섞인다. 자동 확정 조건에 `license_kind` 일치가 없어서, 드물게는 의약품 항목이 의료기기 허가로 자동 확정될 수도 있다.
- 고칠 것: Q-M · Q-E · Q-C 는 `service=device` 일 때만 보낸다. Q-D 는 `drug` 일 때만 보낸다.

### W-12 · `card_hash` 의 「각 후보의 내용 해시」가 정의되지 않았다 — SPEC-003 §3.4

- 위치: `SPEC-003-mfds-ingest.md:188`
- 근거: 브론즈 내용 해시는 **페이지 단위**다(:126). 허가 한 건의 내용 해시를 무엇으로 구하는지가 없다. 같은 허가가 두 질의(Q-M · Q-E)의 다른 페이지에 함께 들어 있으면, 페이지 해시를 쓸 때 어느 것을 쓰느냐에 따라 카드 해시가 달라진다. 이것은 결정론 위반이다.
- 고칠 것: 「후보 내용 해시 = 한 겹 벗긴 허가 항목(W-1)의 정규화 JSON SHA-256」으로 적는다.

### W-13 · `httpx` 기본 로그가 키를 남긴다 — SPEC-002 §5.4 · SPEC-003 §3.2

- 위치: `SPEC-002-mfds-mcp.md:219` · `:290-293` · `SPEC-003-mfds-ingest.md:128` · AC `:387`
- 근거: 공공데이터포털 키는 질의 문자열(`serviceKey=`)로만 보낸다. 그런데 `httpx` 는 로거 `httpx` 에 INFO 로 요청 URL 전체를 남긴다. 예외 문자열(`HTTPStatusError` · `ConnectError` 등)에도 URL 이 들어간다. SPEC 은 「URL 을 싣지 않는다」는 원칙만 적었다. 이 두 길은 구현에서 쉽게 놓친다.
- 고칠 것: Implementation Rules 에 두 줄을 넣는다. 「`httpx` · `httpcore` 로거를 WARNING 이상으로 둔다」, 「에러 사유에는 예외 클래스 이름과 상태 코드만 싣는다(`str(exc)` 금지)」. AC 에는 「`MFDS_API_KEY` 를 가짜 값으로 두고 401/연결 실패를 일으켜 stderr · 로그 · 브론즈에서 그 값을 grep → 0」을 넣는다.

---

## 볼 것 1~5 정리

1. **DEC 이탈**: Hub 모델 호출 0(SPEC-003 :345 · SPEC-002 :263). 부분 일치 · 편집 거리 · 모델로 자동 확정하는 곳 0(:89 · :345). 레거시 · canonical 접촉 0(:328). 미허가 · 취소는 상태로 남기고 노드를 지우지 않는다(:231-239, `_RESUME` OQ 처리와 일치). 남은 것: 자동 확정 범위 해석(W-3), 옛 승인이 새는 길(F-1), 조회 표면에서 상태가 안 보이는 것(W-7).
2. **실물 대조**: 오퍼레이션 이름 · 대문자/소문자 파라미터 · 부분 일치 · 대소문자 구분 · 빈 결과 모양 · 취소 필드 · 업체 필드 목록은 모두 맞다. 틀린 곳은 items 감싸기(W-1)와 S-1 유효 건수(W-2)다. 미확인으로 남겨 둔 OQ-M03 은 답이 났다(W-8). 의약품의 「응답 미확인」 표시는 정직하다.
3. **구현 가능성**: SPEC-002 는 문서만 보고 만들 수 있다. SPEC-003 은 매칭 → 카드 → 답 → 빌드 흐름이 그려져 있다. 다만 고리 둘이 열려 있어 F-1 · F-2 를 닫아야 한다. 정의가 빈 곳은 W-5 · W-6 · W-10 · W-12 다.
4. **보안**: `.env` · `cache/` 가 gitignore 에 걸리는 것을 `git check-ignore` 로 확인했다(`reference/2026-10-27-mfds-mcp/.gitignore:1-2`). `.env` 의 키는 `MFDS_API_KEY` 하나뿐이다. `claude mcp add` 에 키를 넣지 않는다(:287). SPEC 두 개 · NOTES 에 키 값과 사람 실명은 없다. 실호출표의 업체는 `<업체 일부>` 로 가렸다. 응답에 대표자 같은 실명 필드는 없다(R3). 업체 주소(`ENTP_ADDR`)는 출력에서 빼고 캐시에만 남는다(gitignore). 남은 구멍은 `httpx` 로그와 예외 문자열(W-13)이다. 카드 파일은 레포 밖에 두고 private 아티팩트로 간다. 업체 이름뿐이라 문제없다.
5. **사용자가 실물에서 만날 자리**: 아래.

## 사용자가 실물에서 만날 자리

- **게이트 카드가 대상 수만큼 나온다.** 자동 확정은 드물 것이다. taxonomy 이름이 대부분 한글이고(R7), F-2 를 고쳐도 영문명은 products.json 에 이어진 59 제품 쪽에만 있다. 업체 조건(OQ-I02 · 법인 표기)도 거의 안 맞는다. 340 가운데 `undecided`(M15 필링 · M17 — 약 45)를 빼면 **약 290 장**이 카드나 의약품 대기로 나온다고 보면 된다.
- **업체 문자열이 없는 172 항목**은 한글 이름 모델명 질의 하나만 받는다. 대부분 `no_candidate` 카드로 나오고, 사용자는 「허가 없음」과 「질의 다시 짜기(반려)」 둘 가운데 하나를 골라야 한다. 반려 뒤 「대상 항목 고치기」가 누구 몫인지(코디가 업체 문자열을 채우는가)를 미리 정해 두면 왕복이 준다.
- **업체로 잡힌 카드는 그 업체의 제품 전부가 후보로 나온다.** 「써마지FLX」 카드에 솔타메디칼코리아의 Fraxel · Liposonix · Clear+Brilliant · 젤(Parker) 등 18건과 관계없는 한국솔타(주) 2건이 함께 나온다(R2). 써마지 FLX 는 모델 코드(「TG-3A」 추정)로만 등록돼 있어, 사용자가 코드를 알아야 고를 수 있다. 카드에 사용목적(`USE_PURPS`)이 보이는 것이 유일한 단서다. 정렬이 「유효 먼저 → 허가일 최신」인 것은 맞다.
- **「Thermage」 로 찾으면 유효한 허가는 국내 제조 1건(「Thermage Deep Skin외 4건」, 제허)뿐이다.** 정품 수입 허가 두 건은 취소다(R1). 「써마지가 취소됐다」로 잘못 읽힐 수 있다. 카드의 `is_cancelled` 와 취소일 표시가 눈에 띄어야 한다.
- 의약품(톡신 M1 18 · 수액 M16 13)은 키가 반영되기 전까지 전부 `query_failed` 로 카드가 나오지 않는다. 사용자는 이 31건을 게이트에서 보지 못하고, 검증 리포트 숫자로만 본다.

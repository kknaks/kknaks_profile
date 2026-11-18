# 허브 gold 호출 안내 — REST · MCP

> Procedure Hub stg 에 올라간 **데이터 메달리온 gold** 를 다른 서비스(앱 · 에이전트)가 REST 나 MCP 로 불러 쓰는 법.
> 예시 응답은 전부 2026-11-18 stg 실물 호출에서 뽑아 줄인 것이다(`gold_hash` `8accbb21…`).

## 1. 무엇인가

**한 줄** — 시술 · 제품 · 고민 · 부작용 · 금기 · 상품 · 패키지를 코드로 엮은 표 15 개를 **읽기 전용 결정론 도구 9 개**로 조회한다. 같은 입력 · 같은 데이터 판이면 같은 응답이다.

| 성질 | 뜻 |
|---|---|
| 읽기 전용 | 전부 `GET`(REST) · `readOnlyHint`(MCP). 쓰기 · 갱신 요청 없음 |
| LLM 없음 | 허브는 고르지 않고 · 점수를 매기지 않고 · 문장을 해석하지 않는다. 판단은 부르는 쪽 몫 |
| 폭을 자르지 않음 | `limit` 은 쪽 크기일 뿐이다. `next_cursor` 를 `null` 까지 따라가면 `total` 전부가 나온다 |
| 공개 정보 | 원천이 공개 자료(시술 원장)라 응답에 비밀값은 없다 |
| 데이터 판 | 응답 머리 `build.gold_hash` 하나가 판을 가리킨다. 데이터를 다시 적재하면 바뀐다 |
| 근거 추적 | 모든 행이 `gold_table` · `gid` · `evidence_kind` 를 갖고, `evidence` 로 원장 위치(`source_ref.ref`)까지 되짚는다 |

**gold 15 표**(행 수 = stg `health` 실측)

| 표 | 행 | 무엇 |
|---|---:|---|
| `g_entry` | 2,642 | 입구 — 이름 · 별칭 → 코드(`resolve` 가 읽는다) |
| `g_node` | 1,545 | 관계의 끝이 된 노드(`표:코드`) |
| `g_edge` | 10,389 | 노드 사이 관계(`neighbors`) |
| `g_scope` | 4,202 | 대상의 층 — 자기 · 물려받음(계열·시술에서) · 하위 시술 · 하위 케이스 · 하위 제품 |
| `g_profile` | 739 | 개요 · 원리 · 재료 · 방법 · 부위 |
| `g_indication` | 4,866 | 어디에 쓰나(고민 → 대상) |
| `g_outcome` | 1,604 | 효과 |
| `g_adverse` | 2,923 | 부작용 |
| `g_adverse_detail` | 3,828 | 부작용 위험 요인 · 대응 |
| `g_recovery` | 37 | 회복 |
| `g_contraindication` | 350 | 금기(사람 조건) |
| `g_offer` | 163 | 상품 |
| `g_package` | 312 | 패키지 · 같은 날 조합 |
| `g_pair` | 904 | 시술 간 관계 — 회피 · 보완 · 순서 · 간격 · 재시술 간격 · 같은 날 |
| `g_evidence` | 27,740 | gold 행 → silver 행 근거 |

- silver(정규화 중간층)와 그림 데이터는 허브 **DB 에만** 있다. 도구는 gold 와 `source_ref`(원장 포인터)만 낸다.
- 입구 개념 수(`g_entry` 의 서로 다른 코드): product 315 · concern 260 · adverse 188 · condition 151 · material 143 · procedure 138 · offer 122 · package 119 · anatomy 105 · site 89 · effect 70 · method 49 · procedure_case 44 · modality 18.

## 2. 주소 · 인증 · 상태

| 무엇 | stg |
|---|---|
| REST 기본 | `https://api-stg-csp.medisolveai.com/procedure-hub/gold` |
| REST 문서 | `…/procedure-hub/gold/api-docs` · `…/redoc` · `…/openapi.json` |
| MCP 끝점 | `https://api-stg-csp.medisolveai.com/procedure-hub/gold-mcp/mcp`(streamable HTTP · 서버 이름 `procedure-hub-gold`) |
| 인증 | **지금은 없다** |
| 상태 확인 | `GET …/gold/health` — `200` 이면 켜짐 · `503` + `{"detail": "unavailable: gold 꺼짐 — <이유>"}` 이면 꺼짐 |

- gold 가 꺼져 있으면 REST 전 경로(`health` 포함)와 MCP 가 모두 `503` `unavailable` 이다. 허브의 나머지 API 는 그대로 돈다.
- 켜짐 · 꺼짐은 허브 시작 때 한 번 정해진다. 다시 켜는 길은 재시작뿐이다.

```bash
curl -s https://api-stg-csp.medisolveai.com/procedure-hub/gold/health
```

```json
{
  "build": {"gold_hash": "8accbb213ac5327d8675f8156bc57d87c12a3245c383c8239074444da7f6228c",
            "aux_hash": "93ec89fdd7d66781cdf18025c4698cc31a543fe252ebb1f16948fc0876ae0eeb",
            "loaded_at": "2026-11-18T09:33:29+00:00"},
  "request": {},
  "files": [{"name": "g_adverse.csv", "sha256": "5a8bab5b…", "rows": 2923, "kind": "gold"}, "… 22 줄"],
  "expected_hash_checked": false,
  "load_ms": 1465.7,
  "integrity": {"gold_rows_without_evidence": 0, "evidence_without_source_ref": 0,
                "hierarchy_orphan_parents": 0, "scope_duplicate_subject_holder_rows": 0},
  "aux": {"hierarchy": {"concern": 260, "adverse": 188, "condition": 151},
          "concern_site": {"rows": 103, "concerns": 92, "sites": 52},
          "ledger_check": {"rows": 325, "rows_with_code": 251, "codes": 218}}
}
```

## 3. 시작하는 길

모든 도구는 대상을 **`표:코드`**(예: `product:PRD-400` · `concern:CON-001` · `procedure:PRC-001`)로 받는다. 그래서 첫걸음은 늘 **이름 → 코드**다.

```text
이름 ──resolve──▶ 코드 ──┬─ 고민이면 ─▶ concern_candidates ─▶ 후보 시술 코드들
                        │
                        └─ 대상이면 ─▶ coverage(무슨 정보가 몇 행 있나)
                                      ─▶ facets · pair · scope · neighbors(행 읽기)
                                      ─▶ evidence(행의 원장 근거)
```

**이름 → 코드는 두 꼴이다**

| 꼴 | 부르는 법 | 언제 |
|---|---|---|
| 맞춤 꼴 | `resolve?text=울쎄라` | 이름(또는 별칭) 하나를 정확히 알 때. 공백 제거 + 소문자로 맞춘 글자가 **완전히 같아야** 후보다 |
| 목록 꼴 | `resolve?tables=concern,procedure` 또는 `resolve?range=시술` | 사용자 문장에서 대상을 골라야 할 때. 입구 목록을 끝까지 받아 **부르는 쪽(LLM 등)이 고른다** |

**흔한 질문 꼴 넷**

| 질문 | 호출 순서 |
|---|---|
| 「울쎄라 부작용은?」 | `resolve?text=울쎄라` → `product:PRD-400` → `facets?node=product:PRD-400&facet=adverse` → (근거가 필요하면) `evidence?gold_table=g_adverse&gold_id=<gid>` |
| 「주름엔 뭐가 좋아?」 | `resolve?text=주름` → `CON-001` → `concern-candidates?concern_code=CON-001`(부위가 있으면 `&site=이마`) → 후보마다 `facets … facet=profile` |
| 「울쎄라랑 같이 하면 안 되는 거?」 | `resolve` → `pair?a=product:PRD-400&classes=회피`(같은 날은 `same_day_only=true`) |
| 「이 시술 정보가 뭐가 있지?」 | `coverage?nodes=product:PRD-400` 로 종류별 행 수 → 0 이 아닌 종류만 `facets` · `pair` 로 읽기 |

- 하위 층(하위 시술 · 하위 케이스 · 하위 제품)의 자기 행은 `roles` 에 그 이름을 **명시해야** 나온다. 기본값은 `자기,물려받음` 이다.
- 재료 · 방법 · 해부 · 부위 코드로 시작하면 `facets` 의 `node` 에 그 코드를 준다 — 그 값을 칸에 가진 행(= 대상)이 전부 나온다.

**범위 8**(`resolve` 의 `range` 값 · 범위마다 시작 표)

| `range` | 시작 표 |
|---|---|
| `시술` | procedure · procedure_case · product · modality |
| `부위·고민` | concern |
| `부작용` | 대상 4 표 · adverse |
| `시술 조합` | 대상 4 표 · concern |
| `동시 가능` | 대상 4 표 |
| `순서·간격` | 대상 4 표 |
| `회피` | 대상 4 표 · condition |
| `상품` | product · procedure · procedure_case · offer |

대상 4 표 = modality · procedure · procedure_case · product. 속성 4 표(material · method · anatomy · site)는 어느 범위에서나 시작 표로 함께 나온다.

## 4. 도구 9

REST 는 전부 `GET <REST 기본><경로>` · MCP 는 같은 이름 · 같은 입력 · 같은 JSON 이다. 목록 입력은 REST 에선 **콤마 목록**(`roles=자기,물려받음`) · MCP 에선 문자열 배열.

| MCP 이름 | REST 경로 | 필수 입력 | 선택 입력(기본) | 출력 핵심 | 쪽 넘김 · `total` |
|---|---|---|---|---|---|
| `resolve` | `/resolve` | 맞춤 꼴 `text` / 목록 꼴 `range` 또는 `tables` | `range`(맞춤 꼴에선 정렬 · `in_range` 에만) | `candidates[]`(`entity_table` · `entity_code` · `entity_name` · `name_kind` · `matched.span`) · `ambiguous` · 목록 꼴 `counts{by_table, entities}` | 맞춤 꼴 없음(후보 0 ~ 3) · 목록 꼴 있음 · 단위 = 후보 |
| `scope` | `/scope` | `node` | `roles`(전부) · `descend`(`all` · `one`) | `holders[]`(`holder_*` · `role` · `path` · `depth` · `via[]`) · `counts_by_role` | 있음 · 단위 = 층 행 |
| `neighbors` | `/neighbors` | `node_id` · `edge_types`(1 개 이상) | `direction`(`out` · `in`) | `items[]`(엣지 + 반대쪽 `node{node_id, node_table, node_code, label}`) · `counts_by_type` · `distinct_nodes` | 있음 · 단위 = 엣지 |
| `facets` | `/facets` | `facet` · `node`(`offer_name_contains` 를 줄 때만 생략) | `roles`(`자기,물려받음` · 제품의 offer 는 `자기,하위 제품`) · `filters` · `hier`(`expand`) · `offer_name_contains` · `descend`(`all`) | `rows[]`(그 표 행 그대로 + `layer` · `hier` · `attr`) · `counts{by_role, distinct_rows, …}` · `ledger_check[]` | 있음 · 단위 = 행 |
| `concern_candidates` | `/concern-candidates` | `concern_code` | `site` · `site_mode`(`auto`) · `upper`(`auto`) · `to_procedure`(`auto`) | `groups[]`(후보 시술 · 케이스 · 제품 묶음 + `rows[]`) · `counts` · 첫 쪽 `sites[]` · `descended[]` · `modality_only[]` · `unreached[]` · `ledger_check[]` | 있음 · 단위 = **묶음**(행 수는 `counts.rows`) |
| `pair` | `/pair` | `a` | `b` · `classes` · `self_pair`(`any`) · `same_day_only`(`false`) · `package_kinds` · `descend`(`all`) | `rows[]`(`g_pair` 행 + `a_side` · `a_layer` · `b_layer`) · `counts{by_class, same_day, conflict}` · 첫 쪽 `same_day_packages[]` · `ledger_check[]` | 있음 · 단위 = 행 |
| `evidence` | `/evidence` | `gold_table`(`g_edge` 제외) · `gold_id` | — | `refs[]`(`silver_table` · `silver_id` · `source_refs[]{ref}` · `n_source_refs`) | 있음 · 단위 = 원장 포인터 줄 |
| `coverage` | `/coverage` | `nodes`(1 ~ 64) | `kinds`(전부) | `items[]{node, name, kinds[]{kind, self, lower, lower_holders, inherited}}` — 셈뿐 | 없음 · 단위 = 노드 |
| `health` | `/health` | — | — | `build` · `files[]` · `integrity` · `aux` | 없음 |

**입력 값**

| 입력 | 값 |
|---|---|
| `facet` | `profile` · `indication` · `outcome` · `adverse` · `adverse_detail` · `recovery` · `contraindication` · `offer` · `package` |
| `roles` | `자기` · `물려받음` · `하위 시술` · `하위 케이스` · `하위 제품` (계열의 케이스까지 가려면 `하위 시술,하위 케이스` 를 함께) |
| `filters` | 그 facet 표의 헤더 칸 = 값, 정확 일치. REST 는 되풀이 쿼리 `filters=polarity=발생함&filters=site_name=이마` · MCP 는 문자열 배열 또는 객체 |
| `classes`(pair) | `회피` · `보완` · `순서` · `간격` · `재시술 간격` 등 `g_pair.question_class` 값 |
| `edge_types`(neighbors) | `g_edge.edge_type` 값 — `부작용 위험` · `물려받음` · `적응` · `효과` · `하위 제품` · `재시술 간격` · `금기` · `제품 경유` · `하위 케이스` · `패키지 구성` · `구성 항목` · `보완` · `판매` · `하위 시술` · `순서` · `간격` · `상위 제품` · `대안` · `회피` · `이전 시술 확인` · `비교` · `관련 기법` · `반복 회차` |
| `kinds`(coverage) | `overview` · `mechanism` · `indication` · `outcome` · `adverse` · `recovery` · `contraindication` · `avoid` · `combo` · `same_day` · `order_interval` · `offer` · `package` · `lineup` |
| `limit` | 기본 100 · 최대 500 |

**자주 헷갈리는 것**

- `concern_candidates` 의 `site`: 물은 부위가 그 고민에 묶인 부위(`sites[]`) 안이면 **거르고**(`site_applied = filter`), 밖이면 거르지 않고 맞는 행에 `site_prefer: true` 표지만 단다(`site_applied = prefer`). 늘 거르려면 `site_mode=filter`.
- `concern_candidates` 의 `upper=auto`: 물은 고민에 행이 0 이면 가장 가까운 윗고민의 행을 낸다(머리 `inherited_from`).
- `descended[]`: 계열 · 메뉴 · 제품 층에만 닿은 적응을 시술까지 내린 **계열 단위 묶음**이다 — 그 안의 시술 하나하나가 그 적응을 자기 것으로 가진 것은 아니다.
- `facets` 의 대상 쪽은 같은 행이 층만 달리해 되풀이될 수 있다 — 서로 다른 행 수는 `counts.distinct_rows`.
- `ledger_check[]`: 원장 쪽에서 아직 확인이 걸린 코드의 id 목록. 행은 그대로 나오고, 「원천 미확정」 판정은 부르는 쪽이 한다.

## 5. 공통

**응답 머리**(모든 도구)

| 필드 | 뜻 |
|---|---|
| `build.gold_hash` | 데이터 판. 캐시 키로 쓴다 |
| `build.aux_hash` | 보조 입력(계층 · 부위 · 원장 확인) 판 |
| `build.loaded_at` | 적재 시각 |
| `request` | 기본값을 채운 입력. 「전부」 가 기본인 입력은 `null` |
| `total` | 이 조회의 전체 수(쪽과 무관 · 단위는 §4 표) |
| `next_cursor` | 다음 쪽 cursor · 마지막 쪽이면 `null` |

- **행 0 은 오류가 아니다** — `200` · `total: 0`. 「이 조회 범위에 행 없음」 일 뿐이다.
- 행의 gold 칸은 CSV 헤더 이름 그대로 · 값도 문자열 그대로(빈칸은 `""`).
- `cursor` 는 불투명 문자열이다. 같은 도구 · 같은 입력 · 같은 데이터 판에서만 쓴다 — 데이터가 바뀌었거나 입력이 다르면 `cursor_invalid`. 이때는 첫 쪽부터 다시 부른다.
- 쪽 밖 목록(`sites[]` · `descended[]` · `same_day_packages[]` · `ledger_check[]` 등)은 **첫 쪽(cursor 없는 요청)에만** 실린다. `counts*` 는 모든 쪽에 실린다.

**오류** — REST 본문은 `{"detail": "<코드>: <사유>"}` · MCP 는 같은 문구의 tool 오류(`isError: true`)

| 코드 | REST | 언제 |
|---|---|---|
| `invalid_argument` | 422 | 필수 없음 · 값 목록 밖 · 한도 밖 · `표:코드` 꼴 아님 · 없앤 입력(`abbr`) |
| `not_found` | 404 | 대상 · 값 · `gid` 가 gold 에 없음(`resolve` 후보 0 은 오류 아님) |
| `cursor_invalid` | 400 | cursor 해석 실패 · 다른 데이터 판 · 다른 도구 · 다른 입력 |
| `unavailable` | 503 | gold 꺼짐(§2) |

```text
GET /facets?node=product:PRD-400          → 422 {"detail":"invalid_argument: facet 는 필수다"}
GET /scope?node=product:PRD-999999        → 404 {"detail":"not_found: node = product:PRD-999999 가 gold 에 없다(g_scope)"}
```

**`Server-Timing`** — gold 응답마다 `Server-Timing: app;dur=<ms>` 머리가 붙는다(허브 안 처리 시간). stg `health` 실측 `app;dur=0.62`.

## 6. 예시

### REST — curl

```bash
G=https://api-stg-csp.medisolveai.com/procedure-hub/gold
```

**① 이름 → 코드(맞춤 꼴)**

```bash
curl -s -G $G/resolve --data-urlencode text=울쎄라
```

```json
{"build": {"gold_hash": "8accbb21…", "…": "…"},
 "request": {"text": "울쎄라", "range": null, "tables": null, "cursor": null, "limit": null},
 "total": 1, "next_cursor": null, "ambiguous": false,
 "candidates": [{"gold_table": "g_entry", "gid": "GEN-00391", "text": "울쎄라", "norm": "울쎄라",
                 "entity_table": "product", "entity_code": "PRD-400", "entity_name": "울쎄라",
                 "name_kind": "이름", "evidence_kind": "원장", "matched": {"span": "울쎄라"}, "in_range": null}]}
```

문장을 넣으면 후보 0 이다 — `text=울쎄라 아파요?` → `200` · `"total": 0` · `"candidates": []`.

**② 입구 목록(목록 꼴)** — 고민 입구 전부를 쪽으로

```bash
curl -s -G $G/resolve --data-urlencode tables=concern --data-urlencode limit=3
```

```json
{"total": 415, "next_cursor": "eyJhIjoiOTNlYzg5…",
 "counts": {"by_table": {"concern": 415}, "entities": 260},
 "candidates": [{"text": "주름", "entity_table": "concern", "entity_code": "CON-001", "name_kind": "이름", "…": "…"},
                {"text": "표정주름", "entity_code": "CON-002", "…": "…"},
                {"text": "동적 주름", "entity_code": "CON-003", "…": "…"}]}
```

다음 쪽은 `&cursor=<next_cursor>` 를 더해 같은 입력으로 부른다. 415 행 = 개념 260 의 이름 + 별칭.

**③ 고민 → 시술 후보**

```bash
curl -s -G $G/concern-candidates --data-urlencode concern_code=CON-001 --data-urlencode limit=2
```

```json
{"request": {"concern_code": "CON-001", "site": null, "upper": "auto", "to_procedure": "auto", "site_mode": "auto", "cursor": null, "limit": 2},
 "total": 114, "next_cursor": "eyJ…", "inherited_from": null, "site_applied": null,
 "counts": {"rows": 524, "groups": 114, "procedures": 50, "modality_only": 40, "unreached": 10,
            "descended": {"rows": 50, "modalities": 10, "procedures": 100, "new_procedures": 55, "undescended": 0},
            "sites": {"direct": 0, "lower": 13, "distinct_sites": 10}, "…": "…"},
 "ledger_check": [],
 "groups": [{"candidate_table": "procedure_case", "candidate_code": "CAS-001", "candidate_name": "보톡스(이마)",
             "procedure_code": "PRC-001", "procedure_name": "보톡스",
             "reach": ["제품 경유", "케이스 직접"], "concern_match": ["하위 고민"], "n_rows": 16,
             "rows": [{"gid": "GIN-00097", "concern_code": "CON-006", "concern_name": "미간주름",
                       "concern_match": "하위 고민", "target_code": "PRD-001", "reach": "제품 경유", "…": "…"}]}],
 "sites": [{"site_code": "SITE-014", "site_name": "이마", "concern_code": "CON-005", "csi_id": "CSI-0001", "match": "하위"}, "…"],
 "descended": [{"modality_code": "M1", "modality_name": "보톡스", "unit": "계열",
                "procedures": [{"procedure_code": "PRC-001", "procedure_name": "보톡스", "in_groups": true}],
                "from": [{"gid": "GIN-00003", "reach": "계열 층만", "lands": "modality", "path": ["…"]}]}]}
```

**④ 대상의 정보 — 부작용**

```bash
curl -s -G $G/facets --data-urlencode node=product:PRD-400 --data-urlencode facet=adverse --data-urlencode limit=2
```

```json
{"request": {"node": "product:PRD-400", "facet": "adverse", "roles": ["자기", "물려받음"], "filters": null,
             "hier": "expand", "offer_name_contains": null, "descend": "all", "cursor": null, "limit": 2},
 "total": 47, "next_cursor": "eyJ…",
 "counts": {"by_role": {"물려받음": 38, "자기": 9}, "polarity": {"발생함": 46, "해당 없음": 1}, "distinct_rows": 47},
 "ledger_check": [],
 "rows": [{"gold_table": "g_adverse", "gid": "GAD-01566", "target_code": "PRD-400", "target_name": "울쎄라",
           "adverse_code": "ADV-015", "adverse_name": "홍반", "adverse_top_name": "국소 반응",
           "polarity": "발생함", "duration_text": "일시적", "silver_id": "ADR-1530", "evidence_kind": "원장", "…": "…",
           "layer": {"role": "자기", "path": "제품",
                     "holder": {"holder_table": "product", "holder_code": "PRD-400", "holder_name": "울쎄라"},
                     "scope_gid": "GSC-03285", "depth": 1, "via": []}}]}
```

**⑤ 어떤 정보가 있나 · 행의 근거 · 시술 간 관계**

```bash
curl -s -G $G/coverage --data-urlencode nodes=product:PRD-400 --data-urlencode kinds=overview,adverse,offer,same_day
curl -s -G $G/evidence --data-urlencode gold_table=g_adverse --data-urlencode gold_id=GAD-01566
curl -s -G $G/pair --data-urlencode a=product:PRD-400 --data-urlencode classes=회피 --data-urlencode limit=1
```

```json
{"total": 1, "items": [{"node": "product:PRD-400", "name": "울쎄라", "kinds": [
  {"kind": "overview", "self": 1, "lower": 1, "lower_holders": 1, "inherited": 3},
  {"kind": "adverse", "self": 9, "lower": 7, "lower_holders": 1, "inherited": 38},
  {"kind": "same_day", "self": 9, "lower": 0, "lower_holders": 0, "inherited": 80},
  {"kind": "offer", "self": 2, "lower": 0, "lower_holders": 0, "inherited": 0}]}]}
```

```json
{"total": 2, "refs": [{"gold_table": "g_adverse", "gold_id": "GAD-01566", "silver_table": "adverse_risk", "silver_id": "ADR-1530",
  "n_source_refs": 2, "source_refs": [
    {"target_table": "adverse_risk", "target_id": "ADR-1530", "ref": "taxonomy.json:/modality/8/subcategories/0/items/0/extracted/safety/common/0"},
    {"target_table": "adverse_risk", "target_id": "ADR-1530", "ref": "taxonomy.json:/modality/8/products/0/extracted/safety/common/0"}]}]}
```

```json
{"total": 3, "counts": {"by_class": {"회피": 3}, "same_day": {"": 1, "불가": 1, "조건부": 1}, "conflict": 0},
 "same_day_packages": [], "ledger_check": [],
 "rows": [{"gid": "GPR-00638", "from_code": "M7", "from_name": "실리프팅", "to_code": "M9", "to_name": "기기 리프팅",
           "kind": "주의", "question_class": "회피", "text": "실리프팅 부위 열 시술 주의", "…": "…",
           "a_side": "to", "a_layer": {"role": "물려받음", "holder": {"holder_code": "M9", "holder_name": "기기 리프팅"}, "…": "…"},
           "b_layer": null}]}
```

`a_layer.role = 물려받음` — 울쎄라 자체가 아니라 상위 계열(기기 리프팅)의 관계를 물려받은 행이라는 뜻이다. 답에 쓸 땐 층을 함께 밝힌다.

### MCP — curl 로 세션 열기

streamable HTTP 다. 요청마다 `Accept: application/json, text/event-stream` 을 준다.

```bash
M=https://api-stg-csp.medisolveai.com/procedure-hub/gold-mcp/mcp
A='Accept: application/json, text/event-stream'

# 1) initialize — 응답 머리의 mcp-session-id 를 받는다
curl -s -D - -X POST $M -H 'Content-Type: application/json' -H "$A" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"my-service","version":"0"}}}'
# → mcp-session-id: <SID>
# → {"result":{"serverInfo":{"name":"procedure-hub-gold"},"instructions":"Procedure Hub gold 결정론 조회(LLM 없음 · 쓰기 없음). …", …}}

S="mcp-session-id: <SID>"; V='mcp-protocol-version: 2025-06-18'

# 2) initialized 알림 → 202
curl -s -X POST $M -H 'Content-Type: application/json' -H "$A" -H "$S" -H "$V" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized"}'

# 3) 도구 목록 → resolve · scope · neighbors · facets · concern_candidates · pair · evidence · coverage · health
curl -s -X POST $M -H 'Content-Type: application/json' -H "$A" -H "$S" -H "$V" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list"}'

# 4) 도구 부르기
curl -s -X POST $M -H 'Content-Type: application/json' -H "$A" -H "$S" -H "$V" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"resolve","arguments":{"text":"울쎄라"}}}'
```

```json
{"jsonrpc": "2.0", "id": 3, "result": {
  "isError": false,
  "content": [{"type": "text", "text": "{\n  \"build\": {…}, …}"}],
  "structuredContent": {"build": {"gold_hash": "8accbb21…", "…": "…"}, "total": 1, "next_cursor": null,
                        "candidates": [{"entity_table": "product", "entity_code": "PRD-400", "entity_name": "울쎄라", "…": "…"}]}}}
```

- `structuredContent` 가 REST 응답 JSON 과 같다. 오류면 `isError: true` 이고 `content[0].text` 가 REST `detail` 과 같은 문구다.
- 도구마다 `_meta` 에 `anthropic/maxResultSizeChars: 1000000` 이 있다 — 한 쪽(최대 `limit` 500)이 커도 잘리지 않게.

### Python — httpx(REST · 쪽 끝까지)

```python
import httpx

BASE = "https://api-stg-csp.medisolveai.com/procedure-hub/gold"

def call_all(client: httpx.Client, path: str, params: dict, key: str) -> tuple[str, list]:
    """next_cursor 가 null 이 될 때까지 넘겨 key 목록을 모은다. (gold_hash, rows) 를 돌려준다."""
    rows, cursor, gold_hash = [], None, None
    while True:
        r = client.get(path, params={**params, **({"cursor": cursor} if cursor else {})})
        if r.status_code == 503:
            raise RuntimeError(r.json()["detail"])  # unavailable: gold 꺼짐
        r.raise_for_status()                      # 400 · 404 · 422 → detail = "<코드>: <사유>"
        body = r.json()
        gold_hash = gold_hash or body["build"]["gold_hash"]
        rows += body[key]
        cursor = body["next_cursor"]
        if cursor is None:
            return gold_hash, rows

with httpx.Client(base_url=BASE, timeout=10) as c:
    cands = c.get("/resolve", params={"text": "울쎄라"}).json()["candidates"]
    node = f'{cands[0]["entity_table"]}:{cands[0]["entity_code"]}'          # product:PRD-400
    _, adverse = call_all(c, "/facets", {"node": node, "facet": "adverse", "limit": 500}, "rows")
    print(node, len(adverse))                                               # product:PRD-400 47
```

목록 입력은 콤마로 이어 준다(`{"roles": "자기,물려받음,하위 제품"}`). `filters` 는 `[("filters", "polarity=발생함"), ("filters", "site_name=이마")]` 처럼 키를 되풀이한다.

### Claude · MCP 클라이언트 설정

Claude Code:

```bash
claude mcp add --transport http procedure-hub-gold https://api-stg-csp.medisolveai.com/procedure-hub/gold-mcp/mcp
```

`.mcp.json`(또는 같은 꼴을 받는 클라이언트):

```json
{
  "mcpServers": {
    "procedure-hub-gold": {
      "type": "http",
      "url": "https://api-stg-csp.medisolveai.com/procedure-hub/gold-mcp/mcp"
    }
  }
}
```

Python 공식 SDK 로 직접 붙을 때는 `mcp.client.streamable_http.streamable_http_client(url)` → `ClientSession(read, write)` → `initialize()` · `list_tools()` · `call_tool(name, arguments)` 꼴이다(상담 앱 `clinic_chat/clients/hub_mcp.py` 가 같은 꼴).

## 7. 주의

| 무엇 | 내용 |
|---|---|
| `resolve` 는 정확한 이름만 | 공백 · 대소문자만 무시하고 나머지는 글자 그대로 같아야 한다. 문장 · 조사 붙은 말 · 줄임말 · 오타는 후보 0 이다. **문장 해석은 부르는 쪽 몫** — 목록 꼴로 입구를 받아(상담 앱은 `tables=concern,site,modality,procedure,product` 로 끝까지 받아 `gold_hash` 마다 한 번 캐시) LLM 이 고르게 한다 |
| 겹치는 이름 | 같은 이름에 개념이 여럿이면(`ambiguous: true`) 전부 낸다. 고르는 것은 부르는 쪽이다 |
| 데이터 판 | 데이터를 다시 적재하면 `gold_hash` 가 바뀐다. 코드 · 입구 목록 캐시는 `gold_hash` 를 키로 두고, 바뀌면 다시 받는다. 옛 cursor 는 `cursor_invalid` |
| 층을 밝혀 쓰기 | `layer.role`(자기 · 물려받음 · 하위 *)이 붙은 행은 그 대상 것이 아닐 수 있다. 물려받은 행을 대상 자신의 사실처럼 쓰지 않는다 |
| 그림 | 원리 · 방법 그림은 허브 DB 에만 올라가 있고 **응답에는 아직 없다**(다음 판) |
| 인증 · 주소 | 지금은 stg 만 · 인증 없음. 운영 주소 · 인증이 생기면 이 문서를 고친다 |
| 계약이 바뀌는 곳 | 도구 계약 `orchestration/work/phub-gold-jev/SPEC-001-hub-gold-mcp.md` · stg 기동 · 꺼짐 `SPEC-003-hub-gold-db.md` §11 · 그림 데이터 `SPEC-007-image-data.md` |

## 변경 기록

- 2026-11-18 — stg 첫 공개(허브 `release/v1.2.0` · `gold_hash` `8accbb213ac5…` · 도구 9 · 인증 없음).

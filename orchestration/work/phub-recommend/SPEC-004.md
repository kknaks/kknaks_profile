---
type: spec
id: SPEC-004
title: "그래프 v2 — 새 실버 원장 + 시맨틱 엣지 + 골드 tool"
status: draft
product: procedure-hub
feature: phub-recommend
version: 0.2.0
created_at: 2026-10-27
updated_at: 2026-10-27
tags:
  - product/procedure-hub
  - feature/phub-recommend
  - doc/spec
  - status/draft
links:
  baselines: []
  decisions:
    - "orchestration/work/phub-recommend/DEC-001.md"
    - "orchestration/work/phub-recommend/DEC-002.md"
    - "orchestration/work/phub-recommend/DEC-003.md"
  specs:
    - "orchestration/work/phub-recommend/SPEC-001.md"
    - "orchestration/work/phub-recommend/SPEC-003-mfds-ingest.md"
  works:
    - "orchestration/work/phub-recommend/WORK-002.md"
  releases: []
  related:
    - "orchestration/work/phub-recommend/_RESUME.md"
    - "orchestration/work/phub-recommend/review-spec-004-report.md"
---

> **SPEC-005 · WORK-003 으로 대체됨(2026-10-30)**

# 그래프 v2 — 새 실버 원장 + 시맨틱 엣지 + 골드 tool

SPEC-001(v1)은 taxonomy 시술 항목 521 을 시술 노드로 썼다. DEC-002 는 그 자리를 **단위 시술(무엇을 × 어디에 × 어떻게)** 로 바꿨고, DEC-003 은 제조사 · 제품/장비 · 규격 원장을 더했다. 이 SPEC 은 그 결정에 맞춰 그래프를 다시 짓는다.

- **브론즈**: stg 21 은 그대로 둔다. 오늘 만든 작업 산출물 JSON(시술 원장 v3 · 제품 원장 v4 · 원천 수정 목록)과 게이트 답 JSON 을 「큐레이션 원천」으로 더 적재한다. 해시 · 멱등 규칙은 같다
- **실버**: 계열 · 단위 시술 · 부위(트리) · 기법 · 목적 · 패키지 · 제품(라인) ⊃ 품목 · 제조사 · 규격 · 고민(트리)을 둔다. 노드마다 상담 용어 이름 · 공식명 · 동의어 · 원천 · 게이트 상태를 단다
- **시맨틱**: 고민 → 단위 시술 · 계열 ↔ 계열(엣지 하나) · 단위 시술 → 부위 · 기법 · 계열 · 장비 · 제품 → 품목 → 제조사 · 규격 · 계열 단위 안전을 잇는다. 원천이 시술군 코드에만 있는 관계를 단위 시술로 **내리는 규칙**을 정한다
- **골드**: v1 의 REST 7 · MCP 6 tool 을 v2 에 다시 건다. 기본 응답은 **승인 · 자동만** 낸다. `include_unconfirmed=true` 를 주면 나머지도 함께 낸다(§4.1)

모델 호출은 어디에도 없다(DEC-001 D-12). 이 SPEC 은 **오늘 범위**(§1 Scope)만 구현 계약으로 둔다. 나머지는 §8 「2차」로 옮겼다.

> **변경 이력**
> - 0.2.0 (2026-10-27) 검수 FAIL 3 · WARN 9 반영(`review-spec-004-report.md`). §3.1 계약을 실물 입력의 키로 다시 썼다 — 시술 원장 v3 의 단위 시술 236 · `ledger_map` 행선지 11종 · X 계열 · 부위 예외, `gate-answers/product-match.json`, 제품 원장 v4(F-1 · F-2). 제조사는 고른 허가 후보의 `company` · `manufacturer_original` 로 세운다(F-3). 골드 기본 응답은 승인 · 자동만 낸다(W-1, 코디 기본값). 동점은 후보를 전부 돌려주고 임의로 고르지 않는다(W-2). 「(묶음)」 이름(W-3) · E2E 문장(W-4) · 규격 원천 하나(W-6) · 테스트 범위(W-8) · schema 판정(W-9)을 고쳤다. 오늘 범위를 줄이고 나머지는 §8 로 옮겼다
> - 0.1.0 (2026-10-27) 초안

> SPEC-001 규칙 가운데 이 문서가 **바꾸지 않는 것**은 그대로 유효하다. 브론즈 해시 · 멱등(§3.1), 정규화 함수(§3.3.1-1), 발행 정책(error 만 차단), 발행본, 조회 응답 공통 필드, MCP 전송 · 위치(§5.1), 모듈 경계 import 허용 목록(§5.2), 로컬 포트(§5.4)가 그렇다. 이 문서에는 달라지는 것만 적는다. 두 문서가 다르면 이 문서를 따른다.

## 1. Context

### Meta

- Decision reference: `DEC-001`(D-02 · D-03 · D-04 · D-05/06 · D-12) · `DEC-002`(D-01~D-08) · `DEC-003`(D-01~D-06) · `_RESUME.md` §2 2026-10-27 행 전부
- 구현 기준(재사용): SPEC-001 0.2.1 · 코드 `PROCEDURE-HUB/phub-recommend/backend/app/modules/graph/`
- 단순화: SPEC-003(식약처 API 브론즈 · 매칭 테이블)은 구현하지 않는다. 같은 일을 이미 끝낸 작업 산출물을 원천으로 쓴다(OQ-G14)
- 실물 대조 시점: 2026-10-27 17:00 전후 — `procedure-master-v3.json`(단위 시술 236) · `product-master-draft.json`(`version` 4) · `gate-answers/*.json`. 아래 숫자는 이 시점 값이다
- 근거 개념: [[medallion-architecture]] · [[data-lineage]]

### Business Requirement

상담 발화 넷 — 「처짐이 고민이에요」 · 「턱쪽에 필러」 · 「포텐자 하고 싶어요」 · 「보톡스랑 필러 같이」 — 이 그래프에서 단위 시술에 닿아야 한다. 거기서 안전 · 제품 · 제조사까지 끊기지 않아야 한다.
승인 게이트 원칙(`_RESUME` §2 「승인된 것만 다음 단계」 · DEC-003 D-03)에 따라 골드 기본 응답은 승인 · 자동만 낸다. 미확인 · 원천 근거만 · 임시값도 그래프에는 싣는다. 대신 상태를 달고, 요청할 때만 내보낸다.

### Scope — 오늘

In scope:

- 큐레이션 브론즈 적재 — §3.1
- 노드 16종(제조사 포함 — F-3 (a)) — §3.2
- 엣지 16종의 오늘 규칙 — §3.3(`procedure_relation` 은 계열 단위만 · `treats` ④ 의 장비 갈래 없음)
- 검증 v2 · 발행 — §3.4
- 조회 tool 재배선 + `include_unconfirmed` — §4
- v1 교체 — §5.1 · E2E E-1~E-5 — §6

Out of scope: §8 「2차」에 모았다.

## 2. UX Contract

해당 없음 — 화면이 없다. 사용자는 Swagger 와 MCP 클라이언트로 쓴다(SPEC-001 §5.4).

## 3. 데이터 계약

| 레이어 | 입력 | 출력 | 허용 변환 | 금지 |
|---|---|---|---|---|
| 브론즈 | stg 21 + 큐레이션 7행(§3.1) | 원천별 원본 JSON 행 | 해시 계산만 | 필드 가공 |
| 실버 | 원천별 최신 브론즈 | 노드 v2(§3.2) | 필드 선택 · 정규화 · 이름 치환표(§3.2.3) · id 부여 | 큐레이션에 없는 단위 시술 · 부위 · 기법 만들기 · 모델 호출 |
| 시맨틱 | 같은 브론즈 + 실버 | 엣지 v2 · 주장 · 게이트 상태(§3.3) | 결정론 이름 해석 · 내림 규칙 | 원천 값 하나만 고르기 · **동점 임의 선택** · 부분 일치 · 편집 거리 |
| 골드 | 최신 발행본 | 조회 응답(§4) | 조회 시 조합 · 게이트 거르기 · 안전 동반 | 발행 전 버전 · 브론즈 직접 참조 |

### 3.1 브론즈 — 큐레이션 원천

#### 3.1.1 원천 목록

v1 의 `graph_bronze_snapshot` 에 그대로 넣는다(새 테이블 없음). 파일 위치 `$W` = 코디 워크트리 `orchestration/work/phub-recommend/`.

| endpoint | 파일 | 빌드 |
|---|---|---|
| `curation:procedure-master` | `$W/procedure-master-v3.json` | 필수 |
| `curation:product-master` | `$W/product-master-draft.json`(지금 `version` 4) | 필수 |
| `curation:source-fix-list` | `$W/source-fix-list.json` | 필수 |
| `gate:product-match` | `$W/gate-answers/product-match.json` | 필수 |
| `gate:source-fix` | `$W/gate-answers/source-fix.json` | 필수 |
| `gate:classify-v1` · `gate:classify-v2` | `$W/gate-answers/classify-v1.json` · `classify-v2.json` | **보관만** — 답은 이미 시술 원장 v3 의 `approval` 에 반영됐다(시술 원장 `rules.answers`) |

- stg 10 가운데 `products` 는 보관만 한다. 제품의 원천은 `curation:product-master` 다. 나머지 stg 9 는 계속 빌드에 쓴다
- 빌드 필수 원천 = stg 9 + 큐레이션 5 = **14**. 하나라도 없으면 `missing_bronze`(error)

#### 3.1.2 `curation:procedure-master` — 실물 칸

빌드가 읽는 최상위 칸은 `site_tree` · `site_special` · `site_out_of_tree` · `families` · `techniques` · `unit_procedures` · `ledger_map` 이다. 나머지(`rules` · `summary` · `provisional` · `market_rows` · `market_rows_skipped` · `rejected_combinations`)는 브론즈에 보관만 한다.
「필수」 칸이 없으면 `curation_shape_error`(error)다. **값이 참조를 못 찾는 것은 error 가 아니다** — 그 노드 · 엣지만 만들지 않고 warning 으로 센다.

| 배열 | 필수 칸 | 쓰는 선택 칸 | 실물 |
|---|---|---|---|
| `families[]` | `id` · `name` | `synonyms[]`(문자열) · `sub_families[]` · `source_name` · `name_status` | 23 = M1~M17 · **X1~X6**(사용자 답에서 온 계열) |
| `site_tree[]` | `name` · `parent`(이름 또는 null) | `added_oq206` | 43. 묶음은 이름에 「(묶음)」 이 붙는다 |
| `site_special[]` | `name` · `meaning` | — | 「해당 없음」 1(수액 — DEC-003 OQ-306 처리) |
| `site_out_of_tree[]` | 문자열 | — | 7 |
| `techniques[]` | `id` · `name` | `source_expressions[]` · `provisional` | 65 |
| `unit_procedures[]` | `id` · `name` · `family` · `site`(null 허용) · `site_status` · `approval` | `sub_family` · `technique`(기법 **이름**) · `synonyms[{text, type}]` · `devices[]` · `product_item_ids[]` · `purposes[]`(이름) · `source_items[]` · `source_market[]` · `provisional` · `ingredient` · `route_status` · `name_status` · `key` | 236 |
| `ledger_map[]` | `id`(원장 항목 id) · `name` · `family` · `approval` · `destinations[]` | `kind_v2` · `provisional` · `note` | 521 |

**계열 `modality_codes`** — 실물에는 이 칸이 없다. `id` 가 `M` 으로 시작하면 `[id]`, 아니면(X1~X6) `[]` 다. **코드와 계열은 1:1** 이다(M9 의 HIFU · RF 는 계열이 아니라 단위 시술의 `sub_family` 속성이다). X 계열은 stg 원천(금기 · 부작용 · `treats` · 환자 금기)에 걸리지 않는다 → safety `gaps` 에 `no_modality_source` 가 붙는다(OQ-G04).

**부위 이름 · id(W-3)** — `node_id` = `site:<원문 이름>`(「턱(묶음)」 처럼 접미 포함) · `name` = 「(묶음)」 을 뗀 값(「턱」) · `parent_id` = 부모 원문의 id. 원문은 동의어에 넣지 않는다. 그래서 이마 · 눈가 · 코 · 볼 · 목은 묶음과 하위가 같은 이름으로 둘이 된다. 검색 동점은 타입 순서 다음 `node_id` 사전순으로 낸다(둘 다 낸다).

**단위 시술의 부위(`site_status`)**

| `site_status` | 실물 | `at_site` 엣지 | 검증 |
|---|---|---|---|
| `tree` · `added` | 175 · 7 | `site:<site>` 로. 트리에서 못 찾으면 만들지 않음 | `dangling_reference`(warning) |
| `not_applicable` | 27(`site`=「해당 없음」 — 수액) | 없음. `attributes.site_status` 로만 둔다 | 없음(결정된 상태) |
| `missing` | 25(`site`=null) | 없음 | `unit_without_site`(warning) |
| `out_of_tree` | 2(옆구리 · 등) | 없음 | `site_out_of_tree`(warning) |
| 그 밖 | 0 | 없음 | `unknown_site_status`(warning) |

**`approval` → 게이트 상태**(단위 시술 · 원장 항목 공통):

| `approval` | 뜻(시술 원장 `rules.approval`) | 단위 시술 | 원장 항목 | `gate_status` |
|---|---|---|---|---|
| `approved` | 사용자 승인 | 30 | 230 | `approved` |
| `source_only` | 원천 근거(시장가 · 장비 · 고민 이름)로만 세웠고 분류표 게이트를 거치지 않음 | 123 | — | `unconfirmed` |
| `regate_pending` | 재판정값만 있고 2차 답 없음 | 40 | 89 | `unconfirmed` |
| `provisional` | 답 없는 질문의 첫 선택지를 임시 적용 | 27 | 59 | `unconfirmed` |
| `waiting_mfds` | 식약처 대기 | 16 | 137 | `unconfirmed` |
| `hold` | 보류 | — | 6 | `unconfirmed` |
| `market` · 그 밖 | (`rules` 에 정의는 있으나 실물 0) | 0 | 0 | `unconfirmed` + 모르는 값이면 `unknown_approval_value`(warning) |

`provisional: true` 는 `approval` 과 상관없이 `unconfirmed` 다.

**`ledger_map[].destinations[]` — 행선지 11종**

행 하나에 행선지가 1~8개 있다. 타입마다 칸이 다르다.

| `type` | 칸 | 실물 | 처리 |
|---|---|---|---|
| `unit_procedure` | `unit_procedure_id` · `name` · `via` | 403 | 노드 · 엣지 없음 — 이름 해석의 행선지(§3.3.2). 없는 id 면 `dangling_reference` |
| `product` · `device` | `product_master_id` · `product_name`(product 만) · `match_status` | 184 · 154 | 제품 노드(§3.2.4). **계열 = 같은 행의 `ledger_map[].family`** → `has_product` |
| `purpose` | `purposes[]`(이름) | 10 | 목적 노드 `purpose:<normalize(이름)>`(목적 id 가 없어 이름으로 세운다) |
| `package` | `components[{family, site, unit_procedure_ids[]}]` · `components_source` | 17 | 패키지 노드 `package:<ledger id>`(이름 = 행 `name`) · `includes` → `unit_procedure_ids` 전부 |
| `family` | `family` · `sub_family` | 6 | 노드 · 엣지 없음. 이름 해석에서 그 원장 이름 → 계열 |
| `technique` | `technique`(이름) | 8 | 노드 · 엣지 없음. 이름이 `techniques[].name` 과 같으면 그 원장 이름을 기법 동의어로 더한다 |
| `material` · `device_attribute` · `hold` · `not_procedure` | 각자 | 2 · 1 · 21 · 21 | 노드 · 엣지 없음. `ledger_destination_skipped`(warning, `subject_kind` = type) |

모르는 `type` 은 `ledger_destination_skipped`(`subject_kind=unknown`)로 센다.

**`unit_procedures[].synonyms[{text, type}]`** — type: product 149 · device 127 · ledger_item 125 · problem_tree 61 · market 50 · technique_expression 13 · device_accessory 1. 모든 type 을 **검색**에 쓴다. **이름 해석 사전(§3.3.2)** 에는 `ledger_item` · `market` 만 넣는다(W-2).

#### 3.1.3 게이트 답 — 실물 모양

**`gate:product-match`** = `{"items": [ {ledger_id, name, status, license_keys[], source, note} × 340 ], "new_devices": [35]}`

| `status` | 실물 | 뜻 | 제품 `license_status` | 제품 `gate_status` |
|---|---|---|---|---|
| `auto` | 143 | 자동 확정(규칙 A · 라인 자동). `license_keys` = 이 원장 항목의 허가 | `licensed`(정상 하나 이상) · `cancelled`(전부 취소) | `auto` |
| `not_applicable` | 45 | 허가 대상 아님 | `not_applicable` | `auto` |
| `unconfirmed` | 129 | 허가 미확인 | `unconfirmed` | `unconfirmed` |
| `pending` | 23 | 「이름 맞고 업체 다름」 — 직접 확인 대기(답 전) | `unconfirmed` | `unconfirmed` |

- `source` 는 auto 317 · none 23. **사용자 답(`user`)은 아직 0** 이다. 그래서 오늘은 `approved` 제품이 없다. 사용자 답이 생기면 `source=user` 행이 `gate_status=approved` 가 된다(다시 적재 → 다시 빌드)
- 「해당 허가 없음」 확정(`none` 등)은 실물에 없다. 나오면 `license_status=unlicensed` · `gate_status=approved` 로 둔다. 모르는 `status` 는 `unconfirmed` + `unknown_gate_value`(warning)
- 파일에 없는 원장 항목은 `unconfirmed` 다. `new_devices[]` 는 보관만 한다(OQ-G11)

**`gate:source-fix`** = 최상위 `{ "<항목 id>": {decision, note, proposed, updated_at} }`(감싸는 `items` 키 없음). 실물은 A1-001~006 이고 6건 모두 `fix` 다. `proposed` 는 **문자열 전체**다(A1-006 「바디 처짐」).

**`gate:classify-v1` · `-v2`** = `{ "<항목 id>": {decision, reason, updated_at, …} }` — 보관만 한다.

### 3.2 실버 — 노드 v2

#### 3.2.1 공통 필드

v1 공통 필드(`node_id` · `type` · `name` · `names` · `synonyms` · `attributes` · `source_refs`)를 그대로 쓴다.

| 필드 | v2 의 뜻 |
|---|---|
| `name` | 상담 용어(DEC-002 D-04). 계열 = `families[].name`(M1 「보툴리눔 톡신」) · 제품 = `product_name` · 부위 = 「(묶음)」 을 뗀 이름 |
| `names` | `ko` · `en`(있을 때) · `official`(품목의 공식 품목명 등 — 있을 때) |
| `synonyms` | 채운다. 정규화값 기준으로 중복을 지우고, 이름과 같은 것은 뺀다. 원문 첫 표기를 남긴다 |
| `attributes.gate_status` | `approved` · `auto` · `unconfirmed` — **모든 노드** |
| `attributes.approval` | 원천의 승인 원값(`approval` · 제품 게이트 `status`) — 있을 때 |

#### 3.2.2 게이트 상태

| 값 | 뜻 | 붙는 곳 |
|---|---|---|
| `approved` | 사람이 게이트에서 승인 | `approval=approved` 인 단위 시술 · 패키지 · 목적 / 제품 게이트 `source=user` / 치환된 이름(`fix`) |
| `auto` | 원천 그대로 · 자동 확정 | stg 원천 노드(고민 트리 · 부작용 · 최적화 고민 · 시너지 목표) / 계열 · 부위 / `provisional` 아닌 기법 / 제품 게이트 `auto` · `not_applicable` / 그 허가에서 만든 품목 · 제조사 · 규격 |
| `unconfirmed` | 미확인 · 원천 근거만 · 임시값 | §3.1.2 · §3.1.3 표의 나머지 |

- **주장**도 같은 세 값을 갖는다. 주장의 상태는 그 주장이 기댄 양 끝 노드 · 규칙 가운데 **가장 약한 값**이다(`unconfirmed` < `auto` < `approved`). 임시 내림 규칙(규칙 A · 부위 일치 — OQ-G01 · G02)으로 만든 주장은 `unconfirmed` 다
- 패키지 · 목적은 그것을 낸 원장 항목 · 단위 시술의 상태를 따른다. 목적이 여러 원천에서 나오면 가장 강한 값을 쓴다 — 승인된 원천이 하나라도 있으면 그 목적 이름은 승인된 것이다
- **모든 상태를 발행한다.** 거르는 것은 골드(§4.1)다

#### 3.2.3 이름 치환표 — 「쳐짐 → 처짐」

원천 수정이 stg 에 반영되기 전까지는, 브론즈를 읽을 때 **값만 치환**한다. 브론즈 원본은 그대로다.

- 대상: `source-fix-list.json` `items[]` 의 그룹 `A1` 가운데 `gate:source-fix` 답이 `fix` 인 것. 다른 그룹은 적용하지 않는다(OQ-G09)
- 규칙: `taxonomy` · `problem-packages` 의 문자열 값이 항목의 `current` 와 **전체가 같으면** `proposed`(답의 값, 비면 목록의 값)로 바꾼다. 실물 6 항목이 고유 문자열 6개(「쳐짐」 · 「얼굴 쳐짐」 · 「볼쳐짐/불독살」 · 「눈가 쳐짐」 · 「눈꺼풀쳐짐」 · 「바디 쳐짐」)를 모두 덮는다. 부분 치환은 하지 않는다
- 같은 표를 시술 원장 단위 시술의 `problem_tree` 동의어에도 적용한다(W-2 — 「볼쳐짐/불독살」 · 「눈꺼풀쳐짐」 이 남아 있다)
- 바뀐 노드 · 동의어에는 원천 표기를 동의어로 남긴다(「쳐짐」 검색도 계속 걸린다). CC 문자열(`cc` · `cc_group` · `problem`)에도 적용한다 — 그래야 v1 의 「CC → 고민 항목」 매칭이 맞는다
- 적용 건수를 `source_fix_applied`(warning)로 남긴다. stg 가 고쳐지면 0 이 된다

#### 3.2.4 노드 타입 16

| 타입 | 원천 | `node_id` | `name` | 주요 `attributes` |
|---|---|---|---|---|
| `family` | `families[]` | `family:<id>` | `name` | `modality_codes[]` · `sub_families[]` · `extracted`(코드의 taxonomy `modality[].extracted` — X 없음) · `session_phase_order`(v1 규칙 · 코드 기준) |
| `unit_procedure` | `unit_procedures[]` | `unit:<id>` | `name` | `family_id` · `sub_family` · `site_id`(있을 때) · `site_status` · `technique_id` · `ingredient` · `route_status` · `source_item_ids[]` · `source_market[]` · `provisional` · `approval` · `name_status` |
| `site` | `site_tree[]` | `site:<원문 이름>` | 「(묶음)」 을 뗀 이름 | `parent_id` · `is_bundle` · `added_oq206` · `danger_zone_ids[]` |
| `technique` | `techniques[]` | `technique:<id>` | `name` | `provisional`. 동의어 = `source_expressions` + 행선지 `technique` 의 원장 이름 |
| `purpose` | 행선지 `purpose` 이름 + `unit_procedures[].purposes` | `purpose:<normalize(이름)>` | 이름 | `source_item_ids[]` |
| `package` | 행선지 `package` | `package:<ledger id>` | 원장 이름 | `components_source` · `composition_known` |
| `product` | 행선지 `product` · `device` 가 가리키는 `product-master` `products[]` | `product:<normalize(product_name)>` — 같은 브랜드면 한 노드(OQ-G08) | `product_name` | `product_kind`(`products[].kind`) · `license_kind` · `license_status` · `family_ids[]`(행 `family`) · `ledger_ids[]` · `maker_texts[]` · `in_use_at_clinic[]` · `approval` |
| `product_item` | 고른 허가(`license_keys`)를 아래 「묶음」 규칙으로 묶은 것 | `product_item:<묶음 허가 key 사전순 첫째>` | 아래 | `license_kind` · `licenses[]`(key · 허가번호 · 허가일 · `state` · 모델명 · 공식 품목명 · 성분 · 효능/사용목적 · `role` · `consign_manufacturer`) · `state`(정상 하나 이상이면 `정상`) |
| `manufacturer` | 고른 허가의 후보 행(§3.2.6) | `manufacturer:<normalize(열쇠 이름)>` | §3.2.6 | `name_original` · `roles[]` |
| `spec` | `product-master` `specs[]` 중 ① `source=mfds-license` 이고 `license_key` 가 고른 허가 ② `source=market-pricing` · `parsed` · `amount` 있음 · `product_id` 가 만든 제품의 원장 항목(W-6 — 원천은 `specs[]` 하나) | `spec:<제품 키>:<normalize(raw)>` | `raw` | `amount` · `unit` · `sessions` · `scope_text` · `source` · `license_key` |
| `concern` · `concern_subcategory` · `concern_item` | stg `taxonomy` `problem[]` + 치환표 | v1 그대로 | v1(치환 뒤) | v1 + `site_ids[]`(`concern_item` — §3.3.3 A) |
| `opt_concern` · `synergy_target` · `complication` | v1 그대로 | v1 | v1 | v1 |

- 타입 순서(검색 동점 · 스키마): `concern` · `concern_subcategory` · `concern_item` · `purpose` · `opt_concern` · `synergy_target` · `site` · `family` · `unit_procedure` · `technique` · `package` · `product` · `product_item` · `manufacturer` · `spec` · `complication`
- 없어지는 v1 타입은 `procedure_group` · `procedure` · v1 `product` · v1 `site` 다. 원천 id 는 `source_item_ids` · `ledger_ids` · `modality_codes` · `danger_zone_ids` 로 남는다
- **품목 묶음**(제품 게이트 페이지 `product-match-build.py` `groups()` 와 같은 결정론): 허가 후보 행의 키 = `company` + `|` + base(이름). 이름 = 의료기기는 `model_name`(비면 `official_name`), 의약품은 `official_name`. base = 괄호 · 대괄호 내용과 용량 표기(숫자 + `단위|유니트|유닛|U|mg|mL|ml|cc|g|IU`)를 떼고 공백을 지운 소문자. 품목 `name` = 묶음 첫 행(허가 key 사전순)의 이름에서 용량 표기를 뗀 값 · `names.official` = `official_name`. 의료기기 `official_name` 은 「조직수복용생체재료」 같은 **일반명칭**이라 이름으로 쓰지 않는다
- 제품 동의어 = 원장 이름(`products[].name` 전부) · `products_json.name` · `products_json.name_en` · 품목 이름들

#### 3.2.5 위험 부위 → 부위 노드

v1 위험 부위 11 은 부위 노드 `danger_zone_ids` 와 `site_caution` 엣지로 간다. 대응은 DEC-002 표를 따르고, 「확인 필요」 는 **묶음**(넓은 쪽)에 단다(OQ-G10): forehead → 이마 · glabella → 미간 · temple → 관자놀이 · periorbital → 눈가(묶음) · nose → 코(묶음) · nasolabial → 팔자 · cheek → 볼(묶음) · lips → 입술 · chin → 턱(묶음) · jawline → 턱선 · neck → 목(묶음). 대응이 안 되면 `danger_zone_unmapped`(warning).

#### 3.2.6 제조사 — 고른 허가 후보에서(F-3 (a))

조인: 제품 게이트 `license_keys` 의 key → `product-master` `products[ledger_id].match.candidates[]` 가운데 `key` 가 같은 행. 실물 486 key 가 **전부** 조인된다. 못 찾으면 `license_key_not_in_candidates`(warning)를 내고 그 허가는 건너뛴다.
`manufacturers[]` 배열은 **쓰지 않는다**(`products[].link` 는 매칭 상태라 조인 키가 아니다 — 국가 · 역할 병합은 2차).

| 엣지 | 끝 노드의 열쇠 | `name` | `name_original` | 언제 |
|---|---|---|---|---|
| `licensed_to`(허가 보유 = 국내 수입 · 제조 업체) | `company`(항상 있다) | `company` 원문 | 의약품 = `manufacturer_original`(의약품에서는 허가 업체의 영문명이다) · 의료기기 = `company_original`(있으면) | 모든 허가 |
| `manufactured_by`(제조원) | 의료기기 `manufacturer_original` | 원문 | 같은 값 | 의료기기 · `manufacturer_original` 있음(해외 제조원) |
| `manufactured_by` | `company`(위 `licensed_to` 와 같은 노드) | — | — | 의료기기 · `manufacturer_original` 빔(국내 제조) |
| (없음) | — | — | — | 의약품 — 실제 제조원은 `consign_manufacturer` 자유 문자열이다. 품목 속성으로만 둔다(2차) |

- 정규화는 SPEC-001 `normalize()` 만 쓴다. 법인 표기는 떼지 않는다(OQ-G16). 정규화값이 같은 표기는 한 노드로 모으고, 첫 표기가 아닌 원문은 동의어로 둔다
- `roles` = `licensed_to` 로 쓰였으면 `license_holder` + 허가 행 `role`(제조업 · 수입업), `manufactured_by` 로 쓰였으면 `manufacturer`
- 예(실물): 쥬비덤 품목 → `licensed_to` 한국애브비(주) · `manufactured_by` Allergan. 보톡스 품목(`drug:200901660` · `drug:200804190` 한 묶음) → `licensed_to` 한국애브비(주)만
- 취소된 허가(`state=취소`)도 품목 · 제조사로 만든다. 상태는 품목 `state` · 제품 `license_status` 에 남는다

### 3.3 시맨틱 — 엣지 v2

#### 3.3.1 엣지 메타(DEC-001 D-04)

v1 공통 필드를 그대로 쓴다. 주장에 칸을 더한다.

| 주장 칸 | 뜻 |
|---|---|
| `gate_status` | §3.2.2 — 주장마다 |
| `lowering` | `direct`(원천이 이 양 끝을 그대로 가리킴) · `item`(원장 항목 → 행선지 단위 시술) · `modality_site`(시술군 코드 → 계열 × 고민 부위) · `modality`(시술군 코드 → 계열) |
| `conditions.from_modality` · `site_match` · `from_item` | 내림에 쓴 값 |

엣지 단위 게이트 상태는 저장하지 않는다. 조회 때 남은 주장 중 가장 약한 값을 계산한다. 테이블 변경은 없다.

#### 3.3.2 이름 해석 — 후보 전부, 임의 선택 없음(W-2)

1. 사전 순서: `unit_procedure`(이름 + `ledger_item` · `market` 동의어) → `family`(이름 + 동의어) → `product`(이름 + 동의어) → 원장 항목 이름(`ledger_map[].name` → 행선지 `unit_procedure` 의 id 들 · `family` 의 계열 · `product`/`device` 의 제품)
2. 앞 단계에서 맞으면 뒤는 보지 않는다
3. **한 단계에서 후보가 둘 이상이면 고르지 않는다** → 결과 「모호(후보 목록)」 + `ambiguous_name_ref`(warning, `detail.candidates`). 원장 항목 하나가 단위 시술 여럿으로 가는 경우도 모호다. v1 의 「`node_id` 사전순 첫째」 · 「원천 시술군 우선」 동점 규칙은 **없앤다**
4. 못 풀면 `unresolved_name_ref`(v1 원천별 키)

#### 3.3.3 내림 규칙

**A. 고민 항목의 부위(`concern_item.site_ids`) — 임시(OQ-G01)**

1. 고민 항목 이름(치환 뒤)을 `/` · `,` · `·` · 공백으로 토막 낸다
2. 토막의 정규화값이 부위 `name` 의 정규화값과 같으면 그 부위다
3. 아니면 토막이 부위 `name` 으로 시작하고 남은 꼬리가 고민 대분류 이름(치환 뒤 · 정규화)과 같으면 그 부위다. 가장 긴 부위 이름을 쓴다
4. 같은 이름의 묶음 · 하위가 둘 다 맞으면 **하위**다
5. 못 찾으면 `site_ids=[]` + `concern_site_unmapped`(warning)

실물 P3: 「볼처짐/불독살」 → 볼(하위) · 「눈꺼풀처짐」 → 눈꺼풀 · 「팔뚝/복부/허벅지」 → 셋 · 「턱선무너짐」 → 못 찾음(꼬리 「무너짐」 이 대분류가 아니다) · 「이중턱」 → 못 찾음(부위 동의어 칸이 없다).

**B. 고민 → 단위 시술(`treats`)**

| 원천 | from | 내림 |
|---|---|---|
| ① `taxonomy` `modality_ref[]` | `concern_item` | 코드 M → `family:M`. 고민 항목에 부위가 있으면 그 계열의 단위 시술 가운데 **부위가 맞는 것 전부**로(`modality_site` · `unconfirmed`). 부위가 없거나 맞는 단위 시술이 0 이면 계열로(`modality` · `auto`) + `treats_not_lowered`(`concern_without_site` · `no_unit_at_site`) |
| ② `problem-combos` | `concern` | 계열로(`modality` · `auto`) |
| ③ `problem-packages` CC `procedures[].category` | `concern_item`(v1 CC 매칭 · 치환 뒤) | ① 과 같음. evidence = `name` · `role` · `products` |
| ④ `treatment-optimization` `optimal_combo[]` | `opt_concern` | §3.3.2: 단위 시술 하나 → 그것(`direct` · 원장 항목 경유면 `item`) · 계열 → 계열(`direct`) · 제품 → `family_ids` 가 하나면 그 계열(`modality`) · **모호 · 못 풂 → 엣지 없음** |
| ⑤ 단위 시술 `purposes[]` | `purpose` | 그 단위 시술로(`direct`) · 상태 = 단위 시술의 상태 |

**부위 일치(OQ-G02 — 임시)**: 고민 부위 s 와 단위 시술 부위 u 가 `exact`(u = s) · `ancestor`(u 가 s 의 조상) · `whole_area`(u 가 「얼굴 전체」 이고 s 가 「얼굴」 아래이거나, u 가 「전신」 이고 s 가 「바디」 아래) 가운데 하나면 맞는다. 원천이 다르면 엣지가 다르다(원천 키 = 엔드포인트 — v1 그대로).

**C. 시술 ↔ 시술(`procedure_relation`) — 오늘은 계열 단위만**

| 원천 | 끝 |
|---|---|
| `contraindications` `rules[]` | `family:<from>` ↔ `family:<to>`. `first` 는 v1 규칙으로 찾은 쪽 계열 |
| `treatment-sequence` `sequence_order[]` | v1 규칙 그대로(이미 생긴 계열 쌍에만) |
| `synergy` `links[]` | **원천 시술군 코드**(`from_category` · `to_category`)의 계열. 이름은 evidence 로만 둔다 |
| `treatment-sequence` `minimum_intervals[]` · `incompatible_same_day[]` | 이름을 §3.3.2 로 풀어 단위 시술 하나 → 그 계열 · 계열 → 그 계열 · `family_ids` 하나짜리 제품 → 그 계열. 모호 · 못 풂이면 엣지 없음(v1 과 같음) |

- 모든 주장의 `lowering=modality` · `gate_status=auto`. 자기 쌍은 버린다(`self_relation_skipped`). `first` 가 갈리면 `conflict` 다 — v1 그대로
- 단위 시술은 계열 엣지를 **조회 때 상속**한다(§4 Safety). 펼쳐 저장하지 않는다

**D. 그 밖의 엣지**

- `has_complication`: v1 `complications.categories[].id`(코드) → `family:<코드>`
- `site_caution`: 위험 부위 `botox_specific` → `family:M1` · `filler_specific` → `family:M2`(부위는 §3.2.5)
- `has_product`: 제품 `family_ids` 원소마다 계열 → 제품. 상태 = 제품의 상태
- `uses_product`: 단위 시술 `devices[]`(= `product_item_ids`, 원장 항목 id) → 그 제품 노드(실물 21 링크, 전부 장비). 약제 · 필러는 단위 시술에 id 로 이어지지 않는다 — 그 길은 `has_product` 가 맡는다. 상태 = 두 끝 중 약한 값

#### 3.3.4 엣지 타입 16

| 타입 | from → to | 원천 |
|---|---|---|
| `has_child` | 고민 트리 · 부위 트리 | taxonomy · `site_tree[].parent` |
| `has_unit` | `family` → `unit_procedure` | `unit_procedures[].family` |
| `at_site` | `unit_procedure` → `site` | §3.1.2 부위 표 |
| `uses_technique` | `unit_procedure` → `technique` | `technique` 이름 → `techniques[].name` 완전 일치(없으면 `dangling_reference`) |
| `uses_product` | `unit_procedure` → `product` | §3.3.3 D |
| `includes` | `package` → `unit_procedure` | 행선지 `components[].unit_procedure_ids` |
| `treats` | `concern` · `concern_item` · `opt_concern` · `purpose` → `unit_procedure` · `family` | §3.3.3 B |
| `procedure_relation` | `family` ↔ `family`(오늘) | §3.3.3 C |
| `has_complication` | `family` → `complication` | §3.3.3 D |
| `site_caution` | `site` → `family` | §3.3.3 D |
| `has_product` | `family` → `product` | §3.3.3 D |
| `has_item` | `product` → `product_item` | 제품 게이트 `license_keys` |
| `licensed_to` · `manufactured_by` | `product_item` → `manufacturer` | §3.2.6 |
| `has_spec` | `product_item`(①) · `product`(②) → `spec` | `specs[]` |
| `synonym` | `opt_concern` · `synergy_target` · `purpose` ↔ 고민 트리 | v1 규칙(정규화 완전 일치) |

없어지는 v1 타입은 `has_procedure` · v1 `has_product` · 제품 ↔ 제품 `synonym` 이다.

### 3.4 검증 v2 · 발행

발행 정책 · 발행본은 SPEC-001 §3.4 그대로다. `bronze_hashes` 키는 필수 원천 14 개다. 발행본 `counts` 에 `"schema": "v2"` 를 싣는다. 이것은 구분 표기일 뿐이고 「같은 입력」 판정에는 넣지 않는다 — 키 집합이 v1(10)과 달라서 겹치지 않는다(W-9).

| 코드 | 등급 | 무엇 |
|---|---|---|
| `missing_bronze` · `parse_error` · `duplicate_node_id` | error | v1 그대로(대상 14) |
| `curation_shape_error` | error | §3.1.2 · §3.1.3 의 **필수 칸** 없음 |
| `dangling_reference` | warning | 큐레이션 안 참조 대상 없음(단위 시술의 계열 · 트리 부위 · 기법, 부위 부모, 행선지 id, 패키지 구성). 노드 · 엣지를 만들지 않고 센다 |
| `unit_without_site` · `site_out_of_tree` · `unknown_site_status` | warning | §3.1.2 부위 표 |
| `ledger_destination_skipped` | warning | §3.1.2 행선지 표(type 별) |
| `unknown_approval_value` · `unknown_gate_value` | warning | 모르는 상태값 → `unconfirmed` |
| `license_key_not_in_candidates` | warning | §3.2.6 |
| `provisional_node` | warning | `unconfirmed` 노드(`subject_kind` = 타입) |
| `product_license_unconfirmed` · `product_cancelled` | warning | 제품 `license_status` 별 |
| `concern_site_unmapped` · `treats_not_lowered` · `ambiguous_name_ref` | warning | §3.3.3 A · B · §3.3.2 |
| `danger_zone_unmapped` · `source_fix_applied` | warning | §3.2.5 · §3.2.3 |
| `unresolved_name_ref` · `self_relation_skipped` · `source_conflict` · `combo_not_in_procedures` · `ambiguous_cc_match` · `unlinked_vocabulary` · `orphan_node` | warning | v1 그대로(타입 이름만 v2) |
| `coverage_gap` | warning | v1 하위 종류의 **이름만** 바꾼다: `procedure_group_*` → `family_*` · `procedure_without_concern` → `unit_without_concern`. 종류 재정의는 2차 |

실물 입력(17:00)에는 error 를 낼 칸이 없다. WORK-002 Phase 0 이 이를 확인한다.

## 4. Interface Contract

경로 · 파라미터 · 응답 최상위 · 에러 · MCP 전송/마운트는 SPEC-001 §4 · §5.1 그대로다. tool 수도 그대로다(REST 7 · MCP 6).

### 4.1 게이트 거르기 — `include_unconfirmed`(W-1 · 코디 기본값)

근거: `_RESUME` §2 「승인된 것만 다음 단계, 미결은 진행 안 함」 · DEC-003 D-03. 그래프에는 다 싣고, 골드 응답에서 거른다.

| 파라미터 | tool | 기본 |
|---|---|---|
| `include_unconfirmed: bool` | search · get_node · neighbors · subgraph · list_nodes(REST 쿼리 · MCP 입력 같은 이름) | `false` |

`false`(기본)일 때:

- `gate_status=unconfirmed` 노드는 응답에 나오지 않는다(검색 후보 · 목록 · 이웃 · 부분 그래프). 부분 그래프는 그 노드를 지나 펼치지도 않는다
- 엣지는 `unconfirmed` 주장을 뺀 주장만 싣는다. 남은 주장이 0 이거나 한쪽 끝 노드가 빠지면 엣지도 뺀다
- `get_node` 로 `unconfirmed` 노드를 직접 부르면 404 `{"detail": "node is unconfirmed: <id> — include_unconfirmed=true"}`
- `safety` 의 **안전 주장(금기 · 간격 · 같은 날 불가 · 부작용 · 위험 부위)은 거르지 않는다.** 안전 정보가 빠져 「안전」 으로 읽히는 것을 막기 위해서다(DEC-001 D-06). 오늘 안전 주장은 전부 stg 원천이라 `auto` 이고, 이 예외는 앞으로 생길 경우를 위한 것이다
- 응답 최상위에 `gate_filter: "approved_auto"` 를 싣는다(`true` 이면 `"all"`)

`schema` · `validation` 은 거르지 않는다. 스키마의 타입별 `count` 와 함께 `count_by_gate{approved, auto, unconfirmed}` 를 낸다.

### 4.2 그 밖의 변경

| 무엇 | v2 |
|---|---|
| 타입 허용값 | §3.2.4 16 · §3.3.4 16. v1 이름이면 422 |
| `Edge` | + `gate_status`(남은 주장 중 가장 약한 값 — 조회 때 계산) |
| `Claim` | + `gate_status` · `lowering` |
| `safety` | `family` · `unit_procedure` 노드마다 |
| 검색 | synonym 열 = `synonyms` · `names.en` · `names.official`. 점수표는 v1 그대로다. 정렬 = 점수 → 타입 순서 → `node_id`. **같은 점수의 후보는 전부 낸다**(`limit` 안에서) |
| 목록 항목 | + `gate_status` |

**Safety v2**

```text
Safety = {
  for_node, inherited_from?,                       # unit_procedure 면 그 계열
  procedure_relations[Edge],                       # 자기 + 계열의 procedure_relation 중 안전 주장(contraindications · minimum_intervals · incompatible_same_day)이 있는 것
  complications[ {node_id, name, severity, incidence} ],
  patient_contraindications{ absolute[], relative[] },
  site_cautions[ {site_id, zone_id, family_id, claim} ],   # unit_procedure — 그 부위와 조상 부위의 site_caution 중 계열이 같은 것
  gaps[str]   # "no_contraindication_rule" · "no_complication" · "no_site_caution_source" · "no_modality_source"(X 계열)
}
```

응답 크기 규칙은 v1 의 「시술군 / 시술 항목」 을 「계열 / 단위 시술」 로 바꿔 그대로 쓴다. `site_cautions` 는 단위 시술 키에 싣는다.

**MCP tool 설명 — 더하는 문장**

| tool | 문장 |
|---|---|
| `graph_schema` | 「시술의 최소 단위는 unit_procedure(계열 × 부위 × 기법)다. family 는 약제 · 장비 종류, product 는 브랜드, product_item 은 식약처 허가 품목이다. gate_status: approved(사람 승인) · auto(원천 그대로 · 자동 확정) · unconfirmed(미확인 · 원천 근거만 · 임시값). 기본 응답은 approved · auto 만 낸다.」 |
| `graph_search` | 「동의어(구어 · 원장 이름 · 장비 이름 · 원천 표기)까지 본다. 같은 점수의 후보는 전부 낸다 — 『보톡스』 처럼 계열과 제품이 함께 나오면 고르거나 되묻는다. 결과가 비면 include_unconfirmed=true 로 미확인 후보를 볼 수 있으나 확정 정보로 쓰지 않는다.」 |
| `graph_get_node` | 「product.license_status 가 licensed 가 아니면 추천 대상으로 쓰지 않는다. unit_procedure 의 safety 는 계열에서 상속한 것과 부위 주의를 합친 것이다.」 |
| `graph_neighbors` · `graph_subgraph` | 「claims[].lowering 이 modality · modality_site 인 주장은 원천이 시술군 단위였던 것을 규칙으로 내린 것이다.」 |

## 5. Implementation Rules

### 5.1 v1 과의 관계 — 교체 · 마이그레이션 없음

같은 테이블 · 같은 앱 · 같은 tool 경로에서 v1 을 v2 로 **교체**한다. 근거:

- DEC-002 D-08 이 v1 노드 단위를 대체했다
- 로컬 전용이라 소비자가 없다
- 병행하면 같은 검색어에 v1 · v2 후보가 섞인다
- `graph_node.type` · `graph_edge.type` · 속성 · 주장 · 브론즈 `endpoint`(64자)가 이미 일반형이라 스키마 변경이 필요 없다
- 발행본 번호가 이어지므로 v1 결과도 `graph_version` 으로 거슬러 볼 수 있다

변경 범위와 되돌리기:

- alembic revision 0 · `app/model/graph.py` 변경 0
- 되돌리기: WORK-002 Phase 0 체크포인트로 코드를 되돌리고 `graph_build --force`. DB 는 지우지 않는다
- v1 단언 테스트는 v2 로 고친다(`tests/graph_support.py` fixture 포함 — W-8)

### 5.2 모듈 위치

SPEC-001 §5.2 그대로다. 더하는 파일은 둘이다: `app/modules/graph/curation.py`(§3.1 어댑터 · 치환표 · 노드 · 제조사) · `app/modules/graph/lowering.py`(§3.3.3).
CLI 는 `scripts/graph_ingest.py --curation-dir <$W>` 이다. E2E 는 `scripts/graph_e2e_check.py` 를 v2 로 바꾼다. graph 밖은 건드리지 않는다.

### 5.3 결정론 · 멱등

SPEC-001 §5.3 그대로다. 입력 파일이 바뀌면(제품 원장 갱신 · 게이트 답 추가) 다시 적재 → 다시 빌드 → 새 발행본이다. 코드는 바꾸지 않는다.

## 6. Verification

발화 → 검색어는 외부 판단기가 맡는다(DEC-001 D-08). 기대값은 실물 입력(17:00) 기준이다.

#### E-1. 「처짐이 고민이에요」

1. `GET /graph/search?q=처짐` → 1위 `concern:P3` 「처짐」(`exact` 1.0). 함께: `concern_subcategory` P3-1 「얼굴 처짐」 · P3-2 「눈가 처짐」 · P3-3 「바디 처짐」 · `concern_item` 「볼처짐/불독살」 · 「눈꺼풀처짐」(`contains` 0.5) · `opt_concern` 「처짐/탄력」(`prefix` 0.7). `q=쳐짐` 도 `concern:P3` 를 `synonym` `exact` 0.9 로 낸다
2. `GET /graph/subgraph?start=concern:P3&hops=3&edge_types=has_child,treats`(기본 — 승인 · 자동만)
   - 고민 항목 5 + `treats` 는 **계열만**: `family:M9` · `M7` · `M14` · `M10` · `M4`(① · ③ 에서 계열로 남은 주장)
   - 단위 시술은 나오지 않는다. 부위로 내린 주장이 `unconfirmed` 이고(OQ-G01 · G02), M9 · M7 단위 시술도 전부 `source_only` 이기 때문이다
3. 같은 요청 + `&include_unconfirmed=true`
   - 「볼처짐/불독살」 → `UP-M9-018` 볼 HIFU · `UP-M9-027` 볼 고주파 · `UP-M7-009` 볼 실리프팅(`exact`) + M9 · M7 의 「얼굴 전체」 단위 시술(예 `UP-M9-002` · `UP-M9-004` · `UP-M9-006` — `whole_area`)
   - 「눈꺼풀처짐」 → `UP-M9-038` · `UP-M7-014`(`exact`) + 얼굴 전체 단위 시술
   - 「팔뚝/복부/허벅지」 → M9 · M10 의 팔뚝 · 복부 · 허벅지 · 전신 단위 시술(예 `UP-M9-012` · `UP-M9-023` · `UP-M9-026` · `UP-M9-032`)
   - 「턱선무너짐」 · 「이중턱」 → 계열로만(`treats_not_lowered` `concern_without_site`)
   - 없어야 함: 「볼처짐」 에서 나온 턱선 · 바디 단위 시술
4. `GET /graph/subgraph?start=concern:P3&hops=1&edge_types=treats` → `problem-combos` ② 계열 `M9` · `M1` · `M2` · `M4`

#### E-2. 「턱쪽에 필러」

1. `GET /graph/search?q=턱` → `site:턱(묶음)`(name 「턱」, `exact` 1.0) + 「턱끝」 · 「턱선」 · 「턱밑」(`prefix`) · 「사각턱」(`contains`) · 고민 트리 항목
2. `GET /graph/search?q=필러` → `family:M2` 「필러」(`exact` 1.0)
3. `GET /graph/nodes/site:턱(묶음)/neighbors?edge_types=has_child&direction=out` → 턱끝 · 턱선 · 사각턱 · 턱밑
4. `GET /graph/subgraph?start=site:턱끝&start=site:턱선&start=site:사각턱&start=site:턱밑&hops=1&edge_types=at_site&direction=in&include_unconfirmed=true` → `family_id=family:M2` 인 것: **`UP-M2-004` 턱끝 필러 · `UP-M2-011` 턱선 필러**. 없어야 함: 사각턱 필러(실물에 없다 — DEC-002 D-06)
5. 같은 요청을 기본값으로 보내면 M2 단위 시술은 나오지 않는다(둘 다 `source_only`) — **정상이다.** `UP-M1-006` 사각턱 보톡스(`approved`)는 나온다
6. `GET /graph/nodes/unit:UP-M2-004?include_unconfirmed=true` → `safety.site_cautions` 에 `chin`(턱 묶음 — 조상) `filler_specific` · `inherited_from=family:M2`

#### E-3. 「포텐자 하고 싶어요」 — 오늘은 미확인 갈래

1. `GET /graph/search?q=포텐자` → 기본값에서는 **후보 0**. `product:포텐자` 는 제품 게이트 `pending`, `UP-M11-001` 은 `source_only` 로 둘 다 `unconfirmed` 다
2. `…&include_unconfirmed=true` → `product:포텐자`(`device` · name `exact` 1.0) · `unit:UP-M11-001` 「얼굴 전체 니들RF」(동의어 `exact` 0.9)
3. `GET /graph/nodes/unit:UP-M11-001/neighbors?edge_types=uses_product,has_unit,at_site&include_unconfirmed=true` → `uses_product` → `product:포텐자` 와 `auto-M11-1775364775143` 의 제품 · `has_unit` ← `family:M11` · `at_site` → `site:얼굴 전체`
4. `GET /graph/nodes/product:포텐자?include_unconfirmed=true` → `license_status=unconfirmed` · `has_item` 0(답 전에는 허가를 단정하지 않는다)
5. **허가 갈래는 제품 게이트 `auto` 인 보톡스 · 쥬비덤으로 확인한다**: `product:보톡스` → `licensed` · `has_item` → 품목 하나(`drug:200901660` · `drug:200804190`) → `licensed_to` 한국애브비(주) / `product:쥬비덤` → 품목 여럿(모델명별) → `licensed_to` 한국애브비(주) · `manufactured_by` Allergan

#### E-4. 「보톡스랑 필러 같이」

1. `GET /graph/search?q=보톡스` → `product:보톡스`(`exact` 1.0)와 `family:M1` 「보툴리눔 톡신」(동의어 `exact` 0.9) **둘 다**(`_RESUME` 「『보톡스』 검색은 계열 · 제품 둘 다」) + 이름에 「보톡스」 가 든 승인 단위 시술(`contains`)
2. `GET /graph/nodes/family:M1/neighbors?edge_types=procedure_relation` → `family:M1` ↔ `family:M2` 엣지 **하나**. 주장: `contraindications`(`strength=safe` · 「같은 날 가능」 · `first=family:M1` · evidence 「동일 부위는 보톡스 먼저 → 필러 …」) · `treatment-sequence` `sequence_order`(`first=family:M2`) · `synergy` 「함께」(전부 계열). `review_status=conflict` · `gate_status=auto`
3. `GET /graph/nodes/unit:UP-M1-006`(`approved`) → `safety.inherited_from=family:M1` · `procedure_relations` 에 위 엣지
4. `GET /graph/validation?code=source_conflict` 에 이 엣지가 있다
5. MCP `graph_search` · `graph_get_node` 로 1 · 3 을 다시 부르면 REST 와 같은 JSON 이다

#### E-5. 검증 · 멱등 · 스키마

1. `GET /graph/validation?limit=0` → `error` 0. 노드 타입별 · 게이트별 수가 Phase 0 기대값과 같다
2. `graph_ingest --curation-dir $W` 를 다시 → 7행 모두 `unchanged` · `graph_build` 다시 → `unchanged`
3. `GET /graph/schema` → `counts.schema="v2"` · 노드 16 · 엣지 16 · `count_by_gate`

### 6.1 기대값(W-5 — 축소)

WORK-002 Phase 0 이 빌드 코드를 import 하지 않고 입력 파일만 읽는다. 그리고 **노드 타입별 수 · 게이트 상태별 수**와 E-1~E-4 의 「있어야 함 / 없어야 함」 id 를 `tests/fixtures/graph_v2/expected.json` 에 쓴다. 엣지 · 이슈 수의 독립 재계산은 2차다.

### 6.2 Acceptance Criteria

- [ ] E-1~E-4 가 Swagger 에서, E-5 가 CLI 에서 재현된다. E-4 는 MCP 로도 같다
- [ ] 기본 응답에 `unconfirmed` 노드 · 주장이 0 이다(안전 주장 예외 제외). `include_unconfirmed=true` 에서는 전부 나온다
- [ ] 모든 노드에 `gate_status`, 모든 주장에 `gate_status` · `lowering` 이 있다
- [ ] 이름 해석 · 검색에 동점을 임의로 고르는 경로가 없다(테스트)
- [ ] 같은 브론즈로 두 번 빌드하면 id 집합 · 이슈 수가 같다
- [ ] alembic 0 · graph 밖 변경 0 · 경계 테스트 통과 · 모델 호출 0 · v1 발행본 보존

## 7. Open Questions

DEC 에 없는 정책이다. 오늘은 임시값으로 진행한다. Owner 는 사용자다.

| ID | 질문 | 임시값 | 영향 |
|---|---|---|---|
| OQ-G01 | 고민 항목 → 부위를 이름 규칙으로 뽑을까, 큐레이션 표로 받을까 | 이름 규칙(§3.3.3 A) · 결과 `unconfirmed` | E-1 |
| OQ-G02 | 부위 일치 범위(조상 · 얼굴 전체 · 전신 포함?) | 셋 다 · 종류 표시 | E-1 |
| OQ-G03 | 부위 없는 고민을 계열에 둘까, 계열의 단위 시술 전부로 펼칠까 | 계열 | §3.3.3 B |
| OQ-G04 | X1~X6 계열의 안전 원천 — 원래 시술군(M16 · M10 등)의 금기 · 부작용을 빌려 줄까 | 빌려 주지 않음 · `gaps: no_modality_source` | §4 Safety |
| OQ-G05 | 원장 항목 하나 → 단위 시술 여럿일 때 시너지 · 간격 주장을 각각 붙일까(2차의 단위 시술 해석 전제) | 오늘은 계열 단위라 해당 없음 | §8 |
| OQ-G06 | ~~골드에서 `unconfirmed` 를 뺄까~~ → **2026-10-27 코디 기본값**: 기본 응답 = 승인 · 자동만, `include_unconfirmed=true` 일 때 전부(§4.1). 사용자 확인 대기 | — | §4.1 |
| OQ-G07 | `source_only` 단위 시술 123(E-2 · E-3 의 단위 시술 전부)을 언제 게이트에 올리나 | 그래프엔 싣고 기본 응답에선 뺀다 | E-2 · E-3 |
| OQ-G08 | 같은 브랜드의 원장 여러 곳을 제품 노드 하나로 | 정규화 브랜드명이 같으면 하나 | §3.2.4 |
| OQ-G09 | 원천 수정 A1 밖의 `fix` 도 치환할까 | A1 만 | §3.2.3 |
| OQ-G10 | 위험 부위 「확인 필요」 5 의 대응 | 묶음 | §3.2.5 |
| OQ-G11 | 현장 신규 기기 35 | 보관만 | — |
| OQ-G12 | 제품 게이트 유효 상태 | 내려받은 `status` 그대로(게이트 페이지가 합친 값) | §3.1.3 |
| OQ-G13 | v1 테스트 · E2E | v2 로 고치고, v1 은 체크포인트 · 발행본으로 남김 | §5.1 |
| OQ-G14 | 식약처 API 직접 적재 | 미룬다 | — |
| OQ-G15 | 시술 1회 · 가격 노드 | 규격까지만 | — |
| OQ-G16 | 제조사 정규화에 법인 표기 제거를 넣을까 · 의약품 실제 제조원(`consign_manufacturer`)을 노드로 세울까 | 넣지 않음 · 속성으로만 | §3.2.6 |

DEC · SPEC-001 에서 넘어와 그대로 둔 것: OQ-S01 · S03 · S04 · S05 · S06(E-4 conflict 원인) · DEC-001 OQ-111 · OQ-119.

## 8. 2차 — 오늘 범위에서 뺀 것

| 무엇 | 왜 | 다시 할 때 필요한 것 |
|---|---|---|
| `procedure_relation` 이름 끝점의 **단위 시술 해석** | 공유 동의어 40(W-2). 오늘은 계열만 | §3.3.2 「모호 → 후보 전부」 위에서 OQ-G05 결정 |
| `treats` ④ 의 **제품 → 그 장비를 쓰는 단위 시술** 갈래 | 같은 이유. 오늘은 제품 → 계열 | 위와 같음 |
| 규격 ②(품목 허가 `PACK_UNIT` 별도 파싱) | `specs[]` `mfds-license` 32 와 겹침(W-6) — **없앤다** | — |
| 기대값의 엣지 · 이슈 수 독립 재계산 | 사실상 두 번째 구현(W-5) | 오늘 E2E 통과 뒤 |
| 제품 원장 `manufacturers[]` 병합(국가 · 역할 · 원천 표기) · 의약품 위탁 제조원 노드 | 조인 키가 없다(F-3) | `manufacturers[].sources` 의 허가 key 로 잇는 규칙 · OQ-G16 |
| 부위 노드 `danger_level` | 오늘 E2E 에 쓰지 않음 | — |
| `coverage_gap` 하위 종류 재정의 | 오늘은 이름만 바꿈 | — |
| 현장 신규 기기 · 시술 1회 · 가격 · 식약처 API 직접 적재 | OQ-G11 · G15 · G14 | — |

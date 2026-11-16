# Procedure Hub 데이터 구조 조사 — 「○○가 고민이에요」 추천에 쓸 수 있나

> 작성: researcher 워커 · 2026-10-26
> 원천: 코드 `PROCEDURE-HUB` `release/v1.2.0` @ `5b9af03`(read-only) · 기획 `mediness-mediness` `origin/main:products/procedure-hub/`(v1.1.0) · stg API `https://api-stg-csp.medisolveai.com/procedure-hub/api/v1/*`(GET 만, 2026-10-26 19:42 KST 수집)
> 이 리포트는 설계안을 내지 않는다. 결정거리는 Q7 에 질문으로만 모았다.

## 요약 (사용자 판단 대조)

1. **「매핑이 빠진 곳이 많다」 → 맞다.** 고민 항목 117개 중 26개(22%)는 시술 연결이 비어 있고, 14개 고민 중 6개(P6·P8·P10·P12·P13·P14)는 고민별 조합(problem-combos)이 아예 없다. 시술 세부 항목 521개로 가는 연결은 0개다. 조합 원장 문자열은 optimization 48/74 · synergy 끝점 67/230 이 어떤 엔티티와도 맞지 않는다.
2. **「그래프 구조가 아니다」 → 부분적으로 맞다.** FK 엣지는 있다(고민 항목→시술군, CC→시술군, 시술군↔시술군 금기·시너지). 하지만 엣지가 47개 JSON 파일 경계를 따라 섬처럼 끊겨 있다. 고민 어휘가 최소 5벌 따로 있고 서로 이어지지 않는다. 모든 FK 가 17개짜리 최상위 시술군(M1~M17)에서 끝난다. 엣지에는 가중치·출처가 없다.
3. **「고민에서 시술로 타고 갈 수 없다」 → 부분적으로 맞다.** 고민 어휘에 정확히 있는 단어(「모공」=P7 · 「기미」=P5-1)는 FK 3홉으로 **시술군**까지 간다. 하지만 도착점이 「레이저(M8)」처럼 하위 항목 100개 이상을 품은 덩어리라 「어떤 시술」은 안 나온다. 표기만 다른 단어는 첫 홉에서 끊긴다(「처짐」 0건 ↔ 데이터는 「쳐짐」).
4. **고민→시술 근거가 구조로 없다.** 「왜 이 시술인가」는 자유 텍스트(`clinical_rationale`·`reason`·`evidence`)뿐이다. 문헌(`knowledge_claim_citation`)은 시술에만 붙고 「고민–시술」 관계에는 붙지 않는다.
5. **새 canonical 계층도 지금은 답이 아니다.** `catalog_concern → recommendation_package → catalog_procedure_concept` FK 경로가 스키마에는 있다. 하지만 이 경로를 읽는 `recommendations()` 는 어디서도 호출되지 않는다(`persistence.py:489`). 공개 API 는 레거시 테이블만 서빙한다. canonical 검색(`/knowledge/retrieve`)은 게시 release 가 없으면 `unavailable` 이다(release 발행은 의사 검수 대기).

---

## Q1. 데이터 지도

**답.** 테이블은 **166개**다. 모델 `__tablename__` 166개와 단일 baseline 마이그레이션 `b202609030001_initial_schema.py` 의 `op.create_table` 166개가 **diff 0** 으로 일치한다. 계층은 둘이다.

- **레거시 계층(약 120개)** — JSON 파일 1개 = 도메인 1개 = 테이블 묶음 1개. 지금 GET API 는 전부 여기서 서빙한다.
- **canonical 계층(46개)** — `catalog_*` · `knowledge_*` · `recommendation_*` · `safety_*` · `guidance_*` · `publication_*`. 서빙하는 곳은 `POST /knowledge/retrieve` 하나다. 그마저 게시 release 가 있어야 동작한다.

근거: `backend/app/model/*.py`(31파일) · `backend/alembic/versions/b202609030001_initial_schema.py`(2206줄, 유일한 마이그레이션). 셈은 `grep -oE "op.create_table\('[a-z_0-9]+'"` 와 `grep __tablename__` 결과의 `diff`(차이 0).

### 1-1. 레거시 계층 (모델 파일 → 테이블 → 담는 것)

| 모델 파일 | 테이블 | 담는 것 |
|---|---|---|
| `taxonomy.py` | `modality` | 시술군 17개(M1~M17). 개요·기전·지속기간 |
| | `modality_subcategory` | 시술군 하위 분류 74개(수입/국산/용도별/HIFU 등) |
| | `modality_item` | 실제 시술·브랜드 항목 521개. `extra_json` 텍스트 |
| | `modality_product` | taxonomy 안의 제품 59개(제조사·국가·식약처) |
| | `modality_indication` · `modality_item_indication` · `modality_product_indication` | 적응증 **문장**(primary/secondary/extended) |
| | `modality_safety` · `modality_item_safety` · `modality_product_safety` | 부작용 **문장**(severity 라벨) |
| | `modality_aftercare` · `modality_item_aftercare` · `modality_product_aftercare` | 사후관리 문장 |
| | `modality_contraindication` | 환자 금기 문장(absolute/relative) |
| | `modality_related_technique` | 관련 기법 문장 |
| | `problem` | 고민 분류 14개(P1~P14) |
| | `problem_subcategory` | 고민 하위 53개(「기미」·「얼굴 쳐짐」·「코」) |
| | `problem_item` | 고민 항목 117개. 이름 대부분이 **시술명**(「레이저토닝」·「코필러」) |
| | `problem_item_modality_ref` | 고민 항목 → 시술군 조인 |
| | `modality_i18n` · `modality_item_i18n` · `modality_product_i18n` · `problem_i18n` · `subcategory_label_i18n` | 이름 번역 |
| `problem_combos.py` | `problem_combo` | 고민별 tier 패키지 묶음(8개 고민만) |
| | `problem_package` | 패키지 24개. 가격대·영업 멘트·임상 근거 **텍스트** |
| | `problem_package_procedure` | 패키지 → `procedure_profile.id`(=M 코드) |
| | `problem_package_product` | 패키지 제품 **자유 텍스트** |
| | `problem_combo_i18n` · `problem_package_i18n` · `problem_combos_meta` | 번역·메타 |
| `problem_packages.py` | `problem_complaint` | CC(주소) 115개. `cc`=고민 항목명 |
| | `complaint_procedure` | CC별 권장 시술: `name` 텍스트 + `category`→modality FK |
| | `complaint_procedure_product` | 권장 제품 **자유 텍스트** |
| | `complaint_combo` · `complaint_combo_item` | CC별 조합. 구성은 `procedure_name` **텍스트** |
| | `complaint_alternative` | 대안 **자유 텍스트** |
| | `problem_packages_meta` | 메타 |
| `procedure_profiles.py` | `procedure_profile` (+`_mechanism` · `_practical_note` · `_aftercare` · `_meta`) | 시술군 17개의 운영 속성(열부하·출혈·마취·소요시간) |
| `combo_recipes.py` | `combo_recipe` · `combo_recipe_procedure` · `combo_recipe_follow_up` · `combo_recipe_i18n` · `combo_recipe_meta` | 목적별 조합 프리셋 7개(goal=lifting 등) |
| `synergy.py` | `synergy_link` · `synergy_link_i18n` · `synergy_meta` | 시술 간 시너지 115개(함께/다음에/대신, `target` 텍스트) |
| `contraindications.py` | `contraindication_rule` · `contraindications_meta` | 시술군 쌍 금기·간격 27개 |
| `complications.py` | `complication` · `complication_risk_factor` · `complication_severity_level` | 시술군별 합병증 65개 |
| `treatment_optimization.py` | `optimization_meta` · `_principle` · `_concern` · `_severity_level` · `_severity_combo` · `_severity_contraindication` · `_severity_caveat` · `_age_group` · `_age_group_primary_concern` · `_age_group_base` · `_age_group_upgrade` · `_age_group_avoid` · `combination_rule` · `annual_plan` · `annual_plan_month_procedure` | 고민 8종×중증도 3단 최적 조합, 연령대별 추천, 연간 플랜 — **taxonomy FK 없음, 전부 텍스트** |
| `treatment_sequence.py` | `treatment_sequence_meta` · `_principle` · `_phase` · `_phase_category` · `incompatible_same_day_pair` · `_item` · `common_combo` · `common_combo_step` · `minimum_interval` | 같은 날 순서·불가 조합·최소 간격(텍스트) |
| `procedure_comparison.py` | `procedure_comparison` · `_evidence` · `_item` · `_meta` | 비교 9주제 39시술. `best_for` 텍스트 |
| `market_pricing.py` | `pricing_category` · `pricing_item` · `pricing_meta` | 시술군별 시장가 122행(부위·국산/수입이 이름 텍스트 안에) |
| `products.py` | `product_category` · `product_category_modality` · `product` · `product_meta` | 제품-제조사 사전(products.json) |
| `literature_evidence.py` | `literature_evidence_category` · `_item` · `_citation` · `_meta` | 시술군별 문헌 |
| `pih_risk.py` | `pih_risk_procedure` · `pih_risk_factor` · `pih_risk_meta` | 색소침착 위험 26행. `procedure_ref` 는 3레벨 혼재라 FK 없음 |
| `anatomy_danger_zones.py` | `anatomy_danger_zone` · `anatomy_zone_vessel` · `_nerve` · `_clinical_pearl` · `_botox_spec` · `_filler_spec` · `_meta` | 얼굴 위험 부위 11곳. 보톡스/필러 스펙만 modality FK |
| `patient_education.py` | `patient_education` · `patient_education_concern` · `_meta` | 환자 설명. `_concern` 은 **고민이 아니라 Q&A** |
| `post_procedure_timeline.py` | `post_procedure_timeline` · `post_procedure_phase` · `_phase_reaction` · `_meta` | 회복 타임라인 10개 |
| `pre_procedure_checklist.py` | `pre_procedure_universal_check` · `pre_procedure_category_check` · `_meta` | 시술 전 확인 |
| `consent_checklist.py` | `consent_checklist` · `consent_mandatory_disclosure` · `consent_contraindication` · `consent_emergency_sign` · `_meta` | 동의서 항목 |
| `glossary.py` · `glossary_version.py` | `translation_glossary` · `glossary_version` | 통역 용어집 |

### 1-2. canonical 계층

| 모델 파일 | 테이블 | 담는 것 |
|---|---|---|
| `canonical_catalog.py` | `catalog_procedure_concept` | 시술 개념 계층(modality/category/procedure/technique, `parent_id` 자기참조) |
| | `catalog_procedure_alias` | 시술 별칭 |
| | `catalog_product` · `catalog_product_alias` · `catalog_manufacturer` · `catalog_product_regulatory_status` | 제품 단일 원장 |
| | `catalog_procedure_product` | 시술↔제품 조인 |
| | `catalog_concern` | 고민(public_code P1~P14, `data-model.md:142`) |
| | `catalog_complaint` | 고민 하위 CC(`group_name`·`name_ko`) |
| `canonical_recommendation.py` | `recommendation_package` | 고민(+CC)별 패키지(tiered/complaint/optimization), 가격 정수 |
| | `recommendation_package_item` | 패키지→시술 개념 FK, role(primary/adjunct/alternative) |
| | `recommendation_package_narrative` | 패키지 설명(audience별) |
| | `recommendation_package_component` · `recommendation_component_procedure` | 레거시 「A + B」 묶음 표현 |
| | `recommendation_combination_recipe` · `_recipe_step` · `_recipe_follow_up` | 레시피 |
| | `recommendation_procedure_synergy` | 시술 개념 간 시너지 |
| `canonical_knowledge.py` | `knowledge_clinical_claim` | 시술 개념별 임상 주장(mechanism/effect/adverse_effect) |
| | `knowledge_claim_citation` · `knowledge_evidence_source` · `knowledge_claim_verification` · `knowledge_claim_narrative` | 문헌 인용·검증·설명 |
| | `knowledge_document` · `knowledge_document_claim` | audience별 문서 |
| `canonical_safety.py` | `safety_subject` · `safety_subject_procedure` · `safety_procedure_constraint` | 일반화 안전 규칙(ADR-0003) |
| `canonical_guidance.py` | `guidance_recovery_timeline` · `_phase` · `_reaction` · `guidance_complication` · `guidance_procedure_complication` · `_risk_factor` · `_protocol` | 회복·합병증 |
| `canonical_publication.py` | `publication_source_artifact` · `_import_job` · `_content_revision` · `_content_release` · `_release_revision` · `_audit_event` · `_import_mapping_issue` · `_validation_issue` | 원본 스냅샷·검수·발행 |
| `knowledge_search.py` | `knowledge_search_unit` | 게시 revision 을 잘게 쪼갠 검색 단위(trigram) |

### 1-3. 어느 쪽이 서빙되나 · 이관은 어디까지

- **데이터 GET API 23개(`router/data.py`) = 전부 레거시 테이블.** `router/data.py:62~429` 가 `app/service/*`(레거시 repository)와 `ClinicalReferenceReadService` 를 부른다. `ClinicalReferenceReadService` 도 레거시 테이블을 읽는다(`modules/reference_read/persistence.py:164~`). 예외는 `/extracted` · `/literature-evidence-integrity` · `/i18n/{lang}` 셋이다 — `publication_content_revision.snapshot` JSON 을 그대로 내보낸다(`persistence.py:103~148`).
- **canonical 을 읽는 공개 경로는 `POST /api/v1/knowledge/retrieve` 하나.** 그것도 `knowledge_search_unit` + catalog identity + safety + evidence 만 쓴다(`modules/retrieval/application.py:361~`).
- **추천 도메인은 정책 클래스만 있다.** `modules/recommendation/` 에는 `domain.py` 만 있고 application/repository 가 없다. `RecommendationEligibilityPolicy`(`domain.py:431`)를 쓰는 곳은 테스트(`tests/test_recommendation_domain.py`)뿐이다.
- **ADR-0002 상태**: 「Historical — 초기 전환 검증에만 적용」(`adr/0002…md:3`). 「신규 기능은 canonical DB만 사용하고 외부 API의 기존 응답 DTO만 보존한다」(같은 문서 :97). 「legacy cutover 보류」(`data-model.md` §13 Task 5). importer·seed 는 제거됐다. 새 환경은 PostgreSQL dump 를 수동 복원한다(`reviews/canonical-delivery.md:248,610`).
- **stg 의 canonical 적재·release 상태 → 확인 안 됨.** stg 는 GET 만 허용이라 canonical 을 읽는 유일한 경로(POST retrieve)를 부르지 않았다. 문서상으로는 「최초 release 전까지 `status=unavailable`」(`guides/deployment.md:281`), 「STG 최초 반영에서 … release를 publish하지 않는다」(`:270`), 「피부과 의사 claim 검수 대기」(`reviews/clinical-review.md:4`)다. `/extracted` 가 17개 시술군 응답을 준 것으로 보아 `publication_content_revision` 행은 stg 에 있다.

---

## Q2. 엔티티 연결

연결 종류: ① FK ② 조인 테이블 ③ JSON/배열 안의 id ④ JSON/텍스트 안의 이름 문자열(조인 불가) ⑤ 연결 없음

### 2-1. 레거시 계층 (지금 서빙되는 것)

| 연결 | 종류 | 근거 |
|---|---|---|
| 고민 P → 하위 → 항목 | ① | `taxonomy.py:333~352` |
| 고민 항목 → 시술군 M | ② `problem_item_modality_ref` | `taxonomy.py:361~371` |
| 고민 항목 → 시술 항목(`modality_item`) · 제품 | ⑤ | 해당 테이블 없음 |
| 고민 P → tier 패키지 → 시술군 | ① + ① `problem_package_procedure.procedure_id → procedure_profile.id`(값은 M 코드) | `problem_combos.py:18,36,78~80` |
| tier 패키지 → 제품 | ④ `product_description` 자유 텍스트 | `problem_combos.py:84~101` |
| 고민 P → CC | ① `problem_complaint.problem_id` | `problem_packages.py:26` |
| CC → 고민 항목(taxonomy) | ④ `cc` 문자열 = `problem_item.name` (stg 115/115 일치, FK 아님) | `problem_packages.py:29` |
| CC → 권장 시술 | ① `complaint_procedure.category → modality.id` + ④ `name` 텍스트 | `problem_packages.py:62~65` |
| CC → 권장 제품 | ④ `product_name` | `problem_packages.py:74~91` |
| CC 조합 → 시술 | ④ `procedure_name`(「느슨한 참조」 주석) | `problem_packages.py:120~136` |
| CC → 대안 | ④ 자유 문장 | `problem_packages.py:140~157` |
| optimization 고민 8종 → 시술 | ④ `procedure_text` (「taxonomy FK 없음」) | `treatment_optimization.py:10,46~101` |
| 연령대 → 고민 · 시술 | ④ | `treatment_optimization.py:147~` |
| 시술 ↔ 시술 시너지 | ① `from/to_modality_code → modality` + ④ `from/to_item_name` + ④ `target`(목표 효과 문자열) | `synergy.py:27~38` |
| 시술 ↔ 시술 금기·간격 | ① 양방향 modality FK. `interval` 텍스트 | `contraindications.py` `contraindication_rule` |
| 같은 날 불가·최소 간격 | ④ | `treatment_sequence.py`(modality FK 없음) |
| 레시피 → 시술군 | ② `combo_recipe_procedure → modality` | `combo_recipes.py` |
| 시술군 → 시술 항목 → 제품 | ① | `taxonomy.py:73,91,129` |
| 제품 사전(products.json) ↔ taxonomy 제품 | ② `product_category_modality` 로 시술군만. 제품끼리는 ⑤(이름이 같을 뿐) | `products.py` |
| 시술 → 적응증·효과 | ① 시술 쪽 FK, 내용은 ④ 문장 | `modality_*_indication` |
| 시술 → 부작용 | ① `complication.modality_id` + ④ 문장 | `complications.py` |
| 시술 → 환자 금기 | ① + ④ 문장 | `modality_contraindication` · `consent_contraindication` |
| 시술 → 가격 | ① `pricing_category → modality`. 부위·제품 등급은 ④ 항목 이름 안 | `market_pricing.py` |
| 부위 엔티티 | ⑤ — 부위 마스터 없음. 부위는 고민 하위 라벨(「코」「턱/턱선」)·가격 항목명(「이마 주름 (수입)」)·위험 부위 `anatomy_danger_zone`(11곳) 세 곳에 흩어짐. 위험 부위→시술은 보톡스/필러 스펙만 ① | `anatomy_danger_zones.py` |
| 고민 ↔ 부위 · 고민 ↔ 증상 · 고민 ↔ 효과 | ⑤ | — |
| PIH 위험 → 시술 | ④ `procedure_ref`(3레벨 혼재라 FK 불가) | `pih_risk.py:30` |
| 문헌 → 시술 | ① `literature_evidence_category → modality` | `literature_evidence.py` |

### 2-2. canonical 계층 (스키마만, 서빙 안 됨)

| 연결 | 종류 | 근거 |
|---|---|---|
| concern → complaint | ① | `canonical_catalog.py:272` |
| concern(+complaint) → 추천 패키지 → 시술 개념 | ① `recommendation_package.concern_id` · `recommendation_package_item.procedure_concept_id` | `canonical_recommendation.py:55~72,126~134` |
| concern → 시술 개념 **직접** | ⑤ — 패키지를 거쳐야만 닿음 | — |
| concern → indication · 부위 | ⑤ — `data-model.md:84~91` 의 `CONCERN_INDICATION` · `PROCEDURE_INDICATION` · `ANATOMICAL_SITE` · `PROCEDURE_SITE` 는 **스키마에 없음** | Q6 |
| 시술 개념 → claim → 문헌 | ① + ② | `canonical_knowledge.py:105,177~194` |
| 시술 개념 → 제품 | ② `catalog_procedure_product` | `canonical_catalog.py:205` |
| 시술 개념 ↔ 시술 개념 시너지 | ① | `canonical_recommendation.py:371~431` |
| 안전 subject → 시술 개념 | ② | `canonical_safety.py:68~95` |
| 검색 단위 → 엔티티 | ③ `entity_refs` JSONB. 본문에서 정규식 `\b(?:M\|P)\d+…` 으로 뽑은 코드 | `knowledge_search.py:54` · `modules/retrieval/indexing.py:112,167` |

### 2-3. 다이어그램 (지금 서빙되는 레거시 계층 중심)

실선 = FK/조인, 점선 = 이름 문자열(조인 불가), `✗` = 연결 없음.

```mermaid
flowchart LR
  subgraph 고민어휘
    P[problem P1~P14<br/>14]
    PS[problem_subcategory<br/>53 · 기미/얼굴 쳐짐/코]
    PI[problem_item<br/>117 · 대부분 시술명]
    CC[problem_complaint CC<br/>115]
    OC[optimization_concern<br/>8 · 주름 개선/처짐·탄력…]
    ST[synergy.target<br/>문자열]
    CMP[comparison.best_for<br/>문자열]
  end
  subgraph 시술
    M[modality M1~M17<br/>17]
    MS[modality_subcategory 74]
    MI[modality_item 521]
    PR[procedure_profile 17]
  end
  subgraph 기타
    MP[modality_product 59]
    PD[product 사전]
    IND[indication 문장]
    SAF[safety/complication 문장]
    CI[contraindication_rule 27]
    SY[synergy_link 115]
    PRC[pricing_item 122]
    AZ[anatomy_danger_zone 11]
    PK[problem_package 24]
  end
  P --> PS --> PI
  PI -- modality_ref 91/117 --> M
  P --> CC
  CC -. cc = item.name .-> PI
  CC -- category FK --> M
  CC -. product_name .-> PD
  P --> PK
  PK -- procedure_id --> PR
  PR -. 같은 M 코드 .- M
  PK -. product 문장 .-> PD
  OC -. procedure_text .-> MI
  OC -. ✗ .- P
  M --> MS --> MI
  M --> MP
  MI --> IND
  M --> IND
  M --> SAF
  CI --> M
  SY --> M
  SY -. item_name .-> MI
  ST -. ✗ .- P
  PRC --> M
  AZ -. 보톡스/필러만 .-> M
  PI -. ✗ .- MI
```

---

## Q3. 매핑 누락 실측 (stg)

**수집**: `GET {stg}/api/v1/{taxonomy,products,problem-combos,problem-packages,combo-recipes,synergy,contraindications,complications,treatment-optimization,treatment-sequence,procedure-profiles,market-pricing,patient-education,procedure-comparison,pih-risk,post-procedure-timeline,literature-evidence,consent-checklist,anatomy-danger-zones,pre-procedure-checklist,extracted}` — 21개 목록 엔드포인트를 각 1회(전부 200). 이후 로컬 파이썬으로 셌다.
**이름 일치 판정**: `re.sub('[^0-9A-Za-z가-힣]+','',s).casefold()` 로 정규화한 뒤 완전 일치. 이 정규화는 코드의 `normalize_term`(`modules/retrieval/domain.py:58`)과 같다. 대상은 시술군명 17 · `modality_item.name` 521 · 제품명(taxonomy 제품 59 + products.json).

### 3-1. 고민 → 시술

| 수치 | 값 | 비고 |
|---|---|---|
| 고민 P 14개 중 고민 항목→시술군 연결이 있는 것 | 14/14 | 적어도 1개 항목이 연결됨 |
| 고민 항목 117개 중 `modality_ref` 있음 / 없음 | **91 / 26** | 잘못된 ref 0(SPEC-001 INV-5 준수) |
| 연결 개수 분포 | 1개 79 · 2개 10 · 3개 2 · 0개 26 | |
| 고민 항목 → `modality_item`(521개) 연결 | **0** | 테이블 자체가 없음 |
| 고민 항목 이름이 시술 엔티티 이름과 일치 | 시술군 6 · 시술 항목 19 · 없음 92 | 고민 항목명이 시술명인데도 시술 원장과 이름이 안 맞음 |
| 고민 14개 중 problem-combos(tier 패키지)가 있는 것 | **8** (P1·P2·P3·P4·P5·P7·P9·P11) | 없음: **P6 여드름 · P8 홍조/혈관 · P10 제모 · P12 바디 · P13 두피/탈모 · P14 기타** (SPEC-004 OPEN-012 로 이미 인지) |
| problem-combos 패키지 24개의 시술 ref 63개 | 모두 유효, 서로 다른 시술군 **9개만** | |
| CC 115개 중 권장 시술 있음 | 115 | |
| CC 권장 시술 254행의 `category` | 254 유효 | |
| CC 권장 시술 254행의 `name` 이 시술 원장과 일치 | 시술군 171 · 시술 항목 17 · **없음 66** | 예: 「리프팅기기」「프락셔널」「피코레이저」「혈관레이저」「제모레이저」「크라이오」 |
| CC 권장 시술 목록이 다른 CC 와 **완전히 같은** 것 | **98/115** (서로 다른 목록 48개) | 「CC 자동 생성」(problem-packages `description`) 흔적 |
| CC 의 taxonomy `modality_ref` 와 그 CC 권장 시술 시술군의 교집합이 ∅ | **9/90** | 예: P7 「CO2프락셀」 ref M8 → 권장 [M11 니들RF, M4 스킨부스터] |

### 3-2. 시술 → 고민 (역방향)

| 수치 | 값 |
|---|---|
| 시술군 17개 중 어떤 고민 항목에도 안 걸리는 것 | **1** — M13 플라즈마 |
| 시술군 17개 중 problem-combos 패키지에 안 나오는 것 | **8** (패키지에 쓰인 시술군 9개 외 전부) |
| 시술 항목 521개 중 어떤 고민에도 FK 로 안 걸리는 것 | **521 (100%)** — 고민은 시술군까지만 연결됨 |
| 시술 항목 521개 중 적응증 문장이 있는 것 | 521 (문장 1,684개) — 고민 연결의 유일한 실마리지만 **④ 텍스트** |

### 3-3. 끊긴 이름 참조

| 원장 | 참조 수 | 엔티티와 안 맞음 | 끊긴 예시(실물) |
|---|---|---|---|
| CC 조합 구성 `complaint_combo_item.procedure_name` vs 같은 CC 의 권장 시술명 | 277 | **36** (SPEC-018 INV-4 「부분집합」 위반) | CC「이마지방이식」 조합에 `PRP` ↔ 권장 시술명은 「PRP/자가혈」 · CC「필러볼륨」 조합에 `바이오스티뮬레이터` ↔ 권장은 「바이오스티뮬레이터/콜라겐부스터」 · CC「압출」 조합에 `필링` ↔ 권장 [니들RF, 메디컬스킨케어] |
| optimization `optimal_combo` 문자열 | 74 | **48** | 「HIFU(슈링크/울쎄라)」「HA 필러(딥)」「PRP (엑소좀은 보조·근거 제한적)」「MTS/니들RF」「TCA Cross」 |
| synergy 끝점(`M?-이름`의 이름 부분) | 230 | **67** (`*_category` M 코드 230/230 유효) | 「M9-리프팅기기」「M8-프락셔널」「M4-리쥬란」「M2-코필러」「M17-엑소좀」 |
| problem-combos 패키지 제품 문장(+·or·/ 로 쪼갠 토큰) | 88 | **36** | 「엘러간」(제조사), 「리쥬란」(원장은 「리쥬란 힐러」「리쥬란 HB+」) |
| CC 권장 제품 `product_name` | 388 | 9 | 「CO2레이저」「PDL(V빔)」「트리암시놀론(±5-FU)」「헤어맥스(LLLT)」 |
| CC 권장 시술 `name` vs 시술 항목의 시술군 | 254 | 6행이 다른 시술군을 가리킴 | 「서브시전」이 `category=M8` ↔ taxonomy 시술 항목 「서브시전」은 M15 소속(ADR-0002 의 `M8-서브시전` 충돌과 같은 건) |

### 3-4. 다른 연결

| 연결 | 실측 | 비고 |
|---|---|---|
| 고민 어휘 간 연결 | **0** | optimization 고민 8종 중 taxonomy P 이름과 같은 것은 「제모」 1개, 하위 라벨과 같은 것은 「여드름/흉터」 1개. synergy `target` 12종 이상(「리프팅」 31·「안티에이징」 30·「여드름/모공」 8 …)은 어디에도 FK 없음 |
| 부위 | 부위 엔티티 0 | 위험 부위 11곳(`id` forehead…neck, `body_part_key` 전부 null), 고민 하위 라벨, 가격 항목명에만 있음 |
| 효과(적응증) | 시술군 문장 156 · 시술 항목 1,684 · 제품 270 | 전부 ④. 「모공」 문장이 있는 시술 항목 91개, 「기미」 41개, 「처짐」 72개, 「쳐짐」 **0개** |
| 시술 간 금기 | 27쌍 · 시술군 11/17 · 136쌍 중 27 | M 코드 FK. 나머지 6개 시술군은 규칙 없음 |
| 환자 금기 | absolute 53 · relative 55 | 시술군 FK + 문장. 환자 상태 엔티티 없음 |
| 부작용 | 합병증 65 · 시술군 10/17 | M4·M5·M6·M10·M12·M13·M17 없음 |
| 가격 | 시술군 17/17 · 항목 122 | 부위·국산/수입 구분은 항목명 텍스트(「이마 주름 (수입)」). 패키지 가격은 「5~8만」 문자열 |
| PIH 위험 | 26행 · 항목 ref 19 + 하위 분류 ref 7 | 레벨 혼재 |
| 회복 타임라인 | 10개 | id 가 slug(「botox」「hifu-rf」) |

---

## Q4. 지금 코드로 「○○가 고민이에요」를 넣으면

### 4-1. 갈 수 있는 경로 (코드 추적)

| 경로 | 입력 | 하는 일 | 끊기는 곳 |
|---|---|---|---|
| A. `GET /taxonomy` | 없음(전량) | 고민 트리 + `modality_ref` 를 그대로 반환 | 질의 파라미터 없음. 문자열→고민 매칭은 소비자 몫 |
| B. `GET /problem-combos` | `lang` 만 | 8개 고민의 tier 패키지 전량 | 6개 고민 없음, 도착점이 시술군 |
| C. `GET /problem-packages` | 없음 | 14고민×CC 전량 | CC 가 시술명이라 고민 질의와 바로 안 맞음 |
| D. `GET /treatment-optimization` | 없음 | 고민 8종×중증도 조합 | 조합이 텍스트(48/74 원장 불일치) |
| E. `POST /knowledge/retrieve` | `query` | 아래 4-2 | 게시 release 가 없으면 `unavailable` |
| F. canonical `recommendations()` | concern 코드 | concern→package→concept 조인 | **호출하는 곳이 없음** (`grep -rn '\.recommendations(' backend` → 0건) |

### 4-2. retrieve 경로 (코드 추적, stg 호출 안 함)

1. 「고민」이 들어 있으면 의도 `problem_recommendation` (`modules/retrieval/domain.py:198`)
2. 게시 release 가 없으면 즉시 `unavailable` (`application.py:364~392`)
3. 고민 식별: `catalog_concern.name_ko` 와 `catalog_complaint.name_ko`·`group_name` 을 별칭으로 써서, 정규화한 질의에 **부분 문자열**로 들어 있는지 본다 (`persistence.py:338~357`, `domain.py:65~`)
4. 고민이 잡혀도 **랭킹 의도만 추가**한다(`application.py:399~402`). 추천 패키지 조회(`recommendations()`)로 이어지지 않는다
5. 실제 후보는 `knowledge_search_unit.search_text ILIKE '%term%'` 다(`persistence.py:226~276`). 검색 단위는 레거시 JSON 스냅샷을 dict 노드마다 쪼갠 텍스트다(`indexing.py:176~`). 그래프 순회가 아니라 어휘 검색이다
6. 후보는 `domain_key, stable_ref` 순으로 정렬해 **500개에서 자른 뒤** 점수를 매긴다(`persistence.py:231,251`). 점수 임계값은 0.9(`application.py:131`)
7. 응답의 「근거」는 매칭 이유(`title_match`·`entity_relation`·`intent_match`)다. 임상 근거가 아니다(`retrieval.md` §3.4 「의료적 신뢰도 점수가 아님」)

### 4-3. 세 질의 실측 (stg GET 응답을 로컬에서 같은 단어로 걸러 발췌)

retrieve 는 POST 라 브리프 제약상 부르지 않았다. 대신 가장 가까운 GET 목록 엔드포인트를 받아 같은 단어로 걸렀다.

**「모공」** — 고민 어휘에 있다
- taxonomy: `P7 모공`(대분류) · 하위 `P6-2 피지/모공` · `P7-3 흉터형(열린모공)`
- problem-combos P7: `entry 스킨보톡스 + 레이저 [M1,M8]` · `recommended 니들RF + PRP [M11,M5]` · `premium 니들RF + 레이저 + PRP + 스킨부스터 [M11,M8,M5,M4]`
- problem-packages P7: CC 6개 중 「아그네스」「CO2프락셀」「서브시전」 셋이 모두 `[니들RF M11, 스킨부스터 M4]` 로 같다
- optimization 「피부결/모공」: `중등도 → [프락셔널 레이저, MTS/니들RF, 스킨부스터] evidence high`
- retrieve 예상: 「모공」이 concern P7 이름에 부분일치 → 고민 엔티티 P7 → 랭킹 가산. 패키지 조인은 없음
- **결과**: 시술군 단위 추천은 나온다. 고르는 근거는 큐레이션된 tier 와 `clinicalRationale` 텍스트다. 「레이저(M8)」 안의 어떤 레이저인지는 안 나온다

**「기미」** — 하위 라벨에만 있다
- taxonomy: 대분류 없음, 하위 `P5-1 기미` → 항목 `레이저토닝 / 피코토닝 → M8`, `미백필링 → M15`
- problem-combos P5: `entry 레이저 토닝 [M8]` · `recommended … [M8,M5,M4]` · `premium … [M8,M11,M5,M4]`
- problem-packages P5 기미: CC 3개 전부 `[레이저 M8 「색소 파괴」, 스킨부스터 M4]`
- optimization 「색소/기미」: `중등도 → [피코토닝, 트라넥삼산(경구/국소), 스킨부스터(미백성분), 저출력 IPL(병용 보조)] evidence high`
- retrieve 예상: complaint `group_name`「기미」가 P5 별칭 → 고민 엔티티 P5
- **결과**: 시술군까지 간다. 단, P5 tier 패키지는 「색소/미백」 전체용이라 기미 전용이 아니다. 「기미」 하나에 큐레이션 셋(combos·packages·optimization)이 서로 다른 답을 낸다

**「처짐」** — 고민 어휘에 없다(데이터는 「쳐짐」)
- taxonomy: 대분류·하위·항목 **0건**. 데이터는 `P3 쳐짐` · `P3-1 얼굴 쳐짐` · 「볼쳐짐/불독살」
- problem-combos · problem-packages: **0건**
- optimization 「처짐/탄력」: `중등도 → [HIFU(슈링크/울쎄라), 보톡스(턱선/광대), 바이오스티뮬레이터] evidence high`(텍스트, taxonomy 와 연결 없음)
- 적응증 문장: 「처짐」 72개 시술 항목 ↔ 「쳐짐」 0개
- retrieve 예상: 「처짐이」→ 「처짐」. 고민 엔티티 매칭 실패(「쳐짐」≠「처짐」) → 어휘 검색만
- **결과**: FK 경로는 첫 홉에서 끊긴다. 텍스트 원장(optimization·적응증)에만 걸린다

---

## Q5. 그래프로 옮기면

### 5-1. 노드

| 노드 | 원장 | 개수(stg) | 비고 |
|---|---|---|---|
| Concern(대) | `problem` | 14 | 「쁘띠시술」「제모」「얼굴윤곽」처럼 고민이 아닌 시술 범주가 섞임 |
| Concern(하) | `problem_subcategory` | 53 | 「기미」 같은 실제 고민 + 「코」 같은 부위 + 「반영구화장」 같은 시술 |
| ConcernItem / Complaint | `problem_item` = `problem_complaint.cc` | 117 / 115 | 이름 대부분이 시술명 |
| OptConcern | `optimization_concern` | 8 | 별도 어휘 |
| Severity / AgeGroup | `optimization_severity_level` / `_age_group` | 24 / 4 | |
| ProcedureGroup | `modality` | 17 | 모든 FK 의 종착점 |
| Procedure | `modality_item` | 521 | 고민 쪽 FK 없음 |
| Product | `modality_product` + `product` | 59 + 사전 | 두 원장, 서로 FK 없음 |
| Package | `problem_package` · CC 권장 | 24 · 254행 | |
| Indication/Effect | indication 문장 | 2,110 | 노드가 아니라 문장 |
| Complication | `complication` | 65 | |
| Site | — | 0 | 부위 노드 없음 |
| Evidence | `literature_evidence_*` · canonical claim | — | 시술군 단위 |

### 5-2. 엣지

| 엣지 | 지금 있나 | 근거(출처) | 강도(가중치) |
|---|---|---|---|
| Concern → ConcernItem | ① 있음 | 없음 | 없음(정렬만) |
| ConcernItem → ProcedureGroup | ② 91/117 | 없음 | 없음 |
| ConcernItem → Procedure | **없음** | — | — |
| Concern → Package → ProcedureGroup | ① 8/14 고민 | `clinicalRationale` · `riskBenefit` 텍스트 | tier(entry~vip)만 |
| Complaint → ProcedureGroup | ① 254 | `role` 텍스트(「색소 파괴」) | 없음(정렬만) |
| Complaint → Combo → 시술명 | ④ 277 (36 끊김) | `reason` · `evidence` 텍스트 | 없음 |
| OptConcern×Severity → 시술명 | ④ 74 (48 불일치) | `rationale` 텍스트 | `evidence_level` high/moderate/low(조합 단위) |
| ProcedureGroup ↔ ProcedureGroup 시너지 | ① 115 | `reason` 텍스트 | 없음(type 만). canonical 쪽은 `priority` |
| ProcedureGroup ↔ ProcedureGroup 금기 | ① 27 | `note` 텍스트 | `level` safe/caution/warning |
| Procedure → Indication | ① 시술 쪽만, 고민 쪽 ④ | 없음 | primary/secondary/extended |
| Procedure → Complication | ① 65 | `evidence` URL 문자열 | `severity` · `incidence` 텍스트 |
| Concern → Site | 없음 | — | — |
| Procedure → Site | 없음(위험 부위 보톡스/필러만) | — | — |
| Concern ↔ OptConcern ↔ synergy.target | **없음** | — | — |
| Procedure → Evidence(canonical claim) | ① 스키마 | 인용·검증 상태 | `support_level` · `accuracy_score` |
| Concern → Procedure 근거 | **없음** | — | — |

### 5-3. 「고민 → 시술」 경로

| 경로 | 홉 | 도착 | 비는 곳 |
|---|---|---|---|
| 질의어 → `problem`/`problem_subcategory` 이름 | 0(문자열 매칭) | 고민 노드 | 어휘·표기 불일치(「처짐」) — 동의어 없음 |
| → `problem_item` → `modality` | 2 (총 3) | 시술군 17개 중 하나 | 26 항목 끊김 · 시술 항목(521)까지 못 감 |
| → `problem_combo` → `problem_package` → `procedure_profile`(M) | 3 | 시술군 | 6개 고민 없음 |
| → `problem_complaint` → `complaint_procedure` → `modality` | 3 | 시술군 | CC 가 시술명이라 「고민」 노드가 아님, 98/115 같은 목록 |
| 시술군 → 시술 항목 | +1 FK | 521 | 어떤 항목인지 고를 근거 없음(적응증 문장뿐) |
| (canonical) concern → package → item → concept | 3 | concept(계층 어느 레벨이든) | 경로를 읽는 코드가 호출되지 않음, stg 적재 확인 안 됨 |

---

## Q6. 문서 ↔ 코드 차이 (추천 관련)

| 문서(위치) | 문서가 말하는 것 | 코드·데이터 실물 |
|---|---|---|
| SPEC-001 Business Req (`spec-001-taxonomy.md:48`) | `modality_ref` 로 「이 고민에는 어떤 시술」을 도출 | 시술군(17) 단위까지만 됨. 26/117 비어 있음 |
| SPEC-004 Business Req (`spec-004…md:45`) | 「P3 리프팅, P4 피부재생, P5 여드름, P7 색소침착, P9 안티에이징, P11 지방·윤곽」 | 실제 P3=쳐짐, P4=항노화, P5=색소/미백, P7=모공, P9=흉터, P11=얼굴윤곽 — 문서 안에서 이름이 틀림 |
| SPEC-004 INV-4 | `procedures[]` = taxonomy modality ID | 코드 FK 는 `procedure_profile.id`(`problem_combos.py:78~80`). 값이 같은 M 코드라 지금은 동작 |
| SPEC-018 INV-4 | `combos[].combo[]` ⊆ `procedures[].name` | stg 36/277 위반 |
| SPEC-015 (`spec-015…md:39`) · OPEN-023 | treatment-optimization BE 엔드포인트 없음 | v1.2.0 에 `GET /treatment-optimization` 있음(`router/data.py:405`) — 코드가 앞섬 |
| SPEC-015 INV-4 · OPEN-022 | `optimal_combo` 는 display name, modality ID 와 lookup 불가 | 그대로. 48/74 불일치 |
| SPEC-003 · `guides/api.md:133` | synergy 116 링크 | stg 115 |
| SPEC-050 (`spec-050…md:51`) | problem-packages 는 CHARTY 미사용, CHARTY 추천 컨텍스트는 taxonomy·combo-recipes·synergy·problem-combos | 문서 범위가 v1.1.0 에서 멈춤, canonical/retrieve 언급 없음 |
| `data-model.md:84~91` ERD A | `INDICATION` · `CONCERN_INDICATION` · `PROCEDURE_INDICATION` · `ANATOMICAL_SITE` · `PROCEDURE_SITE` | **테이블 없음**(166개 목록에 없음) |
| `data-model.md:425~` ERD D | `CARE_PLAN_TEMPLATE` · `CARE_PLAN_STEP` · `PRICING_OBSERVATION` | 테이블 없음 |
| 같은 ERD D `RECOMMENDATION_PACKAGE` | `age_min` · `age_max` · `severity_scope` 컬럼 | 도메인 객체에만 있음(`modules/recommendation/domain.py:119~121`), ORM·마이그레이션에 없음 |
| 같은 ERD D `PACKAGE_ITEM.product_id` · `PROCEDURE_SYNERGY.score` | 있음 | 없음. 제품은 `recommendation_package_component`, 시너지는 `priority` |
| `data-model.md` §13 Task 4 | 「추천 항목의 시술·제품이 모두 FK로 연결됨」 완료 | canonical 스키마 기준으로는 맞음. 서빙되는 레거시 원장은 텍스트 참조 그대로 |
| `data-model.md` §12 · `retrieval.md` §1 | 판단 결과에 `rule_refs`·`evidence_refs` 포함 / retrieve 는 「시술 추천 API가 아니다」 | 추천 판단 API 자체가 없음. retrieve 는 범용 검색 |
| `retrieval.md` §5.2 | 「결과의 canonical entity를 기준으로 relation 확장」 | 고민 엔티티는 랭킹 의도만 추가, 추천 관계 확장 없음(`application.py:399~402`) |
| 기획 문서 전체 | v1.1.0(2026-07-03), JSON 파일 SSOT · Docker 재빌드 | 코드는 DB 단일 원장 · dump 복원 · canonical 계층(2026-09-03). 기획에 canonical·ADR-0002/0003 반영 없음 |

---

## Q7. 정할 것 (질문만)

1. **고민 어휘의 정본**은 어디인가 — taxonomy `problem`(14, 시술 범주 섞임) · `problem_subcategory`(53) · `optimization_concern`(8) · synergy `target` · canonical `catalog_concern` 중 무엇, 또는 새로?
2. 「쁘띠시술」「제모」「얼굴윤곽」「반영구화장」처럼 **고민이 아닌 항목**을 고민 어휘에 계속 둘 것인가?
3. **표기·동의어**(「처짐/쳐짐」, 「여드름흉터/여드름 흉터」, 「피부결/모공」)를 누가 어디서 관리하나?
4. 추천의 **도착 단위**는 시술군(17) · 시술 항목(521) · 제품 중 무엇인가?
5. **세 큐레이션 원장**(problem-combos tier · problem-packages CC · treatment-optimization 중증도) 가운데 무엇을 원천으로 삼나? 하나의 고민에 서로 다른 답을 내는 지금 상태를 어떻게 다루나?
6. 고민–시술 엣지의 **근거**(문헌·전문가 합의·AI 컨센서스 표기)와 **강도**를 엣지에 둘 것인가? 둔다면 원천은 무엇인가?
7. 적응증 문장 2,110개처럼 **텍스트로만 있는 고민 신호**를 구조로 끌어올릴 것인가, 검색으로 쓸 것인가?
8. **부위**를 엔티티로 세울 것인가? 고민·시술·가격·위험 부위 중 어디와 잇나?
9. 중증도·연령 같은 **조건**을 추천 입력으로 받을 것인가? 받는다면 `severity_scope` 등 도메인에만 있는 필드는 어떻게 하나?
10. 추천을 **레거시 계층 위**에 올리나, **canonical 계층 위**에 올리나? canonical 이면 release 발행(의사 검수)이 선행 조건인가?
11. 기존 `RecommendationEligibilityPolicy`(안전 우선 판정, 테스트만 있음)와 미사용 `recommendations()` 를 살리나?
12. 안전 필터(시술 간 금기 27쌍, 시술군 11/17 만 커버)의 **빈칸**을 추천 전에 채워야 하나?
13. 추천 결과는 **누가 승인**하나 — 큐레이션(사람) 원장만 내보내나, 경로 탐색으로 생성된 후보도 내보내나?
14. 기획 문서(v1.1.0)와 코드(v1.2.0) 중 이번 설계의 **기준 문서**는 무엇인가? 기획 SPEC 을 먼저 갱신하나?

---

## 부록 — 셈 재현

- stg 수집: `curl -s https://api-stg-csp.medisolveai.com/procedure-hub/api/v1/<endpoint>` (21개, GET, 각 1회)
- 정규화 일치: `norm = lambda s: re.sub(r'[^0-9A-Za-z가-힣]+','',s).casefold()`
- 스키마 일치: `grep -oE "op.create_table\('[a-z_0-9]+'" b202609030001_initial_schema.py | sort` vs `grep -rhoE '__tablename__ = "[a-z_0-9]+"' app/model | sort` → diff 0
- 미호출 확인: `grep -rn '\.recommendations(' backend` → 0건, `grep -rl 'RecommendationEligibilityPolicy' backend` → domain·tests 만
- 조사하지 않은 것: canonical 테이블의 stg 행 수(POST·DB 접근 금지로 확인 안 됨), 프론트엔드 코드의 추천 계산(`frontend/` 는 범위 밖), 지난 목업 스냅샷 `hub-snapshot.json`(참고만 — 키 `meta·modalities·nodes·problems`)

# 시맨틱 정본 — 노드 · 엣지 · 용어 · 사전 · id · 읽는 규칙 · 표시 · 상속

정본 데이터 `semantic.json`(이 문서는 그 json 에서 만든 것) · 결정론 `semantic-build.py`(실버 파일에서 계산 · 시각 없음) · 결정 _RESUME.md §2 2026-10-30 「시맨틱 조사 반영 — 추천대로」(B1~B12 · U1~U3) · 조사 semantic-research.json

입력: `step1-products.json` 2 41128c7d5bce171b · `step2-families.json` step2-families v1 42eef4dc7dc70b26 · `step3-sites.json` 3.0 f92f4a8411c15cd1 · `step4-techniques.json` v1 cc6c0291a0b3506a · `step5-units.json` step5-units v1 38bcc0853547edb7 · `step6-packages.json` step6-packages v1 293b50e565ddf61e · `step7-concerns.json` step7-concerns v1 (2026-10-29) b2fa90915876de1d · `step8-relations.json` step8-v1 4f91a2abe7e3aae2 · `step7-decisions.json` 2 ae73f09bced8c13b · `step8-decisions.json` 1 2fbeb45c010185e6 · `step3-lexicon.json` 1.1 c3b4effa7662af8c · `step9-explanations.json` step9-v1 5d394f87dca53602

## 0. 요약

노드 종류 **13** · 엣지 종류 **21** · 용어 **47** · 표시 **12** · gate_status **3값** · 상속 규칙 **9** · 사전 표현 **2053**(대상 2991 · 겹침 208) · id 대응 **1071** · 합병증 35 · 부작용 72 · 합병증 gap 12 · open **0**

## 1. 노드 종류

| # | 정본 종류 | 이름 | 뜻 | 정본 id · 실버 id 규칙 | 필수 | 선택 | 정본 파일 · 칸 | 셈 |
|---|---|---|---|---|---|---|---|---|
| 1 | `product` | 제품 | 허가 · 업체 · 규격을 가진 제품 · 장비(라인이면 상위 제품) — 시술에 「쓰는 것」 | `product:{키}` — 원장 ledger_id 그대로(원천 추적) — 꼴이 여럿이라 접두로만 구분<br>실버 꼴 {"M9-9-9": 85, "M9-P-9": 14, "auto-9-9": 35, "auto-M9-9": 176, "auto-M9-DCA-9": 7, "auto-M9-hADM-9": 1, "new-DEV-9": 34, "step9-new-APTOS": 1, "step9-new-FASCELLA": 1} | ledger_id · 2_names.display_name · 4_license.status · 4_license.recommendable · active | 2_names.search_names[] · 1_identity.kind · 4_license.licenses[] · history[] · 5_spec · 6_companies · line · evidence · open | `step1-products.json` items[] (active) | **354** items 395 중 active 354 · 추천 236 |
| 2 | `family` | 계열 | 무엇을 — 공식 일반명 약제 · 장비 계열(문헌 M1~M17 + 늘린 N1~N10) | `family:{키}` — M{n} · N{n} 그대로<br>실버 꼴 {"M9": 17, "N9": 10} | id · name · definition · name_status | synonyms[] · literature_name · literature_evidence[] · sub_families[] · new_family | `step2-families.json` families[] | **27** 새 계열 10 |
| 3 | `site` | 부위 | 어디에 — 몸 겉에서 가리킬 수 있는 자리(일반인 이름 + 전문의 이름) | `site:{키}` — site.{영문} 그대로<br>실버 꼴 {"site.abdomen": 1, "site.arm": 1, "site.axilla": 1, "site.back": 1, "site.beard": 1, "site.bikini": 1, "site.body": 1, "site.buttock": 1, "site.calf": 1, "site.cheek": 1, "site.cheek-group": 1, "site.chest": 1, "site.chin": 1, "site.chin-group": 1, "site.eyebrow": 1, "site.eyelid": 1, "site.face": 1, "site.flank": 1, "site.foot": 1, "site.forehead": 1, "site.forehead-group": 1, "site.full-face": 1, "site.gingiva": 1, "site.glabella": 1, "site.hand": 1, "site.infraorbital": 1, "site.jawline": 1, "site.lateral-canthus": 1, "site.leg": 1, "site.lips": 1, "site.marionette": 1, "site.masseter": 1, "site.mouth-corner": 1, "site.nasal-ala": 1, "site.nasal-dorsum": 1, "site.nasal-tip": 1, "site.nasolabial": 1, "site.neck": 1, "site.neck-group": 1, "site.nose": 1, "site.nose-group": 1, "site.perioral": 1, "site.periorbital-group": 1, "site.philtrum": 1, "site.scalp": 1, "site.sideburn": 1, "site.submental": 1, "site.temple": 1, "site.thigh": 1, "site.trapezius": 1, "site.upper-arm": 1, "site.whole-body": 1, "site.zygoma": 1} | id · name · parent · status | synonyms[] · anatomical_name · danger_zone · compound_strings[] | `step3-sites.json` nodes[] | **53** 최상위 영역 4 |
| 4 | `technique` | 기법 | 어떻게 — 큰 기법 + 세부 기법 | `technique:{키}` — K{nn}[a-c] 그대로<br>실버 꼴 {"K9": 14, "K9a": 4, "K9b": 4, "K9c": 4} | id · name · level · parent | medical_name · family_default[] · source_expressions[] | `step4-techniques.json` nodes[] | **26** {"세부": 12, "큰": 14} |
| 5 | `unit_procedure` | 단위 시술 | 제일 작은 단위 행위 = 계열 × [하위 · 성분] × 부위 × 기법(원천에 있는 조합만) | `unit_procedure:{키}` — U5-{nnn} 그대로<br>실버 꼴 {"U9-9": 162} | id · key{family,sub_family,ingredient,site,technique} · name · site_basis | synonyms[] · candidate_of[] · uses_product[] · market[] · route_status · ops · step4_attrs · pih_not_applicable | `step5-units.json` units[] | **162** 특수 부위(노드 없음) 31 |
| 6 | `package` | 패키지 | 이름 있는 단위 시술 묶음(일반 · 회차 · 병원 시그니처) | `package:{키}` — P6-{nn} 그대로<br>실버 꼴 {"P9-9": 24} | id · name · kind · recommendable | shape · synonyms[] · price[] · same_day_raw · detail_raw | `step6-packages.json` packages[] | **24** {"병원 시그니처": 2, "일반 패키지": 19, "회차 묶음": 3} |
| 7 | `concern` | 고민 | 상태 이름 — taxonomy problem 「고민」 갈래 3층 + 결정 노드 | `concern:{키}` — P{n} · P{n}-{n} · auto-{n}-{ts} 그대로 · 결정 노드 J{n}-{한글} → J{n}(이름은 name 칸)<br>실버 꼴 {"J9-가": 3, "P9": 12, "P9-9": 31, "auto-9-9": 11} | id · name | sites[] · parent · related[] · kind · en · basis | `step7-concerns.json` concerns.categories[node] · subcategories[node] · items[kind=고민] · extra_items[] | **57** 대분류 12 · 중분류 31 · 항목 11 · 결정 노드 3 |
| 8 | `purpose` | 목적 | 시술이 하는 일 — 고민과 같은 말이면 노드 없이 그 고민에 붙음(R6) | `purpose:{키}` — 실버는 id 없음(이름 · 「목적:{이름}」 문자열) → PU-{nn}(purposes[] 순서)<br>실버 꼴 {"가": 9, "가 가": 1, "가 가(가)": 1, "가(가)": 2} | name · kind | aliases[] · from[] | `step7-concerns.json` purposes[] (node) | **13** 고민에 붙은 목적 이름 17 |
| 9 | `combo` | 추천 조합(사이트 「추천 패키지」) | 원천이 고민 · 목적별로 적은 시술 조합(원천별 · 합치지 않음) | `combo:{키}` — RC-… 그대로<br>실버 꼴 {"RC-AG-9가": 3, "RC-AG-9가+": 1, "RC-AN-9가": 2, "RC-AN-9가+": 1, "RC-CP-acne": 1, "RC-CP-body_contouring": 1, "RC-CP-hair_removal": 1, "RC-CP-lifting": 1, "RC-CP-pigment": 1, "RC-CP-rejuvenation": 1, "RC-CP-skin_texture": 1, "RC-CP-volume": 1, "RC-CP-wrinkle": 1, "RC-OP-Acne-가": 3, "RC-OP-Body-가": 3, "RC-OP-Hair-가": 3, "RC-OP-Pigmen-가": 3, "RC-OP-Saggin-가": 3, "RC-OP-Skin-가": 3, "RC-OP-Volume-가": 3, "RC-OP-Wrinkl-가": 3, "RC-PC-P9-9": 24, "RC-RE-R9": 7, "RC-SQ-9": 8} | id · kind · source · name · anchor | components[] · tier · price · effect · sales_copy | `step7-concerns.json` combos[] | **79** {"고민 패키지(사이트 「추천 패키지」)": 24, "목적 레시피": 7, "비교": 9, "세션 조합(순서)": 8, "연간 플랜": 3, "연령 플랜": 4, "중증도 조합": 24} |
| 10 | `check_condition` | 확인 조건 | 사람 쪽 조건(임신 · 약물 · 체질 …) | `check_condition:{키}` — C-{약어} 그대로<br>실버 꼴 {"C-ACNE": 1, "C-AGE": 1, "C-ALLERGY": 1, "C-AMINO": 1, "C-ANTICOAG": 1, "C-AUTO": 1, "C-BF": 1, "C-BLEED": 1, "C-BMI": 1, "C-CANCER": 1, "C-CARDIO": 1, "C-CHF": 1, "C-CHRONINF": 1, "C-COLD": 1, "C-DENTAL": 1, "C-DERM": 1, "C-DM": 1, "C-DPEN": 1, "C-EPI": 1, "C-EXPECT": 1, "C-FITZ": 1, "C-FLIGHT": 1, "C-G9PD": 1, "C-GRAN": 1, "C-HERNIA": 1, "C-HORMONE": 1, "C-HSV": 1, "C-HYAL": 1, "C-INDIC": 1, "C-INFECT": 1, "C-ISO": 1, "C-KEL": 1, "C-LIDO": 1, "C-LIVER": 1, "C-METAL": 1, "C-MUSCLE": 1, "C-NEURO": 1, "C-NMJ": 1, "C-NSAID": 1, "C-PACE": 1, "C-PEELALG": 1, "C-PHOTO": 1, "C-PREG": 1, "C-PRIOR": 1, "C-RADIO": 1, "C-RESID": 1, "C-RETIN": 1, "C-SKINCARE": 1, "C-SMOKE": 1, "C-SUN": 1, "C-SUPPL": 1, "C-SURG": 1, "C-VASC": 1} | id · name · match_pattern | n_claims · sources[] | `step8-relations.json` conditions.nodes[] | **53**  |
| 11 | `complication` | 합병증 | 예상 밖 이상 결과(혈관 폐색 · 감염 …) — severity moderate 이상 + U1 원문 serious. 흔한 예상 반응(부작용)은 노드 아님(계열 속성) | `complication:{키}` — CX-{계열}-{원천 번호} · U1 원문 serious = CX-{계열}-T{n}<br>실버 꼴 {"CX-M9-9": 27, "CX-M9-T9": 8} | id · name · family · severity\|severity_site | incidence · onset · mechanism · management · prevention · risk_factors · evidence[] · source | `step8-relations.json` safety.complications[] | **35** {"critical": 3, "moderate": 13, "severe": 11, "원문 serious(taxonomy)": 8} |
| 12 | `evidence_statement` | 근거 문장 | 계열 단위 문헌 문장(기전 · 효과 · 이상 반응) + 환자용 4개 언어 | `evidence_statement:{키}` — ST-{계열}-{field}-{nn} 그대로<br>실버 꼴 {"ST-M9-adverse_effects-9": 32, "ST-M9-effects-9": 37, "ST-M9-moa-9": 50} | id · family · field · statement · evidence[] | accuracy_score · patient{} · class(B2 — 이 정본) | `step8-relations.json` evidence.statements[] | **119** {"adverse_effects": 32, "effects": 37, "moa": 50} |
| 13 | `evidence_source` | 근거 출처 | 문헌 · 웹 · 가이드(원천 출처 문자열) | `evidence_source:{키}` — EV-LIT · EV-WEB · EV-GD 그대로<br>실버 꼴 {"EV-GD-9": 15, "EV-LIT-9": 25, "EV-WEB-9": 29} | id · kind | pmid · doi · title · journal · year · url · urls[] · multi_url · label · used_by[] | `step8-relations.json` evidence.literature[] · web[] · guides[] | **69** 문헌 25 · 웹 29 · 가이드 15 |

### 1-1. 노드가 아닌 것(속성 · 칸)

| 무엇 | 자리 | 셈 | 규칙 | 결정 |
|---|---|---|---|---|
| 부작용(흔한 예상 반응) | `step8 safety.side_effects[]` | 72 원천 {"complications.json categories": 38, "taxonomy modality": 34} · 의료진 질문 예외 9 · 부작용 없는 계열 10 | U2 · B1 — 부작용(흔한 예상 반응) = 계열 속성 safety.side_effects · 합병증 노드 = complications.json severity moderate 이상만. 제품 × 계열 · 단위 시술에 값(5단계 extracted safety.common)이 있으면 그 값이 계열 값을 덮어씀 — 덮어쓰기는 골드 계산(B7 · 저장 안 함) | U2 · B1(10-30) |
| 끝점 묶음 | `step8 edges[].endpoints.a\|b.candidates[]` | 113 {"계열": 182, "계열 + 조건": 1, "계열 묶음": 2, "단위 시술": 163, "단위 시술 후보": 111, "모든 시술": 1} | U3 · B3 — 끝점 묶음은 노드가 아니라 엣지 칸 endpoints.a\|b{kind, id, qualifier, candidates[]} · 엣지 a · b 문자열은 그대로(뒤 호환) | U3 · B3(10-30) |
| 확인 조건 아닌 문장 | `step8 conditions.not_condition[]` | 37 {"고지 항목": 6, "근거 수준 문장(조건 ": 1, "부위 조건(사람 조건 ": 2, "상담 항목": 22, "시술 준비 항목": 5, "효과 문장(조건 아님)": 1} | B8 — 확인 조건 주장 중 kind 가 「…항목」(상담 · 시술 준비 · 고지)이거나 사람 조건 · 연령대 조건이 아닌 것 = 확인 조건 엣지 아님 → conditions.not_condition(원문 보관) · 계열 대상은 safety.family_text 「상담 · 준비 · 고지 · 조건 아닌 문장」(G10 그대로) · 엣지 셈에서 뺌 | B8(10-30) |
| 허가 · 업체 · 규격 | `step1 items[].4_license · 6_companies · 5_spec` | 327  | 제품 속성(1단계 「제품 ↔ 허가만」). 업체는 DEC-003 「제조사 원장」 — 노드 세우기는 적재(B9) · 지금 실버엔 업체 id 없음 | B9 |
| 시장가 | `step5 market[] · units[].market[]` | 122  | 단위 시술 × 제품 × 규격의 원문 가격 | 10-27 |
| 경과 타임라인 · PIH · 운영 속성 · 계열 원문 | `step8 safety.timelines · pih · family_text · step5 units[].ops · pih` | 10  | 붙는 수준(계열 · 하위 · 단위 · 제품)에 속성 — 상속 I8 | G11~G13 |
| 설명 사실(9단계) | `step9 node_slots[] · records[]` | 5312 {"한 원천": 2317, "같음": 33, "①": 43, "②": 196, "③": 357} | D9-1~D9-9(11-01) — 효과 시작 · 지속 · 작용 원리 · 개요 · 적응증 · 제품 메모 · 대안 · 관련 기법 · 고민 상세 = 붙는 노드(단위 시술 · 제품 · 계열 · 고민)의 속성 원문(section recovery · method · overview · disclosure). 같은 노드 · 같은 칸 충돌은 D9-3(① 긴 쪽 · ② resolved 하나 + alternatives · ③ 둘 다) | D9-1~D9-9(11-01) |

## 2. 엣지 종류

| # | 정본 종류 | 이름 | 뜻 | 시작 → 끝 | 방향 | 속성 | 정본 파일 · 칸 | 셈 | 상속 | 페이지 종류 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `product_family` | 계열 판정 | 제품이 어느 계열 제품인가(주 1 + 보조) | product → family | True | role(주 · 보조) · sub_family · also_sub_families · verdict · evidence_level · conflict · confirm_question | `step2-families.json` product_family[].family · also_families[] | **370**  |  | prod_fam, prod_fam_also |
| 2 | `key_family` | 단위 시술 키 — 계열 | 단위 시술 정체 첫 칸(무엇을) | unit_procedure → family | True | sub_family · ingredient | `step5-units.json` units[].key.family | **162**  |  | unit_fam |
| 3 | `key_site` | 단위 시술 키 — 부위 | 어디에(특수 부위 「해당 없음」 · 「병변 단위」는 엣지 없음 — 값만) | unit_procedure → site | True | site_basis | `step5-units.json` units[].key.site | **131**  |  | unit_site |
| 4 | `key_technique` | 단위 시술 키 — 기법 | 어떻게 | unit_procedure → technique | True | step4_attrs | `step5-units.json` units[].key.technique | **162**  |  | unit_tech |
| 5 | `child_of` | 상위 | 같은 종류 트리의 상하(부위 · 기법 · 고민) | site · technique · concern → 같은 종류 | True |  | `step3-sites.json · step4-techniques.json · step7-concerns.json` nodes[].parent · nodes[].parent · subcategories[].parent · items[].subcategory · extra_items[].parent | **104**  |  | site_parent, tech_parent, con_parent(상위) |
| 6 | `concern_related` | 관련 고민 | 상위 없는 결정 노드가 걸친 고민(J10 피부결) | concern → concern | False |  | `step7-concerns.json` concerns.extra_items[].related[] | **4**  |  | con_parent(관련) |
| 7 | `family_technique` | 계열 기법 | 계열 기본 기법 · 함께 쓰는 기법 | family → technique | True | role(기본 · 함께) · default_layer | `step4-techniques.json` family_defaults[].default · also[] | **34**  |  | fam_tech, fam_tech_also |
| 8 | `uses_product` | 쓰는 제품(저장) | 원천 이름이 제품을 부를 때만 저장 | unit_procedure → product | True | basis | `step5-units.json` units[].uses_product[] | **44**  |  | unit_prod |
| 9 | `contains` | 패키지 구성 | 패키지가 담은 단위 시술(확정 · 슬롯 후보) | package → unit_procedure | True | order · status(확정 · 슬롯 후보) · quantity_raw · sessions · evidence_level · origin_question | `step6-packages.json` contains[] · slots[].candidates[] | **71**  |  | pkg_unit, pkg_slot |
| 10 | `treats` | 추천(고민 · 목적 → 시술) | 원천 구조가 고민 · 목적에 적은 시술 | concern · purpose → unit_procedure · family | True | source · target_kind · lowering · resolve_flag · site_check · concern_region_check · severity · basis | `step7-concerns.json` edges[] | **437** {"계열만": 84, "단위 시술": 352, "대상 없음": 1} | 계열 단위 | con_unit, con_fam |
| 11 | `concern_site` | 고민 부위 | 부위가 붙은 고민의 부위 | concern → site | True |  | `step7-concerns.json` concerns.*.sites[] | **23**  |  | con_site |
| 12 | `anchors_combo` | 추천 조합 앵커 | 추천 조합이 걸린 고민 | concern → combo | True | kind | `step7-concerns.json` combos[].anchor.concern · concerns | **94**  |  | con_combo |
| 13 | `combo_component` | 조합 구성 | 추천 조합의 구성 시술 — 구성 칸 components(구성) · members(비교 대상) · upgrade(연령 플랜 업그레이드)(골드 빈틈 ② · 사용자 10-30) | combo → unit_procedure | True | field(구성 칸 이름 그대로) · order · status · flag | `step7-concerns.json` combos[].components\|members\|upgrade[].units[] | **581** components 462 · members 107 · upgrade 12 |  | combo_unit |
| 14 | `procedure_relation` | 시술 ↔ 시술 관계 | 시너지 · 순서 · 간격 · 같은 날 · 대체 · 금기 — 쌍 하나에 엣지 하나 · 주장 칸 | unit_procedure · family · 묶음(candidates) → 같음 | 주장마다 | endpoints.a\|b{kind,id,qualifier,candidates[]} · claims[]{kind, interval{days,first,same_day,open_high,by_sub_condition,options}, level_site, reason, evidence_kind, gate_status, review_status} · conditional_claims · review_status | `step8-relations.json` edges[] · claims[] | **230** 주장 395 · 끝점 {"계열": 182, "계열 + 조건": 1, "계열 묶음": 2, "단위 시술": 163, "단위 시술 후보": 111, "모든 시술": 1} | 계열 단위 | rel, rel_fam |
| 15 | `concern_avoid` | 피함(금기 조합) | 고민 조건 금기 | concern → unit_procedure · family | True | qualifier · scope · default_apply · grade_original | `step8-relations.json` avoid_edges[] | **5**  | 계열 단위 | avoid, avoid_fam |
| 16 | `requires_check` | 확인 조건 | 시술 → 사람 조건 · 등급(금기 · 주의 · 확인만) | family · product · unit_procedure · 모든 시술 → check_condition | True | grade_original · grade3 · kind · where · strength_original · scope_conditional | `step8-relations.json` conditions.claims[] (B8 — not_condition 뺌) | **422** 주장 336 · 등급 {"금기": 196, "주의": 61, "확인만": 74, "확인만(고지)": 5} | 계열 단위 | cond, cond_fam |
| 17 | `has_complication` | 합병증 | 계열 → 합병증(중대 반응만 — B1) | family → complication | True | severity_site | `step8-relations.json` safety.complications[].family | **35**  | 계열 단위 | fam_cx |
| 18 | `site_caution` | 위험지대 주의 | 부위 × 계열 위험지대 | site → family | True | zone · danger_level · vessels · nerves · safe_injection_depth · units_affected | `step8-relations.json` safety.site_caution[] | **22**  | 계열 단위 | site_caution |
| 19 | `has_statement` | 근거 문장 | 계열 → 근거 문장 | family → evidence_statement | True | field · class(B2) | `step8-relations.json` evidence.statements[].family | **119**  | 계열 단위 | fam_stmt |
| 20 | `cites` | 출처 | 근거 문장 · 합병증이 기댄 출처(관계 주장 출처는 주장 칸 claims[].evidence) | evidence_statement · complication → evidence_source | True |  | `step8-relations.json` evidence.statements[].evidence[] · safety.complications[].evidence[] | **124**  |  | stmt_ev, cx_ev, ev_claim |
| 21 | `line_item` | 라인 품목 | 라인(상위 제품) → 품목(하위 제품) — 결정 10-27 ④ | product → product | True | decision | `step1-products.json` lines{}.items[] (ledger_id 있는 것) | **5** 라인 11 · 품목 칸 26(허가번호만 있는 품목은 엣지 아님 — 라인 속성) |  | (새로) |

- 저장 엣지 아님: `prod_unit_inh` — 상속 후보 = 상속 I4 계산 결과 — 저장 안 함(B7 · 골드)
- 저장 엣지 아님: `set_member` — 끝점 묶음 = endpoints.candidates[] 칸(U3 · B3)

## 3. 용어집

| 용어 | 정의 | 출처 |
|---|---|---|
| **단위 시술** | 제일 작은 단위 행위 = 무엇을(계열) × 어디에(부위) × 어떻게(기법). 키 = 계열 × [하위 · 성분(J1 안 C)] × 부위 × 기법 · 원천에 있는 조합만 | _RESUME §2 10-27 · 10-29 「5단계 시작」 · 로그 step5 §3-1 |
| **계열** | 무엇을 — 공식 일반명 약제 · 장비 계열. 기준 = 교과서 · 임상 · 학회 문헌. 계열이 없으면 시술을 빼지 않고 계열을 늘림(N1~N10) | _RESUME §2 10-27 · 10-28 · 10-29 |
| **하위 계열** | 계열 안 매질 · 재료 축 · 주 1 + 보조. 단위 시술 키에는 「무엇을」을 바꾸는 계열만(M5 · M8 · M9 · M13 · M16 성분) | _RESUME §2 10-28 · 로그 step5 §3-1 |
| **기법** | 어떻게 — 큰 기법 + 세부 기법(K01~K13). 층 · 깊이 · 대상 근육 · 도구는 단위 시술 속성 · 펄스 · 박피 · 방식은 장비 속성 | _RESUME §2 10-28 J1 안 1 |
| **계열 기본 기법** | 계열이 따로 말하지 않을 때 쓰는 기법(default) · 함께 쓰는 기법(also) | step4 family_defaults |
| **부위** | 몸 겉에서 가리킬 수 있는 자리. 쪼개는 규칙 = ① 원천이 따로 부른다 ② 가능 시술 · 안전이 달라진다. 뼈 · 근육 · 혈관 · 층은 부위 아님 | _RESUME §2 10-27 · 10-28 |
| **부위 이름(일반인)** | 노드 이름 = 상담 용어 | _RESUME §2 10-28 「부위 노드 이름 2벌」 |
| **부위 이름(전문의)** | anatomical_name — 같은 겉자리의 의학 이름만 | _RESUME §2 10-28 |
| **묶음 부위** | 하위를 묶는 부위 노드 — 동의어 없음 · 단위 시술 키를 만들지 않음 · 부위 올라가기(R21)에서 통과 | 로그 step5 §3-2 · step7 site_rules.climb |
| **최상위 영역** | 3단계 트리에서 부모 없는 노드(얼굴 · 목(묶음) · 두피 · 바디 …) — 부위 올라가기 · 고민 영역의 경계 | step7-decisions site_rules.climb.regions · R21 · R22 |
| **특수 부위 「해당 없음」 · 「병변 단위」** | 해당 없음 = 전신 투여 · 병변 단위 = 병변 수 · 면적으로 매기는 시술. 부위 노드 없음 · 영역 검사 밖 | step5 rules.special_sites |
| **기본값 부위** | 부위 이름 없는 얼굴 계열 항목 = 얼굴 전체 + site_basis 「기본값」 표시(J2) | 로그 step5 §3-4 |
| **제품** | 허가 · 업체 · 규격을 가진 제품 · 장비. 이름 3칸(대표 한글 1 · 허가 이름은 허가 쪽에만 · 검색 이름[]) | _RESUME §2 10-27 |
| **라인 · 품목** | 라인 = 상위 제품 · 개별 품목 = 하위 제품 | _RESUME §2 10-27 ④ |
| **허가 상태** | 정상 · 허가번호 미확인(추천 포함) · 확인 불가 · 미허가 · 허가 취소(이력) · 허가 대상 아님(출처 있을 때만) | _RESUME §2 10-27 · 10-28 |
| **장비 이름 = 시술 동의어** | 장비 이름이 시술 이름으로 쓰이면 장비 노드는 두고 그 이름을 단위 시술 동의어로도 | _RESUME §2 10-27 |
| **패키지** | 이름 있는 단위 시술 묶음 — 일반 · 회차 · 병원 시그니처(추천 기본 제외). 구성은 원천에 적힌 만큼 | 로그 step6 §3 |
| **슬롯** | 패키지 구성 중 못 푼 자리 — 후보 전부 + 원천 질문 | 로그 step6 §3-2 |
| **추천 조합** | 원천이 고민 · 목적별로 적은 시술 조합(원천별 · 합치지 않음) — 사이트 「추천 패키지」 | _RESUME §2 10-28 U3 · 10-29 |
| **영업 문구** | salesPitch · upsellHook — 보관 · 기본 응답 제외 | step7 rules R9 |
| **고민** | 상태 이름 — taxonomy problem 「고민」 갈래 + 결정 노드(J8 · J10 · J14) | 로그 step7 §3-1 |
| **목적** | 시술이 하는 일 — 고민과 같은 말이면 그 고민에 붙음(R6) | step7 rules R6 |
| **중증도** | 고민의 정도 — 하위 고민이 있으면 하위로(주름) · 없으면 상위 + severity | step7 rules R18 |
| **고민 영역** | 고민(과 하위 고민 · 항목)의 앵커 부위들의 최상위 영역 합집합 — 앵커 부위 없는 엣지 · 조합 구성의 영역 밖 단위 시술을 뺌(목적 갈래 중분류는 안 넣음) | step7 rules R22 · site_rules.concern_region · 사용자 10-30 |
| **확인 조건** | 사람 쪽 조건 원장 · 시술 → 조건 엣지에 등급 | _RESUME §2 10-28 · 로그 step8 §3-10 |
| **등급 3분류** | 금기 · 주의 · 확인만(+ 확인만(고지)) — 원문 등급은 그대로 두고 덧붙임 | step8-decisions labels.grade3 |
| **조건 아닌 문장** | 상담 · 시술 준비 · 고지 · 효과 · 근거 수준 문장 — 확인 조건 엣지가 아니라 원문 보관(계열 대상은 계열 원문 속성) | step8 conditions.not_condition_rule · B8 |
| **피함(금기 조합)** | 고민 조건 금기 = 고민 → 단위 시술 엣지(concern_avoid) | step8-decisions U8-2 |
| **관계 주장** | 시술↔시술 엣지 안에 쌓는 원천 주장 한 줄 | 로그 step8 §3-1 |
| **시너지 · 순서 · 간격 · 금기** | 시술↔시술 엣지 하나의 주장 종류 — 「대신」은 대체(택 1) | _RESUME §2 10-26 · 로그 step8 §3-2 |
| **간격** | days [하한, 상한](일) · first(a\|b\|null) · same_day · open_high — 추천 · AI 는 edges[].resolved 의 이 칸만 읽음(10-30 · 원문 claims[].interval 은 근거) | step8 reading_contract |
| **합병증** | 예상 밖 이상 결과(혈관 폐색 · 감염 …) — complications.json severity moderate 이상 + U1 원문 serious · 원천 없는 계열은 gap | 사용자 10-29 · U1 · U2 · B1(10-30) |
| **부작용** | 흔한 예상 반응(멍 · 부기 · 홍반 …) — 계열 속성(safety.side_effects) · 제품 × 계열 · 단위 시술 값이 있으면 덮어씀(골드 계산) | 사용자 10-29 · U2 · B1(10-30) · step8 side_effect_rule |
| **위험지대** | 부위 × 계열의 혈관 · 신경 · 안전 층 위험 — 위험지대 주의 엣지 속성 | 로그 step8 §3-11 |
| **필수 고지** | 원문 그대로 보관(쪼개지 않음) · 계열 원문 속성 | _RESUME §2 10-28 |
| **근거 문장** | 계열 단위 문헌 문장 · field(moa · effects · adverse_effects) + class(B2 · 이 정본) | step8 evidence.statements · B2 |
| **근거 출처** | 문헌 · 웹 · 가이드. URL 없는 출처 문자열 = 웹 아님 · 「;」 URL 여럿 = multi_url | step8-decisions web_evidence_rule |
| **근거 강도** | 원문 등급만(숫자를 만들지 않음) | 로그 step8 §3-12 |
| **근거 약 · 중** | 판정 근거가 약하면 값을 넣고 「약」 + 확인 질문(open 아님) | _RESUME §2 10-28 |
| **충돌** | 원천끼리 다른 말 — 10-30 부터 하나로: 조건 다르면 나눔(R1 · 방향 포함) · 등급 더 엄격(R2) · 간격 더 긴 쪽(R3) · 같은 날 불가(R4) · 순서 반대만 순서 단정 안 함 + 의료진(R5) · 대기 더 긴 쪽(R6) · 원문은 alternatives | step8-decisions conflict_resolution · user_decisions 「충돌(10-30)」(D-13b 바꿈) |
| **조건부(단위 시술 미특정)** | 한정어 붙은 끝점이 묶음으로 열림 → default_apply false · 기본 상속 · 응답에서 뺌 | step8-decisions scope_rule |
| **하위 조건별 값** | 겉 칸을 비우고 options[].sub_condition 별 값을 읽음 | step8 F2 · reading_contract |
| **gap** | 원천이 없어 비운 것 — 「없음 = 안전」 아님(합병증 gap 계열 · PIH gap · 이 부위 단위 시술 없음) | 로그 step8 §6 · step5 pih_gap_units |
| **끝점 묶음** | 끝점이 하나로 안 좁혀진 것 — 노드가 아니라 엣지 endpoints.candidates[] | U3 · B3(10-30) |
| **후보 전부** | 이름이 여럿을 가리키면 고르지 않고 후보 전부 + 표시 — 외부 LLM 이 고르거나 되묻기 | _RESUME §2 10-27 W-1 |
| **부위로 내림 · 올라가기** | 부위가 있으면 그 부위(또는 하위)의 단위 시술 · 없으면 R21 상위 노드 자신으로 올라가며(영역 경계 안 · 영역 「전체」 노드까지) · 그래도 없으면 계열만 + 「이 부위 단위 시술 없음」 | step7 rules R21 · site_rules.climb |
| **원천 질문** | 규칙으로 하나로 안 정해지는 것만 병원 · 의료진 · 원장님에게 — 값은 추천값 · 답 오면 그 행만 | step8 U8-1 · _RESUME §2 10-29 |

## 4. 사전 하나(B5)

표현 **2053** · 대상 2991 · 겹침 208 · 7↔8단계 수준 합침(F) 31 · 정규화 「NFKC → 라틴 악센트 접기(NFKD 결합 부호 제거 · NFC) → 입력 접기 fold(「쳐짐」 → 「처짐」 — 10-27 원천 수정 결정과 같은 방향 · 사전 · 질의 양쪽) → 공백 제거 → 괄호 ( ) [ ] 지움(안 글자는 남김 — 「코그(Cog)」 = 「코그 Cog」) → 전부 소문자」

- 행 = `expr` · `norm` · `variants[]` · `targets[{id, qualifier, reasons[]}]` · `sources[]` · `mode`(하나 · 전부 · 후보) · `ambiguous` · `collision` · `prefer`
- 조사(semantic-research)의 겹침 147 은 F 갈래 21 을 겹침으로 셌음 — 정본은 F 를 qualifier 로 합쳐 겹침에서 빠짐 · 셈은 이 파일에서 다시 셈

| 겹침 갈래 | 셈 | 처리 | 뜻 |
|---|---|---|---|
| A | 30 | 전부 | 묶음 이름 → 고민 · 목적 여럿(R12) — 대상 전부에 적용 |
| B | 42 | 후보 | 장비 · 제품 이름 = 단위 시술 동의어(10-27) — 제품 · 시술 후보 전부 + 모호 |
| C | 4 | 후보 | 브랜드 이름이 계열 낱말로도 — 「보톡스」 = 계열 · 제품 둘 다(10-27) · 나머지 같은 처리 |
| D | 15 | 후보 | 같은 검색 이름이 제품 둘(라인 · 같은 허가) — 후보 전부 |
| E | 28 | 후보 | 같은 말이 단위 시술 여럿 — 후보 전부(모호 표시) |
| G | 1 | 후보 | 부위 이름 = 단위 시술 원장 이름(「사각턱」 …) — 부위 · 시술 후보 |
| H | 2 | 후보 | 기법 이름 = 단위 시술 이름(서브시전 · 펀치 · 압출) — 기법 · 시술 후보 |
| I | 1 | 전부 | 나열 문자열(「볼/관자놀이」)이 부위 둘 — 대상 전부 |
| J | 85 | 후보 | 종류가 다른 노드끼리(고민 · 계열 · 목적 · 부위 · 시술) — 후보 전부 · 고민 이름이 시술 동의어 칸에 든 것은 7단계 W3 교훈대로 고민 우선 표시 |

출처별 원소: patient-education categories[].patient_name 17 · step1 items[].2_names.display_name 354 · step1 items[].2_names.search_names[] 544 · step2 families[].name 27 · step2 families[].synonyms[] 73 · step3 nodes[].name 53 · step3 nodes[].synonyms[] 74 · step4 nodes[].medical_name 26 · step4 nodes[].name 26 · step5 device_name_synonyms[] 36 · step5 ledger[].name 520 · step5 market[].name 112 · step5 units[].name 162 · step5 units[].synonyms[] 323 · step6 packages[].name 24 · step6 packages[].synonyms[] 25 · step7 concerns.*.name 26 · step7 concerns.subcategories[].concern 28 · step7 concerns.subcategories[].source_label 45 · step7 correspondence[] 226 · step7 edges[③].ccs[] 80 · step7 purposes[].aliases[] 16 · step7 purposes[].name 13 · step7-decisions concern_synonyms[] 6 · step7-decisions resolver.fam_kw[] 78 · step8 conditions.nodes[].name 53 · step8-decisions resolver.alias[] 65

**7 · 8단계 같은 낱말 → 8단계 수준(계열 + qualifier)으로 합침**

| 낱말 | 7단계 | 8단계(정본) |
|---|---|---|
| 지방흡입 | {"families": null, "units": ["U5-162"]} | {"family": "N10"} |
| 보톡스 | {"families": ["M1"], "units": null} | {"family": "M1"} |
| CaHA | {"families": ["M3"], "units": null} | {"family": "M3", "sub": "CaHA"} |
| 바이오스티뮬 | {"families": ["M3"], "units": null} | {"family": "M3"} |
| 필러 | {"families": ["M2"], "units": null} | {"family": "M2"} |
| 스킨부스터 | {"families": ["M4"], "units": null} | {"family": "M4"} |
| PRP | {"families": null, "units": ["U5-020", "U5-042"]} | {"family": "M5", "sub": "혈소판 농축물(PRP·PRF)"} |
| 엑소좀 | {"families": null, "units": ["U5-019", "U5-040", "U5-142"]} | {"family": "M5", "sub": "엑소좀"} |
| 지방이식 | {"families": ["M6"], "units": null} | {"family": "M6"} |
| 실리프팅 | {"families": ["M7"], "units": null} | {"family": "M7"} |
| LED | {"families": null, "units": ["U5-050", "U5-043"]} | {"family": "M8", "sub": "LED"} |
| CO2 | {"families": null, "units": ["U5-028"]} | {"family": "M8", "sub": "탄산가스 레이저"} |
| 프락셔널 | {"families": null, "units": ["U5-026", "U5-027", "U5-028", "U5-029"]} | {"family": "M8", "technique": "K04b"} |
| 토닝 | {"families": null, "units": ["U5-023", "U5-024", "U5-025"]} | {"family": "M8", "technique": "K04a"} |
| 제모 | {"families": null, "units": ["U5-100", "U5-101"]} | {"family": "M8", "note": "제모"} |
| 다이오드 | {"families": null, "units": ["U5-100", "U5-101"]} | {"family": "M8", "sub": "반도체 레이저"} |
| 알렉산드라이트 | {"families": null, "units": ["U5-100", "U5-101"]} | {"family": "M8", "sub": "알렉산드라이트 레이저"} |
| 혈관레이저 | {"families": null, "units": ["U5-141", "U5-099", "U5-138"]} | {"family": "M8", "note": "혈관"} |
| 니들RF | {"families": ["M11"], "units": null} | {"family": "M11"} |
| HIFU | {"families": null, "units": ["U5-102", "U5-103"]} | {"family": "M9", "sub": "HIFU"} |
| 써마지 | {"families": null, "units": ["U5-091", "U5-104"]} | {"units": ["U5-091", "U5-104"]} |
| RF | {"families": null, "units": ["U5-091", "U5-104"]} | {"family": "M9", "sub": "RF"} |
| MTS | {"families": ["M12"], "units": null} | {"family": "M12"} |
| 마이크로니들 | {"families": ["M12"], "units": null} | {"family": "M12"} |
| 플라즈마 | {"families": ["M13"], "units": null} | {"family": "M13"} |
| 크라이오 | {"families": ["M14"], "units": null} | {"family": "M14"} |
| 필링 | {"families": null, "units": ["U5-034"]} | {"family": "M15", "technique": "K09"} |
| 비타민C | {"families": null, "units": ["U5-052"]} | {"none": "시술 아님(비타민C 도포 = 외용제 — 7단계 not_procedure 「외용제」) · 단 U5-036 「이온토포레시스 (비타민C)」와 구분 필요"} |
| 카복시 | {"families": null, "units": ["U5-123"]} | {"family": "N2"} |
| 줄기세포 | {"families": ["M17"], "units": null} | {"family": "M17"} |
| 레이저 | {"families": ["M8"], "units": null} | {"family": "M8"} |

**보고(7단계 결정은 이번에 안 바꿈)**

- 비타민C: 7단계 = 단위 시술 · 8단계 = 시술 아님 — 정본은 8단계(시술 아님) 따르고 7단계 결정 고칠 거리로 보고(이번에 안 바꿈)

**겹침 행**

| 표현 | 대상 | 갈래 | 처리 |
|---|---|---|---|
| AAPE | product:auto-M17-1775364775191 · unit_procedure:U5-143 · unit_procedure:U5-143+{"ledger": "auto-M17-1775364775191", "dest": "제품 + 단위 시술"} | B | 후보 |
| ASCE+엑소좀 | product:M4-3-1 · unit_procedure:U5-142 · unit_procedure:U5-142+{"ledger": "M4-3-1", "dest": "제품 + 단위 시술"} | B | 후보 |
| CO2프락셔널 | concern:P9-1+{"cc": "CO2프락셔널"} · unit_procedure:U5-028 · unit_procedure:U5-028+{"ledger": "M8-2-1", "dest": "단위 시술"} | J | 후보 · concern 우선 |
| CoolSculpting Elite System | product:M14-1-1 · product:auto-M14-1775363067062 | D | 후보 |
| CoolSculpting System(Zeltiq System) | product:M14-1-1 · product:auto-M14-1775363067062 | D | 후보 |
| DNA리셋프로그램 | family:M9+{"ledger": "auto-42-1774737181584", "dest": "6단계 패키지", "to": "병원 메뉴 패키지 — 구성 단위 시술은 6단계(DEC-003 OQ-313 · U1)"} · package:P6-09 | J | 후보 |
| DOUBLO-GOLD™ | product:M9-1-5 · product:M9-1-6 | D | 후보 |
| eCO2 | product:auto-M8-1775362603297 · product:auto-M8-1775364775119 | D | 후보 |
| eCO2 EVOLUTION＆SURGICAL | product:auto-M8-1775362603297 · product:auto-M8-1775364775119 | D | 후보 |
| eCO2 Plus | product:auto-M8-1775362603297 · product:auto-M8-1775364775119 | D | 후보 |
| EMSCULPT NEO | product:M10-2-1 · product:M10-2-2 | D | 후보 |
| EMS 바디 (팔뚝/허벅지) | unit_procedure:U5-108 · unit_procedure:U5-108+{"market_role": "이름"} · unit_procedure:U5-109 · unit_procedure:U5-109+{"market_role": "이름"} | E | 후보 |
| FUE | concern:P13+{"cc": "FUE"} · unit_procedure:U5-161 | J | 후보 · concern 우선 |
| FUT | concern:P13+{"cc": "FUT"} · unit_procedure:U5-161 | J | 후보 · concern 우선 |
| GPC주사 | unit_procedure:U5-070+{"ledger": "auto-M16-1775403176936", "dest": "단위 시술"} · unit_procedure:U5-071+{"ledger": "auto-M16-1775403176936", "dest": "단위 시술"} · unit_procedure:U5-072+{"ledger": "auto-M16-1775403176936", "dest": "단위 시술"} · unit_procedure:U5-073+{"ledger": "auto-M16-1775403176936", "dest": "단위 시술"} · unit_procedure:U5-074+{"ledger": "auto-M16-1775403176936", "dest": "단위 시술"} · unit_procedure:U5-077+{"ledger": "auto-M16-1775403176936", "dest": "단위 시술"} · unit_procedure:U5-078+{"ledger": "auto-M16-1775403176936", "dest": "단위 시술"} · unit_procedure:U5-079+{"ledger": "auto-M16-1775403176936", "dest": "단위 시술"} · unit_procedure:U5-080+{"ledger": "auto-M16-1775403176936", "dest": "단위 시술"} | E | 후보 |
| Hair | concern:P10 · concern:P13 | A | 전부 |
| Hair → 모발 · 체모 | concern:P10 · concern:P13 | A | 전부 |
| IPL | concern:P5-2+{"cc": "IPL"} · family:M8 · unit_procedure:U5-030 · unit_procedure:U5-030+{"ledger": "M8-3-1", "dest": "단위 시술"} | J | 후보 · concern 우선 |
| Joule BBL SkinTyte II | product:auto-29-1774737181584 · product:auto-32-1774737181584 | D | 후보 |
| LDM | product:M15-4-1 · product:M15-4-1+{"ledger": "M15-4-1", "dest": "제품"} · unit_procedure:U5-036 | B | 후보 |
| LDM 초음파 관리 | product:M15-4-1 · product:M15-4-1+{"ledger": "auto-M16-1775363074847", "dest": "제품"} · unit_procedure:U5-036 · unit_procedure:U5-036+{"market_role": "이름"} | B | 후보 |
| Liftera Cool | product:M9-1-8 · product:auto-37-1774737181584 | D | 후보 |
| lifting | concern:P3 · concern:P4-1 · purpose:PU-01 | A | 전부 |
| lifting / 리프팅 비교 | concern:P3 · concern:P4-1 · purpose:PU-01 | A | 전부 |
| LLLT | concern:P13+{"cc": "LLLT"} · unit_procedure:U5-039 | J | 후보 · concern 우선 |
| M16-1 미백/항산화 | concern:P5 · purpose:PU-09 | A | 전부 |
| M16-3 재생/면역 | concern:P4-1 · purpose:PU-03 · purpose:PU-11 | A | 전부 |
| NAD+ 수액 | concern:P4-3+{"cc": "NAD+수액"} · unit_procedure:U5-063 | J | 후보 · concern 우선 |
| Oligio X | product:M9-2-2 · product:auto-M9-1775361486532 | D | 후보 |
| PCA실 | unit_procedure:U5-022+{"ledger": "auto-M7-1775361902160", "dest": "다른 단계 이름"} · unit_procedure:U5-097+{"ledger": "auto-M7-1775361902160", "dest": "다른 단계 이름"} · unit_procedure:U5-098+{"ledger": "auto-M7-1775361902160", "dest": "다른 단계 이름"} · unit_procedure:U5-122+{"ledger": "auto-M7-1775361902160", "dest": "다른 단계 이름"} | E | 후보 |
| PCL | family:M7 · unit_procedure:U5-022+{"ledger": "M7-1-2", "dest": "다른 단계 이름"} · unit_procedure:U5-097+{"ledger": "M7-1-2", "dest": "다른 단계 이름"} · unit_procedure:U5-098+{"ledger": "M7-1-2", "dest": "다른 단계 이름"} · unit_procedure:U5-122+{"ledger": "M7-1-2", "dest": "다른 단계 이름"} | J | 후보 |
| PDO | family:M7 · unit_procedure:U5-022+{"ledger": "M7-1-1", "dest": "다른 단계 이름"} · unit_procedure:U5-097+{"ledger": "M7-1-1", "dest": "다른 단계 이름"} · unit_procedure:U5-098+{"ledger": "M7-1-1", "dest": "다른 단계 이름"} · unit_procedure:U5-122+{"ledger": "M7-1-1", "dest": "다른 단계 이름"} | J | 후보 |
| PDT | concern:P6-1+{"cc": "PDT"} · unit_procedure:U5-049 | J | 후보 · concern 우선 |
| PLCL | unit_procedure:U5-022+{"ledger": "M7-1-3", "dest": "다른 단계 이름"} · unit_procedure:U5-097+{"ledger": "M7-1-3", "dest": "다른 단계 이름"} · unit_procedure:U5-098+{"ledger": "M7-1-3", "dest": "다른 단계 이름"} · unit_procedure:U5-122+{"ledger": "M7-1-3", "dest": "다른 단계 이름"} | E | 후보 |
| PLLA | unit_procedure:U5-022+{"ledger": "auto-26-1774737181584", "dest": "다른 단계 이름"} · unit_procedure:U5-097+{"ledger": "auto-26-1774737181584", "dest": "다른 단계 이름"} · unit_procedure:U5-098+{"ledger": "auto-26-1774737181584", "dest": "다른 단계 이름"} · unit_procedure:U5-122+{"ledger": "auto-26-1774737181584", "dest": "다른 단계 이름"} | E | 후보 |
| PLLA+PCL복합실 | unit_procedure:U5-022+{"ledger": "auto-M7-1775364775160", "dest": "다른 단계 이름"} · unit_procedure:U5-097+{"ledger": "auto-M7-1775364775160", "dest": "다른 단계 이름"} · unit_procedure:U5-098+{"ledger": "auto-M7-1775364775160", "dest": "다른 단계 이름"} · unit_procedure:U5-122+{"ledger": "auto-M7-1775364775160", "dest": "다른 단계 이름"} | E | 후보 |
| PRP | family:M5 · family:M5+{"sub": "혈소판 농축물(PRP·PRF)"} · unit_procedure:U5-020 · unit_procedure:U5-020+{"ledger": "M5-1-1", "dest": "단위 시술"} | J | 후보 |
| Q-스위치 | unit_procedure:U5-023 · unit_procedure:U5-131 | E | 후보 |
| Q스위치 | unit_procedure:U5-023 · unit_procedure:U5-131 | E | 후보 |
| regeneration | concern:P4-1 · purpose:PU-03 | A | 전부 |
| SP 다이나미스 | product:auto-M8-1775360944918 · unit_procedure:U5-099 | B | 후보 |
| StarWalker | product:auto-M8-1775364775120 · product:auto-M8-1775364775128 | D | 후보 |
| subcision | technique:K12a · unit_procedure:U5-045 | H | 후보 |
| tightening | concern:P4-1 · purpose:PU-02 | A | 전부 |
| Ultherapy Prime | product:M9-1-1 · product:M9-1-2 | D | 후보 |
| ULTRAcel Q+ | product:M9-1-9 · product:auto-M9-1775362627041 · product:auto-M9-1775363043305 | D | 후보 |
| V라인주사 | unit_procedure:U5-070+{"ledger": "auto-M16-1775402996209", "dest": "단위 시술"} · unit_procedure:U5-071+{"ledger": "auto-M16-1775402996209", "dest": "단위 시술"} · unit_procedure:U5-072+{"ledger": "auto-M16-1775402996209", "dest": "단위 시술"} · unit_procedure:U5-073+{"ledger": "auto-M16-1775402996209", "dest": "단위 시술"} · unit_procedure:U5-074+{"ledger": "auto-M16-1775402996209", "dest": "단위 시술"} | E | 후보 |
| V빔 | concern:P8-1+{"cc": "V빔"} · unit_procedure:U5-141 | J | 후보 · concern 우선 |
| 건선 | concern:P14-4+{"cc": "건선"} · unit_procedure:U5-157 | J | 후보 · concern 우선 |
| 겨드랑이/팔/다리 | concern:P10+{"cc": "겨드랑이/팔/다리"} · unit_procedure:U5-100 · unit_procedure:U5-146 · unit_procedure:U5-147 | J | 후보 · concern 우선 |
| 경화요법 | concern:P8-3+{"taxonomy_entry": "auto-127-1774737181584"} · unit_procedure:U5-158 | J | 후보 · concern 우선 |
| 고주파 | unit_procedure:U5-091 · unit_procedure:U5-104 | E | 후보 |
| 광대 | concern:P11+{"taxonomy_entry": "P11-4"} · site:site.zygoma | J | 후보 |
| 근육강화 | concern:P12+{"taxonomy_entry": "P12-2"} · purpose:PU-08 | A | 전부 |
| 기타 엑소좀 | unit_procedure:U5-019+{"ledger": "auto-25-1774737181584", "dest": "다른 단계 이름"} · unit_procedure:U5-040+{"ledger": "auto-25-1774737181584", "dest": "다른 단계 이름"} · unit_procedure:U5-142+{"ledger": "auto-25-1774737181584", "dest": "다른 단계 이름"} | E | 후보 |
| 꿀광토닝 | family:M8+{"ledger": "auto-M8-1775402572157", "dest": "6단계 패키지", "to": "병원 메뉴 패키지 — 구성 단위 시술은 6단계(DEC-003 OQ-313 · U1)"} · package:P6-05 | J | 후보 |
| 넥큐레이션 | family:M1+{"ledger": "auto-6-1774737181584", "dest": "6단계 패키지", "to": "병원 메뉴 패키지 — 구성 단위 시술은 6단계(DEC-003 OQ-313 · U1)"} · package:P6-03 | J | 후보 |
| 눈밑꺼짐 → 꺼짐 · 주름 · 볼륨 | none:고민 노드 아님(트리 항목)+{"taxonomy_entry": "P1-5"} · purpose:PU-04 | J | 후보 |
| 니들RF | concern:P7-2+{"cc": "니들RF"} · concern:P9-1+{"cc": "니들RF"} · family:M11 | J | 후보 |
| 다빼주사 | unit_procedure:U5-070+{"ledger": "auto-M16-1775403076220", "dest": "단위 시술"} · unit_procedure:U5-071+{"ledger": "auto-M16-1775403076220", "dest": "단위 시술"} · unit_procedure:U5-072+{"ledger": "auto-M16-1775403076220", "dest": "단위 시술"} · unit_procedure:U5-073+{"ledger": "auto-M16-1775403076220", "dest": "단위 시술"} · unit_procedure:U5-074+{"ledger": "auto-M16-1775403076220", "dest": "단위 시술"} | E | 후보 |
| 다크서클필러 → 다크서클 | none:고민 노드 아님(트리 항목)+{"taxonomy_entry": "P1-5"} · purpose:PU-04 | J | 후보 |
| 다한증 | concern:P14-3 · unit_procedure:U5-010 · unit_procedure:U5-010+{"ledger": "M1-3-7", "dest": "단위 시술"} · unit_procedure:U5-011 · unit_procedure:U5-011+{"ledger": "M1-3-7", "dest": "단위 시술"} · unit_procedure:U5-012 · unit_procedure:U5-012+{"ledger": "M1-3-7", "dest": "단위 시술"} | J | 후보 · concern 우선 |
| 더마펜4 | product:auto-M12-1775363026852 · product:auto-M12-1775363026852+{"ledger": "auto-M12-1775363026852", "dest": "제품"} · unit_procedure:U5-032 | B | 후보 |
| 더블로 골드 | product:M9-1-5 · product:M9-1-6 · product:M9-1-6+{"ledger": "M9-1-6", "dest": "제품"} · unit_procedure:U5-102 | B | 후보 |
| 도자기피부관리 | family:M15+{"ledger": "auto-M15-1775402736448", "dest": "6단계 패키지", "to": "병원 메뉴 패키지 — 구성 단위 시술은 6단계(DEC-003 OQ-313 · U1)"} · package:P6-13 | J | 후보 |
| 두피 PRP | concern:P13+{"cc": "두피PRP"} · unit_procedure:U5-042 · unit_procedure:U5-042+{"ledger": "auto-M15-1775361179322", "dest": "단위 시술"} | J | 후보 · concern 우선 |
| 두피스케일링 | concern:P13+{"cc": "두피스케일링"} · unit_procedure:U5-044 · unit_procedure:U5-044+{"ledger": "auto-M15-1775364775177", "dest": "단위 시술"} | J | 후보 · concern 우선 |
| 두피 엑소좀 | concern:P13+{"cc": "두피엑소좀"} · unit_procedure:U5-040 | J | 후보 · concern 우선 |
| 듀오 하이드로젠 | product:new-DEV-041 · unit_procedure:U5-035 | B | 후보 |
| 라이넥 | product:M16-3-1 · unit_procedure:U5-128 | B | 후보 |
| 래디어스 | product:M3-2-1 · product:M3-2-1+{"ledger": "M3-2-1", "dest": "제품"} · unit_procedure:U5-090 | B | 후보 |
| 레이저토닝 | concern:P5-1+{"cc": "레이저토닝"} · unit_procedure:U5-023 · unit_procedure:U5-023+{"ledger": "M8-1-1", "dest": "단위 시술"} | J | 후보 · concern 우선 |
| 리쥬란 | product:M4-1-1 · unit_procedure:U5-018 | B | 후보 |
| 리쥬란 아이 | product:M4-1-2 · product:M4-1-2+{"ledger": "M4-1-2", "dest": "제품"} · unit_procedure:U5-018 | B | 후보 |
| 리프팅 | concern:P3 · concern:P4-1 · family:M9 · purpose:PU-01 | J | 후보 |
| 메조테라피 | family:M4 · technique:K01a | J | 후보 |
| 멜스몬 | product:auto-M16-1775364775098 · unit_procedure:U5-128 | B | 후보 |
| 모노 | unit_procedure:U5-022+{"ledger": "M7-2-2", "dest": "다른 단계 이름"} · unit_procedure:U5-097+{"ledger": "M7-2-2", "dest": "다른 단계 이름"} · unit_procedure:U5-098+{"ledger": "M7-2-2", "dest": "다른 단계 이름"} · unit_procedure:U5-122+{"ledger": "M7-2-2", "dest": "다른 단계 이름"} | E | 후보 |
| 모르페우스8 | product:M11-1-4 · product:M11-1-4+{"ledger": "M11-1-4", "dest": "제품"} · unit_procedure:U5-110 | B | 후보 |
| 모발이식 | concern:P13+{"taxonomy_entry": "P13-4"} · family:N9 · unit_procedure:U5-161 | J | 후보 · concern 우선 |
| 목주름/턱선 | unit_procedure:U5-016 · unit_procedure:U5-016+{"ledger": "auto-3-1774737181584", "dest": "단위 시술"} · unit_procedure:U5-017 · unit_procedure:U5-017+{"ledger": "auto-3-1774737181584", "dest": "단위 시술"} | E | 후보 |
| 미라드라이 | concern:P14-3+{"cc": "미라드라이"} · unit_procedure:U5-153 | J | 후보 · concern 우선 |
| 민트리프트 | product:M7-3-1 · product:M7-3-1+{"ledger": "M7-3-1", "dest": "제품"} · unit_procedure:U5-022 | B | 후보 |
| 바디 | concern:P12 · site:site.body | J | 후보 |
| 바디리프팅 → 라인 · 리프팅 · 탄력 | concern:P12-3 · concern:P3-3 · purpose:PU-01 | A | 전부 |
| 바디써마지 | concern:P12-3+{"cc": "바디써마지"} · unit_procedure:U5-152 | J | 후보 · concern 우선 |
| 바디인모드 | concern:P12-3+{"cc": "바디인모드"} · unit_procedure:U5-152 | J | 후보 · concern 우선 |
| 바디큐레이션 | family:M1+{"ledger": "auto-5-1774737181584", "dest": "6단계 패키지", "to": "병원 메뉴 패키지 — 구성 단위 시술은 6단계(DEC-003 OQ-313 · U1)"} · package:P6-02 | J | 후보 |
| 백반증 | concern:P14-4+{"cc": "백반증"} · unit_procedure:U5-156 | J | 후보 · concern 우선 |
| 백옥주사 | concern:P5-4+{"cc": "백옥주사"} · unit_procedure:U5-051 · unit_procedure:U5-051+{"ledger": "M16-1-1", "dest": "단위 시술"} | J | 후보 · concern 우선 |
| 보톡스 | concern:P14-3+{"cc": "보톡스"} · family:M1 · product:M1-2-1 | J | 후보 |
| 볼/관자놀이 | concern:P11+{"taxonomy_entry": "P11-5"} · site:site.cheek-group · site:site.temple | J | 후보 |
| 볼뉴머 | product:M9-2-3 · product:M9-2-3+{"ledger": "M9-2-3", "dest": "제품"} · product:M9-2-3+{"ledger": "auto-M4-1775362490962", "dest": "제품"} · unit_procedure:U5-091 · unit_procedure:U5-091+{"market_role": "이름"} | B | 후보 |
| 볼륨실 | unit_procedure:U5-022+{"ledger": "M7-2-3", "dest": "다른 단계 이름"} · unit_procedure:U5-097+{"ledger": "M7-2-3", "dest": "다른 단계 이름"} · unit_procedure:U5-098+{"ledger": "M7-2-3", "dest": "다른 단계 이름"} · unit_procedure:U5-122+{"ledger": "M7-2-3", "dest": "다른 단계 이름"} | E | 후보 |
| 볼륨 회복 | concern:P4+{"taxonomy_entry": "P4-2"} · purpose:PU-04 | A | 전부 |
| 브라이트닝레이저 | family:M8+{"ledger": "auto-M8-1775402586665", "dest": "6단계 패키지", "to": "병원 메뉴 패키지 — 구성 단위 시술은 6단계(DEC-003 OQ-313 · U1)"} · package:P6-06 | J | 후보 |
| 브이빔 | product:M8-4-1 · unit_procedure:U5-141 · unit_procedure:U5-141+{"ledger": "M8-4-1", "dest": "제품 + 단위 시술"} | B | 후보 |
| 브이빔 퍼펙타 | product:auto-M8-1775364775121 · unit_procedure:U5-141 · unit_procedure:U5-141+{"ledger": "auto-M8-1775364775121", "dest": "제품 + 단위 시술"} | B | 후보 |
| 브이올렛 | concern:P11-2+{"cc": "브이올렛"} · family:N1 · product:auto-M16-1775403016892 · product:auto-M16-1775403016892+{"ledger": "auto-M16-1775403016892", "dest": "제품"} | J | 후보 |
| 비키니 | concern:P10+{"cc": "비키니"} · site:site.bikini · unit_procedure:U5-148 | J | 후보 · concern 우선 |
| 비타민C주사 | concern:P5-4+{"cc": "비타민C주사"} · unit_procedure:U5-052 | J | 후보 · concern 우선 |
| 빼당주사 | unit_procedure:U5-070 · unit_procedure:U5-070+{"ledger": "auto-M16-1775403176937", "dest": "단위 시술"} · unit_procedure:U5-073 · unit_procedure:U5-073+{"ledger": "auto-M16-1775403176937", "dest": "단위 시술"} · unit_procedure:U5-074 · unit_procedure:U5-074+{"ledger": "auto-M16-1775403176937", "dest": "단위 시술"} | E | 후보 |
| 사각턱 | concern:P11+{"taxonomy_entry": "P11-1"} · site:site.masseter · unit_procedure:U5-006 · unit_procedure:U5-006+{"ledger": "M1-3-2", "dest": "단위 시술"} | J | 후보 · concern 우선 |
| 사각턱 보톡스 | concern:P11+{"cc": "사각턱보톡스"} · unit_procedure:U5-006 | J | 후보 · concern 우선 |
| 색소/기미 | concern:P5 · concern:P5-1 | A | 전부 |
| 서브시전 | concern:P7-3+{"cc": "서브시전"} · concern:P9-1+{"cc": "서브시전"} · technique:K12a · unit_procedure:U5-045 · unit_procedure:U5-045+{"ledger": "auto-M15-1775361858045", "dest": "단위 시술"} | J | 후보 · concern 우선 |
| 서브시전 [유착 해제] | concern:P7-3+{"taxonomy_entry": "auto-121-1774737181584"} · concern:P9-1+{"taxonomy_entry": "auto-128-1774737181584"} | A | 전부 |
| 성장호르몬 주사 | family:N6 · unit_procedure:U5-129 · unit_procedure:U5-129+{"ledger": "auto-M16-1775364775099", "dest": "단위 시술"} | J | 후보 |
| 셀리부트프로그램 | family:M9+{"ledger": "auto-41-1774737181584", "dest": "6단계 패키지", "to": "병원 메뉴 패키지 — 구성 단위 시술은 6단계(DEC-003 OQ-313 · U1)"} · package:P6-08 | J | 후보 |
| 소프웨이브 | product:auto-40-1774737181584 · unit_procedure:U5-140 · unit_procedure:U5-140+{"ledger": "auto-40-1774737181584", "dest": "제품 + 단위 시술"} | B | 후보 |
| 수염/가슴/등 | concern:P10+{"cc": "수염/가슴/등"} · unit_procedure:U5-149 · unit_procedure:U5-150 · unit_procedure:U5-151 | J | 후보 · concern 우선 |
| 슈링크 | product:M9-1-3 · product:M9-1-3+{"ledger": "M9-1-3", "dest": "제품"} · unit_procedure:U5-102 · unit_procedure:U5-103 | B | 후보 |
| 슈링크 유니버스 | product:M9-1-4 · product:M9-1-4+{"ledger": "M9-1-4", "dest": "제품"} · unit_procedure:U5-102 · unit_procedure:U5-103 | B | 후보 |
| 스컬트라 | family:M3 · product:M3-1-1 · product:M3-1-1+{"ledger": "M3-1-1", "dest": "제품"} · unit_procedure:U5-090 | B | 후보 |
| 스케일링 | unit_procedure:U5-035 · unit_procedure:U5-044 | E | 후보 |
| 스킨보톡스 | concern:P6-2+{"cc": "스킨보톡스"} · concern:P7-1+{"cc": "스킨보톡스"} · unit_procedure:U5-009 · unit_procedure:U5-009+{"ledger": "M1-3-5", "dest": "단위 시술"} | J | 후보 · concern 우선 |
| 스킨부스터오마카세 | family:M15+{"ledger": "auto-M15-1775402736452", "dest": "6단계 패키지", "to": "병원 메뉴 패키지 — 구성 단위 시술은 6단계(DEC-003 OQ-313 · U1)"} · package:P6-16 | J | 후보 |
| 스타워커 | product:auto-M8-1775364775120 · product:auto-M8-1775364775120+{"ledger": "auto-M8-1775364775120", "dest": "제품"} · product:auto-M8-1775364775128 | D | 후보 |
| 승모근 | concern:P11+{"taxonomy_entry": "P11-3"} · site:site.trapezius · unit_procedure:U5-007 · unit_procedure:U5-007+{"ledger": "M1-3-3", "dest": "단위 시술"} · unit_procedure:U5-007+{"market_role": "이름"} | J | 후보 · concern 우선 |
| 승모근 보톡스 | concern:P11+{"cc": "승모근보톡스"} · unit_procedure:U5-007 | J | 후보 · concern 우선 |
| 시크릿 | product:M11-1-2 · unit_procedure:U5-110 | B | 후보 |
| 시크릿 RF | product:M11-1-2 · product:M11-1-2+{"ledger": "M11-1-2", "dest": "제품"} · unit_procedure:U5-110 | B | 후보 |
| 실리콘시트 | concern:P9-3+{"cc": "실리콘시트"} · family:M15+{"ledger": "auto-M15-1775361864704", "dest": "값", "to": "값 — M15 하위 「외용제」 성분 값 · 사후관리 권장 제품(F9 · 버림 0)"} | J | 후보 |
| 써마지 | unit_procedure:U5-091 · unit_procedure:U5-104 | E | 후보 |
| 써마지 FLX | product:M9-2-1 · product:M9-2-1+{"ledger": "M9-2-1", "dest": "제품"} · unit_procedure:U5-091 · unit_procedure:U5-104 | B | 후보 |
| 아그네스 | concern:P6-2+{"cc": "아그네스"} · concern:P7-1+{"cc": "아그네스"} · family:M11 · product:auto-M11-1775364775142 · product:auto-M11-1775364775142+{"ledger": "auto-M11-1775364775142", "dest": "제품"} | J | 후보 |
| 아쿠아필 | product:M15-2-1 · product:M15-2-1+{"ledger": "M15-2-1", "dest": "제품"} · unit_procedure:U5-035 | B | 후보 |
| 아큐주사 | unit_procedure:U5-070+{"ledger": "auto-M16-1775403176935", "dest": "단위 시술"} · unit_procedure:U5-071+{"ledger": "auto-M16-1775403176935", "dest": "단위 시술"} · unit_procedure:U5-072+{"ledger": "auto-M16-1775403176935", "dest": "단위 시술"} · unit_procedure:U5-073+{"ledger": "auto-M16-1775403176935", "dest": "단위 시술"} · unit_procedure:U5-074+{"ledger": "auto-M16-1775403176935", "dest": "단위 시술"} | E | 후보 |
| 아큐탄 | family:M15+{"ledger": "auto-M15-1775361951923", "dest": "시술 아님", "to": "처방약(경구 이소트레티노인) — 1단계 제품 행 그대로 · 단위 시술 없음"} · product:auto-M15-1775361951923 | C | 후보 |
| 알렉 | unit_procedure:U5-100 · unit_procedure:U5-101 | E | 후보 |
| 알렉산드라이트 | family:M8+{"sub": "알렉산드라이트 레이저"} · unit_procedure:U5-024+{"ledger": "auto-M8-1775361951910", "dest": "다른 단계 이름"} · unit_procedure:U5-026+{"ledger": "auto-M8-1775361951910", "dest": "다른 단계 이름"} | J | 후보 |
| 알렉스필 | family:M15+{"ledger": "auto-M15-1775401780659", "dest": "원장님 문의", "to": "2단계 pending_director — family null · 추천 제외 그대로(F0 상태) · 답 오면 이 행만 5단계 판정"} · product:auto-M15-1775401780659 | C | 후보 |
| 압출 | concern:P6-1+{"cc": "압출"} · technique:K12c · unit_procedure:U5-048 | J | 후보 · concern 우선 |
| 약물치료 | concern:P13+{"taxonomy_entry": "P13-3"} · concern:P6-1+{"cc": "약물치료"} | A | 전부 |
| 얼굴 | concern:P10+{"taxonomy_entry": "P10-1"} · site:site.face | J | 후보 |
| 에코2 | product:auto-M8-1775362603297 · product:auto-M8-1775362603297+{"ledger": "auto-M8-1775362603297", "dest": "제품"} · product:auto-M8-1775364775119 | D | 후보 |
| 엑셀 V | concern:P8-2+{"cc": "엑셀V"} · product:M8-4-2 · unit_procedure:U5-099 · unit_procedure:U5-138 | B | 후보 |
| 엔더몰로지 | concern:P12-4+{"cc": "엔더몰로지"} · family:N8 · unit_procedure:U5-160 | J | 후보 · concern 우선 |
| 엘란쎄 | family:M3 · product:M3-3-1 · product:M3-3-1+{"ledger": "M3-3-1", "dest": "제품"} · unit_procedure:U5-090 | B | 후보 |
| 엠스컬프트 | family:M10 · product:M10-2-1 · product:M10-2-1+{"ledger": "M10-2-1", "dest": "제품"} | C | 후보 |
| 여드름/모공 | concern:P6 · concern:P7 | A | 전부 |
| 여드름/흉터 | concern:P6 · concern:P9 | A | 전부 |
| 여신토닝 | family:M8+{"ledger": "auto-M8-1775402736445", "dest": "6단계 패키지", "to": "병원 메뉴 패키지 — 구성 단위 시술은 6단계(DEC-003 OQ-313 · U1)"} · package:P6-07 | J | 후보 |
| 온다 | product:M9-3-1 · unit_procedure:U5-139 · unit_procedure:U5-139+{"ledger": "M9-3-1", "dest": "제품 + 단위 시술"} | B | 후보 |
| 올리지오 | product:M9-2-2 · product:M9-2-2+{"ledger": "M9-2-2", "dest": "제품"} · product:auto-M9-1775361486532 · unit_procedure:U5-091 · unit_procedure:U5-104 | B | 후보 |
| 울쎄라 | product:M9-1-1 · product:M9-1-1+{"ledger": "M9-1-1", "dest": "제품"} · product:M9-1-2 · unit_procedure:U5-102 · unit_procedure:U5-103 | B | 후보 |
| 유리피부관리 | family:M15+{"ledger": "auto-M15-1775402626587", "dest": "6단계 패키지", "to": "병원 메뉴 패키지 — 구성 단위 시술은 6단계(DEC-003 OQ-313 · U1)"} · package:P6-12 | J | 후보 |
| 윤곽주사 | concern:P11-2+{"cc": "윤곽주사"} · family:N1 | J | 후보 |
| 이마/관자놀이 | site:site.forehead-group · site:site.temple | I | 전부 |
| 이소트레티노인 | check_condition:C-ISO · family:M15+{"ledger": "auto-M15-1775361878302", "dest": "시술 아님(다른 단계)", "to": "8단계 확인 조건 「이소트레티노인」 원천 주장(B04) · 실버 단위 시술 없음"} | J | 후보 |
| 이중턱 | concern:P11-2 · concern:auto-89-1774737181584 · concern:auto-89-1774737181584+{"cc": "이중턱"} | A | 전부 |
| 이중턱 → 이중턱(지방) | concern:P11-2 · concern:auto-89-1774737181584 | A | 전부 |
| 인모드 | product:M9-2-5 · product:M9-2-5+{"ledger": "M9-2-5", "dest": "제품"} · unit_procedure:U5-091 | B | 후보 |
| 인중/구레나룻 | concern:P10+{"cc": "인중/구레나룻"} · unit_procedure:U5-144 · unit_procedure:U5-145 | J | 후보 · concern 우선 |
| 인트라셀 | family:M11 · product:M11-P-1 | C | 후보 |
| 인피니 | product:auto-M11-1775364775143 · product:auto-M11-1775364775143+{"ledger": "auto-M11-1775364775143", "dest": "제품"} · unit_procedure:U5-110 | B | 후보 |
| 인형피부관리 | family:M15+{"ledger": "auto-M15-1775402736449", "dest": "6단계 패키지", "to": "병원 메뉴 패키지 — 구성 단위 시술은 6단계(DEC-003 OQ-313 · U1)"} · package:P6-14 | J | 후보 |
| 입꼬리/잇몸미소/코끝 | unit_procedure:U5-013 · unit_procedure:U5-013+{"ledger": "M1-3-8", "dest": "단위 시술"} · unit_procedure:U5-014 · unit_procedure:U5-014+{"ledger": "M1-3-8", "dest": "단위 시술"} · unit_procedure:U5-015 · unit_procedure:U5-015+{"ledger": "M1-3-8", "dest": "단위 시술"} | E | 후보 |
| 자가혈 | family:M5 · unit_procedure:U5-020 · unit_procedure:U5-042 | J | 후보 |
| 잔주름 | concern:P2-3 · concern:auto-86-1774737181584 · concern:auto-86-1774737181584+{"cc": "잔주름"} | A | 전부 |
| 재생/면역 | purpose:PU-03 · purpose:PU-11 | A | 전부 |
| 전신재생 | concern:P4 · concern:P4-1 · purpose:PU-03 | A | 전부 |
| 전신재생 → 항노화 · 재생 | concern:P4 · concern:P4-1 · purpose:PU-03 | A | 전부 |
| 제모 | concern:P10 · family:M8+{"note": "제모"} | J | 후보 |
| 종아리 | site:site.calf · unit_procedure:U5-008 · unit_procedure:U5-008+{"ledger": "M1-3-4", "dest": "단위 시술"} | G | 후보 |
| 주름 | concern:P2 · unit_procedure:U5-001 · unit_procedure:U5-001+{"ledger": "M1-3-1", "dest": "단위 시술"} · unit_procedure:U5-002 · unit_procedure:U5-002+{"ledger": "M1-3-1", "dest": "단위 시술"} · unit_procedure:U5-003 · unit_procedure:U5-003+{"ledger": "M1-3-1", "dest": "단위 시술"} · unit_procedure:U5-004 · unit_procedure:U5-004+{"ledger": "M1-3-1", "dest": "단위 시술"} · unit_procedure:U5-005 · unit_procedure:U5-005+{"ledger": "M1-3-1", "dest": "단위 시술"} | J | 후보 · concern 우선 |
| 줄기세포 배양액 | family:M17 · unit_procedure:U5-081+{"ledger": "M17-1-1", "dest": "다른 단계 이름"} · unit_procedure:U5-121+{"ledger": "M17-1-1", "dest": "다른 단계 이름"} · unit_procedure:U5-143+{"ledger": "M17-1-1", "dest": "다른 단계 이름"} | J | 후보 |
| 줄기세포유래 엑소좀 | unit_procedure:U5-019+{"ledger": "M17-3-1", "dest": "다른 단계 이름"} · unit_procedure:U5-040+{"ledger": "M17-3-1", "dest": "다른 단계 이름"} · unit_procedure:U5-142+{"ledger": "M17-3-1", "dest": "다른 단계 이름"} | E | 후보 |
| 줄기세포치료 | concern:P4-3+{"taxonomy_entry": "auto-98-1774737181584"} · family:M17 | J | 후보 |
| 쥬베룩 | product:M3-4-1 · product:M3-4-1+{"ledger": "M3-4-1", "dest": "제품"} · unit_procedure:U5-090 | B | 후보 |
| 쥬베룩 볼륨 | product:M3-4-2 · product:M3-4-2+{"ledger": "M3-4-2", "dest": "제품"} · unit_procedure:U5-090 | B | 후보 |
| 지방감소 | concern:P12+{"taxonomy_entry": "P12-1"} · purpose:PU-07 | A | 전부 |
| 지방분해 | family:N1 · purpose:PU-07 | J | 후보 |
| 지방분해주사(PPC) | unit_procedure:U5-070+{"ledger": "auto-M16-1775361054038", "dest": "단위 시술"} · unit_procedure:U5-071+{"ledger": "auto-M16-1775361054038", "dest": "단위 시술"} · unit_procedure:U5-072+{"ledger": "auto-M16-1775361054038", "dest": "단위 시술"} · unit_procedure:U5-073+{"ledger": "auto-M16-1775361054038", "dest": "단위 시술"} · unit_procedure:U5-074+{"ledger": "auto-M16-1775361054038", "dest": "단위 시술"} · unit_procedure:U5-077+{"ledger": "auto-M16-1775361054038", "dest": "단위 시술"} · unit_procedure:U5-078+{"ledger": "auto-M16-1775361054038", "dest": "단위 시술"} · unit_procedure:U5-079+{"ledger": "auto-M16-1775361054038", "dest": "단위 시술"} · unit_procedure:U5-080+{"ledger": "auto-M16-1775361054038", "dest": "단위 시술"} | E | 후보 |
| 처짐 | concern:P3 · concern:P3-1 · concern:P3-2 · concern:P3-3 | A | 전부 |
| 처짐/탄력 | concern:P3 · concern:P4-1 | A | 전부 |
| 카복시테라피 | family:N2 · unit_procedure:U5-123 · unit_procedure:U5-123+{"ledger": "auto-M16-1775361069392", "dest": "단위 시술"} | J | 후보 |
| 케미컬 필링 | concern:P6-2+{"cc": "케미컬필링"} · family:M15+{"technique": "K09"} | J | 후보 |
| 코그(Cog) | unit_procedure:U5-022+{"ledger": "M7-2-1", "dest": "다른 단계 이름"} · unit_procedure:U5-097+{"ledger": "M7-2-1", "dest": "다른 단계 이름"} · unit_procedure:U5-098+{"ledger": "M7-2-1", "dest": "다른 단계 이름"} · unit_procedure:U5-122+{"ledger": "M7-2-1", "dest": "다른 단계 이름"} | E | 후보 |
| 쿨미니 (소부위 1개) | unit_procedure:U5-116+{"market_role": "후보"} · unit_procedure:U5-117+{"market_role": "후보"} · unit_procedure:U5-118+{"market_role": "후보"} · unit_procedure:U5-119+{"market_role": "후보"} · unit_procedure:U5-120+{"market_role": "후보"} | E | 후보 |
| 쿨스컬프팅 | family:M14 · product:M14-1-1 · product:M14-1-1+{"ledger": "M14-1-1", "dest": "제품"} · unit_procedure:U5-116 · unit_procedure:U5-117 · unit_procedure:U5-118 · unit_procedure:U5-119 · unit_procedure:U5-120 | B | 후보 |
| 쿨핏프로그램 | family:M14+{"ledger": "auto-M14-1775402698241", "dest": "6단계 패키지", "to": "병원 메뉴 패키지 — 구성 단위 시술은 6단계(DEC-003 OQ-313 · U1)"} · package:P6-11 | J | 후보 |
| 탄력 | concern:P12-3 · concern:P4-1 · purpose:PU-02 | A | 전부 |
| 태반주사 | family:N5 · unit_procedure:U5-128 | J | 후보 |
| 태반주사멜스몬 | product:auto-M16-1775364775098 · unit_procedure:U5-128 · unit_procedure:U5-128+{"ledger": "auto-M16-1775364775098", "dest": "제품 + 단위 시술"} | B | 후보 |
| 턱 끝 볼륨 → 볼륨 · 연장 | purpose:PU-04 · purpose:PU-05 | A | 전부 |
| 텍스쳐스무딩 | family:M11+{"ledger": "auto-44-1774737181584", "dest": "6단계 패키지", "to": "병원 메뉴 패키지 — 구성 단위 시술은 6단계(DEC-003 OQ-313 · U1)"} · package:P6-10 | J | 후보 |
| 토닝 | concern:P6-3+{"cc": "토닝"} · family:M8+{"technique": "K04a"} · technique:K04a | J | 후보 |
| 파셀라 | product:step1-new-FASCELLA · unit_procedure:U5-091 | B | 후보 |
| 팻킬주사 | unit_procedure:U5-070+{"ledger": "auto-M16-1775403054538", "dest": "단위 시술"} · unit_procedure:U5-071+{"ledger": "auto-M16-1775403054538", "dest": "단위 시술"} · unit_procedure:U5-072+{"ledger": "auto-M16-1775403054538", "dest": "단위 시술"} · unit_procedure:U5-073+{"ledger": "auto-M16-1775403054538", "dest": "단위 시술"} · unit_procedure:U5-074+{"ledger": "auto-M16-1775403054538", "dest": "단위 시술"} · unit_procedure:U5-077+{"ledger": "auto-M16-1775403054538", "dest": "단위 시술"} · unit_procedure:U5-078+{"ledger": "auto-M16-1775403054538", "dest": "단위 시술"} · unit_procedure:U5-079+{"ledger": "auto-M16-1775403054538", "dest": "단위 시술"} · unit_procedure:U5-080+{"ledger": "auto-M16-1775403054538", "dest": "단위 시술"} | E | 후보 |
| 펀치 | technique:K12b · unit_procedure:U5-047 | H | 후보 |
| 페이스앤넥큐레이션 | family:M1+{"ledger": "auto-7-1774737181584", "dest": "6단계 패키지", "to": "병원 메뉴 패키지 — 구성 단위 시술은 6단계(DEC-003 OQ-313 · U1)"} · package:P6-04 | J | 후보 |
| 포텐자 | product:M11-1-1 · product:M11-1-1+{"ledger": "M11-1-1", "dest": "제품"} · unit_procedure:U5-110 | B | 후보 |
| 풀페이스큐레이션 | family:M1+{"ledger": "auto-4-1774737181584", "dest": "6단계 패키지", "to": "병원 메뉴 패키지 — 구성 단위 시술은 6단계(DEC-003 OQ-313 · U1)"} · package:P6-01 | J | 후보 |
| 프락셀 | product:M8-2-4 · unit_procedure:U5-026 · unit_procedure:U5-027 · unit_procedure:U5-028 · unit_procedure:U5-029 | B | 후보 |
| 프락셔널 | family:M8+{"technique": "K04b"} · technique:K04b | J | 후보 |
| 프락셔널 레이저 | concern:P7-2+{"cc": "프락셔널레이저"} · concern:P9-3+{"cc": "프락셔널레이저"} · family:M8+{"technique": "K04b"} | J | 후보 |
| 프랙셔널 | unit_procedure:U5-026 · unit_procedure:U5-027 · unit_procedure:U5-028 · unit_procedure:U5-029 | E | 후보 |
| 프로파일로 | product:auto-M4-1775362484436 · product:auto-M4-1775362484436+{"ledger": "auto-M4-1775362484436", "dest": "제품"} · unit_procedure:U5-018 | B | 후보 |
| 피부결/모공 | concern:J10 · concern:P7 | A | 전부 |
| 피부결/톤/항노화 | concern:J10 · concern:P4 · concern:P5 | A | 전부 |
| 피코 | unit_procedure:U5-023 · unit_procedure:U5-026 · unit_procedure:U5-027 · unit_procedure:U5-131 | E | 후보 |
| 피코토닝 | concern:P5-1+{"cc": "피코토닝"} · unit_procedure:U5-023 · unit_procedure:U5-023+{"ledger": "M8-1-2", "dest": "단위 시술"} | J | 후보 · concern 우선 |
| 항산화수액 | concern:P4-3+{"cc": "항산화수액"} · unit_procedure:U5-051 · unit_procedure:U5-052 | J | 후보 · concern 우선 |
| 허니스킨관리 | family:M15+{"ledger": "auto-M15-1775402736450", "dest": "6단계 패키지", "to": "병원 메뉴 패키지 — 구성 단위 시술은 6단계(DEC-003 OQ-313 · U1)"} · package:P6-15 | J | 후보 |
| 헤어셀 | product:auto-M15-1775364775178 · unit_procedure:U5-130 · unit_procedure:U5-130+{"ledger": "auto-M15-1775364775178", "dest": "제품 + 단위 시술"} | B | 후보 |
| 혈관레이저 | concern:P8-2+{"cc": "혈관레이저"} · family:M8+{"note": "혈관"} | J | 후보 |
| 흉터/재생 | concern:P4-1 · concern:P9 · purpose:PU-03 | A | 전부 |

해석 규칙(사전 행 아님): 고민 규칙 R12, R13, R14, R15, R16, R17, R18, R19, R20, R21, R22 · 8단계 꼬리 낱말 29 · 3단계 패턴 251 · 문장 패턴 20 · 조건 패턴 53

## 5. id 규칙(B6) — 정본 id ↔ 실버 id

정본 id = {종류}:{키} — 실버 id 는 바꾸지 않음(B6). 골드 · 적재는 map 으로 실버 id → 정본 id

| 종류 | 규칙 |
|---|---|
| `product` | 원장 ledger_id 그대로(원천 추적) — 꼴이 여럿이라 접두로만 구분 |
| `family` | M{n} · N{n} 그대로 |
| `site` | site.{영문} 그대로 |
| `technique` | K{nn}[a-c] 그대로 |
| `unit_procedure` | U5-{nnn} 그대로 |
| `package` | P6-{nn} 그대로 |
| `concern` | P{n} · P{n}-{n} · auto-{n}-{ts} 그대로 · 결정 노드 J{n}-{한글} → J{n}(이름은 name 칸) |
| `purpose` | 실버는 id 없음(이름 · 「목적:{이름}」 문자열) → PU-{nn}(purposes[] 순서) |
| `combo` | RC-… 그대로 |
| `check_condition` | C-{약어} 그대로 |
| `complication` | CX-{계열}-{원천 번호} · U1 원문 serious = CX-{계열}-T{n} |
| `evidence_statement` | ST-{계열}-{field}-{nn} 그대로 |
| `evidence_source` | EV-LIT · EV-WEB · EV-GD 그대로 |

| 실버 안 문자열 꼴 | 자리 | → 정본 | 메모 |
|---|---|---|---|
| `family:{계열}` | step8 edges[].a\|b · conditions.claims[].target · safety.timelines[].attach | family:{계열} | 「family:M9#HIFU」 꼴은 endpoints.a\|b.qualifier(B3) |
| `units:{U5,…}` | step8 edges[].a\|b | unit_procedure:{U5} 하나 · 둘 이상이면 endpoints.candidates[](B3 — 노드 아님) |  |
| `bundle:{M\|M}` | step8 edges[].a\|b | endpoints.candidates[] 계열 |  |
| `all · 「모든 시술(공통)」` | step8 edges · conditions.claims[].target | 대상 「모든 시술」(노드 아님) |  |
| `ledger:{원장 id} · product:{원장 id}` | step8 conditions.claims[].target | product:{원장 id} | 행선지 없는 원장 항목이면 대상 없음 표시 |
| `unit:{U5}` | step8 safety.timelines[].attach · pih | unit_procedure:{U5} |  |
| `목적:{이름}` | step7 edges[].from · from_concerns · correspondence[].target | purpose:PU-{nn} · 고민에 붙은 목적은 concern:{P} | purpose_nodes[] 는 「:」 없는 이름 |
| `J{n}-{한글}` | step7 concerns.extra_items[].id · edges[].from_concerns | concern:J{n} |  |

「목적:」 · 결정 노드 문자열 대응: `목적:거상` → `purpose:PU-01` · `목적:근육강화` → `purpose:PU-08` · `목적:다한증` → `concern:P14-3` · `목적:라인 정리` → `concern:P11` · `목적:리프팅` → `purpose:PU-01` · `목적:면역` → `purpose:PU-11` · `목적:모공` → `concern:P7` · `목적:문신 제거` → `purpose:PU-13` · `목적:미백` → `concern:P5` · `목적:미백/항산화` → `concern:P5` · `목적:병변(점 · 문신 제거)` → `purpose:PU-13` · `목적:볼륨` → `purpose:PU-04` · `목적:볼륨 회복` → `purpose:PU-04` · `목적:볼륨 회복(충전)` → `purpose:PU-04` · `목적:색소` → `concern:P5` · `목적:색소/토닝` → `concern:P5` · `목적:셀룰라이트` → `concern:P12-4` · `목적:여드름` → `concern:P6` · `목적:연장` → `purpose:PU-05` · `목적:영양보충` → `purpose:PU-12` · `목적:윤곽(라인 정리)` → `concern:P11` · `목적:이중턱` → `concern:P11-2` · `목적:재생` → `purpose:PU-03` · `목적:재생/면역` → `purpose:PU-03` · `목적:점 · 사마귀 제거` → `concern:P14-1` · `목적:제모` → `concern:P10` · `목적:주근깨` → `concern:P5-2` · `목적:주름` → `concern:P2` · `목적:지방감소` → `purpose:PU-07` · `목적:지방분해` → `purpose:PU-07` · `목적:지방분해(지방감소)` → `purpose:PU-07` · `목적:축소` → `purpose:PU-06` · `목적:타이트닝(탄력)` → `purpose:PU-02` · `목적:탄력` → `purpose:PU-02` · `목적:탈모` → `concern:P13` · `목적:피로회복` → `purpose:PU-10` · `목적:피지` → `concern:P6-2` · `목적:항노화` → `concern:P4` · `목적:항산화` → `purpose:PU-09` · `목적:혈관` → `concern:P8` · `목적:흉터` → `concern:P9`

전체 대응표 1071행은 `semantic.json` ids.map(정본 id · 종류 · 실버 id · 이름) — 실버 id 와 다른 것만:

- `J8-자갈턱` → `concern:J8`
- `J10-피부결` → `concern:J10`
- `J14-잇몸미소` → `concern:J14`
- `리프팅` → `purpose:PU-01`
- `타이트닝(탄력)` → `purpose:PU-02`
- `재생` → `purpose:PU-03`
- `볼륨 회복(충전)` → `purpose:PU-04`
- `연장` → `purpose:PU-05`
- `축소` → `purpose:PU-06`
- `지방분해(지방감소)` → `purpose:PU-07`
- `근육강화` → `purpose:PU-08`
- `항산화` → `purpose:PU-09`
- `피로회복` → `purpose:PU-10`
- `면역` → `purpose:PU-11`
- `영양보충` → `purpose:PU-12`
- `문신 제거` → `purpose:PU-13`

## 6. 읽는 규칙

**reading_contract**: 추천 · AI 는 edges[].resolved 만 읽는다(10-30 · 충돌 하나로) — resolved.first(a | b | null = 순서 단정 안 함) · days = [하한, 상한](일) · open_high · same_day. 필드 겉 칸이 null 이고 resolved.by_sub_condition 이 true 면 resolved.options[] 중 그 field 의 sub_condition 맞는 것(조건을 모르면 sub_condition 「조건: 모름」 = 전부 접은 가장 보수적인 값). 같은 날 값이 먼저 하는 쪽에 따라 갈리면 resolved.by_direction.a|b.same_day(a = 엣지 a 끝 먼저 · 겉 same_day 는 null). 단위 시술 쌍은 resolved_pairs 에 있으면 그것 · 없으면 그 쌍에 닿는 가장 구체적인 엣지의 resolved(위 엣지 주장은 상속해 이미 접힘). 확인 조건 등급은 conditions.resolved(대상 키 × 조건 — 단위 시술 키 · 계열 키 · 공통 순으로 가장 구체적인 것) · 대기 기간은 conditions.wait_resolved. claims[].interval(원문 칸)은 근거 · alternatives 로만 — 앱에 바로 내지 않는다. 끝점 · 피함에 default_apply false(scope 「조건부 — 단위 시술 미특정」)면 기본 응답 · 계열 상속 · 값 접기에서 뺀다(조회 옵션으로만)

| 칸 | 뜻 |
|---|---|
| `days` | [하한, 상한](일) |
| `open_high` | 위로 열림(이상) |
| `first` | a \| b \| null(순서 단정 안 함) |
| `same_day` | true · false · null |
| `by_sub_condition` | 겉 칸 비움 → options[] |
| `options[]` | sub_condition 별 days · same_day · first(+ 조건 모름 = 전부 접음) |
| `by_direction` | 먼저 하는 쪽별 same_day(a \| b) |
| `marks[]` | 원문 낱말 갈래 표시 |
| `text` | 원문(보관만) |
| `resolved` | 10-30 — 앱이 읽는 칸(edges[].resolved · resolved_pairs[].resolved) |

- 끝점: 엣지 끝 = endpoints.a|b{kind, id, qualifier, candidates[]} — kind 「단위 시술」 · 「계열」 · 「계열 + 조건」 은 id 하나 · 「단위 시술 후보」 · 「계열 묶음」 · 「계열 후보」 는 candidates[] 전부(후보 표시) · 「모든 시술」(B3)
- 부작용: U2 · B1 — 부작용(흔한 예상 반응) = 계열 속성 safety.side_effects · 합병증 노드 = complications.json severity moderate 이상만. 제품 × 계열 · 단위 시술에 값(5단계 extracted safety.common)이 있으면 그 값이 계열 값을 덮어씀 — 덮어쓰기는 골드 계산(B7 · 저장 안 함)
- 조건 아님: B8 — 확인 조건 주장 중 kind 가 「…항목」(상담 · 시술 준비 · 고지)이거나 사람 조건 · 연령대 조건이 아닌 것 = 확인 조건 엣지 아님 → conditions.not_condition(원문 보관) · 계열 대상은 safety.family_text 「상담 · 준비 · 고지 · 조건 아닌 문장」(G10 그대로) · 엣지 셈에서 뺌
- recommendable false · active false · 시그니처 · 영업 문구(default_response false) · default_apply false 는 기본 응답에서 뺌
- 충돌은 resolved 하나(순서 반대는 순서 단정 안 함 + 의료진) · 후보는 전부 · gap 은 「정보 없음」으로

셈: {"claims": 395, "with_interval": 258, "days": 116, "first": {"None": 242, "a": 147, "b": 6}, "same_day": {"False": 15, "None": 302, "True": 78}}

### 6-1. 간격 낱말 사전

| id | 패턴 | 칸 | 메모 |
|---|---|---|---|
| L-ALT | `택\s*1` | {"kind": "대체(택 1)", "days": null, "mark": "대체(택 1) — 간격 비움"} | 「택 1 시술」 → kind 대체 · 간격 비움 |
| L-MD | `의료진이.*(평가\|판단).*(간격\|결정)` | {"days": null, "mark": "의료진 판단(간격 원천 없음)"} | 「의료진이 … 평가해 간격 결정」 → 간격 없음 + 의료진 판단 표시 |
| L-SEP | `별도\s*세션` | {"same_day": false, "mark": "별도 세션"} | 「별도 세션」 → same_day false |
| L-SDNO | `(동시\|같은\s*날\|같은날\|당일)\s*(시술\s*)?(금지\|불가)\|당일\s+\S+\s*금지\|후\s*당일` | {"same_day": false} | 「동시 금지 · 동시 시술 금지 · 당일 금지 · 같은 날 불가」 → same_day false |
| L-SAMESITE | `(같은\|동일)\s*부위\|같은\s*날이면\s*다른\s*부위\|부위\s+\S+\s*동시` | {"condition": "같은 부위"} | 「같은 부위 · 동일 부위」 조건(같은 날 불가와 함께) |
| L-SDIFFSITE | `같은\s*날이면\s*다른\s*부위` | {"same_day": false, "mark": "같은 날이면 다른 부위"} | 「같은 날이면 다른 부위」 → 같은 부위 같은 날 불가 |
| L-IMM | `직후\|즉시` | {"same_day": true, "days_if_none": [0, 0]} | 「직후」 → same_day true · days [0,0] |
| L-SDOK | `(같은\s*날\|같은날\|당일)\s*(시술\s*\|에\s*)?(가능\|병행\|조합)\|같은\s*날\s*또는\|(같은\s*날\|같은날)\s*$\|^같은\s*날\|동시(?!\s*(시술\s*)?금지)` | {"same_day": true} | 「같은 날 가능 · 당일 병행 · 동시(금지 없이)」 → same_day true |
| L-BEFORE | `전에` | {"mark": "순서만(「…전에」)"} | 「…전에」 → first 만 |
| L-BETWEEN | `사이사이` | {"days": null, "mark": "반복 사이(사이사이) — 간격 없음"} | 「사이사이」 → 반복 표시 · 간격 없음 |
| L-REPEAT | `반복\|매회` | {"repeat": true, "mark": "반복"} | 「N주 간격 반복」 → 반복 표시(같은 시술 회차 간격) |
| L-COUNT | `\d+\s*[\-~]?\s*\d*\s*회` | {"mark": "회차(횟수 — 간격 아님)"} | 「8-10회」 → 회차 표시 |
| L-ONLY | `에\s*한해` | {"mark": "조건부(원문 「…에 한해」)"} | 「…에 한해 같은 날 가능」 → 조건부 표시 |
| L-FLEX | `순서\s*(유연\|무관)` | {"mark": "순서 유연(원문 「순서 유연 · 무관」)"} | 「같은 날엔 순서 유연 · 순서 무관」 → 표시 |
| L-SEQ | `순차` | {"first_from_source_order": true} | 「순차 시술」 → 원천 from → to 순서 |
| L-NUM | `(\d+(?:\.\d+)?)\s*(시간\|일\|주\|개월)?\s*(?:[~\-]\s*(\d+(?:\.\d+)?))?\s*(시간\|일\|주\|개월)` | {"days": "number"} | 「N주/N일/N개월(후 · 이상 · 간격)」 → days [N,M] (단위 일) · open_high = 이상 · 최소 · 후 · 뒤 · 부터 · 이내/내 금지(그 기간이 지나야 함) |

단위 환산 {"시간": 0.0416667, "일": 1, "주": 7, "개월": 30} · 조건부 한정어 `고출력\|고에너지\|고강도\|강한\|박리성\|박리\|어블레이티브\|ablative\|심부`

### 6-2. 표시 12

| 표시 | 뜻 | 실버 칸 | 셈 | 읽는 법 |
|---|---|---|---|---|
| `conflict` | 충돌 처분(보수적 선택 · 의료진 확인) | step8 claims[] · edges[].review_status=conservative\|staff_check · review_label · edges[].resolved · resolved_pairs[] · conflicts[].resolution · conditions.resolved · wait_resolved · step2 product_family[].conflict | 90 | 앱엔 resolved 하나(10-30) — 보수적 선택은 값 하나 + 원문 alternatives · 의료진 확인(순서 반대)은 순서 단정 안 함 + 원천 질문 |
| `conditional` | 조건부(단위 시술 미특정) | claims[].a\|b.default_apply=false · avoid_edges[].default_apply=false · conditions.claims[].scope_conditional | 6 | 기본 응답 · 계열 상속에서 뺌(조회 옵션으로만) |
| `candidates` | 후보 여럿 | edges[].endpoints.*.candidates[](2 이상) · units[].synonyms[].ambiguous · units[].candidate_of · step7 edges[].resolve_flag=ambiguous · step6 slots[] · 사전 mode 후보 | 222 | 고르지 않고 후보 전부 · 외부 LLM 이 고르거나 되묻기 |
| `weak` | 근거 약 | evidence_level 약 · 중 · step3 synonyms[].weak · anatomical_name.level 약 | 17 | 값은 쓰되 약함 표시 |
| `question` | 원천 질문(병원 · 의료진 · 원장님) | origin_question · staff_question · doctor_questions · pending_director · confirm_question · origin_questions[] | 93 | 추천값으로 쓰되 표시 · 답 오면 그 행만 |
| `not_recommended` | 추천 제외 | step1 4_license.recommendable=false · step6 recommendable=false · combos sales_copy.default_response=false | 120 | 기본 응답에서 뺌 · 노드는 남김 |
| `gap` | gap(원천 없음) | safety.complication_gap_families · safety.side_effect_gap_families · step5 pih_gap_units · step7 resolve_flag=no_unit_at_site | 88 | 「없음 = 안전」 아님 |
| `default_value` | 기본값(규칙으로 채움) | step5 units[].site_basis 기본값 · route_status 허가 용법 미확인 · family_defaults | 66 | 원천 값과 구분해 표시 |
| `unresolved` | 못 풂 | step7 resolve_flag=unresolved · step8 claims[].resolved=false · 끝점 「해석 안 됨」 | 20 | 원문 보관 · 끝 없음 |
| `not_procedure` | 시술 아님 | step7 resolve_flag=not_procedure · step8 claims[].not_procedure · 사전 none:시술 아님 | 8 | 엣지 끝 아님 |
| `by_sub_condition` | 하위 조건별 값 | claims[].interval.by_sub_condition · options[] | 2 | 겉 칸이 비면 options[].sub_condition 별로 |
| `license_unconfirmed` | 허가번호 미확인 | step1 4_license.status | 7 | 추천 포함 · 표시 |

### 6-3. gate_status 3값

| 값 | 뜻 |
|---|---|
| 자동(완전 일치) | 원천 말과 대상 이름이 정규화 뒤 같음 |
| 자동(규칙) | 결정 파일의 규칙 · 사전 · 패턴으로 결정론 |
| 결정 | 사람이 정한 값 — decided_by 에 사용자 결정 id(_RESUME §2) |

- 모든 노드 · 엣지 · 주장 공통 3값. 「미확인」은 상태가 아니라 표시(question · weak · gap). 실버 칸 → 값: gate_status 칸이 있으면 그대로(7단계 correspondence · 8단계 claims) · 없으면 decided_by 가 사용자 결정 id 면 「결정」 · 나머지 「자동(규칙)」
- 지금: {"step7 correspondence": {"자동(규칙)": 98, "자동(완전 일치)": 151}, "step8 claims": {"자동(규칙)": 395}, "step5 units decided_by 있음": 162}

## 7. 상속 규칙(B7 — 저장 안 함 · 골드 계산)

| id | 이름 | 규칙 | 실버 칸 | 셈 | 지금 저장된 것 |
|---|---|---|---|---|---|
| I1 | 계열 → 단위 시술 | 계열 끝 엣지(관계 · 피함 · 확인 조건 · 합병증 · 근거 문장 · 위험지대 · 추천 계열만)는 key.family 가 그 계열인 단위 시술 전부에. default_apply false 는 상속 안 함 | step5 units[].key.family · step8 edges[].endpoints kind 계열 · conditions.claims[].target_level 계열 · step7 edges[].target_kind 계열만 | {"relation_family_endpoints": 306, "condition_family_claims": 304, "treats_family_only": 84} | safety.complications[].units_inherit(합병증만 미리 펼침) — 정본은 계산(B7) · 칸은 실버에 남아도 골드는 다시 셈 |
| I2 | 하위 계열 | 하위 끝(qualifier.sub_family)은 key.sub_family 같은 단위 시술로 · 키에 그 하위 없는 계열은 계열(+조건) 후보 전부 · 하위 원문 보관 | edges[].endpoints.*.qualifier.sub_family · claims[].a\|b.sub_family · flag · step8-decisions timeline_attach.units_where · step5 rules.product_link.inherit | {"sub_family_endpoints": 42} |  |
| I3 | 기법 조건 | 기법 끝(qualifier.technique)은 key.technique 가 그 기법(또는 하위)인 단위 시술로 · 사전 「토닝 = M8 + K04a」 도 이 규칙으로 단위 시술이 나옴(B5) | edges[].endpoints.*.qualifier.technique · claims[].a\|b.technique · conditions.claims[].target.technique · step5 rules.product_link.technique_compat | {"technique_endpoints": 25} |  |
| I4 | 제품 → 단위 시술 | 같은 계열(주 · 보조) · 키 하위가 있으면 같은 하위(주 · 보조 하위) · 키 하위 null 이면 계열 전부 — S7 · 그리고 기법 호환(technique_compat · 10-29 F1) | step5 units[].uses_product(저장) · product_links[].inherited_candidates · technique_excluded · guard · rules.product_link | {"link": {"계열 has_product 만(기법 호환 단위 시술 없음 — F1)": 7, "계열 밖(단위 시술 없음)": 5, "원장님 문의(계열 없음)": 3, "저장 uses_product": 36, "조회 때 상속 후보": 303}} | product_links[].inherited_candidates(5단계 계산 기록) — 정본은 계산(B7) |
| I5 | 부위 — 내림 · 올라가기(R21) · 고민 영역(R22) | 내림: 이름 · 동의어 · 제품 · 고정 키로 잡은 단위 시술이 앵커 부위(또는 하위)에 없으면 같은 계열(하위 하나면 그 하위)을 units_at(계열, 부위)로 내린다 · R21: 앵커 부위(또는 하위)에 그 계열 단위 시술이 없으면 3단계 부위 트리의 상위로 올라가며 찾는다. 층 = 조상 노드 자신(형제 부위는 다른 부위라 넣지 않음 · 묶음 노드는 직접 붙은 단위 시술이 없어 통과) · 마지막 층 = 최상위 영역의 「전체」 노드. 처음 찾은 층의 단위 시술만 · 영역: 최상위 영역 = 3단계 트리에서 부모 없는 노드(계산 · 얼굴 · 목(묶음) · 두피 · 바디). 영역 경계를 넘지 않는다 — 얼굴 고민에 바디 · 두피 · 목 단위 시술 0 · 전체 노드: 영역 R 의 「전체」 노드 = 「R 전체」 자식이 있으면 그것(얼굴 → 얼굴 전체 · 5단계 J2) · 없으면 R 자신(바디 · 두피) · R 이 묶음이면 없음(목(묶음) → 계열만) · 없으면: 영역 「전체」 노드까지 없으면 계열 엣지만(to_units 비움 · to_family 유지) + 표시 「이 부위 단위 시술 없음 · 계열만」 · 단위 시술 후보 붙이지 않음 · R22: R22 — 앵커 부위 없는 엣지(① ~ ⑧) · 추천 조합 구성(components · members · upgrade · schedule)의 단위 시술을 앵커 고민(엣지 from · from_concerns / 조합 anchor.concerns · concern)의 영역 밖이면 뺀다. 다 빠지면 계열만 · 고민 영역: 고민 영역 = 대분류 · 중분류 · 항목 · 결정 노드(extra_concern_items)의 sites → 3단계 최상위 영역. 대분류 = 하위 전부 합 · 중분류 kind == 「목적」 은 넣지 않음 · 영역 없음: 영역 없음(색소 · 여드름 · 모공 · 흉터 · 항노화 등 하위 부위 0) = 손대지 않음 · concern_region_check 「고민 영역 없음(R22 · 셈만)」 | step7-decisions site_rules{lowering, climb, concern_region} · step7 edges[].lowering · site_layer · site_check · concern_region_check · concern_region_dropped · step3 nodes[].parent | {"site_check": {"부위 안": 119, "상위 부위 얼굴 전체": 35, "앵커 부위 없음": 267, "원천 하위 안 정함 · 계열만(R31)": 3, "이 부위 단위 시술 없음 · 계열만": 13}, "concern_region_check": {"고민 아님(RN 밖)": 23, "고민 영역 밖 N 뺌(RN)": 5, "고민 영역 밖 N 뺌(RN) · 기본 영역(판단 ①)": 41, "고민 영역 안(RN)": 18, "고민 영역 안(RN) · 기본 영역(판단 ①)": 64, "고민 영역 없음(RN · 셈만)": 13, "없음": 273}} | 7단계가 엣지에 적용해 저장(엣지 값) — 상속 아님 |
| I6 | 끝점 묶음 | candidates[] 는 원문 이름이 가리킨 후보 전부(OR · 고르지 않음) — 각 후보에 「후보」 표시로 적용 · 계열 묶음은 그 계열 전부 · 모든 시술은 전부 | edges[].endpoints.*.candidates[] · avoid_edges[].to.units · conditions.claims[].target.units | {"endpoints": {"계열": 182, "계열 + 조건": 1, "계열 묶음": 2, "단위 시술": 163, "단위 시술 후보": 111, "모든 시술": 1}} |  |
| I7 | 조건부 제외 | default_apply false 는 기본 상속 · 기본 응답에서 뺌 | claims[].a\|b.default_apply · avoid_edges[].default_apply · conditions.claims[].scope_conditional | {"conditional": 6} |  |
| I8 | 안전 · 운영 원문 붙는 수준 · 부작용 덮어쓰기 | 경과 타임라인 · PIH · 운영 속성 · 부작용은 원천이 가리킨 수준(계열 · 하위 · 단위 · 제품)에 붙고 아래로 상속 · 아래 수준 값(제품 × 계열 · 단위 시술 extracted safety.common)이 있으면 위 값을 덮어씀 | step8 safety.timelines[].attach_level · step8-decisions timeline_attach · step5 pih[].attach · step8 safety.pih · step5 units[].ops.inherit · step8 safety.side_effects[].attach · step5 extracted[](safety.common 키) | {"timelines": {"계열": 5, "계열 N1(C5 — M": 1, "계열(하위 HA — M": 1, "단위 시술": 1, "하위 계열 HIFU ·": 1, "하위 계열 화학 박피 ": 1}, "pih": {"family": 3, "family_sub": 8, "product": 6, "unit": 9}, "side_effects": 72, "side_effect_override_keys": 521} |  |
| I9 | 해당 없음 ≠ gap | PIH 해당 없음 계열은 「해당 없음」 · 원천 없음은 gap · 합병증 원천은 있으나 전부 mild 인 계열은 「중대 반응 없음(원천)」 — 셋을 나눠 표시 | step5 rules.pih_not_applicable · pih_not_applicable_units · pih_gap_units · step8 safety.complication_gap_families · complication_mild_only_families | {"pih_not_applicable": 77, "pih_gap": 63, "complication_gap": 12, "complication_mild_only": 1} |  |

## 8. 근거 문장 종류(B2)

field {"adverse_effects": 32, "effects": 37, "moa": 50} → class {"근거 수준 · 규제(효과 칸)": 2, "기전": 44, "기전 · 효과 한계(이상 반응 칸)": 4, "드문 · 중대 반응(합병증 성격)": 9, "부작용(흔한 예상 반응)": 9, "색소 반응(PIH)": 4, "안전성 비교(기전 칸)": 1, "안전성 총평": 6, "적응증(기전 칸)": 2, "효과": 35, "효과(기전 칸)": 3}

- field(원천 칸)는 그대로 · class 는 이 정본(B2). 칸과 뜻이 다른 문장 = 원천 수정 후보
- 원천 수정 후보(칸과 뜻이 다름) 12: ST-M1-adverse_effects-04, ST-M15-moa-03, ST-M15-moa-04, ST-M15-moa-05, ST-M16-effects-01, ST-M16-effects-02, ST-M2-adverse_effects-02, ST-M2-moa-02, ST-M3-adverse_effects-01, ST-M4-adverse_effects-01, ST-M8-moa-03, ST-M8-moa-08

## open

없음

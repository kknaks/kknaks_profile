# 시맨틱 정의 조사 — 실버 1~8단계 위 노드 · 엣지 · 용어 · 사전 · 읽는 규칙 정본 초안

생성 2026-10-29T23:02:34 · 읽기 전용 · 정본 데이터 `semantic-research.json`(이 문서는 그 json 에서 만든 것). 셈은 전부 실버 json 에서 다시 셈.

입력 판(파일 수정 시각): `step1-products.json` 10-29T12:11 · `step2-families.json` 10-29T17:55 · `step3-sites.json` 10-29T12:11 · `step4-techniques.json` 10-29T17:55 · `step5-units.json` 10-29T18:14 · `step6-packages.json` 10-29T16:31 · `step7-concerns.json` 10-29T23:00 · `step8-relations.json` 10-29T23:00

> 코디 알림(10-29): 7단계 「그 부위 단위 시술 없음 → 후보 전부」 규칙이 「상위 부위로 올라가기(R21)」로 바뀜 — 이 판은 바뀐 파일(step7-decisions 22:56 · step7-concerns · step8 22:59)로 셈했고 상속 I5 · 용어 「부위로 내림」에 step7-decisions site_rules.climb 문장을 그대로 옮김. 셈은 inputs.mtime 시점 파일 기준

## 0. 한 장 요약

- **노드 종류 13**(페이지 14 — 「끝점 묶음」은 실버에 노드가 아니라 끝점 문자열 · 결정 U3) · **엣지 종류 21**(페이지 32 → 합침 · 나눔) · **용어 47** · **사전 14곳**(원소 2454 · 겹침 147) · 표시 12 · 상속 규칙 9 · **결정 묶음 12** · **사용자 판단 3**
- 가장 큰 발견 다섯:
  1. **부작용이 네 곳에 흩어짐** — 합병증 노드 안 severity mild · family_text 「부작용 문장 common」 · 근거 문장 adverse_effects · 5단계 extracted safety.common. 전체 65 · severity {'mild': 38, 'moderate': 13, 'severe': 11, 'critical': 3} · 계열 ['M1', 'M11', 'M14', 'M15', 'M16', 'M2', 'M3', 'M7', 'M8', 'M9'] — 합병증 노드의 절반 넘게가 흔한 예상 반응(B1 · U2)
  2. **합병증 gap 17계열 중 7계열(M10, M12, M13, M17, M4, M5, M6)은 이미 원천 문장이 있음**(family_text 「부작용 문장」 — 지금 「합병증 노드 아님」 라벨) → U1
  3. **같은 낱말을 7단계 · 8단계 사전이 다른 수준으로 풂** — 7단계 resolver 는 단위 시술로, 8단계 alias 는 계열 + 조건으로(17/31) · 「비타민C」는 7단계 = 단위 시술 · 8단계 = 시술 아님(B5)
  4. **그림 밖 52 중 18 은 데이터에 앵커가 있음** — 목적이 id 없이 「목적:{이름}」 문자열 · purpose_nodes 칸이라 페이지가 못 찾음(B6 · B10)
  5. **읽는 규칙 · 게이트 상태가 8단계에만 정본** — 1~6단계는 decided_by · 칸 이름으로만 상태를 말함(B12)

## 1. 노드 종류

| # | 내부 이름 | 사이트 용어 | 뜻 | id 규칙 | 필수 속성 | 선택 속성 | 정본 · 칸 경로 | 셈(파일) | 페이지 | 출처 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `product` | 제품(장비 · 제품) | 허가 · 업체 · 규격을 가진 제품 · 장비 하나(라인이면 상위 제품) — 시술이 아니라 시술에 「쓰는 것」 | 원장 ledger_id 그대로(문자열) — M{n}-{n}-{n} · auto-M{n}-{timestamp} · auto-{n}-{timestamp} · new-DEV-{n} · M{n}-P-{n} · auto-M{n}-DCA-{n} · step1-new-APTOS 등 8꼴<br>꼴 {"M9-9-9": 85, "auto-M9-9": 176, "auto-9-9": 35, "auto-M9-hADM-9": 1, "auto-M9-DCA-9": 7, "new-DEV-9": 34, "M9-P-9": 14, "step9-new-APTOS": 1, "step9-new-FASCELLA": 1} | ledger_id · 2_names.display_name · 4_license.status(6값) · 4_license.recommendable · active · 계열(2단계 product_family.family) | 2_names.search_names[]{name,lang} · 2_names.name_basis · 1_identity.kind · 4_license.licenses[] · history[] · reference[] · 5_spec · 6_companies{manufacturer · importer · seller · license_holder · other · conflicts} · line · taxonomy_product_ids · evidence · open | `step1-products.json` items[] (active=true) | **354** items 395 중 active 354 · 합침/빠짐 41 은 노드 아님(이력) | 354 | _RESUME §2 10-27 「이름 규칙」 · 「허가 규칙」 · 10-27 「1단계는 제품 ↔ 허가만」 · 로그 step1 §3 |
| 2 | `family` | 계열 | 무엇을(약제 · 장비 계열) — 문헌 카테고리(M1~M17) + 늘린 계열(N1~N10) | M{1..17} · N{1..10}<br>꼴 {"M9": 17, "N9": 10} | id · name(공식 일반명) · definition · name_status | synonyms[] · literature_name · literature_evidence[] · sub_families[] · sub_family_handling[] · deferred[] · new_family · note | `step2-families.json` families[] | **27** new_family 10 · name_status {'확정(10-27)': 1, '국내 공식 출처': 1, '공식 출처 미확인': 24, '국내 품목명 있음 · 계열 일부만 해당(3/12행) — 공식 일반명 아님': 1} | 27 | _RESUME §2 10-27 「계열 이름 = 공식 일반명」 · 10-28 「2단계 계열 기준 = 교과서 · 임상 · 학회 문헌」 · 10-29 「클리닉 시술은 전부 단위 시술 — 계열을 늘린다」 |
| 3 | `site` | 부위 | 어디에 — 시술 받는 사람 몸 겉에서 가리킬 수 있는 자리(뼈 · 근육 · 혈관 · 층은 부위 아님) | site.{영문-kebab}(묶음은 -group)<br>꼴 {"site.{en}": 53} | id · name(일반인 용어) · parent · status | synonyms[]{text,type,weak} · compound_strings[] · anatomical_name{en,ko,basis,level}(전문의 용어) · danger_zone{zone,relation,basis} · note | `step3-sites.json` nodes[] | **53** status {'tree': 37, 'added_oq206': 6, 'added_step3': 10} · 해부학 이름 근거 {'강': 20, '약': 29, '중': 4} | 53 | _RESUME §2 10-28 「부위 기준 = 어디에 맞냐」 · 「부위 노드 이름 2벌」 · 10-27 부위 트리 확정 |
| 4 | `technique` | 기법 | 어떻게 — 큰 기법 + 세부 기법(층 · 깊이 · 대상 근육 · 도구는 단위 시술 속성) | K{nn} · K{nn}{a\|b\|c}<br>꼴 {"K9": 14, "K9a": 4, "K9b": 4, "K9c": 4} | id · name · level(큰 · 세부) · parent | medical_name · basis · children[] · family_default[] · family_also[] · source_expressions[] · draft_techniques[] · modes[] | `step4-techniques.json` nodes[] | **26** level {'큰': 14, '세부': 12} | 26 | _RESUME §2 10-28 「4단계 기법 조사 반영 J1 안 1」 |
| 5 | `unit_procedure` | 단위 시술 | 제일 작은 단위 행위 = 계열 × [하위 계열 · 성분] × 부위 × 기법 (원천에 있는 조합만) | U5-{nnn}<br>꼴 {"U9-9": 162} | id · key{family,sub_family,ingredient,site,technique} · name · site_basis · decided_by · sources[] | synonyms[]{text,type,src,ambiguous} · candidate_of[] · uses_product[] · purposes[] · route_status · market[] · pih_not_applicable · ops · step4_attrs · dose_range_text · evidence_level · notes | `step5-units.json` units[] | **162** 하위 키 30 · 성분 키 25 · 부위 특수(해당 없음 · 병변 단위) 31 | 162 | _RESUME §2 10-27 「시술 = 무엇을 × 어디에 × 어떻게」 · 10-29 「5단계 원칙」 · 로그 step5 §3-1 |
| 6 | `package` | 패키지 | 이름 있는 단위 시술 묶음(일반 패키지 · 회차 묶음 · 병원 시그니처) | P6-{nn}<br>꼴 {"P9-9": 24} | id · name · kind · recommendable | shape · menu_group · same_day_raw · synonyms[] · price[] · description · notes · detail_raw · ledger_id | `step6-packages.json` packages[] | **24** kind {'일반 패키지': 19, '병원 시그니처': 2, '회차 묶음': 3} | 24 | _RESUME §2 10-29 「6단계 패키지 이해」 · 「6단계 시작 — 계획 승인」 |
| 7 | `concern` | 고민 | 상태 이름(주름 · 처짐 · 기미 …) — taxonomy problem 3층 중 「고민」 갈래 + 결정 노드 3 | 대분류 P{n} · 중분류 P{n}-{n} · 항목 auto-{n}-{timestamp} · 결정 노드 J{n}-{한글} — 4꼴<br>꼴 {"P9": 12, "P9-9": 31, "auto-9-9": 11, "J9-가": 3} | id · name | en · source_name/source_label · kind · sites[] · parent/subcategory · related[](J10) · basis · decided_by | `step7-concerns.json` concerns.categories[node] · subcategories[node] · items[kind=고민] · extra_items[] | **57** 대분류 12 · 중분류 31 · 항목 11 · 결정 노드 3 | 57 | _RESUME §2 10-29 「7단계 시작」 · 「7단계 조사 반영」 · 로그 step7 §3-1 |
| 8 | `purpose` | 목적 | 시술이 하는 일(리프팅 · 재생 · 볼륨 회복 …) — 고민과 같은 말이면 노드를 따로 안 세우고 그 고민에 붙임 | id 없음 — 이름 문자열이 곧 키(엣지 쪽에서는 「목적:{이름}」 문자열)<br>꼴 {"이름 문자열": 13} | name · kind · node | from[] · same_as_concern · aliases[]{source,text} | `step7-concerns.json` purposes[] (node=true) | **13** purposes 30 중 노드 13 · 고민에 붙음(same_as_concern) 17 | 13 | _RESUME §2 10-29 J4 · 로그 step7 §3-4 · step7-decisions rules R6 |
| 9 | `recommend_combo` | 추천 조합(사이트 「추천 패키지」) | 원천이 고민 · 목적별로 묶어 둔 시술 조합(원천별 · 합치지 않음) — 6단계 패키지와 다름 | RC-{원천}-… (RC-PC · RC-SQ · RC-RE · RC-OP …)<br>꼴 {"RC-PC-P9-9": 24, "RC-RE-R9": 7, "RC-SQ-9": 8, "RC-OP-Wrinkl-가": 3, "RC-OP-Saggin-가": 3, "RC-OP-Volume-가": 3, "RC-OP-Skin-가": 3, "RC-OP-Pigmen-가": 3, "RC-OP-Acne-가": 3, "RC-OP-Hair-가": 3, "RC-OP-Body-가": 3, "RC-AN-9가": 2, "RC-AN-9가+": 1, "RC-AG-9가": 3, "RC-AG-9가+": 1, "RC-CP-lifting": 1, "RC-CP-wrinkle": 1, "RC-CP-volume": 1, "RC-CP-skin_texture": 1, "RC-CP-pigment": 1, "RC-CP-hair_removal": 1, "RC-CP-body_contouring": 1, "RC-CP-acne": 1, "RC-CP-rejuvenation": 1} | id · kind · source · name · anchor | tier · tier_label_site · components[] · products_text · price · effect{} · sales_copy{default_response} · site_names | `step7-concerns.json` combos[] | **79** kind {'고민 패키지(사이트 「추천 패키지」)': 24, '목적 레시피': 7, '세션 조합(순서)': 8, '중증도 조합': 24, '연간 플랜': 3, '연령 플랜': 4, '비교': 9} | 79 | _RESUME §2 10-28 U3 「추천 조합 노드 한 타입」 · 10-29 「6단계 패키지 이해」(사이트 「추천 패키지」 = 7단계 추천 조합) |
| 10 | `check_condition` | 확인 조건 | 사람 쪽 조건(임신 · 약물 · 체질 …) — 시술 → 조건 엣지에 금기 · 주의 · 확인만 등급 | C-{영문 약어}<br>꼴 {"C-{ABBR}": 53} | id · name · match_pattern | n_claims · sources[] | `step8-relations.json` conditions.nodes[] | **53**  | 53 | _RESUME §2 10-28 「사람 조건 금기 노드 이름 = 확인 조건」 · 로그 step8 §3-10 |
| 11 | `complication` | 합병증(부작용 섞임 — 결정 묶음 B1) | 계열에 생길 수 있는 이상 반응 — 지금은 흔한 예상 반응(부작용)과 드문 · 중대 반응(합병증)이 한 노드 종류에 섞여 있음 | CX-{계열}-{nn}<br>꼴 {"CX-M9-9": 65} | id · name · family · severity | severity_site · incidence · onset · duration · mechanism · risk_factors · management · prevention · evidence[] · units_inherit[] | `step8-relations.json` safety.complications[] | **65** severity {'mild': 38, 'moderate': 13, 'severe': 11, 'critical': 3} · 계열 10 | 65 | 로그 step8 §3-11 · _RESUME §2 10-28 「해부학 용어 = … 합병증 → 안전 정보(8단계)」 · 사용자 10-29 「부작용 ≠ 합병증」(브리프) |
| 12 | `evidence_statement` | 근거 문장 | 계열 단위 문헌 문장(기전 · 효과 · 이상 반응) + 환자용 4개 언어 풀이 | ST-{계열}-{field}-{nn}<br>꼴 {"ST-M9-moa-9": 50, "ST-M9-adverse_effects-9": 32, "ST-M9-effects-9": 37} | id · family · field(moa · effects · adverse_effects) · statement · evidence[] | accuracy_score · accuracy_note · patient{ko,en,zh,ja} · added_at | `step8-relations.json` evidence.statements[] | **119** field {'moa': 50, 'adverse_effects': 32, 'effects': 37} | 119 | 로그 step8 §3-12 · source-map U4(근거 노드 8단계) |
| 13 | `evidence_source` | 근거 출처 | 문헌(PMID · DOI) · 웹(URL) · 가이드(원천 출처 문자열) | EV-LIT-{nnn} · EV-WEB-{nnn} · EV-GD-{nnn}<br>꼴 {"EV-LIT-9": 25, "EV-WEB-9": 29, "EV-GD-9": 15} | id · kind | literature: pmid · doi · pmc · title · journal · year · authors · oa_url · web: url · urls[] · multi_url · guides: label · pmc · used_by[] | `step8-relations.json` evidence.literature[] · web[] · guides[] | **69** 문헌 25 · 웹 29 · 가이드 15 | 69 | step8-decisions web_evidence_rule · guide_not_source_rule |

- 페이지에만 있는 종류: **끝점 묶음 43** — 8단계 끝점이 하나로 안 좁혀진 것(units:a,b,c · bundle:M\|M · all · 해석 안 된 문자열) — 실버 파일에는 노드가 아니라 끝점 문자열 · target 칸 · 실버 자리 `step8-relations.json` edges[].a · b(문자열) · conditions.claims[].target · avoid_edges[].to → 결정 U3

### 1-1. 실버에 있으나 노드가 아닌 개체

| 개체 | 자리 | 셈 | 지금 | 메모 | 추천 |
|---|---|---|---|---|---|
| 라인(상위 제품) | `step1-products.json lines{} · items[].line` | lines 11(summary.lines.count 20) · 라인 품목 26 · items[].line 모양 {'라인 구성': 17, '라인': 11, '품목': 6} | 제품 속성(페이지 엣지 없음) | items[].line 이 두 모양(role 「라인」 {items[]} · 「라인 구성」 {members[]}) — 칸 모양 불일치 | 제품 → 제품 「라인 품목」 엣지(결정 10-27 「라인 = 상위 제품 · 품목 = 하위 제품」) |
| 업체(제조 · 수입 · 판매) | `step1-products.json items[].6_companies` | 이름 269종(중복 제거 · id 없음) | 제품 속성 {name, role, basis} | DEC-003 은 「제조사 원장」(국문명 · 원어명 · 국가 · 동의어)을 정했으나 실버 1단계는 업체 id 없이 이름 문자열 | 결정 묶음 B9 |
| 허가 | `step1-products.json items[].4_license.licenses[] · history[]` | 정상 327 · 이력 104 | 제품 속성 | SPEC-004 는 product_item 노드였음(옛) | 제품 속성 유지(1단계 「제품 ↔ 허가만」 · 허가 이름은 허가 쪽에만) |
| 시장가 행 | `step5-units.json market[] · units[].market[]` | market 122 | 단위 시술 속성 | 10-27 「시술 1회 = 단위 시술 + 제품 + 규격 · 양, 가격은 그 조합에」 | 단위 시술 속성(가격 키 = 단위 시술 × 제품 × 규격) |
| 위험지대(zone) | `step3-sites.json nodes[].danger_zone · step8 safety.site_caution[].zone` | site_caution 22 · zone 11 | 부위 속성 + 위험지대 주의 엣지 속성 |  | 엣지 속성 유지(로그 step8 §3-11) |
| 경과 타임라인 | `step8 safety.timelines[]` | 10 | 계열 · 하위 · 단위 시술 원문 속성(attach) | id 가 원천 영문 키(botox · ha-filler …) | 속성 유지 · 상속 규칙 I8 |
| 관계 주장 · 조건 주장 | `step8 claims[] · conditions.claims[]` | 관계 주장 395 · 조건 주장 373 | 엣지 안 칸(쌍 하나에 엣지 하나 + 주장 칸) |  | 엣지 속성 유지(로그 step8 §3-1) |

## 2. 엣지 종류(추천 — 합친 뒤)

| # | 내부 이름 | 이름 | 뜻 | 시작 → 끝 | 방향 | 속성 | 정본 · 칸 경로 | 셈(파일) | 계열 단위(상속) | 페이지 종류에서 | 왜 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `product_family` | 계열 판정 | 제품이 어느 계열 제품인가(2단계 판정 · 주 1 + 보조) | 제품 → 계열 | True | role(주 · 보조) · sub_family · also_sub_families · verdict · evidence_level · conflict · confirm_question · pending_director · basis | `step2-families.json` product_family[].family · also_families[] | 행 354 · 주 351 · 보조 19 |  | prod_fam, prod_fam_also | 같은 뜻(계열에 속함) · 주/보조는 속성(10-28 「하위 계열도 주 · 보조로」) |
| 2 | `key_family` | 단위 시술 키 — 계열 | 단위 시술 정체의 첫 칸(무엇을) | 단위 시술 → 계열 | True | sub_family(J1 안 C 계열만) · ingredient | `step5-units.json` units[].key.family · sub_family · ingredient | 162 |  | unit_fam | 제품의 「계열 판정」과 이름이 같았지만 뜻이 다름 — 이건 정체(키) 칸이라 판정 · 근거 칸이 없고 하나뿐 · 바뀌면 다른 단위 시술 |
| 3 | `key_site` | 단위 시술 키 — 부위 | 어디에 | 단위 시술 → 부위 | True | site_basis(원천 · 기본값) | `step5-units.json` units[].key.site | 131(부위 노드 있음) · 특수 부위 31 은 엣지 없음 |  | unit_site | 그대로 |
| 4 | `key_technique` | 단위 시술 키 — 기법 | 어떻게 | 단위 시술 → 기법 | True | step4_attrs(층 · 대상 근육 …) | `step5-units.json` units[].key.technique | 162 |  | unit_tech | 그대로 |
| 5 | `child_of` | 상위 | 같은 종류 노드의 상하 관계(부위 트리 · 기법 큰/세부 · 고민 3층) | 부위 · 기법 · 고민 → 같은 종류 | True |  | `step3-sites.json · step4-techniques.json · step7-concerns.json` nodes[].parent · nodes[].parent · subcategories[].parent · items[].subcategory · extra_items[].parent | 부위 49 · 기법 12 · 고민 43 |  | site_parent, tech_parent, con_parent(상위만) | 세 트리 모두 「상위」 한 뜻 — 옛 SPEC-004 has_child 도 한 종류 |
| 6 | `concern_related` | 관련 고민(상위 없음) | 상위가 없는 결정 노드가 걸쳐 있는 고민(J10 피부결 → 모공 · 흉터 · 색소 · 항노화) | 고민 → 고민 | False |  | `step7-concerns.json` concerns.extra_items[].related[] | 4 |  | con_parent(라벨 「관련(상위 없음)」) | 페이지는 「상위 고민」 한 종류에 라벨로 섞음 — 상하가 아니라 옆 관계라 나눔 |
| 7 | `family_technique` | 계열 기법 | 계열이 기본으로 쓰는 기법 · 함께 쓰는 기법 | 계열 → 기법 | True | role(기본 · 함께) · default_layer · basis | `step4-techniques.json` family_defaults[].default · also[] | 기본 27 · 함께 7 |  | fam_tech, fam_tech_also | 같은 뜻 · 기본/함께는 속성 |
| 8 | `uses_product` | 쓰는 제품(저장) | 원천 이름이 이 제품을 부를 때만 저장한 단위 시술 → 제품 | 단위 시술 → 제품 | True | basis · recommendable | `step5-units.json` units[].uses_product[] | 43 |  | unit_prod | 그대로. 「상속 후보(prod_unit_inh)」는 저장 엣지가 아니라 상속 규칙 I4 의 조회 결과 → 골드 |
| 9 | `contains` | 패키지 구성 | 패키지가 담은 단위 시술(확정) · 못 푼 자리(슬롯 후보 + 원천 질문) | 패키지 → 단위 시술 | True | order · status(확정 · 슬롯 후보) · quantity_raw · sessions · evidence_level · origin_question · basis | `step6-packages.json` contains[] · slots[].candidates[] | 구성 49 · 슬롯 8(후보 22) |  | pkg_unit, pkg_slot | 같은 뜻(구성) · 슬롯은 「후보 여럿」 표시 |
| 10 | `treats` | 추천(고민 · 목적 → 시술) | 원천 구조(①~⑧)가 고민 · 목적에 적어 둔 시술 | 고민 · 목적 → 단위 시술 · 계열 | True | source · source_id · target_kind(단위 시술 · 계열만) · lowering · resolve_flag · site_check · anchor_sites · severity · basis · evidence | `step7-concerns.json` edges[] (from · from_concerns · purpose_nodes → to_units · to_family) | 행 537 · target_kind {'단위 시술': 461, '계열만': 75, '대상 없음': 1} | 예 | con_unit, con_fam | 같은 뜻 · 끝이 계열이면 상속(target_kind 속성) |
| 11 | `concern_site` | 고민 부위 | 부위가 붙은 고민의 부위(D-07 분리) | 고민 → 부위 | True |  | `step7-concerns.json` concerns.*.sites[] | 22 |  | con_site | 그대로 |
| 12 | `anchors_combo` | 추천 조합 앵커 | 추천 조합이 걸린 고민(· 목적) | 고민 → 추천 조합 | True | kind | `step7-concerns.json` combos[].anchor.concern · concerns | 83 |  | con_combo | 그대로 |
| 13 | `combo_component` | 조합 구성 | 추천 조합의 구성 시술 | 추천 조합 → 단위 시술 | True | order · status · flag · basis | `step7-concerns.json` combos[].components[].units[] | 구성 칸 199 · 페이지 엣지 944 |  | combo_unit | 그대로 |
| 14 | `procedure_relation` | 시술 ↔ 시술 관계 | 시너지 · 순서 · 간격 · 같은 날 · 대체 · 금기를 한 엣지의 주장 칸으로(쌍 하나에 엣지 하나) | 단위 시술 · 계열 · (끝점 묶음) → 같음 | 주장마다(claims[].directed) | claims[]{kind, interval{days, first, same_day, open_high, by_sub_condition, options}, level_original, level_site, reason, evidence_kind, gate_status, review_status} · conditional_claims · self_pair · review_status | `step8-relations.json` edges[] + claims[] | 엣지 221 · 주장 395 · 끝점 {'all': 1, 'units': 137, 'bundle(여럿)': 2, 'family': 177, 'units(여럿)': 124, 'family(여럿)': 1} | 예 | rel, rel_fam | 같은 뜻 — 끝점 수준(단위 · 계열 · 묶음)은 끝점 속성(endpoint_levels) |
| 15 | `concern_avoid` | 피함(금기 조합) | 고민 조건 금기 — 이 고민이면 이 시술을 피함 | 고민 → 단위 시술 · 계열 | True | qualifier · scope · default_apply · scope_conditional · grade_original · strength_original · concern_basis · text | `step8-relations.json` avoid_edges[] | 주장 5 · 끝 {'계열': 3, '단위 시술': 2} | 예 | avoid, avoid_fam | 같은 뜻(U8-2 concern_avoid 한 타입) · 계열 끝은 상속 |
| 16 | `requires_check` | 확인 조건 | 시술(계열 · 제품 · 단위) → 사람 조건 · 등급 3분류(금기 · 주의 · 확인만) | 계열 · 제품 · 단위 시술 · (끝점 묶음) → 확인 조건 | True | grade_original · grade_site · grade3 · kind · rule · where · strength_original · scope_conditional | `step8-relations.json` conditions.claims[] | 주장 373 · 대상 수준 {'기법 조건': 3, '해석 안 됨': 1, '용도 조건': 1, '공통': 12, '계열': 340, '제품': 6, '원장 항목(행선지 없음)': 2, '단위 시술': 3, '복합(나눔)': 3, '모든 시술': 2} · 등급 {'금기': 197, '확인만': 74, '주의': 64, '조건 아님(상담)': 22, '확인만(고지)': 11, '조건 아님(시술 준비)': 5} | 예 | cond, cond_fam | 같은 뜻 · 대상 수준은 속성. 단 grade3 「조건 아님(상담 · 시술 준비)」 27 은 엣지가 아님(결정 묶음 B8) |
| 17 | `has_complication` | 합병증 | 계열 → 합병증 노드(부작용 분리 뒤엔 중대 반응만 — B1) | 계열 → 합병증 | True | severity_site | `step8-relations.json` safety.complications[].family(edge 칸 「has_complication」) | 65 | 예 | fam_cx | 그대로 · 부작용은 B1 |
| 18 | `site_caution` | 위험지대 주의 | 부위 × 계열 위험지대(혈관 · 신경 · 안전 층) | 부위 → 계열 | True | zone · danger_level · vessels · nerves · tissue_data · clinical_pearls · safe_injection_depth · site_mapping · units_affected | `step8-relations.json` safety.site_caution[] | 22(계열 {'M1': 11, 'M2': 11}) | 예 | site_caution | 그대로 |
| 19 | `has_statement` | 근거 문장 | 계열 → 근거 문장 | 계열 → 근거 문장 | True | field | `step8-relations.json` evidence.statements[].family | 119 | 예 | fam_stmt | 그대로 · 문장 종류 재분류는 B2 |
| 20 | `cites` | 출처 | 근거 문장 · 합병증이 기댄 근거 출처 | 근거 문장 · 합병증 → 근거 출처 | True |  | `step8-relations.json` evidence.statements[].evidence[] · safety.complications[].evidence[] | 문장 119 · 합병증 38 |  | stmt_ev, cx_ev, ev_claim | 「출처」 3종은 한 뜻. 관계 주장의 출처(ev_claim)는 엣지가 아니라 주장 칸 claims[].evidence + guides.used_by — 페이지는 주장 출처를 끝점 노드에 이어 그렸음(주장 단위 정보가 사라짐) |
| 21 | `line_item` | 라인 품목 | 라인(상위 제품) → 품목(하위 제품) | 제품 → 제품 | True | decision | `step1-products.json` lines{}.items[] · items[].line | 라인 11 · 품목 26 |  | (새로) | 페이지에 없던 것 — 10-27 결정 ④(라인 = 상위 제품)가 실버에 칸으로 있음 |

### 2-1. 페이지 32종 → 추천 대응

| 페이지 종류 | 라벨 | 셈(페이지) | 시작 → 끝 | 상속 | 칸 | → 추천 |
|---|---|---|---|---|---|---|
| `prod_fam` | 계열 | 346 | prod → fam |  | step2-families.json product_family.family | product_family |
| `prod_fam_also` | 함께 계열 | 19 | prod → fam |  | step2-families.json product_family.also_families | product_family |
| `site_parent` | 상위 부위 | 49 | site → site |  | step3-sites.json nodes.parent | child_of |
| `tech_parent` | 상위 기법 | 12 | tech → tech |  | step4-techniques.json nodes.parent | child_of |
| `fam_tech` | 기본 기법 | 27 | fam → tech |  | step4-techniques.json family_defaults.default | family_technique |
| `fam_tech_also` | 함께 쓰는 기법 | 7 | fam → tech |  | step4-techniques.json family_defaults.also | family_technique |
| `unit_fam` | 계열 | 162 | unit → fam |  | step5-units.json units.key.family | key_family |
| `unit_site` | 부위 | 131 | unit → site |  | step5-units.json units.key.site | key_site |
| `unit_tech` | 기법 | 162 | unit → tech |  | step5-units.json units.key.technique | key_technique |
| `unit_prod` | 쓰는 제품(저장) | 43 | unit → prod |  | step5-units.json units.uses_product | uses_product |
| `prod_unit_inh` | 상속 후보(계열 · 조회 때) | 1364 | prod → unit | 예 | step5-units.json product_links.inherited_candidates | (저장 엣지 아님 — 상속 규칙 I4 · 골드) |
| `pkg_unit` | 구성 | 48 | pkg → unit |  | step6-packages.json contains | contains |
| `pkg_slot` | 구성 후보(슬롯 · 원천 질문) | 22 | pkg → unit |  | step6-packages.json slots.candidates | contains |
| `con_parent` | 상위 고민 | 44 | con → con |  | step7-concerns.json concerns.subcategories.parent · items.subcategory · extra_items.parent | concern_related |
| `con_site` | 고민 부위 | 22 | con → site |  | step7-concerns.json concerns.*.sites | concern_site |
| `con_unit` | 추천 단위 시술 | 639 | con·pur → unit |  | step7-concerns.json edges.to_units | treats |
| `con_fam` | 추천 계열(계열만) | 56 | con → fam | 예 | step7-concerns.json edges.to_family(target_kind 계열만) | treats |
| `con_combo` | 추천 조합 | 83 | con → combo |  | step7-concerns.json combos.anchor | anchors_combo |
| `combo_unit` | 조합 구성 | 944 | combo → unit |  | step7-concerns.json combos.components.units | combo_component |
| `set_member` | 묶음 원소 | 185 | set → fam·unit |  | step8-relations.json edges a·b(units:· bundle:) | (결정 묶음 B3 — 추천: 끝점 속성 candidates[] 로, 엣지 종류 없앰) |
| `rel` | 시술 ↔ 시술 관계 | 89 | unit·set → unit·set |  | step8-relations.json edges(claims) | procedure_relation |
| `rel_fam` | 시술 ↔ 시술 관계(계열 · 묶음 단위) | 131 | fam·set → fam·unit·set | 예 | step8-relations.json edges(끝점이 계열 · 묶음 · 전체) | procedure_relation |
| `avoid` | 피함(금기 조합) | 1 | con → unit |  | step8-relations.json avoid_edges | concern_avoid |
| `avoid_fam` | 피함(계열 단위) | 1 | con → fam | 예 | step8-relations.json avoid_edges(끝점 계열) | concern_avoid |
| `cond` | 확인 조건 | 12 | prod·unit·set → cond |  | step8-relations.json conditions.claims | requires_check |
| `cond_fam` | 확인 조건(계열 단위) | 219 | fam·set → cond | 예 | step8-relations.json conditions.claims(대상 계열 · 공통) | requires_check |
| `fam_cx` | 합병증 | 65 | fam → cx | 예 | step8-relations.json safety.complications(has_complication 계열) | has_complication |
| `site_caution` | 위험지대 주의 | 22 | site → fam | 예 | step8-relations.json safety.site_caution | site_caution |
| `fam_stmt` | 근거 문장 | 119 | fam → stmt | 예 | step8-relations.json evidence.statements(family) | has_statement |
| `stmt_ev` | 출처 | 119 | stmt → ev |  | step8-relations.json evidence.statements.evidence | cites |
| `cx_ev` | 출처 | 38 | cx → ev |  | step8-relations.json safety.complications.evidence | cites |
| `ev_claim` | 관계 원문 출처 | 41 | ev → fam·unit·set |  | step8-relations.json evidence.guides.used_by(claims) | cites |

- 이름이 같은데 뜻이 다른 것: 「계열」 2번(제품 = 판정 · 근거 칸 있음 / 단위 시술 = 키 · 하나뿐) → `product_family` · `key_family` 로 나눔. 「상위 고민」 안의 「관련(상위 없음)」 → `concern_related` 로 나눔.
- 뜻이 같은데 나뉜 것: 「출처」 3종 · 단위/계열로 갈린 관계 · 피함 · 확인 조건 · 추천 · 주/보조로 갈린 계열 · 기법 · 확정/슬롯 구성 · 세 트리의 상위 → 합침(수준 · 역할은 속성).
- 저장 엣지가 아닌 것: 「상속 후보(prod_unit_inh)」(상속 I4 의 계산 결과) · 「묶음 원소(set_member)」(U3).

## 3. 용어집

| 용어 | 정의 | 출처 |
|---|---|---|
| **단위 시술** | 제일 작은 단위 행위 = 무엇을(계열) × 어디에(부위) × 어떻게(기법). 제품 · 용량은 속성, 목적은 고민 → 시술 엣지, 패키지는 단위 시술 묶음. 키 = 계열 × [하위 · 성분(J1 안 C 계열만)] × 부위 × 기법, 원천에 있는 조합만 | _RESUME §2 10-27 「taxonomy 는 … 분류 트리」 · 10-29 「5단계 시작」 · 로그 step5 §3-1 |
| **계열** | 무엇을 — 공식 일반명으로 부르는 약제 · 장비 계열(M1 보툴리눔 톡신 …). 기준은 교과서 · 임상 · 학회 문헌(literature-evidence M1~M17). 계열이 없으면 시술을 빼지 않고 계열을 늘림(N1~N10) | _RESUME §2 10-27 「계열 이름 = 공식 일반명」 · 10-28 「2단계 계열 기준」 · 10-29 「5단계 원칙」 |
| **하위 계열** | 계열 안의 매질 · 재료 축(M8 광원 매질 · M9 HIFU/RF · M5 PRP/엑소좀 …). 주 1 + 보조(also_sub_families). 단위 시술 키에는 「무엇을」 자체를 바꾸는 계열만(J1 안 C — M5 · M8 · M9 · M13 · M16 성분) | _RESUME §2 10-28 「하위 계열도 주 · 보조로」 · 「M8 하위 계열 = 광원 매질 한 축」 · 로그 step5 §3-1 |
| **기법** | 어떻게 — 큰 기법 + 세부 기법 노드(K01~K13). 층 · 깊이 · 대상 근육 · 도구는 단위 시술 속성, 펄스 · 박피 · 가능 방식은 장비 속성 | _RESUME §2 10-28 「4단계 기법 조사 반영 J1 안 1」 |
| **계열 기본 기법** | 계열이 따로 말하지 않을 때 쓰는 기법(family_defaults.default) · 함께 쓰는 기법(also) | step4-techniques.json family_defaults · _RESUME §2 10-28 |
| **부위** | 시술 받는 사람 몸 겉에서 가리킬 수 있는 자리. 쪼개는 규칙 = ① 원천이 따로 부른다 ② 가능 시술 · 안전이 달라진다. 뼈 · 근육 · 혈관 · 층은 부위 아님 | _RESUME §2 10-27 「부위 트리 확정」 · 10-28 「부위 기준 = 어디에 맞냐」 |
| **부위 이름(일반인)** | 노드 이름 = 상담 용어(일반인 용어) | _RESUME §2 10-28 「부위 노드 이름 2벌」 |
| **부위 이름(전문의)** | anatomical_name — 같은 겉자리의 의학 이름만(예: 팔자 = nasolabial fold). 근육이 섞이면 겉자리 이름으로 바꾸고 근육은 4단계 대상 근육 | _RESUME §2 10-28 「부위 노드 이름 2벌」 · 「해부학 용어 = 시술 방법 · 작용기전 · 안전 쪽」 |
| **묶음 부위** | 하위를 묶는 부위 노드(…(묶음) · -group). 묶음 노드는 동의어 없음 · 단위 시술 키를 만들지 않음(「턱보톡스」 = 턱끝 · 사각턱 · 턱선 후보 전부) | 로그 step5 §3-2 · step3 |
| **특수 부위 「해당 없음」 · 「병변 단위」** | 해당 없음 = 전신 투여(수액 · 태반 · 성장호르몬) · 병변 단위 = 병변 수 · 면적으로 매기는 시술(점 · 문신 · 쥐젖 · 켈로이드). 부위 노드 없음 | step5-units.json rules.special_sites · 로그 step5 §3-4 |
| **기본값 부위(site_basis 기본값)** | 부위 이름 없는 얼굴 계열 항목 = 얼굴 전체 + 「기본값」 표시(J2). 몸 계열은 기본값 없음 | 로그 step5 §3-4 |
| **제품** | 허가 · 업체 · 규격을 가진 제품 · 장비. 이름 칸 3개(대표 한글 1 · 허가 이름은 허가 쪽에만 · 검색 이름[]). 같은 성분 · 용량만 다른 허가는 한 제품 | _RESUME §2 10-27 「이름 규칙」 · 「같은 성분 · 용량만 다른 허가는 한 제품」 |
| **라인 · 품목** | 라인 = 상위 제품(쥬비덤 · 레스틸렌), 개별 품목 = 하위 제품 | _RESUME §2 10-27 「제품 이름 정규화 ④」 |
| **허가 상태** | 정상 · 허가번호 미확인(추천 포함) · 확인 불가(추천 제외) · 미허가 · 허가 취소(이력 · 추천 제외) · 허가 대상 아님(출처 있을 때만) | _RESUME §2 10-27 「허가 규칙」 · 10-28 「허가번호 미특정 규칙」 · step1 basis.fields |
| **장비 이름 = 시술 동의어** | 포텐자 · 써마지 · 울쎄라처럼 장비 이름이 시술 이름으로 쓰이면 장비 노드는 그대로 두고 그 이름을 단위 시술 동의어로도 연결 | _RESUME §2 10-27 「장비 이름이 시술 이름으로 쓰이는 경우」 |
| **패키지** | 이름 있는 단위 시술 묶음 — 일반 패키지 · 회차 묶음 · 병원 시그니처(고정 가격 · 추천 기본 제외). 이름 없는 묶음 · 메뉴 분류 이름은 패키지 아님. 구성은 원천에 적힌 만큼 | 로그 step6 §3-1 · _RESUME §2 10-29 「6단계 패키지 이해」 |
| **슬롯** | 패키지 구성 중 못 푼 자리 — 후보 전부 + 원천 질문(「구성 없음」 아님) | 로그 step6 §3-2 |
| **추천 조합** | 원천이 고민 · 목적별로 적어 둔 시술 조합(고민 패키지 · 중증도 조합 · 비교 · 세션 조합 · 목적 레시피 · 연령 · 연간 플랜). 원천별 · 합치지 않음. 사이트 「추천 패키지」 = 이것(6단계 패키지 아님) | _RESUME §2 10-28 U3 · 10-29 「6단계 패키지 이해」 · 로그 step7 §3-8 |
| **영업 문구** | salesPitch · upsellHook — 보관 · 기본 응답 제외(레시피 환자 설명 · 비유는 상담 문구라 포함) | 로그 step7 §3-9 · step7 rules R9 |
| **고민** | 상태 이름. 정본 = taxonomy problem 3층 중 「고민」 갈래 + 결정 노드(J8 자갈턱 · J10 피부결 · J14 잇몸미소). 쁘띠시술(시술 범주) · 기타(묶음)는 고민 아님 | 로그 step7 §3-1 · _RESUME §2 10-29 |
| **목적** | 시술이 하는 일(13). 고민과 같은 말이면 목적 노드를 따로 안 세우고 그 고민에 붙임(R6) | 로그 step7 §3-4 · step7 rules R6 |
| **중증도** | 고민의 정도(초기 · 경미 · 중기 · 중등도 · 심화 · 중증). 중증도로 나뉜 하위 고민이 있으면 하위로(주름), 없으면 상위 + severity 속성 | step7 rules R18 · _RESUME §2 10-29 「주름 중증도 → 하위 고민」 |
| **확인 조건** | 사람 쪽 조건(임신 · 수유 · 약물 · 체질 · 병력 …) 원장. 시술 → 조건 엣지에 등급(금기 · 주의 · 확인만). 사전 체크 · 금기 = 같은 「확인 조건」 | _RESUME §2 10-28 「사람 조건 금기 노드 이름 = 확인 조건」 · 로그 step8 §3-10 |
| **등급 3분류(grade3)** | 금기 · 주의 · 확인만(+ 확인만(고지)). 원문 등급(grade_original)은 그대로 두고 덧붙임 | step8-decisions labels.grade3 · 로그 step8 §3-10 |
| **피함(금기 조합)** | 고민 조건 금기(「기미에 고에너지 레이저 금지」) = 고민 → 단위 시술 엣지 concern_avoid. 확인 조건 노드를 따로 세우지 않음 | step8-decisions user_decisions U8-2 · 로그 step8 §3-8 |
| **관계 주장(claim)** | 시술↔시술 엣지 안에 쌓는 원천 주장 한 줄(원천 · 원문 · 종류 · 원문 등급 · 사이트 라벨 · 간격 · 먼저 하는 쪽 · 이유 · 조건 · 근거) | 로그 step8 §3-1 · DEC-001 D-03 · D-04 |
| **시너지 · 순서 · 간격 · 금기** | 시술↔시술 엣지 하나의 속성(주장 종류). 「대신」은 대체(택 1)로 세고 시너지로 세지 않음 | _RESUME §2 10-26 「방향: 메달리온」 · 로그 step8 §3-2 |
| **간격(interval)** | days [하한, 상한](일) · first(a\|b) · same_day · open_high. 추천 · AI 는 이 숫자 칸만 읽고 원문은 보관 | step8 reading_contract · 로그 step8 §3-4 · §3-5 |
| **합병증** | 계열에 생길 수 있는 드물거나 중대한 이상 반응 — 계열마다 노드 · 원천 없는 계열은 gap. 지금 노드 65 안에 흔한 예상 반응(severity mild 38)이 섞여 있음 → B1 | 로그 step8 §3-11 · 이 조사 B1 |
| **부작용** | 흔한 예상 반응(멍 · 부기 · 홍반 · 통증 …). 사용자 10-29 「부작용 ≠ 합병증」. 지금 네 곳에 흩어짐: 합병증 노드 severity mild · family_text 「부작용 문장 common」 · 근거 문장 adverse_effects · 5단계 extracted safety.common 키 → B1 | 브리프(사용자 10-29) · DEC-001 D-06 「안전 엣지(금기 · 간격 · 부작용)」 · step8 safety.family_text |
| **위험지대** | 부위 × 계열의 혈관 · 신경 · 안전 층 위험(anatomy-danger-zones) — 부위 노드가 아니라 위험지대 주의 엣지 속성 | 로그 step8 §3-11 · _RESUME §2 10-28 「해부학 용어 …」 |
| **필수 고지** | consent mandatory_disclosures — 원문 그대로 보관(쪼개지 않음) · 계열 원문 속성 | _RESUME §2 10-28 「자리 없는 안전 · 상담 원천 4개」 · 로그 step8 §3-11 |
| **근거 문장** | 계열 단위 문헌 문장(moa · effects · adverse_effects) + 환자용 4개 언어. 정확도 점수는 문장 속성 | step8 evidence.statements · 이 조사 B2 |
| **근거 출처** | 문헌(PMID · DOI) · 웹(URL) · 가이드(원천 출처 문자열). URL 없는 출처 문자열 = 웹 아님(「원문 출처 문자열(내부 · 통설)」) · 「;」로 이은 URL = multi_url 표시 | step8-decisions web_evidence_rule · guide_not_source_rule |
| **근거 강도** | 원문 등급만(숫자를 만들지 않음) | 로그 step8 §3-12 |
| **evidence_level 약 · 중** | 판정 근거가 약하면 값을 넣고 「약」 + 확인 질문(open 으로 두지 않음) | _RESUME §2 10-28 「2단계 open 40 해결안」 |
| **충돌** | 원천끼리 다른 말(순서 · 같은 날 · 간격 · 조건 등급 · 대기 기간) — 전부 보존 + 충돌 표시 · 자동으로 고르지 않음(D-13b) | step8-decisions user_decisions 「충돌」 · 로그 step8 §3-7 |
| **조건부(단위 시술 미특정)** | 끝점 원문에 출력 · 깊이 한정어가 있는데 끝점이 묶음으로 열렸으면 scope 「조건부 — 단위 시술 미특정」 · default_apply false — 기본 상속 · 기본 응답에서 뺌 | step8-decisions scope_rule · user_decisions F1 |
| **하위 조건별 값(by_sub_condition)** | 원문이 하위 조건으로 갈리면 겉 칸을 비우고 options[].sub_condition 별 값을 읽음 | step8-decisions user_decisions F2 · reading_contract |
| **gap(정보 없음)** | 원천이 없어 비워 둔 것 — 합병증 gap 계열 · PIH gap 단위 시술 · 그 부위 단위 시술 없음. 채우려면 원천이 먼저 | 로그 step8 §6 · step5 pih_gap_units |
| **끝점 묶음** | 8단계 끝점 원문이 단위 시술 하나로 안 좁혀진 것(units:a,b,c · bundle:M\|M · all). 실버에선 끝점 문자열 · 페이지에선 노드 → B3 | step8 edges a · b · silver-graph-build.py endpoint() |
| **후보 전부** | 이름이 여럿을 가리키면 고르지 않고 후보를 전부 달고 표시(ambiguous) — 외부 LLM 이 고르거나 되묻기 | _RESUME §2 10-27 「계열 이름 = 공식 일반명」(「보톡스」 둘 다) · SPEC-004 §3.3.2(옛) · step7 site_rules |
| **부위로 내림** | 고민 · 끝점에 부위가 있으면 그 부위(또는 하위)의 단위 시술로 내림. 그 부위에 그 계열 단위 시술이 없으면 R21 부위 올라가기 — 조상 노드 자신 → 최상위 영역의 「전체」 노드까지 · 영역 경계 안 넘음 · 그래도 없으면 계열만 + 「이 부위 단위 시술 없음」(10-29 이전 「계열 후보 전부」 대체) | step7-decisions site_rules.climb · 로그 step7 §3-6 · §3-7(옛) · 코디 알림 · 사용자 10-29 |
| **원천 질문** | 규칙으로 하나로 안 정해지는 것만 사람(병원 · 의료진 · 원장님)에게 묻는 것 — 값은 추천값으로 두고 답 오면 그 행만 | step8-decisions user_decisions U8-1 · _RESUME §2 10-29 「게이트 → 규칙」 |
| **원천 수정 후보** | 오기 · 코드 어긋남은 Hub 사전이 아니라 원천 표기 수정으로(「쳐짐 → 처짐」 선례) | _RESUME §2 10-27 「표기 오류는 … 원천 표기 수정」 |
| **시술 아님** | 행위가 아닌 것 — 처방약 · 성분 · 외용제 · 확인 조건 약물(아큐탄 · 미녹시딜 …) | 로그 step5 §3-3 · step7-decisions resolver.no_unit |
| **추천 제외** | 추천 기본 응답에서 빼되 노드는 남김(허가 확인 불가 · 취소 이력 · 시그니처 · 합친 행) | step1 recommendable · step6 recommendable |

## 4. 동의어 · 이름 해석 사전 지도

| # | 사전 | 파일 | 칸 | 셈 | 가리키는 노드 | 메모 |
|---|---|---|---|---|---|---|
| 1 | 1단계 제품 이름 | `step1-products.json` | items[].2_names.display_name · search_names[]{name,lang} | 930 | 제품 | 이유(음역 · 오기 · 약칭)는 name_basis 에만 — 10-27 이름 규칙 |
| 2 | 2단계 계열 동의어 | `step2-families.json` | families[].name · synonyms[] | 100 | 계열 |  |
| 3 | 3단계 부위 사전 | `step3-sites.json · step3-lexicon.json` | nodes[].synonyms[]{text,type,weak} · lexicon entries[](정규식 · 우선순위) · residual | 노드 이름 · 동의어 129 · lexicon 패턴 251 | 부위 | 정규화 = 공백 제거 · 영문으로 시작하면 소문자 · 라틴 글자 악센트 제거(NFKD 결합 부호 · 글자 수 보존 — v4 F-B, 원천 문자열을 매칭 전에 접는다) |
| 4 | 4단계 기법 이름 | `step4-techniques.json` | nodes[].name · medical_name · source_expressions[](원천 표현 181) | 52 | 기법 | source_expressions 는 판정 기록이라 사전 원소로 셈하지 않음(페이지는 30자 미만을 별칭으로 넣음) |
| 5 | 5단계 단위 시술 동의어 | `step5-units.json` | units[].name · synonyms[]{text,type,src,ambiguous} · device_name_synonyms[] · synonym_multi_unit{} | 553 · type {'원장 이름': 165, '시장가 이름': 104, '쁘띠시술 메뉴 이름': 15, '장비 · 제품 이름(저장 uses_product)': 25, '장비 · 제품 이름(저장 uses_product) · 모호': 11, '7단계 원천 이름': 28} · 모호 39 | 단위 시술 | rules.name(family_term · sub_term · technique_term · medium_term)은 이름을 짓는 말 — 7 · 8단계 사전이 이것을 근거로 씀 |
| 6 | 6단계 패키지 동의어 | `step6-packages.json` | packages[].name · synonyms[] | 49 | 패키지 |  |
| 7 | 7단계 고민 · 목적 이름 | `step7-concerns.json` | concerns.*.name/concern · purposes[].name · aliases[] | 87 | 고민 · 목적 |  |
| 8 | 7단계 고민 대응표 | `step7-concerns.json` | correspondence[]{text, target[], match_class, gate_status} | 행 249 · 대상 여럿 26 · gate {'자동(완전 일치)': 151, '자동(규칙)': 98} | 고민 · 목적(대상 id 「P…」 · 「목적:{이름}」 문자열) | 규칙 R12~R20 결과 — 행별 결정 표는 없앰 |
| 9 | 7단계 고민 규칙 사전 | `step7-decisions.json` | concern_synonyms[] · concern_rules{split_separators, tails, state_tails, lead_words, anti_prefix, purpose_verb_tails, severity_words, severity_children, loanwords, en_extra, concern_words, purpose_concern} · rename · unknown_concern_words | concern_synonyms 4 · loanwords 2 · en_extra 3 · concern_words 5 · purpose_concern 3 | 고민 · 목적 | R12~R20 이 읽는 낱말 사전 |
| 10 | 7단계 시술 이름 해석(resolver) | `step7-decisions.json` | resolver{fam_kw, no_unit, generic_synonyms, brands, body_words, site_kw, ambiguous_site_kw, forced_synonyms, exact_overrides} | fam_kw 112 · no_unit 7 · generic_synonyms 8 · brands 19 · body_words 11 · site_kw 48 · ambiguous_site_kw 8 · forced_synonyms 2 · exact_overrides 1 | 계열 · 단위 시술 · 부위 | fam_kw 는 계열 낱말을 단위 시술로 바로 내리기도 함 |
| 11 | 8단계 이름 해석(resolver) | `step8-decisions.json` | resolver{strip_prefix, tail_words, tail_regex, cut_regex, bundle_paren_rule, note_filters, alias[]} | alias 65 · tail_words 29 · strip_prefix 5 | 계열(+하위 · 부위 · 기법 · 용도 조건) · 단위 시술 | alias 는 계열 + 조건으로 풂(7단계는 단위 시술로 풂) |
| 12 | 8단계 확인 조건 패턴 | `step8-decisions.json · step8-relations.json` | conditions[]{id,name,pattern} · conditions.nodes[].match_pattern · not_person_rules · age_avoid_patterns | 조건 53 · not_person 3 · age 2 | 확인 조건 |  |
| 13 | 8단계 간격 낱말 사전 | `step8-decisions.json` | interval_lexicon{units_days, branches[], word_branches[]} | 갈래 16 · 낱말 13 | 관계 주장 interval 칸 | 이름 사전이 아니라 읽는 규칙 사전(§5) |
| 14 | 8단계 문장 패턴 | `step8-decisions.json` | sentence{patterns[], …} | 패턴 20 | 관계 주장 | 읽는 규칙 사전 |

### 4-1. 겹침 전수 — 같은 말(정규화: 공백 제거 · NFKC · 소문자)이 다른 노드 147

원소 2454 자리별: S1 items[].2_names.display_name 354 · S1 items[].2_names.search_names[].name 576 · S2 families[].name 27 · S2 families[].synonyms[] 73 · S3 nodes[].name 53 · S3 nodes[].synonyms[].text 76 · S4 nodes[].name 26 · S4 nodes[].medical_name 26 · S5 units[].name 162 · S5 units[].synonyms[].text 348 · S5 device_name_synonyms[] 43 · S6 packages[].name 24 · S6 packages[].synonyms[].text 25 · S7 concerns.categories[].name 12 · S7 concerns.subcategories[].concern 31 · S7 concerns.items[].name 11 · S7 concerns.extra_items[].name 3 · D7 concern_synonyms[] 6 · S7 purposes[].name 13 · S7 purposes[].aliases[].text 17 · S7 correspondence[].text → target[] 283 · D7 resolver.fam_kw[] 146 · D8 resolver.alias[] 66 · S8 conditions.nodes[].name 53

| 갈래 | 셈 |
|---|---|
| A 묶음 이름 → 고민 · 목적 여럿(R12 · 의도) | 28 |
| B 장비 · 제품 이름 = 단위 시술 동의어(10-27 결정 · 의도) | 42 |
| C 브랜드 이름이 계열 낱말로도(사전 resolver) — 「보톡스」는 10-27 결정(둘 다) · 나머지는 결정 없음 | 5 |
| D 같은 검색 이름이 제품 둘(라인 · 같은 허가 · 합침 후보) | 15 |
| E 같은 말이 단위 시술 여럿(후보 · 모호 표시) | 16 |
| F 계열 · 기법 낱말을 사전마다 다른 수준으로 풂(7단계 → 단위 시술 · 8단계 → 계열 + 조건) | 21 |
| G 부위 이름 = 단위 시술 동의어(원장 이름 「사각턱」 · 「승모근」 …) | 4 |
| H 기법 이름 = 단위 시술 이름(서브시전 · 펀치 · 압출) | 4 |
| I 나열 문자열이 부위 둘에(동의어 칸에 나열) | 2 |
| J 종류가 다른 노드끼리(고민 · 계열 · 목적 · 부위 섞임 — 확인) | 10 |

**결정 근거가 없는 겹침(진짜 충돌) — C(「보톡스」 제외) · F · J 갈래**

| 말 | 대상 | 자리 | 갈래 |
|---|---|---|---|
| co2 | fam:M8 · unit:U5-028 | D7 resolver.fam_kw[] · D8 resolver.alias[] | F |
| hifu | fam:M9 · unit:U5-102 · unit:U5-103 | D7 resolver.fam_kw[] · D8 resolver.alias[] | F |
| ipl | fam:M8 · unit:U5-030 | D7 resolver.fam_kw[] · S2 families[].synonyms[] · S5 units[].synonyms[].text | F |
| led | fam:M8 · unit:U5-043 · unit:U5-050 | D7 resolver.fam_kw[] · D8 resolver.alias[] | F |
| prp | fam:M5 · unit:U5-020 · unit:U5-042 | D7 resolver.fam_kw[] · D8 resolver.alias[] · S2 families[].synonyms[] · S5 units[].synonyms[].text | F |
| rf | fam:M9 · unit:U5-091 · unit:U5-104 | D7 resolver.fam_kw[] · D8 resolver.alias[] | F |
| 경화요법 | con:auto-127-1774737181584 · unit:U5-158 | S5 units[].synonyms[].text · S7 correspondence[].text → target[] | J |
| 다이오드 | fam:M8 · unit:U5-100 · unit:U5-101 | D7 resolver.fam_kw[] · D8 resolver.alias[] | F |
| 다한증 | con:P14-3 · unit:U5-010 · unit:U5-011 · unit:U5-012 | S5 units[].synonyms[].text · S7 concerns.subcategories[].concern | J |
| 리프팅 | con:P3 · con:P4-1 · fam:M9 · pur:리프팅 | S2 families[].synonyms[] · S7 correspondence[].text → target[] · S7 purposes[].name | J |
| 메조테라피 | fam:M4 · tech:K01a | S2 families[].synonyms[] · S4 nodes[].name | J |
| 모발이식 | fam:N9 · unit:U5-161 | S2 families[].name · S5 units[].synonyms[].text | F |
| 바디 | con:P12 · site:site.body | S3 nodes[].name · S3 nodes[].synonyms[].text · S7 concerns.categories[].name · S7 correspondence[].text → target[] | J |
| 브이올렛 | fam:N1 · prod:auto-M16-1775403016892 | D7 resolver.fam_kw[] · S1 items[].2_names.display_name | C |
| 비타민c | none:시술 아님 · unit:U5-052 | D7 resolver.fam_kw[] · D8 resolver.alias[] | J |
| 성장호르몬주사 | fam:N6 · unit:U5-129 | S2 families[].name · S2 families[].synonyms[] · S5 units[].name | F |
| 아그네스 | fam:M11 · prod:auto-M11-1775364775142 | D7 resolver.fam_kw[] · S1 items[].2_names.display_name | C |
| 알렉산드라이트 | fam:M8 · unit:U5-100 · unit:U5-101 | D7 resolver.fam_kw[] · D8 resolver.alias[] | F |
| 엑소좀 | fam:M5 · unit:U5-019 · unit:U5-040 · unit:U5-142 | D7 resolver.fam_kw[] · D8 resolver.alias[] · S2 families[].synonyms[] | F |
| 엔더몰로지 | fam:N8 · unit:U5-160 | S2 families[].synonyms[] · S5 units[].synonyms[].text | F |
| 엠스컬프트 | fam:M10 · prod:M10-2-1 | D7 resolver.fam_kw[] · S1 items[].2_names.display_name | C |
| 인트라셀 | fam:M11 · prod:M11-P-1 | D7 resolver.fam_kw[] · S1 items[].2_names.display_name | C |
| 자가혈 | fam:M5 · unit:U5-020 · unit:U5-042 | D7 resolver.fam_kw[] · S2 families[].synonyms[] | F |
| 제모 | con:P10 · fam:M8 · unit:U5-100 · unit:U5-101 | D7 resolver.fam_kw[] · D8 resolver.alias[] · S7 concerns.categories[].name · S7 correspondence[].text → target[] | J |
| 주름 | con:P2 · unit:U5-001 · unit:U5-002 · unit:U5-003 · unit:U5-004 · unit:U5-005 | S5 units[].synonyms[].text · S7 concerns.categories[].name · S7 correspondence[].text → target[] | J |
| 줄기세포치료 | con:auto-98-1774737181584 · fam:M17 | S2 families[].synonyms[] · S7 correspondence[].text → target[] | J |
| 지방분해 | fam:N1 · pur:지방분해(지방감소) | D7 resolver.fam_kw[] · S7 purposes[].aliases[].text | J |
| 지방흡입 | fam:N10 · unit:U5-162 | D7 resolver.fam_kw[] · D8 resolver.alias[] · S2 families[].name | F |
| 카복시 | fam:N2 · unit:U5-123 | D7 resolver.fam_kw[] · D8 resolver.alias[] · S2 families[].synonyms[] | F |
| 카복시테라피 | fam:N2 · unit:U5-123 | S2 families[].name · S5 units[].synonyms[].text | F |
| 태반주사 | fam:N5 · unit:U5-128 | S2 families[].synonyms[] · S5 units[].name | F |
| 토닝 | fam:M8 · tech:K04a · unit:U5-023 · unit:U5-024 · unit:U5-025 | D7 resolver.fam_kw[] · D8 resolver.alias[] · S4 nodes[].name | F |
| 프락셔널 | fam:M8 · tech:K04b · unit:U5-026 · unit:U5-027 · unit:U5-028 · unit:U5-029 | D7 resolver.fam_kw[] · D8 resolver.alias[] · S4 nodes[].name | F |
| 필링 | fam:M15 · unit:U5-034 | D7 resolver.fam_kw[] · D8 resolver.alias[] · S2 families[].synonyms[] | F |
| 혈관레이저 | fam:M8 · unit:U5-099 · unit:U5-138 · unit:U5-141 | D7 resolver.fam_kw[] · D8 resolver.alias[] | F |

**7단계 resolver.fam_kw ↔ 8단계 resolver.alias 같은 낱말**

| 낱말 | 7단계 | 8단계 | 같음 |
|---|---|---|---|
| 크라이오 | {"families": ["M14"], "units": null} | {"family": "M14"} | ○ |
| 혈관레이저 | {"families": null, "units": ["U5-141", "U5-099", "U5-138"]} | {"family": "M8", "note": "혈관"} | ✗ |
| 토닝 | {"families": null, "units": ["U5-023", "U5-024", "U5-025"]} | {"family": "M8", "technique": "K04a"} | ✗ |
| 프락셔널 | {"families": null, "units": ["U5-026", "U5-027", "U5-028", "U5-029"]} | {"family": "M8", "technique": "K04b"} | ✗ |
| CO2 | {"families": null, "units": ["U5-028"]} | {"family": "M8", "sub": "탄산가스 레이저"} | ✗ |
| 필링 | {"families": null, "units": ["U5-034"]} | {"family": "M15", "technique": "K09"} | ✗ |
| LED | {"families": null, "units": ["U5-050", "U5-043"]} | {"family": "M8", "sub": "LED"} | ✗ |
| RF | {"families": null, "units": ["U5-091", "U5-104"]} | {"family": "M9", "sub": "RF"} | ✗ |
| HIFU | {"families": null, "units": ["U5-102", "U5-103"]} | {"family": "M9", "sub": "HIFU"} | ✗ |
| 니들RF | {"families": ["M11"], "units": null} | {"family": "M11"} | ○ |
| MTS | {"families": ["M12"], "units": null} | {"family": "M12"} | ○ |
| PRP | {"families": null, "units": ["U5-020", "U5-042"]} | {"family": "M5", "sub": "혈소판 농축물(PRP·PRF)"} | ✗ |
| 엑소좀 | {"families": null, "units": ["U5-019", "U5-040", "U5-142"]} | {"family": "M5", "sub": "엑소좀"} | ✗ |
| 바이오스티뮬 | {"families": ["M3"], "units": null} | {"family": "M3"} | ○ |
| CaHA | {"families": ["M3"], "units": null} | {"family": "M3", "sub": "CaHA"} | ✗ |
| 카복시 | {"families": null, "units": ["U5-123"]} | {"family": "N2"} | ✗ |
| 지방흡입 | {"families": null, "units": ["U5-162"]} | {"family": "N10"} | ✗ |
| 제모 | {"families": null, "units": ["U5-100", "U5-101"]} | {"family": "M8", "note": "제모"} | ✗ |
| 다이오드 | {"families": null, "units": ["U5-100", "U5-101"]} | {"family": "M8", "sub": "반도체 레이저"} | ✗ |
| 알렉산드라이트 | {"families": null, "units": ["U5-100", "U5-101"]} | {"family": "M8", "sub": "알렉산드라이트 레이저"} | ✗ |
| 지방이식 | {"families": ["M6"], "units": null} | {"family": "M6"} | ○ |
| 스킨부스터 | {"families": ["M4"], "units": null} | {"family": "M4"} | ○ |
| 보톡스 | {"families": ["M1"], "units": null} | {"family": "M1"} | ○ |
| 필러 | {"families": ["M2"], "units": null} | {"family": "M2"} | ○ |
| 실리프팅 | {"families": ["M7"], "units": null} | {"family": "M7"} | ○ |
| 레이저 | {"families": ["M8"], "units": null} | {"family": "M8"} | ○ |
| 플라즈마 | {"families": ["M13"], "units": null} | {"family": "M13"} | ○ |
| 줄기세포 | {"families": ["M17"], "units": null} | {"family": "M17"} | ○ |
| 써마지 | {"families": null, "units": ["U5-091", "U5-104"]} | {"units": ["U5-091", "U5-104"]} | ○ |
| 마이크로니들 | {"families": ["M12"], "units": null} | {"family": "M12"} | ○ |
| 비타민C | {"families": null, "units": ["U5-052"]} | {"none": "시술 아님(비타민C 도포 = 외용제 — 7단계 not_procedure 「외용제」) · 단 U5-036 「이온토포레시스 (비타민C)」와 구분 필요"} | ✗ |

<details><summary>겹침 전부(147)</summary>

| 말 | 대상 | 갈래 |
|---|---|---|
| aape | prod:auto-M17-1775364775191 · unit:U5-143 | B |
| asce+엑소좀 | prod:M4-3-1 · unit:U5-142 | B |
| co2 | fam:M8 · unit:U5-028 | F |
| coolsculptingelitesystem | prod:M14-1-1 · prod:auto-M14-1775363067062 | D |
| coolsculptingsystem(zeltiqsystem) | prod:M14-1-1 · prod:auto-M14-1775363067062 | D |
| doublo-goldtm | prod:M9-1-5 · prod:M9-1-6 | D |
| eco2 | prod:auto-M8-1775362603297 · prod:auto-M8-1775364775119 | D |
| eco2evolution&surgical | prod:auto-M8-1775362603297 · prod:auto-M8-1775364775119 | D |
| eco2plus | prod:auto-M8-1775362603297 · prod:auto-M8-1775364775119 | D |
| emsculptneo | prod:M10-2-1 · prod:M10-2-2 | D |
| ems바디(팔뚝/허벅지) | unit:U5-108 · unit:U5-109 | E |
| hair | con:P10 · con:P13 | A |
| hair→모발·체모 | con:P10 · con:P13 | A |
| hifu | fam:M9 · unit:U5-102 · unit:U5-103 | F |
| ipl | fam:M8 · unit:U5-030 | F |
| joulebblskintyteii | prod:auto-29-1774737181584 · prod:auto-32-1774737181584 | D |
| ldm | prod:M15-4-1 · unit:U5-036 | B |
| ldm초음파관리 | prod:M15-4-1 · unit:U5-036 | B |
| led | fam:M8 · unit:U5-043 · unit:U5-050 | F |
| lifteracool | prod:M9-1-8 · prod:auto-37-1774737181584 | D |
| lifting | con:P3 · con:P4-1 · pur:리프팅 | A |
| lifting/리프팅비교 | con:P3 · con:P4-1 · pur:리프팅 | A |
| m16-1미백/항산화 | con:P5 · pur:항산화 | A |
| m16-3재생/면역 | con:P4-1 · pur:면역 · pur:재생 | A |
| oligiox | prod:M9-2-2 · prod:auto-M9-1775361486532 | D |
| prp | fam:M5 · unit:U5-020 · unit:U5-042 | F |
| q-스위치 | unit:U5-023 · unit:U5-131 | E |
| q스위치 | unit:U5-023 · unit:U5-131 | E |
| regeneration | con:P4-1 · pur:재생 | A |
| rf | fam:M9 · unit:U5-091 · unit:U5-104 | F |
| sp다이나미스 | prod:auto-M8-1775360944918 · unit:U5-099 | B |
| starwalker | prod:auto-M8-1775364775120 · prod:auto-M8-1775364775128 | D |
| subcision | tech:K12a · unit:U5-045 | H |
| tightening | con:P4-1 · pur:타이트닝(탄력) | A |
| ultherapyprime | prod:M9-1-1 · prod:M9-1-2 | D |
| ultracelq+ | prod:M9-1-9 · prod:auto-M9-1775362627041 · prod:auto-M9-1775363043305 | D |
| 겨드랑이/팔/다리 | unit:U5-100 · unit:U5-146 · unit:U5-147 | E |
| 경화요법 | con:auto-127-1774737181584 · unit:U5-158 | J |
| 고주파 | unit:U5-091 · unit:U5-104 | E |
| 눈밑꺼짐→꺼짐·주름·볼륨 | con:P1-5 · pur:볼륨 회복(충전) | A |
| 다이오드 | fam:M8 · unit:U5-100 · unit:U5-101 | F |
| 다크서클필러→다크서클 | con:P1-5 · pur:볼륨 회복(충전) | A |
| 다한증 | con:P14-3 · unit:U5-010 · unit:U5-011 · unit:U5-012 | J |
| 더마펜4 | prod:auto-M12-1775363026852 · unit:U5-032 | B |
| 더블로골드 | prod:M9-1-5 · prod:M9-1-6 · unit:U5-102 | B |
| 듀오하이드로젠 | prod:new-DEV-041 · unit:U5-035 | B |
| 라이넥 | prod:M16-3-1 · unit:U5-128 | B |
| 래디어스 | prod:M3-2-1 · unit:U5-090 | B |
| 리쥬란 | prod:M4-1-1 · unit:U5-018 | B |
| 리쥬란아이 | prod:M4-1-2 · unit:U5-018 | B |
| 리프팅 | con:P3 · con:P4-1 · fam:M9 · pur:리프팅 | J |
| 메조테라피 | fam:M4 · tech:K01a | J |
| 멜스몬 | prod:auto-M16-1775364775098 · unit:U5-128 | B |
| 모르페우스8 | prod:M11-1-4 · unit:U5-110 | B |
| 모발이식 | fam:N9 · unit:U5-161 | F |
| 목주름/턱선 | unit:U5-016 · unit:U5-017 | E |
| 민트리프트 | prod:M7-3-1 · unit:U5-022 | B |
| 바디 | con:P12 · site:site.body | J |
| 바디리프팅→라인·리프팅·탄력 | con:P12-3 · con:P3-3 · pur:리프팅 | A |
| 보톡스 | fam:M1 · prod:M1-2-1 | C |
| 볼/관자놀이 | site:site.cheek-group · site:site.temple | I |
| 볼뉴머 | prod:M9-2-3 · unit:U5-091 | B |
| 브이빔 | prod:M8-4-1 · unit:U5-141 | B |
| 브이빔퍼펙타 | prod:auto-M8-1775364775121 · unit:U5-141 | B |
| 브이올렛 | fam:N1 · prod:auto-M16-1775403016892 | C |
| 비키니 | site:site.bikini · unit:U5-148 | G |
| 비타민c | none:시술 아님 · unit:U5-052 | J |
| 빼당주사 | unit:U5-070 · unit:U5-073 · unit:U5-074 | E |
| 사각턱 | site:site.masseter · unit:U5-006 | G |
| 색소/기미 | con:P5 · con:P5-1 | A |
| 서브시전 | tech:K12a · unit:U5-045 | H |
| 서브시전[유착해제] | con:auto-121-1774737181584 · con:auto-128-1774737181584 | A |
| 성장호르몬주사 | fam:N6 · unit:U5-129 | F |
| 소프웨이브 | prod:auto-40-1774737181584 · unit:U5-140 | B |
| 수염/가슴/등 | unit:U5-149 · unit:U5-150 · unit:U5-151 | E |
| 슈링크 | prod:M9-1-3 · unit:U5-102 · unit:U5-103 | B |
| 슈링크유니버스 | prod:M9-1-4 · unit:U5-102 · unit:U5-103 | B |
| 스컬트라 | fam:M3 · prod:M3-1-1 · unit:U5-090 | B |
| 스케일링 | unit:U5-035 · unit:U5-044 | E |
| 스타워커 | prod:auto-M8-1775364775120 · prod:auto-M8-1775364775128 | D |
| 승모근 | site:site.trapezius · unit:U5-007 | G |
| 시크릿 | prod:M11-1-2 · unit:U5-110 | B |
| 시크릿rf | prod:M11-1-2 · unit:U5-110 | B |
| 써마지 | unit:U5-091 · unit:U5-104 | E |
| 써마지flx | prod:M9-2-1 · unit:U5-091 · unit:U5-104 | B |
| 아그네스 | fam:M11 · prod:auto-M11-1775364775142 | C |
| 아쿠아필 | prod:M15-2-1 · unit:U5-035 | B |
| 알렉 | unit:U5-100 · unit:U5-101 | E |
| 알렉산드라이트 | fam:M8 · unit:U5-100 · unit:U5-101 | F |
| 압출 | tech:K12c · unit:U5-048 | H |
| 에코2 | prod:auto-M8-1775362603297 · prod:auto-M8-1775364775119 | D |
| 엑셀v | prod:M8-4-2 · unit:U5-099 | B |
| 엑소좀 | fam:M5 · unit:U5-019 · unit:U5-040 · unit:U5-142 | F |
| 엔더몰로지 | fam:N8 · unit:U5-160 | F |
| 엘란쎄 | fam:M3 · prod:M3-3-1 · unit:U5-090 | B |
| 엠스컬프트 | fam:M10 · prod:M10-2-1 | C |
| 여드름/모공 | con:P6 · con:P7 | A |
| 여드름/흉터 | con:P6 · con:P9 | A |
| 온다 | prod:M9-3-1 · unit:U5-139 | B |
| 올리지오 | prod:M9-2-2 · prod:auto-M9-1775361486532 · unit:U5-091 · unit:U5-104 | B |
| 울쎄라 | prod:M9-1-1 · prod:M9-1-2 · unit:U5-102 · unit:U5-103 | B |
| 이마/관자놀이 | site:site.forehead-group · site:site.temple | I |
| 이중턱 | con:P11-2 · con:auto-89-1774737181584 | A |
| 이중턱→이중턱(지방) | con:P11-2 · con:auto-89-1774737181584 | A |
| 인모드 | prod:M9-2-5 · unit:U5-091 | B |
| 인중/구레나룻 | unit:U5-144 · unit:U5-145 | E |
| 인트라셀 | fam:M11 · prod:M11-P-1 | C |
| 인피니 | prod:auto-M11-1775364775143 · unit:U5-110 | B |
| 입꼬리/잇몸미소/코끝 | unit:U5-013 · unit:U5-014 · unit:U5-015 | E |
| 자가혈 | fam:M5 · unit:U5-020 · unit:U5-042 | F |
| 잔주름 | con:P2-3 · con:auto-86-1774737181584 | A |
| 재생/면역 | pur:면역 · pur:재생 | A |
| 전신재생 | con:P4 · con:P4-1 · pur:재생 | A |
| 전신재생→항노화·재생 | con:P4 · con:P4-1 · pur:재생 | A |
| 제모 | con:P10 · fam:M8 · unit:U5-100 · unit:U5-101 | J |
| 종아리 | site:site.calf · unit:U5-008 | G |
| 주름 | con:P2 · unit:U5-001 · unit:U5-002 · unit:U5-003 · unit:U5-004 · unit:U5-005 | J |
| 줄기세포치료 | con:auto-98-1774737181584 · fam:M17 | J |
| 쥬베룩 | prod:M3-4-1 · unit:U5-090 | B |
| 쥬베룩볼륨 | prod:M3-4-2 · unit:U5-090 | B |
| 지방분해 | fam:N1 · pur:지방분해(지방감소) | J |
| 지방흡입 | fam:N10 · unit:U5-162 | F |
| 처짐 | con:P3 · con:P3-1 · con:P3-2 · con:P3-3 | A |
| 처짐/탄력 | con:P3 · con:P4-1 | A |
| 카복시 | fam:N2 · unit:U5-123 | F |
| 카복시테라피 | fam:N2 · unit:U5-123 | F |
| 쿨스컬프팅 | fam:M14 · prod:M14-1-1 · unit:U5-116 · unit:U5-117 · unit:U5-118 · unit:U5-119 · unit:U5-120 | B |
| 탄력 | con:P12-3 · con:P4-1 · pur:타이트닝(탄력) | A |
| 태반주사 | fam:N5 · unit:U5-128 | F |
| 태반주사멜스몬 | prod:auto-M16-1775364775098 · unit:U5-128 | B |
| 턱끝볼륨→볼륨·연장 | pur:볼륨 회복(충전) · pur:연장 | A |
| 토닝 | fam:M8 · tech:K04a · unit:U5-023 · unit:U5-024 · unit:U5-025 | F |
| 파셀라 | prod:step1-new-FASCELLA · unit:U5-091 | B |
| 펀치 | tech:K12b · unit:U5-047 | H |
| 포텐자 | prod:M11-1-1 · unit:U5-110 | B |
| 프락셀 | prod:M8-2-4 · unit:U5-026 · unit:U5-027 · unit:U5-028 · unit:U5-029 | B |
| 프락셔널 | fam:M8 · tech:K04b · unit:U5-026 · unit:U5-027 · unit:U5-028 · unit:U5-029 | F |
| 프랙셔널 | unit:U5-026 · unit:U5-027 · unit:U5-028 · unit:U5-029 | E |
| 프로파일로 | prod:auto-M4-1775362484436 · unit:U5-018 | B |
| 피부결/모공 | con:J10-피부결 · con:P7 | A |
| 피부결/톤/항노화 | con:J10-피부결 · con:P4 · con:P5 | A |
| 피코 | unit:U5-023 · unit:U5-026 · unit:U5-027 · unit:U5-131 | E |
| 필링 | fam:M15 · unit:U5-034 | F |
| 항산화수액 | unit:U5-051 · unit:U5-052 | E |
| 헤어셀 | prod:auto-M15-1775364775178 · unit:U5-130 | B |
| 혈관레이저 | fam:M8 · unit:U5-099 · unit:U5-138 · unit:U5-141 | F |
| 흉터/재생 | con:P4-1 · con:P9 · pur:재생 | A |

</details>

### 4-2. 한 사전으로 모을 때의 구조(추천)

한 사전 = 표현 행 하나 + 대상 여럿. 칸: text(원문) · norm(정규화 — 3단계 정규화 규칙 하나로) · targets[{kind, id, qualifier{sub · site · technique · note}}] · reason(이름 · 동의어 · 장비 이름 · 묶음 이름 · 외래어 · 오기 · 사이트 용어) · lang · ambiguous(대상 여럿) · source(파일 · 칸 · 결정) · status(자동 · 결정 · 원천 질문). 규칙 사전(꼬리말 · 머리말 · 나눔 구분자 · 간격 낱말 · 문장 패턴)은 표현 행과 따로 「해석 규칙」 칸으로.

- 같은 낱말을 7단계 resolver 는 단위 시술로 · 8단계 alias 는 계열 + 조건으로 풀어(F 갈래) 수준이 둘 — 한 행에 qualifier 를 두면 「토닝 = M8 + K04a」 하나로 쓰고 단위 시술은 상속 규칙(I3)이 냄
- 대상이 여럿인 것은 의도(R12 · 10-27 「보톡스 = 계열 · 제품 둘 다」 · 장비 이름 = 시술 동의어) — 한 행 targets[] 로 두면 모호 표시가 자동으로 섞임
- 정규화가 지금 3단계 lexicon(공백 제거 · 소문자 · 악센트)에만 적혀 있음 — 한 정본으로
- id 없는 대상(목적 이름 · 「목적:」 문자열)을 사전이 직접 가리켜 id 규칙이 사전에 새어 들어감 — 목적 id 먼저(B6)
- 따로 둠: 간격 낱말 사전 · 문장 패턴 · 확인 조건 패턴 — 이름 → 노드가 아니라 원문 → 칸 규칙이라 「읽는 규칙」(§5)에 둠

## 5. 읽는 규칙

**reading_contract(8단계 정본)**: 추천 · AI 는 claims[].interval.days · interval.first · interval.same_day 만 읽는다(원문 interval.text 는 보관). first = a | b(먼저 하는 쪽) · days = [하한, 상한](일) · open_high = 위로 열림(이상). 겉 칸이 비고 interval.by_sub_condition 이 true 면 options[].sub_condition 별 값(options[].days · same_day · first)을 읽는다. 끝점 · 피함에 default_apply false(scope 「조건부 — 단위 시술 미특정」)면 기본 응답 · 계열 상속에서 뺀다(조회 옵션으로만)

| 칸 | 뜻 |
|---|---|
| `days` | [하한, 상한](일) |
| `open_high` | 위로 열림(이상) |
| `first` | a \| b(먼저 하는 쪽) |
| `same_day` | true · false · null |
| `by_sub_condition` | 겉 칸 비움 → options[] 를 읽음 |
| `options[]` | sub_condition 별 days · same_day · first |
| `marks[]` | 표시(원문 낱말 갈래) |
| `text` | 원문(보관만) |

셈: 관계 주장 395 중 interval 있음 258 · days 있음 116 · first {"a": 147, "null": 242, "b": 6} · same_day {"true": 78, "null": 302, "false": 15}

주장 종류: 병행 · 간격 27 · 시너지(함께) 50 · 순서 · 간격(다음에) 49 · 대체(택 1) 16 · 같은 날 불가 7 · 간격 9 · 재시술 간격(자기 쌍) 1 · 순서 · 간격(문장) 8 · 순서(문장) 6 · 병행 · 간격(문장) 6 · 순서(문장 화살표) 63 · 간격 금기 13 · 조합 금기 3 · 시너지(CC 조합) 137

끝점 수준: 계열 291 · 단위 시술 356 · 부위 조건 6 · 제품 → 단위 시술 18 · 기법 조건 25 · 하위 계열 42 · 용도 조건 4 · 복합(나눔) 39 · 모든 시술 1 · 조건 일치(낱말 교집합) 4 · 시술 아님 2 · 계열 묶음 2

단위 환산 {"시간": 0.0416667, "일": 1, "주": 7, "개월": 30}

### 5-1. 간격 낱말 사전(step8-decisions interval_lexicon)

| id | 원문 패턴 | 칸 | 메모 |
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

### 5-2. 조건부(scope_rule)

끝점 원문(앞 낱말 · 괄호 · 수식 포함)에 출력 · 깊이 한정어가 있는데 끝점이 이름 일치 단위 시술이 아니라 묶음(계열 · 기법 · 하위 · 용도 · 부위 · 낱말 교집합)으로 열렸으면 = 조건부 · default_apply false(기본 상속 · 기본 응답에서 뺌) · 한정어 원문 보관 · 원천 질문(scope_conditional). 이름 일치 단위 시술(「IPL 단독·고출력」 → U5-030)은 그대로 — 5단계 키에 출력 · 깊이 칸이 없어 한정어로 좁힐 수 없다 — 한정어 `고출력\|고에너지\|고강도\|강한\|박리성\|박리\|어블레이티브\|ablative\|심부` · 라벨 「조건부 — 단위 시술 미특정」

### 5-3. 사이트 라벨(labels)

- `contra_level_site`: {"safe": "병행 가능", "caution": "간격 필요", "warning": "주의 필요"}
- `synergy_type`: {"함께": "시너지(함께)", "다음에": "순서 · 간격(다음에)", "대신": "대체(택 1)"}
- `precheck_type_site`: {"absolute_contraindication": "절대금기", "relative_contraindication": "상대금기", "must_check": "필수 확인", "inform": "고지", "safety_protocol": "시술 준비", "counseling": "상담"}
- `opt_evidence_site`: {"high": "근거 강함", "moderate": "근거 보통", "low": "근거 제한적"}
- `opt_priority_site`: {"critical": "필수", "important": "중요", "moderate": "권고", "caution": "주의"}
- `grade3`: {"absolute_contraindication": "금기", "relative_contraindication": "주의", "must_check": "확인만", "inform": "확인만(고지)", "absolute": "금기", "relative": "주의", "consent": "금기", "item": "금기", "iso_same_day": "금기", "iso_wait": "주의", "avoid": "주의", "forbid": "금기"}
- `complication_severity_site`: {"mild": "경미", "moderate": "중등도", "severe": "중증", "critical": "위급"}
- `timeline_label_site`: {"normal": "정상 반응", "abnormal": "관찰", "caution": "병원 연락", "emergency": "즉시 연락"}

### 5-4. gate_status

- 지금: {"step7 correspondence.gate_status": {"자동(완전 일치)": 151, "자동(규칙)": 98}, "step8 claims.gate_status": {"자동(규칙)": 395}, "step7 correspondence.human_check": {"false": 249}, "step1 items.gate(사람 확인 메모)": 86}
- 옛: SPEC-004 §3.2.2(옛): approved · auto · unconfirmed 3값 · 주장 상태 = 기댄 끝 중 가장 약한 값
- 발견: 7 · 8단계는 「게이트 → 규칙」(10-29) 뒤 자동(완전 일치) · 자동(규칙) 둘만 남음. 1~6단계는 gate_status 칸이 없고 decided_by(사용자 결정 id) · 근거 칸으로 상태를 말함 — 공통 칸이 없음
- **추천**: gate_status 를 모든 노드 · 엣지 · 주장 공통 3값으로: 자동(완전 일치) · 자동(규칙) · 결정(decided_by 있음 — 사람이 정함). 「미확인」은 상태가 아니라 표시(question · weak · gap)로. 옛 SPEC-004 의 unconfirmed 는 표시로 대체

### 5-5. 표시 — 노드 · 엣지 공통 한 목록

| 표시 | 뜻 | 페이지 코드 | 지금 칸(흩어진 자리) | 셈 | 읽는 법 |
|---|---|---|---|---|---|
| `conflict` | 충돌 | c | step8 claims[].review_status=conflict · edges[].review_status · conflicts[] · conditions.grade_conflicts · wait_conflicts · step2 product_family[].conflict · step4 conflicts | 주장 104 · 엣지 61 · 계열 쌍 19 · 조건 등급 76 · 대기 1 · 제품 계열 6 | 고르지 않고 전부 보존 · 응답에 양쪽 원문 |
| `conditional` | 조건부(단위 시술 미특정) | s(일부) | claims[].a\|b.scope · default_apply · avoid_edges[].scope · default_apply · scope_conditional · conditions.claims[].scope_conditional | 끝점 2 · 피함 3 · 조건 주장 1 | default_apply false → 기본 응답 · 계열 상속에서 뺌(조회 옵션으로만) |
| `candidates` | 후보 여럿(하나로 안 좁혀짐) | s | units[].synonyms[].ambiguous · units[].candidate_of · step7 edges[].resolve_flag=ambiguous · combos[].components[].flag · step8 claims[].a\|b.flag 「후보 전부」 · step6 slots[] · endpoint units:a,b,c | 단위 시술 동의어 모호 39 · candidate_of 35 · 7단계 엣지 ambiguous 151 · 슬롯 8 | 고르지 않고 후보 전부 반환 · 외부 LLM 이 고르거나 되묻기 |
| `weak` | 근거 약 | w | evidence_level 약 · 중(step2 · step5 · step6 contains) · step3 synonyms[].weak · anatomical_name.level · statements accuracy_score<70 | 계열 판정 약 9 · 단위 시술 중 3 · 패키지 구성 약 5 · 부위 동의어 weak 2 | 값은 쓰되 약함 표시 |
| `question` | 원천 질문 걸림(병원 · 의료진 · 원장님) | q · h | origin_question · staff_question · doctor_questions · pending_director · confirm_question · origin_questions[] | 1단계 86 · 2단계 원장님 3 · 3단계 의료진 35 · 5단계 20+1 · 6단계 13 · 7단계 2 · 8단계 18 | 추천값으로 쓰되 질문 표시 · 답 오면 그 행만 |
| `not_recommended` | 추천 제외 | x | step1 4_license.recommendable=false · active=false · step6 recommendable=false · combos sales_copy.default_response=false(영업 문구) | 제품 118 · 패키지 2 · 영업 문구 24 | 기본 응답에서 뺌 · 노드는 남김 |
| `gap` | gap(정보 없음) | g | safety.complication_gap_families · step5 pih_gap_units · step7 resolve_flag no_unit_at_site · site_check | 합병증 gap 계열 17 · PIH gap 단위 시술 64 · 7단계 그 부위 단위 시술 없음 15 | 「정보 없음」을 「안전」으로 읽지 않음 |
| `default_value` | 기본값(원천에 없어 규칙으로 채움) | (없음) | step5 units[].site_basis · route_status 「허가 용법 미확인」 · family_defaults(계열 기본 기법) | site_basis {'원천 이름': 52, '원천 이름 · de': 23, 'DEC-002 D-': 1, '기본값 — DEC-': 41, 'F3 · U4 — ': 1, '규칙 — DEC-0': 25, '근거 약 — v3 ': 1, '기본값 — 보정 「': 1, '원천 이름(쁘띠시술': 4, '규칙 — 전신 투여': 2, 'F3 — 시장가가 ': 2, '원천 이름(「바디」': 3, 'G1 결정 — 미라': 1, '원천 중분류(P8-': 1, '특수 부위 병변 단': 1, 'G6 결정 — 원천': 1, '원천 중분류(P13': 1, '원천 이름(최적화 ': 1} · route 미확인 23 | 원천 값과 구분해 표시 |
| `unresolved` | 못 풂 | (없음) | step7 resolve_flag=unresolved · unresolved[] · unresolved_ok · step8 claims[].resolved=false · 끝점 「해석 안 됨」 | 7단계 엣지 24 · 8단계 주장 1 | 원문 보관 · 엣지 끝 없음 |
| `not_procedure` | 시술 아님 | (없음) | step7 resolve_flag=not_procedure · not_procedure[] · step8 claims[].not_procedure | 7단계 엣지 4 · 8단계 주장 6 | 엣지 끝 아님 |
| `by_sub_condition` | 하위 조건별 값 | (없음) | claims[].interval.by_sub_condition · options[] | by_sub_condition true 2 · options 있음 7 | 겉 칸이 비면 options[].sub_condition 별로 |
| `license_unconfirmed` | 허가번호 미확인 | (info) | step1 4_license.status | 7 | 추천 포함 · 표시 |

- 읽는 규칙이 8단계 관계(reading_contract)에만 정본으로 있고 7단계 엣지 · 6단계 구성 · 5단계 속성에는 「무엇을 읽고 무엇을 보관만 하나」가 칸 이름으로만 흩어짐(default_response · recommendable · resolve_flag · site_basis …)

## 6. 상속 규칙 정의(골드에 넘길 것)

| id | 이름 | 규칙 | 지금 데이터가 표시하는 칸 | 셈 | 메모 |
|---|---|---|---|---|---|
| I1 | 계열 → 단위 시술 | 계열 끝 엣지(관계 · 피함 · 확인 조건 · 합병증 · 근거 문장 · 위험지대 · 추천 계열만)는 key.family 가 그 계열인 단위 시술 전부에 상속. default_apply false 면 상속 안 함 | step5 units[].key.family · step8 edges[].a\|b 'family:M…' · claims[].lowering 「계열(원천 시술군 코드 — 단위 시술은 조회 때 상속 · C4)」 · conditions.claims[].target_level 계열 · safety.complications[].units_inherit[] · step7 edges[].target_kind 계열만 · lowering 「계열(결정)」 | 관계 끝점 계열 291 · 조건 주장 계열 340 · 합병증 units_inherit 합 725 · 7단계 계열만 75 | 합병증만 units_inherit 로 미리 펼쳐 저장 · 나머지는 조회 때 — 칸이 둘(B7) |
| I2 | 하위 계열 | 하위 계열 끝(「family:M9#HIFU」 · a.sub_family)은 key.sub_family 가 같은 단위 시술로. 단위 시술 키에 그 하위가 없는 계열(J1 안 C 밖)이면 계열(+조건) 후보 전부 · 하위 원문 보관 | step8 edges[].a\|b 'family:M…#하위' · claims[].a\|b.sub_family · flag 「단위 시술 키에 이 하위 계열 없음 …」 · timeline_attach.units_where{family,sub} · step5 product_link.inherit(키 하위 있으면 같은 하위) | 끝점 문자열 # 3 · 하위 계열 끝점 42 · 하위 없음 플래그 16 | 하위 표기가 끝점 문자열 안(#) · 끝점 칸(sub_family) · timeline units_where 세 꼴 |
| I3 | 기법 조건 | 기법 끝(K04b 프락셔널 …)은 key.technique 가 그 기법(또는 하위 기법)인 단위 시술로. 제품 → 단위 시술 상속은 기법 호환(technique_compat)을 통과한 것만 | claims[].a\|b.technique · level 기법 조건 · conditions.claims[].target.technique · step5 rules.product_link.technique_compat · guards | 관계 끝점 기법 조건 25 · 조건 주장 기법 조건 3 |  |
| I4 | 제품 → 단위 시술 | 저장(uses_product)은 원천 이름이 제품을 부를 때만. 상속 후보 = 같은 계열(주 · 보조) · 키 하위 있으면 같은 하위 · 없으면 계열 전부 · 기법 호환 · 도포만 가드 | step5 units[].uses_product · product_links[].inherited_candidates · stored_units · technique_excluded · guard · link · rules.product_link | link {'조회 때 상속 후보': 303, '저장 uses_product': 36, '계열 has_product 만(기법 호환 단위 시술 없음 — F1)': 7, '계열 밖(단위 시술 없음)': 5, '원장님 문의(계열 없음)': 3} · 상속 후보 합 1364 | 페이지는 이걸 엣지 「상속 후보(prod_unit_inh)」로 그렸음 — 저장 엣지가 아니라 골드 계산 |
| I5 | 부위 내림 | 고민 · 끝점 부위가 있으면 그 부위(또는 하위)의 단위 시술(site_rules.lowering). 없으면 R21 부위 올라가기: 앵커 부위(또는 하위)에 그 계열 단위 시술이 없으면 3단계 부위 트리의 상위로 올라가며 찾는다. 층 = 조상 노드 자신(형제 부위는 다른 부위라 넣지 않음 · 묶음 노드는 직접 붙은 단위 시술이 없어 통과) · 마지막 층 = 최상위 영역의 「전체」 노드. 처음 찾은 층의 단위 시술만 · 영역: 최상위 영역 = 3단계 트리에서 부모 없는 노드(계산 · 얼굴 · 목(묶음) · 두피 · 바디). 영역 경계를 넘지 않는다 — 얼굴 고민에 바디 · 두피 · 목 단위 시술 0 · 전체 노드: 영역 R 의 「전체」 노드 = 「R 전체」 자식이 있으면 그것(얼굴 → 얼굴 전체 · 5단계 J2) · 없으면 R 자신(바디 · 두피) · R 이 묶음이면 없음(목(묶음) → 계열만) · 없으면: 영역 「전체」 노드까지 없으면 계열 엣지만(to_units 비움 · to_family 유지) + 표시 「이 부위 단위 시술 없음 · 계열만」 · 단위 시술 후보 붙이지 않음 (10-29 이전 「계열 후보 전부 + no_unit_at_site」 대체 — 코디 알림 · 사용자 10-29) | step7-decisions site_rules{lowering, no_unit_at_site, edge_check, site_free, climb{rule, regions, whole_node, none, record, guard}} · step7 edges[].lowering 「상위 부위로 내림(층)」 · site_layer · site_check · anchor_sites · resolve_flag · step8 claims[].a\|b.flag 「7단계 부위로 내림 …」 · step3 nodes[].parent | 7단계 site_check {'앵커 부위 없음': 334, '부위 안': 149, '상위 부위 얼굴 전체': 37, '이 부위 단위 시술 없음 · 계열만': 15, '상위 부위 바디': 2} | 규칙 문장은 step7-decisions 에만 · 8단계는 7단계 엣지를 재사용(via 「7단계 CC 추천 시술 엣지(③) 재사용」)해 같은 규칙을 물려받음 · 부위 트리(3단계 parent)가 상속 경로 — 내림(하위)과 올라가기(상위 · 영역 안) 두 방향 |
| I6 | 끝점 묶음 | units:a,b,c = 이름이 가리킨 후보 전부(OR · 고르지 않음) — 각 후보에 「후보」 표시로 적용 · bundle:M\|M = 묶음 낱말이 연 계열 전부 · all = 모든 시술 | step8 edges[].a\|b 'units:…' · 'bundle:…' · 'all' · claims[].a\|b.units · n_units · flag · conditions.claims[].target · avoid_edges[].to.units | 끝점 {'all': 1, 'units': 137, 'bundle(여럿)': 2, 'family': 177, 'units(여럿)': 124, 'family(여럿)': 1} | B3 |
| I7 | 조건부 제외 | default_apply false(조건부 — 단위 시술 미특정)는 기본 상속 · 기본 응답에서 뺌 | claims[].a\|b.default_apply · avoid_edges[].default_apply · conditions.claims[].scope_conditional | 끝점 2 · 피함 3 · 조건 주장 1 |  |
| I8 | 안전 원문 붙는 수준 | 경과 타임라인 · PIH · 운영 속성은 원천이 가리킨 수준(계열 · 하위 · 단위 · 제품)에 붙고 아래로 상속 | step8-decisions timeline_attach · step8 safety.timelines[].attach_level · step5 pih[].attach · target · step8 safety.pih[].attach · step5 units[].ops.inherit | timeline {'계열': 5, '계열(하위 HA — M': 1, '하위 계열 HIFU ·': 1, '단위 시술': 1, '계열 N1(C5 — M': 1, '하위 계열 화학 박피 ': 1} · PIH attach {'unit': 9, 'family_sub': 8, 'product': 6, 'family': 3} · ops 상속 136 | PIH 는 5단계 pih(26 · target 칸)와 8단계 safety.pih(26 · risk_factors · prevention)로 두 곳 |
| I9 | 해당 없음 계열 | PIH 해당 없음 계열(M1~M7 · M10 · M16 · M17)은 상속 대상에서 「해당 없음」 — gap 과 다름 | step5 rules.pih_not_applicable · pih_not_applicable_units · pih_gap_units | 해당 없음 77 · gap 64 | 「해당 없음」 ≠ 「gap」 — 표시를 나눠야 함 |

## 7. 부작용 · 합병증 · 근거 문장

### 7-1. 부작용이 있는 자리

| 자리 | 무엇 | 셈 |
|---|---|---|
| `step8 safety.complications[](합병증 노드)` | severity mild = 흔한 예상 반응 섞임 | 전체 65 · severity {'mild': 38, 'moderate': 13, 'severe': 11, 'critical': 3} · 계열 ['M1', 'M11', 'M14', 'M15', 'M16', 'M2', 'M3', 'M7', 'M8', 'M9'] |
| `step8 safety.family_text[계열]「부작용 문장 common · uncommon · serious」` | 계열 원문 속성(「합병증 노드 아님 · B13」 라벨) | common 59 · uncommon 45 · serious 37 · 계열 17(M1~M17) |
| `step8 evidence.statements[field=adverse_effects]` | 문헌 문장 | 32 → 분류 부작용(흔한 예상 반응) 9, 색소 반응(PIH — 5단계 PIH 속성과 겹침) 4, 드문 · 중대 반응(합병증 성격) 9, 안전성 총평(내약성 · 경미 · 반응 없음) 6, 기전 · 효과 한계(이상 반응 칸에 있으나 반응 아님) 4 |
| `step5 extracted[](키 safety.common · safety.serious) — 본문은 브론즈 taxonomy modality[].products[].extracted` | 제품 × 계열 · 단위 시술 수준 원문(5단계 「이 제품으로 했을 때」) | safety.common 키 521(attach {'제품 × 계열': 207, '단위 시술': 147, '원문 보관(6단계 패키지)': 16, '제품 × 계열 × 키 하위': 111, '단위 시술 후보': 19, '원문 보관(원장님 문의)': 1, '원문 보관(값)': 17, '원문 보관(시술 아님(다른 단계))': 2, '원문 보관(시술 아님)': 1}) · safety.serious 189 |
| `step8 safety.item_text_counts · item_aftercare_dest` | 원장 항목 안전 문장 셈 | {"aftercare": 521, "safety.common": 521, "safety.long_term": 1, "safety.note": 4, "safety.serious": 187} |

**합병증 gap 17계열 — 원천 안 문장 셈**

| 계열 | 부작용 문장 common | uncommon | serious | 근거 문장 adverse |
|---|---|---|---|---|
| M10 | 3 | 2 | 0 | 0 |
| M12 | 3 | 3 | 1 | 5 |
| M13 | 2 | 1 | 0 | 0 |
| M17 | 2 | 1 | 1 | 1 |
| M4 | 4 | 3 | 2 | 2 |
| M5 | 3 | 1 | 1 | 2 |
| M6 | 3 | 3 | 3 | 0 |
| N1 | 0 | 0 | 0 | 0 |
| N10 | 0 | 0 | 0 | 0 |
| N2 | 0 | 0 | 0 | 0 |
| N3 | 0 | 0 | 0 | 0 |
| N4 | 0 | 0 | 0 | 0 |
| N5 | 0 | 0 | 0 | 0 |
| N6 | 0 | 0 | 0 | 0 |
| N7 | 0 | 0 | 0 | 0 |
| N8 | 0 | 0 | 0 | 0 |
| N9 | 0 | 0 | 0 | 0 |

**severity mild 인데 발생률 낱말이 「흔함」이 아닌 것(B1 예외 — 의료진 질문)**

- CX-M1-02 멍 (타박상) — 약 11-25% (부위·기법에 따라)
- CX-M1-04 두통 — 5-10%
- CX-M1-06 독감 유사 증상 — 1.7-20% (치료 방문의 약 14%)
- CX-M1-07 안면 비대칭 — 3-8%
- CX-M2-01 멍 / 반상출혈 (Bruising / Ecchymosis) — 19-24% (필러 시술 전반, 부위·기법 무관하게 가장 흔한 부작용군)
- CX-M2-07 비대칭 (Asymmetry) — 5-10%
- CX-M7-04 비대칭 — 5-10%
- CX-M7-06 피부 딤플링/주름짐 (Skin Dimpling/Puckering) — 약 7-10%(50세 초과에서 최대 16%)
- CX-M14-07 염증후 색소침착 (Post-inflammatory Hyperpigmentation, PIH) — 드묾. Fitzpatrick IV-VI(진한 피부톤)에서 상대적으로 높음

### 7-2. 근거 문장 119 전수 분류

field(원천 칸) {"moa": 50, "adverse_effects": 32, "effects": 37}

| 종류(추천) | 셈 | id |
|---|---|---|
| 부작용(흔한 예상 반응) | 9 | M5-adverse_effects-01 · M7-adverse_effects-02 · M7-adverse_effects-04 · M8-adverse_effects-02 · M8-adverse_effects-03 · M8-adverse_effects-04 · M12-adverse_effects-05 · M15-adverse_effects-01 · M15-adverse_effects-02 |
| 색소 반응(PIH — 5단계 PIH 속성과 겹침) | 4 | M8-adverse_effects-01 · M8-adverse_effects-05 · M12-adverse_effects-01 · M12-adverse_effects-04 |
| 드문 · 중대 반응(합병증 성격) | 9 | M1-adverse_effects-01 · M1-adverse_effects-02 · M1-adverse_effects-03 · M2-adverse_effects-03 · M4-adverse_effects-02 · M5-adverse_effects-02 · M12-adverse_effects-02 · M16-adverse_effects-01 · M17-adverse_effects-01 |
| 안전성 총평(내약성 · 경미 · 반응 없음) | 6 | M2-adverse_effects-01 · M7-adverse_effects-01 · M7-adverse_effects-03 · M7-adverse_effects-05 · M7-adverse_effects-06 · M12-adverse_effects-03 |
| 기전 · 효과 한계(이상 반응 칸에 있으나 반응 아님) | 4 | M1-adverse_effects-04 · M2-adverse_effects-02 · M3-adverse_effects-01 · M4-adverse_effects-01 |
| 효과(기전 칸에 있음) | 3 | M2-moa-02 · M8-moa-03 · M8-moa-08 |
| 적응증(기전 칸에 있음) | 2 | M15-moa-03 · M15-moa-04 |
| 안전성 비교(기전 칸에 있음) | 1 | M15-moa-05 |
| 근거 수준 · 규제(효과 칸에 있음) | 2 | M16-effects-01 · M16-effects-02 |
| 기전 | 44 | M1-moa-01 · M1-moa-02 · M1-moa-03 · M12-moa-01 · M12-moa-02 · M12-moa-03 · M12-moa-04 · M12-moa-05 · M12-moa-06 · M12-moa-07 · M15-moa-01 · M15-moa-02 · M16-moa-01 · M2-moa-01 · M2-moa-03 · M2-moa-04 · M2-moa-05 · M2-moa-06 · M3-moa-01 · M3-moa-02 · M3-moa-03 · M3-moa-04 · M4-moa-01 · M4-moa-02 · M5-moa-01 · M5-moa-02 · M5-moa-03 · M5-moa-04 · M7-moa-01 · M7-moa-02 · M7-moa-03 · M7-moa-04 · M7-moa-05 · M7-moa-06 · M7-moa-07 · M8-moa-01 · M8-moa-02 · M8-moa-04 · M8-moa-05 · M8-moa-06 · M8-moa-07 · M9-moa-01 · M9-moa-02 · M9-moa-03 |
| 효과 | 35 | M1-effects-01 · M1-effects-02 · M1-effects-03 · M1-effects-04 · M12-effects-01 · M12-effects-02 · M12-effects-03 · M12-effects-04 · M12-effects-05 · M12-effects-06 · M12-effects-07 · M12-effects-08 · M2-effects-01 · M2-effects-02 · M2-effects-03 · M2-effects-04 · M2-effects-05 · M4-effects-01 · M4-effects-02 · M4-effects-03 · M4-effects-04 · M5-effects-01 · M7-effects-01 · M7-effects-02 · M7-effects-03 · M7-effects-04 · M7-effects-05 · M7-effects-06 · M7-effects-07 · M8-effects-01 · M8-effects-02 · M8-effects-03 · M8-effects-04 · M8-effects-05 · M9-effects-01 |

- 분류 기준: 원문 낱말 기준 분류(추천) — 흔한 예상 반응 = 통증 · 부기(swelling · edema · tumefaction) · 멍 · 홍반 · 진물 · 딱지 · 자극 · 건조 · 따가움 / 드문 · 중대 = 실명 · 복시 · 감염 · 과민 · 육아종 · 종양 · 장기 기능 이상 · 위축 · 알레르기(드묾) / 색소 = PIH · 과색소 / 총평 = tolerated · minor · low reactivity · no acute / 나머지는 칸 이름과 뜻이 다른 문장. 「정확도」 · 「환자 문장」은 종류가 아니라 문장 속성(정확도 17/119만 값 · 환자 4개 언어 119/119)
- 문장 속성: {"accuracy_score": {"있음": 17, "없음": 102}, "patient_langs": {"en,ja,ko,zh": 119}, "evidence_per_statement": {"1": 119}}

<details><summary>기전 · 효과 외 분류 문장 원문</summary>

- `ST-M1-adverse_effects-01` Dry eye and diplopia have been reported following injection in the periocular region.
- `ST-M1-adverse_effects-02` Botulinum toxin type A causes submandibular salivary gland atrophy.
- `ST-M1-adverse_effects-03` Mesobotox with botulinum toxin type A induces partial lymphatic drainage insufficiency.
- `ST-M1-adverse_effects-04` Botulinum toxin type A inhibits exocrine function, reducing sebum and sweat production.
- `ST-M12-adverse_effects-01` Post-inflammatory hyperpigmentation can occur, particularly in darker skin phototypes.
- `ST-M12-adverse_effects-02` Bacterial infection and tram-tracking scarring can occur with overly aggressive technique or inadequate aseptic practice.
- `ST-M12-adverse_effects-03` Microneedling is well tolerated by patients with minimal discomfort.
- `ST-M12-adverse_effects-04` Postinflammatory hyperpigmentation occurs after microneedling.
- `ST-M12-adverse_effects-05` Erythema and edema follow microneedling treatments.
- `ST-M15-adverse_effects-01` L-ascorbic acid at low pH can cause transient stinging and erythema in sensitive skin.
- `ST-M15-adverse_effects-02` Adapalene combined with benzoyl peroxide amplifies skin irritation and drying.
- `ST-M15-moa-03` Tretinoin is indicated in the treatment of acne vulgaris and photoaging.
- `ST-M15-moa-04` Tazarotene is indicated in acne vulgaris and plaque psoriasis.
- `ST-M15-moa-05` Adapalene is the least irritating topical retinoid and least prone to photodegradation.
- `ST-M16-adverse_effects-01` Glutathione intravenous skin-lightening use has been associated with skin rashes, Stevens-Johnson-like reactions, and reports of renal and liver dysfunction.
- `ST-M16-effects-01` Intravenous glutathione for skin lightening is not supported by the US FDA or multiple national regulatory agencies and has insufficient high-quality efficacy evidence.
- `ST-M16-effects-02` Topical vitamin C is supported by stronger evidence than IV vitamin C for photoaging and pigmentation.
- `ST-M17-adverse_effects-01` Unregulated stem cell products have caused serious adverse events including blindness after intra-ocular injection and tumor formation at ectopic sites.
- `ST-M2-adverse_effects-01` Hyaluronic acid fillers exhibit limited allergic reactivity.
- `ST-M2-adverse_effects-02` Hyaluronic acid fillers can cause tissue imbalance if muscle activity exceeds tissue firmness.
- `ST-M2-adverse_effects-03` Allergic reactions occur rarely with hyaluronic acid fillers.
- `ST-M2-moa-02` Hyaluronic acid fillers restore facial volume and contour lost due to ageing-related changes in skin, fat pads, bones, and muscles.
- `ST-M3-adverse_effects-01` PLLA heterogeneous particle morphology may result in greater macrophage activation compared to uniform spherical particles of other biostimulators
- `ST-M4-adverse_effects-01` Non-crosslinked hyaluronic acid shows inconsistent results due to rapid degradation.
- `ST-M4-adverse_effects-02` Mesotherapy cocktails may lead to local or systemic hypersensitivity reactions including foreign-body granulomas.
- `ST-M5-adverse_effects-01` Post-procedure pain, swelling, and bruising at injection sites are the most frequently reported PRP adverse events.
- `ST-M5-adverse_effects-02` Transmission of infection is a theoretical risk when exogenous (non-autologous) blood products are used.
- `ST-M7-adverse_effects-01` Thread lifting with absorbable barbed threads is associated with minor and reversible adverse effects.
- `ST-M7-adverse_effects-02` Mild post-operation tumefaction occurs and is successfully treated with non-steroidal drugs.
- `ST-M7-adverse_effects-03` No acute inflammatory responses are elicited by the procedure.
- `ST-M7-adverse_effects-04` Mild post-operation tumefaction occurs and is treated with non-steroidal drugs.
- `ST-M7-adverse_effects-05` Most adverse responses resolve spontaneously or with minimal supportive therapy.
- `ST-M7-adverse_effects-06` Poly(L-lactide-co-ε-caprolactone) has low tissue reactivity.
- `ST-M8-adverse_effects-01` Fractional CO2 laser causes worsening of hyperpigmentation.
- `ST-M8-adverse_effects-02` Ablative lasers cause crusting.
- `ST-M8-adverse_effects-03` Ablative lasers cause oozing.
- `ST-M8-adverse_effects-04` Picosecond lasers cause postoperative oozing and crustation.
- `ST-M8-adverse_effects-05` Fractional CO2 lasers worsen hyperpigmentation temporarily.
- `ST-M8-moa-03` Picosecond Nd:YAG laser reduces pigmentation in hyperpigmented scars.
- `ST-M8-moa-08` Picosecond Nd:YAG lasers improve pigmentation in hyperpigmented scars.

</details>

## 8. 그림 밖 · id · 칸 불일치

### 8-1. 7단계 앵커 없는 고민 → 시술 원천 행 52

| 갈래 | 셈 |
|---|---|
| 앵커 없음(결정대로) — (고민 노드 없음 — 꺼짐) | 1 |
| 앵커 없음(결정대로) — (앵커 없음 — 쁘띠시술) | 30 |
| 앵커 없음(결정대로) — (P1 — 고민 앵커 없음) | 3 |
| 앵커 있음 — from_concerns 가 「목적:{이름}」 문자열(페이지가 고민 id 로만 찾음) | 8 |
| 앵커 있음 — purpose_nodes 칸(페이지가 이 칸을 안 읽음) | 10 |

원천별: ① P1 detail 고민 낱말 1 · ③ problem-packages CC 추천 시술 30 · ② problem-combos 3 · ④ treatment-optimization optimal_combo 8 · ⑥ 5단계 units[].purposes(원장 용도) 6 · ⑥ 5단계 목적 키(제품 출처) 1 · ⑦ 원장 메뉴 분류(6단계 넘김) 3

### 8-2. 부위 노드 없는 단위 시술 31

부위 {"병변 단위": 4, "해당 없음": 27} · 계열 {"N4": 2, "M16": 25, "N5": 1, "N6": 1, "M8": 1, "M13": 1} · 규칙 {"해당 없음": "DEC-003 OQ-306 처리 — 전신 투여(수액 · 태반 · 성장호르몬)", "병변 단위": "F3 · U4 — 병변 수 · 면적으로 매기는 시술(점 · 문신 · 쥐젖 · 켈로이드)"}

- 상위 · 관련 없이 떠 있는 고민 노드: J14-잇몸미소(부위 엣지만)

### 8-3. id 규칙 · 칸 이름 불일치

| 자리 | 불일치 | 셈 |
|---|---|---|
| 제품 | 원장 ledger_id 8꼴(타임스탬프 포함 · step1-new-APTOS) | {"M9-9-9": 85, "auto-M9-9": 176, "auto-9-9": 35, "auto-M9-hADM-9": 1, "auto-M9-DCA-9": 7, "new-DEV-9": 34, "M9-P-9": 14, "step9-new-APTOS": 1, "step9-new-FASCELLA": 1} |
| 고민 | 4꼴(P{n} · P{n}-{n} · auto-{n}-{timestamp} · J{n}-{한글}) — 결정 노드 id 에 한글 이름이 들어감(J10-피부결) | {"P9": 12, "P9-9": 31, "auto-9-9": 11, "J9-가": 3} |
| 목적 | id 없음 — 이름이 키 · 엣지는 「목적:볼륨 회복(충전)」 문자열(from · from_concerns · correspondence target) · purpose_nodes 는 「:」 없는 이름 | {"from_목적": 89, "from_concerns_목적": 8, "purpose_nodes": 55, "corr_목적": 29} |
| 8단계 끝점 | 엣지 끝이 id 가 아니라 문자열 문법(family:M7#PDO \| PDO · units:U5-018,U5-037 · bundle:M11\|M8\|M9 · all) — 칸 안에 하위 · 원문까지 섞임 | {"all": 1, "units": 137, "bundle(여럿)": 2, "family": 177, "units(여럿)": 124, "family(여럿)": 1} |
| 확인 조건 대상 | conditions.claims[].target 이 dict(level · units · families) · 문자열('family:' · 'ledger:' · '모든 시술') · list('product:') 세 꼴 | {"dict": 14, "str": 350, "list": 9} |
| 경과 타임라인 | id = 원천 영문 키(botox · ha-filler …) · attach 문자열(family:M1 · unit:U5-028) | 10 |
| 위험지대 주의 | SC-{zone}-{계열} — zone 이 부위 id 와 다른 원천 영문 | 22 |
| id 머리글 겹침 | K 가 기법(K01) · 조건 주장(K8-0001) 둘 · P 가 고민(P1-1) · 패키지(P6-01) 둘 · R 이 관계 주장(R8-0001) · 7단계 규칙(R12) · 레시피 원천(RC-RE-R1) — 지금 같은 문자열은 없으나 종류 접두가 없으면 겹칠 자리 |  |
| 칸 이름 | 같은 뜻 다른 칸 — 근거 수준(evidence_level 약/중/강 · accuracy_score · strength_original · weak) · 질문(origin_question · staff_question · doctor_questions · pending_director · confirm_question) · 결정 출처(decided_by · decision · basis) · 동의어(synonyms[] 문자열 배열(2단계) · {text,type}(3 · 5 · 6단계) · search_names{name,lang}(1단계) · aliases{source,text}(7단계 목적)) |  |
| 라인 | items[].line 두 모양(role 라인 {items[]} · 라인 구성 {members[]} · 품목) | {"라인 구성": 17, "라인": 11, "품목": 6} |

## 9. 결정 묶음(추천)

| id | 묶음 | 추천 | 근거 | 셈 | 누가 |
|---|---|---|---|---|---|
| B1 | 부작용 ≠ 합병증 — 부작용을 꺼냄 | 합병증 노드는 중대 반응만(severity moderate · severe · critical) · severity mild 는 부작용으로 옮겨 노드가 아닌 계열 속성 「부작용」(+ 제품 × 계열 · 단위 시술은 5단계 extracted safety.common 으로 덮어씀 — 상속 I8 과 같은 꼴). 근거 문장 adverse_effects 중 「부작용」 9 · 색소 4 는 부작용 속성의 근거, 「드문 · 중대」 9 는 합병증 근거 | 사용자 10-29 「부작용 ≠ 합병증」(브리프) · DEC-001 D-06 「안전 엣지(금기 · 간격 · 부작용)」 — 부작용을 따로 부름 · step8 family_text 가 이미 「부작용 문장 … 합병증 노드 아님」으로 나눠 둠 · severity 칸이 원천 칸이라 결정론 | 합병증 65 → 남는 합병증 27 · 부작용으로 38 · 예외 확인 9(mild 인데 발생률 낱말이 「흔함」 아님 — 비대칭 · 딤플링 · 두통 …) | 코디(추천 채택) · 예외 9건은 의료진 질문 |
| B2 | 근거 문장 119 종류 재분류 | field 칸(moa · effects · adverse_effects)은 원천 그대로 두고 class 칸을 더함(분류 위 표). 칸과 뜻이 다른 문장 12 은 원천 수정 후보 | step8 evidence.statements[].field · 이 조사 분류(원문 낱말 기준) | {"부작용(흔한 예상 반응)": 9, "색소 반응(PIH — 5단계 PIH 속성과 겹침)": 4, "드문 · 중대 반응(합병증 성격)": 9, "안전성 총평(내약성 · 경미 · 반응 없음)": 6, "기전 · 효과 한계(이상 반응 칸에 있으나 반응 아님)": 4, "효과(기전 칸에 있음)": 3, "적응증(기전 칸에 있음)": 2, "안전성 비교(기전 칸에 있음)": 1, "근거 수준 · 규제(효과 칸에 있음)": 2, "기전": 44, "효과": 35} | 코디 |
| B3 | 끝점 묶음 — 노드 / 엣지 속성 | 엣지 속성(candidates[]). 끝점 묶음 노드 종류는 세우지 않음: 끝점 = 단위 시술 1 · 계열 1 · 계열 + 조건(하위 · 기법 · 부위 · 용도) · 모든 시술 중 하나 + 후보 목록 칸 + 표시 「후보 여럿」. units:a,b,c 는 같은 원문 이름이 가리킨 후보라 묶음 자체에 이름 · 정체가 없음(노드 기준 「원천이 따로 부른다」에 안 맞음) | step8 claims[].a\|b 가 이미 units[] · n_units · flag 칸을 가짐(끝점 = 칸) · silver-graph-build.py 의 set 노드는 그림용(실버 파일에 노드 없음) · 10-27 「동의어가 여러 노드면 후보 전부 반환」(W-1) — 후보는 응답 쪽 개념 · 부위 기준(10-28): 노드는 원천이 따로 부르는 것 | 페이지 끝점 묶음 노드 43 · 묶음 원소 엣지 185 · 실버 끝점 {'all': 1, 'units': 137, 'bundle(여럿)': 2, 'family': 177, 'units(여럿)': 124, 'family(여럿)': 1} | 코디(추천) — 사용자 표 U3 |
| B4 | 엣지 종류 32 → 21(합침 · 나눔) | 위 「엣지 종류(추천)」 표대로 — 같은 뜻 합침 9묶음 · 상위/관련 나눔 1 · 저장 엣지 아님 2(상속 후보 · 묶음 원소) · 새로 1(라인 품목) | 페이지 ekind 표 · 실버 칸 경로 | 페이지 32 → 추천 21 | 코디 |
| B5 | 사전 한 정본 | 표현 행 하나 + targets[] + qualifier 구조(§4) — 7단계 resolver.fam_kw 와 8단계 alias 의 수준 차이는 qualifier 로 합치고 단위 시술 펼치기는 상속 규칙 I3 로 | 사전 겹침 셈 · 7 · 8단계 같은 낱말 다른 대상 | 사전 자리 14 · 원소 2454 · 겹침 147 · 7↔8 같은 낱말 31(대상 다름 17) | 코디 |
| B6 | id 규칙 하나로 | 노드 id = {종류 접두}:{안정 키}. 제품 = 원장 ledger_id 유지(원천 추적) · 목적 = 새 id(접두 + 일련) + 이름 · 결정 고민 노드 J{n}-{한글} 은 이름을 id 에서 떼어 이름 칸으로 · 8단계 끝점 문자열은 {kind, id, qualifier} 구조로 · 확인 조건 대상 세 꼴을 하나로 | id 규칙 불일치 표 | 불일치 10갈래 | 코디 |
| B7 | 상속 저장 위치 하나로 | 상속은 저장하지 않고 골드가 계산(합병증 units_inherit 도 계산으로) — 실버는 「붙는 수준」만 | 상속 I1 · I4 — 합병증만 펼쳐 저장 · 페이지 상속 후보 엣지 | 합병증 units_inherit 합 725 · 제품 상속 후보 합 1364 | 코디 |
| B8 | 확인 조건 「조건 아님」 주장 27 | grade3 「조건 아님(상담 · 시술 준비)」 · kind 상담 · 시술 준비 · 고지 문장은 확인 조건 엣지가 아니라 계열 원문 속성(G10 그대로) — 지금 conditions.claims 안에 섞여 있어 엣지 셈에서 빼야 함 | 로그 step8 §3-10 「상담 · 시술 준비 · 고지 문장은 조건 엣지가 아니라 계열 원문 속성」 | grade3 {'금기': 197, '확인만': 74, '주의': 64, '조건 아님(상담)': 22, '확인만(고지)': 11, '조건 아님(시술 준비)': 5} · kind {'사람 조건': 325, '상담 항목': 22, '시술 준비 항목': 5, '고지 항목': 6, '부위 조건(사람 조건 아님) → 계열 원문 속성 · 부위 표시(site_caution 은 anatomy M1/M2 만)': 2, '효과 문장(조건 아님) → 계열 원문 속성': 1, '근거 수준 문장(조건 아님) → 계열 원문 속성': 1, '사람 조건(시술 쌍에서 옮김 · C10)': 5, '연령대 조건': 6} | 코디 |
| B9 | 업체 · 허가 · 규격 자리 | 업체 = 노드(DEC-003 「제조사 원장」 결정) — id 는 새로(업체 이름 정규화). 허가 · 규격 = 제품 속성(1단계 그대로) | DEC-003 Decision · _RESUME §2 10-27 「실버에 제조사 … 원장 추가」 · step1 6_companies 이름 문자열 | 업체 이름 269종 · 허가 327 | 코디(이미 결정된 것 적용) |
| B10 | 그림 밖 52 정리 | 고민 → 시술 원천 행 중 앵커 없음 52 가운데 18 은 데이터에 앵커가 있음(purpose_nodes · 「목적:」 문자열) — 목적 id(B6) 뒤 그림 안으로. 나머지는 결정대로 앵커 없음(J5 쁘띠시술 · J9 꺼짐) — 원문 보관 | step7 edges[] purpose_nodes · from_concerns · _RESUME §2 10-29 J5 · J9 | {"앵커 없음(결정대로) — (고민 노드 없음 — 꺼짐)": 1, "앵커 없음(결정대로) — (앵커 없음 — 쁘띠시술)": 30, "앵커 없음(결정대로) — (P1 — 고민 앵커 없음)": 3, "앵커 있음 — from_concerns 가 「목적:{이름}」 문자열(페이지가 고민 id 로만 찾음)": 8, "앵커 있음 — purpose_nodes 칸(페이지가 이 칸을 안 읽음)": 10} | 코디 |
| B11 | 부위 노드 없는 단위 시술 31 | 특수 부위 「해당 없음」 · 「병변 단위」를 부위 노드로 세우지 않고 단위 시술 key.site 값 + 표시로(지금 그대로) — 부위 기준(몸 겉에서 가리킬 수 있는 자리)에 안 맞음 | _RESUME §2 10-28 「부위 기준」 · 10-27 DEC-003 OQ-306 「전신 두 뜻 분리」 · step5 rules.special_sites | {"병변 단위": 4, "해당 없음": 27} | 코디 |
| B12 | gate_status · 표시 공통 | gate_status 를 모든 노드 · 엣지 · 주장 공통 3값으로: 자동(완전 일치) · 자동(규칙) · 결정(decided_by 있음 — 사람이 정함). 「미확인」은 상태가 아니라 표시(question · weak · gap)로. 옛 SPEC-004 의 unconfirmed 는 표시로 대체 · 표시는 §5 표 12종 하나로(페이지 한 글자 코드 7 → 이름 있는 표시) | §5 | 표시 12 | 코디 |

## 10. 사용자 최종 판단 — 한 표

나머지 결정 묶음(B1~B12)은 이미 정한 규칙 · 결정을 적용한 것이라 추천대로 가면 되고, 진짜 사용자 몫은 아래 셋뿐이다.

| id | 물을 것 | 고를 것 | 추천 | 왜 | 셈 |
|---|---|---|---|---|---|
| U1 | 합병증 gap 17계열 — 어떻게 둘까 | (가) gap 유지(원천이 먼저 — 로그 step8 §6) / (나) 원천 안 문장으로 일부 채움 — family_text 「부작용 문장」이 있는 gap 계열 7(M10, M12, M13, M17, M4, M5, M6): serious 문장 있는 5(M12, M17, M4, M5, M6)은 합병증으로 · common · uncommon 은 부작용(B1)으로 / (다) 문헌 조사로 채움(새 원천 — 조사 워커) | **(나) 먼저 — 합병증 gap 은 12계열로 줄고(serious 없는 M10, M13 + 원천 없는 N 계열 10) 그것은 (가) 유지 · (다)는 사용자 판단** | gap 17 중 7계열은 브론즈에 「부작용 문장」이 있어 문헌 조사 없이 채울 수 있음(지금 B13 라벨로 「합병증 노드 아님」) · N 계열 10은 원천에 아무것도 없음 | {"M10": {"common": 3, "uncommon": 2, "serious": 0}, "M12": {"common": 3, "uncommon": 3, "serious": 1}, "M13": {"common": 2, "uncommon": 1, "serious": 0}, "M17": {"common": 2, "uncommon": 1, "serious": 1}, "M4": {"common": 4, "uncommon": 3, "serious": 2}, "M5": {"common": 3, "uncommon": 1, "serious": 1}, "M6": {"common": 3, "uncommon": 3, "serious": 3}, "N1": {"common": 0, "uncommon": 0, "serious": 0}, "N10": {"common": 0, "uncommon": 0, "serious": 0}, "N2": {"common": 0, "uncommon": 0, "serious": 0}, "N3": {"common": 0, "uncommon": 0, "serious": 0}, "N4": {"common": 0, "uncommon": 0, "serious": 0}, "N5": {"common": 0, "uncommon": 0, "serious": 0}, "N6": {"common": 0, "uncommon": 0, "serious": 0}, "N7": {"common": 0, "uncommon": 0, "serious": 0}, "N8": {"common": 0, "uncommon": 0, "serious": 0}, "N9": {"common": 0, "uncommon": 0, "serious": 0}} |
| U2 | 부작용을 어디에 둘까 | (가) 계열 속성 + 제품 × 계열 · 단위 시술 덮어쓰기(추천) / (나) 부작용 노드 종류 새로(합병증처럼) / (다) 합병증 노드 하나에 kind 칸만 | **(가)** | 흔한 예상 반응은 이름이 계열마다 같은 말(멍 · 부기 · 홍반)이라 노드로 세우면 같은 이름 노드가 계열 수만큼 · 사용자 요청 「단위 시술 · 제품 속성으로」(브리프) | severity mild 38 · common 문장 59 |
| U3 | 끝점 묶음 44 — 노드 / 엣지 속성 | (가) 엣지 속성 candidates[](추천) / (나) 정식 노드 종류 | **(가)** | 엣지 속성(candidates[]). 끝점 묶음 노드 종류는 세우지 않음: 끝점 = 단위 시술 1 · 계열 1 · 계열 + 조건(하위 · 기법 · 부위 · 용도) · 모든 시술 중 하나 + 후보 목록 칸 + 표시 「후보 여럿」. units:a,b,c 는 같은 원문 이름이 가리킨 후보라 묶음 자체에 이름 · 정체가 없음(노드 기준 「원천이 따로 부른다」에 안 맞음) | 페이지 끝점 묶음 노드 43 · 묶음 원소 엣지 185 · 실버 끝점 {'all': 1, 'units': 137, 'bundle(여럿)': 2, 'family': 177, 'units(여럿)': 124, 'family(여럿)': 1} |

## 11. 이 조사가 안 한 것

- 골드 규칙(상속을 실제로 펼치는 계산 · 응답 거르기) — 상속 규칙 정의까지만
- 실버 json · 결정 · 기록 수정 — 읽기만. 원천 수정 후보(근거 문장 칸 어긋남 · 비타민C 사전 충돌 등)는 목록으로만
- 가상 문장 시험 — 지금 데이터만 셈
- 셈 스크립트는 워커 scratchpad(semantic-build.py · semantic-md.py)에만 있음 — 작업 폴더에 산출 두 파일 말고는 쓰지 않음. 실버 파일이 또 바뀌면 다시 세야 함

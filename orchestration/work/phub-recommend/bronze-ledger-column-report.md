# 원장 JSON 21개 컬럼(키) 구조 분석 리포트 — 브론즈

- 작성일: 2026-11-03
- 입력(읽기 전용): `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/*.json` 21개
- 방법: `bronze-ledger-column-scan.py` 로 21개 파일을 기계적으로 훑고, 결과 `bronze-ledger-column-scan.json` 에서 이 문서를 렌더(`bronze-ledger-column-report-render.py`). 셋 다 스크래치 디렉토리 `scratchpad/` 에 있다.
- 표기 규약: 배열은 `[]`, 코드형 동적 키(M1, P1-2, M1-2-1, auto-63-…, M1_to_M7)는 `{code}` 로 접었다. 「잎 키」= 스칼라 또는 빈 배열/빈 객체가 놓이는 경로.
- 이 문서는 **관찰만** 적는다. 어느 쪽이 맞다는 판정, 어떻게 고칠지의 설계는 하지 않는다. 기존 작업물(source-map, step*, DATA-001, `_archive/`)은 읽지 않았다.
- 합계: 파일 21 · 잎 키 경로 573 · 바이트 1,252,346

## 1. 요약 표

| 파일 | 바이트 | 최상위 형태 | 레코드 수 | 잎 키 | 한 줄 설명 |
|---|---|---|---|---|---|
| `anatomy-danger-zones.json` | 29,555 | 객체(메타 3 + 데이터 키 2) | zones 11 | 67 | 얼굴 11개 부위(zone)별 혈관·신경·조직 수치·보톡스/필러 주의사항. 계열 코드 없음 |
| `combo-recipes.json` | 6,486 | 객체(메타 3 + 데이터 키 1) | recipes 7 | 15 | 목적(goal)별 시술 조합 레시피 7개. 시술은 M 코드 배열, 후속 프로토콜(week/action) 포함 |
| `complications.json` | 58,333 | 객체(메타 0 + 데이터 키 2) | categories 10 / complications 65 | 17 | 계열 10개(M1·M2·M3·M7·M8·M9·M11·M14·M15·M16)별 합병증 65건: 중증도·발생률·기전·관리·예방 |
| `consent-checklist.json` | 21,047 | 객체(메타 3 + 데이터 키 1) | categories 17 | 8 | 계열 17개별 필수 고지·금기·응급 징후 문자열 배열 |
| `contraindications.json` | 6,390 | 객체(메타 3 + 데이터 키 1) | rules 27 | 10 | 계열 쌍(from→to) 27개의 병행 금기/주의/간격 규칙 |
| `extracted.json` | 56,589 | 객체(최상위 키 = M 코드) | (최상위 {code}) 17 | 24 | 계열 17개의 교과서 추출 요약(개요·기전·적응증·안전성·금기·관리). 최상위 키가 M 코드 |
| `literature-evidence.json` | 118,979 | 객체(메타 3 + 데이터 키 2) | (categories.{code}) 17 / moa 50 / adverse_effects 32 / effects 37 | 68 | 계열 17개별 문헌 근거 문장 119개(moa/adverse_effects/effects) + 인용(PMID/DOI) + 환자용 4개 국어 문장 |
| `market-pricing.json` | 12,214 | 객체(메타 4 + 데이터 키 1) | categories 17 / items 122 | 11 | 계열 17개별 시장 가격 항목 122개(low/mid/high, KRW, 단위 문자열) |
| `patient-education.json` | 26,551 | 객체(메타 2 + 데이터 키 1) | categories 17 / common_concerns 51 | 12 | 계열 17개별 환자 설명(쉬운 설명·원리·지속·통증·다운타임) + Q&A 51개 |
| `pih-risk.json` | 11,875 | 객체(메타 3 + 데이터 키 3) | procedures 26 | 18 | 에너지/필링 계열 세부 시술 26개의 PIH 위험도·발생률·위험인자·예방. procedure_ref 로 taxonomy 하위 id 참조 |
| `post-procedure-timeline.json` | 20,081 | 객체(메타 3 + 데이터 키 2) | timelines 10 / phases 43 | 16 | 시술 10종의 시술 후 경과(phases: Day 구간별 정상/이상/주의/응급 증상 배열) |
| `pre-procedure-checklist.json` | 14,569 | 객체(메타 3 + 데이터 키 2) | universal_checks 12 / category_specific 17 / checks 123 | 11 | 공통 체크 12개 + 계열 17개별 시술 전 확인 항목 123개(label/type) |
| `problem-combos.json` | 25,026 | 객체(메타 3 + 데이터 키 1) | combos 8 / packages 24 | 18 | 고민(P) 8개별 상담용 패키지 24개: tier·제품·가격대·세일즈 멘트·임상 근거 |
| `problem-packages.json` | 73,526 | 객체(메타 3 + 데이터 키 1) | problems 14 / complaints 115 / procedures 254 / combos 146 | 19 | 고민 14개 × 주호소(cc) 115개별 시술(제품 포함)·조합·대안. description 에 「taxonomy P1~P14 기반 자동 생성」 |
| `procedure-comparison.json` | 18,002 | 객체(메타 2 + 데이터 키 1) | comparisons 9 / procedures 39 | 18 | 비교 주제 9개(lifting 등)별 시술 39개의 기전·통증·다운타임·비용·적합/한계·PIH |
| `procedure-profiles.json` | 19,548 | 객체(메타 3 + 데이터 키 1) | profiles 17 | 27 | 계열 17개의 플로어 운영 프로파일(phase 순서·마취·준비시간·소요시간·위험 점수·주의·관리) |
| `products.json` | 8,322 | 객체(메타 3 + 데이터 키 8) | 섹션 8 / products 59 | 61 | 제품-제조사 매핑 8개 섹션 59개 제품(name/name_en/제조사/국가/mfds). 섹션 키가 영문 슬러그 |
| `synergy.json` | 32,905 | 객체(메타 2 + 데이터 키 1) | links 115 | 10 | 시술 노드 쌍 115개의 시너지 링크(함께/다음에/대신). 노드는 `M코드-이름` 합성 문자열 |
| `taxonomy.json` | 660,497 | 객체(메타 0 + 데이터 키 2) | modality 17 / subcategories 74 / items 521 / products 59 / problem 14 / subcategories 53 / items 117 | 87 | 계열(modality) 17 → 하위 74 → 항목 521 + 계열별 extracted/products, 고민(problem) 14 → 하위 53 → 항목 117(modality_ref). 가장 큼(660KB) |
| `treatment-optimization.json` | 22,887 | 객체(메타 3 + 데이터 키 5) | by_concern 8 / severity_levels 24 / by_age_group 4 / combination_rules 8 / annual_plans 3 | 36 | 고민 8개 × 중증도 3단계의 최적 조합·순서·근거, 연령대 4개 권장, 조합 규칙 8개, 연간 플랜 3개 |
| `treatment-sequence.json` | 8,964 | 객체(메타 3 + 데이터 키 5) | principles 13 / sequence_order 11 / incompatible_same_day 9 / common_combos 8 / minimum_intervals 9 | 20 | 동일 세션 시술 순서 11단계, 당일 병행 금기 9쌍, 대표 조합 8개, 최소 간격 9개. 시술명 대부분 자유 텍스트 |

메타 키 현황(`version`/`updated`):

| 파일 | version | updated |
|---|---|---|
| `anatomy-danger-zones.json` | 1.2 | 2026-07-26 |
| `combo-recipes.json` | 1.0 | 2026-04-04 |
| `complications.json` | — | — |
| `consent-checklist.json` | 1.3 | 2026-07-26 |
| `contraindications.json` | 1.1 | 2026-07-11 |
| `extracted.json` | — | — |
| `literature-evidence.json` | 2.0 | 2026-09-03 |
| `market-pricing.json` | 1.1 | 2026-07-26 |
| `patient-education.json` | 1.3 | 2026-07-26 |
| `pih-risk.json` | 1.0 | 2026-04-05 |
| `post-procedure-timeline.json` | 1.1 | 2026-07-11 |
| `pre-procedure-checklist.json` | 1.1 | 2026-04-05 |
| `problem-combos.json` | 1.2 | 2026-07-26 |
| `problem-packages.json` | 6.2 | 2026-07-26 |
| `procedure-comparison.json` | 1.3 | 2026-07-26 |
| `procedure-profiles.json` | 3.3 | 2026-07-26 |
| `products.json` | 1.2 | 2026-07-26 |
| `synergy.json` | 1.3 | 2026-07-26 |
| `taxonomy.json` | — | — |
| `treatment-optimization.json` | 1.4 | 2026-07-26 |
| `treatment-sequence.json` | 1.3 | 2026-07-26 |

키 표기 스타일(camelCase 키가 있는 파일):

| 파일 | 키 수 | camelCase 키 |
|---|---|---|
| `combo-recipes.json` | 17 | `expectedResults`, `followUp`, `patientExplanation`, `repeatCycle` |
| `problem-combos.json` | 20 | `clinicalRationale`, `expectedResult`, `priceRange`, `productTier`, `riskBenefit`, `salesPitch`, `tierLabel`, `upsellHook` |
| `procedure-profiles.json` | 28 | `bleedingRisk`, `createsChannel`, `createsWound`, `durationMax`, `durationMin`, `hasHA`, `hasProtein`, `needsAnesthesia`, `needsCleansing`, `phaseOrder`, `practicalNotes`, `prepNotes`, `prepTime`, `swellingRisk`, `thermalLoad`, `usesGel` |

## 2. 파일별 절

### 2.1 `anatomy-danger-zones.json` — 29,555B · 잎 키 67

얼굴 11개 부위(zone)별 혈관·신경·조직 수치·보톡스/필러 주의사항. 계열 코드 없음

**최상위 구조**

- 메타 키: `version`=`1.2`, `updated`=`2026-07-26`, `consensus_method`=`3-AI Expert Consensus (Perplexity research + Gemin…`
- 데이터 키: `critical_safety_facts` (dict, 4), `zones` (list, 11)
- 배열: `zones`×1(len 11~11, 합 11), `zones[].vessels`×11(len 2~3, 합 24), `zones[].vessels[].depth_range_mm`×5(len 2~2, 합 10), `zones[].nerves`×11(len 1~3, 합 21), `zones[].clinical_pearls`×11(len 4~7, 합 61), `zones[].tissue_data.labial_artery_depth_range_mm`×1(len 2~2, 합 2)

**잎 키 표**

| 경로 | 타입 | 횟수 | null | 빈값 | distinct | 예시 |
|---|---|---|---|---|---|---|
| `version` | str | 1 | 0 | 0 | 1 | `1.2` |
| `updated` | str | 1 | 0 | 0 | 1 | `2026-07-26` |
| `consensus_method` | str | 1 | 0 | 0 | 1 | `3-AI Expert Consensus (Perplexity research + Gemin…` |
| `critical_safety_facts.minimum_filler_for_blindness` | str | 1 | 0 | 0 | 1 | `약 0.04mL (supratrochlear 0.0397mL, supraorbital 0.…` |
| `critical_safety_facts.blindness_highest_risk_zones` | str | 1 | 0 | 0 | 1 | `코 56.3%, 미간 27.1%, 이마 18.8%, 비순주름 14.6% (Beleznay …` |
| `critical_safety_facts.mechanism` | str | 1 | 0 | 0 | 1 | `역행성 동맥 색전 — 안동맥(ophthalmic artery)으로 역류 → 망막 허혈` |
| `critical_safety_facts.caveat` | str | 1 | 0 | 0 | 1 | `이 수치들은 시술자 경계를 느슨하게 만들지 말 것. 어떤 주사라도 혈관 내 주입이면 실명 …` |
| `zones[].id` | str | 11 | 0 | 0 | 11 | `forehead` · `glabella` · `temple` |
| `zones[].name_ko` | str | 11 | 0 | 0 | 11 | `이마` · `미간` · `관자놀이` |
| `zones[].name_en` | str | 11 | 0 | 0 | 11 | `Forehead` · `Glabella` · `Temple` |
| `zones[].danger_level` | int | 11 | 0 | 0 | 4 | `4` · `5` · `3` |
| `zones[].danger_color` | str | 11 | 0 | 0 | 4 | `orange` · `red` · `yellow` |
| `zones[].vessels[].name` | str | 24 | 0 | 0 | 20 | `활차상동맥 (Supratrochlear artery)` · `안와상동맥 (Supraorbital artery)` · `배비동맥 (Dorsal nasal artery)` |
| `zones[].vessels[].depth_mm` | float | 22 | 0 | 0 | 11 | `1.8` · `1.7` · `2.0` |
| `zones[].vessels[].diameter_mm` | float | 24 | 0 | 0 | 13 | `0.7` · `0.8` · `0.6` |
| `zones[].vessels[].course` | str | 24 | 0 | 0 | 24 | `안와상연에서 상방으로 주행, 이마 중앙선 근처` · `안와상절흔에서 상방으로 주행` · `미간 정중앙에서 상방 주행, 양측 교차 문합` |
| `zones[].vessels[].danger` | str | 24 | 0 | 0 | 24 | `안동맥과 직접 연결 — 역행성 색전 시 실명 위험` · `안동맥 분지 — 역행성 색전 위험` · `0.0397mL로 안동맥 폐색 가능 — 미간은 주요 실명 고위험 부위(2019 업데이트 2…` |
| `zones[].vessels[].note` | str | 2 | 0 | 0 | 2 | `평균 1.8mm이나 아시아인 피부는 더 얇고 개인 변이가 커 0.5mm 수준까지 표재성일 …` · `평균값이며 개인 변이 큼 — 고정 깊이 신뢰 금지` |
| `zones[].vessels[].depth_range_mm[]` | float | 10 | 0 | 0 | 6 | `0.5` · `2.2` · `3.2` |
| `zones[].nerves[].name` | str | 21 | 0 | 0 | 16 | `활차상신경 (Supratrochlear nerve)` · `안와상신경 (Supraorbital nerve)` · `측두신경 (Temporal branch of facial nerve)` |
| `zones[].nerves[].type` | str | 21 | 0 | 0 | 2 | `sensory` · `motor` |
| `zones[].nerves[].significance` | str | 21 | 0 | 0 | 21 | `이마 내측 감각` · `이마 외측 감각` · `미간 및 이마 내측 감각` |
| `zones[].safe_injection_depth` | str | 11 | 0 | 0 | 11 | `골막상층 (supraperiosteal) — 혈관은 표재성이므로 깊은 층이 안전` · `골막상층 (supraperiosteal) — 절대 피하층 주사 금지` · `심부측두근막 심층 (deep temporal fascia deep layer) 또는 골막상` |
| `zones[].tissue_data.frontalis_thickness.midpupil_mm` | float | 1 | 0 | 0 | 1 | `1.8` |
| `zones[].tissue_data.frontalis_thickness.lateral_canthus_mm` | float | 1 | 0 | 0 | 1 | `1.61` |
| `zones[].tissue_data.frontalis_thickness.lateral_orbital_rim_mm` | float | 1 | 0 | 0 | 1 | `0.11` |
| `zones[].tissue_data.skin_to_periosteum_mm` | float | 1 | 0 | 0 | 1 | `5.0` |
| `zones[].tissue_data.notes` | str | 11 | 0 | 0 | 11 | `이마 피부-골막 거리 평균 0.5cm — 매우 얇음` · `추미근(CSM, corrugator supercilii muscle) 평균 두께 약 1.6…` · `Pitanguy line 위에서 안면신경 측두분지가 표재성으로 주행 — 이 선 위 피하층 …` |
| `zones[].clinical_pearls[]` | str | 61 | 0 | 0 | 61 | `이마 피부-골막 거리 평균 0.5cm — 매우 얇음` · `활차상동맥은 중앙선 근처에서 표재성 → 정중선 주사 주의` · `캐뉼러 사용 권장 (니들 대비 혈관 천자 위험 감소)` |
| `zones[].botox_specific.target_muscle` | str | 11 | 0 | 0 | 11 | `전두근 (Frontalis)` · `추미근 (Corrugator supercilii), 비근근 (Procerus)` · `측두근 (Temporalis) — 이갈이/사각턱 보조` |
| `zones[].botox_specific.risk` | str | 11 | 0 | 0 | 11 | `눈꺼풀 처짐 (보톡스 확산 시 상안검거근 영향)` · `눈썹 처짐 (과다 주사 시), 이마 보상적 주름 증가` · `측두부 함몰(과도 위축), 씹는 힘 약화` |
| `zones[].botox_specific.safe_zone` | str | 11 | 0 | 0 | 11 | `안와상연 상방 2cm 이상, 외측은 측두선 내측` · `추미근 body 내 주사, 안와상연 상방 1cm 이상` · `측두근 중앙부, 깊은 층` |
| `zones[].botox_specific.diffusion_range_cm` | str | 1 | 0 | 0 | 1 | `1.5-3.0` |
| `zones[].botox_specific.key_warning` | str | 11 | 0 | 0 | 11 | `보톡스 확산 1.5-3cm → 안와상연 너무 가까이 주사 시 안검하수` · `추미근 외측 과다 주사 → 눈썹 처짐(Mephisto sign)` · `표재성 주사 → 안면신경 측두분지 마비 → 이마 거상 불가` |
| `zones[].botox_specific.dose_range` | str | 11 | 0 | 0 | 11 | `10-30 units (2-5 포인트/측, 2-5U/포인트)` · `추미근 10-25U, 비근근 5-10U` · `20-40U/측 (이갈이), 관자놀이 필러와 병행 시 주의` |
| `zones[].filler_specific.risk_level` | int | 11 | 0 | 0 | 4 | `4` · `5` · `3` |
| `zones[].filler_specific.primary_risk` | str | 11 | 0 | 0 | 11 | `역행성 색전 → 실명` · `역행성 색전 → 실명 (최고 위험)` · `천측두동맥-안동맥 및 심부측두동맥-안동맥 문합 경로를 통한 역행성 색전 → 시력손실/실명,…` |
| `zones[].filler_specific.safe_technique` | str | 11 | 0 | 0 | 11 | `골막상 캐뉼러, 소량 다점, 저압 주입` · `골막상 캐뉼러, 0.05mL 이하/점, 흡인은 보조 수단으로만 사용, 저압·저속 주입` · `심부측두근막 심층 캐뉼러 주입, 동맥 촉진 후 주사` |
| `zones[].filler_specific.max_per_point_ml` | float | 11 | 0 | 0 | 4 | `0.1` · `0.05` · `0.2` |
| `zones[].filler_specific.preferred_product` | str | 11 | 0 | 0 | 11 | `용해 가능한 저점도 HA (CaHA는 hyaluronidase로 용해 불가하여 실명 위험 …` · `저점도 HA (hyaluronidase로 용해 가능한 제품만)` · `실명 위험 부위이므로 비가역적 CaHA보다 용해 가능한 HA를 우선 고려. CaHA 사용 …` |
| `zones[].tissue_data.csm_mean_thickness_mm` | float | 1 | 0 | 0 | 1 | `1.62` |
| `zones[].tissue_data.csm_thickness_variation_mm` | float | 1 | 0 | 0 | 1 | `0.4` |
| `zones[].filler_specific.emergency_protocol` | str | 3 | 0 | 0 | 3 | `시력저하·안통 발생 시 즉시 주입 중단/응급콜 및 망막안과·응급실 이송(지체 없이 즉각 대…` · `시야 변화 즉시 → hyaluronidase + 안과 응급` · `blanching 즉시 → 주입 중단 → 고용량 pulsed hyaluronidase 다점…` |
| `zones[].tissue_data.stl_entry_point` | str | 1 | 0 | 0 | 1 | `STL(상측두융합선, Superior temporal line)에서 측두근막이 두 층으로 …` |
| `zones[].tissue_data.pitanguy_line` | str | 1 | 0 | 0 | 1 | `이주(tragus) 하부 0.5cm → 눈썹 외측 1.5cm 상방을 잇는 선 위에 측두신경…` |
| `zones[].tissue_data.tear_trough_anatomy` | str | 1 | 0 | 0 | 1 | `눈물고랑(tear trough)은 안와연 바로 아래 — 안륜근(orbicularis ocu…` |
| `zones[].tissue_data.muscle_fiber_data` | str | 1 | 0 | 0 | 1 | `눈물고랑 부위 안륜근 섬유 두께 0.5-1.0mm (SRA 2024)` |
| `zones[].tissue_data.orbital_septum` | str | 1 | 0 | 0 | 1 | `안와격막(orbital septum)은 안와 내용물의 방벽 — 관통 시 안와 내 합병증` |
| `zones[].tissue_data.rhinion_subcutaneous_mm` | float | 1 | 0 | 0 | 1 | `2.02` |
| `zones[].tissue_data.rhinion_data_source` | str | 1 | 0 | 0 | 1 | `JCD 2024, USG n=52` |
| `zones[].tissue_data.nasal_tip_skin_thickness_mm` | float | 1 | 0 | 0 | 1 | `1.5` |
| `zones[].tissue_data.facial_artery_distance_to_nlf_mm` | float | 1 | 0 | 0 | 1 | `5.0` |
| `zones[].tissue_data.asian_adjacent_distribution_percent` | float | 1 | 0 | 0 | 1 | `93.3` |
| `zones[].tissue_data.within_5mm_percent` | float | 1 | 0 | 0 | 1 | `42.9` |
| `zones[].tissue_data.facial_artery_diameter_mandible_mm` | float | 1 | 0 | 0 | 1 | `1.9` |
| `zones[].tissue_data.facial_artery_diameter_nasal_mm` | float | 1 | 0 | 0 | 1 | `0.8` |
| `zones[].tissue_data.buccal_fat_pad` | str | 1 | 0 | 0 | 1 | `협지방체(Buccal fat pad): SMAS 심층에 위치, 저작공간까지 연장` |
| `zones[].tissue_data.smas_depth_mm` | float | 1 | 0 | 0 | 1 | `4.5` |
| `zones[].tissue_data.sub_smas_vs_subcutaneous` | str | 1 | 0 | 0 | 1 | `Sub-SMAS: 볼륨 리프팅 / Subcutaneous: 표재성 주름 교정` |
| `zones[].tissue_data.labial_artery_depth_range_mm[]` | float | 2 | 0 | 0 | 2 | `3.0` · `6.0` |
| `zones[].tissue_data.superior_labial_artery_submucosal_percent` | float | 1 | 0 | 0 | 1 | `58.5` |
| `zones[].tissue_data.mental_foramen_location` | str | 1 | 0 | 0 | 1 | `하악 제2소구치 하방, 하악연에서 상방 약 13mm` |
| `zones[].tissue_data.dao_coverage` | str | 1 | 0 | 0 | 1 | `DAO(구각하제근)의 67.7%가 이신경공을 덮고 있음` |
| `zones[].tissue_data.marginal_mandibular_depth` | str | 1 | 0 | 0 | 1 | `하악연에서 1-2cm 하방에서 표재성 주행 (20% 환자에서 하악연 하방 1cm까지)` |
| `zones[].tissue_data.facial_artery_crossing` | str | 1 | 0 | 0 | 1 | `안면동맥은 하악연의 교근 전연(anterior border of masseter)에서 교차` |
| `zones[].tissue_data.platysma_thickness_mm` | float | 1 | 0 | 0 | 1 | `1.5` |
| `zones[].tissue_data.platysma_coverage` | str | 1 | 0 | 0 | 1 | `광경근은 쇄골~하악연까지, 정중선에서 결손 부위 있음` |

**enum 처럼 보이는 키** (문자열·3회 이상·distinct ≤ 10·반복 있음)

| 경로 | distinct 값 (횟수) |
|---|---|
| `zones[].danger_color` | `orange`(4), `red`(3), `yellow`(3), `green`(1) |
| `zones[].nerves[].type` | `sensory`(15), `motor`(6) |

**식별자 후보** (레코드 배열별)

| 레코드 배열 | 건수 | 키 | 존재 | distinct | 유일 | 중복 예 |
|---|---|---|---|---|---|---|
| `zones` | 11 | `id` | 11 | 11 | ○ |  |
| `zones[].vessels` | 24 | `name` | 24 | 20 | ✗ | `활차상동맥 (Supratrochlear artery)`, `배비동맥 (Dorsal nasal artery)`, `각동맥 (Angular artery)`, `안면동맥 (Facial artery)` |
| `zones[].nerves` | 21 | `name` | 21 | 16 | ✗ | `활차상신경 (Supratrochlear nerve)`, `안와하신경 (Infraorbital nerve)`, `협근신경 (Buccal branch of facial nerve)`, `이신경 (Mental nerve)` |

**일부 레코드에만 있는 키**

| 레코드 배열 | 건수 | 키=존재수 |
|---|---|---|
| `zones[].vessels` | 24 | `depth_mm`=22, `note`=2, `depth_range_mm`=5 |

**관찰** (원장 자체에서 보이는 것. 판정 아님)

- `zones[].tissue_data` 는 부위마다 키가 전부 다르다(11개 zone 에 `notes` 만 공통, 나머지 31개 잎 경로는 각각 zone 1개에만). 고정 스키마가 아니라 부위별 자유 구조.
- `vessels[].depth_mm` 는 24건 중 22건, 대신 `depth_range_mm[]` 가 5건 — 깊이가 단일값/범위 두 형태로 섞여 있다.
- `danger_level`(2~5 정수)과 `danger_color`(green/yellow/orange/red), `filler_specific.risk_level` 이 zone 마다 같은 값으로 셋 다 들어 있다.
- `botox_specific.diffusion_range_cm` 은 문자열 `1.5-3.0`(1건), `filler_specific.emergency_protocol` 은 3건에만 있다.
- 혈관·신경 이름은 `한글 (영문)` 합성 문자열. 같은 혈관이 여러 zone 에 반복(활차상동맥, 안면동맥 등 4종 중복).
- M/P 코드 참조가 하나도 없다. 부위 id 는 영문 슬러그(forehead, glabella …)이고 taxonomy 의 부위 라벨(코, 이마/관자놀이 …)과는 표기가 다르다.

### 2.2 `combo-recipes.json` — 6,486B · 잎 키 15

목적(goal)별 시술 조합 레시피 7개. 시술은 M 코드 배열, 후속 프로토콜(week/action) 포함

**최상위 구조**

- 메타 키: `version`=`1.0`, `updated`=`2026-04-04`, `description`=`대표원장급 검증 조합 레시피 — 목적별 프리셋 + 기대 효과 + 후속 프로토콜`
- 데이터 키: `recipes` (list, 7)
- 배열: `recipes`×1(len 7~7, 합 7), `recipes[].procedures`×7(len 2~4, 합 19), `recipes[].followUp`×7(len 3~5, 합 28)

**잎 키 표**

| 경로 | 타입 | 횟수 | null | 빈값 | distinct | 예시 |
|---|---|---|---|---|---|---|
| `version` | str | 1 | 0 | 0 | 1 | `1.0` |
| `updated` | str | 1 | 0 | 0 | 1 | `2026-04-04` |
| `description` | str | 1 | 0 | 0 | 1 | `대표원장급 검증 조합 레시피 — 목적별 프리셋 + 기대 효과 + 후속 프로토콜` |
| `recipes[].id` | str | 7 | 0 | 0 | 7 | `R1` · `R2` · `R3` |
| `recipes[].name` | str | 7 | 0 | 0 | 7 | `리프팅 기본` · `리프팅 풀패키지` · `피부 재생 골든루틴` |
| `recipes[].subtitle` | str | 7 | 0 | 0 | 7 | `처진 살 올리기 입문` · `확실한 리프팅 + 볼륨 복원` · `MTS + PRP + 스킨부스터` |
| `recipes[].goal` | str | 7 | 0 | 0 | 6 | `lifting` · `regeneration` · `tightening` |
| `recipes[].intensity` | str | 7 | 0 | 0 | 4 | `기본` · `풀패키지` · `표준` |
| `recipes[].procedures[]` | str | 19 | 0 | 0 | 9 | `M9` · `M1` · `M7` |
| `recipes[].expectedResults` | str | 7 | 0 | 0 | 7 | `턱선 정리 + 볼처짐 개선. 자연스러운 리프팅. 주변에서 '좀 쉬었나?' 수준` · `확실한 턱선 + 볼/관자놀이 볼륨 복원 + 주름 개선. '5살 어려 보이는' 수준` · `피부결 개선 + 톤 균일 + 잔주름 완화 + 탄력 향상. 3~5회 반복 시 확연한 차이` |
| `recipes[].patientExplanation` | str | 7 | 0 | 0 | 7 | `초음파로 피부 아래 콜라겐을 조여서 당기고, 보톡스로 아래로 당기는 근육을 쉬게 해서 올라…` · `실로 처진 뼈대를 올리고(텐트 기둥), 초음파로 주변을 단단하게 고정한 뒤, 꺼진 곳은 필…` · `미세 바늘로 피부에 수천 개의 아주 작은 통로를 만들고, 거기에 본인 피의 성장인자(PRP…` |
| `recipes[].analogy` | str | 7 | 0 | 0 | 7 | `HIFU = 옷감을 다림질해서 팽팽하게, 보톡스 = 늘어진 고무줄을 리셋` · `실 = 텐트 기둥 세우기, HIFU = 천을 팽팽하게, 필러 = 쿠션 넣기, 보톡스 = 찡…` · `MTS = 밭에 씨앗구멍 파기, PRP = 비료 뿌리기, 스킨부스터 = 물 주기` |
| `recipes[].repeatCycle` | str | 7 | 0 | 0 | 7 | `3~6개월 간격 반복` · `실리프팅 12개월, HIFU 6개월, 보톡스 3~4개월, 필러 6~12개월` · `2~4주 간격, 총 3~5회가 1클` |
| `recipes[].followUp[].week` | int | 28 | 0 | 0 | 15 | `4` · `12` · `24` |
| `recipes[].followUp[].action` | str | 28 | 0 | 0 | 27 | `경과 확인. 효과 부족 부위 추가 HIFU 가능` · `보톡스 터치업 (효과 감소 시)` · `리프팅 유지 시술 (HIFU 반복 or 실리프팅 업그레이드)` |

**enum 처럼 보이는 키** (문자열·3회 이상·distinct ≤ 10·반복 있음)

| 경로 | distinct 값 (횟수) |
|---|---|
| `recipes[].goal` | `lifting`(2), `regeneration`(1), `tightening`(1), `texture`(1), `anti-aging`(1), `tone`(1) |
| `recipes[].intensity` | `표준`(3), `기본`(2), `풀패키지`(1), `적극`(1) |
| `recipes[].procedures[]` | `M1`(4), `M9`(3), `M5`(3), `M4`(3), `M2`(2), `M7`(1), `M12`(1), `M11`(1), `M8`(1) |

**식별자 후보** (레코드 배열별)

| 레코드 배열 | 건수 | 키 | 존재 | distinct | 유일 | 중복 예 |
|---|---|---|---|---|---|---|
| `recipes` | 7 | `id` | 7 | 7 | ○ |  |
| `recipes` | 7 | `name` | 7 | 7 | ○ |  |

**관찰** (원장 자체에서 보이는 것. 판정 아님)

- `goal` 은 영문 슬러그(lifting, regeneration, tightening, texture, anti-aging, tone), `intensity` 는 한글(기본/풀패키지/표준/적극) — 한 레코드 안에 영/한 코드가 섞여 있다.
- `procedures[]` 는 M 코드 배열(9종). 레시피 id 는 `R1~R7` 로 이 파일에만 있는 체계.
- 키 이름이 camelCase(expectedResults, patientExplanation, repeatCycle, followUp) — 대부분의 파일(snake_case)과 다르다.
- `followUp[].week` 는 정수(2~52), `action` 은 자유 텍스트. `repeatCycle` 도 자유 텍스트(`3~6개월 간격 반복`).

### 2.3 `complications.json` — 58,333B · 잎 키 17

계열 10개(M1·M2·M3·M7·M8·M9·M11·M14·M15·M16)별 합병증 65건: 중증도·발생률·기전·관리·예방

**최상위 구조**

- 데이터 키: `severity_levels` (dict, 4), `categories` (list, 10)
- 배열: `categories`×1(len 10~10, 합 10), `categories[].complications`×10(len 3~12, 합 65), `categories[].complications[].risk_factors`×19(len 4~6, 합 92)

**잎 키 표**

| 경로 | 타입 | 횟수 | null | 빈값 | distinct | 예시 |
|---|---|---|---|---|---|---|
| `severity_levels.mild` | str | 1 | 0 | 0 | 1 | `경미 — 자연 소실, 경과 관찰` |
| `severity_levels.moderate` | str | 1 | 0 | 0 | 1 | `중등도 — 치료 필요, 클리닉 방문` |
| `severity_levels.severe` | str | 1 | 0 | 0 | 1 | `중증 — 즉시 치료, 후유증 가능` |
| `severity_levels.critical` | str | 1 | 0 | 0 | 1 | `위급 — 응급 대응, 비가역적 손상 가능` |
| `categories[].id` | str | 10 | 0 | 0 | 10 | `M1` · `M2` · `M3` |
| `categories[].name` | str | 10 | 0 | 0 | 10 | `보톡스` · `필러` · `바이오스티뮬레이터/콜라겐부스터` |
| `categories[].complications[].name` | str | 65 | 0 | 0 | 63 | `주사 부위 통증` · `멍 (타박상)` · `주사 부위 홍반·부종` |
| `categories[].complications[].severity` | str | 65 | 0 | 0 | 4 | `mild` · `moderate` · `severe` |
| `categories[].complications[].incidence` | str | 65 | 0 | 0 | 56 | `대부분 (일시적)` · `약 11-25% (부위·기법에 따라)` · `흔함 (일시적)` |
| `categories[].complications[].onset` | str | 65 | 0 | 0 | 47 | `시술 즉시` · `시술 당일` · `시술 직후~수 시간` |
| `categories[].complications[].mechanism` | str | 65 | 0 | 0 | 65 | `바늘 천자 및 약액 주입에 의한 물리적 자극. 부위·용량 무관하게 모든 보톡스 주사에 공통…` · `바늘이 진피/피하 소혈관을 천자하여 혈관외 출혈. 어느 부위든 발생 가능하나 혈관이 풍부·…` · `주입에 대한 국소 염증/자극 반응 및 약액 볼륨에 의한 팽윤. 부위 무관 공통 반응` |
| `categories[].complications[].risk_factors` | list(empty) | 46 | 0 | 46 | 0 |  |
| `categories[].complications[].management` | str | 65 | 0 | 0 | 65 | `냉각(아이스팩), 미세바늘(32G 이상) 사용, 필요시 표면마취크림. 대부분 수 분 내 소…` · `즉시 압박, 24-48시간 냉찜질 후 온찜질, 아르니카/비타민K 크림. 대부분 7-14일 …` · `냉찜질, 대부분 수 시간~1일 내 소실. 지속·확대 시 알레르기/감염 감별` |
| `categories[].complications[].prevention` | str | 65 | 0 | 0 | 65 | `가는 바늘, 저속 주입, 냉각·주의분산, 통증 민감 부위는 국소마취/신경차단 고려` · `시술 전 1주간 항응고·아스피린·NSAID·오메가3·비타민E·음주 자제, 표재 혈관 투과조…` · `무균 술기, 적정 희석·용량, 시술 후 냉각` |
| `categories[].complications[].evidence` | str | 38 | 0 | 0 | 29 | `https://www.goodrx.com/botox/botox-side-effects` · `https://www.goodrx.com/botox/botox-side-effects; h…` · `https://www.medicinenet.com/side_effects_of_botox_…` |
| `categories[].complications[].duration` | str | 19 | 0 | 0 | 19 | `1-3일 (자연 소실)` · `수년에 걸쳐 역가 감소 가능(중단 후 흔히 3-6년 이상 소요) — 완전 영구는 아님. 임…` · `수개월~영구적 (치료 필요)` |
| `categories[].complications[].risk_factors[]` | str | 92 | 0 | 0 | 85 | `이마/미간 부위 시술` · `다량 주입` · `긴장성 두통 병력` |

**enum 처럼 보이는 키** (문자열·3회 이상·distinct ≤ 10·반복 있음)

| 경로 | distinct 값 (횟수) |
|---|---|
| `categories[].complications[].severity` | `mild`(38), `moderate`(13), `severe`(11), `critical`(3) |

**식별자 후보** (레코드 배열별)

| 레코드 배열 | 건수 | 키 | 존재 | distinct | 유일 | 중복 예 |
|---|---|---|---|---|---|---|
| `categories` | 10 | `id` | 10 | 10 | ○ |  |
| `categories` | 10 | `name` | 10 | 10 | ○ |  |
| `categories[].complications` | 65 | `name` | 65 | 63 | ✗ | `감염`, `PIH (시술 후 과색소침착)` |

**일부 레코드에만 있는 키**

| 레코드 배열 | 건수 | 키=존재수 |
|---|---|---|
| `categories[].complications` | 65 | `evidence`=38, `duration`=19 |

**관찰** (원장 자체에서 보이는 것. 판정 아님)

- (기계) 빈값 46/46: `categories[].complications[].risk_factors`
- `version`/`updated` 메타가 없다(21개 중 taxonomy·extracted 와 함께 3개).
- 계열 10개만 다룬다(M4·M5·M6·M10·M12·M13·M17 없음).
- `risk_factors` 가 65건 중 46건은 빈 배열 `[]`, 19건만 채워짐(총 92개 문자열).
- `evidence`(38/65)·`duration`(19/65)은 일부 레코드에만 있다. `evidence` 는 URL 문자열이고 `;` 로 여러 개를 이어 붙인 경우가 있다.
- `incidence`·`onset` 은 자유 텍스트(`대부분 (일시적)`, `약 11-25% (부위·기법에 따라)`).
- 합병증 `name` 이 계열 사이에서 중복된다(`감염`, `PIH (시술 후 과색소침착)`). 같은 개념이 `홍반 (Erythema)` / `홍반 (Erythema / Redness)` / `홍반 (시술 직후 빨개짐)` 처럼 세 표기로도 나온다.

### 2.4 `consent-checklist.json` — 21,047B · 잎 키 8

계열 17개별 필수 고지·금기·응급 징후 문자열 배열

**최상위 구조**

- 메타 키: `version`=`1.3`, `updated`=`2026-07-26`, `description`=`시술별 필수 고지 항목. 법적 동의서 기반 mandatory disclosure, 금기사항…`
- 데이터 키: `categories` (list, 17)
- 배열: `categories`×1(len 17~17, 합 17), `categories[].mandatory_disclosures`×17(len 5~8, 합 109), `categories[].contraindications`×17(len 5~8, 합 105), `categories[].emergency_signs`×17(len 2~5, 합 55)

**잎 키 표**

| 경로 | 타입 | 횟수 | null | 빈값 | distinct | 예시 |
|---|---|---|---|---|---|---|
| `version` | str | 1 | 0 | 0 | 1 | `1.3` |
| `updated` | str | 1 | 0 | 0 | 1 | `2026-07-26` |
| `description` | str | 1 | 0 | 0 | 1 | `시술별 필수 고지 항목. 법적 동의서 기반 mandatory disclosure, 금기사항…` |
| `categories[].id` | str | 17 | 0 | 0 | 17 | `M1` · `M2` · `M3` |
| `categories[].name` | str | 17 | 0 | 0 | 17 | `보톡스` · `필러` · `바이오스티뮬레이터/콜라겐부스터` |
| `categories[].mandatory_disclosures[]` | str | 109 | 0 | 0 | 109 | `보톡스는 영구적이 아니며 3-6개월 후 효과가 소실됩니다` · `시술 후 일시적 멍, 부종, 두통이 발생할 수 있습니다` · `드물게 안검하수(눈꺼풀 처짐), 표정 비대칭이 발생할 수 있습니다` |
| `categories[].contraindications[]` | str | 105 | 0 | 0 | 70 | `임신 및 수유 중` · `신경근접합부 질환(중증근무력증 등)` · `보톡스 성분 과민반응 병력` |
| `categories[].emergency_signs[]` | str | 55 | 0 | 0 | 52 | `호흡 곤란` · `연하 곤란(삼키기 어려움)` · `심한 알레르기 반응(두드러기, 호흡곤란)` |

**enum 처럼 보이는 키** (문자열·3회 이상·distinct ≤ 10·반복 있음)

- 없음

**식별자 후보** (레코드 배열별)

| 레코드 배열 | 건수 | 키 | 존재 | distinct | 유일 | 중복 예 |
|---|---|---|---|---|---|---|
| `categories` | 17 | `id` | 17 | 17 | ○ |  |
| `categories` | 17 | `name` | 17 | 17 | ○ |  |

**관찰** (원장 자체에서 보이는 것. 판정 아님)

- 레코드당 문자열 배열 3개뿐이라 구조가 단순하다. 잎 키 8개.
- `contraindications[]` 105개 중 distinct 70 — `임신 및 수유 중` 15회, `켈로이드 체질` 6회 등 같은 문자열이 계열마다 반복된다. `시술 부위 활동성 감염` 과 `시술 부위 활동성 감염 또는 염증` 처럼 비슷한 문장이 따로 있다.
- `mandatory_disclosures[]` 109개는 전부 distinct.

### 2.5 `contraindications.json` — 6,390B · 잎 키 10

계열 쌍(from→to) 27개의 병행 금기/주의/간격 규칙

**최상위 구조**

- 메타 키: `version`=`1.1`, `updated`=`2026-07-11`, `description`=`시술 간 금기/주의사항/간격 매트릭스`
- 데이터 키: `rules` (list, 27)
- 배열: `rules`×1(len 27~27, 합 27)

**잎 키 표**

| 경로 | 타입 | 횟수 | null | 빈값 | distinct | 예시 |
|---|---|---|---|---|---|---|
| `version` | str | 1 | 0 | 0 | 1 | `1.1` |
| `updated` | str | 1 | 0 | 0 | 1 | `2026-07-11` |
| `description` | str | 1 | 0 | 0 | 1 | `시술 간 금기/주의사항/간격 매트릭스` |
| `rules[].from` | str | 27 | 0 | 0 | 9 | `M1` · `M2` · `M3` |
| `rules[].from_name` | str | 27 | 0 | 0 | 9 | `보톡스` · `필러` · `바이오스티뮬레이터/콜라겐부스터` |
| `rules[].to` | str | 27 | 0 | 0 | 7 | `M2` · `M7` · `M8` |
| `rules[].to_name` | str | 27 | 0 | 0 | 7 | `필러` · `실리프팅` · `레이저` |
| `rules[].level` | str | 27 | 0 | 0 | 3 | `safe` · `caution` · `warning` |
| `rules[].interval` | str | 27 | 0 | 0 | 12 | `같은 날 가능` · `2주 간격 권장` · `비박리·비박리 프락셔널: 같은 날 가능(레이저 먼저 → 보톡스 순서 권장) / 박리 CO2…` |
| `rules[].note` | str | 27 | 0 | 0 | 27 | `동일 부위는 보톡스 먼저 → 필러 순서 권장. 주입 부위가 다르면 순서 무관` · `보톡스가 안정화된 후 실리프팅. 동시 시술 시 보톡스 확산 위험` · `비박리·비박리 프락셔널 레이저와 보톡스의 같은 날 병행은 안전하며 레이저 후 냉각·부기를 …` |

**enum 처럼 보이는 키** (문자열·3회 이상·distinct ≤ 10·반복 있음)

| 경로 | distinct 값 (횟수) |
|---|---|
| `rules[].from` | `M1`(6), `M2`(5), `M7`(3), `M8`(3), `M6`(3), `M3`(2), `M4`(2), `M5`(2), `M9`(1) |
| `rules[].from_name` | `보톡스`(6), `필러`(5), `실리프팅`(3), `레이저`(3), `지방이식`(3), `바이오스티뮬레이터/콜라겐부스터`(2), `스킨부스터`(2), `PRP/자가혈`(2), `기기 리프팅`(1) |
| `rules[].to` | `M8`(7), `M9`(6), `M11`(5), `M12`(4), `M2`(2), `M7`(2), `M4`(1) |
| `rules[].to_name` | `레이저`(7), `기기 리프팅`(6), `니들RF`(5), `마이크로니들링(MTS)`(4), `필러`(2), `실리프팅`(2), `스킨부스터`(1) |
| `rules[].level` | `caution`(14), `safe`(8), `warning`(5) |

**식별자 후보** (레코드 배열별)

| 레코드 배열 | 건수 | 키 | 존재 | distinct | 유일 | 중복 예 |
|---|---|---|---|---|---|---|
| `rules` | 27 | `from` | 27 | 9 | ✗ | `M1`, `M2`, `M3`, `M4`, `M5`, `M7` |
| `rules` | 27 | `to` | 27 | 7 | ✗ | `M2`, `M7`, `M8`, `M9`, `M11`, `M12` |

**관찰** (원장 자체에서 보이는 것. 판정 아님)

- `from`/`to` 코드와 `from_name`/`to_name` 이름이 레코드마다 같이 들어 있다(코드-이름 중복 보관). 이름은 taxonomy 의 category 와 같다.
- `level` 은 caution 14 / safe 8 / warning 5 의 3값, `interval` 은 자유 텍스트 12종(`같은 날 가능`, `2주 간격 권장`).
- 쌍은 27개이며 한 방향만 있다(M1→M2 는 있고 M2→M1 은 없음). M10·M13~M17 은 등장하지 않는다.

### 2.6 `extracted.json` — 56,589B · 잎 키 24

계열 17개의 교과서 추출 요약(개요·기전·적응증·안전성·금기·관리). 최상위 키가 M 코드

**최상위 구조**

- 객체. 최상위 키가 전부 코드: M10, M11, M12, M13, M14, M15, M16, M17, M1, M2, M3, M4, M5, M6, M7, M8, M9
- 배열: `{code}.safety.common`×17(len 2~7, 합 59), `{code}.safety.uncommon`×17(len 1~5, 합 45), `{code}.aftercare`×17(len 2~5, 합 53), `{code}.indications.primary`×17(len 2~5, 합 56), `{code}.indications.extended`×17(len 3~19, 합 101), `{code}.contraindications.absolute`×17(len 2~4, 합 53), `{code}.contraindications.relative`×17(len 2~6, 합 55), `{code}.related_techniques`×17(len 2~4, 합 51), `{code}.safety.serious`×15(len 1~5, 합 37), `{code}.safety.emergency`×2(len 1~1, 합 2)

**잎 키 표**

| 경로 | 타입 | 횟수 | null | 빈값 | distinct | 예시 |
|---|---|---|---|---|---|---|
| `{code}.name` | str | 17 | 0 | 0 | 17 | `HIFES/EMS` · `니들RF` · `MTS (마이크로니들 치료)` |
| `{code}.safety.common[]` | str | 59 | 0 | 0 | 42 | `시술 부위 근육통 (운동 후와 비슷한 느낌)` · `일시적 근육 경련` · `시술 중 약간의 불편감` |
| `{code}.safety.serious` | null | 2 | 2 | 0 | 0 |  |
| `{code}.safety.uncommon[]` | str | 45 | 0 | 0 | 41 | `시술 부위 피부 발적 (빨개짐)` · `일시적 관절/건 불편감` · `색소침착 (박피나 레이저 시술에 비해 위험이 매우 작음)` |
| `{code}.source` | str | 17 | 0 | 0 | 13 | `일반 의학 지식` · `임상적 피부관리 28장 (인트라셀 Fractional RF Microneedle)` · `임상적 피부관리 22장` |
| `{code}.name_en` | str | 17 | 0 | 0 | 17 | `High-Intensity Focused Electromagnetic Stimulation…` · `Microneedle Radiofrequency (MNRF)` · `Microneedle Therapy System (Microneedling)` |
| `{code}.overview` | str | 17 | 0 | 0 | 17 | `HIFES(고강도 집속 전자기 자극)와 EMS(전기근육자극)는 전자기 에너지를 이용해 근육…` · `니들RF는 미세침(마이크로니들)을 피부에 삽입하면서 동시에 고주파(RF) 에너지를 전달하는…` · `MTS는 아주 가느다란 바늘이 많이 달린 롤러나 스탬프로 피부에 미세한 구멍을 내서, 피부…` |
| `{code}.aftercare[]` | str | 53 | 0 | 0 | 49 | `특별한 다운타임 없이 일상생활 바로 가능` · `충분한 수분 섭취` · `운동 병행 시 효과 극대화` |
| `{code}.mechanism` | str | 17 | 0 | 0 | 17 | `고강도 집속 전자기장(HIFEM)이 운동신경을 자극하여 단시간에 수만 회의 근육 초극대 수…` · `니들RF는 특수 제작된 절연 마이크로니들을 순간적으로 피부에 삽입하여 치료 기둥을 만들며,…` · `MTS 롤러의 미세한 바늘(0.2~2.0mm)이 피부 표피층과 진피층을 자극하면, 피부에 …` |
| `{code}.indications.primary[]` | str | 56 | 0 | 0 | 56 | `복부 근육 강화 및 지방 감소` · `엉덩이 리프팅 (힙업)` · `허벅지 근육 강화` |
| `{code}.indications.extended[]` | str | 101 | 0 | 0 | 97 | `팔뚝 근육 토닝` · `종아리 근육 강화` · `산후 복직근이개 (배 근육 벌어짐) 개선` |
| `{code}.source_type` | str | 17 | 0 | 0 | 3 | `general` · `kr` · `us` |
| `{code}.extracted_at` | str | 17 | 0 | 0 | 1 | `2026-03-28` |
| `{code}.procedure_id` | str | 17 | 0 | 0 | 17 | `M10-HIFES` · `M11-NEEDLERF` · `M12-MTS` |
| `{code}.onset_duration.peak` | str | 17 | 0 | 0 | 17 | `마지막 시술 후 2~4주 뒤` · `1~3개월 후 콜라겐 리모델링 효과 최대` · `3~6회 반복시술 후 최대 효과 (콜라겐 리모델링에 수주~수개월 소요)` |
| `{code}.onset_duration.onset` | str | 17 | 0 | 0 | 17 | `시술 직후 근육 피로감, 2~4주 후 근육 강화 체감` · `시술 후 1~2주부터 피부결 개선 체감` · `시술 후 1~2주부터 피부결 개선 느껴짐` |
| `{code}.onset_duration.duration` | str | 17 | 0 | 0 | 17 | `6~12개월 유지 (운동 병행 시 더 오래 유지)` · `6~12개월 유지 (반복 시술 시 효과 누적)` · `반복시술 시 피부가 점점 두꺼워지고 효과가 누적됨` |
| `{code}.contraindications.absolute[]` | str | 53 | 0 | 0 | 48 | `체내 금속 임플란트가 시술 부위에 있는 경우` · `심장박동기(페이스메이커) 또는 이식형 제세동기 사용자` · `임신 중인 경우` |
| `{code}.contraindications.relative[]` | str | 55 | 0 | 0 | 45 | `간질(뇌전증) 환자` · `심각한 심폐질환 환자` · `최근 수술 이력이 있는 부위` |
| `{code}.guardrail_version` | str | 17 | 0 | 0 | 1 | `1.0` |
| `{code}.related_techniques[]` | str | 51 | 0 | 0 | 49 | `크라이오리포라이시스 (냉동지방분해) -- 지방 감소에 병합` · `고주파(RF) 바디 -- 피부 타이트닝과 시너지` · `지방흡입 -- 더 적극적인 지방 제거가 필요한 경우` |
| `{code}.safety.serious[]` | str | 37 | 0 | 0 | 35 | `감염 (1회용 팁 사용으로 위생 관리)` · `드물게 화상 (부적절한 에너지 설정 시)` · `쾨브너현상 (건선 등 피부질환이 있는 환자에서 시술 부위에 병변이 새로 생기는 현상)` |
| `{code}.safety.emergency[]` | str | 2 | 0 | 0 | 2 | `주사 직후 피부가 하얗게 변하면 혈관이 막혔을 가능성 — 즉시 히알루로니다아제(분해효소) …` · `레이저 시술 중 피부가 심하게 하얗게 변하거나 검게 탄다면 즉시 시술 중단` |
| `{code}.updated` | str | 1 | 0 | 0 | 1 | `2026-07-11` |

**enum 처럼 보이는 키** (문자열·3회 이상·distinct ≤ 10·반복 있음)

| 경로 | distinct 값 (횟수) |
|---|---|
| `{code}.source_type` | `kr`(11), `general`(5), `us`(1) |
| `{code}.extracted_at` | `2026-03-28`(17) |
| `{code}.guardrail_version` | `1.0`(17) |

**식별자 후보** (레코드 배열별)

- 없음(식별자 키 없음)

**관찰** (원장 자체에서 보이는 것. 판정 아님)

- (기계) null 2/2: `{code}.safety.serious`
- 최상위가 M 코드 키 17개인 객체이고, 키 순서가 M10…M17, M1…M9 (문자열 정렬 순).
- 같은 내용이 `taxonomy.json` 의 `modality[].extracted` 에도 들어 있다. 17개 중 9개(M1·M4·M6·M7·M9·M11·M14·M15·M16)는 본문이 완전히 같고, 8개(M2·M3·M5·M8·M10·M12·M13·M17)는 일부 키 본문이 다르다(§3.9).
- `safety.serious` 가 M10·M13 은 `null`, 나머지 15개는 배열 — 같은 키에 타입이 섞인다. `safety.emergency` 는 2개에만 있다.
- `procedure_id` 는 `M1-BOTOX` 같은 영문 대문자 슬러그로 다른 파일 어디에도 안 나오는 식별자.
- `source` 는 교과서 장 번호 문자열(`임상적 피부관리 36장`) 또는 `일반 의학 지식`(5건). `source_type` 은 kr 11 / general 5 / us 1. `updated` 는 M3 하나에만 있다.
- `name` 표기가 taxonomy 의 category 와 다른 것: M3 `바이오스티뮬레이터`(taxonomy `바이오스티뮬레이터/콜라겐부스터`), M5 `PRP 피부재생술`(`PRP/자가혈`), M9 `기기리프팅`(`기기 리프팅`), M12 `MTS (마이크로니들 치료)`(`마이크로니들링(MTS)`).

### 2.7 `literature-evidence.json` — 118,979B · 잎 키 68

계열 17개별 문헌 근거 문장 119개(moa/adverse_effects/effects) + 인용(PMID/DOI) + 환자용 4개 국어 문장

**최상위 구조**

- 메타 키: `version`=`2.0`, `updated`=`2026-09-03`, `source_method`=`Curated successor of v1.0. Citation identity and m…`
- 데이터 키: `accuracy_summary` (dict, 8), `categories` (dict, 17)
- 동적 코드 키 객체 `accuracy_summary.by_category_average`: 7개 — M1, M2, M5, M12, M15, M16, M17
- 동적 코드 키 객체 `categories`: 17개 — M1, M2, M3, M4, M5, M6, M7, M8, M9, M10, M11, M12, M13, M14, M15, M16, M17
- 배열: `categories.{code}.moa`×11(len 1~8, 합 50), `categories.{code}.moa[].citations`×50(len 1~1, 합 50), `categories.{code}.adverse_effects`×11(len 1~6, 합 32), `categories.{code}.adverse_effects[].citations`×32(len 1~1, 합 32), `categories.{code}.effects`×9(len 1~8, 합 37), `categories.{code}.effects[].citations`×37(len 1~1, 합 37)

**잎 키 표**

| 경로 | 타입 | 횟수 | null | 빈값 | distinct | 예시 |
|---|---|---|---|---|---|---|
| `version` | str | 1 | 0 | 0 | 1 | `2.0` |
| `updated` | str | 1 | 0 | 0 | 1 | `2026-09-03` |
| `source_method` | str | 1 | 0 | 0 | 1 | `Curated successor of v1.0. Citation identity and m…` |
| `accuracy_summary.scored_by` | str | 1 | 0 | 0 | 1 | `Legacy content-quality scores retained for survivi…` |
| `accuracy_summary.rubric` | str | 1 | 0 | 0 | 1 | `95-100=교과서 consensus, 85-94=주류 표준, 70-84=뉘앙스 보정, 5…` |
| `accuracy_summary.overall_average` | float | 1 | 0 | 0 | 1 | `95.0` |
| `accuracy_summary.n_scored` | int | 1 | 0 | 0 | 1 | `17` |
| `accuracy_summary.by_field_average.moa` | float | 1 | 0 | 0 | 1 | `97.5` |
| `accuracy_summary.by_field_average.adverse_effects` | float | 1 | 0 | 0 | 1 | `95.0` |
| `accuracy_summary.by_field_average.effects` | float | 1 | 0 | 0 | 1 | `90.0` |
| `accuracy_summary.by_category_average.{code}` | float | 7 | 0 | 0 | 5 | `97.5` · `100.0` · `98.0` |
| `accuracy_summary.patient_ko_coverage` | str | 1 | 0 | 0 | 1 | `119/119` |
| `accuracy_summary.patient_translations_coverage.ko` | str | 1 | 0 | 0 | 1 | `119/119` |
| `accuracy_summary.patient_translations_coverage.en` | str | 1 | 0 | 0 | 1 | `119/119` |
| `accuracy_summary.patient_translations_coverage.zh` | str | 1 | 0 | 0 | 1 | `119/119` |
| `accuracy_summary.patient_translations_coverage.ja` | str | 1 | 0 | 0 | 1 | `119/119` |
| `categories.{code}.name` | str | 17 | 0 | 0 | 17 | `Botulinum toxin type A (aesthetic)` · `Hyaluronic acid dermal fillers` · `Collagen-stimulating biostimulators (PLLA/CaHA/PDL…` |
| `categories.{code}.moa[].statement` | str | 50 | 0 | 0 | 50 | `Botulinum toxin type A inhibits the secretion of a…` · `Botulinum toxin type A weakens skeletal muscles by…` · `Botulinum toxin type A paralyses muscles in the fa…` |
| `categories.{code}.moa[].citations[].authors` | str | 50 | 0 | 0 | 20 | `Park MY, Ahn KY` · `Fallacara A, Baldini E, Manfredini S, Vertuani S` · `Lipko-Godlewska S, Bolanča Ž, Kalinová L, Kermen I…` |
| `categories.{code}.moa[].citations[].title` | str | 50 | 0 | 0 | 20 | `Scientific review of the aesthetic uses of botulin…` · `Hyaluronic Acid in the Third Millennium.` · `Whole-Face Approach with Hyaluronic Acid Fillers.` |
| `categories.{code}.moa[].citations[].journal` | str | 50 | 0 | 0 | 18 | `Archives of craniofacial surgery` · `Polymers` · `Clinical, cosmetic and investigational dermatology` |
| `categories.{code}.moa[].citations[].year` | int | 50 | 0 | 0 | 8 | `2021` · `2018` · `2024` |
| `categories.{code}.moa[].citations[].pmid` | str | 50 | 0 | 0 | 20 | `33714246` · `30960626` · `33633459` |
| `categories.{code}.moa[].citations[].doi` | str | 48 | 0 | 0 | 19 | `10.7181/acfs.2021.00003` · `10.3390/polym10070701` · `10.2147/CCID.S292501` |
| `categories.{code}.moa[].citations[].pmc` | str | 49 | 0 | 0 | 19 | `PMC7968983` · `PMC6403654` · `PMC7901566` |
| `categories.{code}.moa[].citations[].oa_url` | str | 49 | 0 | 0 | 19 | `https://pmc.ncbi.nlm.nih.gov/articles/PMC7968983/` · `https://pmc.ncbi.nlm.nih.gov/articles/PMC6403654/` · `https://pmc.ncbi.nlm.nih.gov/articles/PMC7901566/` |
| `categories.{code}.moa[].accuracy_score` | int | 6 | 0 | 0 | 3 | `100` · `95` · `90` |
| `categories.{code}.moa[].accuracy_note` | str | 6 | 0 | 0 | 6 | `아세틸콜린 분비 억제는 보툴리눔 톡신의 핵심 기전임.` · `BDDE 등을 이용한 가교 결합은 유지 기간과 점탄성 조절의 핵심임.` · `PRP 내 성장인자들의 섬유아세포 증식 및 콜라겐 합성 유도 효과는 명확함.` |
| `categories.{code}.moa[].patient_ko` | str | 50 | 0 | 0 | 50 | `보툴리눔 톡신은 근육으로 가는 신경 신호 전달 물질이 나오는 것을 방해하여 근육의 움직임을…` · `보톡스는 신경과 근육 연결 부위에서 신호 전달 물질 방출을 막아 근육을 약하게 합니다.[1…` · `보툴리눔 독소 A는 얼굴 근육을 마비시켜 주름을 치료합니다.` |
| `categories.{code}.moa[].patient_en` | str | 50 | 0 | 0 | 50 | `Botulinum toxin stops nerve signals from reaching …` · `Botulinum toxin gently weakens muscle activity by …` · `Botulinum toxin addresses wrinkles by calming the …` |
| `categories.{code}.moa[].patient_zh` | str | 50 | 0 | 0 | 50 | `肉毒素通过阻断传递给肌肉的神经信号，帮助减少肌肉的过度运动。` · `肉毒素通过中断局部信号传递，温和地减弱肌肉的活动强度。` · `肉毒素通过平复引起皱纹的面部肌肉，达到改善线条的效果。` |
| `categories.{code}.moa[].patient_ja` | str | 50 | 0 | 0 | 50 | `ボツリヌストキシンが筋肉に届く神経の合図を遮断し、動きを和らげます。` · `ボツリヌストキシンが局所の伝달を遮断し、筋肉の動きを優しく和らげます。` · `ボツ리ヌストキシンがしわを作る表情筋を穏やかにして、しわをケアします。` |
| `categories.{code}.moa[].added_at` | str | 44 | 0 | 0 | 1 | `2026-04-19` |
| `categories.{code}.adverse_effects[].statement` | str | 32 | 0 | 0 | 32 | `Dry eye and diplopia have been reported following …` · `Botulinum toxin type A causes submandibular saliva…` · `Mesobotox with botulinum toxin type A induces part…` |
| `categories.{code}.adverse_effects[].citations[].authors` | str | 32 | 0 | 0 | 16 | `Witmanowski H, Błochowiak K` · `Park MY, Ahn KY` · `Lipko-Godlewska S, Bolanča Ž, Kalinová L, Kermen I…` |
| `categories.{code}.adverse_effects[].citations[].title` | str | 32 | 0 | 0 | 16 | `The whole truth about botulinum toxin - a review.` · `Scientific review of the aesthetic uses of botulin…` · `Whole-Face Approach with Hyaluronic Acid Fillers.` |
| `categories.{code}.adverse_effects[].citations[].journal` | str | 32 | 0 | 0 | 15 | `Postepy dermatologii i alergologii` · `Archives of craniofacial surgery` · `Clinical, cosmetic and investigational dermatology` |
| `categories.{code}.adverse_effects[].citations[].year` | int | 32 | 0 | 0 | 7 | `2020` · `2021` · `2024` |
| `categories.{code}.adverse_effects[].citations[].pmid` | str | 32 | 0 | 0 | 16 | `33603602` · `33714246` · `33633459` |
| `categories.{code}.adverse_effects[].citations[].doi` | str | 30 | 0 | 0 | 15 | `10.5114/ada.2019.82795` · `10.7181/acfs.2021.00003` · `10.2147/CCID.S292501` |
| `categories.{code}.adverse_effects[].citations[].pmc` | str | 29 | 0 | 0 | 14 | `PMC7874868` · `PMC7968983` · `PMC7901566` |
| `categories.{code}.adverse_effects[].citations[].oa_url` | str | 29 | 0 | 0 | 14 | `https://pmc.ncbi.nlm.nih.gov/articles/PMC7874868/` · `https://pmc.ncbi.nlm.nih.gov/articles/PMC7968983/` · `https://pmc.ncbi.nlm.nih.gov/articles/PMC7901566/` |
| `categories.{code}.adverse_effects[].accuracy_score` | int | 8 | 0 | 0 | 3 | `95` · `100` · `85` |
| `categories.{code}.adverse_effects[].accuracy_note` | str | 8 | 0 | 0 | 8 | `안구 주위 시술 후 안구 건조 및 복시 발생 가능성이 보고됨.` · `통증, 부기, 멍은 주사 시술에서 가장 빈번한 부작용임.` · `비자가 혈액 제제 사용 시 감염 전파 위험은 이론적, 실제적으로 존재함.` |
| `categories.{code}.adverse_effects[].patient_ko` | str | 32 | 0 | 0 | 32 | `눈 주변 시술 시 드물게 눈이 건조해지거나 사물이 겹쳐 보이는 증상이 나타날 수 있습니다.` · `A형 보툴리눔 독소는 턱 아래 침샘을 위축시킵니다.` · `메소보톡스(A형 보톡스)는 림프 배출을 부분적으로 줄입니다.` |
| `categories.{code}.adverse_effects[].patient_en` | str | 32 | 0 | 0 | 32 | `Temporary dry eyes or vision changes can happen if…` · `Botulinum toxin may cause the salivary glands unde…` · `Specific botulinum toxin techniques might affect t…` |
| `categories.{code}.adverse_effects[].patient_zh` | str | 32 | 0 | 0 | 32 | `如果成分扩散到邻近区域，可能会出现暂时的眼睛干涩或视觉变化。` · `肉毒素可能会引起下巴下方的唾液腺出现体积缩小的现象。` · `特定的肉毒素操作技术可能会影响皮肤水分的自然循环。` |
| `categories.{code}.adverse_effects[].patient_ja` | str | 32 | 0 | 0 | 32 | `成分が周囲に広がると、一時的な目の乾きや見え方の変化が起こります。` · `ボツリヌストキシンが、あごの下にある唾液腺を小さくさせることがあります。` · `特別なボツリヌストキシン法では、肌の水分排出に影響が出ることがあります。` |
| `categories.{code}.adverse_effects[].added_at` | str | 24 | 0 | 0 | 1 | `2026-04-19` |
| `categories.{code}.effects[].statement` | str | 37 | 0 | 0 | 37 | `Botulinum toxin type A eliminates facial wrinkles.` · `Botulinum toxin type A contours the lower face.` · `Botulinum toxin type A treats local hyperhidrosis.` |
| `categories.{code}.effects[].citations[].authors` | str | 37 | 0 | 0 | 15 | `Park MY, Ahn KY` · `Lipko-Godlewska S, Bolanča Ž, Kalinová L, Kermen I…` · `Wongprasert P, Dreiss CA, Murray G` |
| `categories.{code}.effects[].citations[].title` | str | 37 | 0 | 0 | 15 | `Scientific review of the aesthetic uses of botulin…` · `Whole-Face Approach with Hyaluronic Acid Fillers.` · `Evaluating hyaluronic acid dermal fillers: A criti…` |
| `categories.{code}.effects[].citations[].journal` | str | 37 | 0 | 0 | 14 | `Archives of craniofacial surgery` · `Clinical, cosmetic and investigational dermatology` · `Dermatologic therapy` |
| `categories.{code}.effects[].citations[].year` | int | 37 | 0 | 0 | 7 | `2021` · `2022` · `2024` |
| `categories.{code}.effects[].citations[].pmid` | str | 37 | 0 | 0 | 15 | `33714246` · `33633459` · `35293660` |
| `categories.{code}.effects[].citations[].doi` | str | 35 | 0 | 0 | 14 | `10.7181/acfs.2021.00003` · `10.2147/CCID.S292501` · `10.1111/dth.15453` |
| `categories.{code}.effects[].citations[].pmc` | str | 36 | 0 | 0 | 14 | `PMC7968983` · `PMC7901566` · `PMC9285697` |
| `categories.{code}.effects[].citations[].oa_url` | str | 36 | 0 | 0 | 14 | `https://pmc.ncbi.nlm.nih.gov/articles/PMC7968983/` · `https://pmc.ncbi.nlm.nih.gov/articles/PMC7901566/` · `https://pmc.ncbi.nlm.nih.gov/articles/PMC9285697/` |
| `categories.{code}.effects[].patient_ko` | str | 37 | 0 | 0 | 37 | `보톡스는 얼굴의 주름을 펴주는 주사예요.` · `A형 보툴리눔 독소가 하안면 윤곽을 다듬어줍니다.[2]` · `A형 보툴리눔 독소는 국소 다한증 치료에 사용됩니다.[1][2][3]` |
| `categories.{code}.effects[].patient_en` | str | 37 | 0 | 0 | 37 | `Botulinum toxin helps smooth the face by addressin…` · `Botulinum toxin is used to help shape and define t…` · `Botulinum toxin provides relief for areas that exp…` |
| `categories.{code}.effects[].patient_zh` | str | 37 | 0 | 0 | 37 | `肉毒素通过针对表情纹产生的原因，帮助您恢复面部的平滑。` · `肉毒素常被用于帮助塑造和美化下半面部的轮廓与线条。` · `肉毒素能为经常出现局部过度出汗的区域提供显著的缓解。` |
| `categories.{code}.effects[].patient_ja` | str | 37 | 0 | 0 | 37 | `ボツリヌストキシンが表情じわの原因に働き、お顔を滑らかに整えます。` · `ボツリヌストキシンを用いて、お顔の下半分の輪郭を美しく整えます。` · `ボツリヌストキシンが、局所の多すぎる汗を抑えて快適さを保ちます。` |
| `categories.{code}.effects[].added_at` | str | 34 | 0 | 0 | 1 | `2026-04-19` |
| `categories.{code}.effects` | list(empty) | 8 | 0 | 8 | 0 |  |
| `categories.{code}.effects[].accuracy_score` | int | 3 | 0 | 0 | 3 | `95` · `85` · `90` |
| `categories.{code}.effects[].accuracy_note` | str | 3 | 0 | 0 | 3 | `만성 상처 및 시술 후 상처 치유를 돕는 보조 요법으로 가치가 큼.` · `미백 목적의 글루타치온 주사는 FDA 승인 사항이 아니며 근거 수준에 논란이 있음.` · `미백 및 항노화 효과 측면에서는 바르는 비타민 C의 근거가 더 풍부함.` |
| `categories.{code}.moa` | list(empty) | 6 | 0 | 6 | 0 |  |
| `categories.{code}.adverse_effects` | list(empty) | 6 | 0 | 6 | 0 |  |

**enum 처럼 보이는 키** (문자열·3회 이상·distinct ≤ 10·반복 있음)

| 경로 | distinct 값 (횟수) |
|---|---|
| `categories.{code}.moa[].added_at` | `2026-04-19`(44) |
| `categories.{code}.adverse_effects[].added_at` | `2026-04-19`(24) |
| `categories.{code}.effects[].added_at` | `2026-04-19`(34) |

**식별자 후보** (레코드 배열별)

| 레코드 배열 | 건수 | 키 | 존재 | distinct | 유일 | 중복 예 |
|---|---|---|---|---|---|---|
| `categories.{code}.moa` | 50 | `statement` | 50 | 50 | ○ |  |
| `categories.{code}.moa[].citations` | 50 | `title` | 50 | 20 | ✗ | `Scientific review of the aesthetic uses of botulin…`, `Whole-Face Approach with Hyaluronic Acid Fillers.`, `MD Codes™: A Methodological Approach to Facial Aes…`, `A morphological analysis of calcium hydroxylapatit…`, `Injectable "Skin Boosters" in Aging Skin Rejuvenat…`, `The Science of Absorbable Poly(L-Lactide-Co-ε-Capr…` |
| `categories.{code}.moa[].citations` | 50 | `pmid` | 50 | 20 | ✗ | `33714246`, `33633459`, `32445044`, `38853456`, `39544509`, `33469333` |
| `categories.{code}.moa[].citations` | 50 | `doi` | 48 | 19 | ✗ | `10.7181/acfs.2021.00003`, `10.2147/CCID.S292501`, `10.1007/s00266-020-01762-7`, `10.1111/srt.13764`, `10.1055/a-2366-3436`, `10.2147/CCID.S274160` |
| `categories.{code}.adverse_effects` | 32 | `statement` | 32 | 32 | ○ |  |
| `categories.{code}.adverse_effects[].citations` | 32 | `title` | 32 | 16 | ✗ | `Scientific review of the aesthetic uses of botulin…`, `Whole-Face Approach with Hyaluronic Acid Fillers.`, `Injectable "Skin Boosters" in Aging Skin Rejuvenat…`, `A Review of Platelet-Rich Plasma: History, Biology…`, `The Science of Absorbable Poly(L-Lactide-Co-ε-Capr…`, `Picosecond Nd:YAG versus Fractional CO(2) Lasers i…` |
| `categories.{code}.adverse_effects[].citations` | 32 | `pmid` | 32 | 16 | ✗ | `33714246`, `33633459`, `39544509`, `29457008`, `33469333`, `38525494` |
| `categories.{code}.adverse_effects[].citations` | 32 | `doi` | 30 | 15 | ✗ | `10.7181/acfs.2021.00003`, `10.2147/CCID.S292501`, `10.1055/a-2366-3436`, `10.1159/000477353`, `10.2147/CCID.S274160`, `10.1097/GOX.0000000000005700` |
| `categories.{code}.effects` | 37 | `statement` | 37 | 37 | ○ |  |
| `categories.{code}.effects[].citations` | 37 | `title` | 37 | 15 | ✗ | `Scientific review of the aesthetic uses of botulin…`, `Whole-Face Approach with Hyaluronic Acid Fillers.`, `MD Codes™: A Methodological Approach to Facial Aes…`, `Injectable "Skin Boosters" in Aging Skin Rejuvenat…`, `The Science of Absorbable Poly(L-Lactide-Co-ε-Capr…`, `Picosecond Nd:YAG versus Fractional CO(2) Lasers i…` |
| `categories.{code}.effects[].citations` | 37 | `pmid` | 37 | 15 | ✗ | `33714246`, `33633459`, `32445044`, `39544509`, `33469333`, `38525494` |
| `categories.{code}.effects[].citations` | 37 | `doi` | 35 | 14 | ✗ | `10.7181/acfs.2021.00003`, `10.2147/CCID.S292501`, `10.1007/s00266-020-01762-7`, `10.1055/a-2366-3436`, `10.2147/CCID.S274160`, `10.1097/GOX.0000000000005700` |

**일부 레코드에만 있는 키**

| 레코드 배열 | 건수 | 키=존재수 |
|---|---|---|
| `categories.{code}.moa` | 50 | `accuracy_score`=6, `accuracy_note`=6, `added_at`=44 |
| `categories.{code}.moa[].citations` | 50 | `doi`=48, `pmc`=49, `oa_url`=49 |
| `categories.{code}.adverse_effects` | 32 | `accuracy_score`=8, `accuracy_note`=8, `added_at`=24 |
| `categories.{code}.adverse_effects[].citations` | 32 | `doi`=30, `pmc`=29, `oa_url`=29 |
| `categories.{code}.effects` | 37 | `added_at`=34, `accuracy_score`=3, `accuracy_note`=3 |
| `categories.{code}.effects[].citations` | 37 | `doi`=35, `pmc`=36, `oa_url`=36 |

**관찰** (원장 자체에서 보이는 것. 판정 아님)

- (기계) 빈값 8/8: `categories.{code}.effects`
- (기계) 빈값 6/6: `categories.{code}.moa`
- (기계) 빈값 6/6: `categories.{code}.adverse_effects`
- (기계) 식별자 중복 (`categories.{code}.moa[].citations`.pmid): ['33714246', '33633459', '32445044', '38853456', '39544509', '33469333', '32273965', '38525494', '37753689', '27559496']
- (기계) 식별자 중복 (`categories.{code}.adverse_effects[].citations`.pmid): ['33714246', '33633459', '39544509', '29457008', '33469333', '38525494', '28796657', '33584968']
- (기계) 식별자 중복 (`categories.{code}.effects[].citations`.pmid): ['33714246', '33633459', '32445044', '39544509', '33469333', '38525494', '27559496', '33584968']
- `categories` 는 M 코드 키 객체(17개)이지만 섹션이 비어 있는 계열이 많다 — moa 빈 곳 6(M6·M10·M11·M13·M14·M17), adverse_effects 빈 곳 6(M6·M9·M10·M11·M13·M14), effects 빈 곳 8(M3·M6·M10·M11·M13·M14·M15·M17). M6·M10·M11·M13·M14 는 세 섹션 전부 빈 배열.
- `accuracy_score`/`accuracy_note` 는 119개 문장 중 17개에만 있다(moa 6, ae 8, effects 3). `added_at` 은 102개에 있고 값은 전부 `2026-04-19` 하나.
- `citations[]` 는 문장마다 정확히 1개이고, 같은 논문(PMID 33714246 등)이 여러 문장에 반복된다 — 인용 20종이 119회. `doi`(113/119)·`pmc`(114)·`oa_url`(114)은 일부 빠짐.
- `patient_ko` 41개에 `[1][2]` 같은 각주 번호가 본문에 남아 있다. `patient_ja` 5건과 `patient_en` 1건에 한글 글자가 섞여 있다(예: `局所の伝달を`, `ボツ리ヌス`, `狙い通리의`).
- `name` 은 영문 학술 명칭(`Botulinum toxin type A (aesthetic)`)으로, 다른 파일의 한글 계열명과 다르다.
- `accuracy_summary.by_category_average` 는 7개 계열만 있고, `patient_translations_coverage` 는 `119/119` 문자열.

### 2.8 `market-pricing.json` — 12,214B · 잎 키 11

계열 17개별 시장 가격 항목 122개(low/mid/high, KRW, 단위 문자열)

**최상위 구조**

- 메타 키: `version`=`1.1`, `updated`=`2026-07-26`, `currency`=`KRW`, `note`=`한국 시장 참고 가격 범위. 클리닉/지역/의사에 따라 상이. 정가 아닌 시장 범위.`
- 데이터 키: `categories` (list, 17)
- 배열: `categories`×1(len 17~17, 합 17), `categories[].items`×17(len 6~10, 합 122)

**잎 키 표**

| 경로 | 타입 | 횟수 | null | 빈값 | distinct | 예시 |
|---|---|---|---|---|---|---|
| `version` | str | 1 | 0 | 0 | 1 | `1.1` |
| `updated` | str | 1 | 0 | 0 | 1 | `2026-07-26` |
| `currency` | str | 1 | 0 | 0 | 1 | `KRW` |
| `note` | str | 1 | 0 | 0 | 1 | `한국 시장 참고 가격 범위. 클리닉/지역/의사에 따라 상이. 정가 아닌 시장 범위.` |
| `categories[].id` | str | 17 | 0 | 0 | 17 | `M1` · `M2` · `M3` |
| `categories[].name` | str | 17 | 0 | 0 | 17 | `보톡스` · `필러` · `바이오스티뮬레이터/콜라겐부스터` |
| `categories[].items[].name` | str | 122 | 0 | 0 | 122 | `이마 주름 (수입)` · `이마 주름 (국산)` · `미간 주름 (수입)` |
| `categories[].items[].unit` | str | 122 | 0 | 0 | 17 | `1회` · `1cc` · `2cc` |
| `categories[].items[].low` | int | 122 | 0 | 0 | 22 | `50000` · `30000` · `40000` |
| `categories[].items[].mid` | int | 122 | 0 | 0 | 26 | `100000` · `60000` · `80000` |
| `categories[].items[].high` | int | 122 | 0 | 0 | 30 | `200000` · `100000` · `150000` |

**enum 처럼 보이는 키** (문자열·3회 이상·distinct ≤ 10·반복 있음)

- 없음

**식별자 후보** (레코드 배열별)

| 레코드 배열 | 건수 | 키 | 존재 | distinct | 유일 | 중복 예 |
|---|---|---|---|---|---|---|
| `categories` | 17 | `id` | 17 | 17 | ○ |  |
| `categories` | 17 | `name` | 17 | 17 | ○ |  |
| `categories[].items` | 122 | `name` | 122 | 122 | ○ |  |

**관찰** (원장 자체에서 보이는 것. 판정 아님)

- `unit` 이 17종 자유 문자열(`1회` 87, `1cc`, `2cc`, `1바이알`, `900샷`, `10줄`, `양쪽`, `부위/1회` …).
- `items[].name` 에 제품·부위·국산/수입 구분이 괄호로 들어간다(`이마 주름 (수입)`, `울쎄라 (풀페이스)`, `리쥬란 힐러 (2cc)`). 122개 전부 distinct 이고 taxonomy 항목과 직접 연결되는 코드는 없다.
- low ≤ mid ≤ high 위반 0건. 값은 KRW 정수.
- M9 의 `name` 이 `에너지기기(HIFU/RF)` 로 taxonomy `기기 리프팅` 과 다르다(procedure-profiles 도 같은 표기). M5 는 `PRP/엑소좀`(taxonomy `PRP/자가혈`).

### 2.9 `patient-education.json` — 26,551B · 잎 키 12

계열 17개별 환자 설명(쉬운 설명·원리·지속·통증·다운타임) + Q&A 51개

**최상위 구조**

- 메타 키: `version`=`1.3`, `updated`=`2026-07-26`
- 데이터 키: `categories` (list, 17)
- 배열: `categories`×1(len 17~17, 합 17), `categories[].common_concerns`×17(len 3~3, 합 51)

**잎 키 표**

| 경로 | 타입 | 횟수 | null | 빈값 | distinct | 예시 |
|---|---|---|---|---|---|---|
| `version` | str | 1 | 0 | 0 | 1 | `1.3` |
| `updated` | str | 1 | 0 | 0 | 1 | `2026-07-26` |
| `categories[].id` | str | 17 | 0 | 0 | 17 | `M1` · `M2` · `M3` |
| `categories[].name` | str | 17 | 0 | 0 | 17 | `보톡스` · `필러` · `바이오스티뮬레이터/콜라겐부스터` |
| `categories[].patient_name` | str | 17 | 0 | 0 | 17 | `주름 보톡스` · `볼륨 필러` · `콜라겐 재생 주사` |
| `categories[].simple_explanation` | str | 17 | 0 | 0 | 17 | `근육을 일시적으로 쉬게 해서 주름을 펴는 주사입니다.` · `피부 아래에 젤 형태의 물질을 넣어서 꺼진 부위를 채우거나 윤곽을 잡아주는 주사입니다.` · `피부 속에서 콜라겐(피부 탄력 성분)이 스스로 만들어지도록 돕는 주사입니다.` |
| `categories[].how_it_works` | str | 17 | 0 | 0 | 17 | `주름을 만드는 근육에 약을 주사하면 근육이 쉬면서 주름이 펴집니다. 칼로 자르거나 꿰매지 …` · `우리 피부에 원래 있는 히알루론산(수분을 잡아주는 성분)과 비슷한 젤을 주사로 넣어서 볼륨…` · `특수 성분을 피부 아래에 주사하면, 우리 몸이 그 주변에 새로운 콜라겐을 만들어냅니다. 당…` |
| `categories[].duration_simple` | str | 17 | 0 | 0 | 16 | `약 3-6개월 지속됩니다.` · `약 6-18개월 지속됩니다 (제품과 부위에 따라 다름).` · `효과 발현까지 4-6주, 지속 기간은 1-3년입니다.` |
| `categories[].pain_level` | str | 17 | 0 | 0 | 17 | `모기 물린 정도의 따끔함` · `마취 크림을 바르고 시술하여 약간의 압박감 정도` · `주사 시 약간의 통증, 마취 크림 사용 가능` |
| `categories[].downtime` | str | 17 | 0 | 0 | 16 | `바로 일상 복귀 가능` · `가벼운 붓기가 2-3일, 멍이 들 수 있으나 일상생활 가능` · `가벼운 붓기 2-3일, 일상생활 가능` |
| `categories[].common_concerns[].q` | str | 51 | 0 | 0 | 51 | `보톡스 맞으면 표정이 굳나요?` · `보톡스에 중독되나요?` · `보톡스 맞고 바로 운동해도 되나요?` |
| `categories[].common_concerns[].a` | str | 51 | 0 | 0 | 51 | `적절한 양을 맞으면 자연스러운 표정을 유지할 수 있어요. 과도하게 맞는 경우에만 표정이 어…` · `의학적으로 중독성은 없어요. 효과가 빠지면 원래 상태로 돌아갑니다.` · `가벼운 활동은 바로 가능하고, 격한 운동·사우나·음주는 시술 당일(대략 24시간) 삼가는 …` |

**enum 처럼 보이는 키** (문자열·3회 이상·distinct ≤ 10·반복 있음)

- 없음

**식별자 후보** (레코드 배열별)

| 레코드 배열 | 건수 | 키 | 존재 | distinct | 유일 | 중복 예 |
|---|---|---|---|---|---|---|
| `categories` | 17 | `id` | 17 | 17 | ○ |  |
| `categories` | 17 | `name` | 17 | 17 | ○ |  |

**관찰** (원장 자체에서 보이는 것. 판정 아님)

- 계열 17개 전부 있고 잎 키 12개. 모든 값이 자유 텍스트 문장.
- `patient_name` 은 환자용 별칭(`주름 보톡스`, `볼륨 필러`, `실 리프팅 (얼굴 당김 시술)`) — 계열명의 또 다른 표기.
- `duration_simple`·`downtime` 은 17건 중 distinct 16 (같은 문장이 두 계열에).

### 2.10 `pih-risk.json` — 11,875B · 잎 키 18

에너지/필링 계열 세부 시술 26개의 PIH 위험도·발생률·위험인자·예방. procedure_ref 로 taxonomy 하위 id 참조

**최상위 구조**

- 메타 키: `version`=`1.0`, `updated`=`2026-04-05`, `description`=`시술별 PIH(Post-Inflammatory Hyperpigmentation) 위험도. …`
- 데이터 키: `risk_levels` (dict, 5), `notes` (dict, 4), `procedures` (list, 26)
- 동적 코드 키 객체 `notes`: 4개 — M1_to_M7, M10, M16, M17
- 배열: `procedures`×1(len 26~26, 합 26), `procedures[].risk_factors`×26(len 1~5, 합 68)

**잎 키 표**

| 경로 | 타입 | 횟수 | null | 빈값 | distinct | 예시 |
|---|---|---|---|---|---|---|
| `version` | str | 1 | 0 | 0 | 1 | `1.0` |
| `updated` | str | 1 | 0 | 0 | 1 | `2026-04-05` |
| `description` | str | 1 | 0 | 0 | 1 | `시술별 PIH(Post-Inflammatory Hyperpigmentation) 위험도. …` |
| `risk_levels.very_low` | str | 1 | 0 | 0 | 1 | `< 1%` |
| `risk_levels.low` | str | 1 | 0 | 0 | 1 | `1-5%` |
| `risk_levels.moderate` | str | 1 | 0 | 0 | 1 | `5-15%` |
| `risk_levels.high` | str | 1 | 0 | 0 | 1 | `15-30%` |
| `risk_levels.very_high` | str | 1 | 0 | 0 | 1 | `> 30%` |
| `notes.{code}` | str | 4 | 0 | 0 | 4 | `주사 시술(M1 보톡스, M2 필러, M3 바이오스티뮬레이터, M4 스킨부스터, M5 PR…` · `HIFES/EMS는 피부 표면에 작용하지 않으므로 PIH 해당 없음` · `수액치료는 정맥주사이므로 PIH 해당 없음` |
| `procedures[].category` | str | 26 | 0 | 0 | 6 | `M8` · `M9` · `M11` |
| `procedures[].subcategory` | str | 26 | 0 | 0 | 12 | `색소/토닝` · `프락셔널` · `IPL` |
| `procedures[].name` | str | 26 | 0 | 0 | 26 | `레이저 토닝 (QS Nd:YAG 1064nm 저에너지)` · `QS Nd:YAG 1064nm (표준 에너지, 색소 치료)` · `피코토닝 (피코초 Nd:YAG 1064nm)` |
| `procedures[].procedure_ref` | str | 26 | 0 | 0 | 22 | `M8-1-1` · `M8-1-2` · `M8-1-3` |
| `procedures[].pih_risk` | str | 26 | 0 | 0 | 5 | `low` · `moderate` · `very_high` |
| `procedures[].pih_rate` | str | 26 | 0 | 0 | 12 | `~5%` · `~10%` · `1-3%` |
| `procedures[].fitzpatrick_note` | str | 26 | 0 | 0 | 26 | `III-IV에서도 비교적 안전. 저에너지 반복 조사로 멜라닌 점진적 제거` · `III-IV에서 표준 에너지 사용 시 PIH 위험 증가` · `피코초 펄스로 열손상 최소화, QS 대비 PIH 낮음` |
| `procedures[].risk_factors[]` | str | 68 | 0 | 0 | 36 | `과도한 fluence` · `짧은 시술 간격(2주 미만)` · `불충분한 자외선 차단` |
| `procedures[].prevention` | str | 26 | 0 | 0 | 26 | `시술 간격 2-4주 유지, SPF 50+ 자외선 차단, 저에너지 유지` · `테스트 샷 시행, 적정 fluence 설정, SPF 50+ 자외선 차단 4주 이상` · `적정 에너지 유지, 시술 간격 2-4주` |

**enum 처럼 보이는 키** (문자열·3회 이상·distinct ≤ 10·반복 있음)

| 경로 | distinct 값 (횟수) |
|---|---|
| `procedures[].category` | `M8`(15), `M9`(3), `M15`(3), `M11`(2), `M13`(2), `M12`(1) |
| `procedures[].pih_risk` | `low`(14), `moderate`(5), `very_low`(4), `high`(2), `very_high`(1) |

**식별자 후보** (레코드 배열별)

| 레코드 배열 | 건수 | 키 | 존재 | distinct | 유일 | 중복 예 |
|---|---|---|---|---|---|---|
| `procedures` | 26 | `category` | 26 | 6 | ✗ | `M8`, `M9`, `M11`, `M13`, `M15` |
| `procedures` | 26 | `name` | 26 | 26 | ○ |  |

**관찰** (원장 자체에서 보이는 것. 판정 아님)

- `procedure_ref` 가 taxonomy 하위 id 를 가리키는데 깊이가 섞여 있다 — 항목(M8-1-1 등) 16건, 하위분류(M8-5, M9-1, M9-2, M11-1, M15-1) 7건, 계열(M12, M13) 3건. 22 distinct / 26 — `M8-1-1`, `M8-5`, `M11-1`, `M13` 이 각각 2건에 쓰였다.
- `procedure_ref` 가 taxonomy 항목과 이름이 어긋나는 것: `M8-5-3` 은 pih 에서 `알렉산드라이트 제모 (755nm LP)`, taxonomy 에서는 `젠틀맥스프로+`.
- `notes` 객체의 키가 `M1_to_M7`, `M10`, `M16`, `M17` — 범위 표기 키와 단일 코드 키가 섞여 있다.
- `pih_risk` 5값은 `risk_levels` 정의 키와 정확히 일치. `pih_rate` 는 `~5%` 같은 자유 텍스트.
- `subcategory` 는 한글 라벨(`색소/토닝`, `프락셔널`) 12종으로 taxonomy subcategory label 과 같은지 코드로는 확인되지 않는다(코드 없음).

### 2.11 `post-procedure-timeline.json` — 20,081B · 잎 키 16

시술 10종의 시술 후 경과(phases: Day 구간별 정상/이상/주의/응급 증상 배열)

**최상위 구조**

- 메타 키: `version`=`1.1`, `updated`=`2026-07-11`, `consensus_method`=`Perplexity(리서치) + Gemini(분석) + Claude(교과서 종합) 3-AI…`
- 데이터 키: `reaction_levels` (dict, 4), `timelines` (list, 10)
- 배열: `timelines`×1(len 10~10, 합 10), `timelines[].phases`×10(len 3~5, 합 43), `timelines[].phases[].normal`×43(len 3~4, 합 162), `timelines[].phases[].abnormal`×43(len 1~3, 합 86), `timelines[].phases[].caution`×43(len 1~3, 합 93), `timelines[].phases[].emergency`×43(len 1~4, 합 94)

**잎 키 표**

| 경로 | 타입 | 횟수 | null | 빈값 | distinct | 예시 |
|---|---|---|---|---|---|---|
| `version` | str | 1 | 0 | 0 | 1 | `1.1` |
| `updated` | str | 1 | 0 | 0 | 1 | `2026-07-11` |
| `consensus_method` | str | 1 | 0 | 0 | 1 | `Perplexity(리서치) + Gemini(분석) + Claude(교과서 종합) 3-AI…` |
| `reaction_levels.normal` | str | 1 | 0 | 0 | 1 | `정상 반응 -- 예상 범위, 조치 불필요` |
| `reaction_levels.abnormal` | str | 1 | 0 | 0 | 1 | `이상 반응 -- 모니터링 필요, 경과 관찰` |
| `reaction_levels.caution` | str | 1 | 0 | 0 | 1 | `주의 반응 -- 24-48시간 내 클리닉 연락` |
| `reaction_levels.emergency` | str | 1 | 0 | 0 | 1 | `응급 반응 -- 즉시 응급실/클리닉` |
| `timelines[].id` | str | 10 | 0 | 0 | 10 | `botox` · `ha-filler` · `hifu-rf` |
| `timelines[].category` | str | 10 | 0 | 0 | 10 | `M1` · `M2` · `M9` |
| `timelines[].name` | str | 10 | 0 | 0 | 10 | `보톡스` · `HA 필러` · `HIFU/RF 리프팅` |
| `timelines[].phases[].period` | str | 43 | 0 | 0 | 12 | `Day 0` · `Day 1-3` · `Day 3-7` |
| `timelines[].phases[].label` | str | 43 | 0 | 0 | 24 | `시술 당일` · `초기 경과` · `효과 발현기` |
| `timelines[].phases[].normal[]` | str | 162 | 0 | 0 | 153 | `주사 부위 작은 돌기/발적 (15-60분 내 소실)` · `약간의 따끔함/화끈감` · `주사 부위 경미한 압통` |
| `timelines[].phases[].abnormal[]` | str | 86 | 0 | 0 | 83 | `경미한 멍 (혈관 천자 시)` · `멍 (수일 내 소실, 보라색→황색 변화)` · `경미한 두통 (수시간 내 소실)` |
| `timelines[].phases[].caution[]` | str | 93 | 0 | 0 | 85 | `1시간 이상 지속되는 발적/부종` · `지속되는 심한 두통 (24시간 이상)` · `비대칭 느낌 (근육 반응 차이)` |
| `timelines[].phases[].emergency[]` | str | 94 | 0 | 0 | 84 | `심한 두드러기/호흡곤란 (아나필락시스, 극히 드묾)` · `심한 전신 발진/혈관부종` · `시야 변화/복시` |

**enum 처럼 보이는 키** (문자열·3회 이상·distinct ≤ 10·반복 있음)

- 없음

**식별자 후보** (레코드 배열별)

| 레코드 배열 | 건수 | 키 | 존재 | distinct | 유일 | 중복 예 |
|---|---|---|---|---|---|---|
| `timelines` | 10 | `id` | 10 | 10 | ○ |  |
| `timelines` | 10 | `category` | 10 | 10 | ○ |  |
| `timelines` | 10 | `name` | 10 | 10 | ○ |  |
| `timelines[].phases` | 43 | `label` | 43 | 24 | ✗ | `시술 당일`, `효과 발현기`, `최종 평가기`, `부종 피크기`, `회복기`, `안정기` |

**관찰** (원장 자체에서 보이는 것. 판정 아님)

- `timelines[].id` 는 영문 슬러그(botox, ha-filler, hifu-rf …), `category` 는 M 코드 — 단 `dca-injection` 의 category 는 `M16-DCA` 로 코드+하위 라벨 합성값.
- `name` 이 계열명이 아니라 시술명(`HA 필러`, `HIFU/RF 리프팅`, `프락셔널 CO2 레이저`, `케미컬 필링 (중간 깊이)`)이다.
- `phases[].period` 는 `Day 0`, `Day 1-3`, `Day 7-30` 등 12종 문자열이고 구간이 시술마다 다르다. `label` 24종(`시술 당일`, `부종 피크기` …).
- phase 의 증상 키 4개(normal/abnormal/caution/emergency)는 `reaction_levels` 정의와 일치.

### 2.12 `pre-procedure-checklist.json` — 14,569B · 잎 키 11

공통 체크 12개 + 계열 17개별 시술 전 확인 항목 123개(label/type)

**최상위 구조**

- 메타 키: `version`=`1.1`, `updated`=`2026-04-05`, `description`=`시술 전 체크리스트. 카테고리별 universal + category-specific 확인…`
- 데이터 키: `universal_checks` (list, 12), `category_specific` (list, 17)
- 배열: `universal_checks`×1(len 12~12, 합 12), `category_specific`×1(len 17~17, 합 17), `category_specific[].checks`×17(len 5~11, 합 123)

**잎 키 표**

| 경로 | 타입 | 횟수 | null | 빈값 | distinct | 예시 |
|---|---|---|---|---|---|---|
| `version` | str | 1 | 0 | 0 | 1 | `1.1` |
| `updated` | str | 1 | 0 | 0 | 1 | `2026-04-05` |
| `description` | str | 1 | 0 | 0 | 1 | `시술 전 체크리스트. 카테고리별 universal + category-specific 확인…` |
| `universal_checks[].id` | str | 12 | 0 | 0 | 12 | `allergies` · `anticoagulants` · `autoimmune` |
| `universal_checks[].label` | str | 12 | 0 | 0 | 12 | `알레르기 병력` · `항응고제/항혈소판제` · `자가면역질환` |
| `universal_checks[].type` | str | 12 | 0 | 0 | 5 | `must_check` · `relative_contraindication` · `counseling` |
| `universal_checks[].description` | str | 12 | 0 | 0 | 12 | `약물/식품/라텍스 알레르기` · `아스피린, 와파린, NOAC, 오메가3, 은행잎 추출물 등 — 멍/출혈 위험 안내. 중단 …` · `루푸스, 류마티스, 경피증 등 — 시술 반응 예측 어려움, 이물반응/상처 회복 지연 위험 …` |
| `category_specific[].id` | str | 17 | 0 | 0 | 17 | `M1` · `M2` · `M3` |
| `category_specific[].name` | str | 17 | 0 | 0 | 17 | `보톡스` · `필러` · `바이오스티뮬레이터/콜라겐부스터` |
| `category_specific[].checks[].label` | str | 123 | 0 | 0 | 112 | `신경근접합부 질환(중증근무력증 등) 확인` · `이전 보툴리눔 독소 시술 후 이상반응 여부` · `항응고제 복용 여부 (멍 위험 안내)` |
| `category_specific[].checks[].type` | str | 123 | 0 | 0 | 5 | `absolute_contraindication` · `must_check` · `inform` |

**enum 처럼 보이는 키** (문자열·3회 이상·distinct ≤ 10·반복 있음)

| 경로 | distinct 값 (횟수) |
|---|---|
| `universal_checks[].type` | `must_check`(8), `relative_contraindication`(1), `counseling`(1), `inform`(1), `absolute_contraindication`(1) |
| `category_specific[].checks[].type` | `must_check`(66), `absolute_contraindication`(21), `counseling`(21), `inform`(10), `safety_protocol`(5) |

**식별자 후보** (레코드 배열별)

| 레코드 배열 | 건수 | 키 | 존재 | distinct | 유일 | 중복 예 |
|---|---|---|---|---|---|---|
| `universal_checks` | 12 | `id` | 12 | 12 | ○ |  |
| `universal_checks` | 12 | `label` | 12 | 12 | ○ |  |
| `category_specific` | 17 | `id` | 17 | 17 | ○ |  |
| `category_specific` | 17 | `name` | 17 | 17 | ○ |  |
| `category_specific[].checks` | 123 | `label` | 123 | 112 | ✗ | `켈로이드 체질 확인`, `항응고제/항혈소판제 복용 여부`, `활동성 감염/패혈증 여부`, `자가면역질환 여부`, `시술 부위 활동성 감염 여부`, `이소트레티노인 복용 여부/중단 시점 확인 — 프락셔널/얕은 필링 6개월, 박리성 레이저 1…` |

**관찰** (원장 자체에서 보이는 것. 판정 아님)

- `universal_checks[]` 에는 `id`(영문)가 있지만 `category_specific[].checks[]` 에는 id 가 없고 `label`+`type` 뿐이다.
- `type` 은 두 곳 합쳐 6종(must_check, absolute_contraindication, relative_contraindication, counseling, inform, safety_protocol). universal 과 category_specific 이 쓰는 집합이 다르다.
- `checks[].label` 123개 중 distinct 112 — `켈로이드 체질 확인`, `항응고제/항혈소판제 복용 여부` 등이 여러 계열에 반복. `자가면역질환 여부` / `자가면역질환 여부 (육아종 위험)` / `(이물반응 위험)` 처럼 괄호 보충으로 갈라진 표기.

### 2.13 `problem-combos.json` — 25,026B · 잎 키 18

고민(P) 8개별 상담용 패키지 24개: tier·제품·가격대·세일즈 멘트·임상 근거

**최상위 구조**

- 메타 키: `version`=`1.2`, `updated`=`2026-07-26`, `description`=`Problem별 추천 조합 — 상담 안내와 의료진 참고 정보 통합`
- 데이터 키: `combos` (list, 8)
- 배열: `combos`×1(len 8~8, 합 8), `combos[].packages`×8(len 2~4, 합 24), `combos[].packages[].procedures`×24(len 1~5, 합 63), `combos[].packages[].products`×24(len 1~1, 합 24)

**잎 키 표**

| 경로 | 타입 | 횟수 | null | 빈값 | distinct | 예시 |
|---|---|---|---|---|---|---|
| `version` | str | 1 | 0 | 0 | 1 | `1.2` |
| `updated` | str | 1 | 0 | 0 | 1 | `2026-07-26` |
| `description` | str | 1 | 0 | 0 | 1 | `Problem별 추천 조합 — 상담 안내와 의료진 참고 정보 통합` |
| `combos[].problem_id` | str | 8 | 0 | 0 | 8 | `P1` · `P2` · `P3` |
| `combos[].problem` | str | 8 | 0 | 0 | 8 | `쁘띠시술` · `주름` · `처짐/탄력` |
| `combos[].packages[].id` | str | 24 | 0 | 0 | 24 | `P1-1` · `P1-2` · `P1-3` |
| `combos[].packages[].tier` | str | 24 | 0 | 0 | 4 | `entry` · `recommended` · `premium` |
| `combos[].packages[].tierLabel` | str | 24 | 0 | 0 | 4 | `기본` · `표준` · `확장` |
| `combos[].packages[].name` | str | 24 | 0 | 0 | 24 | `보톡스 단독` · `보톡스 + 필러` · `수입 보톡스 + 수입 필러 + 스킨부스터` |
| `combos[].packages[].procedures[]` | str | 63 | 0 | 0 | 9 | `M1` · `M2` · `M4` |
| `combos[].packages[].productTier` | str | 24 | 0 | 0 | 7 | `국산` · `국산+수입 혼합` · `수입` |
| `combos[].packages[].products[]` | str | 24 | 0 | 0 | 23 | `나보타 or 보툴렉스` · `나보타 + 쥬비덤 or 이브아르` · `보톡스(엘러간) + 쥬비덤 + 리쥬란` |
| `combos[].packages[].priceRange` | str | 24 | 0 | 0 | 22 | `5~8만` · `25~45만` · `60~100만` |
| `combos[].packages[].expectedResult` | str | 24 | 0 | 0 | 24 | `이마·미간·눈가 주름 개선. 시술 10분, 바로 일상 복귀` · `주름 개선 + 볼륨 복원. 동적주름(보톡스) + 정적주름·볼륨(필러) 동시 해결` · `주름 + 볼륨 + 피부결·광채까지. 1회로 동안 얼굴 완성` |
| `combos[].packages[].salesPitch` | str | 24 | 0 | 0 | 24 | `처음이시면 가볍게 보톡스부터 시작해보세요. 10분이면 끝나고 점심시간에도 가능해요.` · `보톡스+필러가 가장 인기 있는 동안 조합이에요. 30분이면 끝나고 '좀 쉬었나?' 소리 들…` · `수입 정품으로 주름·볼륨·피부결을 한 번에! 프리미엄 라인이라 결과가 더 자연스럽고 오래가…` |
| `combos[].packages[].upsellHook` | str | 24 | 0 | 0 | 24 | `보톡스로 주름 펴시고, 필러로 꺼진 부분 채우시면 확 달라지세요!` · `여기에 스킨부스터 한 번 추가하시면 피부결까지 달라져요. 패키지로 묶으면 할인도 돼요!` · `피부 탄력까지 원하시면 HIFU 추가하시는 분들이 많으세요. 풀 패키지로 가시면 원장님이 …` |
| `combos[].packages[].clinicalRationale` | str | 24 | 0 | 0 | 24 | `보톡스 단독으로도 동적 주름에 충분한 효과. 첫 방문 환자 신뢰 구축 후 추가 시술 연계` · `보톡스(근이완) + 필러(볼륨)는 가장 검증된 쁘띠 조합. 보톡스가 근육 움직임을 줄여 필…` · `수입 보톡스(엘러간)는 임상 데이터 가장 풍부. 쥬비덤 Vycross 기술로 자연스러운 결…` |
| `combos[].packages[].riskBenefit` | str | 24 | 0 | 0 | 24 | `위험 최소, 효과 확실. 첫 시술로 최적` · `위험 낮음. 필러 혈관 폐색 주의 → 히알루로니다아제 비상 준비. 효과 대비 위험 비율 매…` · `위험 낮음. 수입 제품의 예측 가능한 결과 + 스킨부스터 재생으로 부작용 최소화` |

**enum 처럼 보이는 키** (문자열·3회 이상·distinct ≤ 10·반복 있음)

| 경로 | distinct 값 (횟수) |
|---|---|
| `combos[].packages[].tier` | `entry`(8), `recommended`(8), `premium`(6), `vip`(2) |
| `combos[].packages[].tierLabel` | `기본`(8), `표준`(8), `확장`(6), `종합`(2) |
| `combos[].packages[].procedures[]` | `M1`(13), `M4`(11), `M2`(9), `M8`(8), `M9`(7), `M5`(7), `M11`(4), `M7`(2), `M12`(2) |
| `combos[].packages[].productTier` | `국산`(8), `수입`(7), `국산+수입 혼합`(2), `수입 프리미엄`(2), `국산/수입`(2), `혼합`(2), `수입+국산`(1) |

**식별자 후보** (레코드 배열별)

| 레코드 배열 | 건수 | 키 | 존재 | distinct | 유일 | 중복 예 |
|---|---|---|---|---|---|---|
| `combos` | 8 | `problem_id` | 8 | 8 | ○ |  |
| `combos` | 8 | `problem` | 8 | 8 | ○ |  |
| `combos[].packages` | 24 | `id` | 24 | 24 | ○ |  |
| `combos[].packages` | 24 | `name` | 24 | 24 | ○ |  |

**관찰** (원장 자체에서 보이는 것. 판정 아님)

- 고민 8개만 있다(P6·P8·P10·P12·P13·P14 없음). P3 이름이 `처짐/탄력`, P4 가 `피부결/톤/항노화` 로 taxonomy(`쳐짐`, `항노화`)와 다르다.
- `packages[].id` 가 `P1-1`, `P1-2` … 형식인데 taxonomy 의 problem 하위분류 id(`P1-1`=코, `P1-2`=이마/관자놀이)와 같은 문자열을 다른 뜻으로 쓴다.
- `procedures[]` 는 M 코드이지만 `products[]` 는 `나보타 or 보툴렉스`, `울쎄라(HIFU) 또는 올리지오(모노폴라 RF) + 보톡스 + 쥬비덤` 같은 자유 조합 문장 1개씩이다.
- `priceRange` 는 `5~8만`, `15~30만/회` 식 자유 텍스트(단위 `/회` 가 일부에만).
- `tier`(entry/recommended/premium/vip) 와 `tierLabel`(기본/표준/확장/종합)이 쌍으로 들어 있고, `productTier` 는 7종(`국산`, `수입`, `국산+수입 혼합`, `수입+국산`, `국산/수입`, `혼합`, `수입 프리미엄`).
- 키 이름이 camelCase(salesPitch, upsellHook, clinicalRationale …).

### 2.14 `problem-packages.json` — 73,526B · 잎 키 19

고민 14개 × 주호소(cc) 115개별 시술(제품 포함)·조합·대안. description 에 「taxonomy P1~P14 기반 자동 생성」

**최상위 구조**

- 메타 키: `version`=`6.2`, `updated`=`2026-07-26`, `description`=`taxonomy P1~P14 하위구조 기반 CC 자동 생성`
- 데이터 키: `problems` (list, 14)
- 배열: `problems`×1(len 14~14, 합 14), `problems[].complaints`×14(len 4~17, 합 115), `problems[].complaints[].procedures`×115(len 1~6, 합 254), `problems[].complaints[].procedures[].products`×207(len 1~3, 합 388), `problems[].complaints[].combos`×114(len 1~3, 합 146), `problems[].complaints[].combos[].combo`×146(len 1~3, 합 277), `problems[].complaints[].alternatives`×115(len 1~2, 합 125)

**잎 키 표**

| 경로 | 타입 | 횟수 | null | 빈값 | distinct | 예시 |
|---|---|---|---|---|---|---|
| `version` | str | 1 | 0 | 0 | 1 | `6.2` |
| `updated` | str | 1 | 0 | 0 | 1 | `2026-07-26` |
| `description` | str | 1 | 0 | 0 | 1 | `taxonomy P1~P14 하위구조 기반 CC 자동 생성` |
| `problems[].problem_id` | str | 14 | 0 | 0 | 14 | `P1` · `P2` · `P3` |
| `problems[].problem` | str | 14 | 0 | 0 | 14 | `쁘띠시술` · `주름` · `쳐짐` |
| `problems[].complaints[].cc` | str | 115 | 0 | 0 | 107 | `코필러` · `코실리프팅` · `이마필러` |
| `problems[].complaints[].cc_detail` | str | 115 | 0 | 0 | 107 | `콧대/코끝` · `코끝 거상` · `볼륨/라운딩` |
| `problems[].complaints[].cc_group` | str | 115 | 0 | 0 | 52 | `코` · `이마/관자놀이` · `턱/턱선` |
| `problems[].complaints[].procedures[].name` | str | 254 | 0 | 0 | 29 | `필러` · `보톡스` · `실리프팅` |
| `problems[].complaints[].procedures[].category` | str | 254 | 0 | 0 | 15 | `M2` · `M1` · `M7` |
| `problems[].complaints[].procedures[].role` | str | 254 | 0 | 0 | 63 | `볼륨 충전` · `근이완 보조` · `물리적 거상` |
| `problems[].complaints[].procedures[].products[]` | str | 388 | 0 | 0 | 34 | `쥬비덤` · `이브아르` · `보톡스` |
| `problems[].complaints[].combos[].name` | str | 146 | 0 | 0 | 44 | `필러 + 보톡스` · `실리프팅 + 필러` · `지방이식 + PRP` |
| `problems[].complaints[].combos[].combo[]` | str | 277 | 0 | 0 | 29 | `필러` · `보톡스` · `실리프팅` |
| `problems[].complaints[].combos[].reason` | str | 146 | 0 | 0 | 48 | `볼륨 + 근이완 = 시너지` · `거상 + 볼륨 = 입체적 리프팅` · `자가지방 + 성장인자 = 생착률 향상` |
| `problems[].complaints[].combos[].evidence` | str | 146 | 0 | 0 | 51 | `보톡스가 근육 움직임 줄여 필러 유지력 향상` · `실이 당기고 필러가 채움` · `PRP가 지방세포 생존율 높임` |
| `problems[].complaints[].alternatives[]` | str | 125 | 0 | 0 | 16 | `바이오스티뮬레이터로 장기 관리` · `실 시술 후 2개월간 HIFU/RF 피할 것` · `필러가 간편한 대안` |
| `problems[].complaints[].procedures[].products` | list(empty) | 47 | 0 | 47 | 0 |  |
| `problems[].complaints[].combos` | list(empty) | 1 | 0 | 1 | 0 |  |

**enum 처럼 보이는 키** (문자열·3회 이상·distinct ≤ 10·반복 있음)

- 없음

**식별자 후보** (레코드 배열별)

| 레코드 배열 | 건수 | 키 | 존재 | distinct | 유일 | 중복 예 |
|---|---|---|---|---|---|---|
| `problems` | 14 | `problem_id` | 14 | 14 | ○ |  |
| `problems` | 14 | `problem` | 14 | 14 | ○ |  |
| `problems[].complaints` | 115 | `cc` | 115 | 107 | ✗ | `아그네스`, `스킨보톡스`, `프락셔널레이저`, `니들RF`, `서브시전`, `브이올렛` |
| `problems[].complaints[].procedures` | 254 | `category` | 254 | 15 | ✗ | `M2`, `M1`, `M7`, `M6`, `M5`, `M4` |
| `problems[].complaints[].procedures` | 254 | `name` | 254 | 29 | ✗ | `필러`, `보톡스`, `실리프팅`, `지방이식`, `PRP/자가혈`, `스킨부스터` |
| `problems[].complaints[].combos` | 146 | `name` | 146 | 44 | ✗ | `필러 + 보톡스`, `실리프팅 + 필러`, `지방이식 + PRP`, `보톡스 + 스킨부스터`, `반영구 단독`, `보톡스 + 리프팅기기` |

**관찰** (원장 자체에서 보이는 것. 판정 아님)

- (기계) 빈값 47/47: `problems[].complaints[].procedures[].products`
- (기계) 빈값 1/1: `problems[].complaints[].combos`
- `complaints[].cc` 115개가 taxonomy problem 항목 117개와 이름으로 대응한다 — taxonomy 에만 있는 것 2개(`P4:줄기세포치료`, `P8:경화요법`), packages 에만 있는 것 0. 단 cc 쪽엔 taxonomy 항목 id(`auto-63-…`)가 없다.
- `cc_group` 이 taxonomy 하위분류 label 과 다른 곳 2건(P9 `니들RF`: cc_group `여드름흉터` vs taxonomy `튼살`; P9 `프락셔널레이저`: `수술흉터/화상흉터` vs `튼살`). cc 이름이 P9 안에서 중복되어 생긴 대응.
- `procedures[].name` 29종이 M 코드 15개에 매핑되는데 한 코드에 여러 이름(M8: 레이저/프락셔널/서브시전/혈관레이저/제모레이저/피코레이저, M15: 반영구화장/메디컬스킨케어/약물치료/병변내 스테로이드주사/모발이식, M9: 리프팅기기/인모드/미라드라이, M14: 크라이오/지방분해, M16: 수액/미백주사). `리프팅기기` 는 taxonomy `기기 리프팅` 과 표기가 다르다.
- `procedures[].products` 가 254건 중 47건 빈 배열. `combos` 가 1건 빈 배열.
- `products[]` 34종 중 products.json 에 없는 것 4: `헤어맥스(LLLT)`, `트리암시놀론(±5-FU)`, `PDL(V빔)`, `CO2레이저`. `리쥬란 힐러`·`셀피아`·`프락셀`·`시크릿` 등 10여 종은 products.json 엔 있으나 taxonomy 항목(items) 이름으로는 없음(§3.5).
- `combos[].combo[]` 멤버 이름에 `MTS`, `바이오스티뮬레이터`, `필링` 처럼 `procedures[].name` 에 없는 표기가 섞여 있다.
- `cc` 115 중 distinct 107 — `아그네스`, `스킨보톡스`, `프락셔널레이저`, `니들RF`, `서브시전`, `브이올렛` 이 다른 고민에 중복(taxonomy 도 같음).

### 2.15 `procedure-comparison.json` — 18,002B · 잎 키 18

비교 주제 9개(lifting 등)별 시술 39개의 기전·통증·다운타임·비용·적합/한계·PIH

**최상위 구조**

- 메타 키: `version`=`1.3`, `updated`=`2026-07-26`
- 데이터 키: `comparisons` (list, 9)
- 배열: `comparisons`×1(len 9~9, 합 9), `comparisons[].evidence_notes`×3(len 3~4, 합 11), `comparisons[].procedures`×9(len 4~5, 합 39)

**잎 키 표**

| 경로 | 타입 | 횟수 | null | 빈값 | distinct | 예시 |
|---|---|---|---|---|---|---|
| `version` | str | 1 | 0 | 0 | 1 | `1.3` |
| `updated` | str | 1 | 0 | 0 | 1 | `2026-07-26` |
| `comparisons[].id` | str | 9 | 0 | 0 | 9 | `lifting` · `wrinkle` · `volume` |
| `comparisons[].title` | str | 9 | 0 | 0 | 9 | `리프팅 비교` · `주름 개선 비교` · `볼륨 회복 비교` |
| `comparisons[].subtitle` | str | 9 | 0 | 0 | 9 | `처짐/탄력 개선을 위한 시술 비교` · `이마/미간/눈가 주름 치료 비교` · `볼/관자/이마 볼륨 충전 비교` |
| `comparisons[].evidence_notes[]` | str | 11 | 0 | 0 | 11 | `실리프팅: 즉각적 효과가 가장 뚜렷하지만 3-7일 다운타임. 실+RF/HIFU 조합 시 만…` · `HIFU: 깊은 리프팅(SMAS층 도달), 2-3개월 점진적 효과. 심한 처짐은 효과 제한…` · `RF: 안전성 가장 높지만 리프팅 효과 가장 약함. 피부결+타이트닝에 더 적합` |
| `comparisons[].procedures[].name` | str | 39 | 0 | 0 | 38 | `울쎄라 (HIFU)` · `써마지FLX (RF)` · `실리프팅 (PDO코그)` |
| `comparisons[].procedures[].category` | str | 39 | 0 | 0 | 15 | `M9` · `M7` · `M11` |
| `comparisons[].procedures[].mechanism_simple` | str | 39 | 0 | 0 | 39 | `초음파로 SMAS층 열응고` · `고주파로 콜라겐 수축+재생` · `실로 물리적 당김 + 콜라겐 유도` |
| `comparisons[].procedures[].pain` | str | 39 | 0 | 0 | 4 | `★★★★☆` · `★★★☆☆` · `★★☆☆☆` |
| `comparisons[].procedures[].downtime` | str | 39 | 0 | 0 | 21 | `거의 없음` · `3-7일 부종/멍` · `2-3일 붉은기` |
| `comparisons[].procedures[].onset` | str | 39 | 0 | 0 | 22 | `즉시 + 3개월 점진` · `즉시 + 2-3개월` · `즉시` |
| `comparisons[].procedures[].duration` | str | 39 | 0 | 0 | 18 | `6-12개월` · `12-18개월` · `3-6개월` |
| `comparisons[].procedures[].cost_range` | str | 39 | 0 | 0 | 29 | `100-400만원` · `80-400만원` · `50-200만원` |
| `comparisons[].procedures[].best_for` | str | 39 | 0 | 0 | 39 | `중등도 처짐, 비수술 원하는 경우` · `피부 탄력, 타이트닝` · `즉각적 리프팅 효과` |
| `comparisons[].procedures[].limitations` | str | 39 | 0 | 0 | 38 | `심한 처짐은 효과 제한` · `지방위축 위험 (반복 시)` · `실 이탈, 비대칭 가능` |
| `comparisons[].procedures[].pih_risk` | str | 39 | 0 | 0 | 5 | `very_low` · `none` · `low` |
| `comparisons[].procedures[].asian_skin_note` | str | 2 | 0 | 0 | 2 | `표피 우회 → PIH 최저. 아시아 피부 1차 선택` · `아시아 피부 PIH 위험 가장 높음. 저밀도/저에너지 세팅 + 사전 미백 권장` |

**enum 처럼 보이는 키** (문자열·3회 이상·distinct ≤ 10·반복 있음)

| 경로 | distinct 값 (횟수) |
|---|---|
| `comparisons[].procedures[].pain` | `★★☆☆☆`(20), `★★★☆☆`(11), `★☆☆☆☆`(5), `★★★★☆`(3) |
| `comparisons[].procedures[].pih_risk` | `none`(16), `low`(12), `very_low`(6), `moderate`(4), `high`(1) |

**식별자 후보** (레코드 배열별)

| 레코드 배열 | 건수 | 키 | 존재 | distinct | 유일 | 중복 예 |
|---|---|---|---|---|---|---|
| `comparisons` | 9 | `id` | 9 | 9 | ○ |  |
| `comparisons` | 9 | `title` | 9 | 9 | ○ |  |
| `comparisons[].procedures` | 39 | `category` | 39 | 15 | ✗ | `M9`, `M11`, `M2`, `M8`, `M4`, `M3` |
| `comparisons[].procedures` | 39 | `name` | 39 | 38 | ✗ | `히알루론산 필러` |

**일부 레코드에만 있는 키**

| 레코드 배열 | 건수 | 키=존재수 |
|---|---|---|
| `comparisons` | 9 | `evidence_notes`=3 |
| `comparisons[].procedures` | 39 | `asian_skin_note`=2 |

**관찰** (원장 자체에서 보이는 것. 판정 아님)

- `comparisons[].id` 는 영문 슬러그 9개(lifting, wrinkle, volume, skin_texture, pigment, hair_removal, body_contouring, acne, rejuvenation) — treatment-optimization 의 `icon`(wrinkle, lifting, volume, texture, pigment, acne, laser, body)과 비슷하나 다른 집합.
- `procedures[].name` 은 브랜드+괄호 설명(`울쎄라 (HIFU)`, `써마지FLX (RF)`), `category` 는 M 코드. `히알루론산 필러` 가 두 비교에 중복.
- `pain` 은 `★★★☆☆` 별 문자열 4종, `pih_risk` 는 very_low/none/low/moderate/high 5종(pih-risk.json 의 5단계와 달리 `none` 이 있고 `very_high` 가 없음).
- `cost_range`·`downtime`·`onset`·`duration` 모두 자유 텍스트(`100-400만원`, `즉시 + 3개월 점진`).
- `evidence_notes[]` 는 9개 중 3개에만, `asian_skin_note` 는 39개 중 2개에만.
- M10 자리에 `리포셀 (HIFU 지방)`, M9 에 `IPL (광선치료)`·`IPL 제모`·`바넬라 (고주파 바디)`, M17 에 `엑소좀 (줄기세포 유래)` 가 들어 있다(코드-이름 대응을 그대로 적음).

### 2.16 `procedure-profiles.json` — 19,548B · 잎 키 27

계열 17개의 플로어 운영 프로파일(phase 순서·마취·준비시간·소요시간·위험 점수·주의·관리)

**최상위 구조**

- 메타 키: `version`=`3.3`, `updated`=`2026-07-26`, `description`=`시술 프로파일 v3 — 플로어 매니저 관점: 제품 준비, 소요 시간, 마취, 시술 후 관리…`
- 데이터 키: `profiles` (list, 17)
- 배열: `profiles`×1(len 17~17, 합 17), `profiles[].mechanism`×17(len 1~2, 합 25), `profiles[].practicalNotes`×17(len 3~5, 합 64), `profiles[].aftercare`×17(len 3~5, 합 64)

**잎 키 표**

| 경로 | 타입 | 횟수 | null | 빈값 | distinct | 예시 |
|---|---|---|---|---|---|---|
| `version` | str | 1 | 0 | 0 | 1 | `3.3` |
| `updated` | str | 1 | 0 | 0 | 1 | `2026-07-26` |
| `description` | str | 1 | 0 | 0 | 1 | `시술 프로파일 v3 — 플로어 매니저 관점: 제품 준비, 소요 시간, 마취, 시술 후 관리…` |
| `profiles[].id` | str | 17 | 0 | 0 | 17 | `M1` · `M2` · `M3` |
| `profiles[].name` | str | 17 | 0 | 0 | 17 | `보톡스` · `필러` · `바이오스티뮬레이터/콜라겐부스터` |
| `profiles[].name_en` | str | 17 | 0 | 0 | 17 | `Botulinum Toxin` · `Dermal Filler` · `Biostimulator` |
| `profiles[].phase` | str | 17 | 0 | 0 | 9 | `injection` · `regeneration` · `structure` |
| `profiles[].phaseOrder` | int | 17 | 0 | 0 | 14 | `40` · `38` · `36` |
| `profiles[].mechanism[]` | str | 25 | 0 | 0 | 12 | `injection` · `regenerative` · `mechanical` |
| `profiles[].hasProtein` | bool | 17 | 0 | 0 | 2 | `True` · `False` |
| `profiles[].hasHA` | bool | 17 | 0 | 0 | 2 | `False` · `True` |
| `profiles[].usesGel` | bool | 17 | 0 | 0 | 2 | `False` · `True` |
| `profiles[].createsWound` | bool | 17 | 0 | 0 | 2 | `False` · `True` |
| `profiles[].createsChannel` | bool | 17 | 0 | 0 | 2 | `False` · `True` |
| `profiles[].thermalLoad` | int | 17 | 0 | 0 | 3 | `0` · `2` · `3` |
| `profiles[].bleedingRisk` | int | 17 | 0 | 0 | 4 | `1` · `2` · `3` |
| `profiles[].swellingRisk` | int | 17 | 0 | 0 | 4 | `1` · `3` · `2` |
| `profiles[].needsAnesthesia` | str | 17 | 0 | 0 | 6 | `none` · `topical_or_block` · `topical` |
| `profiles[].position` | str | 17 | 0 | 0 | 2 | `sitting_or_supine` · `supine` |
| `profiles[].needsCleansing` | bool | 17 | 0 | 0 | 2 | `False` · `True` |
| `profiles[].prepTime` | int | 17 | 0 | 0 | 6 | `5` · `10` · `3` |
| `profiles[].prepNotes` | str | 17 | 0 | 0 | 17 | `생리식염수로 희석 (100U/2.5~4ml). 냉장 보관 제품은 30분 전 꺼내기` · `냉장 보관 시 30분 전 상온화. 리도카인 함유 제품이면 추가 마취 불필요. 히알루로니다아…` · `스컬트라(PLLA): 전통적으로 2~72시간 전 재수화를 권장하나 2024 다기관연구상 즉…` |
| `profiles[].durationMin` | int | 17 | 0 | 0 | 6 | `10` · `15` · `60` |
| `profiles[].durationMax` | int | 17 | 0 | 0 | 6 | `15` · `40` · `30` |
| `profiles[].moa_summary` | str | 17 | 0 | 0 | 17 | `신경-근육 접합부 아세틸콜린 차단 → 근이완. 단백질 약물이므로 열에 의해 변성됨` · `HA/CaHA를 진피~피하에 주입 → 즉각 볼륨. HA는 열에 의해 분해 촉진됨` · `PLLA/PCL/CaHA 미립자 → 콜라겐 신생 유도. 효과 발현 1~3개월` |
| `profiles[].practicalNotes[]` | str | 64 | 0 | 0 | 64 | `단백질 약물 → 열 시술 뒤에 (변성 방지)` · `주입 직후 시술 부위 강하게 누르거나 마사지 금지 (실제 확산 위험 인자는 압박·마사지이며…` · `주입 부위 문지르기 금지` |
| `profiles[].aftercare[]` | str | 64 | 0 | 0 | 61 | `시술 부위 압박·문지름 자제 (자세 제한의 확산 방지 효과는 근거 제한적)` · `시술 부위 문지르거나 마사지 금지 (24시간)` · `당일 음주·격한 운동 피하기` |

**enum 처럼 보이는 키** (문자열·3회 이상·distinct ≤ 10·반복 있음)

| 경로 | distinct 값 (횟수) |
|---|---|
| `profiles[].phase` | `injection`(5), `device`(3), `regeneration`(2), `structure`(2), `device_clean`(1), `device_gel`(1), `device_invasive`(1), `channel`(1), `care`(1) |
| `profiles[].needsAnesthesia` | `topical`(7), `none`(6), `topical_or_block`(1), `block_or_sedation`(1), `block`(1), `topical_or_none`(1) |
| `profiles[].position` | `supine`(15), `sitting_or_supine`(2) |

**식별자 후보** (레코드 배열별)

| 레코드 배열 | 건수 | 키 | 존재 | distinct | 유일 | 중복 예 |
|---|---|---|---|---|---|---|
| `profiles` | 17 | `id` | 17 | 17 | ○ |  |
| `profiles` | 17 | `name` | 17 | 17 | ○ |  |

**관찰** (원장 자체에서 보이는 것. 판정 아님)

- 17개 계열 전부. 불리언 5개(hasProtein/hasHA/usesGel/createsWound/createsChannel)·정수 점수 3개(thermalLoad·bleedingRisk·swellingRisk, 0~3)·정수 시간 3개(prepTime, durationMin, durationMax).
- `phase` 9종 + `phaseOrder` 정수인데 phaseOrder 가 중복된다(95: M6·M15, 90: M7·M16, 85: M9·M14).
- `mechanism[]` 12종 중 `regenerative`(M3·M4·M5·M6) 와 `regeneration`(M17) 이 따로 있다.
- `needsAnesthesia` 6종(none, topical, topical_or_block, topical_or_none, block, block_or_sedation), `position` 2종.
- `name` 표기: M5 `PRP/엑소좀`, M9 `에너지기기(HIFU/RF)` (market-pricing 과 같고 taxonomy 와 다름).
- 키 이름 camelCase 16개로 가장 많다.

### 2.17 `products.json` — 8,322B · 잎 키 61

제품-제조사 매핑 8개 섹션 59개 제품(name/name_en/제조사/국가/mfds). 섹션 키가 영문 슬러그

**최상위 구조**

- 메타 키: `version`=`1.2`, `updated`=`2026-07-26`, `description`=`미용시술 제품-제조사 매핑 (유통사 아닌 제조사 기준)`
- 데이터 키: `botulinum_toxin` (dict, 2), `filler_ha` (dict, 2), `biostimulator` (dict, 2), `skin_booster` (dict, 2), `thread_lift` (dict, 2), `energy_device` (dict, 2), `prp_exosome` (dict, 2), `stem_cell` (dict, 2)
- 배열: `botulinum_toxin.products`×1(len 11~11, 합 11), `filler_ha.products`×1(len 7~7, 합 7), `biostimulator.products`×1(len 6~6, 합 6), `skin_booster.products`×1(len 5~5, 합 5), `thread_lift.products`×1(len 5~5, 합 5), `energy_device.category_id`×1(len 3~3, 합 3), `energy_device.products`×1(len 18~18, 합 18), `prp_exosome.products`×1(len 5~5, 합 5), `stem_cell.products`×1(len 2~2, 합 2)

**잎 키 표**

| 경로 | 타입 | 횟수 | null | 빈값 | distinct | 예시 |
|---|---|---|---|---|---|---|
| `version` | str | 1 | 0 | 0 | 1 | `1.2` |
| `updated` | str | 1 | 0 | 0 | 1 | `2026-07-26` |
| `description` | str | 1 | 0 | 0 | 1 | `미용시술 제품-제조사 매핑 (유통사 아닌 제조사 기준)` |
| `botulinum_toxin.category_id` | str | 1 | 0 | 0 | 1 | `M1` |
| `botulinum_toxin.products[].name` | str | 11 | 0 | 0 | 11 | `보톡스` · `디스포트` · `제오민` |
| `botulinum_toxin.products[].name_en` | str | 11 | 0 | 0 | 11 | `Botox` · `Dysport` · `Xeomin` |
| `botulinum_toxin.products[].manufacturer` | str | 11 | 0 | 0 | 10 | `앨러간/애브비` · `입센` · `멀츠` |
| `botulinum_toxin.products[].country` | str | 11 | 0 | 0 | 4 | `US` · `FR` · `DE` |
| `botulinum_toxin.products[].mfds` | bool | 11 | 0 | 0 | 1 | `True` |
| `botulinum_toxin.products[].note` | str | 1 | 0 | 0 | 1 | `휴젤 보툴렉스의 수출용 브랜드명(미국·중국·유럽 등)` |
| `filler_ha.category_id` | str | 1 | 0 | 0 | 1 | `M2` |
| `filler_ha.products[].name` | str | 7 | 0 | 0 | 7 | `쥬비덤` · `레스틸렌` · `이브아르` |
| `filler_ha.products[].name_en` | str | 7 | 0 | 0 | 7 | `Juvéderm` · `Restylane` · `Yvoire` |
| `filler_ha.products[].manufacturer` | str | 7 | 0 | 0 | 6 | `앨러간/애브비` · `갈더마` · `LG화학` |
| `filler_ha.products[].country` | str | 7 | 0 | 0 | 4 | `US` · `SE` · `KR` |
| `filler_ha.products[].mfds` | bool | 7 | 0 | 0 | 1 | `True` |
| `biostimulator.category_id` | str | 1 | 0 | 0 | 1 | `M3` |
| `biostimulator.products[].name` | str | 6 | 0 | 0 | 6 | `스컬트라` · `엘란쎄` · `래디어스` |
| `biostimulator.products[].name_en` | str | 6 | 0 | 0 | 6 | `Sculptra` · `Ellansé` · `Radiesse` |
| `biostimulator.products[].manufacturer` | str | 6 | 0 | 0 | 5 | `갈더마` · `싱클레어` · `멀츠` |
| `biostimulator.products[].country` | str | 6 | 0 | 0 | 4 | `FR` · `NL` · `DE` |
| `biostimulator.products[].mfds` | bool | 6 | 0 | 0 | 1 | `True` |
| `biostimulator.products[].ingredient` | str | 6 | 0 | 0 | 4 | `PLLA` · `PCL` · `CaHA` |
| `skin_booster.category_id` | str | 1 | 0 | 0 | 1 | `M4` |
| `skin_booster.products[].name` | str | 5 | 0 | 0 | 5 | `리쥬란 힐러` · `리쥬란 HB+` · `리쥬란아이` |
| `skin_booster.products[].name_en` | str | 5 | 0 | 0 | 5 | `Rejuran Healer` · `Rejuran HB+` · `Rejuran i` |
| `skin_booster.products[].manufacturer` | str | 5 | 0 | 0 | 3 | `파마리서치` · `-` · `휴메딕스` |
| `skin_booster.products[].country` | str | 5 | 0 | 0 | 2 | `KR` · `-` |
| `skin_booster.products[].mfds` | bool | 5 | 0 | 0 | 2 | `True` · `False` |
| `skin_booster.products[].ingredient` | str | 3 | 0 | 0 | 3 | `PN/PDRN` · `PN+HA` · `PN` |
| `skin_booster.products[].note` | str | 2 | 0 | 0 | 2 | `보톡스 희석 피내주사법 (별도 제품 아님)` · `2026 하반기 출시 예정, PN+HA 복합` |
| `thread_lift.category_id` | str | 1 | 0 | 0 | 1 | `M7` |
| `thread_lift.products[].name` | str | 5 | 0 | 0 | 5 | `민트리프트` · `테스리프트` · `실루엣소프트` |
| `thread_lift.products[].name_en` | str | 5 | 0 | 0 | 5 | `Mint Lift` · `TESSLift` · `Silhouette Soft` |
| `thread_lift.products[].manufacturer` | str | 5 | 0 | 0 | 5 | `한스바이오메드` · `리젠바이오텍` · `싱클레어` |
| `thread_lift.products[].country` | str | 5 | 0 | 0 | 2 | `KR` · `NL` |
| `thread_lift.products[].mfds` | bool | 5 | 0 | 0 | 1 | `True` |
| `thread_lift.products[].material` | str | 5 | 0 | 0 | 3 | `PDO` · `PDO+PCL` · `PLLA` |
| `energy_device.category_id[]` | str | 3 | 0 | 0 | 3 | `M8` · `M9` · `M11` |
| `energy_device.products[].name` | str | 18 | 0 | 0 | 18 | `울쎄라` · `써마지FLX` · `슈링크유니버스` |
| `energy_device.products[].name_en` | str | 18 | 0 | 0 | 18 | `Ultherapy` · `Thermage FLX` · `Shurink Universe` |
| `energy_device.products[].manufacturer` | str | 18 | 0 | 0 | 13 | `멀츠` · `솔타메디컬` · `클래시스` |
| `energy_device.products[].country` | str | 18 | 0 | 0 | 3 | `US` · `KR` · `IL` |
| `energy_device.products[].type` | str | 18 | 0 | 0 | 11 | `HIFU` · `RF` · `모노폴라 RF` |
| `prp_exosome.category_id` | str | 1 | 0 | 0 | 1 | `M5` |
| `prp_exosome.products[].name` | str | 5 | 0 | 0 | 5 | `셀피아` · `리젠ACR` · `마이셀` |
| `prp_exosome.products[].name_en` | str | 5 | 0 | 0 | 5 | `Cellpia` · `RegenACR` · `Mycell` |
| `prp_exosome.products[].manufacturer` | str | 5 | 0 | 0 | 5 | `CGBio` · `리젠바이오텍` · `한스바이오메드` |
| `prp_exosome.products[].country` | str | 5 | 0 | 0 | 1 | `KR` |
| `prp_exosome.products[].mfds` | bool | 5 | 0 | 0 | 2 | `True` · `False` |
| `prp_exosome.products[].type` | str | 5 | 0 | 0 | 2 | `PRP키트` · `엑소좀` |
| `prp_exosome.products[].note` | str | 2 | 0 | 0 | 1 | `화장품 허가. 주사/주입 사용 금지` |
| `prp_exosome.products[].legal_warning` | str | 2 | 0 | 0 | 1 | `국내 의료기관의 주사(injection) 용도 사용은 의료법·화장품법 위반 소지가 있으며 …` |
| `prp_exosome.products[].regulatory_status` | str | 2 | 0 | 0 | 1 | `화장품 허가만 받은 제품 — 식약처의 주사·주입 용도 허가 없음` |
| `stem_cell.category_id` | str | 1 | 0 | 0 | 1 | `M17` |
| `stem_cell.products[].name` | str | 2 | 0 | 0 | 2 | `큐어스킨` · `에스에프` |
| `stem_cell.products[].name_en` | str | 2 | 0 | 0 | 2 | `CureSkin` · `SF Injection` |
| `stem_cell.products[].manufacturer` | str | 2 | 0 | 0 | 2 | `바이오솔루션` · `에이치앤바이오` |
| `stem_cell.products[].country` | str | 2 | 0 | 0 | 1 | `KR` |
| `stem_cell.products[].mfds` | bool | 2 | 0 | 0 | 1 | `False` |
| `stem_cell.products[].type` | str | 2 | 0 | 0 | 2 | `성장인자` · `줄기세포배양액` |

**enum 처럼 보이는 키** (문자열·3회 이상·distinct ≤ 10·반복 있음)

| 경로 | distinct 값 (횟수) |
|---|---|
| `botulinum_toxin.products[].manufacturer` | `휴젤`(2), `앨러간/애브비`(1), `입센`(1), `멀츠`(1), `대웅제약`(1), `메디톡스`(1), `휴온스바이오파마`(1), `제테마`(1), `종근당바이오`(1), `뉴메코(Newmeco, 메디톡스 계열)`(1) |
| `botulinum_toxin.products[].country` | `KR`(8), `US`(1), `FR`(1), `DE`(1) |
| `filler_ha.products[].manufacturer` | `휴젤`(2), `앨러간/애브비`(1), `갈더마`(1), `LG화학`(1), `멀츠`(1), `휴메딕스`(1) |
| `filler_ha.products[].country` | `KR`(4), `US`(1), `SE`(1), `DE`(1) |
| `biostimulator.products[].manufacturer` | `바임(VAIM/바임글로벌)`(2), `갈더마`(1), `싱클레어`(1), `멀츠`(1), `에이씨피바이오`(1) |
| `biostimulator.products[].country` | `KR`(3), `FR`(1), `NL`(1), `DE`(1) |
| `biostimulator.products[].ingredient` | `PDLLA+HA`(3), `PLLA`(1), `PCL`(1), `CaHA`(1) |
| `skin_booster.products[].manufacturer` | `파마리서치`(3), `-`(1), `휴메딕스`(1) |
| `skin_booster.products[].country` | `KR`(4), `-`(1) |
| `thread_lift.products[].country` | `KR`(4), `NL`(1) |
| `thread_lift.products[].material` | `PDO`(3), `PDO+PCL`(1), `PLLA`(1) |
| `energy_device.products[].country` | `KR`(9), `US`(8), `IL`(1) |
| `prp_exosome.products[].country` | `KR`(5) |
| `prp_exosome.products[].type` | `PRP키트`(3), `엑소좀`(2) |

**식별자 후보** (레코드 배열별)

| 레코드 배열 | 건수 | 키 | 존재 | distinct | 유일 | 중복 예 |
|---|---|---|---|---|---|---|
| `botulinum_toxin.products` | 11 | `name` | 11 | 11 | ○ |  |
| `filler_ha.products` | 7 | `name` | 7 | 7 | ○ |  |
| `biostimulator.products` | 6 | `name` | 6 | 6 | ○ |  |
| `skin_booster.products` | 5 | `name` | 5 | 5 | ○ |  |
| `thread_lift.products` | 5 | `name` | 5 | 5 | ○ |  |
| `energy_device.products` | 18 | `name` | 18 | 18 | ○ |  |
| `prp_exosome.products` | 5 | `name` | 5 | 5 | ○ |  |
| `stem_cell.products` | 2 | `name` | 2 | 2 | ○ |  |

**일부 레코드에만 있는 키**

| 레코드 배열 | 건수 | 키=존재수 |
|---|---|---|
| `botulinum_toxin.products` | 11 | `note`=1 |
| `skin_booster.products` | 5 | `ingredient`=3, `note`=2 |
| `prp_exosome.products` | 5 | `note`=2, `legal_warning`=2, `regulatory_status`=2 |

**관찰** (원장 자체에서 보이는 것. 판정 아님)

- 섹션 키 8개가 영문 슬러그(botulinum_toxin, filler_ha, …)이고 안에 `category_id` 가 있다. `energy_device.category_id` 만 배열 `[M8, M9, M11]`, 나머지는 문자열 — 같은 키에 타입이 다르다.
- 섹션마다 제품 키가 다르다: `mfds` 가 energy_device 18개엔 아예 없음, `ingredient`(biostimulator 6·skin_booster 3), `material`(thread_lift), `type`(energy_device·prp_exosome·stem_cell), `note`/`legal_warning`/`regulatory_status`(일부).
- 자리표시자 `-` 가 있다: skin_booster `스킨보톡스` 의 manufacturer·country 가 `-`(note: `보톡스 희석 피내주사법 (별도 제품 아님)`).
- `mfds: false` 6건(스킨보톡스, 벨피엔, ASCEplus, EXOSOME SKIN, 큐어스킨, 에스에프).
- taxonomy `modality[].products` 와 비교: M1 에 products.json 은 `티엠버스`, taxonomy 는 `타임버스`(같은 제품의 다른 표기로 보이는 쌍, 판정 아님); M2 taxonomy 에만 `신펄`; energy_device 의 `볼뉴머` 는 products.json 에만(§3.5).
- 제조사 `클래시스` 와 `클래시스(Classys)` 두 표기.

### 2.18 `synergy.json` — 32,905B · 잎 키 10

시술 노드 쌍 115개의 시너지 링크(함께/다음에/대신). 노드는 `M코드-이름` 합성 문자열

**최상위 구조**

- 메타 키: `version`=`1.3`, `updated`=`2026-07-26`
- 데이터 키: `links` (list, 115)
- 배열: `links`×1(len 115~115, 합 115)

**잎 키 표**

| 경로 | 타입 | 횟수 | null | 빈값 | distinct | 예시 |
|---|---|---|---|---|---|---|
| `version` | str | 1 | 0 | 0 | 1 | `1.3` |
| `updated` | str | 1 | 0 | 0 | 1 | `2026-07-26` |
| `links[].from` | str | 115 | 0 | 0 | 41 | `M1-보톡스` · `M1-사각턱보톡스` · `M10-HIFES` |
| `links[].from_category` | str | 115 | 0 | 0 | 17 | `M1` · `M10` · `M11` |
| `links[].to` | str | 115 | 0 | 0 | 38 | `M2-필러` · `M4-스킨부스터` · `M9-리프팅기기` |
| `links[].to_category` | str | 115 | 0 | 0 | 13 | `M2` · `M4` · `M9` |
| `links[].type` | str | 115 | 0 | 0 | 3 | `함께` · `다음에` · `대신` |
| `links[].reason` | str | 115 | 0 | 0 | 115 | `보톡스로 근육 이완 + 필러로 볼륨 채움 = 자연스러운 동안 얼굴` · `보톡스로 주름 완화 + 스킨부스터로 피부결과 탄력 개선` · `보톡스+필러+리프팅 3종으로 근육·볼륨·처짐을 한번에 해결하는 풀 패키지` |
| `links[].timing` | str | 115 | 0 | 0 | 53 | `같은 날 시술 가능` · `같은 날 또는 2주 간격 순차 시술` · `보톡스 2주 후 리프팅` |
| `links[].target` | str | 115 | 0 | 0 | 17 | `안티에이징` · `안티에이징 패키지` · `리프팅` |

**enum 처럼 보이는 키** (문자열·3회 이상·distinct ≤ 10·반복 있음)

| 경로 | distinct 값 (횟수) |
|---|---|
| `links[].type` | `함께`(50), `다음에`(49), `대신`(16) |

**식별자 후보** (레코드 배열별)

| 레코드 배열 | 건수 | 키 | 존재 | distinct | 유일 | 중복 예 |
|---|---|---|---|---|---|---|
| `links` | 115 | `from` | 115 | 41 | ✗ | `M1-보톡스`, `M10-HIFES`, `M11-포텐자`, `M11-니들RF`, `M12-MTS`, `M13-플라즈마` |
| `links` | 115 | `to` | 115 | 38 | ✗ | `M2-필러`, `M4-스킨부스터`, `M9-리프팅기기`, `M1-보톡스`, `M11-시크릿`, `M12-MTS` |

**관찰** (원장 자체에서 보이는 것. 판정 아님)

- `from`/`to` 가 `M1-보톡스`, `M9-울쎄라`, `M4-쥬베룩` 처럼 코드+이름 합성 문자열이고, 별도로 `from_category`/`to_category` 에 코드가 또 있다. 합성 문자열의 코드 접두와 category 가 어긋난 건 0.
- 노드 이름 52종은 계열명·제품명·부위 변형이 섞여 있다(`M1-보톡스` / `M1-사각턱보톡스` / `M1-보톡스(코끝)`, `M9-인모드` / `M9-인모드(바디)`, `M12-MTS` / `M12-MTS(두피)`).
- `type` 3종(함께 50 / 다음에 49 / 대신 16). `target` 17종에 `안티에이징`/`안티에이징 패키지`, `흉터`/`흉터/재생`, `색소`/`색소/미백`, `여드름`/`여드름/모공` 처럼 비슷한 값이 따로 있다.
- 링크는 방향이 있고(from→to) 115개 전부 `reason` distinct. `timing` 53종 자유 텍스트.

### 2.19 `taxonomy.json` — 660,497B · 잎 키 87

계열(modality) 17 → 하위 74 → 항목 521 + 계열별 extracted/products, 고민(problem) 14 → 하위 53 → 항목 117(modality_ref). 가장 큼(660KB)

**최상위 구조**

- 데이터 키: `modality` (list, 17), `problem` (list, 14)
- 배열: `modality`×1(len 17~17, 합 17), `modality[].subcategories`×17(len 1~16, 합 74), `modality[].subcategories[].items`×72(len 1~61, 합 521), `modality[].subcategories[].items[].extracted.indications.primary`×521(len 2~7, 합 1656), `modality[].subcategories[].items[].extracted.indications.extended`×4(len 2~3, 합 10), `modality[].subcategories[].items[].extracted.safety.common`×521(len 1~5, 합 1278), `modality[].subcategories[].items[].extracted.safety.serious`×187(len 1~4, 합 422), `modality[].subcategories[].items[].extracted.aftercare`×521(len 1~8, 합 1914), `modality[].subcategories[].items[].extracted.indications.secondary`×9(len 1~3, 합 18), `modality[].subcategories[].items[].extracted.safety.common_adverse_effects`×2(len 3~3, 합 6), `modality[].subcategories[].items[].extracted.safety.serious_adverse_effects`×2(len 3~3, 합 6), `modality[].subcategories[].items[].extracted.safety.contraindications`×4(len 2~3, 합 11), `modality[].subcategories[].items[].extracted.safety.long_term`×1(len 1~1, 합 1), `modality[].extracted.indications.primary`×17(len 2~5, 합 56), `modality[].extracted.indications.extended`×17(len 3~19, 합 100), `modality[].extracted.contraindications.absolute`×17(len 2~4, 합 53), `modality[].extracted.contraindications.relative`×17(len 2~6, 합 55), `modality[].extracted.safety.common`×17(len 2~7, 합 59), `modality[].extracted.safety.uncommon`×17(len 1~5, 합 45), `modality[].extracted.safety.serious`×15(len 1~5, 합 37), `modality[].extracted.aftercare`×17(len 2~5, 합 53), `modality[].extracted.related_techniques`×17(len 2~4, 합 51), `modality[].products`×10(len 2~11, 합 59), `modality[].products[].extracted.indications.primary`×59(len 3~7, 합 256), `modality[].products[].extracted.safety.common`×59(len 2~7, 합 222), `modality[].products[].extracted.aftercare`×59(len 3~6, 합 238), `modality[].products[].extracted.indications.secondary`×7(len 2~2, 합 14), `modality[].products[].extracted.safety.serious`×31(len 1~4, 합 62), `modality[].products[].extracted.safety.common_side_effects`×1(len 4~4, 합 4), `modality[].products[].extracted.safety.contraindications`×1(len 1~1, 합 1), `problem`×1(len 14~14, 합 14), `problem[].subcategories`×14(len 3~7, 합 53), `problem[].subcategories[].items`×53(len 1~7, 합 117), `problem[].subcategories[].items[].modality_ref`×91(len 1~3, 합 105)

**잎 키 표**

| 경로 | 타입 | 횟수 | null | 빈값 | distinct | 예시 |
|---|---|---|---|---|---|---|
| `modality[].id` | str | 17 | 0 | 0 | 17 | `M1` · `M2` · `M3` |
| `modality[].category` | str | 17 | 0 | 0 | 17 | `보톡스` · `필러` · `바이오스티뮬레이터/콜라겐부스터` |
| `modality[].category_en` | str | 17 | 0 | 0 | 17 | `Botulinum Toxin` · `Filler` · `Biostimulator / Collagen Stimulator` |
| `modality[].group` | str | 17 | 0 | 0 | 3 | `주사/주입` · `시술/기기` · `관리` |
| `modality[].subcategories[].id` | str | 74 | 0 | 0 | 74 | `M1-2` · `M1-1` · `M1-3` |
| `modality[].subcategories[].label` | str | 74 | 0 | 0 | 72 | `수입` · `국산` · `용도별` |
| `modality[].subcategories[].items[].id` | str | 521 | 0 | 0 | 521 | `M1-2-1` · `M1-2-3` · `M1-2-2` |
| `modality[].subcategories[].items[].name` | str | 521 | 0 | 0 | 520 | `보톡스(엘러간)` · `디스포트` · `제오민` |
| `modality[].subcategories[].items[].detail` | str | 521 | 0 | 20 | 487 | `오리지널 · 900kDa 복합체` · `입센 · 프랑스 · 넓은 확산` · `멀츠 · 독일 · 150kDa 순수톡신` |
| `modality[].subcategories[].items[].extracted.overview` | str | 521 | 0 | 0 | 516 | `오리지널 보톡스, 900kDa 복합체 제형` · `클로스트리디움 보툴리눔 A형 독소 기반의 신경독소 제품으로, 광범위한 확산을 특징으로 하는…` · `150kDa 순수 보툴리눔 톡신 A로 안면 주름 개선 및 근육 이완 치료제` |
| `modality[].subcategories[].items[].extracted.mechanism` | str | 521 | 0 | 0 | 509 | `신경 말단에서 SNARE 복합체(SNAP-25)를 절단하여 아세틸콜린 분비를 차단, 근육 …` · `Clostridium botulinum Type A 독소가 SNARE 복합체의 SNAP-2…` · `Clostridium botulinum Type A가 신경근 접합부에서 SNARE 복합체(…` |
| `modality[].subcategories[].items[].extracted.indications.primary[]` | str | 1656 | 0 | 0 | 1003 | `미간주름` · `눈가주름(까치발)` · `이마주름` |
| `modality[].subcategories[].items[].extracted.indications.extended[]` | str | 10 | 0 | 0 | 10 | `눈썹 올리기` · `목주름` · `전체 얼굴 노화 개선` |
| `modality[].subcategories[].items[].extracted.safety.common[]` | str | 1278 | 0 | 0 | 473 | `주입부위 부종` · `약간의 통증` · `멍` |
| `modality[].subcategories[].items[].extracted.safety.serious[]` | str | 422 | 0 | 0 | 234 | `안검하수(눈꺼풀 처짐)` · `비대칭 표정 (드문 경우)` · `안검하수` |
| `modality[].subcategories[].items[].extracted.onset_duration.onset` | str | 520 | 0 | 0 | 164 | `3-7일 이내 효과 시작, 2-4주 점진적 개선, 1개월 완전 효과` · `2-3일` · `2-3일 시작, 1개월 완전 효과` |
| `modality[].subcategories[].items[].extracted.onset_duration.duration` | str | 521 | 0 | 0 | 184 | `3-4개월` · `12주 이상` · `3-4개월 지속` |
| `modality[].subcategories[].items[].extracted.aftercare[]` | str | 1914 | 0 | 0 | 975 | `시술 후 2-3일 간 과도한 운동 피하기` · `주사 부위 강하게 문지르거나 압박하지 않기 (가볍게 만지는 것은 무방)` · `시술 부위 청결 유지` |
| `modality[].subcategories[].items[].extracted.safety.note` | str | 4 | 0 | 0 | 4 | `반복 시술 시 교근 섬유화 위험 약 1.5%` · `반복 시술 시 1.5% 교근 섬유화 위험` · `반복 시술 시 1.5% 정도의 교근 섬유화 가능성` |
| `modality[].subcategories[].items[].extracted.onset_duration.peak` | str | 7 | 0 | 0 | 6 | `1개월` · `1개월 완전 효과 도달` · `1개월 완전 효과 발현` |
| `modality[].subcategories[].items[].extracted.onset_duration.peak_effect` | str | 8 | 0 | 0 | 5 | `1개월 완전 효과 발현` · `1개월 완전 발현` · `약 1개월에 완전 효과 발현` |
| `modality[].subcategories[].items[].extracted.indications.secondary[]` | str | 18 | 0 | 0 | 14 | `팔자주름` · `목주름` · `사각턱 개선` |
| `modality[].subcategories[].items[].extracted.safety.common_adverse_effects[]` | str | 6 | 0 | 0 | 6 | `주입 부위 부종` · `경미한 통증` · `일시적 발적` |
| `modality[].subcategories[].items[].extracted.safety.serious_adverse_effects[]` | str | 6 | 0 | 0 | 6 | `근력 약화` · `안검하수` · `표정 경직` |
| `modality[].subcategories[].items[].extracted.safety.contraindications[]` | str | 11 | 0 | 0 | 10 | `임신/수유 중` · `신경근 질환` · `항응고제 복용` |
| `modality[].subcategories[].items[].verification_needed` | str | 1 | 0 | 0 | 1 | `식약처 허가 번호 및 임상시험 근거 확인 전까지 '신규 허가' 표현 사용 금지. 확인 전에…` |
| `modality[].subcategories[].items[].extracted.safety.long_term[]` | str | 1 | 0 | 0 | 1 | `반복 시술 시 1.5% 교근 섬유화 위험` |
| `modality[].subcategories[].items[].extracted.onset_duration.maintenance` | str | 1 | 0 | 0 | 1 | `반복 시술 권장` |
| `modality[].extracted.overview` | str | 17 | 0 | 0 | 17 | `보톡스는 근육을 일시적으로 쉬게 만드는 주사제다. 원래 눈 떨림이나 근육 경련 치료에 쓰였…` · `필러는 피부 속 부피가 줄어든 부위에 채움 물질을 주입해서 주름을 펴거나 윤곽을 잡아주는 …` · `바이오스티뮬레이터는 피부 속에 특수 물질을 주입해서 우리 몸이 스스로 콜라겐(피부 탄력 단…` |
| `modality[].extracted.mechanism` | str | 17 | 0 | 0 | 17 | `보톡스는 근육에 명령을 전달하는 신경 끝부분에 작용한다. 신경이 근육에 '움직여라'는 신호…` · `필러는 피부 연조직의 결손부위(꺼진 곳, 주름, 흉터)에 물질을 채워 넣어 즉각적으로 볼륨…` · `바이오스티뮬레이터는 체내에서 분해되는 생체적합성 물질(PLLA, CaHA, PCL 등)을 …` |
| `modality[].extracted.indications.primary[]` | str | 56 | 0 | 0 | 56 | `미간주름 (눈썹 사이 찡그리면 생기는 세로 주름)` · `눈가 주름 (웃을 때 생기는 까치발 주름)` · `이마 주름 (가로로 생기는 이마 줄)` |
| `modality[].extracted.indications.extended[]` | str | 100 | 0 | 0 | 96 | `눈썹 올리기` · `눈밑주름` · `목주름` |
| `modality[].extracted.contraindications.absolute[]` | str | 53 | 0 | 0 | 48 | `보톡스 성분(알부민)에 알레르기가 있는 경우` · `중증근무력증 / 루게릭병 (근육이 점점 약해지는 질환) 환자` · `주사 맞을 부위에 염증이나 감염이 있는 경우` |
| `modality[].extracted.contraindications.relative[]` | str | 55 | 0 | 0 | 45 | `임신 중이거나 수유 중일 때는 미루는 게 좋음` · `특정 약물(항생제 일부, 근이완제 등) 복용 중이면 효과가 과하게 나타날 수 있으니 의사에…` · `혈액 응고에 영향을 주는 약물(아스피린 등) 복용 중이면 멍이 잘 들 수 있으니 의사에게 …` |
| `modality[].extracted.safety.common[]` | str | 59 | 0 | 0 | 42 | `주사 부위 통증` · `약간의 붓기` · `피부 빨개짐` |
| `modality[].extracted.safety.uncommon[]` | str | 45 | 0 | 0 | 41 | `표정이 어색해지는 느낌 (마스크 쓴 것 같은 얼굴)` · `주름이 덜 펴지는 경우` · `윗눈꺼풀이나 눈썹이 처지는 현상` |
| `modality[].extracted.safety.serious[]` | str | 37 | 0 | 0 | 35 | `드물게 메스꺼움, 피로감, 감기 비슷한 증상 (20년간 치명적 부작용 보고 없음)` · `반복 시술 시 몸에서 항체가 생겨 효과가 줄어들 수 있음` · `혈관 막힘 (필러가 혈관에 들어가 피부 괴사를 일으킬 수 있음 — 드물지만 위험)` |
| `modality[].extracted.onset_duration.onset` | str | 17 | 0 | 0 | 17 | `시술 후 12시간~4일 사이에 효과가 나타나기 시작` · `시술 직후 즉각적인 볼륨 효과` · `즉각적 볼륨 효과 + 콜라겐 재생은 4~6주 후부터 시작` |
| `modality[].extracted.onset_duration.peak` | str | 17 | 0 | 0 | 17 | `약 1주일 후 원하는 만큼 효과 도달` · `붓기가 빠진 후 1~2주 뒤 최종 결과 확인` · `시술 후 2~3개월 뒤 콜라겐 재생 효과 최대` |
| `modality[].extracted.onset_duration.duration` | str | 17 | 0 | 0 | 17 | `3~6개월 유지 (사람마다 다름)` · `히알루론산 필러 6~18개월, 칼슘 필러 12~24개월, 자가지방이식 6~12개월 (생착률…` · `PLLA(스컬트라) 18~24개월, CaHA(래디어스) 18~24개월, PCL(엘란쎄) 1…` |
| `modality[].extracted.aftercare[]` | str | 53 | 0 | 0 | 49 | `주사 직후 시술 부위를 강하게 누르거나 문지르지 않기 (확산 방지 목적, 자세 제한의 독립…` · `시술 부위를 만지거나 문지르지 않기` · `시술 후 강한 압력으로 시술 부위를 누르거나 마사지하지 않기` |
| `modality[].extracted.related_techniques[]` | str | 51 | 0 | 0 | 49 | `메조보톡스 (더모톡신) — 피부 탄력 개선, 리프팅 효과` · `에어보톡스 — 여드름 흉터 치료에 활용` · `히알루론산 메조테라피 (물광주사) — 피부 속 수분·탄력 개선` |
| `modality[].products[].id` | str | 59 | 0 | 0 | 59 | `M1-P-0` · `M1-P-1` · `M1-P-2` |
| `modality[].products[].name` | str | 59 | 0 | 0 | 59 | `보톡스` · `디스포트` · `제오민` |
| `modality[].products[].name_en` | str | 59 | 0 | 0 | 59 | `Botox` · `Dysport` · `Xeomin` |
| `modality[].products[].manufacturer` | str | 59 | 0 | 0 | 36 | `앨러간/애브비` · `입센` · `멀츠` |
| `modality[].products[].country` | str | 59 | 0 | 0 | 8 | `US` · `FR` · `DE` |
| `modality[].products[].mfds` | bool,null | 59 | 17 | 0 | 2 | `True` · `False` |
| `modality[].products[].extracted.overview` | str | 59 | 0 | 0 | 59 | `Clostridium botulinum Type A 신경독소를 정제한 근육이완제로, 표정주…` · `Clostridium botulinum Type A 유래 신경독소로 SNARE 복합체를 절…` · `150kDa 순수 보툴리눔 독소 A (복합단백질 제거)` |
| `modality[].products[].extracted.mechanism` | str | 59 | 0 | 0 | 59 | `SNARE 복합체(SNAP-25)를 절단하여 신경근접합부에서 아세틸콜린의 분비를 차단합니다…` · `보톡스는 SNAP-25 SNARE 복합체를 절단하여 신경근 접합부에서 아세틸콜린 분비를 차…` · `SNARE 복합체(SNAP-25)를 선택적으로 절단하여 아세틸콜린 분비를 차단한다. 복합단…` |
| `modality[].products[].extracted.indications.primary[]` | str | 256 | 0 | 0 | 175 | `표정주름(미간, 이마, 눈가)` · `과다발한` · `얼굴 윤곽 개선` |
| `modality[].products[].extracted.safety.common[]` | str | 222 | 0 | 0 | 117 | `주입 부위 통증, 부종, 멍` · `두통` · `안검하수(눈꺼풀 처짐)` |
| `modality[].products[].extracted.safety.note` | str | 1 | 0 | 0 | 1 | `반복 시술 시 1.5% 교근 섬유화 가능` |
| `modality[].products[].extracted.onset_duration.onset` | str | 59 | 0 | 0 | 43 | `2-3일부터 효과 시작` · `2-3일` · `2-3일 시작` |
| `modality[].products[].extracted.onset_duration.duration` | str | 59 | 0 | 0 | 46 | `1개월 완전 효과, 3-4개월 지속` · `완전 효과 도달 1개월, 유지 기간 3-4개월` · `3-4개월` |
| `modality[].products[].extracted.aftercare[]` | str | 238 | 0 | 0 | 218 | `시술 직후 시술 부위 압박·문지름 자제 (자세 제한의 확산 방지 효과는 근거 제한적)` · `시술 당일 운동 및 고온 환경 피하기` · `2주간 안면 마사지 및 과도한 압력 금지` |
| `modality[].products[].extracted.onset_duration.peak_effect` | str | 5 | 0 | 0 | 4 | `1개월 완전 효과` · `1개월 완전 발현` · `1개월` |
| `modality[].products[].extracted.onset_duration.diffusion` | str | 1 | 0 | 0 | 1 | `1U당 1.5-3cm 확산` |
| `modality[].products[].note` | str | 5 | 0 | 0 | 5 | `중국 수출명` · `보톡스 희석 피내주사법 (별도 제품 아님)` · `2026 하반기 출시 예정, PN+HA 복합` |
| `modality[].name` | str | 17 | 0 | 0 | 17 | `보톡스` · `필러` · `바이오스티뮬레이터/콜라겐부스터` |
| `modality[].products[].extracted.indications.secondary[]` | str | 14 | 0 | 0 | 11 | `혼합층 주입` · `얕은/깊은 모든 층` · `비순홈` |
| `modality[].products[].extracted.safety.serious[]` | str | 62 | 0 | 0 | 39 | `실명(미간 38.8%, 코 25.5%)` · `혈관폐색 육아종` · `동맥 폐색(0.04mL)` |
| `modality[].subcategories[].description` | str | 3 | 0 | 0 | 3 | `무세포동종진피(hADM, human Acellular Dermal Matrix) 기반 EC…` · `데옥시콜산(DCA) / 콜산(CA) 기반 지방세포파괴 주사제. FDA(2015 카이벨라) …` · `다양한 약물 혼합 지방분해 주사. 병원마다 성분/배합/명칭이 상이. DCA 제품과 달리 식…` |
| `modality[].products[].ingredient` | str | 9 | 0 | 0 | 8 | `PCL` · `PLLA` · `CaHA` |
| `modality[].subcategories[].items[].classification_issue` | str | 2 | 0 | 0 | 2 | `이 엔트리는 M4(스킨부스터) 섹션에 잘못 등재됨 — 볼뉴머는 클래시스(Classys)의 …` · `본 엔트리는 현재 M9-2(RF/에너지) 섹션에 있으나 실제 에너지원은 레이저(다이오드·알…` |
| `modality[].subcategories[].items[].is_marketing_name` | bool | 6 | 0 | 0 | 1 | `True` |
| `modality[].subcategories[].items[].ingredient_basis` | str | 6 | 0 | 0 | 6 | `히알루론산(비가교 또는 저분자 HA) + 비타민(C/B 계열) 혼합. 제품·클리닉별 배합 …` · `저분자 히알루론산 + 성장인자(EGF/bFGF/IGF 등) 또는 PN 혼합. 제품·클리닉별…` · `히알루론산 + 콜라겐 펩타이드/유래 단백 혼합. 제품·클리닉별 배합 상이` |
| `modality[].subcategories[].items[].canonical_category` | str | 6 | 0 | 0 | 6 | `M4 스킨부스터 > 비가교 HA 메조테라피` · `M4 스킨부스터 > 재생형 메조테라피` · `M4 스킨부스터 > 콜라겐 혼합 메조테라피` |
| `modality[].subcategories[].items[].naming_caveat` | str | 6 | 0 | 0 | 6 | `'꿀광'은 효과 묘사용 마케팅명으로 표준화된 단일 제제가 아님. 실제 사용 성분·농도는 클…` · `'아기피부'를 연상시키는 효과 표현용 마케팅명으로, 표준화된 단일 제품명이 아님. 성장인자…` · `'벨벳 피부결'을 연상시키는 효과 표현용 마케팅명으로 표준화된 단일 제제가 아님. 콜라겐 …` |
| `modality[].products[].type` | str | 24 | 0 | 0 | 14 | `PRP키트` · `엑소좀` · `피코레이저` |
| `modality[].products` | list(empty) | 7 | 0 | 7 | 0 |  |
| `modality[].products[].material` | str | 5 | 0 | 0 | 3 | `PDO` · `PDO+PCL` · `PLLA` |
| `modality[].products[].extracted.safety.common_side_effects[]` | str | 4 | 0 | 0 | 4 | `부종` · `경미한 통증` · `일시적 울퉁불퉁함` |
| `modality[].products[].extracted.safety.contraindications[]` | str | 1 | 0 | 0 | 1 | `PDO+비가교HA 병합 금기(24-72시간 내 시술 금지)` |
| `modality[].subcategories[].items[].correction_note` | str | 1 | 0 | 0 | 1 | `이전 데이터에 '808nm 다이오드 제모 레이저'로 잘못 기재돼 있었음. 실제 사양은 클래…` |
| `modality[].subcategories[].items[].reclassified_to` | str | 1 | 0 | 0 | 1 | `M8` |
| `modality[].subcategories[].items` | list(empty) | 2 | 0 | 2 | 0 |  |
| `problem[].id` | str | 14 | 0 | 0 | 14 | `P1` · `P2` · `P3` |
| `problem[].category` | str | 14 | 0 | 0 | 14 | `쁘띠시술` · `주름` · `쳐짐` |
| `problem[].category_en` | str | 14 | 0 | 0 | 14 | `Petit Procedure` · `Wrinkle` · `Sagging / Laxity` |
| `problem[].subcategories[].id` | str | 53 | 0 | 0 | 53 | `P1-1` · `P1-2` · `P1-3` |
| `problem[].subcategories[].label` | str | 53 | 0 | 0 | 53 | `코` · `이마/관자놀이` · `턱/턱선` |
| `problem[].subcategories[].items[].id` | str | 117 | 0 | 0 | 117 | `auto-63-1774737181584` · `auto-64-1774737181584` · `auto-65-1774737181584` |
| `problem[].subcategories[].items[].name` | str | 117 | 0 | 0 | 109 | `코필러` · `코실리프팅` · `이마필러` |
| `problem[].subcategories[].items[].detail` | str | 117 | 0 | 0 | 109 | `콧대/코끝` · `코끝 거상` · `볼륨/라운딩` |
| `problem[].subcategories[].items[].modality_ref[]` | str | 105 | 0 | 0 | 16 | `M2` · `M7` · `M6` |
| `problem[].subcategories[].items[].modality_ref` | list(empty) | 26 | 0 | 26 | 0 |  |

**enum 처럼 보이는 키** (문자열·3회 이상·distinct ≤ 10·반복 있음)

| 경로 | distinct 값 (횟수) |
|---|---|
| `modality[].group` | `시술/기기`(8), `주사/주입`(6), `관리`(3) |
| `modality[].subcategories[].items[].extracted.onset_duration.peak` | `1개월`(2), `1개월 완전 효과 도달`(1), `1개월 완전 효과 발현`(1), `1개월에 완전한 효과 발현`(1), `1개월 시 최대 효과`(1), `1개월 후 완전한 효과 도달`(1) |
| `modality[].subcategories[].items[].extracted.onset_duration.peak_effect` | `1개월 완전 효과 발현`(3), `1개월 완전 발현`(2), `약 1개월에 완전 효과 발현`(1), `시술 후 1개월 완전 효과 발현`(1), `1개월`(1) |
| `modality[].subcategories[].items[].extracted.safety.contraindications[]` | `임신/수유 중`(2), `신경근 질환`(1), `항응고제 복용`(1), `신경근육 질환`(1), `임신·수유 중`(1), `활동성 감염 부위`(1), `과도한 면역반응 병력`(1), `금속 임플란트 부위`(1), `심장박동기 장착자`(1), `임신 중`(1) |
| `modality[].products[].country` | `KR`(39), `US`(10), `DE`(3), `FR`(2), `NL`(2), `SE`(1), `-`(1), `IL`(1) |
| `modality[].products[].extracted.onset_duration.peak_effect` | `1개월 완전 발현`(2), `1개월 완전 효과`(1), `1개월`(1), `1개월 후 완전한 효과`(1) |
| `modality[].products[].ingredient` | `PDLLA`(2), `PCL`(1), `PLLA`(1), `CaHA`(1), `PDLLA+HA`(1), `PN/PDRN`(1), `PN+HA`(1), `PN`(1) |
| `modality[].products[].material` | `PDO`(3), `PDO+PCL`(1), `PLLA`(1) |

**식별자 후보** (레코드 배열별)

| 레코드 배열 | 건수 | 키 | 존재 | distinct | 유일 | 중복 예 |
|---|---|---|---|---|---|---|
| `modality` | 17 | `id` | 17 | 17 | ○ |  |
| `modality` | 17 | `category` | 17 | 17 | ○ |  |
| `modality` | 17 | `name` | 17 | 17 | ○ |  |
| `modality[].subcategories` | 74 | `id` | 74 | 74 | ○ |  |
| `modality[].subcategories` | 74 | `label` | 74 | 72 | ✗ | `기타`, `추가` |
| `modality[].subcategories[].items` | 521 | `id` | 521 | 521 | ○ |  |
| `modality[].subcategories[].items` | 521 | `name` | 521 | 520 | ✗ | `볼뉴머` |
| `modality[].products` | 59 | `id` | 59 | 59 | ○ |  |
| `modality[].products` | 59 | `name` | 59 | 59 | ○ |  |
| `problem` | 14 | `id` | 14 | 14 | ○ |  |
| `problem` | 14 | `category` | 14 | 14 | ○ |  |
| `problem[].subcategories` | 53 | `id` | 53 | 53 | ○ |  |
| `problem[].subcategories` | 53 | `label` | 53 | 53 | ○ |  |
| `problem[].subcategories[].items` | 117 | `id` | 117 | 117 | ○ |  |
| `problem[].subcategories[].items` | 117 | `name` | 117 | 109 | ✗ | `아그네스`, `스킨보톡스`, `프락셔널레이저`, `니들RF`, `서브시전`, `브이올렛` |

**일부 레코드에만 있는 키**

| 레코드 배열 | 건수 | 키=존재수 |
|---|---|---|
| `modality[].subcategories` | 74 | `description`=3 |
| `modality[].subcategories[].items` | 521 | `verification_needed`=1, `classification_issue`=2, `is_marketing_name`=6, `ingredient_basis`=6, `canonical_category`=6, `naming_caveat`=6, `correction_note`=1, `reclassified_to`=1 |
| `modality[].products` | 59 | `note`=5, `ingredient`=9, `type`=24, `material`=5 |

**관찰** (원장 자체에서 보이는 것. 판정 아님)

- (기계) 빈값 20/521: `modality[].subcategories[].items[].detail`
- (기계) null 17/59: `modality[].products[].mfds`
- (기계) 빈값 7/7: `modality[].products`
- (기계) 빈값 2/2: `modality[].subcategories[].items`
- (기계) 빈값 26/26: `problem[].subcategories[].items[].modality_ref`
- `version`/`updated` 메타 없음. 잎 키 87개로 가장 많다.
- `modality[]` 에 `category` 와 `name` 이 둘 다 있고 17개 전부 같은 값.
- 항목 id 체계가 세 가지: `M1-2-1` 형(128개), `auto-M4-1775362490962` 형(322개), `auto-63-1774737181584` 형(62개), `auto-M16-DCA-<timestamp>` 형 9개(M3 hADM 1, M16 DCA 8). 하위분류 id 도 `M1-2` 형 56개 외에 `M3-new-1774324237649`, `auto-new-M4-1775360442`, `M9-SIG`, `M15-도포`, `M16-DCA`, `auto-1775361777` 등 18개. problem 항목 id 는 117개 전부 `auto-#-timestamp` 형.
- 항목 `extracted` 의 하위 키 표기가 갈린다: `safety.common`(521) 외에 `safety.common_adverse_effects`(2), `safety.serious_adverse_effects`(2), `safety.contraindications`(4), `safety.long_term`(1), `safety.note`(4); `onset_duration.peak`(7) 와 `peak_effect`(8), `maintenance`(1); `indications.extended`(4) 와 `secondary`(9). products[].extracted 에는 `safety.common_side_effects`(4), `onset_duration.diffusion`(1)도 있다.
- `modality[].products` 는 M6·M10·M12·M13·M14·M15·M16 7개 계열에서 빈 배열. `products[].mfds` 는 59개 중 17개 null(M8·M9·M11 기기 전부).
- 항목 `detail` 빈 문자열 20개(PDO, PCL, PLCL, 알라딘필링, 셀레늄 …). `subcategories[].items` 빈 배열 2개(`M15-도포`, `M15-팩`). `subcategories[].label` 중복 `기타`, `추가`.
- 항목 이름 중복: `볼뉴머` 가 M4(auto-M4-…, `classification_issue` 플래그) 와 M9-2-3 두 곳. 원장 안에 이미 교정 메모 키가 있다 — `classification_issue`(2), `reclassified_to`(1: 소프라노 티타늄 → M8), `correction_note`(1: 리팟), `verification_needed`(1: 톡스온), `is_marketing_name`+`canonical_category`+`naming_caveat`(6: 꿀광주사·아기주사·벨벳주사·백옥주사·마늘주사·신데렐라주사).
- `modality[].extracted` 는 extracted.json 과 본문이 같거나(9) 일부 다르며(8), extracted.json 의 메타 키(name_en, source, procedure_id 등)는 없다.
- `problem[].subcategories[].items[].modality_ref` 는 117개 중 26개가 빈 배열(반영구·약물치료·서브시전·윤곽주사·지방분해주사·미녹시딜·FUE/FUT·미라드라이 등). 참조 코드는 전부 M1~M17 안에 있다.
- problem 항목 이름 중복 6건(아그네스, 스킨보톡스 → P6·P7 / 프락셔널레이저, 니들RF → P7·P9(2곳) / 서브시전 → P7·P9 / 브이올렛 → P11·P12).
- P3 의 category 가 `쳐짐`(다른 파일은 `처짐/탄력`, `처짐`).

### 2.20 `treatment-optimization.json` — 22,887B · 잎 키 36

고민 8개 × 중증도 3단계의 최적 조합·순서·근거, 연령대 4개 권장, 조합 규칙 8개, 연간 플랜 3개

**최상위 구조**

- 메타 키: `version`=`1.4`, `updated`=`2026-07-26`, `consensus_method`=`3-AI Expert Panel Consensus (Perplexity+Gemini+Cla…`
- 데이터 키: `optimization_principles` (list, 4), `by_concern` (list, 8), `by_age_group` (list, 4), `combination_rules` (list, 8), `annual_plans` (list, 3)
- 배열: `optimization_principles`×1(len 4~4, 합 4), `by_concern`×1(len 8~8, 합 8), `by_concern[].severity_levels`×8(len 3~3, 합 24), `by_concern[].severity_levels[].optimal_combo`×24(len 1~5, 합 74), `by_concern[].severity_levels[].contraindicated_combos`×13(len 1~2, 합 17), `by_concern[].severity_levels[].caveats`×1(len 2~2, 합 2), `by_age_group`×1(len 4~4, 합 4), `by_age_group[].primary_concerns`×4(len 4~5, 합 17), `by_age_group[].recommended_base`×4(len 4~5, 합 17), `by_age_group[].avoid`×4(len 1~2, 합 6), `by_age_group[].upgrade`×3(len 1~2, 합 5), `combination_rules`×1(len 8~8, 합 8), `annual_plans`×1(len 3~3, 합 3), `annual_plans[].schedule`×3(len 12~12, 합 36), `annual_plans[].schedule[].procedures`×36(len 1~3, 합 77)

**잎 키 표**

| 경로 | 타입 | 횟수 | null | 빈값 | distinct | 예시 |
|---|---|---|---|---|---|---|
| `version` | str | 1 | 0 | 0 | 1 | `1.4` |
| `updated` | str | 1 | 0 | 0 | 1 | `2026-07-26` |
| `consensus_method` | str | 1 | 0 | 0 | 1 | `3-AI Expert Panel Consensus (Perplexity+Gemini+Cla…` |
| `optimization_principles[]` | str | 4 | 0 | 0 | 4 | `안전성 우선 (Do No Harm)` · `시너지 극대화 (상호 보완 효과)` · `다운타임 최소화 (환자 편의)` |
| `by_concern[].concern` | str | 8 | 0 | 0 | 8 | `주름 개선` · `처짐/탄력` · `볼륨 손실` |
| `by_concern[].concern_en` | str | 8 | 0 | 0 | 8 | `Wrinkle Reduction` · `Sagging / Elasticity` · `Volume Loss` |
| `by_concern[].icon` | str | 8 | 0 | 0 | 8 | `wrinkle` · `lifting` · `volume` |
| `by_concern[].severity_levels[].level` | str | 24 | 0 | 0 | 24 | `경미 (fine lines)` · `중등도 (moderate wrinkles)` · `중증 (deep wrinkles)` |
| `by_concern[].severity_levels[].optimal_combo[]` | str | 74 | 0 | 0 | 57 | `레이저토닝` · `스킨부스터(리쥬란)` · `보톡스` |
| `by_concern[].severity_levels[].sequence` | str | 24 | 0 | 0 | 24 | `토닝 먼저 → 2주 후 스킨부스터` · `같은날: 필러→스킨부스터→보톡스. 또는 보톡스 먼저 → 2주 후 필러` · `HIFU/RF 먼저 → 보톡스(같은날 가능) → 2주 후 필러 → 스킨부스터` |
| `by_concern[].severity_levels[].rationale` | str | 24 | 0 | 0 | 24 | `토닝으로 표피 리뉴얼 후 스킨부스터로 진피 재생` · `보톡스(동적주름) + 필러(정적주름/볼륨) + 스킨부스터(피부결)` · `HIFU로 SMAS 리프팅 → 보톡스로 동적주름 → 필러로 볼륨/깊은주름 → 스킨부스터로 …` |
| `by_concern[].severity_levels[].expected_sessions` | str | 24 | 0 | 0 | 24 | `토닝 5-10회 + 스킨부스터 3회` · `보톡스 1회 + 필러 1회 + 스킨부스터 3회` · `HIFU 1-2회 + 보톡스 1회 + 필러 1-2회 + 스킨부스터 3회` |
| `by_concern[].severity_levels[].total_duration` | str | 24 | 0 | 0 | 9 | `3-6개월` · `2-4개월` · `3-4개월` |
| `by_concern[].severity_levels[].evidence_level` | str | 24 | 0 | 0 | 2 | `moderate` · `high` |
| `by_concern[].severity_levels[].contraindicated_combos` | list(empty) | 11 | 0 | 11 | 0 |  |
| `by_concern[].severity_levels[].contraindicated_combos[]` | str | 17 | 0 | 0 | 17 | `HA 필러 후 14일 이내 RF/HIFU 금지` · `PDO실 + 비가교HA 동시 금지` · `지방이식 후 2주 내 RF/HIFU 금지` |
| `by_concern[].severity_levels[].caveats[]` | str | 2 | 0 | 0 | 2 | `엑소좀: 국내외 미승인 — 美 FDA 미용·치료 목적 승인 0건(경고서한·집행 확대), 韓…` · `엑소좀 근거는 파일럿(가설 생성 수준)+소규모 split-face RCT 1건(보조요법으로…` |
| `by_age_group[].age` | str | 4 | 0 | 0 | 4 | `20대` · `30대` · `40대` |
| `by_age_group[].primary_concerns[]` | str | 17 | 0 | 0 | 15 | `여드름/흉터` · `모공` · `피부결` |
| `by_age_group[].recommended_base[]` | str | 17 | 0 | 0 | 11 | `스킨부스터` · `필링` · `토닝` |
| `by_age_group[].avoid[]` | str | 6 | 0 | 0 | 6 | `과도한 필러 (자연스러운 노화 중요)` · `불필요한 보톡스(예방 목적 과잉 금지)` · `과도한 필러량(자연스러움 유지)` |
| `by_age_group[].maintenance` | str | 4 | 0 | 0 | 4 | `토닝 월 1-2회, 스킨부스터 분기 1회, 필링 월 1회` · `보톡스 3-4개월, 스킨부스터 분기, 토닝 월 1-2회` · `보톡스 3-4개월, 필러 6개월+, HIFU 6개월+, 바이오스티뮬 연 1사이클` |
| `by_age_group[].annual_focus` | str | 4 | 0 | 0 | 4 | `피부 기초 관리, 여드름/흉터 집중 치료, 자외선 차단 습관화` · `노화 예방 시작, 보톡스로 동적주름 관리, 콜라겐 투자 시작` · `적극적 안티에이징, 처짐/볼륨 동시 관리, 복합 시술 조합` |
| `by_age_group[].upgrade[]` | str | 5 | 0 | 0 | 5 | `바이오스티뮬레이터 (콜라겐 예방적 투자)` · `실리프팅(PCL/PDO)` · `프락셔널 레이저` |
| `by_age_group[].note` | str | 1 | 0 | 0 | 1 | `수술(페이스리프트) 대안 또는 보완으로 비수술 조합. 전체적 조화 중시` |
| `combination_rules[].rule` | str | 8 | 0 | 0 | 8 | `열시술 → 주사 순서` · `필러 → RF 14일 간격` · `바이오스티뮬 결절 예방 = 희석·수화·주입 깊이 (마사지는 선택)` |
| `combination_rules[].detail` | str | 8 | 0 | 0 | 8 | `보톡스와 HIFU/RF 열시술은 당일 시술 가능하나 웬만하면 열시술을 먼저 시행. MFU/…` · `HA 필러 주입 후 14일 이내 RF/HIFU 시 필러 용해 위험` · `PLLA 균일 분포를 위한 5-5-5 마사지는 기술적 보조로 권장. 2025 동물실험은 균…` |
| `combination_rules[].evidence` | str | 8 | 0 | 0 | 8 | `MFU-보툴리눔독소 진피내 주입 RCT (J Cosmet Dermatol, PMC11945…` · `JCD 2023 논문` · `Dermatologica Sinica 2025;43(3):247-248 동물실험은 마사지 …` |
| `combination_rules[].consensus` | str | 8 | 0 | 0 | 3 | `근거 기반 임상 권고` · `3/3 AI 합의` · `2/3 AI 합의 (제한적 근거)` |
| `combination_rules[].priority` | str | 8 | 0 | 0 | 4 | `moderate` · `critical` · `important` |
| `annual_plans[].plan_name` | str | 3 | 0 | 0 | 3 | `20대 피부관리 베이직 플랜` · `30대 동안 유지 플랜` · `40대+ 안티에이징 집중 플랜` |
| `annual_plans[].age_group` | str | 3 | 0 | 0 | 3 | `20대` · `30대` · `40대+` |
| `annual_plans[].annual_budget_range` | str | 3 | 0 | 0 | 3 | `100-250만원` · `200-500만원` · `400-1000만원` |
| `annual_plans[].focus` | str | 3 | 0 | 0 | 3 | `피부 기초 관리, 여드름/흉터 개선, 모공/피부결 관리` · `노화 예방, 동적주름 관리, 콜라겐 투자 시작` · `처짐/주름 적극 관리, 볼륨 복원, 복합 시술 조합` |
| `annual_plans[].schedule[].month` | int | 36 | 0 | 0 | 12 | `1` · `2` · `3` |
| `annual_plans[].schedule[].procedures[]` | str | 77 | 0 | 0 | 29 | `토닝 4회` · `필링 1회` · `스킨부스터 1차` |

**enum 처럼 보이는 키** (문자열·3회 이상·distinct ≤ 10·반복 있음)

| 경로 | distinct 값 (횟수) |
|---|---|
| `by_concern[].severity_levels[].total_duration` | `6-12개월`(7), `3-6개월`(6), `4-8개월`(4), `2-4개월`(2), `3-4개월`(1), `12-24개월`(1), `12-18개월`(1), `8-15개월`(1), `12-18개월 + 유지`(1) |
| `by_concern[].severity_levels[].evidence_level` | `high`(13), `moderate`(11) |
| `combination_rules[].consensus` | `3/3 AI 합의`(6), `근거 기반 임상 권고`(1), `2/3 AI 합의 (제한적 근거)`(1) |
| `combination_rules[].priority` | `critical`(3), `important`(3), `moderate`(1), `caution`(1) |

**식별자 후보** (레코드 배열별)

- 없음(식별자 키 없음)

**일부 레코드에만 있는 키**

| 레코드 배열 | 건수 | 키=존재수 |
|---|---|---|
| `by_concern[].severity_levels` | 24 | `caveats`=1 |
| `by_age_group` | 4 | `upgrade`=3, `note`=1 |

**관찰** (원장 자체에서 보이는 것. 판정 아님)

- (기계) 빈값 11/11: `by_concern[].severity_levels[].contraindicated_combos`
- M/P 코드가 전혀 없다. `concern` 8개(주름 개선, 처짐/탄력, 볼륨 손실, 피부결/모공, 색소/기미, 여드름/흉터, 제모, 바디컨투어링)는 taxonomy 고민 14개와 이름이 다르고 1:1 대응이 아니다.
- `optimal_combo[]` 57종이 전부 자유 텍스트(`스킨부스터(리쥬란)`, `HIFU(슈링크/울쎄라)`, `HIFU(울쎄라/슈링크)`, `실리프팅(PDO/PCL)`/`실리프팅(PCL/PDO)`, `다이오드 레이저(810nm)`/`다이오드(810nm)` 처럼 순서·괄호만 다른 쌍 다수).
- `severity_levels[].level` 은 `경미 (fine lines)` 처럼 등급+설명 합성 문자열 24종. `evidence_level` 2종(high 13 / moderate 11). `total_duration` 9종 문자열(`12-18개월 + 유지` 포함).
- `contraindicated_combos` 11건 빈 배열, `caveats` 1건만.
- `combination_rules[].priority` 4종(critical/important/moderate/caution), `consensus` 3종(`3/3 AI 합의`, `2/3 AI 합의 (제한적 근거)`, `근거 기반 임상 권고`).
- `annual_plans[].schedule[].procedures[]` 는 `토닝 4회`, `IPL(가을 색소 관리)` 같은 횟수·계절 섞인 문장.
- `by_age_group[].upgrade`(3/4)·`note`(1/4) 일부에만.

### 2.21 `treatment-sequence.json` — 8,964B · 잎 키 20

동일 세션 시술 순서 11단계, 당일 병행 금기 9쌍, 대표 조합 8개, 최소 간격 9개. 시술명 대부분 자유 텍스트

**최상위 구조**

- 메타 키: `version`=`1.3`, `updated`=`2026-07-26`, `description`=`동일 세션 시술 조합 순서 가이드. 안전성과 효과 최적화 기준.`
- 데이터 키: `principles` (list, 13), `sequence_order` (list, 11), `incompatible_same_day` (list, 9), `common_combos` (list, 8), `minimum_intervals` (list, 9)
- 배열: `principles`×1(len 13~13, 합 13), `sequence_order`×1(len 11~11, 합 11), `sequence_order[].categories`×11(len 1~3, 합 19), `incompatible_same_day`×1(len 9~9, 합 9), `incompatible_same_day[].pair`×9(len 1~2, 합 17), `common_combos`×1(len 8~8, 합 8), `common_combos[].sequence`×8(len 3~4, 합 26), `minimum_intervals`×1(len 9~9, 합 9)

**잎 키 표**

| 경로 | 타입 | 횟수 | null | 빈값 | distinct | 예시 |
|---|---|---|---|---|---|---|
| `version` | str | 1 | 0 | 0 | 1 | `1.3` |
| `updated` | str | 1 | 0 | 0 | 1 | `2026-07-26` |
| `description` | str | 1 | 0 | 0 | 1 | `동일 세션 시술 조합 순서 가이드. 안전성과 효과 최적화 기준.` |
| `principles[]` | str | 13 | 0 | 0 | 13 | `클렌징 → 마취 → 시술 → 진정 순서 기본` · `보톡스와 HIFU/RF 열시술은 당일 병행 가능하나, 웬만하면 열시술을 먼저 시행` · `HIFU는 보톡스 주입 후 2주 이내 효력 저하 가능성을 고려해 HIFU 선행 또는 2주 …` |
| `sequence_order[].order` | int | 11 | 0 | 0 | 11 | `1` · `2` · `3` |
| `sequence_order[].phase` | str | 11 | 0 | 0 | 11 | `클렌징/준비` · `마취` · `에너지 기기` |
| `sequence_order[].categories[]` | str | 19 | 0 | 0 | 19 | `M15-클렌징` · `국소마취` · `연고마취` |
| `sequence_order[].reason` | str | 11 | 0 | 0 | 11 | `시술 부위 청결, 메이크업 제거` · `시술 30-60분 전 도포` · `보톡스와 당일 병행 가능하나 웬만하면 열시술 먼저. HIFU는 보톡스 주입 후 2주 이내 …` |
| `incompatible_same_day[].pair[]` | str | 17 | 0 | 0 | 14 | `CO2 프락셔널` · `필러` · `심부 필링(페놀)` |
| `incompatible_same_day[].reason` | str | 9 | 0 | 0 | 9 | `열린 상처에 필러 주입 감염 위험` · `이중 피부 손상` · `HA가 PDO를 24-72시간 내 분해 가능 (in vitro 연구). 실제 임상에서는 병…` |
| `common_combos[].name` | str | 8 | 0 | 0 | 8 | `동안 기본` · `피부결 개선` · `리프팅 풀코스` |
| `common_combos[].sequence[]` | str | 26 | 0 | 0 | 22 | `슈링크 HIFU` · `보톡스 이마/미간` · `필러 팔자` |
| `common_combos[].total_time` | str | 8 | 0 | 0 | 6 | `60-90분` · `45-60분` · `90-120분` |
| `common_combos[].note` | str | 3 | 0 | 0 | 3 | `필러 위치 안정화 먼저 → 스킨부스터 → 보톡스 마지막 순서 준수` · `에너지 기기(HIFU) 먼저 → 레이저 토닝 → 스킨부스터 마지막` · `프락셔널+MTS 채널 오픈 후 PRP 성장인자 경피 침투 극대화` |
| `minimum_intervals[].from` | str | 9 | 0 | 0 | 7 | `HA 필러` · `이소트레티노인` · `심부 필링` |
| `minimum_intervals[].to` | str | 9 | 0 | 0 | 7 | `RF/HIFU` · `레이저` · `프락셔널/얕은 필링` |
| `minimum_intervals[].min_days` | int | 7 | 0 | 0 | 3 | `14` · `5` · `0` |
| `minimum_intervals[].source` | str | 9 | 0 | 0 | 6 | `JCD 2023; ASDS 2024` · `임상 가이드` · `ASDS 2017 consensus; AAD 2024` |
| `minimum_intervals[].reason` | str | 9 | 0 | 0 | 9 | `주입 후 HA가 고온(>55°C) 노출 시 분해/변형 위험. 역순은 같은 날 가능` · `부종/열 상호작용` · `비박리성 프락셔널·얕은 필링은 6개월 일률 대기 근거가 부족하며 중단 후 0~2개월 범위에…` |
| `minimum_intervals[].min_months` | int | 2 | 0 | 0 | 2 | `0` · `6` |

**enum 처럼 보이는 키** (문자열·3회 이상·distinct ≤ 10·반복 있음)

| 경로 | distinct 값 (횟수) |
|---|---|
| `common_combos[].total_time` | `60-90분`(2), `60분`(2), `45-60분`(1), `90-120분`(1), `45분`(1), `90분`(1) |
| `minimum_intervals[].from` | `HA 필러`(2), `이소트레티노인`(2), `심부 필링`(1), `프락셔널 CO2`(1), `보톡스`(1), `RF/HIFU`(1), `필러`(1) |
| `minimum_intervals[].to` | `레이저`(2), `필러`(2), `RF/HIFU`(1), `프락셔널/얕은 필링`(1), `박리성(ablative) 레이저/심부 필링`(1), `필러 (별도 세션)`(1), `필러 (동일 부위 재시술)`(1) |
| `minimum_intervals[].source` | `임상 가이드`(4), `JCD 2023; ASDS 2024`(1), `ASDS 2017 consensus; AAD 2024`(1), `AAD 2024; ASDS 2017 consensus`(1), `피부 회복`(1), `PRS 논문`(1) |

**식별자 후보** (레코드 배열별)

| 레코드 배열 | 건수 | 키 | 존재 | distinct | 유일 | 중복 예 |
|---|---|---|---|---|---|---|
| `common_combos` | 8 | `name` | 8 | 8 | ○ |  |
| `minimum_intervals` | 9 | `from` | 9 | 7 | ✗ | `HA 필러`, `이소트레티노인` |
| `minimum_intervals` | 9 | `to` | 9 | 7 | ✗ | `레이저`, `필러` |

**일부 레코드에만 있는 키**

| 레코드 배열 | 건수 | 키=존재수 |
|---|---|---|
| `common_combos` | 8 | `note`=3 |
| `minimum_intervals` | 9 | `min_days`=7, `min_months`=2 |

**관찰** (원장 자체에서 보이는 것. 판정 아님)

- `sequence_order[].categories[]` 19개가 `M15-클렌징`, `M9-HIFU`, `M8-토닝`(코드+라벨 합성), `M11`·`M2`(코드만), `국소마취`·`연고마취`(코드 없음) 세 형식이 섞여 있다. `M15-클렌징`·`M15-도포`·`M15-LED`·`M15-팩` 중 taxonomy 하위 id 로 실존하는 건 `M15-도포`·`M15-팩` 뿐.
- `incompatible_same_day[].pair[]` 는 길이 1~2 배열(1건은 `HA 필러 주입 후 RF/HIFU` 한 문장). 이름은 자유 텍스트(`CO2 프락셔널`, `심부 필링(페놀)`, `이소트레티노인 복용 중`).
- `minimum_intervals` 의 기간 단위가 `min_days`(7건) 와 `min_months`(2건) 로 갈린다. `from`/`to` 는 자유 텍스트(`필러 (별도 세션)`, `필러 (동일 부위 재시술)`).
- `common_combos[].sequence[]` 는 `슈링크 HIFU`, `보톡스 이마/미간`, `ALA 도포·배양` 처럼 제품·부위·단계가 섞인 문장.
- `principles[]` 13개 문장과 treatment-optimization `combination_rules` 가 같은 주제(열시술→주사 순서, 필러→RF 14일)를 다른 문장으로 담고 있다.

## 3. 교차 식별자 표

### 3.1 계열 코드 M1~M17 × 파일 (코드가 값·키·접두로 등장하면 ○)

| 코드 | taxonomy 이름 | combo-recipes | complications | consent-checklist | contraindications | extracted | literature-evidence | market-pricing | patient-education | pih-risk | post-procedure-timeline | pre-procedure-checklist | problem-combos | problem-packages | procedure-comparison | procedure-profiles | products | synergy | taxonomy | treatment-sequence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M1 | 보톡스 | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |  | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| M2 | 필러 | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |  | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| M3 | 바이오스티뮬레이터/콜라겐부스터 |  | ○ | ○ | ○ | ○ | ○ | ○ | ○ |  | ○ | ○ |  | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| M4 | 스킨부스터 | ○ |  | ○ | ○ | ○ | ○ | ○ | ○ |  | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| M5 | PRP/자가혈 | ○ |  | ○ | ○ | ○ | ○ | ○ | ○ |  |  | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| M6 | 지방이식 |  |  | ○ | ○ | ○ | ○ | ○ | ○ |  |  | ○ |  | ○ | ○ | ○ |  | ○ | ○ |  |
| M7 | 실리프팅 | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |  | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |  |
| M8 | 레이저 | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| M9 | 기기 리프팅 | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| M10 | HIFES/EMS |  |  | ○ |  | ○ | ○ | ○ | ○ | ○ |  | ○ |  | ○ | ○ | ○ |  | ○ | ○ |  |
| M11 | 니들RF | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| M12 | 마이크로니들링(MTS) | ○ |  | ○ | ○ | ○ | ○ | ○ | ○ | ○ |  | ○ | ○ | ○ | ○ | ○ |  | ○ | ○ | ○ |
| M13 | 플라즈마 |  |  | ○ |  | ○ | ○ | ○ | ○ | ○ |  | ○ |  |  |  | ○ |  | ○ | ○ |  |
| M14 | 크라이오리포라이시스 |  | ○ | ○ |  | ○ | ○ | ○ | ○ |  |  | ○ |  | ○ | ○ | ○ |  | ○ | ○ |  |
| M15 | 메디컬스킨케어 |  | ○ | ○ |  | ○ | ○ | ○ | ○ | ○ | ○ | ○ |  | ○ | ○ | ○ |  | ○ | ○ | ○ |
| M16 | 수액치료 |  | ○ | ○ |  | ○ | ○ | ○ | ○ | ○ | ○ | ○ |  | ○ |  | ○ |  | ○ | ○ |  |
| M17 | 줄기세포치료 |  |  | ○ |  | ○ | ○ | ○ | ○ | ○ |  | ○ |  |  | ○ | ○ | ○ | ○ | ○ |  |

`anatomy-danger-zones.json`·`treatment-optimization.json` 에는 M/P 코드가 전혀 없다. `pih-risk.json` 의 `notes.M1_to_M7` 은 범위 키라 M1~M7 열에 세지 않았다(위 표의 pih-risk 열은 `procedures[].category`·`procedure_ref` 기준).

### 3.2 고민 코드 P1~P14 × 파일

| 코드 | taxonomy 이름 | taxonomy | problem-packages | problem-combos |
|---|---|---|---|---|
| P1 | 쁘띠시술 | ○ | ○ | ○ |
| P2 | 주름 | ○ | ○ | ○ |
| P3 | 쳐짐 | ○ | ○ | ○ |
| P4 | 항노화 | ○ | ○ | ○ |
| P5 | 색소/미백 | ○ | ○ | ○ |
| P6 | 여드름 | ○ | ○ |  |
| P7 | 모공 | ○ | ○ | ○ |
| P8 | 홍조/혈관 | ○ | ○ |  |
| P9 | 흉터 | ○ | ○ | ○ |
| P10 | 제모 | ○ | ○ |  |
| P11 | 얼굴윤곽 | ○ | ○ | ○ |
| P12 | 바디 | ○ | ○ |  |
| P13 | 두피/탈모 | ○ | ○ |  |
| P14 | 기타 | ○ | ○ |  |

### 3.3 코드가 쓰인 키 경로 (파일별)

| 파일 | 코드가 나오는 경로 (등장 횟수) |
|---|---|
| `combo-recipes.json` | `recipes[].procedures[]` (19) |
| `complications.json` | `categories[].id` (10) |
| `consent-checklist.json` | `categories[].id` (17) |
| `contraindications.json` | `rules[].from` (27)<br>`rules[].to` (27) |
| `extracted.json` | `{code}` (17)<br>`{code}.procedure_id` (17) |
| `literature-evidence.json` | `accuracy_summary.by_category_average.{code}` (7)<br>`categories.{code}` (17) |
| `market-pricing.json` | `categories[].id` (17) |
| `patient-education.json` | `categories[].id` (17) |
| `pih-risk.json` | `notes.{code}` (4)<br>`procedures[].category` (26)<br>`procedures[].procedure_ref` (26) |
| `post-procedure-timeline.json` | `timelines[].category` (10) |
| `pre-procedure-checklist.json` | `category_specific[].id` (17) |
| `problem-combos.json` | `combos[].packages[].procedures[]` (63)<br>`combos[].problem_id` (8)<br>`combos[].packages[].id` (24) |
| `problem-packages.json` | `problems[].complaints[].procedures[].category` (254)<br>`problems[].problem_id` (14) |
| `procedure-comparison.json` | `comparisons[].procedures[].category` (39) |
| `procedure-profiles.json` | `profiles[].id` (17) |
| `products.json` | `botulinum_toxin.category_id` (1)<br>`filler_ha.category_id` (1)<br>`biostimulator.category_id` (1)<br>`skin_booster.category_id` (1)<br>`prp_exosome.category_id` (1)<br>`thread_lift.category_id` (1)<br>`energy_device.category_id[]` (3)<br>`stem_cell.category_id` (1) |
| `synergy.json` | `links[].from` (115)<br>`links[].from_category` (115)<br>`links[].to` (115)<br>`links[].to_category` (115) |
| `taxonomy.json` | `modality[].id` (17)<br>`modality[].products[].id` (59)<br>`problem[].subcategories[].items[].modality_ref[]` (105)<br>`modality[].subcategories[].id` (66)<br>`modality[].subcategories[].items[].id` (128)<br>`modality[].subcategories[].items[].canonical_category` (6)<br>`modality[].subcategories[].items[].reclassified_to` (1)<br>`problem[].id` (14)<br>`problem[].subcategories[].id` (53) |
| `treatment-sequence.json` | `sequence_order[].categories[]` (17) |

### 3.4 계열 코드 → 이름 표기 (파일별로 코드 옆에 붙은 이름을 그대로)

| 코드 | taxonomy | 파일별 표기 |
|---|---|---|
| M1 | 보톡스 | complications: `보톡스`<br>consent-checklist: `보톡스`<br>contraindications: `보톡스`<br>extracted: `보톡스` / `BOTOX`<br>literature-evidence: `Botulinum toxin type A (aesthetic)`<br>market-pricing: `보톡스`<br>patient-education: `보톡스`<br>post-procedure-timeline: `보톡스`<br>pre-procedure-checklist: `보톡스`<br>problem-packages: `보톡스`<br>procedure-comparison: `보톡스 (보툴리눔톡신)`<br>procedure-profiles: `보톡스`<br>synergy: `보톡스` / `사각턱보톡스` / `보톡스(코끝)`<br>taxonomy: `보톡스` |
| M2 | 필러 | complications: `필러`<br>consent-checklist: `필러`<br>contraindications: `필러`<br>extracted: `필러` / `FILLER`<br>literature-evidence: `Hyaluronic acid dermal fillers`<br>market-pricing: `필러`<br>patient-education: `필러`<br>post-procedure-timeline: `HA 필러`<br>pre-procedure-checklist: `필러`<br>problem-packages: `필러`<br>procedure-comparison: `히알루론산 필러`<br>procedure-profiles: `필러`<br>synergy: `필러` / `턱필러` / `코필러`<br>taxonomy: `필러` |
| M3 | 바이오스티뮬레이터/콜라겐부스터 | complications: `바이오스티뮬레이터/콜라겐부스터`<br>consent-checklist: `바이오스티뮬레이터/콜라겐부스터`<br>contraindications: `바이오스티뮬레이터/콜라겐부스터`<br>extracted: `바이오스티뮬레이터` / `BIOSTIMULATOR`<br>literature-evidence: `Collagen-stimulating biostimulators (PLLA/CaHA/PDLLA/PCL)`<br>market-pricing: `바이오스티뮬레이터/콜라겐부스터`<br>patient-education: `바이오스티뮬레이터/콜라겐부스터`<br>post-procedure-timeline: `바이오스티뮬레이터/콜라겐부스터`<br>pre-procedure-checklist: `바이오스티뮬레이터/콜라겐부스터`<br>problem-packages: `바이오스티뮬레이터/콜라겐부스터`<br>procedure-comparison: `스컬트라 (PLLA)` / `엘란쎄 (PCL)` / `바이오스티뮬레이터 (쥬베룩볼륨)`<br>procedure-profiles: `바이오스티뮬레이터/콜라겐부스터`<br>synergy: `엘란쎄` / `래디어스` / `스컬트라` / `바이오스티뮬레이터`<br>taxonomy: `바이오스티뮬레이터/콜라겐부스터` |
| M4 | 스킨부스터 | consent-checklist: `스킨부스터`<br>contraindications: `스킨부스터`<br>extracted: `스킨부스터` / `SKINBOOSTER`<br>literature-evidence: `Skinboosters and mesotherapy (non-crosslinked HA, polynucleotides, amino-acid/vitamin cocktails)`<br>market-pricing: `스킨부스터`<br>patient-education: `스킨부스터`<br>post-procedure-timeline: `스킨부스터`<br>pre-procedure-checklist: `스킨부스터`<br>problem-packages: `스킨부스터`<br>procedure-comparison: `리쥬란 (PN주사)` / `스킨부스터 (쥬베룩/리쥬란)` / `물광주사 (메소테라피)`<br>procedure-profiles: `스킨부스터`<br>synergy: `스킨부스터` / `리쥬란` / `쥬베룩`<br>taxonomy: `스킨부스터 > 비가교 HA 메조테라피` / `스킨부스터 > 재생형 메조테라피` / `스킨부스터 > 콜라겐 혼합 메조테라피` / `스킨부스터` |
| M5 | PRP/자가혈 | consent-checklist: `PRP/자가혈`<br>contraindications: `PRP/자가혈`<br>extracted: `PRP 피부재생술` / `PRP`<br>literature-evidence: `Platelet-rich plasma (PRP) and exosome therapies`<br>market-pricing: `PRP/엑소좀`<br>patient-education: `PRP/자가혈`<br>pre-procedure-checklist: `PRP/자가혈`<br>problem-packages: `PRP/자가혈` / `PRP`<br>procedure-comparison: `PRP (자가혈 재생)`<br>procedure-profiles: `PRP/엑소좀`<br>synergy: `PRP`<br>taxonomy: `PRP/자가혈` |
| M6 | 지방이식 | consent-checklist: `지방이식`<br>contraindications: `지방이식`<br>extracted: `지방이식` / `FATGRAFT`<br>literature-evidence: `Autologous fat grafting / lipotransfer for facial rejuvenation`<br>market-pricing: `지방이식`<br>patient-education: `지방이식`<br>pre-procedure-checklist: `지방이식`<br>problem-packages: `지방이식`<br>procedure-comparison: `자가지방이식`<br>procedure-profiles: `지방이식`<br>synergy: `지방이식`<br>taxonomy: `지방이식` |
| M7 | 실리프팅 | complications: `실리프팅`<br>consent-checklist: `실리프팅`<br>contraindications: `실리프팅`<br>extracted: `실리프팅` / `THREADLIFT`<br>literature-evidence: `Absorbable suspension threads (PDO/PLLA/PCL) for facial lifting`<br>market-pricing: `실리프팅`<br>patient-education: `실리프팅`<br>post-procedure-timeline: `실리프팅`<br>pre-procedure-checklist: `실리프팅`<br>problem-packages: `실리프팅`<br>procedure-comparison: `실리프팅 (PDO코그)`<br>procedure-profiles: `실리프팅`<br>synergy: `실리프팅`<br>taxonomy: `실리프팅` |
| M8 | 레이저 | complications: `레이저`<br>consent-checklist: `레이저`<br>contraindications: `레이저`<br>extracted: `레이저` / `LASER`<br>literature-evidence: `Aesthetic lasers and IPL`<br>market-pricing: `레이저`<br>patient-education: `레이저`<br>pih-risk: `레이저 토닝 (QS Nd:YAG 1064nm 저에너지)` / `QS Nd:YAG 1064nm (표준 에너지, 색소 치료)` / `피코토닝 (피코초 Nd:YAG 1064nm)` / `피코슈어 (755nm 피코초)` / `CO2 프락셔널 (10600nm, 박리성)` / `어븀야그(Er:YAG) 프락셔널 (2940nm, 박리성)` / `프락셀듀얼 (1550+1927nm, 비박리~얕은 박리)` / `피코프락셀 (비박리성 피코초)` / `피코슈어 프락셀 (755nm 비박리성)` / `IPL (560-950nm 광대역)` / `브이빔 (PDL 595nm)` / `엑셀브이/더마브이 (LP 532+1064nm)` / `장파장 제모 (Nd:YAG 1064nm LP)` / `알렉산드라이트 제모 (755nm LP)` / `다이오드 제모 (800-810nm LP)`<br>post-procedure-timeline: `프락셔널 CO2 레이저`<br>pre-procedure-checklist: `레이저`<br>problem-packages: `레이저` / `혈관레이저` / `프락셔널` / `서브시전` / `제모레이저` / `피코레이저`<br>procedure-comparison: `프락셀 (프랙셔널 레이저)` / `CO2 프랙셔널 레이저` / `피코 프랙셔널` / `피코토닝` / `Q-스위치 Nd:YAG` / `레이저토닝 (저출력 Nd:YAG)` / `알렉산드라이트 (755nm)` / `다이오드 (808nm/810nm)` / `Nd:YAG (1064nm)` / `스컬프슈어 (레이저 지방분해)` / `PDT (광역동치료)` / `제네시스 (Nd:YAG 롱펄스)`<br>procedure-profiles: `레이저`<br>synergy: `레이저토닝` / `저출력레이저(두피)` / `프락셔널` / `서브시전` / `피코슈어` / `피코웨이` / `피코토닝` / `혈관레이저` / `알렉산드라이트` / `다이오드` / `IPL` / `CO2레이저`<br>taxonomy: `레이저`<br>treatment-sequence: `IPL` / `토닝` / `프락셔널` / `혈관` |
| M9 | 기기 리프팅 | complications: `기기 리프팅`<br>consent-checklist: `기기 리프팅`<br>contraindications: `기기 리프팅`<br>extracted: `기기리프팅` / `DEVICELIFT`<br>literature-evidence: `Non-invasive skin tightening: HIFU and radiofrequency`<br>market-pricing: `에너지기기(HIFU/RF)`<br>patient-education: `기기 리프팅`<br>pih-risk: `HIFU (울쎄라, 슈링크 등)` / `써마지/올리지오 (모노폴라 RF)` / `인모드 (바이폴라 RF + IPL/다이오드)`<br>post-procedure-timeline: `HIFU/RF 리프팅`<br>pre-procedure-checklist: `기기 리프팅`<br>problem-packages: `리프팅기기` / `인모드` / `미라드라이`<br>procedure-comparison: `울쎄라 (HIFU)` / `써마지FLX (RF)` / `IPL (광선치료)` / `IPL 제모` / `바넬라 (고주파 바디)`<br>procedure-profiles: `에너지기기(HIFU/RF)`<br>synergy: `리프팅기기` / `인모드(바디)` / `써마지` / `울쎄라` / `더블로` / `볼뉴머` / `슈링크` / `올리지오` / `인모드`<br>taxonomy: `SIG` / `기기 리프팅`<br>treatment-sequence: `HIFU` / `RF` |
| M10 | HIFES/EMS | consent-checklist: `HIFES/EMS`<br>extracted: `HIFES/EMS` / `HIFES`<br>literature-evidence: `HIFEM/HIFES and EMS`<br>market-pricing: `HIFES/EMS`<br>patient-education: `HIFES/EMS`<br>pre-procedure-checklist: `HIFES/EMS`<br>problem-packages: `HIFES`<br>procedure-comparison: `리포셀 (HIFU 지방)`<br>procedure-profiles: `HIFES/EMS`<br>synergy: `HIFES` / `HIFES(바디)`<br>taxonomy: `HIFES/EMS` |
| M11 | 니들RF | complications: `니들RF`<br>consent-checklist: `니들RF`<br>contraindications: `니들RF`<br>extracted: `니들RF` / `NEEDLERF`<br>literature-evidence: `Fractional radiofrequency microneedling (RF microneedling)`<br>market-pricing: `니들RF`<br>patient-education: `니들RF`<br>pih-risk: `니들RF - 절연침 (포텐자, 시크릿RF 등)` / `니들RF - 비절연침`<br>post-procedure-timeline: `니들RF (미세침 고주파)`<br>pre-procedure-checklist: `니들RF`<br>problem-packages: `니들RF`<br>procedure-comparison: `인모드FX (RF마이크로니들)` / `마이크로니들RF (시크릿/인모드)` / `아그네스 (RF 니들 피지선)`<br>procedure-profiles: `니들RF`<br>synergy: `포텐자` / `시크릿` / `인트라셀` / `니들RF`<br>taxonomy: `니들RF` |
| M12 | 마이크로니들링(MTS) | consent-checklist: `마이크로니들링(MTS)`<br>contraindications: `마이크로니들링(MTS)`<br>extracted: `MTS (마이크로니들 치료)` / `MTS`<br>literature-evidence: `Microneedling / percutaneous collagen induction (non-RF)`<br>market-pricing: `마이크로니들링(MTS)`<br>patient-education: `마이크로니들링(MTS)`<br>pih-risk: `마이크로니들링 (MTS, 더마롤러/더마펜)`<br>pre-procedure-checklist: `마이크로니들링(MTS)`<br>problem-packages: `마이크로니들링(MTS)`<br>procedure-comparison: `MTS (더마펜/더마스탬프)`<br>procedure-profiles: `마이크로니들링(MTS)`<br>synergy: `MTS` / `MTS(두피)`<br>taxonomy: `마이크로니들링(MTS)` |
| M13 | 플라즈마 | consent-checklist: `플라즈마`<br>extracted: `플라즈마` / `PLASMA`<br>literature-evidence: `Plasma skin treatment`<br>market-pricing: `플라즈마`<br>patient-education: `플라즈마`<br>pih-risk: `플라즈마 (콜드플라즈마)` / `플라즈마 (열플라즈마/플렉서)`<br>pre-procedure-checklist: `플라즈마`<br>procedure-profiles: `플라즈마`<br>synergy: `플라즈마`<br>taxonomy: `플라즈마` |
| M14 | 크라이오리포라이시스 | complications: `크라이오리포라이시스`<br>consent-checklist: `크라이오리포라이시스`<br>extracted: `크라이오리포라이시스` / `CRYO`<br>literature-evidence: `Cryolipolysis`<br>market-pricing: `크라이오리포라이시스`<br>patient-education: `크라이오리포라이시스`<br>pre-procedure-checklist: `크라이오리포라이시스`<br>problem-packages: `크라이오` / `지방분해`<br>procedure-comparison: `쿨스컬프팅 (냉동지방분해)`<br>procedure-profiles: `크라이오리포라이시스`<br>synergy: `크라이오`<br>taxonomy: `크라이오리포라이시스` |
| M15 | 메디컬스킨케어 | complications: `메디컬스킨케어`<br>consent-checklist: `메디컬스킨케어`<br>extracted: `메디컬스킨케어` / `SKINCARE`<br>literature-evidence: `Topical cosmeceuticals`<br>market-pricing: `메디컬스킨케어`<br>patient-education: `메디컬스킨케어`<br>pih-risk: `AHA/BHA 필링 (표재성)` / `TCA 필링 (중간-심층)` / `제스너 필링`<br>post-procedure-timeline: `케미컬 필링 (중간 깊이)`<br>pre-procedure-checklist: `메디컬스킨케어`<br>problem-packages: `반영구화장` / `메디컬스킨케어` / `병변내 스테로이드주사` / `약물치료` / `모발이식`<br>procedure-comparison: `실리콘피부관리 (아쿠아필/하이드라)` / `살리실릭 필링` / `압출+스킨스케일링`<br>procedure-profiles: `메디컬스킨케어`<br>synergy: `필링` / `메디컬스킨케어`<br>taxonomy: `도포` / `팩` / `메디컬스킨케어`<br>treatment-sequence: `클렌징` / `도포` / `LED` / `팩` |
| M16 | 수액치료 | complications: `수액치료`<br>consent-checklist: `수액치료`<br>extracted: `수액치료` / `IVTHERAPY`<br>literature-evidence: `Intravenous micronutrient / antioxidant therapy (aesthetic)`<br>market-pricing: `수액치료`<br>patient-education: `수액치료`<br>post-procedure-timeline: `DCA`<br>pre-procedure-checklist: `수액치료`<br>problem-packages: `수액` / `미백주사`<br>procedure-profiles: `수액치료`<br>synergy: `수액치료`<br>taxonomy: `수액치료 > 항산화·미백 IV` / `수액치료 > 비타민 B 계열` / `수액치료 > 항산화 IV` / `DCA` / `LIPO` / `수액치료` |
| M17 | 줄기세포치료 | consent-checklist: `줄기세포치료`<br>extracted: `줄기세포치료` / `STEMCELL`<br>literature-evidence: `Stem cells and stem cell-derived products`<br>market-pricing: `줄기세포치료`<br>patient-education: `줄기세포치료`<br>pre-procedure-checklist: `줄기세포치료`<br>procedure-comparison: `엑소좀 (줄기세포 유래)`<br>procedure-profiles: `줄기세포치료`<br>synergy: `엑소좀` / `줄기세포`<br>taxonomy: `줄기세포치료` |

### 3.5 제품명 교차

`products.json` 섹션 vs `taxonomy.json › modality[].products`:

| 섹션 | category_id | 공통 | products.json 에만 | taxonomy 에만 |
|---|---|---|---|---|
| botulinum_toxin | M1 | 10 | 티엠버스 | 타임버스 |
| filler_ha | M2 | 7 | — | 신펄 |
| biostimulator | M3 | 6 | — | — |
| skin_booster | M4 | 5 | — | — |
| thread_lift | M7 | 5 | — | — |
| energy_device | ['M8', 'M9', 'M11'] | 17 | 볼뉴머 | — |
| prp_exosome | M5 | 5 | — | — |
| stem_cell | M17 | 2 | — | — |

`problem-packages.json › procedures[].products[]` 34종의 소재:

| 제품명 | 횟수 | products.json | taxonomy products | taxonomy items |
|---|---|---|---|---|
| 쥬베룩 | 32 | ○ | ○ | ○ |
| 리쥬란 힐러 | 32 | ○ | ○ |  |
| 보톡스 | 28 | ○ | ○ |  |
| 나보타 | 26 | ○ | ○ | ○ |
| 리쥬란 HB+ | 20 | ○ | ○ |  |
| 셀피아 | 18 | ○ | ○ |  |
| 포텐자 | 18 | ○ | ○ | ○ |
| 울쎄라 | 17 | ○ | ○ | ○ |
| 쥬비덤 | 16 | ○ | ○ | ○ |
| 레스틸렌 | 15 | ○ | ○ | ○ |
| 보툴렉스 | 15 | ○ | ○ | ○ |
| 써마지FLX | 15 | ○ | ○ | ○ |
| 리젠ACR | 13 | ○ | ○ |  |
| 피코슈어 | 11 | ○ | ○ | ○ |
| 프락셀 | 10 | ○ | ○ |  |
| 인모드 | 10 | ○ | ○ | ○ |
| 슈링크유니버스 | 9 | ○ | ○ | ○ |
| 피코웨이 | 9 | ○ | ○ |  |
| 시크릿 | 9 | ○ | ○ |  |
| 민트리프트 | 7 | ○ | ○ | ○ |
| 테스리프트 | 7 | ○ | ○ | ○ |
| 엑셀V | 7 | ○ | ○ |  |
| 제니스 | 6 | ○ | ○ |  |
| 인트라셀 | 6 | ○ | ○ |  |
| 이브아르 | 5 | ○ | ○ | ○ |
| 스컬트라 | 5 | ○ | ○ | ○ |
| 엘란쎄 | 5 | ○ | ○ | ○ |
| 클라리티2 | 4 | ○ | ○ | ○ |
| 헤어맥스(LLLT) | 3 |  |  |  |
| 실루엣소프트 | 2 | ○ | ○ | ○ |
| 트리암시놀론(±5-FU) | 2 |  |  |  |
| PDL(V빔) | 2 |  |  |  |
| 올리지오 | 2 | ○ | ○ | ○ |
| CO2레이저 | 2 |  |  |  |

`problem-combos.json › packages[].products[]` 는 조합 문장 1개씩(24건)으로 제품명 단위가 아니다:

- `나보타 or 보툴렉스` ×2
- `나보타 + 쥬비덤 or 이브아르`
- `보톡스(엘러간) + 쥬비덤 + 리쥬란`
- `나보타 + 쥬비덤/이브아르 + 리쥬란`
- `보톡스(엘러간) + 쥬비덤 + 울쎄라 + 리쥬란`
- `실루엣소프트 + 울쎄라 + 보톡스(엘러간) + 쥬비덤 + 리쥬란`
- `슈링크유니버스 or 더블로골드`
- `울쎄라 + 보톡스(엘러간) or 나보타`
- `울쎄라 + 보톡스(엘러간) + 쥬비덤 + 리쥬란`
- `실루엣소프트 + 울쎄라 + 쥬비덤 + 보톡스(엘러간)`
- `리쥬란 힐러`
- `MTS + 자가 PRP + 리쥬란`
- `피코레이저/프락셀 + MTS + PRP + 리쥬란`
- `피코슈어 or 레블라이트 or 클라리티`
- `피코레이저 + PRP + 리쥬란`
- `피코슈어/피코웨이 + 포텐자 + PRP + 리쥬란`
- `나보타(희석) + 레이저 토닝`
- `포텐자/인트라셀 + PRP`
- `포텐자 + 피코레이저 + PRP + 리쥬란`
- `프락셀 or CO2 프락셔널`
- `프락셀 + 포텐자/인트라셀 + PRP`
- `나보타(교근) + 이브아르(턱)`
- `울쎄라(HIFU) 또는 올리지오(모노폴라 RF) + 보톡스 + 쥬비덤`

### 3.6 하위 코드 참조

`pih-risk.json › procedure_ref` → taxonomy:

| procedure_ref | pih name | taxonomy 항목? | taxonomy 하위분류? | taxonomy 항목 이름 |
|---|---|---|---|---|
| M8-1-1 | 레이저 토닝 (QS Nd:YAG 1064nm 저에너지) | ○ |  | 레이저토닝 |
| M8-1-1 | QS Nd:YAG 1064nm (표준 에너지, 색소 치료) | ○ |  | 레이저토닝 |
| M8-1-2 | 피코토닝 (피코초 Nd:YAG 1064nm) | ○ |  | 피코토닝 |
| M8-1-3 | 피코슈어 (755nm 피코초) | ○ |  | 피코슈어 |
| M8-2-1 | CO2 프락셔널 (10600nm, 박리성) | ○ |  | CO2프락셔널 |
| M8-2-3 | 어븀야그(Er:YAG) 프락셔널 (2940nm, 박리성) | ○ |  | 어븀야그 프락셔널 |
| M8-2-4 | 프락셀듀얼 (1550+1927nm, 비박리~얕은 박리) | ○ |  | 프락셀듀얼 |
| M8-2-5 | 피코프락셀 (비박리성 피코초) | ○ |  | 피코프락셀 |
| M8-2-6 | 피코슈어 프락셀 (755nm 비박리성) | ○ |  | 피코슈어 프락셀 |
| M8-3-1 | IPL (560-950nm 광대역) | ○ |  | IPL |
| M8-4-1 | 브이빔 (PDL 595nm) | ○ |  | 브이빔 |
| M8-4-2 | 엑셀브이/더마브이 (LP 532+1064nm) | ○ |  | 엑셀브이 |
| M8-5 | 장파장 제모 (Nd:YAG 1064nm LP) |  | ○ | — |
| M8-5-3 | 알렉산드라이트 제모 (755nm LP) | ○ |  | 젠틀맥스프로+ |
| M8-5 | 다이오드 제모 (800-810nm LP) |  | ○ | — |
| M9-1 | HIFU (울쎄라, 슈링크 등) |  | ○ | — |
| M9-2 | 써마지/올리지오 (모노폴라 RF) |  | ○ | — |
| M9-2-5 | 인모드 (바이폴라 RF + IPL/다이오드) | ○ |  | 인모드 |
| M11-1 | 니들RF - 절연침 (포텐자, 시크릿RF 등) |  | ○ | — |
| M11-1 | 니들RF - 비절연침 |  | ○ | — |
| M12 | 마이크로니들링 (MTS, 더마롤러/더마펜) |  |  | — |
| M13 | 플라즈마 (콜드플라즈마) |  |  | — |
| M13 | 플라즈마 (열플라즈마/플렉서) |  |  | — |
| M15-1-1 | AHA/BHA 필링 (표재성) | ○ |  | AHA/BHA 필링 |
| M15-1-2 | TCA 필링 (중간-심층) | ○ |  | TCA 필링 |
| M15-1 | 제스너 필링 |  | ○ | — |

중복 ref: `M8-1-1`×2, `M8-5`×2, `M11-1`×2, `M13`×2

`problem-combos.json › packages[].id` 와 같은 문자열의 taxonomy problem 하위분류:

| package id | package name | taxonomy 하위분류 label(같은 id) |
|---|---|---|
| P1-1 | 보톡스 단독 | 코 |
| P1-2 | 보톡스 + 필러 | 이마/관자놀이 |
| P1-3 | 수입 보톡스 + 수입 필러 + 스킨부스터 | 턱/턱선 |
| P2-1 | 보톡스 기본 | 표정주름 |
| P2-2 | 보톡스 + 필러 + 스킨부스터 | 깊은주름 |
| P2-3 | 보톡스 + 필러 + HIFU + 스킨부스터 | 잔주름 |
| P2-4 | 실리프팅 + HIFU + 보톡스 + 필러 + 스킨부스터 | (없음) |
| P3-1 | 국산 HIFU 리프팅 | 얼굴 쳐짐 |
| P3-2 | 울쎄라 + 보톡스 | 눈가 쳐짐 |
| P3-3 | 울쎄라 + 보톡스 + 필러 + 스킨부스터 | 바디 쳐짐 |
| P3-4 | 실리프팅 + 울쎄라 + 필러 + 보톡스 | (없음) |
| P4-1 | 스킨부스터 단독 | 피부재생/탄력 |
| P4-2 | MTS + PRP + 스킨부스터 (골든루틴) | 볼륨회복 |
| P4-3 | 레이저 + MTS + PRP + 스킨부스터 | 전신항노화 |
| P5-1 | 레이저 토닝 | 기미 |
| P5-2 | 레이저 토닝 + PRP + 스킨부스터 | 주근깨/잡티 |
| P5-3 | 피코레이저 + 니들RF + PRP + 스킨부스터 | 오타모반/ABNOM |
| P7-1 | 스킨보톡스 + 레이저 | 피지과다형 |
| P7-2 | 니들RF + PRP | 탄력저하형 |
| P7-3 | 니들RF + 레이저 + PRP + 스킨부스터 | 흉터형(열린모공) |
| P9-1 | 프락셔널 레이저 | 여드름흉터 |
| P9-2 | 프락셔널 + 니들RF + PRP | 켈로이드/비후성 |
| P11-1 | 사각턱 보톡스 + 턱필러 | 사각턱 |
| P11-2 | 보톡스 + 필러 + 리프팅(HIFU 또는 고주파) | 이중턱/턱밑 |

`treatment-sequence.json › sequence_order[].categories[]` 값: `M15-클렌징`, `국소마취`, `연고마취`, `M9-HIFU`, `M9-RF`, `M8-IPL`, `M8-토닝`, `M8-프락셔널`, `M8-혈관`, `M11`, `M12`, `M2`, `M3`, `M4`, `M1`, `M5`, `M15-도포`, `M15-LED`, `M15-팩`

`post-procedure-timeline.json › timelines[]` (category:name):

- M1:보톡스 (id=botox)
- M2:HA 필러 (id=ha-filler)
- M9:HIFU/RF 리프팅 (id=hifu-rf)
- M8:프락셔널 CO2 레이저 (id=fractional-co2)
- M7:실리프팅 (id=thread-lift)
- M16-DCA:DCA 지방분해 주사 (id=dca-injection)
- M11:니들RF (미세침 고주파) (id=needle-rf)
- M4:스킨부스터 (id=skin-booster)
- M3:바이오스티뮬레이터/콜라겐부스터 (id=biostimulator)
- M15:케미컬 필링 (중간 깊이) (id=chemical-peel-mid)

### 3.7 `extracted.json` vs `taxonomy.json › modality[].extracted`

| 코드 | 본문 동일 | 다른 키 | extracted.json 에만 있는 키 |
|---|---|---|---|
| M1 | ○ | — | extracted_at, guardrail_version, name, name_en, procedure_id, source, source_type |
| M2 | ✗ | aftercare, indications, mechanism, safety | extracted_at, guardrail_version, name, name_en, procedure_id, source, source_type |
| M3 | ✗ | aftercare | extracted_at, guardrail_version, name, name_en, procedure_id, source, source_type, updated |
| M4 | ○ | — | extracted_at, guardrail_version, name, name_en, procedure_id, source, source_type |
| M5 | ✗ | aftercare, mechanism | extracted_at, guardrail_version, name, name_en, procedure_id, source, source_type |
| M6 | ○ | — | extracted_at, guardrail_version, name, name_en, procedure_id, source, source_type |
| M7 | ○ | — | extracted_at, guardrail_version, name, name_en, procedure_id, source, source_type |
| M8 | ✗ | safety | extracted_at, guardrail_version, name, name_en, procedure_id, source, source_type |
| M9 | ○ | — | extracted_at, guardrail_version, name, name_en, procedure_id, source, source_type |
| M10 | ✗ | safety | extracted_at, guardrail_version, name, name_en, procedure_id, source, source_type |
| M11 | ○ | — | extracted_at, guardrail_version, name, name_en, procedure_id, source, source_type |
| M12 | ✗ | mechanism, overview | extracted_at, guardrail_version, name, name_en, procedure_id, source, source_type |
| M13 | ✗ | safety | extracted_at, guardrail_version, name, name_en, procedure_id, source, source_type |
| M14 | ○ | — | extracted_at, guardrail_version, name, name_en, procedure_id, source, source_type |
| M15 | ○ | — | extracted_at, guardrail_version, name, name_en, procedure_id, source, source_type |
| M16 | ○ | — | extracted_at, guardrail_version, name, name_en, procedure_id, source, source_type |
| M17 | ✗ | mechanism, overview | extracted_at, guardrail_version, name, name_en, procedure_id, source, source_type |

### 3.8 `problem-packages.json › cc` vs `taxonomy.json › problem 항목`

- taxonomy 항목 115 / packages cc 113 (problem_id+이름 쌍 기준)
- taxonomy 에만: P4:줄기세포치료, P8:경화요법
- packages 에만: 없음
- cc_group ≠ taxonomy label: P9 `니들RF` — packages `여드름흉터` / taxonomy `튼살`
- cc_group ≠ taxonomy label: P9 `프락셔널레이저` — packages `수술흉터/화상흉터` / taxonomy `튼살`
- problem-combos 가 다루는 고민: P1 쁘띠시술, P2 주름, P3 처짐/탄력(taxonomy: 쳐짐), P4 피부결/톤/항노화(taxonomy: 항노화), P5 색소/미백, P7 모공, P9 흉터, P11 얼굴윤곽; 없는 고민: P6:여드름, P8:홍조/혈관, P10:제모, P12:바디, P13:두피/탈모, P14:기타

`problem-packages.json › procedures[].name` → category 코드 (한 코드에 여러 이름):

| name | 횟수 | category | taxonomy category 이름 |
|---|---|---|---|
| 스킨부스터 | 47 | M4 | 스킨부스터 |
| 보톡스 | 28 | M1 | 보톡스 |
| 레이저 | 19 | M8 | 레이저 |
| 필러 | 18 | M2 | 필러 |
| 니들RF | 18 | M11 | 니들RF |
| PRP/자가혈 | 17 | M5 | PRP/자가혈 |
| 리프팅기기 | 17 | M9 | 기기 리프팅 |
| 프락셔널 | 10 | M8 | 레이저 |
| 인모드 | 10 | M9 | 기기 리프팅 |
| 크라이오 | 8 | M14 | 크라이오리포라이시스 |
| 실리프팅 | 7 | M7 | 실리프팅 |
| 서브시전 | 6 | M8 | 레이저 |
| 마이크로니들링(MTS) | 6 | M12 | 마이크로니들링(MTS) |
| 바이오스티뮬레이터/콜라겐부스터 | 5 | M3 | 바이오스티뮬레이터/콜라겐부스터 |
| 혈관레이저 | 5 | M8 | 레이저 |
| 반영구화장 | 4 | M15 | 메디컬스킨케어 |
| 제모레이저 | 4 | M8 | 레이저 |
| 지방이식 | 3 | M6 | 지방이식 |
| 메디컬스킨케어 | 3 | M15 | 메디컬스킨케어 |
| 지방분해 | 3 | M14 | 크라이오리포라이시스 |
| 약물치료 | 3 | M15 | 메디컬스킨케어 |
| 수액 | 2 | M16 | 수액치료 |
| 미백주사 | 2 | M16 | 수액치료 |
| 병변내 스테로이드주사 | 2 | M15 | 메디컬스킨케어 |
| HIFES | 2 | M10 | HIFES/EMS |
| 모발이식 | 2 | M15 | 메디컬스킨케어 |
| PRP | 1 | M5 | PRP/자가혈 |
| 피코레이저 | 1 | M8 | 레이저 |
| 미라드라이 | 1 | M9 | 기기 리프팅 |

### 3.9 시술명이 자유 텍스트인 자리

- `synergy.json` 노드 52종: `M1-보톡스`, `M1-사각턱보톡스`, `M1-보톡스(코끝)`, `M2-필러`, `M2-턱필러`, `M2-코필러`, `M3-엘란쎄`, `M3-래디어스`, `M3-스컬트라`, `M3-바이오스티뮬레이터`, `M4-스킨부스터`, `M4-리쥬란`, `M4-쥬베룩`, `M5-PRP`, `M6-지방이식`, `M7-실리프팅`, `M8-레이저토닝`, `M8-저출력레이저(두피)`, `M8-프락셔널`, `M8-서브시전`, `M8-피코슈어`, `M8-피코웨이`, `M8-피코토닝`, `M8-혈관레이저`, `M8-알렉산드라이트`, `M8-다이오드`, `M8-IPL`, `M8-CO2레이저`, `M9-리프팅기기`, `M9-인모드(바디)`, `M9-써마지`, `M9-울쎄라`, `M9-더블로`, `M9-볼뉴머`, `M9-슈링크`, `M9-올리지오`, `M9-인모드`, `M10-HIFES`, `M10-HIFES(바디)`, `M11-포텐자`, `M11-시크릿`, `M11-인트라셀`, `M11-니들RF`, `M12-MTS`, `M12-MTS(두피)`, `M13-플라즈마`, `M14-크라이오`, `M15-필링`, `M15-메디컬스킨케어`, `M16-수액치료`, `M17-엑소좀`, `M17-줄기세포`
- `treatment-optimization.json › optimal_combo[]` 57종: `스킨부스터`, `필러`, `바이오스티뮬레이터`, `레이저토닝`, `보톡스`, `프락셔널 레이저`, `MTS/니들RF`, `CO2 프락셔널`, `피코토닝`, `카복시테라피`, `스킨부스터(리쥬란)`, `HIFU/RF`, `써마지/RF`, `HIFU(슈링크/울쎄라)`, `보톡스(턱선/광대)`, `울쎄라 HIFU`, `실리프팅(PDO/PCL)`, `HA 볼류마이징 스킨부스터`, `바이오스티뮬레이터(쥬베룩)`, `HA 필러`, `바이오스티뮬레이터(스컬트라/엘란쎄)`, `HA 필러(딥)`, `CaHA(레디에스)`, `지방이식`, `필링(약한 산)`, `PRP (엑소좀은 보조·근거 제한적)`, `니들RF`, `IPL`, `비타민C 이온토포레시스`, `트라넥삼산(경구/국소)`, `스킨부스터(미백성분)`, `저출력 IPL(병용 보조)`, `저출력 피코토닝`, `트라넥삼산(경구+주사)`, `마이크로니들링+미백약물`, `ALA-PDT`, `필링(살리실산/글리콜산)`, `LED(블루라이트)`, `서브시전(subcision)`, `PRP`, `서브시전`, `필러(HA/CaHA)`, `TCA Cross`, `PRP/엑소좀`, `다이오드 레이저(810nm)`, `알렉산드라이트(755nm)`, `다이오드(810nm)`, `듀얼파장(알렉+다이오드 or 다이오드+Nd:YAG)`, `IPL(유지)`, `크라이오(냉동지방분해)`, `고주파 바디 RF`, `지방분해주사(데옥시콜산)`, `크라이오`, `바디 RF`, `지방흡입(리포)`, `바디 HIFU(리포셀)`, `RF 타이트닝`
- `treatment-optimization.json › by_age_group[].recommended_base[]`: `HIFU(울쎄라급)`, `HIFU/RF`, `IPL`, `LED`, `바이오스티뮬레이터`, `보톡스`, `스킨부스터`, `실리프팅`, `토닝`, `필러`, `필링`
- `treatment-sequence.json › incompatible_same_day[].pair[]`: `CO2 프락셔널 ↔ 필러`, `심부 필링(페놀) ↔ 레이저`, `PDO실 ↔ 비가교HA`, `이소트레티노인 복용 중 ↔ 프락셔널/필링`, `HA 필러 주입 후 RF/HIFU`, `HA 필러 ↔ 레이저`, `심부 필링(TCA 50%+/페놀) ↔ 모든 시술`, `이소트레티노인 복용 중 ↔ 프락셔널 레이저`, `이소트레티노인 복용 중 ↔ 케미컬 필링`
- `treatment-sequence.json › minimum_intervals[]` from→to: `HA 필러` → `RF/HIFU`, `HA 필러` → `레이저`, `이소트레티노인` → `프락셔널/얕은 필링`, `이소트레티노인` → `박리성(ablative) 레이저/심부 필링`, `심부 필링` → `레이저`, `프락셔널 CO2` → `필러`, `보톡스` → `필러 (별도 세션)`, `RF/HIFU` → `필러`, `필러` → `필러 (동일 부위 재시술)`
- `procedure-comparison.json › procedures[].name` 39종 (category): `울쎄라 (HIFU)`(M9), `써마지FLX (RF)`(M9), `실리프팅 (PDO코그)`(M7), `인모드FX (RF마이크로니들)`(M11), `보톡스 (보툴리눔톡신)`(M1), `히알루론산 필러`(M2), `프락셀 (프랙셔널 레이저)`(M8), `리쥬란 (PN주사)`(M4), `히알루론산 필러`(M2), `스컬트라 (PLLA)`(M3), `엘란쎄 (PCL)`(M3), `자가지방이식`(M6), `마이크로니들RF (시크릿/인모드)`(M11), `CO2 프랙셔널 레이저`(M8), `MTS (더마펜/더마스탬프)`(M12), `피코 프랙셔널`(M8), `실리콘피부관리 (아쿠아필/하이드라)`(M15), `피코토닝`(M8), `Q-스위치 Nd:YAG`(M8), `IPL (광선치료)`(M9), `레이저토닝 (저출력 Nd:YAG)`(M8), `알렉산드라이트 (755nm)`(M8), `다이오드 (808nm/810nm)`(M8), `Nd:YAG (1064nm)`(M8), `IPL 제모`(M9), `쿨스컬프팅 (냉동지방분해)`(M14), `리포셀 (HIFU 지방)`(M10), `스컬프슈어 (레이저 지방분해)`(M8), `바넬라 (고주파 바디)`(M9), `아그네스 (RF 니들 피지선)`(M11), `PDT (광역동치료)`(M8), `살리실릭 필링`(M15), `압출+스킨스케일링`(M15), `제네시스 (Nd:YAG 롱펄스)`(M8), `스킨부스터 (쥬베룩/리쥬란)`(M4), `PRP (자가혈 재생)`(M5), `엑소좀 (줄기세포 유래)`(M17), `물광주사 (메소테라피)`(M4), `바이오스티뮬레이터 (쥬베룩볼륨)`(M3)

### 3.10 표기 변형 목록 (띄어쓰기·괄호·영/한·대소문자만 다른 것; 이름류 키의 24자 이하 값)

정규화(소문자·괄호 제거·공백/구분자 제거)가 같은데 표면형이 2개 이상인 것. **같은 것이라는 판정이 아니다** — 괄호 안이 부위·용량·제품을 구분하는 경우도 함께 섞여 있다.

| 정규화 키 | 표면형 [파일] |
|---|---|
| acne | `Acne` [taxonomy]<br>`acne` [procedure-comparison, treatment-optimization] |
| ahabha필링 | `AHA/BHA 필링` [taxonomy]<br>`AHA/BHA 필링 (표재성)` [pih-risk] |
| antiaging | `Anti-aging` [taxonomy]<br>`anti-aging` [combo-recipes] |
| biostimulator | `Biostimulator` [procedure-profiles]<br>`biostimulator` [post-procedure-timeline] |
| body | `Body` [taxonomy]<br>`body` [treatment-optimization] |
| bodycontouring | `Body Contouring` [treatment-optimization]<br>`body_contouring` [procedure-comparison] |
| botox | `Botox` [products, taxonomy]<br>`botox` [post-procedure-timeline] |
| caha | `CaHA` [products, taxonomy]<br>`CaHA (칼슘하이드록시아파타이트)` [taxonomy]<br>`CaHA(레디에스)` [treatment-optimization] |
| cheek | `Cheek (Malar/Buccal)` [anatomy-danger-zones]<br>`cheek` [anatomy-danger-zones] |
| chin | `Chin (Mentum)` [anatomy-danger-zones]<br>`chin` [anatomy-danger-zones] |
| co2프락셔널 | `CO2 프락셔널` [treatment-optimization, treatment-sequence]<br>`CO2 프락셔널 (10600nm, 박리성)` [pih-risk]<br>`CO2 프락셔널 (전체얼굴)` [market-pricing]<br>`CO2프락셔널` [problem-packages, taxonomy] |
| forehead | `Forehead` [anatomy-danger-zones]<br>`forehead` [anatomy-danger-zones] |
| glabella | `Glabella` [anatomy-danger-zones]<br>`glabella` [anatomy-danger-zones] |
| hairremoval | `Hair Removal` [taxonomy, treatment-optimization]<br>`hair_removal` [procedure-comparison] |
| ha필러 | `HA 필러` [post-procedure-timeline, treatment-optimization, treatment-sequence]<br>`HA 필러(딥)` [treatment-optimization] |
| hifu | `HIFU` [pih-risk, products, taxonomy]<br>`HIFU (울쎄라, 슈링크 등)` [pih-risk]<br>`HIFU (초음파)` [taxonomy]<br>`HIFU(슈링크/울쎄라)` [treatment-optimization]<br>`HIFU(울쎄라/슈링크)` [treatment-optimization]<br>`HIFU(울쎄라급)` [treatment-optimization] |
| hifurf | `HIFU/RF` [treatment-optimization]<br>`HIFU/RF(하반기)` [treatment-optimization]<br>`hifu-rf` [post-procedure-timeline] |
| ipl | `IPL` [pih-risk, problem-packages, taxonomy, treatment-optimization, treatment-sequence]<br>`IPL (560-950nm 광대역)` [pih-risk]<br>`IPL (광선치료)` [procedure-comparison]<br>`IPL (전체얼굴)` [market-pricing]<br>`IPL(가을 색소 관리)` [treatment-optimization]<br>`IPL(가을 색소)` [treatment-optimization]<br>`IPL(색소 관리)` [treatment-optimization]<br>`IPL(유지)` [treatment-optimization] |
| laser | `Laser` [procedure-profiles]<br>`laser` [treatment-optimization] |
| ldm초음파관리 | `LDM 초음파 관리` [market-pricing]<br>`LDM초음파관리` [taxonomy] |
| led | `LED` [treatment-optimization]<br>`LED(블루라이트)` [treatment-optimization] |
| lips | `Lips` [anatomy-danger-zones]<br>`lips` [anatomy-danger-zones] |
| lllt | `LLLT` [problem-packages, taxonomy]<br>`LLLT (저출력 레이저)` [taxonomy] |
| mts | `MTS` [pih-risk, problem-packages, treatment-sequence]<br>`MTS (더마펜/더마스탬프)` [procedure-comparison]<br>`MTS (두피 탈모)` [market-pricing]<br>`MTS (마이크로니들 치료)` [extracted]<br>`MTS (여드름 흉터 집중)` [market-pricing]<br>`MTS (전체얼굴)` [market-pricing]<br>`MTS(미세채널 오픈)` [treatment-sequence] |
| mts+prp+스킨부스터 | `MTS + PRP + 스킨부스터` [combo-recipes]<br>`MTS + PRP + 스킨부스터 (골든루틴)` [problem-combos] |
| nd:yag | `Nd:YAG` [products, taxonomy]<br>`Nd:YAG (1064nm)` [procedure-comparison] |
| neck | `Neck` [anatomy-danger-zones]<br>`neck` [anatomy-danger-zones] |
| needlerf | `Needle RF` [procedure-profiles]<br>`needle-rf` [post-procedure-timeline] |
| nose | `Nose` [anatomy-danger-zones]<br>`nose` [anatomy-danger-zones] |
| pcl | `PCL` [products, taxonomy]<br>`PCL (폴리카프로락톤)` [taxonomy] |
| pdlla | `PDLLA` [taxonomy]<br>`PDLLA (폴리-D,L-락틱산)` [taxonomy] |
| pdo | `PDO` [products, taxonomy]<br>`PDO (폴리디옥사논)` [taxonomy] |
| pdo실 | `PDO 실 (10줄 기준)` [market-pricing]<br>`PDO실` [treatment-sequence] |
| pdt | `PDT` [problem-packages, taxonomy]<br>`PDT (광역동치료)` [procedure-comparison] |
| periorbital | `Periorbital` [anatomy-danger-zones]<br>`periorbital` [anatomy-danger-zones] |
| plla | `PLLA` [products, taxonomy]<br>`PLLA (폴리-L-락틱산)` [taxonomy] |
| prf | `PRF` [taxonomy]<br>`PRF (피브린풍부혈장)` [taxonomy] |
| prp | `PRP` [problem-packages, taxonomy, treatment-optimization]<br>`PRP (두피)` [market-pricing]<br>`PRP (엑소좀은 보조·근거 제한적)` [treatment-optimization]<br>`PRP (자가혈 재생)` [procedure-comparison]<br>`PRP (전체얼굴)` [market-pricing]<br>`PRP (혈소판풍부혈장)` [taxonomy] |
| rf | `RF` [pih-risk, products, taxonomy]<br>`RF (고주파)` [taxonomy] |
| skinbooster | `Skin Booster` [procedure-profiles, taxonomy]<br>`skin-booster` [post-procedure-timeline] |
| svf | `SVF` [taxonomy]<br>`SVF (자가지방줄기세포)` [taxonomy] |
| tca필링 | `TCA 필링` [taxonomy]<br>`TCA 필링 (중간-심층)` [pih-risk] |
| temple | `Temple` [anatomy-danger-zones]<br>`temple` [anatomy-danger-zones] |
| threadlift | `Thread Lift` [procedure-profiles]<br>`thread-lift` [post-procedure-timeline] |
| wrinkle | `Wrinkle` [taxonomy]<br>`wrinkle` [procedure-comparison, treatment-optimization] |
| 감염 | `감염` [complications]<br>`감염 (Infection, 기저 위험)` [complications] |
| 경미 | `경미 (fine lines)` [treatment-optimization]<br>`경미 (가벼운 부분 지방)` [treatment-optimization]<br>`경미 (가벼운 피부결 저하)` [treatment-optimization]<br>`경미 (미세 볼륨 저하)` [treatment-optimization]<br>`경미 (얇은 털, 소범위)` [treatment-optimization]<br>`경미 (초기 처짐)` [treatment-optimization]<br>`경미 (표재성 색소)` [treatment-optimization]<br>`경미 (활성 여드름 위주)` [treatment-optimization] |
| 과도한필러 | `과도한 필러 (자연스러운 노화 중요)` [treatment-optimization]<br>`과도한 필러(부자연스러운 외관)` [treatment-optimization] |
| 관자놀이 | `관자놀이` [anatomy-danger-zones]<br>`관자놀이 (HA 2cc)` [market-pricing] |
| 기기리프팅 | `기기 리프팅` [complications, consent-checklist, contraindications, patient-education, pre-procedure-checklist, taxonomy]<br>`기기리프팅` [extracted] |
| 깊은주름 | `깊은 주름` [treatment-optimization]<br>`깊은주름` [problem-packages, taxonomy] |
| 나노지방이식 | `나노 지방이식 (전체얼굴)` [market-pricing]<br>`나노지방이식` [taxonomy] |
| 냉각지방분해 | `냉각 지방분해 (쿨스컬프팅 등)` [patient-education]<br>`냉각지방분해` [taxonomy] |
| 눈가주름 | `눈가 주름 (국산)` [market-pricing]<br>`눈가 주름 (수입)` [market-pricing]<br>`눈가주름` [problem-packages, taxonomy] |
| 니들rf | `니들RF` [complications, consent-checklist, contraindications, extracted, market-pricing, patient-education, pih-risk, pre-procedure-checklist, problem-packages, procedure-profiles, products, taxonomy, treatment-optimization]<br>`니들RF (모공축소)` [market-pricing]<br>`니들RF (목주름)` [market-pricing]<br>`니들RF (미세침 고주파)` [post-procedure-timeline]<br>`니들RF (여드름 흉터)` [market-pricing] |
| 다이오드 | `다이오드 (808nm/810nm)` [procedure-comparison]<br>`다이오드(810nm)` [treatment-optimization] |
| 더마펜4 | `더마펜4` [taxonomy]<br>`더마펜4 (전체얼굴)` [market-pricing] |
| 더블로골드 | `더블로골드` [products, taxonomy]<br>`더블로골드 (풀페이스)` [market-pricing] |
| 두피prp | `두피 PRP` [taxonomy]<br>`두피PRP` [problem-packages, taxonomy] |
| 라라젯 | `라라젯` [taxonomy]<br>`라라젯 (클렌징)` [taxonomy] |
| 레이저제모 | `레이저 제모 (겨드랑이)` [market-pricing]<br>`레이저 제모 (전신)` [market-pricing] |
| 레이저토닝 | `레이저 토닝` [problem-combos]<br>`레이저토닝` [problem-packages, taxonomy, treatment-optimization, treatment-sequence]<br>`레이저토닝 (저출력 Nd:YAG)` [procedure-comparison] |
| 리쥬란hb+ | `리쥬란 HB+` [problem-packages, products, taxonomy]<br>`리쥬란HB+` [taxonomy] |
| 리쥬란아이 | `리쥬란 아이 (1cc)` [market-pricing]<br>`리쥬란아이` [products, taxonomy] |
| 리쥬란힐러 | `리쥬란 힐러` [problem-combos, problem-packages, products, taxonomy]<br>`리쥬란 힐러 (2cc)` [market-pricing]<br>`리쥬란힐러` [taxonomy] |
| 마늘주사 | `마늘주사` [taxonomy]<br>`마늘주사 (비타민B1)` [market-pricing] |
| 마이크로니들링 | `마이크로니들링 (MTS, 더마롤러/더마펜)` [pih-risk]<br>`마이크로니들링(MTS)` [consent-checklist, contraindications, market-pricing, patient-education, pre-procedure-checklist, problem-packages, procedure-profiles, taxonomy] |
| 목주름 | `목주름` [problem-packages, taxonomy, treatment-optimization]<br>`목주름 (네페르티티)` [market-pricing] |
| 문신제거 | `문신 제거 (10cm2)` [market-pricing]<br>`문신제거` [problem-packages, taxonomy] |
| 미간주름 | `미간 주름 (국산)` [market-pricing]<br>`미간 주름 (수입)` [market-pricing]<br>`미간주름` [problem-packages, taxonomy] |
| 바디 | `바디` [problem-packages, synergy, taxonomy]<br>`바디(여성)` [problem-packages, taxonomy] |
| 바디hifu | `바디 HIFU(리포셀)` [treatment-optimization]<br>`바디HIFU` [problem-packages, taxonomy] |
| 바이오스티뮬레이터 | `바이오스티뮬레이터` [extracted, problem-packages, treatment-optimization]<br>`바이오스티뮬레이터 (쥬베룩볼륨)` [procedure-comparison]<br>`바이오스티뮬레이터 (콜라겐 예방적 투자)` [treatment-optimization]<br>`바이오스티뮬레이터(스컬트라/엘란쎄)` [treatment-optimization]<br>`바이오스티뮬레이터(유지 1차)` [treatment-optimization]<br>`바이오스티뮬레이터(쥬베룩)` [treatment-optimization] |
| 백옥주사 | `백옥주사` [problem-packages, taxonomy]<br>`백옥주사 (글루타치온)` [market-pricing] |
| 보톡스 | `보톡스` [complications, consent-checklist, contraindications, extracted, market-pricing, patient-education, post-procedure-timeline, pre-procedure-checklist, problem-packages, procedure-profiles, products, taxonomy, treatment-optimization, treatment-sequence]<br>`보톡스 (보툴리눔톡신)` [procedure-comparison]<br>`보톡스(엘러간)` [taxonomy]<br>`보톡스(턱선/광대)` [treatment-optimization] |
| 보톡스+필러 | `보톡스 + 필러` [problem-combos, problem-packages]<br>`보톡스 + 필러 (런치타임 시술)` [combo-recipes] |
| 볼지방이식 | `볼 지방이식` [market-pricing]<br>`볼지방이식` [problem-packages, taxonomy] |
| 부종 | `부종 (Edema)` [complications]<br>`부종 (붓기)` [complications] |
| 브이빔 | `브이빔` [taxonomy]<br>`브이빔 (PDL 595nm)` [pih-risk] |
| 비대칭 | `비대칭` [complications]<br>`비대칭 (Asymmetry)` [complications] |
| 사각턱 | `사각턱` [problem-packages, taxonomy]<br>`사각턱 (국산)` [market-pricing]<br>`사각턱 (수입)` [market-pricing] |
| 색소 | `색소` [synergy]<br>`색소(기미 초기)` [treatment-optimization] |
| 서브시전 | `서브시전` [problem-packages, taxonomy, treatment-optimization]<br>`서브시전(subcision)` [treatment-optimization] |
| 슈링크유니버스 | `슈링크 유니버스 (턱라인)` [market-pricing]<br>`슈링크 유니버스 (풀페이스)` [market-pricing]<br>`슈링크유니버스` [problem-packages, products, taxonomy] |
| 스컬트라 | `스컬트라` [problem-packages, products, taxonomy]<br>`스컬트라 (1바이알)` [market-pricing]<br>`스컬트라 (3회 패키지)` [market-pricing]<br>`스컬트라 (PLLA)` [procedure-comparison] |
| 스킨부스터 | `스킨부스터` [consent-checklist, contraindications, extracted, market-pricing, patient-education, post-procedure-timeline, pre-procedure-checklist, problem-packages, procedure-profiles, taxonomy, treatment-optimization, treatment-sequence]<br>`스킨부스터 (쥬베룩/리쥬란)` [procedure-comparison]<br>`스킨부스터(리쥬란)` [treatment-optimization]<br>`스킨부스터(미백성분)` [treatment-optimization] |
| 승모근보톡스 | `승모근 보톡스` [problem-packages]<br>`승모근보톡스` [problem-packages, taxonomy] |
| 시그니처프로그램 | `시그니처 프로그램` [taxonomy]<br>`시그니처프로그램` [taxonomy] |
| 시크릿 | `시크릿` [problem-packages, products, taxonomy]<br>`시크릿 (전체얼굴)` [market-pricing] |
| 신데렐라주사 | `신데렐라주사` [taxonomy]<br>`신데렐라주사 (알파리포산)` [market-pricing] |
| 실리프팅 | `실 리프팅 (얼굴 당김 시술)` [patient-education]<br>`실리프팅` [complications, consent-checklist, contraindications, extracted, market-pricing, patient-education, post-procedure-timeline, pre-procedure-checklist, problem-packages, procedure-profiles, taxonomy, treatment-optimization]<br>`실리프팅 (PDO코그)` [procedure-comparison]<br>`실리프팅(PCL/PDO)` [treatment-optimization]<br>`실리프팅(PDO/PCL)` [treatment-optimization] |
| 심부필링 | `심부 필링` [treatment-sequence]<br>`심부 필링(TCA 50%+/페놀)` [treatment-sequence]<br>`심부 필링(페놀)` [treatment-sequence] |
| 써마지flx | `써마지 FLX (눈가 450샷)` [market-pricing]<br>`써마지 FLX (풀페이스 900샷)` [market-pricing]<br>`써마지FLX` [problem-packages, products, taxonomy]<br>`써마지FLX (RF)` [procedure-comparison] |
| 아그네스 | `아그네스` [problem-packages, taxonomy]<br>`아그네스 (RF 니들 피지선)` [procedure-comparison] |
| 아쿠아필 | `아쿠아필` [taxonomy]<br>`아쿠아필 (전체얼굴)` [market-pricing] |
| 알렉산드라이트 | `알렉산드라이트` [taxonomy]<br>`알렉산드라이트 (755nm)` [procedure-comparison]<br>`알렉산드라이트(755nm)` [treatment-optimization] |
| 에너지기기 | `에너지 기기` [treatment-sequence]<br>`에너지기기(HIFU/RF)` [market-pricing, procedure-profiles] |
| 엑셀v | `엑셀V` [problem-packages, products, taxonomy]<br>`엑셀V (혈관/홍조)` [market-pricing] |
| 엑소좀 | `엑소좀` [products, taxonomy]<br>`엑소좀 (두피)` [market-pricing]<br>`엑소좀 (전체얼굴)` [market-pricing]<br>`엑소좀 (줄기세포 유래)` [procedure-comparison] |
| 엘란쎄 | `엘란쎄` [problem-packages, products, taxonomy]<br>`엘란쎄 (PCL)` [procedure-comparison] |
| 엠페이스 | `엠페이스` [taxonomy]<br>`엠페이스(EMFACE)` [taxonomy] |
| 여드름흉터 | `여드름/흉터` [treatment-optimization]<br>`여드름흉터` [problem-packages, taxonomy] |
| 울쎄라 | `울쎄라` [problem-packages, products, taxonomy]<br>`울쎄라 (HIFU)` [procedure-comparison]<br>`울쎄라 (턱라인)` [market-pricing]<br>`울쎄라 (풀페이스)` [market-pricing] |
| 이마주름 | `이마 주름 (국산)` [market-pricing]<br>`이마 주름 (수입)` [market-pricing]<br>`이마주름` [problem-packages, taxonomy] |
| 이마지방이식 | `이마 지방이식` [market-pricing]<br>`이마지방이식` [problem-packages, taxonomy] |
| 이모드 | `이모드 (4회 패키지)` [market-pricing]<br>`이모드 (복부)` [market-pricing]<br>`이모드 (복부+힙 동시)` [market-pricing]<br>`이모드 (힙)` [market-pricing] |
| 이온토포레시스 | `이온토포레시스` [taxonomy]<br>`이온토포레시스 (비타민C)` [market-pricing] |
| 인모드 | `인모드` [problem-packages, products, taxonomy]<br>`인모드 (바이폴라 RF + IPL/다이오드)` [pih-risk]<br>`인모드 (풀페이스)` [market-pricing] |
| 인피니 | `인피니` [taxonomy]<br>`인피니 (전체얼굴)` [market-pricing] |
| 임신여부 | `임신 여부` [pre-procedure-checklist]<br>`임신 여부 (복부 시술 시 특히 중요)` [pre-procedure-checklist] |
| 자가면역질환여부 | `자가면역질환 여부` [pre-procedure-checklist]<br>`자가면역질환 여부 (육아종 위험)` [pre-procedure-checklist]<br>`자가면역질환 여부 (이물반응 위험)` [pre-procedure-checklist] |
| 점제거 | `점 제거 (1개당)` [market-pricing]<br>`점제거` [problem-packages, taxonomy] |
| 제네시스 | `제네시스 (Nd:YAG 롱펄스)` [procedure-comparison]<br>`제네시스 (전체얼굴)` [market-pricing] |
| 제스너필링 | `제스너 필링` [pih-risk]<br>`제스너필링` [taxonomy] |
| 주사부위반응 | `주사 부위 반응 (부종·압통·멍·홍반)` [complications]<br>`주사부위 반응 (통증·발적·멍·경결)` [complications] |
| 중등도 | `중등도 (moderate wrinkles)` [treatment-optimization]<br>`중등도 (기미, 혼합 색소)` [treatment-optimization]<br>`중등도 (넓은 모공, 거친 피부결)` [treatment-optimization]<br>`중등도 (눈에 띄는 볼륨 감소)` [treatment-optimization]<br>`중등도 (눈에 띄는 처짐)` [treatment-optimization]<br>`중등도 (보통 굵기, 중범위)` [treatment-optimization]<br>`중등도 (부분 비만, 셀룰라이트)` [treatment-optimization]<br>`중등도 (여드름 흉터 위주)` [treatment-optimization] |
| 중증 | `중증 (deep wrinkles)` [treatment-optimization]<br>`중증 (광범위 체형 관리)` [treatment-optimization]<br>`중증 (굵은 털, 대범위/다부위)` [treatment-optimization]<br>`중증 (깊은 기미, 진피 색소)` [treatment-optimization]<br>`중증 (깊은 박스카/아이스픽 흉터)` [treatment-optimization]<br>`중증 (뚜렷한 처짐)` [treatment-optimization]<br>`중증 (심한 모공/흉터급 피부결)` [treatment-optimization]<br>`중증 (심한 볼륨 손실/골격 변화)` [treatment-optimization] |
| 쥬베룩볼륨 | `쥬베룩 볼륨 (2cc)` [market-pricing]<br>`쥬베룩 볼륨 (4cc)` [market-pricing]<br>`쥬베룩볼륨` [products, taxonomy] |
| 지방분해주사 | `지방분해주사 (마케팅명)` [taxonomy]<br>`지방분해주사(PPC)` [taxonomy]<br>`지방분해주사(PPC/DC)` [problem-packages, taxonomy]<br>`지방분해주사(데옥시콜산)` [treatment-optimization] |
| 케미컬필링 | `케미컬 필링` [treatment-sequence]<br>`케미컬 필링 (중간 깊이)` [post-procedure-timeline]<br>`케미컬필링` [pih-risk, problem-packages, taxonomy] |
| 켈로이드체질확인 | `켈로이드 체질 확인` [pre-procedure-checklist]<br>`켈로이드 체질 확인 (어블레이티브 레이저)` [pre-procedure-checklist] |
| 코실리프팅 | `코 실리프팅` [market-pricing]<br>`코실리프팅` [problem-packages, taxonomy] |
| 코필러 | `코 필러 (HA 1cc)` [market-pricing]<br>`코필러` [problem-packages, taxonomy] |
| 쿨미니 | `쿨미니` [taxonomy]<br>`쿨미니 (소부위 1개)` [market-pricing] |
| 쿨스컬프팅 | `쿨스컬프팅` [problem-packages, taxonomy]<br>`쿨스컬프팅 (냉동지방분해)` [procedure-comparison]<br>`쿨스컬프팅 (러브핸들 양쪽)` [market-pricing]<br>`쿨스컬프팅 (복부 1부위)` [market-pricing]<br>`쿨스컬프팅 (턱밑 이중턱)` [market-pricing]<br>`쿨스컬프팅 (팔뚝 양쪽)` [market-pricing]<br>`쿨스컬프팅 (허벅지 안쪽 양쪽)` [market-pricing] |
| 크라이오 | `크라이오` [problem-packages, treatment-optimization]<br>`크라이오(냉동지방분해)` [treatment-optimization] |
| 클라리티2 | `클라리티2` [problem-packages, products, taxonomy]<br>`클라리티2 (혈관)` [taxonomy] |
| 클래시스 | `클래시스` [products, taxonomy]<br>`클래시스(Classys)` [products] |
| 탈모 | `탈모` [synergy]<br>`탈모(비수술)` [taxonomy] |
| 태반주사 | `태반주사 (라이넥)` [market-pricing]<br>`태반주사(라엔넥)` [taxonomy] |
| 트라넥삼산 | `트라넥삼산` [taxonomy]<br>`트라넥삼산(경구+주사)` [treatment-optimization]<br>`트라넥삼산(경구/국소)` [treatment-optimization] |
| 팔자주름 | `팔자주름` [anatomy-danger-zones, problem-packages, taxonomy]<br>`팔자주름 (HA 1cc)` [market-pricing] |
| 포텐자 | `포텐자` [problem-packages, products, taxonomy]<br>`포텐자 (전체얼굴)` [market-pricing] |
| 프락셀 | `프락셀` [problem-packages, products, taxonomy]<br>`프락셀 (프랙셔널 레이저)` [procedure-comparison] |
| 프락셔널 | `프락셔널` [pih-risk, problem-packages, products, taxonomy]<br>`프락셔널(피부결)` [treatment-optimization] |
| 프락셔널co2 | `프락셔널 CO2` [treatment-sequence]<br>`프락셔널 CO2(피부결)` [treatment-optimization] |
| 프락셔널레이저 | `프락셔널 레이저` [problem-combos, treatment-optimization, treatment-sequence]<br>`프락셔널레이저` [problem-packages, taxonomy] |
| 프로파일로 | `프로파일로` [taxonomy]<br>`프로파일로 (2ml)` [market-pricing] |
| 플라즈마 | `플라즈마` [consent-checklist, extracted, market-pricing, patient-education, pih-risk, pre-procedure-checklist, procedure-profiles, taxonomy]<br>`플라즈마 (눈가 주름)` [market-pricing]<br>`플라즈마 (눈꺼풀 처짐 비수술)` [market-pricing]<br>`플라즈마 (여드름 치료)` [market-pricing]<br>`플라즈마 (열플라즈마/플렉서)` [pih-risk]<br>`플라즈마 (쥐젖/사마귀 1개)` [market-pricing]<br>`플라즈마 (콜드플라즈마)` [pih-risk] |
| 피코슈어 | `피코슈어` [problem-packages, products, taxonomy]<br>`피코슈어 (755nm 피코초)` [pih-risk] |
| 피코슈어프락셀 | `피코슈어 프락셀` [taxonomy]<br>`피코슈어 프락셀 (755nm 비박리성)` [pih-risk] |
| 피코토닝 | `피코토닝` [problem-packages, procedure-comparison, taxonomy, treatment-optimization, treatment-sequence]<br>`피코토닝 (전체얼굴)` [market-pricing]<br>`피코토닝 (피코초 Nd:YAG 1064nm)` [pih-risk] |
| 피코프락셀 | `피코프락셀` [taxonomy]<br>`피코프락셀 (비박리성 피코초)` [pih-risk]<br>`피코프락셀 (전체얼굴)` [market-pricing] |
| 필러 | `필러` [complications, consent-checklist, contraindications, extracted, market-pricing, patient-education, pre-procedure-checklist, problem-packages, procedure-profiles, taxonomy, treatment-optimization, treatment-sequence]<br>`필러 (동일 부위 재시술)` [treatment-sequence]<br>`필러 (별도 세션)` [treatment-sequence]<br>`필러(HA/CaHA)` [treatment-optimization]<br>`필러(팔자/볼)` [treatment-optimization] |
| 필링 | `필링` [problem-packages, treatment-optimization]<br>`필링(살리실산/글리콜산)` [treatment-optimization]<br>`필링(약한 산)` [treatment-optimization] |
| 항응고제복용여부 | `항응고제 복용 여부` [pre-procedure-checklist]<br>`항응고제 복용 여부 (멍 위험 안내)` [pre-procedure-checklist]<br>`항응고제 복용 여부 (출혈 위험)` [pre-procedure-checklist] |
| 홍반 | `홍반 (Erythema / Redness)` [complications]<br>`홍반 (Erythema)` [complications]<br>`홍반 (시술 직후 빨개짐)` [complications] |
| 화상 | `화상 (수포 포함)` [complications]<br>`화상 (열손상, Thermal Burn)` [complications] |
| 효과발현시기안내 | `효과 발현 시기 안내 (1-3개월 점진적)` [pre-procedure-checklist]<br>`효과 발현 시기 안내 (2-4개월 점진적)` [pre-procedure-checklist] |

## 4. 다국어 필드 표

| 파일 | 경로 | 횟수 | 예시 |
|---|---|---|---|
| `anatomy-danger-zones.json` | `zones[].name_ko` | 11 | `이마` · `미간` |
| `anatomy-danger-zones.json` | `zones[].name_en` | 11 | `Forehead` · `Glabella` |
| `extracted.json` | `{code}.name_en` | 17 | `High-Intensity Focused Electromagnetic Stimulation…` · `Microneedle Radiofrequency (MNRF)` |
| `literature-evidence.json` | `accuracy_summary.patient_translations_coverage.ko` | 1 | `119/119` |
| `literature-evidence.json` | `accuracy_summary.patient_translations_coverage.en` | 1 | `119/119` |
| `literature-evidence.json` | `accuracy_summary.patient_translations_coverage.zh` | 1 | `119/119` |
| `literature-evidence.json` | `accuracy_summary.patient_translations_coverage.ja` | 1 | `119/119` |
| `literature-evidence.json` | `categories.{code}.moa[].patient_ko` | 50 | `보툴리눔 톡신은 근육으로 가는 신경 신호 전달 물질이 나오는 것을 방해하여 근육의 움직임을…` · `보톡스는 신경과 근육 연결 부위에서 신호 전달 물질 방출을 막아 근육을 약하게 합니다.[1…` |
| `literature-evidence.json` | `categories.{code}.moa[].patient_en` | 50 | `Botulinum toxin stops nerve signals from reaching …` · `Botulinum toxin gently weakens muscle activity by …` |
| `literature-evidence.json` | `categories.{code}.moa[].patient_zh` | 50 | `肉毒素通过阻断传递给肌肉的神经信号，帮助减少肌肉的过度运动。` · `肉毒素通过中断局部信号传递，温和地减弱肌肉的活动强度。` |
| `literature-evidence.json` | `categories.{code}.moa[].patient_ja` | 50 | `ボツリヌストキシンが筋肉に届く神経の合図を遮断し、動きを和らげます。` · `ボツリヌストキシンが局所の伝달を遮断し、筋肉の動きを優しく和らげます。` |
| `literature-evidence.json` | `categories.{code}.adverse_effects[].patient_ko` | 32 | `눈 주변 시술 시 드물게 눈이 건조해지거나 사물이 겹쳐 보이는 증상이 나타날 수 있습니다.` · `A형 보툴리눔 독소는 턱 아래 침샘을 위축시킵니다.` |
| `literature-evidence.json` | `categories.{code}.adverse_effects[].patient_en` | 32 | `Temporary dry eyes or vision changes can happen if…` · `Botulinum toxin may cause the salivary glands unde…` |
| `literature-evidence.json` | `categories.{code}.adverse_effects[].patient_zh` | 32 | `如果成分扩散到邻近区域，可能会出现暂时的眼睛干涩或视觉变化。` · `肉毒素可能会引起下巴下方的唾液腺出现体积缩小的现象。` |
| `literature-evidence.json` | `categories.{code}.adverse_effects[].patient_ja` | 32 | `成分が周囲に広がると、一時的な目の乾きや見え方の変化が起こります。` · `ボツリヌストキシンが、あごの下にある唾液腺を小さくさせることがあります。` |
| `literature-evidence.json` | `categories.{code}.effects[].patient_ko` | 37 | `보톡스는 얼굴의 주름을 펴주는 주사예요.` · `A형 보툴리눔 독소가 하안면 윤곽을 다듬어줍니다.[2]` |
| `literature-evidence.json` | `categories.{code}.effects[].patient_en` | 37 | `Botulinum toxin helps smooth the face by addressin…` · `Botulinum toxin is used to help shape and define t…` |
| `literature-evidence.json` | `categories.{code}.effects[].patient_zh` | 37 | `肉毒素通过针对表情纹产生的原因，帮助您恢复面部的平滑。` · `肉毒素常被用于帮助塑造和美化下半面部的轮廓与线条。` |
| `literature-evidence.json` | `categories.{code}.effects[].patient_ja` | 37 | `ボツリヌストキシンが表情じわの原因に働き、お顔を滑らかに整えます。` · `ボツリヌストキシンを用いて、お顔の下半分の輪郭を美しく整えます。` |
| `procedure-profiles.json` | `profiles[].name_en` | 17 | `Botulinum Toxin` · `Dermal Filler` |
| `products.json` | `botulinum_toxin.products[].name_en` | 11 | `Botox` · `Dysport` |
| `products.json` | `filler_ha.products[].name_en` | 7 | `Juvéderm` · `Restylane` |
| `products.json` | `biostimulator.products[].name_en` | 6 | `Sculptra` · `Ellansé` |
| `products.json` | `skin_booster.products[].name_en` | 5 | `Rejuran Healer` · `Rejuran HB+` |
| `products.json` | `thread_lift.products[].name_en` | 5 | `Mint Lift` · `TESSLift` |
| `products.json` | `energy_device.products[].name_en` | 18 | `Ultherapy` · `Thermage FLX` |
| `products.json` | `prp_exosome.products[].name_en` | 5 | `Cellpia` · `RegenACR` |
| `products.json` | `stem_cell.products[].name_en` | 2 | `CureSkin` · `SF Injection` |
| `taxonomy.json` | `modality[].category_en` | 17 | `Botulinum Toxin` · `Filler` |
| `taxonomy.json` | `modality[].products[].name_en` | 59 | `Botox` · `Dysport` |
| `taxonomy.json` | `problem[].category_en` | 14 | `Petit Procedure` · `Wrinkle` |
| `treatment-optimization.json` | `by_concern[].concern_en` | 8 | `Wrinkle Reduction` · `Sagging / Elasticity` |

- 4개 국어(ko/en/zh/ja)가 모두 있는 곳은 `literature-evidence.json` 의 `patient_*` 뿐(문장 119개 × 4). 나머지는 `name_en`/`category_en`/`concern_en`/`name_ko` 처럼 한글 본문 + 영문 라벨 1개.
- `literature-evidence.json` patient_* 안의 각주 잔재 `[n]`: ko 41건. 다른 언어 본문에 한글 섞임: ja 5건, en 1건 (예: `ボツリヌストキシンが局所の伝달を遮断し、筋肉の動きを優しく和らげます。`, `ボツ리ヌストキシンがしわを作る表情筋を穏やかにして、しわをケアします。`)
- 영문 라벨끼리도 표기가 다르다: taxonomy `Botulinum Toxin` / procedure-profiles `Botulinum Toxin` / products `Botox` / extracted `Botulinum Toxin Type A` / literature `Botulinum toxin type A (aesthetic)`; M9 는 `Energy Based Device Lifting`(taxonomy) / `Non-invasive skin tightening: HIFU and radiofrequency`(literature) / extracted `name_en` 별도.

## 5. 원장만 보고 드는 질문 (실버 설계 전에 물을 것)

1. 계열(M1~M17)·고민(P1~P14) 코드와 이름의 정본은 `taxonomy.json` 인가? 다른 파일의 다른 표기(`기기 리프팅`/`기기리프팅`/`리프팅기기`/`에너지기기(HIFU/RF)`, `처짐/탄력`/`쳐짐`/`처짐`, `PRP/자가혈`/`PRP/엑소좀`/`PRP 피부재생술`)는 taxonomy 쪽으로 맞추는 것으로 보면 되는가, 아니면 파일별 표기에 의미 차이가 있는가?
2. `extracted.json` 과 `taxonomy.json › modality[].extracted` 가 8개 계열에서 본문이 다르다(M2·M3·M5·M8·M10·M12·M13·M17). 어느 쪽이 최신/정본인가? `extracted.json` 에만 있는 메타(`source`, `source_type`, `procedure_id`, `extracted_at`)는 필요한가?
3. `products.json` 과 `taxonomy.json › modality[].products` 가 59개로 같은 수이지만 `티엠버스`/`타임버스`, `신펄`, `볼뉴머` 에서 다르다. 제품 목록의 정본은 어느 쪽인가? taxonomy 쪽에는 `extracted` 본문이 붙어 있고 products.json 쪽에는 `mfds`·`type` 등이 더 있는데 둘을 합칠 것인가?
4. taxonomy 항목 id 가 `M1-2-1` 형(128) / `auto-M4-<timestamp>` 형(322) / `auto-63-<timestamp>` 형(62) / 기타(9) 로 섞여 있고, problem 항목은 전부 `auto-#-<timestamp>` 다. 이 id 들은 외부(앱·DB)에서 이미 참조되고 있어 그대로 보존해야 하는가, 실버에서 새 키를 발급해도 되는가?
5. `pih-risk.json › procedure_ref` 가 항목(M8-1-1)·하위분류(M8-5)·계열(M12) 세 깊이를 섞어 가리키고, 2건에 같은 ref 가 중복된다. 이 참조의 단위를 하나로 맞출 것인가, 아니면 「가장 구체적인 수준」을 그대로 두는가?
6. `problem-combos.json › packages[].id`(P1-1, P1-2 …) 가 taxonomy 의 problem 하위분류 id 와 같은 문자열을 다른 뜻으로 쓴다. 이 패키지 id 를 외부에서 쓰고 있는가? 바꿔도 되는가?
7. `post-procedure-timeline.json` 의 `category` 값 `M16-DCA` 와, `treatment-sequence.json` 의 `M15-클렌징`·`M9-HIFU`·`M8-토닝` 같은 코드+라벨 합성값은 taxonomy 하위분류를 가리키려는 의도인가? (`M15-도포`·`M15-팩`·`M16-DCA` 는 taxonomy 하위분류 id 로 실존하지만 나머지는 없다.)
8. `synergy.json` 의 노드(`M1-보톡스`, `M1-사각턱보톡스`, `M9-울쎄라`, `M4-쥬베룩`)는 계열·시술·제품 어느 단위인가? 실버에서 노드를 taxonomy 항목/제품에 연결해야 하는가, 아니면 계열 코드(from_category/to_category)까지만 쓰는가?
9. `problem-packages.json` 의 `complaints[].cc` 는 taxonomy problem 항목 이름과 113/115 가 일치하지만 id 가 없다. 이름으로 붙여도 되는가? 이름이 중복되는 6개(아그네스, 스킨보톡스, 프락셔널레이저, 니들RF, 서브시전, 브이올렛)와 P9 의 `cc_group` 불일치 2건은 어느 쪽이 맞는가?
10. `problem-packages.json › procedures[].name` 29종(레이저/프락셔널/서브시전/혈관레이저 … → 전부 M8)은 계열보다 세밀한 「시술 종류」 층으로 보인다. 이 층을 실버에 별도 엔티티로 둘 것인가, taxonomy 하위분류에 대응시킬 것인가? 대응표는 누가 주는가?
11. `treatment-optimization.json`(optimal_combo 57종)·`treatment-sequence.json`(pair/sequence/from/to)·`procedure-comparison.json`(name 39)·`market-pricing.json`(items.name 122)·`problem-combos.json`(products 문장)의 시술/제품명은 전부 자유 텍스트다. 실버에서 이들을 코드로 연결해야 하는가? 연결한다면 대응표를 사람이 주는가, 아니면 연결하지 않고 문장으로 둔 채 쓰는가?
12. `treatment-optimization.json › by_concern[].concern` 8개와 `procedure-comparison.json › comparisons[].id` 9개는 taxonomy 고민 14개와 1:1 이 아니다(주름 개선 ↔ P2 는 되지만 바디컨투어링·볼륨 손실·rejuvenation 등은 어디로?). 고민 축의 정본을 taxonomy P 로 볼 것인가, 아니면 이 파일들의 분류를 별개 축으로 두는가?
13. `literature-evidence.json` 에서 M6·M10·M11·M13·M14 는 세 섹션 전부 비어 있고, `complications.json` 은 10개 계열, `post-procedure-timeline.json` 은 10개 시술, `contraindications.json` 은 11개 계열, `problem-combos.json` 은 8개 고민만 다룬다. 빠진 계열/고민은 「없음」으로 둘 것인가, 채워질 예정인가?
14. `taxonomy.json › problem[].…items[].modality_ref` 가 26개 항목에서 빈 배열(반영구화장, 약물치료, 미녹시딜, FUE/FUT, 미라드라이 등)이다. 이 항목들은 M 계열 밖의 시술로 두는가, 새 계열이 필요한가?
15. `complications.json › risk_factors` 46/65 빈 배열, `problem-packages.json › procedures[].products` 47/254 빈 배열, `treatment-optimization.json › contraindicated_combos` 11/24 빈 배열, taxonomy `products` 7개 계열 빈 배열. 빈 배열은 「해당 없음」인가 「미입력」인가? 구분이 필요하면 원장 쪽에서 표시해 줄 수 있는가?
16. `taxonomy.json › modality[].products[].mfds` 가 기기 17개에서 null 이고, `products.json` 의 energy_device 18개에는 `mfds` 키 자체가 없다. 기기는 mfds 허가 개념을 쓰지 않는 것인가(=null 유지), 아니면 미입력인가?
17. `extracted.json › safety.serious` 가 M10·M13 에서 null, 나머지는 배열이다. null 은 「심각 부작용 없음」인가 「미입력」인가?
18. `products.json` 의 `스킨보톡스` 는 manufacturer/country 가 `-` 이고 note 에 「별도 제품 아님」이라고 되어 있다. 제품 목록에 유지하는가?
19. `literature-evidence.json › patient_ko` 41개에 `[1][2]` 각주 번호가 남아 있고 `patient_ja` 5건·`patient_en` 1건에 한글이 섞여 있다. 실버에서 이 문자열을 정제해도 되는가(원문 보존이 필요한가)?
20. taxonomy 항목 `extracted` 하위 키가 갈려 있다(`safety.common` vs `common_adverse_effects` vs `common_side_effects`, `onset_duration.peak` vs `peak_effect`, `indications.extended` vs `secondary`). 같은 뜻으로 합쳐도 되는가? `secondary` 와 `extended` 는 다른 뜻인가?
21. `procedure-profiles.json › mechanism[]` 의 `regenerative`(M3·M4·M5·M6) 와 `regeneration`(M17), `phaseOrder` 중복(95: M6·M15 / 90: M7·M16 / 85: M9·M14)은 의도인가?
22. `treatment-sequence.json › minimum_intervals` 의 `min_days`/`min_months` 두 단위, `market-pricing.json › unit` 17종, `problem-combos.json › priceRange` 의 `/회` 유무 — 단위를 정규화해도 되는가, 원문 단위를 보존해야 하는가?
23. taxonomy 안에 이미 교정 메모 키가 있다(`classification_issue` 2, `reclassified_to` 1, `correction_note` 1, `verification_needed` 1, `is_marketing_name` 6). 실버는 이 메모대로 재분류된 결과를 담는가(예: 소프라노 티타늄 → M8, 볼뉴머 M4 항목 제거), 아니면 원장 위치를 그대로 두고 메모만 옮기는가?
24. `anatomy-danger-zones.json` 의 부위 11개(forehead, glabella …)와 taxonomy problem 하위분류 라벨(코, 이마/관자놀이, 턱/턱선 …), `problem-packages.json › cc_group` 52종은 서로 다른 부위 어휘다. 부위를 실버의 축으로 둘 것인가? 둔다면 정본 어휘는 무엇인가?
25. `version`/`updated` 가 파일마다 다르고(1.0~6.2, 2026-04-04~2026-09-03) taxonomy·extracted·complications 에는 없다. 실버가 원장 버전을 기록해야 하는가? 어느 날짜 스냅샷(`phub-stg-2026-10-26`)을 브론즈의 기준으로 보는가?

## 부록 A. 계열·고민 정준 이름 (taxonomy.json 기준)

| 코드 | category | category_en | group | 하위 | 항목 | products |
|---|---|---|---|---|---|---|
| M1 | 보톡스 | Botulinum Toxin | 주사/주입 | 3 | 31 | 11 |
| M2 | 필러 | Filler | 주사/주입 | 3 | 29 | 8 |
| M3 | 바이오스티뮬레이터/콜라겐부스터 | Biostimulator / Collagen Stimulator | 주사/주입 | 7 | 24 | 6 |
| M4 | 스킨부스터 | Skin Booster | 주사/주입 | 4 | 35 | 5 |
| M5 | PRP/자가혈 | PRP / Autologous Blood | 주사/주입 | 4 | 5 | 5 |
| M6 | 지방이식 | Fat Grafting | 주사/주입 | 3 | 3 | 0 |
| M7 | 실리프팅 | Thread Lifting | 시술/기기 | 3 | 33 | 5 |
| M8 | 레이저 | Laser & Light | 시술/기기 | 7 | 72 | 6 |
| M9 | 기기 리프팅 | Energy Based Device Lifting | 시술/기기 | 5 | 44 | 7 |
| M10 | HIFES/EMS | HIFES/EMS | 시술/기기 | 2 | 10 | 0 |
| M11 | 니들RF | Microneedle RF | 시술/기기 | 1 | 13 | 4 |
| M12 | 마이크로니들링(MTS) | Microneedling | 시술/기기 | 2 | 7 | 0 |
| M13 | 플라즈마 | Plasma | 시술/기기 | 2 | 4 | 0 |
| M14 | 크라이오리포라이시스 | Cryolipolysis | 시술/기기 | 1 | 5 | 0 |
| M15 | 메디컬스킨케어 | Medical Skincare | 관리 | 16 | 136 | 0 |
| M16 | 수액치료 | IV Therapy | 관리 | 7 | 63 | 0 |
| M17 | 줄기세포치료 | Stem Cell Therapy | 관리 | 4 | 7 | 2 |

| 코드 | category | category_en | 하위 | 항목 |
|---|---|---|---|---|
| P1 | 쁘띠시술 | Petit Procedure | 7 | 17 |
| P2 | 주름 | Wrinkle | 3 | 7 |
| P3 | 쳐짐 | Sagging / Laxity | 3 | 5 |
| P4 | 항노화 | Anti-aging | 3 | 8 |
| P5 | 색소/미백 | Pigmentation & Whitening | 4 | 8 |
| P6 | 여드름 | Acne | 3 | 8 |
| P7 | 모공 | Pore | 3 | 6 |
| P8 | 홍조/혈관 | Rosacea & Vascular | 3 | 6 |
| P9 | 흉터 | Scar | 4 | 12 |
| P10 | 제모 | Hair Removal | 3 | 4 |
| P11 | 얼굴윤곽 | Facial Contouring | 5 | 7 |
| P12 | 바디 | Body | 4 | 11 |
| P13 | 두피/탈모 | Scalp & Hair Loss | 4 | 11 |
| P14 | 기타 | Others | 4 | 7 |

## 부록 B. taxonomy id 패턴

| 계열 | 항목 id 패턴 (개수) |
|---|---|
| M1 | `M#-#-#`=17, `auto-M#-timestamp`=7, `auto-#-timestamp`=7 |
| M2 | `M#-#-#`=14, `auto-#-timestamp`=2, `auto-M#-timestamp`=13 |
| M3 | `M#-#-#`=6, `auto-#-timestamp`=13, `auto-M#-timestamp`=4, `auto-M#-word-timestamp`=1 |
| M4 | `M#-#-#`=8, `auto-M#-timestamp`=24, `auto-#-timestamp`=3 |
| M5 | `M#-#-#`=3, `auto-M#-timestamp`=2 |
| M6 | `M#-#-#`=3 |
| M7 | `M#-#-#`=9, `auto-#-timestamp`=1, `auto-M#-timestamp`=23 |
| M8 | `M#-#-#`=15, `auto-#-timestamp`=10, `auto-M#-timestamp`=47 |
| M9 | `M#-#-#`=15, `auto-#-timestamp`=6, `auto-M#-timestamp`=23 |
| M10 | `M#-#-#`=3, `auto-M#-timestamp`=7 |
| M11 | `M#-#-#`=4, `auto-#-timestamp`=2, `auto-M#-timestamp`=7 |
| M12 | `M#-#-#`=2, `auto-#-timestamp`=1, `auto-M#-timestamp`=4 |
| M13 | `auto-M#-timestamp`=3, `M#-#-#`=1 |
| M14 | `M#-#-#`=1, `auto-M#-timestamp`=4 |
| M15 | `M#-#-#`=16, `auto-#-timestamp`=9, `auto-M#-timestamp`=111 |
| M16 | `M#-#-#`=8, `auto-#-timestamp`=6, `auto-M#-timestamp`=41, `auto-M#-word-timestamp`=8 |
| M17 | `M#-#-#`=3, `auto-M#-timestamp`=2, `auto-#-timestamp`=2 |

- 하위분류 id: `M#-#`=56, `other:M3-new-1774324237649`=1, `other:M3-new-1774324512965`=1, `other:auto-new-M4-1775360442`=1, `other:M5-new-1774324656750`=1, `other:auto-new-M8-1775360463`=1, `other:M9-SIG`=1, `other:auto-M15-1775360912`=1, `other:auto-M15-1775360998`=1, `other:auto-1775361777`=1, `other:auto-1775361850`=1, `other:auto-1775361870`=1, `other:auto-1775402620`=1, `other:M15-도포`=1, `other:M15-팩`=1, `other:M16-DCA`=1, `other:M16-LIPO`=1, `other:M16-new-1774325959851`=1, `other:M17-new-1774325986969`=1
- problem 항목 id: `auto-#-timestamp`=117 / products id: `M#-P-#`=59
- 교정 메모 키가 붙은 항목: M1 `톡스온`(auto-M1-1775362462896: verification_needed); M4 `볼뉴머`(auto-M4-1775362490962: classification_issue); M4 `꿀광주사`(auto-M4-1775402593549: is_marketing_name, canonical_category); M4 `아기주사`(auto-M4-1775402599755: is_marketing_name, canonical_category); M4 `벨벳주사`(auto-M4-1775402606093: is_marketing_name, canonical_category); M8 `리팟`(auto-M8-1775362936434: correction_note); M9 `소프라노 티타늄`(M9-2-4: classification_issue, reclassified_to); M16 `백옥주사`(M16-1-1: is_marketing_name, canonical_category); M16 `마늘주사`(M16-2-1: is_marketing_name, canonical_category); M16 `신데렐라주사`(M16-2-2: is_marketing_name, canonical_category)

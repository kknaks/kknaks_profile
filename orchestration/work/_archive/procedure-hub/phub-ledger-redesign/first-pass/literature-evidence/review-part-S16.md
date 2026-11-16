# S16 — /categories/M16

[← review.md 목차](./review.md)

- 읽기 상태: read_direct · 마지막 읽은 Pointer `/categories/M16/effects/1/patient_ja`
- 공동 참조 문맥(소유 아님): `/source_method`, `/accuracy_summary`, `/categories/M16/name`

## 1. 원문 값 (원본 컬럼명 그대로 · 원문 순서)

원문 값 칸은 JSON 리터럴 그대로다(이스케이프 포함). 관찰은 이 표에 섞지 않고 §2 에 둔다. 표현 ID 는 expressions.json.

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 | 파일 cp [s,e) | 형태소 | 표현 ID |
|---|---|---|---|---|---|---|
| `/categories/M16` | M16 | object | (object, 자식 4) | 90271–93545 |  |  |
| `/categories/M16/name` | name | string | "Intravenous micronutrient / antioxidant therapy (aesthetic)" | 90279–90340 | excluded | E0713, E0714 |
| `/categories/M16/moa` | moa | array | (array, 자식 1) | 90347–91120 |  |  |
| `/categories/M16/moa/0` | [0] | object | (object, 자식 8) | 90348–91119 |  |  |
| `/categories/M16/moa/0/statement` | statement | string | "Glutathione inhibits tyrosinase activity and shifts melanogenesis from eumelanin toward pheomelanin in cultured melanocytes." | 90361–90487 | excluded | E0715, E0716, E0717 |
| `/categories/M16/moa/0/citations` | citations | array | (array, 자식 1) | 90500–90774 |  |  |
| `/categories/M16/moa/0/citations/0` | [0] | object | (object, 자식 6) | 90501–90773 |  |  |
| `/categories/M16/moa/0/citations/0/authors` | authors | string | "Sonthalia S, Daulatabad D, Sarkar R" | 90512–90549 | excluded |  |
| `/categories/M16/moa/0/citations/0/title` | title | string | "Glutathione as a skin whitening agent: Facts, myths, evidence and controversies." | 90558–90640 | excluded |  |
| `/categories/M16/moa/0/citations/0/journal` | journal | string | "Indian journal of dermatology, venereology and leprology" | 90651–90709 | excluded |  |
| `/categories/M16/moa/0/citations/0/year` | year | number_int | 2016 | 90717–90721 | excluded |  |
| `/categories/M16/moa/0/citations/0/pmid` | pmid | string | "27088927" | 90729–90739 | excluded |  |
| `/categories/M16/moa/0/citations/0/doi` | doi | string | "10.4103/0378-6323.179088" | 90746–90772 | excluded |  |
| `/categories/M16/moa/0/accuracy_score` | accuracy_score | number_int | 90 | 90792–90794 | excluded |  |
| `/categories/M16/moa/0/accuracy_note` | accuracy_note | string | "글루타치온은 타이로시나제 억제 및 멜라닌 합성 경로 전환을 유도함." | 90811–90850 | applied |  |
| `/categories/M16/moa/0/patient_ko` | patient_ko | string | "피부색을 결정하는 성분의 생성을 조절하여 어두운 톤 대신 밝은 톤이 돌도록 도와줍니다." | 90864–90914 | applied | E0718 |
| `/categories/M16/moa/0/patient_en` | patient_en | string | "A specialized ingredient helps guide your skin's natural tones toward a brighter look." | 90928–91016 | excluded |  |
| `/categories/M16/moa/0/patient_zh` | patient_zh | string | "一种专业成分有助于引导您的皮肤自然色调，从而呈现出更加明亮的观感。" | 91030–91065 | excluded |  |
| `/categories/M16/moa/0/patient_ja` | patient_ja | string | "お肌の色むらを整える働きをサポートし、透明感のある明るい印象へと導きます。" | 91079–91118 | excluded |  |
| `/categories/M16/adverse_effects` | adverse_effects | array | (array, 자식 1) | 91139–91968 |  |  |
| `/categories/M16/adverse_effects/0` | [0] | object | (object, 자식 8) | 91140–91967 |  |  |
| `/categories/M16/adverse_effects/0/statement` | statement | string | "Glutathione intravenous skin-lightening use has been associated with skin rashes, Stevens-Johnson-like reactions, and reports of renal and liver dysfunction." | 91153–91312 | excluded | E0719, E0720, E0721 |
| `/categories/M16/adverse_effects/0/citations` | citations | array | (array, 자식 1) | 91325–91599 |  |  |
| `/categories/M16/adverse_effects/0/citations/0` | [0] | object | (object, 자식 6) | 91326–91598 |  |  |
| `/categories/M16/adverse_effects/0/citations/0/authors` | authors | string | "Sonthalia S, Daulatabad D, Sarkar R" | 91337–91374 | excluded |  |
| `/categories/M16/adverse_effects/0/citations/0/title` | title | string | "Glutathione as a skin whitening agent: Facts, myths, evidence and controversies." | 91383–91465 | excluded |  |
| `/categories/M16/adverse_effects/0/citations/0/journal` | journal | string | "Indian journal of dermatology, venereology and leprology" | 91476–91534 | excluded |  |
| `/categories/M16/adverse_effects/0/citations/0/year` | year | number_int | 2016 | 91542–91546 | excluded |  |
| `/categories/M16/adverse_effects/0/citations/0/pmid` | pmid | string | "27088927" | 91554–91564 | excluded |  |
| `/categories/M16/adverse_effects/0/citations/0/doi` | doi | string | "10.4103/0378-6323.179088" | 91571–91597 | excluded |  |
| `/categories/M16/adverse_effects/0/accuracy_score` | accuracy_score | number_int | 85 | 91617–91619 | excluded |  |
| `/categories/M16/adverse_effects/0/accuracy_note` | accuracy_note | string | "글루타치온 주사는 드물게 스티븐스-존슨 증후군 등 심각한 피부 반응 보고가 있음." | 91636–91683 | applied | E0722, E0723 |
| `/categories/M16/adverse_effects/0/patient_ko` | patient_ko | string | "피부를 밝게 하려는 관리는 드물게 심한 피부 발진이나 간, 신장 수치 변화를 일으킬 수 있습니다." | 91697–91753 | applied | E0724, E0725, E0726 |
| `/categories/M16/adverse_effects/0/patient_en` | patient_en | string | "Very rare sensitivities like temporary skin reactions can occur with focused wellness care." | 91767–91860 | excluded | E0727, E0728, E0729, E0730 |
| `/categories/M16/adverse_effects/0/patient_zh` | patient_zh | string | "在进行针对性健康护理时，极少数情况下可能会出现暂时的皮肤反应等敏感现象。" | 91874–91912 | excluded |  |
| `/categories/M16/adverse_effects/0/patient_ja` | patient_ja | string | "特別なケアの際、まれに一時的なお肌の赤みや不快感が生じる可能性がございます。" | 91926–91966 | excluded |  |
| `/categories/M16/effects` | effects | array | (array, 자식 2) | 91979–93544 |  |  |
| `/categories/M16/effects/0` | [0] | object | (object, 자식 8) | 91980–92806 |  |  |
| `/categories/M16/effects/0/statement` | statement | string | "Intravenous glutathione for skin lightening is not supported by the US FDA or multiple national regulatory agencies and has insufficient high-quality efficacy evidence." | 91993–92163 | excluded | E0731, E0732, E0733, E0734 |
| `/categories/M16/effects/0/citations` | citations | array | (array, 자식 1) | 92176–92450 |  |  |
| `/categories/M16/effects/0/citations/0` | [0] | object | (object, 자식 6) | 92177–92449 |  |  |
| `/categories/M16/effects/0/citations/0/authors` | authors | string | "Sonthalia S, Daulatabad D, Sarkar R" | 92188–92225 | excluded |  |
| `/categories/M16/effects/0/citations/0/title` | title | string | "Glutathione as a skin whitening agent: Facts, myths, evidence and controversies." | 92234–92316 | excluded |  |
| `/categories/M16/effects/0/citations/0/journal` | journal | string | "Indian journal of dermatology, venereology and leprology" | 92327–92385 | excluded |  |
| `/categories/M16/effects/0/citations/0/year` | year | number_int | 2016 | 92393–92397 | excluded |  |
| `/categories/M16/effects/0/citations/0/pmid` | pmid | string | "27088927" | 92405–92415 | excluded |  |
| `/categories/M16/effects/0/citations/0/doi` | doi | string | "10.4103/0378-6323.179088" | 92422–92448 | excluded |  |
| `/categories/M16/effects/0/accuracy_score` | accuracy_score | number_int | 85 | 92468–92470 | excluded |  |
| `/categories/M16/effects/0/accuracy_note` | accuracy_note | string | "미백 목적의 글루타치온 주사는 FDA 승인 사항이 아니며 근거 수준에 논란이 있음." | 92487–92535 | applied | E0735, E0736 |
| `/categories/M16/effects/0/patient_ko` | patient_ko | string | "피부 미백을 위해 주사하는 방법은 아직 공식적인 승인이나 명확한 효과 증거가 부족합니다." | 92549–92600 | applied | E0737 |
| `/categories/M16/effects/0/patient_en` | patient_en | string | "Focused wellness care works to support your body's natural clarity and radiance." | 92614–92696 | excluded | E0738 |
| `/categories/M16/effects/0/patient_zh` | patient_zh | string | "针对性的健康护理致力于支持您身体自然的纯净度，让您由内而外焕发光彩。" | 92710–92746 | excluded |  |
| `/categories/M16/effects/0/patient_ja` | patient_ja | string | "体の内側から働きかけることで、お肌本来の透明感と明るい印象を引き出すサポートをします。" | 92760–92805 | excluded |  |
| `/categories/M16/effects/1` | [1] | object | (object, 자식 8) | 92807–93543 |  |  |
| `/categories/M16/effects/1/statement` | statement | string | "Topical vitamin C is supported by stronger evidence than IV vitamin C for photoaging and pigmentation." | 92820–92924 | excluded | E0739, E0740, E0741 |
| `/categories/M16/effects/1/citations` | citations | array | (array, 자식 1) | 92937–93191 |  |  |
| `/categories/M16/effects/1/citations/0` | [0] | object | (object, 자식 8) | 92938–93190 |  |  |
| `/categories/M16/effects/1/citations/0/authors` | authors | string | "Pullar JM, Carr AC, Vissers MCM" | 92949–92982 | excluded |  |
| `/categories/M16/effects/1/citations/0/title` | title | string | "The Roles of Vitamin C in Skin Health." | 92991–93031 | excluded |  |
| `/categories/M16/effects/1/citations/0/journal` | journal | string | "Nutrients" | 93042–93053 | excluded |  |
| `/categories/M16/effects/1/citations/0/year` | year | number_int | 2017 | 93061–93065 | excluded |  |
| `/categories/M16/effects/1/citations/0/pmid` | pmid | string | "28805671" | 93073–93083 | excluded |  |
| `/categories/M16/effects/1/citations/0/doi` | doi | string | "10.3390/nu9080866" | 93090–93109 | excluded |  |
| `/categories/M16/effects/1/citations/0/pmc` | pmc | string | "PMC5579659" | 93116–93128 | excluded |  |
| `/categories/M16/effects/1/citations/0/oa_url` | oa_url | string | "https://pmc.ncbi.nlm.nih.gov/articles/PMC5579659/" | 93138–93189 | excluded |  |
| `/categories/M16/effects/1/accuracy_score` | accuracy_score | number_int | 90 | 93209–93211 | excluded |  |
| `/categories/M16/effects/1/accuracy_note` | accuracy_note | string | "미백 및 항노화 효과 측면에서는 바르는 비타민 C의 근거가 더 풍부함." | 93228–93269 | applied | E0742, E0743, E0744 |
| `/categories/M16/effects/1/patient_ko` | patient_ko | string | "피부 노화나 색소 개선에는 주사보다 피부에 직접 바르는 형태가 더 확실한 효과를 보입니다." | 93283–93335 | applied | E0745, E0746 |
| `/categories/M16/effects/1/patient_en` | patient_en | string | "Daily topical care is a reliable way to help manage uneven tones and signs of aging." | 93349–93435 | excluded | E0747, E0748, E0749 |
| `/categories/M16/effects/1/patient_zh` | patient_zh | string | "日常的外用护理是帮助管理肤色不均和缓解老化迹象的可靠方式，非常有效。" | 93449–93485 | excluded |  |
| `/categories/M16/effects/1/patient_ja` | patient_ja | string | "毎日のお手入れを続けることで、気になる色むらやエイジングサインを穏やかに整えます。" | 93499–93542 | excluded |  |

## 2. 잠정 관찰 (원문과 분리 · 근거 Pointer 포함)

- **S16-O1** [P] `/categories/M16/moa/0/statement` — 'in cultured melanocytes' — 배양 세포(시험관) 조건의 기전 진술. patient_ko/en/zh/ja 는 이 조건을 모두 뺌.
- **S16-O2** [P] `/categories/M16/adverse_effects/0/statement`, `/categories/M16/adverse_effects/0/accuracy_note`, `/categories/M16/adverse_effects/0/patient_ko`, `/categories/M16/adverse_effects/0/patient_en` — statement 'has been associated with skin rashes, Stevens-Johnson-like reactions, and reports of renal and liver dysfunction'(연관·보고, 빈도 없음). accuracy_note·patient_ko 는 '드물게' 추가, patient_en 'Very rare sensitivities like temporary skin reactions … with focused wellness care' — 정맥 투여·SJS·간신장 탈락, 'temporary' 추가.
- **S16-O3** [P] `/categories/M16/effects/0/statement`, `/categories/M16/effects/0/patient_en`, `/categories/M16/effects/0/patient_zh`, `/categories/M16/effects/0/patient_ja` — effects/0 statement 는 부정 진술 'is not supported by the US FDA or multiple national regulatory agencies and has insufficient high-quality efficacy evidence'. patient_ko 는 부정을 유지('승인이나 명확한 효과 증거가 부족'). patient_en/zh/ja 는 부정을 없애고 긍정 효과 문장('works to support your body's natural clarity and radiance')으로 바뀜 — 극성 반전.
- **S16-O4** [P] `/categories/M16/effects/1/statement`, `/categories/M16/effects/1/patient_ko`, `/categories/M16/effects/1/patient_en` — effects/1 'Topical vitamin C is supported by stronger evidence than IV vitamin C for photoaging and pigmentation' — 근거 강도 비교(효과 크기 비교 아님). patient_ko '더 확실한 효과를 보입니다'(근거→효과로 바뀜), patient_en 'Daily topical care is a reliable way'(IV 비교 탈락, 'Daily' 추가). 이 진술의 주어(topical vitamin C)는 M16 정맥요법이 아니라 바르는 제형이다(M15 와의 연결은 후속).
- **S16-O5** [P] `/categories/M16/moa/0/citations/0` — Sonthalia 2016 'Glutathione as a skin whitening agent: Facts, myths, evidence and controversies.' — pmc·oa_url 없는 6키 인용. moa/0·AE/0·effects/0 근거.
- **S16-O6** [P] `/categories/M16/name` — name 'Intravenous micronutrient / antioxidant therapy (aesthetic)' — '/' 병기, '(aesthetic)' 목적 한정.

## 3. 수동 표현 (직접 읽기에서 수집)

| 표현 ID | Pointer | 구간 | 원문 구절 | facets | 상태 | 메모 |
|---|---|---|---|---|---|---|
| E0713 | `/categories/M16/name` | 0–47 | Intravenous micronutrient / antioxidant therapy | name_candidate, route, alternative_list | P |  |
| E0714 | `/categories/M16/name` | 48–59 | (aesthetic) | purpose, scope | P |  |
| E0715 | `/categories/M16/moa/0/statement` | 12–40 | inhibits tyrosinase activity | mechanism, negation | P |  |
| E0716 | `/categories/M16/moa/0/statement` | 45–99 | shifts melanogenesis from eumelanin toward pheomelanin | mechanism, direction | P |  |
| E0717 | `/categories/M16/moa/0/statement` | 100–123 | in cultured melanocytes | evidence_context, condition | P |  |
| E0718 | `/categories/M16/moa/0/patient_ko` | 23–41 | 어두운 톤 대신 밝은 톤이 돌도록 | direction, comparison | P |  |
| E0719 | `/categories/M16/adverse_effects/0/statement` | 0–43 | Glutathione intravenous skin-lightening use | route, purpose, ingredient | P |  |
| E0720 | `/categories/M16/adverse_effects/0/statement` | 44–68 | has been associated with | evidence_status | P |  |
| E0721 | `/categories/M16/adverse_effects/0/statement` | 69–156 | skin rashes, Stevens-Johnson-like reactions, and reports of renal and liver dysfunction | event, evidence_status | P |  |
| E0722 | `/categories/M16/adverse_effects/0/accuracy_note` | 10–44 | 드물게 스티븐스-존슨 증후군 등 심각한 피부 반응 보고가 있음 | frequency, degree, event, evidence_status | I | statement 에 빈도 없음 |
| E0724 | `/categories/M16/adverse_effects/0/patient_ko` | 15–53 | 드물게 심한 피부 발진이나 간, 신장 수치 변화를 일으킬 수 있습니다 | frequency, degree, event, possibility | P |  |
| E0727 | `/categories/M16/adverse_effects/0/patient_en` | 0–63 | Very rare sensitivities like temporary skin reactions can occur | frequency, duration_quality, possibility | I | SJS·간신장 탈락 |
| E0730 | `/categories/M16/adverse_effects/0/patient_en` | 69–90 | focused wellness care | name_candidate | I | 정맥 투여 표현 탈락 |
| E0731 | `/categories/M16/effects/0/statement` | 44–115 | is not supported by the US FDA or multiple national regulatory agencies | negation, regulatory | P |  |
| E0733 | `/categories/M16/effects/0/statement` | 120–167 | has insufficient high-quality efficacy evidence | negation, evidence_status | P |  |
| E0735 | `/categories/M16/effects/0/accuracy_note` | 17–45 | FDA 승인 사항이 아니며 근거 수준에 논란이 있음 | negation, regulatory, evidence_status | P |  |
| E0737 | `/categories/M16/effects/0/patient_ko` | 19–48 | 아직 공식적인 승인이나 명확한 효과 증거가 부족합니다 | negation, regulatory, evidence_status, time | P |  |
| E0738 | `/categories/M16/effects/0/patient_en` | 22–79 | works to support your body's natural clarity and radiance | effect | I | 부정 진술이 긍정으로 |
| E0739 | `/categories/M16/effects/1/statement` | 18–69 | is supported by stronger evidence than IV vitamin C | comparison, evidence_status, route | P |  |
| E0741 | `/categories/M16/effects/1/statement` | 70–101 | for photoaging and pigmentation | concern, scope | P |  |
| E0742 | `/categories/M16/effects/1/accuracy_note` | 18–38 | 바르는 비타민 C의 근거가 더 풍부함 | comparison, evidence_status | P |  |
| E0745 | `/categories/M16/effects/1/patient_ko` | 15–49 | 주사보다 피부에 직접 바르는 형태가 더 확실한 효과를 보입니다 | comparison, route, effect | I | 근거 비교가 효과 비교로 |
| E0747 | `/categories/M16/effects/1/patient_en` | 0–18 | Daily topical care | frequency, route | I | IV 비교 탈락·'Daily' 추가 |
| E0748 | `/categories/M16/effects/1/patient_en` | 52–83 | uneven tones and signs of aging | concern, negation | P | 읽기 검토(정규식 미포함 후보 대조)에서 추가 |

## 4. 미결

- **S16-I1** [I] `/categories/M16/effects/0/patient_en`, `/categories/M16/effects/0/patient_zh`, `/categories/M16/effects/0/patient_ja` — 부정·불승인 진술(effects/0)이 en/zh/ja 에서 긍정 효과 문장으로 반전. 가장 영향 큰 언어 간 불일치 사례. I-LANG.
- **S16-I2** [I] `/categories/M16/adverse_effects/0/patient_en`, `/categories/M16/adverse_effects/0/accuracy_note`, `/categories/M16/adverse_effects/0/patient_ko`, `/categories/M16/effects/1/patient_ko`, `/categories/M16/effects/1/patient_en` — 중증 사건 탈락·'temporary'·'드물게' 추가, 근거 비교→효과 비교. I-LANG.
- **S16-F1** [F] `/categories/M16/effects/1/statement` — topical vitamin C 진술이 IV 카테고리에 있음 — 대상 시술 연결(M15 등)은 후속, 원문 위치 보존.
- **S16-F2** [F] `/categories/M16/effects/0` — effects 배열의 '효과 근거 불충분' 진술 — 정보 종류(근거 상태) 후속 판단.
- **S16-B1** [B] `/categories/M16/adverse_effects/0/statement` — 빈도 정보 없음('드물게' 근거 없음).

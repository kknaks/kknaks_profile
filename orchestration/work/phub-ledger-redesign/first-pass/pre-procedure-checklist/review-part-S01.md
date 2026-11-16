# review-part-S01 — universal_checks 전체 (12항목)

- 원본: `orchestration/work/phub-recommend/bronze/phub-ledger/pre-procedure-checklist.json` (sha256 `0de87bff91f721fe685884025d31749017d44da250492b2db9d49109a61e4086`)
- 직접 읽기 상태: **read** — /universal_checks/0 … /universal_checks/11 의 id·label·type·description 48말단 전부
- 소유 Pointer: `/universal_checks`
- 공동 참조 문맥(소유 아님): `/description`
- 열 구분: **원문 값** 칸은 원본 그대로(가공 없음). 관찰은 아래 별도 절에만 있다. 형태소 열은 kiwi 원시 결과(`form/tag`)이며 도메인 정답이 아니다.

## 원문 값 (원본 컬럼명 그대로, 원본 순서)

| JSON Pointer | 원본 컬럼명(key/index) | 자료형 | 원문 값 | 분석 적용 | kiwi 원시 토큰(form/tag) |
|---|---|---|---|---|---|
| `/universal_checks` | `universal_checks` | array(자식 12) |  | — | — |
| `/universal_checks/0` | `[0]` | object(자식 4) | keys=['id', 'label', 'type', 'description'] | — | — |
| `/universal_checks/0/id` | `id` | string | allergies | excluded | — |
| `/universal_checks/0/label` | `label` | string | 알레르기 병력 | analyzed | 알레르기/NNG 병력/NNG |
| `/universal_checks/0/type` | `type` | string | must_check | excluded | — |
| `/universal_checks/0/description` | `description` | string | 약물/식품/라텍스 알레르기 | analyzed | 약물/NNG //SP 식품/NNG //SP 라텍스/NNP 알레르기/NNG |
| `/universal_checks/1` | `[1]` | object(자식 4) | keys=['id', 'label', 'type', 'description'] | — | — |
| `/universal_checks/1/id` | `id` | string | anticoagulants | excluded | — |
| `/universal_checks/1/label` | `label` | string | 항응고제/항혈소판제 | analyzed | 항응고제/NNP //SP 항혈소판제/NNP |
| `/universal_checks/1/type` | `type` | string | must_check | excluded | — |
| `/universal_checks/1/description` | `description` | string | 아스피린, 와파린, NOAC, 오메가3, 은행잎 추출물 등 — 멍/출혈 위험 안내. 중단 여부는 처방의와 상의 필수. | analyzed | 아스피린/NNP ,/SP 와파린/NNP ,/SP NOAC/SL ,/SP 오메가/NNG 3/SN ,/SP 은행/NNG 잎/NNG 추출물/NNG 등/NNB —/SW 멍/NNG //SP 출혈/NNG 위험/NNG 안내/NNG ./SF 중단/NNG 여부/NNG 는/JX 처방/NNG 의/JKG 와/JKB 상의/NNG 필수/NNG ./SF |
| `/universal_checks/2` | `[2]` | object(자식 4) | keys=['id', 'label', 'type', 'description'] | — | — |
| `/universal_checks/2/id` | `id` | string | autoimmune | excluded | — |
| `/universal_checks/2/label` | `label` | string | 자가면역질환 | analyzed | 자가/NNG 면역/NNG 질환/NNG |
| `/universal_checks/2/type` | `type` | string | must_check | excluded | — |
| `/universal_checks/2/description` | `description` | string | 루푸스, 류마티스, 경피증 등 — 시술 반응 예측 어려움, 이물반응/상처 회복 지연 위험 증가 | analyzed | 루푸스/NNP ,/SP 류마티스/NNG ,/SP 경피증/NNP 등/NNB —/SW 시술/NNG 반응/NNG 예측/NNG 어려움/NNG ,/SP 이물/NNG 반응/NNG //SP 상처/NNG 회복/NNG 지연/NNG 위험/NNG 증가/NNG |
| `/universal_checks/3` | `[3]` | object(자식 4) | keys=['id', 'label', 'type', 'description'] | — | — |
| `/universal_checks/3/id` | `id` | string | breastfeeding | excluded | — |
| `/universal_checks/3/label` | `label` | string | 수유 여부 | analyzed | 수유/NNP 여부/NNG |
| `/universal_checks/3/type` | `type` | string | relative_contraindication | excluded | — |
| `/universal_checks/3/description` | `description` | string | 수유 중인 경우 일부 시술 제한. 시술별 개별 판단 필요 | analyzed | 수유/NNP 중/NNB 이/VCP ᆫ/ETM 경우/NNG 일부/NNG 시술/NNG 제한/NNG ./SF 시술/NNG 별/XSN 개별/NNG 판단/NNG 필요/NNG |
| `/universal_checks/4` | `[4]` | object(자식 4) | keys=['id', 'label', 'type', 'description'] | — | — |
| `/universal_checks/4/id` | `id` | string | expectations | excluded | — |
| `/universal_checks/4/label` | `label` | string | 기대치 확인 | analyzed | 기대치/NNG 확인/NNG |
| `/universal_checks/4/type` | `type` | string | counseling | excluded | — |
| `/universal_checks/4/description` | `description` | string | 현실적인 결과 설명 | analyzed | 현실/NNG 적/XSN 이/VCP ᆫ/ETM 결과/NNG 설명/NNG |
| `/universal_checks/5` | `[5]` | object(자식 4) | keys=['id', 'label', 'type', 'description'] | — | — |
| `/universal_checks/5/id` | `id` | string | herpes | excluded | — |
| `/universal_checks/5/label` | `label` | string | 헤르페스 병력 | analyzed | 헤르페스/NNG 병력/NNG |
| `/universal_checks/5/type` | `type` | string | must_check | excluded | — |
| `/universal_checks/5/description` | `description` | string | 구순포진 병력 시 항바이러스 예방 투여 필요 (발라시클로비르 500mg x2 또는 아시클로비르 400mg x2, 시술 3일 전부터) | analyzed | 구/NNP 순/NNB 포진/NNG 병력/NNG 시/NNB 항/NNG 바이러스/NNG 예방/NNG 투여/NNG 필요/NNG (/SSO 발라시클로비르/NNP 500/SN mg/SL x/SL 2/SN 또는/MAJ 아시클로비르/NNG 400/SN mg/SL x/SL 2/SN ,/SP 시술/NNG 3/SN 일/NNB 전/NNG 부터/JX )/SSC |
| `/universal_checks/6` | `[6]` | object(자식 4) | keys=['id', 'label', 'type', 'description'] | — | — |
| `/universal_checks/6/id` | `id` | string | isotretinoin | excluded | — |
| `/universal_checks/6/label` | `label` | string | 이소트레티노인 복용력 | analyzed | 이소트레티노인/NNG 복용/NNG 력/XSN |
| `/universal_checks/6/type` | `type` | string | inform | excluded | — |
| `/universal_checks/6/description` | `description` | string | 프락셔널/얕은 필링은 중단 후 최소 6개월, 박리성(ablative) 레이저는 12개월 대기 원칙. 상처 회복 지연·비후성 반흔 위험. 2017 AAD Task Force 이후 비박리성 얕은 시술은 피부 재생 상태에 따라 의사 판단으로 조기 시행 고려 가능. 중단 후 기간 반드시 확인. | analyzed | 프락셔널/NNG //SP 얕/VA 은/ETM 필링/NNG 은/JX 중단/NNG 후/NNG 최소/NNG 6/SN 개월/NNB ,/SP 박리성/NNP (/SSO ablative/SL )/SSC 레이저/NNG 는/JX 12/SN 개월/NNB 대기/NNG 원칙/NNG ./SF 상처/NNG 회복/NNG 지연/NNG ·/SP 비후/NNG 성/XSN 반흔/NNG 위험/NNG ./SF 2017/SN AAD/SL Task/SL Force/SL 이후/NNG 비/XPN 박/NNG 리/XSN 성/NNG 얕/VA 은/ETM 시술/NNG 은/JX 피부/NNG 재생/NNG 상태/NNG 에/JKB 따르/VV 어/EC 의사/NNG 판단/NNG 으로/JKB 조기/NNG 시행/NNG 고려/NNG 가능/NNG ./SF 중단/NNG 후/NNG 기간/NNG 반드시/MAG 확인/NNG ./SF |
| `/universal_checks/7` | `[7]` | object(자식 4) | keys=['id', 'label', 'type', 'description'] | — | — |
| `/universal_checks/7/id` | `id` | string | medical_history | excluded | — |
| `/universal_checks/7/label` | `label` | string | 기저질환 | analyzed | 기저/NNG 질환/NNG |
| `/universal_checks/7/type` | `type` | string | must_check | excluded | — |
| `/universal_checks/7/description` | `description` | string | 자가면역질환, 켈로이드 체질, 당뇨, 간질환 | analyzed | 자가/NNG 면역/NNG 질환/NNG ,/SP 켈로이드/NNG 체질/NNG ,/SP 당뇨/NNG ,/SP 간/NNG 질환/NNG |
| `/universal_checks/8` | `[8]` | object(자식 4) | keys=['id', 'label', 'type', 'description'] | — | — |
| `/universal_checks/8/id` | `id` | string | medications | excluded | — |
| `/universal_checks/8/label` | `label` | string | 현재 복용 약물 | analyzed | 현재/MAG 복용/NNG 약물/NNG |
| `/universal_checks/8/type` | `type` | string | must_check | excluded | — |
| `/universal_checks/8/description` | `description` | string | 항응고제, NSAIDs, 이소트레티노인 등 | analyzed | 항응고제/NNP ,/SP NSAIDs/SL ,/SP 이소트레티노인/NNP 등/NNB |
| `/universal_checks/9` | `[9]` | object(자식 4) | keys=['id', 'label', 'type', 'description'] | — | — |
| `/universal_checks/9/id` | `id` | string | pregnancy | excluded | — |
| `/universal_checks/9/label` | `label` | string | 임신 여부 | analyzed | 임신/NNG 여부/NNG |
| `/universal_checks/9/type` | `type` | string | absolute_contraindication | excluded | — |
| `/universal_checks/9/description` | `description` | string | 임신 중이거나 임신 가능성이 있는 경우 대부분의 시술 불가 | analyzed | 임신/NNG 중/NNB 이/VCP 거나/EC 임신/NNG 가능/NNG 성/XSN 이/JKS 있/VV 는/ETM 경우/NNG 대부분/NNG 의/JKG 시술/NNG 불가/NNG |
| `/universal_checks/10` | `[10]` | object(자식 4) | keys=['id', 'label', 'type', 'description'] | — | — |
| `/universal_checks/10/id` | `id` | string | previous_procedures | excluded | — |
| `/universal_checks/10/label` | `label` | string | 최근 시술 이력 | analyzed | 최근/NNG 시술/NNG 이력/NNG |
| `/universal_checks/10/type` | `type` | string | must_check | excluded | — |
| `/universal_checks/10/description` | `description` | string | 최근 받은 시술과 시기 | analyzed | 최근/NNG 받/VV-R 은/ETM 시술/NNG 과/JC 시기/NNG |
| `/universal_checks/11` | `[11]` | object(자식 4) | keys=['id', 'label', 'type', 'description'] | — | — |
| `/universal_checks/11/id` | `id` | string | skin_condition | excluded | — |
| `/universal_checks/11/label` | `label` | string | 시술 부위 피부 상태 | analyzed | 시술/NNG 부위/NNG 피부/NNG 상태/NNG |
| `/universal_checks/11/type` | `type` | string | must_check | excluded | — |
| `/universal_checks/11/description` | `description` | string | 감염, 염증, 상처, 헤르페스 활성 | analyzed | 감염/NNG ,/SP 염증/NNG ,/SP 상처/NNG ,/SP 헤르페스/NNG 활성/NNG |

## 자동 표현 후보 (정규식 일치분만 — 패턴 밖은 아래 수동 절)

- **AP-NUM-UNIT** (5): `/universal_checks/5/description`[34,39) «500mg»; `/universal_checks/5/description`[53,58) «400mg»; `/universal_checks/5/description`[66,68) «3일»; `/universal_checks/6/description`[20,23) «6개월»; `/universal_checks/6/description`[44,48) «12개월»
- **AP-MULT** (2): `/universal_checks/5/description`[40,42) «x2»; `/universal_checks/5/description`[59,61) «x2»
- **AP-YEAR** (1): `/universal_checks/6/description`[76,80) «2017»
- **AP-PAREN** (2): `/universal_checks/5/description`[25,73) «(발라시클로비르 500mg x2 또는 아시클로비르 400mg x2, 시술 3일 전부터)»; `/universal_checks/6/description`[28,38) «(ablative)»
- **AP-SLASH** (5): `/universal_checks/0/description`[0,9) «약물/식품/라텍스»; `/universal_checks/1/label`[0,10) «항응고제/항혈소판제»; `/universal_checks/1/description`[35,39) «멍/출혈»; `/universal_checks/2/description`[33,40) «이물반응/상처»; `/universal_checks/6/description`[0,7) «프락셔널/얕은»
- **AP-DASH** (2): `/universal_checks/1/description`[33,65) «— 멍/출혈 위험 안내. 중단 여부는 처방의와 상의 필수.»; `/universal_checks/2/description`[17,52) «— 시술 반응 예측 어려움, 이물반응/상처 회복 지연 위험 증가»
- **AP-ALT** (1): `/universal_checks/5/description`[43,45) «또는»
- **AP-NEG** (3): `/universal_checks/3/description`[15,17) «제한»; `/universal_checks/6/description`[99,100) «비»; `/universal_checks/9/description`[30,32) «불가»
- **AP-POSS** (6): `/universal_checks/1/description`[40,42) «위험»; `/universal_checks/2/description`[28,31) «어려움»; `/universal_checks/2/description`[47,49) «위험»; `/universal_checks/6/description`[72,74) «위험»; `/universal_checks/6/description`[141,143) «가능»; `/universal_checks/9/description`[11,14) «가능성»
- **AP-COND** (14): `/universal_checks/1/description`[47,49) «중단»; `/universal_checks/3/description`[3,5) «중인»; `/universal_checks/3/description`[6,8) «경우»; `/universal_checks/5/description`[7,9) « 시»; `/universal_checks/5/description`[69,72) «전부터»; `/universal_checks/6/description`[12,14) «중단»; `/universal_checks/6/description`[15,16) «후»; `/universal_checks/6/description`[49,51) «대기»; `/universal_checks/6/description`[96,98) «이후»; `/universal_checks/6/description`[121,123) «따라»; `/universal_checks/6/description`[145,147) «중단»; `/universal_checks/6/description`[148,149) «후»; `/universal_checks/9/description`[3,7) «중이거나»; `/universal_checks/9/description`[19,21) «경우»
- **AP-MODAL** (13): `/universal_checks/1/description`[43,45) «안내»; `/universal_checks/1/description`[59,61) «상의»; `/universal_checks/1/description`[62,64) «필수»; `/universal_checks/3/description`[26,28) «판단»; `/universal_checks/3/description`[29,31) «필요»; `/universal_checks/4/label`[4,6) «확인»; `/universal_checks/4/description`[8,10) «설명»; `/universal_checks/5/description`[22,24) «필요»; `/universal_checks/6/description`[52,54) «원칙»; `/universal_checks/6/description`[127,129) «판단»; `/universal_checks/6/description`[138,140) «고려»; `/universal_checks/6/description`[153,156) «반드시»; `/universal_checks/6/description`[157,159) «확인»
- **AP-DEGREE** (6): `/universal_checks/3/description`[9,11) «일부»; `/universal_checks/6/description`[17,19) «최소»; `/universal_checks/6/description`[132,134) «조기»; `/universal_checks/9/description`[22,25) «대부분»; `/universal_checks/10/label`[0,2) «최근»; `/universal_checks/10/description`[0,2) «최근»
- **AP-ETC** (3): `/universal_checks/1/description`[30,32) « 등»; `/universal_checks/2/description`[14,16) « 등»; `/universal_checks/8/description`[21,23) « 등»

## 수동 수집 표현 (직접 읽기 — 원문 구간)

| Pointer | 구간 | 원문 구절 | 탐색 관점(잠정) | 메모 |
|---|---|---|---|---|
| `/universal_checks/0/description` | [0,14) | 약물/식품/라텍스 알레르기 | 슬래시 나열, 대상 범위 | '알레르기' 가 세 항목 모두에 걸리는지는 잠정 |
| `/universal_checks/1/label` | [0,10) | 항응고제/항혈소판제 | 슬래시 나열, 약물군 |  |
| `/universal_checks/1/description` | [0,32) | 아스피린, 와파린, NOAC, 오메가3, 은행잎 추출물 등 | 열린 나열(등), 약물·보충제 혼합, 영문 약어 | label 은 약물군인데 예시에 보충제(오메가3·은행잎 추출물)가 섞임 |
| `/universal_checks/1/description` | [35,45) | 멍/출혈 위험 안내 | 위험, 행위(안내) |  |
| `/universal_checks/1/description` | [47,64) | 중단 여부는 처방의와 상의 필수 | 의무(필수), 조건(중단 여부), 행위 주체(처방의) | 중단을 지시하지 않고 상의를 필수로 둔다 — 회피/중단 지시와 구분 |
| `/universal_checks/2/description` | [0,16) | 루푸스, 류마티스, 경피증 등 | 열린 나열(등), 질환 예시 |  |
| `/universal_checks/2/description` | [19,31) | 시술 반응 예측 어려움 | 불확실성 |  |
| `/universal_checks/2/description` | [33,52) | 이물반응/상처 회복 지연 위험 증가 | 슬래시 범위, 위험, 증가(정도) | '위험 증가' 가 이물반응·상처 회복 지연 둘 다에 걸리는지 잠정. 자동 AP-SLASH 는 «이물반응/상처» 까지만 잡음 |
| `/universal_checks/3/description` | [0,17) | 수유 중인 경우 일부 시술 제한 | 조건(경우), 범위(일부), 제한 | 어떤 시술인지 원문 없음 |
| `/universal_checks/3/description` | [19,31) | 시술별 개별 판단 필요 | 판단 유보, 필요 |  |
| `/universal_checks/4/label` | [0,6) | 기대치 확인 | 행위 |  |
| `/universal_checks/4/description` | [0,10) | 현실적인 결과 설명 | 형용사(현실적인), 행위(설명) |  |
| `/universal_checks/5/description` | [0,24) | 구순포진 병력 시 항바이러스 예방 투여 필요 | 조건(병력 시), 필요, 예방 | label '헤르페스 병력' 과 description '구순포진 병력' 의 범위 차이 |
| `/universal_checks/5/description` | [26,61) | 발라시클로비르 500mg x2 또는 아시클로비르 400mg x2 | 대안(또는), 용량, x표기 |  |
| `/universal_checks/5/description` | [26,42) | 발라시클로비르 500mg x2 | 약물+용량 |  |
| `/universal_checks/5/description` | [46,61) | 아시클로비르 400mg x2 | 약물+용량 |  |
| `/universal_checks/5/description` | [63,72) | 시술 3일 전부터 | 시점(시술 전), 기간 시작 | 종료 시점·기간은 이 항목에 없음 |
| `/universal_checks/6/label` | [0,11) | 이소트레티노인 복용력 | 약물 이력 |  |
| `/universal_checks/6/description` | [0,23) | 프락셔널/얕은 필링은 중단 후 최소 6개월 | 슬래시 범위, 시점(중단 후), 최소, 기간 | 자동 AP-SLASH 는 «프락셔널/얕은» 까지만 |
| `/universal_checks/6/description` | [0,10) | 프락셔널/얕은 필링 | 슬래시 범위, 형용사(얕은) | '프락셔널 [레이저]' 인지 '프락셔널 필링' 인지 원문에 없음 |
| `/universal_checks/6/description` | [25,54) | 박리성(ablative) 레이저는 12개월 대기 원칙 | 괄호 영문 병기, 기간, 원칙 | '중단 후' 가 생략된 병렬 구조로 보임(잠정) |
| `/universal_checks/6/description` | [56,74) | 상처 회복 지연·비후성 반흔 위험 | 가운뎃점 나열, 위험 |  |
| `/universal_checks/6/description` | [76,98) | 2017 AAD Task Force 이후 | 연도, 출처 언급, 시점(이후) | 외부 출처 언급 — 내용 확인하지 않음 |
| `/universal_checks/6/description` | [99,143) | 비박리성 얕은 시술은 피부 재생 상태에 따라 의사 판단으로 조기 시행 고려 가능 | 부정 접두(비-), 형용사(얕은), 조건(상태에 따라), 주체(의사 판단), 가능성 | 원칙의 예외 진술 |
| `/universal_checks/6/description` | [132,143) | 조기 시행 고려 가능 | 가능성, 시점(조기) |  |
| `/universal_checks/6/description` | [145,159) | 중단 후 기간 반드시 확인 | 의무(반드시), 시점(중단 후) |  |
| `/universal_checks/7/description` | [0,24) | 자가면역질환, 켈로이드 체질, 당뇨, 간질환 | 닫힌 나열(등 없음), 질환 |  |
| `/universal_checks/8/description` | [0,23) | 항응고제, NSAIDs, 이소트레티노인 등 | 열린 나열(등), 영문 약어 |  |
| `/universal_checks/9/description` | [0,21) | 임신 중이거나 임신 가능성이 있는 경우 | 조건(경우), 가능성, 선언(이거나) |  |
| `/universal_checks/9/description` | [22,32) | 대부분의 시술 불가 | 범위(대부분), 부정(불가) | type absolute_contraindication 과 '대부분' 의 범위가 함께 있음 |
| `/universal_checks/10/description` | [0,12) | 최근 받은 시술과 시기 | 시점(최근), 기간 미정 |  |
| `/universal_checks/11/description` | [0,19) | 감염, 염증, 상처, 헤르페스 활성 | 닫힌 나열, 상태 |  |
| `/universal_checks/5/label` | [0,7) | 헤르페스 병력 | 이력(병력) | description 은 '구순포진 병력' 으로 범위가 다름 |
| `/universal_checks/8/label` | [0,8) | 현재 복용 약물 | 시점(현재) |  |
| `/universal_checks/10/label` | [0,8) | 최근 시술 이력 | 시점(최근), 이력 |  |

## 잠정 관찰 (원문 아님 — 근거 위치 포함)

- P: 12항목은 `id` 알파벳순(allergies→skin_condition)으로 놓여 있다(원문 배열 순서 그대로 보존).
- P: 항목 간 내용 겹침 — `/universal_checks/7/description` 에 '자가면역질환'(=`/universal_checks/2` label), `/universal_checks/8/description` 에 '항응고제'·'이소트레티노인'(=`/universal_checks/1`·`/6`), `/universal_checks/11/description` '헤르페스 활성' 과 `/universal_checks/5` '헤르페스 병력'. 같은 대상인지·상하 관계인지 확정하지 않음.
- P: `/universal_checks/6/type` 은 inform 인데 같은 주제가 category_specific(M8·M11·M12·M15)에서는 must_check 로 나온다(S03~S05 참조).
- P: `/universal_checks/9` type absolute_contraindication 과 description '대부분의 시술 불가'(일부 예외 여지) 가 공존. `/universal_checks/3` relative_contraindication 은 '일부 시술 제한'.
- P: description 은 문장(마침표)·명사 나열·구절이 섞여 있다. 마침표가 있는 값: /1, /3, /6.

## 이 구획의 미결 (A=추출/해석 오류, B=원문 정보 부족, C=사용자 결정 필요, K=분석 한계, P=잠정, F=후속, I=원문 불일치)

- **B-S01-1** [open] 'x2' 의 뜻(1일 2회 등)과 투여 기간이 `/universal_checks/5/description` 에 없다 — 단위·횟수 해석 불가(채우지 않음) — 위치: `/universal_checks/5/description`
- **B-S01-2** [open] '일부 시술'(수유)·'대부분의 시술'(임신)이 어떤 시술인지 원문에 없다 — 위치: `/universal_checks/3/description`, `/universal_checks/9/description`
- **B-S01-3** [open] '최근' 의 기간 기준 없음 — 위치: `/universal_checks/10/label`, `/universal_checks/10/description`
- **B-S01-4** [open] '프락셔널/얕은 필링' 의 슬래시 범위(프락셔널 레이저 vs 필링)가 원문만으로 결정되지 않음 — 위치: `/universal_checks/6/description`
- **I-S01-5** [open] 임신 항목 type=absolute_contraindication 인데 description 은 '대부분의 시술 불가'. type 정의가 원문에 없어 불일치인지 확정 못 함 — 원문 변경 제안 아님, 후속 확인 후보 — 위치: `/universal_checks/9/type`, `/universal_checks/9/description`
- **F-S01-6** [deferred] universal 항목 간 겹침(기저질환⊃자가면역질환?, 복용 약물⊃항응고제·이소트레티노인?) 관계 판단은 의미 조사 단계 — 위치: `/universal_checks/7/description`, `/universal_checks/8/description`
- **F-S01-7** [deferred] 헤르페스 예방 투여 문구가 M8 항목과 순서·세부(7-10일 복용)가 다르다 — 같은 지침의 변형인지 후속 비교 — 위치: `/universal_checks/5/description`, `/category_specific/7/checks/4/label`

## 알려진 형태소 오분절 (K — 출현별)

- `/universal_checks/1/description` «처방의와» → 원시 `처방/NNG 의/JKG 와/JKB` — 영향: '처방의'(처방한 의사, 명사)가 '처방'+관형격 조사로 오분석 — 행위 주체 명사 소실
- `/universal_checks/3/label` «수유» → 원시 `수유/NNP` — 영향: 일반명사가 고유명사(NNP)로 태깅 — 품사만 오류
- `/universal_checks/3/description` «수유» → 원시 `수유/NNP` — 영향: 일반명사가 고유명사(NNP)로 태깅 — 품사만 오류
- `/universal_checks/5/description` «구순포진» → 원시 `구/NNP 순/NNB 포진/NNG` — 영향: '구순(입술)' 이 사라져 부위 정보가 토큰에서 소실 — 원문 구절로만 보존
- `/universal_checks/5/description` «항바이러스» → 원시 `항/NNG 바이러스/NNG` — 영향: 접두 '항-' 이 명사로 분리 — '항바이러스'(약효군) 단위 소실
- `/universal_checks/6/description` «비박리성» → 원시 `비/XPN 박/NNG 리/XSN 성/NNG` — 영향: '박리성' 어간이 박/리/성 으로 깨짐. 부정 접두 '비' 는 XPN 으로 남음 — 같은 문장의 '박리성/NNP' 와 토큰 대응 불가

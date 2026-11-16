# review-part-S03 — category_specific M5–M8 (index 4–7)

- 원본: `orchestration/work/phub-recommend/bronze/phub-ledger/pre-procedure-checklist.json` (sha256 `0de87bff91f721fe685884025d31749017d44da250492b2db9d49109a61e4086`)
- 직접 읽기 상태: **read** — /category_specific/4 … /7 (M5 PRP/자가혈 6·M6 지방이식 7·M7 실리프팅 7·M8 레이저 11 = checks 31) id·name·label·type 전부
- 소유 Pointer: `/category_specific/4`, `/category_specific/5`, `/category_specific/6`, `/category_specific/7`
- 공동 참조 문맥(소유 아님): `/description`, `/category_specific`
- 열 구분: **원문 값** 칸은 원본 그대로(가공 없음). 관찰은 아래 별도 절에만 있다. 형태소 열은 kiwi 원시 결과(`form/tag`)이며 도메인 정답이 아니다.

## 원문 값 (원본 컬럼명 그대로, 원본 순서)

| JSON Pointer | 원본 컬럼명(key/index) | 자료형 | 원문 값 | 분석 적용 | kiwi 원시 토큰(form/tag) |
|---|---|---|---|---|---|
| `/category_specific/4` | `[4]` | object(자식 3) | keys=['id', 'name', 'checks'] | — | — |
| `/category_specific/4/id` | `id` | string | M5 | excluded | — |
| `/category_specific/4/name` | `name` | string | PRP/자가혈 | analyzed | PRP/SL //SP 자가혈/NNP |
| `/category_specific/4/checks` | `checks` | array(자식 6) |  | — | — |
| `/category_specific/4/checks/0` | `[0]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/4/checks/0/label` | `label` | string | 혈소판감소증/혈액질환 여부 | analyzed | 혈소판/NNG 감소증/NNG //SP 혈액/NNG 질환/NNG 여부/NNG |
| `/category_specific/4/checks/0/type` | `type` | string | absolute_contraindication | excluded | — |
| `/category_specific/4/checks/1` | `[1]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/4/checks/1/label` | `label` | string | 항응고제/항혈소판제 복용 여부 | analyzed | 항응고제/NNG //SP 항혈소판제/NNG 복용/NNG 여부/NNG |
| `/category_specific/4/checks/1/type` | `type` | string | must_check | excluded | — |
| `/category_specific/4/checks/2` | `[2]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/4/checks/2/label` | `label` | string | 활동성 감염/패혈증 여부 | analyzed | 활동/NNG 성/XSN 감염/NNG //SP 패혈증/NNG 여부/NNG |
| `/category_specific/4/checks/2/type` | `type` | string | absolute_contraindication | excluded | — |
| `/category_specific/4/checks/3` | `[3]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/4/checks/3/label` | `label` | string | 자가면역질환 여부 | analyzed | 자가/NNG 면역/NNG 질환/NNG 여부/NNG |
| `/category_specific/4/checks/3/type` | `type` | string | must_check | excluded | — |
| `/category_specific/4/checks/4` | `[4]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/4/checks/4/label` | `label` | string | NSAIDs 복용 중단 여부 (시술 1주 전) | analyzed | NSAIDs/SL 복용/NNG 중단/NNG 여부/NNG (/SSO 시술/NNG 1/SN 주/NNB 전/NNG )/SSC |
| `/category_specific/4/checks/4/type` | `type` | string | must_check | excluded | — |
| `/category_specific/4/checks/5` | `[5]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/4/checks/5/label` | `label` | string | 채혈량 및 원심분리 과정 설명 | analyzed | 채혈/NNG 량/NNG 및/MAG 원심/NNG 분리/NNG 과정/NNG 설명/NNG |
| `/category_specific/4/checks/5/type` | `type` | string | counseling | excluded | — |
| `/category_specific/5` | `[5]` | object(자식 3) | keys=['id', 'name', 'checks'] | — | — |
| `/category_specific/5/id` | `id` | string | M6 | excluded | — |
| `/category_specific/5/name` | `name` | string | 지방이식 | analyzed | 지방/NNG 이식/NNG |
| `/category_specific/5/checks` | `checks` | array(자식 7) |  | — | — |
| `/category_specific/5/checks/0` | `[0]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/5/checks/0/label` | `label` | string | 마취 알레르기 여부 (리도카인 등) | analyzed | 마취/NNG 알레르기/NNG 여부/NNG (/SSO 리도카인/NNP 등/NNB )/SSC |
| `/category_specific/5/checks/0/type` | `type` | string | absolute_contraindication | excluded | — |
| `/category_specific/5/checks/1` | `[1]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/5/checks/1/label` | `label` | string | 출혈 경향/응고장애 여부 | analyzed | 출혈/NNG 경향/NNG //SP 응고/NNG 장애/NNG 여부/NNG |
| `/category_specific/5/checks/1/type` | `type` | string | must_check | excluded | — |
| `/category_specific/5/checks/2` | `[2]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/5/checks/2/label` | `label` | string | 공여 부위 충분한 지방량 확인 | analyzed | 공여/NNG 부위/NNG 충분/XR 하/XSA ᆫ/ETM 지방량/NNG 확인/NNG |
| `/category_specific/5/checks/2/type` | `type` | string | must_check | excluded | — |
| `/category_specific/5/checks/3` | `[3]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/5/checks/3/label` | `label` | string | 지방색전증 위험 설명 | analyzed | 지방/NNG 색전증/NNG 위험/NNG 설명/NNG |
| `/category_specific/5/checks/3/type` | `type` | string | safety_protocol | excluded | — |
| `/category_specific/5/checks/4` | `[4]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/5/checks/4/label` | `label` | string | 생착률 안내 (30-70%, 개인차) | analyzed | 생착률/NNG 안내/NNG (/SSO 30-70/W_SERIAL %/SW ,/SP 개인차/NNG )/SSC |
| `/category_specific/5/checks/4/type` | `type` | string | counseling | excluded | — |
| `/category_specific/5/checks/5` | `[5]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/5/checks/5/label` | `label` | string | 비대칭/과교정/흡수 가능성 설명 | analyzed | 비대칭/NNP //SP 과교정/NNG //SP 흡수/NNG 가능/NNG 성/XSN 설명/NNG |
| `/category_specific/5/checks/5/type` | `type` | string | counseling | excluded | — |
| `/category_specific/5/checks/6` | `[6]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/5/checks/6/label` | `label` | string | 감염 예방 항생제 준비 확인 | analyzed | 감염/NNG 예방/NNG 항생제/NNG 준비/NNG 확인/NNG |
| `/category_specific/5/checks/6/type` | `type` | string | safety_protocol | excluded | — |
| `/category_specific/6` | `[6]` | object(자식 3) | keys=['id', 'name', 'checks'] | — | — |
| `/category_specific/6/id` | `id` | string | M7 | excluded | — |
| `/category_specific/6/name` | `name` | string | 실리프팅 | analyzed | 실/NNG 리프팅/NNG |
| `/category_specific/6/checks` | `checks` | array(자식 7) |  | — | — |
| `/category_specific/6/checks/0` | `[0]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/6/checks/0/label` | `label` | string | 시술 부위 활동성 감염 여부 | analyzed | 시술/NNG 부위/NNG 활동/NNG 성/XSN 감염/NNG 여부/NNG |
| `/category_specific/6/checks/0/type` | `type` | string | absolute_contraindication | excluded | — |
| `/category_specific/6/checks/1` | `[1]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/6/checks/1/label` | `label` | string | 항응고제 복용 여부 | analyzed | 항응고제/NNG 복용/NNG 여부/NNG |
| `/category_specific/6/checks/1/type` | `type` | string | must_check | excluded | — |
| `/category_specific/6/checks/2` | `[2]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/6/checks/2/label` | `label` | string | 이전 실리프팅 이력 확인 (잔여 실) | analyzed | 이전/NNG 실/NNG 리프팅/NNG 이력/NNG 확인/NNG (/SSO 잔여/NNG 실/NNG )/SSC |
| `/category_specific/6/checks/2/type` | `type` | string | must_check | excluded | — |
| `/category_specific/6/checks/3` | `[3]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/6/checks/3/label` | `label` | string | 켈로이드 체질 확인 | analyzed | 켈로이드/NNG 체질/NNG 확인/NNG |
| `/category_specific/6/checks/3/type` | `type` | string | must_check | excluded | — |
| `/category_specific/6/checks/4` | `[4]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/6/checks/4/label` | `label` | string | 실 종류(녹는 실 vs 비녹는 실) 및 장단점 설명 | analyzed | 실/NNG 종류/NNG (/SSO 녹/VV 는/ETM 실/NNG vs/SL 비/NNG 녹/VV 는/ETM 실/NNG )/SSC 및/MAG 장단점/NNG 설명/NNG |
| `/category_specific/6/checks/4/type` | `type` | string | counseling | excluded | — |
| `/category_specific/6/checks/5` | `[5]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/6/checks/5/label` | `label` | string | 실 돌출/감염/비대칭 가능성 설명 | analyzed | 실/NNG 돌출/NNG //SP 감염/NNG //SP 비/XPN 대칭/NNG 가능/NNG 성/XSN 설명/NNG |
| `/category_specific/6/checks/5/type` | `type` | string | counseling | excluded | — |
| `/category_specific/6/checks/6` | `[6]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/6/checks/6/label` | `label` | string | 시술 후 크게 입벌리기/마사지 제한 안내 | analyzed | 시술/NNG 후/NNG 크/VA 게/EC 입/NNG 벌리/VV 기/ETN //SP 마사지/NNG 제한/NNG 안/MAG 내/VV 어/EF |
| `/category_specific/6/checks/6/type` | `type` | string | inform | excluded | — |
| `/category_specific/7` | `[7]` | object(자식 3) | keys=['id', 'name', 'checks'] | — | — |
| `/category_specific/7/id` | `id` | string | M8 | excluded | — |
| `/category_specific/7/name` | `name` | string | 레이저 | analyzed | 레이저/NNG |
| `/category_specific/7/checks` | `checks` | array(자식 11) |  | — | — |
| `/category_specific/7/checks/0` | `[0]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/7/checks/0/label` | `label` | string | Fitzpatrick 피부타입 확인 (I-VI) | analyzed | Fitzpatrick/SL 피부/NNG 타입/NNG 확인/NNG (/SSO I/SL -/SO VI/SL )/SSC |
| `/category_specific/7/checks/0/type` | `type` | string | must_check | excluded | — |
| `/category_specific/7/checks/1` | `[1]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/7/checks/1/label` | `label` | string | 최근 일광노출/태닝 여부 — 2-4주 이내 자외선 노출 시 에너지 감소 or 시술 연기 판단 | analyzed | 최근/NNG 일광/NNG 노출/NNG //SP 태닝/NNG 여부/NNG —/SW 2-4/W_SERIAL 주/NNB 이내/NNG 자외선/NNG 노출/NNG 시/NNB 에너지/NNG 감소/NNG or/SL 시술/NNG 연기/NNG 판단/NNG |
| `/category_specific/7/checks/1/type` | `type` | string | must_check | excluded | — |
| `/category_specific/7/checks/2` | `[2]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/7/checks/2/label` | `label` | string | 이소트레티노인 복용 여부/중단 시점 확인 — 프락셔널/얕은 필링 6개월, 박리성 레이저 12개월 대기 원칙. 2017 AAD Task Force 이후 비박리성 얕은 시술은 의사 판단 하에 조기 고려 가능 | analyzed | 이소트레티노인/NNG 복용/NNG 여부/NNG //SP 중단/NNG 시점/NNG 확인/NNG —/SW 프락셔널/NNG //SP 얕/VA 은/ETM 필링/NNG 6/SN 개월/NNB ,/SP 박리성/NNP 레이저/NNG 12/SN 개월/NNB 대기/NNG 원칙/NNG ./SF 2017/SN AAD/SL Task/SL Force/SL 이후/NNG 비/XPN 박/NNG 리/XSN 성/NNG 얕/VA 은/ETM 시술/NNG 은/JX 의사/NNG 판단/NNG 하/NNG 에/JKB 조기/NNG 고려/NNG 가능/NNG |
| `/category_specific/7/checks/2/type` | `type` | string | must_check | excluded | — |
| `/category_specific/7/checks/3` | `[3]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/7/checks/3/label` | `label` | string | 광과민성 약물 복용 여부 (독시사이클린, 아미오다론 등) | analyzed | 광/NNG 과민/NNG 성/XSN 약물/NNG 복용/NNG 여부/NNG (/SSO 독시사이클린/NNG ,/SP 아미오다론/NNG 등/NNB )/SSC |
| `/category_specific/7/checks/3/type` | `type` | string | must_check | excluded | — |
| `/category_specific/7/checks/4` | `[4]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/7/checks/4/label` | `label` | string | 헤르페스 병력 확인 — 구순/안면 레이저 시 예방적 항바이러스제 (아시클로비르 400mg x2 또는 발라시클로비르 500mg x2, 시술 3일 전부터 시작, 7-10일 복용) | analyzed | 헤르페스/NNG 병력/NNG 확인/NNG —/SW 구순/NNG //SP 안면/NNG 레이저/NNG 시/NNB 예방/NNG 적/XSN 항바이러스제/NNP (/SSO 아시클로비르/NNP 400/SN mg/SL x/SL 2/SN 또는/MAJ 발라시클로비르/NNG 500/SN mg/SL x/SL 2/SN ,/SP 시술/NNG 3/SN 일/NNB 전/NNG 부터/JX 시작/NNG ,/SP 7-10/W_SERIAL 일/NNB 복용/NNG )/SSC |
| `/category_specific/7/checks/4/type` | `type` | string | must_check | excluded | — |
| `/category_specific/7/checks/5` | `[5]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/7/checks/5/label` | `label` | string | 켈로이드 체질 확인 (어블레이티브 레이저) | analyzed | 켈로이드/NNG 체질/NNG 확인/NNG (/SSO 어블레이티브/NNG 레이저/NNG )/SSC |
| `/category_specific/7/checks/5/type` | `type` | string | must_check | excluded | — |
| `/category_specific/7/checks/6` | `[6]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/7/checks/6/label` | `label` | string | PIH 위험도 평가 (고위험군 사전 미백 치료) | analyzed | PIH/SL 위험도/NNG 평가/NNG (/SSO 고/XPN 위험/NNG 군/NNG 사전/NNG 미백/NNG 치료/NNG )/SSC |
| `/category_specific/7/checks/6/type` | `type` | string | must_check | excluded | — |
| `/category_specific/7/checks/7` | `[7]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/7/checks/7/label` | `label` | string | 중등도 이상 필링 후 최소 2주 대기 확인 — 피부 장벽 회복 전 레이저 시 합병증 위험 | analyzed | 중등/NNG 도/JX 이상/NNG 필링/NNG 후/NNG 최소/NNG 2/SN 주/NNB 대기/NNG 확인/NNG —/SW 피부/NNG 장벽/NNG 회복/NNG 전/NNG 레이저/NNG 시/NNB 합병증/NNG 위험/NNG |
| `/category_specific/7/checks/7/type` | `type` | string | must_check | excluded | — |
| `/category_specific/7/checks/8` | `[8]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/7/checks/8/label` | `label` | string | 금속 임플란트 확인 — RF/HIFU 병행 시 금속 발열 위험 | analyzed | 금속/NNG 임플란트/NNG 확인/NNG —/SW RF/SL //SP HIFU/SL 병행/NNG 시/NNB 금속/NNG 발열/NNG 위험/NNG |
| `/category_specific/7/checks/8/type` | `type` | string | must_check | excluded | — |
| `/category_specific/7/checks/9` | `[9]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/7/checks/9/label` | `label` | string | 보호안경/눈 보호 준비 확인 | analyzed | 보호안경/NNG //SP 눈/NNG 보호/NNG 준비/NNG 확인/NNG |
| `/category_specific/7/checks/9/type` | `type` | string | safety_protocol | excluded | — |
| `/category_specific/7/checks/10` | `[10]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/7/checks/10/label` | `label` | string | 레이저 종류별 다운타임 설명 | analyzed | 레이저/NNG 종류/NNG 별/XSN 다운/NNG 타임/NNG 설명/NNG |
| `/category_specific/7/checks/10/type` | `type` | string | counseling | excluded | — |

## 자동 표현 후보 (정규식 일치분만 — 패턴 밖은 아래 수동 절)

- **AP-NUM-UNIT** (10): `/category_specific/4/checks/4/label`[20,22) «1주»; `/category_specific/5/checks/4/label`[8,14) «30-70%»; `/category_specific/7/checks/1/label`[16,20) «2-4주»; `/category_specific/7/checks/2/label`[36,39) «6개월»; `/category_specific/7/checks/2/label`[49,53) «12개월»; `/category_specific/7/checks/4/label`[44,49) «400mg»; `/category_specific/7/checks/4/label`[64,69) «500mg»; `/category_specific/7/checks/4/label`[77,79) «3일»; `/category_specific/7/checks/4/label`[88,93) «7-10일»; `/category_specific/7/checks/7/label`[15,17) «2주»
- **AP-RANGE** (4): `/category_specific/5/checks/4/label`[8,13) «30-70»; `/category_specific/7/checks/0/label`[21,25) «I-VI»; `/category_specific/7/checks/1/label`[16,19) «2-4»; `/category_specific/7/checks/4/label`[88,92) «7-10»
- **AP-MULT** (2): `/category_specific/7/checks/4/label`[50,52) «x2»; `/category_specific/7/checks/4/label`[70,72) «x2»
- **AP-YEAR** (1): `/category_specific/7/checks/2/label`[61,65) «2017»
- **AP-PAREN** (10): `/category_specific/4/checks/4/label`[16,25) «(시술 1주 전)»; `/category_specific/5/checks/0/label`[11,19) «(리도카인 등)»; `/category_specific/5/checks/4/label`[7,20) «(30-70%, 개인차)»; `/category_specific/6/checks/2/label`[14,20) «(잔여 실)»; `/category_specific/6/checks/4/label`[4,19) «(녹는 실 vs 비녹는 실)»; `/category_specific/7/checks/0/label`[20,26) «(I-VI)»; `/category_specific/7/checks/3/label`[14,31) «(독시사이클린, 아미오다론 등)»; `/category_specific/7/checks/4/label`[36,97) «(아시클로비르 400mg x2 또는 발라시클로비르 500mg x2, 시술 3일 전부터 시작, 7-10일 복용)»; `/category_specific/7/checks/5/label`[11,23) «(어블레이티브 레이저)»; `/category_specific/7/checks/6/label`[11,26) «(고위험군 사전 미백 치료)»
- **AP-SLASH** (14): `/category_specific/4/name`[0,7) «PRP/자가혈»; `/category_specific/4/checks/0/label`[0,11) «혈소판감소증/혈액질환»; `/category_specific/4/checks/1/label`[0,10) «항응고제/항혈소판제»; `/category_specific/4/checks/2/label`[4,10) «감염/패혈증»; `/category_specific/5/checks/1/label`[3,10) «경향/응고장애»; `/category_specific/5/checks/5/label`[0,10) «비대칭/과교정/흡수»; `/category_specific/6/checks/5/label`[2,11) «돌출/감염/비대칭»; `/category_specific/6/checks/6/label`[8,16) «입벌리기/마사지»; `/category_specific/7/checks/1/label`[3,10) «일광노출/태닝»; `/category_specific/7/checks/2/label`[11,16) «여부/중단»; `/category_specific/7/checks/2/label`[25,32) «프락셔널/얕은»; `/category_specific/7/checks/4/label`[13,18) «구순/안면»; `/category_specific/7/checks/8/label`[13,20) «RF/HIFU»; `/category_specific/7/checks/9/label`[0,6) «보호안경/눈»
- **AP-DASH** (5): `/category_specific/7/checks/1/label`[14,51) «— 2-4주 이내 자외선 노출 시 에너지 감소 or 시술 연기 판단»; `/category_specific/7/checks/2/label`[23,113) «— 프락셔널/얕은 필링 6개월, 박리성 레이저 12개월 대기 원칙. 2017 AAD Task Force 이후 비박리성 얕은 시술은 의사 판단 하에 조기 고려 가능»; `/category_specific/7/checks/4/label`[11,97) «— 구순/안면 레이저 시 예방적 항바이러스제 (아시클로비르 400mg x2 또는 발라시클로비르 500mg x2, 시술 3일 전부터 시작, 7-10일 복용)»; `/category_specific/7/checks/7/label`[24,49) «— 피부 장벽 회복 전 레이저 시 합병증 위험»; `/category_specific/7/checks/8/label`[11,34) «— RF/HIFU 병행 시 금속 발열 위험»
- **AP-ALT** (3): `/category_specific/6/checks/4/label`[10,12) «vs»; `/category_specific/7/checks/1/label`[40,42) «or»; `/category_specific/7/checks/4/label`[53,55) «또는»
- **AP-NEG** (3): `/category_specific/6/checks/4/label`[13,14) «비»; `/category_specific/6/checks/6/label`[17,19) «제한»; `/category_specific/7/checks/2/label`[84,85) «비»
- **AP-POSS** (8): `/category_specific/5/checks/3/label`[6,8) «위험»; `/category_specific/5/checks/5/label`[11,14) «가능성»; `/category_specific/6/checks/5/label`[12,15) «가능성»; `/category_specific/7/checks/2/label`[111,113) «가능»; `/category_specific/7/checks/6/label`[4,6) «위험»; `/category_specific/7/checks/6/label`[13,15) «위험»; `/category_specific/7/checks/7/label`[47,49) «위험»; `/category_specific/7/checks/8/label`[32,34) «위험»
- **AP-COND** (16): `/category_specific/4/checks/4/label`[10,12) «중단»; `/category_specific/4/checks/4/label`[23,24) «전»; `/category_specific/6/checks/6/label`[3,4) «후»; `/category_specific/7/checks/1/label`[21,23) «이내»; `/category_specific/7/checks/1/label`[30,32) « 시»; `/category_specific/7/checks/2/label`[14,16) «중단»; `/category_specific/7/checks/2/label`[54,56) «대기»; `/category_specific/7/checks/2/label`[81,83) «이후»; `/category_specific/7/checks/2/label`[102,104) «하에»; `/category_specific/7/checks/4/label`[22,24) « 시»; `/category_specific/7/checks/4/label`[80,83) «전부터»; `/category_specific/7/checks/7/label`[10,11) «후»; `/category_specific/7/checks/7/label`[18,20) «대기»; `/category_specific/7/checks/7/label`[40,42) « 시»; `/category_specific/7/checks/8/label`[21,23) «병행»; `/category_specific/7/checks/8/label`[23,25) « 시»
- **AP-MODAL** (26): `/category_specific/4/checks/5/label`[14,16) «설명»; `/category_specific/5/checks/2/label`[14,16) «확인»; `/category_specific/5/checks/3/label`[9,11) «설명»; `/category_specific/5/checks/4/label`[4,6) «안내»; `/category_specific/5/checks/5/label`[15,17) «설명»; `/category_specific/5/checks/6/label`[10,12) «준비»; `/category_specific/5/checks/6/label`[13,15) «확인»; `/category_specific/6/checks/2/label`[11,13) «확인»; `/category_specific/6/checks/3/label`[8,10) «확인»; `/category_specific/6/checks/4/label`[26,28) «설명»; `/category_specific/6/checks/5/label`[16,18) «설명»; `/category_specific/6/checks/6/label`[20,22) «안내»; `/category_specific/7/checks/0/label`[17,19) «확인»; `/category_specific/7/checks/1/label`[49,51) «판단»; `/category_specific/7/checks/2/label`[20,22) «확인»; `/category_specific/7/checks/2/label`[57,59) «원칙»; `/category_specific/7/checks/2/label`[99,101) «판단»; `/category_specific/7/checks/2/label`[108,110) «고려»; `/category_specific/7/checks/4/label`[8,10) «확인»; `/category_specific/7/checks/5/label`[8,10) «확인»; `/category_specific/7/checks/6/label`[8,10) «평가»; `/category_specific/7/checks/7/label`[21,23) «확인»; `/category_specific/7/checks/8/label`[8,10) «확인»; `/category_specific/7/checks/9/label`[10,12) «준비»; `/category_specific/7/checks/9/label`[13,15) «확인»; `/category_specific/7/checks/10/label`[13,15) «설명»
- **AP-DEGREE** (9): `/category_specific/5/checks/2/label`[6,9) «충분한»; `/category_specific/5/checks/4/label`[16,19) «개인차»; `/category_specific/6/checks/6/label`[5,7) «크게»; `/category_specific/7/checks/1/label`[0,2) «최근»; `/category_specific/7/checks/2/label`[105,107) «조기»; `/category_specific/7/checks/6/label`[12,16) «고위험군»; `/category_specific/7/checks/6/label`[17,19) «사전»; `/category_specific/7/checks/7/label`[0,6) «중등도 이상»; `/category_specific/7/checks/7/label`[12,14) «최소»
- **AP-ETC** (2): `/category_specific/5/checks/0/label`[16,18) « 등»; `/category_specific/7/checks/3/label`[28,30) « 등»

## 수동 수집 표현 (직접 읽기 — 원문 구간)

| Pointer | 구간 | 원문 구절 | 탐색 관점(잠정) | 메모 |
|---|---|---|---|---|
| `/category_specific/4/name` | [0,7) | PRP/자가혈 | 카테고리명 슬래시, 영문 약어 |  |
| `/category_specific/4/checks/0/label` | [0,14) | 혈소판감소증/혈액질환 여부 | 슬래시(개별 질환/상위군) |  |
| `/category_specific/4/checks/1/label` | [0,16) | 항응고제/항혈소판제 복용 여부 | 슬래시 나열 |  |
| `/category_specific/4/checks/2/label` | [0,13) | 활동성 감염/패혈증 여부 | 형용사(활동성), 슬래시 범위 |  |
| `/category_specific/4/checks/4/label` | [0,25) | NSAIDs 복용 중단 여부 (시술 1주 전) | 중단, 시점(시술 1주 전), 영문 약어 |  |
| `/category_specific/4/checks/5/label` | [0,16) | 채혈량 및 원심분리 과정 설명 | 행위(설명), 절차 |  |
| `/category_specific/5/checks/0/label` | [0,19) | 마취 알레르기 여부 (리도카인 등) | 괄호 예시, 열린 나열(등) |  |
| `/category_specific/5/checks/1/label` | [0,13) | 출혈 경향/응고장애 여부 | 슬래시 나열, 경향 |  |
| `/category_specific/5/checks/2/label` | [0,16) | 공여 부위 충분한 지방량 확인 | 부위(공여 부위), 형용사(충분한), 양 기준 미기재 |  |
| `/category_specific/5/checks/3/label` | [0,11) | 지방색전증 위험 설명 | 위험, 행위(설명) |  |
| `/category_specific/5/checks/4/label` | [0,20) | 생착률 안내 (30-70%, 개인차) | 수치 범위(%), 개인차 |  |
| `/category_specific/5/checks/5/label` | [0,17) | 비대칭/과교정/흡수 가능성 설명 | 슬래시 나열, 가능성 | '비대칭' 의 '비' 는 부정 접두 형태이나 결과 상태어 — 부정 표현으로 분류하지 않음 |
| `/category_specific/5/checks/6/label` | [0,15) | 감염 예방 항생제 준비 확인 | 시술자 준비, 예방 |  |
| `/category_specific/6/name` | [0,4) | 실리프팅 | 카테고리명 |  |
| `/category_specific/6/checks/0/label` | [0,15) | 시술 부위 활동성 감염 여부 | 부위, 형용사(활동성) |  |
| `/category_specific/6/checks/2/label` | [0,20) | 이전 실리프팅 이력 확인 (잔여 실) | 시점(이전), 괄호 목적 |  |
| `/category_specific/6/checks/3/label` | [0,10) | 켈로이드 체질 확인 | 체질 |  |
| `/category_specific/6/checks/4/label` | [0,28) | 실 종류(녹는 실 vs 비녹는 실) 및 장단점 설명 | 비교(vs), 부정 접두(비녹는), 행위(설명) |  |
| `/category_specific/6/checks/5/label` | [0,18) | 실 돌출/감염/비대칭 가능성 설명 | 슬래시 나열, 가능성 |  |
| `/category_specific/6/checks/6/label` | [0,22) | 시술 후 크게 입벌리기/마사지 제한 안내 | 시점(시술 후), 부사(크게), 제한, 슬래시 범위 | 시술 전 체크리스트 안의 시술 후 지시. '크게' 가 마사지까지 걸리지 않는 것으로 보임(잠정) |
| `/category_specific/7/checks/0/label` | [0,26) | Fitzpatrick 피부타입 확인 (I-VI) | 분류 체계 언급, 로마숫자 범위 |  |
| `/category_specific/7/checks/1/label` | [0,13) | 최근 일광노출/태닝 여부 | 시점(최근), 슬래시 나열 |  |
| `/category_specific/7/checks/1/label` | [16,51) | 2-4주 이내 자외선 노출 시 에너지 감소 or 시술 연기 판단 | 시간 범위(2-4주 이내), 조건(노출 시), 대안(or), 감소, 연기, 판단 |  |
| `/category_specific/7/checks/1/label` | [33,48) | 에너지 감소 or 시술 연기 | 대안 행위, 영문 접속사 |  |
| `/category_specific/7/checks/2/label` | [0,22) | 이소트레티노인 복용 여부/중단 시점 확인 | 슬래시(여부/시점), 중단 |  |
| `/category_specific/7/checks/2/label` | [25,59) | 프락셔널/얕은 필링 6개월, 박리성 레이저 12개월 대기 원칙 | 기간, 원칙, 슬래시 범위 | universal 문구와 달리 '중단 후 최소' 가 없음 |
| `/category_specific/7/checks/2/label` | [61,113) | 2017 AAD Task Force 이후 비박리성 얕은 시술은 의사 판단 하에 조기 고려 가능 | 연도·출처, 부정 접두(비-), 주체(의사 판단 하에), 가능성 |  |
| `/category_specific/7/checks/3/label` | [0,31) | 광과민성 약물 복용 여부 (독시사이클린, 아미오다론 등) | 약물군, 열린 나열(등) |  |
| `/category_specific/7/checks/4/label` | [13,35) | 구순/안면 레이저 시 예방적 항바이러스제 | 부위(구순/안면), 조건(레이저 시), 예방 |  |
| `/category_specific/7/checks/4/label` | [37,72) | 아시클로비르 400mg x2 또는 발라시클로비르 500mg x2 | 대안(또는), 용량, x표기 | universal 과 약물 순서 반대 |
| `/category_specific/7/checks/4/label` | [74,96) | 시술 3일 전부터 시작, 7-10일 복용 | 시점(시술 전), 기간 범위 |  |
| `/category_specific/7/checks/5/label` | [0,23) | 켈로이드 체질 확인 (어블레이티브 레이저) | 괄호 조건/범위, 외래어 표기(어블레이티브) |  |
| `/category_specific/7/checks/6/label` | [0,26) | PIH 위험도 평가 (고위험군 사전 미백 치료) | 위험도, 대상(고위험군), 시점(사전), 선행 처치 |  |
| `/category_specific/7/checks/7/label` | [0,23) | 중등도 이상 필링 후 최소 2주 대기 확인 | 정도(중등도 이상), 시점(필링 후), 최소, 기간 |  |
| `/category_specific/7/checks/7/label` | [26,49) | 피부 장벽 회복 전 레이저 시 합병증 위험 | 조건(회복 전·레이저 시), 위험 |  |
| `/category_specific/7/checks/8/label` | [13,34) | RF/HIFU 병행 시 금속 발열 위험 | 다른 시술 참조, 조건(병행 시), 위험 |  |
| `/category_specific/7/checks/9/label` | [0,15) | 보호안경/눈 보호 준비 확인 | 시술자 준비, 슬래시 |  |
| `/category_specific/7/checks/10/label` | [0,15) | 레이저 종류별 다운타임 설명 | 종류별(범위), 행위(설명) |  |
| `/category_specific/7/checks/4/label` | [0,10) | 헤르페스 병력 확인 | 이력(병력) |  |
| `/category_specific/7/checks/8/label` | [0,10) | 금속 임플란트 확인 | 기기·재질 |  |

## 잠정 관찰 (원문 아님 — 근거 위치 포함)

- P: type 분포 — M5 [absolute_contraindication, must_check, absolute_contraindication, must_check×2, counseling], M6 [absolute_contraindication, must_check×2, safety_protocol, counseling×2, safety_protocol], M7 [absolute_contraindication, must_check×3, counseling×2, inform], M8 [must_check×9, safety_protocol, counseling].
- P: `/category_specific/5/checks/3` '지방색전증 위험 설명' 은 설명 행위인데 type 이 safety_protocol(counseling 아님).
- P: `/category_specific/6/checks/6` 은 시술 후 행동 제한을 시술 전 체크리스트에 담은 항목(type inform).
- P: 이소트레티노인 문구 변형 — universal(`/universal_checks/6/description`)은 '중단 후 최소 6개월'·'피부 재생 상태에 따라 의사 판단으로 조기 시행 고려 가능'·'(ablative)', M8(`/category_specific/7/checks/2/label`)은 '6개월'(최소 없음)·'의사 판단 하에 조기 고려 가능'·'(ablative)' 없음.
- P: 'ablative' 표기가 '박리성(ablative)'·'박리성'·'어블레이티브' 로 나뉜다(`/universal_checks/6/description`, `/category_specific/7/checks/2/label`, `/category_specific/7/checks/5/label`). 같은 개념인지 확정하지 않음.
- P: 헤르페스 예방 문구 — universal 은 발라시클로비르→아시클로비르 순·'시술 3일 전부터'; M8 은 아시클로비르→발라시클로비르 순·'시술 3일 전부터 시작, 7-10일 복용'·'구순/안면 레이저 시' 조건 추가.
- P: 레이저 카테고리 안에서 RF/HIFU(다른 장비 계열로 보이는 이름)를 '병행 시' 조건으로 참조한다(`/category_specific/7/checks/8/label`). 참조 표현만 보존.

## 이 구획의 미결 (A=추출/해석 오류, B=원문 정보 부족, C=사용자 결정 필요, K=분석 한계, P=잠정, F=후속, I=원문 불일치)

- **B-S03-1** [open] '충분한 지방량' 의 기준값 없음 — 위치: `/category_specific/5/checks/2/label`
- **B-S03-2** [open] '에너지 감소 or 시술 연기 판단' 의 선택 기준·감소 정도 없음 — 위치: `/category_specific/7/checks/1/label`
- **B-S03-3** [open] 'x2' 의 뜻이 M8 헤르페스 문구에도 없음(S01-1 과 같은 원인) — 위치: `/category_specific/7/checks/4/label`
- **F-S03-4** [deferred] ablative 표기 3종(박리성(ablative)/박리성/어블레이티브)의 동일성 — 후속 의미 조사 — 위치: `/universal_checks/6/description`, `/category_specific/7/checks/2/label`, `/category_specific/7/checks/5/label`
- **F-S03-5** [deferred] M8 안 'RF/HIFU 병행 시' 는 다른 카테고리(M9 기기 리프팅 등) 참조로 보임 — 연결은 후속 — 위치: `/category_specific/7/checks/8/label`
- **F-S03-6** [deferred] 시술 전 체크리스트 안의 시술 후 지시(입벌리기/마사지 제한) — 시점 범위 모델링은 후속 — 위치: `/category_specific/6/checks/6/label`
- **K-S03-7** [recorded] kiwi 가 '안내' 를 '안/MAG 내/VV' 로 나눠 원문에 없는 부정(안)을 만든다 — 형태소 기반 부정 탐지 시 오탐 — 위치: `/category_specific/6/checks/6/label`

## 알려진 형태소 오분절 (K — 출현별)

- `/category_specific/5/checks/4/label` «30-70» → 원시 `30-70/W_SERIAL` — 영향: 수치 범위가 일련번호 단일 토큰 — 범위·% 결합 구조 없음(%/SW 별도)
- `/category_specific/5/checks/5/label` «비대칭» → 원시 `비대칭/NNP` — 영향: 고유명사 태깅. 같은 단어가 `/category_specific/6/checks/5/label` 에서는 비/XPN 대칭/NNG — 출현마다 분석 다름
- `/category_specific/6/checks/4/label` «비녹는» → 원시 `비/NNG 녹/VV 는/ETM` — 영향: 부정 접두 '비' 가 명사(NNG)로 태깅 — 부정 의미가 토큰에서 소실('비HA' 는 XPN 으로 분석됨)
- `/category_specific/6/checks/6/label` «안내» → 원시 `안/MAG 내/VV 어/EF` — 영향: 명사 '안내' 가 부정 부사 '안'+동사 '내다' 로 오분석 — 원문에 없는 부정 생성(심각, 오탐)
- `/category_specific/7/checks/0/label` «I-VI» → 원시 `I/SL -/SO VI/SL` — 영향: 로마숫자 범위가 셋으로 나뉨 — 범위 구조 없음
- `/category_specific/7/checks/1/label` «2-4» → 원시 `2-4/W_SERIAL` — 영향: 수치 범위가 일련번호 단일 토큰
- `/category_specific/7/checks/2/label` «비박리성» → 원시 `비/XPN 박/NNG 리/XSN 성/NNG` — 영향: '박리성' 어간 깨짐(S01 과 같은 패턴)
- `/category_specific/7/checks/4/label` «7-10» → 원시 `7-10/W_SERIAL` — 영향: 수치 범위가 일련번호 단일 토큰
- `/category_specific/7/checks/7/label` «중등도» → 원시 `중등/NNG 도/JX` — 영향: 정도어 '중등도' 의 '도' 가 보조사(도)로 오분석 — '중등도 이상' 정도 표현이 토큰에서 깨짐
- `/category_specific/7/checks/10/label` «다운타임» → 원시 `다운/NNG 타임/NNG` — 영향: 같은 단어가 `/category_specific/3/checks/4/label` 에서는 다운타임/NNP — 출현마다 분석 다름

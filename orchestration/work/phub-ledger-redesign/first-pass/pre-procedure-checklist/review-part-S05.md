# review-part-S05 — category_specific M14–M17 (index 13–16)

- 원본: `orchestration/work/phub-recommend/bronze/phub-ledger/pre-procedure-checklist.json` (sha256 `0de87bff91f721fe685884025d31749017d44da250492b2db9d49109a61e4086`)
- 직접 읽기 상태: **read** — /category_specific/13 … /16 (M14 크라이오리포라이시스 8·M15 메디컬스킨케어 9·M16 수액치료 7·M17 줄기세포치료 8 = checks 32) id·name·label·type 전부
- 소유 Pointer: `/category_specific/13`, `/category_specific/14`, `/category_specific/15`, `/category_specific/16`
- 공동 참조 문맥(소유 아님): `/description`, `/category_specific`
- 열 구분: **원문 값** 칸은 원본 그대로(가공 없음). 관찰은 아래 별도 절에만 있다. 형태소 열은 kiwi 원시 결과(`form/tag`)이며 도메인 정답이 아니다.

## 원문 값 (원본 컬럼명 그대로, 원본 순서)

| JSON Pointer | 원본 컬럼명(key/index) | 자료형 | 원문 값 | 분석 적용 | kiwi 원시 토큰(form/tag) |
|---|---|---|---|---|---|
| `/category_specific/13` | `[13]` | object(자식 3) | keys=['id', 'name', 'checks'] | — | — |
| `/category_specific/13/id` | `id` | string | M14 | excluded | — |
| `/category_specific/13/name` | `name` | string | 크라이오리포라이시스 | analyzed | 크라이오리포라이시스/NNG |
| `/category_specific/13/checks` | `checks` | array(자식 8) |  | — | — |
| `/category_specific/13/checks/0` | `[0]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/13/checks/0/label` | `label` | string | 한냉두드러기/한냉글로불린혈증 여부 | analyzed | 한/MM 냉/NNG 두드러기/NNG //SP 한냉글로불린혈증/NNG 여부/NNG |
| `/category_specific/13/checks/0/type` | `type` | string | absolute_contraindication | excluded | — |
| `/category_specific/13/checks/1` | `[1]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/13/checks/1/label` | `label` | string | 발작성 한냉혈색소뇨증 여부 | analyzed | 발작/NNG 성/XSN 한냉혈색소뇨증/NNG 여부/NNG |
| `/category_specific/13/checks/1/type` | `type` | string | absolute_contraindication | excluded | — |
| `/category_specific/13/checks/2` | `[2]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/13/checks/2/label` | `label` | string | 레이노 증후군 여부 | analyzed | 레이노/NNP 증후군/NNG 여부/NNG |
| `/category_specific/13/checks/2/type` | `type` | string | must_check | excluded | — |
| `/category_specific/13/checks/3` | `[3]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/13/checks/3/label` | `label` | string | BMI/체형 적합성 평가 (피하지방 두께 측정) | analyzed | BMI/SL //SP 체형/NNG 적합/NNG 성/XSN 평가/NNG (/SSO 피하/NNG 지방/NNG 두께/NNG 측정/NNG )/SSC |
| `/category_specific/13/checks/3/type` | `type` | string | must_check | excluded | — |
| `/category_specific/13/checks/4` | `[4]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/13/checks/4/label` | `label` | string | 탈장 여부 (복부 시술 시) | analyzed | 탈장/NNG 여부/NNG (/SSO 복부/NNG 시술/NNG 시/NNB )/SSC |
| `/category_specific/13/checks/4/type` | `type` | string | must_check | excluded | — |
| `/category_specific/13/checks/5` | `[5]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/13/checks/5/label` | `label` | string | 역설적 지방증식(PAH) 가능성 설명 (0.005-0.39%) | analyzed | 역설/NNG 적/XSN 지방/NNG 증식/NNG (/SSO PAH/SL )/SSC 가능/NNG 성/XSN 설명/NNG (/SSO 0.005/SN -/SO 0.39/SN %/SW )/SSC |
| `/category_specific/13/checks/5/type` | `type` | string | counseling | excluded | — |
| `/category_specific/13/checks/6` | `[6]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/13/checks/6/label` | `label` | string | 시술 부위 피부 감각 이상/무감각 가능성 안내 | analyzed | 시술/NNG 부위/NNG 피부/NNG 감각/NNG 이상/NNG //SP 무/XPN 감각/NNG 가능/NNG 성/XSN 안내/NNG |
| `/category_specific/13/checks/6/type` | `type` | string | inform | excluded | — |
| `/category_specific/13/checks/7` | `[7]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/13/checks/7/label` | `label` | string | 효과 발현 시기 안내 (2-4개월 점진적) | analyzed | 효과/NNG 발현/NNG 시기/NNG 안내/NNG (/SSO 2-4/W_SERIAL 개월/NNB 점진/NNG 적/XSN )/SSC |
| `/category_specific/13/checks/7/type` | `type` | string | counseling | excluded | — |
| `/category_specific/14` | `[14]` | object(자식 3) | keys=['id', 'name', 'checks'] | — | — |
| `/category_specific/14/id` | `id` | string | M15 | excluded | — |
| `/category_specific/14/name` | `name` | string | 메디컬스킨케어 | analyzed | 메디컬/NNG 스킨/NNG 케어/NNG |
| `/category_specific/14/checks` | `checks` | array(자식 9) |  | — | — |
| `/category_specific/14/checks/0` | `[0]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/14/checks/0/label` | `label` | string | 이소트레티노인 복용 여부/중단 시점 확인 — 프락셔널/얕은 필링 6개월, 박리성 레이저 12개월 대기 원칙. 2017 AAD Task Force 이후 비박리성 얕은 시술은 의사 판단 하에 조기 고려 가능 | analyzed | 이소트레티노인/NNG 복용/NNG 여부/NNG //SP 중단/NNG 시점/NNG 확인/NNG —/SW 프락셔널/NNG //SP 얕/VA 은/ETM 필링/NNG 6/SN 개월/NNB ,/SP 박리성/NNP 레이저/NNG 12/SN 개월/NNB 대기/NNG 원칙/NNG ./SF 2017/SN AAD/SL Task/SL Force/SL 이후/NNG 비/XPN 박/NNG 리/XSN 성/NNG 얕/VA 은/ETM 시술/NNG 은/JX 의사/NNG 판단/NNG 하/NNG 에/JKB 조기/NNG 고려/NNG 가능/NNG |
| `/category_specific/14/checks/0/type` | `type` | string | must_check | excluded | — |
| `/category_specific/14/checks/1` | `[1]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/14/checks/1/label` | `label` | string | 임신 테스트 (레티노이드 처방 시 필수) | analyzed | 임신/NNG 테스트/NNG (/SSO 레티노이드/NNG 처방/NNG 시/NNB 필수/NNG )/SSC |
| `/category_specific/14/checks/1/type` | `type` | string | absolute_contraindication | excluded | — |
| `/category_specific/14/checks/2` | `[2]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/14/checks/2/label` | `label` | string | 간기능 검사 결과 확인 (레티노이드/이소트레티노인 처방 시) | analyzed | 간/NNG 기능/NNG 검사/NNG 결과/NNG 확인/NNG (/SSO 레티노이드/NNG //SP 이소트레티노인/NNG 처방/NNG 시/NNB )/SSC |
| `/category_specific/14/checks/2/type` | `type` | string | must_check | excluded | — |
| `/category_specific/14/checks/3` | `[3]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/14/checks/3/label` | `label` | string | 지질 수치 확인 (이소트레티노인 처방 시) | analyzed | 지질/NNG 수치/NNG 확인/NNG (/SSO 이소트레티노인/NNG 처방/NNG 시/NNB )/SSC |
| `/category_specific/14/checks/3/type` | `type` | string | must_check | excluded | — |
| `/category_specific/14/checks/4` | `[4]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/14/checks/4/label` | `label` | string | 현재 사용 중인 스킨케어 제품 확인 | analyzed | 현재/MAG 사용/NNG 중/NNB 이/VCP ᆫ/ETM 스킨케어/NNG 제품/NNG 확인/NNG |
| `/category_specific/14/checks/4/type` | `type` | string | must_check | excluded | — |
| `/category_specific/14/checks/5` | `[5]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/14/checks/5/label` | `label` | string | 활동성 피부염/습진/건선 여부 | analyzed | 활동/NNG 성/XSN 피부염/NNG //SP 습진/NNG //SP 건선/NNP 여부/NNG |
| `/category_specific/14/checks/5/type` | `type` | string | must_check | excluded | — |
| `/category_specific/14/checks/6` | `[6]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/14/checks/6/label` | `label` | string | 화학적 필링 제제 알레르기 여부 (살리실산, 글리콜산 등) | analyzed | 화학/NNG 적/XSN 필링/NNG 제제/NNG 알레르기/NNG 여부/NNG (/SSO 살리실산/NNP ,/SP 글리콜산/NNP 등/NNB )/SSC |
| `/category_specific/14/checks/6/type` | `type` | string | must_check | excluded | — |
| `/category_specific/14/checks/7` | `[7]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/14/checks/7/label` | `label` | string | 최근 레이저/시술 이력 (필링 간격) | analyzed | 최근/NNG 레이저/NNG //SP 시술/NNG 이력/NNG (/SSO 필링/NNG 간격/NNG )/SSC |
| `/category_specific/14/checks/7/type` | `type` | string | must_check | excluded | — |
| `/category_specific/14/checks/8` | `[8]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/14/checks/8/label` | `label` | string | 자외선 차단 생활습관 확인 | analyzed | 자외선/NNG 차단/NNG 생활/NNG 습관/NNG 확인/NNG |
| `/category_specific/14/checks/8/type` | `type` | string | inform | excluded | — |
| `/category_specific/15` | `[15]` | object(자식 3) | keys=['id', 'name', 'checks'] | — | — |
| `/category_specific/15/id` | `id` | string | M16 | excluded | — |
| `/category_specific/15/name` | `name` | string | 수액치료 | analyzed | 수액/NNG 치료/NNG |
| `/category_specific/15/checks` | `checks` | array(자식 7) |  | — | — |
| `/category_specific/15/checks/0` | `[0]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/15/checks/0/label` | `label` | string | 심부전/신부전 여부 (수분 과부하 위험) | analyzed | 심부전/NNG //SP 신부전/NNP 여부/NNG (/SSO 수분/NNG 과/XPN 부하/NNG 위험/NNG )/SSC |
| `/category_specific/15/checks/0/type` | `type` | string | absolute_contraindication | excluded | — |
| `/category_specific/15/checks/1` | `[1]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/15/checks/1/label` | `label` | string | 약물 알레르기 여부 (비타민제 포함) | analyzed | 약물/NNG 알레르기/NNG 여부/NNG (/SSO 비타민제/NNG 포함/NNG )/SSC |
| `/category_specific/15/checks/1/type` | `type` | string | must_check | excluded | — |
| `/category_specific/15/checks/2` | `[2]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/15/checks/2/label` | `label` | string | 신장 기능 확인 (고용량 비타민 C 시) | analyzed | 신장/NNG 기능/NNG 확인/NNG (/SSO 고/XPN 용량/NNG 비타민/NNG C/SL 시/NNG )/SSC |
| `/category_specific/15/checks/2/type` | `type` | string | must_check | excluded | — |
| `/category_specific/15/checks/3` | `[3]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/15/checks/3/label` | `label` | string | G6PD 결핍증 여부 (고용량 비타민 C 금기) | analyzed | G/SL 6/SN PD/SL 결핍증/NNG 여부/NNG (/SSO 고/XPN 용량/NNG 비타민/NNG C/SL 금/NNG 기/XSN )/SSC |
| `/category_specific/15/checks/3/type` | `type` | string | absolute_contraindication | excluded | — |
| `/category_specific/15/checks/4` | `[4]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/15/checks/4/label` | `label` | string | 현재 복용 중인 영양제/약물 확인 (상호작용) | analyzed | 현재/MAG 복용/NNG 중/NNB 이/VCP ᆫ/ETM 영양제/NNG //SP 약물/NNG 확인/NNG (/SSO 상호/NNG 작용/NNG )/SSC |
| `/category_specific/15/checks/4/type` | `type` | string | must_check | excluded | — |
| `/category_specific/15/checks/5` | `[5]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/15/checks/5/label` | `label` | string | 혈관 접근 상태 확인 | analyzed | 혈관/NNG 접근/NNG 상태/NNG 확인/NNG |
| `/category_specific/15/checks/5/type` | `type` | string | must_check | excluded | — |
| `/category_specific/15/checks/6` | `[6]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/15/checks/6/label` | `label` | string | 수액 조성 및 기대 효과 설명 | analyzed | 수액/NNG 조성/NNG 및/MAG 기대/NNG 효과/NNG 설명/NNG |
| `/category_specific/15/checks/6/type` | `type` | string | counseling | excluded | — |
| `/category_specific/16` | `[16]` | object(자식 3) | keys=['id', 'name', 'checks'] | — | — |
| `/category_specific/16/id` | `id` | string | M17 | excluded | — |
| `/category_specific/16/name` | `name` | string | 줄기세포치료 | analyzed | 줄기세포/NNG 치료/NNG |
| `/category_specific/16/checks` | `checks` | array(자식 8) |  | — | — |
| `/category_specific/16/checks/0` | `[0]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/16/checks/0/label` | `label` | string | 악성종양 병력/활동성 암 여부 | analyzed | 악성/NNG 종양/NNG 병력/NNG //SP 활동/NNG 성/XSN 암/NNG 여부/NNG |
| `/category_specific/16/checks/0/type` | `type` | string | absolute_contraindication | excluded | — |
| `/category_specific/16/checks/1` | `[1]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/16/checks/1/label` | `label` | string | 활동성 감염/패혈증 여부 | analyzed | 활동/NNG 성/XSN 감염/NNG //SP 패혈증/NNG 여부/NNG |
| `/category_specific/16/checks/1/type` | `type` | string | absolute_contraindication | excluded | — |
| `/category_specific/16/checks/2` | `[2]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/16/checks/2/label` | `label` | string | 자가면역질환 여부 | analyzed | 자가/NNG 면역/NNG 질환/NNG 여부/NNG |
| `/category_specific/16/checks/2/type` | `type` | string | must_check | excluded | — |
| `/category_specific/16/checks/3` | `[3]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/16/checks/3/label` | `label` | string | 혈액질환/응고장애 여부 | analyzed | 혈액/NNG 질환/NNG //SP 응고/NNG 장애/NNG 여부/NNG |
| `/category_specific/16/checks/3/type` | `type` | string | must_check | excluded | — |
| `/category_specific/16/checks/4` | `[4]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/16/checks/4/label` | `label` | string | 줄기세포 유래(자가/동종) 및 채취 부위 설명 | analyzed | 줄기세포/NNG 유래/NNG (/SSO 자가/NNG //SP 동종/NNG )/SSC 및/MAG 채취/NNG 부위/NNG 설명/NNG |
| `/category_specific/16/checks/4/type` | `type` | string | counseling | excluded | — |
| `/category_specific/16/checks/5` | `[5]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/16/checks/5/label` | `label` | string | 규제 현황 및 근거 수준 설명 | analyzed | 규제/NNG 현황/NNG 및/MAG 근거/NNG 수준/NNG 설명/NNG |
| `/category_specific/16/checks/5/type` | `type` | string | counseling | excluded | — |
| `/category_specific/16/checks/6` | `[6]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/16/checks/6/label` | `label` | string | 기대 효과의 한계 및 부작용 가능성 설명 | analyzed | 기대/NNG 효과/NNG 의/JKG 한계/NNG 및/MAG 부작용/NNG 가능/NNG 성/XSN 설명/NNG |
| `/category_specific/16/checks/6/type` | `type` | string | counseling | excluded | — |
| `/category_specific/16/checks/7` | `[7]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/16/checks/7/label` | `label` | string | 감염/종양 발생 위험성 고지 | analyzed | 감염/NNG //SP 종양/NNG 발생/NNG 위험/NNG 성/XSN 고지/NNG |
| `/category_specific/16/checks/7/type` | `type` | string | inform | excluded | — |

## 자동 표현 후보 (정규식 일치분만 — 패턴 밖은 아래 수동 절)

- **AP-NUM-UNIT** (4): `/category_specific/13/checks/5/label`[22,33) «0.005-0.39%»; `/category_specific/13/checks/7/label`[13,18) «2-4개월»; `/category_specific/14/checks/0/label`[36,39) «6개월»; `/category_specific/14/checks/0/label`[49,53) «12개월»
- **AP-RANGE** (2): `/category_specific/13/checks/5/label`[22,32) «0.005-0.39»; `/category_specific/13/checks/7/label`[13,16) «2-4»
- **AP-YEAR** (1): `/category_specific/14/checks/0/label`[61,65) «2017»
- **AP-PAREN** (16): `/category_specific/13/checks/3/label`[14,26) «(피하지방 두께 측정)»; `/category_specific/13/checks/4/label`[6,15) «(복부 시술 시)»; `/category_specific/13/checks/5/label`[8,13) «(PAH)»; `/category_specific/13/checks/5/label`[21,34) «(0.005-0.39%)»; `/category_specific/13/checks/7/label`[12,23) «(2-4개월 점진적)»; `/category_specific/14/checks/1/label`[7,22) «(레티노이드 처방 시 필수)»; `/category_specific/14/checks/2/label`[13,33) «(레티노이드/이소트레티노인 처방 시)»; `/category_specific/14/checks/3/label`[9,23) «(이소트레티노인 처방 시)»; `/category_specific/14/checks/6/label`[18,32) «(살리실산, 글리콜산 등)»; `/category_specific/14/checks/7/label`[13,20) «(필링 간격)»; `/category_specific/15/checks/0/label`[11,22) «(수분 과부하 위험)»; `/category_specific/15/checks/1/label`[11,20) «(비타민제 포함)»; `/category_specific/15/checks/2/label`[9,22) «(고용량 비타민 C 시)»; `/category_specific/15/checks/3/label`[12,26) «(고용량 비타민 C 금기)»; `/category_specific/15/checks/4/label`[19,25) «(상호작용)»; `/category_specific/16/checks/4/label`[7,14) «(자가/동종)»
- **AP-SLASH** (15): `/category_specific/13/checks/0/label`[0,15) «한냉두드러기/한냉글로불린혈증»; `/category_specific/13/checks/3/label`[0,6) «BMI/체형»; `/category_specific/13/checks/6/label`[12,18) «이상/무감각»; `/category_specific/14/checks/0/label`[11,16) «여부/중단»; `/category_specific/14/checks/0/label`[25,32) «프락셔널/얕은»; `/category_specific/14/checks/2/label`[14,27) «레티노이드/이소트레티노인»; `/category_specific/14/checks/5/label`[4,13) «피부염/습진/건선»; `/category_specific/14/checks/7/label`[3,9) «레이저/시술»; `/category_specific/15/checks/0/label`[0,7) «심부전/신부전»; `/category_specific/15/checks/4/label`[9,15) «영양제/약물»; `/category_specific/16/checks/0/label`[5,11) «병력/활동성»; `/category_specific/16/checks/1/label`[4,10) «감염/패혈증»; `/category_specific/16/checks/3/label`[0,9) «혈액질환/응고장애»; `/category_specific/16/checks/4/label`[8,13) «자가/동종»; `/category_specific/16/checks/7/label`[0,5) «감염/종양»
- **AP-DASH** (1): `/category_specific/14/checks/0/label`[23,113) «— 프락셔널/얕은 필링 6개월, 박리성 레이저 12개월 대기 원칙. 2017 AAD Task Force 이후 비박리성 얕은 시술은 의사 판단 하에 조기 고려 가능»
- **AP-NEG** (3): `/category_specific/13/checks/6/label`[15,18) «무감각»; `/category_specific/14/checks/0/label`[84,85) «비»; `/category_specific/15/checks/3/label`[23,25) «금기»
- **AP-POSS** (6): `/category_specific/13/checks/5/label`[14,17) «가능성»; `/category_specific/13/checks/6/label`[19,22) «가능성»; `/category_specific/14/checks/0/label`[111,113) «가능»; `/category_specific/15/checks/0/label`[19,21) «위험»; `/category_specific/16/checks/6/label`[16,19) «가능성»; `/category_specific/16/checks/7/label`[9,11) «위험»
- **AP-COND** (11): `/category_specific/13/checks/4/label`[12,14) « 시»; `/category_specific/14/checks/0/label`[14,16) «중단»; `/category_specific/14/checks/0/label`[54,56) «대기»; `/category_specific/14/checks/0/label`[81,83) «이후»; `/category_specific/14/checks/0/label`[102,104) «하에»; `/category_specific/14/checks/1/label`[16,18) « 시»; `/category_specific/14/checks/2/label`[30,32) « 시»; `/category_specific/14/checks/3/label`[20,22) « 시»; `/category_specific/14/checks/4/label`[6,8) «중인»; `/category_specific/15/checks/2/label`[19,21) « 시»; `/category_specific/15/checks/4/label`[6,8) «중인»
- **AP-MODAL** (21): `/category_specific/13/checks/3/label`[11,13) «평가»; `/category_specific/13/checks/5/label`[18,20) «설명»; `/category_specific/13/checks/6/label`[23,25) «안내»; `/category_specific/13/checks/7/label`[9,11) «안내»; `/category_specific/14/checks/0/label`[20,22) «확인»; `/category_specific/14/checks/0/label`[57,59) «원칙»; `/category_specific/14/checks/0/label`[99,101) «판단»; `/category_specific/14/checks/0/label`[108,110) «고려»; `/category_specific/14/checks/1/label`[19,21) «필수»; `/category_specific/14/checks/2/label`[10,12) «확인»; `/category_specific/14/checks/3/label`[6,8) «확인»; `/category_specific/14/checks/4/label`[17,19) «확인»; `/category_specific/14/checks/8/label`[12,14) «확인»; `/category_specific/15/checks/2/label`[6,8) «확인»; `/category_specific/15/checks/4/label`[16,18) «확인»; `/category_specific/15/checks/5/label`[9,11) «확인»; `/category_specific/15/checks/6/label`[14,16) «설명»; `/category_specific/16/checks/4/label`[23,25) «설명»; `/category_specific/16/checks/5/label`[14,16) «설명»; `/category_specific/16/checks/6/label`[20,22) «설명»; `/category_specific/16/checks/7/label`[13,15) «고지»
- **AP-DEGREE** (6): `/category_specific/13/checks/6/label`[12,14) «이상»; `/category_specific/13/checks/7/label`[19,22) «점진적»; `/category_specific/14/checks/0/label`[105,107) «조기»; `/category_specific/14/checks/7/label`[0,2) «최근»; `/category_specific/15/checks/2/label`[10,13) «고용량»; `/category_specific/15/checks/3/label`[13,16) «고용량»
- **AP-ETC** (1): `/category_specific/14/checks/6/label`[29,31) « 등»

## 수동 수집 표현 (직접 읽기 — 원문 구간)

| Pointer | 구간 | 원문 구절 | 탐색 관점(잠정) | 메모 |
|---|---|---|---|---|
| `/category_specific/13/checks/0/label` | [0,18) | 한냉두드러기/한냉글로불린혈증 여부 | 슬래시 나열, 질환 |  |
| `/category_specific/13/checks/1/label` | [0,14) | 발작성 한냉혈색소뇨증 여부 | 형용사(발작성), 질환 |  |
| `/category_specific/13/checks/2/label` | [0,10) | 레이노 증후군 여부 | 질환 |  |
| `/category_specific/13/checks/3/label` | [0,26) | BMI/체형 적합성 평가 (피하지방 두께 측정) | 영문 약어, 적합성, 두께(기준 미기재), 측정 |  |
| `/category_specific/13/checks/4/label` | [0,15) | 탈장 여부 (복부 시술 시) | 조건(복부 시술 시), 부위(복부) |  |
| `/category_specific/13/checks/5/label` | [0,34) | 역설적 지방증식(PAH) 가능성 설명 (0.005-0.39%) | 형용사(역설적), 괄호 약어, 가능성, 수치 범위(%) |  |
| `/category_specific/13/checks/5/label` | [22,33) | 0.005-0.39% | 수치 범위, 백분율 | 모집단·출처는 원문에 없음 |
| `/category_specific/13/checks/6/label` | [0,25) | 시술 부위 피부 감각 이상/무감각 가능성 안내 | 부위, 부정 접두(무-), 가능성 | '감각 이상' 의 '이상' 은 정도 표현 아님(자동 AP-DEGREE 오탐) |
| `/category_specific/13/checks/7/label` | [0,23) | 효과 발현 시기 안내 (2-4개월 점진적) | 시간 범위, 형용사(점진적) |  |
| `/category_specific/14/name` | [0,7) | 메디컬스킨케어 | 카테고리명 |  |
| `/category_specific/14/checks/0/label` | [0,22) | 이소트레티노인 복용 여부/중단 시점 확인 | 슬래시(여부/시점), 중단 |  |
| `/category_specific/14/checks/0/label` | [25,59) | 프락셔널/얕은 필링 6개월, 박리성 레이저 12개월 대기 원칙 | 기간, 원칙 |  |
| `/category_specific/14/checks/0/label` | [61,113) | 2017 AAD Task Force 이후 비박리성 얕은 시술은 의사 판단 하에 조기 고려 가능 | 연도·출처, 부정 접두(비-), 가능성 | `/category_specific/7/checks/2/label` 과 같은 문자열 |
| `/category_specific/14/checks/1/label` | [0,22) | 임신 테스트 (레티노이드 처방 시 필수) | 검사 행위, 조건(처방 시), 의무(필수) |  |
| `/category_specific/14/checks/2/label` | [0,33) | 간기능 검사 결과 확인 (레티노이드/이소트레티노인 처방 시) | 검사, 조건(처방 시), 슬래시 나열 |  |
| `/category_specific/14/checks/3/label` | [0,23) | 지질 수치 확인 (이소트레티노인 처방 시) | 검사 수치(값 미기재), 조건(처방 시) |  |
| `/category_specific/14/checks/4/label` | [0,19) | 현재 사용 중인 스킨케어 제품 확인 | 시점(현재), 제품 |  |
| `/category_specific/14/checks/5/label` | [0,16) | 활동성 피부염/습진/건선 여부 | 형용사(활동성), 슬래시 범위 |  |
| `/category_specific/14/checks/6/label` | [0,32) | 화학적 필링 제제 알레르기 여부 (살리실산, 글리콜산 등) | 형용사(화학적), 열린 나열(등) |  |
| `/category_specific/14/checks/7/label` | [0,20) | 최근 레이저/시술 이력 (필링 간격) | 시점(최근), 간격(값 미기재) |  |
| `/category_specific/14/checks/8/label` | [0,14) | 자외선 차단 생활습관 확인 | 생활습관 |  |
| `/category_specific/15/checks/0/label` | [0,22) | 심부전/신부전 여부 (수분 과부하 위험) | 슬래시 나열, 괄호 위험 |  |
| `/category_specific/15/checks/1/label` | [0,20) | 약물 알레르기 여부 (비타민제 포함) | 괄호 범위 확장(포함) |  |
| `/category_specific/15/checks/2/label` | [0,22) | 신장 기능 확인 (고용량 비타민 C 시) | 조건(고용량 … 시), 정도(고용량, 기준 미기재) |  |
| `/category_specific/15/checks/3/label` | [0,26) | G6PD 결핍증 여부 (고용량 비타민 C 금기) | 금기(명시어), 정도(고용량), 영문·숫자 혼합 명칭 |  |
| `/category_specific/15/checks/4/label` | [0,25) | 현재 복용 중인 영양제/약물 확인 (상호작용) | 시점(현재), 슬래시, 괄호 목적 |  |
| `/category_specific/15/checks/5/label` | [0,11) | 혈관 접근 상태 확인 | 상태 |  |
| `/category_specific/15/checks/6/label` | [0,16) | 수액 조성 및 기대 효과 설명 | 행위(설명) |  |
| `/category_specific/16/checks/0/label` | [0,16) | 악성종양 병력/활동성 암 여부 | 슬래시(병력/활동성), 형용사(활동성) |  |
| `/category_specific/16/checks/1/label` | [0,13) | 활동성 감염/패혈증 여부 | 형용사(활동성), 슬래시 범위 |  |
| `/category_specific/16/checks/3/label` | [0,12) | 혈액질환/응고장애 여부 | 슬래시 나열 |  |
| `/category_specific/16/checks/4/label` | [0,25) | 줄기세포 유래(자가/동종) 및 채취 부위 설명 | 괄호 대안(자가/동종), 부위(채취 부위) |  |
| `/category_specific/16/checks/5/label` | [0,16) | 규제 현황 및 근거 수준 설명 | 규제, 근거 수준 |  |
| `/category_specific/16/checks/6/label` | [0,22) | 기대 효과의 한계 및 부작용 가능성 설명 | 한계, 가능성 |  |
| `/category_specific/16/checks/7/label` | [0,15) | 감염/종양 발생 위험성 고지 | 위험, 행위(고지) |  |

## 잠정 관찰 (원문 아님 — 근거 위치 포함)

- P: type 분포 — M14 [absolute_contraindication×2, must_check×3, counseling, inform, counseling], M15 [must_check, absolute_contraindication, must_check×6, inform], M16 [absolute_contraindication, must_check×2, absolute_contraindication, must_check×2, counseling], M17 [absolute_contraindication×2, must_check×2, counseling×3, inform].
- P: `/category_specific/14/checks/1` '임신 테스트 (레티노이드 처방 시 필수)' 는 검사 행위 문구인데 type 이 absolute_contraindication — 문구 종류와 type 이 다른 축으로 보임(잠정).
- P: M15 의 간기능·지질 확인은 '(… 처방 시)' 조건이 붙는다 — 시술이 아니라 처방이 조건이다.
- P: `/category_specific/15/checks/3/label` 은 문구 안에 '금기' 를 명시한 유일한 값이다(원문 전체에서 '금기' 출현 1회).
- P: 수치가 원문에 있는 곳은 범위·백분율 형태(0.005-0.39%·2-4개월). 모집단·출처 미기재.
- P: '이소트레티노인' 문구는 원장 전체 5곳(`/universal_checks/6/description`, M8·M11·M12·M15)에 있고 M8 과 M15 는 같은 문자열, M11 과 M12 는 같은 문자열이다.

## 이 구획의 미결 (A=추출/해석 오류, B=원문 정보 부족, C=사용자 결정 필요, K=분석 한계, P=잠정, F=후속, I=원문 불일치)

- **B-S05-1** [open] '고용량' 비타민 C 기준 없음 — 위치: `/category_specific/15/checks/2/label`, `/category_specific/15/checks/3/label`
- **B-S05-2** [open] '피하지방 두께'·'지질 수치'·'필링 간격' 기준값 없음(S04-1 과 같은 유형) — 위치: `/category_specific/13/checks/3/label`, `/category_specific/14/checks/3/label`, `/category_specific/14/checks/7/label`
- **B-S05-3** [open] PAH '0.005-0.39%' 의 분모·출처 없음(값은 그대로 보존, 해석하지 않음) — 위치: `/category_specific/13/checks/5/label`
- **P-S05-4** [open] 검사 행위 문구(임신 테스트)에 absolute_contraindication — type 이 문구 종류가 아니라 다른 축(중대도 등)일 가능성. 확정하지 않음 — 위치: `/category_specific/14/checks/1/label`, `/category_specific/14/checks/1/type`
- **K-S05-5** [recorded] 자동 AP-DEGREE «이상» 이 '감각 이상'(abnormality) 에서 일치 — 오탐 — 위치: `/category_specific/13/checks/6/label`
- **K-S05-6** [recorded] kiwi 가 '금기' 를 '금/NNG 기/XSN' 로 나눔 — 원문의 유일한 '금기' 명시어가 토큰에서 깨짐. 자동 AP-NEG 는 원문 문자열에서 '금기' 를 잡았다 — 위치: `/category_specific/15/checks/3/label`

## 알려진 형태소 오분절 (K — 출현별)

- `/category_specific/13/checks/0/label` «한냉두드러기» → 원시 `한/MM 냉/NNG 두드러기/NNG` — 영향: '한냉' 이 관형사 '한'(one)+'냉' 으로 오분석 — 질환명 단위 소실
- `/category_specific/13/checks/7/label` «2-4» → 원시 `2-4/W_SERIAL` — 영향: 수치 범위가 일련번호 단일 토큰
- `/category_specific/14/checks/0/label` «비박리성» → 원시 `비/XPN 박/NNG 리/XSN 성/NNG` — 영향: '박리성' 어간 깨짐
- `/category_specific/15/checks/3/label` «G6PD» → 원시 `G/SL 6/SN PD/SL` — 영향: 효소명 식별자가 셋으로 나뉨 — 원문 구절로만 보존
- `/category_specific/15/checks/3/label` «금기» → 원시 `금/NNG 기/XSN` — 영향: 금지 명시어 '금기' 가 깨짐 — 형태소 기반 금기 탐지 실패
- `/category_specific/15/checks/2/label` «시» → 원시 `시/NNG` — 영향: 조건 의존명사 '시' 가 다른 곳(NNB)과 달리 NNG — 조건 표지 태그가 출현마다 다름

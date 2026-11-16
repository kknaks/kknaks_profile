# review-part-S04 — category_specific M9–M13 (index 8–12)

- 원본: `orchestration/work/phub-recommend/bronze/phub-ledger/pre-procedure-checklist.json` (sha256 `0de87bff91f721fe685884025d31749017d44da250492b2db9d49109a61e4086`)
- 직접 읽기 상태: **read** — /category_specific/8 … /12 (M9 기기 리프팅 6·M10 HIFES/EMS 6·M11 니들RF 7·M12 마이크로니들링(MTS) 7·M13 플라즈마 6 = checks 32) id·name·label·type 전부
- 소유 Pointer: `/category_specific/8`, `/category_specific/9`, `/category_specific/10`, `/category_specific/11`, `/category_specific/12`
- 공동 참조 문맥(소유 아님): `/description`, `/category_specific`
- 열 구분: **원문 값** 칸은 원본 그대로(가공 없음). 관찰은 아래 별도 절에만 있다. 형태소 열은 kiwi 원시 결과(`form/tag`)이며 도메인 정답이 아니다.

## 원문 값 (원본 컬럼명 그대로, 원본 순서)

| JSON Pointer | 원본 컬럼명(key/index) | 자료형 | 원문 값 | 분석 적용 | kiwi 원시 토큰(form/tag) |
|---|---|---|---|---|---|
| `/category_specific/8` | `[8]` | object(자식 3) | keys=['id', 'name', 'checks'] | — | — |
| `/category_specific/8/id` | `id` | string | M9 | excluded | — |
| `/category_specific/8/name` | `name` | string | 기기 리프팅 | analyzed | 기기/NNG 리프팅/NNG |
| `/category_specific/8/checks` | `checks` | array(자식 6) |  | — | — |
| `/category_specific/8/checks/0` | `[0]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/8/checks/0/label` | `label` | string | 체내 금속 임플란트/페이스메이커 여부 | analyzed | 체내/NNG 금속/NNG 임플란트/NNG //SP 페이스/NNG 메이커/NNG 여부/NNG |
| `/category_specific/8/checks/0/type` | `type` | string | absolute_contraindication | excluded | — |
| `/category_specific/8/checks/1` | `[1]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/8/checks/1/label` | `label` | string | 시술 부위 필러/실리콘 존재 여부 | analyzed | 시술/NNG 부위/NNG 필/NNG 러/EC //SP 실리콘/NNG 존재/NNG 여부/NNG |
| `/category_specific/8/checks/1/type` | `type` | string | must_check | excluded | — |
| `/category_specific/8/checks/2` | `[2]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/8/checks/2/label` | `label` | string | 최근 골드 실/금속 실 시술 이력 | analyzed | 최근/MAG 골드/NNG 실/NNG //SP 금속/NNG 실/NNG 시술/NNG 이력/NNG |
| `/category_specific/8/checks/2/type` | `type` | string | absolute_contraindication | excluded | — |
| `/category_specific/8/checks/3` | `[3]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/8/checks/3/label` | `label` | string | 신경계 질환 여부 (간질 등) | analyzed | 신경/NNG 계/XSN 질환/NNG 여부/NNG (/SSO 간질/NNG 등/NNB )/SSC |
| `/category_specific/8/checks/3/type` | `type` | string | must_check | excluded | — |
| `/category_specific/8/checks/4` | `[4]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/8/checks/4/label` | `label` | string | 초음파/RF 에너지별 특성 및 통증 수준 설명 | analyzed | 초/XPN 음파/NNG //SP RF/SL 에너지/NNG 별/XSN 특성/NNG 및/MAG 통증/NNG 수준/NNG 설명/NNG |
| `/category_specific/8/checks/4/type` | `type` | string | counseling | excluded | — |
| `/category_specific/8/checks/5` | `[5]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/8/checks/5/label` | `label` | string | 지방층 두께 확인 (HIFU 시 화상 위험) | analyzed | 지방/NNG 층/XSN 두께/NNG 확인/NNG (/SSO HIFU/SL 시/NNB 화상/NNG 위험/NNG )/SSC |
| `/category_specific/8/checks/5/type` | `type` | string | must_check | excluded | — |
| `/category_specific/9` | `[9]` | object(자식 3) | keys=['id', 'name', 'checks'] | — | — |
| `/category_specific/9/id` | `id` | string | M10 | excluded | — |
| `/category_specific/9/name` | `name` | string | HIFES/EMS | analyzed | HIFES/SL //SP EMS/SL |
| `/category_specific/9/checks` | `checks` | array(자식 6) |  | — | — |
| `/category_specific/9/checks/0` | `[0]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/9/checks/0/label` | `label` | string | 체내 금속 임플란트/페이스메이커 여부 | analyzed | 체내/NNG 금속/NNG 임플란트/NNG //SP 페이스/NNG 메이커/NNG 여부/NNG |
| `/category_specific/9/checks/0/type` | `type` | string | absolute_contraindication | excluded | — |
| `/category_specific/9/checks/1` | `[1]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/9/checks/1/label` | `label` | string | 간질/경련성 질환 여부 | analyzed | 간질/NNG //SP 경련/NNG 성/XSN 질환/NNG 여부/NNG |
| `/category_specific/9/checks/1/type` | `type` | string | absolute_contraindication | excluded | — |
| `/category_specific/9/checks/2` | `[2]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/9/checks/2/label` | `label` | string | 최근 복부/시술 부위 수술 이력 | analyzed | 최근/NNG 복부/NNG //SP 시술/NNG 부위/NNG 수술/NNG 이력/NNG |
| `/category_specific/9/checks/2/type` | `type` | string | must_check | excluded | — |
| `/category_specific/9/checks/3` | `[3]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/9/checks/3/label` | `label` | string | 임신 여부 (복부 시술 시 특히 중요) | analyzed | 임신/NNG 여부/NNG (/SSO 복부/NNG 시술/NNG 시/NNB 특히/MAG 중요/NNG )/SSC |
| `/category_specific/9/checks/3/type` | `type` | string | absolute_contraindication | excluded | — |
| `/category_specific/9/checks/4` | `[4]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/9/checks/4/label` | `label` | string | 횡문근융해증 위험 설명 (과도한 세팅) | analyzed | 횡문근융해증/NNG 위험/NNG 설명/NNG (/SSO 과도/NNG 하/XSA ᆫ/ETM 세팅/NNG )/SSC |
| `/category_specific/9/checks/4/type` | `type` | string | inform | excluded | — |
| `/category_specific/9/checks/5` | `[5]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/9/checks/5/label` | `label` | string | 기대 효과 및 한계 설명 (지방감소가 아닌 근육강화) | analyzed | 기대/NNG 효과/NNG 및/MAG 한계/NNG 설명/NNG (/SSO 지방/NNG 감소/NNG 가/JKC 아니/VCN ᆫ/ETM 근육/NNG 강화/NNG )/SSC |
| `/category_specific/9/checks/5/type` | `type` | string | counseling | excluded | — |
| `/category_specific/10` | `[10]` | object(자식 3) | keys=['id', 'name', 'checks'] | — | — |
| `/category_specific/10/id` | `id` | string | M11 | excluded | — |
| `/category_specific/10/name` | `name` | string | 니들RF | analyzed | 니들/NNP RF/SL |
| `/category_specific/10/checks` | `checks` | array(자식 7) |  | — | — |
| `/category_specific/10/checks/0` | `[0]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/10/checks/0/label` | `label` | string | 체내 금속 임플란트 여부 (시술 부위) | analyzed | 체내/NNG 금속/NNG 임플란트/NNG 여부/NNG (/SSO 시술/NNG 부위/NNG )/SSC |
| `/category_specific/10/checks/0/type` | `type` | string | absolute_contraindication | excluded | — |
| `/category_specific/10/checks/1` | `[1]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/10/checks/1/label` | `label` | string | 켈로이드 체질 확인 | analyzed | 켈로이드/NNG 체질/NNG 확인/NNG |
| `/category_specific/10/checks/1/type` | `type` | string | must_check | excluded | — |
| `/category_specific/10/checks/2` | `[2]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/10/checks/2/label` | `label` | string | 이소트레티노인 복용 여부/중단 시점 확인 — 프락셔널/얕은 필링 6개월, 박리성 레이저 12개월 대기 원칙 (비박리성 얕은 시술은 의사 판단 하에 조기 고려 가능) | analyzed | 이소트레티노인/NNG 복용/NNG 여부/NNG //SP 중단/NNG 시점/NNG 확인/NNG —/SW 프락셔널/NNG //SP 얕/VA 은/ETM 필링/NNG 6/SN 개월/NNB ,/SP 박리성/NNP 레이저/NNG 12/SN 개월/NNB 대기/NNG 원칙/NNG (/SSO 비/XPN 박/NNG 리/XSN 성/NNG 얕/VA 은/ETM 시술/NNG 은/JX 의사/NNG 판단/NNG 하/NNG 에/JKB 조기/NNG 고려/NNG 가능/NNG )/SSC |
| `/category_specific/10/checks/2/type` | `type` | string | must_check | excluded | — |
| `/category_specific/10/checks/3` | `[3]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/10/checks/3/label` | `label` | string | 항응고제 복용 여부 (출혈 위험) | analyzed | 항응고제/NNG 복용/NNG 여부/NNG (/SSO 출혈/NNG 위험/NNG )/SSC |
| `/category_specific/10/checks/3/type` | `type` | string | must_check | excluded | — |
| `/category_specific/10/checks/4` | `[4]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/10/checks/4/label` | `label` | string | 활동성 여드름/감염 부위 확인 | analyzed | 활동/NNG 성/XSN 여드름/NNG //SP 감염/NNG 부위/NNG 확인/NNG |
| `/category_specific/10/checks/4/type` | `type` | string | must_check | excluded | — |
| `/category_specific/10/checks/5` | `[5]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/10/checks/5/label` | `label` | string | 마취크림 도포 및 시간 안내 | analyzed | 마취/NNG 크림/NNG 도포/NNG 및/MAG 시간/NNG 안내/NNG |
| `/category_specific/10/checks/5/type` | `type` | string | inform | excluded | — |
| `/category_specific/10/checks/6` | `[6]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/10/checks/6/label` | `label` | string | 시술 후 붉어짐/부종 다운타임 설명 | analyzed | 시술/NNG 후/NNG 붉어지/VV ᆷ/ETN //SP 부종/NNG 다운타임/NNP 설명/NNG |
| `/category_specific/10/checks/6/type` | `type` | string | counseling | excluded | — |
| `/category_specific/11` | `[11]` | object(자식 3) | keys=['id', 'name', 'checks'] | — | — |
| `/category_specific/11/id` | `id` | string | M12 | excluded | — |
| `/category_specific/11/name` | `name` | string | 마이크로니들링(MTS) | analyzed | 마이크로니들링/NNP (/SSO MTS/SL )/SSC |
| `/category_specific/11/checks` | `checks` | array(자식 7) |  | — | — |
| `/category_specific/11/checks/0` | `[0]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/11/checks/0/label` | `label` | string | 활동성 여드름/감염/헤르페스 여부 | analyzed | 활동/NNG 성/XSN 여드름/NNG //SP 감염/NNG //SP 헤르페스/NNG 여부/NNG |
| `/category_specific/11/checks/0/type` | `type` | string | absolute_contraindication | excluded | — |
| `/category_specific/11/checks/1` | `[1]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/11/checks/1/label` | `label` | string | 켈로이드 체질 확인 | analyzed | 켈로이드/NNG 체질/NNG 확인/NNG |
| `/category_specific/11/checks/1/type` | `type` | string | must_check | excluded | — |
| `/category_specific/11/checks/2` | `[2]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/11/checks/2/label` | `label` | string | 이소트레티노인 복용 여부/중단 시점 확인 — 프락셔널/얕은 필링 6개월, 박리성 레이저 12개월 대기 원칙 (비박리성 얕은 시술은 의사 판단 하에 조기 고려 가능) | analyzed | 이소트레티노인/NNG 복용/NNG 여부/NNG //SP 중단/NNG 시점/NNG 확인/NNG —/SW 프락셔널/NNG //SP 얕/VA 은/ETM 필링/NNG 6/SN 개월/NNB ,/SP 박리성/NNP 레이저/NNG 12/SN 개월/NNB 대기/NNG 원칙/NNG (/SSO 비/XPN 박/NNG 리/XSN 성/NNG 얕/VA 은/ETM 시술/NNG 은/JX 의사/NNG 판단/NNG 하/NNG 에/JKB 조기/NNG 고려/NNG 가능/NNG )/SSC |
| `/category_specific/11/checks/2/type` | `type` | string | must_check | excluded | — |
| `/category_specific/11/checks/3` | `[3]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/11/checks/3/label` | `label` | string | 항응고제/항혈소판제 복용 여부 | analyzed | 항응고제/NNG //SP 항혈소판제/NNG 복용/NNG 여부/NNG |
| `/category_specific/11/checks/3/type` | `type` | string | must_check | excluded | — |
| `/category_specific/11/checks/4` | `[4]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/11/checks/4/label` | `label` | string | 당뇨/면역저하 상태 (감염 위험 증가) | analyzed | 당뇨/NNG //SP 면역/NNG 저하/NNG 상태/NNG (/SSO 감염/NNG 위험/NNG 증가/NNG )/SSC |
| `/category_specific/11/checks/4/type` | `type` | string | must_check | excluded | — |
| `/category_specific/11/checks/5` | `[5]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/11/checks/5/label` | `label` | string | 니들 깊이별 다운타임 설명 | analyzed | 니/NP 들/XSN 깊이/NNG 별/XSN 다운/NNG 타임/NNG 설명/NNG |
| `/category_specific/11/checks/5/type` | `type` | string | counseling | excluded | — |
| `/category_specific/11/checks/6` | `[6]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/11/checks/6/label` | `label` | string | 시술 후 자외선 차단 필수 안내 | analyzed | 시술/NNG 후/NNG 자외선/NNG 차단/NNG 필수/NNG 안내/NNG |
| `/category_specific/11/checks/6/type` | `type` | string | inform | excluded | — |
| `/category_specific/12` | `[12]` | object(자식 3) | keys=['id', 'name', 'checks'] | — | — |
| `/category_specific/12/id` | `id` | string | M13 | excluded | — |
| `/category_specific/12/name` | `name` | string | 플라즈마 | analyzed | 플라즈마/NNG |
| `/category_specific/12/checks` | `checks` | array(자식 6) |  | — | — |
| `/category_specific/12/checks/0` | `[0]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/12/checks/0/label` | `label` | string | 페이스메이커/전자 의료기기 여부 | analyzed | 페이스/NNG 메이커/NNG //SP 전자/NNG 의료/NNG 기기/NNG 여부/NNG |
| `/category_specific/12/checks/0/type` | `type` | string | absolute_contraindication | excluded | — |
| `/category_specific/12/checks/1` | `[1]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/12/checks/1/label` | `label` | string | 시술 부위 금속 임플란트 여부 | analyzed | 시술/NNG 부위/NNG 금속/NNG 임플란트/NNG 여부/NNG |
| `/category_specific/12/checks/1/type` | `type` | string | must_check | excluded | — |
| `/category_specific/12/checks/2` | `[2]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/12/checks/2/label` | `label` | string | 광과민성 질환/약물 복용 여부 | analyzed | 광/NNG 과민/NNG 성/XSN 질환/NNG //SP 약물/NNG 복용/NNG 여부/NNG |
| `/category_specific/12/checks/2/type` | `type` | string | must_check | excluded | — |
| `/category_specific/12/checks/3` | `[3]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/12/checks/3/label` | `label` | string | 켈로이드 체질 확인 | analyzed | 켈로이드/NNG 체질/NNG 확인/NNG |
| `/category_specific/12/checks/3/type` | `type` | string | must_check | excluded | — |
| `/category_specific/12/checks/4` | `[4]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/12/checks/4/label` | `label` | string | 시술 부위 활동성 감염 여부 | analyzed | 시술/NNG 부위/NNG 활동/NNG 성/XSN 감염/NNG 여부/NNG |
| `/category_specific/12/checks/4/type` | `type` | string | must_check | excluded | — |
| `/category_specific/12/checks/5` | `[5]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/12/checks/5/label` | `label` | string | 크러스트(딱지) 형성 및 관리 방법 설명 | analyzed | 크러스트/NNP (/SSO 딱지/NNG )/SSC 형성/NNG 및/MAG 관리/NNG 방법/NNG 설명/NNG |
| `/category_specific/12/checks/5/type` | `type` | string | counseling | excluded | — |

## 자동 표현 후보 (정규식 일치분만 — 패턴 밖은 아래 수동 절)

- **AP-NUM-UNIT** (4): `/category_specific/10/checks/2/label`[36,39) «6개월»; `/category_specific/10/checks/2/label`[49,53) «12개월»; `/category_specific/11/checks/2/label`[36,39) «6개월»; `/category_specific/11/checks/2/label`[49,53) «12개월»
- **AP-PAREN** (12): `/category_specific/8/checks/3/label`[10,16) «(간질 등)»; `/category_specific/8/checks/5/label`[10,24) «(HIFU 시 화상 위험)»; `/category_specific/9/checks/3/label`[6,21) «(복부 시술 시 특히 중요)»; `/category_specific/9/checks/4/label`[13,21) «(과도한 세팅)»; `/category_specific/9/checks/5/label`[14,29) «(지방감소가 아닌 근육강화)»; `/category_specific/10/checks/0/label`[14,21) «(시술 부위)»; `/category_specific/10/checks/2/label`[60,91) «(비박리성 얕은 시술은 의사 판단 하에 조기 고려 가능)»; `/category_specific/10/checks/3/label`[11,18) «(출혈 위험)»; `/category_specific/11/name`[7,12) «(MTS)»; `/category_specific/11/checks/2/label`[60,91) «(비박리성 얕은 시술은 의사 판단 하에 조기 고려 가능)»; `/category_specific/11/checks/4/label`[11,21) «(감염 위험 증가)»; `/category_specific/12/checks/5/label`[4,8) «(딱지)»
- **AP-SLASH** (19): `/category_specific/8/checks/0/label`[6,17) «임플란트/페이스메이커»; `/category_specific/8/checks/1/label`[6,12) «필러/실리콘»; `/category_specific/8/checks/2/label`[6,10) «실/금속»; `/category_specific/8/checks/4/label`[0,6) «초음파/RF»; `/category_specific/9/name`[0,9) «HIFES/EMS»; `/category_specific/9/checks/0/label`[6,17) «임플란트/페이스메이커»; `/category_specific/9/checks/1/label`[0,6) «간질/경련성»; `/category_specific/9/checks/2/label`[3,8) «복부/시술»; `/category_specific/10/checks/2/label`[11,16) «여부/중단»; `/category_specific/10/checks/2/label`[25,32) «프락셔널/얕은»; `/category_specific/10/checks/4/label`[4,10) «여드름/감염»; `/category_specific/10/checks/6/label`[5,11) «붉어짐/부종»; `/category_specific/11/checks/0/label`[4,15) «여드름/감염/헤르페스»; `/category_specific/11/checks/2/label`[11,16) «여부/중단»; `/category_specific/11/checks/2/label`[25,32) «프락셔널/얕은»; `/category_specific/11/checks/3/label`[0,10) «항응고제/항혈소판제»; `/category_specific/11/checks/4/label`[0,7) «당뇨/면역저하»; `/category_specific/12/checks/0/label`[0,9) «페이스메이커/전자»; `/category_specific/12/checks/2/label`[5,10) «질환/약물»
- **AP-DASH** (2): `/category_specific/10/checks/2/label`[23,91) «— 프락셔널/얕은 필링 6개월, 박리성 레이저 12개월 대기 원칙 (비박리성 얕은 시술은 의사 판단 하에 조기 고려 가능)»; `/category_specific/11/checks/2/label`[23,91) «— 프락셔널/얕은 필링 6개월, 박리성 레이저 12개월 대기 원칙 (비박리성 얕은 시술은 의사 판단 하에 조기 고려 가능)»
- **AP-NEG** (3): `/category_specific/9/checks/5/label`[21,23) «아닌»; `/category_specific/10/checks/2/label`[61,62) «비»; `/category_specific/11/checks/2/label`[61,62) «비»
- **AP-POSS** (6): `/category_specific/8/checks/5/label`[21,23) «위험»; `/category_specific/9/checks/4/label`[7,9) «위험»; `/category_specific/10/checks/2/label`[88,90) «가능»; `/category_specific/10/checks/3/label`[15,17) «위험»; `/category_specific/11/checks/2/label`[88,90) «가능»; `/category_specific/11/checks/4/label`[15,17) «위험»
- **AP-COND** (10): `/category_specific/8/checks/5/label`[15,17) « 시»; `/category_specific/9/checks/3/label`[12,14) « 시»; `/category_specific/10/checks/2/label`[14,16) «중단»; `/category_specific/10/checks/2/label`[54,56) «대기»; `/category_specific/10/checks/2/label`[79,81) «하에»; `/category_specific/10/checks/6/label`[3,4) «후»; `/category_specific/11/checks/2/label`[14,16) «중단»; `/category_specific/11/checks/2/label`[54,56) «대기»; `/category_specific/11/checks/2/label`[79,81) «하에»; `/category_specific/11/checks/6/label`[3,4) «후»
- **AP-MODAL** (22): `/category_specific/8/checks/4/label`[23,25) «설명»; `/category_specific/8/checks/5/label`[7,9) «확인»; `/category_specific/9/checks/4/label`[10,12) «설명»; `/category_specific/9/checks/5/label`[11,13) «설명»; `/category_specific/10/checks/1/label`[8,10) «확인»; `/category_specific/10/checks/2/label`[20,22) «확인»; `/category_specific/10/checks/2/label`[57,59) «원칙»; `/category_specific/10/checks/2/label`[76,78) «판단»; `/category_specific/10/checks/2/label`[85,87) «고려»; `/category_specific/10/checks/4/label`[14,16) «확인»; `/category_specific/10/checks/5/label`[13,15) «안내»; `/category_specific/10/checks/6/label`[17,19) «설명»; `/category_specific/11/checks/1/label`[8,10) «확인»; `/category_specific/11/checks/2/label`[20,22) «확인»; `/category_specific/11/checks/2/label`[57,59) «원칙»; `/category_specific/11/checks/2/label`[76,78) «판단»; `/category_specific/11/checks/2/label`[85,87) «고려»; `/category_specific/11/checks/5/label`[12,14) «설명»; `/category_specific/11/checks/6/label`[12,14) «필수»; `/category_specific/11/checks/6/label`[15,17) «안내»; `/category_specific/12/checks/3/label`[8,10) «확인»; `/category_specific/12/checks/5/label`[20,22) «설명»
- **AP-DEGREE** (6): `/category_specific/8/checks/2/label`[0,2) «최근»; `/category_specific/9/checks/2/label`[0,2) «최근»; `/category_specific/9/checks/3/label`[15,17) «특히»; `/category_specific/9/checks/4/label`[14,17) «과도한»; `/category_specific/10/checks/2/label`[82,84) «조기»; `/category_specific/11/checks/2/label`[82,84) «조기»
- **AP-ETC** (1): `/category_specific/8/checks/3/label`[13,15) « 등»

## 수동 수집 표현 (직접 읽기 — 원문 구간)

| Pointer | 구간 | 원문 구절 | 탐색 관점(잠정) | 메모 |
|---|---|---|---|---|
| `/category_specific/8/checks/0/label` | [0,20) | 체내 금속 임플란트/페이스메이커 여부 | 부위(체내), 슬래시 나열, 기기 |  |
| `/category_specific/8/checks/1/label` | [0,18) | 시술 부위 필러/실리콘 존재 여부 | 부위, 다른 시술 잔여물 |  |
| `/category_specific/8/checks/2/label` | [0,18) | 최근 골드 실/금속 실 시술 이력 | 시점(최근), 슬래시 나열, 재질 |  |
| `/category_specific/8/checks/3/label` | [0,16) | 신경계 질환 여부 (간질 등) | 괄호 예시, 열린 나열(등) |  |
| `/category_specific/8/checks/4/label` | [0,25) | 초음파/RF 에너지별 특성 및 통증 수준 설명 | 슬래시(에너지 종류), 별(범위), 수준, 행위(설명) |  |
| `/category_specific/8/checks/5/label` | [0,24) | 지방층 두께 확인 (HIFU 시 화상 위험) | 두께(기준 미기재), 조건(HIFU 시), 위험 |  |
| `/category_specific/9/name` | [0,9) | HIFES/EMS | 카테고리명 슬래시, 영문 약어 |  |
| `/category_specific/9/checks/0/label` | [0,20) | 체내 금속 임플란트/페이스메이커 여부 | 부위(체내), 슬래시 나열 | `/category_specific/8/checks/0/label` 과 같은 문자열 |
| `/category_specific/9/checks/1/label` | [0,12) | 간질/경련성 질환 여부 | 슬래시 나열 |  |
| `/category_specific/9/checks/2/label` | [0,17) | 최근 복부/시술 부위 수술 이력 | 시점(최근), 부위(복부/시술 부위) |  |
| `/category_specific/9/checks/3/label` | [0,21) | 임신 여부 (복부 시술 시 특히 중요) | 조건(복부 시술 시), 강조(특히) | type absolute_contraindication 과 조건적 강조가 함께 있음 |
| `/category_specific/9/checks/4/label` | [0,21) | 횡문근융해증 위험 설명 (과도한 세팅) | 위험, 괄호 조건/원인, 형용사(과도한) |  |
| `/category_specific/9/checks/5/label` | [0,29) | 기대 효과 및 한계 설명 (지방감소가 아닌 근육강화) | 한계, 부정 대조(아닌) |  |
| `/category_specific/9/checks/5/label` | [15,28) | 지방감소가 아닌 근육강화 | 부정 대조 |  |
| `/category_specific/10/name` | [0,4) | 니들RF | 카테고리명, 한영 혼합 |  |
| `/category_specific/10/checks/0/label` | [0,21) | 체내 금속 임플란트 여부 (시술 부위) | 부위(체내 vs 괄호 시술 부위), 괄호 한정 |  |
| `/category_specific/10/checks/2/label` | [0,22) | 이소트레티노인 복용 여부/중단 시점 확인 | 슬래시(여부/시점), 중단 |  |
| `/category_specific/10/checks/2/label` | [25,59) | 프락셔널/얕은 필링 6개월, 박리성 레이저 12개월 대기 원칙 | 기간, 원칙 |  |
| `/category_specific/10/checks/2/label` | [60,91) | (비박리성 얕은 시술은 의사 판단 하에 조기 고려 가능) | 괄호 예외, 부정 접두(비-), 가능성 | '2017 AAD Task Force' 언급 없음 |
| `/category_specific/10/checks/3/label` | [0,18) | 항응고제 복용 여부 (출혈 위험) | 괄호 위험 |  |
| `/category_specific/10/checks/4/label` | [0,16) | 활동성 여드름/감염 부위 확인 | 형용사(활동성), 슬래시 범위, 부위 |  |
| `/category_specific/10/checks/5/label` | [0,15) | 마취크림 도포 및 시간 안내 | 절차, 시간(값 미기재) |  |
| `/category_specific/10/checks/6/label` | [0,19) | 시술 후 붉어짐/부종 다운타임 설명 | 시점(시술 후), 증상 나열 |  |
| `/category_specific/11/name` | [0,12) | 마이크로니들링(MTS) | 카테고리명, 괄호 약어 |  |
| `/category_specific/11/checks/0/label` | [0,18) | 활동성 여드름/감염/헤르페스 여부 | 형용사(활동성), 슬래시 범위 | '활동성' 이 세 항목 모두에 걸리는지 잠정 |
| `/category_specific/11/checks/2/label` | [60,91) | (비박리성 얕은 시술은 의사 판단 하에 조기 고려 가능) | 괄호 예외, 부정 접두(비-), 가능성 | `/category_specific/10/checks/2/label` 과 같은 문자열 |
| `/category_specific/11/checks/3/label` | [0,16) | 항응고제/항혈소판제 복용 여부 | 슬래시 나열 |  |
| `/category_specific/11/checks/4/label` | [0,21) | 당뇨/면역저하 상태 (감염 위험 증가) | 슬래시 나열, 괄호 위험, 증가 |  |
| `/category_specific/11/checks/5/label` | [0,14) | 니들 깊이별 다운타임 설명 | 깊이(값 미기재), 별(범위) |  |
| `/category_specific/11/checks/6/label` | [0,17) | 시술 후 자외선 차단 필수 안내 | 시점(시술 후), 의무(필수) |  |
| `/category_specific/12/checks/0/label` | [0,17) | 페이스메이커/전자 의료기기 여부 | 슬래시(개별/상위), 기기 |  |
| `/category_specific/12/checks/1/label` | [0,16) | 시술 부위 금속 임플란트 여부 | 부위(시술 부위) |  |
| `/category_specific/12/checks/2/label` | [0,16) | 광과민성 질환/약물 복용 여부 | 슬래시 범위 | '복용' 이 질환에는 걸리지 않음 — 슬래시가 '질환/약물 복용' 의 축약으로 보임(잠정) |
| `/category_specific/12/checks/4/label` | [0,15) | 시술 부위 활동성 감염 여부 | 부위, 형용사(활동성) |  |
| `/category_specific/12/checks/5/label` | [0,22) | 크러스트(딱지) 형성 및 관리 방법 설명 | 괄호 풀이(동의 표기), 행위(설명) |  |
| `/category_specific/11/checks/2/label` | [0,22) | 이소트레티노인 복용 여부/중단 시점 확인 | 슬래시(여부/시점), 중단 | 읽기 검토에서 누락 발견 후 추가(A-S04-6) |
| `/category_specific/11/checks/2/label` | [25,59) | 프락셔널/얕은 필링 6개월, 박리성 레이저 12개월 대기 원칙 | 기간, 원칙, 슬래시 범위 | 읽기 검토에서 누락 발견 후 추가(A-S04-6) |
| `/category_specific/10/checks/1/label` | [0,10) | 켈로이드 체질 확인 | 체질 |  |
| `/category_specific/11/checks/1/label` | [0,10) | 켈로이드 체질 확인 | 체질 |  |
| `/category_specific/12/checks/3/label` | [0,10) | 켈로이드 체질 확인 | 체질 |  |

## 잠정 관찰 (원문 아님 — 근거 위치 포함)

- P: type 분포 — M9 [absolute_contraindication, must_check, absolute_contraindication, must_check, counseling, must_check], M10 [absolute_contraindication×2, must_check, absolute_contraindication, inform, counseling], M11 [absolute_contraindication, must_check×4, inform, counseling], M12 [absolute_contraindication, must_check×4, counseling, inform], M13 [absolute_contraindication, must_check×4, counseling].
- P: 금속 임플란트·페이스메이커 문구 변형 — M9·M10 '체내 금속 임플란트/페이스메이커 여부'(absolute_contraindication), M11 '체내 금속 임플란트 여부 (시술 부위)'(absolute_contraindication), M13 '시술 부위 금속 임플란트 여부'(must_check)·'페이스메이커/전자 의료기기 여부'(absolute_contraindication), M8 '금속 임플란트 확인 — RF/HIFU 병행 시'(must_check).
- P: 이소트레티노인 문구 — M11·M12 는 서로 같은 문자열이고 예외를 괄호에 넣으며 '2017 AAD Task Force' 가 없다. M8·M15 는 마침표 뒤 문장·출처 언급 있음.
- P: M12 '시술 후 자외선 차단 필수 안내', M11 '시술 후 붉어짐/부종 다운타임 설명' — 시술 후 내용이 시술 전 체크리스트에 있음(S03 관찰과 같은 유형).
- P: 깊이·두께·시간처럼 수치가 들어갈 자리를 말하지만 값은 없다: '지방층 두께', '니들 깊이별', '마취크림 도포 및 시간'.

## 이 구획의 미결 (A=추출/해석 오류, B=원문 정보 부족, C=사용자 결정 필요, K=분석 한계, P=잠정, F=후속, I=원문 불일치)

- **B-S04-1** [open] 수치 자리만 있고 값이 없음 — 지방층 두께 기준, 니들 깊이별 구분, 마취크림 시간, '과도한 세팅' 기준 — 위치: `/category_specific/8/checks/5/label`, `/category_specific/11/checks/5/label`, `/category_specific/10/checks/5/label`, `/category_specific/9/checks/4/label`
- **B-S04-2** [open] '최근' 기간 기준 없음(골드 실/금속 실, 복부/시술 부위 수술) — 위치: `/category_specific/8/checks/2/label`, `/category_specific/9/checks/2/label`
- **I-S04-3** [open] 한 문자열 안에서 '체내'(전신) 와 '(시술 부위)'(국소) 범위가 함께 쓰임 — 범위 불일치 후보. 원문 변경 제안 아님, 후속 확인 후보 — 위치: `/category_specific/10/checks/0/label`
- **P-S04-4** [open] M10 임신 항목은 type absolute_contraindication 인데 '(복부 시술 시 특히 중요)' 로 조건적 강조 — type 과 문구의 범위 관계 잠정 — 위치: `/category_specific/9/checks/3/label`, `/category_specific/9/checks/3/type`
- **F-S04-5** [deferred] 금속 임플란트/페이스메이커 계열 확인이 카테고리마다 문구·type 이 다름 — 같은 확인 대상인지 후속 비교 — 위치: `/category_specific/7/checks/8/label`, `/category_specific/8/checks/0/label`, `/category_specific/9/checks/0/label`, `/category_specific/10/checks/0/label`, `/category_specific/12/checks/0/label`, `/category_specific/12/checks/1/label`
- **A-S04-6** [fixed] 수동 표현 누락 — M12 이소트레티노인 문구의 괄호 앞 구절(복용 여부/중단 시점 확인 · 6개월/12개월 대기 원칙)을 직접 읽기 기록에서 빠뜨렸다. 자동 후보↔수동 표현 대조(읽기 검토)에서 발견, 추가 후 verify 재통과 — 위치: `/category_specific/11/checks/2/label`

## 알려진 형태소 오분절 (K — 출현별)

- `/category_specific/8/checks/0/label` «페이스메이커» → 원시 `페이스/NNG 메이커/NNG` — 영향: 기기명이 둘로 나뉨 — 의미 손실 작음
- `/category_specific/9/checks/0/label` «페이스메이커» → 원시 `페이스/NNG 메이커/NNG` — 영향: 기기명이 둘로 나뉨
- `/category_specific/12/checks/0/label` «페이스메이커» → 원시 `페이스/NNG 메이커/NNG` — 영향: 기기명이 둘로 나뉨
- `/category_specific/8/checks/1/label` «필러» → 원시 `필/NNG 러/EC` — 영향: '필러' 가 명사+어미로 깨짐 — 대상 명사 소실(같은 단어가 다른 곳에서는 필러/NNP)
- `/category_specific/8/checks/4/label` «초음파» → 원시 `초/XPN 음파/NNG` — 영향: '초음파' 가 접두+명사로 분리 — 에너지 종류 단위 소실
- `/category_specific/10/checks/2/label` «비박리성» → 원시 `비/XPN 박/NNG 리/XSN 성/NNG` — 영향: '박리성' 어간 깨짐
- `/category_specific/11/checks/2/label` «비박리성» → 원시 `비/XPN 박/NNG 리/XSN 성/NNG` — 영향: '박리성' 어간 깨짐
- `/category_specific/11/checks/5/label` «니들» → 원시 `니/NP 들/XSN` — 영향: '니들'(needle) 이 대명사 '니'+복수 접미 '들' 로 오분석 — 기구 명사 소실(심각). 카테고리명 '니들RF' 에서는 니들/NNP
- `/category_specific/11/checks/5/label` «다운타임» → 원시 `다운/NNG 타임/NNG` — 영향: 출현마다 분석 다름(다운타임/NNP 인 곳도 있음)

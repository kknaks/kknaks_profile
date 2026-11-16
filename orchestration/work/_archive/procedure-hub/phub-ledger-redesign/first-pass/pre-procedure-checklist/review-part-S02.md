# review-part-S02 — category_specific M1–M4 (index 0–3)

- 원본: `orchestration/work/phub-recommend/bronze/phub-ledger/pre-procedure-checklist.json` (sha256 `0de87bff91f721fe685884025d31749017d44da250492b2db9d49109a61e4086`)
- 직접 읽기 상태: **read** — /category_specific/0 … /3 (M1 보톡스 7·M2 필러 10·M3 6·M4 5 = checks 28) id·name·label·type 전부
- 소유 Pointer: `/category_specific/0`, `/category_specific/1`, `/category_specific/2`, `/category_specific/3`
- 공동 참조 문맥(소유 아님): `/description`, `/category_specific`
- 열 구분: **원문 값** 칸은 원본 그대로(가공 없음). 관찰은 아래 별도 절에만 있다. 형태소 열은 kiwi 원시 결과(`form/tag`)이며 도메인 정답이 아니다.

## 원문 값 (원본 컬럼명 그대로, 원본 순서)

| JSON Pointer | 원본 컬럼명(key/index) | 자료형 | 원문 값 | 분석 적용 | kiwi 원시 토큰(form/tag) |
|---|---|---|---|---|---|
| `/category_specific/0` | `[0]` | object(자식 3) | keys=['id', 'name', 'checks'] | — | — |
| `/category_specific/0/id` | `id` | string | M1 | excluded | — |
| `/category_specific/0/name` | `name` | string | 보톡스 | analyzed | 보톡스/NNG |
| `/category_specific/0/checks` | `checks` | array(자식 7) |  | — | — |
| `/category_specific/0/checks/0` | `[0]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/0/checks/0/label` | `label` | string | 신경근접합부 질환(중증근무력증 등) 확인 | analyzed | 신경/NNG 근/NNG 접합부/NNG 질환/NNG (/SSO 중증 근무력증/NNP 등/NNB )/SSC 확인/NNG |
| `/category_specific/0/checks/0/type` | `type` | string | absolute_contraindication | excluded | — |
| `/category_specific/0/checks/1` | `[1]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/0/checks/1/label` | `label` | string | 이전 보툴리눔 독소 시술 후 이상반응 여부 | analyzed | 이전/NNG 보툴리눔/NNG 독소/NNG 시술/NNG 후/NNG 이상/NNG 반응/NNG 여부/NNG |
| `/category_specific/0/checks/1/type` | `type` | string | must_check | excluded | — |
| `/category_specific/0/checks/2` | `[2]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/0/checks/2/label` | `label` | string | 항응고제 복용 여부 (멍 위험 안내) | analyzed | 항응고제/NNG 복용/NNG 여부/NNG (/SSO 멍/NNG 위험/NNG 안내/NNG )/SSC |
| `/category_specific/0/checks/2/type` | `type` | string | inform | excluded | — |
| `/category_specific/0/checks/3` | `[3]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/0/checks/3/label` | `label` | string | 최근 보톡스 시술 시기 확인 (항체 내성) | analyzed | 최근/MAG 보톡스/NNG 시술/NNG 시기/NNG 확인/NNG (/SSO 항체/NNG 내성/NNG )/SSC |
| `/category_specific/0/checks/3/type` | `type` | string | must_check | excluded | — |
| `/category_specific/0/checks/4` | `[4]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/0/checks/4/label` | `label` | string | 아미노글리코시드 항생제 복용 여부 (보톡스 효과 증강 위험 — 겐타마이신, 토브라마이신 등) | analyzed | 아미노글리코시드/NNG 항생제/NNG 복용/NNG 여부/NNG (/SSO 보톡스/NNG 효과/NNG 증강/NNG 위험/NNG —/SW 겐타마이신/NNG ,/SP 토브라마이신/NNG 등/NNB )/SSC |
| `/category_specific/0/checks/4/type` | `type` | string | must_check | excluded | — |
| `/category_specific/0/checks/5` | `[5]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/0/checks/5/label` | `label` | string | D-페니실라민 복용 여부 (신경근접합부 기능 감소 — 보톡스 효과 예측 불가) | analyzed | D/SL -/SO 페니실라민/NNG 복용/NNG 여부/NNG (/SSO 신경/NNG 근/NNG 접합부/NNG 기능/NNG 감소/NNG —/SW 보톡스/NNG 효과/NNG 예측/NNG 불가/NNG )/SSC |
| `/category_specific/0/checks/5/type` | `type` | string | must_check | excluded | — |
| `/category_specific/0/checks/6` | `[6]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/0/checks/6/label` | `label` | string | 시술 부위 감염/염증 여부 | analyzed | 시술/NNG 부위/NNG 감염/NNG //SP 염증/NNG 여부/NNG |
| `/category_specific/0/checks/6/type` | `type` | string | must_check | excluded | — |
| `/category_specific/1` | `[1]` | object(자식 3) | keys=['id', 'name', 'checks'] | — | — |
| `/category_specific/1/id` | `id` | string | M2 | excluded | — |
| `/category_specific/1/name` | `name` | string | 필러 | analyzed | 필러/NNP |
| `/category_specific/1/checks` | `checks` | array(자식 10) |  | — | — |
| `/category_specific/1/checks/0` | `[0]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/1/checks/0/label` | `label` | string | 히알루로니다아제 알레르기 여부 | analyzed | 히알루로니다아제/NNG 알레르기/NNG 여부/NNG |
| `/category_specific/1/checks/0/type` | `type` | string | must_check | excluded | — |
| `/category_specific/1/checks/1` | `[1]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/1/checks/1/label` | `label` | string | 이전 필러 시술 부위 및 제품 확인 (잔여 필러) | analyzed | 이/NNP 전/MM 필러/NNP 시술/NNG 부위/NNG 및/MAG 제품/NNG 확인/NNG (/SSO 잔여/NNG 필러/NNP )/SSC |
| `/category_specific/1/checks/1/type` | `type` | string | must_check | excluded | — |
| `/category_specific/1/checks/2` | `[2]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/1/checks/2/label` | `label` | string | 잔여 영구필러(실리콘/PMMA) 존재 여부 — 이물반응, 합병증 위험 대폭 증가 | analyzed | 잔여/NNG 영구필러/NNG (/SSO 실리콘/NNG //SP PMMA/SL )/SSC 존재/NNG 여부/NNG —/SW 이/MM 물/NNG 반응/NNG ,/SP 합병증/NNG 위험/NNG 대폭/MAG 증가/NNG |
| `/category_specific/1/checks/2/type` | `type` | string | must_check | excluded | — |
| `/category_specific/1/checks/3` | `[3]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/1/checks/3/label` | `label` | string | 자가면역질환 여부 (육아종 위험) | analyzed | 자가/NNG 면역/NNG 질환/NNG 여부/NNG (/SSO 육아종/NNG 위험/NNG )/SSC |
| `/category_specific/1/checks/3/type` | `type` | string | must_check | excluded | — |
| `/category_specific/1/checks/4` | `[4]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/1/checks/4/label` | `label` | string | 혈관폐색 응급 프로토콜 준비 확인 | analyzed | 혈관/NNG 폐색/NNG 응급/NNG 프로토콜/NNG 준비/NNG 확인/NNG |
| `/category_specific/1/checks/4/type` | `type` | string | safety_protocol | excluded | — |
| `/category_specific/1/checks/5` | `[5]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/1/checks/5/label` | `label` | string | 히알루로니다아제 비상 비치 확인 | analyzed | 히알루로니다아제/NNP 비상/NNG 비치/NNG 확인/NNG |
| `/category_specific/1/checks/5/type` | `type` | string | safety_protocol | excluded | — |
| `/category_specific/1/checks/6` | `[6]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/1/checks/6/label` | `label` | string | HA vs 비HA 필러 선택 및 용해 가능 여부 설명 | analyzed | HA/SL vs/SL 비/XPN HA/SL 필러/NNP 선택/NNG 및/MAG 용해/NNG 가능/NNG 여부/NNG 설명/NNG |
| `/category_specific/1/checks/6/type` | `type` | string | counseling | excluded | — |
| `/category_specific/1/checks/7` | `[7]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/1/checks/7/label` | `label` | string | 최근 치과 시술 여부 확인 — 구강 내 세균이 혈행성 전파로 필러 감염 경로가 될 수 있음 | analyzed | 최근/NNG 치과/NNG 시술/NNG 여부/NNG 확인/NNG —/SW 구강/NNG 내/NNB 세균/NNG 이/JKS 혈/NNG 행/NNG 성/XSN 전파/NNG 로/JKB 피/VV ᆯ러/EC 감염/NNG 경로/NNG 가/JKC 되/VV ᆯ/ETM 수/NNB 있/VA 음/EF |
| `/category_specific/1/checks/7/type` | `type` | string | must_check | excluded | — |
| `/category_specific/1/checks/8` | `[8]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/1/checks/8/label` | `label` | string | 48시간 이내 비행기 탑승 예정 여부 — 기내 기압이 필러를 이동시키지는 않으나, 장시간 비행 시 붓기·멍이 더 도드라져 보일 수 있음(미용상) | analyzed | 48/SN 시간/NNB 이내/NNG 비행기/NNG 탑승/NNG 예정/NNG 여부/NNG —/SW 기내/NNG 기압/NNG 이/MM 필러/NNP 를/JKO 이동/NNG 시키/XSV 지/EC 는/JX 않/VX 으나/EC ,/SP 장시간/NNG 비행/NNG 시/NNB 붓/VV-I 기/ETN ·/SP 멍/NNG 이/JKS 더/MAG 도드라지/VV 어/EC 보이/VV ᆯ/ETM 수/NNB 있/VA 음/EF (/SSO 미용상/NNP )/SSC |
| `/category_specific/1/checks/8/type` | `type` | string | inform | excluded | — |
| `/category_specific/1/checks/9` | `[9]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/1/checks/9/label` | `label` | string | 피부결핵/매독 등 만성감염 여부 | analyzed | 피부/NNG 결핵/NNG //SP 매독/NNG 등/NNB 만성/NNG 감염/NNG 여부/NNG |
| `/category_specific/1/checks/9/type` | `type` | string | must_check | excluded | — |
| `/category_specific/2` | `[2]` | object(자식 3) | keys=['id', 'name', 'checks'] | — | — |
| `/category_specific/2/id` | `id` | string | M3 | excluded | — |
| `/category_specific/2/name` | `name` | string | 바이오스티뮬레이터/콜라겐부스터 | analyzed | 바이오스티뮬레이터/NNP //SP 콜라겐부스터/NNP |
| `/category_specific/2/checks` | `checks` | array(자식 6) |  | — | — |
| `/category_specific/2/checks/0` | `[0]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/2/checks/0/label` | `label` | string | 켈로이드 체질 확인 | analyzed | 켈로이드/NNG 체질/NNG 확인/NNG |
| `/category_specific/2/checks/0/type` | `type` | string | absolute_contraindication | excluded | — |
| `/category_specific/2/checks/1` | `[1]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/2/checks/1/label` | `label` | string | 자가면역질환 여부 (이물반응 위험) | analyzed | 자가/NNG 면역/NNG 질환/NNG 여부/NNG (/SSO 이물/NNG 반응/NNG 위험/NNG )/SSC |
| `/category_specific/2/checks/1/type` | `type` | string | must_check | excluded | — |
| `/category_specific/2/checks/2` | `[2]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/2/checks/2/label` | `label` | string | 이전 바이오스티뮬레이터 시술 이력 및 제품 확인 | analyzed | 이전/NNG 바이오스티뮬레이터/NNG 시술/NNG 이력/NNG 및/MAG 제품/NNG 확인/NNG |
| `/category_specific/2/checks/2/type` | `type` | string | must_check | excluded | — |
| `/category_specific/2/checks/3` | `[3]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/2/checks/3/label` | `label` | string | 결절/육아종 발생 가능성 설명 | analyzed | 결절/NNG //SP 육아종/NNP 발생/NNG 가능/NNG 성/XSN 설명/NNG |
| `/category_specific/2/checks/3/type` | `type` | string | counseling | excluded | — |
| `/category_specific/2/checks/4` | `[4]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/2/checks/4/label` | `label` | string | 효과 발현 시기 안내 (1-3개월 점진적) | analyzed | 효과/NNG 발현/NNG 시기/NNG 안내/NNG (/SSO 1-3/W_SERIAL 개월/NNB 점진/NNG 적/XSN )/SSC |
| `/category_specific/2/checks/4/type` | `type` | string | counseling | excluded | — |
| `/category_specific/2/checks/5` | `[5]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/2/checks/5/label` | `label` | string | 시술 부위 감염/활동성 피부질환 여부 | analyzed | 시술/NNG 부위/NNG 감염/NNG //SP 활동/NNG 성/XSN 피부/NNG 질환/NNG 여부/NNG |
| `/category_specific/2/checks/5/type` | `type` | string | must_check | excluded | — |
| `/category_specific/3` | `[3]` | object(자식 3) | keys=['id', 'name', 'checks'] | — | — |
| `/category_specific/3/id` | `id` | string | M4 | excluded | — |
| `/category_specific/3/name` | `name` | string | 스킨부스터 | analyzed | 스킨부스터/NNG |
| `/category_specific/3/checks` | `checks` | array(자식 5) |  | — | — |
| `/category_specific/3/checks/0` | `[0]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/3/checks/0/label` | `label` | string | HA 성분 알레르기 여부 | analyzed | HA/SL 성분/NNG 알레르기/NNG 여부/NNG |
| `/category_specific/3/checks/0/type` | `type` | string | must_check | excluded | — |
| `/category_specific/3/checks/1` | `[1]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/3/checks/1/label` | `label` | string | 최근 피부 시술 이력 (레이저, 필링 등) | analyzed | 최근/NNG 피부/NNG 시술/NNG 이력/NNG (/SSO 레이저/NNG ,/SP 필링/NNG 등/NNB )/SSC |
| `/category_specific/3/checks/1/type` | `type` | string | must_check | excluded | — |
| `/category_specific/3/checks/2` | `[2]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/3/checks/2/label` | `label` | string | 항응고제/아스피린 복용 여부 (멍 위험) | analyzed | 항응고제/NNP //SP 아스피린/NNP 복용/NNG 여부/NNG (/SSO 멍/NNG 위험/NNG )/SSC |
| `/category_specific/3/checks/2/type` | `type` | string | inform | excluded | — |
| `/category_specific/3/checks/3` | `[3]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/3/checks/3/label` | `label` | string | 시술 부위 활동성 여드름/감염 여부 | analyzed | 시술/NNG 부위/NNG 활동/NNG 성/XSN 여드름/NNG //SP 감염/NNG 여부/NNG |
| `/category_specific/3/checks/3/type` | `type` | string | must_check | excluded | — |
| `/category_specific/3/checks/4` | `[4]` | object(자식 2) | keys=['label', 'type'] | — | — |
| `/category_specific/3/checks/4/label` | `label` | string | 다운타임 안내 (붉어짐, 구진 1-3일) | analyzed | 다운타임/NNP 안내/NNG (/SSO 붉/VA 어/EC 지/VX ᆷ/ETN ,/SP 구/NR 진/NNG 1-3/W_SERIAL 일/NNB )/SSC |
| `/category_specific/3/checks/4/type` | `type` | string | counseling | excluded | — |

## 자동 표현 후보 (정규식 일치분만 — 패턴 밖은 아래 수동 절)

- **AP-NUM-UNIT** (3): `/category_specific/1/checks/8/label`[0,4) «48시간»; `/category_specific/2/checks/4/label`[13,18) «1-3개월»; `/category_specific/3/checks/4/label`[17,21) «1-3일»
- **AP-RANGE** (2): `/category_specific/2/checks/4/label`[13,16) «1-3»; `/category_specific/3/checks/4/label`[17,20) «1-3»
- **AP-PAREN** (14): `/category_specific/0/checks/0/label`[9,19) «(중증근무력증 등)»; `/category_specific/0/checks/2/label`[11,20) «(멍 위험 안내)»; `/category_specific/0/checks/3/label`[16,23) «(항체 내성)»; `/category_specific/0/checks/4/label`[19,51) «(보톡스 효과 증강 위험 — 겐타마이신, 토브라마이신 등)»; `/category_specific/0/checks/5/label`[14,43) «(신경근접합부 기능 감소 — 보톡스 효과 예측 불가)»; `/category_specific/1/checks/1/label`[20,27) «(잔여 필러)»; `/category_specific/1/checks/2/label`[7,17) «(실리콘/PMMA)»; `/category_specific/1/checks/3/label`[10,18) «(육아종 위험)»; `/category_specific/1/checks/8/label`[75,80) «(미용상)»; `/category_specific/2/checks/1/label`[10,19) «(이물반응 위험)»; `/category_specific/2/checks/4/label`[12,23) «(1-3개월 점진적)»; `/category_specific/3/checks/1/label`[12,23) «(레이저, 필링 등)»; `/category_specific/3/checks/2/label`[16,22) «(멍 위험)»; `/category_specific/3/checks/4/label`[8,22) «(붉어짐, 구진 1-3일)»
- **AP-SLASH** (8): `/category_specific/0/checks/6/label`[6,11) «감염/염증»; `/category_specific/1/checks/2/label`[8,16) «실리콘/PMMA»; `/category_specific/1/checks/9/label`[0,7) «피부결핵/매독»; `/category_specific/2/name`[0,16) «바이오스티뮬레이터/콜라겐부스터»; `/category_specific/2/checks/3/label`[0,6) «결절/육아종»; `/category_specific/2/checks/5/label`[6,12) «감염/활동성»; `/category_specific/3/checks/2/label`[0,9) «항응고제/아스피린»; `/category_specific/3/checks/3/label`[10,16) «여드름/감염»
- **AP-DASH** (5): `/category_specific/0/checks/4/label`[33,51) «— 겐타마이신, 토브라마이신 등)»; `/category_specific/0/checks/5/label`[28,43) «— 보톡스 효과 예측 불가)»; `/category_specific/1/checks/2/label`[24,44) «— 이물반응, 합병증 위험 대폭 증가»; `/category_specific/1/checks/7/label`[15,50) «— 구강 내 세균이 혈행성 전파로 필러 감염 경로가 될 수 있음»; `/category_specific/1/checks/8/label`[21,80) «— 기내 기압이 필러를 이동시키지는 않으나, 장시간 비행 시 붓기·멍이 더 도드라져 보일 수 있음(미용상)»
- **AP-ALT** (1): `/category_specific/1/checks/6/label`[3,5) «vs»
- **AP-NEG** (3): `/category_specific/0/checks/5/label`[40,42) «불가»; `/category_specific/1/checks/6/label`[6,7) «비»; `/category_specific/1/checks/8/label`[41,42) «않»
- **AP-POSS** (11): `/category_specific/0/checks/2/label`[14,16) «위험»; `/category_specific/0/checks/4/label`[30,32) «위험»; `/category_specific/0/checks/5/label`[37,42) «예측 불가»; `/category_specific/1/checks/2/label`[36,38) «위험»; `/category_specific/1/checks/3/label`[15,17) «위험»; `/category_specific/1/checks/6/label`[21,23) «가능»; `/category_specific/1/checks/7/label`[46,49) «수 있»; `/category_specific/1/checks/8/label`[71,74) «수 있»; `/category_specific/2/checks/1/label`[16,18) «위험»; `/category_specific/2/checks/3/label`[10,13) «가능성»; `/category_specific/3/checks/2/label`[19,21) «위험»
- **AP-COND** (3): `/category_specific/0/checks/1/label`[14,15) «후»; `/category_specific/1/checks/8/label`[5,7) «이내»; `/category_specific/1/checks/8/label`[52,54) « 시»
- **AP-MODAL** (14): `/category_specific/0/checks/0/label`[20,22) «확인»; `/category_specific/0/checks/2/label`[17,19) «안내»; `/category_specific/0/checks/3/label`[13,15) «확인»; `/category_specific/1/checks/1/label`[17,19) «확인»; `/category_specific/1/checks/4/label`[13,15) «준비»; `/category_specific/1/checks/4/label`[16,18) «확인»; `/category_specific/1/checks/5/label`[15,17) «확인»; `/category_specific/1/checks/6/label`[27,29) «설명»; `/category_specific/1/checks/7/label`[12,14) «확인»; `/category_specific/2/checks/0/label`[8,10) «확인»; `/category_specific/2/checks/2/label`[24,26) «확인»; `/category_specific/2/checks/3/label`[14,16) «설명»; `/category_specific/2/checks/4/label`[9,11) «안내»; `/category_specific/3/checks/4/label`[5,7) «안내»
- **AP-DEGREE** (8): `/category_specific/0/checks/1/label`[16,18) «이상»; `/category_specific/0/checks/3/label`[0,2) «최근»; `/category_specific/1/checks/2/label`[39,41) «대폭»; `/category_specific/1/checks/7/label`[0,2) «최근»; `/category_specific/1/checks/8/label`[46,49) «장시간»; `/category_specific/1/checks/8/label`[61,62) «더»; `/category_specific/2/checks/4/label`[19,22) «점진적»; `/category_specific/3/checks/1/label`[0,2) «최근»
- **AP-ETC** (4): `/category_specific/0/checks/0/label`[16,18) « 등»; `/category_specific/0/checks/4/label`[48,50) « 등»; `/category_specific/1/checks/9/label`[7,9) « 등»; `/category_specific/3/checks/1/label`[20,22) « 등»

## 수동 수집 표현 (직접 읽기 — 원문 구간)

| Pointer | 구간 | 원문 구절 | 탐색 관점(잠정) | 메모 |
|---|---|---|---|---|
| `/category_specific/0/checks/0/label` | [0,22) | 신경근접합부 질환(중증근무력증 등) 확인 | 질환군+괄호 예시, 열린 나열(등) |  |
| `/category_specific/0/checks/1/label` | [0,23) | 이전 보툴리눔 독소 시술 후 이상반응 여부 | 시점(이전·시술 후), 이력 |  |
| `/category_specific/0/checks/2/label` | [0,20) | 항응고제 복용 여부 (멍 위험 안내) | 괄호 목적, 위험, 행위(안내) |  |
| `/category_specific/0/checks/3/label` | [0,23) | 최근 보톡스 시술 시기 확인 (항체 내성) | 시점(최근), 괄호 사유 | '항체 내성' 과 시기 확인의 관계(사유)는 원문에 서술 없음 |
| `/category_specific/0/checks/4/label` | [0,18) | 아미노글리코시드 항생제 복용 여부 | 약물군 |  |
| `/category_specific/0/checks/4/label` | [20,50) | 보톡스 효과 증강 위험 — 겐타마이신, 토브라마이신 등 | 위험, 증강(정도), 괄호 안 줄표, 열린 나열(등) |  |
| `/category_specific/0/checks/5/label` | [0,13) | D-페니실라민 복용 여부 | 약물 |  |
| `/category_specific/0/checks/5/label` | [15,42) | 신경근접합부 기능 감소 — 보톡스 효과 예측 불가 | 감소(정도), 불확실성, 부정(불가) |  |
| `/category_specific/0/checks/6/label` | [0,14) | 시술 부위 감염/염증 여부 | 부위(시술 부위), 슬래시 나열 |  |
| `/category_specific/1/checks/0/label` | [0,16) | 히알루로니다아제 알레르기 여부 | 알레르기 |  |
| `/category_specific/1/checks/1/label` | [0,27) | 이전 필러 시술 부위 및 제품 확인 (잔여 필러) | 시점(이전), 부위, 제품, 괄호 목적 |  |
| `/category_specific/1/checks/2/label` | [0,23) | 잔여 영구필러(실리콘/PMMA) 존재 여부 | 괄호 예시, 슬래시 나열, 영문 약어 |  |
| `/category_specific/1/checks/2/label` | [26,44) | 이물반응, 합병증 위험 대폭 증가 | 위험, 정도(대폭), 증가 |  |
| `/category_specific/1/checks/3/label` | [0,18) | 자가면역질환 여부 (육아종 위험) | 괄호 위험 |  |
| `/category_specific/1/checks/4/label` | [0,18) | 혈관폐색 응급 프로토콜 준비 확인 | 시술자 준비, 응급 |  |
| `/category_specific/1/checks/5/label` | [0,17) | 히알루로니다아제 비상 비치 확인 | 시술자 준비, 비상 |  |
| `/category_specific/1/checks/6/label` | [0,29) | HA vs 비HA 필러 선택 및 용해 가능 여부 설명 | 비교(vs), 부정 접두(비HA), 가능 여부, 행위(설명) |  |
| `/category_specific/1/checks/7/label` | [0,14) | 최근 치과 시술 여부 확인 | 시점(최근), 다른 시술 이력 |  |
| `/category_specific/1/checks/7/label` | [17,50) | 구강 내 세균이 혈행성 전파로 필러 감염 경로가 될 수 있음 | 기전 서술, 가능성(수 있음), 부위(구강 내) |  |
| `/category_specific/1/checks/8/label` | [0,20) | 48시간 이내 비행기 탑승 예정 여부 | 시간(48시간 이내), 예정, 시점 기준 미기재 | 48시간이 시술 전후 어느 쪽 기준인지 원문 없음 |
| `/category_specific/1/checks/8/label` | [23,44) | 기내 기압이 필러를 이동시키지는 않으나 | 부정(않으나), 양보, 오해 반박 |  |
| `/category_specific/1/checks/8/label` | [46,80) | 장시간 비행 시 붓기·멍이 더 도드라져 보일 수 있음(미용상) | 조건(비행 시), 정도(장시간·더), 가능성, 괄호 한정(미용상) |  |
| `/category_specific/1/checks/9/label` | [0,17) | 피부결핵/매독 등 만성감염 여부 | 슬래시 나열, 열린 나열(등), 상위어(만성감염) |  |
| `/category_specific/2/name` | [0,16) | 바이오스티뮬레이터/콜라겐부스터 | 카테고리명 슬래시 | 두 이름이 같은 것인지 대안인지 원문 없음 |
| `/category_specific/2/checks/0/label` | [0,10) | 켈로이드 체질 확인 | 체질 |  |
| `/category_specific/2/checks/1/label` | [0,19) | 자가면역질환 여부 (이물반응 위험) | 괄호 위험 |  |
| `/category_specific/2/checks/2/label` | [0,26) | 이전 바이오스티뮬레이터 시술 이력 및 제품 확인 | 시점(이전), 이력, 제품 |  |
| `/category_specific/2/checks/3/label` | [0,16) | 결절/육아종 발생 가능성 설명 | 슬래시 나열, 가능성, 행위(설명) |  |
| `/category_specific/2/checks/4/label` | [0,23) | 효과 발현 시기 안내 (1-3개월 점진적) | 시간 범위, 형용사(점진적) |  |
| `/category_specific/2/checks/5/label` | [0,20) | 시술 부위 감염/활동성 피부질환 여부 | 부위, 슬래시 나열, 형용사(활동성) |  |
| `/category_specific/3/checks/0/label` | [0,13) | HA 성분 알레르기 여부 | 성분, 영문 약어 |  |
| `/category_specific/3/checks/1/label` | [0,23) | 최근 피부 시술 이력 (레이저, 필링 등) | 시점(최근), 열린 나열(등) |  |
| `/category_specific/3/checks/2/label` | [0,22) | 항응고제/아스피린 복용 여부 (멍 위험) | 슬래시(약물군/개별 약물), 괄호 위험 |  |
| `/category_specific/3/checks/3/label` | [0,19) | 시술 부위 활동성 여드름/감염 여부 | 부위, 형용사(활동성), 슬래시 범위 | '활동성' 이 감염까지 걸리는지 잠정 |
| `/category_specific/3/checks/4/label` | [0,22) | 다운타임 안내 (붉어짐, 구진 1-3일) | 시간 범위, 증상 나열 | '1-3일' 이 붉어짐까지 걸리는지 잠정 |

## 잠정 관찰 (원문 아님 — 근거 위치 포함)

- P: type 분포 — M1 [absolute_contraindication, must_check, inform, must_check×4], M2 [must_check×4, safety_protocol×2, counseling, must_check, inform, must_check], M3 [absolute_contraindication, must_check×2, counseling×2, must_check], M4 [must_check×2, inform, must_check, counseling].
- P: `safety_protocol` 2건(`/category_specific/1/checks/4`·`/5`)은 환자 상태 확인이 아니라 시술자 측 준비 진술이다 — 같은 checks 배열 안에 환자 확인·설명·준비가 섞여 있다.
- P: '항응고제' 확인이 M1 에서는 inform('멍 위험 안내'), M4 에서도 inform('항응고제/아스피린 … 멍 위험'), universal 에서는 must_check. 같은 주제 다른 type.
- P: '켈로이드 체질 확인' 이 M3 에서는 absolute_contraindication(`/category_specific/2/checks/0/type`). 다른 카테고리(M7·M8·M11·M12·M13)에서는 must_check(S03~S05).
- P: `/category_specific/1/checks/8/label` 은 확인 항목이면서 '이동시키지는 않으나' 로 오해를 부정하고 영향을 '(미용상)' 으로 한정한다 — 금기 관계로 읽으면 안 되는 예.
- P: 괄호 안에 줄표가 다시 들어가는 이중 구조: `/category_specific/0/checks/4/label`·`/5/label`.
- P: `/category_specific/3/checks/2/label` '항응고제/아스피린' 은 약물군과 개별 약물을 슬래시로 나란히 둔다(universal 에서 아스피린은 항응고제/항혈소판제의 예시).

## 이 구획의 미결 (A=추출/해석 오류, B=원문 정보 부족, C=사용자 결정 필요, K=분석 한계, P=잠정, F=후속, I=원문 불일치)

- **B-S02-1** [open] '최근' 기간 기준 없음(보톡스·치과·피부 시술) — 위치: `/category_specific/0/checks/3/label`, `/category_specific/1/checks/7/label`, `/category_specific/3/checks/1/label`
- **B-S02-2** [open] '48시간 이내' 의 기준 시점(시술 전/후)이 없음 — 위치: `/category_specific/1/checks/8/label`
- **P-S02-3** [open] '(항체 내성)'·'(잔여 필러)'·'(육아종 위험)' 등 괄호가 사유·목적·예시 중 무엇인지 문법적으로 표시되지 않음 — 잠정 관점 태그만 붙임 — 위치: `/category_specific/0/checks/3/label`, `/category_specific/1/checks/1/label`, `/category_specific/1/checks/3/label`
- **K-S02-4** [recorded] 자동 패턴 AP-DEGREE «이상» 이 '이상반응'(abnormal reaction) 안에서 일치 — 오탐(정도 표현 아님). 자동 후보는 패턴 일치분일 뿐임을 재확인 — 위치: `/category_specific/0/checks/1/label`
- **F-S02-5** [deferred] type 값(must_check·inform·safety_protocol·counseling·absolute_contraindication)이 같은 주제에서 카테고리마다 다르다 — type 의미·용도는 21개 비교 후 설계 과제 — 위치: `/category_specific/0/checks/2/type`, `/category_specific/2/checks/0/type`, `/category_specific/3/checks/2/type`

## 알려진 형태소 오분절 (K — 출현별)

- `/category_specific/0/checks/0/label` «신경근접합부» → 원시 `신경/NNG 근/NNG 접합부/NNG` — 영향: '신경근' 단위가 '신경'+'근' 으로 나뉨 — 의미 손실 작음
- `/category_specific/0/checks/0/label` «중증근무력증» → 원시 `중증 근무력증/NNP` — 영향: kiwi form 에 원문에 없는 공백이 들어감(surface≠form). 구간은 원문 6자를 덮음
- `/category_specific/0/checks/5/label` «D-페니실라민» → 원시 `D/SL -/SO 페니실라민/NNG` — 영향: 약물명이 셋으로 나뉨 — 원문 구절로만 약물명 보존
- `/category_specific/0/checks/5/label` «신경근접합부» → 원시 `신경/NNG 근/NNG 접합부/NNG` — 영향: '신경근' 단위 분리
- `/category_specific/1/checks/1/label` «이전» → 원시 `이/NNP 전/MM` — 영향: 시점어 '이전' 이 고유명사+관형사로 오분석 — 시점 정보가 토큰에서 소실
- `/category_specific/1/checks/2/label` «이물반응» → 원시 `이/MM 물/NNG 반응/NNG` — 영향: '이물'(foreign body) 이 관형사 '이'+'물' 로 오분석 — 위험 대상 소실(같은 단어가 `/universal_checks/2/description` 에서는 이물/NNG)
- `/category_specific/1/checks/7/label` «혈행성» → 원시 `혈/NNG 행/NNG 성/XSN` — 영향: '혈행성' 이 혈/행/성 으로 깨짐
- `/category_specific/1/checks/7/label` «필러» → 원시 `피/VV ᆯ러/EC` — 영향: 시술 대상 명사 '필러' 가 동사 '피-'+어미로 오분석 — 대상 명사 소실(심각)
- `/category_specific/1/checks/8/label` «기압이» → 원시 `기압/NNG 이/MM` — 영향: 주격조사 '이' 가 관형사로 태깅 — 주어 표시 소실
- `/category_specific/2/checks/4/label` «1-3» → 원시 `1-3/W_SERIAL` — 영향: 수치 범위가 일련번호(W_SERIAL) 단일 토큰 — 범위 구조 없음
- `/category_specific/3/checks/4/label` «1-3» → 원시 `1-3/W_SERIAL` — 영향: 수치 범위가 일련번호(W_SERIAL) 단일 토큰
- `/category_specific/3/checks/4/label` «구진» → 원시 `구/NR 진/NNG` — 영향: 증상명 '구진'(papule) 이 수사 '구'+'진' 으로 오분석 — 증상 소실

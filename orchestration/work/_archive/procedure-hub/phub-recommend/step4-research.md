# 실버 4단계(기법) 조사 — 「어떻게」 축

read-only 조사 · 결정 아님. 정본 후보 `step4-research.json`. 생성 2026-10-28.

## ① 결정 묶음 (추천 · 근거 · 영향)

| # | 묶음 | 추천 | 근거 | 영향 |
|---|---|---|---|---|
| S1 | 기법 축 구조 = 안 1(노드 2층 · 나머지 속성) | 큰 기법 12 + 세부 기법 12 노드. 층 · 대상 근육 · 도구 형태 = 단위 시술 속성(키 밖) · 펄스 방식 · 가능 방식 · 박피 여부 · 전극 · 주입기 · 침투 방식 · 실 디자인 = 장비(제품) 속성 | 부위 트리 쪼개기 규칙(10-27 · ① 원천이 따로 부른다 ② 가능 시술 · 안전이 달라진다) 재사용 · 코드 graph domain technique 노드 + uses_technique 단일(unit_procedure.technique_id) · canonical concept_type technique(parent_id 계층) · D-03 「제품 · 장비는 속성」 | 노드 24 · 초안 236행 → 키 199(초안 209) · 사용자 판단 J1 |
| S2 | 큰 기법 12 이름 · 근거 | 주입 · 삽입 · 미세침 천공 · 조사 · 에너지 가열 · 전자기 자극 · 플라즈마 전달 · 냉각 · 도포 · 침투 · 박리·흡인 · 소수술 | procedure-profiles mechanism 12태그 중 전달 태그 9(mechanical · thermal 은 계열별 2노드씩) + 2단계 계열 정의 동사(문헌 기준 · 정본) · 박리·흡인은 2단계 M15 하위 「기계적 박리·클렌징」 · 소수술은 step2 M15 deferred(서브시전 · 펀치 · 압출 → 5단계) 받을 칸 | 노드 12 · 태그 25 판정 |
| S3 | 세부 기법 12 | 주입 › 메조테라피 · 정맥 주사 · 무바늘 제트 주입 / 삽입 › 코그 · 모노 · 볼륨 / 조사 › 토닝 · 프락셔널 · 광역학 / 소수술 › 서브시전 · 펀치 · 압출 | treatment-sequence 「M8-토닝」「M8-프락셔널」 · related_techniques(메조 5 · PDT · 프랙셔널) · DEC-003 D-05 · M4 정의 · 원천 M7-2 · 문헌 33469333 | 노드 12 |
| S4 | 층 · 깊이 = 속성 | 값 사전 13(표피 · 진피 · 피하 · 피하-근막 경계 · Sub-SMAS · 근육 내 · 골막상 · 연골막상 · 심부측두근막 심층 · 점막하 · 정맥 내 · 병변 내 · 피하 지방층) · anatomy safe_injection_depth 11 → (부위 × 주입) `safe_layers` + 제약 원문 | _RESUME 10-28 해부학 결정(층 · 깊이 → 4단계) · 같은 부위에 층 2개(「또는」) 5곳 — 노드로 두면 한 부위 주입이 둘로 갈림 | 값 11행 · 사전 13 |
| S5 | 대상 근육 = 속성 | 값 사전 16(영문 키 · KMA 한글 · 원천 표기 · 붙는 부위) · M1 단위 시술 `target_muscles` · 근육 두께 · 덮임 수치 11 = 근거 속성 | 근육 ↔ 부위가 1:1(3단계 부위 노드가 이미 사각턱 · 잇몸 · 턱선 · 목으로 갈라 줌) — 노드로 두어도 키가 안 늘어남 · 10-28 「부위 이름 2벌」 근육 4 넘김 | 값 11행 + 넘김 4 + DAO 1 · 사전 16 |
| S6 | 에너지 방식 = 장비 속성(technique_hint 25 재확인) | 피코초 · Q스위치(나노초) · 롱펄스 = pulse_mode · 프락셔널 = 가능 방식(→ K04b 와 잇는 조건) · 박피 여부 = 원천 「비박리성」 또는 매질(CO2 · Er:YAG 박피성 · Er:Glass · 톨륨 비박피성) | 펄스 방식은 장비가 내는 것(한 장비가 둘 — 스타워커) · step2 M8 deferred · 문헌 32273965 | 25행 값 · 버림 표현 3 · 원천 수정 후보 1 |
| S7 | 원천 칸 판정(C) | related_techniques 51 · mechanism 25 · group 17 · sequence 19 · anatomy 52 · extracted 17칸(중복) | source-map B03 · B06 · B13 rec 그대로 | 값 181 · open 0 |
| S8 | 계열 기본 기법 18(주 + 보조) | E 표 | 2단계 계열 정의(문헌) 동사 + mechanism | 18행 |
| S9 | 초안 큰 기법 65 대응 | 유지 4 · 합침 29 · 버림(다른 단계/속성) 32 | F 표 | 65행 |
| S10 | 넘겨받은 것 처리 | D 표 14줄 | step2 · step3 · source-map U5 | 14줄 |
| S11 | 원천 충돌 6 · 원천 수정 후보 3 | X1~X6 | 원천 문구 · 허가 모델명 | 충돌 6 · 수정 후보 3 |
| S12 | 열린 OQ 정리 | OQ-201 · OQ-310 · OQ-311 닫힘 · OQ-308 = 5단계 결정론 | 이 조사 | OQ 4 |

## ② 사용자 최종 판단만 (2)

- **J1** 기법 축 구조 — 안 1(추천: 노드 24 · 층 · 근육 · 펄스는 속성) / 안 2(층 · 펄스 · 근육까지 노드 — 노드 56 · 키 약 210) → 추천: 안 1 — 같은 부위 「또는」 층 5곳과 장비마다 다른 펄스가 단위 시술을 쪼개지 않음 · 근육은 부위로 이미 갈림
- **J2** DEC-002 D-02 예시 「HA 필러 · 코 · 피하 주입」을 원천(골막상 · 연골막상)에 맞게 고칠지 → 추천: 고친다 — 「HA 필러 · 코 · 골막상 주입」(예시 문구만 · 결정 내용은 그대로). 고치지 않으면 예시와 원천이 계속 어긋남

## ③ 셈

- 지도 4단계 칸 **27** · 값 **181**(extracted 중복 17칸 = 51줄 포함하면 문자열 215)
- 노드로 **41** · 속성(값 · 근거) **64** · 넘김 **59** · 중복 **17** · **open 0**
- 「근거 원문 + 넘김」처럼 4단계 속성이면서 일부 문구를 다른 단계로 넘기는 행 6 — 속성으로 셈
- 넘김 행선지: 2단계 21 · 5단계 2 · 7단계 1 · 8단계 31 · 계열 밖 3 · 시맨틱 1
- 노드 24(큰 12 · 세부 12) · 값 사전: 층 13 · 펄스 3 · 대상 근육 16 · 박피 2 · 도구 3 · 박피 깊이 3
- technique_hint 25행 → 값 25 · 버림 표현 3 · 원천 수정 후보 1 / 넘겨받은 것 14줄 전부 행선지 / 계열 기본 18 / 초안 65 → 유지 4 · 합침 29 · 버림 32
- 단위 시술 키(초안 236행 기준 추정): 초안 209 → 안 1 **199**(2단계 하위 계열을 키에 넣으면 202) · 안 2 약 210 · 안 3 209
- 원천 충돌 6 · 원천 수정 후보 3 · OQ 닫힘 3(201 · 310 · 311) + 5단계로 1(308)

범위: 지도가 4단계로 정한 칸만 표현을 셌다. 항목 `detail` · `overview` · `mechanism` 문장은 지도상 1 · 3 · 5단계라 셈 밖 — 초안 65 · how 86 은 F 대응표로만 본다.

## A. 기준 근거 (레포 안)

| 무엇 | 어디 | 쓰는 곳 |
|---|---|---|
| 2단계 계열 정의(문헌 기준 · 정본) | `step2-families.json families[].definition` | 큰 기법 = 정의의 전달 동사(주사 · 주입 · 넣어 · 조사 · 가열 · 자극 · 전달 · 냉각 · 바르거나 흡수 · 정맥 투여) |
| procedure-profiles mechanism(17 · 태그 12종) | `procedure-profiles.json profiles[].mechanism` | 전달 태그 9 → 큰 기법 10 · ablative → 속성 · regenerative/regeneration → 기법 아님 |
| 문헌 moa | `literature-evidence.json categories.M8/M9/M7/M12.moa` | M8 박피 · 비박피 프락셔널 · 피코초(32273965 · 38525494) · M9 HIFU 깊이 dermis/SMAS · RF papillary dermis(37753689) · M7 inserted subcutaneously(33469333) · M12 micro-punctures(27559496) |
| 해부 원천 | `anatomy-danger-zones.json safe_injection_depth · botox_specific.target_muscle · tissue_data` | 층 값 · 대상 근육 · 근거 수치 |
| 코드 | `backend/app/modules/graph/domain.py:189-192 · :275-279 · app/model/canonical_catalog.py:32-39` | technique 노드 + uses_technique(단위 시술 → 기법 하나) · canonical concept_type technique 은 parent_id 계층 — 안 1 의 2층 노드와 맞음 |
| 결정 | `_RESUME 10-27 부위 트리 쪼개기 규칙 · D-03 제품 · 장비 = 속성 · 10-28 해부학 결정` | 노드로 세우는 기준 · 장비가 정하는 값은 장비 속성 · 층 · 근육 = 4단계 · 혈관 · 신경 = 8단계 |

2단계처럼 근거가 이미 있다 — **큰 기법 = 2단계 계열 정의(문헌)의 전달 동사 + profiles mechanism 전달 태그**. 새 체계를 짜지 않는다. 세부 노드는 10-27 부위 쪼개기 규칙(① 원천이 따로 부른다 ② 가능 시술 · 안전이 달라진다)을 그대로 쓴다.

## B. 기법 축 구조안

| 안 | 추천 | 무엇 | 노드 | 단위 시술 키(초안 기준) | 장점 | 단점 |
|---|---|---|---|---|---|---|
| 안 1 | **추천** | 큰 기법 12 + 세부 12 노드 · 층 · 대상 근육 · 도구 = 단위 시술 속성(키 밖) · 펄스 · 가능 방식 · 박피 · 전극 · 주입기 · 침투 방식 · 실 디자인 = 장비 속성 | 24 | 199 | 키가 원천이 따로 부르는 것에서만 갈림 · 코드(uses_technique 단일)와 맞음 · 장비가 정하는 값이 장비에 붙음 | technique 노드에 parent 속성 · 단위 시술/장비 속성 칸 추가(SPEC 개정 몫) |
| 안 2 |  | 층 13 · 펄스 3 · 대상 근육 16 까지 하위 노드 | 56 | 약 210(추정) | 층 · 펄스로 바로 질의 가능 | 「또는」 층 5곳(관자놀이 · 팔자 · 입술 · 턱선 · 목)에서 한 시술이 둘로 · M8 토닝 3행 × 펄스 최대 3 → +6 · 근육 노드는 부위와 1:1 이라 키 0 증가인데 노드만 16 |
| 안 3 |  | 초안 그대로(평평한 65) | 65 | 209 | 없음 | 장비 속성(모노폴라) · 하위 계열(IPL · 루비) · 제품 디자인(오메가)이 기법과 섞임 — 2단계 이전 문제 재발 |

안 1 이 초안 키를 줄이는 곳(장비 속성 · 하위 계열로 옮겨서 합쳐짐): `M6|None|None|K01` ← UP-M6-002, UP-M6-003 · `M10|None|바디|K06` ← UP-M10-001, UP-M10-002 · `M12|None|None|K03` ← UP-M12-001, UP-M12-002, UP-M12-003 · `M6|None|얼굴 전체|K01` ← UP-M6-007, UP-M6-010 · `M8|프락셔널|얼굴 전체|K04b` ← UP-M8-008, UP-M8-009 · `M9|RF (고주파)|얼굴 전체|K05` ← UP-M9-004, UP-M9-006 · `M9|RF (고주파)|목|K05` ← UP-M9-007, UP-M9-025, UP-M9-029 · `M9|RF (고주파)|팔뚝|K05` ← UP-M9-023, UP-M9-026 — M6 · M8 프락셔널 3묶음은 2단계 하위 계열(입자 크기 · 매질)을 키에 넣으면 다시 갈린다(+3).

### 노드 24 (안 1)

| id | 이름 | 상위 | 의학 용어(속성) | 근거 |
|---|---|---|---|---|
| K01 | 주입 | — | injection | mechanism injection(M1~M6 · M17) · group 주사/주입 · 계열 정의 「주사」「주입」(M1~M6 · M17 · N1) · DEC-002 D-02 예시 「근육 내 주입」「피하 주입」 |
| K01a | 메조테라피 | 주입 | mesotherapy — 진피 내 미세 다점 주입 | 문헌 M4 이름 「Skinboosters and mesotherapy」 · M4 정의 「진피에 소량씩 여러 점 주입」 · related_techniques 「메조보톡스 — 보톡스를 진피층에 소량 주사」「히알루론산 메조테라피(물광주사)」「메조리프트」「메조페시아」「메조테라피 — 피부에 직접 영양 성분 주입」 · D-02 예시 「진피 내 미세 주입(스킨보톡스)」 |
| K01b | 정맥 주사 | 주입 | intravenous | mechanism intravenous(M16) · M16 정의 「정맥으로 투여」 · DEC-003 D-05 「수액 = 기법 「정맥 주사」」 |
| K01c | 무바늘 제트 주입 | 주입 | needle-free jet injection | M4 정의 「(또는 무바늘 제트 주입)」(39544509 Delivery Methods) · step2 M4 deferred 「주입 기기 → 4단계」 |
| K02 | 삽입 | — | thread insertion | mechanism mechanical(M7) · M7 정의 「실을 피하에 넣어」 · 문헌 33469333 「inserted subcutaneously along a planned course」 |
| K02a | 코그실 삽입 | 삽입 | barbed (cog) thread | 문헌 33469333 「Absorbable barbed threads … mechanically reposition」 · 원천 M7-2 하위 항목 「코그(Cog)」 |
| K02b | 모노실 삽입 | 삽입 | mono (smooth) thread | 원천 M7-2 하위 항목 「모노」 · 문헌 33469333 「Thread insertion stimulates … collagen」(당김 없음) |
| K02c | 볼륨실 삽입 | 삽입 | volume thread | 원천 M7-2 하위 항목 「볼륨실」 |
| K03 | 미세침 천공 | — | microneedling (percutaneous) | mechanism mechanical(M12) · thermal+mechanical(M11) · createsChannel · M11/M12 정의 「미세침 … 찔러 / 미세 천공」 · 문헌 27559496 「micro-punctures」 |
| K04 | 조사 | — | irradiation (laser · IPL · LED) | mechanism thermal · ablative(M8) · M8 정의 「피부에 조사해」 |
| K04a | 토닝 | 조사 | laser toning (low-fluence multi-pass) | treatment-sequence 「M8-토닝」(레이저 단계 안에서 따로 부름) · 원천 항목 레이저토닝 · 피코토닝 · 알렉스토닝 · 제네시스토닝 |
| K04b | 프락셔널 | 조사 | fractional photothermolysis | treatment-sequence 「M8-프락셔널」 · related_techniques 「프랙셔널 레이저」 · 문헌 32273965 「Fractional ablative / Non-ablative fractional lasers」 |
| K04c | 광역학 | 조사 | photodynamic therapy (PDT) | related_techniques 「PDT (광역학요법) — 광감작제 약물 + 레이저」 · 원천 항목 ALA-PDT |
| K05 | 에너지 가열 | — | non-invasive energy heating (HIFU · RF · microwave) | mechanism thermal(M9) · M9 정의 「피부를 뚫지 않고 … 가열」 · 문헌 37753689 HIFU · RF |
| K06 | 전자기 자극 | — | electromagnetic / electrical muscle stimulation | mechanism electromagnetic_stimulation(M10) · M10 정의 |
| K07 | 플라즈마 전달 | — | plasma energy delivery | mechanism plasma_energy(M13) · M13 정의 「피부 표면에 직접 전달」 |
| K08 | 냉각 | — | cooling (cryo) | mechanism cooling(M14) · M14 정의 「냉각해」 |
| K09 | 도포 | — | topical application | mechanism topical(M15) · treatment-sequence 「M15-도포」 · M5 · M17 정의 「주입·도포」 · source-map U5 |
| K10 | 침투 | — | transdermal delivery assist (iontophoresis · electroporation · sonophoresis) | mechanism infusion(M15) · treatment-sequence phase 「약물 도포/침투」 · 2단계 M15 하위 「흡수 보조 기기」 · related 「MTS + 약물 투입 — 경피 흡수 촉진」 |
| K11 | 박리·흡인 | — | mechanical exfoliation · suction | 2단계 M15 하위 「기계적 박리·클렌징」 · treatment-sequence 「M15-클렌징」 |
| K12 | 소수술 | — | minor dermatologic procedure | 2단계 M15 deferred 「서브시전 · 면포압출 · 펀치 → 5단계 시술」 — 단위 시술이 되려면 기법 칸이 있어야 함 |
| K12a | 서브시전 | 소수술 | subcision | 원천 항목 서브시전 detail 「섬유 밴드 절단」 · related 「진피절제주입법(서브시전 + 필러)」 |
| K12b | 펀치 | 소수술 | punch technique | 원천 항목 펀치시술 「펀치이식」 |
| K12c | 압출 | 소수술 | comedone extraction | 원천 항목 면포압출 「압출」 |

### 값 사전 (속성 · 키 밖)

- 층 13: 표피 · 진피 · 피하 · 피하-근막 경계(SMAS 상방) · Sub-SMAS · 근육 내 · 골막상 · 연골막상 · 심부측두근막 심층 · 점막하 · 정맥 내 · 병변 내 · 피하 지방층
- 펄스 방식 3(장비 속성): 피코초 · Q스위치(나노초) · 롱펄스
- 박피 여부: 박피성 · 비박피성(원천 「비박리성」 또는 매질에서 유도) · 박피 깊이: 얕은 · 중간 · 깊은 · 도구 형태: 롤러형 · 스탬프형 · 전동
- 장비 속성 칸: pulse_mode · modes · ablative · electrode(모노폴라 · 바이폴라) · energy(RF · 캐비테이션) · injector(멀티니들) · delivery(이온도입 · 전기천공 · 초음파) · thread_design · suction · cooling
- 단위 시술 속성 칸: safe_layers(+ constraint_text) · target_muscles · landmarks · tool_form · peel_depth · application · evidence

대상 근육 16:

| 키 | KMA 한글 | 원천 표기 | 부위(3단계 노드) | 근거 |
|---|---|---|---|---|
| Frontalis | 이마근(전두근) | 전두근 (Frontalis) | 이마 | zones forehead target_muscle |
| Corrugator supercilii | 눈썹주름근(추미근) | 추미근 (Corrugator supercilii) | 미간 | zones glabella target_muscle |
| Procerus | 눈살근 | 비근근 (Procerus) | 미간 | zones glabella target_muscle — 원천 「비근근」 표기(코 Nasalis 와 같은 표기 · 충돌 X1) |
| Temporalis | 관자근(측두근) | 측두근 (Temporalis) | 관자놀이 | zones temple target_muscle 「이갈이/사각턱 보조」 |
| Orbicularis oculi | 눈둘레근(안륜근) | 안륜근 (Orbicularis oculi) | 눈가 · 눈밑 | zones periorbital target_muscle 「까마귀발, 눈밑 주름」 |
| Nasalis | 코근 | 비근근 (Nasalis) | 코 | zones nose target_muscle 「bunny lines」 — 원천 「비근근」 표기(충돌 X1) |
| Depressor septi nasi | 코중격내림근 | depressor septi nasi | 코끝 | zones nose target_muscle 「코끝 처짐(depressor septi nasi)」 |
| Levator labii superioris | 위입술올림근(상순거근) | 상순거근 (Levator labii superioris) | 팔자 | zones nasolabial target_muscle 「NLF 보조 치료」 |
| Masseter | 깨물근(교근) | 교근 (Masseter) | 사각턱 | zones cheek · jawline target_muscle 「사각턱」 · step3 handoff_note 사각턱 |
| Zygomaticus | 광대근 | 광대근 (Zygomaticus) | 잇몸 | zones cheek target_muscle 「gummy smile」 |
| Orbicularis oris | 입둘레근(구륜근) | 구륜근 (Orbicularis oris) | 입술 · 입가 | zones lips target_muscle 「lip flip, 입가 주름」 |
| Mentalis | 턱끝근(이근) | 이근 (Mentalis) | 턱끝 | zones chin target_muscle 「턱 딤플(peach pit chin)」 |
| Platysma | 넓은목근(광경근) | 광경근 (Platysma) | 턱선 · 목 | zones jawline · neck target_muscle 「턱선 리프트 · platysmal bands, 목 주름」 · step3 handoff_note 목 |
| Depressor anguli oris | 입꼬리내림근(구각하제근) | DAO(구각하제근) | 입꼬리 | zones chin tissue_data.dao_coverage · notes 「DAO 보톡스 시 이신경 손상 주의」 |
| Trapezius | 등세모근 | (원천 이름 칸 「승모근」) | 승모근 | step3 handoff_note 승모근(10-28 부위 이름 2벌 결정) |
| Gastrocnemius | 장딴지근 | (원천 이름 칸 「종아리」) | 종아리 | step3 handoff_note 종아리 |

## C. 원천 표현 전수 (지도 4단계 칸 27 · 값 181)

| 파일 | 키 | 원문 | 수 | 판정 | 행선지 |
|---|---|---|---|---|---|
| anatomy-danger-zones | `zones[forehead].safe_injection_depth` | 골막상층 (supraperiosteal) — 혈관은 표재성이므로 깊은 층이 안전 | 1 | 속성 값 | 4단계 — 단위 시술 속성 `safe_layers`(부위 × 큰 기법 주입 제약 · 키 밖) · 3단계 danger_zone_mapping 으로 부위 노드 「이마」에 대응 |
| anatomy-danger-zones | `zones[glabella].safe_injection_depth` | 골막상층 (supraperiosteal) — 절대 피하층 주사 금지 | 1 | 속성 값 | 4단계 — 단위 시술 속성 `safe_layers`(부위 × 큰 기법 주입 제약 · 키 밖) · 3단계 danger_zone_mapping 으로 부위 노드 「미간」에 대응 |
| anatomy-danger-zones | `zones[temple].safe_injection_depth` | 심부측두근막 심층 (deep temporal fascia deep layer) 또는 골막상 | 1 | 속성 값 | 4단계 — 단위 시술 속성 `safe_layers`(부위 × 큰 기법 주입 제약 · 키 밖) · 3단계 danger_zone_mapping 으로 부위 노드 「관자놀이」에 대응 |
| anatomy-danger-zones | `zones[periorbital].safe_injection_depth` | 안와연(orbital rim) 외측, 골막상 | 1 | 속성 값 | 4단계 — 단위 시술 속성 `safe_layers`(부위 × 큰 기법 주입 제약 · 키 밖) · 3단계 danger_zone_mapping 으로 부위 노드 「눈가(묶음)」에 대응 |
| anatomy-danger-zones | `zones[nose].safe_injection_depth` | 골막상 (코뼈 부위) 또는 연골막상 (비첨부) | 1 | 속성 값 | 4단계 — 단위 시술 속성 `safe_layers`(부위 × 큰 기법 주입 제약 · 키 밖) · 3단계 danger_zone_mapping 으로 부위 노드 「코(묶음)」에 대응 |
| anatomy-danger-zones | `zones[nasolabial].safe_injection_depth` | 피하 또는 피하-근막 경계 (SMAS 상방) | 1 | 속성 값 | 4단계 — 단위 시술 속성 `safe_layers`(부위 × 큰 기법 주입 제약 · 키 밖) · 3단계 danger_zone_mapping 으로 부위 노드 「팔자」에 대응 |
| anatomy-danger-zones | `zones[cheek].safe_injection_depth` | 골막상 (관골부) 또는 피하 (협부), Sub-SMAS 층 주의 | 1 | 속성 값 | 4단계 — 단위 시술 속성 `safe_layers`(부위 × 큰 기법 주입 제약 · 키 밖) · 3단계 danger_zone_mapping 으로 부위 노드 「볼(묶음)」에 대응 |
| anatomy-danger-zones | `zones[lips].safe_injection_depth` | 점막-피부 경계(vermillion border) 진피 내 또는 점막하 | 1 | 속성 값 | 4단계 — 단위 시술 속성 `safe_layers`(부위 × 큰 기법 주입 제약 · 키 밖) · 3단계 danger_zone_mapping 으로 부위 노드 「입술」에 대응 |
| anatomy-danger-zones | `zones[chin].safe_injection_depth` | 골막상 (이부 정중앙) — 이신경공 외측 피할 것 | 1 | 속성 값 | 4단계 — 단위 시술 속성 `safe_layers`(부위 × 큰 기법 주입 제약 · 키 밖) · 3단계 danger_zone_mapping 으로 부위 노드 「턱끝」에 대응 |
| anatomy-danger-zones | `zones[jawline].safe_injection_depth` | 골막상 또는 피하 (하악연 위/아래 구분) | 1 | 속성 값 | 4단계 — 단위 시술 속성 `safe_layers`(부위 × 큰 기법 주입 제약 · 키 밖) · 3단계 danger_zone_mapping 으로 부위 노드 「턱선」에 대응 |
| anatomy-danger-zones | `zones[neck].safe_injection_depth` | 광경근(Platysma) 내 또는 피내 (진피층) | 1 | 속성 값 | 4단계 — 단위 시술 속성 `safe_layers`(부위 × 큰 기법 주입 제약 · 키 밖) · 3단계 danger_zone_mapping 으로 부위 노드 「목(묶음)」에 대응 |
| anatomy-danger-zones | `zones[forehead].botox_specific.target_muscle` | 전두근 (Frontalis) | 1 | 속성 값 | 4단계 — 대상 근육 값 사전(시맨틱 16) · 단위 시술 속성 `target_muscles`(M1 보툴리눔 톡신 × 부위 · 키 밖) |
| anatomy-danger-zones | `zones[glabella].botox_specific.target_muscle` | 추미근 (Corrugator supercilii), 비근근 (Procerus) | 1 | 속성 값 | 4단계 — 대상 근육 값 사전(시맨틱 16) · 단위 시술 속성 `target_muscles`(M1 보툴리눔 톡신 × 부위 · 키 밖) |
| anatomy-danger-zones | `zones[temple].botox_specific.target_muscle` | 측두근 (Temporalis) — 이갈이/사각턱 보조 | 1 | 속성 값 | 4단계 — 대상 근육 값 사전(시맨틱 16) · 단위 시술 속성 `target_muscles`(M1 보툴리눔 톡신 × 부위 · 키 밖) |
| anatomy-danger-zones | `zones[periorbital].botox_specific.target_muscle` | 안륜근 (Orbicularis oculi) — 까마귀발, 눈밑 주름 | 1 | 속성 값 | 4단계 — 대상 근육 값 사전(시맨틱 16) · 단위 시술 속성 `target_muscles`(M1 보툴리눔 톡신 × 부위 · 키 밖) |
| anatomy-danger-zones | `zones[nose].botox_specific.target_muscle` | 비근근 (Nasalis) — bunny lines, 코끝 처짐(depressor septi nasi) | 1 | 속성 값 | 4단계 — 대상 근육 값 사전(시맨틱 16) · 단위 시술 속성 `target_muscles`(M1 보툴리눔 톡신 × 부위 · 키 밖) |
| anatomy-danger-zones | `zones[nasolabial].botox_specific.target_muscle` | 상순거근 (Levator labii superioris) — NLF 보조 치료 | 1 | 속성 값 | 4단계 — 대상 근육 값 사전(시맨틱 16) · 단위 시술 속성 `target_muscles`(M1 보툴리눔 톡신 × 부위 · 키 밖) |
| anatomy-danger-zones | `zones[cheek].botox_specific.target_muscle` | 교근 (Masseter) — 사각턱, 광대근 (Zygomaticus) — gummy smile | 1 | 속성 값 | 4단계 — 대상 근육 값 사전(시맨틱 16) · 단위 시술 속성 `target_muscles`(M1 보툴리눔 톡신 × 부위 · 키 밖) |
| anatomy-danger-zones | `zones[lips].botox_specific.target_muscle` | 구륜근 (Orbicularis oris) — lip flip, 입가 주름 | 1 | 속성 값 | 4단계 — 대상 근육 값 사전(시맨틱 16) · 단위 시술 속성 `target_muscles`(M1 보툴리눔 톡신 × 부위 · 키 밖) |
| anatomy-danger-zones | `zones[chin].botox_specific.target_muscle` | 이근 (Mentalis) — 턱 딤플(peach pit chin) | 1 | 속성 값 | 4단계 — 대상 근육 값 사전(시맨틱 16) · 단위 시술 속성 `target_muscles`(M1 보툴리눔 톡신 × 부위 · 키 밖) |
| anatomy-danger-zones | `zones[jawline].botox_specific.target_muscle` | 교근 (Masseter) — 사각턱, 광경근 (Platysma) — 턱선 리프트 | 1 | 속성 값 | 4단계 — 대상 근육 값 사전(시맨틱 16) · 단위 시술 속성 `target_muscles`(M1 보툴리눔 톡신 × 부위 · 키 밖) |
| anatomy-danger-zones | `zones[neck].botox_specific.target_muscle` | 광경근 (Platysma) — platysmal bands, 목 주름 | 1 | 속성 값 | 4단계 — 대상 근육 값 사전(시맨틱 16) · 단위 시술 속성 `target_muscles`(M1 보툴리눔 톡신 × 부위 · 키 밖) |
| anatomy-danger-zones | `zones[forehead].tissue_data.frontalis_thickness.midpupil_mm` | 1.8 | 1 | 근거 수치 | 4단계 — 근거 속성(`evidence`) — Frontalis |
| anatomy-danger-zones | `zones[forehead].tissue_data.frontalis_thickness.lateral_canthus_mm` | 1.61 | 1 | 근거 수치 | 4단계 — 근거 속성(`evidence`) — Frontalis |
| anatomy-danger-zones | `zones[forehead].tissue_data.frontalis_thickness.lateral_orbital_rim_mm` | 0.11 | 1 | 근거 수치 | 4단계 — 근거 속성(`evidence`) — Frontalis |
| anatomy-danger-zones | `zones[forehead].tissue_data.skin_to_periosteum_mm` | 5.0 | 1 | 근거 수치 | 4단계 — 근거 속성(`evidence`) — layer:골막상@이마 |
| anatomy-danger-zones | `zones[forehead].tissue_data.notes` | 이마 피부-골막 거리 평균 0.5cm — 매우 얇음 | 1 | 근거 원문 | 4단계 — 층 근거(피부-골막 거리) · layer:골막상@이마 |
| anatomy-danger-zones | `zones[glabella].tissue_data.csm_mean_thickness_mm` | 1.62 | 1 | 근거 수치 | 4단계 — 근거 속성(`evidence`) — Corrugator supercilii |
| anatomy-danger-zones | `zones[glabella].tissue_data.csm_thickness_variation_mm` | 0.4 | 1 | 근거 수치 | 4단계 — 근거 속성(`evidence`) — Corrugator supercilii |
| anatomy-danger-zones | `zones[glabella].tissue_data.notes` | 추미근(CSM, corrugator supercilii muscle) 평균 두께 약 1.62±0.4mm. 기존 15mm/21mm 값은 근육 두께로 해부학적으로 성립하지 않아 삭제했으며, 특정 인종 간 두께 차이로 혈관 표재성을 단정할 근거는 불충분 | 1 | 근거 원문 | 4단계 — 대상 근육 근거(추미근 두께 · 삭제 사유 포함) · Corrugator supercilii |
| anatomy-danger-zones | `zones[temple].tissue_data.stl_entry_point` | STL(상측두융합선, Superior temporal line)에서 측두근막이 두 층으로 분리 | 1 | 근거 원문(주입 지표) | 4단계 — 근거 속성(`evidence`) — layer:심부측두근막 심층@관자놀이 |
| anatomy-danger-zones | `zones[temple].tissue_data.notes` | Pitanguy line 위에서 안면신경 측두분지가 표재성으로 주행 — 이 선 위 피하층 주사 주의 | 1 | 넘김 | 8단계 — site_caution 신경(안면신경 측두분지 · Pitanguy line) |
| anatomy-danger-zones | `zones[periorbital].tissue_data.tear_trough_anatomy` | 눈물고랑(tear trough)은 안와연 바로 아래 — 안륜근(orbicularis oculi) 매우 얇음 | 1 | 근거 원문 | 4단계 — 근거 속성(`evidence`) — Orbicularis oculi · layer:골막상@눈밑 |
| anatomy-danger-zones | `zones[periorbital].tissue_data.muscle_fiber_data` | 눈물고랑 부위 안륜근 섬유 두께 0.5-1.0mm (SRA 2024) | 1 | 근거 수치 | 4단계 — 근거 속성(`evidence`) — Orbicularis oculi |
| anatomy-danger-zones | `zones[periorbital].tissue_data.orbital_septum` | 안와격막(orbital septum)은 안와 내용물의 방벽 — 관통 시 안와 내 합병증 | 1 | 근거 원문(관통 금지 지표) + 넘김 | 4단계 — 근거 속성(`evidence`) — layer:골막상@눈가 · 「관통 시 안와 내 합병증」 → 8단계 합병증 참조 |
| anatomy-danger-zones | `zones[periorbital].tissue_data.notes` | 각동맥: 내안각에서 medial 9.0mm, 깊이 2.3mm, 직경 1.7mm (교과서) | 1 | 넘김 | 8단계 — site_caution 혈관(각동맥 위치 · 깊이 · 지름) |
| anatomy-danger-zones | `zones[nose].tissue_data.rhinion_subcutaneous_mm` | 2.02 | 1 | 근거 수치 | 4단계 — 근거 속성(`evidence`) — layer:피하@코 |
| anatomy-danger-zones | `zones[nose].tissue_data.rhinion_data_source` | JCD 2024, USG n=52 | 1 | 근거 출처 | 4단계 — 근거 속성(`evidence`) — layer:피하@코 |
| anatomy-danger-zones | `zones[nose].tissue_data.nasal_tip_skin_thickness_mm` | 1.5 | 1 | 근거 수치 | 4단계 — 근거 속성(`evidence`) — layer:연골막상@코끝 |
| anatomy-danger-zones | `zones[nose].tissue_data.notes` | Rhinion 피하조직 2.02mm (초음파 측정) — 혈관이 매우 표재성 | 1 | 근거 원문 + 넘김 | 4단계 — 층 근거(Rhinion 피하 2.02mm) · 「혈관이 매우 표재성」 → 8단계 site_caution 참조 |
| anatomy-danger-zones | `zones[nasolabial].tissue_data.notes` | 안면동맥 분지가 NLF 인접부에 존재하는 비율은 93.3%이며, 이 중 NLF 5mm 이내 주행은 약 42.9% | 1 | 넘김 | 8단계 — site_caution 혈관(안면동맥 분포 비율) |
| anatomy-danger-zones | `zones[cheek].tissue_data.buccal_fat_pad` | 협지방체(Buccal fat pad): SMAS 심층에 위치, 저작공간까지 연장 | 1 | 근거 원문 | 4단계 — 근거 속성(`evidence`) — layer:Sub-SMAS@볼 |
| anatomy-danger-zones | `zones[cheek].tissue_data.smas_depth_mm` | 4.5 | 1 | 근거 수치 | 4단계 — 근거 속성(`evidence`) — layer:Sub-SMAS@볼 |
| anatomy-danger-zones | `zones[cheek].tissue_data.sub_smas_vs_subcutaneous` | Sub-SMAS: 볼륨 리프팅 / Subcutaneous: 표재성 주름 교정 | 1 | 속성 값 + 넘김 | 4단계 — 근거 속성(`evidence`) — layer:Sub-SMAS · 피하@볼 · 「볼륨 리프팅 / 표재성 주름 교정」 목적 낱말 → 7단계 고민 엣지 근거 |
| anatomy-danger-zones | `zones[cheek].tissue_data.notes` | 협지방체는 관골, 측두, 협부, 익구개 공간에 걸쳐 있음 — 감염 시 파급 위험 | 1 | 넘김 | 8단계 — 합병증(협지방체 감염 파급) |
| anatomy-danger-zones | `zones[lips].tissue_data.notes` | 상순동맥은 대부분 점막하층에 위치(약 58.5%)하고 점막면에서 평균 약 4.5-5.6mm(가장 얕은 경우 약 3.2mm) 깊이로 주행하며 구각(구각에서 0.5cm 이내 유입) 쪽에서 더 깊다. 후방 주행 덕분에 vermillion border의 표재성 진피 내 소량 주입이 가장 안전하 | 1 | 근거 원문 + 넘김 | 4단계 — 층 근거(「vermillion border 표재성 진피 내 소량 주입이 가장 안전」) · 상순동맥 깊이 → 8단계 site_caution |
| anatomy-danger-zones | `zones[chin].tissue_data.dao_coverage` | DAO(구각하제근)의 67.7%가 이신경공을 덮고 있음 | 1 | 근거 원문 + 넘김 | 4단계 — 근거 속성(`evidence`) — Depressor anguli oris · 이신경공 덮임 → 8단계 site_caution(신경) 참조 |
| anatomy-danger-zones | `zones[chin].tissue_data.notes` | 이신경공(Mental foramen): DAO의 67.7%가 덮음 — DAO 보톡스 시 이신경 손상 주의 | 1 | 넘김 | 8단계 — site_caution 신경(이신경공) · DAO 는 C-3 dao_coverage 로 대상 근육 |
| anatomy-danger-zones | `zones[jawline].tissue_data.notes` | 안면동맥: 하악각 부위에서 직경 1.9mm로 가장 굵음 — 하악연 주사 최대 위험 혈관 | 1 | 넘김 | 8단계 — site_caution 혈관(안면동맥 하악각) |
| anatomy-danger-zones | `zones[neck].tissue_data.platysma_thickness_mm` | 1.5 | 1 | 근거 수치 | 4단계 — 근거 속성(`evidence`) — Platysma |
| anatomy-danger-zones | `zones[neck].tissue_data.platysma_coverage` | 광경근은 쇄골~하악연까지, 정중선에서 결손 부위 있음 | 1 | 근거 원문 | 4단계 — 근거 속성(`evidence`) — Platysma |
| anatomy-danger-zones | `zones[neck].tissue_data.notes` | 광경근(Platysma) 하방에 외경정맥 등 주요 혈관 — 광경근 관통 주사 주의 | 1 | 근거 원문 + 넘김 | 4단계 — 층 제약 「광경근 관통 주사 주의」 · 외경정맥 → 8단계 site_caution |
| taxonomy | `modality[M1].extracted.related_techniques` | 메조보톡스 (더모톡신) — 피부 탄력 개선, 리프팅 효과 | 1 | 기법 노드 근거 | 4단계 K01a 메조테라피 — 단위 시술 이름(스킨보톡스 동의어)은 5단계 |
| taxonomy | `modality[M1].extracted.related_techniques` | 에어보톡스 — 여드름 흉터 치료에 활용 | 1 | 기법 노드 근거 | 4단계 K01c 무바늘 제트 주입 — 이름은 5단계(M1 × 흉터 · 고민 7단계) |
| extracted | `M1.related_techniques` | (taxonomy modality[M1] 와 2줄 같음) | 2 | 중복 | taxonomy.json 행으로 셈(중복 제거) — 새 표현 0 |
| taxonomy | `modality[M2].extracted.related_techniques` | 히알루론산 메조테라피 (물광주사) — 피부 속 수분·탄력 개선 | 1 | 기법 노드 근거 | 4단계 K01a 메조테라피 — 「물광주사」 이름은 5단계(M4) |
| taxonomy | `modality[M2].extracted.related_techniques` | 자가지방이식 — 본인 지방으로 볼륨 채움, 알레르기 위험 없음 | 1 | 넘김 | 2단계 계열 M6 (계열 이름 동의어 — 이미 정본) |
| taxonomy | `modality[M2].extracted.related_techniques` | 진피절제주입법 (서브시전 + 필러) — 흉터 치료에 병합 활용 | 1 | 기법 노드 근거 | 4단계 K12a 서브시전 + K01 주입 — 같은 세션 두 단위 시술 조합은 7단계 추천 조합(U3) |
| extracted | `M2.related_techniques` | (taxonomy modality[M2] 와 3줄 같음) | 3 | 중복 | taxonomy.json 행으로 셈(중복 제거) — 새 표현 0 |
| taxonomy | `modality[M3].extracted.related_techniques` | 히알루론산 필러 -- 즉각적 볼륨 효과가 필요할 때 병합 | 1 | 넘김 | 8단계 시술↔시술 관계(병합) — 계열 M2 |
| taxonomy | `modality[M3].extracted.related_techniques` | 보톡스 -- 주름 예방 목적으로 병합 가능 | 1 | 넘김 | 8단계 시술↔시술 관계(병합) — 계열 M1 |
| taxonomy | `modality[M3].extracted.related_techniques` | 고주파(RF) 시술 -- 피부 타이트닝 효과 시너지 | 1 | 넘김 | 8단계 시술↔시술 관계(병합) — 계열 M9 하위 RF |
| extracted | `M3.related_techniques` | (taxonomy modality[M3] 와 3줄 같음) | 3 | 중복 | taxonomy.json 행으로 셈(중복 제거) — 새 표현 0 |
| taxonomy | `modality[M4].extracted.related_techniques` | 메조리프트 (Mesolift) -- 비타민과 히알루론산 주사로 리프팅 효과 | 1 | 기법 노드 근거 | 4단계 K01a 메조테라피 — 이름은 5단계(M4) |
| taxonomy | `modality[M4].extracted.related_techniques` | 메조보톡스 -- 보톡스를 진피층에 소량 주사해 모공/탄력 개선 | 1 | 기법 노드 근거 | 4단계 K01a 메조테라피 — 「보톡스를 진피층에 소량 주사」(층 진피) |
| taxonomy | `modality[M4].extracted.related_techniques` | 메조페시아 (Mesopecia) -- 두피에 약물 주사해 탈모 치료 | 1 | 기법 노드 근거 | 4단계 K01a 메조테라피 — 부위 두피(3단계) · 고민 탈모(7단계) · 이름 5단계 |
| extracted | `M4.related_techniques` | (taxonomy modality[M4] 와 3줄 같음) | 3 | 중복 | taxonomy.json 행으로 셈(중복 제거) — 새 표현 0 |
| taxonomy | `modality[M5].extracted.related_techniques` | MTS + PRP — MTS로 미세 구멍을 낸 후 PRP를 도포해 흡수 촉진 | 1 | 기법 노드 근거 | 4단계 K03 미세침 천공 → K09 도포(채널 후) — 두 단위 시술 순서 조합은 7단계 추천 조합 · 순서는 8단계 |
| taxonomy | `modality[M5].extracted.related_techniques` | 프랙셔널 레이저 + PRP — 레이저 시술 후 PRP를 도포해 재생 효과 증대 | 1 | 기법 노드 근거 | 4단계 K04b 프락셔널 → K09 도포 — 조합은 7단계 · 순서 8단계 |
| taxonomy | `modality[M5].extracted.related_techniques` | 진피절제주입법 + PRP — 여드름흉터에 서브시전 후 PRP 주입 | 1 | 기법 노드 근거 | 4단계 K12a 서브시전 + K01 주입 — 조합은 7단계 |
| extracted | `M5.related_techniques` | (taxonomy modality[M5] 와 3줄 같음) | 3 | 중복 | taxonomy.json 행으로 셈(중복 제거) — 새 표현 0 |
| taxonomy | `modality[M6].extracted.related_techniques` | 히알루론산 필러 -- 소량 볼륨 보정에 간편한 대안 | 1 | 넘김 | 8단계 시술↔시술 관계(병합) — 계열 M2 |
| taxonomy | `modality[M6].extracted.related_techniques` | SVF(기질혈관분획) -- 지방에서 줄기세포를 분리하여 추가 재생 효과 | 1 | 넘김 | 2단계 M17 하위 「세포(SVF)」(이미 정본) · step2 M6 deferred SVF → 5단계 |
| taxonomy | `modality[M6].extracted.related_techniques` | PRP(혈소판풍부혈장) -- 지방이식 시 병합하여 생착률 향상 | 1 | 넘김 | 8단계 시술↔시술 관계(병합) — 계열 M5 |
| extracted | `M6.related_techniques` | (taxonomy modality[M6] 와 3줄 같음) | 3 | 중복 | taxonomy.json 행으로 셈(중복 제거) — 새 표현 0 |
| taxonomy | `modality[M7].extracted.related_techniques` | 필러 -- 볼륨 부족한 부위에 병합 시술 | 1 | 넘김 | 8단계 시술↔시술 관계(병합) — 계열 M2 |
| taxonomy | `modality[M7].extracted.related_techniques` | 보톡스 -- 근육성 주름에 병합 가능 | 1 | 넘김 | 8단계 시술↔시술 관계(병합) — 계열 M1 |
| taxonomy | `modality[M7].extracted.related_techniques` | 고주파(RF)/HIFU -- 피부 타이트닝과 시너지 | 1 | 넘김 | 8단계 시술↔시술 관계(병합) — 계열 M9 |
| extracted | `M7.related_techniques` | (taxonomy modality[M7] 와 3줄 같음) | 3 | 중복 | taxonomy.json 행으로 셈(중복 제거) — 새 표현 0 |
| taxonomy | `modality[M8].extracted.related_techniques` | IPL (Intense Pulsed Light) — 레이저와 비슷하지만 여러 파장의 빛을 동시에 사용 | 1 | 넘김 | 2단계 M8 하위 「IPL」(이미 정본 · 매질) — 기법은 K04 조사 |
| taxonomy | `modality[M8].extracted.related_techniques` | 프랙셔널 레이저 — 기존 박피 레이저의 다운타임을 줄인 최신 기술 | 1 | 기법 노드 근거 | 4단계 K04b 프락셔널 |
| taxonomy | `modality[M8].extracted.related_techniques` | PDT (광역학요법) — 광감작제 약물 + 레이저를 병합한 여드름/피부암 치료 | 1 | 기법 노드 근거 | 4단계 K04c 광역학 |
| extracted | `M8.related_techniques` | (taxonomy modality[M8] 와 3줄 같음) | 3 | 중복 | taxonomy.json 행으로 셈(중복 제거) — 새 표현 0 |
| taxonomy | `modality[M9].extracted.related_techniques` | 실리프팅 -- 물리적 리프팅과 기기 타이트닝 병합 | 1 | 넘김 | 8단계 시술↔시술 관계(병합) — 계열 M7 |
| taxonomy | `modality[M9].extracted.related_techniques` | 보톡스 -- 근육성 주름에 병합 | 1 | 넘김 | 8단계 시술↔시술 관계(병합) — 계열 M1 |
| taxonomy | `modality[M9].extracted.related_techniques` | 필러 -- 볼륨 부족 부위에 병합 | 1 | 넘김 | 8단계 시술↔시술 관계(병합) — 계열 M2 |
| taxonomy | `modality[M9].extracted.related_techniques` | IPL/레이저 -- 색소, 혈관 치료와 병합 시 시너지 | 1 | 넘김 | 8단계 시술↔시술 관계(병합) — 계열 M8 |
| extracted | `M9.related_techniques` | (taxonomy modality[M9] 와 4줄 같음) | 4 | 중복 | taxonomy.json 행으로 셈(중복 제거) — 새 표현 0 |
| taxonomy | `modality[M10].extracted.related_techniques` | 크라이오리포라이시스 (냉동지방분해) -- 지방 감소에 병합 | 1 | 넘김 | 8단계 시술↔시술 관계(병합) — 계열 M14 |
| taxonomy | `modality[M10].extracted.related_techniques` | 고주파(RF) 바디 -- 피부 타이트닝과 시너지 | 1 | 넘김 | 8단계 시술↔시술 관계(병합) — 계열 M9 × 바디(3단계) |
| taxonomy | `modality[M10].extracted.related_techniques` | 지방흡입 -- 더 적극적인 지방 제거가 필요한 경우 | 1 | 넘김 | 계열 밖(수술) — 8단계 「대신」 관계 원문(synergy 「대신」 B06 ④ 와 같은 처리) |
| extracted | `M10.related_techniques` | (taxonomy modality[M10] 와 3줄 같음) | 3 | 중복 | taxonomy.json 행으로 셈(중복 제거) — 새 표현 0 |
| taxonomy | `modality[M11].extracted.related_techniques` | 프랙셔널 레이저 -- 비슷한 피부 재생 원리이나 표피 손상이 더 큼 | 1 | 기법 노드 근거 | 4단계 K04b 프락셔널 |
| taxonomy | `modality[M11].extracted.related_techniques` | 일반 고주파(RF) -- 비침습적 타이트닝 | 1 | 넘김 | 8단계 시술↔시술 관계(비교) — 계열 M9 하위 RF |
| taxonomy | `modality[M11].extracted.related_techniques` | MTS(마이크로니들링) -- RF 없이 물리적 자극만으로 콜라겐 유도 | 1 | 넘김 | 8단계 시술↔시술 관계(병합 · 비교) — 계열 M12 · 기법 K03 |
| extracted | `M11.related_techniques` | (taxonomy modality[M11] 와 3줄 같음) | 3 | 중복 | taxonomy.json 행으로 셈(중복 제거) — 새 표현 0 |
| taxonomy | `modality[M12].extracted.related_techniques` | MTS + PRP — 미세 구멍 후 PRP 도포로 피부 재생 효과 극대화 | 1 | 기법 노드 근거 | 4단계 K03 미세침 천공 → K09 도포(채널 후) — 두 단위 시술 순서 조합은 7단계 추천 조합 · 순서는 8단계 |
| taxonomy | `modality[M12].extracted.related_techniques` | MTS + 약물 투입 — 비타민C, 히알루론산 등 유효 성분 경피 흡수 촉진 | 1 | 기법 노드 근거 | 4단계 K10 침투(「경피 흡수 촉진」) — 채널 후 침투는 U5 가드 대상 |
| taxonomy | `modality[M12].extracted.related_techniques` | 프랙셔널 레이저 — 비슷한 원리(미세 열손상 → 재생)이지만 레이저 에너지 사용 | 1 | 기법 노드 근거 | 4단계 K04b 프락셔널 |
| extracted | `M12.related_techniques` | (taxonomy modality[M12] 와 3줄 같음) | 3 | 중복 | taxonomy.json 행으로 셈(중복 제거) — 새 표현 0 |
| taxonomy | `modality[M13].extracted.related_techniques` | 메디컬스킨케어(필링) -- 병합 시 약물 흡수율 향상 | 1 | 넘김 | 8단계 시술↔시술 관계(병합) — 계열 M15 하위 화학 박피 |
| taxonomy | `modality[M13].extracted.related_techniques` | 레이저 토닝 -- 색소 치료와 병합 | 1 | 기법 노드 근거 | 4단계 K04a 토닝 |
| taxonomy | `modality[M13].extracted.related_techniques` | MTS(마이크로니들링) -- 피부 재생 시너지 | 1 | 넘김 | 8단계 시술↔시술 관계(병합 · 비교) — 계열 M12 · 기법 K03 |
| extracted | `M13.related_techniques` | (taxonomy modality[M13] 와 3줄 같음) | 3 | 중복 | taxonomy.json 행으로 셈(중복 제거) — 새 표현 0 |
| taxonomy | `modality[M14].extracted.related_techniques` | HIFES/EMS -- 근육 강화와 병합하여 바디 윤곽 개선 | 1 | 넘김 | 8단계 시술↔시술 관계(병합) — 계열 M10 |
| taxonomy | `modality[M14].extracted.related_techniques` | 고주파(RF) 바디 -- 피부 타이트닝과 시너지 | 1 | 넘김 | 8단계 시술↔시술 관계(병합) — 계열 M9 × 바디(3단계) |
| taxonomy | `modality[M14].extracted.related_techniques` | 지방흡입 -- 더 적극적인 지방 제거가 필요한 경우 | 1 | 넘김 | 계열 밖(수술) — 8단계 「대신」 관계 원문(synergy 「대신」 B06 ④ 와 같은 처리) |
| extracted | `M14.related_techniques` | (taxonomy modality[M14] 와 3줄 같음) | 3 | 중복 | taxonomy.json 행으로 셈(중복 제거) — 새 표현 0 |
| taxonomy | `modality[M15].extracted.related_techniques` | MTS(마이크로니들링) -- 물리적 자극으로 피부 재생 유도 | 1 | 넘김 | 8단계 시술↔시술 관계(병합 · 비교) — 계열 M12 · 기법 K03 |
| taxonomy | `modality[M15].extracted.related_techniques` | 레이저토닝 -- 기미/색소 치료에 병합 | 1 | 기법 노드 근거 | 4단계 K04a 토닝 |
| taxonomy | `modality[M15].extracted.related_techniques` | LDM(초음파) -- 피부 진정 및 재생 시너지 | 1 | 넘김 | 8단계 시술↔시술 관계(병합) — 1단계 제품 LDM(M15 흡수 보조 · 기법 K10) |
| extracted | `M15.related_techniques` | (taxonomy modality[M15] 와 3줄 같음) | 3 | 중복 | taxonomy.json 행으로 셈(중복 제거) — 새 표현 0 |
| taxonomy | `modality[M16].extracted.related_techniques` | 메조테라피 -- 피부에 직접 영양 성분 주입 | 1 | 기법 노드 근거 | 4단계 K01a 메조테라피 |
| taxonomy | `modality[M16].extracted.related_techniques` | PRP(혈소판풍부혈장) -- 자가 혈액 활용 재생 치료 | 1 | 넘김 | 8단계 시술↔시술 관계(병합) — 계열 M5 |
| taxonomy | `modality[M16].extracted.related_techniques` | 경구 영양제 -- 유지 요법으로 병행 | 1 | 넘김 | 계열 밖(경구) — 8단계 관계 원문(유지 요법) |
| extracted | `M16.related_techniques` | (taxonomy modality[M16] 와 3줄 같음) | 3 | 중복 | taxonomy.json 행으로 셈(중복 제거) — 새 표현 0 |
| taxonomy | `modality[M17].extracted.related_techniques` | 자가지방이식 — 줄기세포 없이 지방만 이식하는 기존 방법 | 1 | 넘김 | 2단계 계열 M6 (계열 이름 동의어 — 이미 정본) |
| taxonomy | `modality[M17].extracted.related_techniques` | SVF(기질혈관분획) 치료법 — 지방에서 추출한 줄기세포 혼합물 이식 | 1 | 넘김 | 2단계 M17 하위 「세포(SVF)」(이미 정본) |
| taxonomy | `modality[M17].extracted.related_techniques` | 줄기세포 배양액(AAPE) — 줄기세포가 분비한 성장인자 단백질을 이용한 치료 | 1 | 넘김 | 2단계 M17 하위 「배양액·추출물」 · 1단계 제품 AAPE(이미 정본) |
| extracted | `M17.related_techniques` | (taxonomy modality[M17] 와 3줄 같음) | 3 | 중복 | taxonomy.json 행으로 셈(중복 제거) — 새 표현 0 |
| procedure-profiles | `profiles[M1].mechanism` | injection | 1 | 기법 노드 | K01 주입(큰 기법) |
| procedure-profiles | `profiles[M2].mechanism` | injection | 1 | 기법 노드 | K01 주입(큰 기법) |
| procedure-profiles | `profiles[M3].mechanism` | injection | 1 | 기법 노드 | K01 주입(큰 기법) |
| procedure-profiles | `profiles[M3].mechanism` | regenerative | 1 | 넘김 | 작용(효과) 태그 — 기법 아님 → 2단계 계열 정의(문헌 moa) 대조 · 8단계 근거 |
| procedure-profiles | `profiles[M4].mechanism` | injection | 1 | 기법 노드 | K01 주입(큰 기법) |
| procedure-profiles | `profiles[M4].mechanism` | regenerative | 1 | 넘김 | 작용(효과) 태그 — 기법 아님 → 2단계 계열 정의(문헌 moa) 대조 · 8단계 근거 |
| procedure-profiles | `profiles[M5].mechanism` | injection | 1 | 기법 노드 | K01 주입(큰 기법) |
| procedure-profiles | `profiles[M5].mechanism` | regenerative | 1 | 넘김 | 작용(효과) 태그 — 기법 아님 → 2단계 계열 정의(문헌 moa) 대조 · 8단계 근거 |
| procedure-profiles | `profiles[M6].mechanism` | injection | 1 | 기법 노드 | K01 주입(큰 기법) |
| procedure-profiles | `profiles[M6].mechanism` | regenerative | 1 | 넘김 | 작용(효과) 태그 — 기법 아님 → 2단계 계열 정의(문헌 moa) 대조 · 8단계 근거 |
| procedure-profiles | `profiles[M7].mechanism` | mechanical | 1 | 기법 노드 | K02 삽입 |
| procedure-profiles | `profiles[M8].mechanism` | thermal | 1 | 기법 노드 | K04 조사 |
| procedure-profiles | `profiles[M8].mechanism` | ablative | 1 | 속성 값 | 4단계 — 속성 `ablative` 값 「박피성」(M8 · 매질 CO2 · Er:YAG 에서 유도 — 문헌 32273965) |
| procedure-profiles | `profiles[M9].mechanism` | thermal | 1 | 기법 노드 | K05 에너지 가열 |
| procedure-profiles | `profiles[M11].mechanism` | thermal | 1 | 기법 노드 | K03 미세침 천공 — M11 은 미세침 + 고주파 에너지(장비 속성 `energy` = RF) |
| procedure-profiles | `profiles[M11].mechanism` | mechanical | 1 | 기법 노드 | K03 미세침 천공 — M11 은 미세침 + 고주파 에너지(장비 속성 `energy` = RF) |
| procedure-profiles | `profiles[M12].mechanism` | mechanical | 1 | 기법 노드 | K03 미세침 천공 |
| procedure-profiles | `profiles[M10].mechanism` | electromagnetic_stimulation | 1 | 기법 노드 | K06 전자기 자극 |
| procedure-profiles | `profiles[M13].mechanism` | plasma_energy | 1 | 기법 노드 | K07 플라즈마 전달 |
| procedure-profiles | `profiles[M14].mechanism` | cooling | 1 | 기법 노드 | K08 냉각 |
| procedure-profiles | `profiles[M15].mechanism` | topical | 1 | 기법 노드 | K09 도포 |
| procedure-profiles | `profiles[M15].mechanism` | infusion | 1 | 기법 노드 | K10 침투 — M15 하위 「흡수 보조 기기」 |
| procedure-profiles | `profiles[M16].mechanism` | intravenous | 1 | 기법 노드 | K01b 정맥 주사 |
| procedure-profiles | `profiles[M17].mechanism` | injection | 1 | 기법 노드 | K01 주입(큰 기법) |
| procedure-profiles | `profiles[M17].mechanism` | regeneration | 1 | 넘김 | 「regenerative」 표기 변형 → 시맨틱 정규화(같은 값) 후 같은 행선지 |
| taxonomy | `modality[M1].group` | 주사/주입 | 1 | 속성 값 | 2단계 계열 속성 `group`(메뉴 묶음 원문 · 표시용) — 기법 노드 아님 · 2단계 정본은 고치지 않고 4단계 반영 때 속성만 더함 |
| taxonomy | `modality[M2].group` | 주사/주입 | 1 | 속성 값 | 2단계 계열 속성 `group`(메뉴 묶음 원문 · 표시용) — 기법 노드 아님 · 2단계 정본은 고치지 않고 4단계 반영 때 속성만 더함 |
| taxonomy | `modality[M3].group` | 주사/주입 | 1 | 속성 값 | 2단계 계열 속성 `group`(메뉴 묶음 원문 · 표시용) — 기법 노드 아님 · 2단계 정본은 고치지 않고 4단계 반영 때 속성만 더함 |
| taxonomy | `modality[M4].group` | 주사/주입 | 1 | 속성 값 | 2단계 계열 속성 `group`(메뉴 묶음 원문 · 표시용) — 기법 노드 아님 · 2단계 정본은 고치지 않고 4단계 반영 때 속성만 더함 |
| taxonomy | `modality[M5].group` | 주사/주입 | 1 | 속성 값 | 2단계 계열 속성 `group`(메뉴 묶음 원문 · 표시용) — 기법 노드 아님 · 2단계 정본은 고치지 않고 4단계 반영 때 속성만 더함 |
| taxonomy | `modality[M6].group` | 주사/주입 | 1 | 속성 값 | 2단계 계열 속성 `group`(메뉴 묶음 원문 · 표시용) — 기법 노드 아님 · 2단계 정본은 고치지 않고 4단계 반영 때 속성만 더함 |
| taxonomy | `modality[M7].group` | 시술/기기 | 1 | 속성 값 | 2단계 계열 속성 `group`(메뉴 묶음 원문 · 표시용) — 기법 노드 아님 · 2단계 정본은 고치지 않고 4단계 반영 때 속성만 더함 — group 「시술/기기」 ↔ mechanism mechanical · 정의 「실을 넣어」(삽입) |
| taxonomy | `modality[M8].group` | 시술/기기 | 1 | 속성 값 | 2단계 계열 속성 `group`(메뉴 묶음 원문 · 표시용) — 기법 노드 아님 · 2단계 정본은 고치지 않고 4단계 반영 때 속성만 더함 |
| taxonomy | `modality[M9].group` | 시술/기기 | 1 | 속성 값 | 2단계 계열 속성 `group`(메뉴 묶음 원문 · 표시용) — 기법 노드 아님 · 2단계 정본은 고치지 않고 4단계 반영 때 속성만 더함 |
| taxonomy | `modality[M10].group` | 시술/기기 | 1 | 속성 값 | 2단계 계열 속성 `group`(메뉴 묶음 원문 · 표시용) — 기법 노드 아님 · 2단계 정본은 고치지 않고 4단계 반영 때 속성만 더함 |
| taxonomy | `modality[M11].group` | 시술/기기 | 1 | 속성 값 | 2단계 계열 속성 `group`(메뉴 묶음 원문 · 표시용) — 기법 노드 아님 · 2단계 정본은 고치지 않고 4단계 반영 때 속성만 더함 |
| taxonomy | `modality[M12].group` | 시술/기기 | 1 | 속성 값 | 2단계 계열 속성 `group`(메뉴 묶음 원문 · 표시용) — 기법 노드 아님 · 2단계 정본은 고치지 않고 4단계 반영 때 속성만 더함 |
| taxonomy | `modality[M13].group` | 시술/기기 | 1 | 속성 값 | 2단계 계열 속성 `group`(메뉴 묶음 원문 · 표시용) — 기법 노드 아님 · 2단계 정본은 고치지 않고 4단계 반영 때 속성만 더함 |
| taxonomy | `modality[M14].group` | 시술/기기 | 1 | 속성 값 | 2단계 계열 속성 `group`(메뉴 묶음 원문 · 표시용) — 기법 노드 아님 · 2단계 정본은 고치지 않고 4단계 반영 때 속성만 더함 |
| taxonomy | `modality[M15].group` | 관리 | 1 | 속성 값 | 2단계 계열 속성 `group`(메뉴 묶음 원문 · 표시용) — 기법 노드 아님 · 2단계 정본은 고치지 않고 4단계 반영 때 속성만 더함 |
| taxonomy | `modality[M16].group` | 관리 | 1 | 속성 값 | 2단계 계열 속성 `group`(메뉴 묶음 원문 · 표시용) — 기법 노드 아님 · 2단계 정본은 고치지 않고 4단계 반영 때 속성만 더함 — group 「관리」 ↔ mechanism intravenous |
| taxonomy | `modality[M17].group` | 관리 | 1 | 속성 값 | 2단계 계열 속성 `group`(메뉴 묶음 원문 · 표시용) — 기법 노드 아님 · 2단계 정본은 고치지 않고 4단계 반영 때 속성만 더함 — group 「관리」 ↔ mechanism injection |
| treatment-sequence | `sequence_order[1].categories` | M15-클렌징 | 1 | 넘김 | 8단계 세션 단계(순서 원문) — 단위 시술 아님(source-map B06 rec) · 기법은 K11 박리·흡인 |
| treatment-sequence | `sequence_order[2].categories` | 국소마취 | 1 | 넘김 | 5단계 단위 시술 운영 속성 `anesthesia` 값(profiles needsAnesthesia 와 같은 칸) — 단위 시술 아님 |
| treatment-sequence | `sequence_order[2].categories` | 연고마취 | 1 | 넘김 | 5단계 단위 시술 운영 속성 `anesthesia` 값 — 단위 시술 아님 |
| treatment-sequence | `sequence_order[3].categories` | M9-HIFU | 1 | 넘김 | 2단계 M9 하위 「HIFU」 → 순서 주장 `conditions.sub` |
| treatment-sequence | `sequence_order[3].categories` | M9-RF | 1 | 넘김 | 2단계 M9 하위 「RF」 → 순서 주장 `conditions.sub` |
| treatment-sequence | `sequence_order[3].categories` | M8-IPL | 1 | 넘김 | 2단계 M8 하위 「IPL」 → 순서 주장 `conditions.sub` |
| treatment-sequence | `sequence_order[4].categories` | M8-토닝 | 1 | 기법 노드 | 4단계 K04a 토닝 → 순서 주장 `conditions.technique` |
| treatment-sequence | `sequence_order[4].categories` | M8-프락셔널 | 1 | 기법 노드 | 4단계 K04b 프락셔널 → 순서 주장 `conditions.technique` |
| treatment-sequence | `sequence_order[4].categories` | M8-혈관 | 1 | 넘김 | 7단계 목적(혈관) — step2 M8 deferred 「M8-4 혈관 → 목적」 · 순서 주장 조건은 목적 |
| treatment-sequence | `sequence_order[5].categories` | M11 | 1 | 넘김 | 2단계 계열(이미 정본) |
| treatment-sequence | `sequence_order[5].categories` | M12 | 1 | 넘김 | 2단계 계열(이미 정본) |
| treatment-sequence | `sequence_order[6].categories` | M2 | 1 | 넘김 | 2단계 계열(이미 정본) |
| treatment-sequence | `sequence_order[6].categories` | M3 | 1 | 넘김 | 2단계 계열(이미 정본) |
| treatment-sequence | `sequence_order[7].categories` | M4 | 1 | 넘김 | 2단계 계열(이미 정본) |
| treatment-sequence | `sequence_order[8].categories` | M1 | 1 | 넘김 | 2단계 계열(이미 정본) |
| treatment-sequence | `sequence_order[9].categories` | M5 | 1 | 넘김 | 2단계 계열(이미 정본) |
| treatment-sequence | `sequence_order[10].categories` | M15-도포 | 1 | 기법 노드 | 4단계 K09 도포 → 순서 주장 `conditions.technique` · 이 단계 reason(화장품 엑소좀 채널 내 도포 금지)은 U5 가드 근거 |
| treatment-sequence | `sequence_order[11].categories` | M15-LED | 1 | 넘김 | 2단계 M8 하위 「LED」(D04 로 M8 편입 — 원천 「M15-」 접두는 옛 자리) → 순서 주장 `conditions.sub` |
| treatment-sequence | `sequence_order[11].categories` | M15-팩 | 1 | 넘김 | 8단계 세션 단계(진정/마무리 원문) — 단위 시술 아님(B06 rec) · step2 M15 deferred 「도포/팩 → 6단계 해체」 |

붙지 않는 것: **0** — 모든 값이 노드 · 속성 · 넘김(행선지 있음) · 중복 중 하나.

## D. 넘겨받은 것

| 출처 | 항목 | 행선지 |
|---|---|---|
| step3 deferred | 진피(6) — taxonomy 하위 이름 「무세포동종진피(hADM)」(재료 이름) · problem-packages cc_detail 「진피색소」「진피 타이트닝」 · 항목 detail 「미녹시딜 진피 주입」 | 「무세포동종진피」 = 2단계 하위 계열 이름(이미 정본 · 층 아님) / 「진피색소」 = 7단계 고민(병변 깊이) / 「진피 타이트닝」 = 7단계 고민 · 목적 / 「진피 주입」 = 층 값 「진피」 + K01a 메조테라피(5단계 미녹시딜 두피 메조 단위 시술) |
| step3 deferred | 표피(1) — 탄앤막필링 detail 「TAN(표피재생)」 | 7단계 목적(표피 재생) — 층 값 아님(효과 낱말) |
| step3 deferred | 피하(1) — 카복시테라피 detail 「CO2 가스 피하주입」 | 층 값 「피하」 + K01 주입 — 5단계 카복시 단위 시술(계열은 step2 D 「카복시 N2 세우지 않음」 그대로) |
| step3 compound | 네페르티티 리프트(턱선 · 목 각 2문자열) — auto-3 「목주름/턱선(네페르티티 리프트)」 · DEC-002 D-03 표 OQ-201 「이름 있는 기법인지 상담 용어인지」 | 기법 노드 아님 → 상담 용어 = 5단계 단위 시술 이름(M1 × 턱선 · 목) · 기법 = K01 주입(근육 내) · 대상 근육 Platysma(원천 zones jawline 「광경근 — 턱선 리프트」 · neck 「platysmal bands」). OQ-201 의 이 물음은 닫힘 |
| step3 handoff_note | 사각턱 — 깨물근 · 아래턱뼈각 | 대상 근육 Masseter(M1 × 사각턱) · 「아래턱뼈각」 = 주입 지표 근거(`landmarks` 원문) |
| step3 handoff_note | 목 — 넓은목근 | 대상 근육 Platysma(M1 × 목) |
| step3 handoff_note | 승모근 — 등세모근 | 대상 근육 Trapezius(M1 × 승모근) |
| step3 handoff_note | 종아리 — 장딴지근 | 대상 근육 Gastrocnemius(M1 × 종아리) |
| step3 handoff_note | 턱선 — 아래턱뼈 아래모서리(mandibular border) | 주입 지표 근거(`landmarks` 원문) — zones jawline safe_injection_depth 「하악연 위/아래 구분」과 같은 지표 |
| step2 M8 deferred | 방식(피코초 · 프락셔널 · 롱펄스 · Q스위치 …) + 원천 하위 M8-2 「프락셔널」 · 「피코초(Picosecond)」 | 프락셔널 = 세부 기법 노드 K04b · 피코초 · Q스위치 · 롱펄스 = 장비(제품) 속성 `pulse_mode` — 하위 이름 「피코초(Picosecond)」는 제품 3행(피코플러스 · 디스커버리 피코 · 엔라이튼)의 pulse_mode 로 |
| step2 technique_hint | 25행 | 행마다 재확인(hints 표) — 값 25행 전부 · 버림 표현 3(피코코어 나노초 · 스타워커 피코나노 · 클라리티2 Q-switched) · 원천 수정 후보 1(M8-P-3 설명) |
| step2 M4 deferred | 주입 기기(원천 M15-6 주입장비 · 물광/메조건) | 기기는 1단계 제품(정본) · 「어떻게」 = K01a 메조테라피(멀티니들 자동 주입 — 장비 속성 `injector` = 멀티니들) / K01c 무바늘 제트 주입(니들리스 · 공기압 · 제트) / K10 침투(초음파 주입 벨라소닉 · 옥시덤) |
| source-map U5 | 도포 제약 — ASCE+ · EXOSOME SKIN(화장품 허가) | 4단계는 기법 노드만 준다: 이 두 제품의 uses_product 는 K09 도포(온전한 피부)만 · K01 주입 · K10 침투(채널 경유) 금지 — 근거 products legal_warning(2) + treatment-sequence order 10 reason 「화장품 분류 엑소좀 · 배양액의 채널 내 도포는 금지」. 가드 적용은 5단계(지도 5) |
| step2 셀렉V · BBL 히어로 open 사유 | 허가 ↔ 원천 매질 충돌(v3 W-b) | 기법은 둘 다 K04 조사 — 매질 충돌은 기법 값을 바꾸지 않음. 셀렉V 펄스 방식은 보조 매질에만(hints 표) · BBL 히어로 hint 없음 |

### technique_hint 25 재확인 (원천 문맥 다시 읽음)

| ledger_id | 이름 | 하위 계열 | hint(그대로) | pulse_mode | 가능 방식 | 박피 | 버림 | 메모 |
|---|---|---|---|---|---|---|---|---|
| `M8-1-3` | 피코슈어 | 알렉산드라이트 레이저 | 프락셔널 · 피코초 | 피코초 | 프락셔널 | — | — | 프락셔널 = 「Focus Lens Array로 프락셔널 효과도 제공」 — 렌즈로 되는 가능 방식(mode) |
| `auto-M8-1775361386532` | 레블라이트 SI | 엔디야그 레이저 | Q-switched · 나노초 · 큐스위치 | Q스위치(나노초) | — | — | — |  |
| `auto-M8-1775361394023` | 피코케어 | 엔디야그 레이저 | 피코초 | 피코초 | — | — | — |  |
| `auto-M8-1775362587235` | 피코코어 | 엔디야그 레이저 | 나노초 · 피코초 | 피코초 | — | — | 나노초: 비교 문장 「기존 나노초 레이저 대비」(step2 v3 W-a) |  |
| `auto-M8-1775362943490` | 트루피코 | 엔디야그 레이저 | Q-switched | Q스위치(나노초) | — | — | — | 값은 원천 설명 「Q-switched 기술」 그대로 · 1단계 확인 불가 · step2 근거 약(실제 장비명 질문) 그대로 따라감 — 새 질문 없음 |
| `auto-M8-1775362951135` | 리레이저 | 엔디야그 레이저 | Q-switched | Q스위치(나노초) | — | — | — |  |
| `auto-M8-1775364775120` | 스타워커 | 엔디야그 레이저 | 나노초 · 피코나노 · 피코초 | Q스위치(나노초) · 피코초 | — | — | 피코나노: 기술 이름(「포토나 피코나노 기술」) — 값은 「나노초 펄스와 피코초 펄스를 결합」에서 둘 다 |  |
| `M8-2-4` | 프락셀 듀얼 | Er:Glass | 비박리성 · 비박피 · 프락셔널 | — | 프락셔널 | 비박피성 | — |  |
| `auto-M8-1775361850481` | 모자이크 | Er:Glass | 비박리성 · 프락셔널 | — | 프락셔널 | 비박피성 | — |  |
| `auto-M8-1775362603297` | 에코2 | 탄산가스 레이저 | 프락셔널 · 프랙셔널 | — | 프락셔널 | 박피성(매질 유도) | — | 박피성은 매질 탄산가스에서 유도(문헌 32273965 「Ablative CO2」) |
| `auto-M8-1775364106103` | 셀렉V | IPL | Q-switched | Q스위치(나노초) | — | — | — | Q스위치는 원천 설명의 Nd:YAG 에 붙음 → 2단계 보조 하위 계열 「엔디야그 레이저」 쪽 장비 속성으로 한정(주 IPL 에는 펄스 방식 없음) · 허가 ↔ 원천 매질 충돌은 step2 conflict 그대로 |
| `auto-M8-1775364775119` | 에코2 에볼루션 | 탄산가스 레이저 | 프락셔널 | — | 프락셔널 | 박피성(매질 유도) | — | 프락셔널 = 원천 하위 이름 「프락셔널」(M8-2)에서 · 박피성은 매질 탄산가스에서 유도 |
| `auto-M8-1775364775129` | 울트라펄스 | 탄산가스 레이저 | 프락셔널 | — | 프락셔널 | 박피성(매질 유도) | — | 프락셔널 = 원천 하위 이름 「프락셔널」(M8-2)에서 · 박피성은 매질 탄산가스에서 유도 |
| `M8-4-1` | 브이빔 | PDL | 롱펄스 | 롱펄스 | — | — | — |  |
| `M8-4-2` | 엑셀 V | 엔디야그 레이저 | 롱펄스 | 롱펄스 | — | — | — |  |
| `M8-4-3` | 더마V | 엔디야그 레이저 | 롱펄스 | 롱펄스 | — | — | — |  |
| `auto-34-1774737181584` | 노블린 | 알렉산드라이트 레이저 | 롱펄스 | 롱펄스 | — | — | — |  |
| `M8-5-4` | 클라리티2 | 엔디야그 레이저 | Q-switched · 롱펄스 | 롱펄스 | — | — | Q-switched: 제품 항목 M8-P-3 설명 「Q-switched」 ↔ 원장 항목 「롱펄스 532+1064」 · 허가 모델명 「CLARITY II LPA」(Long Pulse Alexandrite) → 롱펄스가 허가 근거 · M8-P-3 설명은 원천 수정 후보 |  |
| `M8-5-5` | 아발란체 | 엔디야그 레이저 | 롱펄스 | 롱펄스 | — | — | — |  |
| `auto-36-1774737181584` | 아포지 엘리트 플러스 | 알렉산드라이트 레이저 | 롱펄스 | 롱펄스 | — | — | — |  |
| `auto-M8-1775362936434` | 리팟 | 엔디야그 레이저 | Q-switched · 나노초 | Q스위치(나노초) | — | — | — |  |
| `auto-M8-1775360583893` | 피코플러스 | 엔디야그 레이저 | Picosecond · 피코초 | 피코초 | — | — | — |  |
| `auto-M8-1775360593064` | 디스커버리 피코 | 엔디야그 레이저 | Picosecond · 피코초 | 피코초 | — | — | — |  |
| `auto-M8-1775360601666` | 엔라이튼 | 엔디야그 레이저 | Picosecond · 피코초 | 피코초 | — | — | — |  |
| `M8-P-1` | 피코웨이 | 엔디야그 레이저 | 피코초 | 피코초 | — | — | — |  |

매질별 펄스 방식(장비에서 모음): 알렉산드라이트 레이저 = 롱펄스/피코초 · 엔디야그 레이저 = Q스위치(나노초)/롱펄스/피코초 · PDL = 롱펄스

## E. 계열 기본 기법 18

| 계열 | 기본 | 보조 | 기본 층 | 근거 |
|---|---|---|---|---|
| M1 보툴리눔 톡신 | K01 주입 | — | 근육 내 | 정의 「근육·피부에 주사」 · mechanism injection · D-02 예시 「사각턱 · 근육 내 주입」 — 「피부(진피)」 쪽은 K01a(스킨보톡스 · 다한증)로 단위 시술에서 덮어씀 |
| M2 성형용 필러 | K01 주입 | — | 부위 safe_layers | 정의 「진피·피하에 … 주입」 · mechanism injection · 층은 부위별(anatomy safe_injection_depth) |
| M3 바이오스티뮬레이터 | K01 주입 | — | 부위 safe_layers | 정의 「주입」 · mechanism injection |
| M4 스킨부스터 | K01a 메조테라피 | K01c 무바늘 제트 주입 | 진피 | 정의 「진피에 소량씩 여러 점 주입(또는 무바늘 제트 주입)」 · 문헌 이름 mesotherapy |
| M5 PRP·엑소좀 | K01 주입 | K09 도포 | — | 정의 「주입·도포」 · related 「MTS + PRP — 도포」 |
| M6 자가지방이식 | K01 주입 | — | — | 정의 「꺼진 곳에 주입」 · mechanism injection |
| M7 실리프팅 | K02 삽입 | — | 피하 | 정의 「실을 피하에 넣어」 · 문헌 33469333 「inserted subcutaneously」 — 세부(코그 · 모노 · 볼륨)는 단위 시술에서 |
| M8 레이저·광치료 | K04 조사 | — | — | 정의 「피부에 조사」 · mechanism thermal · ablative — 세부(토닝 · 프락셔널 · 광역학)는 단위 시술에서 |
| M9 HIFU·고주파 리프팅 | K05 에너지 가열 | — | 진피 · SMAS(문헌) | 정의 「피부를 뚫지 않고 … 가열」 · 문헌 37753689 「HIFU … dermis and SMAS · RF … papillary dermis」 |
| M10 HIFEM·EMS 근육 자극 | K06 전자기 자극 | — | — | 정의 「전자기장 또는 전기 자극으로 근육을 수축」 |
| M11 고주파 마이크로니들(니들RF) | K03 미세침 천공 | — | 진피 | 정의 「미세침을 진피에 찌른 뒤 … 고주파」 — 장비 속성 energy = RF |
| M12 마이크로니들링(MTS) | K03 미세침 천공 | — | — | 정의 「미세침(롤러·스탬프·전동 펜)으로 미세 천공」 — 롤러 · 스탬프 · 전동 = 도구 형태 속성 |
| M13 플라즈마 | K07 플라즈마 전달 | — | 표피 | 정의 「피부 표면에 직접 전달」 |
| M14 냉동지방분해 | K08 냉각 | — | 피하 지방층 | 정의 「피부 밖에서 지방층을 냉각」 |
| M15 외용 관리 | K09 도포 | K11 박리·흡인 · K10 침투 | — | 정의 「바르거나 흡수 … 기계적 박리·클렌징 기기 · 흡수 보조 기기」 — 하위 계열별: 화학 박피 · 외용제 = K09 / 기계적 박리·클렌징 = K11 / 흡수 보조 기기 = K10 |
| M16 정맥 영양 수액 | K01b 정맥 주사 | — | 정맥 내 | 정의 「정맥으로 투여」 · mechanism intravenous · DEC-003 D-05 — 정맥 아닌 성분 주사(DEC-003 OQ-308)는 5단계에서 허가 용법으로 K01 덮어씀 |
| M17 줄기세포·줄기세포 유래 제제 | K01 주입 | K09 도포 | — | 정의 「주입·도포」 · mechanism injection |
| N1 지방분해 주사 | K01 주입 | — | 피하 지방층 | 정의 「피하 지방층에 … 직접 주사」 |

단위 시술이 원천에서 다른 기법을 부르면(스킨보톡스 · 다한증 = 메조테라피, 성분 주사 = 허가 용법) 5단계에서 덮어쓴다 — 기본은 덮어쓸 값이 없을 때만.

## F. 초안 큰 기법 65 → 새 구조

| id | 초안 | 원천 표현 | 초안 단위 시술 | 판정 | 새 자리 | 이유 |
|---|---|---|---|---|---|---|
| T01 | 근육축소 | 근육축소 · 교근축소 | 2 | 합침 | K01 주입 | 층 근육 내 + 대상 근육(교근 · 장딴지근) — 「축소」는 7단계 목적 · 「교근축소」는 D-03 표대로 해부학·기법 속성 |
| T02 | 스킨보톡스 | 스킨보톡스 | 1 | 합침 | K01a 메조테라피 | 「스킨보톡스」 = 상담 용어 → 5단계 단위 시술 이름(M1 × 얼굴 전체 × 메조테라피) — D-02 예시 |
| T03 | 네페르티티 리프트 | 네페르티티 리프트 | 0 | 버림 | — | 5단계 단위 시술 이름(M1 × 턱선 · 목 · 기법 K01 · 대상 근육 Platysma) — D 표 네페르티티 |
| T04 | 토닝 | 토닝 · 532nm 포커스 토닝 · 포커스 토닝 · 피코토닝 · 알렉스토닝 · 듀얼 토닝 · 제네시스토닝 | 3 | 유지 | K04a 토닝 | 변형 이름(피코토닝 · 알렉스토닝 · 제네시스토닝 · 포커스 · 듀얼)은 5단계 이름 · 동의어 — 펄스 · 매질은 장비 속성/2단계 하위 |
| T05 | 박피성 프락셔널 | 박피성 | 1 | 합침 | K04b 프락셔널 | 속성 ablative = 박피성 |
| T06 | 비박피성 프락셔널 | 비박피성 · 비박리성 · 비박피성 피코 프락셀 | 2 | 합침 | K04b 프락셔널 | 속성 ablative = 비박피성 |
| T07 | 프락셔널 | 프락셔널 · 프락셀 · 피코슈어 프락셔널 · 얕은 박피 | 0 | 유지 | K04b 프락셔널 | 「얕은 박피」 = 속성 peel_depth 「얕은」(프락셀 듀얼 1927nm) |
| T08 | BBL 시술 프로토콜 | BBL 시술 프로토콜 · BBL 여드름 시술 프로토콜 | 0 | 버림 | — | 장비 프로그램 이름(BBL Forever Young · Clear) → 5단계 단위 시술 이름 · 기법은 K04 조사 |
| T09 | 일반 레이저 방식 | 루비 · KTP | 0 | 버림 | — | 루비 · KTP = 2단계 M8 하위 계열(매질 · 이미 정본) |
| T10 | 4단계리프팅 | 4단계리프팅 | 1 | 버림 | — | 장비 프로그램 이름(포토나 4D) → 5단계 단위 시술 이름 · 기법 K04 조사 |
| T11 | 모노폴라 | 모노폴라 | 11 | 버림 | — | 모노폴라 = RF 전극 방식 → 장비(제품) 속성 `electrode` |
| T12 | 바이폴라 | 바이폴라 · 양극성 | 3 | 버림 | — | 바이폴라 · 양극성 = 장비 속성 `electrode` |
| T13 | 침습+비침습 | 침습+비침습 | 1 | 버림 | — | 침습+비침습 = 장비 속성(니들 · 비니들 핸드피스 겸용) — 단위 시술은 쓰는 쪽 기법(K03 · K05)으로 각각 |
| T14 | 마이크로웨이브 | 마이크로웨이브 · 극초단파 | 3 | 버림 | — | 마이크로웨이브 = 2단계 M9 하위 계열(이미 정본) |
| T15 | 캐비테이션 | 캐비테이션 | 0 | 버림 | — | 캐비테이션 = 장비 속성 `energy`(바이캐빈) — 기법 K05 |
| T16 | 석션 | 석션 | 2 | 버림 | — | 석션 = 장비 속성(어플리케이터 흡인 · 바넥스 · 바넥스프로 · 소노퀸) — 기법은 계열 기본(K08 · K06 · K10) |
| T17 | 냉각 | 냉각 | 0 | 합침 | K08 냉각 | 크라이오셀(M15-8) 냉각 · 사파이어레이저 「냉각」은 장비 속성(표피 냉각) |
| T18 | 코그 | 코그 · 코그(Cog) · Cog · 양방향 · 단방향 | 1 | 합침 | K02a 코그실 삽입 | 「양방향 · 단방향」 = 실 디자인 → 제품 속성 `thread_design`(5단계 uses_product) |
| T19 | 모노 | 모노 | 1 | 합침 | K02b 모노실 삽입 |  |
| T20 | 볼륨실 | 볼륨실 | 1 | 합침 | K02c 볼륨실 삽입 |  |
| T21 | 2방향 | 2방향 | 0 | 버림 | — | 실 디자인 → 제품 속성 `thread_design`(5단계 uses_product · 원문 그대로) |
| T22 | 다방향 | 다방향 | 0 | 버림 | — | 실 디자인 → 제품 속성 `thread_design`(5단계 uses_product · 원문 그대로) |
| T23 | 전방향 | 전방향 | 0 | 버림 | — | 실 디자인 → 제품 속성 `thread_design`(5단계 uses_product · 원문 그대로) |
| T24 | 콘 | 콘 | 0 | 버림 | — | 실 디자인 → 제품 속성 `thread_design`(5단계 uses_product · 원문 그대로) |
| T25 | 오메가 형태 | 오메가 형태 | 0 | 버림 | — | 실 디자인 → 제품 속성 `thread_design`(5단계 uses_product · 원문 그대로) |
| T26 | 루프형 | 루프형 | 0 | 버림 | — | 실 디자인 → 제품 속성 `thread_design`(5단계 uses_product · 원문 그대로) |
| T27 | 텐션형 | 텐션형 | 0 | 버림 | — | 실 디자인 → 제품 속성 `thread_design`(5단계 uses_product · 원문 그대로) |
| T28 | 벌집형 | 벌집형 | 0 | 버림 | — | 실 디자인 → 제품 속성 `thread_design`(5단계 uses_product · 원문 그대로) |
| T29 | 몰딩 메쉬 | 몰딩 메쉬 | 0 | 버림 | — | 실 디자인 → 제품 속성 `thread_design`(5단계 uses_product · 원문 그대로) |
| T30 | 롤러형 | 롤러형 | 1 | 버림 | — | 도구 형태 → 단위 시술/장비 속성 `tool_form` = 롤러형 (DEC-003 OQ-311 닫힘) |
| T31 | 스탬프형 | 스탬프형 · 전동 스탬프형 | 1 | 버림 | — | 도구 형태 `tool_form` = 스탬프형 |
| T32 | 전동 | 전자동 · 펜타입 · 진동형 | 1 | 버림 | — | 도구 형태 `tool_form` = 전동(펜타입 · 진동형) |
| T33 | 멀티니들 | 멀티니들 | 0 | 합침 | K01a 메조테라피 | 멀티니들 = 주입 기기 형태 → 장비 속성 `injector` |
| T34 | 니들리스 | 니들리스 · 공기압 주입 · 제트 주입 · 공기압 약물주입 | 0 | 합침 | K01c 무바늘 제트 주입 | 니들리스 · 공기압 · 제트 주입 |
| T35 | 분사 | 분사 | 0 | 합침 | K01c 무바늘 제트 주입 | 분사(노보젯) — 크리스탈필 「분사」는 K11 박리(결정 분사 박피) |
| T36 | 초음파 주입 | 초음파 주입 | 0 | 합침 | K10 침투 | 초음파 주입(벨라소닉) = 침투 방식 장비 속성 `delivery` = 초음파 |
| T37 | 이온도입 | 이온도입 · 전류 약물침투 | 1 | 합침 | K10 침투 | 이온도입 = 장비 속성 `delivery` |
| T38 | 전기천공 | 전기천공 | 1 | 합침 | K10 침투 | 전기천공 = 장비 속성 `delivery` |
| T39 | 워터제트 | 워터제트 · 고압 워터젯 · 물 흡인 | 1 | 합침 | K11 박리·흡인 | 워터제트 · 물 흡인 |
| T40 | 미세박피 | 미세박피 | 0 | 합침 | K11 박리·흡인 | 미세박피(크리스탈필) |
| T41 | 중간~심층 | 중간~심층 | 0 | 합침 | K09 도포 | 속성 peel_depth = 중간(TCA) |
| T42 | 심부필링 | 심부필링 | 0 | 합침 | K09 도포 | 속성 peel_depth = 깊은(페놀) |
| T43 | CROSS 기법 | CROSS 기법 | 1 | 합침 | K09 도포 | 속성 application = 국소(점) — CROSS |
| T44 | 도포 | 도포 · 국소 적용 | 0 | 유지 | K09 도포 |  |
| T45 | 마사지 | 마사지 · 림프순환 | 0 | 버림 | — | 마사지 · 림프순환 = 장비 동작(제네오X · LDM) → 장비 속성 · 파셀라 경락은 2단계 판정 그대로 |
| T46 | 섬유 밴드 절단 | 섬유 밴드 절단 | 1 | 합침 | K12a 서브시전 |  |
| T47 | 압박 | 압박 | 0 | 버림 | — | 압박(실리콘시트) = 외용제 사용 형태 → K09 도포 · 제품 속성 |
| T48 | 펀치이식 | 펀치이식 | 1 | 합침 | K12b 펀치 |  |
| T49 | 압출 | 압출 | 1 | 합침 | K12c 압출 |  |
| T50 | 광역학치료 | 광역학치료 | 1 | 합침 | K04c 광역학 |  |
| T51 | 원심분리 | 원심분리 | 0 | 버림 | — | 원심분리 = 재료 준비(PRP) → 5단계 운영 속성 `prep`(profiles prepNotes 와 같은 칸) |
| T52 | 미세 지방 주입 | 미세 지방 주입 | 1 | 버림 | — | 미세 지방 = 2단계 M6 하위 「지방 입자 크기(마이크로 · 나노)」(이미 정본) — 기법은 K01 |
| T53 | 초미세 | 초미세 | 2 | 버림 | — | 초미세(나노) = 2단계 M6 하위 「지방 입자 크기」(이미 정본) |
| T54 | SVF(줄기세포 포함) | SVF(줄기세포 포함) | 1 | 버림 | — | SVF = 2단계 M17 하위 「세포(SVF)」 · step2 M6 deferred → 5단계 |
| T55 | 메조테라피 | 메조테라피 | 1 | 합침 | K01a 메조테라피 |  |
| T56 | 진피 주입 | 진피 주입 | 1 | 합침 | K01a 메조테라피 | 층 값 「진피」 |
| T57 | 피하 주사 | 피하주입 · 피하 | 2 | 합침 | K01 주입 | 층 값 「피하」 |
| T58 | 국소 주사 | 국소 | 1 | 합침 | K01 주입 | 층 값 「피하 지방층」(N1 지방분해 주사) |
| T59 | 병변내 주사 | 병변내 주사 | 1 | 합침 | K01 주입 | 층 값 「병변 내」(스테로이드 병변내 주사) |
| T60 | 정맥 주사 | IV · 정맥주사 | 0 | 합침 | K01b 정맥 주사 |  |
| T61 | 주입 | 주입 · 주사 · 두피 주입 | 4 | 유지 | K01 주입 | 「두피 주입」의 「두피」는 3단계 부위 |
| T62 | IPL | IPL | 2 | 버림 | — | IPL = 2단계 M8 하위 계열(이미 정본) — 기법 K04 조사 (OQ-311 닫힘) |
| T63 | BBL스킨타이트 | BBL스킨타이트 | 0 | 버림 | — | BBL스킨타이트 = 장비 프로그램 이름 → 5단계 단위 시술 이름 · 기법 K04 조사 |
| T64 | 알렉산드라이트 | 알렉산드라이트 | 1 | 버림 | — | 알렉산드라이트 = 2단계 M8 하위 계열(이미 정본) |
| T65 | 콜드플라즈마 | 콜드플라즈마 | 1 | 버림 | — | 콜드플라즈마 = 2단계 M13 하위 「콜드 플라즈마」(이미 정본) — 기법 K07 |

## 충돌 · 원천 수정 후보

| id | 무엇 | A | B | 해결 |
|---|---|---|---|---|
| X1 | 「비근근」 한 표기에 두 근육 | zones glabella 「비근근 (Procerus)」 | zones nose 「비근근 (Nasalis)」 | 값 사전 키 = 영문(Procerus 눈살근 · Nasalis 코근 — KMA 표준 한글) · 원천 표기는 `source_label` 로 보관 · 원천 수정 후보: glabella 표기 「비근근」→「눈살근」 |
| X2 | 클라리티2 펄스 방식 | 원장 항목 M8-5-4 「롱펄스 532+1064nm」 · 허가 모델 「CLARITY II LPA」(Long Pulse Alexandrite) | 제품 항목 M8-P-3 「Q-switched Nd:YAG」 | 롱펄스(허가 모델명 근거) · M8-P-3 설명은 원천 수정 후보 |
| X3 | 기법 상위 축 — taxonomy group ↔ profiles mechanism | group: M7 시술/기기 · M16 관리 · M17 관리 | mechanism: M7 mechanical(삽입) · M16 intravenous · M17 injection | 큰 기법은 mechanism + 2단계 정의(문헌) 기준 · group 은 계열 표시 속성(원문) — 고치지 않음 |
| X4 | DEC-002 D-02 예시 ↔ 원천 층 | D-02 예시 「HA 필러 · 코 · 피하 주입」 | zones nose safe_injection_depth 「골막상 (코뼈 부위) 또는 연골막상 (비첨부)」 | 층 값은 원천 기준(골막상 @코 · 연골막상 @코끝) — D-02 예시는 형식 예시로 보고 문구 고침은 사용자 판단 J2 |
| X5 | LED 자리 | treatment-sequence 「M15-LED」 | 2단계 정본 M8 하위 「LED」(D04) | 2단계 정본 따름 · 원천 수정 후보: categories 「M15-LED」→「M8-LED」 |
| X6 | 셀렉V Q스위치 | 2단계 주 하위 IPL(허가 펄스광선조사기) | 원천 설명 Q-switched Nd:YAG | pulse_mode 를 보조 하위(엔디야그) 쪽에만 — 기법 값(K04 조사)은 그대로 |

원천 수정 후보:
- `anatomy-danger-zones.json` zones[glabella].botox_specific.target_muscle: 「비근근 (Procerus)」 → 「눈살근 (Procerus)」 (X1)
- `taxonomy.json` modality[M8].products[M8-P-3] 설명: 「Q-switched Nd:YAG」 → 「(허가 모델 CLARITY II LPA — 롱펄스)」 (X2)
- `treatment-sequence.json` sequence_order[11].categories: 「M15-LED」 → 「M8-LED」 (X5)

## 열린 OQ 정리

- **DEC-002 OQ-201** 「어떻게(기법)」 목록과 세분화 · 네페르티티 리프트가 기법인가 → 안 1 노드 24 + 속성 사전 — 층은 속성(키 밖) · 네페르티티 리프트 = 5단계 단위 시술 이름(기법 K01 · 대상 근육 Platysma)
- **DEC-003 OQ-310** 실 구조 · 유형(코그 · 모노 · 볼륨) → 삽입 세부 노드 3(K02a~c) · 모양 낱말(2방향 · 다방향 · 콘 · 오메가 · 루프 · 텐션 · 벌집 · 몰딩 메쉬)은 제품 속성 thread_design
- **DEC-003 OQ-311** 도구 · 방식명 vs 기법 · 장비 → 더마롤러 · 더마스탬프 · MTS롤러 = 도구 형태 속성 · IPL · 알렉산드라이트 · 콜드플라즈마 = 2단계 하위 계열(정본) · BBL스킨타이트 = 5단계 이름
- **DEC-003 OQ-308** 수액의 투여 경로 → 4단계는 노드 둘(K01 주입 · K01b 정맥 주사)만 준다 — 단위 시술마다 고르는 일은 5단계(1단계 정본 허가 품목 · MFDS 용법 조회 결정론). 4단계 open 아님

## 하지 않은 것

- 단위 시술마다 기법 붙이기(5단계 — 항목 이름 · detail 칸은 지도상 5단계)
- site_caution · 혈관 · 신경 · 합병증(8단계)
- SPEC 개정(technique.parent · 속성 칸)

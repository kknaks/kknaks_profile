# 원천 21 JSON 행선지 지도 — 메달리온 실버 1~8

> 조사(read-only) · 2026-10-28 · 결정 아님. 원천 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/` 21파일 전 칸. 기계용 정본 `source-map.json`(칸 517개 전부 · 행선지 · 상태 · 근거 · 추천).
>
> **칸 517 = 끝 39 · 표시 99 · 결정됨 158 · 미정 221** · 결정 묶음 17 · 사용자 판단 5. 미정 221 칸은 전부 묶음에 들어 있고 추천이 있다(빈칸 0).

셈 규칙: **칸** = 잎 키 경로(스칼라 또는 스칼라 배열 · 배열 원소 키까지 · `M1` 같은 코드 키는 `{code}` 로 접음). 칸 하나에 행선지가 여럿이면 **가장 덜 된 상태**로 센다(미정 < 표시 < 결정됨 < 끝) — 예: taxonomy 원장 항목 이름은 1 · 3단계 끝이지만 5단계가 결정됨이라 「결정됨」. 상태 뜻: **끝** = 정본(step1/2/3)에 들어감 · **표시** = 넘김 표시만(_RESUME 10-28 「단계로 넘길 결정」 · 해부학 결정) · **결정됨** = 결정표(DEC · SPEC · _RESUME)에 자리 있음 · **미정** = 자리 없음.

## ① 파일 21

| 파일 | 무엇 | 주 행선지 단계 | 칸 | 끝 | 표시 | 결정됨 | 미정 |
|---|---|---|---|---|---|---|---|
| `anatomy-danger-zones.json` | 위험 부위 11 — 혈관 · 신경 · 층 · 톡신/필러 주의 | 3 · 4 · 8 | 67 | 3 | 44 | 13 | 7 |
| `combo-recipes.json` | 목적별 조합 레시피 7(후속 프로토콜) | 7 | 15 | 0 | 0 | 3 | 12 |
| `complications.json` | 계열별 합병증 65(10 계열) | 8 | 16 | 0 | 0 | 11 | 5 |
| `consent-checklist.json` | 계열 17 필수 고지 · 금기 · 응급 징후 | 8 | 8 | 0 | 5 | 3 | 0 |
| `contraindications.json` | 시술군 쌍 금기 · 간격 27 | 8 | 10 | 0 | 0 | 10 | 0 |
| `extracted.json` | 시술군 17 extracted 사본(+ 추출 메타) — taxonomy modality[].extracted 와 9/17 같음 | 2(대조) · 8 | 23 | 3 | 4 | 0 | 16 |
| `literature-evidence.json` | 계열 17 문헌 근거(기전 · 부작용 · 효과 + 인용 · 4개 언어) | 2 · 8 | 65 | 1 | 0 | 2 | 62 |
| `market-pricing.json` | 시장가 메뉴 122(이름 · 규격 · 하/중/상) | 3 · 1 · 5 | 11 | 2 | 0 | 9 | 0 |
| `patient-education.json` | 계열 17 환자 교육(쉬운 설명 · FAQ) | 8 · 2 | 12 | 0 | 9 | 3 | 0 |
| `pih-risk.json` | PIH 위험 26 시술(원장 항목 기준) | 5 · 8 | 19 | 0 | 11 | 3 | 5 |
| `post-procedure-timeline.json` | 계열 10 시술 후 경과(구간 × 정상/이상/주의/응급) | 8 | 16 | 0 | 9 | 2 | 5 |
| `pre-procedure-checklist.json` | 시술 전 확인 — 공통 12 + 계열 17 × 123 | 8 | 11 | 0 | 8 | 3 | 0 |
| `problem-combos.json` | 고민 8 × 단계 패키지 24(영업 문구 포함) | 7 | 18 | 0 | 0 | 9 | 9 |
| `problem-packages.json` | 고민 14 × CC 115 × 추천 시술 · 조합 · 대안 | 7 · 8 · 3 | 17 | 0 | 0 | 12 | 5 |
| `procedure-comparison.json` | 고민 테마 9 × 시술 비교표 39 | 7 · 5 | 18 | 0 | 0 | 2 | 16 |
| `procedure-profiles.json` | 계열 프로파일 17 — 세션 단계 · 순서 플래그 · 운영 정보 | 8 · 5 · 4 | 27 | 3 | 1 | 5 | 18 |
| `products.json` | 제품-제조사 매핑 59 — taxonomy modality[].products 와 같은 59 | 1(보관) | 15 | 9 | 0 | 4 | 2 |
| `synergy.json` | 시너지 링크 115(함께 · 다음에 · 대신) | 8 · 7 | 10 | 0 | 0 | 9 | 1 |
| `taxonomy.json` | 관리 화면 분류 트리 — 시술군 17 · 원장 항목 521(+ extracted) · 제품 59 · 고민 트리 14/53/117 | 1 · 2 · 3 · 5 · 7 | 84 | 18 | 5 | 41 | 20 |
| `treatment-optimization.json` | 고민 8 × 중증도 최적 조합 · 연령대 · 조합 규칙 · 연간 플랜 | 7 · 8 | 35 | 0 | 0 | 4 | 31 |
| `treatment-sequence.json` | 같은 세션 순서 · 같은 날 불가 · 최소 간격 · 흔한 조합 | 8 · 7 | 20 | 0 | 3 | 10 | 7 |
| **합** | | | **517** | **39** | **99** | **158** | **221** |

- 「끝」이 적은 이유: 정본 셋(1 제품 · 2 계열 · 3 부위)은 원천의 **이름 · 정체** 칸만 먹었다. 원천 칸 대부분은 설명 · 안전 · 관계라 5 · 7 · 8 단계 몫이다
- SPEC-004 빌드는 stg 9파일만 쓰고 11파일(combo-recipes · procedure-profiles · market-pricing · patient-education · procedure-comparison · pih-risk · post-procedure-timeline · literature-evidence · consent-checklist · pre-procedure-checklist · extracted)은 **보관만**(SPEC-001 OQ-S02) — 미정 칸의 대부분이 여기서 나온다

## ② 결정 묶음

영향 = 그 묶음에 든 칸 수 / 파일 수(상태별). 묶음 없는 칸 77개는 끝 · 결정됨이라 정할 것이 없다.

| 묶음 | 추천 | 근거 | 영향 |
|---|---|---|---|
| **B01 원천 메타 · 리니지** | 파일 버전 · 갱신일 · 설명은 브론즈 스냅샷 메타로 두고 주장마다 원천 버전을 단다. `consensus_method` · `source_method` 는 근거 종류(문헌 / 3-AI 합의 / 큐레이션 / 일반 지식)로 정규화해 그 파일에서 나온 모든 주장의 `evidence_kind` 로 복사 — 강도 숫자는 만들지 않는다 | DEC-001 D-02 · D-04 · D-10 · OQ-111 | 50칸 / 18파일 (미정 4 · 표시 0 · 결정됨 46 · 끝 0) — `anatomy-danger-zones`, `combo-recipes`, `consent-checklist`, `contraindications`, `literature-evidence`, `market-pricing`, `patient-education`, `pih-risk`, `post-procedure-timeline`, `pre-procedure-checklist`, `problem-combos`, `problem-packages`, `procedure-comparison`, `procedure-profiles`, `products`, `synergy`, `treatment-optimization`, `treatment-sequence` |
| **B02 값 사전 · 화면 값 · 파생 집계** | 등급 · 단계 정의(중증도 · PIH 등급 · 반응 단계 · tier · 정확도 기준)는 시맨틱 값 사전으로(스키마 tool 응답) — 노드 아님. 화면 값(icon · danger_color)과 다시 셀 수 있는 집계(정확도 평균 · 번역 비율)는 버린다 | DEC-001 D-02(시맨틱 = 스키마 설명) · 메달리온 개요(시맨틱 = 값 정의) | 29칸 / 7파일 (미정 29 · 표시 0 · 결정됨 0 · 끝 0) — `anatomy-danger-zones`, `complications`, `literature-evidence`, `pih-risk`, `post-procedure-timeline`, `problem-combos`, `treatment-optimization` |
| **B03 닫힌 단계 밖 계열 칸 · 4단계 기법 입력** | taxonomy `group` · 프로파일 `mechanism` 태그 · `related_techniques` 문장 → 4단계 기법 조사 입력(계열에는 「기본 방식」 속성만). 환자용 계열 이름 17(`patient_name`)은 2단계 동의어(구어)로 한 줄 보강 — 이름만이라 재검수 없이. 프로파일 `moa_summary` 는 원문 보관(정의는 문헌 기준 그대로) | DEC-002 D-04 · OQ-201 · 2단계 정본 | 6칸 / 4파일 (미정 5 · 표시 0 · 결정됨 1 · 끝 0) — `extracted`, `patient-education`, `procedure-profiles`, `taxonomy` |
| **B04 사람 조건 금기 = 「확인 조건」 원장(8단계)** | 뼈대 = pre-procedure-checklist(공통 12 + 계열별 123 · type 5종 — 유일하게 구조화). consent `contraindications` 105 · taxonomy/extracted 계열 금기 108 · 원장 항목 금기 11 · treatment-sequence 이소트레티노인 쌍 5 · 연령대 4는 같은 조건 노드에 붙는 **원천별 주장**(합치지 않음 · level 원문). 조건 이름은 결정론 사전(임신 · 수유 · 켈로이드 · 항응고제 · 이소트레티노인 · 헤르페스 · 자가면역 · 금속 · 심박기 · 알레르기 …)으로. 이소트레티노인 조건은 1단계 아큐탄(계열 밖 의약품)과 잇는다 | _RESUME 10-28 「단계로 넘길 결정」 8단계(이미 같은 추천) · DEC-001 D-13b | 19칸 / 6파일 (미정 2 · 표시 17 · 결정됨 0 · 끝 0) — `consent-checklist`, `extracted`, `pre-procedure-checklist`, `taxonomy`, `treatment-optimization`, `treatment-sequence` |
| **B05 안전 · 상담 콘텐츠 = 계열 속성 원문(8단계)** | 필수 고지 109(원문 그대로) · 응급 징후(consent 55 + 경과표 94 + extracted 2 + 필러 응급 대응 3 — 원천 표시로 한 칸) · 환자 교육 · 경과표 10 · 사후관리(계열 · 프로파일) · PIH 위험 요인/예방 → **계열(경과표는 하위 계열 ha-filler · dca-injection 까지) 속성 원문**, 단위 시술은 조회 때 상속(SPEC-004 상속 규칙 재사용). **N1 은 M16 원천을 빌리지 않는다**(M16 원천은 수액만 다룸) — dca-injection 경과표만 N1 | _RESUME 10-28 「단계로 넘길 결정」 · 10-28 해부학 결정 · SPEC-004 OQ-G04(빌려 주지 않음)와 같은 기준 | 29칸 / 7파일 (미정 0 · 표시 29 · 결정됨 0 · 끝 0) — `consent-checklist`, `extracted`, `patient-education`, `pih-risk`, `post-procedure-timeline`, `procedure-profiles`, `taxonomy` |
| **B06 시술↔시술 관계 원천 확장(8단계)** | SPEC-004 C 의 3원천(contraindications · synergy · treatment-sequence)에 더해 ① optimization `contraindicated_combos` 17 = 이름 해석되면 금기 주장 ② `combination_rules` 8 = 수작업 대응표(규칙 → 계열 쌍 · 주장 종류)를 게이트에 ③ problem-packages CC `combos` 146 = 조건(그 CC) 붙은 시너지 주장 ④ synergy `type=대신` 16 = `alternative` 로 분리(시너지 아님) ⑤ sequence `categories` 꼬리(-HIFU · -도포 · 마취) = 하위 계열 · 기법 조건 ⑥ 원칙 · 실무 메모 · 프로파일 플래그 = 원문만(파생 엣지 계산 안 함) | DEC-001 D-03 · D-04 · D-13b · SPEC-004 §3.3.3 C | 43칸 / 7파일 (미정 20 · 표시 0 · 결정됨 23 · 끝 0) — `contraindications`, `problem-packages`, `procedure-profiles`, `synergy`, `taxonomy`, `treatment-optimization`, `treatment-sequence` |
| **B07 큐레이션 「추천 조합」 노드 한 타입(7단계)** | problem-combos 패키지 24 · combo-recipes 7 · common_combos 8 · optimization 중증도 조합 24 · 연간 플랜 3 · 연령 플랜 4(+ 비교 9 = B12)를 **노드 타입 하나**(종류 칸으로 구분)로 싣고 원천마다 따로 둔다(합치지 않음). 구성 = includes(계열 → 고민 부위로 단위 시술 내림 · 이름은 §3.3.2 해석) · 고민 = 고민 대응표. 기대 결과 · 이유 · 회차 · 후속 일정은 원문 속성. 영업 문구(salesPitch · upsellHook)는 보관하되 골드 기본 응답 제외. treats ② · ④ 엣지는 결정대로 그대로 | DEC-001 D-13e(3종 전부 적재 · 합치지 않음)를 나머지 큐레이션에 연장 · DEC-002 OQ-204 · DEC-001 OQ-120 | 47칸 / 5파일 (미정 43 · 표시 0 · 결정됨 4 · 끝 0) — `combo-recipes`, `problem-combos`, `problem-packages`, `treatment-optimization`, `treatment-sequence` |
| **B08 고민 어휘 정본(7단계)** | 정본 = taxonomy `problem`(P id 3층). problem-packages 는 같은 P id · CC 115 = 고민 항목(115/115) → 동의어. problem-combos 는 P id 로 바로. 나머지(최적화 고민 8 · 시너지 목표 17 · 레시피 goal 6 · 비교 9 · 연령 주 고민 15)는 **고민 대응표**(사람 확인 게이트)로 — 완전 일치는 2/8 · 7/17 · 0/6 · 0/9 · 5/15 뿐이라 D-13d(완전 일치만)로는 대부분 끊긴다 | DEC-001 D-13d(임시) · OQ-104 · SPEC-004 §3.2.4 | 18칸 / 6파일 (미정 1 · 표시 0 · 결정됨 17 · 끝 0) — `combo-recipes`, `problem-combos`, `problem-packages`, `synergy`, `taxonomy`, `treatment-optimization` |
| **B09 고민이 아닌 대분류(7단계)** | P1 쁘띠시술 · P14 기타 = 고민 노드로 세우지 않음(하위 항목은 부위 + 목적으로 분해) · P10 제모 · P11 얼굴윤곽 = 목적형 고민으로 유지(이름 「털」 · 「윤곽」 같은 상담 용어로) | DEC-001 OQ-105 · DEC-002 D-07 | 1칸 / 1파일 (미정 1 · 표시 0 · 결정됨 0 · 끝 0) — `taxonomy` |
| **B10 단위 시술 속성 추가분(5단계)** | PIH(등급 · 발생률 · 피부 타입 · 해당 없음 계열) · 부위별 톡신 용량 원문(위험 부위 dose_range) · 운영 정보(마취 · 자세 · 준비 · 소요 — 계열값 상속) · 적응증 문장 = 고민 엣지 근거로만(엣지 생성 안 함) · 비교표 PIH 는 pih-risk 와 대조만 | _RESUME 10-28 5단계 넘김 · DEC-001 OQ-110 | 23칸 / 5파일 (미정 14 · 표시 9 · 결정됨 0 · 끝 0) — `anatomy-danger-zones`, `pih-risk`, `procedure-comparison`, `procedure-profiles`, `taxonomy` |
| **B11 근거 노드(8단계 안)** | DEC-001 D-02 가 실버 개체로 「근거」를 두었는데 실버 1~8 순서에 자리가 없다 → 8단계 안에 근거 노드(문헌 = PMID/DOI 키 · 웹 URL · 가이드 표기). 문헌 문장 119(기전 50 · 부작용 32 · 효과 37) · 다국어 환자 문장 · 정확도는 근거 노드 속성, 합병증 URL 38 · 간격 출처 · 규칙 근거도 같은 타입. evidence_level · priority 는 D-04 강도 칸에 원문 등급 | DEC-001 D-02 · D-04 · OQ-111 | 54칸 / 4파일 (미정 54 · 표시 0 · 결정됨 0 · 끝 0) — `complications`, `literature-evidence`, `treatment-optimization`, `treatment-sequence` |
| **B12 비교표(7단계)** | procedure-comparison 9 = 추천 조합 타입의 종류 「비교」(고민 앵커). 비교 대상 39 = 이름 해석으로 단위 시술 · 제품 구성원 엣지, 통증 · 회복 · 비용 등 칸은 **구성원 엣지 속성 원문**(비교 맥락 값 — 단위 시술 속성과 합치지 않음) | OQ-S02(보관만) 이후 결정 없음 | 15칸 / 1파일 (미정 15 · 표시 0 · 결정됨 0 · 끝 0) — `procedure-comparison` |
| **B13 위험 부위 · 합병증 = 안전 정보(8단계)** | 위험 부위 상세는 `site_caution`(부위 → M1/M2) **엣지 속성**(혈관 · 신경 · 위치 수치 · 요령 · 등급), 층 · 깊이 · 대상 근육은 4단계, `critical_safety_facts` 는 M2 계열 안전 속성 원문. 부작용 정본 = complications 65 노드(계열마다 따로), taxonomy · extracted 부작용 문장과 문헌 부작용은 근거 | _RESUME 10-28 해부학 결정 · SPEC-004 §3.2.5 · §3.3.3 D | 67칸 / 3파일 (미정 11 · 표시 44 · 결정됨 12 · 끝 0) — `anatomy-danger-zones`, `complications`, `taxonomy` |
| **B14 같은 뜻 다른 키 정규화** | 적재 때 결정론 키 표(peak_effect → peak · common_adverse_effects → common · serious_adverse_effects → serious · common_side_effects → common) + 원천 수정 목록에 올림 | DEC-001 D-12(결정론) | 5칸 / 1파일 (미정 5 · 표시 0 · 결정됨 0 · 끝 0) — `taxonomy` |
| **B15 중복 원천 2개** | extracted.json · products.json 은 정본(taxonomy modality[].extracted · products — 1/2단계 정본이 이미 씀) 옆에 원문 보관 + 대조만. extracted.json 의 다른 8 계열 칸 · products 6쌍 차이는 검증 리포트 `source_conflict`. extracted.json `source` · `source_type` 만 계열 extracted 속성의 리니지로 | SPEC-004 §3.1.1 · SPEC-001 OQ-S02 | 27칸 / 2파일 (미정 15 · 표시 0 · 결정됨 0 · 끝 12) — `extracted`, `products` |
| **B16 제품 사용 제약(화장품 허가 제품)** | ASCE+ · EXOSOME SKIN = 「주사 · 주입 사용 금지 · 도포로만」(원천 legal_warning). 1단계 상태(ASCE+ 허가 대상 아님 · 추천 포함)는 그대로 두고 제품에 `allowed_routes: [도포]` + 5단계에서 주입 기법 단위 시술과는 잇지 않는 결정론 가드 | 원천 products.json legal_warning · 1단계 정본(고치지 않음) | 2칸 / 1파일 (미정 2 · 표시 0 · 결정됨 0 · 끝 0) — `products` |
| **B17 시장가 = 시술 1회 가격(5단계)** | 결정대로 — 단위 시술 + 제품(등급) + 규격 조합에 가격. 1단계가 제품 행 148에 들고 있는 시장가 사본은 5단계에서 시술 1회로 옮긴다. 패키지 · 비교 · 연간 예산 가격 문장은 그 노드의 원문(시장가와 합치지 않음) | DEC-003 D-02 · SPEC-004 OQ-G15 | 5칸 / 1파일 (미정 0 · 표시 0 · 결정됨 5 · 끝 0) — `market-pricing` |

## ③ 사용자 최종 판단

나머지 묶음은 추천대로 진행하는 기본값이다(B04 · B05 는 이미 _RESUME 10-28 에 같은 추천이 있고 8단계에서 닫는다). 아래 다섯만 사용자 판단.

| # | 판단 | 추천 | 이유 |
|---|---|---|---|
| U1 | 실버 6 · 7 단계 경계 — 「목적」과 고민 앵커 큐레이션(problem-combos · 레시피 · 최적화 · 비교)을 7 고민 단계로 옮기고 6 은 병원 메뉴 패키지만 둘까 | 옮긴다 — 6 패키지(메뉴 묶음, 단위 시술만 필요) → 7 고민 · 목적 · 추천 조합(고민 정본 먼저) → 8 관계 · 안전 · 근거. 번호는 그대로 | 목적은 고민 → 단위 시술 엣지라 고민 어휘가 먼저 있어야 한다(C3). 지금 순서면 6 에서 만든 목적 · 조합을 7 에서 다시 붙여야 한다 |
| U2 | 고민 어휘 정본 = taxonomy problem(P id 3층) · 나머지 고민 어휘는 대응표(사람 확인 게이트)로 · 쁘띠시술 · 기타는 고민에서 뺄까 | 그렇게 — D-13d 임시값(완전 일치만)을 대응표로 바꿈 · 제모 · 얼굴윤곽은 목적형 고민으로 유지 | 완전 일치로는 큐레이션 고민 대부분이 끊긴다(C7 · O7) |
| U3 | 큐레이션 묶음 전부(problem-combos · 레시피 · 흔한 조합 · 최적화 · 연령/연간 플랜 · 비교)를 「추천 조합」 노드 한 타입 · 원천별로 싣고, 영업 문구는 보관만(기본 응답 제외)할까 | 그렇게 — D-13e(합치지 않음)를 나머지 큐레이션에 연장 | 원소만 treats 엣지로 풀면 묶음(순서 · 회차 · 단계)이 사라진다 · 영업 문구는 상담 근거가 아니다(OQ-120) |
| U4 | 근거(문헌 · 웹 · 가이드) 노드를 8단계 안에 둘까 | 8단계 안 — 관계 엣지의 근거 칸(D-04)과 같이 만든다 | DEC-001 D-02 실버 개체에 「근거」가 있는데 실버 1~8 순서에 자리가 없다 |
| U5 | ASCE+ · EXOSOME SKIN(화장품 허가)은 「도포」 단위 시술에만 잇는 가드를 둘까 | 둔다 — 1단계 상태 · 추천 포함은 그대로 | 원천이 주사 · 주입 사용을 법 위반 소지로 명시(C2) |

## ④ 단계 순서 점검

**결론: 6 · 7 경계가 의존과 거꾸로다 — 목적(고민 → 단위 시술 엣지)과 고민 앵커 조합을 7 고민 뒤로, 6 은 메뉴 패키지만(번호 유지 · 사용자 판단 U1).** 정해진 순서(_RESUME §2 10-27)는 뒤집지 않고 충돌 C3 으로 적었다.

```text
지금(10-27 결정)   5 단위 시술 → 6 목적 · 패키지 → 7 고민 → 8 관계 → 빌드
추천(U1)          5 단위 시술 → 6 패키지(병원 메뉴 묶음) → 7 고민 · 목적 · 추천 조합 · 비교 → 8 관계 · 안전 · 사람 조건 · 근거 → 빌드
```

| 단계 | 필요한 것 | 판정 |
|---|---|---|
| 6 목적 · 패키지 | 목적 = 고민 → 단위 시술 엣지(DEC-002 D-03) — 고민 노드 필요 · 패키지(메뉴 묶음) = 단위 시술만 필요 | 목적은 7 뒤로 · 패키지는 6 그대로 |
| 7 고민 | 고민 정본(taxonomy problem) · 부위 분리는 3단계에서 끝 · 대응표 | 목적 · 추천 조합 · 비교를 같이 — 같은 고민 대응표를 쓴다 |
| 8 관계 | 단위 시술 이름(5) · 고민(7) · 근거 | 시술↔시술 · 사람 조건 · 안전 · 상담 콘텐츠 · 근거 노드 — 순서 맞음. 단 CC 조건 시너지(problem-packages combos)는 7 뒤라 여기서 맞음 |
| 4 기법(다음) | 이 지도에서 4단계 입력이 나온다 — taxonomy group · 프로파일 mechanism · related_techniques · 위험 부위 층 · 깊이 · 대상 근육 · sequence 꼬리 · items 「도포」 제약(B16) | 4 전에 지도를 먼저 한 것이 맞음 — 입력 목록에 넣는다 |
| 2 계열(닫힘) | 계열 단위 원천 6파일이 옛 M 코드 경계로 쓰였다(C5) | 2단계를 다시 열지 않는다 — 계열 콘텐츠는 8단계 속성으로 붙이고 N1 빈칸 표시 |

- **고민(7) 자리**: 고민 노드 자체는 taxonomy problem 하나로 서지만, 원천의 고민 쪽 칸(큐레이션 5파일 · 비교 · 시너지 목표)은 전부 「고민 → 무엇」 관계다. 그래서 고민 단계 = 어휘 정본 + 그 어휘를 쓰는 묶음까지가 한 덩어리다
- **combo-recipes 자리**: 「목적별 프리셋」이지만 시술은 계열 코드(M9 · M1 …)라 단위 시술 묶음(6 패키지)이 아니다 — goal(영문 6키)이 고민 대응표를 거쳐야 앵커가 서므로 7. 시술↔시술 관계(8)도 아니다 — 쌍이 아니라 묶음이고 후속 일정이 붙어 있다
- **조합 엣지(8)**: 쌍으로 된 주장(금기 · 간격 · 같은 날 · 순서 · 시너지 · 대체)만 8. 묶음(3개 이상 · 회차 · 플랜)은 7 「추천 조합」. 같은 원천 줄이 둘 다에 걸리면(problem-packages CC 조합) 묶음은 7 · 쌍 주장은 8

## 겹침 — 같은 사실이 여러 파일에

| # | 사실 | 원천 | 실측 | 정본 추천 |
|---|---|---|---|---|
| O1 | 사람 조건 금기 | pre-procedure-checklist(공통 12 · 계열 123) · consent-checklist contraindications 105 · taxonomy modality extracted.contraindications 108(= extracted.json 같은 108) · 원장 항목 safety.contraindications 11 · treatment-sequence 이소트레티노인 쌍 5 · optimization 연령대 avoid 6 | 키워드 계열 수(taxonomy / consent / pre 계열별 / pre 공통): 임신 10/17/2/Y · 수유 9/17/0/Y · 켈로이드 7/7/6/Y · 항응고 5/7/6/Y · 이소트레티노인 2/2/4/Y · 헤르페스 0/0/2/Y · 자가면역 3/5/4/Y · 금속 4/3/5/N · 심박기 4/0/3/N · 알레르기 7/7/7/Y — 원천마다 빈칸이 다르다 | pre-procedure-checklist 를 조건 원장 뼈대로(구조화 · 공통/계열 두 층 · level 5종), 나머지는 같은 조건 노드의 원천별 주장(B04) |
| O2 | 응급 징후 | consent emergency_signs 55 · post-procedure-timeline phases[].emergency 94 · extracted.json safety.emergency 2 · anatomy filler_specific.emergency_protocol 3 | consent 는 계열 단위 목록, 경과표는 시간 구간별, 위험 부위는 부위별 대응 절차 — 단위가 다르다 | 계열 `emergency_signs[]` 한 칸에 원천 표시로 모으고(구간 · 부위가 있으면 그 칸까지) — 고르지 않음(B05) |
| O3 | 사후관리 | taxonomy 원장 항목 aftercare 1,914 · 제품 aftercare 238 · 계열 aftercare 53(= extracted.json 53) · procedure-profiles aftercare 64 · 경과표 normal 162 | 계열 · 제품 · 원장 항목 세 층에 같은 문장이 반복 | 계열 = taxonomy modality extracted.aftercare(정본) + 프로파일은 보조 주장 · 원장 항목/제품 aftercare 는 5단계 단위 시술 × 제품 속성(B05 · 결정 10-27) |
| O4 | 부작용 · 합병증 | complications 65(10 계열 · 중증도/발생률/처치 구조화) · taxonomy 계열 safety 141 · 원장 항목 safety 1,700+ · 제품 safety 284 · 문헌 adverse_effects 32 · 경과표 abnormal/caution | 구조화된 것은 complications 뿐 · 7 계열(M4 · M5 · M6 · M10 · M12 · M13 · M17)은 합병증 원천 없음(OQ-119) | complications = 노드 정본 · 나머지 문장은 근거 · 단위 시술 속성(B13) |
| O5 | 시술↔시술 금기 · 간격 · 순서 · 시너지 | contraindications 27 · synergy 115 · treatment-sequence(순서 11 · 같은 날 불가 9 · 간격 9) · optimization(규칙 8 · 피할 조합 17) · problem-packages CC 조합 146 · 제품 금기 1 · 프로파일 순서 값 17 | 보톡스 · 필러: contraindications 「동일 부위 보톡스 먼저 → 필러」 ↔ sequence_order 필러(6) → 보톡스(8) ↔ optimization 「같은날: 필러→스킨부스터→보톡스. 또는 보톡스 먼저」 — 셋이 다름 | procedure_relation 엣지 하나(D-03 · 결정됨) — 원천은 주장, 충돌은 보존(D-13b). 원천 확장은 B06 |
| O6 | 조합 · 패키지 · 플랜(묶음) | problem-combos 24 · combo-recipes 7 · common_combos 8 · optimization 중증도 조합 24 · 연간 플랜 3 · 연령 플랜 4 · 비교 9 · taxonomy 원장 「큐레이션」 메뉴(패키지 17 행선지) | 앵커가 다르다 — 고민(problem-combos · optimization · 비교) · 목적 키(레시피) · 이름 없음(흔한 조합) · 연령(플랜) · 병원 메뉴(taxonomy 패키지) | 병원 메뉴 묶음 = 6단계 패키지(DEC-002 D-03) · 나머지 = 7단계 「추천 조합」 노드(원천별 · B07 · B12) |
| O7 | 고민 어휘 | taxonomy problem 14/53/117 · problem-packages 14 · CC 115 · problem-combos 8 · 최적화 고민 8 · 시너지 목표 17 · 레시피 goal 6 · 비교 9 · 연령 주 고민 15 | taxonomy 이름과 완전 일치(쳐짐→처짐 · 구분자 제거): 최적화 2/8 · 시너지 7/17 · goal 0/6 · 비교 0/9 · 연령 5/15 · problem-combos 6/8(P id 는 같음) | taxonomy problem 정본 + 고민 대응표(B08) |
| O8 | 계열 설명 · 정의 | taxonomy modality extracted(17) · extracted.json(17 · 9 같음) · 문헌 moa 50 · 프로파일 moa_summary 17 · 환자 교육 how_it_works 17 | 정의는 2단계에서 문헌 기준으로 확정됨 | 정의 = step2 · 설명 속성 = taxonomy modality extracted · 나머지 원문(B03 · B05 · B15) |
| O9 | 제품 목록 | taxonomy modality[].products 59 · products.json 59 | 이름 + 제조사 53쌍 같음 · 6 다름 · products.json 에만 legal_warning · regulatory_status 2 | 1단계 정본(step1-products) · 두 원천은 원문 보관(B15) · 법적 경고는 B16 |
| O10 | PIH 위험 | pih-risk 26 · procedure-comparison pih_risk 39 | 비교표 값은 비교 맥락 · 원장 항목 id 없음 | pih-risk 정본(5단계 속성) · 비교표 값은 대조(B10) |
| O11 | 가격 | market-pricing 122 · problem-combos priceRange 24 · 비교 cost_range 39 · 연간 플랜 예산 3 | 단위가 다르다(시술 1회 / 패키지 / 시술군 범위 / 연간) | 시장가 = 시술 1회 가격 정본(DEC-003 D-02) · 나머지는 그 노드의 원문(B17) |
| O12 | 이름으로만 가리키는 시술 끝점 | synergy from/to 230 · sequence categories 19 · 같은 날 불가 17 · 간격 18 · 최적 조합 74 · 흔한 조합 26 · 비교 39 · 연간 플랜 77 · problem-packages 시술 254 · 조합 원소 277 | 코드가 없는 이름 끝점 — 5단계 단위 시술 이름 · 동의어가 서야 풀린다 | SPEC-004 §3.3.2 이름 해석(후보 전부 · 고르지 않음)을 5단계 뒤에 한 번 — 모든 원천 공통 |

## 충돌 — 결정은 뒤집지 않고 기록만

| # | 무엇 | 한쪽 | 다른 쪽 | 추천 |
|---|---|---|---|---|
| C1 | 위험 등급 자리 | SPEC-004 §8 「부위 노드 danger_level」(2차) | _RESUME §2 10-28 해부학 결정 — 위험 부위 속성은 부위 노드에 안 붙임 | site_caution 엣지 속성으로(10-28 결정 쪽). SPEC-004 §8 줄은 다음 SPEC 개정 때 정리 |
| C2 | 화장품 허가 엑소좀 제품의 추천 | 1단계 정본 ASCE+ = 「허가 대상 아님」 · recommendable true(10-28 「출처 있으면 추천 포함」) | 원천 products.json legal_warning — 주사 · 주입 사용은 의료법 · 화장품법 위반 소지 · 「도포」로만 | 1단계는 그대로 · 사용 방식 가드(B16) — 사용자 판단 U5 |
| C3 | 실버 6 · 7 단계 순서 | _RESUME §2 10-27 순서 — 6 목적 · 패키지 → 7 고민 | DEC-002 D-03 「목적 = 고민 → 단위 시술 엣지」 · 큐레이션 조합(problem-combos · 레시피 · 최적화 · 비교)은 고민 노드가 있어야 앵커가 섬 | §4 순서 점검 — 사용자 판단 U1 |
| C4 | 계열 단위 금기를 단위 시술에 붙이는 방식 | _RESUME 10-28 「contraindications.json 은 계열 단위 → 단위 시술로 내림」 | SPEC-004 §3.3.3 C 「단위 시술은 계열 엣지를 조회 때 상속 · 펼쳐 저장하지 않는다」 | 같은 뜻으로 읽고 상속으로 구현(저장 안 함). 단위 시술 이름으로 된 주장(간격 · 같은 날 불가)만 단위 시술 끝점으로 저장 |
| C5 | N1 지방분해 주사의 계열 단위 원천 | 2단계 정본 N1(M16 DCA · LIPO 등에서 분리) · 옮김 66행으로 계열 경계가 바뀜 | 계열 키 원천(consent · 교육 · 프로파일 · 사전 체크 · 합병증 · 시장가)의 M16 은 전부 수액 내용(DCA · 지방분해 언급 0) · N1 은 경과표 dca-injection 1개뿐 | N1 은 M16 원천을 빌리지 않고 빈칸 표시(`no_family_source`) — SPEC-004 OQ-G04 와 같은 기준. 다른 계열도 원천은 옛 M 코드 경계로 쓰였다는 표시(scope) |
| C6 | extracted.json ↔ taxonomy modality extracted | extracted.json | taxonomy modality[].extracted(SPEC-004 가 씀) | taxonomy 정본 · 다른 8 계열 칸은 검증 리포트(B15) |
| C7 | 고민 동의어 규칙 | DEC-001 D-13d(임시) — 다른 고민 어휘는 정규화 완전 일치일 때만 동의어 | 완전 일치 실측 2/8 · 7/17 · 0/6 · 0/9 · 5/15 — 큐레이션 고민이 대부분 고민 트리와 끊김 | 고민 대응표(사람 확인 게이트) — 사용자 판단 U2 |
| C8 | 보톡스 · 필러 순서 | contraindications 「보톡스 먼저 → 필러」 | sequence_order 필러(6) → 보톡스(8) · optimization 「필러→스킨부스터→보톡스. 또는 보톡스 먼저」 | 이미 D-13b(충돌 보존 · 「충돌」 표시) — 그대로 |
| C9 | synergy 「대신」 | SPEC-004 C — synergy links 전부 procedure_relation 주장 | type 「대신」 16 = 대체 관계(시너지 아님) | `alternative` 로 분리(B06 ④) |
| C10 | 이소트레티노인 「쌍」 | SPEC-004 C — 같은 날 불가 · 간격 이름 해석, 못 풀면 엣지 없음 | 「이소트레티노인 복용 중」 3쌍 · 간격 2쌍은 사람 조건 — 시술 쌍으로 안 풀려 조용히 사라짐 | 사람 조건 금기(B04)로 옮김 |

## 칸 전수

행선지 표기 = `단계 · 종류 → 대상 〔상태〕`. 근거 · 값 개수 · 예시는 `source-map.json` `fields[]` 에 있다. 미정 칸은 「추천」 칸이 채워져 있다.

### `anatomy-danger-zones.json`

| 칸 | 무엇 | 단위 | 행선지 | 상태 | 묶음 | 추천(미정) |
|---|---|---|---|---|---|---|
| `version` | 파일 버전 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `updated` | 파일 갱신일 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `consensus_method` | 이 파일 내용을 만든 방법(문헌 큐레이션 · AI 합의 등) | 전역 | 브론즈 · 원문 보관 → 브론즈 스냅샷 메타 〔결정됨〕<br>8 · 엣지 속성 → 엣지 근거 종류(source_method) — 강도 칸 재료 〔미정〕 | **미정** | B01 | 근거 종류 값으로 정규화(문헌 / 3-AI 합의 / 큐레이션 / 일반 지식)해 이 파일에서 나온 모든 주장의 `evidence_kind` 로 복사. 강도 숫자는 만들지 않는다 |
| `critical_safety_facts.minimum_filler_for_blindness` | 필러 실명 위험 핵심 사실(최소량 · 고위험 부위 · 기전 · 단서) | 계열 | 8 · 속성 → 필러 계열(M2) 안전 정보 원문 — 위험 부위 공통 〔미정〕 | **미정** | B13 | M2 계열의 안전 속성(`critical_safety_facts`) 원문 보관 + 위험 부위 site_caution(M2) 엣지들이 이 노드 문구를 참조. 숫자는 바꾸지 않음 |
| `critical_safety_facts.blindness_highest_risk_zones` | 필러 실명 위험 핵심 사실(최소량 · 고위험 부위 · 기전 · 단서) | 계열 | 8 · 속성 → 필러 계열(M2) 안전 정보 원문 — 위험 부위 공통 〔미정〕 | **미정** | B13 | M2 계열의 안전 속성(`critical_safety_facts`) 원문 보관 + 위험 부위 site_caution(M2) 엣지들이 이 노드 문구를 참조. 숫자는 바꾸지 않음 |
| `critical_safety_facts.mechanism` | 필러 실명 위험 핵심 사실(최소량 · 고위험 부위 · 기전 · 단서) | 계열 | 8 · 속성 → 필러 계열(M2) 안전 정보 원문 — 위험 부위 공통 〔미정〕 | **미정** | B13 | M2 계열의 안전 속성(`critical_safety_facts`) 원문 보관 + 위험 부위 site_caution(M2) 엣지들이 이 노드 문구를 참조. 숫자는 바꾸지 않음 |
| `critical_safety_facts.caveat` | 필러 실명 위험 핵심 사실(최소량 · 고위험 부위 · 기전 · 단서) | 계열 | 8 · 속성 → 필러 계열(M2) 안전 정보 원문 — 위험 부위 공통 〔미정〕 | **미정** | B13 | M2 계열의 안전 속성(`critical_safety_facts`) 원문 보관 + 위험 부위 site_caution(M2) 엣지들이 이 노드 문구를 참조. 숫자는 바꾸지 않음 |
| `zones[].id` | 위험 부위 zone id · 이름(11) | 부위 | 3 · 속성 → 부위 노드 danger_zone 대응 〔끝〕 | **끝** | — |  |
| `zones[].name_ko` | 위험 부위 zone id · 이름(11) | 부위 | 3 · 속성 → 부위 노드 danger_zone 대응 〔끝〕 | **끝** | — |  |
| `zones[].name_en` | 위험 부위 zone id · 이름(11) | 부위 | 3 · 속성 → 부위 노드 danger_zone 대응 〔끝〕 | **끝** | — |  |
| `zones[].danger_level` | 위험 등급 1~5 | 부위 | 8 · 엣지 속성 → site_caution 엣지 속성(부위 노드에는 안 붙임) 〔결정됨〕 | **결정됨** | B13 |  |
| `zones[].danger_color` | 위험 등급 색(UI) | 부위 | 버림 · 버림 → danger_level 에서 파생되는 화면 색 〔미정〕 | **미정** | B02 | 버린다 — danger_level 로 다시 만들 수 있는 화면 값 |
| `zones[].vessels[].name` | 위험 혈관 이름 · 깊이 · 지름 · 주행 · 위험 · 메모 | 부위 | 8 · 엣지 속성 → 안전 정보(혈관) — site_caution 엣지 속성 〔표시〕 | **표시** | B13 |  |
| `zones[].vessels[].depth_mm` | 위험 혈관 이름 · 깊이 · 지름 · 주행 · 위험 · 메모 | 부위 | 8 · 엣지 속성 → 안전 정보(혈관) — site_caution 엣지 속성 〔표시〕 | **표시** | B13 |  |
| `zones[].vessels[].diameter_mm` | 위험 혈관 이름 · 깊이 · 지름 · 주행 · 위험 · 메모 | 부위 | 8 · 엣지 속성 → 안전 정보(혈관) — site_caution 엣지 속성 〔표시〕 | **표시** | B13 |  |
| `zones[].vessels[].course` | 위험 혈관 이름 · 깊이 · 지름 · 주행 · 위험 · 메모 | 부위 | 8 · 엣지 속성 → 안전 정보(혈관) — site_caution 엣지 속성 〔표시〕 | **표시** | B13 |  |
| `zones[].vessels[].danger` | 위험 혈관 이름 · 깊이 · 지름 · 주행 · 위험 · 메모 | 부위 | 8 · 엣지 속성 → 안전 정보(혈관) — site_caution 엣지 속성 〔표시〕 | **표시** | B13 |  |
| `zones[].vessels[].note` | 위험 혈관 이름 · 깊이 · 지름 · 주행 · 위험 · 메모 | 부위 | 8 · 엣지 속성 → 안전 정보(혈관) — site_caution 엣지 속성 〔표시〕 | **표시** | B13 |  |
| `zones[].vessels[].depth_range_mm` | 위험 혈관 이름 · 깊이 · 지름 · 주행 · 위험 · 메모 | 부위 | 8 · 엣지 속성 → 안전 정보(혈관) — site_caution 엣지 속성 〔표시〕 | **표시** | B13 |  |
| `zones[].nerves[].name` | 위험 신경 이름 · 종류 · 의미 | 부위 | 8 · 엣지 속성 → 안전 정보(신경) — site_caution 엣지 속성 〔표시〕 | **표시** | B13 |  |
| `zones[].nerves[].type` | 위험 신경 이름 · 종류 · 의미 | 부위 | 8 · 엣지 속성 → 안전 정보(신경) — site_caution 엣지 속성 〔표시〕 | **표시** | B13 |  |
| `zones[].nerves[].significance` | 위험 신경 이름 · 종류 · 의미 | 부위 | 8 · 엣지 속성 → 안전 정보(신경) — site_caution 엣지 속성 〔표시〕 | **표시** | B13 |  |
| `zones[].safe_injection_depth` | 안전 주입 층(골막상 등) | 부위 | 4 · 속성 → 기법(층 · 깊이) — 부위별 주입 층 제약 〔표시〕 | **표시** | B13 |  |
| `zones[].tissue_data.frontalis_thickness.midpupil_mm` | 근육 두께 · 섬유 · 덮임(전두근 · 추미근 · 광경근 · DAO) | 부위 | 4 · 속성 → 기법(대상 근육 · 깊이) 근거 수치 〔표시〕 | **표시** | B13 |  |
| `zones[].tissue_data.frontalis_thickness.lateral_canthus_mm` | 근육 두께 · 섬유 · 덮임(전두근 · 추미근 · 광경근 · DAO) | 부위 | 4 · 속성 → 기법(대상 근육 · 깊이) 근거 수치 〔표시〕 | **표시** | B13 |  |
| `zones[].tissue_data.frontalis_thickness.lateral_orbital_rim_mm` | 근육 두께 · 섬유 · 덮임(전두근 · 추미근 · 광경근 · DAO) | 부위 | 4 · 속성 → 기법(대상 근육 · 깊이) 근거 수치 〔표시〕 | **표시** | B13 |  |
| `zones[].tissue_data.skin_to_periosteum_mm` | 층 · 깊이 · 구조 수치와 설명(피부-골막 · SMAS · 안와격막 · 눈물고랑 · 협지방 · STL) | 부위 | 4 · 속성 → 기법(층 · 깊이 · 주입 지표) 근거 〔표시〕 | **표시** | B13 |  |
| `zones[].tissue_data.notes` | 층 · 깊이 · 구조 수치와 설명(피부-골막 · SMAS · 안와격막 · 눈물고랑 · 협지방 · STL) | 부위 | 4 · 속성 → 기법(층 · 깊이 · 주입 지표) 근거 〔표시〕 | **표시** | B13 |  |
| `zones[].clinical_pearls` | 임상 요령 문장 | 부위 | 8 · 엣지 속성 → 안전 정보 원문 — site_caution 〔표시〕 | **표시** | B13 |  |
| `zones[].botox_specific.target_muscle` | 보톡스 대상 근육 | 부위 | 4 · 속성 → 기법(대상 근육) — 톡신 × 부위 단위 시술 〔표시〕 | **표시** | B13 |  |
| `zones[].botox_specific.risk` | 보톡스 위험 · 안전 구역 · 확산 · 경고 | 부위 | 8 · 엣지 속성 → site_caution(부위 → M1) 엣지 속성 〔결정됨〕 | **결정됨** | — |  |
| `zones[].botox_specific.safe_zone` | 보톡스 위험 · 안전 구역 · 확산 · 경고 | 부위 | 8 · 엣지 속성 → site_caution(부위 → M1) 엣지 속성 〔결정됨〕 | **결정됨** | — |  |
| `zones[].botox_specific.diffusion_range_cm` | 보톡스 위험 · 안전 구역 · 확산 · 경고 | 부위 | 8 · 엣지 속성 → site_caution(부위 → M1) 엣지 속성 〔결정됨〕 | **결정됨** | — |  |
| `zones[].botox_specific.key_warning` | 보톡스 위험 · 안전 구역 · 확산 · 경고 | 부위 | 8 · 엣지 속성 → site_caution(부위 → M1) 엣지 속성 〔결정됨〕 | **결정됨** | — |  |
| `zones[].botox_specific.dose_range` | 부위별 톡신 용량 범위(U) | 단위 시술 | 5 · 속성 → 단위 시술(톡신 × 부위) 권장 용량 원문 — 규격 · 양 참고 〔미정〕 | **미정** | B10 | 5단계 단위 시술 「보툴리눔 톡신 × 그 부위」의 `dose_range_text` 속성(원문 · 숫자 파싱 안 함) · 출처 zone id |
| `zones[].filler_specific.risk_level` | 필러 위험 등급 · 주 위험 · 안전 기법 · 점당 최대량 · 권장 제품 · 응급 대응 | 부위 | 8 · 엣지 속성 → site_caution(부위 → M2) 엣지 속성 〔결정됨〕 | **결정됨** | — |  |
| `zones[].filler_specific.primary_risk` | 필러 위험 등급 · 주 위험 · 안전 기법 · 점당 최대량 · 권장 제품 · 응급 대응 | 부위 | 8 · 엣지 속성 → site_caution(부위 → M2) 엣지 속성 〔결정됨〕 | **결정됨** | — |  |
| `zones[].filler_specific.safe_technique` | 필러 위험 등급 · 주 위험 · 안전 기법 · 점당 최대량 · 권장 제품 · 응급 대응 | 부위 | 8 · 엣지 속성 → site_caution(부위 → M2) 엣지 속성 〔결정됨〕 | **결정됨** | — |  |
| `zones[].filler_specific.max_per_point_ml` | 필러 위험 등급 · 주 위험 · 안전 기법 · 점당 최대량 · 권장 제품 · 응급 대응 | 부위 | 8 · 엣지 속성 → site_caution(부위 → M2) 엣지 속성 〔결정됨〕 | **결정됨** | — |  |
| `zones[].filler_specific.preferred_product` | 필러 위험 등급 · 주 위험 · 안전 기법 · 점당 최대량 · 권장 제품 · 응급 대응 | 부위 | 8 · 엣지 속성 → site_caution(부위 → M2) 엣지 속성 〔결정됨〕 | **결정됨** | — |  |
| `zones[].tissue_data.csm_mean_thickness_mm` | 근육 두께 · 섬유 · 덮임(전두근 · 추미근 · 광경근 · DAO) | 부위 | 4 · 속성 → 기법(대상 근육 · 깊이) 근거 수치 〔표시〕 | **표시** | B13 |  |
| `zones[].tissue_data.csm_thickness_variation_mm` | 근육 두께 · 섬유 · 덮임(전두근 · 추미근 · 광경근 · DAO) | 부위 | 4 · 속성 → 기법(대상 근육 · 깊이) 근거 수치 〔표시〕 | **표시** | B13 |  |
| `zones[].filler_specific.emergency_protocol` | 필러 위험 등급 · 주 위험 · 안전 기법 · 점당 최대량 · 권장 제품 · 응급 대응 | 부위 | 8 · 엣지 속성 → site_caution(부위 → M2) 엣지 속성 〔결정됨〕 | **결정됨** | — |  |
| `zones[].tissue_data.stl_entry_point` | 층 · 깊이 · 구조 수치와 설명(피부-골막 · SMAS · 안와격막 · 눈물고랑 · 협지방 · STL) | 부위 | 4 · 속성 → 기법(층 · 깊이 · 주입 지표) 근거 〔표시〕 | **표시** | B13 |  |
| `zones[].tissue_data.pitanguy_line` | 혈관 · 신경 위치 수치(안면동맥 · 입술동맥 · 이신경공 · 하악연지 · 측두지 경로) | 부위 | 8 · 엣지 속성 → 안전 정보(혈관 · 신경 위치) — site_caution 엣지 속성 〔표시〕 | **표시** | B13 |  |
| `zones[].tissue_data.tear_trough_anatomy` | 층 · 깊이 · 구조 수치와 설명(피부-골막 · SMAS · 안와격막 · 눈물고랑 · 협지방 · STL) | 부위 | 4 · 속성 → 기법(층 · 깊이 · 주입 지표) 근거 〔표시〕 | **표시** | B13 |  |
| `zones[].tissue_data.muscle_fiber_data` | 근육 두께 · 섬유 · 덮임(전두근 · 추미근 · 광경근 · DAO) | 부위 | 4 · 속성 → 기법(대상 근육 · 깊이) 근거 수치 〔표시〕 | **표시** | B13 |  |
| `zones[].tissue_data.orbital_septum` | 층 · 깊이 · 구조 수치와 설명(피부-골막 · SMAS · 안와격막 · 눈물고랑 · 협지방 · STL) | 부위 | 4 · 속성 → 기법(층 · 깊이 · 주입 지표) 근거 〔표시〕 | **표시** | B13 |  |
| `zones[].tissue_data.rhinion_subcutaneous_mm` | 층 · 깊이 · 구조 수치와 설명(피부-골막 · SMAS · 안와격막 · 눈물고랑 · 협지방 · STL) | 부위 | 4 · 속성 → 기법(층 · 깊이 · 주입 지표) 근거 〔표시〕 | **표시** | B13 |  |
| `zones[].tissue_data.rhinion_data_source` | 층 · 깊이 · 구조 수치와 설명(피부-골막 · SMAS · 안와격막 · 눈물고랑 · 협지방 · STL) | 부위 | 4 · 속성 → 기법(층 · 깊이 · 주입 지표) 근거 〔표시〕 | **표시** | B13 |  |
| `zones[].tissue_data.nasal_tip_skin_thickness_mm` | 층 · 깊이 · 구조 수치와 설명(피부-골막 · SMAS · 안와격막 · 눈물고랑 · 협지방 · STL) | 부위 | 4 · 속성 → 기법(층 · 깊이 · 주입 지표) 근거 〔표시〕 | **표시** | B13 |  |
| `zones[].tissue_data.facial_artery_distance_to_nlf_mm` | 혈관 · 신경 위치 수치(안면동맥 · 입술동맥 · 이신경공 · 하악연지 · 측두지 경로) | 부위 | 8 · 엣지 속성 → 안전 정보(혈관 · 신경 위치) — site_caution 엣지 속성 〔표시〕 | **표시** | B13 |  |
| `zones[].tissue_data.asian_adjacent_distribution_percent` | 혈관 · 신경 위치 수치(안면동맥 · 입술동맥 · 이신경공 · 하악연지 · 측두지 경로) | 부위 | 8 · 엣지 속성 → 안전 정보(혈관 · 신경 위치) — site_caution 엣지 속성 〔표시〕 | **표시** | B13 |  |
| `zones[].tissue_data.within_5mm_percent` | 혈관 · 신경 위치 수치(안면동맥 · 입술동맥 · 이신경공 · 하악연지 · 측두지 경로) | 부위 | 8 · 엣지 속성 → 안전 정보(혈관 · 신경 위치) — site_caution 엣지 속성 〔표시〕 | **표시** | B13 |  |
| `zones[].tissue_data.facial_artery_diameter_mandible_mm` | 혈관 · 신경 위치 수치(안면동맥 · 입술동맥 · 이신경공 · 하악연지 · 측두지 경로) | 부위 | 8 · 엣지 속성 → 안전 정보(혈관 · 신경 위치) — site_caution 엣지 속성 〔표시〕 | **표시** | B13 |  |
| `zones[].tissue_data.facial_artery_diameter_nasal_mm` | 혈관 · 신경 위치 수치(안면동맥 · 입술동맥 · 이신경공 · 하악연지 · 측두지 경로) | 부위 | 8 · 엣지 속성 → 안전 정보(혈관 · 신경 위치) — site_caution 엣지 속성 〔표시〕 | **표시** | B13 |  |
| `zones[].tissue_data.buccal_fat_pad` | 층 · 깊이 · 구조 수치와 설명(피부-골막 · SMAS · 안와격막 · 눈물고랑 · 협지방 · STL) | 부위 | 4 · 속성 → 기법(층 · 깊이 · 주입 지표) 근거 〔표시〕 | **표시** | B13 |  |
| `zones[].tissue_data.smas_depth_mm` | 층 · 깊이 · 구조 수치와 설명(피부-골막 · SMAS · 안와격막 · 눈물고랑 · 협지방 · STL) | 부위 | 4 · 속성 → 기법(층 · 깊이 · 주입 지표) 근거 〔표시〕 | **표시** | B13 |  |
| `zones[].tissue_data.sub_smas_vs_subcutaneous` | 층 · 깊이 · 구조 수치와 설명(피부-골막 · SMAS · 안와격막 · 눈물고랑 · 협지방 · STL) | 부위 | 4 · 속성 → 기법(층 · 깊이 · 주입 지표) 근거 〔표시〕 | **표시** | B13 |  |
| `zones[].tissue_data.labial_artery_depth_range_mm` | 혈관 · 신경 위치 수치(안면동맥 · 입술동맥 · 이신경공 · 하악연지 · 측두지 경로) | 부위 | 8 · 엣지 속성 → 안전 정보(혈관 · 신경 위치) — site_caution 엣지 속성 〔표시〕 | **표시** | B13 |  |
| `zones[].tissue_data.superior_labial_artery_submucosal_percent` | 혈관 · 신경 위치 수치(안면동맥 · 입술동맥 · 이신경공 · 하악연지 · 측두지 경로) | 부위 | 8 · 엣지 속성 → 안전 정보(혈관 · 신경 위치) — site_caution 엣지 속성 〔표시〕 | **표시** | B13 |  |
| `zones[].tissue_data.mental_foramen_location` | 혈관 · 신경 위치 수치(안면동맥 · 입술동맥 · 이신경공 · 하악연지 · 측두지 경로) | 부위 | 8 · 엣지 속성 → 안전 정보(혈관 · 신경 위치) — site_caution 엣지 속성 〔표시〕 | **표시** | B13 |  |
| `zones[].tissue_data.dao_coverage` | 근육 두께 · 섬유 · 덮임(전두근 · 추미근 · 광경근 · DAO) | 부위 | 4 · 속성 → 기법(대상 근육 · 깊이) 근거 수치 〔표시〕 | **표시** | B13 |  |
| `zones[].tissue_data.marginal_mandibular_depth` | 혈관 · 신경 위치 수치(안면동맥 · 입술동맥 · 이신경공 · 하악연지 · 측두지 경로) | 부위 | 8 · 엣지 속성 → 안전 정보(혈관 · 신경 위치) — site_caution 엣지 속성 〔표시〕 | **표시** | B13 |  |
| `zones[].tissue_data.facial_artery_crossing` | 혈관 · 신경 위치 수치(안면동맥 · 입술동맥 · 이신경공 · 하악연지 · 측두지 경로) | 부위 | 8 · 엣지 속성 → 안전 정보(혈관 · 신경 위치) — site_caution 엣지 속성 〔표시〕 | **표시** | B13 |  |
| `zones[].tissue_data.platysma_thickness_mm` | 근육 두께 · 섬유 · 덮임(전두근 · 추미근 · 광경근 · DAO) | 부위 | 4 · 속성 → 기법(대상 근육 · 깊이) 근거 수치 〔표시〕 | **표시** | B13 |  |
| `zones[].tissue_data.platysma_coverage` | 근육 두께 · 섬유 · 덮임(전두근 · 추미근 · 광경근 · DAO) | 부위 | 4 · 속성 → 기법(대상 근육 · 깊이) 근거 수치 〔표시〕 | **표시** | B13 |  |

### `combo-recipes.json`

| 칸 | 무엇 | 단위 | 행선지 | 상태 | 묶음 | 추천(미정) |
|---|---|---|---|---|---|---|
| `version` | 파일 버전 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `updated` | 파일 갱신일 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `description` | 파일 설명 문장 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `recipes[].id` | 레시피 id · 이름 · 부제 · 강도(7) | 고민 | 7 · 노드 → 추천 조합 노드(종류 = 목적 레시피) 〔미정〕 | **미정** | B07 | 추천 조합 노드 — 고민 단계 뒤(goal 이 고민 대응표를 거쳐야 함) |
| `recipes[].name` | 레시피 id · 이름 · 부제 · 강도(7) | 고민 | 7 · 노드 → 추천 조합 노드(종류 = 목적 레시피) 〔미정〕 | **미정** | B07 | 추천 조합 노드 — 고민 단계 뒤(goal 이 고민 대응표를 거쳐야 함) |
| `recipes[].subtitle` | 레시피 id · 이름 · 부제 · 강도(7) | 고민 | 7 · 노드 → 추천 조합 노드(종류 = 목적 레시피) 〔미정〕 | **미정** | B07 | 추천 조합 노드 — 고민 단계 뒤(goal 이 고민 대응표를 거쳐야 함) |
| `recipes[].goal` | 목적 키(lifting · regeneration · tightening · texture · anti-aging · tone) | 고민 | 7 · 엣지 → 추천 조합 → 고민(목적) — 영문 키 → 고민 대응표 〔미정〕 | **미정** | B08 | 고민 대응표에 6키 추가(lifting → 처짐 · tone → 색소/미백 …) · 사람 확인 게이트 |
| `recipes[].intensity` | 레시피 id · 이름 · 부제 · 강도(7) | 고민 | 7 · 노드 → 추천 조합 노드(종류 = 목적 레시피) 〔미정〕 | **미정** | B07 | 추천 조합 노드 — 고민 단계 뒤(goal 이 고민 대응표를 거쳐야 함) |
| `recipes[].procedures` | 구성 시술군 코드(19) | 계열 | 7 · 엣지 → 추천 조합 includes → 계열(→ 단위 시술은 고민 부위로 내림) 〔미정〕 | **미정** | B07 | includes(계열 · lowering=modality) — treats ② 와 같은 내림 규칙 |
| `recipes[].expectedResults` | 기대 결과 · 반복 주기 문장 | 고민 | 7 · 속성 → 추천 조합 속성 원문 〔미정〕 | **미정** | B07 | 원문 속성 |
| `recipes[].patientExplanation` | 환자 설명 · 비유 문장 | 고민 | 7 · 원문 보관 → 추천 조합 상담 문구 〔미정〕 | **미정** | B07 | 원문 보관 · `kind: 상담 문구`(영업 문구와 달리 기본 응답에 포함) |
| `recipes[].analogy` | 환자 설명 · 비유 문장 | 고민 | 7 · 원문 보관 → 추천 조합 상담 문구 〔미정〕 | **미정** | B07 | 원문 보관 · `kind: 상담 문구`(영업 문구와 달리 기본 응답에 포함) |
| `recipes[].repeatCycle` | 기대 결과 · 반복 주기 문장 | 고민 | 7 · 속성 → 추천 조합 속성 원문 〔미정〕 | **미정** | B07 | 원문 속성 |
| `recipes[].followUp[].week` | 후속 프로토콜 주차 · 할 일(28) | 고민 | 7 · 속성 → 추천 조합 후속 일정(주차 · 할 일 원문) 〔미정〕 | **미정** | B07 | 추천 조합 속성 `follow_up[]` 원문 — 8단계 간격 주장으로 파싱하지 않음 |
| `recipes[].followUp[].action` | 후속 프로토콜 주차 · 할 일(28) | 고민 | 7 · 속성 → 추천 조합 후속 일정(주차 · 할 일 원문) 〔미정〕 | **미정** | B07 | 추천 조합 속성 `follow_up[]` 원문 — 8단계 간격 주장으로 파싱하지 않음 |

### `complications.json`

| 칸 | 무엇 | 단위 | 행선지 | 상태 | 묶음 | 추천(미정) |
|---|---|---|---|---|---|---|
| `severity_levels.mild` | 중증도 값 정의(경미 · 중등도 · 중증 · 위급) | 전역 | 시맨틱 · 속성 → 값 사전(complication.severity 의 뜻) 〔미정〕 | **미정** | B02 | 시맨틱 값 사전 — 노드 아님. 스키마 tool 응답에 싣는다 |
| `severity_levels.moderate` | 중증도 값 정의(경미 · 중등도 · 중증 · 위급) | 전역 | 시맨틱 · 속성 → 값 사전(complication.severity 의 뜻) 〔미정〕 | **미정** | B02 | 시맨틱 값 사전 — 노드 아님. 스키마 tool 응답에 싣는다 |
| `severity_levels.severe` | 중증도 값 정의(경미 · 중등도 · 중증 · 위급) | 전역 | 시맨틱 · 속성 → 값 사전(complication.severity 의 뜻) 〔미정〕 | **미정** | B02 | 시맨틱 값 사전 — 노드 아님. 스키마 tool 응답에 싣는다 |
| `severity_levels.critical` | 중증도 값 정의(경미 · 중등도 · 중증 · 위급) | 전역 | 시맨틱 · 속성 → 값 사전(complication.severity 의 뜻) 〔미정〕 | **미정** | B02 | 시맨틱 값 사전 — 노드 아님. 스키마 tool 응답에 싣는다 |
| `categories[].id` | 합병증 계열 코드 · 이름(10 계열) | 계열 | 8 · 엣지 → has_complication(계열 → 합병증) 끝점 〔결정됨〕 | **결정됨** | B13 |  |
| `categories[].name` | 합병증 계열 코드 · 이름(10 계열) | 계열 | 8 · 엣지 → has_complication(계열 → 합병증) 끝점 〔결정됨〕 | **결정됨** | B13 |  |
| `categories[].complications[].name` | 합병증 이름(65) | 계열 | 8 · 노드 → complication 노드 이름 〔결정됨〕 | **결정됨** | B13 |  |
| `categories[].complications[].severity` | 합병증 중증도 · 발생률 · 발생 시점 · 기전 · 지속 · 처치 · 예방 · 위험 요인 | 계열 | 8 · 속성 → complication 노드 속성(계열마다 따로 — 같은 이름이라도 합치지 않음) 〔결정됨〕 | **결정됨** | B13 |  |
| `categories[].complications[].incidence` | 합병증 중증도 · 발생률 · 발생 시점 · 기전 · 지속 · 처치 · 예방 · 위험 요인 | 계열 | 8 · 속성 → complication 노드 속성(계열마다 따로 — 같은 이름이라도 합치지 않음) 〔결정됨〕 | **결정됨** | B13 |  |
| `categories[].complications[].onset` | 합병증 중증도 · 발생률 · 발생 시점 · 기전 · 지속 · 처치 · 예방 · 위험 요인 | 계열 | 8 · 속성 → complication 노드 속성(계열마다 따로 — 같은 이름이라도 합치지 않음) 〔결정됨〕 | **결정됨** | B13 |  |
| `categories[].complications[].mechanism` | 합병증 중증도 · 발생률 · 발생 시점 · 기전 · 지속 · 처치 · 예방 · 위험 요인 | 계열 | 8 · 속성 → complication 노드 속성(계열마다 따로 — 같은 이름이라도 합치지 않음) 〔결정됨〕 | **결정됨** | B13 |  |
| `categories[].complications[].risk_factors` | 합병증 중증도 · 발생률 · 발생 시점 · 기전 · 지속 · 처치 · 예방 · 위험 요인 | 계열 | 8 · 속성 → complication 노드 속성(계열마다 따로 — 같은 이름이라도 합치지 않음) 〔결정됨〕 | **결정됨** | B13 |  |
| `categories[].complications[].management` | 합병증 중증도 · 발생률 · 발생 시점 · 기전 · 지속 · 처치 · 예방 · 위험 요인 | 계열 | 8 · 속성 → complication 노드 속성(계열마다 따로 — 같은 이름이라도 합치지 않음) 〔결정됨〕 | **결정됨** | B13 |  |
| `categories[].complications[].prevention` | 합병증 중증도 · 발생률 · 발생 시점 · 기전 · 지속 · 처치 · 예방 · 위험 요인 | 계열 | 8 · 속성 → complication 노드 속성(계열마다 따로 — 같은 이름이라도 합치지 않음) 〔결정됨〕 | **결정됨** | B13 |  |
| `categories[].complications[].evidence` | 합병증 근거 URL(38) | 계열 | 8 · 노드 → 근거 노드(URL) + complication → 근거 〔미정〕 | **미정** | B11 | 근거 노드(키 = URL 정규화) — 문헌 근거와 같은 타입, 종류 `웹` |
| `categories[].complications[].duration` | 합병증 중증도 · 발생률 · 발생 시점 · 기전 · 지속 · 처치 · 예방 · 위험 요인 | 계열 | 8 · 속성 → complication 노드 속성(계열마다 따로 — 같은 이름이라도 합치지 않음) 〔결정됨〕 | **결정됨** | B13 |  |

### `consent-checklist.json`

| 칸 | 무엇 | 단위 | 행선지 | 상태 | 묶음 | 추천(미정) |
|---|---|---|---|---|---|---|
| `version` | 파일 버전 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `updated` | 파일 갱신일 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `description` | 파일 설명 문장 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `categories[].id` | 계열 코드 · 이름(17) | 계열 | 8 · 리니지 → 계열 키 〔표시〕 | **표시** | B05 |  |
| `categories[].name` | 계열 코드 · 이름(17) | 계열 | 8 · 리니지 → 계열 키 〔표시〕 | **표시** | B05 |  |
| `categories[].mandatory_disclosures` | 필수 고지 문장(109) | 계열 | 8 · 원문 보관 → 계열 필수 고지 — 원문 그대로(쪼개지 않음) 〔표시〕 | **표시** | B05 |  |
| `categories[].contraindications` | 계열 금기(사람 조건) 문장(105) | 계열 | 8 · 엣지 → 사람 조건 금기(확인 조건 노드 + 계열 → 조건) 〔표시〕 | **표시** | B04 |  |
| `categories[].emergency_signs` | 응급 징후(55) | 계열 | 8 · 속성 → 응급 징후(안전 · 상담 묶음) 〔표시〕 | **표시** | B05 |  |

### `contraindications.json`

| 칸 | 무엇 | 단위 | 행선지 | 상태 | 묶음 | 추천(미정) |
|---|---|---|---|---|---|---|
| `version` | 파일 버전 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `updated` | 파일 갱신일 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `description` | 파일 설명 문장 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `rules[].from` | 시술군 쌍 끝점(코드) | 계열 쌍 | 8 · 엣지 → procedure_relation(계열 ↔ 계열) · 단위 시술로 내림 〔결정됨〕 | **결정됨** | B06 |  |
| `rules[].from_name` | 끝점 이름(보톡스 · 필러) | 계열 쌍 | 8 · 리니지 → evidence 원문 〔결정됨〕 | **결정됨** | B06 |  |
| `rules[].to` | 시술군 쌍 끝점(코드) | 계열 쌍 | 8 · 엣지 → procedure_relation(계열 ↔ 계열) · 단위 시술로 내림 〔결정됨〕 | **결정됨** | B06 |  |
| `rules[].to_name` | 끝점 이름(보톡스 · 필러) | 계열 쌍 | 8 · 리니지 → evidence 원문 〔결정됨〕 | **결정됨** | B06 |  |
| `rules[].level` | 금기 수준(safe · caution · warning) | 계열 쌍 | 8 · 엣지 속성 → procedure_relation 금기 수준 〔결정됨〕 | **결정됨** | B06 |  |
| `rules[].interval` | 간격 문장(같은 날 가능 · 2주 간격 권장) | 계열 쌍 | 8 · 엣지 속성 → procedure_relation 같은 날 · 최소 간격 〔결정됨〕 | **결정됨** | B06 |  |
| `rules[].note` | 순서 · 이유 메모(보톡스 먼저 → 필러) | 계열 쌍 | 8 · 엣지 속성 → procedure_relation 순서(first) · evidence 〔결정됨〕 | **결정됨** | B06 |  |

### `extracted.json`

| 칸 | 무엇 | 단위 | 행선지 | 상태 | 묶음 | 추천(미정) |
|---|---|---|---|---|---|---|
| `{code}.name` | 계열 이름 · 영문 · 원천 시술 id(M10-HIFES) | 계열 | 2 · 리니지 → 계열 동의어 대조(정본 = step2) 〔끝〕 | **끝** | B15 |  |
| `{code}.safety.common` | 계열 설명 · 기전 · 적응증 · 발현 · 부작용(taxonomy 와 같은 칸) | 계열 | 2 · 원문 보관 → taxonomy modality[].extracted 와 대조만(다르면 충돌 기록) 〔미정〕 | **미정** | B15 | 정본 = taxonomy modality[].extracted(SPEC-004 가 이미 씀). 이 파일 값은 원문 보관 · 다른 8 계열 칸은 검증 리포트 `source_conflict` |
| `{code}.safety.serious` | 계열 설명 · 기전 · 적응증 · 발현 · 부작용(taxonomy 와 같은 칸) | 계열 | 2 · 원문 보관 → taxonomy modality[].extracted 와 대조만(다르면 충돌 기록) 〔미정〕 | **미정** | B15 | 정본 = taxonomy modality[].extracted(SPEC-004 가 이미 씀). 이 파일 값은 원문 보관 · 다른 8 계열 칸은 검증 리포트 `source_conflict` |
| `{code}.safety.uncommon` | 계열 설명 · 기전 · 적응증 · 발현 · 부작용(taxonomy 와 같은 칸) | 계열 | 2 · 원문 보관 → taxonomy modality[].extracted 와 대조만(다르면 충돌 기록) 〔미정〕 | **미정** | B15 | 정본 = taxonomy modality[].extracted(SPEC-004 가 이미 씀). 이 파일 값은 원문 보관 · 다른 8 계열 칸은 검증 리포트 `source_conflict` |
| `{code}.source` | 추출 출처 · 종류 · 시각 · 가드레일 버전 | 계열 | 브론즈 · 리니지 → 계열 extracted 속성의 원천 메타 〔미정〕 | **미정** | B15 | taxonomy modality[].extracted 를 정본으로 싣고, 이 파일은 `source` · `source_type` 만 그 속성의 리니지로 붙인다(나머지 메타 원문 보관) |
| `{code}.name_en` | 계열 이름 · 영문 · 원천 시술 id(M10-HIFES) | 계열 | 2 · 리니지 → 계열 동의어 대조(정본 = step2) 〔끝〕 | **끝** | B15 |  |
| `{code}.overview` | 계열 설명 · 기전 · 적응증 · 발현 · 부작용(taxonomy 와 같은 칸) | 계열 | 2 · 원문 보관 → taxonomy modality[].extracted 와 대조만(다르면 충돌 기록) 〔미정〕 | **미정** | B15 | 정본 = taxonomy modality[].extracted(SPEC-004 가 이미 씀). 이 파일 값은 원문 보관 · 다른 8 계열 칸은 검증 리포트 `source_conflict` |
| `{code}.aftercare` | 계열 사후관리(taxonomy 와 같은 칸) | 계열 | 8 · 속성 → 사후관리 안전 정보(중복 원천) 〔표시〕 | **표시** | B05 |  |
| `{code}.mechanism` | 계열 설명 · 기전 · 적응증 · 발현 · 부작용(taxonomy 와 같은 칸) | 계열 | 2 · 원문 보관 → taxonomy modality[].extracted 와 대조만(다르면 충돌 기록) 〔미정〕 | **미정** | B15 | 정본 = taxonomy modality[].extracted(SPEC-004 가 이미 씀). 이 파일 값은 원문 보관 · 다른 8 계열 칸은 검증 리포트 `source_conflict` |
| `{code}.indications.primary` | 계열 설명 · 기전 · 적응증 · 발현 · 부작용(taxonomy 와 같은 칸) | 계열 | 2 · 원문 보관 → taxonomy modality[].extracted 와 대조만(다르면 충돌 기록) 〔미정〕 | **미정** | B15 | 정본 = taxonomy modality[].extracted(SPEC-004 가 이미 씀). 이 파일 값은 원문 보관 · 다른 8 계열 칸은 검증 리포트 `source_conflict` |
| `{code}.indications.extended` | 계열 설명 · 기전 · 적응증 · 발현 · 부작용(taxonomy 와 같은 칸) | 계열 | 2 · 원문 보관 → taxonomy modality[].extracted 와 대조만(다르면 충돌 기록) 〔미정〕 | **미정** | B15 | 정본 = taxonomy modality[].extracted(SPEC-004 가 이미 씀). 이 파일 값은 원문 보관 · 다른 8 계열 칸은 검증 리포트 `source_conflict` |
| `{code}.source_type` | 추출 출처 · 종류 · 시각 · 가드레일 버전 | 계열 | 브론즈 · 리니지 → 계열 extracted 속성의 원천 메타 〔미정〕 | **미정** | B15 | taxonomy modality[].extracted 를 정본으로 싣고, 이 파일은 `source` · `source_type` 만 그 속성의 리니지로 붙인다(나머지 메타 원문 보관) |
| `{code}.extracted_at` | 추출 출처 · 종류 · 시각 · 가드레일 버전 | 계열 | 브론즈 · 리니지 → 계열 extracted 속성의 원천 메타 〔미정〕 | **미정** | B15 | taxonomy modality[].extracted 를 정본으로 싣고, 이 파일은 `source` · `source_type` 만 그 속성의 리니지로 붙인다(나머지 메타 원문 보관) |
| `{code}.procedure_id` | 계열 이름 · 영문 · 원천 시술 id(M10-HIFES) | 계열 | 2 · 리니지 → 계열 동의어 대조(정본 = step2) 〔끝〕 | **끝** | B15 |  |
| `{code}.onset_duration.peak` | 계열 설명 · 기전 · 적응증 · 발현 · 부작용(taxonomy 와 같은 칸) | 계열 | 2 · 원문 보관 → taxonomy modality[].extracted 와 대조만(다르면 충돌 기록) 〔미정〕 | **미정** | B15 | 정본 = taxonomy modality[].extracted(SPEC-004 가 이미 씀). 이 파일 값은 원문 보관 · 다른 8 계열 칸은 검증 리포트 `source_conflict` |
| `{code}.onset_duration.onset` | 계열 설명 · 기전 · 적응증 · 발현 · 부작용(taxonomy 와 같은 칸) | 계열 | 2 · 원문 보관 → taxonomy modality[].extracted 와 대조만(다르면 충돌 기록) 〔미정〕 | **미정** | B15 | 정본 = taxonomy modality[].extracted(SPEC-004 가 이미 씀). 이 파일 값은 원문 보관 · 다른 8 계열 칸은 검증 리포트 `source_conflict` |
| `{code}.onset_duration.duration` | 계열 설명 · 기전 · 적응증 · 발현 · 부작용(taxonomy 와 같은 칸) | 계열 | 2 · 원문 보관 → taxonomy modality[].extracted 와 대조만(다르면 충돌 기록) 〔미정〕 | **미정** | B15 | 정본 = taxonomy modality[].extracted(SPEC-004 가 이미 씀). 이 파일 값은 원문 보관 · 다른 8 계열 칸은 검증 리포트 `source_conflict` |
| `{code}.contraindications.absolute` | 계열 금기(taxonomy 와 같은 칸) | 계열 | 8 · 엣지 → 사람 조건 금기 — taxonomy 쪽과 같은 주장(중복) 〔표시〕 | **표시** | B04 |  |
| `{code}.contraindications.relative` | 계열 금기(taxonomy 와 같은 칸) | 계열 | 8 · 엣지 → 사람 조건 금기 — taxonomy 쪽과 같은 주장(중복) 〔표시〕 | **표시** | B04 |  |
| `{code}.guardrail_version` | 추출 출처 · 종류 · 시각 · 가드레일 버전 | 계열 | 브론즈 · 리니지 → 계열 extracted 속성의 원천 메타 〔미정〕 | **미정** | B15 | taxonomy modality[].extracted 를 정본으로 싣고, 이 파일은 `source` · `source_type` 만 그 속성의 리니지로 붙인다(나머지 메타 원문 보관) |
| `{code}.related_techniques` | 관련 기법 문장(taxonomy 와 같은 칸) | 계열 | 4 · 노드 → 기법 원천 표현(중복) 〔미정〕 | **미정** | B03 | taxonomy 쪽과 같이 4단계 입력 — 중복 제거 |
| `{code}.safety.emergency` | 응급 징후 문장(2 계열 — 필러 혈관 폐색 · 레이저 화상) | 계열 | 8 · 속성 → 응급 징후(안전 · 상담 묶음) 〔표시〕 | **표시** | B05 |  |
| `{code}.updated` | 추출 출처 · 종류 · 시각 · 가드레일 버전 | 계열 | 브론즈 · 리니지 → 계열 extracted 속성의 원천 메타 〔미정〕 | **미정** | B15 | taxonomy modality[].extracted 를 정본으로 싣고, 이 파일은 `source` · `source_type` 만 그 속성의 리니지로 붙인다(나머지 메타 원문 보관) |

### `literature-evidence.json`

| 칸 | 무엇 | 단위 | 행선지 | 상태 | 묶음 | 추천(미정) |
|---|---|---|---|---|---|---|
| `version` | 파일 버전 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `updated` | 파일 갱신일 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `source_method` | 이 파일 내용을 만든 방법(문헌 큐레이션 · AI 합의 등) | 전역 | 브론즈 · 원문 보관 → 브론즈 스냅샷 메타 〔결정됨〕<br>8 · 엣지 속성 → 엣지 근거 종류(source_method) — 강도 칸 재료 〔미정〕 | **미정** | B01 | 근거 종류 값으로 정규화(문헌 / 3-AI 합의 / 큐레이션 / 일반 지식)해 이 파일에서 나온 모든 주장의 `evidence_kind` 로 복사. 강도 숫자는 만들지 않는다 |
| `accuracy_summary.scored_by` | 정확도 채점 주체 · 기준표 | 전역 | 브론즈 · 리니지 → 근거 품질 점수의 뜻(시맨틱 설명) 〔미정〕 | **미정** | B02 | 시맨틱 값 사전(accuracy_score 뜻) 원문 |
| `accuracy_summary.rubric` | 정확도 채점 주체 · 기준표 | 전역 | 브론즈 · 리니지 → 근거 품질 점수의 뜻(시맨틱 설명) 〔미정〕 | **미정** | B02 | 시맨틱 값 사전(accuracy_score 뜻) 원문 |
| `accuracy_summary.overall_average` | 정확도 평균 · 개수 · 번역 비율(파생 집계) | 전역 | 버림 · 버림 → 원문에서 다시 셀 수 있는 집계 〔미정〕 | **미정** | B02 | 버린다 — 근거 노드에서 재계산 가능 |
| `accuracy_summary.n_scored` | 정확도 평균 · 개수 · 번역 비율(파생 집계) | 전역 | 버림 · 버림 → 원문에서 다시 셀 수 있는 집계 〔미정〕 | **미정** | B02 | 버린다 — 근거 노드에서 재계산 가능 |
| `accuracy_summary.by_field_average.moa` | 정확도 평균 · 개수 · 번역 비율(파생 집계) | 전역 | 버림 · 버림 → 원문에서 다시 셀 수 있는 집계 〔미정〕 | **미정** | B02 | 버린다 — 근거 노드에서 재계산 가능 |
| `accuracy_summary.by_field_average.adverse_effects` | 정확도 평균 · 개수 · 번역 비율(파생 집계) | 전역 | 버림 · 버림 → 원문에서 다시 셀 수 있는 집계 〔미정〕 | **미정** | B02 | 버린다 — 근거 노드에서 재계산 가능 |
| `accuracy_summary.by_field_average.effects` | 정확도 평균 · 개수 · 번역 비율(파생 집계) | 전역 | 버림 · 버림 → 원문에서 다시 셀 수 있는 집계 〔미정〕 | **미정** | B02 | 버린다 — 근거 노드에서 재계산 가능 |
| `accuracy_summary.by_category_average.{code}` | 정확도 평균 · 개수 · 번역 비율(파생 집계) | 전역 | 버림 · 버림 → 원문에서 다시 셀 수 있는 집계 〔미정〕 | **미정** | B02 | 버린다 — 근거 노드에서 재계산 가능 |
| `accuracy_summary.patient_ko_coverage` | 정확도 평균 · 개수 · 번역 비율(파생 집계) | 전역 | 버림 · 버림 → 원문에서 다시 셀 수 있는 집계 〔미정〕 | **미정** | B02 | 버린다 — 근거 노드에서 재계산 가능 |
| `accuracy_summary.patient_translations_coverage.ko` | 정확도 평균 · 개수 · 번역 비율(파생 집계) | 전역 | 버림 · 버림 → 원문에서 다시 셀 수 있는 집계 〔미정〕 | **미정** | B02 | 버린다 — 근거 노드에서 재계산 가능 |
| `accuracy_summary.patient_translations_coverage.en` | 정확도 평균 · 개수 · 번역 비율(파생 집계) | 전역 | 버림 · 버림 → 원문에서 다시 셀 수 있는 집계 〔미정〕 | **미정** | B02 | 버린다 — 근거 노드에서 재계산 가능 |
| `accuracy_summary.patient_translations_coverage.zh` | 정확도 평균 · 개수 · 번역 비율(파생 집계) | 전역 | 버림 · 버림 → 원문에서 다시 셀 수 있는 집계 〔미정〕 | **미정** | B02 | 버린다 — 근거 노드에서 재계산 가능 |
| `accuracy_summary.patient_translations_coverage.ja` | 정확도 평균 · 개수 · 번역 비율(파생 집계) | 전역 | 버림 · 버림 → 원문에서 다시 셀 수 있는 집계 〔미정〕 | **미정** | B02 | 버린다 — 근거 노드에서 재계산 가능 |
| `categories.{code}.name` | 문헌 카테고리 이름(영문) | 계열 | 2 · 속성 → 계열 literature_name 〔끝〕 | **끝** | — |  |
| `categories.{code}.moa[].statement` | 작용기전 문헌 문장(50) | 계열 | 2 · 속성 → 계열 정의 근거(literature_evidence) 〔끝〕<br>8 · 노드 → 근거 노드(문장 + 인용) 〔미정〕 | **미정** | B11 | 근거 노드(문장 · 계열 · 종류 moa) — 2단계가 쓴 것은 같은 노드를 가리킴 |
| `categories.{code}.moa[].citations[].authors` | 인용(저자 · 제목 · 학술지 · 연도 · PMID · DOI · PMC · OA URL) | 계열 | 8 · 속성 → 근거 노드 인용 속성(키 = PMID · DOI) 〔미정〕 | **미정** | B11 | 근거 노드 속성 — 같은 PMID 는 한 문헌 노드로 |
| `categories.{code}.moa[].citations[].title` | 인용(저자 · 제목 · 학술지 · 연도 · PMID · DOI · PMC · OA URL) | 계열 | 8 · 속성 → 근거 노드 인용 속성(키 = PMID · DOI) 〔미정〕 | **미정** | B11 | 근거 노드 속성 — 같은 PMID 는 한 문헌 노드로 |
| `categories.{code}.moa[].citations[].journal` | 인용(저자 · 제목 · 학술지 · 연도 · PMID · DOI · PMC · OA URL) | 계열 | 8 · 속성 → 근거 노드 인용 속성(키 = PMID · DOI) 〔미정〕 | **미정** | B11 | 근거 노드 속성 — 같은 PMID 는 한 문헌 노드로 |
| `categories.{code}.moa[].citations[].year` | 인용(저자 · 제목 · 학술지 · 연도 · PMID · DOI · PMC · OA URL) | 계열 | 8 · 속성 → 근거 노드 인용 속성(키 = PMID · DOI) 〔미정〕 | **미정** | B11 | 근거 노드 속성 — 같은 PMID 는 한 문헌 노드로 |
| `categories.{code}.moa[].citations[].pmid` | 인용(저자 · 제목 · 학술지 · 연도 · PMID · DOI · PMC · OA URL) | 계열 | 8 · 속성 → 근거 노드 인용 속성(키 = PMID · DOI) 〔미정〕 | **미정** | B11 | 근거 노드 속성 — 같은 PMID 는 한 문헌 노드로 |
| `categories.{code}.moa[].citations[].doi` | 인용(저자 · 제목 · 학술지 · 연도 · PMID · DOI · PMC · OA URL) | 계열 | 8 · 속성 → 근거 노드 인용 속성(키 = PMID · DOI) 〔미정〕 | **미정** | B11 | 근거 노드 속성 — 같은 PMID 는 한 문헌 노드로 |
| `categories.{code}.moa[].citations[].pmc` | 인용(저자 · 제목 · 학술지 · 연도 · PMID · DOI · PMC · OA URL) | 계열 | 8 · 속성 → 근거 노드 인용 속성(키 = PMID · DOI) 〔미정〕 | **미정** | B11 | 근거 노드 속성 — 같은 PMID 는 한 문헌 노드로 |
| `categories.{code}.moa[].citations[].oa_url` | 인용(저자 · 제목 · 학술지 · 연도 · PMID · DOI · PMC · OA URL) | 계열 | 8 · 속성 → 근거 노드 인용 속성(키 = PMID · DOI) 〔미정〕 | **미정** | B11 | 근거 노드 속성 — 같은 PMID 는 한 문헌 노드로 |
| `categories.{code}.moa[].accuracy_score` | 문장별 정확도 점수 · 메모 | 계열 | 8 · 속성 → 근거 노드 품질 속성 〔미정〕 | **미정** | B11 | 근거 노드 속성(강도 아님 — 내용 정확도) |
| `categories.{code}.moa[].accuracy_note` | 문장별 정확도 점수 · 메모 | 계열 | 8 · 속성 → 근거 노드 품질 속성 〔미정〕 | **미정** | B11 | 근거 노드 속성(강도 아님 — 내용 정확도) |
| `categories.{code}.moa[].patient_ko` | 환자용 문장 4개 언어 | 계열 | 8 · 속성 → 근거 노드 다국어 상담 문장 〔미정〕 | **미정** | B11 | 근거 노드 속성 `patient_text{ko,en,zh,ja}` |
| `categories.{code}.moa[].patient_en` | 환자용 문장 4개 언어 | 계열 | 8 · 속성 → 근거 노드 다국어 상담 문장 〔미정〕 | **미정** | B11 | 근거 노드 속성 `patient_text{ko,en,zh,ja}` |
| `categories.{code}.moa[].patient_zh` | 환자용 문장 4개 언어 | 계열 | 8 · 속성 → 근거 노드 다국어 상담 문장 〔미정〕 | **미정** | B11 | 근거 노드 속성 `patient_text{ko,en,zh,ja}` |
| `categories.{code}.moa[].patient_ja` | 환자용 문장 4개 언어 | 계열 | 8 · 속성 → 근거 노드 다국어 상담 문장 〔미정〕 | **미정** | B11 | 근거 노드 속성 `patient_text{ko,en,zh,ja}` |
| `categories.{code}.moa[].added_at` | 추가일 | 계열 | 브론즈 · 리니지 → 근거 노드 리니지 〔미정〕 | **미정** | B11 | 근거 노드 리니지 |
| `categories.{code}.adverse_effects[].statement` | 부작용 문헌 문장(32) | 계열 | 8 · 노드 → 근거 노드 → complication(결정론 일치 시) · 계열 〔미정〕 | **미정** | B11 | 근거 노드(종류 adverse) · complication 과 이름 일치 시 근거 엣지 |
| `categories.{code}.adverse_effects[].citations[].authors` | 인용(저자 · 제목 · 학술지 · 연도 · PMID · DOI · PMC · OA URL) | 계열 | 8 · 속성 → 근거 노드 인용 속성(키 = PMID · DOI) 〔미정〕 | **미정** | B11 | 근거 노드 속성 — 같은 PMID 는 한 문헌 노드로 |
| `categories.{code}.adverse_effects[].citations[].title` | 인용(저자 · 제목 · 학술지 · 연도 · PMID · DOI · PMC · OA URL) | 계열 | 8 · 속성 → 근거 노드 인용 속성(키 = PMID · DOI) 〔미정〕 | **미정** | B11 | 근거 노드 속성 — 같은 PMID 는 한 문헌 노드로 |
| `categories.{code}.adverse_effects[].citations[].journal` | 인용(저자 · 제목 · 학술지 · 연도 · PMID · DOI · PMC · OA URL) | 계열 | 8 · 속성 → 근거 노드 인용 속성(키 = PMID · DOI) 〔미정〕 | **미정** | B11 | 근거 노드 속성 — 같은 PMID 는 한 문헌 노드로 |
| `categories.{code}.adverse_effects[].citations[].year` | 인용(저자 · 제목 · 학술지 · 연도 · PMID · DOI · PMC · OA URL) | 계열 | 8 · 속성 → 근거 노드 인용 속성(키 = PMID · DOI) 〔미정〕 | **미정** | B11 | 근거 노드 속성 — 같은 PMID 는 한 문헌 노드로 |
| `categories.{code}.adverse_effects[].citations[].pmid` | 인용(저자 · 제목 · 학술지 · 연도 · PMID · DOI · PMC · OA URL) | 계열 | 8 · 속성 → 근거 노드 인용 속성(키 = PMID · DOI) 〔미정〕 | **미정** | B11 | 근거 노드 속성 — 같은 PMID 는 한 문헌 노드로 |
| `categories.{code}.adverse_effects[].citations[].doi` | 인용(저자 · 제목 · 학술지 · 연도 · PMID · DOI · PMC · OA URL) | 계열 | 8 · 속성 → 근거 노드 인용 속성(키 = PMID · DOI) 〔미정〕 | **미정** | B11 | 근거 노드 속성 — 같은 PMID 는 한 문헌 노드로 |
| `categories.{code}.adverse_effects[].citations[].pmc` | 인용(저자 · 제목 · 학술지 · 연도 · PMID · DOI · PMC · OA URL) | 계열 | 8 · 속성 → 근거 노드 인용 속성(키 = PMID · DOI) 〔미정〕 | **미정** | B11 | 근거 노드 속성 — 같은 PMID 는 한 문헌 노드로 |
| `categories.{code}.adverse_effects[].citations[].oa_url` | 인용(저자 · 제목 · 학술지 · 연도 · PMID · DOI · PMC · OA URL) | 계열 | 8 · 속성 → 근거 노드 인용 속성(키 = PMID · DOI) 〔미정〕 | **미정** | B11 | 근거 노드 속성 — 같은 PMID 는 한 문헌 노드로 |
| `categories.{code}.adverse_effects[].accuracy_score` | 문장별 정확도 점수 · 메모 | 계열 | 8 · 속성 → 근거 노드 품질 속성 〔미정〕 | **미정** | B11 | 근거 노드 속성(강도 아님 — 내용 정확도) |
| `categories.{code}.adverse_effects[].accuracy_note` | 문장별 정확도 점수 · 메모 | 계열 | 8 · 속성 → 근거 노드 품질 속성 〔미정〕 | **미정** | B11 | 근거 노드 속성(강도 아님 — 내용 정확도) |
| `categories.{code}.adverse_effects[].patient_ko` | 환자용 문장 4개 언어 | 계열 | 8 · 속성 → 근거 노드 다국어 상담 문장 〔미정〕 | **미정** | B11 | 근거 노드 속성 `patient_text{ko,en,zh,ja}` |
| `categories.{code}.adverse_effects[].patient_en` | 환자용 문장 4개 언어 | 계열 | 8 · 속성 → 근거 노드 다국어 상담 문장 〔미정〕 | **미정** | B11 | 근거 노드 속성 `patient_text{ko,en,zh,ja}` |
| `categories.{code}.adverse_effects[].patient_zh` | 환자용 문장 4개 언어 | 계열 | 8 · 속성 → 근거 노드 다국어 상담 문장 〔미정〕 | **미정** | B11 | 근거 노드 속성 `patient_text{ko,en,zh,ja}` |
| `categories.{code}.adverse_effects[].patient_ja` | 환자용 문장 4개 언어 | 계열 | 8 · 속성 → 근거 노드 다국어 상담 문장 〔미정〕 | **미정** | B11 | 근거 노드 속성 `patient_text{ko,en,zh,ja}` |
| `categories.{code}.adverse_effects[].added_at` | 추가일 | 계열 | 브론즈 · 리니지 → 근거 노드 리니지 〔미정〕 | **미정** | B11 | 근거 노드 리니지 |
| `categories.{code}.effects[].statement` | 효과 문헌 문장(37) | 계열 | 8 · 노드 → 근거 노드 → treats(계열 · 고민) 근거 〔미정〕 | **미정** | B11 | 근거 노드(종류 effect) — treats 엣지의 근거 후보(사람 확인) |
| `categories.{code}.effects[].citations[].authors` | 인용(저자 · 제목 · 학술지 · 연도 · PMID · DOI · PMC · OA URL) | 계열 | 8 · 속성 → 근거 노드 인용 속성(키 = PMID · DOI) 〔미정〕 | **미정** | B11 | 근거 노드 속성 — 같은 PMID 는 한 문헌 노드로 |
| `categories.{code}.effects[].citations[].title` | 인용(저자 · 제목 · 학술지 · 연도 · PMID · DOI · PMC · OA URL) | 계열 | 8 · 속성 → 근거 노드 인용 속성(키 = PMID · DOI) 〔미정〕 | **미정** | B11 | 근거 노드 속성 — 같은 PMID 는 한 문헌 노드로 |
| `categories.{code}.effects[].citations[].journal` | 인용(저자 · 제목 · 학술지 · 연도 · PMID · DOI · PMC · OA URL) | 계열 | 8 · 속성 → 근거 노드 인용 속성(키 = PMID · DOI) 〔미정〕 | **미정** | B11 | 근거 노드 속성 — 같은 PMID 는 한 문헌 노드로 |
| `categories.{code}.effects[].citations[].year` | 인용(저자 · 제목 · 학술지 · 연도 · PMID · DOI · PMC · OA URL) | 계열 | 8 · 속성 → 근거 노드 인용 속성(키 = PMID · DOI) 〔미정〕 | **미정** | B11 | 근거 노드 속성 — 같은 PMID 는 한 문헌 노드로 |
| `categories.{code}.effects[].citations[].pmid` | 인용(저자 · 제목 · 학술지 · 연도 · PMID · DOI · PMC · OA URL) | 계열 | 8 · 속성 → 근거 노드 인용 속성(키 = PMID · DOI) 〔미정〕 | **미정** | B11 | 근거 노드 속성 — 같은 PMID 는 한 문헌 노드로 |
| `categories.{code}.effects[].citations[].doi` | 인용(저자 · 제목 · 학술지 · 연도 · PMID · DOI · PMC · OA URL) | 계열 | 8 · 속성 → 근거 노드 인용 속성(키 = PMID · DOI) 〔미정〕 | **미정** | B11 | 근거 노드 속성 — 같은 PMID 는 한 문헌 노드로 |
| `categories.{code}.effects[].citations[].pmc` | 인용(저자 · 제목 · 학술지 · 연도 · PMID · DOI · PMC · OA URL) | 계열 | 8 · 속성 → 근거 노드 인용 속성(키 = PMID · DOI) 〔미정〕 | **미정** | B11 | 근거 노드 속성 — 같은 PMID 는 한 문헌 노드로 |
| `categories.{code}.effects[].citations[].oa_url` | 인용(저자 · 제목 · 학술지 · 연도 · PMID · DOI · PMC · OA URL) | 계열 | 8 · 속성 → 근거 노드 인용 속성(키 = PMID · DOI) 〔미정〕 | **미정** | B11 | 근거 노드 속성 — 같은 PMID 는 한 문헌 노드로 |
| `categories.{code}.effects[].patient_ko` | 환자용 문장 4개 언어 | 계열 | 8 · 속성 → 근거 노드 다국어 상담 문장 〔미정〕 | **미정** | B11 | 근거 노드 속성 `patient_text{ko,en,zh,ja}` |
| `categories.{code}.effects[].patient_en` | 환자용 문장 4개 언어 | 계열 | 8 · 속성 → 근거 노드 다국어 상담 문장 〔미정〕 | **미정** | B11 | 근거 노드 속성 `patient_text{ko,en,zh,ja}` |
| `categories.{code}.effects[].patient_zh` | 환자용 문장 4개 언어 | 계열 | 8 · 속성 → 근거 노드 다국어 상담 문장 〔미정〕 | **미정** | B11 | 근거 노드 속성 `patient_text{ko,en,zh,ja}` |
| `categories.{code}.effects[].patient_ja` | 환자용 문장 4개 언어 | 계열 | 8 · 속성 → 근거 노드 다국어 상담 문장 〔미정〕 | **미정** | B11 | 근거 노드 속성 `patient_text{ko,en,zh,ja}` |
| `categories.{code}.effects[].added_at` | 추가일 | 계열 | 브론즈 · 리니지 → 근거 노드 리니지 〔미정〕 | **미정** | B11 | 근거 노드 리니지 |
| `categories.{code}.effects[].accuracy_score` | 문장별 정확도 점수 · 메모 | 계열 | 8 · 속성 → 근거 노드 품질 속성 〔미정〕 | **미정** | B11 | 근거 노드 속성(강도 아님 — 내용 정확도) |
| `categories.{code}.effects[].accuracy_note` | 문장별 정확도 점수 · 메모 | 계열 | 8 · 속성 → 근거 노드 품질 속성 〔미정〕 | **미정** | B11 | 근거 노드 속성(강도 아님 — 내용 정확도) |

### `market-pricing.json`

| 칸 | 무엇 | 단위 | 행선지 | 상태 | 묶음 | 추천(미정) |
|---|---|---|---|---|---|---|
| `version` | 파일 버전 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `updated` | 파일 갱신일 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `currency` | 가격 통화(KRW) | 전역 | 5 · 속성 → 시술 1회 가격의 통화 · 단서(가격 칸 메타) 〔결정됨〕 | **결정됨** | B17 |  |
| `note` | 시장가가 참고 범위라는 단서 문장 | 전역 | 5 · 속성 → 시술 1회 가격의 통화 · 단서(가격 칸 메타) 〔결정됨〕 | **결정됨** | B17 |  |
| `categories[].id` | 시장가 분류 = 시술군 코드 · 이름 | 계열 | 2 · 리니지 → 시장가 행의 계열 〔끝〕 | **끝** | — |  |
| `categories[].name` | 시장가 분류 = 시술군 코드 · 이름 | 계열 | 2 · 리니지 → 시장가 행의 계열 〔끝〕 | **끝** | — |  |
| `categories[].items[].name` | 시장가 메뉴 이름(「이마 주름 (수입)」) | 단위 시술 | 3 · 속성 → 부위 문자열(이름 칸) 〔끝〕<br>1 · 속성 → 제품 규격(5_spec.market · 148 제품 행) 〔끝〕<br>5 · 속성 → 시술 1회 = 단위 시술 + 제품(등급) + 규격 쪼개기 〔결정됨〕 | **결정됨** | — |  |
| `categories[].items[].unit` | 규격 · 회차 표기(1회 · 1cc · 900샷 …) | 단위 시술 | 1 · 속성 → 규격(spec raw · amount · unit) 〔끝〕<br>5 · 속성 → 시술 1회 규격 · 회차(OQ-304 정규화) 〔결정됨〕 | **결정됨** | — |  |
| `categories[].items[].low` | 시장가 하 · 중 · 상(원) | 단위 시술 | 5 · 속성 → 시술 1회(단위 시술 + 제품 + 규격) 가격 〔결정됨〕 | **결정됨** | B17 |  |
| `categories[].items[].mid` | 시장가 하 · 중 · 상(원) | 단위 시술 | 5 · 속성 → 시술 1회(단위 시술 + 제품 + 규격) 가격 〔결정됨〕 | **결정됨** | B17 |  |
| `categories[].items[].high` | 시장가 하 · 중 · 상(원) | 단위 시술 | 5 · 속성 → 시술 1회(단위 시술 + 제품 + 규격) 가격 〔결정됨〕 | **결정됨** | B17 |  |

### `patient-education.json`

| 칸 | 무엇 | 단위 | 행선지 | 상태 | 묶음 | 추천(미정) |
|---|---|---|---|---|---|---|
| `version` | 파일 버전 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `updated` | 파일 갱신일 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `categories[].id` | 계열 코드 · 이름(17) | 계열 | 8 · 리니지 → 계열 키 〔표시〕 | **표시** | B05 |  |
| `categories[].name` | 계열 코드 · 이름(17) | 계열 | 8 · 리니지 → 계열 키 〔표시〕 | **표시** | B05 |  |
| `categories[].patient_name` | 환자용 계열 이름(「주름 보톡스」 · 「볼륨 필러」) | 계열 | 2 · 속성 → 계열 동의어(구어 · 상담) — 2단계 정본 synonyms 에 0/17 〔결정됨〕 | **결정됨** | B03 |  |
| `categories[].simple_explanation` | 환자용 쉬운 설명 · 원리 · 지속 · 통증 · 회복 | 계열 | 8 · 속성 → 계열 상담 설명 원문(단위 시술 상속) 〔표시〕 | **표시** | B05 |  |
| `categories[].how_it_works` | 환자용 쉬운 설명 · 원리 · 지속 · 통증 · 회복 | 계열 | 8 · 속성 → 계열 상담 설명 원문(단위 시술 상속) 〔표시〕 | **표시** | B05 |  |
| `categories[].duration_simple` | 환자용 쉬운 설명 · 원리 · 지속 · 통증 · 회복 | 계열 | 8 · 속성 → 계열 상담 설명 원문(단위 시술 상속) 〔표시〕 | **표시** | B05 |  |
| `categories[].pain_level` | 환자용 쉬운 설명 · 원리 · 지속 · 통증 · 회복 | 계열 | 8 · 속성 → 계열 상담 설명 원문(단위 시술 상속) 〔표시〕 | **표시** | B05 |  |
| `categories[].downtime` | 환자용 쉬운 설명 · 원리 · 지속 · 통증 · 회복 | 계열 | 8 · 속성 → 계열 상담 설명 원문(단위 시술 상속) 〔표시〕 | **표시** | B05 |  |
| `categories[].common_concerns[].q` | 자주 묻는 질문 · 답(51) | 계열 | 8 · 속성 → 계열 FAQ 원문 〔표시〕 | **표시** | B05 |  |
| `categories[].common_concerns[].a` | 자주 묻는 질문 · 답(51) | 계열 | 8 · 속성 → 계열 FAQ 원문 〔표시〕 | **표시** | B05 |  |

### `pih-risk.json`

| 칸 | 무엇 | 단위 | 행선지 | 상태 | 묶음 | 추천(미정) |
|---|---|---|---|---|---|---|
| `version` | 파일 버전 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `updated` | 파일 갱신일 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `description` | 파일 설명 문장 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `risk_levels.very_low` | PIH 등급 값 정의(very_low < 1% …) | 전역 | 시맨틱 · 속성 → 값 사전(pih_risk 등급 뜻) 〔미정〕 | **미정** | B02 | 시맨틱 값 사전 |
| `risk_levels.low` | PIH 등급 값 정의(very_low < 1% …) | 전역 | 시맨틱 · 속성 → 값 사전(pih_risk 등급 뜻) 〔미정〕 | **미정** | B02 | 시맨틱 값 사전 |
| `risk_levels.moderate` | PIH 등급 값 정의(very_low < 1% …) | 전역 | 시맨틱 · 속성 → 값 사전(pih_risk 등급 뜻) 〔미정〕 | **미정** | B02 | 시맨틱 값 사전 |
| `risk_levels.high` | PIH 등급 값 정의(very_low < 1% …) | 전역 | 시맨틱 · 속성 → 값 사전(pih_risk 등급 뜻) 〔미정〕 | **미정** | B02 | 시맨틱 값 사전 |
| `risk_levels.very_high` | PIH 등급 값 정의(very_low < 1% …) | 전역 | 시맨틱 · 속성 → 값 사전(pih_risk 등급 뜻) 〔미정〕 | **미정** | B02 | 시맨틱 값 사전 |
| `notes.M1_to_M7` | 「PIH 해당 없음」 계열 메모(M1~M7 · M10 · M16 · M17) | 계열 | 5 · 속성 → 단위 시술 pih_risk = 해당 없음(계열 단위) 〔표시〕 | **표시** | B10 |  |
| `notes.{code}` | 「PIH 해당 없음」 계열 메모(M1~M7 · M10 · M16 · M17) | 계열 | 5 · 속성 → 단위 시술 pih_risk = 해당 없음(계열 단위) 〔표시〕 | **표시** | B10 |  |
| `procedures[].category` | PIH 대상 시술 시술군 · 하위 · 이름 · 원장 항목 id(26) | 원장 항목 | 5 · 리니지 → 원장 항목 → 단위 시술 내림 키 〔표시〕 | **표시** | B10 |  |
| `procedures[].subcategory` | PIH 대상 시술 시술군 · 하위 · 이름 · 원장 항목 id(26) | 원장 항목 | 5 · 리니지 → 원장 항목 → 단위 시술 내림 키 〔표시〕 | **표시** | B10 |  |
| `procedures[].name` | PIH 대상 시술 시술군 · 하위 · 이름 · 원장 항목 id(26) | 원장 항목 | 5 · 리니지 → 원장 항목 → 단위 시술 내림 키 〔표시〕 | **표시** | B10 |  |
| `procedures[].procedure_ref` | PIH 대상 시술 시술군 · 하위 · 이름 · 원장 항목 id(26) | 원장 항목 | 5 · 리니지 → 원장 항목 → 단위 시술 내림 키 〔표시〕 | **표시** | B10 |  |
| `procedures[].pih_risk` | PIH 등급 · 발생률 · 피부 타입 메모 | 원장 항목 | 5 · 속성 → 단위 시술 속성(등급 · 발생률 · 피부 타입) 〔표시〕 | **표시** | B10 |  |
| `procedures[].pih_rate` | PIH 등급 · 발생률 · 피부 타입 메모 | 원장 항목 | 5 · 속성 → 단위 시술 속성(등급 · 발생률 · 피부 타입) 〔표시〕 | **표시** | B10 |  |
| `procedures[].fitzpatrick_note` | PIH 등급 · 발생률 · 피부 타입 메모 | 원장 항목 | 5 · 속성 → 단위 시술 속성(등급 · 발생률 · 피부 타입) 〔표시〕 | **표시** | B10 |  |
| `procedures[].risk_factors` | PIH 위험 요인 · 예방 | 원장 항목 | 8 · 속성 → 안전 정보(PIH 위험 요인 · 예방) 〔표시〕 | **표시** | B05 |  |
| `procedures[].prevention` | PIH 위험 요인 · 예방 | 원장 항목 | 8 · 속성 → 안전 정보(PIH 위험 요인 · 예방) 〔표시〕 | **표시** | B05 |  |

### `post-procedure-timeline.json`

| 칸 | 무엇 | 단위 | 행선지 | 상태 | 묶음 | 추천(미정) |
|---|---|---|---|---|---|---|
| `version` | 파일 버전 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `updated` | 파일 갱신일 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `consensus_method` | 이 파일 내용을 만든 방법(문헌 큐레이션 · AI 합의 등) | 전역 | 브론즈 · 원문 보관 → 브론즈 스냅샷 메타 〔결정됨〕<br>8 · 엣지 속성 → 엣지 근거 종류(source_method) — 강도 칸 재료 〔미정〕 | **미정** | B01 | 근거 종류 값으로 정규화(문헌 / 3-AI 합의 / 큐레이션 / 일반 지식)해 이 파일에서 나온 모든 주장의 `evidence_kind` 로 복사. 강도 숫자는 만들지 않는다 |
| `reaction_levels.normal` | 반응 단계 값 정의(정상 · 이상 · 주의 · 응급) | 전역 | 시맨틱 · 속성 → 값 사전 〔미정〕 | **미정** | B02 | 시맨틱 값 사전 |
| `reaction_levels.abnormal` | 반응 단계 값 정의(정상 · 이상 · 주의 · 응급) | 전역 | 시맨틱 · 속성 → 값 사전 〔미정〕 | **미정** | B02 | 시맨틱 값 사전 |
| `reaction_levels.caution` | 반응 단계 값 정의(정상 · 이상 · 주의 · 응급) | 전역 | 시맨틱 · 속성 → 값 사전 〔미정〕 | **미정** | B02 | 시맨틱 값 사전 |
| `reaction_levels.emergency` | 반응 단계 값 정의(정상 · 이상 · 주의 · 응급) | 전역 | 시맨틱 · 속성 → 값 사전 〔미정〕 | **미정** | B02 | 시맨틱 값 사전 |
| `timelines[].id` | 경과표 id · 시술군(M16-DCA = N1 포함) · 이름(10) | 계열 | 8 · 리니지 → 계열 · 하위 계열 키(ha-filler = M2 HA · M16-DCA = N1) 〔표시〕 | **표시** | B05 |  |
| `timelines[].category` | 경과표 id · 시술군(M16-DCA = N1 포함) · 이름(10) | 계열 | 8 · 리니지 → 계열 · 하위 계열 키(ha-filler = M2 HA · M16-DCA = N1) 〔표시〕 | **표시** | B05 |  |
| `timelines[].name` | 경과표 id · 시술군(M16-DCA = N1 포함) · 이름(10) | 계열 | 8 · 리니지 → 계열 · 하위 계열 키(ha-filler = M2 HA · M16-DCA = N1) 〔표시〕 | **표시** | B05 |  |
| `timelines[].phases[].period` | 경과 구간 · 이름(43) | 계열 | 8 · 속성 → 계열 경과표 원문 〔표시〕 | **표시** | B05 |  |
| `timelines[].phases[].label` | 경과 구간 · 이름(43) | 계열 | 8 · 속성 → 계열 경과표 원문 〔표시〕 | **표시** | B05 |  |
| `timelines[].phases[].normal` | 구간별 정상 · 이상 · 주의 반응 | 계열 | 8 · 속성 → 계열 경과표 원문 〔표시〕 | **표시** | B05 |  |
| `timelines[].phases[].abnormal` | 구간별 정상 · 이상 · 주의 반응 | 계열 | 8 · 속성 → 계열 경과표 원문 〔표시〕 | **표시** | B05 |  |
| `timelines[].phases[].caution` | 구간별 정상 · 이상 · 주의 반응 | 계열 | 8 · 속성 → 계열 경과표 원문 〔표시〕 | **표시** | B05 |  |
| `timelines[].phases[].emergency` | 구간별 응급 반응(94) | 계열 | 8 · 속성 → 응급 징후(경과 구간 표시 포함) 〔표시〕 | **표시** | B05 |  |

### `pre-procedure-checklist.json`

| 칸 | 무엇 | 단위 | 행선지 | 상태 | 묶음 | 추천(미정) |
|---|---|---|---|---|---|---|
| `version` | 파일 버전 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `updated` | 파일 갱신일 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `description` | 파일 설명 문장 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `universal_checks[].id` | 전 시술 공통 확인 항목 id · 이름 · 설명(12) | 전역 | 8 · 노드 → 확인 조건 노드(전 계열 공통) 〔표시〕 | **표시** | B04 |  |
| `universal_checks[].label` | 전 시술 공통 확인 항목 id · 이름 · 설명(12) | 전역 | 8 · 노드 → 확인 조건 노드(전 계열 공통) 〔표시〕 | **표시** | B04 |  |
| `universal_checks[].type` | 확인 종류(must_check · 절대/상대 금기 · counseling · inform) | 전역 | 8 · 엣지 속성 → 조건 엣지 level 〔표시〕 | **표시** | B04 |  |
| `universal_checks[].description` | 전 시술 공통 확인 항목 id · 이름 · 설명(12) | 전역 | 8 · 노드 → 확인 조건 노드(전 계열 공통) 〔표시〕 | **표시** | B04 |  |
| `category_specific[].id` | 계열 코드 · 이름(17) | 계열 | 8 · 리니지 → 계열 키 〔표시〕 | **표시** | B04 |  |
| `category_specific[].name` | 계열 코드 · 이름(17) | 계열 | 8 · 리니지 → 계열 키 〔표시〕 | **표시** | B04 |  |
| `category_specific[].checks[].label` | 계열별 확인 항목(123) | 계열 | 8 · 엣지 → 계열 → 확인 조건(조건 이름 사전으로 정규화) 〔표시〕 | **표시** | B04 |  |
| `category_specific[].checks[].type` | 확인 종류(must_check 66 · 절대 금기 21 · counseling 21 · inform 10 · safety_protocol 5) | 계열 | 8 · 엣지 속성 → 조건 엣지 level 〔표시〕 | **표시** | B04 |  |

### `problem-combos.json`

| 칸 | 무엇 | 단위 | 행선지 | 상태 | 묶음 | 추천(미정) |
|---|---|---|---|---|---|---|
| `version` | 파일 버전 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `updated` | 파일 갱신일 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `description` | 파일 설명 문장 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `combos[].problem_id` | 고민 대분류 id · 이름(8 — 라벨은 taxonomy 와 다름) | 고민 | 7 · 노드 → 고민 노드(P id 로 바로 연결) 〔결정됨〕<br>3 · 속성 → 부위 문자열(이름 칸) 〔끝〕 | **결정됨** | B08 |  |
| `combos[].problem` | 고민 대분류 id · 이름(8 — 라벨은 taxonomy 와 다름) | 고민 | 7 · 노드 → 고민 노드(P id 로 바로 연결) 〔결정됨〕<br>3 · 속성 → 부위 문자열(이름 칸) 〔끝〕 | **결정됨** | B08 |  |
| `combos[].packages[].id` | 패키지 id · 단계(entry · recommended · premium) · 이름(24) | 고민 | 7 · 노드 → 추천 조합 노드(종류 = 고민 패키지) 〔결정됨〕<br>6 · 노드 → 패키지 = 단위 시술 묶음 구성 원천 후보 〔미정〕 | **미정** | B07 | 6단계 「패키지」(병원 메뉴 묶음)가 아니라 고민 앵커 「추천 조합」으로 둔다 — 고민이 먼저 서야 해서 고민 단계 뒤 |
| `combos[].packages[].tier` | 패키지 id · 단계(entry · recommended · premium) · 이름(24) | 고민 | 7 · 노드 → 추천 조합 노드(종류 = 고민 패키지) 〔결정됨〕<br>6 · 노드 → 패키지 = 단위 시술 묶음 구성 원천 후보 〔미정〕 | **미정** | B07 | 6단계 「패키지」(병원 메뉴 묶음)가 아니라 고민 앵커 「추천 조합」으로 둔다 — 고민이 먼저 서야 해서 고민 단계 뒤 |
| `combos[].packages[].tierLabel` | 단계 한글 표시(기본 · 표준 …) | 고민 | 시맨틱 · 속성 → tier 값 사전 한글 이름 〔미정〕 | **미정** | B02 | tier 값 사전(시맨틱) — 행마다 저장하지 않음 |
| `combos[].packages[].name` | 패키지 id · 단계(entry · recommended · premium) · 이름(24) | 고민 | 7 · 노드 → 추천 조합 노드(종류 = 고민 패키지) 〔결정됨〕<br>6 · 노드 → 패키지 = 단위 시술 묶음 구성 원천 후보 〔미정〕 | **미정** | B07 | 6단계 「패키지」(병원 메뉴 묶음)가 아니라 고민 앵커 「추천 조합」으로 둔다 — 고민이 먼저 서야 해서 고민 단계 뒤 |
| `combos[].packages[].procedures` | 패키지 구성 시술군 코드(63) | 계열 | 7 · 엣지 → treats ②(고민 → 계열) 〔결정됨〕 | **결정됨** | B07 |  |
| `combos[].packages[].productTier` | 제품 등급(국산 · 수입) · 제품 이름 문장(「나보타 or 보툴렉스」) | 제품 | 7 · 엣지 속성 → 추천 조합 구성 원소의 제품 후보(1단계 제품 이름 해석) 〔미정〕 | **미정** | B07 | 「or · + 」로 쪼개 1단계 search_names 결정론 일치 → 구성 원소의 `product_candidates` · 등급은 원문 |
| `combos[].packages[].products` | 제품 등급(국산 · 수입) · 제품 이름 문장(「나보타 or 보툴렉스」) | 제품 | 7 · 엣지 속성 → 추천 조합 구성 원소의 제품 후보(1단계 제품 이름 해석) 〔미정〕 | **미정** | B07 | 「or · + 」로 쪼개 1단계 search_names 결정론 일치 → 구성 원소의 `product_candidates` · 등급은 원문 |
| `combos[].packages[].priceRange` | 패키지 가격 범위 문장 | 고민 | 7 · 속성 → 추천 조합 노드 속성 원문(시장가와 별개) 〔미정〕 | **미정** | B07 | 원문 속성 — 시장가(시술 1회)와 합치지 않음 |
| `combos[].packages[].expectedResult` | 기대 결과 · 임상 근거 · 위험 대비 효과 문장 | 고민 | 7 · 엣지 속성 → treats ② evidence · 추천 조합 속성 〔결정됨〕 | **결정됨** | B07 |  |
| `combos[].packages[].salesPitch` | 영업 문구 · 추가 판매 문구 | 고민 | 7 · 원문 보관 → 추천 조합 노드의 상담(영업) 문구 — 기본 응답 제외 〔미정〕 | **미정** | B07 | 원문 보관 · `kind: 영업 문구` 표시 · 골드 기본 응답에서 뺀다(사용자 판단 U3) |
| `combos[].packages[].upsellHook` | 영업 문구 · 추가 판매 문구 | 고민 | 7 · 원문 보관 → 추천 조합 노드의 상담(영업) 문구 — 기본 응답 제외 〔미정〕 | **미정** | B07 | 원문 보관 · `kind: 영업 문구` 표시 · 골드 기본 응답에서 뺀다(사용자 판단 U3) |
| `combos[].packages[].clinicalRationale` | 기대 결과 · 임상 근거 · 위험 대비 효과 문장 | 고민 | 7 · 엣지 속성 → treats ② evidence · 추천 조합 속성 〔결정됨〕 | **결정됨** | B07 |  |
| `combos[].packages[].riskBenefit` | 기대 결과 · 임상 근거 · 위험 대비 효과 문장 | 고민 | 7 · 엣지 속성 → treats ② evidence · 추천 조합 속성 〔결정됨〕 | **결정됨** | B07 |  |

### `problem-packages.json`

| 칸 | 무엇 | 단위 | 행선지 | 상태 | 묶음 | 추천(미정) |
|---|---|---|---|---|---|---|
| `version` | 파일 버전 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `updated` | 파일 갱신일 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `description` | 파일 설명 문장 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `problems[].problem_id` | 고민 대분류 id · 이름(14 — taxonomy 와 같음) | 고민 | 7 · 노드 → 고민 노드(같은 P id) 〔결정됨〕<br>3 · 속성 → 부위 문자열(이름 칸) 〔끝〕 | **결정됨** | B08 |  |
| `problems[].problem` | 고민 대분류 id · 이름(14 — taxonomy 와 같음) | 고민 | 7 · 노드 → 고민 노드(같은 P id) 〔결정됨〕<br>3 · 속성 → 부위 문자열(이름 칸) 〔끝〕 | **결정됨** | B08 |  |
| `problems[].complaints[].cc` | CC 이름 · 꼬리표 · 묶음(115) | 고민 | 3 · 속성 → 부위 문자열(이름 칸) 〔끝〕<br>7 · 노드 → concern_item 매칭(CC = 고민 항목, 115/115) 〔결정됨〕 | **결정됨** | B08 |  |
| `problems[].complaints[].cc_detail` | CC 이름 · 꼬리표 · 묶음(115) | 고민 | 3 · 속성 → 부위 문자열(이름 칸) 〔끝〕<br>7 · 노드 → concern_item 매칭(CC = 고민 항목, 115/115) 〔결정됨〕 | **결정됨** | B08 |  |
| `problems[].complaints[].cc_group` | CC 이름 · 꼬리표 · 묶음(115) | 고민 | 3 · 속성 → 부위 문자열(이름 칸) 〔끝〕<br>7 · 노드 → concern_item 매칭(CC = 고민 항목, 115/115) 〔결정됨〕 | **결정됨** | B08 |  |
| `problems[].complaints[].procedures[].name` | CC 추천 시술 이름 · 시술군(254) | 고민 | 7 · 엣지 → treats ③(CC → 계열 → 부위 맞는 단위 시술) 〔결정됨〕 | **결정됨** | — |  |
| `problems[].complaints[].procedures[].category` | CC 추천 시술 이름 · 시술군(254) | 고민 | 7 · 엣지 → treats ③(CC → 계열 → 부위 맞는 단위 시술) 〔결정됨〕 | **결정됨** | — |  |
| `problems[].complaints[].procedures[].role` | 시술 역할 · 제품 이름(388) | 고민 | 7 · 엣지 속성 → treats ③ evidence(name · role · products) 〔결정됨〕 | **결정됨** | — |  |
| `problems[].complaints[].procedures[].products` | 시술 역할 · 제품 이름(388) | 고민 | 7 · 엣지 속성 → treats ③ evidence(name · role · products) 〔결정됨〕 | **결정됨** | — |  |
| `problems[].complaints[].combos[].name` | CC 안 조합 이름 · 구성(146 · 원소 277) | 고민 | 8 · 엣지 → procedure_relation 시너지 주장 + 조건 concern_item 〔미정〕 | **미정** | B06 | 원소를 계열로 풀어 시너지 주장(conditions.concern_item = 그 CC) · 원천 키 problem-packages · 같은 CC 의 procedures 밖 원소는 검증 리포트(부분집합 위반) |
| `problems[].complaints[].combos[].combo` | CC 안 조합 이름 · 구성(146 · 원소 277) | 고민 | 8 · 엣지 → procedure_relation 시너지 주장 + 조건 concern_item 〔미정〕 | **미정** | B06 | 원소를 계열로 풀어 시너지 주장(conditions.concern_item = 그 CC) · 원천 키 problem-packages · 같은 CC 의 procedures 밖 원소는 검증 리포트(부분집합 위반) |
| `problems[].complaints[].combos[].reason` | 조합 이유 · 근거 문장 | 고민 | 8 · 엣지 속성 → 시너지 주장 evidence 〔미정〕 | **미정** | B06 | 위 주장의 evidence |
| `problems[].complaints[].combos[].evidence` | 조합 이유 · 근거 문장 | 고민 | 8 · 엣지 속성 → 시너지 주장 evidence 〔미정〕 | **미정** | B06 | 위 주장의 evidence |
| `problems[].complaints[].alternatives` | CC 대안 문장(125 — 「실 시술 후 2개월간 HIFU/RF 피할 것」처럼 간격 경고 섞임) | 고민 | 7 · 속성 → concern_item 대안 원문 〔미정〕 | **미정** | B07 | concern_item 속성 원문. 간격 · 금기 문장은 파싱하지 않고 검증 리포트에 「안전 문장 섞임」으로 표시(정본 간격은 treatment-sequence) |

### `procedure-comparison.json`

| 칸 | 무엇 | 단위 | 행선지 | 상태 | 묶음 | 추천(미정) |
|---|---|---|---|---|---|---|
| `version` | 파일 버전 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `updated` | 파일 갱신일 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `comparisons[].id` | 비교표 id · 제목 · 부제(9 — lifting · wrinkle …) | 고민 | 7 · 노드 → 추천 조합 노드(종류 = 비교) + 고민 대응 〔미정〕 | **미정** | B12 | 비교 노드(고민 앵커 · 7단계) — id 영문 키는 고민 대응표로 |
| `comparisons[].title` | 비교표 id · 제목 · 부제(9 — lifting · wrinkle …) | 고민 | 7 · 노드 → 추천 조합 노드(종류 = 비교) + 고민 대응 〔미정〕 | **미정** | B12 | 비교 노드(고민 앵커 · 7단계) — id 영문 키는 고민 대응표로 |
| `comparisons[].subtitle` | 비교표 id · 제목 · 부제(9 — lifting · wrinkle …) | 고민 | 7 · 노드 → 추천 조합 노드(종류 = 비교) + 고민 대응 〔미정〕 | **미정** | B12 | 비교 노드(고민 앵커 · 7단계) — id 영문 키는 고민 대응표로 |
| `comparisons[].evidence_notes` | 비교 근거 메모(3 비교 · 11) | 고민 | 7 · 속성 → 비교 노드 근거 원문 〔미정〕 | **미정** | B12 | 비교 노드 속성 원문 |
| `comparisons[].procedures[].name` | 비교 대상 시술 이름(「울쎄라 (HIFU)」) · 시술군(39) | 이름 | 7 · 엣지 → 비교 노드 → 단위 시술 · 제품(이름 해석) 구성원 엣지 〔미정〕 | **미정** | B12 | §3.3.2 이름 해석(단위 시술 → 계열 → 제품) — 장비 이름이면 제품 + 그 계열 |
| `comparisons[].procedures[].category` | 비교 대상 시술 이름(「울쎄라 (HIFU)」) · 시술군(39) | 이름 | 7 · 엣지 → 비교 노드 → 단위 시술 · 제품(이름 해석) 구성원 엣지 〔미정〕 | **미정** | B12 | §3.3.2 이름 해석(단위 시술 → 계열 → 제품) — 장비 이름이면 제품 + 그 계열 |
| `comparisons[].procedures[].mechanism_simple` | 비교 칸(기전 · 통증 ★ · 회복 · 발현 · 지속 · 비용 · 적합 · 한계 · 아시아 피부) | 이름 | 7 · 엣지 속성 → 비교 구성원 엣지 속성 원문(비교 맥락 값 — 단위 시술 속성과 합치지 않음) 〔미정〕 | **미정** | B12 | 구성원 엣지 속성 원문. 단위 시술 속성(5단계)과 값이 다르면 둘 다 둔다 |
| `comparisons[].procedures[].pain` | 비교 칸(기전 · 통증 ★ · 회복 · 발현 · 지속 · 비용 · 적합 · 한계 · 아시아 피부) | 이름 | 7 · 엣지 속성 → 비교 구성원 엣지 속성 원문(비교 맥락 값 — 단위 시술 속성과 합치지 않음) 〔미정〕 | **미정** | B12 | 구성원 엣지 속성 원문. 단위 시술 속성(5단계)과 값이 다르면 둘 다 둔다 |
| `comparisons[].procedures[].downtime` | 비교 칸(기전 · 통증 ★ · 회복 · 발현 · 지속 · 비용 · 적합 · 한계 · 아시아 피부) | 이름 | 7 · 엣지 속성 → 비교 구성원 엣지 속성 원문(비교 맥락 값 — 단위 시술 속성과 합치지 않음) 〔미정〕 | **미정** | B12 | 구성원 엣지 속성 원문. 단위 시술 속성(5단계)과 값이 다르면 둘 다 둔다 |
| `comparisons[].procedures[].onset` | 비교 칸(기전 · 통증 ★ · 회복 · 발현 · 지속 · 비용 · 적합 · 한계 · 아시아 피부) | 이름 | 7 · 엣지 속성 → 비교 구성원 엣지 속성 원문(비교 맥락 값 — 단위 시술 속성과 합치지 않음) 〔미정〕 | **미정** | B12 | 구성원 엣지 속성 원문. 단위 시술 속성(5단계)과 값이 다르면 둘 다 둔다 |
| `comparisons[].procedures[].duration` | 비교 칸(기전 · 통증 ★ · 회복 · 발현 · 지속 · 비용 · 적합 · 한계 · 아시아 피부) | 이름 | 7 · 엣지 속성 → 비교 구성원 엣지 속성 원문(비교 맥락 값 — 단위 시술 속성과 합치지 않음) 〔미정〕 | **미정** | B12 | 구성원 엣지 속성 원문. 단위 시술 속성(5단계)과 값이 다르면 둘 다 둔다 |
| `comparisons[].procedures[].cost_range` | 비교 칸(기전 · 통증 ★ · 회복 · 발현 · 지속 · 비용 · 적합 · 한계 · 아시아 피부) | 이름 | 7 · 엣지 속성 → 비교 구성원 엣지 속성 원문(비교 맥락 값 — 단위 시술 속성과 합치지 않음) 〔미정〕 | **미정** | B12 | 구성원 엣지 속성 원문. 단위 시술 속성(5단계)과 값이 다르면 둘 다 둔다 |
| `comparisons[].procedures[].best_for` | 비교 칸(기전 · 통증 ★ · 회복 · 발현 · 지속 · 비용 · 적합 · 한계 · 아시아 피부) | 이름 | 7 · 엣지 속성 → 비교 구성원 엣지 속성 원문(비교 맥락 값 — 단위 시술 속성과 합치지 않음) 〔미정〕 | **미정** | B12 | 구성원 엣지 속성 원문. 단위 시술 속성(5단계)과 값이 다르면 둘 다 둔다 |
| `comparisons[].procedures[].limitations` | 비교 칸(기전 · 통증 ★ · 회복 · 발현 · 지속 · 비용 · 적합 · 한계 · 아시아 피부) | 이름 | 7 · 엣지 속성 → 비교 구성원 엣지 속성 원문(비교 맥락 값 — 단위 시술 속성과 합치지 않음) 〔미정〕 | **미정** | B12 | 구성원 엣지 속성 원문. 단위 시술 속성(5단계)과 값이 다르면 둘 다 둔다 |
| `comparisons[].procedures[].pih_risk` | 비교 대상 PIH 등급 | 이름 | 5 · 속성 → pih-risk.json 과 대조(같으면 근거 · 다르면 충돌) 〔미정〕 | **미정** | B10 | pih-risk 가 정본 · 이 값은 대조만 |
| `comparisons[].procedures[].asian_skin_note` | 비교 칸(기전 · 통증 ★ · 회복 · 발현 · 지속 · 비용 · 적합 · 한계 · 아시아 피부) | 이름 | 7 · 엣지 속성 → 비교 구성원 엣지 속성 원문(비교 맥락 값 — 단위 시술 속성과 합치지 않음) 〔미정〕 | **미정** | B12 | 구성원 엣지 속성 원문. 단위 시술 속성(5단계)과 값이 다르면 둘 다 둔다 |

### `procedure-profiles.json`

| 칸 | 무엇 | 단위 | 행선지 | 상태 | 묶음 | 추천(미정) |
|---|---|---|---|---|---|---|
| `version` | 파일 버전 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `updated` | 파일 갱신일 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `description` | 파일 설명 문장 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `profiles[].id` | 프로파일 계열 코드 · 이름 · 영문(17) | 계열 | 2 · 리니지 → 계열 키(정본 = step2) 〔끝〕 | **끝** | — |  |
| `profiles[].name` | 프로파일 계열 코드 · 이름 · 영문(17) | 계열 | 2 · 리니지 → 계열 키(정본 = step2) 〔끝〕 | **끝** | — |  |
| `profiles[].name_en` | 프로파일 계열 코드 · 이름 · 영문(17) | 계열 | 2 · 리니지 → 계열 키(정본 = step2) 〔끝〕 | **끝** | — |  |
| `profiles[].phase` | 세션 단계 · 순서 값(injection 40 …) | 계열 | 8 · 속성 → 계열 session_phase_order — 순서 주장 재료 〔결정됨〕 | **결정됨** | B06 |  |
| `profiles[].phaseOrder` | 세션 단계 · 순서 값(injection 40 …) | 계열 | 8 · 속성 → 계열 session_phase_order — 순서 주장 재료 〔결정됨〕 | **결정됨** | B06 |  |
| `profiles[].mechanism` | 작용 방식 태그(injection · regenerative · thermal …) | 계열 | 4 · 속성 → 기법 상위 축 원천 표현 〔미정〕 | **미정** | B03 | 4단계 기법 조사 입력(계열 기본 방식 태그) — taxonomy group 과 같이 |
| `profiles[].hasProtein` | 순서 · 같은 날 판단 플래그(단백질 · HA · 젤 · 상처 · 채널 · 열 · 출혈 · 부종) | 계열 | 8 · 속성 → 계열 속성 — 시술↔시술 주장 근거(파생 규칙 재료) 〔미정〕 | **미정** | B06 | 계열 속성 원문으로만 싣는다. 이 플래그로 새 엣지를 계산해 만들지 않는다(원천 주장이 아니라 파생 — DEC-001 D-12 결정론이어도 의료 판단) |
| `profiles[].hasHA` | 순서 · 같은 날 판단 플래그(단백질 · HA · 젤 · 상처 · 채널 · 열 · 출혈 · 부종) | 계열 | 8 · 속성 → 계열 속성 — 시술↔시술 주장 근거(파생 규칙 재료) 〔미정〕 | **미정** | B06 | 계열 속성 원문으로만 싣는다. 이 플래그로 새 엣지를 계산해 만들지 않는다(원천 주장이 아니라 파생 — DEC-001 D-12 결정론이어도 의료 판단) |
| `profiles[].usesGel` | 순서 · 같은 날 판단 플래그(단백질 · HA · 젤 · 상처 · 채널 · 열 · 출혈 · 부종) | 계열 | 8 · 속성 → 계열 속성 — 시술↔시술 주장 근거(파생 규칙 재료) 〔미정〕 | **미정** | B06 | 계열 속성 원문으로만 싣는다. 이 플래그로 새 엣지를 계산해 만들지 않는다(원천 주장이 아니라 파생 — DEC-001 D-12 결정론이어도 의료 판단) |
| `profiles[].createsWound` | 순서 · 같은 날 판단 플래그(단백질 · HA · 젤 · 상처 · 채널 · 열 · 출혈 · 부종) | 계열 | 8 · 속성 → 계열 속성 — 시술↔시술 주장 근거(파생 규칙 재료) 〔미정〕 | **미정** | B06 | 계열 속성 원문으로만 싣는다. 이 플래그로 새 엣지를 계산해 만들지 않는다(원천 주장이 아니라 파생 — DEC-001 D-12 결정론이어도 의료 판단) |
| `profiles[].createsChannel` | 순서 · 같은 날 판단 플래그(단백질 · HA · 젤 · 상처 · 채널 · 열 · 출혈 · 부종) | 계열 | 8 · 속성 → 계열 속성 — 시술↔시술 주장 근거(파생 규칙 재료) 〔미정〕 | **미정** | B06 | 계열 속성 원문으로만 싣는다. 이 플래그로 새 엣지를 계산해 만들지 않는다(원천 주장이 아니라 파생 — DEC-001 D-12 결정론이어도 의료 판단) |
| `profiles[].thermalLoad` | 순서 · 같은 날 판단 플래그(단백질 · HA · 젤 · 상처 · 채널 · 열 · 출혈 · 부종) | 계열 | 8 · 속성 → 계열 속성 — 시술↔시술 주장 근거(파생 규칙 재료) 〔미정〕 | **미정** | B06 | 계열 속성 원문으로만 싣는다. 이 플래그로 새 엣지를 계산해 만들지 않는다(원천 주장이 아니라 파생 — DEC-001 D-12 결정론이어도 의료 판단) |
| `profiles[].bleedingRisk` | 순서 · 같은 날 판단 플래그(단백질 · HA · 젤 · 상처 · 채널 · 열 · 출혈 · 부종) | 계열 | 8 · 속성 → 계열 속성 — 시술↔시술 주장 근거(파생 규칙 재료) 〔미정〕 | **미정** | B06 | 계열 속성 원문으로만 싣는다. 이 플래그로 새 엣지를 계산해 만들지 않는다(원천 주장이 아니라 파생 — DEC-001 D-12 결정론이어도 의료 판단) |
| `profiles[].swellingRisk` | 순서 · 같은 날 판단 플래그(단백질 · HA · 젤 · 상처 · 채널 · 열 · 출혈 · 부종) | 계열 | 8 · 속성 → 계열 속성 — 시술↔시술 주장 근거(파생 규칙 재료) 〔미정〕 | **미정** | B06 | 계열 속성 원문으로만 싣는다. 이 플래그로 새 엣지를 계산해 만들지 않는다(원천 주장이 아니라 파생 — DEC-001 D-12 결정론이어도 의료 판단) |
| `profiles[].needsAnesthesia` | 운영 정보(마취 · 자세 · 클렌징 · 준비 시간 · 준비 메모 · 소요 최소/최대) | 계열 | 5 · 속성 → 단위 시술 운영 속성(계열값 상속 · 단위 시술이 덮어쓸 수 있음) 〔미정〕 | **미정** | B10 | 계열 속성으로 싣고 단위 시술은 조회 때 상속(SPEC-004 상속 규칙 재사용) |
| `profiles[].position` | 운영 정보(마취 · 자세 · 클렌징 · 준비 시간 · 준비 메모 · 소요 최소/최대) | 계열 | 5 · 속성 → 단위 시술 운영 속성(계열값 상속 · 단위 시술이 덮어쓸 수 있음) 〔미정〕 | **미정** | B10 | 계열 속성으로 싣고 단위 시술은 조회 때 상속(SPEC-004 상속 규칙 재사용) |
| `profiles[].needsCleansing` | 운영 정보(마취 · 자세 · 클렌징 · 준비 시간 · 준비 메모 · 소요 최소/최대) | 계열 | 5 · 속성 → 단위 시술 운영 속성(계열값 상속 · 단위 시술이 덮어쓸 수 있음) 〔미정〕 | **미정** | B10 | 계열 속성으로 싣고 단위 시술은 조회 때 상속(SPEC-004 상속 규칙 재사용) |
| `profiles[].prepTime` | 운영 정보(마취 · 자세 · 클렌징 · 준비 시간 · 준비 메모 · 소요 최소/최대) | 계열 | 5 · 속성 → 단위 시술 운영 속성(계열값 상속 · 단위 시술이 덮어쓸 수 있음) 〔미정〕 | **미정** | B10 | 계열 속성으로 싣고 단위 시술은 조회 때 상속(SPEC-004 상속 규칙 재사용) |
| `profiles[].prepNotes` | 운영 정보(마취 · 자세 · 클렌징 · 준비 시간 · 준비 메모 · 소요 최소/최대) | 계열 | 5 · 속성 → 단위 시술 운영 속성(계열값 상속 · 단위 시술이 덮어쓸 수 있음) 〔미정〕 | **미정** | B10 | 계열 속성으로 싣고 단위 시술은 조회 때 상속(SPEC-004 상속 규칙 재사용) |
| `profiles[].durationMin` | 운영 정보(마취 · 자세 · 클렌징 · 준비 시간 · 준비 메모 · 소요 최소/최대) | 계열 | 5 · 속성 → 단위 시술 운영 속성(계열값 상속 · 단위 시술이 덮어쓸 수 있음) 〔미정〕 | **미정** | B10 | 계열 속성으로 싣고 단위 시술은 조회 때 상속(SPEC-004 상속 규칙 재사용) |
| `profiles[].durationMax` | 운영 정보(마취 · 자세 · 클렌징 · 준비 시간 · 준비 메모 · 소요 최소/최대) | 계열 | 5 · 속성 → 단위 시술 운영 속성(계열값 상속 · 단위 시술이 덮어쓸 수 있음) 〔미정〕 | **미정** | B10 | 계열 속성으로 싣고 단위 시술은 조회 때 상속(SPEC-004 상속 규칙 재사용) |
| `profiles[].moa_summary` | 기전 요약(순서 관점) | 계열 | 2 · 원문 보관 → 계열 정의는 문헌 기준으로 확정 — 대조용 〔미정〕 | **미정** | B03 | 원문 보관(계열 정의 대체 안 함) |
| `profiles[].practicalNotes` | 실무 메모(「단백질 약물 → 열 시술 뒤에」) | 계열 | 8 · 원문 보관 → 순서 · 간격 근거 문장 〔미정〕 | **미정** | B06 | 계열 속성 원문 — 엣지 파싱 안 함 |
| `profiles[].aftercare` | 사후관리 | 계열 | 8 · 속성 → 사후관리 안전 정보 〔표시〕 | **표시** | B05 |  |

### `products.json`

| 칸 | 무엇 | 단위 | 행선지 | 상태 | 묶음 | 추천(미정) |
|---|---|---|---|---|---|---|
| `version` | 파일 버전 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `updated` | 파일 갱신일 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `description` | 파일 설명 문장 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `{category}.category_id` | 제품 분류의 시술군 코드(문자열 · 배열) | 제품 | 1 · 리니지 → 제품 → 계열(1단계 family · 2단계 판정) 〔끝〕 | **끝** | B15 |  |
| `{category}.products[].name` | 제품 이름 · 영문 · 제조사 · 허가 여부 · 메모 · 성분 · 재질 · 방식 — taxonomy modality[].products 와 같은 59(53쌍 일치) | 제품 | 1 · 원문 보관 → taxonomy products 와 대조(정본 = step1) 〔끝〕 | **끝** | B15 |  |
| `{category}.products[].name_en` | 제품 이름 · 영문 · 제조사 · 허가 여부 · 메모 · 성분 · 재질 · 방식 — taxonomy modality[].products 와 같은 59(53쌍 일치) | 제품 | 1 · 원문 보관 → taxonomy products 와 대조(정본 = step1) 〔끝〕 | **끝** | B15 |  |
| `{category}.products[].manufacturer` | 제품 이름 · 영문 · 제조사 · 허가 여부 · 메모 · 성분 · 재질 · 방식 — taxonomy modality[].products 와 같은 59(53쌍 일치) | 제품 | 1 · 원문 보관 → taxonomy products 와 대조(정본 = step1) 〔끝〕 | **끝** | B15 |  |
| `{category}.products[].country` | 제조사 국가 | 제품 | 1 · 속성 → 제조사 국가 〔결정됨〕 | **결정됨** | — |  |
| `{category}.products[].mfds` | 제품 이름 · 영문 · 제조사 · 허가 여부 · 메모 · 성분 · 재질 · 방식 — taxonomy modality[].products 와 같은 59(53쌍 일치) | 제품 | 1 · 원문 보관 → taxonomy products 와 대조(정본 = step1) 〔끝〕 | **끝** | B15 |  |
| `{category}.products[].note` | 제품 이름 · 영문 · 제조사 · 허가 여부 · 메모 · 성분 · 재질 · 방식 — taxonomy modality[].products 와 같은 59(53쌍 일치) | 제품 | 1 · 원문 보관 → taxonomy products 와 대조(정본 = step1) 〔끝〕 | **끝** | B15 |  |
| `{category}.products[].ingredient` | 제품 이름 · 영문 · 제조사 · 허가 여부 · 메모 · 성분 · 재질 · 방식 — taxonomy modality[].products 와 같은 59(53쌍 일치) | 제품 | 1 · 원문 보관 → taxonomy products 와 대조(정본 = step1) 〔끝〕 | **끝** | B15 |  |
| `{category}.products[].material` | 제품 이름 · 영문 · 제조사 · 허가 여부 · 메모 · 성분 · 재질 · 방식 — taxonomy modality[].products 와 같은 59(53쌍 일치) | 제품 | 1 · 원문 보관 → taxonomy products 와 대조(정본 = step1) 〔끝〕 | **끝** | B15 |  |
| `{category}.products[].type` | 제품 이름 · 영문 · 제조사 · 허가 여부 · 메모 · 성분 · 재질 · 방식 — taxonomy modality[].products 와 같은 59(53쌍 일치) | 제품 | 1 · 원문 보관 → taxonomy products 와 대조(정본 = step1) 〔끝〕 | **끝** | B15 |  |
| `{category}.products[].legal_warning` | 법적 경고 · 규제 상태(2: ASCEplus · EXOSOME SKIN = 화장품 · 주사 금지) | 제품 | 1 · 속성 → 허가 상태 근거(1단계 「허가 대상 아님」 · 확인 불가) 〔끝〕<br>5 · 속성 → 단위 시술 제약 — 이 제품은 「도포」 기법만(주입 단위 시술에 쓰는 제품으로 잇지 않음) 〔미정〕 | **미정** | B16 | 제품에 `allowed_routes: [도포]` 속성 + 5단계 단위 시술 × 제품 조합 만들 때 주입 기법이면 만들지 않는 결정론 가드. 1단계 정본은 고치지 않는다 |
| `{category}.products[].regulatory_status` | 법적 경고 · 규제 상태(2: ASCEplus · EXOSOME SKIN = 화장품 · 주사 금지) | 제품 | 1 · 속성 → 허가 상태 근거(1단계 「허가 대상 아님」 · 확인 불가) 〔끝〕<br>5 · 속성 → 단위 시술 제약 — 이 제품은 「도포」 기법만(주입 단위 시술에 쓰는 제품으로 잇지 않음) 〔미정〕 | **미정** | B16 | 제품에 `allowed_routes: [도포]` 속성 + 5단계 단위 시술 × 제품 조합 만들 때 주입 기법이면 만들지 않는 결정론 가드. 1단계 정본은 고치지 않는다 |

### `synergy.json`

| 칸 | 무엇 | 단위 | 행선지 | 상태 | 묶음 | 추천(미정) |
|---|---|---|---|---|---|---|
| `version` | 파일 버전 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `updated` | 파일 갱신일 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `links[].from` | 시너지 끝점 이름(「M1-사각턱보톡스」 · 「M11-시크릿」) | 이름 | 8 · 엣지 → procedure_relation 끝점 — 오늘은 계열, 단위 시술 해석은 2차 〔결정됨〕 | **결정됨** | B06 |  |
| `links[].from_category` | 끝점 시술군 코드 | 계열 쌍 | 8 · 엣지 → procedure_relation(계열 쌍) 〔결정됨〕 | **결정됨** | B06 |  |
| `links[].to` | 시너지 끝점 이름(「M1-사각턱보톡스」 · 「M11-시크릿」) | 이름 | 8 · 엣지 → procedure_relation 끝점 — 오늘은 계열, 단위 시술 해석은 2차 〔결정됨〕 | **결정됨** | B06 |  |
| `links[].to_category` | 끝점 시술군 코드 | 계열 쌍 | 8 · 엣지 → procedure_relation(계열 쌍) 〔결정됨〕 | **결정됨** | B06 |  |
| `links[].type` | 관계 종류(함께 50 · 다음에 49 · 대신 16) | 계열 쌍 | 8 · 엣지 속성 → 함께 = 같은 날 시너지 · 다음에 = 순서 · 대신 = 대체(시너지 아님) 〔미정〕 | **미정** | B06 | 「대신」 16 은 procedure_relation 의 `alternative=true` 속성으로 분리(시너지 강도에 넣지 않음). 함께 → same_day 주장 · 다음에 → order 주장 |
| `links[].reason` | 시너지 이유 문장 | 계열 쌍 | 8 · 엣지 속성 → procedure_relation evidence 〔결정됨〕 | **결정됨** | B06 |  |
| `links[].timing` | 시점 문장(같은 날 · 2주 간격) | 계열 쌍 | 8 · 엣지 속성 → 같은 날 · 간격 주장 〔결정됨〕 | **결정됨** | B06 |  |
| `links[].target` | 시너지 목표 고민(리프팅 · 안티에이징 … 17종) | 고민 | 7 · 노드 → synergy_target 노드 + 고민 트리 동의어(완전 일치만) 〔결정됨〕 | **결정됨** | B08 |  |

### `taxonomy.json`

| 칸 | 무엇 | 단위 | 행선지 | 상태 | 묶음 | 추천(미정) |
|---|---|---|---|---|---|---|
| `modality[].id` | 시술군 코드 M1~M17 | 계열 | 2 · 속성 → 계열 modality_codes(계열 id) 〔끝〕 | **끝** | — |  |
| `modality[].category` | 시술군 원천 이름(보톡스 · 필러 …) | 계열 | 2 · 속성 → 계열 동의어(원천 이름 · 상담 용어) 〔끝〕 | **끝** | — |  |
| `modality[].category_en` | 시술군 영문 이름 | 계열 | 2 · 속성 → 계열 영문 동의어 · literature_name 대조 〔끝〕 | **끝** | — |  |
| `modality[].group` | 시술군 큰 묶음(주사/주입 · 시술/기기) | 계열 | 4 · 속성 → 기법 상위 축(주입 / 기기) — 계열 기본 투여 방식 〔미정〕 | **미정** | B03 | 4단계 기법의 상위 축(주입 · 기기 · 도포 …) 원천 표현으로 쓰고 계열에는 「기본 방식」 속성으로만 남긴다(2단계 정본은 고치지 않음) |
| `modality[].subcategories[].id` | 시술군 하위 분류 코드(M1-2 등) | 계열 | 2 · 리니지 → 하위 계열 처리 근거(sub_family_handling.source) 〔끝〕 | **끝** | — |  |
| `modality[].subcategories[].label` | 하위 분류 이름(수입 · 국산 · 용도별 · 재질 …) | 계열 | 2 · 속성 → 하위 계열 · 또는 제품 속성으로 판정 〔끝〕<br>3 · 속성 → 부위 문자열(이름 칸) 〔끝〕 | **끝** | — |  |
| `modality[].subcategories[].items[].id` | 원장 항목 id(521) | 원장 항목 | 1 · 리니지 → 제품 원장 ledger_id(343/521) 〔끝〕<br>5 · 리니지 → 단위 시술 source_items · ledger_map(521) 〔결정됨〕 | **결정됨** | — |  |
| `modality[].subcategories[].items[].name` | 원장 항목 이름(제품 · 장비 · 용도별 · 메뉴명) | 원장 항목 | 1 · 속성 → 제품 search_names · ledger_name 〔끝〕<br>3 · 속성 → 부위 문자열(이름 칸) 〔끝〕<br>5 · 속성 → 단위 시술 이름 · 동의어(ledger_item) 〔결정됨〕 | **결정됨** | — |  |
| `modality[].subcategories[].items[].detail` | 원장 항목 꼬리표(제조사 · 특징 · 부위 나열) | 원장 항목 | 1 · 속성 → 제품 정체 근거(1_identity.basis) 〔끝〕<br>3 · 속성 → 부위 문자열(이름 칸) 〔끝〕<br>5 · 속성 → 단위 시술 부위 · 목적 쪼개기 근거 〔결정됨〕 | **결정됨** | — |  |
| `modality[].subcategories[].items[].extracted.overview` | 원장 항목 설명 · 작용기전 문장 | 원장 항목 | 5 · 속성 → 단위 시술 × 제품/장비 「이 제품으로 했을 때」 설명 〔결정됨〕 | **결정됨** | — |  |
| `modality[].subcategories[].items[].extracted.mechanism` | 원장 항목 설명 · 작용기전 문장 | 원장 항목 | 5 · 속성 → 단위 시술 × 제품/장비 「이 제품으로 했을 때」 설명 〔결정됨〕 | **결정됨** | — |  |
| `modality[].subcategories[].items[].extracted.indications.primary` | 원장 항목 적응증 목록 | 원장 항목 | 5 · 속성 → 단위 시술 × 제품 적응증(원문) 〔결정됨〕<br>7 · 엣지 속성 → 고민 → 단위 시술 treats 의 근거 문장(엣지를 새로 만들지는 않음) 〔미정〕 | **미정** | B10 | 적응증은 엣지를 만들지 않고 7단계 고민 어휘 사전과 결정론 일치할 때 treats 주장의 `evidence` 로만 붙인다(gate_status=unconfirmed). 엣지 생성 원천은 목적(용도별) · 큐레이션 원장 |
| `modality[].subcategories[].items[].extracted.indications.extended` | 원장 항목 적응증 목록 | 원장 항목 | 5 · 속성 → 단위 시술 × 제품 적응증(원문) 〔결정됨〕<br>7 · 엣지 속성 → 고민 → 단위 시술 treats 의 근거 문장(엣지를 새로 만들지는 않음) 〔미정〕 | **미정** | B10 | 적응증은 엣지를 만들지 않고 7단계 고민 어휘 사전과 결정론 일치할 때 treats 주장의 `evidence` 로만 붙인다(gate_status=unconfirmed). 엣지 생성 원천은 목적(용도별) · 큐레이션 원장 |
| `modality[].subcategories[].items[].extracted.safety.common` | 원장 항목 부작용 문장(흔함 · 심각 · 장기) | 원장 항목 | 5 · 속성 → 단위 시술 × 제품 부작용 원문 〔결정됨〕<br>8 · 엣지 속성 → has_complication 주장의 근거 문장(정본은 complications.json) 〔미정〕 | **미정** | B13 | 부작용 정본 = complications.json 노드. 이 문장들은 단위 시술 속성 원문으로 두고 complication 노드와는 결정론 일치일 때만 근거로 잇는다 |
| `modality[].subcategories[].items[].extracted.safety.serious` | 원장 항목 부작용 문장(흔함 · 심각 · 장기) | 원장 항목 | 5 · 속성 → 단위 시술 × 제품 부작용 원문 〔결정됨〕<br>8 · 엣지 속성 → has_complication 주장의 근거 문장(정본은 complications.json) 〔미정〕 | **미정** | B13 | 부작용 정본 = complications.json 노드. 이 문장들은 단위 시술 속성 원문으로 두고 complication 노드와는 결정론 일치일 때만 근거로 잇는다 |
| `modality[].subcategories[].items[].extracted.onset_duration.onset` | 원장 항목 발현 · 지속 · 최대 효과 문장 | 원장 항목 | 5 · 속성 → 단위 시술 × 제품 발현/지속 〔결정됨〕 | **결정됨** | — |  |
| `modality[].subcategories[].items[].extracted.onset_duration.duration` | 원장 항목 발현 · 지속 · 최대 효과 문장 | 원장 항목 | 5 · 속성 → 단위 시술 × 제품 발현/지속 〔결정됨〕 | **결정됨** | — |  |
| `modality[].subcategories[].items[].extracted.aftercare` | 원장 항목 사후관리 목록 | 원장 항목 | 5 · 속성 → 단위 시술 × 제품 사후관리 원문 〔결정됨〕<br>8 · 속성 → 사후관리 = 안전 정보(계열 사후관리와 합쳐 상속) 〔표시〕 | **표시** | B05 |  |
| `modality[].subcategories[].items[].extracted.safety.note` | 원장 항목 부작용 문장(흔함 · 심각 · 장기) | 원장 항목 | 5 · 속성 → 단위 시술 × 제품 부작용 원문 〔결정됨〕<br>8 · 엣지 속성 → has_complication 주장의 근거 문장(정본은 complications.json) 〔미정〕 | **미정** | B13 | 부작용 정본 = complications.json 노드. 이 문장들은 단위 시술 속성 원문으로 두고 complication 노드와는 결정론 일치일 때만 근거로 잇는다 |
| `modality[].subcategories[].items[].extracted.onset_duration.peak` | 원장 항목 발현 · 지속 · 최대 효과 문장 | 원장 항목 | 5 · 속성 → 단위 시술 × 제품 발현/지속 〔결정됨〕 | **결정됨** | — |  |
| `modality[].subcategories[].items[].extracted.onset_duration.peak_effect` | 최대 효과 — 다른 키 이름(8항목) | 원장 항목 | 5 · 속성 → onset_duration.peak 와 같은 칸(키 정규화) 〔미정〕 | **미정** | B14 | peak_effect → peak 로 정규화 |
| `modality[].subcategories[].items[].extracted.indications.secondary` | 원장 항목 적응증 목록 | 원장 항목 | 5 · 속성 → 단위 시술 × 제품 적응증(원문) 〔결정됨〕<br>7 · 엣지 속성 → 고민 → 단위 시술 treats 의 근거 문장(엣지를 새로 만들지는 않음) 〔미정〕 | **미정** | B10 | 적응증은 엣지를 만들지 않고 7단계 고민 어휘 사전과 결정론 일치할 때 treats 주장의 `evidence` 로만 붙인다(gate_status=unconfirmed). 엣지 생성 원천은 목적(용도별) · 큐레이션 원장 |
| `modality[].subcategories[].items[].extracted.safety.common_adverse_effects` | 부작용 문장 — 다른 키 이름(2항목) | 원장 항목 | 5 · 속성 → safety.common / serious 와 같은 칸(키 정규화) 〔미정〕 | **미정** | B14 | 적재 때 결정론 키 정규화표(common_adverse_effects → common · serious_adverse_effects → serious)로 합치고 원천 수정 목록에 올린다 |
| `modality[].subcategories[].items[].extracted.safety.serious_adverse_effects` | 부작용 문장 — 다른 키 이름(2항목) | 원장 항목 | 5 · 속성 → safety.common / serious 와 같은 칸(키 정규화) 〔미정〕 | **미정** | B14 | 적재 때 결정론 키 정규화표(common_adverse_effects → common · serious_adverse_effects → serious)로 합치고 원천 수정 목록에 올린다 |
| `modality[].subcategories[].items[].extracted.safety.contraindications` | 원장 항목 금기(사람 조건) 문장(4항목) | 원장 항목 | 8 · 엣지 → 사람 조건 금기(확인 조건 노드 + 시술 → 조건 엣지) 〔표시〕 | **표시** | B04 |  |
| `modality[].subcategories[].items[].verification_needed` | 허가 확인 필요 메모(1) | 원장 항목 | 1 · 리니지 → 1단계 4_license 가 대체(식약처 확인 끝) 〔끝〕 | **끝** | — |  |
| `modality[].subcategories[].items[].extracted.safety.long_term` | 원장 항목 부작용 문장(흔함 · 심각 · 장기) | 원장 항목 | 5 · 속성 → 단위 시술 × 제품 부작용 원문 〔결정됨〕<br>8 · 엣지 속성 → has_complication 주장의 근거 문장(정본은 complications.json) 〔미정〕 | **미정** | B13 | 부작용 정본 = complications.json 노드. 이 문장들은 단위 시술 속성 원문으로 두고 complication 노드와는 결정론 일치일 때만 근거로 잇는다 |
| `modality[].subcategories[].items[].extracted.onset_duration.maintenance` | 원장 항목 발현 · 지속 · 최대 효과 문장 | 원장 항목 | 5 · 속성 → 단위 시술 × 제품 발현/지속 〔결정됨〕 | **결정됨** | — |  |
| `modality[].extracted.overview` | 계열 설명 · 작용기전(환자 말투) | 계열 | 2 · 속성 → 계열 extracted 속성(정의는 문헌 기준으로 이미 확정) 〔결정됨〕 | **결정됨** | — |  |
| `modality[].extracted.mechanism` | 계열 설명 · 작용기전(환자 말투) | 계열 | 2 · 속성 → 계열 extracted 속성(정의는 문헌 기준으로 이미 확정) 〔결정됨〕 | **결정됨** | — |  |
| `modality[].extracted.indications.primary` | 계열 적응증 목록 | 계열 | 2 · 속성 → 계열 extracted 속성 〔결정됨〕<br>7 · 엣지 속성 → 고민 → 계열 treats 근거 문장 〔미정〕 | **미정** | B10 | 원장 항목 적응증과 같은 규칙 — 근거 문장으로만 |
| `modality[].extracted.indications.extended` | 계열 적응증 목록 | 계열 | 2 · 속성 → 계열 extracted 속성 〔결정됨〕<br>7 · 엣지 속성 → 고민 → 계열 treats 근거 문장 〔미정〕 | **미정** | B10 | 원장 항목 적응증과 같은 규칙 — 근거 문장으로만 |
| `modality[].extracted.contraindications.absolute` | 계열 금기(사람 조건) 절대 · 상대 | 계열 | 8 · 엣지 → 사람 조건 금기(확인 조건 노드 + 계열 → 조건 엣지 level 절대/상대) 〔표시〕 | **표시** | B04 |  |
| `modality[].extracted.contraindications.relative` | 계열 금기(사람 조건) 절대 · 상대 | 계열 | 8 · 엣지 → 사람 조건 금기(확인 조건 노드 + 계열 → 조건 엣지 level 절대/상대) 〔표시〕 | **표시** | B04 |  |
| `modality[].extracted.safety.common` | 계열 부작용 문장 | 계열 | 2 · 속성 → 계열 extracted 속성 〔결정됨〕<br>8 · 엣지 속성 → has_complication 근거 문장 〔미정〕 | **미정** | B13 | complications.json 노드가 정본 · 이 문장은 근거 |
| `modality[].extracted.safety.uncommon` | 계열 부작용 문장 | 계열 | 2 · 속성 → 계열 extracted 속성 〔결정됨〕<br>8 · 엣지 속성 → has_complication 근거 문장 〔미정〕 | **미정** | B13 | complications.json 노드가 정본 · 이 문장은 근거 |
| `modality[].extracted.safety.serious` | 계열 부작용 문장 | 계열 | 2 · 속성 → 계열 extracted 속성 〔결정됨〕<br>8 · 엣지 속성 → has_complication 근거 문장 〔미정〕 | **미정** | B13 | complications.json 노드가 정본 · 이 문장은 근거 |
| `modality[].extracted.onset_duration.onset` | 계열 발현 · 최대 · 지속 | 계열 | 2 · 속성 → 계열 extracted 속성 〔결정됨〕 | **결정됨** | — |  |
| `modality[].extracted.onset_duration.peak` | 계열 발현 · 최대 · 지속 | 계열 | 2 · 속성 → 계열 extracted 속성 〔결정됨〕 | **결정됨** | — |  |
| `modality[].extracted.onset_duration.duration` | 계열 발현 · 최대 · 지속 | 계열 | 2 · 속성 → 계열 extracted 속성 〔결정됨〕 | **결정됨** | — |  |
| `modality[].extracted.aftercare` | 계열 사후관리 목록 | 계열 | 8 · 속성 → 사후관리 = 안전 정보(계열 속성 · 단위 시술 상속) 〔표시〕 | **표시** | B05 |  |
| `modality[].extracted.related_techniques` | 계열과 관련된 기법 · 응용 시술 문장(메조보톡스 · 에어보톡스 …) | 계열 | 4 · 노드 → 기법 원천 표현(기법 후보) · 일부는 5단계 단위 시술 이름 〔미정〕 | **미정** | B03 | 4단계 기법 조사 입력에 넣는다 — 「— 」 앞 이름은 기법/단위 시술 후보, 뒤 문장은 근거. 계열 노드에는 붙이지 않음 |
| `modality[].products[].id` | 계열 아래 제품 id(M1-P-0 …, 59) | 제품 | 1 · 리니지 → 제품 원장 taxonomy_product_ids(58/59) 〔끝〕 | **끝** | — |  |
| `modality[].products[].name` | 제품 이름 · 영문 이름 | 제품 | 1 · 속성 → 제품 search_names(한/영) 〔끝〕 | **끝** | — |  |
| `modality[].products[].name_en` | 제품 이름 · 영문 이름 | 제품 | 1 · 속성 → 제품 search_names(한/영) 〔끝〕 | **끝** | — |  |
| `modality[].products[].manufacturer` | 제품 제조사 표기(원천) | 제품 | 1 · 속성 → 6_companies(허가 기준) · 원천 표기는 업체 검색 이름 · 충돌 기록 〔끝〕 | **끝** | — |  |
| `modality[].products[].country` | 제조사 국가 | 제품 | 1 · 속성 → 제조사 원장 국가 필드 〔결정됨〕 | **결정됨** | — |  |
| `modality[].products[].mfds` | 식약처 허가 여부(원천 bool) | 제품 | 1 · 리니지 → 4_license.status 가 대체 〔끝〕 | **끝** | — |  |
| `modality[].products[].extracted.overview` | 제품 설명 · 작용기전 | 제품 | 5 · 속성 → 단위 시술 × 제품 「이 제품으로 했을 때」 〔결정됨〕 | **결정됨** | — |  |
| `modality[].products[].extracted.mechanism` | 제품 설명 · 작용기전 | 제품 | 5 · 속성 → 단위 시술 × 제품 「이 제품으로 했을 때」 〔결정됨〕 | **결정됨** | — |  |
| `modality[].products[].extracted.indications.primary` | 제품 적응증 · 주입층 메모 | 제품 | 5 · 속성 → 단위 시술 × 제품 적응증 〔결정됨〕 | **결정됨** | — |  |
| `modality[].products[].extracted.safety.common` | 제품 부작용 | 제품 | 5 · 속성 → 단위 시술 × 제품 부작용 원문 〔결정됨〕 | **결정됨** | — |  |
| `modality[].products[].extracted.safety.note` | 제품 부작용 | 제품 | 5 · 속성 → 단위 시술 × 제품 부작용 원문 〔결정됨〕 | **결정됨** | — |  |
| `modality[].products[].extracted.onset_duration.onset` | 제품 발현 · 지속 | 제품 | 5 · 속성 → 단위 시술 × 제품 발현/지속 〔결정됨〕 | **결정됨** | — |  |
| `modality[].products[].extracted.onset_duration.duration` | 제품 발현 · 지속 | 제품 | 5 · 속성 → 단위 시술 × 제품 발현/지속 〔결정됨〕 | **결정됨** | — |  |
| `modality[].products[].extracted.aftercare` | 제품 사후관리 | 제품 | 5 · 속성 → 단위 시술 × 제품 사후관리 〔결정됨〕 | **결정됨** | — |  |
| `modality[].products[].extracted.onset_duration.peak_effect` | 제품 최대 효과 — 다른 키(5) | 제품 | 5 · 속성 → peak 와 같은 칸 〔미정〕 | **미정** | B14 | peak_effect → peak |
| `modality[].products[].extracted.onset_duration.diffusion` | 톡신 확산 범위(1U당 cm) | 제품 | 5 · 속성 → 단위 시술 × 제품 확산(안전 참고) 〔결정됨〕 | **결정됨** | — |  |
| `modality[].products[].note` | 제품 메모(수출명 · 「별도 제품 아님」) | 제품 | 1 · 속성 → name_basis · 시술 이름 이동(moved_to) 〔끝〕 | **끝** | — |  |
| `modality[].name` | 시술군 원천 이름(보톡스 · 필러 …) | 계열 | 2 · 속성 → 계열 동의어(원천 이름 · 상담 용어) 〔끝〕 | **끝** | — |  |
| `modality[].products[].extracted.indications.secondary` | 제품 적응증 · 주입층 메모 | 제품 | 5 · 속성 → 단위 시술 × 제품 적응증 〔결정됨〕 | **결정됨** | — |  |
| `modality[].products[].extracted.safety.serious` | 제품 부작용 | 제품 | 5 · 속성 → 단위 시술 × 제품 부작용 원문 〔결정됨〕 | **결정됨** | — |  |
| `modality[].subcategories[].description` | 하위 분류 정의 문장(hADM · DCA 등 3) | 계열 | 2 · 속성 → 하위 계열 정의 근거 〔끝〕 | **끝** | — |  |
| `modality[].products[].ingredient` | 제품 성분 · 재질 · 방식(PLLA · PDO · HIFU · RF …) | 제품 | 2 · 속성 → 하위 계열(재질 · 방식) 판정 근거 〔끝〕<br>1 · 속성 → 제품 성분/원리(DEC-003 필드) 〔결정됨〕 | **결정됨** | — |  |
| `modality[].subcategories[].items[].classification_issue` | 원천 자체의 오분류 · 정정 메모 | 원장 항목 | 2 · 리니지 → 계열 판정 근거(조사 정정) 〔끝〕 | **끝** | — |  |
| `modality[].subcategories[].items[].is_marketing_name` | 마케팅명 표시 · 이름 주의 문장(스킨부스터 6) | 원장 항목 | 5 · 속성 → 단위 시술 이름(마케팅명 = 동의어) · name_status 〔결정됨〕 | **결정됨** | — |  |
| `modality[].subcategories[].items[].ingredient_basis` | 마케팅명 시술의 실제 성분 설명(6) | 원장 항목 | 5 · 속성 → 단위 시술 ingredient 〔결정됨〕 | **결정됨** | — |  |
| `modality[].subcategories[].items[].canonical_category` | 마케팅명 시술의 원천 표준 분류(6) | 원장 항목 | 2 · 리니지 → 계열 · 하위 계열 판정 근거 〔끝〕 | **끝** | — |  |
| `modality[].subcategories[].items[].naming_caveat` | 마케팅명 표시 · 이름 주의 문장(스킨부스터 6) | 원장 항목 | 5 · 속성 → 단위 시술 이름(마케팅명 = 동의어) · name_status 〔결정됨〕 | **결정됨** | — |  |
| `modality[].products[].type` | 제품 성분 · 재질 · 방식(PLLA · PDO · HIFU · RF …) | 제품 | 2 · 속성 → 하위 계열(재질 · 방식) 판정 근거 〔끝〕<br>1 · 속성 → 제품 성분/원리(DEC-003 필드) 〔결정됨〕 | **결정됨** | — |  |
| `modality[].products[].material` | 제품 성분 · 재질 · 방식(PLLA · PDO · HIFU · RF …) | 제품 | 2 · 속성 → 하위 계열(재질 · 방식) 판정 근거 〔끝〕<br>1 · 속성 → 제품 성분/원리(DEC-003 필드) 〔결정됨〕 | **결정됨** | — |  |
| `modality[].products[].extracted.safety.common_side_effects` | 제품 부작용 — 다른 키(1) | 제품 | 5 · 속성 → safety.common 과 같은 칸 〔미정〕 | **미정** | B14 | common_side_effects → common |
| `modality[].products[].extracted.safety.contraindications` | 제품 금기 — 병용 금기 문장(1: PDO+비가교HA) | 제품 | 8 · 엣지 → 시술↔시술 금기 주장(procedure_relation) 〔결정됨〕 | **결정됨** | B06 |  |
| `modality[].subcategories[].items[].correction_note` | 원천 자체의 오분류 · 정정 메모 | 원장 항목 | 2 · 리니지 → 계열 판정 근거(조사 정정) 〔끝〕 | **끝** | — |  |
| `modality[].subcategories[].items[].reclassified_to` | 원천 자체의 오분류 · 정정 메모 | 원장 항목 | 2 · 리니지 → 계열 판정 근거(조사 정정) 〔끝〕 | **끝** | — |  |
| `problem[].id` | 고민 대분류 코드 P1~P14 | 고민 | 7 · 노드 → 고민 노드 id(concern) 〔결정됨〕 | **결정됨** | B08 |  |
| `problem[].category` | 고민 대분류 이름(쁘띠시술 · 주름 · 쳐짐 …) | 고민 | 7 · 노드 → 고민 노드 이름(치환 뒤) 〔결정됨〕<br>3 · 속성 → 부위 문자열(이름 칸) 〔끝〕<br>7 · 노드 → 고민이 아닌 대분류(쁘띠시술 · 제모 · 얼굴윤곽 · 기타) 처리 〔미정〕 | **미정** | B09 | P1 쁘띠시술 · P14 기타 = 고민 노드로 세우지 않음(하위 항목은 부위 + 목적으로 분해) · P10 제모 · P11 얼굴윤곽 = 목적형 고민(「털」 · 「윤곽」)으로 이름만 바꿔 유지 |
| `problem[].category_en` | 고민 대분류 영문 | 고민 | 7 · 속성 → 고민 영문 동의어 〔결정됨〕<br>3 · 속성 → 부위 문자열(이름 칸) 〔끝〕 | **결정됨** | B08 |  |
| `problem[].subcategories[].id` | 고민 중분류 코드(P1-1 …) | 고민 | 7 · 노드 → concern_subcategory id 〔결정됨〕 | **결정됨** | B08 |  |
| `problem[].subcategories[].label` | 고민 중분류 이름(부위 묶음 꼬리표 「이마/관자놀이」 등) | 고민 | 3 · 속성 → 부위 분리(부위 노드 동의어 · 묶음) 〔끝〕<br>7 · 노드 → concern_subcategory 이름(부위를 뗀 고민) 〔결정됨〕 | **결정됨** | B08 |  |
| `problem[].subcategories[].items[].id` | 고민 항목 id(117) | 고민 | 7 · 노드 → concern_item id 〔결정됨〕 | **결정됨** | B08 |  |
| `problem[].subcategories[].items[].name` | 고민 항목 이름 · 꼬리표(「코필러」 · 「콧대/코끝」) | 고민 | 3 · 속성 → 부위 분리 〔끝〕<br>7 · 노드 → concern_item 이름 = 부위 + 고민(+ 계열) 분해 〔결정됨〕 | **결정됨** | B08 |  |
| `problem[].subcategories[].items[].detail` | 고민 항목 이름 · 꼬리표(「코필러」 · 「콧대/코끝」) | 고민 | 3 · 속성 → 부위 분리 〔끝〕<br>7 · 노드 → concern_item 이름 = 부위 + 고민(+ 계열) 분해 〔결정됨〕 | **결정됨** | B08 |  |
| `problem[].subcategories[].items[].modality_ref` | 고민 항목 → 시술군 코드 목록 | 고민 | 7 · 엣지 → treats ①(고민 항목 → 계열 → 부위 맞는 단위 시술) 〔결정됨〕 | **결정됨** | — |  |

### `treatment-optimization.json`

| 칸 | 무엇 | 단위 | 행선지 | 상태 | 묶음 | 추천(미정) |
|---|---|---|---|---|---|---|
| `version` | 파일 버전 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `updated` | 파일 갱신일 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `consensus_method` | 이 파일 내용을 만든 방법(문헌 큐레이션 · AI 합의 등) | 전역 | 브론즈 · 원문 보관 → 브론즈 스냅샷 메타 〔결정됨〕<br>8 · 엣지 속성 → 엣지 근거 종류(source_method) — 강도 칸 재료 〔미정〕 | **미정** | B01 | 근거 종류 값으로 정규화(문헌 / 3-AI 합의 / 큐레이션 / 일반 지식)해 이 파일에서 나온 모든 주장의 `evidence_kind` 로 복사. 강도 숫자는 만들지 않는다 |
| `optimization_principles` | 최적화 원칙(4) | 전역 | 8 · 원문 보관 → 추천 원칙 문장 — 스키마 설명 〔미정〕 | **미정** | B06 | 원문 보관(시맨틱 설명) — 엣지 아님 |
| `by_concern[].concern` | 최적화 고민 이름(8) · 영문 | 고민 | 7 · 노드 → opt_concern 노드 + 고민 트리 동의어(완전 일치만) 〔결정됨〕 | **결정됨** | B08 |  |
| `by_concern[].concern_en` | 최적화 고민 이름(8) · 영문 | 고민 | 7 · 노드 → opt_concern 노드 + 고민 트리 동의어(완전 일치만) 〔결정됨〕 | **결정됨** | B08 |  |
| `by_concern[].icon` | 고민 아이콘 키(UI) | 고민 | 버림 · 버림 → 화면 아이콘 〔미정〕 | **미정** | B02 | 버린다 — 화면용 |
| `by_concern[].severity_levels[].level` | 중증도 단계(경미 · 중등도 · 중증) | 고민 | 7 · 엣지 속성 → treats ④ 조건 `severity` 〔미정〕 | **미정** | B07 | treats ④ 주장의 `conditions.severity` 원문으로 둔다(값 사전은 시맨틱). 받을지 말지는 상담 에이전트 쪽 |
| `by_concern[].severity_levels[].optimal_combo` | 중증도별 최적 조합 시술 이름(74) | 이름 | 7 · 엣지 → treats ④(opt_concern → 단위 시술 · 계열) 〔결정됨〕<br>7 · 노드 → 조합 자체 = 추천 조합 노드(구성 순서 · 묶음) 〔미정〕 | **미정** | B07 | 엣지(treats ④)는 결정대로 두고, 같은 줄 전체를 「추천 조합」 노드(종류 = 중증도별)로도 싣는다 — 묶음이 깨져 원소만 남는 것을 막음 |
| `by_concern[].severity_levels[].sequence` | 조합 순서 · 이유 · 회차 · 기간 | 고민 | 7 · 속성 → 추천 조합 노드 속성(원문) 〔미정〕 | **미정** | B07 | 추천 조합 노드 속성 원문. sequence 문장은 8단계 순서 주장으로 파싱하지 않음(원천이 이미 sequence_order 에 있음) |
| `by_concern[].severity_levels[].rationale` | 조합 순서 · 이유 · 회차 · 기간 | 고민 | 7 · 속성 → 추천 조합 노드 속성(원문) 〔미정〕 | **미정** | B07 | 추천 조합 노드 속성 원문. sequence 문장은 8단계 순서 주장으로 파싱하지 않음(원천이 이미 sequence_order 에 있음) |
| `by_concern[].severity_levels[].expected_sessions` | 조합 순서 · 이유 · 회차 · 기간 | 고민 | 7 · 속성 → 추천 조합 노드 속성(원문) 〔미정〕 | **미정** | B07 | 추천 조합 노드 속성 원문. sequence 문장은 8단계 순서 주장으로 파싱하지 않음(원천이 이미 sequence_order 에 있음) |
| `by_concern[].severity_levels[].total_duration` | 조합 순서 · 이유 · 회차 · 기간 | 고민 | 7 · 속성 → 추천 조합 노드 속성(원문) 〔미정〕 | **미정** | B07 | 추천 조합 노드 속성 원문. sequence 문장은 8단계 순서 주장으로 파싱하지 않음(원천이 이미 sequence_order 에 있음) |
| `by_concern[].severity_levels[].evidence_level` | 근거 수준(high · moderate · low) | 고민 | 7 · 엣지 속성 → treats ④ 강도 칸 〔미정〕 | **미정** | B11 | D-04 강도 칸에 원문 등급 그대로(숫자 만들지 않음) |
| `by_concern[].severity_levels[].contraindicated_combos` | 피해야 할 조합 문장(17) | 이름 | 8 · 엣지 → procedure_relation 금기 주장(이름 풀리면) 〔미정〕 | **미정** | B06 | §3.3.2 이름 해석으로 양 끝 풀리면 금기 주장(원천 키 = treatment-optimization) · 못 풀면 추천 조합 노드 속성 원문 + 검증 리포트 |
| `by_concern[].severity_levels[].caveats` | 주의 단서(엑소좀 미승인 등 2) | 고민 | 7 · 속성 → 추천 조합 노드 안전 단서 원문 〔미정〕 | **미정** | B07 | 추천 조합 노드 속성(안전 단서) · 골드 응답에 함께 |
| `by_age_group[].age` | 연령대(20대 …) | 전역 | 8 · 노드 → 사람 조건 「연령대」(확인 조건) 〔미정〕 | **미정** | B04 | 확인 조건 원장에 연령대 4값 · 추천 조합(연령 플랜)의 조건 |
| `by_age_group[].primary_concerns` | 연령대별 주 고민 · 기본 시술 · 유지 · 초점 · 다음 단계 | 전역 | 7 · 노드 → 추천 조합 노드(종류 = 연령 플랜) · primary_concerns 는 고민 동의어 〔미정〕 | **미정** | B07 | 추천 조합 노드(연령 플랜) 원문 + 조건 연령대. primary_concerns 는 7단계 고민 대응표에 넣는다 |
| `by_age_group[].recommended_base` | 연령대별 주 고민 · 기본 시술 · 유지 · 초점 · 다음 단계 | 전역 | 7 · 노드 → 추천 조합 노드(종류 = 연령 플랜) · primary_concerns 는 고민 동의어 〔미정〕 | **미정** | B07 | 추천 조합 노드(연령 플랜) 원문 + 조건 연령대. primary_concerns 는 7단계 고민 대응표에 넣는다 |
| `by_age_group[].avoid` | 연령대별 피할 것 | 전역 | 8 · 엣지 → 사람 조건(연령대) → 시술 주의 주장 〔미정〕 | **미정** | B04 | 이름 풀리면 조건(연령대) → 계열/단위 시술 「주의」 엣지 · 못 풀면 원문 |
| `by_age_group[].maintenance` | 연령대별 주 고민 · 기본 시술 · 유지 · 초점 · 다음 단계 | 전역 | 7 · 노드 → 추천 조합 노드(종류 = 연령 플랜) · primary_concerns 는 고민 동의어 〔미정〕 | **미정** | B07 | 추천 조합 노드(연령 플랜) 원문 + 조건 연령대. primary_concerns 는 7단계 고민 대응표에 넣는다 |
| `by_age_group[].annual_focus` | 연령대별 주 고민 · 기본 시술 · 유지 · 초점 · 다음 단계 | 전역 | 7 · 노드 → 추천 조합 노드(종류 = 연령 플랜) · primary_concerns 는 고민 동의어 〔미정〕 | **미정** | B07 | 추천 조합 노드(연령 플랜) 원문 + 조건 연령대. primary_concerns 는 7단계 고민 대응표에 넣는다 |
| `by_age_group[].upgrade` | 연령대별 주 고민 · 기본 시술 · 유지 · 초점 · 다음 단계 | 전역 | 7 · 노드 → 추천 조합 노드(종류 = 연령 플랜) · primary_concerns 는 고민 동의어 〔미정〕 | **미정** | B07 | 추천 조합 노드(연령 플랜) 원문 + 조건 연령대. primary_concerns 는 7단계 고민 대응표에 넣는다 |
| `by_age_group[].note` | 연령대별 주 고민 · 기본 시술 · 유지 · 초점 · 다음 단계 | 전역 | 7 · 노드 → 추천 조합 노드(종류 = 연령 플랜) · primary_concerns 는 고민 동의어 〔미정〕 | **미정** | B07 | 추천 조합 노드(연령 플랜) 원문 + 조건 연령대. primary_concerns 는 7단계 고민 대응표에 넣는다 |
| `combination_rules[].rule` | 조합 규칙 이름 · 내용(8) | 계열 쌍 | 8 · 엣지 → procedure_relation 순서 · 간격 · 금기 주장(이름 풀리면) 〔미정〕 | **미정** | B06 | 규칙 8개는 수작업 대응표(규칙 → 계열 쌍 · 주장 종류)로 주장화 — 결정론 파싱 불가 문장이라 표를 원천 수정 목록처럼 게이트에 올린다 |
| `combination_rules[].detail` | 조합 규칙 이름 · 내용(8) | 계열 쌍 | 8 · 엣지 → procedure_relation 순서 · 간격 · 금기 주장(이름 풀리면) 〔미정〕 | **미정** | B06 | 규칙 8개는 수작업 대응표(규칙 → 계열 쌍 · 주장 종류)로 주장화 — 결정론 파싱 불가 문장이라 표를 원천 수정 목록처럼 게이트에 올린다 |
| `combination_rules[].evidence` | 조합 규칙 근거 · 합의 표시 | 계열 쌍 | 8 · 노드 → 근거 노드 · 엣지 근거 종류 〔미정〕 | **미정** | B11 | 근거 노드 + evidence_kind(합의 표시) |
| `combination_rules[].consensus` | 조합 규칙 근거 · 합의 표시 | 계열 쌍 | 8 · 노드 → 근거 노드 · 엣지 근거 종류 〔미정〕 | **미정** | B11 | 근거 노드 + evidence_kind(합의 표시) |
| `combination_rules[].priority` | 규칙 중요도(critical · moderate …) | 계열 쌍 | 8 · 엣지 속성 → 주장 강도 〔미정〕 | **미정** | B11 | 강도 칸에 원문 등급 |
| `annual_plans[].plan_name` | 연간 플랜 이름 · 연령 · 예산 · 초점 · 월 · 월별 시술(회차 포함) | 전역 | 7 · 노드 → 추천 조합 노드(종류 = 연간 플랜) + 월별 구성 〔미정〕 | **미정** | B07 | 추천 조합 노드(연간 플랜). 월별 「토닝 4회」 = 단위 시술 이름 + 회차(5단계 해석) |
| `annual_plans[].age_group` | 연간 플랜 이름 · 연령 · 예산 · 초점 · 월 · 월별 시술(회차 포함) | 전역 | 7 · 노드 → 추천 조합 노드(종류 = 연간 플랜) + 월별 구성 〔미정〕 | **미정** | B07 | 추천 조합 노드(연간 플랜). 월별 「토닝 4회」 = 단위 시술 이름 + 회차(5단계 해석) |
| `annual_plans[].annual_budget_range` | 연간 플랜 이름 · 연령 · 예산 · 초점 · 월 · 월별 시술(회차 포함) | 전역 | 7 · 노드 → 추천 조합 노드(종류 = 연간 플랜) + 월별 구성 〔미정〕 | **미정** | B07 | 추천 조합 노드(연간 플랜). 월별 「토닝 4회」 = 단위 시술 이름 + 회차(5단계 해석) |
| `annual_plans[].focus` | 연간 플랜 이름 · 연령 · 예산 · 초점 · 월 · 월별 시술(회차 포함) | 전역 | 7 · 노드 → 추천 조합 노드(종류 = 연간 플랜) + 월별 구성 〔미정〕 | **미정** | B07 | 추천 조합 노드(연간 플랜). 월별 「토닝 4회」 = 단위 시술 이름 + 회차(5단계 해석) |
| `annual_plans[].schedule[].month` | 연간 플랜 이름 · 연령 · 예산 · 초점 · 월 · 월별 시술(회차 포함) | 전역 | 7 · 노드 → 추천 조합 노드(종류 = 연간 플랜) + 월별 구성 〔미정〕 | **미정** | B07 | 추천 조합 노드(연간 플랜). 월별 「토닝 4회」 = 단위 시술 이름 + 회차(5단계 해석) |
| `annual_plans[].schedule[].procedures` | 연간 플랜 이름 · 연령 · 예산 · 초점 · 월 · 월별 시술(회차 포함) | 전역 | 7 · 노드 → 추천 조합 노드(종류 = 연간 플랜) + 월별 구성 〔미정〕 | **미정** | B07 | 추천 조합 노드(연간 플랜). 월별 「토닝 4회」 = 단위 시술 이름 + 회차(5단계 해석) |

### `treatment-sequence.json`

| 칸 | 무엇 | 단위 | 행선지 | 상태 | 묶음 | 추천(미정) |
|---|---|---|---|---|---|---|
| `version` | 파일 버전 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `updated` | 파일 갱신일 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `description` | 파일 설명 문장 | 전역 | 브론즈 · 리니지 → 브론즈 스냅샷 메타(엣지 · 속성의 원천 버전) 〔결정됨〕 | **결정됨** | B01 |  |
| `principles` | 같은 세션 순서 원칙 문장(13) | 전역 | 8 · 원문 보관 → 전역 순서 원칙 — 스키마 설명 · 근거 〔미정〕 | **미정** | B06 | 원문 보관 + 시맨틱 「순서 규칙 설명」 — 엣지로 만들지 않음(sequence_order 가 구조화본) |
| `sequence_order[].order` | 세션 순서 단계 번호 · 이름(11) | 계열 | 8 · 엣지 속성 → procedure_relation 순서(first) — v1 규칙 〔결정됨〕 | **결정됨** | B06 |  |
| `sequence_order[].phase` | 세션 순서 단계 번호 · 이름(11) | 계열 | 8 · 엣지 속성 → procedure_relation 순서(first) — v1 규칙 〔결정됨〕 | **결정됨** | B06 |  |
| `sequence_order[].categories` | 단계에 든 시술(「M9-HIFU」 · 「M15-클렌징」 · 「국소마취」) | 이름 | 8 · 엣지 → 순서 끝점 — 오늘은 계열(코드 앞부분) 〔결정됨〕<br>4 · 속성 → 「-HIFU」 · 「-도포」 · 「국소마취」 꼬리 = 하위 계열 · 기법 · 마취 〔미정〕 | **미정** | B06 | 꼬리는 4단계 기법 / 2단계 하위 계열 사전으로 풀어 순서 주장의 `conditions.sub` 로 둔다. 마취 · 클렌징 · 진정은 단위 시술이 아니라 세션 단계라 엣지 끝점에서 뺀다 |
| `sequence_order[].reason` | 순서 이유 | 계열 | 8 · 엣지 속성 → evidence 〔결정됨〕 | **결정됨** | B06 |  |
| `incompatible_same_day[].pair` | 같은 날 불가 쌍(9 — 이소트레티노인 복용 중 3 포함) | 이름 | 8 · 엣지 → procedure_relation same_day=false 〔결정됨〕<br>8 · 엣지 → 「이소트레티노인 복용 중」 3쌍 = 사람 조건 금기(시술쌍 아님) 〔표시〕 | **표시** | B04 |  |
| `incompatible_same_day[].reason` | 같은 날 불가 이유 | 이름 | 8 · 엣지 속성 → evidence 〔결정됨〕 | **결정됨** | B06 |  |
| `common_combos[].name` | 흔한 조합 이름 · 순서(시술 이름) · 총 소요 · 메모(8) | 이름 | 7 · 노드 → 추천 조합 노드(종류 = 세션 조합) + 구성 단위 시술 순서 엣지 〔미정〕 | **미정** | B07 | 큐레이션 「추천 조합」 노드 한 타입(원천 표시)으로 싣고 sequence[] 는 이름 → 단위 시술 해석(5단계) 뒤 includes(순서 번호) 엣지 |
| `common_combos[].sequence` | 흔한 조합 이름 · 순서(시술 이름) · 총 소요 · 메모(8) | 이름 | 7 · 노드 → 추천 조합 노드(종류 = 세션 조합) + 구성 단위 시술 순서 엣지 〔미정〕 | **미정** | B07 | 큐레이션 「추천 조합」 노드 한 타입(원천 표시)으로 싣고 sequence[] 는 이름 → 단위 시술 해석(5단계) 뒤 includes(순서 번호) 엣지 |
| `common_combos[].total_time` | 흔한 조합 이름 · 순서(시술 이름) · 총 소요 · 메모(8) | 이름 | 7 · 노드 → 추천 조합 노드(종류 = 세션 조합) + 구성 단위 시술 순서 엣지 〔미정〕 | **미정** | B07 | 큐레이션 「추천 조합」 노드 한 타입(원천 표시)으로 싣고 sequence[] 는 이름 → 단위 시술 해석(5단계) 뒤 includes(순서 번호) 엣지 |
| `common_combos[].note` | 흔한 조합 이름 · 순서(시술 이름) · 총 소요 · 메모(8) | 이름 | 7 · 노드 → 추천 조합 노드(종류 = 세션 조합) + 구성 단위 시술 순서 엣지 〔미정〕 | **미정** | B07 | 큐레이션 「추천 조합」 노드 한 타입(원천 표시)으로 싣고 sequence[] 는 이름 → 단위 시술 해석(5단계) 뒤 includes(순서 번호) 엣지 |
| `minimum_intervals[].from` | 최소 간격 끝점 이름(HA 필러 · 이소트레티노인 …) | 이름 | 8 · 엣지 → procedure_relation 최소 간격 끝점 〔결정됨〕<br>8 · 엣지 → 「이소트레티노인」 2쌍 = 사람 조건(복용 후 간격) 〔표시〕 | **표시** | B04 |  |
| `minimum_intervals[].to` | 최소 간격 끝점 이름(HA 필러 · 이소트레티노인 …) | 이름 | 8 · 엣지 → procedure_relation 최소 간격 끝점 〔결정됨〕<br>8 · 엣지 → 「이소트레티노인」 2쌍 = 사람 조건(복용 후 간격) 〔표시〕 | **표시** | B04 |  |
| `minimum_intervals[].min_days` | 최소 간격 일 · 개월 | 이름 | 8 · 엣지 속성 → procedure_relation 최소 간격 〔결정됨〕 | **결정됨** | B06 |  |
| `minimum_intervals[].source` | 간격 출처 문자열(JCD 2023 · ASDS 2024 · 임상 가이드) | 이름 | 8 · 노드 → 근거 노드 + 엣지 근거 칸 〔미정〕 | **미정** | B11 | 근거 노드(문자열 그대로 · 문헌 식별자 없으면 종류 `가이드 표기`) |
| `minimum_intervals[].reason` | 간격 이유 | 이름 | 8 · 엣지 속성 → evidence 〔결정됨〕 | **결정됨** | B06 |  |
| `minimum_intervals[].min_months` | 최소 간격 일 · 개월 | 이름 | 8 · 엣지 속성 → procedure_relation 최소 간격 〔결정됨〕 | **결정됨** | B06 |  |

## 근거 약어

- `_RESUME §2` 결정 표 행(날짜 · 따옴표 구절) · DEC-001 D-02/03/04/06/12/13b/13d/13e · OQ-104/105/110/111/114/119/120 · DEC-002 D-03/04/07 · OQ-201/204 · DEC-003 D-01/02 · OQ-304/312/313 · SPEC-004 §3.1.1 · §3.2.4 · §3.2.5 · §3.3.2 · §3.3.3 B/C/D · §8 · OQ-G04/G15 · SPEC-001 OQ-S02
- 정본: `step1-products.json` · `step2-families.json` · `step3-sites.json`(이름 칸 17 = `step3-decisions.json` name_fields) · 5단계 초안 `procedure-master-v3.json`
- 셈 스크립트는 조사용(레포 밖 scratchpad) — 이 지도는 결정론 재빌드 대상이 아니다

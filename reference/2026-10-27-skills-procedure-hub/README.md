# Procedure Hub 스킬 모음

Procedure Hub 실버 원장 작업(`orchestration/work/phub-recommend/`)에서 실제로 한 방법을 Claude Code 스킬로 옮긴 것.
단계 순서대로 여덟이다 — 1단계 제품 확인 → 2단계 계열 판정 → 3단계 부위 판정 → 4단계 기법 판정 → 5단계 단위 시술 판정 → 6단계 패키지 판정 → 7단계 고민 판정 → 8단계 관계 판정. 새 행 · 허가 품목이 바뀐 행은 product-check 다음에 family-check 로 넘기고, 새 메뉴 · 이름 칸이 바뀌어 부위 문자열이 생기면 site-check 로, 지도(`source-map.json`) 4단계 칸에 새 기법 표현이 생기거나 새 계열 · 장비 hint · 층 · 대상 근육 넘김이 생기면 technique-check 로 넘긴다. 새 원장 항목 · 시장가 · 메뉴가 오거나 새 제품이 이어질 단위 시술을 찾아야 하면, 또는 원천 질문 답이 오면 unit-check 로 간다 — 거기서 계열 없는 시술이 나오면 family-check(계열) · technique-check(기법)로 되돌아간다. 5단계가 행선지 「6단계 패키지」로 넘긴 행 · 새 묶음 메뉴 · 회차 패키지 · 시장가 패키지 가격이 오면 package-check 로 간다 — 거기서 「단위 시술」(한 장비 다중 모드 · 같은 키 두 제제)로 판정되거나 구성에 5단계 키가 없으면 unit-check 로 되돌아간다. 새 고민 · 고민 표현 · 추천 조합(추천 패키지 · 레시피 · 최적화 · 비교)이 오거나 대응표 사람 확인(게이트) 답이 오면 concern-check 로 간다 — 거기서 단위 시술이 없는 이름이 나오면 unit-check 로 되돌아가 키부터 세운다. 시술↔시술 관계(시너지 · 순서 · 간격 · 금기) · 확인 조건 · 고민 조건 금기 · 안전 · 근거 원천이 바뀌거나 8단계 원천 질문 답이 오면 relation-check 로 간다 — 거기서 7단계 끝점(조합 · CC 엣지 · 고민 노드)이 어긋나면 concern-check, 못 푼 이름의 키가 없으면 unit-check 로 되돌아간다.

## 지도

```text
reference/2026-10-27-skills-procedure-hub/
├── README.md                              ← 이 파일
├── procedure-hub-product-check/           ← 스킬: 제품 탐색 · 허가 확인 · 실버 제품 원장 갱신
│   ├── SKILL.md                           언제 · 찾는 순서 · 판정 체크리스트 · 갱신 방법 · 변경 보고 형식
│   ├── references/
│   │   ├── rules.md                       1단계 규칙 13개 상세(막는 사고 · 맞게 한 예 · 틀렸던 예 · 결정) · 상태 6종
│   │   ├── record-schema.md               step1-products.json 칸 설명 + 실제 행 발췌(디클래씨 · 슈링크 · 리프세라 …)
│   │   ├── query-patterns.md              식약처 MCP tool · emedi 목록/상세 POST · KPIC tool · 국내 유통 출처
│   │   └── mistakes.md                    1단계에서 틀린 것 8
│   └── scripts/
│       └── recheck_licenses.py            정기 점검 — 연결 허가 전부 재조회(식약처 상태 · emedi xprtppYn · 유효기간) → 변경분 JSON
└── procedure-hub-family-check/            ← 스킬: 계열 · 하위 계열 판정 · 실버 계열 원장(step2-families) 갱신
    ├── SKILL.md                           언제 · 판정 순서 · 2단계 규칙 체크리스트 · 갱신 방법(step2-apply.py) · 변경 보고 형식
    ├── references/
    │   ├── families.md                    계열 18 정의 · PMID · 하위 칸 표(행 수) · 원천 하위 행선지 · M8 매질 표기 대응
    │   ├── record-schema.md               step2-families.json 칸 설명 · 입력(step2-research · step2-open-resolve) 행 · 실제 행 발췌
    │   └── mistakes.md                    2단계에서 틀린 것 7 + 행 단위 사례
    └── scripts/
        └── check_families.py              원장 점검 — product_family 전수(칸 · 보조 코드 · open · summary · 1단계 active 일치 · 근거 약) → JSON
└── procedure-hub-site-check/              ← 스킬: 부위 판정 · 실버 부위 원장(step3-sites) 갱신
    ├── SKILL.md                           언제 · 판정 순서(이름 칸 → 몸 겉 → 동의어 / D-07 / 새 노드 D-05 / 부위 아님) · 3단계 규칙 체크리스트 · 갱신 방법(결정 한 줄 · 사전 → step3-apply.py) · 변경 보고 형식
    ├── references/
    │   ├── nodes.md                       노드 53 표(일반인 · 전문의 용어 · 수준 · 상위 · 위험 부위 · 이름 칸 근거 · 동의어) · 근육 · 뼈 뺀 5 노드 · zone 11 대응 · 경계 규칙 · 트리 밖 판정
    │   ├── name-fields.md                 이름 칸 17(파일 · 키 · 칸 수 1,953) · 세지 않는 칸 · 칸을 더하는 조건
    │   ├── record-schema.md               step3-decisions.json(strings · nodes) · step3-lexicon.json · step3-sites.json 칸 설명 + 실제 행
    │   └── mistakes.md                    3단계에서 틀린 것 8(설명 문장 범위 · 가상 문장 루프 · 치골궁 · 지방흡입술 → 입술 · 코조각주사 …) + 이름 · 속성 사례
    └── scripts/
        └── check_sites.py                 원장 점검 — 이름 칸 전수 재추출 → 결정 없는 문자열 = open · 결정 행 · 노드 근거 · 전문의 용어 표지 · 원장 ↔ 재추출 · summary → JSON
└── procedure-hub-technique-check/         ← 스킬: 기법 판정 · 실버 기법 원장(step4-techniques) 갱신
    ├── SKILL.md                           언제 · 판정 순서(지도 4단계 칸 → 큰 기법(계열 정의 동사 · mechanism) → 세부 노드(D-05) / 단위 시술 속성(층 · 근육 · 도구) / 장비 속성(펄스 · 박피) / 넘김) · 4단계 규칙 체크리스트 · 갱신 방법(결정 한 줄 → step4-apply.py) · 변경 보고 형식
    ├── references/
    │   ├── nodes.md                       노드 24 표(큰 12 · 세부 12 · 의학 용어 · 계열 기본 · 원천 표현 · 초안 합침 · 근거) · 노드로 간 표현 41행 · 세우는 규칙 · J1 대안 구조
    │   ├── value-dictionary.md            값 사전(층 13 · 펄스 3 · 박피 2 · 도구 3 · 박피 깊이 3 · 가능 방식 1 · 대상 근육 17) · 부위 × 층 safe_layers 17 · 코 층 나눔 · 주입 지표 2 · 매질별 펄스 · 장비 속성 칸
    │   ├── family-defaults.md             계열 기본 기법 18(기본 · 보조 · 기본 층 · 근거) · 고르는 법
    │   ├── record-schema.md               step4-decisions.json 칸 · 노드 · 표현 · 넘겨받은 것 · technique_hint · 계열 · 초안 행(실제 값) · 원장 칸 · 지도 4단계 칸 27 표
    │   └── mistakes.md                    4단계에서 틀린 것 4(J2 골막상 · 연골막상 · pulse_scope 누락 · md 고정 숫자 · 지도 늦음) · 초안 65 가 섞은 것 · 같은 글자 다른 자리 · 되풀이하지 않은 것
    └── scripts/
        └── check_techniques.py            원장 점검 — 지도 4단계 칸 재추출 → 결정 없는 표현 = open · 노드 2층 · 값이 사전 안 · 계열 기본 = step2 계열 · 넘겨받은 것 역검사 · hint · 초안 · 원장 ↔ 재추출 · summary · md 셈 → JSON
└── procedure-hub-unit-check/              ← 스킬: 단위 시술 판정 · 실버 단위 시술 원장(step5-units) 갱신
    ├── SKILL.md                           언제 · 판정 순서(원장 항목 행선지 9종 → 시술이면 전부 단위 시술 · 계열 없으면 family-check 로 계열부터 → 키(J1 안 C) → 부위 기본값 · 해당 없음 · 병변 단위 → 이름 · 동의어 → 붙는 것) · 제품 상속 규칙 · 체크리스트 · 갱신 방법(결정 한 줄 → step5-apply.py) · 끝 조건 · 변경 보고 형식
    ├── references/
    │   ├── key-rules.md                   원장 행선지 9종 · 판정 규칙 L1~L11(행 수) · 키 칸 규칙(안 C · 성분 미상) · 부위 기본값 · 특수 부위 · 이름 C1~C3 · 붙는 것
    │   ├── inheritance-rules.md           저장 · 상속 세 조건 · 기법 근거 판정 순서 7(쌍 수) · 계열 근거(M4 · M5 · M15 · M17 · N4) · 매질이 기법을 정하는가 · 매질 미지정 키 · 제품 출처(실제 행) · 추천 가능 단위 시술 0 · 규칙 고칠 때 셈
    │   ├── record-schema.md               step5-decisions.json(units · ledger · market · problem_P1 · product_link_rule) · step5-units.json(product_links …) 칸 + 실제 행 · open 종류와 닫는 법
    │   ├── mistakes.md                    5단계에서 틀린 것 8(계열 없으면 시술 0 · 버림 17 · 지도 칸 45 · F1 네 번(기법 조건 누락 → 부분 적용 → 하위 키 → 반대 방향) · 전수 늦음 · 성분 미상 · 파셀라 · 재생팩) · 전후 비교
    │   └── origin-questions.md            원천 질문 다섯 갈래(성분 · 정체 · 시술 방식 · 근거 약 · 원천 수정) · 지금 값 · 의료진 질문 · 원장님 문의 · 답이 왔을 때 순서
    └── scripts/
        └── check_units.py                 원장 점검 — 원장 항목 521 재추출 → 행선지 셈 · 시술인데 단위 시술 없음 · 키 칸 · 상속 쌍마다 기법 근거 다시 가림 · 추천 가능 제품 단위 시술 0 목록 · open · summary → JSON
└── procedure-hub-package-check/           ← 스킬: 패키지 판정 · 실버 패키지 원장(step6-packages) 갱신
    ├── SKILL.md                           언제 · 「패키지」 두 뜻(사이트 추천 패키지 = 7단계) · 판정 순서(패키지인가 5갈래 → 구성 = 원천 적힌 시술 낱말만 → 단위 시술 키(없으면 unit-check) → 슬롯 + 원천 질문 → 가격 · 같은 날 원문) · 시너지는 8단계 · 체크리스트 · 끝 조건 · 갱신 방법(결정 한 줄 → step6-apply.py) · 변경 보고 형식
    ├── references/
    │   ├── package-rules.md               다섯 갈래 실제 예 · 구성 원천 칸(적응증 아님) · 키 · 슬롯 · 근거 약 · 가격 · 같은 날 · 수량 · 6 ↔ 7 ↔ 8 경계
    │   ├── record-schema.md               step6-decisions.json(packages · components · non_packages · handoffs · origin_questions …) · step6-packages.json 칸 + 실제 행 · open · 오류를 어느 스크립트가 보나
    │   └── mistakes.md                    6단계에서 틀린 것 5(「패키지」 두 뜻 · 「병원 메뉴 묶음」 · 특정 병원 의심 · 옛 번호 · 「같은 날」) + 전후 비교
    └── scripts/
        └── check_packages.py              원장 점검 — 패키지 원천 행 재추출 → 결정 없는 행 = open · 구성 엣지 원문을 원천 칸에서 다시 찾기(적응증만이면 오류) · 키 실재 · 슬롯 · 근거 약 질문 · 시그니처 노출 · menu_group ↔ 원천 하위 · 가격 원문 · 회차 · 원장 ↔ 결정 · summary → JSON
└── procedure-hub-concern-check/           ← 스킬: 고민 · 목적 · 추천 조합 판정 · 실버 고민 원장(step7-concerns) 갱신
    ├── SKILL.md                           언제 · 판정 순서(고민 정본 = taxonomy problem → 시술 이름 항목은 엣지 → 대응표 완전 일치만 자동 · 나머지 게이트 → 목적 vs 고민 → 엣지는 원천 구조만 → 부위로 내림 · 후보 전부 + 표시 → 단위 시술 없으면 unit-check → 추천 조합 원천별 · 영업 문구 제외 · 사이트 용어) · 체크리스트(F1 · F2 · W2 · W3) · 끝 조건 · 갱신 방법(결정 한 줄 → step7-apply.py) · 변경 보고 형식 · 게이트 답 반영 방법
    ├── references/
    │   ├── concern-rules.md               고민 트리 갈래별 행선지(대분류 · 중분류 · 항목) · 대응표 원천 9곳 · 게이트 규칙 · 목적 ↔ 고민 · 엣지 원천 칸 일곱 갈래 · 이름 → 단위 시술 · 부위 거름 순서 · 추천 조합 kind · 8단계 메모
    │   ├── record-schema.md               step7-decisions.json(대응 · 이름 풀이 · site_rules …) · step7-concerns.json(대응 · 엣지 · 조합) 칸 + 실제 행 · open · 오류를 어느 스크립트가 보나
    │   └── mistakes.md                    7단계에서 틀린 것(F1 꼬리말 완전 일치 · F2 부위 밖 · W1 계열 코드 표시 · W2 경로별 처리 · v2 W1 · W2 · W3 질환 이름 · W4) + 전후 비교
    └── scripts/
        └── check_concerns.py              원장 점검 — 고민 칸 · 고민 표현(원천 9곳) 재추출 → 원장에 없음 = open · 자동 대응을 글자로 다시 비교(완전 일치만) · 결정 「완전」 행 · 결정 ↔ 원장 target · 게이트 초기값 · 질문 수 · 엣지를 원천 칸에서 다시 찾기(일곱 갈래 밖 · 적응증 유래 = 오류) · 원천 행 수 ↔ 엣지 수 · 엣지 부위 · 후보 전부 표시 · 영업 문구 · summary → JSON
└── procedure-hub-relation-check/          ← 스킬: 관계 · 확인 조건 · 피함 · 안전 · 근거 판정 · 실버 관계 원장(step8-relations) 갱신
    ├── SKILL.md                           언제 · 판정 순서(8단계 칸 → 끝점 = 이름이 가리키는 만큼(고르지 않음) → 문장 패턴(게이트 없음 · U8-1) → 간격 낱말 사전 → 숫자 칸(days · first · same_day) → 고민 조건 금기 = 피함(U8-2) → 확인 조건 · 안전 · 근거 → 충돌 보존 · 규칙 밖만 원천 질문) · 체크리스트 · 끝 조건 · 갱신 방법(결정 한 줄 → step8-apply.py) · 변경 보고 형식
    ├── references/
    │   ├── relation-rules.md              G1~G14 실제 예 · 문장 패턴 꼬리 다시 찾기 · 생략 상대 · 규칙 제목 · 간격 낱말별 검사 · first 머리말 · 7단계 끝점 대조 · 원천 질문 갈래
    │   ├── record-schema.md               step8-decisions.json · step8-relations.json 칸 · open 종류와 닫는 법
    │   └── mistakes.md                    8단계에서 틀린 것(W1 행별 대응표 → 패턴 · W2 간격 한 줄 정규식 · W3 꼬리 먼저 떼기 · W4 「24시간 내」 · W5 기전 문장 붙임 · W6 CC 원소 글자 비교 · W7 괄호 복합 · W8 제품 계열 · W9 칸 셈)
    └── scripts/
        └── check_relations.py             원장 점검 — apply 재실행 바이트 비교(낡음 · 결정론) · 게이트 상태 없음 · 간격 숫자 칸(first · days · 낱말별 사전 갈래) · 같은 날 불가 = false · 대체 = 간격 비움 · 끝점 키 · 엣지 ↔ 주장 · 충돌 표시 · 피함 출발 = 7단계 고민 노드 · 조건 id · 질문 걸린 행 · summary → JSON · --selftest(틀린 값 11가지를 넣어 잡히는지)
```

## 기대는 것

product-check:

- 원장 `orchestration/work/phub-recommend/step1-products.json` · 결정 `_RESUME.md` §2 · 기록 `para/projects/company/procedure-hub/log/2026-10-28-silver-step1-product-normalization.md`
- MFDS MCP `reference/2026-10-27-mfds-mcp/` — 스크립트가 그 `src/` 와 `.venv` 를 쓰고 키는 그 `.env` 에서 읽는다(값 출력 없음)
- KPIC MCP `reference/2026-10-28-kpic-mcp/` — 의약품 확인

family-check:

- 원장 `orchestration/work/phub-recommend/step2-families.json` · 반영 `step2-apply.py` · 입력 `step2-research.json` · `step2-open-resolve.json` · 결정 `_RESUME.md` §2 10-28 · 기록 `para/projects/company/procedure-hub/log/2026-10-28-silver-step2-family.md`
- 기준 문헌 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/literature-evidence.json` · taxonomy `…/taxonomy.json`(`step2-apply.py` 가 이 절대 경로를 읽는다)
- 1단계 원장 `step1-products.json` — 점검 스크립트가 active 행 일치를 본다

site-check:

- 원장 `orchestration/work/phub-recommend/step3-sites.json` · 결정 `step3-decisions.json` · 사전 `step3-lexicon.json` · 반영 `step3-apply.py` · 가드 시험 `step3-fixture-test.py` + `step3-fixtures/` · 트리 `procedure-master-v3.json` `site_tree` · 결정 `_RESUME.md` §2 10-28 · `DEC-002.md` · 기록 `para/projects/company/procedure-hub/log/2026-10-28-silver-step3-site.md`
- 원천 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/`(결정 `source.path` — 점검 스크립트 · `step3-apply.py` 가 이 절대 경로를 읽는다. `--source` 로 바꿀 수 있다)

technique-check:

- 원장 `orchestration/work/phub-recommend/step4-techniques.json` · `.md` · 결정 `step4-decisions.json` · 반영 `step4-apply.py` · 가드 시험 `step4-fixture-test.py` + `step4-fixtures/` · 지도 `source-map.json`(4단계 칸 27) · 검수 `review-step4-report.md` · 결정 `_RESUME.md` §2 10-28 · 기록 `para/projects/company/procedure-hub/log/2026-10-28-silver-step4-technique.md`
- 앞 단계 정본(읽기만): `step3-sites.json` · `step3-decisions.json` `danger_zone_mapping` · `step2-families.json` · 초안 `procedure-master-v3.json` `techniques`
- 원천 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/`(결정 `source.path` — 점검 스크립트 · `step4-apply.py` 가 이 절대 경로를 읽는다. `--source` 로 바꿀 수 있다)

unit-check:

- 원장 `orchestration/work/phub-recommend/step5-units.json` · `.md` · 결정 `step5-decisions.json` · 반영 `step5-apply.py` · 가드 시험 `step5-fixture-test.py` + `step5-fixtures/` · 원천 질문 `step5-origin-questions.md` · 검수 `review-step5-report.md` ~ `-v3-report.md` · 결정 `_RESUME.md` §2 10-29 · 기록 `para/projects/company/procedure-hub/log/2026-10-29-silver-step5-unit.md`
- 앞 단계 정본(읽기만): `step1-products.json` · `step2-families.json` · `step3-sites.json` · `step4-techniques.json`(결정 `canon`)
- 원천 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/`(결정 `source.path` — 점검 스크립트 · `step5-apply.py` 가 이 절대 경로의 `taxonomy.json` 을 읽는다. `--source` 로 바꿀 수 있다)

package-check:

- 원장 `orchestration/work/phub-recommend/step6-packages.json` · `.md` · 결정 `step6-decisions.json` · 반영 `step6-apply.py` · 가드 시험 `step6-fixture-test.py` + `step6-fixtures/` · 원천 질문 `step6-origin-questions.md` · 원천 수정 후보 `step6-source-fix.md` · 검수 `review-step6-report.md` · 결정 `_RESUME.md` §2 10-29 6단계 행 · 기록 `para/projects/company/procedure-hub/log/2026-10-29-silver-step6-package.md`
- 앞 단계 정본(읽기만): `step5-units.json`(키 · 원장 행선지 · 시장가 kind · handoffs) · `step5-decisions.json`(행선지 대조)
- 원천 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/`(결정 `source.path` — 점검 스크립트 · `step6-apply.py` 가 이 절대 경로의 `taxonomy.json` · `market-pricing.json`(+ apply 는 `synergy.json`)을 읽는다. `--source` 로 바꿀 수 있다)

concern-check:

- 원장 `orchestration/work/phub-recommend/step7-concerns.json` · `.md` · 결정 `step7-decisions.json` · 반영 `step7-apply.py` · 가드 시험 `step7-fixture-test.py` + `step7-fixtures/` · 원천 질문 `step7-origin-questions.md` · 원천 수정 후보 `step7-source-fix.md` · 검수 `review-step7-report.md` · `-v2-report.md` · 결정 `_RESUME.md` §2 10-29 7단계 행 · 기록 `para/projects/company/procedure-hub/log/2026-10-29-silver-step7-concern.md`
- 앞 단계 정본(읽기만): `step3-sites.json`(부위 트리 · deferred · strings handoff) · `step5-units.json`(키 · 동의어 · purposes · product_evidence · 제품 연결) · `step6-packages.json`(non_packages 7단계 넘김)
- 원천 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/`(결정 `source.path` — 점검 스크립트가 taxonomy · problem-packages · problem-combos · combo-recipes · treatment-optimization · procedure-comparison · synergy 를 읽고, apply 는 treatment-sequence 도 읽는다. `--source` 로 바꿀 수 있다)

relation-check:

- 원장 `orchestration/work/phub-recommend/step8-relations.json` · `.md` · 결정 `step8-decisions.json` · 반영 `step8-apply.py` · 가드 시험 `step8-fixture-test.py` + `step8-fixtures/` · 원천 질문 `step8-origin-questions.md` · 조사 `step8-research.*` · 결정 `_RESUME.md` §2 10-29 8단계 행
- 앞 단계 정본(읽기만): `step1-products` · `step2-families` · `step3-sites`(danger_zone_mapping) · `step4-techniques`(safe_layers) · `step5-units`(키 · 동의어 · 장비 · product_links · ledger · pih) · `step6-packages`(8단계 메모) · `step7-concerns`(고민 노드 · 조합 앵커 · CC ③ 엣지 · 8단계 메모) · `source-map.json`(8단계 칸)
- 원천 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/`(결정 `source.path` — apply 가 18파일을 읽는다. `--source` 로 바꿀 수 있다)

## 정기 점검 실행

프로필 레포 루트에서:

```bash
MFDS=reference/2026-10-27-mfds-mcp
$MFDS/.venv/bin/python reference/2026-10-27-skills-procedure-hub/procedure-hub-product-check/scripts/recheck_licenses.py \
  --ledger orchestration/work/phub-recommend/step1-products.json \
  --mfds-dir $MFDS --out /tmp/recheck.json        # --limit N · --ids a,b · --no-emedi
```

원장은 읽기만 한다. 결과의 `changes[]` 가 결정 목록 재료다(SKILL.md §4).

10-28 시험 실행(원장 v2):
- `--ids` 10행(슈링크 · 디클래씨 · 디스포트 · 온다 · 더채움 · 젠틀맥스 프로+ · 리프테라 · 더톡신 · 더블로 · 보툴렉스) — 허가 23건 · emedi 15회 · 변경 0 · 오류 0
- `--limit 10`(앞 10행 · 전부 톡신 의약품) — 허가 25건 · 변경 0 · 오류 0
- 판정 확인: 제허 15-1401 → 「수출용」 · 제허 23-60 → 「취소·취하 · 수출용」 · 의약품 202004236 → 「수출용」 · 제허 14-1422 → 변경 없음

## 계열 원장 점검 실행

프로필 레포 루트에서(표준 라이브러리만 · 읽기만):

```bash
python3 reference/2026-10-27-skills-procedure-hub/procedure-hub-family-check/scripts/check_families.py \
  --ledger orchestration/work/phub-recommend/step2-families.json \
  --products orchestration/work/phub-recommend/step1-products.json \
  --out /tmp/family-check.json        # 오류 있으면 종료 코드 1
```

10-28 실행(재검수 v5 PASS 판 · 원장 md5 `3e3ba6d1…` · 1단계 `cfa00e1a…` — 실행 전후 같음):
- `rows 352 · step1 active 352 · 새 행 0 · 빠진 행 0 · 오류 0 · open 0 · 근거 약 9 · 원장님 문의 3 · 충돌 6 · 하위 null(칸 있는 계열) 8` · 종료 코드 0
- 판정 맞음 256 · 옮김 66 · 여러 19 · 계열 밖 8 · 판단 필요 3 — summary 와 다시 센 값 일치(기록 §2-1 과 같음)
- 하위 null 8 = 주입 기기 7(큐어젯 · 미라젯 · 하이쿡스 · 더마샤인 · 에어젯 · 노보젯 · 비타인젝터) + 트리필 프로 — 「기기는 하위 아님」 규칙대로
- 쓰인 행 0 인 하위 칸: M6 「지방 입자 크기」 · M7 「PLCL」 · M17 「세포(SVF)」 · 1단계 코드 ↔ 이름 다른 행 4(소프라노 티타늄 · 셀리뉴 · 소노퀸 · 버츄RF)
- 결함 주입 확인(scratchpad 사본): 정의 밖 하위 · 없는 보조 코드 · 문자열 보조 하위 · 행 1개 삭제 → 오류 4(summary 불일치 포함) · 새 행 1 · 종료 코드 1

## 부위 원장 점검 실행

프로필 레포 루트에서(표준 라이브러리만 · 읽기만):

```bash
python3 reference/2026-10-27-skills-procedure-hub/procedure-hub-site-check/scripts/check_sites.py \
  --work orchestration/work/phub-recommend \
  --out /tmp/site-check.json          # 새 스냅샷은 --source <폴더> · 오류나 open 있으면 종료 코드 1
```

지금 원천 기준만 본다 — 가상 문장 · 해부학 목록 확장 시험은 넣지 않았다(`_RESUME` §2 10-28 「끝 조건 = 지금 원천 기준」).

10-28 실행(v5 + 한 줄 수정 판 · `step3-sites.json` md5 `02e3662c…` · `step3-decisions.json` `063c4883…` · `step3-lexicon.json` `6c9d3a6c…` — 실행 전후 같음):
- 원천 21파일 · 문자열 칸 22,749 · 이름 칸 17종 1,953칸
- `open 0 · stale 0 · errors 0` · 종료 코드 0
- 다시 센 값 = 원장 summary: 문자열 176 · 등장 440 · 노드로 154 · 넘김 22 · 노드 53 · 근거 약 4(팔뚝 · 임신선 · 불독살 · 하관)
- kind(행): D-07 79 · 노드 이름 49 · 부위 아님 22 · 동의어 14 · 해부학 이름(속성) 8 · 여러 부위(나열) 4 / 넘김 단계: 1단계 제품 8 · 7단계 고민 6 · 4단계 기법 3 · 5단계 경로 2 · 계열 밖 1 · 2단계 계열 1 · 사후관리 1
- 해부학 수준 강 20 · 중 4 · 약 29 · 의료진 질문 35 · 이름 칸 예외 입가 1 · handoff_note 5(턱선 · 사각턱 · 목 · 승모근 · 종아리) · 전문의 용어 근육 · 뼈 · 혈관 표지 0
- 결함 주입 확인(scratchpad 사본): 결정 「코조각주사」 한 줄 빼기 · 사각턱 anatomical_ko 「깨물근」 · 입가 name_field_exception 지움 → open 1(결정 없는 문자열) · 오류 3(전문의 용어 표지 · 노드 근거 0 · summary 노드로 154 ≠ 153) · 종료 코드 1
- 관찰(스크립트 밖 · 고치지 않음 — 판단은 사람): 이름 칸 문자열 「표정근」(시장가 「안면 EMS (표정근 강화)」)이 얼굴 노드의 kind 「해부학 이름(속성)」(B3)이다. 근육 묶음 이름이라 규칙 「대상 근육 → 4단계 기법」과 맞는지 확인할 거리
- 함께 확인: `step3-apply.py --out <scratchpad>` 재생성 → `step3-sites.json` · `.md` · `step3-source-fix.md` 정본과 바이트 같음(정본은 지금 입력의 결정론 출력)

## 기법 원장 점검 실행

프로필 레포 루트에서(표준 라이브러리만 · 읽기만):

```bash
python3 reference/2026-10-27-skills-procedure-hub/procedure-hub-technique-check/scripts/check_techniques.py \
  --work orchestration/work/phub-recommend \
  --out /tmp/technique-check.json     # 새 스냅샷은 --source <폴더> · 오류나 open 있으면 종료 코드 1
```

지금 원천 기준만 본다 — 가상 문장 시험은 넣지 않았다(`_RESUME` §2 10-28 4단계 「끝 조건 지금 원천 open 0 · 가상 문장 시험 없음」).

2026-10-29 실행(v1 + 3단계 「표정근」 반영 판 · `step4-techniques.json` md5 `96b39ce7…` · `step4-decisions.json` `46089c1d…` · `step3-sites.json` `26742f60…` · `source-map.json` `61f1b488…` · `step2-families.json` `3e3ba6d1…` — 실행 전후 같음):
- 지도 4단계 칸 27 · 줄 215(칸별 1줄 19칸 · 11줄 3칸 · 51줄 2칸 · 25 · 17 · 19줄 각 1칸) · 중복 묶음 17행(51줄)
- `open 0 · stale 0 · errors 0` · 종료 코드 0
- 다시 센 값 = 원장 summary: 노드 24 · 표현 181행(새 표현 164 + 중복 17) · 속성 64 · 넘김 59 · 노드로 41 · 중복 17 · 계열 기본 18 · technique_hint 25 · 넘겨받은 것 15 · 대상 근육 17 · 값 사전 층 13 · 펄스 3 · 박피 2 · 도구 3 · 박피 깊이 3 · 가능 방식 1
- 계열 기본 18 = step2 계열 18(M1 ~ M17 · N1) — 보조 있는 계열 M4(K01c) · M5(K09) · M15(K11 · K10) · M17(K09)
- pulse_scope 1행 — 셀렉V `auto-M8-1775364106103` Q스위치(나노초) = 보조 하위 계열 엔디야그 레이저(step2 보조 하위 계열에 있음)
- 고정 시험 결과 파일 `step4-fixtures/result.json` 10/10(스크립트는 읽기만 · 시험을 돌리지 않는다)
- 결함 주입 확인(scratchpad 사본): 표현 결정 「zones[forehead].botox_specific.target_muscle」 한 줄 빼기 · K04a 상위를 세부 K04b 로 · M7 기본을 없는 K99 로 · M8-1-3 pulse_mode 「피코」 → open 1(결정 없는 표현) · 오류 4(노드 2층 넘음 · 값 사전 밖 · 계열 기본 기법 오류 · summary 불일치) · 종료 코드 1
- 함께 확인: `step4-apply.py --out <scratchpad>` 두 번 → `step4-techniques.json` · `.md` · `step4-source-fix.md` 서로 · 정본과 바이트 같음(정본은 지금 입력의 결정론 출력)
- 실행 중 관찰: 같은 시각에 3단계 「표정근」 한 줄 반영(별도 발주)이 돌아 09:44 ~ 09:46 사이 `step4-apply.py` 가 한때 open 1(「넘겨받은 것 행선지 없음: 표정근」 — 3단계가 deferred 로 바꾸고 H15 가 아직 `step3_string` 이던 사이)을 냈다. 위 결과는 그 반영이 끝난 뒤(09:46:48 판)다

## 단위 시술 원장 점검 실행

프로필 레포 루트에서(표준 라이브러리만 · 읽기만):

```bash
python3 reference/2026-10-27-skills-procedure-hub/procedure-hub-unit-check/scripts/check_units.py \
  --work orchestration/work/phub-recommend \
  --out /tmp/unit-check.json          # 새 스냅샷은 --source <폴더> · 오류나 open 있으면 종료 코드 1
```

지금 원천 기준만 본다 — 가상 문장 시험은 넣지 않았다(`_RESUME` §2 10-28 「끝 조건 = 지금 원천 기준」 · 5단계 고정 시험은 「결정 한 줄 빼면 open」만).

2026-10-29 실행(재검수 v3 PASS 판 · `step5-units.json` md5 `cb92d762…` · `step5-decisions.json` `fd200fbd…` · `step1-products.json` `33915cdb…` · `step2-families.json` `7ec731df…` · `step3-sites.json` `26742f60…` · `step4-techniques.json` `737d2ffd…` — 실행 전후 같음):
- 원천 원장 항목 521 · `open 0 · stale 0 · errors 0` · 종료 코드 0
- 다시 센 행선지 = 원장 summary: 제품 309 · 단위 시술 149 · 6단계 패키지 18 · 값 17 · 다른 단계 이름 15 · 제품 + 단위 시술 9 · 시술 아님(다른 단계) 2 · 시술 아님 1 · 원장님 문의 1 · 결정 없음 0
- **시술 173(단위 시술 149 · 제품 + 단위 시술 9 · 다른 단계 이름 15) — 시술인데 단위 시술 없음 0**
- 키 143(M1 17 · M2 8 · M3 1 · M4 3 · M5 5 · M6 6 · M7 4 · M8 20 · M9 6 · M10 5 · M11 2 · M12 2 · M13 5 · M14 5 · M15 5 · M16 25 · M17 3 · N1 9 · N2 1 · N3 4 · N4 4 · N5 1 · N6 1 · N7 1) · 부위 기본값 40 · 해당 없음 27 · 병변 단위 3 · 성분 미상 4(U5-133 ~ 136) · 키 오류 0
- **상속 1227쌍(제품 320) — 기법 근거 없는 쌍 0** · 근거 종류 = S7(기법 안 갈리는 계열) 801 · 계열 근거 145 · 계열 기법 하나 100 · 매질이 기법을 정함 88 · 장비 속성 48 · 제품 출처 44 · 4단계 가드 1 · 뺀 쌍 716 · 저장 42쌍(제품 35) · 출처 제외 2(슬렌더엑스 · 리팟 — 제모)
- **추천 가능 제품 236 중 단위 시술 0 = 5 — 예외 목록뿐**: 계열 밖 2(3D 메타뷰 · 마크뷰) · 원천 질문 예외 3(미라셀 · 셀엑소좀 · 스마트자이드) · 예외 결정 없음 0
- 원천 질문 19 · 의료진 질문 1 · 고정 시험 결과 파일 `step5-fixtures/result.json` 24/24(스크립트는 읽기만 · 시험을 돌리지 않는다)
- 결함 주입 확인(scratchpad 사본): 결정 「사각턱」(M1-3-2) 한 줄 빼기 · 원장 셀디톡스수액 units 비우기 · 스마트사이드 `origin_question` 지움 · 젠틀맥스 프로 플러스 → 얼굴 전체 알렉스토닝(U5-024) 상속 쌍 더하기 → open 3(결정 없는 원장 항목 · 시술인데 단위 시술 없음 · 추천 가능 제품인데 단위 시술 0 · 예외 결정 없음) · 오류 5(summary 불일치 4 · 기법 근거 없는 상속 쌍 1) · 종료 코드 1

## 패키지 원장 점검 실행

프로필 레포 루트에서(표준 라이브러리만 · 읽기만):

```bash
python3 reference/2026-10-27-skills-procedure-hub/procedure-hub-package-check/scripts/check_packages.py \
  --work orchestration/work/phub-recommend \
  --out /tmp/package-check.json       # 새 스냅샷은 --source <폴더> · 오류나 open 있으면 종료 코드 1
```

지금 원천 기준만 본다 — 가상 문장 시험은 넣지 않았다(`_RESUME` §2 10-29 6단계 「끝 조건 open 0 + 패키지인데 구성 없음 0」). 아래 수치는 그날 실행 기록이다 — 지금 값은 스크립트를 다시 돌려 본다.

2026-10-29 실행(6단계 데이터 끝 판 · `step6-packages.json` md5 `93967fbe…` · `step6-decisions.json` `496e369b…` · `step5-units.json` `674336eb…` · `step5-decisions.json` `a5624b35…` — 실행 전후 같음):
- 패키지 원천 행 = 5단계 원장 「6단계 패키지」 16 + 시장가 「6단계 패키지」 9 · 5단계 정본 ↔ 5단계 결정 행선지 일치
- `open 0 · stale 0 · errors 0` · 종료 코드 0
- 다시 센 값 = 원장 summary: 패키지 24(일반 패키지 19 · 병원 시그니처 2 · 회차 묶음 3) · 추천 노출 22 · 엣지 49(근거 약 5) · 슬롯 8(5단계에 키 없음 1 — 인모드바디) · 구성 다 풀린 패키지 18 · 엣지 0 패키지 4(P6-01 · 11 · 20 · 23 — 전부 슬롯 + 원천 질문) · 시그니처 P6-08 · 09(추천 노출 0)
- 구성 엣지 원문을 원천 칸에서 다시 찾음 — 원장 detail · overview · mechanism 39 · 시장가 이름 8 · 회차(5단계 시장가 행 `to` 가 그 키를 부름 · sessions 같음) 2 · 원천에 없는 구성 0 · 적응증에서 온 구성 0
- 묶음 이름 9 · 넘겨받은 것 4 · 원천 질문 13 · 원천 수정 후보 1 · 고정 시험 결과 파일 `step6-fixtures/result.json` 10/10(스크립트는 읽기만 · 시험을 돌리지 않는다)
- 결함 주입 확인(scratchpad 사본): 결정 P6-03 한 줄 빼기 · P6-08 recommendable true · P6-05 구성 원문 「피부재생레이저」 · P6-02 구성 키 U5-999 · P6-01 슬롯 원천 질문 지움 → open 3(결정 없는 패키지 원천 행 · 구성 키도 질문도 없음 · 구성도 질문도 없는 패키지) · 오류 7(키 없음 · 원천에 없는 구성 · 시그니처 추천 노출 · summary 불일치 3 · 원장 낡음) · 종료 코드 1 / 따로: P6-02 에 indications 낱말 「사각턱」 구성 더하기 · P6-12 menu_group 을 M9-SIG 로 → 오류 「적응증에서 온 구성」 · 「메뉴 묶음 어긋남」(+ summary · 원장 낡음)
- 함께 확인: `step6-apply.py --out <scratchpad>` 두 번 → `step6-packages.json` · `.md` · `step6-origin-questions.md` · `step6-source-fix.md` 서로 · 정본과 바이트 같음(정본은 지금 입력의 결정론 출력)

## 고민 원장 점검 실행

프로필 레포 루트에서(표준 라이브러리만 · 읽기만):

```bash
python3 reference/2026-10-27-skills-procedure-hub/procedure-hub-concern-check/scripts/check_concerns.py \
  --work orchestration/work/phub-recommend \
  --out /tmp/concern-check.json       # 새 스냅샷은 --source <폴더> · 오류나 open 있으면 종료 코드 1
```

## 관계 원장 점검 실행

8단계 관계 원장(step8-relations)이 결정 · 원천 · 앞 단계 정본과 맞는지 본다. 읽기만 · 표준 라이브러리. apply 를 임시 폴더로 다시 돌려 바이트 비교한다.

```bash
python3 reference/2026-10-27-skills-procedure-hub/procedure-hub-relation-check/scripts/check_relations.py \
  --work orchestration/work/phub-recommend \
  --out /tmp/relation-check.json --selftest     # 새 스냅샷은 --source <폴더> · 오류 · open · 안 잡힌 selftest 있으면 종료 코드 1
```

지금 원천 기준만 본다 — 가상 문장 시험은 넣지 않았다(`_RESUME` §2 10-29 7단계 「끝 조건 open 0」). 아래 수치는 그날 실행 기록이다 — 지금 값은 스크립트를 다시 돌려 본다.

2026-10-29 실행(7단계 데이터 끝 판 · `step7-concerns.json` md5 `085842a9…` · `step7-decisions.json` `fb8d99d0…` · `step3-sites.json` `26742f60…` · `step5-units.json` `b0aacf30…` · `step6-packages.json` `93967fbe…` — 실행 전후 같음):
- 원천 고민 표현 247행(9곳 다시 뽑음) = 원장 대응표 249행 중 역방향 2 밖 전부 · 결정 대응표 97행 · 원장에 없는 표현 0 · 원천에 없는 대응 0
- `open 0 · stale 0 · errors 0` · 종료 코드 0
- 고민 노드 55(결정 extra 1 — 자갈턱) · 원천 밖 고민 노드 0
- **대응 자동 161 = 전부 글자 완전 일치 · 결정 「완전」 행 글자 다름 0** · 게이트(확인 대기) 88 = 게이트 질문 88 · 결정 ↔ 원장 target 어긋남 0
  - 게이트 원천별: 3단계 strings handoff 32 · 최적화 18 · synergy 10 · 비교 9 · 레시피 6 · 6단계 메뉴 분류 6 · 3단계 deferred 4 · problem-combos 3
  - 글자가 같은데 게이트에 오른 행 4(안전한 쪽 · 고치지 않음): problem-combos 「쁘띠시술」(J5 앵커 없음 의도) · 3단계 조각 「홍조」 · 「자갈턱」 · 「정맥류」 — apply 의 3단계 조각 「완전 일치」 판정은 중분류 라벨 · 항목 이름 표만 보고 중분류 고민 이름 · 결정 extra 노드는 안 본다(관찰 — 판단은 사람)
- **엣지 523 — 원천 구조에 없는 엣지 0 · 일곱 갈래 밖(적응증 · 효과 문장 · 8단계 원천) 0** · 갈래별 ① 36 · ② 32 · ③ 254 · ④ 74 · ⑤ 79 · ⑥ 41 · ⑦ 7 · 원천 구조 행 수 = 엣지 수(③ CC procedures 254 · ④ optimal_combo 74 · ⑤ 시술 이름 항목 79 · ⑥ 5단계 purposes 39)
- **엣지 부위**: 앵커 부위 없음 321 · 부위 안 148 · 그 부위 단위 시술 없음 · 후보 전부(표시) 54 · **부위 밖 0** · 후보 전부인데 표시 없음 0 · 후보 전부인데 그 부위 단위 시술 있음 0
- 추천 조합 단위 시술 없음 0 · 영업 문구 기본 응답 포함 0 · 원천 질문 90(의료진 1 · 병원 1 · 게이트 88) · 원천 수정 후보 24 · 고정 시험 결과 파일 `step7-fixtures/result.json` 14/14(스크립트는 읽기만 · 시험을 돌리지 않는다)
- 결함 주입 확인(scratchpad 사본 · 8가지 한 번에): 게이트 행(비교 acne)을 자동으로 · 바디 CC 쿨스컬프팅 엣지를 얼굴 전체 고주파 리프팅(U5-091)으로 · 「extracted indications」 엣지 더하기 · ④ 엣지 하나 빼기 · 팔자주름 ① 엣지 no_unit_at_site 표시 지우기 · 결정 synergy 「리프팅」 target 을 P2 로(apply 안 돌림) · 고민 패키지 영업 문구 default_response true · 원장 taxonomy 항목 하나 빼기 → open 1(원장에 없는 taxonomy 고민 칸) · 오류 14(자동 대응 글자 다름 2(주입 1 + 뺀 항목을 가리키던 역방향 행 1) · 게이트 질문 수 · 원장 낡음 · 원천 구조 밖 엣지 · 원천 구조 행 수 ≠ 엣지 수 · 후보 전부 표시 없음 · 앵커 부위 밖 · 영업 문구 · summary 불일치 5) · 종료 코드 1
- 함께 확인: `step7-apply.py --out <scratchpad>` 두 번 → `step7-concerns.json` · `.md` · `step7-origin-questions.md` · `step7-source-fix.md` 서로 · 정본과 바이트 같음(정본은 지금 입력의 결정론 출력)

## 설치 (명령만 — 실행하지 않았다)

```bash
# 이 프로젝트에서만 (프로필 레포 루트)
mkdir -p .claude/skills
ln -s "$PWD/reference/2026-10-27-skills-procedure-hub/procedure-hub-product-check" .claude/skills/procedure-hub-product-check
ln -s "$PWD/reference/2026-10-27-skills-procedure-hub/procedure-hub-family-check" .claude/skills/procedure-hub-family-check
ln -s "$PWD/reference/2026-10-27-skills-procedure-hub/procedure-hub-site-check" .claude/skills/procedure-hub-site-check
ln -s "$PWD/reference/2026-10-27-skills-procedure-hub/procedure-hub-technique-check" .claude/skills/procedure-hub-technique-check
ln -s "$PWD/reference/2026-10-27-skills-procedure-hub/procedure-hub-unit-check" .claude/skills/procedure-hub-unit-check
ln -s "$PWD/reference/2026-10-27-skills-procedure-hub/procedure-hub-package-check" .claude/skills/procedure-hub-package-check
ln -s "$PWD/reference/2026-10-27-skills-procedure-hub/procedure-hub-concern-check" .claude/skills/procedure-hub-concern-check

# 전역 (모든 프로젝트)
mkdir -p ~/.claude/skills
ln -s "$PWD/reference/2026-10-27-skills-procedure-hub/procedure-hub-product-check" ~/.claude/skills/procedure-hub-product-check
ln -s "$PWD/reference/2026-10-27-skills-procedure-hub/procedure-hub-family-check" ~/.claude/skills/procedure-hub-family-check
ln -s "$PWD/reference/2026-10-27-skills-procedure-hub/procedure-hub-site-check" ~/.claude/skills/procedure-hub-site-check
ln -s "$PWD/reference/2026-10-27-skills-procedure-hub/procedure-hub-technique-check" ~/.claude/skills/procedure-hub-technique-check
ln -s "$PWD/reference/2026-10-27-skills-procedure-hub/procedure-hub-unit-check" ~/.claude/skills/procedure-hub-unit-check
ln -s "$PWD/reference/2026-10-27-skills-procedure-hub/procedure-hub-package-check" ~/.claude/skills/procedure-hub-package-check
ln -s "$PWD/reference/2026-10-27-skills-procedure-hub/procedure-hub-concern-check" ~/.claude/skills/procedure-hub-concern-check

# 링크 대신 복사
cp -R reference/2026-10-27-skills-procedure-hub/procedure-hub-product-check ~/.claude/skills/
cp -R reference/2026-10-27-skills-procedure-hub/procedure-hub-family-check ~/.claude/skills/
cp -R reference/2026-10-27-skills-procedure-hub/procedure-hub-site-check ~/.claude/skills/
cp -R reference/2026-10-27-skills-procedure-hub/procedure-hub-technique-check ~/.claude/skills/
cp -R reference/2026-10-27-skills-procedure-hub/procedure-hub-unit-check ~/.claude/skills/
cp -R reference/2026-10-27-skills-procedure-hub/procedure-hub-package-check ~/.claude/skills/
cp -R reference/2026-10-27-skills-procedure-hub/procedure-hub-concern-check ~/.claude/skills/
cp -R reference/2026-10-27-skills-procedure-hub/procedure-hub-relation-check ~/.claude/skills/
```

스킬 본문의 경로는 프로필 레포 기준이다 — 전역으로 깔아도 이 레포에서 쓰는 것을 전제로 한다.

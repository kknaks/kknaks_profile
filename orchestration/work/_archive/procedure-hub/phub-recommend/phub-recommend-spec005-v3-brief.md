# 발주서 — SPEC-005 v3 · WORK-005: 허브 응답 설계 수정(전달 문제 B 239건 + 앱 오류 15건)

## 왜
hub-evals 239문항 실행 → 골드 실패 320건 전수 분류(`reference/2026-10-30-hub-evals/build-out/fail-triage.md` · 정본): **B 골드엔 있는데 허브가 안 줌 239건(75%)** · A 골드에 없음 61 · C 6 · D 0. 이번 작업은 **B 전부 + 오류 15건**만. A(데이터)는 다음 단계(실버 9단계)라 범위 밖.

## 입력(읽기)
- `fail-triage.md` §3(빠진 칸 20종 · 큰 묶음 ①②④⑤⑥⑦⑧ · 예) · §3-1(Jev) · §5(그래프) · 부록 320행 · `fail-triage.json`
- `SPEC-005.md`(현행 v2 PASS) · `WORK-003.md` · `review-spec005-v2-report.md`
- 허브 코드(읽기만 · 수정 금지) `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend` — 도구 · section 매핑 · slim 카드 · 의도 경로 실물. 18005 떠 있음(호출 가능 · 서버 손대지 말 것)
- `build-out/work003-report.md` · `cli-provider-report.md` 「SPEC-006 과 다른 점」 — 구현이 SPEC 과 이미 달라진 점(cc_roots · technique_excluded · slim/sections/limit · 조사 떼기 · family/product 펼침)
- `_RESUME.md` §2 결정표(정해진 것 다시 열지 않기 · 허브에 LLM 없음 · 결정론 · 병원 독립)

## SPEC-005 v3 에 넣을 것(B 묶음 ↔ 조항 1:1 · 근거 건수 적기)
1. **의도별 고정 동봉(⑤ 90 · ⑦ 20)** — recommend · procedure_card · resolve 가 돌려주는 시술 노드마다 1-hop 이웃을 **의도에 따라 고정으로** 같이 냄: site_caution(부위 위험) · check_condition(금기 조건) · 쌍 관계 간격/순서(엣지 속성 → 응답 필드로). 의도 I-01~I-12 × 동봉 묶음 표. 크기 상한과 함께(slim 원칙 유지 · 동봉은 요약 꼴 + id)
2. **의도 → 섹션 기본 묶음(① 53)** — 허브가 `intent=` 를 받아 섹션을 기본 붙임(Jev · Claude 가 안 골라도): I-02 → overview · method / I-03 → aftercare · recovery / I-04 → safety.* · management / I-05 → recovery · timeline / I-06 → compare 차이 필드 / I-07·08 → pair evidence / I-09 → checks · site_caution / I-10·11 → products · market. 표로. `sections=` 명시가 오면 합집합
3. **쌍 관계(④ 27)** — pair_check · compare 가 evidence(간격 · 순서 · 이유)를 기본 포함 · I-07·08 경로는 쌍 도구 필수 · 같은 계열 자기 쌍 처리
4. **full 전용 속성(⑥ 18)** — 가격대 · 계열 overview · 조합 구성 중 어느 것을 slim 으로 올릴지(건수 기준으로 정하고 나머지는 섹션으로)
5. **섹션 매핑 구멍(② 16) · 안 붙은 fact(⑧ 15)** — fail-triage 부록에서 해당 fact id 전부 열거 → 붙일 노드 · 섹션 규칙(step8 메모 · CC 조합 fact 의 owner 정하기)
6. **check_conditions 가 family · product id 를 받으면 단위 시술로 펼쳐 합침**(오류 15 · resolve 펼침과 같은 규칙)
7. 구현이 이미 달라진 점(cc_roots 등 위 목록)을 v3 본문에 반영해 SPEC = 실물로
8. **끝 조건(측정)**: 실패 174문항 재실행에서 B 로 분류된 건의 인용이 허브 응답에 들어가는 비율 — 결정론 검사(fail-triage 와 같은 대조 스크립트)로 ≥ 90% · 응답 크기 중앙값 상한(현 7.2KB 기준 ×2 이내) · 기존 품질 6/6 · 106/106 유지

## WORK-005
WP 로 쪼개기(동봉 / 섹션 묶음 / 쌍 / fact 재부착 / checks 펼침 / 측정 스크립트) · WP 마다 시험 · 끝 조건 · 검수 PASS 뒤 구현 발주는 코디가.

## 제약
스펙 문서만(코드 · 데이터 수정 금지) · 열린 결정은 「아직 안 정한 것」에 적고 추측으로 메우지 않기 · 원장 인용 본문은 스펙에 옮기지 않기(fact id · 경로만 — 공개 레포) · 끝나면 worker_done(바뀐 조항 목록 + 아직 안 정한 것).

# 발주서 — SPEC-005 v3(0.3.0) · WORK-005 검수(읽기 전용 · 결과 보고서만)

## 대상
`orchestration/work/phub-recommend/SPEC-005.md`(v3 · §5-13 ~ §5-15 · §6-5 · §7 V-1~V-5 새로 들어감) · `WORK-005.md`(WP-0 ~ WP-7)

## 검수 기준(FAIL 은 조항 번호 · 근거 · 고칠 방향까지)
1. **전수 대조**: `reference/2026-10-30-hub-evals/build-out/fail-triage.md` §3 빠진 칸 20종 · 큰 묶음 ①②④⑤⑥⑦⑧ 239건이 v3 조항에 **빠짐없이** 대응되는가(묶음 → 조항 표를 직접 만들어 대조 · 대응 없는 건수 0 이어야 PASS). 부록 320행 중 B 행을 표본 아닌 **전부** 훑어 조항으로 닫히는지
2. **실물 대조**: 허브 코드 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend`(읽기만) 의 도구 시그니처 · section 이름 · 노드 종류 · fact 구조와 스펙의 이름 · 경로가 같은가 — 없는 section · 필드 이름을 스펙이 쓰면 FAIL
3. **결정표 충돌**: `_RESUME.md` §2 결정(허브 LLM 없음 · 결정론 · slim D-14 · G13 안전 동봉 · 충돌 = 하나 · 실버 수정 없음)과 어긋나는 조항
4. **끝 조건(§6-5) 검증 가능성**: 재인용률 분모 · 판정 규칙 · 크기 상한이 숫자로 닫혀 있고 fail-triage 와 같은 대조로 재현되는가
5. **WORK-005**: WP 의존 순서 · WP 마다 시험 · 끝 조건이 §6-5 와 1:1 인가 · 코드 표면이 열거되어 있는가(「고칠 곳 N개」가 아니라 쓰는 곳 전부)
6. §7 V-1 ~ V-5 외에 **본문이 추측으로 메운 자리**가 있는가

## 산출
`review-spec005-v3-report.md` — 판정 PASS/FAIL · 기준별 표 · FAIL 목록(조항 · 근거 · 방향) · 스펙 · 코드 수정 금지. 끝나면 worker_done(판정 + FAIL 수).

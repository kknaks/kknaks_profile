# 발주서 — SPEC-005 v3.4(0.3.5) · WORK-010: 실버 9단계(설명 사실)를 골드에 반영
정본 입력: `step9-decisions.json` · `step9-explanations.json/.md` · `step9-research.md` · 로그 `para/projects/company/procedure-hub/log/2026-11-01-silver-step9-explanations.md` · 효과 `step9-effect.*` · 점검 스킬 `procedure-hub-explanation-check` · `semantic.json`(값 사전 8 반영본) · `SPEC-005.md`(0.3.4).
넣을 것:
1. §2 입력 계약에 step9 파일 · 해시 가드 추가 · §3 빌드 규칙(G 번호)으로 step9 레코드 → fact(G9-1 id 꼴 · section 매핑 D9-1/2/8/9 · resolved 하나 + alternatives 는 골드에 원문 안 내보냄 또는 alternatives 칸 — D-13b 와 같게) · 값 사전 8 → globals(D9-7)
2. 새 section `safety.management`(D9-1)를 §4-3 · §5-14′(의도 → 섹션 기본 묶음 · I-04 에 추가 · V-4 닫음) · §5-16(peek sections · expand) · SPEC-006 §3-4-1-1 의도별 고정 섹션(I-04)에 미치는 영향 한 줄(006 은 코디가 따로)
3. V-4 문구 정정(severity_levels 는 이미 골드 24/24)
4. 끝 조건: 빌드 결정론 · 가드 · step9 fact 5,312 가 export 에 · section 별 셈 · 2차 A 54 · v5a A 30 중 골드 fact 로 닫히는 행(step9-effect 와 같은 셈) · 기존 품질 6/6 · 106/106 · walk3 재생 숫자 회귀 없음 · 크기 표 영향
5. WORK-010 WP(입력 · 빌드 규칙 · section · 시험 · 발행) · 코드 표면 grep 전부
제약: 스펙 문서만 · 실버 수정 없음 · 원장 인용 본문 금지 · 열린 것 §7 · worker_done.

# 발주서 — 「핵심 수치 카드」 스펙(SPEC-005 0.3.6 + SPEC-006 0.3.7 · 한 판으로 · 짧게)
## 왜
rerun-v6a case3 정확성 실패 65 대조: 걷기가 가져왔는데 답이 안 씀 0 · **골드에 있는데 걷기가 못 가져옴 45(69%)** — 대부분 시술마다 있는 핵심 숫자(지속 · 시작 · 다운타임 · 간격 · 횟수 · 가격대)가 여러 section 에 흩어져 Jev 의 섹션 선택 하나로 못 모음. 안전은 필수 묶음(checks · site_caution 늘 받기)으로 61→81% 회복 → 숫자도 같은 방식으로.
## 넣을 것
1. SPEC-005(허브): 시술 노드(단위 · 제품 · 계열)마다 **key_facts 카드** — 칸 고정(onset · duration · downtime · interval · sessions · price_range · 필요하면 anesthesia · pain) · 각 칸 = 정본 fact 하나(id + 한 줄 · 결정론 고르기 규칙: 그 노드 자신 fact 우선 → 단위면 계열 · 9단계 resolved 값) · 없으면 빈 칸(gap) · 크기 ≤ 1KB · 새 도구 또는 peek/expand 의 `key_facts` 칸(실물 보고 정함) · REST · MCP 같은 코어 · LLM 없음
2. SPEC-006(앱): 필수 묶음 확장 — 답에 나올 시술 rank 상위 3 은 걷기와 별개로 key_facts 를 늘 받음(예산 먼저 차감) · Claude 꼴에 「핵심 수치」 블록 · 기록 칸 walk.key_facts
3. 끝 조건: v6a 정확성 실패 45 중 key_facts 로 닿는 행 수(결정론 셈 · 근거 스크립트) · 카드 크기 · 기존 품질 · 재측정 = **rerun-v8a(case3 · sample50-questions.txt 50문항 · v7a 와 같은 문항)**
4. WORK-011(허브) · WORK-012(앱) WP · 코드 표면 grep
제약: 스펙 문서만 · 실버 수정 없음 · 원장 인용 본문 금지 · 열린 것은 추천값과 함께 §7 · **검수는 코디가 짧게 · 이 판으로 끝낼 것** · worker_done(닿는 행 수 · 카드 꼴).
입력: `reference/2026-10-30-hub-evals/runs/`(v6a 배치 b202611011935-f9a211) · 새 export `PROCEDURE-HUB/phub-recommend/backend/build-out/gold-export.json`(567677ed) · SPEC-005 0.3.5 · SPEC-006 0.3.6 · `phub-recommend-walk-fix2.md`.

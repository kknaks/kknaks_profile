# [backend] 허브 응답 짧게(D-14) — 기본 = 짧은 카드 · 상세는 sections 로 (사용자 10-30)

(앞 작업 WORK-003 이어서 · 코드 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend` · 로컬 커밋만 · push 금지)

## 왜(사용자)
실험 실물 질문에서 `recommend` 응답 하나가 **145KB(약 5만 토큰)** — 연결된 시술마다 금기 · 부작용 · 합병증 · 위험지대 · 사후관리 · 근거 원문이 전부 실림. case2 · case3 입력 · 응답 시간 · 비용의 대부분. 사용자: 「모든 단계를 다 받아야 해? · 질문 한 번에 2달러는 너무 비싸」. SPEC-005 D-14(카드 slim 기본 · 원문은 sections 요청)를 구현이 지키지 않음.

## 할 일
1. **도구 9 기본 응답 = 짧은 카드**: 노드 id · 이름 · 왜 붙었나(엣지 종류 · 층 · CC) · 표시(flags 이름만) · **안전 요약은 늘**(10-26 경계 — 금기 · 같은 날 불가 · 피함 · 응급 징후의 **이름 · 등급만**, 원문 없음) · fact id 목록(원문 없이) · 「더 있음」 개수
2. **`sections` 입력**(모든 도구 · 쉼표 목록 · SPEC-005 §4-3 section 이름 그대로: overview · method · recovery · aftercare · timeline · emergency · disclosure · safety.side_effects · safety.complications · safety.pih · checks · site_caution · dose · products · evidence · ops · market): 요청한 section 만 원문 facts 를 붙임 · `sections=all` = 지금 응답(실험 대조용)
3. **응답 크기 목표**: recommend 기본 ≤ 8KB(실물 「팔자주름」 · 「이마 주름」 질의로 측정) · 다른 도구도 기본 크기 보고
4. claude_contract 는 그대로(실린 fact id 만 allowed)
5. **품질 6/6 · 106/106 유지**(어댑터 `scripts/gold_quality_eval.py` 가 필요한 section 을 요청하게 — 정답 · 문항은 안 건드림) · REST · MCP 같은 응답 · 시험 · ruff · 속도
6. 허브 18005 재시작은 코디가 함(사용자 실험 중일 수 있음) — 끝나면 worker_done 에 「재시작 필요」만 · `build-out/work003-report.md` 에 「SPEC 과 다른 점」 갱신
## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_5aa0d8e8-74db-4b9f-9be6-467f20566ac3 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "backend 완료: 허브 짧은 카드" --body "recommend 기본 N KB(팔자 · 이마) · 품질 N/6 · N/106 · 시험 N passed · 커밋"
orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb --text "[worker_done] backend 완료 — 허브 짧은 카드. 상세는 인박스." --enter
```

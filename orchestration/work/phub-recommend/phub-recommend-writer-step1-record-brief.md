# [writer] 실버 1단계(제품 원장) 정규화 과정 기록 — 전후 비교 · 교육 자료용

역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/writer/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 쓸 곳 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/projects/company/procedure-hub/` — 먼저 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/projects/company/procedure-hub/README.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/para.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/projects/project.md`(company/ 규칙)를 읽고 그 규칙에 맞는 자리 · 이름을 정하라(예: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/projects/company/procedure-hub/notes/2026-10-28-silver-step1-product-normalization.md` 또는 규칙상 맞는 곳). README 지도에 한 줄 추가.

## 사용자 요구(10-28)
「지금 어떻게 정규화했는지 과정을 기록 — **전후를 비교**해야 하고 **교육 자료용**」

## 원천 (전부 읽어라)
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/_RESUME.md` §2 결정표(10-26 ~ 10-28 전 행) — 규칙 · 결정 · 정정의 정본
- 전(before): stg 스냅샷 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/`(taxonomy.json 원장 · products) · `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/research-report.md` · `product-master-draft*.json` · `step1-products-A/B/C`
- 후(after): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-products.json` · `.md` · `step1-apply-log.md` · `step1-source-fix.md` · `step1-origin-questions.md`
- 과정: `step1-decisions.json`(32묶음) · 조사 결과(`step1-d09-web` · `d12-web` · `d15-web` · `d16-web` · `d17` · `d17-2` · `d18` · `d19` · `d20-31` · `cancel-recheck` · `export-recheck` · `domestic7`) · 검수(`review-step1-report` · `-v2` · `-v3` · `-v4`) · `gate-answers/step1-decisions-db-2026-10-28.md`
- 도구: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-mfds-mcp/NOTES.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-28-kpic-mcp/NOTES.md`

## 담을 것 (교육 자료 — 처음 보는 사람이 따라올 수 있게, 쉬운 말)
1. **왜** — 「○○가 고민이에요」 추천을 하려는데 원장이 왜 그대로 못 쓰였나(이름 섞임 · 허가 없음 · 중복 · 메뉴명이 제품 자리에 · 업체 오기 등) — 실제 예로
2. **전후 비교** — 수치 표(행 수 · 상태별 · 허가 연결 · 업체 칸 채움 · 추천 가능) + **같은 제품의 전/후 레코드를 나란히** 5~8개(디클래씨 · 젠틀맥스프로 · 슈링크(수출용) · 리프세라→리프테라 · 에이비오톡신→디스포트 · PHA필(제품→시술 이름) · 온다(라인 · 품목) · 더채움 프리미어(오기))
3. **정한 규칙** — 각 규칙 한 줄 + 왜 + 예: 정상만 연결 · 취소는 이력 · 수출용은 국내 허가 아님 · 재제조는 정품 아님 · 비침습 ≠ 허가 대상 아님 · 허가번호 미확인(유통 확인)은 추천 포함 · 이름 3칸 · 라인/품목 · 업체 역할 여러 개 · 1단계는 제품↔허가만 · 추정 금지
4. **과정** — 조사(워커) → 결정 목록(사람) → 반영 → 검수 루프 · 결정 페이지 · 묶음 설계 · 「추천은 추천대로, 사람은 최종 판단만」으로 바뀐 흐름 · 쓴 출처(식약처 API · emedi · KPIC · 피부과 홈페이지 · 병원 가격 자료 · FDA · 제조사 공식)
5. **틀렸던 것 · 배운 것** — 정직하게: 수출용 규칙 과적용(124건 해제 → 원인은 원장이 수출 허가에 붙어 있던 것) · 이름 질의로만 찾아 놓친 허가(젠틀맥스 · 벨라소닉 · 고우리) · 「Joule = IPL 없음」 일반화 · 「비침습이라 미용기기」 추정 · 라라젯 미용기기 확정 정정 · 결정 개수 셈 단위(묶음 vs 행) 혼동 · 질문에 제품 이름 빠진 카드
6. **남은 것** — 병원 질문 · 원천 수정 · 2단계로 넘긴 것
- 실명(개인) · 키 금지. 회사 · 제품 · 허가번호는 그대로. 수치는 파일에서 다시 세어 쓴다(이 브리프 수치 베끼지 말 것). 추정 금지

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: 1단계 정규화 기록" \
  --body "파일 경로 / 섹션 / 전후 수치 요약"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] writer 완료 — 1단계 정규화 기록. 상세는 인박스." --enter
```

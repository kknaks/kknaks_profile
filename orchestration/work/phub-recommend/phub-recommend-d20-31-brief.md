# [researcher] 1단계 남은 조사 8묶음 — 묶음별 추천 + 근거

역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 방법 · 출처 · 형식은 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-d18.md` · `step1-d19` 브리프와 같게. MFDS MCP `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-mfds-mcp/` · emedi · 피부과 홈페이지(데이뷰의원 · 세라미크의원 · 다른 피부과) · `/Users/kknaks/Downloads/data-anyang`(read-only) · 공식 · 보도.

## 대상 — `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-decisions.json` 의 묶음 · 행(상세 `step1-products.json` · 원천 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/taxonomy.json`)
- **D20** 정체 · 분류 충돌(8) — 제품이 무엇인지 출처로 확정
- **D22** 주사 · 스킨부스터 이름 근거 0(11) · **D23** 장비 이름 근거 0(19) — 실제 제품인지 · 제조/수입사 · 현행 국내 허가(업체명으로 재탐색). 실제 제품이 아니라 메뉴명 · 일반명이면 그렇게 표시(→ 5단계 시술 이름 후보)
- **D25** 초안 대비 바뀐 연결(29) — 바뀐 판정이 맞는지
- **D28** 근거 약한 연결(4) · **D30** taxonomy 제품 부분 일치(3) — 같은 제품인지
- **D29** 새로 넣은 taxonomy 제품(13) — 실제 제품 · 국내 허가 · 원장에 둘지
- **D31** 「허가 대상 아님」 근거(4) — 출처 확인

## 이미 정한 규칙(`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/_RESUME.md` §2) — 지켜라
정상 허가만 연결 · 취소/취하는 이력 · 수출용은 국내 허가 아님 · 비침습 ≠ 허가 대상 아님 · 재제조는 정품 아님 · 이름 규칙(대표 한글 1 · 허가 이름 · 검색 이름) · 1단계는 제품↔허가만(시술 범위는 5단계) · 추정 금지 · URL/질의 없는 칸 금지 · 판매사 여러 개

## 산출
`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-d20-31.json` · `.md` 만. 원장 · 결정 파일 수정 금지.
md 맨 위: **묶음마다 추천 한 줄 + 사용자가 판단해야 하는 행만 따로 목록**(이유 한 줄). 나머지는 행별 한 줄 결론 + 근거.

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 1단계 남은 조사 8묶음" \
  --body "묶음별 추천 한 줄 / 사용자 판단 필요 N행"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] researcher 완료 — 1단계 남은 조사 8묶음. 상세는 인박스." --enter
```

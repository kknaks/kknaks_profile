# [reviewer] 1단계 제품 원장 검수 — 원천 대조 (끝 조건: 미확인 0 · 근거 없는 칸 0)

역할: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/reviewer/role.md` (read-only). 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`.

## 대상 · 기준 (`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/`)
- 대상: `step1-products.json` · `.md`(합친 제품 원장) · `step1-decisions.json` · `.md`(사람이 정할 것)
- 기준: 브리프 `phub-recommend-step1-A-brief.md`(필드 1~7 · 「미확인 0」 · 추정 금지) · `_RESUME.md` §2 10-27 행(제품 이름 정규화 · 라인 제품 · 함량만 다른 허가 = 한 제품 + 규격 · 업체 역할 3종 · 같은 허가 원장 중복 = 라인 + 품목 · 현장 기기 포함)
- 원천: stg `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/`(taxonomy 원장 항목) · 구간 산출 `step1-products-A/B/C.json`(질의 기록 · 근거) · 식약처 확인이 필요하면 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-mfds-mcp` 패키지로 **표본만**(키 출력 금지)

## 볼 것
1. **빠짐**: taxonomy 의 제품 · 장비 성격 원장 항목이 전부 들어왔나(원장 id 로 대조) · 현장 기기 35 전부
2. **근거 없는 칸**: 허가 · 업체 역할 · 정체에 근거(식약처 필드 · URL · 질의 기록) 없이 채운 것
3. **틀린 연결 표본 검사**: 허가가 연결된 항목에서 무작위 30개 + 「자동」 성격 전부를 식약처 값과 대조(이름 · 업체 · 사용목적이 그 제품인가 — 1단계에서 유축기 · 안과 레이저 같은 엉뚱한 연결이 발견된 전례)
4. **「확인 불가」가 진짜 다 찾았나**: 질의 기록(API · emedi · 웹)이 있는가
5. **결정 목록**: 원장의 ⚑ · 게이트 · 확인 불가 · 변경이 빠짐없이 들어갔나 · 질문이 「무엇이 부족해서 무엇을 정하는지」 한 줄로 되어 있나

## 산출물
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/review-step1-report.md` 1개 · 맨 위 PASS/FAIL · 지적마다 원장 id + 근거

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: 1단계 <판정>" \
  --body "빠짐 / 근거 없는 칸 / 틀린 연결 / 결정 목록 누락"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] reviewer 완료 — 1단계 <판정>. 상세는 인박스." --enter
```

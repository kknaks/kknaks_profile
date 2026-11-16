# [researcher] 1단계 D16 — 같은 제품인지 2쌍 국내 웹 확인

역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 형식은 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-d09-web.md` 와 같게. 행 상세 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-products.json` · 원천 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/taxonomy.json`(detail · extracted).

## 대상 (메디컬 스킨케어 · 허가 대상 아님)
1. **PHA필(auto-M15-1775401670325) ↔ 물톡스(auto-M15-1775402148301)** — 원천 PHA필 detail 「물톡스 · PHA 기반」. 물톡스가 ① PHA필과 같은 제품 ② 다른 제품 ③ 제품이 아니라 시술 이름(물+보톡스류 일반명) 중 무엇인지
2. **라라닥터 ↔ 라라필(M15-1-7)** — 원천 detail 「라라필 의료용 업그레이드」. 같은 회사 · 같은 라인의 다른 제품인지, 같은 제품의 다른 이름인지

## 할 일 (대한민국 기준)
- 제조 · 판매사 공식 사이트 · 보도 · 병원 시술 페이지 · 식약처(화장품이면 화장품 여부도) — 성분 · 회사 · 출시 · 관계
- 결과: 같은 제품 / 같은 라인 다른 제품 / 시술 이름 / 확인 불가(질의 기록). 업체 · 판매사(여러 개) · URL 필수 · 추정 금지

## 산출
`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-d16-web.json` · `.md` 만. 원장 · 결정 파일 수정 금지

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: D16 2쌍 웹 확인" \
  --body "쌍별 결과 · 업체 · 판매사"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] researcher 완료 — D16 2쌍 웹 확인. 상세는 인박스." --enter
```

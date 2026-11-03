# [researcher] 1단계 D09 — 이름만 맞춘 16개 국내 웹 확인 + 판매사(여러 개)

역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`.

## 대상
`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-decisions.json` 묶음 **D09**(16행: 톡스온 · 퍼펙타 · 아말리안 · 매쿰7 · 트리니티 · 리레이저 · 포커스듀얼 · 소노퀸 · 큐어젯 · 하이쿡스 · 올타이트 · 덴서티하이 · 이브타이탄 · 이래비티 · 소노케어 · 더마큐어). 원장에 업체가 없어 이름만으로 허가에 연결된 것들. 행 상세는 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-products.json`.

## 할 일 — **대한민국 기준** 웹(제조 · 수입사 공식 사이트 · 국내 보도 · 학회/전시 · 병원 장비 소개 · 공시)
1. **연결 확인**: 원장 이름(한글 브랜드) ↔ 연결된 허가 업체 · 제품이 같은 제품인지 출처로 확인. 결과 = 일치 / 불일치(다른 제품이면 무엇인지) / 확인 불가(조사 기록)
2. **판매사**: 국내 판매 · 유통사를 **전부**(여러 개 가능) — 각각 이름 · 역할 표기(총판 · 공동판매 · 유통 · 미용 적응증 판매 등 출처 표현 그대로) · 출처 URL · 시기(있으면). 없으면 「근거 없음(조사 기록)」
3. 제조사 · 수입사도 허가와 다른 출처가 나오면 충돌로 기록(덮어쓰지 않음)
- 추정 금지 · URL 없는 칸 금지 · 실명(개인) 금지

## 산출
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-d09-web.json` · `.md` (행별: ledger_id · 연결 확인 · 판매사[] · 충돌 · 출처 · 질의 기록) — 원장 · 결정 파일은 건드리지 않는다(코디가 반영 판단)

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: D09 국내 웹 확인" \
  --body "일치/불일치/확인 불가 수 / 판매사 찾은 제품 수 · 판매사 총수 / 충돌"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] researcher 완료 — D09 국내 웹 확인. 상세는 인박스." --enter
```

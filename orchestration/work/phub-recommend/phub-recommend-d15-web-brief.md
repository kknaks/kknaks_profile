# [researcher] 1단계 D15 — 실 3종 현재 제품 · 허가 국내 웹 확인

역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 방법 · 형식은 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-d09-web.md` 와 같게. 행 상세 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-products.json` · `step1-cancel-recheck.json`.

## 대상 (실리프팅)
1. **울트라V** — 연결 허가 제허 13-1398(정상)의 업체 · 제품명 확인. 원장 detail 「PDO전문」. 업체 「울트라브이」(제허 14-182 취하)와 같은 회사인지 · 원장 「울트라V」가 어느 회사의 어느 실인지. 이전 기록 「울트라V ≈ V리프트(울트라브이 Ultra V Lift)」도 확인
2. **해피리프트** — 이름 일치 허가 수허 05-144 는 2015 취하. 국내 현재 유통 · 현재 허가(제조사 Promoitalia 등 · 수입사 변경 여부) · 후보 APTOS(수허 25-219)와의 관계
3. **오메가리프트** — 이름 일치 허가 제허 12-516 · 12-419 는 2013 취하. 국내 현재 유통 · 현재 허가 · 후보 오브이메디 「OMEGA VJ」(제허 23-814)와 같은 제품인지(병원 「오메가실」 페이지 포함)

## 할 일 (행마다, 대한민국 기준)
- 식약처 API · emedi(업체명 · 제품명 · 영문 · 모델) + 웹(공식 · 보도 · 병원 시술 페이지)
- 결과: 현재 허가 특정(허가번호 · 업체 · 모델) / 후보와 같은 제품(출처) / 확인 불가(질의 기록)
- 판매사 여러 개 · URL 필수 · 추정 금지

## 산출
`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-d15-web.json` · `.md` 만. 원장 · 결정 파일 수정 금지

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: D15 실 3종 웹 확인" \
  --body "제품별 결과(허가 · 업체 · 판매사) / 확인 불가"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] researcher 완료 — D15 실 3종 웹 확인. 상세는 인박스." --enter
```

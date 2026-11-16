# [researcher] 1단계 D19 — 실재 제품인데 국내 허가 못 찾은 11개 재탐색

역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 형식 · 출처 방식은 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-d18.md` 와 같게(md 맨 위 행마다 쉬운 한 줄 결론). MFDS MCP `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-27-mfds-mcp/` · emedi. 행 상세 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-products.json` · `step1-decisions.json` D19.

## 왜
젠틀맥스 · 젠틀레이즈 · 브이빔퍼펙타는 이름 질의 0 이었지만 **수입사 이름**으로 찾으니 현행 허가가 있었다(`step1-cancel-recheck.md`).

## 대상 11
시크릿맥스(기사 「2024-05 식약처 허가」 — 그 허가를 특정) · 벨라소닉 · 더마펜4(본체) · 이볼브(InMode — 신한네트웍스 허가 3건 · EVOKE 26-107 과 다른 제품인지) · 쿨톤(Allergan/애브비) · 벨카이라 · 카이벨라(D16 에서 벨카이라로 묶임 · 의약품) · 리포린(의약품) · 미라쥬 · 슬렌더엑스 · 시너론 아이플러스

## 할 일 (행마다)
1. 제조사 · 국내 수입사 · 판매사 특정(피부과 홈페이지 — 데이뷰의원 · 세라미크의원 · 다른 피부과 · `/Users/kknaks/Downloads/data-anyang` read-only · 공식 · 보도)
2. 그 **업체명**으로 식약처(의료기기: 업체 · 모델 · 품목 / 의약품: 업체 · 성분 · 영문명) + emedi 재탐색 — 수출용(「수출용에 한함」)은 국내 허가로 치지 않음(10-27 규칙)
3. 결과: 현행 국내 허가 찾음(번호 · 업체 · 모델 · 상태) / 없음(질의 기록 전부) / 비의료기기 여부는 출처 있을 때만 — **비침습 ≠ 허가 대상 아님**(10-27)
- 판매사 여러 개 · URL 필수 · 추정 금지

## 산출
`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-d19.json` · `.md` 만. 원장 · 결정 파일 수정 금지

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: D19 11개" \
  --body "허가 찾음 N / 없음 N — 행별 한 줄"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] researcher 완료 — D19 11개. 상세는 인박스." --enter
```

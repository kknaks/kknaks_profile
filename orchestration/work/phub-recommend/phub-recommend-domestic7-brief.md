# [researcher] 수출 전용 허가만 남은 7개 — 국내 내수 허가 찾기

역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 배경 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-export-recheck.json` · `step1-apply-log.md`(수출용 재판정): 슈링크 · 더블로 · 뉴라미스 · 시크릿RF 는 같은 업체의 **다른 내수 허가**가 있었다. 남은 7개도 국내에서 팔리는지 · 내수 허가가 다른 이름/모델로 있는지 찾는다.

## 대상
인트라셀 · 고우리 · 더블로 골드 · 잼버실 · N코그 · 에코2 에볼루션 · 스텔라듀오 (`step1-products.json` open 행)

## 할 일 (행마다)
- 같은 업체의 전체 허가 목록(식약처 API 업체명 · emedi 업체 검색)에서 xprtppYn=N(내수) 허가 중 이 제품에 해당하는 것 — 모델명 · 제품명 · 품목 · 허가 시기 대조
- 국내 유통 출처(피부과 홈페이지 · `/Users/kknaks/Downloads/data-anyang` read-only · 공식 · 보도)
- 결과: 내수 허가 찾음(번호 · 근거) / 국내 유통 확인 · 허가 특정 못 함(→ 허가번호 미확인 규칙) / 국내 유통 근거 없음(→ 확인 불가)
- 추정 금지 · URL/질의 기록

## 산출
`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-domestic7.json` · `.md` 만(원장 수정 금지 — 검수 중)

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 내수 허가 7" \
  --body "행별 한 줄"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] researcher 완료 — 내수 허가 7. 상세는 인박스." --enter
```

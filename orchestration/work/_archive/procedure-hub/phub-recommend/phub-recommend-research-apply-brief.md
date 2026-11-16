# [researcher] 업체 관계 결정 반영 · 원천 수정 목록 보강

역할: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`.

## 사용자 결정(10-27, `_RESUME.md` §2 「업체 관계 조사 반영」 행)
- `company-relation-check.json` 23개: 같은 제품 17 → 허가 연결(조사에서 고른 허가 · 복수 허가 5건은 유효(정상) 허가 전부 · 취소뿐 4건은 취소 허가로 연결하되 상태 「취소」) · 다른 제품 2 → 해당 허가 없음 · 확인 불가 4 → 허가 미확인
- 업체 역할 3종(제조사 · 수입사 · 판매사) — 항목마다 누가 무엇인지 조사 결과 그대로(근거 URL)
- 원장 업체 오기 → 원천 수정 목록에 추가

## 할 일
1. `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/gate-answers/company-relation-decisions.json` 생성 — 항목마다 {ledger_id, decision(link|no_license|unconfirmed), license_keys[], roles{manufacturer, importer, seller}, sources[]}
2. `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/source-fix-list.json` 에 새 그룹 추가(기존 그룹 · 항목 · 답 id 는 건드리지 않는다): **E7 원장 업체 표기 오류**(이번 6건 + 4차 md ⑤ 의 업체 오류 — 인에이블=동국제약 화장품 등) · **E8 원장 이름 오기**(리즈톡신 → 리즈톡스 등 지금까지 확인된 것). 항목 모양은 기존과 같게(current · proposed · why · evidence · 출처 URL). md 도 갱신
3. 원천 수정 목록 아티팩트용 HTML 을 다시 만든다: 템플릿 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/source-fix-review.template.html` 의 `/*__DATA__*/` 자리에 갱신된 JSON 을 넣어 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/source-fix-review.html` 로(코디가 게시한다 — 너는 파일만)

## 제약
- 식약처 · stg · 웹 새 호출 없음(이미 있는 조사 결과만). 다른 파일 수정 금지

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 업체 관계 반영 · 원천 수정 목록" \
  --body "결과 / 산출물 / 미결"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] researcher 완료 — 업체 관계 반영 · 원천 수정 목록. 상세는 인박스." --enter
```

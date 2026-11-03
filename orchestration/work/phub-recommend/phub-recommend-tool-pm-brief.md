# [tool_dev] 제품 허가 매칭 페이지 — 업체 관계 결정 23건 반영

역할: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/tool_dev/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`.

## 할 일
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/product-match-review.html` 의 내장 데이터(`<script id="data">`)에서 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/gate-answers/company-relation-decisions.json` 의 23건을 반영한다:
  - link 18 → 상태 `auto`(자동 확정 묶음으로 이동), `autoKeys` = 결정의 license_keys, 설명 한 줄 「업체 관계 조사로 확정: <관계> (근거 URL)」, 업체 역할(제조사 · 수입사 · 판매사) 표시
  - no_license 2 → 「해당 허가 없음」 확정 표시 · unconfirmed 3 → 상태 `unknown`(허가 미확인)
- 결과적으로 「직접 확인」 카드가 0 이 되게. 페이지 코드 · 스타일 · db 컬렉션(answers)은 바꾸지 않는다
- 데이터에 U+FFFD 글자가 있으면 JSON 이스케이프(\\ufffd)로 바꾼다(게시가 막힌다)
- node 로 스크립트 구문 검사 1회 · 상태별 수 출력

## 산출
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/product-match-review.html` 수정만(게시는 코디)

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "tool_dev 완료: 제품 페이지 23건 반영" \
  --body "상태별 수 / 직접 확인 남은 수"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] tool_dev 완료 — 제품 페이지 23건 반영. 상세는 인박스." --enter
```

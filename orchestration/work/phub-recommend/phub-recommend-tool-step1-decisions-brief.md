# [tool_dev] 1단계 결정 목록 페이지 — 사람이 정할 것만

역할: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/tool_dev/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/` 에 HTML 하나를 만든다(코디가 아티팩트로 게시).

## 사용자 요구(10-27)
- 「결정해야 할 것 리스트업」 — **묶음마다 첫 줄: 무엇이 부족해서 · 무엇을 정하는가** 한 문장. 그 아래 선택지. 원장 행 · 근거는 접어 둔다
- 「글만 길고 알맹이 없다」 금지 — 설명은 한 줄, 정보 나열 금지
- 정할 게 없는 것(이미 정해진 미허가 · 취소 등)은 페이지에 넣지 않는다

## 입력
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-decisions.json` · `.md` (32묶음) · 행 상세는 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-products.json` (ledger_id 로 조인)

## 화면
- 맨 위: 1단계 상황 한 줄(제품 원장 390행 중 정해진 것 / 정할 것 묶음 수 · 남은 수)
- 묶음 카드: 제목 = 질문 한 줄 · 선택지(라디오, 묶음 전체에 한 번 · 묶음 안 개별 예외는 행마다 바꿀 수 있게) · 「다른 답」 입력 · 행 목록(제품 이름 · 지금 값 · 근거 한 줄)은 접힘
- 저장: window.claude.use('db') · 컬렉션 decisions(묶음 id → {choice, other, exceptions{ledger_id: choice}}) · 저장 상태 표시 · 테마 토큰 · 폰트/CDN 규칙은 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/product-match-review.html` 과 같게
- 데이터 안 U+FFFD 는 JSON 이스케이프로
- 산출: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-decisions.html` 1개 · node 구문 검사 1회

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "tool_dev 완료: 1단계 결정 페이지" \
  --body "묶음 수 / 파일 크기 / 검사 결과"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] tool_dev 완료 — 1단계 결정 페이지. 상세는 인박스." --enter
```

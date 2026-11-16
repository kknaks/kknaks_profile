# [tool_dev] 실버 승인 페이지 — 단위 시술 · 질문 · 계열 이름 (승인 게이트)

역할: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/tool_dev/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 이번엔 reference 가 아니라 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/` 에 HTML 파일 하나를 만든다(코디가 아티팩트로 게시).

## 배경
사용자(10-27): 실버가 확정돼야 골드를 빌드한다. 남은 결정을 **한 페이지**에서 한다. 사용자 피드백 — 「글만 길고 무엇이 부족해서 무엇을 결정하는지가 없다」. **카드마다 첫 줄에 「무엇을 정하는가」 한 문장**, 근거는 접어 둔다.

## 입력 (`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/procedure-master-v3.json`)
- 계열 23(`families`, name_status 가 source_name_provisional 인 16 이 결정 대상) — 공식 일반명 후보는 계열 동의어 + 원천 이름에서(지어내지 마라). 선택지: 후보 중 하나 / 직접 입력
- 단위 시술 236(`unit_procedures`, approval ≠ approved 인 206 이 결정 대상) — 카드: 「<이름> = <계열> × <부위> × <기법> 맞습니까?」 + 근거(evidence 접힘) · 승인 / 반려(사유 필수). **계열별 일괄 승인**(두 번 눌러 실행) 필수
- 질문 59(`provisional`) — 「<항목> : <질문>」 + 선택지(options) 라디오 + 직접 입력. 현재 임시 적용값 표시
- 맨 위 상황판: 메달리온 층별 진행(실버 원장 4개 — 부위 끝 · 제품(별도 페이지 링크 https://claude.ai/artifact/7Sp9nWc9VirzwTkXZTWhKN) · 시술 · 고민) · 남은 결정 수

## 기술
- 기존 게이트 페이지 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/product-match-review.html` 의 스타일 · 저장 방식(window.claude.use('db') · user · answers 컬렉션 · 저장 상태 표시 · 테마 토큰)을 따른다. 컬렉션 이름: families · units · questions
- 데이터는 페이지 안 JSON. 폰트 · CDN 규칙은 그 파일과 같게. 키 · 실명 없음
- 산출: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/silver-approval.html` 1개. node 로 스크립트 구문 검사 1회

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "tool_dev 완료: 실버 승인 페이지" \
  --body "결과 / 산출물 / 미결"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] tool_dev 완료 — 실버 승인 페이지. 상세는 인박스." --enter
```

# [tool_dev] KPIC MCP 설치 · 검증 — 추가 검색 가능 여부

역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/tool_dev/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 사용자 요청(10-28): https://github.com/antegral/kpic-mcp.git 를 설치해 추가 검색에 쓸 수 있는지.

## 할 일
1. `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-28-kpic-mcp/` 에 clone(기존 `reference/2026-10-27-mfds-mcp/` 옆). **다른 곳에 설치 금지**
2. **코드 전부 읽기 — 보안 검토 먼저**: 어디로 네트워크 요청을 보내는지(호스트 목록) · 키/토큰 요구 · 로컬 파일 읽기/쓰기 · 셸 실행 · 의존성(package.json/pyproject) — 의심스러운 것 있으면 **실행하지 말고** 보고
3. 문제 없으면 의존성 설치(레포 안에서만) · stdio 로 실행 · MCP inspector 또는 직접 호출로 tool 목록 · 입력 스키마 확인
4. **실호출 검증**(우리 남은 건으로): 리포린(삼익제약 2025-08 허가 보도 ↔ 식약처 0) · 벨카이라/카이벨라(데옥시콜산) · 아큐탄 · 컨트라투벡스 · 라엔넥 · 디스포트(abobotulinumtoxinA) · 티엠버스주 — 무엇이 나오는지(성분 · 업체 · 허가/보험 코드 · 분류)
5. 의료기기도 되는지 확인(되면 셀엑소좀 · 모르페우스8 1건씩)
6. 사용자 Claude 설정(~/.claude · 전역 MCP 등록)은 **건드리지 않는다** — 등록 명령은 NOTES 에 적어 두기만

## 산출
`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-28-kpic-mcp/NOTES.md`(보안 검토 결과 · 네트워크 호스트 · tool 목록 · 실호출 기록 · 할 수 있는 것/없는 것 · 등록 명령). 키가 필요하면 `.env`(gitignore 확인) — 키 값을 출력 · 커밋하지 마라. 원장 · 결정 파일 수정 금지

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "tool_dev 완료: KPIC MCP 검증" \
  --body "보안 검토 / tool 목록 / 실호출 결과(제품별 한 줄) / 쓸 수 있는지"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] tool_dev 완료 — KPIC MCP 검증. 상세는 인박스." --enter
```

# [tool_dev] KPIC MCP 검색 고치기 (사용자 승인 10-28)

역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/tool_dev/role.md`. 대상 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-28-kpic-mcp/` 사본만(원 레포 · 사용자 Claude 설정 건드리지 않음). 이전 검증 `NOTES.md` 이어서.

## 할 일
1. `search_drugs_by_name` 을 health.kr 새 API(`/api/searchDrug` — 검증 때 직접 호출한 방식)로 바꾼다. 입력 스키마는 그대로(drugname), 출력은 기존 형태 유지 + 새 API 에서 오는 drugcode · 제품명 · 업체 · 성분 · 분류가 들어가게
2. 성분명 검색이 되면 그것도(새 tool 이 필요하면 `search_drugs_by_ingredient` 추가 — 성분 → 제품 역조회)
3. 빌드 · stdio 실행 · **실호출 재검증**: 디스포트 · 티엠버스 · 라이넥 · 콘투락투벡스 · 이소트레티노인(성분) · 데옥시콜산(성분) · 리포린 — search → detail 까지 한 번에 되는지
4. NOTES.md 갱신(바꾼 곳 · 실호출 결과 · 등록 명령). 접속 호스트는 health.kr 하나로 유지 · 키 · 파일 IO · 셸 추가 금지
5. clone 의 `.git` 은 그대로 두고 NOTES 에 「커밋 전 처리 필요」만 적는다

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "tool_dev 완료: KPIC 검색 수정" \
  --body "바꾼 tool / 실호출 결과(제품별 한 줄)"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] tool_dev 완료 — KPIC 검색 수정. 상세는 인박스." --enter
```

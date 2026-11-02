# [backend] WORK-008 Phase 5 — 검수 FAIL 재수정 (fix1)

너는 Phase 5 를 구현한 **strong-hajin `backend` 워커**다. 같은 워크트리·같은 규칙(`strong-hajin-polish-be-p5-brief.md`). `backend/` 만(`frontend/` 에 Phase 5 FE 미커밋 변경 있음 — 건드리지 마라). 코디 핸들 `term_d7b4a334-2cbd-42ab-9eab-e64a7b255d44`.
검수 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/work/strong-hajin-polish/review-p5-report.md`

## 고칠 것
1. **FAIL-1 (필수)** `_remember`(mcp.py:474-479)가 `AX_MCP_CAUSATION_ID` 를 UUID 로 읽어, 회의 배치·합성의 causation(`meeting-batch:<id>`·`meeting-finalize:<id>`)에서 ValueError → 회의 레지스트리의 `project_list`·`task_list`·`meeting_get` 이 매번 실패. **UUID 가 아닌 causation 은 기억을 건너뛴다**(도구 자체는 성공). `_remember` 를 부르는 곳 전부를 세어 같은 문을 지나는지 확인
2. **WARN-3** 테스트: 회의 causation 으로 세 도구가 성공 · 프로젝트 권한을 잃은 뒤 그 프로젝트를 인용한 답변이 재인가에서 걸러짐
3. **WARN-1 (코디 결정)** `graph_overview`(최대 120 노드)로 본 노드는 근거로 **기억하지 않는다** — `graph_search`·`graph_neighbors`·`list_projects`·`get_project` 처럼 대상을 좁혀 본 것만. 오인용 문턱을 다시 높인다
4. WARN-2: 판단만 보고(고칠 필요 있으면 최소)

## 검증
`make test-unit` · `make test-contract`. 커밋·서버·운영·로컬 codex 금지.

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send --to term_d7b4a334-2cbd-42ab-9eab-e64a7b255d44 --from <네 워커handle> --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "backend 완료: WORK-008 Phase 5 fix1" --body "FAIL-1·WARN 처리(파일:줄) / _remember 호출 전수 / 테스트 결과"
orca terminal send --terminal term_d7b4a334-2cbd-42ab-9eab-e64a7b255d44 --text "[worker_done] backend 완료 — Phase 5 fix1. 상세는 인박스." --enter
```

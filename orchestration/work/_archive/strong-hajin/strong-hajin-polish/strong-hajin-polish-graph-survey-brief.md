# [backend] E2E-12 조사 — AX 대화의 graph_search 즉시 실패 (read-only)

너는 **strong-hajin `backend` 워커**(조사)다. 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/roles/strong-hajin/backend/role.md`. 코드 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish` (HEAD `dc4fe90`, 읽기만). 코디 핸들 `term_d7b4a334-2cbd-42ab-9eab-e64a7b255d44`.

## 증상 (사용자, 로컬 스택 — 데모 DB `ax_demo_polish`, 2026-10-01)
AX 대화 실행 단계에 「× 관련 항목 검색 `graph_search` 22ms」 실패가 보인다(같은 대화 다른 턴에서는 `graph_search` 성공·`graph_neighbors` 성공도 있음). 사용자: 「버그야? 왜 프로젝트 연결이 안 돼? 업무 만들 때 프로젝트·업무들 탐색 안 해?」

## 물음
1. `graph_search` 가 즉시 실패하는 원인 — 도구 입력 검증·그래프 인덱스(빈 인덱스·미적재)·권한·MCP 가드 중 무엇인가. 로컬 로그: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-kknaks-profile----------/fcf73967-37d6-4176-b25d-08d378ab9da6/scratchpad/local-stack.log`(conversation worker 출력 포함) · 로컬 DB `ax_demo_polish` 의 대화 턴·도구 호출 기록 **조회만**
2. 업무 생성(`task_create_self`·`work_request_create`) 때 AX 가 **프로젝트·기존 업무를 탐색해 project_id·reference/preceding 을 채우도록** 프롬프트·도구 설명·흐름이 되어 있는가. 안 되어 있다면 어디서 정하나(파일:줄)
3. 운영에서도 같은 일이 날 수 있는가(그래프 인덱스 적재 경로가 운영에 있는가)
4. 고칠 자리 후보(위치만 — 설계는 쓰지 마라)

## 하지 말 것
- 코드 수정·커밋 금지. 서버 재시작 금지(코디 스택 8001·5176). 로컬 codex 실행 금지. 운영 접근 금지. DB 쓰기 금지. `~/strong-hajin-deploy-data/` 금지

## 산출물
`/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/work/strong-hajin-polish/research-graph-search.md` — 0 한 줄 원인 · 1 증거 · 2 업무 생성 탐색 흐름 · 3 운영 영향 · 4 고칠 자리 · 5 한계

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send --to term_d7b4a334-2cbd-42ab-9eab-e64a7b255d44 --from <네 워커handle> --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "조사 완료: E2E-12 graph_search" --body "한 줄 원인 / 업무 생성 탐색 여부 / 운영 영향 / 고칠 자리 / 리포트 경로"
orca terminal send --terminal term_d7b4a334-2cbd-42ab-9eab-e64a7b255d44 --text "[worker_done] E2E-12 graph_search 조사 완료. 리포트 research-graph-search.md" --enter
```

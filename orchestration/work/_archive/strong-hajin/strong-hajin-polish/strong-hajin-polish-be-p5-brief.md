# [backend] WORK-008 Phase 5 — AX 업무 생성이 프로젝트·업무를 찾아 채운다 (E2E-12)

너는 이 원인을 조사한 **strong-hajin `backend` 워커**다(`research-graph-search.md`). 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/roles/strong-hajin/backend/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish` (HEAD `dc4fe90`). 코디 핸들 `term_d7b4a334-2cbd-42ab-9eab-e64a7b255d44`.
⚠ frontend 워커가 같은 워크트리 `frontend/` 에서 E2E 묶음을 고치는 중 — **`backend/` 만**. FE 가 project 참조를 그려야 하면 고치지 말고 보고에 적는다.

## SSOT
- WP `…/para/projects/summer-star/strong-hajin/30-work/work-008-polish.md` **Phase 5** (계약 셋)
- 너의 조사 `…/orchestration/work/strong-hajin-polish/research-graph-search.md` §4 고칠 자리

## 계약 (WP Phase 5 그대로)
1. 업무 생성·요청 초안 전에 AX 가 관련 프로젝트·기존 업무를 찾아 project_id·parent·reference·preceding 을 채울 수 있게 — 생성 도구 설명(`tool_catalog.py` task_create_self·work_request_create) · 라우팅 정책(`codex_cli.py` WORK_AND_REPORT_ROUTING_POLICY — 「graph_search 먼저 부르지 말라」와의 충돌 정리) · `project_list` 설명(「회의용」 한정 풀기). 못 찾거나 모호하면 **비우고 답변에 그렇게 말한다 — 지어내지 않는다**. Claude 어댑터 쪽 같은 정책 문구가 있으면 함께(전수)
2. 답변 참조에 `project` 종류(`answer_documents.py` ResourceRef·bind) + graph 도구로 본 대상도 근거로 묶이게(`mcp.py` graph 도구 `_remember`) + 허용 ref 문구(`codex_cli.py`). 프로젝트를 가리킨 답변이 턴 실패가 되지 않는다
3. `graph_search` 인자 설명을 실제 스키마와 맞춘다(지어낸 `kinds` 감소)
- operation inventory drift 는 diff 항목만. 스키마 변경 없음(필요하면 [질문])

## 하지 말 것 / 검증
- 커밋·서버 기동 금지(코디 스택). 로컬 codex 실행 금지 — 테스트는 가짜 provider. 운영 접근 금지
- 테스트: project 참조 답변 bind 성공 · graph 도구로 본 대상 근거 묶임 · 도구 설명/정책 문구 회귀 단언 · `make test-unit` · `make test-contract`(기존 플레이크는 `flaky-baseline-evidence.md` 참고해 분리)

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send --to term_d7b4a334-2cbd-42ab-9eab-e64a7b255d44 --from <네 워커handle> --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "backend 완료: WORK-008 Phase 5 AX 탐색" --body "계약 1~3 처리(파일:줄) / FE 가 할 일(project 참조 렌더) / 테스트 결과"
orca terminal send --terminal term_d7b4a334-2cbd-42ab-9eab-e64a7b255d44 --text "[worker_done] backend 완료 — Phase 5 AX 탐색. 상세는 인박스." --enter
```

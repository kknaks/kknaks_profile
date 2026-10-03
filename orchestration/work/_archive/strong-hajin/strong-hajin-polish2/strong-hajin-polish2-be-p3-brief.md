# [backend] WORK-009 Phase 3 — AX 초안 전 회의·업무·자료 탐색 (E2E-6)

너는 이 워크트리에서 조사·Phase 1 · E2E-6 조사를 한 **strong-hajin `backend` 워커**다. 역할 문서·AGENTS 는 앞 판과 같다(`/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/roles/strong-hajin/backend/` · `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish2/AGENTS.md`). 작업 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish2` (Phase 1 `6efdac1` 위). `frontend/` 는 건드리지 마라.

## 1. SSOT
- WP `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/para/projects/summer-star/strong-hajin/30-work/work-009-polish2.md` **Phase 3** — 체크박스 하나하나가 계약
- SPEC-001 v0.5.0 **S-9 7·8 · §5 · §6**(E2E-6 반영분) · SPEC-002 §2.9 체크리스트 줄 (`/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/para/projects/summer-star/strong-hajin/20-spec/`)
- 너의 조사 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/be-survey2-report.md` (도구·제동 문장·근거 묶기·권한·시간 — 파일:줄 출발점)
- 개념 `evidence-binding`·`human-in-the-loop`(`/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/para/areas/concept/`)

## 2. 무엇을 하나 (요약 — 상세는 WP)
- 업무 생성·요청 도구 설명(`tool_catalog.py` task_create_self · work_request_create)과 라우팅 정책(`codex_cli.py`)에: 초안 전에 **주제 핵심어(짧게)** 로 `graph_search`·회의 목록·`material_search` 로 관련 회의·업무·자료를 찾고, 가장 관련 높은 것 **상세 최대 3건**(`meeting_get`·`task_get`)을 읽어 **업무 내용·체크리스트의 근거**로 쓴다 · 답변에 출처 · 못 찾으면 일반 제안 + 그렇다고 말함 · **사람·날짜는 채우지 않음** — 사람(참조자·결재자·담당자)은 **대화가 이름을 댄 사람만**, 탐색에서 본 회의 참석자·할 일 담당자·마감 후보는 옮기지 않는다(SPEC 검수 W1 — 코디 2026-10-02)
- 제동 문장(`codex_cli.py:372-374`·`:381`·`:385`·`:395`·`:408` · `tool_catalog.py:568`)은 **업무 생성·요청 턴만 예외** — 문장 단위로 예외를 명시하고, 다른 질문 턴 문장은 의미를 바꾸지 않는다
- 상세 조회(`meeting_get`·`task_get`·`material_search`)가 답변 참조로 묶이는지(`_remember`) 확인 — 빠졌으면 같은 방식으로(종류는 기존 task·meeting·material). `meeting_transcript` 등 새로 쓰게 되는 도구가 있으면 같은 확인
- 검색 엔진·타임아웃·reasoning·초안 Evidence 는 바꾸지 않는다
- 문장을 쓰는 곳 **전부**(카탈로그·정책 6절·Claude 어댑터·inventory description·단언 테스트) 세고 개수표

## 3. allowed_paths
- `backend/src/ax_workspace/` · `backend/tests/` · (drift 패치) `docs/unified-operations-inventory.json` 그 항목만

## 4. 하지 말 것
- 커밋·push 금지 · **서버·DB·codex 띄우지 마라 — 코디 로컬 스택이 8001·5176·54329 에 떠 있다.** 실물 확인은 코디가 한다
- 스키마 변경 없음

## 5. 검증
- `make test-unit` · `make test-contract` · architecture · inventory drift. 기준선(Phase 1 뒤 403 / 1161+128) 대비 보고
- 새 테스트: 정책·도구 설명 단언(회의·자료·업무 상세 탐색 · 상세 최대 3 · 사람·날짜 안 채움 · 제동 예외가 생성 턴에만) · 근거 묶기(상세 조회가 답변 참조로)

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_b2ea0fd5-1473-4b83-9a04-dcf769fbedba --from term_2cf4fdea-dd6c-411f-b344-41b6d61078de \
  --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "backend 완료: WORK-009 Phase 3" \
  --body "변경 파일 / 바꾼 문장(원문 전후) / 제동 예외 범위 / 근거 묶기 / 개수표 / 기준선 vs 결과 / 미결"
orca terminal send --terminal term_b2ea0fd5-1473-4b83-9a04-dcf769fbedba \
  --text "[worker_done] backend 완료 — WORK-009 Phase 3. 상세는 인박스." --enter
```

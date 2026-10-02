# [backend] WORK-008 Phase 3a — AX 업무 초안 = 새 업무 추가 필드 객체

너는 앞서 이 워크트리를 조사한 **strong-hajin `backend` 워커**다(`be-survey-report.md`). 역할 문서:
`/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/roles/strong-hajin/backend/role.md` (+ rules 등)

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish` (Phase 1 커밋 `9255028` 위)
⚠ **frontend 워커가 같은 워크트리 `frontend/` 에서 Phase 2 를 하고 있다.** 너는 `backend/` 만. `frontend/` 를 건드리지 마라.

## 1. SSOT
- WP `…/kknaks_profile/스트롱하진-고도화/para/projects/summer-star/strong-hajin/30-work/work-008-polish.md` **Phase 3a** + 원칙 P-1·P-3
- SPEC(정본 — WP 와 다르면 SPEC 이 맞다): `…/strong-hajin/20-spec/`
  - SPEC-001 **S-9** · **§4 Validation** · **§5** (P-1: AX 초안도 같은 표·기한 선택)
  - SPEC-002 **§2.4**(보이는 자리·만든 시각) · **§2.9**(카드가 쓰는 필드) · **§4**(confirm 의 고친 초안 예외) · S-7 · §6
- 너의 조사 `…/orchestration/work/strong-hajin-polish/be-survey-report.md` §1

## 2. 계약
- **P-1** — 대상 두 kind(`ax.task.create_self` · `ax.work_request.create`)의 초안 객체는 「새 업무 추가」 생성 명령과 **같은 필드 · 같은 필수값 · 같은 검증**이다. 필드 정본은 생성 명령(`modules/work/creation_commands.py` 의 업무/요청 명령)이다.
  - 초안 정규화(`_normalize_ax_draft`) · 스냅샷 · 편집 계약(`ActionPresenter._edit_contract`) · MCP 도구 인자(`task_create_self`, `work_request_create`) 가 그 필드를 **빠짐없이** 싣는지 **표로 대조**한다. 빠진 필드는 더한다
  - 자료(첨부)는 생성 명령의 필드가 아니다 — 자료 초안으로 따로 센다(SPEC-001 S-9 6)
- AX 경로에만 있는 **기한 필수 검사를 뺀다**(`platform/action_center.py` `task.create_self` 의 「업무 기한을 입력해 주세요」). 필수는 새 업무 추가와 같다(제목 · 요청이면 담당자). 같은 종류의 「AX 경로에만 있는 검사」가 다른 곳에도 있는지 grep 으로 전부 찾는다
- confirm + 고친 초안(draft) 경로는 **그대로**(회차 증가·diff 기록 유지)
- 판단 대기 목록 응답(`GET /api/action-items`, AX 핸들러)이 카드에 필요한 것을 싣는다: **초안 필드 전체** · **만든 시각**. 없는 것만 더한다. 필드 이름은 기존 응답 관례를 따르고 보고에 적는다(3b FE 가 쓴다)
- MCP 도구 설명이 「새 업무 추가의 필드를 채워 초안을 만든다」를 말하게 한다 — AI 가 객체를 다 채우도록. **새 도구는 내지 않는다**
- operation inventory drift 는 실패 diff 의 그 항목만 패치. 스키마 변경 없음(필요하면 먼저 [질문])

## 3. allowed_paths
- `backend/src/ax_workspace/` · `backend/tests/`

## 4. 하지 말 것
- 커밋·push 금지. **서버를 띄우지 마라 — 코디의 로컬 스택(8001·5176·54329)이 떠 있다. 그 프로세스와 DB `ax_demo`·`ax_demo_polish` 를 건드리지 마라.** postgres 테스트는 Makefile 의 격리 타깃만
- `~/strong-hajin-deploy-data/` 접근 금지. 로컬 codex 인증 사용 금지

## 5. 검증
```
코드 레포 AGENTS.md 준수: backend 테스트는 Makefile 타겟으로만. make test-unit · make test-contract, 필요 시 격리 PostgreSQL 의 make test-postgres. tests/architecture 경계 및 operation inventory drift 확인(diff 항목만 패치). 스키마 변경은 reset_demo 전용 경로, 일반 API startup DDL 금지. 기존 실패는 기준선과 분리 보고.
```
- 기준선 먼저(고치기 전 test-unit · test-contract 실패 목록)
- 새 테스트: 기한 없는 task.create_self 초안 confirm 통과 · 고친 draft 가 회차 2 · 목록 응답에 필드 전체와 만든 시각 · 두 kind 의 초안 필드 = 생성 명령 필드(대조 테스트)

## 6. 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**
```bash
orca orchestration send \
  --to term_7941dbc9-8078-4818-8d3d-bfd5545cce31 --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "backend 완료: WORK-008 Phase 3a" \
  --body "변경 파일 / 필드 대조표 / 뺀 검사(전수) / 목록 응답에 더한 필드 이름·모양(FE 계약) / 기준선 vs 결과 / 미결"
orca terminal send --terminal term_7941dbc9-8078-4818-8d3d-bfd5545cce31 \
  --text "[worker_done] backend 완료 — WORK-008 Phase 3a. 상세는 인박스." --enter
```
막히면: `orca terminal send --terminal term_7941dbc9-8078-4818-8d3d-bfd5545cce31 --text "[질문] backend: <질문>" --enter`

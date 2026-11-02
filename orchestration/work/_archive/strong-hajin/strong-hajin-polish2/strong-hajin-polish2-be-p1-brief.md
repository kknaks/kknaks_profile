# [backend] WORK-009 Phase 1 — AX 초안 저장 · AI 체크리스트·내용 제안 · 완료 시 마감일 채움

너는 앞서 이 워크트리를 조사한 **strong-hajin `backend` 워커**다(`/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/be-survey-report.md`). 맥락이 끊겼으면 아래 파일만으로 이어 갈 수 있다. 역할 문서:
`/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/roles/strong-hajin/backend/role.md` (+ 같은 폴더 rules·skills·tools·workflow) · 코드 레포 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish2/AGENTS.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish2` (base `origin/main` `3d47a32`)
⚠ **frontend 워커가 같은 워크트리 `frontend/` 에서 Phase 2b 를 동시에 한다.** 너는 `backend/` 만. `frontend/` 를 건드리지 마라.

## 1. SSOT
- WP `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/para/projects/summer-star/strong-hajin/30-work/work-009-polish2.md` — **Phase 1(1-1 · 1-2 · 1-3)** 과 원칙 P-1~P-5. 체크박스 하나하나가 계약이다
- SPEC(정본 — WP 와 다르면 SPEC 이 맞다, 다르면 코디에게 알려라): `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/para/projects/summer-star/strong-hajin/20-spec/`
  - SPEC-002 v0.4.0 §2.9 · S-7 · **§4 「초안 저장」** · §5 · §6
  - SPEC-001 v0.5.0 S-9 6·7 · §5 · §6 · OQ-R
  - SPEC-003 v0.4.0 Data Contract 「업무 날짜」·「날짜 채움」 · §6
  - SPEC-004 v0.3.2 §5 거는 자리(넷째 — 완료의 마감일 채움)
- 너의 조사 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/be-survey-report.md` §1·§2·§3 (줄 번호는 `3d47a32` 기준 — 심볼로 다시 찾아라)
- 기대는 개념: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/para/areas/concept/` 의 `human-in-the-loop`·`evidence-binding` — AI 는 제안, ID 는 근거가 있을 때만

## 2. 무엇을 하나 (요약 — 상세는 WP)
1. **초안 저장 명령(신규)** — 두 AX 초안 kind 를 확정 없이 고쳐 저장: 확인 대기 유지 · 회차 +1 · 고친 차이 기록 · effect 없음 · 변경 없으면 회차 안 오름 · 낡은 버전 거부. confirm+draft 경로는 지우지 않는다. 기존 `revise` 를 재사용할 수 있는지 먼저 보고 판단을 보고에 적는다
2. **AI 지시문** — 체크리스트·업무 내용은 대화 주제로부터 **제안해 채운다**, ID·날짜는 지금처럼 근거가 있을 때만. 도구 설명·라우팅 정책·답변 지침·정책 단언 테스트를 **전부** 센다
3. **완료 시 마감일 채움** — `completed_at` 이 찍히는 순간 `due_date` 가 비어 있으면 그날(Asia/Seoul). 직접 완료·완료 보고 제출. 되돌리지 않음. 배정 검증 훅·이력·스냅샷은 시작일 채움과 같은 수준

**쓰는 곳을 전부 센다** — WP 의 파일:줄은 출발점이다. 명령 목록·정책·편집 계약·operation inventory·`completed_at` 쓰기·도구 설명 문자열을 grep 으로 전부 세고 보고에 개수표를 낸다.

## 3. FE 계약 (2a 가 쓴다 — 보고에 그대로 적어라)
- 저장 명령의 **id·경로·입력 모양·응답 모양·오류 코드** · 편집 계약/명령 목록에서 FE 가 저장 명령을 찾는 법 · 저장 뒤 `edit_contract.values`·`base_submission_version`·회차 표시 원천이 어디서 새 값이 되나

## 4. allowed_paths
- `backend/src/ax_workspace/` · `backend/tests/`

## 5. 하지 말 것
- 커밋·push 금지. **서버·스택을 띄우지 마라. 사용자 포트(8001·5176·54329)와 DB `ax_demo` 를 건드리지 마라.** postgres 테스트는 Makefile 의 격리 타깃만
- `~/strong-hajin-deploy-data/` 접근 금지. codex 실행 금지(실물 확인은 코디가 한다)
- 스키마 변경 없음 — 필요해 보이면 먼저 [질문]

## 6. 검증
```
코드 레포 AGENTS.md 준수: backend 테스트는 Makefile 타겟으로만. make test-unit · make test-contract, 필요 시 격리 PostgreSQL 의 make test-postgres. tests/architecture 경계 및 operation inventory drift 확인(diff 항목만 패치). 기존 실패는 기준선과 분리 보고.
```
- **기준선 먼저**(고치기 전 test-unit · test-contract 실패 목록)
- 새 테스트: 저장 → pending·회차 2·diff · 변경 없는 저장 → 회차 그대로 · 낡은 저장 거부 · 저장 뒤 draft 없는 confirm 이 저장 값으로 업무 생성(회차 안 오름) · 도구 설명/정책 문장 단언 · 마감일 없는 업무 직접 완료/완료 보고 → due_date=오늘, 있던 마감일 유지, 보완 요청 뒤 유지

## 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 코디handle 은 작성 시점 값이다. preamble 과 다르면 preamble 이 맞다.

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다.
```bash
orca orchestration send \
  --to term_b2ea0fd5-1473-4b83-9a04-dcf769fbedba --from term_2cf4fdea-dd6c-411f-b344-41b6d61078de \
  --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "backend 완료: WORK-009 Phase 1" \
  --body "변경 파일 / 저장 명령 FE 계약(id·경로·입력·응답·오류) / revise 재사용 판단 / grep 개수표 / 기준선 vs 결과 / 미결"
orca terminal send --terminal term_b2ea0fd5-1473-4b83-9a04-dcf769fbedba \
  --text "[worker_done] backend 완료 — WORK-009 Phase 1. 상세는 인박스." --enter
```
막히면: `orca terminal send --terminal term_b2ea0fd5-1473-4b83-9a04-dcf769fbedba --text "[질문] backend: <질문>" --enter`

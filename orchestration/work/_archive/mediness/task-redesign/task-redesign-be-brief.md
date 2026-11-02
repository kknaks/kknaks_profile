
# [backend] WP-125 태스크 원장 단일화 — BE+MCP (P0~P4·P6~P8 + P5 MCP)

너는 **mediness `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/roles/mediness/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/task-redesign`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

⚠ **FE 워커가 같은 워크트리 `front/` 에서 병렬 작업 중** — `front/` 를 건드리지 마라. 너는 `back/`·`mcp/` 만.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/mediness-mediness/task-redesign-spec/products/mediness/30-work/work-125-task-ledger-unification.md` ← **빌드 계획의 SoT.** Phase·파일 후보·invariant·Open Issues 전부 여기. **여기 없는 건 발명하지 마라.**
- `/Users/kknaks/orca/workspaces/mediness-mediness/task-redesign-spec/products/mediness/40-architecture/domains/runtime_task.md` — 상태 5값·전이표·스탬프·TaskEvent 어휘·삭제⟂취소 축 **정본**
- `/Users/kknaks/orca/workspaces/mediness-mediness/task-redesign-spec/products/mediness/40-architecture/domains/version_wbs_task.md` — WBS `status` = `phase` 전용 계약
- `/Users/kknaks/orca/workspaces/mediness-mediness/task-redesign-spec/products/mediness/40-architecture/domains/decision_execution_task.md` §이관·폐기 계획 — P7 의 SoT
- (참고) `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/work/task-redesign/research-task-status.md` §B — 조사 시점 코드 좌표 스냅샷. **계약이 아니라 지도다** — 어긋나면 코드 실물이 맞다

**기대는 개념** — 이 작업이 따를 판단 기준. 안 주면 워커가 매번 처음부터 정하고,
같은 결정이 작업마다 달라진다. 없으면 "해당 없음".

- 해당 없음

## 2. 배경 / 무엇을 바꾸나

업무 태스크 원장이 3벌(`tasks` 정본 / `version_wbs_task` 미러 / `decision_execution_task` 레거시)로 갈라져 상태 어휘가 4벌이다. 스펙 라운드에서 사용자 확정으로 **`accept_pending`·수락·거절 폐기(5값) · 착수 = 명시 시작만 · 원장 단일화**가 정본이 됐고(spec PR #661, base `mediness` 머지 대기), 이 발주는 그 계약을 back/·mcp/ 에 착지시키는 것이다.

**P0~P3 은 한 배포 단위다** — enum 이 바뀌는 순간 표면이 함께 나가지 않으면 400/500. 전부 이 브랜치 하나에서 작업하고 PR 분리는 코디네이터가 판단한다.

## 3. 계약 (다른 워커와 합의됨 — 이대로 소비/제공)

FE 워커와 합의된 계약 (이대로 제공하라):

- 상태 어휘 = **5값** `todo|in_progress|blocked|done|canceled`. 응답에서 `accept_pending` 이 나가는 일이 없어야 한다
- `allowed_transitions`(projection) = FE 가 소비하는 유일한 전이 축 — 전이표 변경은 여기로 자동 전파된다
- `MyTask.declined`·`decline_reason`·`declined_at` 파생 필드 **제거** (FE 도 같은 라운드에 렌더 제거)
- decline REST 3곳(`/tasks/{id}/decline`·run 하위 2곳)·`/task-declines` 제거 — FE 가 BFF 라우트 3건을 같이 지운다
- 재배정 = `todo` 리셋 + `started_at` 클리어, terminal(done/canceled) 재배정 금지(BUG-023 가드 유지). **담당자 본인도 재배정 요청 가능**

## 4. 먼저 읽을 핵심 파일

- WP-125 §Code Surface 표 — 만질 파일 후보 전체가 표로 정리돼 있다. 이 표부터 읽어라
- `back/app/services/action_runtime/tasks/machine.py` — 전이표 정본 구현. `_STATUS_EVENT`/`_STAMP` 재정의·`decline()` 삭제·`reassign()` 리셋 대상 변경이 여기
- `back/alembic/versions/0108_wbs_status_vocab_task_axis.py` — enum cutover 선례(rename→새 타입→USING 캐스트→drop + 사전 RAISE 가드). 신규 migration 은 이 꼴을 따른다
- `back/app/services/action_runtime/tasks/lifecycle.py` — 전이 seam. P8 라운드 평가 호출 자리
- `back/tests/services/engine_v2/test_task_machine.py` — 전이표 테스트 정본. 가장 먼저 갱신될 파일

## 5. allowed_paths — 이 밖은 건드리지 마라

- `back/`
- `mcp/`
- `docker-compose.yml`
- `docker-compose.local.yml`

## 6. 구현 단계

1. WP-125 를 정독하고 P0(사전 실측)부터 Phase 순서대로 진행한다. 각 Phase 완료 시 WP 의 해당 Phase Status 는 **갱신하지 말고**(문서 레포 접근 금지) 완료 보고에 Phase 별 결과를 적는다
2. **P0 실측 주의(OI-6)**: `tasks.accepted_at` 비NULL 행이 `task_events` 의 `task_accepted` 이벤트와 대응하는지 확인하라. **이벤트 없이 스탬프만 있는 행이 존재하면 drop 을 멈추고 §9 질문 채널로 보고** — 대응이 다 되면 이력은 이벤트 원장에 보존되므로 drop 진행
3. P1 migration: 두 enum **같은 migration** 동시 cutover + `accepted_at` drop + meeting default 제거. `accept_pending` 행 → `todo` 매핑. downgrade 는 0108 선례의 역방향
4. P2~P4·P6~P8 은 WP 명세대로. **P8 은 «호출 위치 이동»만** — 라운드 판정 규칙 자체를 고치지 마라(후속 incident WP 소관, OI-3)
5. P5 중 **MCP 만**: `task_decline` 툴 제거·`wbs_common.py` STATUSES 5값. front/ 는 FE 워커 몫
6. P9: 만들거나 고친 테스트를 §8 방식으로 검증

## 7. 범위 제약 — 하지 말 것

- `front/` 수정 금지 (FE 워커 병렬 작업 중) · 문서 레포(mediness-mediness) 수정 금지
- WP-125 §Scope «제외» 목록을 침범하지 마라 — incident 라운드 판정 수렴·run 감사·Slack fail-loud·`is_required`/`scope_slug` drop 은 후속 WP
- `task_events` 의 과거 `task_accepted`·`task_declined` 행을 지우지 마라 (append-only 원장)
- 삭제(`deleted_at`)⟂취소(`canceled`) 배제 앵커(`RuntimeTaskRepository._scoped()`)를 무효화하지 마라
- 구현 중 계약과 어긋나는 사실이 나오면 **코드를 고치지 말고 §9 질문 채널로** — 계약 수정은 스펙으로 되돌린다

## 8. 검증

```
cd back && pytest -q <네가 만들거나 고친 테스트 파일만> (전체 스위트 금지 — 사용자 방침. DATABASE_URL 은 back/pyproject.toml 의 테스트 DB = localhost:25434/mediness_test). 검증은 1회만 — 통과하면 반복하지 마라
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_1d6e5d93-2be9-4125-b7eb-42b1de52b5ed --from term_75b70534-ae89-4f02-ae26-f3c5bf6531db \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_1d6e5d93-2be9-4125-b7eb-42b1de52b5ed \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_1d6e5d93-2be9-4125-b7eb-42b1de52b5ed --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)

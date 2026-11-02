# [backend] 체크리스트 전량 완료 시 자동 `done` 폐지 — 완료는 근거 seam 단일 통로 (BE 단독)

너는 **mediness `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/roles/mediness/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/task-complete-gate`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

워크트리 공유 없음 — BE 단독.

## 1. SSOT — 먼저 읽을 것

- 스펙 정정은 **코디가 별도로 쓴다** — 이 브리프의 §2·§3 이 이번 계약의 임시 정본이다. 여기 없는 건 발명하지 마라.
- `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/para/areas/concept/cs/contract-surface-enumeration.md` — P0 에서 파생 규칙 소비처를 전수 세고 시작하는 근거

## 2. 배경 — 실기동 버그 (사용자 발견 2026-09-02)

WP-130 이 **완료 근거 강제**를 세웠다: 완료 전이는 「완료기록(요약) 또는 제출자료 최소 1」 없으면 서버 422 (`POST /task-completions` 전이 seam 안쪽). 그런데 **체크리스트를 전부 체크하면 다른 길로 `done` 에 들어간다** — 체크 파생 축(`checklist_target_status`: all→DONE)이 상태를 자동 전이시키고, 이 길은 근거 검사를 안 지난다. 완료 모달도 안 뜨고 빈손 완료가 된다.

**사용자 확정**: ① 자동완료 **폐지** — 전부 체크돼도 태스크는 진행 중(진행률 100%)에 머물고, **사람이 [완료] 버튼을 눌러 근거를 남겨야** `done` 이 된다. ② FE 모달 자동 오픈도 **하지 않는다** — FE 변경 없음이 목표.

## 3. 계약 — 이대로

- **runtime 태스크의 `done` 자동 파생만 죽인다.** `checklist_target_status` 가 DONE 을 낼 때 runtime 태스크 상태 전이를 **하지 않는다**(현 상태 유지). TODO↔IN_PROGRESS 파생·진행률·WBS mirror 등 나머지 파생은 **전부 불변**.
- **규칙 함수 자체(`checklist_target_status`)는 고치지 않는 것을 우선 검토하라** — WBS 도메인(버전 WBS work item)이 같은 규칙을 쓰면 그쪽 계약(근거 개념 없음)은 불변이어야 한다. 죽이는 자리는 **runtime 태스크 상태에 닿는 소비처**다.
- **명시 완료의 되치기는 유지** — `done` 전이 시 미완료 체크 항목 함께 완료(BUG-021 cascade)는 그대로.
- 이미 자동완료로 `done` 이 된 과거 태스크는 **소급하지 않는다**(백필·수리 0).

## 4. 먼저 읽을 핵심 파일

- `back/app/services/action_runtime/tasks/checklist.py:21` — 규칙 단일 자리(all→DONE / any→IN_PROGRESS / none→TODO). `:64` 배열 교체 경로도 같은 규칙 소비
- `back/app/services/action_runtime/tasks/check_items.py:111-140` — `apply_derivation`(미연결 태스크 소비처, AUTO_LANE·U22 축)
- `back/app/services/version_wbs.py` — `cascade_canonical_checklist`(연결 태스크 소비처 — WBS 캐스케이드가 origin 태스크 상태를 만진다)
- `back/app/services/action_runtime/tasks/lifecycle.py` — 명시 완료 seam(근거 422·BUG-021 cascade — **불변 확인용**)
- `mcp/app/tools/task_lifecycle.py` — `task_check`·`task_done` 문구(§6 5번)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `back/`
- `mcp/`

## 6. 구현 단계

1. **P0 표면 전수**: `checklist_target_status` 소비처 전부 + 「runtime 태스크 status 를 체크 파생으로 바꾸는」 경로 전부를 grep 으로 목록화. 브리프 §4 밖의 경로가 나오면 **구현 전에 코디에게 보고**(§9 채널) — 임의 확장 금지.
2. DONE 파생 → runtime 태스크 전이 차단 (미연결 `apply_derivation` + 연결 캐스케이드 + 채팅 번역기 등 P0 목록 전부, **한 판정 자리로 수렴**할 수 있으면 수렴).
3. WBS work item 자체의 파생 계약 불변 확인 (버전 WBS 화면 쪽 상태 파생이 이번 변경으로 달라지면 안 된다 — 달라지면 보고).
4. 테스트: ① 전부 체크 → 태스크 진행 중 유지(미연결·연결 각 1) ② 그 상태에서 명시 완료(근거 있음) → done + 잔여 항목 없음 ③ 근거 없이 명시 완료 → 422 불변 ④ TODO↔IN_PROGRESS 파생 불변.
5. MCP 문구 정합: `task_check`(또는 관련 툴 설명)에 「전부 체크 시 자동완료」류 문구가 있으면 「전부 체크해도 완료는 [완료]에서 근거와 함께」로 정정. 기존 자동완료를 전제한 back 테스트가 깨지면 신계약으로 고친다(무엇을 왜 고쳤는지 보고에 명시).

## 7. 범위 제약 — 하지 말 것

- FE(`front/`) 금지 — 사용자 확정: FE 변경 없음(모달 자동 오픈 안 함)
- migration·새 컬럼·과거 데이터 소급 수리 금지
- WBS 도메인 자체 계약(간트 화면 상태 파생) 변경 금지 — runtime 태스크에 닿는 자리만
- 완료 근거 seam(lifecycle 422)·BUG-021 cascade 수정 금지 — 불변 확인만
- **커밋·push·PR 금지** — 워크트리에 변경만 남긴다

## 8. 검증

```
cd back && pytest -q <네가 만들거나 고친 테스트 파일만> (전체 스위트 금지 — 사용자 방침. DATABASE_URL 은 back/pyproject.toml 의 테스트 DB = localhost:25434/mediness_test). 검증은 1회만 — 통과하면 반복하지 마라
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: 체크리스트 자동완료 폐지" \
  --body "변경 파일 목록 / P0 표면 목록 / 구현 요약 / 검증 결과(수치) / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_d5bec05e-881f-4a29-a144-fd73be7e23c4 \
  --text "[worker_done] backend 완료 — 체크리스트 자동완료 폐지. 상세는 인박스." --enter
```

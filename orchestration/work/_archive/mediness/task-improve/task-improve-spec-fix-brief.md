
# [planner] 검수 V-1 정정 — 배정 부트스트랩 비활성을 «지시 흐름 발»로 한정

너는 **mediness `planner` 워커**다. 검수 FAIL 1건을 정정한다. 범위가 좁다 — 이것만 하고 끝낸다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/roles/mediness/planner/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/task-improve-spec` (직전 산출물 미커밋 15파일 위에서 작업)

## 1. SSOT

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/work/task-improve/review-spec-report.md` — 검수 리포트 V-1 (좌표·수정안 포함)
- `/Users/kknaks/orca/workspaces/kknaks_profile/task-improve/orchestration/work/task-improve/_RESUME.md` §2 — 결정 표 (샤라웃 행에 V-1 정정 반영됨)

## 2. 확정된 수정 방향 = 리포트의 ⓐ안 (사용자 결정과 정합 — 코디 확정)

사용자 결정은 「**지시(실행 요청) 유형** 배제 · 결정 요청/공유/**승인·결재 유지**」다. 배정 부트스트랩의 생성 시점 3곳 중 결정 승인·[후속 실행] 발은 **유지 축**이라 살아 있어야 하고, WP-130 P3(부트스트랩 자동 완료 전제)·spec-154:890 도 그 전제다.

1. **WP-129** (`work-129-task-request-axis.md:50,123,208`) — «배정 부트스트랩 비활성» 문구를 **«지시 흐름 발 부트스트랩만 비활성»** 으로 한정. 결정 승인·[후속 실행] 발 부트스트랩은 유지임을 명시
2. **spec-154 §4.8** (`:972-990` 부트스트랩 계약) — 생성 시점 3곳 표에서 **지시 흐름 발 행만** 취소선 + 2026-09-01 개정 표기(지시 입구 차단에 따름). 나머지 두 시점은 불변 명시
3. **spec-115:71** — 비활성 3자리 열거는 그대로 두되, 부트스트랩 관련 오해 소지가 있으면 «지시 발 한정» 한 줄만 보강 (필요 시)
4. **WP-130 P3 과의 정합** — 두 WP 가 같은 메커니즘에 같은 말을 하는지 재확인 (P3 은 수정 불필요할 것 — 전제가 맞아진다)

**ⓑ안(전면 비활성·12자리 정정)은 하지 마라** — 유지 축을 깬다.

WARN 은 조치 불요(리포트 판단 유지). 단, `spec-060:250` 이 어느 WP 에도 안 실린 점은 — 구현작업 0 이므로 WP-129 관련 phase 에 «문서 정합만, 코드 0» 한 줄로 배선만 남겨라.

## 3. 검증

```
cd /Users/kknaks/orca/workspaces/mediness-mediness/task-improve-spec && python3 scripts/lint-pipeline.py --strict
```

mediness 범위 ERROR 0 유지. 정정 후 «부트스트랩» grep 으로 WP-129/130/spec-154/115 가 같은 말을 하는지 수치 보고.

**하지 말 것**: 위 좌표 밖 신규 개정 금지 · 커밋/push/PR 금지.

## 4. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**

```bash
orca orchestration send \
  --to term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --from <네 워커handle> \
  --type worker_done \
  --task-id <preamble 의 taskId> --dispatch-id <preamble 의 dispatchId> \
  --subject "planner V-1 정정 완료: <한 줄>" \
  --body "정정 좌표 목록 / 부트스트랩 grep 정합 수치 / lint 결과"

orca terminal send --terminal term_d5bec05e-881f-4a29-a144-fd73be7e23c4 \
  --text "[worker_done] planner V-1 정정 완료 — <한 줄>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_d5bec05e-881f-4a29-a144-fd73be7e23c4 --text "[질문] planner: <질문>" --enter`

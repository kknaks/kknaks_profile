
# [backend] WP-126 incident 재정비 — 코드 착지 (P0~P6, back/·mcp/)

너는 **mediness `backend` 워커**다. 역할 문서(절대경로): `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/roles/mediness/backend/role.md` (+ 같은 폴더 문서들)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/task-redesign` — **WP-125 코드가 이미 커밋된 브랜치(`task-redesign`) 위에서** 작업한다. 같은 브랜치에 쌓여 PR #136 에 합쳐진다.
⚠ FE 워커가 같은 워크트리 `front/` 에서 병렬 작업 중 — 건드리지 마라. 너는 `back/`·`mcp/` 만.
⚠ 코디가 이 브랜치의 **커밋 시점 스냅샷**을 별도 워크트리로 로컬 기동 중이다 — 네 작업과 간섭 없음.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/mediness-mediness/task-redesign-spec/products/mediness/30-work/work-126-incident-workflow-realign.md` ← **빌드 계획 SoT.** 7 phase·invariant·OI 전부 여기
- `/Users/kknaks/orca/workspaces/mediness-mediness/task-redesign-spec/products/mediness/20-spec/spec-152-incident-response-workflow.md` — incident 계약 정본
- `/Users/kknaks/orca/workspaces/mediness-mediness/task-redesign-spec/products/mediness/40-architecture/domains/runtime_task.md` — 상태·이벤트 정본
- `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/work/task-redesign/_RESUME.md` §2 — 결정 SoT (특히: run 감사 payload 폐기 · Slack fail-loud · 라운드 판정 = 활성 라운드)

기대는 개념 — 해당 없음.

## 2. 배경

WP-125(태스크 원장 단일화)가 이 브랜치에 착지했다. 이번 발주는 그 위에 서는 incident 재정비 — 라운드 판정 3벌을 1벌로, run 감사 배선, Slack fail-loud, 죽은 코드 정리. **migration 0 확정**(run 감사는 기존 `workflow_run_events` 원장 사용).

## 3. 계약 (핵심 — WP-126 이 SoT)

- **라운드 판정 1벌** = 활성 라운드(최대 `round_no`) 기준. WP-125 P8 이 옮겨 둔 seam 훅 위에서 3벌(round_piece / tasks_surface.round_complete / factory.has_open_in_run_chain) 수렴
- **run 감사** = 기존 원장 사용. payload 없음 — 종결 시 추적 Task 는 `task_canceled`(사유 `run_closed`) 로 각자 원장에 남기고 run 사슬 역조회로 답한다. cause 는 기존 `human_approval` 로 충분(P2 에서 재확인)
- **Slack fail-loud** = 토큰 미설정 시 declare 승인 실행 실패(`SLACK_NOT_CONFIGURED` 503), 조용한 no-op 폐기
- RegenGate 이벤트 이름 가드는 **버그 수정 범위까지만**(OI-3 — SPEC-150 소유 공용 조각)
- is_lead 게이트 · 추적 Task cc(버전 미특정이면 비움 — OQ-13 발명 금지)
- 죽은 코드: 참조 0 상수 3종 + 도메인 이벤트 12종 per-symbol grep. **STATUS_FAILED 는 존치**(소비처 있음 — 검수 확정). front/ BFF 3건은 FE 워커 몫
- WP-125 가 남긴 것 함께: `tasks_surface.patch_task` 죽은 인자 4개 제거(reviewer_code W6)

## 4. 먼저 읽을 핵심 파일

- WP-126 §Code Surface (심볼 기준 — P0 에서 grep 으로 좌표 잡으라고 명시돼 있다)
- `back/app/services/action_runtime/workflow/round_eval.py` — WP-125 가 만든 seam 훅 (신규 파일)
- `back/app/services/action_runtime/engine/runtime.py::set_run_status` — run 원장 유일 쓰기 경로

## 5. allowed_paths — 이 밖은 건드리지 마라

- `back/` · `mcp/` (docker-compose 2종 포함 — 필요시)

## 6. 구현 단계

WP-126 P0→P6 순서대로. P0 의 운영 DB 실측 항목은 접근 불가면 코드 기준 확인으로 대체하고 보고에 명시. 각 Phase 결과는 완료 보고에 (WP 문서는 갱신하지 않는다 — 문서 레포 접근 금지).

## 7. 하지 말 것

- `front/` 수정 금지 · 문서 레포 수정 금지 · **커밋·push·PR 금지**(같은 브랜치에 코디가 커밋한다)
- 라운드 판정 수렴 시 판정 의미 변경 금지 — 정본 = 활성 라운드, 나머지 2벌은 제거/위임
- WP-126 §범위 밖(알림/DM·에스컬레이션·인바운드 어댑터·SPEC-153 콘솔 본체·웹 완료 버튼) 침범 금지
- 계약과 어긋나는 사실 발견 시 코드 고치지 말고 §9 질문 채널로

## 8. 검증

```
cd back && uv run pytest -q <네가 만들거나 고친 테스트 파일만> (전체 스위트 금지 — 사용자 방침. DATABASE_URL 은 back/pyproject.toml 의 테스트 DB = localhost:25434/mediness_test). 검증은 1회만
```

- mcp 를 만졌으면 mcp 쪽 변경 테스트도 동일 방식.
- 기존 무관 실패는 stash baseline 대조로 "무관" 분리 보고.

## 9. 완료 보고 — **문구 변경 금지**

> ⚠ 핸들은 dispatch preamble 값을 믿어라.

- **커밋·push·PR 하지 마라.** 끝나면 두 명령 모두:

```bash
orca orchestration send \
  --to term_1d6e5d93-2be9-4125-b7eb-42b1de52b5ed --from term_4d57e332-5fc7-4550-9dc6-da4d84117bbc \
  --type worker_done \
  --task-id <dispatch preamble 의 taskId> \
  --dispatch-id <dispatch preamble 의 dispatchId> \
  --subject "backend(WP-126) 완료: <한 줄>" \
  --body "변경 파일 / Phase 별 결과 / 검증 수치 / 계약 준수 / 미결"

orca terminal send --terminal term_1d6e5d93-2be9-4125-b7eb-42b1de52b5ed \
  --text "[worker_done] backend(WP-126) 완료 — <한 줄>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_1d6e5d93-2be9-4125-b7eb-42b1de52b5ed --text "[질문] backend(WP-126): <질문>" --enter`

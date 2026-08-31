
# [backend] 재개 — WARN 4건 수정(R2)이 중단됨. 상태 확인 후 완료하라

너는 **mediness `backend` 워커**다. 전임 워커가 아래 4건을 고치던 중 **머신 종료로 죽었다.** 워크트리에 부분 수정이 남아 있다 — **지우지 말고 그 위에서 이어받아라.**

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/meeting-room-workflow` (미커밋 변경 10파일, +465/−24 근방)

## 1. 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/work/meeting-room-workflow/review-code-report.md` ← W-1·W-3·W-4·W-5 의 파일:줄과 권장 수정 (판정 기준)
- `/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/work/meeting-room-workflow/meeting-room-workflow-be-fix1-brief.md` ← 원 수정 지시 (코디 판정 4건). §9 의 옛 핸들은 무시 — **이 브리프와 preamble 의 핸들이 정본**
- `git diff` · `git status` — 전임 워커가 어디까지 갔는지

## 2. 할 것

1. 현 diff 를 리뷰 리포트의 4건과 대조해 **각각 완료/미완/부분** 을 판정하라:
   - **W-1** 실행 result 의 회의 id 키 **제거** (근거: WP 「result 키 신설 0」 + §7.9.7 원장 방향)
   - **W-3** 저장 前 예외도 보상 경로 안으로 — 어떤 실패든 보상 발동, FAILED_RETRYABLE 아닌 조합표 C(최종 실패) 종결
   - **W-4** 보상이 execution.result 의 원 external_id 를 덮어쓰지 않게 — 크래시 창 이중 예약 방지
   - **W-5** ActionRepository tenant 인자 보강
2. 미완·부분인 것을 완료하라. W-3·W-4 고정 테스트가 없으면 추가하라.
3. 반쯤 고쳐진 코드가 기존 테스트를 깨뜨리지 않는지 포함해 검증하라.

## 3. 하지 말 것

- 4건 외 수정 금지. W-2(채팅 안내)·W-6(§7.2 스펙 환류)은 범위 밖. 커밋·push 금지. 전임 작업 되돌리기(checkout·stash) 금지.

## 4. 검증

```
cd back && pytest -q tests/services/engine_v2/test_wp125_reservation_meeting_chain.py tests/services/engine_v2/test_meeting_definitions.py (전체 스위트 금지). 1회만
```

## 5. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 값과 preamble 이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_6a44553f-d13c-48f6-93ab-bda16d83ffec --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "4건 각각 전임 상태(완료/미완/부분)와 내가 한 것 / 검증 수치"

# (2) 직접 주입
orca terminal send --terminal term_6a44553f-d13c-48f6-93ab-bda16d83ffec \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_6a44553f-d13c-48f6-93ab-bda16d83ffec --text "[질문] backend: <질문>" --enter`

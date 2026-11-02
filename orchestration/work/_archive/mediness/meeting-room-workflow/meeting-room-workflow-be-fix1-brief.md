
# [backend] 수정 R2 — 코드 리뷰 WARN 4건 국소 수정 (W-1·W-3·W-4·W-5)

너는 **mediness `backend` 워커**다. 네 WP-125 착지가 검수에서 WARN(FAIL 0) 을 받았고, 코디 판정으로 4건을 고친다. **국소 수정만** — 구조 재작업 아님.

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/meeting-room-workflow` (네 미커밋 변경 위에서 계속)

## 1. 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/work/meeting-room-workflow/review-code-report.md` ← W-1·W-3·W-4·W-5 의 파일:줄과 권장 수정

## 2. 고칠 것 (코디 판정)

- **W-1** — 실행 result 에 신설한 회의 id 키를 **제거**하라. 근거: WP §Domain/Schema 「result 키 신설 0」 + SPEC-151 §7.9.7 「참조는 회의가 소유 — 예약 원장은 회의를 알지 않는다」. 예약→회의는 역방향 조회가 정본이고 카드 facts 에 이미 회의 참조가 실린다. 되읽는 코드가 0 이니 제거로 끝난다.
- **W-3** — 체인 저장 前 예외도 보상 경로 안으로: try 경계를 옮겨 **어떤 실패든 보상(예약 취소)이 발동**하고, 카드가 FAILED_RETRYABLE(재시도 명령 노출)이 아니라 **조합표 C 계약(최종 실패·재시도 없음)** 대로 종결되게 하라.
- **W-4** — 보상이 execution.result 의 external_id 를 중간에 덮어쓰지 않게 하라 — 크래시 창에서 원 예약 id 가 유실되면 이중 예약이 가능하다. 보상 시도는 원 external_id 를 보존한 채 별도 자리에 기록하라 (result 키 신설 금지와 충돌하면 기존 자리 재사용 — 리포트 권장안 따르되, 안 되면 질문).
- **W-5** — ActionRepository 호출의 tenant 인자 누락 보강.

## 3. 하지 말 것

- 위 4건 외 수정 금지. W-2(채팅 안내)는 코디가 facts 도달로 만족 처리 — 손대지 마라. W-6(§7.2)은 spec 몫. 커밋·push 금지.

## 4. 검증

```
cd back && pytest -q tests/services/engine_v2/test_wp125_reservation_meeting_chain.py tests/services/engine_v2/test_meeting_definitions.py (전체 스위트 금지). W-3·W-4 를 고정하는 테스트를 추가하고 1회만 돌린다
```

## 5. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 값과 preamble 이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_ae5c9156-a854-48b7-8f65-528976906150 --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "4건 각각 처리 / 추가 테스트 / 검증 수치"

# (2) 직접 주입
orca terminal send --terminal term_ae5c9156-a854-48b7-8f65-528976906150 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_ae5c9156-a854-48b7-8f65-528976906150 --text "[질문] backend: <질문>" --enter`

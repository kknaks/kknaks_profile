
# [reviewer_code] 재검수 R2 — WARN 4건(W-1·W-3·W-4·W-5) 해소 확인 (경량)

너는 **mediness `reviewer_code` 워커**다. 먼저 역할 문서를 읽어라: `/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/roles/mediness/reviewer/role.md` (+ 같은 폴더 문서들)

전 리뷰(WARN 6건)를 낸 워커의 터미널이 죽어 네가 이어받는다. backend 가 코디 판정 4건을 고쳤다. **재검수만** 한다 — 전면 재리뷰 아님.

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/meeting-room-workflow` (**read-only — 수정·stash·checkout·테스트 실행 금지.** 코디가 74 passed 독립 확인)

## 1. 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/work/meeting-room-workflow/review-code-report.md` — 원 리뷰 (W-1~W-6 의 파일:줄·권장 수정이 판정 기준)
- `git diff` + untracked — 현재 상태 (10파일 +465/−24 근방)

## 2. 판정할 것

1. **W-1** — 실행 result 에서 회의 id 키가 제거됐나. 감사 이벤트에 남긴 것이 원장 방향(§7.9.7)과 충돌하지 않나.
2. **W-3** — 저장 前 예외(run 조회·연결 조회·payload 검증·역해소)가 전부 보상 경로 안으로 들어와 조합표 C/D 로 종결되나. FAILED_RETRYABLE 노출 잔존 없나.
3. **W-4** — 보상 경로(성공·실패 모두)에서 원 external_id 가 보존되나. 크래시 창 이중 예약 시나리오가 실제로 닫혔나.
4. **W-5** — tenant 인자 보강 + 고정 테스트가 실제로 그 파급 tail 을 무는가.
5. **수정이 새 문제를 만들지 않았나** — 고친 자리 주변만 (모달 발 경로 diff 0 유지 포함).
6. W-2(채팅 안내 — 코디가 facts 도달로 만족 처리)·W-6(§7.2 spec 환류 별건) — 판정 불필요, 리포트에 캐리로만 기재.

## 3. 산출물 — 리포트 1개

`/Users/kknaks/orca/workspaces/kknaks_profile/meeting-ax/orchestration/work/meeting-room-workflow/review-code-report-r2.md`

- 판정(PASS/WARN/FAIL) + 항목별 근거(파일:줄). 리포 파일 수정·생성 금지.

## 4. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 값과 preamble 이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_6a44553f-d13c-48f6-93ab-bda16d83ffec --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_code 완료: <판정 한 줄>" \
  --body "판정 / W-1~W-5 각각 해소 여부 / 신규 문제 유무"

# (2) 직접 주입
orca terminal send --terminal term_6a44553f-d13c-48f6-93ab-bda16d83ffec \
  --text "[worker_done] reviewer_code 재검수 완료 — <판정>. 상세는 인박스." --enter
```

- 막히면: `orca terminal send --terminal term_6a44553f-d13c-48f6-93ab-bda16d83ffec --text "[질문] reviewer_code: <질문>" --enter`

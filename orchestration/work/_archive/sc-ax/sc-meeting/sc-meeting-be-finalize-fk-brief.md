# [backend] 결함 — 합성 적재 FK 위반(AI 안건 교체) · 실패한 잡이 completed 로 닫혀 회의가 「정리 중」에 갇힘

너는 **sc-ax `backend` 워커**다. 세션 그대로. 작업 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`(HEAD = 20723a7). `backend/` 만. 커밋 금지.

## 발견 (코디 브라우저 실물 e2e 3차, 회의 `340e7fd1-c68f-4764-bc34-76d740bd0f41`)

바로 시작 → 전사 3블록 → 메모 1 → **중간 배치 1회 성공(AI 가 안건 「온보딩 자료」를 새로 세움, source ai, order 1 · ai 줄 3)** → `/end` → 합성 job.

1. **`commit_finalized` 가 IntegrityError** — `update or delete on table "meeting_agendas" violates foreign key constraint "meeting_lines_agenda_id_fkey"`. 로그 전문 `orchestration/work/sc-meeting/live-e2e-3-finalize-error.log`(`application.py:474 commit_finalized`). 회의 중 배치가 세운 **AI 안건에 ai 줄이 매달린 채** 합성 적재가 그 안건을 지우거나 교체하려 한다. 지금까지의 e2e 는 배치가 새 안건을 세운 적이 없어 안 드러났다.
2. **잡이 `completed` 로 닫혔는데 회의는 `summarizing` 그대로**(`durable_jobs` attempt_count 1, completed_at 11:39:08, `failure_reason` 없음). 워커 로그는 「poll failed (attempt 1); retrying after backoff」 뒤 traceback. 합성이 예외로 끝났으면 재시도 상한(3) 뒤 **`failed` + `failure_reason`** 이 계약이다(SPEC §5.1·WP-004). 지금은 실패가 삼켜져 화면이 정리 중 폴링에 영원히 갇힌다.

## 고칠 것

1. 합성 적재 순서: **track ai·final 줄을 먼저 지우고(또는 새 안건으로 옮기고)** 그 다음 AI 안건 교체 — AI 안건 매칭 규칙은 브리프 WP-004 §3 그대로(agenda_id 매칭 · 없으면 신설 · 사람 안건 불변). memo 줄은 사람 안건에만 있으니 건드리지 않는다(AI 안건에 memo 가 있을 수 없음을 확인). 테스트: 배치가 세운 AI 안건(+ai 줄)이 있는 회의를 합성하면 IntegrityError 없이 final 줄·AI 안건이 교체된다.
2. `meeting_worker._handle`/`finalize_service.run`: 예외가 나면 잡을 completed 로 닫지 않는다 — 재시도(상한 3) 뒤 `failed` + `failure_reason`(예외 종류 한 줄, 스택·내부 값 없이). 테스트: 합성이 두 번 예외 → 세 번째 성공 / 세 번 예외 → failed·failure_reason·잡 종결.
3. 이 회의(`340e7fd1…`)는 코디가 `/finalize` 로 재시도해 본다 — 지금은 summarizing 이라 409 다. **`summarizing` 인데 살아 있는 잡이 없으면 `/finalize` 를 허용**할지는 코디 판단: 허용하지 않는다(상태 전이표 유지). 대신 2 가 제대로 failed 로 보내면 된다.

## 검증

```
cd backend && uv run pytest -q tests/contract/test_meeting_finalize.py tests/contract/test_meeting_memo_batch.py tests/contract/test_meeting_core.py tests/architecture -m 'not integration'. 검증 1회
```

## 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_50bcf0cc-bae5-4c55-b23a-4143537dd1f3 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "backend 완료: 합성 FK·실패 전이" \
  --body "원인 / 변경 파일 / 검증 수치 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] backend 완료 — 합성 FK·실패 전이. 상세는 인박스." --enter
```

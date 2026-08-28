
# [backend] fix2 — 제출 배선이 커밋 전에 돈다 (e2e 실측 결함 1건)

너는 WORK-023 의 **kknaks-dev `backend` 워커**다. 코디가 로컬 compose 통합 검증에서 실결함을 잡았다. 이 한 건만 고친다.

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/recruiter-chat` (기존 변경 위에)

## 실측 증상 (2026-08-28, 로컬 compose)

- `POST /api/chat/conversations` 201 직후 back 로그:
  `chat: message 2 는 제출 대상이 아니다 — 건너뛴다`
- 워커에 태스크가 영영 안 가고, 대화는 **영구 pending** — 방문자는 컴포저 잠금에 갇힌다.
- GET 폴링에는 재큐잉 경로가 없어 복구 불가. 기동 스윕만이 (재시작 시) failed 로 마감한다.

## 원인

`core/db.py get_db` 는 **의존성 teardown 에서 커밋**한다. 이 FastAPI 버전에서
BackgroundTasks(`_queue_turn` → `start_turn`)가 teardown 보다 **먼저** 실행돼,
`build_plan_for` 가 새 세션으로 **커밋 전** row 를 조회 → `get_message` None → 스킵.
`_queue_turn` 의 주석 「커밋 뒤에 돈다」가 사실이 아니었다.

레퍼런스가 같은 사고를 겪고 계약으로 박은 지점이다 —
`/Users/kknaks/git/harness_works/mediness-app/back/app/services/landing_chat/runtime.py`
머리 주석 「라우터는 **요청 트랜잭션을 커밋한 뒤** submit_and_consume 하나만 부른다」.

## 수정 (판정: 명시 커밋 후 배선 — 레퍼런스 패턴)

1. 제출을 거는 **세 경로 전부**(대화 생성 · add_message · retry)에서, 큐잉 전에
   라우터(또는 서비스 경계)가 `await db.commit()` 을 **명시적으로** 호출한다.
   teardown 의 commit 은 no-op 이 되므로 이중 커밋 무해. `_queue_turn` 주석을
   사실에 맞게 고친다(「명시 커밋 뒤에 건다 — teardown 순서에 기대지 않는다」+ 실측 근거).
2. 방어선 하나: `start_turn` 에서 `build_plan_for` 가 None 인데 **message 가 존재하고
   pending 인** 경우는 「대상 아님」이 아니라 이상 상태다 — 이 경우를 구분해 warning
   으로 남겨라(같은 스킵이라도 로그에서 원인이 보이게).
3. 테스트: 라우터가 큐잉 **전에** 커밋했는지를 순서로 단언(예: commit 을 spy 하고
   add_task 호출 시점과의 순서 검증, 세 경로 모두). 기존 테스트가 이 결함을 못 잡은
   이유를 한 줄 주석으로 남겨라(테스트 클라이언트에선 커밋 타이밍이 달랐다면 그 사실).

## 검증

```
cd app/back && uv run pytest -q tests/
```

## 완료 보고 — 2채널, 핸들은 preamble 우선

```bash
orca orchestration send --to term_53806a6d-ced5-4948-88bd-4181b7ba4323 --from <네 워커handle> \
  --type worker_done --task-id <preamble taskId> --dispatch-id <preamble dispatchId> \
  --subject "backend fix2 완료: <한 줄>" --body "수정 요약 / 테스트 수치"
orca terminal send --terminal term_53806a6d-ced5-4948-88bd-4181b7ba4323 \
  --text "[worker_done] backend fix2 완료 — <한 줄>. 상세는 인박스." --enter
```

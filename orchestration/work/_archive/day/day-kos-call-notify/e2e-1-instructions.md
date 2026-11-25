# [backend · e2e-1] 로컬 스택 + KOS DEMO 실물 — #283 완료 조건

같은 터미널 · 같은 맥락. **코디가 로컬 스택을 띄워 뒀다**: `http://127.0.0.1:11140`(`--kos-demo --scheduler` · DEMO 지점 연결 · migration 0028 · 이 워크트리 미커밋 코드). **스택 시작 · 멈춤 · 재시작 · 코드 수정 금지**(파일을 바꾸면 API 가 리로드에서 멈춘다 — 버그는 원인 file:line 만 리포트에). 다른 워크트리 스택(11040 등) 금지. 로컬 DB 는 SELECT 만(`deploy/local.env` · 스키마 `day_dev` · 포트 11142). 로그 `.run/*.log`.

## KOS 쪽 호출 = 간호사 대신 네가 KOS 를 직접 부른다

- 계정 = `~/.config/day/kos-test-account.env`(`KOS_TEST_EMAIL` · `KOS_TEST_PASSWORD` — **값 출력 금지** · `~/.config/day/` 다른 파일 금지). KOS 주소 = `deploy/kos-demo.env` 의 `KOS_INTERNAL_API_BASE` · `KOS_WEB_BASE` · 테넌트 `DAY_SEED_KOS_TENANT_ID`.
- KOS sign-in → 그 토큰으로 HAR `/Users/kknaks/Downloads/의사호출2.har` 와 같은 모양의 `schedule/flow/v1/commands/call-tasks-doctors`(필요하면 `change-tasks-assignees` 먼저 — HAR 순서). 헤더는 코드 `backend/day/emr/kos/staff_client.py` 의 브라우저 헤더 관례를 따른다(KOS 내부 API 는 브라우저 UA 필수).
- 원장 id = 로컬 DB `staff`(원장 목록 · `external_id`). 끝나면 **네 KOS 로그인 세션을 해제**(`revoke-active-sign-in` · 5기기 한도).
- DEMO 지점은 다른 사람도 쓴다. **오늘 `ready` 이고 호출 안 된 작업**만 고르고, 다른 사람이 쓰는 작업(이미 waiting · 진행)은 건드리지 마라. 시험 뒤 상태를 되돌릴 KOS 명령이 있으면 되돌리고, 없으면 리포트에 남긴 상태를 적어라.

## 시험 (각각 10 ~ 20초 기다려 동기화 확인 · DB SELECT + 로그)

1. **지정 1명** — 작업 1개 · doctorIds 1명 → `doctor_call` 1(kind one · target = 그 원장 · called_by = 시스템 계정) · `notification` = 그 원장 계정 1행 · `push_log`(키 없으면 skipped_no_key 도 OK) · `event_log` call.create payload source kos · kosCalledAt.
2. **전체 호출** — doctorIds 없이 → KOS 일정 응답(동기화 로그 또는 KOS 일정 조회 직접)의 `calledDoctors` 가 **무엇으로 오는지 그대로 기록**(OQ-99 닫기) → DAY 결과(kind · 받는 사람 수) 기록.
3. **여러 작업 한 번에** — sequences 2개 이상 한 요청 → 작업별 `doctorCallDateTime` 이 같은지(밀리초까지) 기록(OQ-106) → doctor_call 1개 · 알림 계정당 1.
4. **재호출** — 1번 작업을 KOS 에서 다시 호출 → 새 doctor_call · 앞 호출 closed · 알림 1 더.
5. **DAY 에서 호출(메아리)** — DAY 웹 API 로 다른 ready 작업에 [의사 호출](로그인 = 같은 테스트 계정 · `/login` 흐름 · 세션 쿠키) → outbox op 이 KOS 에 확인될 때까지 → **doctor_call 1 · 알림 1 그대로**(두 번 아님). **KOS `doctorCallDateTime` 과 op `created_at` · `updated_at` 시각 차**를 초 단위로 기록(I6 · OQ-101 · 30초 창 안인지).
6. **KOS 수락** — 호출된 작업에 KOS 에서 집도의 배정(HAR 의 `change-tasks-doctors` 모양) → DAY `doctor_call_accept` 1 · 알림 추가 없음.
7. 배포 직후 모양 — 이 스택 첫 동기화 때 이미 waiting 이던 6작업(03:48Z)은 doctor_call 0 이었다. 왜 0 인지 코드 근거 한 줄(⑦ 어느 거름인지) — prod 첫 배포 때 오늘 남은 호출이 쏟아지지 않는다는 근거로 쓴다.

## 리포트

`/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/work/day-kos-call-notify/e2e-1-report.md` — 맨 위 표(시험 × 결과 O/X · 수치 · 비고) · OQ-99 · OQ-106 · OQ-101 실측 · 남긴 KOS 상태 · 버그면 원인 file:line. 완료 보고 두 명령(subject 「backend 완료: e2e-1」 · 이번 dispatch 값 · 코디 term_ff2b168e-072a-4b6d-ac4a-8dd2eacda5ce):

```bash
orca orchestration send --to term_ff2b168e-072a-4b6d-ac4a-8dd2eacda5ce --from <네 워커handle> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "backend 완료: e2e-1" --body "<요약>"
orca terminal send --terminal term_ff2b168e-072a-4b6d-ac4a-8dd2eacda5ce --text "[worker_done] backend 완료 — e2e-1 <한 줄>. 상세는 인박스." --enter
```

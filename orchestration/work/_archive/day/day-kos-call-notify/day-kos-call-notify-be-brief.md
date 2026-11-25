
# [backend] #283 — KOS 에서 건 원장 호출 → DAY 원장 호출 알림 · 푸시

너는 **day `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/roles/day/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-kos-call-notify`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

이 워크트리는 너 혼자 쓴다(frontend 워커 없음). base 는 `origin/dev` `55e60aa4` — 워크트리 HEAD 확인 후 시작.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/mediness-mediness/day-kos-call-notify-spec/products/day/20-spec/spec-002-procedure-board.md` — **개정 ㉚ · 규칙 40 ① ~ ⑨** · OQ-99 ~ 107 · KOS 읽기/쓰기 표의 `doctor_called_at` · `call-tasks-doctors` 줄 · 호출 상태 mermaid ← 계약의 SoT. **여기 없는 건 발명하지 마라.**
- `/Users/kknaks/orca/workspaces/mediness-mediness/day-kos-call-notify-spec/products/day/20-spec/spec-005-notifications.md` — §3 「알림 행 만들기 — 원장 호출」 「언제」 ② · 「KOS 에서 건 호출」 표 · 「받는 계정」(N1 · kind one 만 called_doctor) · S-7 · OQ-N21 ~ N24
- Delivery Issue: https://github.com/MediSolveAIDev/CENTURION_DAY/issues/283 (Acceptance · 범위 — `gh issue view 283 -R MediSolveAIDev/CENTURION_DAY`)
- 검수 리포트(구현이 빠지기 쉬운 경쟁 상황 정리): `/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/work/day-kos-call-notify/review-doc-r1-report.md` · `review-doc-r2-report.md` · `review-doc-r3-report.md`

기대는 개념: 해당 없음.

## 2. 배경 / 무엇을 바꾸나

간호사가 KOS 에서 원장을 호출하면 DAY 는 동기화로 `visit_task.doctor_called_at` · `visit_task_staff(role=called_doctor)` 를 받지만 `doctor_call` 을 만들지 않아 알림 · 실시간 · 푸시가 0 이다(dev DB 2026-11-25 확인). DAY 에서 누른 호출만 `services/board_calls.py` `call` · `recall` → 커밋 뒤 `notifications.after_call()` 을 탄다.
이번 변경: 작업 쓰기 공통 경로에서 KOS 호출을 판정해 DAY `doctor_call` 을 만들고, 기존 알림 경로를 그대로 태운다. **핫픽스 — dev 배포 뒤 dev → prod ff 로 prod 에 나간다.** prod 정식 앱 0.1.0 이 그대로 받아야 하므로 `kind = doctor_call` · 글자 · payload 모양을 바꾸지 않는다.

## 3. 계약

해당 없음(BE 단독). 앱 · 웹 화면 코드 변경 없음 — 판 · 앱은 기존 `doctor_call` 표시를 그대로 쓴다.

## 4. 먼저 읽을 핵심 파일

- `backend/day/emr/sync_tasks.py` — `_apply_tasks`(판정 자리 · 규칙 40 ①) · 잠금 `:86-101` · `:215` · existing 읽기 `:268-295` · held `:335-336` · `pending_guards` `:104-120`
- `backend/day/emr/sync_schedules.py:329` · `:421` — (ㄱ) 10초 일정 조회 경로 · 커밋 지점
- `backend/day/services/emr_sync.py:457` · `:464` · `:493` · `:496` — (ㄴ) 예약 상세 반영 연쇄 · 커밋 지점(둘 다 커밋 뒤 `after_call`)
- `backend/day/dtos/sync_state.py:12-18` `PreviousTaskData` — 이전 값(`doctor_called_at` 없음 → 더해야 함)
- `backend/day/services/board_calls.py` — `call` · `recall` · `accept` · 사슬(`reassigned_from_call_id` · `closed_at`) 만드는 방식을 그대로 따라라
- `backend/day/services/board_transactions.py:349-359` `_system_staff` — 호출자 = 시스템 계정(⑧)
- `backend/day/services/notifications.py:310-330` `_recipients` — kind one 규칙 40 호출만 called_doctor 행으로(②·N1) · `:332-407` 중복 막기 · `after_call`
- `backend/day/emr/outbox_rules.py` · `emr/outbox_persistence.py` · `emr/kos/writes.py:481` · `:492-497` — 메아리 판정(⑥ (가) ~ (라) · `last_error` BLOCKED/토큰 없음)
- `backend/day/policies/board_rules.py` — 유효 호출 · `task_state` · `recall_target`/`chain_root`
- `backend/day/models/task.py:223-260` — `DoctorCall` · `DoctorCallTask` · `DoctorCallAccept`

## 5. allowed_paths — 이 밖은 건드리지 마라

- `backend/ (frontend 몫 — backend/day/routers/(api 제외) · templates/ · static/ · styles/ — 제외) 중 브리프가 지정한 곳`
- `pyproject.toml · uv.lock (의존성 추가가 브리프에 있을 때만)`
- `deploy/ · scripts/ (브리프가 지정할 때만)`

## 6. 구현 단계

1. 스펙 규칙 40 ① ~ ⑨ 를 **한 줄도 빼지 말고** 구현한다: 판정 자리 `_apply_tasks`(두 경로) · 잠금 뒤 이전 값 · 묶음(같은 kind + 원장 집합 · 가장 이른 새 시각과 허용 오차) · 재호출 사슬 · KOS 수락(W1 (i) + 전이) · 메아리 창 · 늦은 관측 거름(오늘 · WAITING · 판 카드 · 수락/진행/완료 아님 · 시스템 계정 있음) · 호출자 시스템 계정 · 커밋 뒤 `after_call`.
2. 허용 오차 등 수치는 스펙 기본값 그대로 상수로(새 설정값 · 환경 변수 만들지 마라).
3. `event_log` 에 근원 표시가 스펙에 있으면 그대로(`source: "kos"`).
4. 시험(`backend/tests/` 기존 관례 따라): 최소 — 지정 1명 · 지정 2명(받는 사람 = 그 원장들) · 전체(빈 calledDoctors → 원장 전원) · 여러 작업 묶음 · 시각 어긋남 묶음 · 메아리(op pending/sent/confirmed/failed-BLOCKED/failed-STALE) · 재호출 사슬 · KOS 수락 전이 · 옛 READY 거름 · 늦은 관측 거름 · (ㄴ) 경로에서 먼저 저장돼도 알림 1번 · 같은 변화 두 회차 → 호출 1개 · 알림 행 계정당 1번.
5. 기존 시험 중 이 변경이 닿는 파일(동기화 · 판 호출 · 알림)도 돌려 회귀 확인.

## 7. 범위 제약 — 하지 말 것

- migration · 새 알림 kind · 새 글자 · 새 설정 스위치 · 환경 이름 분기 금지(필요해 보이면 멈추고 질문).
- 웹 화면 · 앱 코드 · 템플릿 · static 수정 금지. 웹 예약/고객 화면 끄기는 **범위 밖**(사용자가 따로).
- 사용자 로컬 스택 · 포트 · docker · `~/git/CENTURION_DAY` 정본 체크아웃 · 공유 dev/prod DB 손대지 않기. 시험 DB 는 로컬 compose 시험 스키마만.
- 커밋 · push · PR 금지. 스펙과 코드가 어긋나 보이면 스펙을 고치지 말고 질문.
- 실물 e2e(로컬 스택 + KOS DEMO)는 **이번 단계 아님** — 코디가 스택을 띄운 뒤 따로 발주한다.

## 8. 검증

```
cd backend && uv run pytest -q <네가 만들거나 고친 테스트 파일만> · uv run ruff check <네가 만진 파일> — 각 1회, 통과하면 반복하지 마라. 테스트 DB 는 로컬 compose — 공유 STG·PROD 금지. 사용자 포트·프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending
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
  --to term_ff2b168e-072a-4b6d-ac4a-8dd2eacda5ce --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: #283 1루프" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_ff2b168e-072a-4b6d-ac4a-8dd2eacda5ce \
  --text "[worker_done] backend 완료 — #283 1루프 요약. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_ff2b168e-072a-4b6d-ac4a-8dd2eacda5ce --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)

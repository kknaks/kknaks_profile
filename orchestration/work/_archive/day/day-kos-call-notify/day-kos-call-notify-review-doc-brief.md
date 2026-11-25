# [reviewer_doc] 스펙 개정 검수 — KOS 원장 호출 → DAY 알림 · 웹 예약/고객 화면 열림 설정

너는 **day `reviewer_doc` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-kos-call-notify-spec` (planner 가 미커밋 변경을 남겨 둠 — **읽기만**)
base 브랜치: `origin/main` → 최종 PR 대상 `main`

## 1. SSOT — 먼저 읽을 것

- 검수 대상 = 워크트리 미커밋 diff(`git diff origin/main -- products/day/`): `20-spec/spec-005-notifications.md` · `spec-002-procedure-board.md`(개정 ㉚ · 규칙 40 · OQ-99~105) · `spec-006-reservation-board.md`(개정 ⑭ 「웹 화면 열림 설정」) · `spec-007-reservation-detail.md` · `20-spec.md` · `log.md`.
- 발주 내역(무엇을 정했나 · 사용자 결정): `/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/work/day-kos-call-notify/day-kos-call-notify-spec-brief.md` §2 · §3 · §7 — 이게 계약 기준. planner 보고의 「브리프와 다른 곳」 7건은 아래 §6 에서 맞는지 본다.
- 코드(읽기 전용 · `origin/dev` = `55e60aa4`): `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-kos-call-notify`
- 실물: HAR `/Users/kknaks/Downloads/의사호출2.har`(KOS `call-tasks-doctors` 두 번 — doctorIds 없음 / 있음).

기대는 개념: 해당 없음.

## 2. 배경

간호사가 KOS 에서 원장을 호출하면 DAY 는 동기화로 `doctor_called_at` · `called_doctor` 를 받지만 `doctor_call` 을 안 만들어 알림 · 푸시가 0 이다. 이번 개정은 ① 동기화가 KOS 호출을 DAY 원장 호출로 만들어 기존 알림 경로에 태우는 규칙 ② prod 웹에서 고객 차트 · 예약 현황을 설정값으로 끄는 규칙이다. 이 스펙으로 바로 구현 · dev → prod 배포가 나간다.

## 3. 계약

해당 없음(스펙 검수).

## 4. 먼저 읽을 핵심 파일 (코드 사실 대조용)

- `backend/day/services/board_calls.py` — call · recall · accept · cancel_call(accept 가 `closed_at` 을 안 채우는지)
- `backend/day/services/board_rules.py` · `task_state` 관련 — 유효 호출 · 「준비중」 판정
- `backend/day/services/notifications.py` — `after_call` 받는 사람(전체/지정 · `target_staff_id`)
- `backend/day/emr/kos/mapper.py:484` 근처 · `sync_tasks.py` · `sync_schedules.py` · `sync_tables.py` — 동기화가 `doctor_called_at` · staff 를 어떻게 갱신하나(매 회차 같은 값 쓰는지 — A7 「배포 직후 안 걸림」 주장)
- `backend/day/emr/kos/writes.py` · `outbox_rules.py` — call-tasks-doctors 본문(doctorIds 있나) · 확인 조건 · op 상태(pending/sent/confirmed/failed) · created_at/updated_at — A6 메아리 판정 근거
- `backend/day/models/task.py` — `DoctorCall.target_staff_id` · 호출자 칸 필수 여부(A8)
- 웹 설정 관례: `backend/common/config.py` · `deploy/config/*.env` · `deploy/local.env.example` — B3 위치 · 기본값 fail-closed 관례가 정말 있는지

## 5. allowed_paths

- 리포 파일 수정 · 생성 금지. 산출물은 리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/work/day-kos-call-notify/review-doc-r1-report.md`

## 6. 검수 항목

1. 브리프 §3 A1~A9 · B1~B4 · C 가 빠짐없이 들어갔나 · 사용자 결정(새 알림 종류 · 글자 · 스위치 없음 · 환경 이름 분기 없음 · 화면 문구 발명 없음 · 「전체 호출」 추측 확정 없음)을 어긴 곳이 없나.
2. planner 의 「브리프와 다른 곳」 7건 각각 — 코드 사실로 맞나(파일:줄):
   ① A5 수락 = `doctor_call_accept` · 호출 안 닫음 ② 지정 2명 이상 = 전체(target 1칸) ③ 메아리 = op 시간 창 + 허용 오차 30초 ④ 배포 직후 첫 동기화가 안 걸림 ⑤ KOS 호출 줄이 DAY 판에서도 「호출」로 보이는 부수 효과 · 호출 취소 뒤 되살아나지 않음 ⑥ 고객 화면 스펙 부재 → SPEC-006 정본 ⑦ 설정 위치 `deploy/config/<env>.env` · 이름 `DAY_WEB_RESERVATION_CUSTOMER_ENABLED` · 꺼짐 = 메뉴 숨김 + 303 /board · HX-Redirect · SSE.
3. 구현자가 이 스펙만 보고 **한 가지로** 짤 수 있나 — 묶음 기준 · 메아리 경쟁 (가)~(라) · 늦은 관측 거름 · 재호출 사슬 · 동시 실행(동기화 두 회차 · API 프로세스) 때 같은 KOS 호출로 `doctor_call` 이 두 번 생기지 않는 보장(잠금 · 유일성)이 적혀 있나.
4. 알림 중복: KOS 호출 1건 → 원장 계정당 알림 1번 · 푸시 1번이 보장되나(SPEC-005 「중복」 줄과 맞나).
5. 정식 앱 0.1.0 이 받는 모양이 바뀌지 않나(kind · 본문 칸).
6. OQ 마다 기본값이 있고 착수를 막지 않나 · 기본값이 추측으로 사실을 확정하지 않나.
7. `python3 scripts/lint-pipeline.py --strict` → products/day ERROR 0.

## 7. 범위 제약

- 고치지 마라 — 지적만. 사용자 결정을 뒤집자고 하지 마라(문제라면 「위험」으로 적고 근거).
- 코드 레포 · 스펙 레포 수정 금지. 커밋 · push 금지.

## 8. 검증 · 판정

리포트 = 판정 PASS / WARN / FAIL + 지적마다 [심각도 · 파일:줄 · 근거(코드 파일:줄 또는 브리프 줄) · 고칠 방향]. FAIL = 구현이 틀리게 나갈 지적이 하나라도 있을 때.

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
  --subject "reviewer_doc 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_ff2b168e-072a-4b6d-ac4a-8dd2eacda5ce \
  --text "[worker_done] reviewer_doc 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_ff2b168e-072a-4b6d-ac4a-8dd2eacda5ce --text "[질문] reviewer_doc: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)

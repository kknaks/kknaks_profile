# [backend] SPEC-008 예약 요청 스레드 — WP-0 바닥(실물 확인 · migration · ext 키) → WP-1 ext → WP-2 웹 동작

너는 **day `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation3/orchestration/roles/day/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation3`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

⚠ **frontend 워커가 같은 워크트리에서 동시에** 화면 조각 라우트(`routers/reservation_requests.py` · GET) · templates · static · styles · `tests/day/web/` 를 만든다 — 건드리지 마라. **너는 앞 맥락이 없다.** 워크트리는 origin/dev `a76496c4` 깨끗 · alembic head `20261125_0030`.

## 1. SSOT — 먼저 읽을 것

- **Delivery Issue #297**(승인됨 · `delivery-plan:approved`) — `gh issue view 297 --repo MediSolveAIDev/CENTURION_DAY`(Target Delta · Acceptance A1 ~ A7 · Non-Goals)
- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation3/orchestration/work/day-reservation3/delivery-1-report.md` ← **WP-0 ~ WP-3 표 · BE ↔ FE 계약(조각 경로 · 오류 · SSE · 버튼 규칙 · 알림). 둘 사이 계약은 이것**
- SPEC-008 `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation3-spec/products/day/20-spec/spec-008-reservation-request.md`(PR #968 · 정본) + 같은 폴더 SPEC-006 ⑭ · 005 · 007 고침 6 · 000 ③(개정 머리의 「계획」 문구는 이번 구현 대상이라는 뜻)
- 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation3/reference/2026-11-26-reservation-request/reservation-request-decisions.md`(RQ1 ~ RQ44)
- 시안 v15 `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation3/orchestration/work/day-reservation3/design/20261126_예약현황_시연_v15.html`(생김새 · 문구 정본 · base64 빼고 grep) · 스크린샷 같은 폴더 `v15-*.png`
- KOS 실물 근거 `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation3/orchestration/work/_archive/day/day-reservation2/be-probe-1 ~ 4-report.md`
- 코드 레포 `AGENTS.md`(이 워크트리 루트) · SPEC-007 구현(예약 등록 · 쓰기 큐 · SSE — 이미 dev 에 있음)

**질문하지 말고 기준으로 정해라**: SPEC-008 에 있으면 그대로 · KOS 값 = KOS 를 따른다 · 화면 = 시안 v15 · 글자 = SPEC-008 §2 「임시 글자 목록」(없는 글자는 비움) · 데이터 없는 칸 = 빈 값. 이 기준으로도 안 정해지는 것만 코디에게. **사용자 질문으로 열린 것**(OQ-Q04 문구 · Q05 · Q08 · Q12 · Q15 · Q20)은 SPEC 기본값대로 짜고 막지 마라.

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

링키(외부)가 ext 로 완성된 예약 요청을 보내고, 병원은 스레드에서 주고받다 버튼 한 번으로 DAY · KOS 에 예약을 만든다/고친다/취소한다. 너는 서버 전부(실물 확인 · DB · ext API · 웹 동작 · 쓰기 묶음 · 알림 · SSE 신호)를 맡는다. 화면은 frontend.

## 3. 계약

`delivery-1-report.md` 「BE ↔ FE 계약」 그대로. 웹 **POST 동작 경로**(create · update · cancel · retry · dismiss-failure · comments · withdraw)와 SSE 신호 `reservation_request` 는 **네가** 만든다(새 라우터 파일 `routers/reservation_request_actions.py` 하나 — 응답 = 성공이면 FE 조각을 다시 그리게 하는 SPEC-007 동작 라우트와 같은 방식). GET 조각(목록 · 창 · 2열)은 frontend 가 만들고, 그 조각이 쓸 **읽기 서비스 함수**(목록 · 창 상태 · U-5 버튼 상태 · 2열 칸)는 네가 `services/` 에 만들어 이름 · 반환 dataclass 를 보고에 적는다(frontend 가 먼저 가짜로 그리고 이어 붙인다).

## 4. 먼저 읽을 핵심 파일

`backend/day/routers/api/ext.py` · `schemas/ext*.py` · `services/ext_*.py` · `models/ext.py` · `emr/ext_commands.py` — `git grep -n partner -- backend`(전수 · SPEC-008 partner 표와 대조) · `services/reservation_book.py` · `dtos/emr_writes.py` · `emr/kos/writes.py`(`write_open` · `plan_reservation` · `_resource_body`) · `emr/outbox_rules.py` · `routers/reservation_detail.py`(공용 retry 두 길) · `enums/notification.py` · `services/notification*` · `notification_events` · `routers/board_streams.py`/`reservations` 스트림 · `models/visit.py` · `models/customer.py` · migrations `20261125_0029_partner_charty.py` · `0030`

## 5. allowed_paths — 이 밖은 건드리지 마라

- `backend/` 중 frontend 몫(`routers/reservation_requests.py` · 그 밖 화면 GET 라우트 · `templates/` · `static/` · `styles/` · `tests/day/web/`) 뺀 전부 — 새 `routers/reservation_request_actions.py` 는 네 것 · `routers/reservation_detail.py` 는 공용 retry 409 몇 줄만
- migrations · `backend/tests/`(web 제외)
- 실물 확인 스크립트 = `/private/tmp/day-probe-r3/` · 리포트 = `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation3/orchestration/work/day-reservation3/be-probe-1-report.md`

## 6. 구현 단계

1. **WP-0 ① 실물 확인(맨 먼저)** — 규칙은 `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation3/orchestration/work/_archive/day/day-reservation2/be-probe-1-instructions.md` 그대로(데모 지점 확인 통과 뒤에만 쓰기 · 레포 안 고침 · 값/토큰/개인정보 출력 금지 · 시험 고객 하나 · 만든 예약은 끝에 취소 정리). 셋: OQ-Q01(`reserve` 본문에 `counselor` 바로 되나 · 안 되면 reserve 뒤 `update-reservation {scheduleId, counselor}` · 다시 읽어 `reservation.counselor`) · OQ-Q02(W4 한 본문에 최상위 `reservationMemo` · `funnel` → 다시 읽어 메모 · 유입 · 다른 칸 안 지워짐) · OQ-Q03(`create-visitor` `email` → 다시 읽어 저장됨). 결과 표를 `be-probe-1-report.md` 에. **Q02 가 안 되면 멈추고 `[질문]`**(SPEC F3 · 사용자 질문). Q01 · Q03 이 안 되면 SPEC 대체 경로로 짜고 보고
2. **WP-0 ②~④** migration(새 표 4 · `notification.reservation_request_id` · `NotificationKind` 값 · `closed_reason` · ext `partner` null 가능 · 유일키 병원 단위 — 겹치는 행이 있으면 migration 이 멈추고 메시지) · 모델 · ext 키 병원당 하나(PartnerGrant `partner` 선택 · 한도 · outbox · `_charty` 막음 없앰 · 테스트 11 파일 고침) — 기존 ext 회귀 0
3. **WP-1** ext E1 ~ E8 · 본문 검증(길이 상한 · `phone` · 합친 메모 1000자 · 예약 그룹 / 유입 / 직원 id 존재) · 판정 RQ24 · 버전 번호 · Idempotency-Key · 상태 전이 ext 줄 · 철회 · 자동 닫힘(희망 일시 지남 — 기존 주기 작업에 붙임) · 알림 행 + `announce_unread` · SSE 신호
4. **WP-2** 웹 동작(위 §3) · 쓰기 묶음(W2 · W3 · W18 / W4(+메모 · 유입) / W5 · 메모 합치기 · `visit_id` = W3 확인 · `reservation_applied` = 묶음 마지막 확인 뒤) · 확인 대기 유지 · 접음 · 스레드 retry · **공용 retry 두 길 = 스레드 행이면 409** · 같이 누름 409(행 잠금) · 변경 요청(칩 · 대체됨 · 철회) · 댓글 · `hospital_seen_at` · 알림 목록 transport 거름 · target `{requestId, date}` · 권한 = 예약 등록 권한
5. §8 검증 · 보고에 frontend 가 쓸 읽기 서비스 이름 · 반환 모양 · 오류 코드 목록

## 7. 범위 제약 — 하지 말 것

- 실물 확인(§6-1) 밖에서 KOS 실제 호출 금지(테스트는 가짜 · e2e 는 코디) · `deploy/*.env` · `~/.config/day/` · 로컬 스택 · 사용자 포트 · 커밋 · push
- 기존 ext 경로 동작 변경(키 범위 RQ7 빼고) · 웹 예약 등록 동작 변경 · 앱(푸시 · 화면)
- 글자 짓기 금지(SPEC-008 §2 임시 목록만 · 없으면 빈 값)

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
  --to term_5c196973-a9ec-4982-81c2-655361f18aec --from term_b1118a66-0d50-43c8-9b6b-57ebfc4be800 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_5c196973-a9ec-4982-81c2-655361f18aec \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_5c196973-a9ec-4982-81c2-655361f18aec --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)

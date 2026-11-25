# [planner] KOS 에서 건 원장 호출도 DAY 알림 · 푸시 + prod 웹 고객 차트 · 예약 현황 끄기 — 스펙 개정

너는 **day `planner` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/roles/day/planner/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-kos-call-notify-spec`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

이 워크트리는 너 혼자 쓴다. 코드 레포는 **읽기만**.

## 1. SSOT — 먼저 읽을 것

- `products/day/20-spec/spec-005-notifications.md` — §3 「알림 행 만들기 — 원장 호출 (서버)」 · 「원장 호출 푸시 — 발송」 · 「웹 — 브라우저 OS 알림」. 이번 개정의 본체.
- `products/day/20-spec/spec-002-procedure-board.md` — KOS 동기화 칸 표(§946 근처 `visit_task.doctor_called_at` ← `tasks[].doctorCallDateTime`) · 호출 · 재호출 · 수락 · 호출 취소(규칙 38) · KOS 쓰기 표(§1096 근처).
- `products/day/20-spec/spec-000-data-model.md` — `doctor_call` · `doctor_call_task` · `visit_task_staff(role = called_doctor)` · `notification`.
- `products/day/20-spec/spec-006-reservation-board.md` · `spec-007-reservation-detail.md` — 예약 현황 · 예약 등록 · 상세 웹 화면. 고객 목록 · 고객 차트 웹 화면이 어느 스펙에 있는지는 `products/day/` 안을 grep 해서 찾아라(코드 CENTURION_DAY #274 「고객 목록 · 차트 추가」).
- 기획 원천: `products/day/00-baseline/planning/데이(CC)-개요.md:681` 「KOS에서 잡은 의사 호출 · 처방 = 읽기」.
- 코드(읽기 전용 · `origin/dev` = `55e60aa4`): `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-kos-call-notify`

기대는 개념: 해당 없음.

## 2. 배경 / 무엇을 바꾸나

간호사들이 DAY 대신 KOS 화면에서 원장을 호출하는 경우가 있다. 지금 DAY 는 그 호출을 **동기화로 받기는 하는데**(10초 · `visit_task.doctor_called_at` · `visit_task_staff role=called_doctor`) 원장 호출 알림을 만들지 않는다. 알림 · 실시간 · 푸시는 DAY 에서 누른 호출(`services/board_calls.py` `call` · `recall` → `doctor_call` 행 → 커밋 뒤 `notifications.after_call()`)에서만 생긴다. 그래서 KOS 에서 부르면 원장에게 아무 알림이 안 간다.

코디가 2026-11-25 확인한 실물:
- HAR `/Users/kknaks/Downloads/의사호출2.har`(DEMO 지점 · 10:48 KST): KOS 웹 명령 `schedule/flow/v1/commands/call-tasks-doctors` 두 번 — ① `{scheduleId, sequences:[1]}`(doctorIds 없음 = 전체 호출) ② `{scheduleId, sequences:[1], doctorIds:[…]}`(지정 호출). 6초 간격.
- dev DB: 그 작업 `doctor_called_at = 01:48:56Z`(두 번째 시각 → **다시 부르면 시각이 바뀐다**) · `called_doctor` 1명 · `status = waiting` · 그 사이 `doctor_call` 행 **0건**.
- **모르는 것**: 「전체 호출」만 했을 때 KOS `calledDoctors` 가 무엇으로 오는지(원장 전원 · 빈 배열 · 다른 값). 이 HAR 은 곧바로 지정 호출로 덮였다. → 스펙에 OQ 로 열어 두고 구현 단계 첫 실물 1회로 닫는다고 적는다. 추측으로 메우지 마라.

이번에 같이 나가는 배포: dev 에 넣고 **dev → prod ff 로 처음 크게 올린다**(prod 는 `a6aa4ba5` · DB 0009 → 0028). 그때 prod 웹에서는 **고객 차트 · 예약 현황을 끈다**(사용자 2026-11-25 「고객 차트, 예약현황은 비활성화(프론트)에서 나중에 할거야」).

## 3. 정해진 것 — 스펙에 그대로 반영 (되묻지 마라)

사용자 · 코디 2026-11-25 결정. 각 줄에 근거로 「사용자 2026-11-25」를 단다.

**A. KOS 에서 건 호출 → DAY 원장 호출**
1. 언제: 시술 현황 동기화가 작업의 `doctor_called_at` 이 **새로 생기거나 바뀐 것**을 봤고, 그 호출이 DAY 가 KOS 에 쓴 호출(outbox `call_doctors` 의 되돌아온 값)이 **아닐 때** → DAY `doctor_call` 을 만들고, 동기화 커밋 뒤 기존 「알림 행 만들기 — 원장 호출」 · 실시간 · 푸시를 **그대로** 탄다. 새 알림 종류 · 새 글자 · 새 설정 스위치 없음(`kind = doctor_call` · 제목 · 본문 규칙 그대로 → 정식 앱 0.1.0 도 받는다).
2. 받는 사람: KOS `calledDoctors` 로 정한다. 지정(1명 이상) = 그 원장(들) · 전체 호출 표현은 OQ(§2) — 닫히기 전 기본값 = 「`calledDoctors` 가 비어 있으면 전체 호출(병원 원장 목록 전부)」로 두고 OQ 에 「실물로 확인 · 다르면 고침」.
3. 묶음: 같은 방문 · 같은 동기화 회차에서 같은 시각으로 새로 호출된 작업들은 **호출 하나**(DAY 호출처럼 `doctor_call_task` 여러 줄)로 묶는다. 묶는 기준은 기존 DAY 호출 모델에 맞춰 너가 정하고 근거를 적어라.
4. 재호출: 열린 DAY 호출이 있는 작업에서 `doctor_called_at` 이 바뀌면 DAY 재호출과 같은 처리(새 호출이 이어받고 앞 호출은 닫힘 · 기존 `reassigned_from_call_id` · `closed_at` 규칙).
5. 수락 · 닫힘: KOS 에서 집도의가 정해지거나(`doctor_assigned_at` · `doctors`) 작업이 진행되면 기존 동기화가 DAY 호출을 어떻게 다루는지 **코드에서 확인**해 그대로 쓰거나, 빈 곳이면 「DAY 수락과 같은 결과(호출 닫힘)」로 적는다. 호출 취소는 KOS 에 명령이 없으니 해당 없음.
6. 메아리 막기: DAY 에서 누른 호출이 KOS 에 쓰이고(outbox) 다음 동기화로 같은 시각이 돌아와도 **알림이 두 번 가면 안 된다**. 판정 방법(outbox 행 · 이미 열린 DAY 호출의 시각 비교 등)을 코드 사실 위에서 정하고 경쟁 상황(outbox 반영 전 동기화가 먼저 돈 경우)을 적어라.
7. 늦은 관측: 배포 직후 첫 동기화 · 동기화가 멈췄다 다시 돈 경우에 **이미 오래된 호출**이 한꺼번에 알림으로 쏟아지지 않게 한다. 기본값 = 「이미 그 작업이 수락 · 진행 · 완료됐으면 만들지 않음」 + 「오늘(병원 현지) 것만」. 더 필요한 기준이 있으면 OQ 로.
8. 호출한 사람: KOS 호출이라 DAY 직원이 아니다 — `doctor_call` 의 호출자 칸이 필수라면 기존 규칙(예: 병원 시스템 계정 · SPEC-002 「바로 시작」 경로)과 맞춰 정하고 근거를 적어라. migration 이 필요하면 **필요하다고 적고 멈추지 말고** 최소안으로 적되, migration 없이 되는 안이 있으면 그쪽이 기본.
9. 웹 OS 알림 · 앱 푸시 · 알림 목록: 모두 기존 경로 그대로. 바뀌는 것 없음을 명시.

**B. prod 웹에서 고객 차트 · 예약 현황 끄기**
1. **프론트만** 끈다 — 메뉴(내비)에서 숨기고 그 화면 주소로 직접 들어오면 들어가지 못하게(기본값: 시술 현황으로 보냄). 서버 API · 동기화 · 테이블은 그대로 둔다.
2. 대상 = 고객 목록 · 고객 차트 화면, 예약 현황 화면(그 안의 예약 등록 · 예약 상세 포함). 시술 현황 · 차트 모달(시술 현황 안) · 채팅 · 알림은 그대로.
3. 켜고 끄는 방법 = **서버 설정값(환경 변수) 하나**로 화면을 연다(기본: dev 켬 · prod 끔). 환경 이름(APP_ENV 등)으로 분기하지 않는다 — 「제품 규칙은 설정으로 연다」. 설정 이름 · 위치(로컬 `deploy/local.env` · 서버 Key Vault/app.env)는 코드 관례를 보고 정해라.
4. 화면에 새 글자를 지어 넣지 마라(꺼진 화면 안내 문구 등). 필요하면 OQ 로.

**C. 배포 · 백필 (스펙에는 운영 메모로만)**
- dev 배포 → 확인 → dev → prod ff · migrate-prod(`--ref prod`) · prod FCM 키 · worker. **지난 이력 백필은 나중**(수동 · 사용자 2026-11-25). 정식 앱 0.1.0 이 서버 업데이트 뒤 깨질 수 있음을 사용자가 받아들였다(2026-11-25).
- 배포 절차 문서(`40-architecture/deployment.md` 등)에 이미 있는 내용이면 고치지 말고 가리키기만.

## 4. 먼저 읽을 핵심 파일 (코드 · 읽기 전용)

- `backend/day/services/board_calls.py` — `call` · `recall` · `cancel_call` · `doctor_call` 만드는 곳 · 커밋 뒤 `notifications.after_call`.
- `backend/day/services/notifications.py` — `after_call` 받는 사람 · 행 · 실시간 · 푸시.
- `backend/day/emr/kos/mapper.py:484` 근처 — `doctorCallDateTime` · `calledDoctors` · `doctorAssignedDateTimeUtc` 받는 곳.
- `backend/day/emr/sync_tasks.py` · `sync_schedules.py` · `sync_tables.py` — 작업 · 담당자 동기화(DAY 호출과 겹칠 때 어떻게 되는지).
- `backend/day/emr/kos/writes.py` · `backend/day/emr/outbox_rules.py` — `call-tasks-doctors` 쓰기 · 반영 대기 판정.
- `backend/day/models/task.py` — `DoctorCall` · `DoctorCallTask` · `DoctorCallAccept`.
- 웹 내비 · 라우트: `grep -rn "reservation\|customer" frontend backend/day/web* backend/day/static 2>/dev/null` 로 찾아라(위치는 코드 관례 따름).

## 5. allowed_paths — 이 밖은 건드리지 마라

- `products/day/`

## 6. 할 일

1. SPEC-005 개정(A) — 「알림 행 만들기 — 원장 호출」 「언제」 줄을 DAY 호출 + KOS 호출로 넓히고, KOS 호출 하위 표(§3 A1~A9)를 같은 틀로 더한다. User Scenario 에 「간호사가 KOS 에서 호출」 한 줄.
2. SPEC-002 개정(A) — 동기화가 KOS 호출을 DAY 호출로 만드는 규칙 · 메아리 · 재호출 · 수락 연결. 개정 번호는 기존 관례(㉙ 등) 다음.
3. 고객 차트 · 예약 현황이 있는 스펙(006 · 007 · 고객 화면 스펙)에 B 개정 — 화면 열림 설정.
4. SPEC-000 은 migration 이 필요할 때만.
5. `products/day/log.md` 에 한 줄씩(기존 형식).
6. OQ: 전체 호출 `calledDoctors` 표현 · 그 밖 네가 찾은 열린 것. 각 OQ 에 기본값.
7. 30-work WP 는 **이번엔 쓰지 마라**(스펙 검수 · 사용자 확인 뒤 따로 발주).

## 7. 범위 제약 — 하지 말 것

- 새 알림 종류 · 새 글자 · 새 설정 스위치 만들지 않기(정식 앱 0.1.0 그대로 받게).
- 환경 이름 분기(「prod 면 숨김」) 금지 — 설정값으로.
- 화면 문구 지어 넣지 않기.
- 코드 레포 수정 금지. 커밋 · push · PR 금지.
- 「전체 호출」 표현을 추측으로 확정하지 않기(OQ + 기본값).

## 8. 검증

```
python3 scripts/lint-pipeline.py --strict → products/day/ 범위 ERROR 0 (타 제품 기존 WARN/ERROR 는 '무관'으로 분리 보고). 근거 없는 정책 0 · 열린 것은 열린 것으로
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.
- 보고 본문에 §3 A1~A9 · B1~B4 각각 어느 문서 어느 절에 들어갔는지 표로.

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
  --subject "planner 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_ff2b168e-072a-4b6d-ac4a-8dd2eacda5ce \
  --text "[worker_done] planner 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_ff2b168e-072a-4b6d-ac4a-8dd2eacda5ce --text "[질문] planner: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)

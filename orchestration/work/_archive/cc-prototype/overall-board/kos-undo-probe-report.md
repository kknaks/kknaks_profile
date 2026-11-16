# WORK-006 WP-KOS — 되돌리기 KOS 실호출 확인 결과 보고

## 상태: in-progress — K1 ~ K4 끝 · K5 는 「방 없는 ETCETERA 붙은 일정」 대기(질문 채널로 요청함)

- 대상: 데모 테넌트(`procedure/.env` · 운영 명동점 키 아님) · 4층 · 2026-10-26(KST) 일정 **1건(일정 A)** — 방 있음. 작업 = 작업 1 ETCETERA 「방 배정」(READY · 방1) · 작업 2 PROCEDURE(DONE) · 작업 3 PROCEDURE(READY · 집도의 1 · 담당 1) · 작업 4 PROCEDURE(READY). **방 없는 ETCETERA 없음** → K1 ~ K4 는 PROCEDURE(작업 3)로
- 방법: scratchpad 일회성 스크립트(back `KosClient` 토큰만 빌림 · 별도 scratch DB) — 코드 레포 변경 0 · 사용자 스택(3700 · 8700) 손대지 않음. 보낼 때마다 2초 뒤 내부 `get-schedules-grouped-by-zone` 으로 다시 읽어 전후 비교. 원본 응답은 scratchpad 에만(이 리포트엔 id · 이름 · 토큰 0)
- 순서 변경: 일정 A 가 이미 `PROCEDURE` 라 **K4(뒤로 가기)를 먼저**, K3(`PROCEDURE_WAITING` → `PROCEDURE`)를 그 뒤에 해 기준선 겸 원상 복구로 썼다

## K1 ~ K4

| # | 요청 | 본문 모양 | HTTP | 거절 코드 | 전 → 후(KOS 조회) | KOS 화면 |
|---|---|---|---|---|---|---|
| K1 | 내부 `schedule/flow/v1/commands/change-tasks-complete` | `{scheduleId, sequences:[작업 3], complete:true}` | 200(본문 키 없음) | — | 작업 3 `status` READY → **DONE** · `completedDateTimeUtc` 없음 → 있음 · flowStep `PROCEDURE` 그대로 | 미관찰(워커는 KOS 웹 화면을 못 봄) |
| K2 | 같은 경로 | `{scheduleId, sequences:[작업 3], complete:false}` | **200**(본문 키 없음) | — | 작업 3 `status` DONE → **READY** · `completedDateTimeUtc` 있음 → **없음** · `doctors`(1) · `assignees`(1) · `doctorCallDateTime` · `doctorAssignedDateTimeUtc` **그대로** · 22초 뒤 다시 읽어도 READY(DONE 으로 안 돌아감) | 미관찰 — E2E #22 에서 코디/사용자 확인 필요 |
| K4 | 공개 `schedule/open/v1/commands/change-flow-step` | `{scheduleId, step:"PROCEDURE_WAITING"}`(지금 `PROCEDURE`) | **200**(본문 키 없음) | — | flowStep `PROCEDURE` → **`PROCEDURE_WAITING`** · `flowStepUpdatedDateTimeUtc` 바뀜 · 작업 4개 값 변화 없음 | 미관찰 |
| K3 | 같은 경로 | `{scheduleId, step:"PROCEDURE"}`(지금 `PROCEDURE_WAITING`) | 200 | — | flowStep `PROCEDURE_WAITING` → `PROCEDURE`(기준선 · 원상 복구) | 미관찰 |

- **K2 뒤 작업 상태 실제 값 = `READY`** — SPEC-003 §5.13 즉시 값 `READY` 와 **같다**(이 작업은 집도의 · 담당이 있던 작업. 집도의 없는 작업의 `complete:false` 값은 보지 않았다)
- K1 · K2 뒤 작업 3 은 처음 값(READY)으로 돌아와 따로 정리할 것 없음. K3 로 flowStep 도 처음 값(`PROCEDURE`)

## K5 (OQ-528) — 대기
방 없는 ETCETERA 작업이 붙은 오늘 일정이 없어 멈춤 → 질문 채널로 요청함. 붙으면 그 작업에 `change-tasks-room` → `change-tasks-assignees` → `call-tasks-doctors` → `change-tasks-doctors` → `complete:true` → `complete:false` 를 1회씩 보낸다.

## 판정(지금까지)
- **OQ-529 `complete:false`: 받음** — HTTP 200 · DONE → READY · 완료 시각 지움 · 집도의 · 담당 유지 · 22초 뒤에도 READY
- **OQ-530 flow-step 뒤로 가기(`PROCEDURE` → `PROCEDURE_WAITING`): 받음** — HTTP 200 · flowStep 바뀜 · 작업 값 그대로
- **OQ-528 ETCETERA 호출 · 완료: 미확인(K5 대기)**

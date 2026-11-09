# planner-spec002 결과 보고 — DAY-SPEC-002 시술 현황(1차 · 웹)

## 상태: done (미커밋 · 워크트리 `day-data-architecture-spec` · PR #909)

## 수행 내용

| 파일 | 변경 |
|---|---|
| `products/day/20-spec/spec-002-procedure-board.md` | **신규** — DAY-SPEC-002 · `doc_no: DAY-DOC-6` · draft · version 0.0.1 |
| `products/day/20-spec/spec-000-data-model.md` | `doctor_call.closed_at` 행 추가(U3) · OQ-04-2 에 SPEC-002 OQ-02 링크 · sources 에 결정 원천 · last_updated 11-06 |
| `products/day/20-spec.md` | In Scope 줄 · Out Of Scope 줄(방 옮기기 · 차트 작성 · 앱) · SPEC Bundle · SPEC List · 영역별 읽는 순서 · OQ 링크 · 최종 수정 |
| `products/day/30-work.md` | Spec Coverage 에 DAY-SPEC-002 행(lint 필수 — 브리프 목록 밖이지만 `products/day/` 안) |
| `products/day/log.md` | 2026-11-06 `spec-add, spec-change` 한 줄 |

## 검증

- `python3 scripts/lint-pipeline.py --strict` → **0 error**, `products/day` 경고 0(전체 263 warning 은 다른 제품).

## SPEC-002 절 목록

1. 개요 — 메타 · Business Requirement · 1차 범위(넣음 / 다음 스펙 표)
2. 사용자 경험 — Placement · **화면 구성(E01 ~ E56 별 넣음 / 뺌)** · UX Contract U-1 ~ U-12(판 · 순서 · 시술 줄 · 호출 · 재호출 · 수락 · 시작/종료/되돌리기 · 마취 · 귀가 대기 · 인박스 3탭) · User Scenario S-1 ~ S-7
3. 계약 — 용어 · 상태(방문 단계 · 시술 줄 5상태 · 호출 상태 · 마취) · API 계약(14 경로 · 스냅샷 모양 · Validation) · 케이스 매트릭스(26행) · KOS 읽기 추가분 · KOS 쓰기 동작별 · 실시간 갱신(SSE)
4. 구현 규칙 — Functional Rule 1 ~ 23 · DB · `event_log.type` 제안
5. Open Questions — 사용자 결정 8 · HAR 요청 5 · 기본값 확인 5

## 결정 U1 ~ U12 반영 위치

| # | 반영 |
|---|---|
| U1 | U-7 · 상태(준비중) · 규칙 10 · 케이스 `no_doctor` · S-4 |
| U2 | U-4 · 규칙 5(기본 선택 없음 · 「모든 의사」 \| 원장 한 명) |
| U3 | U-5 · 용어 「유효 호출」 · 호출 상태 「닫힘」 · 규칙 6 · 7 · 케이스 `call_closed` · **SPEC-000 `doctor_call.closed_at`** |
| U4 | U-6 · 규칙 8 · 9(누른 사람 안 남김 — `event_log.actor_staff_id` 도 수락한 의사) · OQ-05(토큰) |
| U5 | 범위 밖 — 1차 범위 표 · 화면 구성 「빼는 것」(E33 버튼 · E47 · E48 · E53 · E54) |
| U6 | U-1(빈 방 안 그림 · E49 뺌) · U-2 · 규칙 18(카드 단위 · 새 카드 뒤 · D&D) |
| U7 | U-1 · 규칙 1(시술 3단계 + 방) |
| U8 | U-9 · 방문 단계 표 · 규칙 17(cc D-33 — 흐리게 맨 뒤 · completed 에 사라짐 · 방 안 비움) |
| U9 | 화면 구성 「수납 필요」 · U-1 · 규칙 4 |
| U10 | U-8 · 마취 상태 · 규칙 15 |
| U11 | 범위 밖 · E55 · E56 읽기 전용 · 규칙 23 |
| U12 | U-10 · 규칙 16(마취 20분 초과 · 호출 5분 · 재호출 · 전부 완료 제외) |
| 추정 금지 7 | 방 순서(KOS order 안 씀 — 카드 순서만) · 방 연결(범위 밖) · 차트 작성자(규칙 23) · 시술 완료 묶음 방(U-12 · OQ-03) · 「의사별」(E10 동작 없음) · 성별 미지정(U-1 · OQ-15) · 지정 원장 메모 읽기(KOS 읽기 표 아래 줄) |

## cc 에서 가져온 규칙 (D 번호 · cc SPEC-003 절)

D-09(KOS 기준 · 반영 대기 칸 덮지 않음) · D-10(현장 KOS 직접 조작 안 함) · D-11(원장 목록) · D-21 · D-22(카드 조건 · 수납 전도 띄움) · D-23(마취) · D-24(호출 · 비어 있는 원장 먼저 · KOS 3단계) · D-26(진행 · 완료는 호출 대상 아님) · D-27(수락 = 유효 호출의 미수락 전부 · 재호출 KOS 요청 = 호출과 같음) · D-28(호출 · 수락 · 마취 · 귀가 대기 되돌리기 없음) · D-29(지금은 스테이션에서 시작 · 종료) · D-30(시작 조건) · D-31([종료]는 시작한 것만) · D-32(첫 시작 = 시술 진행 · 시작 시각 DAY 만) · D-33(귀가 대기 · 방 안 비움 · 흐리게 맨 뒤) · OQ-501(지정 원장은 KOS 요청에 안 실림).
cc SPEC-003: §4.3(덮어쓰기) · §4.4(op 순서 · superseded · 재전송 · 실패) · §5.1(규칙 하나 · 「방 배정」) · §5.7 · §5.12(카드 순서 · 통째 바꾸기 · 마지막 쓰기) · §5.13(시작 · 완료 되돌리기) · §7.2(스냅샷 · 규칙 서버 계산) · §7.3(409 코드 · 검사 순서) · §7.5(SSE) · §8(KOS 반영 · 같은 단계 규칙). cc `rules.py` `is_room_task` · `start_block` · `payment_required` · `sync.py` `_card_room_task`.

**시안 / 결정이 cc 와 다른 곳**: 호출 대상 = 준비중만(시안 E41 · E42 — cc D-25 는 호출된 시술도 다시 고를 수 있었음) · 재호출은 기존 호출을 닫음(U3) · 확인 필요에서 「전부 완료」 뺌(U12) · 되돌리기는 더보기 메뉴 + 확인 창(시안 E50 — cc 토스트 [되돌리기] 없음) · 인박스 3탭(시안 — cc 오른쪽 현황/호출/고객).

**브리프 범위 목록에 없지만 넣은 것**: 「시작 취소」 · 「완료 취소」(시안 E45 · E50 · cc §5.13 — 결정 없음 → cc 로직). 빼려면 알려 달라.

## OQ — 사용자 결정 필요 (선택지 + 추천)

| OQ | 질문 | 추천 |
|---|---|---|
| OQ-01 | API 경로 · 웹 갱신 방식 — ① JSON `/api/board*` 등 웹 · 앱 공용 + 웹은 SSE 신호로 `GET /board` 조각 다시 받기 ② 웹은 화면 라우트가 HTML 조각 · JSON 은 앱 전용 | ① (SPEC-001 선례 · 규칙 한 곳) |
| OQ-02 | `permission_key` — ① `board`(view/edit) + `board.accept` ② `board` 하나 ③ 동작마다 | ① |
| OQ-03 | 시술 완료 탭 방별 묶음 — ① 묶지 않음 ② `visit.room_id` 로 ③ 새 칸 | ② (HAR 확인 뒤) — 1차 SPEC 은 ① 로 둠 |
| OQ-04 | 재호출 대상(① 모든 의사 \| 한 명 ② 모든 의사만) · 5분 기준(ⓐ 열린 호출부터 ⓑ 처음 호출부터) | ① + ⓐ |
| OQ-05 | 수락 KOS 쓰기 토큰 — ① 수락한 의사 ② 누른 사람(outbox 칸 필요) ③ 시스템 계정 | ① (U4 · SPEC-001 규칙 4 둘 다 지킴 · 대리 수락은 의사 로그인 전까지 반영 중) |
| OQ-06 | KOS 담당자(`assigneeIds`) — ① 시스템 계정(cc) ② 누른 직원 | ① |
| OQ-07 | 「반영 중 · 실패」 표시 — ① 스냅샷 `reflecting` + 디자인 · 실패 토스트 ② 안 그림(cc 웹) | ① (DAY 데이터 규칙) |
| OQ-11 | 「마취용」 계정 빼기 — ① 연결 설정에 뺄 id 목록 ② 안 뺌 ③ 이름 | ① — 설정 자리(모델 영향 가능) 결정 필요 |

## OQ — HAR 요청 (사용자가 HAR 를 넣어야 「확인됨」)

OQ-08 [귀가 대기] `cancel-flow-tasks` · `change-flow-step(PROCEDURE_DONE)` · OQ-09 `WAITING` 작업 재호출 · OQ-10 되돌리기 값(`PROCEDURE_WAITING` · `complete:false`) · OQ-12 시술 작업 있는 일정 응답(`procedureConfiguration` 안쪽 · `doctors[]` 등 안쪽) · OQ-13 상담 배열 안쪽.

**HAR 로 확인된 KOS 쓰기**(경로 · 요청 칸 이름만 봄 · 값 안 옮김): `change-tasks-room {scheduleId, sequences, roomId}` · `change-tasks-assignees {scheduleId, sequences, assigneeIds}` · `call-tasks-doctors {scheduleId, sequences}` · `change-tasks-doctors {scheduleId, sequences, doctorIds}` · `change-tasks-complete {scheduleId, sequences, complete=true}` · 내부 `schedule/v1/commands/change-flow-step {id, step=PROCEDURE}`. ※ cc 는 flow-step 을 공개 API(`scheduleId`)로 보냈지만 HAR 는 내부(`id`)라 SPEC 은 내부 경로로 적었다.

## SPEC-000 변경분

- §3 05 `doctor_call` — `closed_at` timestamptz NULL 「닫힌 시각 — 재호출로 새 호출이 이어받으면 기존 호출을 닫는다 · null = 열림」(U3). `reassigned_from_call_id` 그대로.
- §6 OQ-04-2 — 「시술 현황 몫 제안은 DAY-SPEC-002 §5 OQ-02」 덧붙임(결정 아님).
- frontmatter sources 에 `screen/procedure-board-decisions.md`.
- 그 밖 모델 변경 없음. OQ-05 를 ② 로 정하면 `external_outbox` 에 보낼 세션 칸이, OQ-11 을 ① 로 정하면 뺄 계정 목록 자리가 필요하다.

## 미결 · 주의점

- **#226 과 맞출 것**: `visit.room_id` 를 「방이 붙은 작업 중 `roomAssignedDateTimeUtc` 가장 늦은 것」(cc 규칙)으로 적었다 — #226 구현이 다르면 맞춰야 한다(리포트 A1 은 room_id 가 채워진다는 것만 보였다).
- 시술 줄 `state` 이름(`ready_wait` · `called` · `accepted` · `doing` · `done`) · 409 코드 DAY 이름(`task_*`) · `event_log.type` 값은 이 SPEC 이 붙인 이름이다(cc 이름을 DAY 용어로).
- 카드 순서 「먼저 생긴 순」을 「시술 대기가 된 시각과 입실 중 늦은 것」으로 계산한다(U6 문장 → 기존 칸 계산 · cc 는 입실순).
- 수락 모드에서 지정 호출도 다른 원장이 받을 수 있게 했다(시안 E51 수락 창 = 원장 전체). cc 는 지정 원장만.

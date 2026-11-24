# [backend · 실물 확인 4] KOS 데모 지점 — 상담사 지정(상담 기록) · 시술만 진행 관리실 배정 연쇄

**앞 판 먼저 읽기**: 같은 폴더 `be-probe-1-instructions.md`(규칙 · 금지 · 보고 — 전부 그대로) · `be-probe-2-report.md` · `be-probe-3-report.md`. 스크립트 `/private/tmp/day-probe-4/`(앞 판 lib 재사용).

**레포 수정 · 커밋 금지 · 데모 지점 확인 통과 뒤에만 쓴다 · `~/.config/day/` 금지 · 로컬 스택 · DB · docker 금지 · 값 · 토큰 · 개인정보 출력 금지.** 고객 = 시험 고객 `6b051a9e…` 만 · 오늘 예약을 새로 만들어 쓰고 끝나면 귀가 완료로 정리.

## 1. 왜 (코디 `_RESUME.md` §2 새 결정)

- 상담사 = **상담 기록의 상담사**. KOS 화면 「상담사 지정」 = `consultation/v1/commands/create-consultation`(HAR `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/reference/2026-11-24-reservation-detail/상담사 지정.har` #8 — 본문 `{consultationId(새 uuid), visitorId, consultationStartedDateTimeUtc, scheduleId, content{text:""}, counselorIds[]}` · 응답 `{}` · 다음 `consultation/v1/queries/get-consultations-by-visitor-id`)
- 시술만 진행 [시술 대기] = 「방 배정」 작업 + 방 지정 + 시술권 작업들(방 지정) + 오더 메모 → `PROCEDURE_WAITING`

## 2. 시험

**예약 P (상담 경로)**
1. 오늘 예약 → 접수 → 「방 배정」 + 방 지정 → `CONSULTATION_WAITING`(2판 그대로)
2. **상담사 지정** `create-consultation`(HAR #8 모양 · `consultationStartedDateTimeUtc` 는 HAR 처럼 그 일정 시작 시각) → 다시 읽기: 일정 상세 `flowStep` 이 바뀌나(그대로 `CONSULTATION_WAITING` 인가 · `CONSULTATION` 으로 가나) · 상세 `consultations[]` / `consultation` 칸 · `get-consultations-by-visitor-id` 의 그 기록 · DAY 동기화가 읽는 자리(`backend/day/emr/kos/mapper.py` 상담 매핑 · `:496` 근처)에 상담사가 보이나
3. **상담사 바꾸기**(같은 예약 · 다른 상담 직원): HAR 에 고치기 명령이 없다. ⓐ `consultation/v1/commands/` 아래 고치기 명령을 KOS openapi · DAY 코드 · cc 코드에서 찾아(이름 · 본문) 있으면 그것으로 · ⓑ 없으면 같은 `consultationId` 로 `create-consultation` 을 다시 보내 보기(400 이면 기록) · ⓒ 새 `consultationId` 로 하나 더 만들면 기록이 둘이 되는지. 각각 다시 읽은 상담 기록 수 · 상담사
4. 귀가 처리(2판 방식 — 「방 배정」 CANCEL → `COMPLETED`) → 상담 기록이 남는 모양

**예약 Q (시술만 진행)**
5. 오늘 예약 → 접수 → **「방 배정」 작업**(ETCETERA) → **방 지정** → **시술권 작업**(3판 본문 · 남은 `AVAILABLE` 시술권 · `round` = D48 규칙) → **그 시술 작업에 같은 방 지정**(`change-tasks-room` · NOT_STARTED → READY 되나) → **오더 메모** → `PROCEDURE_WAITING` → 다시 읽어 작업 둘(방 배정 · 시술)의 방 · 상태 · `flowStep`
6. 순서 바꿔 보기는 하지 마라(위 순서 한 번). 끝나면 작업 CANCEL → `COMPLETED` 로 정리(시술권 AVAILABLE 로 돌아오는지)

## 3. 리포트

`/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/orchestration/work/day-reservation2/be-probe-4-report.md` — 맨 위 표(시험 × 경로 · 응답 · O / X · 비고) → 결론: ⓐ 상담사 지정이 단계를 바꾸나 ⓑ 상담사 바꾸기 길 ⓒ 차티 [상담 시작]과 겹칠 위험(기록이 둘 생기는지 — 관찰한 만큼만) ⓓ 시술만 진행 연쇄 결과 → 「DAY `writes.py` 에 열 때 필요한 것」(후보).

## 4. 완료 보고 — 1 과 같은 두 명령(subject 「backend 완료: KOS 데모 실물 확인 4」) · task-id · dispatch-id 는 이번 dispatch 값. 막히면 `[질문] backend:` 로 코디 터미널에.

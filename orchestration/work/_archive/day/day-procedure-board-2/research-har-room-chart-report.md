# 조사 리포트 — HAR 분석: 방 이동 · 차트 작성 (2026-11-10)

조사자: day researcher(read-only). 원천:
- HAR(KOS 데모 지점 · 사용자 2026-11-10): `reference/2026-11-09-cc-day/har/방이동.har`(16항목) · `차트작성.har`(57) · `차트작성2.har`(9). 참고로 같은 폴더의 다른 HAR 3개를 일정 id 로 교차 검색했다.
- 기획안 `cc-기획안-시술현황.md` §2-1(:289-343) · §4-2(:562-634) · §6-1(:666-731) · 용어(:17-45) · `cc-개요.md` 「KOS 연동 원칙」(:544-558) · 「KOS 읽기 · 쓰기」(:560-590).
- 사용자 결정 `_RESUME.md` §2 :61 「차트(④) 사용자 확인 · 결정」.
- DAY 코드(PR #238 브랜치) · SPEC-002.

**값은 옮기지 않았다** — 칸 이름 · 타입 · 건수 · 같음/다름 비교만. id 는 `id24`(24자리 hex) · 일정 id 는 `str(36)`, 글은 `str(글자 수)`로 적는다.
항목 번호 `#n` = HAR `log.entries[n]`(0부터). 시각은 HAR `startedDateTime`(UTC).

---

## 1. HAR 마다 쓰기 요청(commands) 순서

### 1-1. `방이동.har` — 화면 = KOS 웹 시술 현황판(`/<tenant>/reservation/procedure` · RUM view 경로)

| # | 시각 | 요청 | 요청 칸(타입) | 응답 |
|---|---|---|---|---|
| #2 · #4 | 08:32:37 | `account/v2/queries/get-accounts-last-update-date-time-utc` · `get-accounts` | — · `{}` | 200 · 계정 81건(`id` · `roleId` · `roleName` · `role.roleTags[int]` …) |
| #5 | 08:32:37 | `schedule/zone/room/v1/queries/get-rooms` | `zoneId: id24` | 200 · `data[]` 28건 · 칸 = **`id` · `zoneId` · `title` · `order` 넷뿐** |
| **#8** | 08:32:43 | **`schedule/flow/v1/commands/change-tasks-room`** | `scheduleId: str(36)` · `sequences: [int]`(1개 · 값 1) · `roomId: id24` | 200 · `{}` |
| #12 | 08:32:53 | `get-rooms` | `zoneId` | 200 · #5 와 같은 28건 |
| **#14** | 08:32:58 | **`change-tasks-room`** | 위와 같은 칸 · `sequences` 1개(값 1) | 200 · `{}` |

- #8 과 #14 는 **서로 다른 일정(고객 둘)** 이고, 둘 다 `sequence 1` · **같은 `roomId`** 로 옮겼다. 둘 다 200이다.
- 이 HAR 에는 일정 조회(`get-schedules` 등)가 **없다**. 그래서 옮기기 전과 뒤의 작업 값(어느 작업이 seq 1 인지 · `roomAssignedDateTimeUtc` 가 바뀌는지)은 HAR 로 **확인 안 됨**.
- `#14` 의 일정은 `차트작성.har` 의 쓰기 대상 일정과 같다(id 비교 True) — 같은 고객으로 이어서 한 시험이다.

### 1-2. `차트작성.har` — 화면 = KOS 웹 예약 > 고객 차트의 시술 작업 표(Amplitude `entryPoint = VisitorChartFlowTaskTable` · 경로 `/reservation/schedule/`)

| # | 시각 | 요청 | 요청 칸(타입) | 응답 |
|---|---|---|---|---|
| **#18** | 08:33:42 | **`schedule/flow/v1/commands/change-tasks-doctors`** | `scheduleId` · `sequences: [int]`(1개) · `doctorIds: [id24]`(1개) | 200 `{}` |
| (#25) | 08:33:43 | Amplitude 이벤트 `requested.changed_assignee_doctor` | — | — |
| **#29** | 08:33:48 | **`schedule/flow/v1/commands/change-tasks-assignees`** | `scheduleId` · `sequences`(1개) · `assigneeIds: [id24]`(1개) | 200 `{}` |
| **#39** | 08:33:56 | **`schedule/v1/commands/change-flow-tasks-assignee-memo`** | `scheduleId` · `sequences: [int]`(1개) · **`assigneeMemo: str`**(7자) | 200 `{}` |
| **#48** | 08:34:00 | **`schedule/v1/commands/change-flow-tasks-doctor-memo`** | `scheduleId` · `sequences`(1개) · **`doctorMemo: str`**(3자) | 200 `{}` |
| (#55) | 08:34:01 | Amplitude `requested.changed_doctor_memo` | — | — |

- 네 쓰기 모두 **같은 일정 · 같은 `sequence 1`** 이다. `doctorIds` 와 `assigneeIds` 는 서로 다른 직원이다.
- 앞뒤 조회는 `get-visitor`(고객 · `lastVisitedDateTimeUtc` 등) · `get-reservation-group` · `get-purchase-summaries` · `get-visitor-images` · `get-payment-settings` · `get-currency-settings` 뿐이다. **일정 · 작업 조회가 없어** 쓴 뒤의 메모 · 담당자 · 집도의 값은 HAR 로 **확인 안 됨**.
- 경로 차이: 메모 두 개는 `schedule/v1/commands/…`, 담당자 · 집도의 · 방은 `schedule/flow/v1/commands/…` 다.

### 1-3. `차트작성2.har` — 화면 = KOS 웹 시술 현황판(Amplitude `multi_select.flow_card+procedure_dashboard`(type DRAG) → `requested.changed_doctor_memo` · `entryPoint = ProcedureDashboardFlowCardFloatingActionBar`)

| # | 시각 | 요청 | 요청 칸 | 응답 |
|---|---|---|---|---|
| #0 · #1 | 08:34:1x | `role/v2/queries/get-roles` · `get-rooms` | — | 200 |
| **#5** | 08:34:19 | **`change-flow-tasks-assignee-memo`** | `scheduleId` · `sequences`(1개) · `assigneeMemo`(13자) | 200 `{}` |
| **#7** | 08:34:22 | **`change-flow-tasks-doctor-memo`** | `scheduleId` · `sequences`(1개) · `doctorMemo`(6자) | 200 `{}` |

- 대상 = `차트작성.har` 와 **같은 일정 · 같은 sequence 1**.
- 이번 글은 앞 HAR 글로 **시작한다**(`startswith` True · 담당자 · 원장 메모 둘 다 · 줄바꿈 없음). 이 HAR 에서는 담당자 · 집도의 쓰기 없이 메모만 썼다.

### 1-4. 모든 쓰기 공통
- 본문에 **작성자 칸이 없다**(`scheduleId` · `sequences` · 값 하나뿐). 요청 헤더에도 작성자 칸이 없고, HAR 에는 `authorization` 헤더 자체가 빠져 있다(내보내기 때 지워짐 · 이전 HAR 들과 같음). → KOS 에 남는 작성자는 있다면 **토큰 주인**이다. 그 값을 돌려주는 조회는 HAR 에 없다 — **확인 안 됨**.
- 응답은 모두 `{}`(200)다. 쓴 결과를 응답이 돌려주지 않는다.

---

## 2. 방 이동

### 2-1. 무엇을 바꾸나

| 질문 | 답 | 근거 |
|---|---|---|
| 요청이 바꾸는 단위 | **작업(sequence) 단위의 방**(`change-tasks-room {scheduleId, sequences[], roomId}`). 방문 칸을 바꾸는 요청은 없다 | 방이동 #8 · #14 |
| KOS 웹이 고객 한 명을 옮길 때 고른 작업 | 두 번 다 `sequences=[1]` 하나뿐 — 고객의 다른 작업도 같이 옮겼는지는 아니다(1개). 그 seq 1 이 시술 작업인지 「방 배정」(기타 작업)인지는 **확인 안 됨**(일정 조회 없음) | 방이동 #8 · #14 |
| KOS 의 방 칸은 어디 있나 | **작업마다** `room{id, zoneId, title, order}` + `roomAssignedDateTimeUtc`. 방문 칸에는 방이 없다(`visitorLocation` = `zoneId` 뿐) | DAY 응답 고정본 `tests/day/emr/fixtures/kos_schedules.json`(작업 키 21개) · `day/emr/kos/mapper.py:483-508` |
| DAY 카드 방이 따라오나(읽기) | 따라온다 — DAY `visit.room_id` = 방이 붙은 작업 중 `roomAssignedDateTimeUtc` 가 가장 늦은 작업의 방. 그래서 KOS 웹에서 한 작업을 다른 방으로 옮기면 다음 조회에서 DAY 카드 방이 그 방이 된다. 단, 옮긴 작업의 `roomAssignedDateTimeUtc` 가 새로 찍힌다는 전제다(**HAR 로 확인 안 됨**) | `mapper.py:423-441` `card_room` · SPEC-002 데이터 표(`visit.room_id` 행) |
| 시술 대기 / 진행 중 차이 | HAR 에 일정 단계 · 작업 상태 조회가 없어 **확인 안 됨**. 두 요청 본문은 같은 모양이다 | 방이동 전체 |
| 침대 · 정원 | **없다** — `get-rooms` 칸은 `id` · `zoneId` · `title` · `order` 넷뿐(28건 모두). 두 고객을 **같은 방**으로 옮긴 두 요청이 모두 200이라 KOS 가 방 정원을 막지 않는다(적어도 이 데모 · 이 방) | 방이동 #5 · #8 · #14 |
| 들어온 · 나간 시각 기록 조회 | **없다**. KOS 가 주는 것은 작업마다 지금 방 + `roomAssignedDateTimeUtc`(마지막 배정 시각 하나)뿐이다. 이력 · 나간 시각을 주는 조회는 HAR 에도 DAY 고정본에도 없다 | 방이동 전체 · 고정본 작업 키 |
| 점유(hold) 개념 | **없다** — 요청 · 응답 어디에도 없다 | 방이동 전체 |

### 2-2. 기획 2-1 · 6-1 대조 — KOS 로 되는 것 / DAY 가 가져야 하는 것 / 안 되는 것

| 기획 항목 | KOS 로 되는 것 | DAY 자체로 가져야 하는 것 | 안 되는 것 · 확인 안 됨 |
|---|---|---|---|
| 2-1 「다른 관리실로 이동」(원래 방 비움 · 새 방) | `change-tasks-room` 로 작업 방을 새 방으로(HAR 확인). DAY 는 같은 경로를 이미 쓴다(호출 1단계 `assign_room` · `emr/kos/writes.py:38` · `:85-90`) | 어느 작업을 옮길지(방 배정 작업만 · 안 끝난 시술 전부 · 전부) — KOS 웹은 1개만 옮겼다 | 시술 진행 중 작업도 옮겨지는지 · 옮긴 뒤 `roomAssignedDateTimeUtc` 가 바뀌는지 — 확인 안 됨 |
| 2-1 「점유 이동」(원래 방을 「점유 중」으로 잡아 둠) | 없음 — KOS 에 점유 칸이 없다 | **점유 상태 전부**(원래 방 · 누가 잡았나 · 풀리는 때) · 원래 방을 다른 접수 · 이동에서 못 고르게 하는 것 | KOS 웹 · KOS 접수 화면에서는 점유가 보이지 않는다 → KOS 에서 그 방에 다른 고객을 넣을 수 있다(막을 길 없음) |
| 2-1 「원래 관리실로 복귀」 | `change-tasks-room` 로 다시 원래 방으로(같은 요청) | 원래 방이 어디였는지(점유 기록) | — |
| 2-1 정책 1 · 2 「빈 관리실 = 고객 수 < 침대 수 · 점유 아님」 · 「n/m」 | 방 목록(`get-rooms`)만 | **침대 수**(기획 「관리실 정보 = 관리실과 침대 수」 · CC-23) · 사용을 켠 관리실 · 고객 수 셈 | KOS 가 정원을 막지 않으므로 KOS 웹 쪽 이동은 침대 수를 넘을 수 있다 |
| 2-1 예외 1 「마지막 자리 동시 이동 → 먼저 저장된 것」 | — | 병원 · 방 단위 잠금 · 자리 셈 | — |
| 6-1 관리실 기록(체류 구간 · 들어온 · 나간 시각 · 「체류 중」) | 지금 방 + 마지막 배정 시각만 | **체류 구간 기록 전부**(방 · 들어온 · 나간 · 고객 · 방문) — 접수 배정 · 이동 · 복귀 · 귀가 때 남김 | KOS 웹에서 한 이동은 DAY 조회로 「지금 방이 바뀌었다」로만 보인다 → 나간 · 들어온 시각을 조회 시각(최대 10초 늦음)이나 `roomAssignedDateTimeUtc` 로 추정해야 한다(추정 금지 규칙과 부딪침 · 정할 것) |
| 6-1 그 관리실에서 시작한 시술 줄(시작 · 종료 · 담당 원장 · 간호관리 담당자) | 작업 방 · 담당자 · 집도의 · 완료 시각(읽기) | 시작 시각(DAY `started_at` — KOS 에 없음) · 「그 관리실에 있는 동안 시작」 판정(체류 구간과 시작 시각 대조) | — |
| 6-1 날짜 이동(지난 날) | — | DAY 가 그날 남긴 체류 기록 | DAY 를 켜기 전 날짜 · DAY 가 조회하지 않은 날은 없다 |

---

## 3. 차트 작성

### 3-1. 요청이 보여 주는 것

| 질문 | 답 | 근거 |
|---|---|---|
| 간호 차트 쓰기 | `change-flow-tasks-assignee-memo {scheduleId, sequences[], assigneeMemo: str}` | 차트작성 #39 · 차트작성2 #5 |
| 의사 차트 쓰기 | `change-flow-tasks-doctor-memo {scheduleId, sequences[], doctorMemo: str}` | 차트작성 #48 · 차트작성2 #7 |
| 칸 모양 | 작업마다 **글 칸 하나**(`assigneeMemo` 문자열 · `doctorMemo` 문자열). 사람별 칸 · 여러 칸 구조 없음 | 위 · 고정본 작업 키(`assigneeMemo` · `doctorMemo`) |
| 담당자(간호관리) | 메모와 **따로** `change-tasks-assignees {assigneeIds: [id]}` | 차트작성 #29 |
| 집도의(의사 차트) | 메모와 **따로** `change-tasks-doctors {doctorIds: [id]}` — 덮어쓰기(교체)는 `집도의변경.har` · `삭제후의사호출.har` 로 이미 확인(SPEC-002 KOS 쓰기 표 · OQ-31 닫음) | 차트작성 #18 |
| 작성자 | 본문에 없다 — 토큰 주인(DAY 규칙 24 = 누른 사람). KOS 가 작성자 · 시각을 저장 · 반환하는지는 **확인 안 됨**(조회 없음 · DAY 고정본 작업 키에도 작성자 · 메모 시각 칸이 없다) | 1-4 · 고정본 |
| 담당자 / 집도의 필수가 요청에서 드러나나 | 드러나지 않는다 — 메모 요청에 담당자 칸이 없다. 차트작성2 에서는 담당자 · 집도의 쓰기 없이 메모만 200(단, 그 작업에는 앞 HAR 에서 이미 담당자 · 집도의가 들어가 있었다). 담당자가 **빈** 작업에 메모를 쓰면 KOS 가 거절하는지는 **확인 안 됨** | 차트작성2 #5 · #7 |
| 여러 시술에 한 번에(「전체 시술에 내용 적용」) | 칸 `sequences` 가 **배열**이라 여러 작업을 한 요청에 실을 수는 있어 보인다. 그러나 HAR 은 모두 1개다 — 여러 개를 보내면 되는지는 **확인 안 됨** | 모든 쓰기 |
| 고쳐 쓰기 | **통째 바꾸기(덮어쓰기)** — 두 번째 쓰기 글이 첫 글로 시작했다 = 화면이 지금 글 전체를 보내고, KOS 에 덧붙이기 요청은 없다 | 차트작성 #39 · #48 ↔ 차트작성2 #5 · #7 |
| 이력 | 이력을 돌려주는 조회가 없다. KOS 가 이전 값을 남기는지는 **확인 안 됨** | — |
| 지난 방문 차트 읽기 | HAR 에 없다. `get-visitor` 는 `lastVisitedDateTimeUtc` 만 준다. 지난 일정(작업 메모)을 읽는 조회는 **확인 안 됨** | 차트작성 #2 · #10 |
| `assigneeIds` 개수 | 1개만 보냄. 배열이라 여러 명이 될 수는 있으나, 여러 명을 보낼 때 덮어쓰는지 · 더하는지는 **확인 안 됨**(`change-tasks-doctors` 는 덮어쓰기로 확인됨 — 같은 모양이라 같을 가능성이 높지만 추정) | 차트작성 #29 |

### 3-2. 기획 4-2 · 사용자 결정 대조

| 기획 4-2 / 결정 | KOS 요청으로 되는 것 | DAY 가 가져야 하는 것 | 부딪힘 · 확인 안 됨 |
|---|---|---|---|
| 의사 차트 = 줄마다 담당자 + 글 칸 하나 | `doctorMemo` 글 하나 + `doctors[]` | — | — |
| 간호관리차트 = **직원마다** 이름 + 글 칸(「작성자 추가」로 여러 명) | 글 칸 **하나**(`assigneeMemo`) + `assignees[]` | — | **사용자 결정(11-10) 「작성자 1명」**이 기획(여러 명)을 바꿨다 — KOS 구조(글 하나)와 결정이 맞는다. 기획 「작성자 추가」 · 「칸 지우기」는 안 쓰는 방향(정할 것 ①) |
| 결정: 간호관리차트 담당자 필수 · 의사차트 집도의 필수 | KOS 는 막지 않는 것으로 보인다(요청에 연결 없음 · 확인 안 됨) | DAY 가 저장 전에 검사 | — |
| 결정: 담당자 드롭다운 = 간호사 · 관리팀 / 원장 | `assigneeIds` · `doctorIds` = KOS 계정 id | DAY 직원 ↔ KOS id(`external_ref`) · 직무 태그로 목록 | **DAY 는 지금 호출 2단계에서 `assigneeIds` = 병원 시스템 계정으로 덮는다**(SPEC-002 규칙 25 · `:735`). 차트 담당자를 KOS `assignees` 에 쓰면, 그 뒤 호출 · 재호출 때 시스템 계정으로 다시 덮인다(정할 것 ②) |
| 「전체 시술에 내용 적용」(글만 복제 · 이미 글 있는 줄은 빼고 · 확인 창에 수) | `sequences[]` 배열 — 여러 개가 되는지 확인 안 됨. 줄마다 따로 보내면 된다 | 「이미 글 있는 줄」 판정 · 확인 창 | — |
| 정책 12 저장 단위 = 줄 · 저장 계정 · 저장 시각 · 담당자 남김 | 메모 · 담당자 · 집도의 3요청을 따로(원자 아님) | **저장 계정 · 시각**(KOS 가 돌려주지 않음) | 3요청 중 하나만 실패하면 KOS 는 반쯤 바뀐다 — outbox 순서 · 실패 처리(정할 것 ⑤) |
| 정책 15 고치면 이전 값 · 고친 값 · 계정 · 시각을 남기고 지우지 않음 · 정책 16 의사 차트 10년 · 간호관리 5년 | 덮어쓰기만 · 이력 조회 없음 | **차트 이력 표 전부** · 보존 기간 | KOS 원본으로는 이력을 지킬 수 없다 |
| 예외 1 동시 저장 — 먼저 저장된 줄은 덮지 않음 | 없음(KOS 는 마지막 쓰기가 이긴다) | DAY 판(version) 검사 | KOS 웹에서 동시에 쓰면 DAY 는 다음 조회에서 덮인 값을 받는다(정할 것 ③) |
| 정책 9 처음 열면 예시 글만 · 오더 메모 · 마취 · 관리실 기록을 미리 채우지 않음 | — | 화면 | — |
| 지난 방문 기록(최근부터 · 못 고침) | 확인 안 됨 | DAY 가 그 방문을 조회해 둔 것만 있다 | DAY 를 켜기 전 방문 · KOS 시술 이력(CC-00-1) — 조회 경로 확인 안 됨 |
| cc-개요 「KOS 읽기 · 쓰기」 :589 「의사 차트 · 간호관리차트 = **CC에 저장**」 · K-9 「시술 차팅은 CC가 원본이고 KOS 칸은 CC가 쓰는 사본」 | HAR 로 KOS 칸 쓰기는 된다 | 원본 · 이력은 DAY | 두 줄이 「KOS 에 쓰나 안 쓰나」에서 서로 다르게 읽힌다(:589 「CC에 저장」 vs K-9 「KOS 칸은 사본」) — 정할 것 ④ |
| 결정: 로그인 직무별 먼저 보이는 탭 | — | DAY 직무 태그(`doctor` 등 · SPEC-002 규칙 19) | — |

---

## 4. DAY 지금 코드 · 스펙과의 차이

| 영역 | 이미 있는 것 | 새로 만들어야 하는 것 |
|---|---|---|
| 방 | 방 목록 동기화(`Room` · `get-rooms`) · 카드 방 = 가장 늦게 배정된 작업의 방(`mapper.py:423-441`) · KOS `change-tasks-room` 쓰기(호출 1단계 · `writes.py:85-90` · 확인 조건 `room_external_id`) · 「방 배정」 작업 판정 · [귀가 대기] 때 취소(SPEC-002 규칙 3 · 17) | 방 이동 라우트 · 화면(SPEC-002 는 E33 방 이름 버튼 · E53 · E54 를 「뺌 — U5」로 둠 `spec-002:83` · `:141`) · 점유 상태 · 침대 수(관리실 정보) · 체류 구간 기록(6-1) · 빈 관리실 계산 · 동시 이동 잠금 · KOS 에 몇 개 작업을 옮길지 규칙 |
| 차트 | 차트 모달 읽기 전용 · 글 = `visit_task.assignee_note` · `doctor_note`(KOS `assigneeMemo` · `doctorMemo` 를 조회로 덮어씀 · `mapper.py:505-506` · `sync.py:1198-1199`) · 차트 라우트(웹 조각 · `/api` 짝) · 규칙 23 「읽기만」(`spec-002:731`) · 「차트 작성 · 작성자 · 시각(U11) — 1차는 KOS 메모 읽기만」(`spec-002:84`) | 쓰기 라우트 · KOS op 종류 3개(`assignee_memo` · `doctor_memo` · `assign_assignee` 를 담당자로 · 집도의는 기존 `change_doctor` 재사용 가능) · 확인 조건(메모 글 같음 — 확인 칸 새로) · 동기화가 반영 중 메모를 덮지 않게(guard) · **차트 이력 표**(작성자 · 시각 · 이전 값) · 탭 · 표 디자인 · 직무별 첫 탭 · 담당자 드롭다운(간호사 · 관리팀 / 원장 — 직무 태그) · 필수 검사 |
| 담당자 | 호출 때 KOS `assignees` = 시스템 계정(규칙 25) · 동기화가 `assignees[]` 를 받음(`mapper.py` `assignee_external_ids`) | 「간호관리 담당자」를 어디에 둘지(KOS `assignees` 를 쓰면 규칙 25 와 충돌) |

---

## 5. 정할 것 (결정하지 않음)

1. **간호관리차트 작성자 · 담당자 수** — 사용자 결정 「작성자 1명」(11-10)이 기획 4-2 「작성자 추가(여러 명) · 칸 지우기」를 바꾸는 것으로 볼지. KOS 는 글 칸 하나 · `assignees[]` 배열이다.
2. **간호관리 담당자를 KOS `assignees` 에 쓸지** — 쓰면 DAY 호출 · 재호출의 `change-tasks-assignees = 시스템 계정`(규칙 25)이 차트 담당자를 덮는다. ⓐ 호출 때 담당자 쓰기를 그만둠, ⓑ 차트 담당자는 DAY 에만 둠, ⓒ 차트 저장 때 덮어쓰고 호출 때도 덮음(마지막이 이김) 가운데 하나.
3. **차트 원본 · 동시 저장** — DAY 원본 + KOS 사본으로 쓴다면, KOS 웹에서 고친 메모가 다음 조회에서 DAY 사본을 덮는 것을 받아들일지(지금 동기화 동작). 받지 않는다면 DAY 이력에 어떻게 남길지(KOS 쪽 작성자 · 시각을 모름).
4. **KOS 에 차트를 쓸지 자체** — `cc-개요` :589 「CC에 저장」 vs K-9 「KOS 칸은 CC가 쓰는 사본」. HAR 로 쓰기 경로는 확인됐다.
5. **차트 저장 = KOS 요청 2~3개**(담당자/집도의 + 메모) — 순서(담당자 먼저?)와 일부 실패 때 화면 표시(지금 규칙 22 · 실패 토스트만).
6. **이력 · 보존**(정책 15 · 16) — DAY 에 차트 이력 표를 둘지 · 보존 기간(10년 · 5년)을 DAY 가 책임질지 · 지우기 금지.
7. **지난 방문 차트** — DAY 가 가진 방문만 보일지, KOS 지난 일정을 따로 읽을지(조회 경로 확인 안 됨 · HAR 필요).
8. **「전체 시술에 내용 적용」** — 이번에 넣을지 · 넣으면 KOS 에 `sequences` 여러 개 한 요청인지 줄마다인지(여러 개 확인 안 됨 → 데모 실물).
9. **방 이동 때 KOS 에 옮길 작업 범위** — KOS 웹은 작업 1개(seq 1)만 옮겼다. DAY 는 ⓐ 「방 배정」 작업만, ⓑ 끝나지 않은 작업 전부, ⓒ 전부 가운데 무엇. (DAY 카드 방은 「가장 늦게 배정된 작업의 방」이라 하나만 옮겨도 카드는 따라온다.)
10. **점유 이동** — DAY 에만 있는 상태로 넣을지. KOS 웹 · KOS 접수에서는 점유가 안 보여 그 방에 다른 고객이 들어갈 수 있다 — 받아들일지.
11. **침대 수 · 사용하는 관리실** — DAY 에 관리실 정보(CC-23)를 새로 둘지 · 1차 기본값(방마다 1 등)을 무엇으로 할지. KOS 는 정원을 막지 않는다.
12. **관리실 기록(6-1)의 시각 출처** — DAY 에서 한 이동 · 복귀 · 귀가는 DAY 가 시각을 안다. KOS 웹에서 한 이동은 조회로만 알게 된다 → `roomAssignedDateTimeUtc` 를 들어온 시각으로 쓸지 · 조회 시각을 쓸지 · 비울지(추정 금지).
13. **시술 진행 중 방 이동** — 진행 중 작업도 옮길지 · KOS 가 받는지(확인 안 됨 → 데모 실물).
14. **방 이동 · 차트 화면 자리** — SPEC-002 가 「뺌(U5)」 · 「읽기만(U11)」으로 둔 결정(사용자 2026-11-06 원천)을 이번 작업에서 연다는 것을 스펙에 적기(결정 원천 갱신).

## 6. 확인 안 됨 (데모 실물 · HAR 가 더 필요)

- 방 이동 seq 1 이 어떤 작업인지(일정 조회가 든 HAR) · 옮긴 뒤 `roomAssignedDateTimeUtc` 가 바뀌는지 · 진행 중 작업 이동.
- 담당자가 빈 작업에 메모 쓰기 · `assigneeIds` 여러 명 · `sequences` 여러 개 한 번에.
- KOS 가 메모 작성자 · 시각 · 이력을 남기거나 돌려주는지.
- 지난 방문(지난 일정) 메모를 읽는 조회.

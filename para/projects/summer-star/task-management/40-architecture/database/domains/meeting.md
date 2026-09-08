---
type: architecture
id: DOMAIN-003
title: "meeting — 2트랙 회의록과 최종 회의록"
status: draft
product: "task-management"
created_at: 2026-09-04
updated_at: 2026-09-08
tags:
  - product/task-management
  - doc/architecture
  - architecture/database
links:
  baselines: [BASE-003]
  decisions: [DEC-003, DEC-001, DEC-002, DEC-004, DEC-005]
  specs: [SPEC-006, SPEC-007, SPEC-008]
  works: []
  related: []
---

# meeting

**사람과 AI 가 각자 회의록을 쓰고, 종료 후 AI 가 최종 회의록을 한 번에 쓴다.** 이 도메인의 설계 축은 그 2트랙 + 최종 한 벌이다(BASE-003 · DEC-003 §4 2026-09-07).

## Purpose

DEC-003 의 2트랙 모델·배치 파이프라인·실패 정책을 스키마로 옮긴다. 12-meeting-notes 의 「줄 하나에 배치가 `detail`·`evidence` 를 채운다」 단일 트랙 모델은 폐기됐다(§A-5).

> **2026-09-06 개정.** 재작성된 SPEC-006·007·008 이 §7 「ERD 변경 필요」로 올린 컬럼과, 같은 날 DEC-003 §1 표에 들어온 사용자 결정 2건(AI 한 줄 요약 바 · 종료 후 줄 삭제/안건 이름 수정)을 반영했다.
>
> **2026-09-07 개정 — `Meeting flow.md` MF-1 ~ MF-70.** 통합 호출이 없어져(MF-56 · 57) **`source_human_line_id` · `source_ai_line_id` 와 그 부분 UNIQUE · CHECK 를 지웠고**, 업무 페이로드(MF-59)를 위해 **`pending_change` 를 `payload` 로 바꿨으며**, 용어 보정 표(MF-54)를 `meeting.term_corrections` 로, `work_type.description`(MF-21)을 `account.md` 에 더했다. AI 트랙 쓰기 규약(M-7)이 「INSERT 만」에서 **「배치마다 전량 교체」**(MF-53)로 바뀌었다. 컬럼마다 **어느 결정이 왜 요구했나**를 병기한다 — 나중에 근거를 몰라 지우는 일이 없게.
>
> **2026-09-07 저녁 추가 — MF-64(정정) · 66 · 67.** 스키마는 그대로다. 바뀐 것은 **`payload` · `task_id` 가 채워지는 길**이다(M-14 · M-14-a) — 회의록 payload 드로어(회의록 것이다 · 업무 탭 드로어 재사용 폐기)의 **모드별 푸터**에서 「저장」이 `payload` 를 붙이고 「넣기」가 업무를 만든다. 액션·업무 줄은 **`POST …/lines` 가 줄과 `payload` 를 한 요청으로** 만들 수 있다(칩 진입 — 그때도 업무는 안 생긴다). **MF-69** 로 단명 토큰이 `auth_session(kind='meeting')` 행이 됐다 — 회의 도메인에 컬럼이 늘지는 않는다(`account.md` A-13).
>
> **2026-09-08 개정 — MF-71 「중간 배치는 AI 혼자 쓴다」.** **스키마는 그대로다.** 바뀐 것은 **`source_agenda_id` 가 채워지는 자리**다 —
> 회의 중 배치가 사람 안건을 조회하지 않게 되면서(도구를 안 준다) **미러 안건이 없어졌다**: `track='ai'` 안건은 **전부 `source_agenda_id NULL`**,
> `state` 도 `NULL`, 배치 출력의 `humanAgendaId` 는 **서버가 무시**한다. 이 컬럼을 채우는 것은 **`track='merged'` 뿐**이다(최종 회의록).
> 걸린 규칙 — **M-5-a · M-5-b · M-5-c · M-6 · M-7 · M-8**. 구현은 **WORK-015**.

## Entities / Tables

| Entity/Table | Purpose | Notes |
|---|---|---|
| `meeting` | 회의록 본체 | 소프트 딜리트. **일시(`start_at`/`end_at`)를 소유**. `recording_started_at` 이 **경과 시간·`at_ms` 의 기준점**. `ai_headline` · `term_corrections` 는 최종 회의록 호출(②)과 같은 트랜잭션에서 찬다 |
| `meeting_agenda` | 안건 | **줄과 같이 트랙별로 갈린다** — `track ∈ {human, ai, merged}`. `source_agenda_id` 로 사람 안건을 가리킨다 |
| `meeting_line` | **줄 — 3트랙** | `track ∈ {human, ai, merged}`. `merged` 의 액션·업무 줄은 `payload` 에 DB 에 바로 넣을 업무 생성분·변경분을 갖는다(MF-59) |
| `meeting_transcript` | 확정 발화 블록 | 근거 칩의 원천. 회의 중에는 실시간 확정 토큰, **종료 후 async 재전사 결과로 전량 교체**(MF-37) |
| `meeting_attachment` | 첨부 | **md 문서 · URL 링크 두 갈래**(`kind ∈ {doc, link}`) — `task_attachment` 와 같은 모양 |
| `meeting_batch_run` | 배치 실행 이력 | 실패 구간을 다음 배치로 넘기는 커서. AI 탭 「배치 n회」·종료 job 의 `progress.phase` 가 여기서 **파생**된다 |

### 왜 줄이 세 테이블이 아니라 한 테이블 + `track` 인가

세 집합의 컬럼이 사실상 같고(안건·종류·본문·순서·근거·업무 참조), 최종 회의록(`merged`)이 AI 트랙과 같은 스키마 한 벌로 나온다(MF-52). 테이블을 셋으로 가르면 같은 컬럼 정의를 세 번 쓰고 적재 로직이 세 모델을 오간다. 트랙별 조회는 `(meeting_id, track, agenda_id, order_index)` 인덱스 하나로 끝난다.

**안건에도 같은 `track` 을 둔다**(2026-09-05). 「안건 > 줄」 트리가 트랙마다 통째로 하나씩 있고, 탭 하나가 트랙 하나를 그대로 그린다.

### 컬럼 변경 — 근거 표 (2026-09-06 · 2026-09-07)

`../README.md` §1 ERD 가 정본이다. 여기는 **왜 생겼나·왜 없어졌나**만 적는다.

| 대상 | 변경 | 누가 왜 요구했나 |
|---|---|---|
| `meeting.recording_started_at timestamptz NULL` | `/start` 가 성공한 시각. `status='recording'` 전이와 같은 트랜잭션에서 채운다 | **SPEC-007 §7-C** — 경과 시간의 기준이고 **M-11 「`at_ms` 는 회의 시작 기준 오프셋」의 그 기준점**이다. `start_at` 은 **예정** 일시라 늦게 시작하면 어긋난다. 근거 칩 벽시계 = `recording_started_at + fromMs`(SPEC-007 U-6) |
| `meeting.ai_session_id` | **`/start` 가 채우지 않는다.** 웜스타트 워커가 끝났을 때 UPDATE 한다(MF-1). `recording` 인데 `NULL` 인 상태가 정상적으로 존재한다 — 그동안 배치는 돌지 않는다 | **MF-1** — `/start` 는 전이만 하고 즉시 응답. 웜스타트에서 받는 것은 세션 id 하나뿐이고 첫 배치 때까지만 있으면 된다 |
| `meeting_agenda.state` CHECK → `next \| active \| done`, **NULL 허용** | `active` 추가 · 시작 전은 `NULL` | **SPEC-007 §7-C** — 「논의 중」 배지 · 프롬프트 바의 활성 안건 · **안건 전환 배치 트리거**(DEC-003 §STT)의 원천. **SPEC-006 §7** — 시작 전 안건은 상태가 없다 |
| `meeting_agenda.source_agenda_id bigint NULL` (self FK) | **`track='merged'` 안건이 가리키는 사람 안건** id. **`track='ai'` 는 항상 `NULL`**(2026-09-08 · MF-71) · `human` 도 항상 `NULL` | 원래는 SPEC-007 §7-C 가 AI 트랙의 **미러 안건**을 위해 넣었다. **MF-71 이 회의 중 미러를 없앴다** — 중간 배치가 사람 안건을 조회하지 않으므로 가리킬 대상이 없다. 컬럼은 남기고 **쓰는 자리는 최종 회의록뿐**이다(**SPEC-008 §4** — `merged` 안건이 사람 안건을 가리키고 `state` 를 거기서 복사한다) |
| `meeting_attachment.kind varchar CHECK (doc \| link)` · `url` · `label` 추가 · `document_id` **NULL 허용** | 첨부 두 갈래. `kind` 에 따라 채워지는 컬럼이 갈린다(`doc` → `document_id` 만 · `link` → `url`·`label` 만, CHECK 강제 — `task.md` T-9-a 와 같다) | **SPEC-006 §7** · **SPEC-007 §7-C** — DEC-003 §1 표(2026-09-06) 「자료함 문서(md)와 URL 링크 두 갈래는 실동작」 |
| `meeting_attachment` `UNIQUE (meeting_id, document_id) WHERE document_id IS NOT NULL` | 같은 문서 중복 첨부 금지 | **SPEC-006 §7** — §4 「같은 문서 중복 첨부는 중복 행을 만들지 않는다」 |
| ~~`meeting_line.source_human_line_id` · `source_ai_line_id`~~ + 부분 UNIQUE 두 건 + CHECK | **삭제**(2026-09-07) | **MF-56 · MF-57** — 통합 호출이 없어졌다. 이 두 컬럼은 「사람 줄 우선 · 서버가 본문 복사 · 이중 계승 금지」 통합 규칙(DEC-003 OQ-7)의 검증 축이었는데 그 규칙 자체가 폐기됐다. 최종 회의록은 AI 가 한 벌로 쓰고 사람 줄과의 대응을 출력하지 않는다(MF-52 스키마에 그 자리가 없다). 쓰는 곳이 없는 컬럼을 남기지 않는다(G-7 의 결) |
| `meeting_line.pending_change` → **`payload jsonb NULL`** (이름 변경 · 뜻 확장) | **회의록 탭이 그리는 트랙(`merged` · 실패 상태면 `human`)의 `kind ∈ {action, task}` 줄에만 값.** AI 가 최종 회의록에서 채우거나 사람이 편집 드로어 「저장」으로 채운다 — 같은 컬럼, 출처 구분 없음(MF-65). 액션 줄 = 새 업무 생성분 `{title, workTypeId, projectId, startDate, dueDate, description, todos[]}` · 업무 줄 = 기존 업무 변경분 `{dueDate, status, note, todos[], relatedTaskIds[], projectId, completionResult}`. 그 밖의 줄·트랙은 `NULL`(CHECK) | **MF-59** — 최종 회의록의 액션·업무 줄에 DB 에 바로 넣을 페이로드를 담는다. **MF-52** — 스키마는 한 벌이고 페이로드만 nullable(회의 중 AI 줄은 서버가 `NULL` 로 버린다). **MF-61 · MF-65** — 사람이 적은 줄은 `NULL` 이라 빈 드로어로 열고, 사람이 채워 「저장」하면 그 값이 `payload` 가 된다. **`payload` 가 있다고 업무가 있는 게 아니다** — 「넣기」가 업무를 만든다(브리프 §3). 이전 `pending_change` 는 업무 줄의 변경분 셋(기한·상태·note)만 담았다 — 액션 줄의 생성분까지 한 컬럼에 담으므로 이름을 `payload` 로 바꿨다 |
| **`meeting.term_corrections jsonb NULL`** (신설) | 최종 회의록 호출이 낸 **STT 용어 매핑표** `[{stt, correct, grade}]`, `grade ∈ {auto, guess}`. `ai_headline` 과 같은 트랜잭션에서 찬다. 회의 1건 단위 | **MF-54** ② — 「표가 곧 백업이다 — 표에 없는 치환은 하지 않는다. 그래야 되돌릴 수 있다」. 서버가 `grade='auto'` 항목만 `meeting_transcript.content` 에 치환하고, 표를 남겨 되돌릴 근거를 둔다. 별도 테이블로 두지 않는 이유 — 회의당 몇 줄이고 조회 축(용어로 검색)이 v1 에 없다. 화면은 v1 에 없다(기획·정책에 표시 화면이 없다) |
| `meeting_batch_run.phase` CHECK → `incremental \| final` | `integration` 삭제. `final` = 최종 회의록 호출(②) | **MF-56** — 통합 호출이 없다. 재전사(①)는 codex 호출이 아니라 Soniox 호출이라 배치 이력이 아니다 — job 의 `progress.phase='transcription'` 은 `job` 행에서 파생한다(SPEC-008 §4) |
| `meeting` 인덱스 `(account_id, start_at) WHERE deleted_at IS NULL` | 목록 월 범위 조회 | **SPEC-006 §7** — U-1 월 단위 목록이 이 인덱스를 탄다 |
| `job.error_code` 값 · `progress{phase, attempt}` 는 **파생** | `error_code ∈ {transcription_failed, transcription_timeout, final_failed, final_timeout, job_timeout}`. `progress.phase ∈ {transcription, final}` — `transcription` 은 job 이 ① 을 도는 동안, `final` 은 `meeting_batch_run(phase='final')` 이 생긴 뒤. `attempt` 는 `job.attempt`(② 시도 회차 1~3) | **SPEC-008 §4** · **MF-37 · MF-58** — 재전사 실패가 별개 실패 코드다(fallback 없음 · 「다시 시도」). G-7 「파생값을 컬럼으로 두지 않는다」 |
| `meeting.ai_headline` | **컬럼은 그대로.** 규칙은 M-19 | **DEC-003 §1 표 · §4 종료 파이프라인** — 최종 회의록 호출(②)의 출력 필드 하나 |
| `work_type.description text NULL` | `account.md` A-12 | **MF-21** — AI 가 새 업무의 유형을 고를 근거. `list_work_types()` 가 이름 · 종류 · 설명을 준다 |

## Invariants

- **M-1** **회의록이 일시를 소유한다**(2026-09-05 개정). `start_at`·`end_at` 은 `meeting` 에 있고, `schedule` 은 그 **파생**이다. 캘린더에서 드래그해도 고쳐지는 것은 `meeting` 쪽이고 `schedule` 은 따라 내려온다(DEC-005 §3 · §A-4 · `../README.md` §3). 회의는 시간이 사실상 필수라 두 컬럼은 NOT NULL 이다.
- **M-1-a** **`start_at` 은 예정, `recording_started_at` 은 실적이다**(2026-09-06 · SPEC-007 §7-C). `/start` 성공 시각을 `recording_started_at` 에 넣고, **경과 시간·`at_ms`·근거 칩의 벽시계 환산은 전부 이 값을 기준**으로 한다. `start_at` 으로 환산하지 않는다 — 늦게 시작한 회의에서 칩이 어긋난다. `scheduled` 에서는 `NULL` 이고, 한 번 채우면 바꾸지 않는다(회의 시작은 한 번뿐 — M-3).
- **M-2** `work_type_id` 는 **`kind='meeting'` 인 유형만** 받는다. 디자인의 `미팅·회의|반복|개인` 3종 enum 은 폐기됐고 **반복 회의는 v1 제외**다(DEC-003 §3 · §A-7).
- **M-3** `status` 는 **4종** — `scheduled → recording → generating → ended`. **`generating` 은 신설**이다(DEC-003 §3 · §A-6). `generating` 이 뜻하는 것은 **① async 재전사 → ② 최종 회의록 호출**(MF-37 · MF-56)이다.
- **M-4** 종료 파이프라인 결과는 `integration_state` 가 든다(컬럼명은 그대로 — 값의 뜻은 「최종 회의록 생성 상태」다). **`status='ended'` + `integration_state='failed'`** 가 「회의록 생성 실패 · 다시 시도」 배너의 조건이다. **「다시 시도」는 이 조합에서만 노출**되고, 정상 생성분의 재생성은 없다(DEC-003 §4 · MF-58).
- **M-5** **줄은 항상 어떤 안건에 속한다** — `agenda_id` 는 NOT NULL 이고, **줄과 안건의 `track` 은 반드시 같다**(트랙을 넘는 참조를 만들지 않는다).
- **M-5-a** **안건도 트랙별이다**(2026-09-05 확정). AI 가 만든 안건은 `track='ai'` 에만 존재하고 **회의 중 사람 회의록 탭에 보이지 않는다.** 공유 축 + `origin` 표식 안은 폐기됐다. 두 축은 **종료 후 최종 회의록(`track='merged'`)에서 합쳐진다** — AI 가 `list_agendas()` 로 둘 다 보고 한 벌로 낸다(MF-51 · MF-56). **회의 중에는 둘이 서로를 모른다**(MF-71) — AI 는 사람 안건을 조회하지 않고 발화만 보고 자기 안건을 가른다. 제목이 겹쳐도 상관없다.
- **M-5-b** **`source_agenda_id` 를 채우는 것은 최종 회의록뿐이다**(2026-09-08 재정정 · **MF-71**). **회의 중 배치의 AI 안건은 전부 신설이다** — `source_agenda_id` 는 항상 `NULL` 이고, 배치 출력의 `humanAgendaId` 는 **서버가 무시한다**(값이 와도 폐기 사유가 아니다 — SPEC-007 §4 검증 2). 미러 안건을 만드는 갈래는 코드에 **없어야 한다**. **배치마다 AI 트랙을 전량 교체하므로(M-7) AI 안건 id 는 배치마다 새로 생긴다** — 출력이 앞 배치의 AI 안건 id 를 참조하는 갈래(`aiAgendaId`)도 없다. **`merged` 안건은 이 컬럼으로 사람 안건을 가리킨다**(SPEC-008 §4 — 사람 안건이 정확히 한 번씩). `human` · `ai` 안건은 항상 `NULL` 이다 — CHECK 로 잡는다. *(이전 판 「배치 출력이 `humanAgendaId` 를 참조하면 미러 AI 안건을 만든다」는 폐기 — 2026-09-06~09-07 판)*
- **M-5-c** **안건 `state` 는 회의 중·종료 후의 것이다**(2026-09-06 · SPEC-006 §7 · SPEC-007 §7-C). `scheduled` 에서는 `NULL`. `recording` 에서 사람 트랙은 `active` 를 **최대 하나** 갖는다 — 부분 UNIQUE `(meeting_id) WHERE track='human' AND state='active'`. `/end` 가 `active` 를 `done` 으로 바꾸므로 **`ended` 회의에 `active` 안건은 없다**(SPEC-008 §4 `/end`). `merged` 안건의 `state` 는 원본 사람 안건에서 복사한 표시값이고 트리거로 쓰지 않는다. **`ai` 안건의 `state` 는 항상 `NULL`** 이다 — 미러가 없어 복사할 원본이 없다(MF-71). AI 탭은 배지 대신 「AI 안건」 캡션만 그린다(SPEC-007 U-4).
- **M-5-d** **안건은 지우지 않는다 — 종료 후에는 이름만 고친다**(2026-09-06 · MF-62). 줄은 항상 안건에 속하므로(M-5) 안건을 지우면 딸린 줄이 통째로 날아간다. 필요 없는 줄은 줄 단위로 지운다. **유일한 예외는 시작 전(`scheduled`) 사람 안건**이다 — 줄이 아직 없어 잃을 것이 없다(SPEC-006 §4 `DELETE …/agendas`). `recording` 이후 안건 DELETE 표면은 없다. AI 안건은 어느 상태에서도 사람이 지우지 않는다(M-6) — 배치의 전량 교체(M-7)만이 AI 안건을 지운다.
- **M-5-e** **`meeting_agenda.title` 의 쓰기 경로는 둘이다**(2026-09-06 확인). ① **시작 전** — `PATCH …/agendas/{id} {title}`(SPEC-006 §4). ② **종료 후** — 회의록 탭 편집에서 이름 수정(MF-62 「제목 수정은 된다 — AI 가 오타를 낼 수 있다」). 대상 트랙은 줄 삭제와 같은 규칙이다(M-20 — `succeeded` 면 `merged`, `failed` 면 `human`). **회의 중(`recording`)에는 제목을 고치지 않는다** — SPEC-007 §4 의 `PATCH agendas` 는 **상태만** 받는다. AI 안건 제목은 어느 경로로도 사람이 고치지 않는다(M-6).
- **M-6** 회의 중 AI 는 **`track='ai'` 에만 쓰고, 사람 것을 읽지도 않는다**(2026-09-08 · **MF-71**). 사람 줄·사람 안건을 고치지도 제안하지도 않고(DEC-003 §4), **조회하지도 않는다** — 배치 입력에 싣지 않을 뿐 아니라 `list_agendas()` · `get_agenda(id)` 가 **회의 중 워커의 `enabled_tools` 에 없다.** 회의 중에 열리는 것은 **업무 셋**(`list_tasks` · `get_task` · `list_work_types`)뿐이고, 도구는 백엔드 API 의 래퍼이지 DB 직결이 아니다(MF-2). 사람 안건·사람 줄을 AI 가 보는 것은 **최종 제출 한 번**이다(M-8). *(문구 이력 — 최초 「읽기 전용 컨텍스트로 배치 입력에 넣는다」 → 2026-09-07 「읽기는 도구로 한다」(MF-50) → 2026-09-08 「회의 중에는 읽지 않는다」(MF-71))*
- **M-6-a** **AI 증분은 즉시 반영한다**(2026-09-05 확정). 배치 결과가 들어오는 대로 AI 탭에 나가고, **몇 번째 배치까지 반영됐는지**를 화면이 표시한다(「배치 2회 → 3회」). 버퍼링하지 않는다. 그 회차는 컬럼으로 두지 않고 `meeting_batch_run` 의 성공분 최대 `seq` 에서 **파생**한다(G-7). **종료 후 「종결」 표시는 없다** — 종료 시 배치가 없다(MF-56).
- **M-7** **회의 중 배치는 매번 AI 트랙 전체를 낸다. 서버는 검증을 통과한 결과로 `track='ai'` 안건·줄을 한 트랜잭션에서 DELETE + INSERT 한다**(2026-09-07 · MF-53). 앞 배치가 잘못 가른 안건을 다음 배치가 합친다. 검증(스키마 · 참조 · 강등)에서 떨어지면 **직전 성공분이 그대로 남는다** — 검증 전에 지우지 않는다. **INSERT 하는 안건은 전부 `source_agenda_id = NULL` 이다**(M-5-b · MF-71) — 출력의 `humanAgendaId` 를 보고 갈라지는 자리가 없다. AI 줄·안건 id 가 배치마다 새로 생기지만, 회의 중 AI 트랙을 가리키는 것은 없다(`merged` 는 종료 후에야 생기고 원본 참조 컬럼이 없다). *(이전 판 「INSERT 만 · 전체 재정리는 종료 후 종료 시 배치 한 번」은 폐기)*
- **M-8** 최종 회의록(`track='merged'`)은 **AI 가 한 번에 쓴다**(2026-09-07 · MF-56 · MF-57). 재전사 스크립트를 주고, AI 가 `list_agendas()` · `get_agenda(id)` 로 사람 줄과 자기 AI 줄을 보고 **정리본 한 벌**을 낸다. **두 트랙이 만나는 자리는 여기뿐이고**(MF-71), 도구 일곱이 다 열리는 자리도 여기뿐이다. **사람이 적은 문장도 AI 가 다듬는다** — 「사람 문장 그대로 복사」 규칙은 없다. 최종이 끝나면 **AI 정리본 = 회의록**이다(`Meeting flow.md` §3-3). *(이전 M-8 「본문은 사람이 쓴 문장 그대로 · AI 에서는 `evidence` 만」과 M-8-a 「통합 줄은 원본을 가리킨다」는 폐기)*
- **M-8-a** **최종 회의록 출력은 회의 중 배치와 같은 스키마 한 벌이다**(MF-52). 다른 것은 셋 — `payload`(액션·업무 줄에만, 회의 중은 `NULL`) · `headline`(`ai_headline`) · `termCorrections`(`term_corrections`). 서버 검증은 **안건 참조 존재**(`humanAgendaId` 가 이 회의 사람 안건) · **업무 참조 사후 검사**(M-15) · **페이로드 참조**(유형 · 프로젝트 · 연관 업무가 본인의 삭제되지 않은 것) · **`evidence` 범위**(재전사 스크립트 안) · **`payload.status ≠ done`**(M-14-a)이다. 어기면 그 시도 실패(재시도 2회 — DEC-003 §7).
- **M-9** `meeting_transcript` 에는 **확정 토큰만** 들어간다. 잠정 토큰은 화면 표시용으로 흘려보내고 저장하지 않는다(DEC-003 §3).
- **M-9-a** **종료 후 재전사가 `meeting_transcript` 를 전량 교체한다**(2026-09-07 · MF-37). ① 이 성공하면 실시간 블록을 DELETE 하고 재전사 블록을 INSERT 한다(한 트랜잭션). **`at_ms` 기준은 같다**(녹음 파일 시작 = `recording_started_at`) — 그래서 근거 칩(`evidence[{fromMs,toMs}]`)은 **블록 id 가 아니라 시각(ms)** 으로 매칭하고, 어느 컬럼도 `meeting_transcript.id` 를 가리키지 않는다. 블록 경계 규칙은 실시간과 같다(화자 변경 · 300자 · 2초 공백 — SPEC-007 §4). ① 이 실패하면 실시간 블록이 그대로 남고 회의는 `ended`+`failed` 다(MF-58 — 실시간 결과로 최종 회의록을 만들지 않는다).
- **M-9-b** **용어 보정은 표대로만 한다**(2026-09-07 · MF-54). `term_corrections` 의 `grade='auto'` 항목만 `meeting_transcript.content` 에 치환하고, `grade='guess'` 는 본문을 건드리지 않는다. **`speaker_label` 은 어떤 경우에도 바꾸지 않는다.** 표에 없는 치환은 없다.
- **M-10** `speaker_label` 은 **익명**(`화자 1`/`화자 2`)이다. 참석자·발언자 이름 컬럼을 두지 않는다(DEC-003 §2). Soniox 는 **세션당 최대 15명**을 라벨링한다(soniox).
- **M-11** `at_ms` 는 **회의 시작 기준 오프셋**이다 — 그 기준점은 **`meeting.recording_started_at`** 이다(M-1-a). 근거 칩의 `evidence` 도 같은 기준이라 벽시계 시각과 섞지 않는다. **줄에는 시각을 붙이지 않는다**(MF-9) — 줄의 `created_at` 을 화면에 그리지 않고, 시각은 안건(첫 줄 `created_at`)과 근거 칩 구간에만 있다.
- **M-12** `ai_session_id` 는 **회의 하나에 하나**다. 매 배치가 이 세션을 `resume` 한다 — 배치마다 새 세션을 만들지 않는다(DEC-003 §STT). **`/start` 가 채우지 않는다**(MF-1) — 웜스타트 워커가 끝나면 UPDATE 한다. `NULL` 인 동안 배치는 제출되지 않는다.
- **M-13** **`recording_path` 는 영구 보관**이다. 회의록을 소프트 딜리트해도 녹음 파일을 지우지 않는다. 보존 기간·자동 삭제 정책이 없다(DEC-003 §4·§6). **종료 후 재전사(M-9-a)와 「다시 시도」(MF-58)의 입력**이다.
- **M-14** `meeting_line.task_id` 가 채워지는 길은 셋이다(2026-09-07 · MF-65 · **MF-64 정정** · **MF-67**) — ① **최종 회의록의 업무 줄**은 AI 가 `get_task(id)` 로 확인한 `task_id` 를 갖고 온다(MF-59 「taskId — 조회로 확인한 것만」 · M-15 사후 검사를 지나야 남는다) ② **업무 payload 드로어의 헤더 업무 셀렉터**에서 사람이 고르고 「저장」 또는 「넣기」 — AI 가 엉뚱한 업무를 골랐을 때 바꾸는 길도 이것뿐이다. **그 드로어는 회의록 것이다**(MF-67 — 업무 탭 드로어를 재사용하지 않는다) ③ **액션 줄의 「넣기」**가 업무를 만들면서 채운다. **줄을 적는 것만으로는 안 생긴다**(DEC-003 §5). **`POST …/lines` 는 `kind='task'` 줄에 한해 `task_id` 를 함께 받는다**(MF-64 정정 — 「+ 연관 업무」 칩이 payload 드로어를 바로 열고 「저장」이 줄과 `task_id`·`payload` 를 한 요청으로 만든다. 논의·결정 줄에 오면 422). **그래도 업무는 안 생긴다** — 그 표면은 `task_service` 를 부르지 않는다. **`task_id` 가 있어도 업무가 바뀐 것은 아니다** — 업무를 바꾸는 것은 「넣기」(`…/lines/{id}/task`)뿐이다.
  - **푸터는 모드별이다**(**MF-66**) — **편집 모드 「취소 · 저장」**(`payload`(와 `task_id`)만 줄에 붙는다 · 업무 없음) / **보기 모드 「취소 · 넣기」**(업무 생성·갱신). 한 푸터에 셋을 두지 않는다. 「둘 다 「넣기」」로 읽지 않는다.
- **M-14-a** `payload` 가 담는 것(2026-09-07 · MF-59 · MF-65 · **MF-64 정정** · **MF-66** · **MF-67**). **`payload` 는 줄에 붙는 데이터이고 업무가 아니다** — AI 가 채우든 사람이 **회의록 payload 드로어**에서 「저장」하든 같은 컬럼이고 서버는 출처를 구분하지 않는다. 「넣기」가 그것을 업무로 만들고 `NULL` 로 비운다. **`payload` 를 쓰는 표면은 둘**이다 — `PATCH …/lines/{id} {payload}`(있는 줄) · **`POST …/lines {…, payload}`**(액션·업무 칩이 연 드로어의 「저장」 — 줄과 `payload` 가 한 요청). **둘 다 `task_service` 를 부르지 않는다.** 푸터가 모드별이라(**MF-66** — 편집 「저장」 / 보기 「넣기」) `payload` 를 붙이는 것과 업무를 바꾸는 것이 화면에서도 갈린다.
  - **드로어의 필드는 `payload` 키 그대로다**(MF-67). 액션 payload 드로어 = 안건(고정) · 제목 · 유형 · 프로젝트 · 계획 시작~종료 · 설명 · 할일 / 업무 payload 드로어 = 헤더 업무 셀렉터 + 변경분 일곱. 제목 · 유형 · 설명 · 시작일은 업무 줄에서 못 바꾸고, 첨부 · 로그 · 참고자료는 어느 쪽에도 없다 — **업무 탭 드로어를 재사용하지 않기 때문에 그 블록이 딸려 오지 않는다.** 담는 것 — **액션 줄**: 새 업무 생성분(제목 · 유형 · 프로젝트 · 시작일~기한 · 설명 · 할일 목록. 상태는 `todo` 고정이라 담지 않는다). **업무 줄**: 변경분 일곱 — **기한**(`task.due_date`) · **상태**(`todo | in_progress` 만 — **`done` 을 담지 않는다**: 완료 게이트에 회의록 뒷문을 만들지 않는다. 취소도 없다 — 사유 필수) · **진행 메모**(업무 **메모에 새 항목 추가**) · **할일 추가** · **연관 업무** · **프로젝트** · **완료 결과**(`task.completion_result` — 채워 두면 사람이 업무 화면에서 완료를 누를 때 게이트가 이미 열려 있다). 그 밖의 필드는 담지 않는다. *(이전 셋 — 기한·상태·note — 을 확장)*
- **M-15** 배치·최종 출력의 `task_id` 는 **회의 프로젝트의 업무(무소속 회의면 무소속 업무 — M-15-a) 안**에 있어야 한다. 검사는 **서버 사후 검사**다(MF-50 — 입력에 화이트리스트를 싣지 않는다. 기준 목록은 검사 시점에 서버가 조회한다). 밖이면 `task_id` 를 떼고 `kind='action'` 으로 강등하되 **본문은 살린다**(DEC-003 §7). 강등된 줄의 `payload` 는 `NULL` 로 둔다(업무 변경분이 갈 곳이 없다).
- **M-15-a** 사후 검사 기준은 회의의 프로젝트를 따른다. **무소속 회의에는 무소속 업무**(프로젝트 없는 업무)다(2026-09-05 확정, DEC-003 §4).
- **M-16** JSON 스키마를 위반한 배치 결과는 **행 하나도 넣지 않고 통째로 폐기**한다. 부분 파싱 금지 — `meeting_batch_run.status='discarded'` 로 남기고 그 구간을 다음 배치에 합친다(DEC-003 §7). **AI 트랙은 직전 성공분 그대로**다(M-7).
- **M-17** 첨부는 **두 갈래**다(2026-09-06 개정 · SPEC-006 §7 · SPEC-007 §7-C · DEC-003 §1 표) — `kind='doc'` 은 자료함 문서 참조(`document_id`, **md 만** — DEC-004 §8), `kind='link'` 는 URL 링크(`url`·`label`). `kind` 에 따라 채워지는 컬럼이 갈리고 CHECK 로 강제한다(`task.md` T-9-a 와 같다). **로컬 파일 업로드 경로는 v1 에 없다** — UI 는 v2 게이트다. **회의 중 md 작성(`source=local`·`agendaId`)은 v2** — v1 에 문서 생성 경로가 없다(DEC-004 §8 · §A-11).
- **M-18** **300분 초과 회의를 다루지 않는다** — 세션 경계·재연결 컬럼을 만들지 않는다(DEC-003 §4). 재전사 파일 상한(300분)과도 맞는다.
- **M-19** **`ai_headline` 은 최종 회의록 호출(종료 파이프라인 ②)의 출력 필드다**(2026-09-06 · 2026-09-07 MF-56 반영). ① **최종 회의록이 성공한 회의에만 값이 있다** — `integration_state='succeeded'` · `merged` 행 · `term_corrections` 와 같은 트랜잭션에서 채운다. ② **실패하면 `NULL` 로 남는다** — 부분 저장하지 않는다. ③ **재생성이 없다**(DEC-003 §4) — 「다시 시도」(`ended`+`failed` 에서만, M-4)가 성공할 때 처음 채워진다. ④ 사람이 편집하지 않는다 — 편집 범위(DEC-003 §5)에 없다.
- **M-20** **종료 후 줄 삭제는 회의록 탭의 줄만 지운다**(2026-09-06 · DEC-003 §1 표 · §5). 대상 트랙은 편집 모드와 같다 — `integration_state='succeeded'` 면 **`merged`**, `failed` 면 **`human`**. **`ai` 트랙·`meeting_transcript`·녹음은 남는다**(DEC-003 §6 「AI 탭은 최종 회의록과 별개로 남는다」) — 근거 칩이 가리킬 원본이 있어야 한다. 규칙 넷.
  - **하드 딜리트다.** 근거 — `../README.md` §0-1 「모든 자식 행은 하드 삭제 · v1 에 복원 창구가 없다」가 그대로 적용된다. 회의 본체만 소프트 딜리트다(DEC-003 §4). `deleted_at` 을 줄에 두지 않는다.
  - **업무가 생성된 줄을 지워도 업무는 지우지 않는다**(DEC-003 §8 「회의록은 업무를 만들고 갱신만 한다」). `task_id` 가 가리키던 업무는 그대로 남고, 회의록 쪽 연결만 사라진다. `payload` 로 대기 중이던 갱신은 줄과 함께 없어진다(업무에 반영된 적이 없다).
  - **지운 자리는 그대로 둔다**(MF-36). `order_index` 를 당기지 않는다 — 당기면 지울 때마다 뒤 줄을 전부 UPDATE 해야 한다. 화면은 번호순으로 그리고, 새 줄은 「그 안건의 마지막 번호 + 1」이라 구멍이 있어도 상관없다. **줄 순서 변경은 여전히 없다**(DEC-003 §1 표) — `order_index` 를 사람이 고치는 표면은 없다.
  - **줄 종류는 못 바꾼다**(MF-60). `kind` 를 고치는 표면이 없다 — 그래서 `kind=task ↔ task_id` 불변식이 전환으로 깨질 일이 없다. 종류가 틀렸으면 줄을 지우고 새로 적는다.

## Related Specs / Works

- SPEC-006 회의록 — 목록·생성·시작 전 (첨부 두 갈래 · 안건 `state` NULL · `meeting` 인덱스 · `/start` 즉시 응답)
- SPEC-007 회의록 — 회의 중 (`recording_started_at` · 안건 `active` · AI 트랙 전량 교체 · **회의 중 도구 셋** — MF-71)
- WORK-015 중간 배치 단독화 (`build_codex_options(phase)` · `humanAgendaId` 무시 · 미러 갈래 삭제 — MF-71)
- SPEC-008 회의록 — 종료·최종 회의록·편집 (재전사 · `payload` · `term_corrections` · `job` · `ai_headline` · 줄 삭제)
- 참조: `domains/account.md`(유형·프로젝트 · `work_type.description`) · `domains/task.md`(업무 생성·갱신 · 첨부 T-9) · `domains/calendar.md`(시간) · `domains/library.md`(첨부)

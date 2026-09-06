---
type: architecture
id: DOMAIN-003
title: "meeting — 2트랙 회의록과 통합본"
status: draft
product: "task-management"
created_at: 2026-09-04
updated_at: 2026-09-06
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

**사람과 AI 가 각자 회의록을 쓰고, 종료 후 통합한다.** 이 도메인의 설계 축은 그 2트랙이다(BASE-003).

## Purpose

DEC-003 의 2트랙 모델·배치 파이프라인·실패 정책을 스키마로 옮긴다. 12-meeting-notes 의 「줄 하나에 배치가 `detail`·`evidence` 를 채운다」 단일 트랙 모델은 폐기됐다(§A-5).

> **2026-09-06 개정.** 재작성된 SPEC-006·007·008 이 §7 「ERD 변경 필요」로 올린 컬럼과, 같은 날 DEC-003 §1 표에 들어온 사용자 결정 2건(AI 한 줄 요약 바 · 종료 후 줄 삭제/안건 이름 수정)을 반영했다. 컬럼마다 **어느 SPEC 이 왜 요구했나**를 병기한다 — 나중에 근거를 몰라 지우는 일이 없게.

## Entities / Tables

| Entity/Table | Purpose | Notes |
|---|---|---|
| `meeting` | 회의록 본체 | 소프트 딜리트. **일시(`start_at`/`end_at`)를 소유**. `recording_started_at` 이 **경과 시간·`at_ms` 의 기준점** |
| `meeting_agenda` | 안건 | **줄과 같이 트랙별로 갈린다** — `track ∈ {human, ai, merged}`. `source_agenda_id` 로 사람 안건을 가리킨다 |
| `meeting_line` | **줄 — 3트랙** | `track ∈ {human, ai, merged}`. `merged` 줄은 `source_human_line_id`·`source_ai_line_id` 로 원본을 가리킨다 |
| `meeting_transcript` | 확정 발화 블록 | 근거 칩의 원천 |
| `meeting_attachment` | 첨부 | **md 문서 · URL 링크 두 갈래**(`kind ∈ {doc, link}`) — `task_attachment` 와 같은 모양 |
| `meeting_batch_run` | 배치 실행 이력 | 실패 구간을 다음 배치로 넘기는 커서. AI 탭 「배치 n회」·「종결」·통합 시각이 여기서 **파생**된다 |

### 왜 줄이 세 테이블이 아니라 한 테이블 + `track` 인가

세 집합의 컬럼이 사실상 같고(안건·종류·본문·순서·근거·업무 참조), **통합본이 AI 줄의 타임스탬프를 물려받으므로** 같은 모양이어야 한다(DEC-003 §4). 테이블을 셋으로 가르면 같은 컬럼 정의를 세 번 쓰고 통합 로직이 세 모델을 오간다. 트랙별 조회는 `(meeting_id, track, agenda_id, order_index)` 인덱스 하나로 끝난다.

**안건에도 같은 `track` 을 둔다**(2026-09-05). 「안건 > 줄」 트리가 트랙마다 통째로 하나씩 있고, 탭 하나가 트랙 하나를 그대로 그린다.

### 2026-09-06 컬럼 변경 — 근거 표

`../README.md` §1 ERD 가 정본이다. 여기는 **왜 생겼나**만 적는다.

| 대상 | 변경 | 누가 왜 요구했나 |
|---|---|---|
| `meeting.recording_started_at timestamptz NULL` | `/start` 가 성공한 시각. `status='recording'` 전이와 같은 트랜잭션에서 채운다 | **SPEC-007 §7-C** — 경과 시간의 기준이고 **M-11 「`at_ms` 는 회의 시작 기준 오프셋」의 그 기준점**이다. `start_at` 은 **예정** 일시라 늦게 시작하면 어긋난다. 근거 칩 벽시계 = `recording_started_at + fromMs`(SPEC-007 U-6) |
| `meeting_agenda.state` CHECK → `next \| active \| done`, **NULL 허용** | `active` 추가 · 시작 전은 `NULL` | **SPEC-007 §7-C** — 「논의 중」 배지 · 프롬프트 바의 활성 안건 · **안건 전환 배치 트리거**(DEC-003 §STT)의 원천. `done \| next` 만으로는 서버가 어느 안건이 진행 중인지 모른다. **SPEC-006 §7** — 시작 전 안건은 상태가 없다(「완료/다음으로」는 회의 중·종료 후의 것) |
| `meeting_agenda.source_agenda_id bigint NULL` (self FK) | `track='ai'` 안건이 미러하는 **사람 안건** id. `NULL` = AI 신설 안건 | **SPEC-007 §7-C** — 안건이 트랙별로 갈렸으므로(M-5-a) AI 가 사람 안건에 맞춰 채우려면 AI 트랙에 그 안건의 사본과 **연결**이 있어야 한다. U-4 「AI 안건」 배지가 이 값으로 갈린다. **SPEC-008 §4** — `merged` 안건에도 같은 컬럼을 쓴다(사람 안건 id 또는 AI 신설 안건 id) → 통합의 「사람 안건 우선」이 이 연결로 판정된다 |
| `meeting_attachment.kind varchar CHECK (doc \| link)` · `url` · `label` 추가 · `document_id` **NULL 허용** | 첨부 두 갈래. `kind` 에 따라 채워지는 컬럼이 갈린다(`doc` → `document_id` 만 · `link` → `url`·`label` 만, CHECK 강제 — `task.md` T-9-a 와 같다) | **SPEC-006 §7** · **SPEC-007 §7-C** — DEC-003 §1 표(2026-09-06) 「자료함 문서(md)와 URL 링크 두 갈래는 실동작」. 업무(SPEC-003 U-7 · T-9)가 이미 그렇게 돌고 회의도 같다 |
| `meeting_attachment` `UNIQUE (meeting_id, document_id) WHERE document_id IS NOT NULL` | 같은 문서 중복 첨부 금지 | **SPEC-006 §7** — §4 「같은 문서 중복 첨부는 중복 행을 만들지 않는다」. 링크는 URL 중복을 막지 않는다(정책에 없다) |
| `meeting_line.source_human_line_id` · `source_ai_line_id` (`bigint NULL` self FK) | **`track='merged'` 에서만 값**(CHECK). 사람 줄 계승분 · 근거를 가져온 AI 줄 · AI 에만 있어 추가된 줄을 이 두 값의 조합으로 구분한다 | **SPEC-008 §7·§4 통합 규칙** — DEC-003 OQ-7 이 「`sourceHumanLineId` 계승」을 통합 판정의 축으로 못박았는데 컬럼이 없었다. 저장하지 않으면 이중 계승 검증도, 검수에서 「어느 줄이 어디서 왔나」 되짚기도 못 한다 |
| `meeting_line` `UNIQUE (source_human_line_id) WHERE source_human_line_id IS NOT NULL` | 한 사람 줄의 **이중 계승**을 DB 가 막는다 | **SPEC-008 §4** — 「사람 줄 우선 — 모든 사람 줄이 정확히 한 번 계승된다」. DEC-003 OQ-7 「구조로 판정」 |
| `meeting_line` `UNIQUE (source_ai_line_id) WHERE source_ai_line_id IS NOT NULL` | 한 AI 줄은 한 통합 줄에만 붙는다 | **SPEC-008 §4** — 「한 AI 줄은 한 사람 줄에만 짝지어진다 · 중복 AI 참조 → 그 시도 실패」. 위와 같은 결 |
| `meeting` 인덱스 `(account_id, start_at) WHERE deleted_at IS NULL` | 목록 월 범위 조회 | **SPEC-006 §7** — U-1 월 단위 목록이 이 인덱스를 탄다. `../README.md` §4 |
| `job.error_code` 값 3종 · `progress{phase, attempt}` 는 **파생** | `error_code ∈ {integration_failed, integration_timeout, job_timeout}`. `progress` 는 컬럼이 아니다 — `phase` 는 `meeting_batch_run` 최신 행, `attempt` 는 `job.attempt` | **SPEC-008 §4 `GET /api/jobs/{jobId}`** · `../backend/README.md` §6. G-7 「파생값을 컬럼으로 두지 않는다」 |
| `meeting.ai_headline` | **컬럼은 이미 있었다**(`../README.md` L202). 규칙이 없어 **M-19** 로 올린다 | **DEC-003 §1 표 · §4 종료 파이프라인(2026-09-06)** — SPEC-008 S008-OQ-1 을 사용자가 「v1 에 넣는다」로 닫았다 |

## Invariants

- **M-1** **회의록이 일시를 소유한다**(2026-09-05 개정). `start_at`·`end_at` 은 `meeting` 에 있고, `schedule` 은 그 **파생**이다. 캘린더에서 드래그해도 고쳐지는 것은 `meeting` 쪽이고 `schedule` 은 따라 내려온다(DEC-005 §3 · §A-4 · `../README.md` §3). 회의는 시간이 사실상 필수라 두 컬럼은 NOT NULL 이다.
- **M-1-a** **`start_at` 은 예정, `recording_started_at` 은 실적이다**(2026-09-06 · SPEC-007 §7-C). `/start` 성공 시각을 `recording_started_at` 에 넣고, **경과 시간·`at_ms`·근거 칩의 벽시계 환산은 전부 이 값을 기준**으로 한다. `start_at` 으로 환산하지 않는다 — 늦게 시작한 회의에서 칩이 어긋난다. `scheduled` 에서는 `NULL` 이고, 한 번 채우면 바꾸지 않는다(회의 시작은 한 번뿐 — M-3).
- **M-2** `work_type_id` 는 **`kind='meeting'` 인 유형만** 받는다. 디자인의 `미팅·회의|반복|개인` 3종 enum 은 폐기됐고 **반복 회의는 v1 제외**다(DEC-003 §3 · §A-7).
- **M-3** `status` 는 **4종** — `scheduled → recording → generating → ended`. **`generating` 은 신설**이다(DEC-003 §3 · §A-6).
- **M-4** 통합 결과는 `integration_state` 가 든다. **`status='ended'` + `integration_state='failed'`** 가 「통합 정리 실패 · 다시 생성」 배너의 조건이다. **「다시 생성」은 이 조합에서만 노출**되고, 정상 생성분의 재생성은 없다(DEC-003 §4).
- **M-5** **줄은 항상 어떤 안건에 속한다** — `agenda_id` 는 NOT NULL 이고, **줄과 안건의 `track` 은 반드시 같다**(트랙을 넘는 참조를 만들지 않는다).
- **M-5-a** **안건도 트랙별이다**(2026-09-05 확정). AI 가 만든 안건은 `track='ai'` 에만 존재하고 **회의 중 사람 회의록 탭에 보이지 않는다.** 공유 축 + `origin` 표식 안은 폐기됐다. 두 축은 **종료 후 통합본(`track='merged'`)에서 합쳐진다** — 사람 안건 우선(DEC-003 §4).
- **M-5-b** **AI 안건은 `source_agenda_id` 로 사람 안건을 가리킨다**(2026-09-06 · SPEC-007 §7-C). 배치가 `humanAgendaId` 를 참조하면 그 사람 안건을 미러하는 AI 안건(`source_agenda_id` = 그 id, 제목 복사)이 없을 때만 만들고, `newTitle` 이면 `source_agenda_id=NULL` 로 신설한다. **`merged` 안건도 같은 컬럼**으로 원본(사람 안건 id 또는 AI 신설 안건 id)을 가리킨다(SPEC-008 §4). `human` 안건은 항상 `NULL` 이다 — CHECK 로 잡는다.
- **M-5-c** **안건 `state` 는 회의 중·종료 후의 것이다**(2026-09-06 · SPEC-006 §7 · SPEC-007 §7-C). `scheduled` 에서는 `NULL`. `recording` 에서 사람 트랙은 `active` 를 **최대 하나** 갖는다 — 부분 UNIQUE `(meeting_id) WHERE track='human' AND state='active'`. `/end` 가 `active` 를 `done` 으로 바꾸므로 **`ended` 회의에 `active` 안건은 없다**(SPEC-008 §4 `/end`). AI·`merged` 안건의 `state` 는 원본에서 복사한 표시값이고 트리거로 쓰지 않는다.
- **M-5-d** **안건은 지우지 않는다 — 종료 후에는 이름만 고친다**(2026-09-06 · DEC-003 §1 표 「안건은 이름만 고친다. 안건 삭제는 없다」). 줄은 항상 안건에 속하므로(M-5) 안건을 지우면 딸린 줄이 갈 곳이 없다. **유일한 예외는 시작 전(`scheduled`) 사람 안건**이다 — 줄이 아직 없어 잃을 것이 없다(SPEC-006 §4 `DELETE …/agendas`). `recording` 이후 안건 DELETE 표면은 없다. AI 안건은 어느 상태에서도 사람이 지우지 않는다(M-6) — 최종 배치의 전량 교체(M-7)만이 AI 안건을 지운다.
- **M-5-e** **`meeting_agenda.title` 의 쓰기 경로는 둘이다**(2026-09-06 확인). ① **시작 전** — `PATCH …/agendas/{id} {title}`(SPEC-006 §4). ② **종료 후** — 회의록 탭 편집에서 이름 수정(DEC-003 §1 표·§5, 2026-09-06 추가). 대상 트랙은 줄 삭제와 같은 규칙이다(M-20 — `succeeded` 면 `merged`, `failed` 면 `human`). **회의 중(`recording`)에는 제목을 고치지 않는다** — SPEC-007 §4 의 `PATCH agendas` 는 **상태만** 받는다. AI 안건 제목은 어느 경로로도 사람이 고치지 않는다(M-6).
- **M-6** 회의 중 AI 는 **`track='ai'` 에만 INSERT 한다.** 사람 줄·사람 안건을 **고치지도 제안하지도 않는다**(DEC-003 §4). **읽기는 한다** — 사람 안건·사람 줄은 배치 입력의 **읽기 전용 컨텍스트**다(BASE-003 L36 「사람 입력 + 트랜스크립트를 워커로」 · L38 「사람이 적은 안건이 DB 에 있으니 컨텍스트로 같이 전달」 · DEC-003 §4 「사람이 만든 안건을 컨텍스트로 받아」 · §8 웜스타트 「미리 작성된 안건」 · SPEC-007 §4 AI 배치 계약). *(2026-09-06 문구 정정 — 이전 판은 읽기까지 금지했으나 기획·정책과 어긋났다. SPEC-007 §7-D D-1)*
- **M-6-a** **AI 증분은 즉시 반영한다**(2026-09-05 확정). 배치 결과가 들어오는 대로 AI 탭에 나가고, **몇 번째 배치까지 반영됐는지**를 화면이 표시한다(「배치 2회 → 3회 → 종결」). 버퍼링하지 않는다. 그 회차는 컬럼으로 두지 않고 `meeting_batch_run` 의 성공분 최대 `seq` 에서 **파생**한다(G-7).
- **M-7** 회의 중 배치는 **증분 추가만** — 기존 `track='ai'` 줄을 UPDATE 하지 않는다. 전체 재정리(DELETE + INSERT)는 **종료 후 최종 배치 한 번**뿐이다(DEC-003 §4).
- **M-8** 통합본(`track='merged'`)의 본문은 **사람이 쓴 문장 그대로**다. AI 에서 가져오는 것은 `evidence` 와, AI 트랙에만 있는 내용의 추가분뿐이다(DEC-003 §4).
- **M-8-a** **통합 줄은 원본을 가리킨다**(2026-09-06 · SPEC-008 §4 통합 규칙). `track='merged'` 줄은 `source_human_line_id`·`source_ai_line_id` 중 **최소 하나**를 갖고, 다른 트랙의 줄은 둘 다 `NULL` 이다(CHECK). 조합의 뜻 — 사람 id 만: 사람 줄 계승 · 둘 다: 사람 줄 계승 + 그 AI 줄의 `evidence`(과 빈 `detail`) 복사 · AI id 만: AI 에만 있는 내용의 추가분(AI 줄 그대로 복사). **모든 사람 줄이 정확히 한 번 계승된다**(부분 UNIQUE) · **한 AI 줄은 한 통합 줄에만 붙는다**(부분 UNIQUE). 모델은 참조 id 와 자리만 내고 **본문은 서버가 원본에서 복사**한다 — 모델이 문장을 낼 자리가 없다(DEC-003 OQ-7 「구조로 판정」).
- **M-9** `meeting_transcript` 에는 **확정 토큰만** 들어간다. 잠정 토큰은 화면 표시용으로 흘려보내고 저장하지 않는다(DEC-003 §3).
- **M-10** `speaker_label` 은 **익명**(`화자 1`/`화자 2`)이다. 참석자·발언자 이름 컬럼을 두지 않는다(DEC-003 §2). Soniox 는 **세션당 최대 15명**을 라벨링한다(soniox).
- **M-11** `at_ms` 는 **회의 시작 기준 오프셋**이다 — 그 기준점은 **`meeting.recording_started_at`** 이다(M-1-a). 근거 칩의 `evidence` 도 같은 기준이라 벽시계 시각과 섞지 않는다.
- **M-12** `ai_session_id` 는 **회의 하나에 하나**다. 매 배치가 이 세션을 `resume` 한다 — 배치마다 새 세션을 만들지 않는다(DEC-003 §STT).
- **M-13** **`recording_path` 는 영구 보관**이다. 회의록을 소프트 딜리트해도 녹음 파일을 지우지 않는다. 보존 기간·자동 삭제 정책이 없다(DEC-003 §4·§6).
- **M-14** `meeting_line.task_id` 는 **버튼을 눌러 업무가 실제로 생기거나 연결됐을 때만** 채워진다. 줄을 적는 것만으로는 안 생긴다(DEC-003 §5).
- **M-14-a** `pending_change` 가 담는 것은 **세 가지뿐**이다(2026-09-05 확정) — **기한**(`task.due_date`, 업무가 소유 · `schedule` 은 파생) · **상태**(전이 규칙을 따르고 완료로 가면 **완료 게이트**를 통과해야 한다 — DEC-002 §4) · **note**(업무 **메모에 새 항목 추가**, 기존 필드를 덮어쓰지 않는다). 그 밖의 필드는 담지 않는다.
- **M-15** 배치 결과의 `task_id` 는 **웜스타트로 준 업무 ID 화이트리스트** 안에 있어야 한다. 밖이면 `task_id` 를 떼고 `kind='action'` 으로 강등하되 **본문은 살린다**(DEC-003 §7).
- **M-15-a** 화이트리스트는 회의의 프로젝트를 따른다. **무소속 회의에는 무소속 업무**(프로젝트 없는 업무)를 준다(2026-09-05 확정, DEC-003 §4).
- **M-16** JSON 스키마를 위반한 배치 결과는 **행 하나도 넣지 않고 통째로 폐기**한다. 부분 파싱 금지 — `meeting_batch_run.status='discarded'` 로 남기고 그 구간을 다음 배치에 합친다(DEC-003 §7).
- **M-17** 첨부는 **두 갈래**다(2026-09-06 개정 · SPEC-006 §7 · SPEC-007 §7-C · DEC-003 §1 표) — `kind='doc'` 은 자료함 문서 참조(`document_id`, **md 만** — DEC-004 §8), `kind='link'` 는 URL 링크(`url`·`label`). `kind` 에 따라 채워지는 컬럼이 갈리고 CHECK 로 강제한다(`task.md` T-9-a 와 같다). **로컬 파일 업로드 경로는 v1 에 없다** — UI 는 v2 게이트다. **회의 중 md 작성(`source=local`·`agendaId`)은 v2** — v1 에 문서 생성 경로가 없다(DEC-004 §8 · §A-11). *(이전 판 「첨부는 자료함 문서 참조뿐」은 이 개정으로 폐기)*
- **M-18** **300분 초과 회의를 다루지 않는다** — 세션 경계·재연결 컬럼을 만들지 않는다(DEC-003 §4).
- **M-19** **`ai_headline` 은 통합본 생성(종료 파이프라인 ②)과 같은 응답에서 온다**(2026-09-06 · DEC-003 §1 표 · §4). 통합 출력 JSON 에 `headline` 필드 하나가 더 붙는 것이고 **별도 호출을 만들지 않는다.** 그래서 ① **통합이 성공한 회의에만 값이 있다** — `integration_state='succeeded'` 와 함께 같은 트랜잭션에서 채운다. ② **통합이 실패하면 `NULL` 로 남는다** — 부분 저장하지 않는다(통합 시도 실패는 그 시도 전체의 실패다 — SPEC-008 §4). ③ **재생성이 없다**(DEC-003 §4 「통합본 재생성 없음」) — 정상 생성분의 한 줄 요약을 다시 받는 경로가 없고, `/integrate`(다시 생성)는 `ended`+`failed` 에서만 돈다(M-4). 그때는 통합본과 함께 처음 채워진다. ④ 사람이 편집하지 않는다 — 편집 범위(DEC-003 §5)에 없다. 표시는 SPEC-008 U-1(디자인 시스템 [09] L727~733) 의 몫이다.
- **M-20** **종료 후 줄 삭제는 회의록 탭의 줄만 지운다**(2026-09-06 · DEC-003 §1 표 · §5). 대상 트랙은 편집 모드와 같다 — `integration_state='succeeded'` 면 **`merged`**, `failed` 면 **`human`**. **`ai` 트랙·`meeting_transcript`·녹음은 남는다**(DEC-003 §6 「AI 탭은 통합본과 별개로 남는다」) — 근거 칩이 가리킬 원본이 있어야 한다. 규칙 셋.
  - **원본을 따라 지우지 않는다.** `merged` 줄을 지워도 `source_human_line_id`·`source_ai_line_id` 가 가리키는 `human`·`ai` 줄은 그대로다. `human` 줄(실패 상태)을 지울 때도 같은 사람 줄을 계승한 `merged` 줄은 없다(실패 상태에는 `merged` 행이 0건 — SPEC-008 §4). 지우는 방향은 항상 **가리키는 쪽 → 없어짐**이고 가리켜지는 쪽은 안 건드린다.
  - **하드 딜리트다.** 근거 — `../README.md` §0-1 「모든 자식 행은 하드 삭제 · v1 에 복원 창구가 없다」가 그대로 적용된다. 통합 줄은 원본에서 복사한 **파생물**이라 지워도 원천(`human`·`ai`·`transcript`)이 남고, 되살릴 화면이 없어 표식을 남길 이유가 없다. 회의 본체만 소프트 딜리트다(DEC-003 §4). `deleted_at` 을 줄에 두지 않는다 — 두면 부분 UNIQUE 와 「정확히 한 번 계승」 검증이 삭제분을 어떻게 셀지 갈라진다.
  - **업무가 생성된 줄을 지워도 업무는 지우지 않는다**(DEC-003 §8 「회의록은 업무를 만들고 갱신만 한다」). `task_id` 가 가리키던 업무는 그대로 남고, 회의록 쪽 연결만 사라진다. `pending_change` 로 대기 중이던 갱신은 줄과 함께 없어진다(업무에 반영된 적이 없다).
  - **줄 순서 변경은 여전히 없다**(DEC-003 §1 표). `order_index` 를 사람이 고치는 표면은 없다 — 지운 뒤 빈 자리는 그대로 두고 화면이 순서대로 그린다.

## Related Specs / Works

- SPEC-006 회의록 — 목록·생성·시작 전 (첨부 두 갈래 · 안건 `state` NULL · `meeting` 인덱스)
- SPEC-007 회의록 — 회의 중 (`recording_started_at` · 안건 `active` · `source_agenda_id` · M-6 정정)
- SPEC-008 회의록 — 종료·통합·편집 (`source_*_line_id` · `job` · `ai_headline` · 줄 삭제)
- 참조: `domains/account.md`(유형·프로젝트) · `domains/task.md`(업무 생성·갱신 · 첨부 T-9) · `domains/calendar.md`(시간) · `domains/library.md`(첨부)

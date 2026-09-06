---
type: architecture
id: DOMAIN-002
title: "task — 업무와 완료 게이트"
status: draft
product: "task-management"
created_at: 2026-09-04
updated_at: 2026-09-04
tags:
  - product/task-management
  - doc/architecture
  - architecture/database
links:
  baselines: [BASE-002]
  decisions: [DEC-002, DEC-001, DEC-004, DEC-005]
  specs: []
  works: []
  related: []
---

# task

업무 본체와 그 자식들(할일·메모·로그·첨부·연관). **시간은 여기 없다** — `schedule` 이 소유한다.

## Purpose

DEC-002 의 필드·상태·게이트를 담는다. 업무는 두 입구를 갖는다 — 사람이 만드는 것과 회의록의 액션 줄이 만드는 것(DEC-003 §5).

## Entities / Tables

| Entity/Table | Purpose | Notes |
|---|---|---|
| `task` | 업무 본체 | 소프트 딜리트. `work_type_id` 필수, `project_id` 는 0..1, **일정 5필드를 소유**(`start_date`·`due_date` 계획 / `started_at`·`completed_at`·`cancelled_at` 실적 — T-1) |
| `task_todo` | 할일 | 진행률 = `done` 개수 / 전체 |
| `task_memo` | 메모 | 사람 기록. 작성자 표기 없음(단일 사용자) |
| `task_log` | 시스템 로그 | **사용자 입력·수정 불가.** 서비스만 쓴다. 전이 로그는 `from_status`·`to_status` 를 함께 갖는다(T-8-a) |
| `task_attachment` | 참고자료 · 결과자료 | `role ∈ {reference, deliverable}` · `kind ∈ {doc, link}` |
| `task_relation` | 연관업무 | 무방향 — `low_task_id < high_task_id` 로 한 행만 |

## Invariants

- **T-1** **업무가 일정을 소유한다.** **일정 필드는 5개다** — 계획 2 + 실적 3 (2026-09-06 개정 — §A-4 번복 · DEC-002 §「일정 필드 4개 확정」 + `cancelled_at` 승격).

  | 컬럼 | 뜻 | 누가 |
  |---|---|---|
  | `start_date` `DATE NULL` | **계획 시작** | 사용자 |
  | `due_date` `DATE NULL` | **계획 종료 = 기한** | 사용자 |
  | `started_at` `TIMESTAMPTZ NULL` | **실적 시작** — `in_progress` 전이 시각 | 시스템 |
  | `completed_at` `TIMESTAMPTZ NULL` | **실적 종료** — `done` 전이 시각 | 시스템 |
  | `cancelled_at` `TIMESTAMPTZ NULL` | **실적 취소** — `cancelled` 전이 시각 | 시스템 |

  「기한」을 계획 종료와 **따로 두지 않는다** — 개인 워크스페이스라 요청자가 없어 갈릴 상대가 없다.
  **업무에 시간은 없다** — 「시간 지정」과 `due_start_time`/`due_end_time` 은 **제거됐다**(2026-09-06 · DEC-002).
  시간을 갖는 것은 회의뿐이고 `meeting.start_at`·`end_at` 이 소유한다.
  **리스트 기본 정렬·D-day 는 조인 없이 `task` 만 읽는다.**

- **T-1-c** **실적 3개는 전이 로그(T-8-a)에서 파생 가능하지만 컬럼으로 승격한다.** 「오늘 완료 처리하면 오늘 완료 칸에
  간다」(DEC-002)가 조회·정렬에서 매번 쓰이므로 로그를 되짚지 않는다.

  **값을 대입하지 않는다 — 로그에서 다시 계산한다**(`sync_actuals`). 전이가 로그를 **쓴 뒤**, 실행취소가 로그를 **지운 뒤**
  **같은 트랜잭션**에서 재계산하므로 로그와 컬럼이 갈릴 수 없다. 실행취소가 「무엇을 되돌릴지」를 따로 기억하지 않는다 —
  되돌린 뒤의 로그를 읽으면 되돌린 뒤의 실적이 나온다. **`NOW()` 를 쓰지 않는다**(로그 행의 `created_at` 이 전이 시각의 정본).

  > 이 설계가 **T-8-a 의 「컬럼을 만들면 두 번째 사실이 생긴다」를 무력화했다.** 컬럼은 로그의 materialization 이다.

- **T-1-d** **`schedule` 은 계획 기간의 파생이다**(DEC-005 §3 개정). 실적(`started_at`·`completed_at`·`cancelled_at`)은 **캘린더에 쓰지 않는다.**

  | 업무가 가진 것 | 캘린더 |
  |---|---|
  | `start_date` + `due_date` | **기간 일정**(디자인 시스템 [11] Period Bar) — 종일 밴드 |
  | `due_date` 만 | 종일 일정 **하루** |
  | **`start_date` 만** | 시작일 하루에 종일 일정. **끝이 없어 무한 바를 그릴 수 없다**(2026-09-06 코디 판단) |
  | 둘 다 없음 | **캘린더에 뜨지 않는다.** 「내 업무」 오늘 화면에만 매일 뜬다(DEC-002) |

  업무는 `schedule` 을 직접 쓰지 않는다(`../README.md` §3).
- **T-1-a** 기한이 없으면: 리스트 칸 비움 · **칸반 카드 우측은 「미정」** · 기본 정렬 맨 아래. ~~월 소속은 생성일 기준~~ → **폐기.** **미완료인 동안 매일 「오늘」에 뜬다**(2026-09-06 · DEC-002 조회 규칙 R-2).
- ~~**T-1-b**~~ **폐기**(2026-09-06 · DEC-002) — `due_start_time`·`due_end_time` 컬럼과 그 CHECK 를 **제거**했다. 업무는 날짜 단위이고 시간을 갖지 않는다.
- **T-2** `work_type_id` 는 **필수**다. 02-data-model 의 고정 enum 3종은 폐기됐다(DEC-002 §3 · §A-1).
- **T-3** `project_id` 는 **N:1, 0..1**. M:N 이 아니다. 「프로젝트 없음」은 **표시 계층의 가상 그룹**이고 저장 계층에 기본 프로젝트 행을 만들지 않는다(DEC-002 §3).
- **T-4** `status` 는 **4종만 저장한다** — `todo` · `in_progress` · `done` · `cancelled`. **「지연」은 컬럼이 아니다** — 종료일 경과 + 완료·취소 아님으로 조회 시 파생한다(DEC-002 §3·§4 · G-7).
- **T-5** **완료 게이트** — `done` 으로 가려면 `deliverable` 첨부가 1건 이상이거나 `completion_result` 가 비어 있지 않아야 한다. 미충족이면 **상태가 바뀌지 않는다**. 05-status §완료 4 의 「막지 않는다」는 뒤집혔다(DEC-002 §4 · §A-3).
- **T-6** 전이 그래프를 벗어나는 변경은 거부한다. **완료 → 취소는 불가**(DEC-002 §4).
- **T-7** `cancel_reason` 은 `status='cancelled'` 일 때만 값이 있다. **취소는 상태이지 유형이 아니다** — `work_type` 에 「취소」를 만들지 않는다(DEC-002 OQ-5 · §A-2).
- **T-8** 모든 상태 전이·할일 완료·첨부는 **같은 트랜잭션에서 `task_log` 한 줄을 남긴다**(DEC-002 §6). 로그 없는 전이는 없다.
- **T-8-a** **전이 로그는 `from_status`·`to_status` 를 컬럼으로 갖는다**(리비전 `0003`, 2026-09-06 추가). 전이 로그만 두 값을 갖고 나머지 로그는 둘 다 `NULL` 이다(CHECK 로 강제).
  - **왜 컬럼인가** — 실행취소가 「마지막 로그가 전이인가 + 직전 상태는 무엇인가」를 판정한다. 그걸 **한국어 본문에서 되파싱하면 문구를 바꾸는 순간 조용히 깨진다.** 로그 본문은 사람이 읽는 것이고 판정 근거가 아니다.
  - ~~**`cancelledAt` 도 여기서 나온다** — 별도 컬럼을 만들면 로그와 어긋날 수 있는 두 번째 사실이 생긴다.~~
    → **2026-09-06 개정. `cancelled_at` 을 컬럼으로 둔다**(T-1 실적 3필드).
    **전제가 깨졌다** — `sync_actuals`(T-1-c)가 값을 대입하지 않고 **로그에서 다시 계산**한다. 컬럼은 로그의 materialization 일 뿐이라 **어긋날 수 있는 두 번째 사실이 아니다.** 전이가 로그를 쓴 뒤, 실행취소가 로그를 지운 뒤 **같은 트랜잭션**에서 재계산하므로 둘은 갈릴 수 없다.
    승격 근거 셋 — ① 실적 3개가 같은 성격인데 둘만 컬럼이면 비대칭에 설명이 필요하다 ② 조회 규칙 R-4 의 취소 갈래가 **스칼라 서브쿼리 없이** 완료와 같은 모양이 된다 ③ `task_log` 본문을 되파싱하지 않는다는 T-8-a 의 원래 취지는 그대로 지켜진다(근거는 `to_status` 컬럼이다).
- **T-8-b** `task_log` 를 **DELETE 하는 경로는 실행취소 하나뿐**이다. 그 밖에서는 지우지 않는다(SPEC-004 · WORK-005 §Pre-deploy).
- **T-9** 첨부는 **두 종류**다(2026-09-05 확정) — `kind='doc'` 은 자료함 문서(`document_id`, **md 만** — DEC-004 §8), `kind='link'` 은 **URL 링크**(`url` + `label`). DEC-004 의 「md 만」 제약은 **파일 업로드**에 대한 것이고 링크는 별개 축이다(DEC-002 §8). 로컬 파일 업로드 경로는 v1 에 없다.
- **T-9-a** `kind` 에 따라 채워지는 컬럼이 갈린다 — `doc` 이면 `document_id` 만, `link` 면 `url`·`label` 만. CHECK 로 강제한다.
- **T-10** `task_relation` 은 **무방향 1행**이다. 조회는 두 컬럼을 모두 본다. 자기 자신과의 연관은 만들지 않는다.
- **T-11** 소프트 딜리트된 업무는 목록·칸반·캘린더·집계에서 빠진다. **자식 행은 지우지 않는다** — 부모 필터로 함께 사라진다(§0-1).

## Related Specs / Works

- SPEC-00x 내 업무 (DEC-002 Resulting Spec)
- 참조: `domains/account.md`(유형·프로젝트) · `domains/calendar.md`(시간) · `domains/meeting.md`(업무 생성·갱신 입구)

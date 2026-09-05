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
| `task` | 업무 본체 | 소프트 딜리트. `work_type_id` 필수, `project_id` 는 0..1, **기한(`due_date`)을 소유** |
| `task_todo` | 할일 | 진행률 = `done` 개수 / 전체 |
| `task_memo` | 메모 | 사람 기록. 작성자 표기 없음(단일 사용자) |
| `task_log` | 시스템 로그 | **사용자 입력·수정 불가.** 서비스만 쓴다 |
| `task_attachment` | 참고자료 · 결과자료 | `role ∈ {reference, deliverable}` · `kind ∈ {doc, link}` |
| `task_relation` | 연관업무 | 무방향 — `low_task_id < high_task_id` 로 한 행만 |

## Invariants

- **T-1** **업무가 기한을 소유한다**(2026-09-05 개정). 디자인의 `startDate`/`endDate` 두 필드는 **`due_date` 하나로 정리**됐고, 시간까지 지정하면 `due_start_time`/`due_end_time` 이 붙는다. **리스트 기본 정렬·D-day 는 조인 없이 `task` 만 읽는다.** `schedule` 은 이 값의 **파생**이고 업무는 그쪽을 직접 쓰지 않는다(DEC-005 §3 · §A-4 · `../README.md` §3).
- **T-1-a** 기한이 없으면: 리스트 칸 비움 · D-day 미표시 · 기본 정렬 맨 아래 · 월 소속은 생성일 기준(DEC-002 §3).
- **T-1-b** `due_start_time` 과 `due_end_time` 은 **함께 있거나 함께 없다.** 시간만 있고 `due_date` 가 없는 상태를 만들지 않는다(CHECK 로 강제).
- **T-2** `work_type_id` 는 **필수**다. 02-data-model 의 고정 enum 3종은 폐기됐다(DEC-002 §3 · §A-1).
- **T-3** `project_id` 는 **N:1, 0..1**. M:N 이 아니다. 「프로젝트 없음」은 **표시 계층의 가상 그룹**이고 저장 계층에 기본 프로젝트 행을 만들지 않는다(DEC-002 §3).
- **T-4** `status` 는 **4종만 저장한다** — `todo` · `in_progress` · `done` · `cancelled`. **「지연」은 컬럼이 아니다** — 종료일 경과 + 완료·취소 아님으로 조회 시 파생한다(DEC-002 §3·§4 · G-7).
- **T-5** **완료 게이트** — `done` 으로 가려면 `deliverable` 첨부가 1건 이상이거나 `completion_result` 가 비어 있지 않아야 한다. 미충족이면 **상태가 바뀌지 않는다**. 05-status §완료 4 의 「막지 않는다」는 뒤집혔다(DEC-002 §4 · §A-3).
- **T-6** 전이 그래프를 벗어나는 변경은 거부한다. **완료 → 취소는 불가**(DEC-002 §4).
- **T-7** `cancel_reason` 은 `status='cancelled'` 일 때만 값이 있다. **취소는 상태이지 유형이 아니다** — `work_type` 에 「취소」를 만들지 않는다(DEC-002 OQ-5 · §A-2).
- **T-8** 모든 상태 전이·할일 완료·첨부는 **같은 트랜잭션에서 `task_log` 한 줄을 남긴다**(DEC-002 §6). 로그 없는 전이는 없다.
- **T-9** 첨부는 **두 종류**다(2026-09-05 확정) — `kind='doc'` 은 자료함 문서(`document_id`, **md 만** — DEC-004 §8), `kind='link'` 은 **URL 링크**(`url` + `label`). DEC-004 의 「md 만」 제약은 **파일 업로드**에 대한 것이고 링크는 별개 축이다(DEC-002 §8). 로컬 파일 업로드 경로는 v1 에 없다.
- **T-9-a** `kind` 에 따라 채워지는 컬럼이 갈린다 — `doc` 이면 `document_id` 만, `link` 면 `url`·`label` 만. CHECK 로 강제한다.
- **T-10** `task_relation` 은 **무방향 1행**이다. 조회는 두 컬럼을 모두 본다. 자기 자신과의 연관은 만들지 않는다.
- **T-11** 소프트 딜리트된 업무는 목록·칸반·캘린더·집계에서 빠진다. **자식 행은 지우지 않는다** — 부모 필터로 함께 사라진다(§0-1).

## Related Specs / Works

- SPEC-00x 내 업무 (DEC-002 Resulting Spec)
- 참조: `domains/account.md`(유형·프로젝트) · `domains/calendar.md`(시간) · `domains/meeting.md`(업무 생성·갱신 입구)

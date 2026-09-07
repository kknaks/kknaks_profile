---
type: architecture
id: DOMAIN-004
title: "calendar — schedule 파생과 겹침 차단"
status: draft
product: "task-management"
created_at: 2026-09-04
updated_at: 2026-09-04
tags:
  - product/task-management
  - doc/architecture
  - architecture/database
links:
  baselines: [BASE-005]
  decisions: [DEC-005, DEC-002, DEC-003]
  specs: []
  works: []
  related: []
---

# calendar

**캘린더는 데이터를 소유하지 않는다.** `schedule` 조차 소유가 아니라 **파생**이다 — 원본은 업무의 기한과 회의의 일시다.

## Purpose

DEC-005 §3 이 분리한 `schedule` 을 담는다. 파생이 된 뒤에도 분리한 이유는 그대로다 — **캘린더가 두 소스를 한 번에 읽고, 겹침 검사를 한 곳에서 한다.** v2 외부 캘린더가 붙을 자리도 여기다.

## Entities / Tables

| Entity/Table | Purpose | Notes |
|---|---|---|
| `schedule` | **시간축 배치의 파생 테이블** | `source_type ∈ {task, meeting}` (v2: `external`) |

캘린더 전용 테이블은 이것뿐이다. 뷰(월·주·일)는 같은 데이터의 세 표현이라 저장 구조가 갈리지 않는다(F-7).

## Invariants

> **2026-09-05 개정.** 이전 판(「시간은 `schedule` 이 단독 소유」)은 폐기됐다. 상세는 `../README.md` §3.

- **C-1** **원본은 각 영역이 갖는다** — 업무의 기한은 `task.due_date`(+`due_start_time`/`due_end_time`), 회의의 일시는 `meeting.start_at`/`end_at`. `schedule` 은 그 **파생**이다(DEC-005 §3 · §A-4).
- **C-2** **`schedule` 을 직접 쓰지 않는다.** 원본을 고치면 `schedule_service` 가 같은 트랜잭션에서 다시 만든다.
- **C-3** **방향은 한 쪽뿐이다.** 캘린더 드래그는 **원본을 고치고** 결과가 `schedule` 로 내려온다. 원본이 하나라 어긋날 자리가 없다(DEC-005 §3).
- **C-4** `UNIQUE (source_type, source_id)` — 업무·회의는 일정을 **0..1개** 갖는다. 회의는 사실상 항상 있고, **기한도 시간도 없는 업무는 행이 없다**(DEC-002 §3).
- **C-5** `schedule` 이 담는 것은 **시간축 배치뿐**(`start_at`·`end_at`·`is_all_day`)이다. **기한 같은 도메인 속성을 담지 않는다.**
- **C-5-a** 기한만 있으면 **종일 일정**(`is_all_day=true`), 시간까지 지정하면 **시간 일정**으로 파생한다. 종일의 범위는 그 날짜 `00:00`~다음 날 `00:00`(KST)이다.
- **C-5-b** **FK 를 걸지 않는다.** v2 `external` 은 우리 테이블에 원본 행이 없어 FK 가 그 자리를 막는다. 참조 정합은 서비스 불변식과 테스트로 지킨다.
- **C-5-c** **소프트 딜리트·취소 상태를 `schedule` 에 복제하지 않는다.** 조회·검사는 `source_type` 으로 갈라 원본을 조인해 거른다.
- **C-6** **겹침 검사 대상은 `is_all_day = false` 인 일정끼리만**이다. 종일·기간 일정은 검사하지 않는다 — 기간에 걸친 일이지 그 시간을 점유한 게 아니다(DEC-005 §7).
- **C-7** **종류를 가리지 않는다** — 업무↔회의도 서로 막는다(DEC-005 OQ-4).
- **C-8** 판정식은 `start_at < :end AND end_at > :start`. **경계 접촉(10–11 / 11–12)은 겹침이 아니다**(DEC-005 §7).
- **C-9** 겹치면 **거부한다.** 경고만 하고 통과시키지 않는다(DEC-005 §7). 검사는 **원본을 쓰기 전에 파생될 배치로** 한다 — 걸리면 원본도 바뀌지 않는다.
- **C-10** 취소된 일정·소프트 딜리트분은 검사에서 빠진다(DEC-005 §7).
- **C-11** 캘린더는 **자체 로그를 남기지 않는다.** 드래그로 바꾼 일정도 원 영역의 로그(`task_log`)에 기록된다(DEC-005 §6).
- **C-12** 캘린더에서 **삭제하지 않는다.** 삭제는 원 영역에서만(DEC-005 §5).
- **C-13** 유형 색은 `work_type.color_token` 을 쓴다. **유형 4색 고정은 폐기**됐다(DEC-005 §3 · §A-10).
- **C-14** 유형 분포 카운트는 **기간 일정도 포함**한다 — 세는 집합과 거르는 집합을 일치시킨다(DEC-005 OQ-3 · §A-10).

## Related Specs / Works

- SPEC-00x 캘린더 (DEC-005 Resulting Spec — **일정 테이블 분리는 DB 스키마 선행 사항**)
- 참조: `domains/task.md` · `domains/meeting.md`

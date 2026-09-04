---
type: architecture
id: DOMAIN-004
title: "calendar — schedule 단독 소유와 겹침 차단"
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

**캘린더는 데이터를 소유하지 않는다.** 소유하는 것은 `schedule` 테이블 하나 — 업무와 회의의 시간이다.

## Purpose

DEC-005 §3 이 분리한 `schedule` 을 담고, 캘린더가 두 소스를 한 번에 읽고 겹침 검사를 한 곳에서 하게 만든다. v2 외부 캘린더가 붙을 자리도 여기다.

## Entities / Tables

| Entity/Table | Purpose | Notes |
|---|---|---|
| `schedule` | **업무·회의 시간의 단독 소유자** | `source_type ∈ {task, meeting}` (v2: `external`) |

캘린더 전용 테이블은 이것뿐이다. 뷰(월·주·일)는 같은 데이터의 세 표현이라 저장 구조가 갈리지 않는다(F-7).

## Invariants

- **C-1** **`task` 와 `meeting` 에 시간 컬럼이 없다.** 있으면 버그다(DEC-005 §3 · §A-4).
- **C-2** `UNIQUE (source_type, source_id)` — 업무·회의는 일정을 **0..1개** 갖는다. 회의는 사실상 항상 있고, 업무는 무일정을 허용한다(DEC-005 §3 · DEC-002 §3).
- **C-3** **FK 를 걸지 않는다.** v2 `external` 은 우리 테이블에 원본 행이 없어 FK 가 그 자리를 막는다. 참조 정합은 서비스 불변식과 테스트로 지킨다.
- **C-4** 업무·회의 생성과 `schedule` 행 생성은 **같은 트랜잭션**이다.
- **C-5** **소프트 딜리트·취소 상태를 `schedule` 에 복제하지 않는다.** 조회·검사는 `source_type` 으로 갈라 원본을 조인해 거른다 — 같은 사실을 두 곳에 두면 어긋난다(DEC-005 §3 의 판단을 상태에 확장).
- **C-6** **겹침 검사 대상은 `is_all_day = false` 인 일정끼리만**이다. 종일·기간 일정은 검사하지 않는다 — 기간에 걸친 일이지 그 시간을 점유한 게 아니다(DEC-005 §7).
- **C-7** **종류를 가리지 않는다** — 업무↔회의도 서로 막는다(DEC-005 OQ-4).
- **C-8** 판정식은 `start_at < :end AND end_at > :start`. **경계 접촉(10–11 / 11–12)은 겹침이 아니다**(DEC-005 §7).
- **C-9** 겹치면 **거부한다.** 경고만 하고 통과시키지 않는다(DEC-005 §7).
- **C-10** 취소된 일정·소프트 딜리트분은 검사에서 빠진다(DEC-005 §7).
- **C-11** 캘린더는 **자체 로그를 남기지 않는다.** 드래그로 바꾼 일정도 원 영역의 로그(`task_log`)에 기록된다(DEC-005 §6).
- **C-12** 캘린더에서 **삭제하지 않는다.** 삭제는 원 영역에서만(DEC-005 §5).
- **C-13** 유형 색은 `work_type.color_token` 을 쓴다. **유형 4색 고정은 폐기**됐다(DEC-005 §3 · §A-10).
- **C-14** 유형 분포 카운트는 **기간 일정도 포함**한다 — 세는 집합과 거르는 집합을 일치시킨다(DEC-005 OQ-3 · §A-10).

## Related Specs / Works

- SPEC-00x 캘린더 (DEC-005 Resulting Spec — **일정 테이블 분리는 DB 스키마 선행 사항**)
- 참조: `domains/task.md` · `domains/meeting.md`

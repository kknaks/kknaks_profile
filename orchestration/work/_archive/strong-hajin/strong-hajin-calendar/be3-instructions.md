# [backend] Phase BE-3 — 겹침 검증 · 배정 쪽

너는 **strong-hajin `backend` 워커**다. **앞 판을 한 워커는 죽었다 — 너는 맥락이 없다.**
먼저 읽어라:

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/backend/role.md` (+ 같은 폴더 `rules.md`·`skills.md`·`tools.md`·`workflow.md`)
- 코드 레포 루트 `AGENTS.md`
- `orchestration/work/strong-hajin-calendar/be2-report.md` — **앞 판이 만든 것**(BE-1·BE-2)의 실물 API 계약과 구현 요약. 네가 그 위에 얹는다

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-calendar`

> ⚠ 1루프는 전부 커밋됐다 (`1c15d02` · `2a85176` · `c5b109d` · `aa8576b`). 네 새 변경만 uncommitted.
> ⚠ **이번 판은 회의 도메인을 건드리지 않는다** — 그건 BE-4 다. 당겨 하지 마라.
> ⚠ 커밋·push 금지.

## 작업 지시서

`…/30-work/work-004-calendar-scheduling.md` 의 **`Phase BE-3`** — 작업과 완료 판정 그대로.
계약은 `…/20-spec/spec-004-calendar-scheduling.md` **v0.3.1** (커밋 `bfe299a`) **§2.9**.
왜 그렇게 정했는지는 `…/10-decision/decision-003-calendar.md` **증보 8 K22**.

한 줄로: **`overlapping_blocks` 한 함수를 세우고 배정 생성·시각 변경에 건다.**

## 틀리기 쉬운 자리 — 여섯

1. **반열림 `[시작, 끝)`** — 경계가 닿는 것은 **겹침이 아니다**. 10:00–11:00 과 11:00–12:00 은 선다.
   **새 규칙이 아니다** — `meetings_visible_to` docstring 이 이미 같은 규칙을 쓴다. **그것을 따라라.**
2. **읽는 문은 하나다** — `overlapping_blocks(member_ids, 구간)` 가 **두 표를 조회**한다
   (`task_schedules` + `meetings`). 겹침 검사가 전부 이 함수를 지난다.
   **BE-4 가 이 함수를 그대로 재사용한다** — 회의 쪽을 위해 지금부터 `member_ids` 를 **복수**로 받아라.
3. **타입이 다르다** — 회의는 `timestamptz`, 배정은 `Date` + `Time`. **Asia/Seoul 기준**으로 맞춘다.
   **자정을 넘는 회의는 날짜별로 쪼갠다** — 배정은 자정을 못 넘지만 회의는 넘는다.
4. **영수증이 겹침보다 먼저다 (K12).** 같은 멱등 키의 재전송은 **자기가 방금 만든 배정과
   같은 구간**이라 **자기 자신과 겹친다.** 영수증을 먼저 안 보면 **드래그 연타가 409 를 맞는다** —
   그게 멱등 키가 있는 이유다. SPEC §5 가 「이 목록은 닫힌 열거가 아니다」로 못 박았다.
5. **배정 쪽은 「나의 시간만」 본다** — 남의 일정은 애초에 안 나온다. 그건 BE-4(회의) 몫이다.
6. **`TASK_SCHEDULE_OVERLAP` 409** — 문구는 SPEC Case Matrix 그대로.

## 하지 마라 — **이 Phase 의 가장 흔한 오답**

**겹침을 DB 제약으로 올리려 하지 마라.** `EXCLUDE USING gist` 로 막고 싶어지는데
**두 표라 못 건다.** 「하루 한 칸」은 부분 unique 로 DB 가 막지만 **겹침은 application 이 막는다.**
그 차이는 SPEC §2.9 가 **한계로 인정한 것**이다 — 없애려 들지 말고 **검사와 저장을 한 트랜잭션**에 둬라.

## 검수가 이 Phase 로 넘긴 것 — 하나

**완료 판정에 자정 분할 증명이 없다.** 자정 분할의 **구현은 BE-3**(`overlapping_blocks` 안)인데
인수조건이 BE-4 에 있다. 구멍은 아니지만 **네가 만든 로직을 네가 증명하지 않고 넘어간다.**

> **완료 판정에 한 줄 더하고 그 테스트를 써라** — 「자정을 넘는 회의와 겹치는 배정이 막힌다」.
> 배정 쪽도 회의를 블록으로 읽으므로 BE-3 에서 증명할 수 있다.

## allowed_paths

`backend/` · `docker-compose.yml` · `Makefile`. **`docs/` 는 이번 Phase 에 필요 없다**(대장은 BE-4).
`frontend/`·`para/`·`orchestration/` 금지.

## 검증

```
make test-unit
make test-contract
make test-postgres POSTGRES_TEST_URL=postgresql+psycopg://ax:ax@127.0.0.1:54329/ax_test_calendar
```

기준선: `test-unit` 356p/0f · `test-contract` 1117p/2f(`material_worker_recovery` **기존 flaky**,
직렬로 돌리면 통과 — 무관으로 분리) · `test-postgres` 89p/0f.

**새 라우트가 없으므로 운영 대장은 안 깨져야 한다.** 깨지면 뭔가 잘못한 것이다.

## 범위 제약

- 계약을 다시 정하지 마라. 모순은 **코디에게 물어라** — 조용히 정하지 마라
- **회의 생성·시각 변경에 손대지 마라** (BE-4)
- `approval` 필드도 BE-4 다
- 커밋·push 금지

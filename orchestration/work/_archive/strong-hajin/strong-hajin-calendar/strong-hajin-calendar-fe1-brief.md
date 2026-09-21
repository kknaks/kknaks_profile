# [frontend] Phase FE-1 — 화면 골격: 3분할 · 좌측 레일 · 월/주 뷰

너는 **strong-hajin `frontend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- 그 다음 코드 레포 루트의 `AGENTS.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-calendar`

> ⚠ **백엔드는 끝났고 커밋됐다** (BE-1 `1c15d02` · BE-2 `2a85176`). API 가 **실제로 돈다.**
> ⚠ **네 변경만 uncommitted 로 남아야 한다.** 커밋·push 금지.
> ⚠ **이번엔 읽기까지다.** 드래그·손잡이·쓰기는 **FE-2** 다. 당겨 하지 마라.

## 1. 작업 지시서

`…/30-work/work-004-calendar-scheduling.md` 의 **`Phase FE-1`** — 작업 0~8 · DS-gaps 처분표 ·
완료 판정. **그대로 따라라.**

계약은 `…/20-spec/spec-004-calendar-scheduling.md`, 왜 그렇게 정했는지는
`…/10-decision/decision-003-calendar.md`(증보 **K1~K16**).
조사는 `orchestration/work/strong-hajin-calendar/fe-survey-report.md` (727줄 — 네가 앞서 썼다).

## 2. 실제 API 계약 — **BE 워커가 돌려 본 실물이다. 추정하지 마라**

전문은 `orchestration/work/strong-hajin-calendar/be2-report.md` §5 (288줄). **반드시 읽어라.**
여기엔 **틀리기 쉬운 자리만** 옮긴다.

### `GET /api/calendar?from=&to=` → 200, **한 배열**, `kind` 로 가름

```json
{"kind":"task","task_id":"…","title":"…","state":"open",
 "start_date":"2027-03-01","due_date":"2027-03-05",
 "span_from":"2027-03-01","span_to":"2027-03-05","version":1,
 "schedules":[{"schedule_id":"…","on_date":"2027-03-03","starts_at":"10:00","ends_at":"11:30","version":1}]}

{"kind":"meeting","meeting_id":"…","title":"…",
 "starts_at":"2027-03-04T01:00:00+00:00","ends_at":"2027-03-04T02:00:00+00:00",
 "location":null,"status":"scheduled","viewer_relation":"attendee",
 "created_by":"mina","attendee_count":1,"created_by_display_name":"민아 (구성원)"}
```

**함정 일곱 — 하나씩 확인하라**

1. **`start_date`·`due_date` 로 띠를 그리지 마라.** 원본 그대로라 **뒤집힌 업무는 `start > due` 가
   실제로 온다.** 그리기도 드롭 가드도 **`span_from`·`span_to`** 를 쓴다 (K14).
   기간 없는 업무는 둘 다 `null`.
2. **회의 `starts_at`·`ends_at` 은 UTC ISO** (`+00:00`). **Asia/Seoul 로 변환**해 놓아라.
   업무의 `on_date`·`starts_at`(`"10:00"`)과 **타입이 다르다.**
3. **`schedules[]` 원소에 `task_id` 가 없다.** 요청 기간과 겹치는 **살아 있는 것만** 온다.
4. **`state` 는 5종**이고 `completion_submitted` 는 **`"done"` 으로 투영**된다 —
   **그래서 좌측 카드는 상태를 내지 않는다** (K15). 유형(업무/회의) 배지만.
5. **`is_active_assignee` 가 없다** (K13). 축이 `my_work` 라 뜨는 업무는 전부 내 담당이다.
6. **기간으로 업무를 거르지 않는다** — 기간 없는 업무도 행으로 온다. 끝난 업무는 애초에 안 실린다.
7. `from`·`to` **둘 다 필수**, 역전이면 422.

### 에러 — **본문에 `code` 필드가 없다**

```json
{"detail": "이 날에는 이미 시간 배정이 있습니다"}
```

**상태 코드 + 어떤 명령을 불렀는지로 갈라라.** 문구는 **네가 만든다**(SPEC 이 화면 문구를 갖는다).
`WORK_SCHEDULE_START_AFTER_DUE` 는 서버 문구가 **영문**이다 — 그대로 내보내지 마라.

### `GET /api/meetings`

- `from`·`to` 가 오면 **한 배열**, 없으면 기존 `{upcoming, past:{items,next_cursor}}` 그대로.
- **`created_by_display_name` 은 이 라우트에 없다** — 합본 조회에만 있다 (K4).

## 3. 선행 확인 ① — **한 줄로 끝낸다**

`_ds_bundle.css`(4069줄)·`_ds_bundle.js`(1862줄)의 **토큰 값**이 저장소 `styles/scax.css` 정의와
같은지 대조한다. 참조 이름은 이미 맞췄고 **값은 안 봤다**. **결정이 아니라 확인 작업**이다 —
다르면 **저장소 값이 정본**이고 그 사실만 기록한다. 여기서 시간을 쓰지 마라.

## 4. 이 Phase 에서 특히 조심할 것

- **`TaskCalendar` 를 고치지 마라.** 새로 세운다(G-CAL-06). `taskSpan()` 은 `TaskTimeline` 과
  공유라 **읽기만** 한다 — 캘린더에서는 **쓰지 않는다**(K14).
- **`ds/Empty.tsx` 는 소비처가 19곳이다.** `icon` 은 **additive** 여야 한다 —
  기존 `variant` 경로를 건드리면 19개 화면이 같이 깨진다. 그 파일 docstring 이
  「props 는 우리 것을 그대로 지켰다(D-4) — 소비처를 고치지 않는다」를 규율로 적어 뒀다.
- **새 레일 부품에 `GutterList` 라는 이름을 주지 마라** — 저장소 DS 에 이미 있다. `ScheduleRail` 제안.
- **`api.ts` 밖에서 `fetch` 하지 마라.**
- **한 화면 = 한 요청** — 주 뷰 7일·월 뷰 42일이 각각 **합본 조회 한 번**으로 그려진다.
- **격자에 상태 색을 쓰지 마라** — 유형 둘(업무/회의)로만 (§J).
- **시안은 레이아웃 정본이다.** 기능·모달 항목·상태 어휘는 **우리 것**이 정본이다(DEC-003 정정).
  업무 만들기는 **기존 모달**을 쓴다(G-CAL-03).

## 5. allowed_paths

- `frontend/`

`backend/`·`docs/`·`para/`·`orchestration/` 은 **금지**다. 백엔드가 모자라 보이면
**고치지 말고 코디에게 물어라** — 계약은 검수 4회를 지났다.

## 6. 검증 — WORK-004 `Phase FE-1` 완료 판정 그대로

```
make frontend-test          ← Node 20
cd frontend && npx tsc --noEmit
```

- **`ds/Empty.tsx` 소비처 19곳 중 한 곳도 고치지 않았다**를 `tsc` 로 증명하라
- 같은 검증을 중복 실행하지 마라
- **기존에 깨져 있던 실패는 「무관」으로 분리 보고.** 기준선을 먼저 재라
- 시안 부재는 **DS-gaps 로 기록**한다

## 7. 범위 제약

- **FE-2 를 당겨 하지 마라** — 드래그·손잡이·시간 배정 생성·금지 문구는 다음 Phase 다
- **계약을 다시 정하지 마라.** 모순은 고치지 말고 **코디에게 물어라.** 조용히 정하지 마라
- 백엔드를 건드리지 마라
- 커밋·push 금지

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_a9d49810-1ce8-4885-8c5f-b93200c501ac --from term_49972e50-eed3-461b-8174-fc4f61de218d \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_a9d49810-1ce8-4885-8c5f-b93200c501ac \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_a9d49810-1ce8-4885-8c5f-b93200c501ac --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)

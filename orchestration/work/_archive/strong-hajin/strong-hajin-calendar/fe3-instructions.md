# [frontend] Phase FE-3 — 월 뷰 정리 · 겹침 나란히 · 카드 배지

너는 **strong-hajin `frontend` 워커**다. **앞 판을 한 워커는 죽었다 — 너는 맥락이 없다.**
먼저 읽어라:

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/frontend/role.md` (+ 같은 폴더 `rules.md`·`skills.md`·`tools.md`·`workflow.md`)
- 코드 레포 루트 `AGENTS.md`
- `orchestration/work/strong-hajin-calendar/fe1-report.md` · `fe2-report.md` — **앞 판(1루프)이 만든 것**.
  `features/calendar/` 는 그들이 세웠다. 네가 그 위에 얹는다

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-calendar`

> ⚠ **백엔드는 끝났다** — BE-3 `bc3b5d8` · BE-4 `434003c` 커밋됨. API 가 실제로 돈다.
> ⚠ **이번 판은 보이는 것까지다.** 거절 문구·업무 탭 레일은 **FE-4** 다. 당겨 하지 마라.
> ⚠ 커밋·push 금지.

## 작업 지시서

`…/30-work/work-004-calendar-scheduling.md` 의 **`Phase FE-3`**.
계약은 `…/20-spec/spec-004-calendar-scheduling.md` **v0.3.1** (커밋 `bfe299a`).
근거는 `…/10-decision/decision-003-calendar.md` **증보 8~10 (K19~K30)**.

## 셋을 한다

### K20 — 월 뷰는 종일 띠만. 그리고 시간순

지금 `calendarModel.ts` 의 `gridSegments` 가 **띠와 시간 배정을 둘 다** 넣어서
**같은 업무가 한 칸에 두 번** 뜬다(사용자가 실물에서 찾았다).

- **월 뷰는 업무의 시간 배정을 그리지 않는다.** 종일 띠만.
- **회의는 계속 그린다** — 회의는 그 자체가 일정이지 업무의 배정이 아니다.
- **셀 안은 시간순으로 정렬**한다.
- **주 뷰는 그대로** — 종일 칸과 시간 격자가 이미 나뉘어 있다.
- 시안은 둘 다 그리지만 **목데이터라 두 번 뜨는 게 눈에 안 띄었을 뿐**이다. 시안과 다르게 간다.

### K21 — 겹치는 시간 블록을 나란히

지금 `packLanes` 가 **종일 띠에만** 쓰이고 시간 격자엔 줄 배치가 없다. 그래서 09:30–12:30 안에 든
10:00–11:00 회의가 **밑에 깔려 안 보인다**(사용자가 찾았다).

**겹치면 나란히 앉는다.** 이것은 **그리기**이지 막는 것이 아니다 —
**이미 겹쳐 있는 것은 여전히 그려져야 한다**(기존 데이터는 소급해 막지 않는다).

### K19 — 좌측 카드에 배지 둘

**BE-4 가 `approval` 을 실어 준다.** 합본 조회 `kind:'task'` 행에 필드 하나가 늘었다:

```
approval: null | "awaiting_review" | "awaiting_revision" | "approved"
```

- 카드는 **상태 배지 + 승인 배지 둘**을 낸다. **업무 화면이 이미 그렇게 한다** —
  `features/work/WorkTables.tsx:197` 이 `derivedApprovalLabel.awaiting_review` 로 Badge 를 낸다.
  **같은 어휘·같은 방식을 쓰라. 새로 만들지 마라.**
- **왜 필요한가** — `state` 는 5종 투영이고 `completion_submitted` 가 **`"done"` 으로 온다.**
  승인 배지 없이 상태만 내면 **승인 대기 업무를 「완료」라고 말한다.**
- **K15 를 뒤집는 것이다.** K15 는 「보여줄 방법이 없어서」 뺐는데 **방법이 이미 있었다.**
- **격자는 여전히 상태를 말하지 않는다** — 유형 둘(업무/회의)로만. 배지는 **좌측 카드**만.

## 조심할 것

- **`span_from`·`span_to` 로만 그린다** — `start_date`/`due_date` 는 원본이라 뒤집힌 업무에서
  `start > due` 가 실제로 온다. 캘린더는 업무 기간을 **자체 계산하지 않는다**.
- **`api.ts` 밖에서 `fetch` 하지 마라.**
- **한 화면 = 한 요청** — 탭 전환에 재조회가 없다. 이 규율이 1루프에서 검수를 지났다. 깨지 마라.
- **레일과 격자는 같은 범위를 본다**(K18) — 월 뷰면 그 달. 이미 그렇게 돼 있다. 깨지 마라.
- **회의 시각은 UTC** 로 온다. Asia/Seoul 변환은 이미 있다.

## allowed_paths

`frontend/` 만. `backend/`·`docs/`·`para/`·`orchestration/` 금지.
백엔드가 모자라 보이면 **고치지 말고 코디에게 물어라.**

## 검증

```
make frontend-test
cd frontend && npx tsc --noEmit
```

기준선: **69파일 914 passed / 0 failed · tsc exit 0**.
기존에 깨져 있던 실패는 「무관」으로 분리 보고. **기준선을 먼저 재라.**

⚠ **기계에 E2E 스택이 떠 있다**(코디가 띄웠다 — API 8001 · 프론트 5176). 부하가 있을 수 있다.
**내리지 마라** — 사용자 것이다.

## 범위 제약

- **FE-4 를 당겨 하지 마라** — 겹침 거절 문구 · 업무 탭 레일에 회의 · 「업무 만들기」 단추
- 계약을 다시 정하지 마라. 모순은 **코디에게 물어라** — 조용히 정하지 마라
- 커밋·push 금지

## 보고

```bash
orca terminal send --terminal term_a9d49810-1ce8-4885-8c5f-b93200c501ac \
  --text "[worker_done] frontend FE-3 완료 — <한 줄>" --enter
```

본문에 담을 것: 변경 파일 / 구현 요약 / **검증 수치** / 기존 실패와 새 실패의 분리 /
계약 준수 / **미결·주의점**. 막히면 같은 방식으로 `[질문]`.

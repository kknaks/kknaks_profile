# 리뷰 리포트 — strong-hajin-calendar / WORK-004 검수 (2026-09-21)

> **⚠ 브리프가 잘려 들어왔다.** 받은 메시지가 「…지, Phase 넷의 「완료 판정」이」 로 시작해
> **①②③ 과 대상 파일 경로가 없다.** `strong-hajin-calendar-wp-brief.md` §6(검증)이
> 보이는 ④⑤⑥ 과 정확히 이어지므로 **①=절 구성·frontmatter · ②=Code Surface 전수 ·
> ③=인수조건 전수 매핑**으로 보고 진행했다. FAIL 기준에 「빠진 Code Surface」·
> 「닫는 Phase 가 없는 인수조건」이 박혀 있어 ②③ 은 사실상 확정이다.
> **다르게 의도했으면 말해 달라 — 그 축만 다시 본다.**

## 판정: **FAIL** — 한 건

**계획으로서는 섰다.** 인수조건 **124줄 전수**가 Phase 에 붙었고(빠진 줄 0),
Code Surface 가 `be-survey-report.md` §2 의 12항을 **전부** 옮겼으며, Phase 넷의 완료 판정이
**실제로 돌릴 수 있는 명령**으로 적혔다. 검수가 넘긴 넷도 **넷 다** 자리를 찾았고
DS-gaps 8건도 **전부** 처분됐다.

**걸리는 것은 하나** — WP 가 **편집을 예약한 파일 하나가 Code Surface 에 없다.**
`ds/Empty.tsx` 는 **소비처 19곳**을 가진 공유 DS 부품이고, 그 파일 자신이
「props 는 우리 것을 그대로 지켰다 — **소비처 29곳을 고치지 않는다**」는 규율을 적어 두었다.
**「빠진 Code Surface」가 이번 FAIL 기준에 박혀 있어** 그대로 FAIL 로 낸다.

**고칠 양은 한 줄이다** — Code Surface 표에 행 하나.

---

## 검수 범위

- 대상: `para/projects/summer-star/strong-hajin/30-work/work-004-calendar-scheduling.md` (719줄, 신규)
  · `30-work/README.md` 갱신분
- 기준: `strong-hajin-calendar-wp-brief.md` · `20-spec/spec-004-calendar-scheduling.md`(검수 4회 PASS)
  · `10-decision/decision-003-calendar.md`(A~J · K1~K14) · `be-survey-report.md` · `fe-survey-report.md`
  · `review-spec-004-report.md` 4차 「WP 로 넘길 것」 · 본보기 `work-002-task-lifecycle-v2.md`
- 코드 워크트리는 **주장 확인용으로만** 읽었다(`ds/Empty.tsx` 소비처 · `meetings_visible_to` 소비처 ·
  `shell/CalendarRail.tsx` 성격 · `styles/shell.css` 위치). **한 줄도 고치지 않았다.**

---

## ① 절 구성 · frontmatter — **맞다**

| 항목 | 결과 |
|---|---|
| 절 구성 | 브리프가 지정한 17절이 **순서대로** 있다(`Meta` → `Related`). `work-002` 와 같다 |
| frontmatter | `type/id/title/status/product/work_type/owner/roles/progress/created_at/updated_at/tags/links` — `work-002` 와 **같은 꼴**. `status: todo` · `progress: 0` |
| `links` | `baselines: BASE-003` · `decisions: DEC-003` · `specs: SPEC-004 · SPEC-003` |
| 본보기에만 있는 절 | `work-002` 의 `W1 유지 회귀`·`SPEC 환류 후보`·`미설계 화면 처분`·`Automated Completion Evidence` 는 그 work 고유다. WORK-004 는 같은 내용을 `Open Issues`(환류 후보 0건) 와 `Code Surface`(회귀 가드 표) 로 갖는다 |
| `30-work/README.md` | **세 표 전부** 갱신됐다 — Status Board · Work List · Spec Coverage. 「최종 수정」도 |
| allowed_paths | `git status --short` 가 **허용된 둘만** 낸다(+ 검수 리포트가 사는 untracked `orchestration/`) |

---

## ② Code Surface — `be-survey-report.md` §2 는 전수. **그런데 한 자리가 빠졌다**

### be-survey §2 의 12항 대조 — **전부 옮겨졌다**

| §2 | 자리 | WORK-004 |
|---|---|---|
| 1 | `platform/persistence.py` | **#1** |
| 2 | `bootstrap/schema_sync.py` | **#2**(수정 불필요 명시) |
| 3 | `entrypoints/reset_demo.py` | **#3** |
| 4 | `bootstrap/reset.py` | **#3**(같은 행) |
| 5 | `docs/domain-model.md` | **#14** |
| 6 | `bootstrap/application.py` | **#7** |
| 7 | `platform/task_schedules.py` | **#4** |
| 8 | `modules/work/…` | **#5**(신규 순수 도메인) · **#6** |
| 9 | `entrypoints/http.py` | **#8** |
| 10 | `mcp.py` + `tool_catalog.py` | **건드리지 않는다** — 사유와 함께 명시 |
| 11 | `docs/unified-operations-inventory.json` | **#11** |
| 12 | `tests/contract/` · `tests/unit/` | **#16** |
| §2 「여기 없던 자리」 | 회귀 가드 셋 | **「고치지 않지만 걸리는 회귀 가드」 표**로 따로 세웠다 |

브리프 §3-2 가 최소로 요구한 것(D1 세 자리 · 운영 대장 count · `Makefile:170`+`test_local_stack_targets` ·
`PURE_DOMAIN_MODULES` · FE 다섯)도 **전부** 있다. **D1 세 자리**는 진입 표면까지 붙은 별도 표이고,
**상태 아홉 경로**는 「여기에는 걸지 않는다」로 명시적으로 배제됐다.

### FAIL — F-1. `ds/Empty.tsx` 가 Code Surface 에 없다

- `work-004-calendar-scheduling.md:484`(DS-gaps 표 G-CAL-02) —
  「**만든다** — **`ds/Empty.tsx`** 에 `icon` 을 **추가**한다(기존 `variant` 경로는 그대로)」,
  「어디에: **`ds/Empty.tsx`**」, 「Phase: **FE-1**」
- **Code Surface 표(`:148-169`, 22행)에 그 파일이 없다.** FE 쪽은 #17 `CalendarPage.tsx` ·
  #18 `App.tsx` · #19 `features/calendar/`(신규) · #20 `lib/api.ts` · #21 `lib/viewModels.ts` ·
  #22 `styles/` 뿐이다. **`ds/` 는 어느 행에도 안 걸린다** —
  문서 전체에서 `ds/` 가 나오는 곳은 **`:484` 한 줄뿐**이다.

**왜 이것이 센서스의 구멍인가.**

- `frontend/src/ds/Empty.tsx` 는 **소비처 19곳**이다(직접 셌다 — `features/action`·`features/graph`·
  `features/meetings` 5곳·`features/org` 5곳·`features/today`·`features/work` 4곳·
  `shell/CalendarRail.tsx`·`shell/InboxRail.tsx`).
- 그 파일 자신이 규율을 적어 두었다 — docstring:
  「**props 는 우리 것을 그대로 지켰다**(D-4): **소비처 29곳을 고치지 않는다**」.
  **props 를 더하는 것이 바로 그 규율을 건드리는 일**이다.
- Code Surface 만 읽은 FE 워커는 **DS 를 안 건드리는 줄 안다.** 그러다 DS-gaps 표에서
  DS 편집 지시를 만난다. **센서스가 존재하는 이유가 정확히 이 자리다.**

**권장 수정 — 한 줄.** Code Surface 표에 행을 더하라:

> `| 23 | frontend/src/ds/Empty.tsx | G-CAL-02 — `icon` prop **추가**(additive). 소비처 19곳의 기존 호출은 안 바뀐다. docstring 의 D-4 규율(「소비처를 고치지 않는다」)을 지킨다 | FE-1 |`

그리고 FE-1 완료 판정에 「**`ds/Empty.tsx` 의 기존 소비처가 전부 그대로 컴파일된다**(`npx tsc --noEmit`)」
한 줄을 붙이면 이 자리는 닫힌다. **계약은 바뀌지 않는다** — additive 이고 SPEC §2.8 G-CAL-02 가
이미 「선다」로 받은 항목이다.

---

## ③ 인수조건 전수 매핑 — **닫는 Phase 가 없는 줄은 없다**

SPEC-004 §6 의 체크박스를 직접 셌다 — **14묶음 · 124줄**. WORK-004 `:605-628` 의 추적표와
**묶음별 줄 수가 전부 일치**한다.

| 묶음 | SPEC 실측 | WP 표기 | 닫는 Phase |
|---|---|---|---|
| 배정 만들기 | 13 | 13 | BE-1(11) · FE-2(2) |
| 하루 한 칸 | 10 | 10 | BE-1(9) · FE-2(1) |
| 회차 | 10 | 10 | BE-1 |
| 시각 조정 | 5 | 5 | BE-1(1) · FE-2(4) |
| 기간 이동·조정 | 7 | 7 | FE-2 |
| (가) 기간 밖 | 20 | 20 | BE-2(18) · FE-2(2) |
| (나) 업무 종료 | 7 | 7 | BE-1(6) · FE-2(1) |
| 합본 조회 | 13 | 13 | BE-1(11) · FE-1(2) |
| 회의 | 9 | 9 | BE-1(7) · FE-1(2) |
| 금지는 말로 | 2 | 2 | FE-2 |
| 화면 | 12 | 12 | FE-1(10) · FE-2(2) |
| 표면 등록 | 8 | 8 | BE-2 |
| 「선다」 | 7 | 7 | BE-1 |
| 계층 | 1 | 1 | BE-1 |
| **합계** | **124** | **124** | |

- **한 줄이 두 Phase 에 걸치는 자리**를 별도 표(`:629-640`)로 여섯 줄 뽑아 BE 절반·FE 절반을 갈랐다.
  「서버가 낸 구간과 화면이 그리는 구간이 같다」·「띠와 드롭 가드 양쪽에」 같은 K14 줄까지 들어갔다.
- **Phase 별 부담**(BE-1 60 · BE-2 26 · FE-1 14 · FE-2 24)도 적혔다.
- **고아 줄 0.** 묶음마다 Phase 가 있고, 각 Phase 의 완료 판정이 그 묶음을 돌리는 명령을 갖는다.

---

## ④ Phase 넷의 완료 판정 — **넷 다 판정 가능하다**

| Phase | 돌릴 명령이 적혔나 | 무엇으로 판정하나 |
|---|---|---|
| **BE-1** | ✔ | `make test-unit` · `make test-contract` · **`make test-postgres POSTGRES_TEST_URL=postgresql+psycopg://ax:ax@127.0.0.1:54329/ax_test_calendar`**(전체 명령이 박혔다) · `curl` 로 세 라우트 실물 응답(`201`/`409`/`200`/`200`/`kind` 두 종) · **커밋 후 API 재기동** |
| **BE-2** | ✔ | `make test-unit`(`test_operation_inventory` 포함) · `make test-contract` · `make test-postgres` 재통과 · **대장 diff 상한**(「행 3 + count 1줄 + `http_signature` 2줄 **이내**」) · `make local-stack` preflight 가 `task_schedules` 를 본다 |
| **FE-1** | ✔ | `make frontend-test`(**Node 20**) · `cd frontend && npx tsc --noEmit` + 관측 가능한 조건들(3분할 · 8시 · **뒤집힌 업무의 띠가 `[9/4, 9/6]`** · 주최자 이름 · 공유 회의 제자리 · 상태 색 없음) |
| **FE-2** | ✔ | `make frontend-test` · `npx tsc --noEmit` · **최종 `make verify`** + `make test-postgres` 재통과 + 관측 조건(조용한 거절 0개 · 같은 날 재배정이 `PATCH` · 연타가 `409` 안 띄움 · WARN-A 한 줄이 코드와 테스트에 같이) |

- **BE-1 의 PostgreSQL 증명 넷**(있음 · 술어 · 거절 · 재배정)이 **각각 한 건씩**으로 요구됐다 —
  SPEC §6 「선언했다가 아니라 선다」가 그대로 내려왔다.
- **직렬 규칙**(`:344-357`)이 「BE 가 닫히기 전에 FE 를 태우지 않는다」·「BE-2 뒤에 **실제 API 계약을
  FE 브리프에 박는다**」·「백엔드 커밋이 들어가면 API 재기동」까지 적었다.
- **전량 반복 금지**도 지켜졌다 — `make verify` 는 **FE-2 에서 한 번**.

---

## ⑤ 검수가 넘긴 넷 — **넷 다 받았다**

| 넘긴 것 | 어디에 앉았나 | 확인 |
|---|---|---|
| **WARN-A** — 손잡이·길이 | **FE-2 작업 8**(`:528-546`)이 **한 줄로 정했다** — 「뒤집힌 업무에서도 `start` 손잡이는 `start_date` 를, `end` 손잡이는 `due_date` 를 쓴다. 띠 위에서 좌우가 바뀌어 보일 수 있다」 + 「R1 의 「길이」는 **span 길이**다」. **왜 이 쪽인가**까지 적었다(손잡이의 정체가 필드여야 예측 가능) | ✔ **인수조건도 두 줄**(`:644-648`) — 코디가 말한 그대로 |
| **배정 삭제 구멍** | **Open Issues**(`:695-700`) — 「이번 판에 열지 않는다 · 2루프 E2E 에서 불편이 나오면 그때」. **Rollback 이 BE-2 를 되돌릴 때도 드러난다**는 연결까지 달았다 | ✔ |
| **`_ds_bundle` 토큰 대조** | **FE-1 작업 0**(`:463-467`) — 「한 줄로 끝낸다 · 결정이 아니라 확인 · 다르면 **저장소 값이 정본**」. 완료 판정에 「결과가 한 줄로 기록됐다」 | ✔ |
| **실행 PostgreSQL 실제 제약** | **BE-1 작업 1**(`:367-371`) — 읽기 전용 선행 점검, 「여기서 코드를 고치지 않는다」 + **Pre-deploy Check**(`:654-655`) 「배포 직전 다시 묻는다. **BE-1 의 격리 DB 통과는 이 조건의 근거가 아니다**」 | ✔ 두 자리 |

`Meta` 의 **「착수를 막는 것과 막지 않는 것」 표**(`:70-78`)가 넷을 다시 한 번 모아
**전부 「막지 않는다」**로 판정하고 각각 어느 Phase 에 걸리는지 적었다 — 영수증이 두 겹이다.

---

## ⑥ DS-gaps 8건 처분 — **8건 전부 배치됐다.** 「안 만든다」 셋의 근거도 맞다

| ID | 처분 | Phase | 근거 대조 |
|---|---|---|---|
| G-CAL-01 레일형 `GutterList` | **만든다** → `features/calendar/ScheduleRail.tsx` | FE-1 | DEC-003 §J 「새것에 **다른 이름**」 ✔ |
| G-CAL-02 `Empty` 의 `icon` | **만든다** → `ds/Empty.tsx` | FE-1 | SPEC §2.8 「선다」 ✔ — **단 Code Surface 누락(F-1)** |
| G-CAL-03 `TaskCreateModal` | **만들지 않는다** | — | DEC-003 §J 정정 「**기존 모달을 그대로 쓴다.** 시안 필드 구성을 따라가지 않는다」 ✔ |
| G-CAL-04 `ItemCard`/`InboxCard` | **만든다** → `features/calendar/ScheduleCard.tsx` | FE-1 | SPEC §2.8 「선다 — 항목 구성은 우리 어휘」 ✔ |
| G-CAL-05 일정 조각 일체 | **만든다** → `features/calendar/EventBar.tsx` 등 | FE-1(띠·`+N건`) · FE-2(손잡이·고스트) | SPEC §2.8 「선다」 ✔ |
| G-CAL-06 `MonthGrid`·`WeekGrid` | **만든다** | FE-1 | SPEC §2.8 「선다」 ✔ |
| G-CAL-07 `AppHeader` 의 `titleEnd` | **만들지 않는다** | — | SPEC §2.8 「캘린더는 `title`+`actions` 만 쓴다 — 요구하지 않는다」 ✔ |
| G-CAL-08 상태 색 tint | **격자에는 만들지 않는다.** 좌측 카드는 **기존 상태 톤** | FE-1(재사용) | DEC-003 §J 「캘린더가 상태를 색으로 말할까 → **말하지 않는다** — 유형 둘로만」 ✔ |

**빠진 것 없음. 「안 만든다」 셋(03·07·08)의 근거가 DEC-003·SPEC 과 전부 맞는다.**

> **코디 브리프의 수치 정정** — 브리프는 「**만든다 넷**·안 만든다 셋」이라고 적었는데
> 실제는 **만든다 다섯(01·02·04·05·06) · 안 만든다 셋(03·07·08)** = 8 이다.
> **WP 의 흠이 아니다** — WP 는 8건을 전부 처분했다. 브리프 쪽 숫자만 바로잡으면 된다.

---

## WARN — 구현 중에 닫아도 되는 것. **어느 Phase 브리프에 실을지**

### WARN-1 → **Phase BE-1 브리프**

`work-004:157`(Code Surface #10) — 「`platform/meetings.py` | `meetings_visible_to`(`:144-170`)에
**시각 조건 추가(또는 호출부 필터)**」.

**두 선택지가 대등하지 않다.** `meetings_visible_to` 의 소비처를 직접 셌더니 **셋**이다 —
`modules/meetings/application.py:180`(`my_meetings`) · `:198`(`readable_rows`) · `:218`(`board`).
같은 문서 **#9 가 「`_is_past`·`my_meetings` 는 건드리지 않는다」**고 못 박았는데,
첫 선택지를 **무조건 필터**로 구현하면 `my_meetings`(MCP `my_meeting_list`)와
`readable_rows`(자료 검색의 소유자 조회)가 **같이 바뀐다.**

**FAIL 이 아닌 이유** — 제대로 하면(인자를 **선택적**으로 두고 기본을 끔, 또는 호출부 필터)
두 선택지가 **관찰상 같다.** 계약이 갈리는 것이 아니라 **잘못 짚을 수 있는 자리**다.

**브리프에 실을 한 줄**: 「`meetings_visible_to` 는 **세 곳이 공유**한다(`:180`·`:198`·`:218`).
시각 조건은 **선택적 인자(기본 없음)**로 넣거나 **`board()` 호출부에서 거른다.**
`my_meetings`·`readable_rows` 의 결과가 **바뀌지 않는 것**을 테스트로 남긴다.」

### WARN-2 → **Phase BE-1 브리프**

`work-004:623`(인수조건 추적 M행) — 「「선언했다」가 아니라 「선다」 | 7 | BE-1 |
**`make test-postgres`** — 이 줄들은 **다른 명령으로 닫히지 않는다**」.

M 묶음 7줄 중 **마지막 한 줄**은 「**API startup 경로에 스키마 생성이 끼지 않는다** — 저장소의
startup 회귀 검사가 그대로 통과한다」이고, 이것은 `make test-postgres` 가 아니라
**`make test-unit`**(`test_architecture` 의 startup 테스트)이 닫는다.

**구멍은 아니다** — BE-1 완료 판정이 `make test-unit` 통과를 이미 요구하므로 그 줄은 닫힌다.
**추적표의 「확인 방법」 칸만 부정확**하다.

**브리프에 실을 한 줄**: 「M 묶음의 마지막 줄(startup 회귀)은 **`make test-unit`** 이 닫는다.
나머지 6줄이 `make test-postgres` 다.」

---

## 확인한 것 (근거)

- **①** 절 구성 17절·frontmatter·`links`·`30-work/README.md` 세 표·allowed_paths 를 전부 대조했다.
- **②** `be-survey-report.md` §2 의 12항 + 「여기 없던 자리」를 Code Surface 22행과 1:1 로 맞췄다.
  **FAIL 1건**(`ds/Empty.tsx`) — 소비처 19곳과 그 파일의 D-4 규율을 코드에서 직접 확인했다.
  DS-gaps 표의 나머지 「어디에」(`features/calendar/*`)는 #19 가 덮고, `styles/shell.css` 는 #22 가 덮는다.
  기존 `shell/CalendarRail.tsx`(MyWorkPage 의 **우측** 레일)는 새 좌측 레일과 **역할이 달라 충돌이 없다** — 확인했다.
- **③** SPEC §6 체크박스를 **직접 세어**(14묶음·124줄) WP 의 묶음별 수와 전부 일치함을 확인했다. 고아 줄 0.
- **④** Phase 넷의 완료 판정에 **실행 가능한 명령**이 있는지 각각 확인했다 — 넷 다 있다.
  `POSTGRES_TEST_URL` 은 전체 명령이 박혔다.
- **⑤** 넷의 착지점을 각각 줄로 확인했다(FE-2 작업 8 + 인수조건 두 줄 · Open Issues · FE-1 작업 0 ·
  BE-1 작업 1 + Pre-deploy). `Meta` 의 착수 판정 표가 한 번 더 받는다.
- **⑥** 8건 전부 배치 확인. 「안 만든다」 셋의 근거를 DEC-003 §J·SPEC §2.8 에 각각 대조했다.
  **브리프의 「만든다 넷」은 다섯이 맞다.**
- **판정 기준 준수** — 문장 다듬기·근거 보강·표기 고르기는 **지적하지 않았다.**
  FAIL 은 명시된 셋(다르게 읽히는 자리 · 닫는 Phase 없는 인수조건 · **빠진 Code Surface**) 중
  마지막 하나에만 걸렸다.
- **read-only 준수** — 문서도 코드도 한 줄 고치지 않았다. 산출물은 이 리포트 하나.

---

## `git -C /Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin status --short`

```text
 M para/projects/summer-star/strong-hajin/30-work/README.md
?? orchestration/work/strong-hajin-calendar/
?? para/projects/summer-star/strong-hajin/30-work/work-004-calendar-scheduling.md
```

**allowed_paths 를 지켰다** — 허용된 둘(`work-004-*.md` 신규 · `30-work/README.md` 수정)만 떴다.
`orchestration/work/strong-hajin-calendar/` 는 조사·검수 리포트가 사는 untracked 디렉토리다.

## `git -C /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-calendar status --short`

```text
```

(출력 없음 — **코드 워크트리가 깨끗하다.** 검증용으로 읽기만 했다.)

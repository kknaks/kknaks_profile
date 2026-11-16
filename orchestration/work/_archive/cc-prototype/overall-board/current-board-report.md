# overall-board 0판 결과 보고 — 현재 시술 현황판(procedure) 인벤토리

## 상태: done (read-only 조사)

- 기준 코드: 워크트리 `cc-prototype/overall-board`, 브랜치 `kknaksss/overall-board`, HEAD `eaa9169`(= base `origin/main`). 작업 트리는 깨끗하고 고친 파일은 없다.
- 기준 문서: SPEC-003 0.3.0, WORK-003, 로그 `2026-10-22-myeongdong-poc-v2.md` §7.
- 근거는 레포 상대경로 `파일:줄`로 적었다. 앞 경로를 줄여 `F/` = `procedure/front/`, `B/` = `procedure/back/app/`로 쓴다.
- 코드에서 확인하지 못한 것은 「확인 못 함」으로 적었다. 디자인과는 비교하지 않았다(다음 판에서 한다).

## 수행 — 읽은 파일

- front: `F/app/layout.tsx` · `F/app/page.tsx` · `F/app/login/page.tsx` · `F/app/(main)/layout.tsx` · `F/app/(main)/procedures/page.tsx` · `F/app/(main)/procedures/live/page.tsx` · `F/components/common/AppHeader.tsx` · `F/components/procedures/{OrderCard.tsx, Aside.tsx, CallPopover.tsx, view.ts}` · `F/lib/{api,session,hooks,time,memo,types}.ts(x)` · `F/tailwind.config.ts` · `F/app/globals.css` · `F/app/styles/{ceramique-theme,medikit-patches}.css` · `F/package.json` · `F/next.config.ts` · `F/.env.example`
- back: `B/schemas/board.py` · `B/service/board_service.py` · `B/domain/rules.py` · `B/domain/models.py`(상수) · `B/api/{board,auth,actions,deps}.py` · `B/service/{stream,actions,auth}.py`(필요한 부분) · `B/container.py` · `B/main.py` · `B/config.py` · `B/kos/{sync,runtime,client}.py` · `B/repository/repo.py:231-241`

## 검증

- 이번 판은 read-only 조사라 tsc · lint · build는 하지 않았다(브리프 §7 금지). `F/node_modules`도 없다.
- 그래서 **medikit 패키지 내부(글꼴 지정 · Badge/Button 실제 색 · Tabs/Menu 모양)는 확인 못 함**이다.

---

## 1. 라우트 · 화면 구성 · 로그인 · 역할

| 경로 | 무엇 | 근거 |
|---|---|---|
| `/` | 클라이언트에서 `readSession()`을 보고 로그인돼 있으면 `/procedures/live`, 아니면 `/login`으로 `replace`. 화면은 그리지 않는다(`return null`) | `F/app/page.tsx:8-13` · `HOME` = `F/lib/session.ts:61` |
| `/procedures` | `/`와 같은 동작(redirect만) | `F/app/(main)/procedures/page.tsx:8-13` |
| `/procedures/live` | **현황판 본체(유일한 실제 화면)** | `F/app/(main)/procedures/live/page.tsx:26-276` |
| `/login` | 아이디 · 비밀번호 폼과 [로그인]. 헤더 없음. 로고 + 「명동점」 | `F/app/login/page.tsx:12-123` |

- **공통 헤더**: `(main)` 그룹 레이아웃이 `AppHeader`를 모든 로그인 화면 위에 붙인다(`F/app/(main)/layout.tsx:4-10`). `/login`은 그룹 밖이라 헤더가 없다.
- **세션**: localStorage 키 `procedure.session`에 `{token,id,expiresAt,role,name}`를 둔다(`F/lib/session.ts:4-10,14,43-49`). 만료됐거나 role이 `admin|doctor|nurse`가 아니면 세션 없음으로 본다(`:28-41`).
  - `useSession`이 storage 이벤트를 구독하다 세션이 없으면 `/login`으로 보낸다(`F/lib/hooks.ts:36-45`).
  - 로그아웃은 세션을 지우고 `/login`으로 간다(`F/components/common/AppHeader.tsx:25-28`).
- **로그인 흐름**: `POST /api/auth/login {id,password}` → 세션 저장 → `HOME`(`F/app/login/page.tsx:19-37` · `F/lib/api.ts:52`).
  - 401이면 「아이디 또는 비밀번호가 맞지 않아요.」, 429 같은 그 밖 오류는 back 문구를 그대로 보인다(`F/app/login/page.tsx:10,32-33`).
- **역할별 진입**: front는 역할로 화면을 나누지 않는다. 세 역할 모두 같은 `/procedures/live`로 간다(`F/app/login/page.tsx:28-29`).
  - back 로그인도 역할로 막지 않는다(`B/api/auth.py:9-12`). → OQ-518과 같은 상태다.
  - 조작에서 역할 검사는 **수락 하나뿐**이다: doctor는 자기 원장으로만, admin은 `doctorId` 필수, nurse는 403(`B/service/actions.py:156-169`).
  - 나머지 조작(마취 · 호출 · 다른 원장에게 · 시작 · 종료 · 귀가 대기) 라우터에는 역할 검사가 없다(`B/api/actions.py:18-72`).
  - 헤더 계정 표시는 `session.name || session.id`다(`F/components/common/AppHeader.tsx:80-82`).

## 2. (a) 레이아웃 영역

```
┌ AppHeader 57px ─ 로고 │ 「시술 현황」 nav ─────────── HH:MM │ 세라미크 명동점 │ <계정명> │ 로그아웃 ┐
├ Menu(사이드바) ┬ main(padding 20/28) ──────────────────────────────────────────────────────┤
│ 「시술 현황」   │ 제목 줄: 시술 현황 · 명동점 · 마지막 KOS 동기화 HH:MM:SS [조회 시간 밖][동기화 실패] │
│ (wide 만)      │          범례 Badge 5 │ [입실순|배치순]                                         │
│                │ ┌ 흰 판(r12) ─ 회색 격자(카드 auto-fill minmax 300) ┐ ┌ Aside 340 (wide 만) ┐   │
│                │ │ OrderCard …                                      │ │ 검색 / 탭 3         │   │
│                │ └──────────────────────────────────────────────────┘ └─────────────────────┘   │
│                │                       (토스트: 화면 아래 가운데 fixed)                         │
└────────────────┴────────────────────────────────────────────────────────────────────────┘
```

| 영역 | 내용 | 근거 |
|---|---|---|
| 헤더 | 높이 57 · sticky · 흰 바탕 · 아래 경계선. 왼쪽 = 로고(`/ceramique-logo-color.svg`, wide 22px · 좁으면 18px) + nav 「시술 현황」(href는 `/procedures`, 링크는 `HOME`). 오른쪽 = (wide만) 시계 `HH:MM` · 「세라미크 명동점」(하드코딩), 그다음 계정 이름 · 「로그아웃」 | `F/components/common/AppHeader.tsx:10,13,31-87` |
| 사이드바 | medikit `Menu`, 묶음 · 항목 모두 「시술 현황」, `currentPath=/procedures/live`. 클릭은 `preventDefault`(이동 없음). **wide(≥760)일 때만** | `F/app/(main)/procedures/live/page.tsx:17-24,120` |
| 제목 줄 | `h1` 「시술 현황」 · 「명동점 · 마지막 KOS 동기화 {hms(sync.lastOkAt) 또는 —}」 · 「조회 시간 밖」(`!sync.inWindow`) · 「동기화 실패」(`sync.lastError`, 빨강, title = 오류 문구) · 범례 Badge sm dot 5개 · 세로 구분선 · 정렬 버튼 2개 | `…/live/page.tsx:133-168` · 범례 `F/components/procedures/view.ts:9-15` |
| 필터/툴바 | 제목 줄의 **[입실순 \| 배치순]** 하나(sm Button · 고른 쪽 solid blue · 아닌 쪽 outlined gray). 상태 필터는 제목 줄이 아니라 **Aside 현황 탭의 6칸**에 있다(§3 · §5) | `…/live/page.tsx:108-112,163-166` |
| 본문 | 흰 판(반경 12 · 패딩 12 · `containerType:size` · overflow auto) 안에 회색(`bg-ms-gray-100`) 격자. `grid-template-columns: repeat(auto-fill, minmax(300px,1fr))` · gap 8 · pad 6. **wide일 때만** 줄 최소 높이 = `(100cqh - pad*2 - gap)/2`(판 높이의 절반쯤) · `alignItems: stretch` | `…/live/page.tsx:170-222` |
| Aside | 폭 340 · 반경 12 · 그림자. 위 = 검색 input, 그 아래 = medikit `Tabs` 3개(현황 · 호출 · 고객). 검색어가 있으면 탭 대신 검색 결과. **wide일 때만** | `F/components/procedures/Aside.tsx:21-25,63-139` · `…/live/page.tsx:229-243` |
| 하단 | 고정 하단 바는 없다. 토스트가 `position:fixed; bottom:28; left:50%`(아래 가운데)에 뜬다 | `…/live/page.tsx:246-267` |
| 오버레이 | 의사 호출 팝오버(fixed · 560×440 · 바깥 투명 막을 누르면 닫힘) | `F/components/procedures/CallPopover.tsx:80-100` · `…/live/page.tsx:271-273` |

## 3. (b) 상태 · 칸 체계

> 현재 현황판은 **칸반 칸(상태별 열)이 아니다.** 모든 카드가 한 격자에 섞여 정렬된다.
> 「칸」에 해당하는 것은 ① 고객 상태 3개(Badge), ② Aside 현황 탭 필터 6칸, ③ 범례 5개다.

### 3.1 고객 상태(카드 단위) — 3개

| ccc 상태 | 라벨 원문 | Badge 변형 | KOS 원천 `flowStep` | 근거 |
|---|---|---|---|---|
| `waiting` | 시술 대기 | `warning` | `PROCEDURE_WAITING` | `F/components/procedures/view.ts:6-7` · `B/domain/rules.py:25,65-66` · `B/domain/models.py:7` |
| `doing` | 시술 진행 | `primary` | `PROCEDURE` | 같은 곳 · `B/domain/models.py:8` |
| `home` | 귀가 대기 | `neutral` (카드 opacity 0.55 · 맨 뒤) | `PROCEDURE_DONE` | 같은 곳 · `B/domain/models.py:9` · `view.ts:145-151` |

- **Badge 자리 덮어쓰기**(`F/components/procedures/OrderCard.tsx:38-39`) — 우선순위는 위에서부터다.
  1. `need` → `danger`. 문구는 `needView().state`: 「시술 모두 완료 · 귀가 대기 전」 / 「마취 중」 / 「전체 호출 · 수락 전」 또는 「<원장> 지정 호출 · 수락 전」(`view.ts:121-128`)
  2. `home` → `neutral` 「귀가 대기」
  3. 진행 중 마취 → `purple` 「마취 중」
  4. 그 밖 → 위 표
- **카드가 되는 조건**(back이 판정): `present && flow_step ∈ {PROCEDURE_WAITING, PROCEDURE, PROCEDURE_DONE} && room_id != null`(`B/domain/rules.py:38-39` · `B/domain/models.py:10`).
  - `room_id` = 일정 `tasks[]` 중 `type=ETCETERA`이고 `room.id`가 있는 작업. 여럿이면 `roomAssignedDateTimeUtc`가 가장 늦은 것(`B/kos/sync.py:38-44,91-102`).
- **정렬**
  - back 기본: 귀가 대기 아님 → `room_assigned_at`, 귀가 대기 → `flow_step_at`(`B/service/board_service.py:36-39`).
  - front: 입실순 = `inAt`, 배치순 = `room.order`. 귀가 대기는 뒤에 `homeAt` 순으로 다시 정렬한다(`F/components/procedures/view.ts:46-54`).

### 3.2 Aside 현황 탭 필터 6칸 (순서 · 라벨 · 색 · 개수)

| 순서 | id | 라벨 | 칸 클래스 | 개수 = `counts.*` (back) | front 필터 판정 | 근거 |
|---|---|---|---|---|---|---|
| 1 | all | 전체 | 흰 · 회 테두리 | `len(cards)` (귀가 대기 포함) | 전부 | `view.ts:20,35` · `B/service/board_service.py:61` |
| 2 | need | 확인 | `bg-red-100 border-red text-red` | `need` 있는 카드 | `!!c.need` | `view.ts:21,30` · `board_service.py:62` |
| 3 | waiting | 대기 | `bg-yellow-100` | `state==waiting` | 같음 | `view.ts:22,31` · `:63` |
| 4 | anes | 마취 | `bg-purple-100 border-purple` | 귀가 대기 아님 · 진행 중 마취 | 같음 | `view.ts:23,32` · `:64` |
| 5 | call | 호출 | 흰 · `border-primary text-primary` | 귀가 대기 아님 · 받을 시술이 남은 호출 있음 | `board.calls`에 그 visit 있음 | `view.ts:24,33` · `:65` |
| 6 | doing | 진행 | `bg-primary-100 border-primary` | `state==doing` | 같음 | `view.ts:25,34` · `:66` |

- 고른 칸은 `outline 2px var(--ms-primary)`(`Aside.tsx:182`). 같은 칸을 다시 눌러도 풀리지 않는다(`onFilter(f.id)` — `Aside.tsx:168`). 탭을 옮기면 필터 · 포커스가 풀린다(`…/live/page.tsx:70-75`).
- 숫자는 `text-typo-title-sm-600`, 6칸은 한 줄 `repeat(6, minmax(0,1fr))`(`Aside.tsx:164,189-191`).
- **「귀가」 칸은 없다**(P-3 — 아래 §9).

### 3.3 범례 5개 (제목 줄)

`시술 대기(warning) · 마취 중(purple) · 시술 진행(primary) · 확인 필요(danger) · 귀가 대기(neutral)` — `view.ts:9-15`

### 3.4 시술(작업) 상태 — 카드 안 줄 단위

| 상태 | 판정 | 근거 |
|---|---|---|
| `done` | KOS `status == DONE` | `B/domain/rules.py:100-102` |
| `doing` | ccc `started_at` 있음 | `:103-104` |
| `wait` | 그 밖 | `:105` |

- 목록 = KOS 목록에 있고(`present`) `CANCELED`가 아닌 작업 전부(PROCEDURE + ETCETERA)다(`rules.py:75-78`). 판정(호출 · 시작 · 전부 완료 · 수납)은 `kind=procedure`만 본다(`:80-97`).
- 「확인이 필요」 판정: 귀가 대기 전(전부 완료) → 마취 ≥ 20분 → 미수락 호출 ≥ 5분 중 **하나만**. 귀가 대기 카드는 대상이 아니다(`rules.py:22-23,172-184`).

## 4. (c) 카드 해부 — `OrderCard`

카드 틀: `bg-ms-white`, 테두리는 `need`면 `border-red`, 아니면 `border-ms-gray-300`. 반경 6 · 패딩 6/8 · 세로 gap 4 · `cc-room` hover 그림자(`OrderCard.tsx:316-335` · `F/app/globals.css:37-39`). 포커스 카드 = `outline 2px primary`, 나머지 opacity 0.45, 귀가 대기 0.55(`view.ts:145-151`). 카드 안 스크롤은 없고, 큰 버튼은 `marginTop:auto`로 바닥에 붙는다(`OrderCard.tsx:295`).

| # | 줄 | 표시 필드 · 문구 | 색 · 타이포 | 조건 | 근거 |
|---|---|---|---|---|---|
| 1a | 머리 1 | `room.title`(왼쪽) · 「입실 HH:MM」(`inAt`, 오른쪽) | `title-lg-600 gray-800` / `caption-md-400 gray-600` | `inAt` 없으면 빈칸 | `OrderCard.tsx:55-62` |
| 1b | 머리 2 | 상태 Badge(sm · dot) · 오른쪽 경과 글자 | Badge §3.1. 글자: need면 `caption-md-600 text-red`, 아니면 `caption-md-400 gray-700` | 글자 = need(마취 이유 제외)면 「호출 N분 경과」 / 「완료 뒤 N분 경과」(1분 미만이면 「1분 미만」). 귀가 대기면 「귀가 대기 HH:MM」. 그 밖은 없음 | `:38-42,63-72` · `view.ts:136` |
| 1c | 머리 3 | 「KOS 반영 중」 / 「KOS 반영 실패」(오른쪽 정렬 작은 글자 · title = 실패 op · 오류) | 실패 `caption-md-500 text-red` / 중 `caption-md-400 gray-500` | `kos.status`가 `pending` 또는 `failed` | `:48-49,74-82` |
| 1d | 고객 줄 | 검은 점 7px(`#3e3e3e` 고정) · 이름(한 줄 말줄임) · 국적 칩(**KOS 코드 원문**) · 첫내원/재내원 칩 · 「수납 필요」 Badge `warning` sm | 국적 = `bg-ms-gray-200 caption-md-500`. 첫내원 = `bg-primary-100 text-primary`, 재내원 = `bg-ms-gray-200 gray-700`(`view.ts:38-39`) | 국적은 값이 있을 때만, 수납 필요는 `paymentRequired`일 때만 | `:84-112` |
| 2 | 오더 메모 | `MemoCard` 제목 「오더 메모」 · 본문(`**굵게**` 지원). 3줄 넘거나 120자 넘으면 접고 [펼치기/접기] | 본문 `body-400 gray-800` | `orderMemo`가 있을 때만 | `:115-120` · `F/lib/memo.tsx:23-59` |
| 3 | 마취 줄 | 「마취」 + 진행 중이면 「NN분 경과」(2자리), 끝났으면 「완료 N분」, 안 했으면 「안 함」 · 오른쪽 [마취 시작](outlined gray) / [마취 종료](solid blue) 26px | 진행 중 `text-purple`, `anesthesia.long`이면 `text-red` | 버튼 = 귀가 대기 아님 && (`canStart` 또는 `canEnd`) | `:121-160` · 26px 보정 `medikit-patches.css:31` |
| 4 | 선택 줄 | 체크칸(전부 ✓ · 일부 「–」) + 「전체 선택」 / 「N개 선택됨」 / 「호출할 대기 시술 없음」 | 고르면 `bg-primary-100 border-primary`, 아니면 흰 · gray-200 | 귀가 대기 아님 | `:165-193` |
| 5a | etc 줄(「방 배정」 등) | 제목 + KOS 상태 글자(대기중 · 준비중 · 호출함 · 진행중 · 완료 · 취소). 체크 · 버튼 · 배지 없음 | 제목 `body-500 gray-600`, 상태 `caption-md-400 gray-500` | `kind=etc`면 **시술 줄 맨 위**에 그림 | `:196-211` · `view.ts:56-83` |
| 5b | 시술 줄 | 체크칸 20 · 제목 · 오른쪽(「호출함」 Badge / [시작] / [종료] / 「완료」 Badge) · 둘째 줄 `procLine` | 상자: 진행 `bg-primary-100 border-primary`, 고름 `border-primary`, 그 밖 gray-200. 제목: 완료 `heading-sm-400 gray-500`, 진행 `title-sm-600 primary`, 대기 `heading-md-500 gray-800` | 아래 표 | `:212-286` |
| 6 | 큰 버튼 | [귀가 대기](solid blue md) 또는 [의사 호출 · N건] / 「시술 선택 후 의사 호출」(꺼짐) | 꽉 찬 폭(`data-fill-buttons`) | **`!home && (canCall \|\| canHome)`일 때만 보임.** `canHome`이 우선 | `:291-313` |

**시술 줄 오른쪽 · 둘째 줄**

| 경우 | 오른쪽 | 둘째 줄 문구(`procLine`) | 근거 |
|---|---|---|---|
| done | 「완료」 Badge neutral | 「<원장> · HH:MM~HH:MM」(caption-400 gray-500) | `OrderCard.tsx:276-280` · `view.ts:92-95` |
| doing | [종료] solid blue(`canFinish`) | 「<원장> · HH:MM 시작」 | `:271-275` · `view.ts:96` |
| wait · 유효 호출 미수락 | 「호출함」 Badge primary + 파랑 외곽선(`data-badge-call`) + [시작] 꺼짐 | 「전체 호출 · 수락 전」 / 「<원장> 지정 호출 · 수락 전」 | `:214,259-270` · `view.ts:99` · `medikit-patches.css:35-36` |
| wait · 수락됨 | [시작] outlined blue | 「<원장> 수락 · 시작 가능」(`caption-md-600 text-primary`) | `view.ts:97-98` |
| wait · 호출 없음 · 담당의 있음 | [시작] | 「<원장>」 | `view.ts:100` |
| wait · 담당의 없음 | [시작] 꺼짐 | 「담당의 미정」(gray-500) | `view.ts:101` |

- **줄 순서**: etc(sequence 순) → 완료(완료 시각 순) → 진행 → 대기(sequence 순)(`view.ts:75-83`). back도 같은 순서로 보낸다(`B/domain/rules.py:84-90`).
- **조건부 표시 요점**
  - 「방 배정 · 준비중」 줄은 **지금 그린다**(`OrderCard.tsx:196-211`).
  - `canCall`이 false면(예: etc만 있는 카드, 남은 시술이 진행 중뿐인 카드) **큰 버튼 자리가 통째로 없다**(`OrderCard.tsx:294`). `canCall` 판정은 `B/service/board_service.py:122`.
  - `canStart` · `canFinish` · `pickable` · `canCall` · `canHome` · `need`는 모두 back이 계산하고 front는 쓰기만 한다(`view.ts:1` 주석 · `B/domain/rules.py:123-135`).

## 5. (d) 상호작용

| 무엇 | 동작 | 근거 |
|---|---|---|
| 실시간 갱신 | **SSE 하나**(`EventSource GET /api/board/stream?token=`). 폴링은 없다. 이벤트는 `board` 하나이고 본문은 전체 스냅샷 + `version`. `version`이 같거나 작으면 버린다. 끊기면 기본 재연결(`retry: 3000`). 닫히면(401 등) `/api/auth/me`로 확인해 401이면 세션을 지우고, 아니면 3초 뒤 다시 연다 | `F/lib/hooks.ts:60-114` · `F/lib/api.ts:56` · `B/api/board.py:15-23` · `B/service/stream.py:9-54` |
| 발행 주기(back) | ① 조작 직후(`changed` → `publish` + KOS kick) ② 일정 조회 tick 뒤 ③ 직원 · 방 조회 뒤 ④ op 상태 변화 ⑤ **heartbeat: 마지막 발행 뒤 `KOS_POLL_SCHEDULE_SEC`(기본 10초)가 지나면 발행** + 날짜가 바뀌면 전날 카드를 내림. ping은 15초 | `B/container.py:48-72` · `B/main.py:64` · `B/kos/runtime.py:51-64,66-74` · `B/config.py:26` · `B/service/stream.py:10` |
| KOS 조회 주기 | 일정 10초 · 직원/방 3600초(+ 서버 시작 1회) · 조회 창 `09:00-21:00` KST. 조작으로 보낸 것이 있으면 1.5초 뒤 일정 1회 더 | `B/config.py:26-28` · `B/kos/runtime.py:23,43-49,104-114` |
| 경과 시간 | `useNow` 1초 + 서버 시각 skew 보정(`board.now - Date.now()`) | `F/lib/hooks.ts:21-28,86-87` · `…/live/page.tsx:30` |
| 조작 호출 | 모두 `lib/api.ts`에서 부른다. 응답은 `{ok…}`만 받고 화면은 뒤따르는 SSE로 바뀐다. 401이면 세션 삭제, 그 밖 오류는 **오류 문구를 토스트로** 보인다 | `F/lib/api.ts:58-69` · `…/live/page.tsx:50-66` |
| 토스트 | 아래 가운데 · `bg-ms-gray-800 text-ms-white` · 2.6초 · 되돌리기 없음. 문구: 「<방> 마취 시작/종료」 · 「<방> <이름> 귀가 대기」 · 「<방> N개 시술 · 전체 호출 / <원장> 호출」. [시작] · [종료] · 수락 · 다른 원장에게는 **성공 토스트가 없다**(실패면 오류 토스트) | `…/live/page.tsx:40-47,79-104,246-267` |
| 의사 호출 | 카드에서 대기 시술을 체크 → [의사 호출 · N건] → `placePopover`(버튼 아래, 모자라면 위). 팝오버 왼쪽 = 검색 + 추천(「모든 의사」 ALL 「콜 잡은 원장이 집도」 + 원장 목록, 비어 있는 원장 먼저, 「대기」/「시술 중」). 하나만 고르고 다시 누르면 해제. 오른쪽 = 「선택됨」 + 「호출할 시술 · N개」. CTA는 「의사를 선택하세요」(꺼짐) / 「<원장> 호출」 / 「모든 의사 호출」. 헤더에 **✕ 닫기 버튼**이 있다. 보낸 뒤 체크를 비운다 | `F/components/procedures/CallPopover.tsx:16-25,45-78,101-206` · `…/live/page.tsx:87-102` |
| 호출 탭(의국) | 「수락 대기 N건」 · 호출 카드(오래된 순): 「전체 호출/지정 호출」 Badge · 방 · 「호출 N분」(≥ `limits.callMin`이면 빨강 · 빨간 테두리) · 「기준 N분 / 기준 도달 / +N분 초과」 · 이름 · 국적 · 받을 시술 목록. 전체 호출 → 「담당의 선택」 목록(보라 점 `#ac47ff` · 「<방> 시술 중」/「비어있음」) → [<원장> 수락]. 지정 호출 → 「지정 <원장> 상태」 + [다른 원장에게] · [수락]. 아래에 「최근 수락」 3건. 카드를 누르면 그 카드에 포커스 | `F/components/procedures/Aside.tsx:262-448` |
| 고객 탭 | 고객 줄: 상태 Badge · 이름 · 방 / 번호 원 시술 줄(etc 제외 · sequence 순 · 「호출함 · 전체/<원장>」 · 완료/진행 중/대기). 귀가 대기는 0.55. 누르면 포커스 토글 | `Aside.tsx:451-555` |
| 검색 | 이름 · 읽기 · **차트번호** 부분 일치(공백 무시). 결과를 누르면 고객 탭으로 옮기고 그 카드에 포커스. placeholder 「고객 검색 — 영문 이름 · 한글 읽기」 | `Aside.tsx:54-61,79-127` |
| 현황 탭 아래 | 「확인이 필요한 고객」 목록(since 오름차순 = 경과 긴 순). 카드 = 「확인 필요」 Badge · 방 · 담당(진행 중 원장 → 배정 원장 → 「미배정」) · 이름 + 이유 문구 · 빨간 상자(종류 · N분 · 초과 글자 · 막대 · 「기준 N분」). 빈 문구 「확인이 필요한 고객 없음」 | `Aside.tsx:142-259` |
| 앱(시술실 앱)과 주고받는 것 | 웹과 앱이 **같은 back · 같은 SSE 스냅샷 · 같은 조작 API**를 쓴다. 웹에서 직접 앱을 부르는 코드는 없다. 연결점은 back에 있다: ① 호출 생성/다른 원장에게 뒤 `on_call` → APNs 원장 푸시 ② 수락 `source`(`X-Accept-Source` 헤더, 없으면 Origin 있음 = `web`, 그 밖 = `app`). 웹 `acceptCall`은 그 헤더를 싣지 않는다 | `B/container.py:90` · `B/service/actions.py:130,153` · `B/api/actions.py:37-50` · `F/lib/api.ts:63-64` |

## 6. (e) 데이터 필드 표 — 화면 → front 타입 → back 응답 → KOS 원천

KOS 경로(`B/kos/sync.py:22-24`):
- **[내부]일정** = 내부 API `POST {KOS_INTERNAL_API_BASE}/tenants/{tenantId}/schedule/v2/queries/get-schedules-grouped-by-zone` `data[].schedules[]`
- **[내부]방** = 내부 `schedule/zone/room/v1/queries/get-rooms`
- **[공개]직원** = 공개 API `account/open/v1/queries/get-accounts`

「ccc」 = KOS에 없고 ccc DB에서 계산하거나 저장하는 값이다.

| 화면 필드 | front 타입(`F/lib/types.ts`) | back 응답(`B/schemas/board.py`) · 계산 | KOS 원천 | 근거 |
|---|---|---|---|---|
| 방 이름 · 배치순 키 | `Card.room.{title,order}` (`:30-34,98`) | `Card.room` ← `visit.room_id` → `room` (`board_service.py:76-78`) | [내부]일정 `tasks[](type=ETCETERA, room 있음).room.{id,title,order}` (+ [내부]방 `data[].{id,title,order}` 1시간) | `sync.py:38-44,91-96,176-179` |
| 입실 HH:MM · 입실순 | `Card.inAt` | `iso(visit.room_assigned_at)` (`board_service.py:112`) | [내부]일정 그 방 작업의 `roomAssignedDateTimeUtc` | `sync.py:102` |
| 귀가 대기 HH:MM | `Card.homeAt` | 귀가 대기일 때만 `iso(visit.flow_step_at)` | [내부]일정 `flowStepUpdatedDateTimeUtc` | `board_service.py:112` · `sync.py:107` |
| 상태 Badge | `Card.state` | `VISIT_STATE[flow_step]` (`rules.py:25,65-66`) | [내부]일정 `flowStep` (반영 대기 중 changeFlowStep이 있으면 덮지 않음) | `sync.py:105-107` |
| 고객 이름 | `customer.name` | `customer.name` | [내부]일정 `visitor.name` | `sync.py:86-89` |
| (검색) 읽기 | `customer.phoneticName` | 같음 | [내부]일정 `visitor.phoneticName` | 같음 |
| 국적 칩 | `customer.nationality` | 같음(가공 없음) | [내부]일정 `visitor.nationality` (코드 원문) | 같음 |
| 첫내원/재내원 | `customer.isNew` | 같음 | [내부]일정 `visitor.isNew` | 같음 |
| (검색) 차트번호 | `customer.chartNumber` | 같음 | [내부]일정 `visitor.chartNumber` | 같음 |
| 수납 필요 | `Card.paymentRequired` | PROCEDURE 작업 중 하나라도 `payment_required` (`rules.py:96-97`) | [내부]일정 `tasks[].paymentRequired` | `sync.py:126` |
| 오더 메모 | `Card.orderMemo` | `visit.order_memo` | [내부]일정 `orderMemo` | `sync.py:101` |
| 마취 경과 · 완료 N분 · 길어짐 | `Card.anesthesia.*` | `running_anes` · `last_anes_minutes` · `anes_long` (`rules.py:157-169`) | **ccc**(KOS 없음) | `board_service.py:117-119` |
| 시술 제목 · 순서 | `Procedure.{title,sequence}` | `p.title` · `p.kos_sequence` | [내부]일정 `tasks[].title` · `sequence` | `sync.py:122-125` |
| etc 여부 | `Procedure.kind` | `kind` | [내부]일정 `tasks[].type` (`PROCEDURE` / `ETCETERA`, 그 밖은 버림) | `sync.py:120,124` |
| etc 상태 글자 | `Procedure.kosStatus` | `p.kos_status` | [내부]일정 `tasks[].status` | `sync.py:129` · `view.ts:59-73` |
| 시술 상태 | `Procedure.state` | `proc_state` = KOS DONE → done / ccc `started_at` → doing / wait | KOS `status` + ccc | `rules.py:100-105` |
| 시작 시각 | `Procedure.startedAt` | `p.started_at` | **ccc** | `board_service.py:92` |
| 완료 시각 | `Procedure.completedAt` | done일 때만 `p.completed_at` | [내부]일정 `tasks[].completedDateTimeUtc` | `sync.py:134` · `board_service.py:92` |
| 원장 이름(줄) | `Procedure.doctor.{id,name}` | `shown_doctor` = `doctor_staff_ids` 중 원장 목록 계정 첫째 (`rules.py:116-121`) | id: [내부]일정 `tasks[].doctors[].id` / 이름: [공개]직원 `data[].name` (목록에 없으면 일정 `doctors[].name`) | `sync.py:59-69,130,174-175` |
| 호출함 · 수락 정보 | `Procedure.call.*` | 유효 호출 + 수락 (`rules.py:107-111`) | **ccc**(`doctor_call` · `call_accept`). KOS `doctorCallDateTime`은 저장만 하고 화면엔 안 씀 | `board_service.py:81-86` · `sync.py:133` |
| 체크 · 시작 · 종료 가능 | `pickable` · `canStart` · `canFinish` | `rules.py:123-135` · `board_service.py:94-95` | ccc 계산 | — |
| 큰 버튼 | `Card.canCall` · `canHome` | `board_service.py:122-123` | ccc 계산 | — |
| 확인 필요 | `Card.need` | `rules.need` | ccc 계산(KOS 완료 시각 · ccc 마취 · ccc 호출) | `rules.py:172-184` |
| KOS 반영 중/실패 | `Card.kos` | `kos_op` 상태 (`board_service.py:104-109,125`) | ccc(`kos_op` 표) | — |
| 원장 목록 · 비어있음/시술 중 | `Board.doctors[]` | `is_doctor` 직원 + `busy_room` (`board_service.py:26-30` · `rules.py:43-56`) | [공개]직원 `roleTags` 에 `DOCTOR` · `activate` · 시스템 계정 아님 · `KOS_EXCLUDE_ACCOUNT_IDS` 아님 | `sync.py:174-175,180` · `B/repository/repo.py:231-241` |
| 6칸 개수 | `Board.counts` | `board_service.py:59-67` | ccc 계산 | — |
| 기준 분 | `Board.limits` | 상수 5 / 20 | ccc | `rules.py:22-23` · `board_service.py:71` |
| 마지막 KOS 동기화 · 실패 · 조회 시간 밖 | `Board.sync` | `sync_state.schedules` · `in_window` | ccc(조회 성공 시각 · 오류) | `board_service.py:70` · `sync.py:189-196,211` |
| 호출 탭 카드 | `Board.calls[]` | `open_calls` · `receivable` | ccc | `board_service.py:41-50` |
| 최근 수락 | `Board.recentAccepts[]` | `w.recent_accepts` | ccc | `board_service.py:52-57` |
| 지점 이름 「세라미크 명동점」 · 「명동점」 | (없음) | (없음) | **하드코딩**(KOS 원천 없음) | `AppHeader.tsx:75` · `…/live/page.tsx:140` |

> 스냅샷 필드 가운데 화면에 쓰지 않는 것: `Procedure.call.acceptedAt`, `Card.customer.chartNumber`(검색만), `doctors[].busyRoom`(팝오버는 「시술 중」만 보이고 호출 탭은 씀). 원천을 못 찾은 필드는 없다.

## 7. (f) 테마

- **디자인 시스템**: `@medisolve-ai/medikit` 1.4.0(`F/package.json:12`). 쓰는 컴포넌트는 `Badge` · `Button` · `Menu` · `Tabs` · `BadgeVariant` 타입이다(`…/live/page.tsx:5` · `OrderCard.tsx:4` · `Aside.tsx:5` · `CallPopover.tsx:5` · `view.ts:2`). 스타일은 `@medisolve-ai/medikit/styles`를 import한다(`F/app/layout.tsx:3`).
- **tailwind**: 3.x + `medikitPreset`만 쓰고 프로젝트 자체 토큰은 없다(`F/tailwind.config.ts:1-14`). 클래스는 medikit 토큰이다: `bg-ms-*` · `text-ms-gray-*` · `text-primary` · `bg-primary-100` · `border-primary` · `text-red` · `bg-red-100` · `text-purple` · `bg-purple-100` · `bg-yellow-100` · 타이포 `text-typo-{title-lg/md/sm, heading-md/sm, body, caption-md}-{400,500,600}`.
- **제품 오버라이드**: `[data-product="ceramique"]`에서 `--ms-primary #2498bd` · `-50/-100 #e9f5f8` · `-300 #d3f4fe` · `-500 #b2e3f2` · `-shadow`(`F/app/styles/ceramique-theme.css:3-10`). `<html data-product="ceramique">`(`F/app/layout.tsx:14`).
- **medikit 보정 CSS**: `Menu-1/2` · `Button-1/2/3`(`data-fill-buttons` · `data-compact-buttons` 26px) · `Tabs-1/2`(aside 탭 균등) · `Badge-1`(`data-badge-call` 파랑 외곽선). `Token-1` 메모에 「success = primary와 구분 안 됨」이 남아 있다(`F/app/styles/medikit-patches.css:1-44`).
- **글꼴**: `pretendard/dist/web/variable/pretendardvariable.css` import(`F/app/layout.tsx:2`, `pretendard` 1.3.9). `font-family`를 직접 지정하는 곳은 front 코드에 없다 → **실제 적용 글꼴은 medikit styles에 달려 있어 확인 못 함**(node_modules 없음).
- **로고**: `/ceramique-logo-color.svg`. 헤더 22/18px, 로그인 20px(`AppHeader.tsx:51` · `F/app/login/page.tsx:71` · `F/public/ceramique-logo-color.svg`).
- **globals.css**: `a #2498bd` · `.cc-btn` · `.cc-input`(48px · r8 · `#e3e3e3`) · `.cc-room:hover` 그림자. 그 밖에 이 화면에서 안 쓰는 cc 잔재(`ip-pulse` · `rv-*` · `cc-text`)가 있다(`F/app/globals.css:1-135`).
- **토큰 밖 하드코딩 색 · 값**: 고객 점 `#3e3e3e`(`OrderCard.tsx:85`), 원장 점 `#ac47ff`(`Aside.tsx:368`), 판 배경 fallback `#f5f6f8`(`…/live/page.tsx:117`), 로그인 배경 `#e9ecef`(`login/page.tsx:40`), 막대 fallback `#e5484d`(`Aside.tsx:239`), 그림자 rgba 여러 곳. 스타일 대부분은 tailwind 클래스가 아니라 **인라인 `style`**이다.
- 다크 모드: 없음(관련 코드 없음).

## 8. (g) 상태 변형

| 변형 | 표시 | 근거 |
|---|---|---|
| 세션 확인 전 · 없음 | 페이지 `return null`, 헤더 `return null`. 없으면 `/login` | `…/live/page.tsx:68` · `AppHeader.tsx:22` · `hooks.ts:41-43` |
| 로딩(스냅샷 전) | 판 안 회색 글자: `live.error` 또는 「불러오는 중…」(연결됨) / 「서버에 연결하는 중…」. Aside는 숨김 | `…/live/page.tsx:223-227,229` |
| 설정 오류 | `NEXT_PUBLIC_API_BASE_URL`이 비면 「back 주소(NEXT_PUBLIC_API_BASE_URL)가 비어 있어요 — …」를 판에 보이고 SSE를 열지 않는다 | `F/lib/api.ts:9-12` · `hooks.ts:61,64` |
| 빈 상태 | 카드 0이면 「시술 대기 중인 고객 없음」, 필터 결과 0이면 「조건에 맞는 고객 없음」. 호출 탭 「수락 대기 중인 호출 없음」, 현황 탭 「확인이 필요한 고객 없음」, 검색 「검색 결과 없음」, 팝오버 「검색 결과가 없어요」 | `…/live/page.tsx:217-221` · `Aside.tsx:122-126,251-255,420-424` · `CallPopover.tsx:156-160` |
| 동기화 에러 | 제목 줄 「동기화 실패」(빨강 · title = 오류). 카드는 마지막 값 그대로 | `…/live/page.tsx:148-152` |
| 조회 시간 밖 | 제목 줄 「조회 시간 밖」(gray-500) | `…/live/page.tsx:143-147` |
| 연결 끊김 | 화면에 따로 표시하지 않는다(`connected`는 로딩 문구에만 쓰고, 스냅샷이 있으면 마지막 값 그대로) | `hooks.ts:89-90` · `…/live/page.tsx:225` |
| 조작 실패 | 오류 문구 토스트 · 401이면 세션 삭제 | `…/live/page.tsx:56-62` |
| KOS 반영 | 카드 머리 「KOS 반영 중 / 실패」 | §4 1c |
| 반응형 | 경계 `(min-width: 760px)`, SSR은 wide로 가정. **좁으면**: 사이드바 · Aside(호출 탭 포함) 숨김, 시계 · 지점명 숨김, 헤더 패딩 16, main 패딩 16, 격자 줄 최소 높이(cqh) 끔 → 카드 내용 높이. 넓으면 카드 폭 ≥ 300 auto-fill | `hooks.ts:9-18` · `…/live/page.tsx:120,126,199,229` · `AppHeader.tsx:43,51,69-78` |

---

## 9. 스펙 ↔ 코드 어긋난 자리

| # | 항목 | 스펙 · 문서 | 코드 | 근거 |
|---|---|---|---|---|
| 1 | **OQ-517 / P-2 「방 배정 · 준비중」 줄** | 웹에서 빼기로 기록(E2E-10) · 다음 수정 batch | 아직 **시술 줄 맨 위에 그린다**(제목 + KOS 상태 글자) | `OrderCard.tsx:196-211` · `view.ts:76-83` · SPEC §5.1 308줄 · §10 OQ-517 |
| 2 | **P-1 토스트 위치** | 앱은 위(「웹/앱 같은 규칙」 후보) · SPEC §6.3은 위치를 정하지 않음 | 웹은 **아래 가운데** `bottom:28` | `…/live/page.tsx:246-254` |
| 3 | **P-3 「귀가」 칩** | 앱엔 있음(T5) | 웹 현황 6칸(전체 · 확인 · 대기 · 마취 · 호출 · 진행)에 귀가 칸 없음 · `counts`에도 home 필드 없음 | `view.ts:19-26` · `B/schemas/board.py:31-37` |
| 4 | **P-4 `canCall` · 바닥 버튼** | SPEC §5.11: [의사 호출]은 「귀가 대기 아님 · 전부 완료 아님」이면 **보임**(켜짐 = 체크 ≥ 1). 원본 r4 Q4는 꺼진 버튼이 보임 | `!canCall && !canHome`이면 **버튼 자리가 통째로 없다**. `canCall`은 pickable(대기) 시술이 1개 이상일 때만 true → etc만 있는 카드, 남은 게 진행 중 시술뿐인 카드는 바닥 버튼 없음 | `OrderCard.tsx:294` · `B/service/board_service.py:122` · SPEC §5.11 416 · 417줄 |
| 5 | **P-5 국적 칩** | 원본 시안은 한글 이름 | KOS 코드 원문 그대로(대응표 없음) | `OrderCard.tsx:93-100` · `Aside.tsx:329-333` |
| 6 | **OQ-518 웹 로그인 역할** | 결정: 웹 = 관리자 | front · back 모두 역할로 막지 않음. 세션도 3역할 다 받음 | `F/app/login/page.tsx:27-29` · `F/lib/session.ts:12,34` · `B/api/auth.py:9-12` |
| 7 | 팝오버 닫기 | §6.5 「바깥 누르면 닫힘 · [취소] 없음」 | 바깥 닫힘에 더해 **헤더 ✕ 버튼**이 있다([취소] 글자 버튼은 없음) | `CallPopover.tsx:82,121-129` |
| 8 | 검색 결과 클릭 | §6.4 「결과 누르면 그 카드 강조」 | 강조에 더해 **고객 탭으로 옮긴다**(검색어 지움) | `Aside.tsx:92-96` |
| 9 | 검색 대상 | §6.4 「이름 · 읽기」 | 차트번호도 찾는다(§7.2 「chartNumber는 검색에만」과는 맞음). placeholder는 「영문 이름 · 한글 읽기」 | `Aside.tsx:56-60,83` |
| 10 | 지점 이름 | §6.2 「지점 이름」 · 「명동점 · 마지막 KOS 동기화」 | 「세라미크 명동점」 · 「명동점」 하드코딩(env · 데이터 아님) | `AppHeader.tsx:75` · `…/live/page.tsx:140` |
| 11 | 사이드바 메뉴 | §6.2 medikit `Menu` 「시술 현황」 | 있음. 다만 클릭을 `preventDefault`로 막아 이동하지 않음(장식) | `…/live/page.tsx:120` |
| 12 | 오류 토스트 | §6.3 토스트는 시안 문구(성공)만 | 실패도 back 오류 `message`를 같은 토스트로 보인다 · 시작/종료/수락/다른 원장에게는 성공 토스트 없음 | `…/live/page.tsx:61,84-85,103-104` |
| 13 | 수락 출처 | §7.3 `X-Accept-Source` 선택 | 웹은 헤더를 싣지 않고 back이 Origin으로 `web`을 추정 | `F/lib/api.ts:63-64` · `B/api/actions.py:42-50` |
| 14 | etc 상태 문구 표 | §7.2 `kosStatus` 값 = NOT_STARTED · WAITING · READY · DONE · CANCELED | front 표에 `IN_PROGRESS` · `PROGRESS` · `COMPLETED` · `CANCELLED`가 더 있음(무해 · 여분) | `view.ts:59-69` |
| 15 | 카드 높이 | §6.3 「px 상수 금지」 · 판 높이 절반 최소 | 맞음(`100cqh` 계산). 다만 좁은 화면에서는 최소 높이를 끈다(스펙은 좁은 화면 높이를 말하지 않음) | `…/live/page.tsx:180,199` |

같다고 확인한 주요 항목: 범례 5 · 6칸 정의 · 필터 재클릭 무해제(§6.7 #10) · 탭 이동 시 해제 · 확인 필요 빨간 테두리 · 마취 버튼 대기/진행 모두 · 「호출함」 누를 수 없음 · 되돌리기 없음 · SSE만(폴링 없음) · version 순서 · `limits` 값만 사용 · 760 미만 Aside 숨김 · 팝오버 560×440 · 아래/위 배치 · 보낸 뒤 체크 비움.

## 이슈 · 코디가 확인할 것

1. 현재 현황판은 **상태별 칸(열) 보드가 아니라 단일 격자 + 우측 패널 필터**다. 새 「전체현황판」이 칸반형이면 정렬 · 필터(§3) 구조가 바뀐다. 다음 판 비교 때 첫 축으로 보길 권한다.
2. 스타일 대부분이 인라인 `style`이고 tailwind는 medikit 토큰 클래스만 쓴다. 새 디자인의 토큰 · 글꼴이 medikit과 다르면 `ceramique-theme.css`를 덮어쓰는 것만으로는 부족할 수 있다(추정이 아니라 구조 사실만 적음).
3. 글꼴 · medikit 컴포넌트 실제 모양은 node_modules가 없어 **확인 못 함**이다. 필요하면 다음 판에서 `npm install`을 허용해야 한다.
4. 열린 결정은 그대로다: OQ-517 · OQ-518 · OQ-519(원장 목록 데모 표식 계정 — 코드는 `KOS_EXCLUDE_ACCOUNT_IDS` env만 지원, `B/repository/repo.py:239-240`) · P-1~P-5.

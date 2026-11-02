# 검수 — 프론트 「세 벌 뼈대」 (SPEC-004 v0.5.1 · 커밋 `952f8f5`) · 2026-09-14

검수자: reviewer (read-only). **코드도 문서도 한 글자 고치지 않았다** — 검증용 probe 는 돌린 뒤 지웠고
`git status` 가 비어 있다.
대상: `952f8f5` 하나(12파일). `a4d1c93`(사이드바 5파일)·`backend/` 는 대상 밖이다.
정본 보정 둘을 반영했다 — 벌 이름은 **`memo`·`ai`·`final`** 이고(§4.0-2 본문은 낡았다),
**원본 두 벌을 여는 자리는 만들지 않는다**(`OQ-319` 닫힘).

---

## 0. 판정

**조건부 PASS — FAIL 3 · WARN 3 · nit 1.**

일곱 갈래는 **일곱 다 닫혔다.** 「조용히 통과하는 자리」 다섯도 다섯 다 제대로 서 있다 —
`?? 'memo'` 류 폴백 0건 · SSE `ai_batch` 가 사람 벌을 못 지움 · 두 게이트를 혼동하지 않음 ·
**줄 id 가 모든 저장 경로에서 실림**(409 경로 포함, 실측) · 결론 표시가 회의 중 어느 탭에도 없음.

FAIL 셋은 **한 뿌리**다 — 회의록 본문은 `track` 으로 걸렀는데 **본문 «밖» 의 세 소비자가
걸러지지 않은 `agendas` 를 그대로 받는다.** 내가 백엔드에서 낸 F-1 과 같은 결의 누락이다:
한 벌 시절에 맞던 호출부가 벌 축이 생기며 조용히 틀린 코드가 됐다.

---

## 1. 일곱 갈래 대조표

| # | 갈래 | 확인한 자리 | 판정 |
|---|---|---|---|
| ① | 탭마다 자기 벌의 안건 목록 | `MeetingDetailPage.tsx:503 shownTrack`(live→memo/ai · planned·cancelled→memo · 그 밖→final) · `:557 trackAgendas = agendas.filter(a => a.track === shownTrack)` · `:562 shownAgendas` · `:928 shownAgendas.map` · `index={index}` 라 번호가 벌 안에서 1부터 선다 | **PASS**(본문) / 본문 밖은 F-1·F-2 |
| ② | 게이트 벌별 셋 + `can_add_agenda` | `viewModels.ts:861 MeetingTrackGates` · `:~940 can_edit_agendas: MeetingTrackGates` · `can_add_agenda: MeetingTrackGates`(선언이 없던 필드를 새로 받았다) · `MeetingDetailPage.tsx:321 canEditAgendas = Boolean(agendaGates?.[shownTrack])` · `:323 canAddAgenda` · `:345 agendaAddOpen` 이 **`canAddAgenda`** 를, `:340 agendaOpen` 이 **`canEditAgendas`** 를 읽는다 — **혼동 없다** | **PASS** |
| ③ | 종료는 최종 벌만 (`OQ-319` 「만들지 않는다」) | `shownTrack` 이 done·failed 에서 `"final"` 이므로 memo·ai 는 걸러진다. 탭·드로어·접힘·컨트롤 **0건**(grep: `원본`·`drawer`·`접` — 걸린 것은 전부 자료 드로어 등 기존 자리) | **PASS** |
| ④ | 결론 표시 최종 벌 한정 | `MeetingDetailPage.tsx:966` `mark={settled && agenda.track === "final" ? … : null}` | **PASS** |
| ⑤ | 자리표시 제목 (§12 R-50) | `labels.ts:~470 agendaHead: (position, title) => title ? \`안건 ${position}. ${title}\` : \`안건 ${position}\`` · `AgendaBlock.tsx:82` 가 `titlePlaceholder` 로 클래스를 건다 · `MeetingDetailPage.tsx:975 titlePlaceholder={agenda.title_placeholder}` | **PASS**(클래스는 nit) |
| ⑥ | 저장이 줄 id 를 싣는다 (§8-9) | `MeetingDetailPage.tsx:83 DraftLine{line_id?,text}` · `:85 linesOf` 가 `line_id` 를 든다 · `:440 draftOf` · `:498` 저장이 `{...line, text: trim}` 로 **id 를 보존** · `:510` **409 경로도 `linesOf(stale,"final")`** · `:940 onChange` 가 `{...line, text}` · `:935 onAdd` 가 `{text:""}`(id 없음=새 줄) · `api.ts:970 lines?: Array<{line_id?; text}>` | **PASS**(실측 §3) |
| ⑦ | 계보는 타입만 | `merged_from`·`from_lines` grep 결과 **`viewModels.ts:879`·`:932` 두 자리뿐**이고 화면 코드에 0건 | **PASS** |

### 1.1 「조용히 통과하는 자리」 다섯 — 전수 재확인

| 자리 | 무엇을 봤나 | 결과 |
|---|---|---|
| `?? 'memo'` 류 폴백 | `grep -rnE "\?\? *['\"]memo\|\|\| *['\"]memo\|track *\?\?" src/` | **트랙 폴백 0건.** 걸린 둘은 `MessageList.tsx` 의 `body_state ?? "final"` — 채팅 도메인의 기존 값이고 회의 트랙과 무관 |
| SSE `ai_batch` 가 사람 벌을 지우나 | `MeetingDetailPage.tsx:562-565` — 갈아 끼우기가 **`aiTab && stream.batch` 조건 «안»** 이고 그 안에서 **`.filter(a => a.track === "ai")`** 로 한 번 더 거른다. `trackAgendas`(사람 벌)에는 손대지 않는다 | **지우지 못한다.** 워커 주장이 맞다. `MeetingLive.test.tsx:1093` 이 그것을 못박았다 |
| 두 게이트 혼동 | 「진행 중」+메모 탭에서 `canAddAgenda=true`·`canEditAgendas=false` → `agendaOpen=false`(지우기 닫힘) · 본문 `agendaAddOpen=false`, 더하는 자리는 `MemoComposer` 의 [+ 새 안건] | **혼동 없다.** 단 그 자리의 «대상 목록» 이 F-1 이다 |
| 줄 id 가 모든 저장 경로에서 | 첫 저장 · `onChange` · `onAdd` · **409 재저장**까지 코드로 확인하고 **실측**(§3) | **전 경로에서 실린다** |
| 결론 표시가 회의 중에 서나 | `settled && track==="final"` 이라 live 에서는 `settled=false` | **서지 않는다.** `MeetingLive.test.tsx:1081` 이 두 탭 모두 건다 |

---

## 2. 지적 목록

> FAIL 셋은 한 뿌리다 — `MeetingDetailPage.tsx:366 agendas`(세 벌 합본)를 본문 밖 세 자리가 그대로 쓴다.
> `:557` 은 걸렀지만 `:1052`·`:1127`·`:1031` 은 걸르지 않았다.

### F-1 · **FAIL** — 메모 칸의 「대상 안건」 드롭다운이 **AI 벌 안건을 고르게 한다**

**자리** `frontend/src/features/meetings/MeetingDetailPage.tsx:1052` — `<MemoComposer agendas={agendas} …>`
(`agendas` 는 `:366` 의 **세 벌 합본**이고 `trackAgendas` 가 아니다)

**실측 — 돌려서 봤다** (사람 벌 안건 1 + AI 벌 안건 1 인 「진행 중」 회의)

```
PROBE OPTIONS:     [ '안건 1', '안건 2' ]        ← 둘째는 AI 벌 안건이다
PROBE MEMO TARGET: [ 'm1', 'a-1', '적은 말' ]   ← addMeetingMemoLine 이 AI 안건 id 로 간다
```

**근거**
- §4.1-6 · §6-8 — **「AI 벌의 안건은 사람이 언제도 고치지 못한다」**, 메모는 사람 벌의 안건에만 매달린다(§4.0-1).
  화면이 **계약이 금지한 대상을 고르게 내주고 있다.**
- 서버는 막는다 — `backend/…/application.py:524 ensure_line_track(TRACK_MEMO, agenda_track=agenda.track)` 가
  **422** 를 던진다. 그런데 `MemoComposer.tsx:69` 의 `catch` 는 사유를 가리지 않고 `failed=true` 만 세우므로
  사람은 **「메모를 저장하지 못했습니다」 한 줄만 보고 왜인지 알 수 없다.** 회의 중에 적은 말이 사라진다.
- 번호도 어긋난다 — `MemoComposer.tsx:99` 가 `${meetingScreen.agenda} ${index + 1}` 로 **배열 인덱스**를 쓴다.
  `order` 가 벌 안에서 1부터 다시 매겨지므로(백엔드 §4.5) 합본에서는 「안건 2」가 AI 벌의 «안건 1» 이다.
  회의록 본문의 「안건 1」과 드롭다운의 「안건 1」이 다른 것을 가리킬 수 있다.
- **「안건이 없으면 비활성」 불변식도 깨진다** — `MemoComposer.tsx:39 empty = agendas.length === 0`.
  사람 벌이 비어 있어도 AI 벌이 차 있으면 `empty` 가 거짓이 되어 드롭다운이 열리고,
  기본값 `agendas[0]` 이 AI 안건일 수 있다.

**언제 터지나** — 회의가 시작되고 **첫 배치가 한 번 돌면** AI 벌 안건이 상세 응답에 실린다.
그 순간부터 실회의에서 계속 재현된다. `0.4.x` 에서는 안건이 한 벌이라 이 줄이 맞는 코드였다 —
벌 축이 생기며 조용히 틀린 코드가 됐다.

**테스트가 왜 못 잡았나** — 「자리표시 제목」 검사(`MeetingLive.test.tsx:1117`)가 단정을
`.scax-note__body` 안으로 좁히면서 주석에 이렇게 적었다:

```
/* 회의록 칸 «안» 에서만 본다 — 메모 칸의 대상 드롭다운도 「안건 1」이라 문서 전체로 보면 둘이다 */
```

**드롭다운이 걸러지지 않았다는 사실을 보고도 단정 범위를 좁혀 비켜 갔다.** 그 주석이 이 FAIL 의 자백이다.

### F-2 · **FAIL** — [다음 회의 예약]이 **원본 두 벌까지 담아** 연다

**자리** `MeetingDetailPage.tsx:1127` — `initialAgendas={record.agendas.filter(a => !a.concluded)…}`
(`record.agendas` 는 세 벌 전부. 트리거는 `:826 settled && attendee` 라 **세 벌이 다 차 있는 상태**다)

**실측** (최종 벌 2 — 결론 남/안 남 — 과 사람 벌·AI 벌 원본 하나씩인 「종료」 회의)

```
PROBE BOOKING TEXT: … 안건 1 사람 벌 원본  지난 회의에서 넘어옴
                       2 AI 벌 원본       지난 회의에서 넘어옴
                       3 최종 · 결론 안 남 지난 회의에서 넘어옴 …
```

**근거**
- §4.1-11 — 「[다음 회의 예약]은 **최종 벌의 결론 안 난 안건**을 담아 예약 모달을 연다」.
  담겨야 할 것은 **하나**(「최종 · 결론 안 남」)인데 **셋**이 담겼다.
- 필터 `!a.concluded` 가 이제 무력하다 — §4.0-5 가 「사람 벌·AI 벌의 안건은 **결론 여부를 갖지 않는다**」고
  했으므로 원본 두 벌은 `concluded` 가 언제나 거짓이다. **원본은 한 건도 걸러지지 않는다.**
- AI 벌 안건은 배치가 회차마다 갈아 끼우던 중간 산물이다. 그것이 「지난 회의에서 넘어옴」 출처를 달고
  **다음 회의의 사람 벌에 그대로 선다** — 사람이 지우지 않으면 회의가 이어질수록 불어난다.

### F-3 · **FAIL** — 안건 20개 한도를 **세 벌 합산**으로 센다

**자리** `MeetingDetailPage.tsx:1031` — `disabled={agendas.length >= 20 || …}`

**근거** §4.0-3 — 「**벌마다** 안건은 20개까지다 — **합쳐서 20이 아니다**」.
서버는 벌마다 센다(`backend/…/application.py:994 ensure_agenda_capacity(agenda_count(meeting, track=track))`).
화면만 합산해서 세므로, 예컨대 사람 벌 8 · AI 벌 12 인 회의에서 **사람 벌에 아홉째 안건을 세울 수 있는데도
[안건 추가]가 잠긴다.** 세어야 하는 것은 `trackAgendas.length` 다.

**도달성은 낮다** — 한 회의에 안건이 20개 쌓여야 한다. 그래도 계약과 다르게 도는 것은 분명하다.

### W-1 · **WARN** — 409 경로가 줄 id 를 든다는 사실을 **테스트가 잠그지 않았다**

`MeetingAfter.test.tsx:373 「저장 충돌은 덮어쓰지 않고 지금 있는 줄로 갈아 끼운다」` 는
**입력칸의 «값» 만** 본다. `linesOf(stale, "final")` 를 `.map(l => l.text)` 로 되돌려도
**이 검사는 그대로 통과하고** 다음 저장이 계보를 통째로 버린다.
워커 스스로 보고서에 「여기서 글자만 뽑으면 다음 저장이 계보를 통째로 버린다」고 적어 둔 자리인데
그 성질만 잠그지 않았다. 지금 구현은 맞다(§3 실측) — **잠금이 없을 뿐이다.**

### W-2 · **WARN** — 커밋 위생: 사이드바 작업의 라벨이 세 벌 커밋에 섞였다

`952f8f5` 의 `frontend/src/lib/labels.ts` 에 **`shellNav`**(좌측 기둥 머리의 말 — 알림·설정·로그아웃)이
들어 있다. 그것을 쓰는 곳은 **`a4d1c93` 의 `App.tsx:32,399,402,420`** 뿐이다.
즉 사이드바 작업이 두 커밋에 걸쳐 있고, `952f8f5` 는 자기 커밋에서 **쓰이지 않는 export** 를 싣는다.
`a4d1c93` 만 되돌리면 죽은 코드가 남고, `952f8f5` 만 되돌리면 `App.tsx` 가 깨진다.
**세 벌 작업 자체가 사이드바 커밋으로 샌 것은 없다**(`a4d1c93` 에 `features/meetings`·`lib` **0건**) —
샌 방향이 반대다.

### W-3 · **WARN** — 「진행 중」의 «보기만 하는 창» 이 AI 벌로 떨어지는 근거가 코드 주석뿐이다

`MeetingDetailPage.tsx:503-509` — `shownTrack` 이 `live && !attendee` 일 때 `"ai"` 다
(`:424 aiTab = live && (!leftTabs || left === "ai")` 도 같은 결).
§4.2-6 표는 「진행 중」에 두 탭을 두지만 **탭이 없는 창이 어느 벌을 보는지는 계약이 말하지 않는다.**
기존 동작을 이어받은 것이라 회귀는 아니지만, 공유받은 사람에게 **사람 벌을 가리는** 판단이므로
(§8-11 의 「참석자·공유받은 사람에게 원본을 가릴 이유가 없다」와 결이 다르다) 스펙이 한 줄 정해 주어야 한다.

### nit · `scax-agenda-block__title--placeholder` 에 CSS 가 없다

`AgendaBlock.tsx:82` 가 그 클래스를 거는데 **`src/` 전역에 그 선택자를 정의한 규칙이 0건**이다
(커밋에 `.css` 파일이 없다). 자리표시 제목이 보통 제목과 **똑같이 그려진다.**
§12 R-50 이 요구한 「번호를 두 번 붙이지 않는다」는 지켜졌으므로 계약 위반은 아니다 —
다만 건 클래스가 아무 일도 하지 않는다.

---

## 3. 저장이 계보를 살리는가 — **살린다** (백엔드에서 살린 것을 프론트가 죽이지 않는다)

백엔드 검수에서 `save_final_lines` 가 계보를 잇는 것을 확인했다. 프론트가 그 앞단에서 id 를 버리면
헛일이므로 **가장 위험한 경로(409 충돌 재저장)를 직접 돌려 봤다.**

```
① [수정] → 줄 하나를 고침
② 저장 → 서버가 409 meeting_agenda_stale 로 「지금 있는 줄」(line_id: l9)을 함께 냄
③ 화면이 그것으로 갈아 끼움 → 사람이 그 위에 다시 고침
④ 다시 저장 →
   PROBE RESAVE PAYLOAD:
   {"lines":[{"line_id":"l9","text":"그 위에 내가 다시 고친다."}], "expected_last_saved_at":"…"}
```

**409 를 거친 뒤에도 `line_id` 가 실린다.** 네 갈래가 모두 살아 있다 —
id 보존(`:498`) · 본문만 갱신(`:940`) · 새 줄은 id 없이(`:935`) · 충돌 재적재도 id 째(`:510`).
**판정: 프론트는 계보를 죽이지 않는다.** 남은 것은 그 성질의 «잠금» 뿐이다(W-1).

---

## 4. 내 백엔드 검수 §5 목록과의 대조

백엔드 검수가 센 프론트 계약 13건 전수 대조. **빠진 것은 없고, 처리가 불완전한 것이 하나다.**

| # | 백엔드 §5 항목 | 프론트 처리 | 판정 |
|---|---|---|---|
| 1 | `can_edit_agendas` 객체화 | `viewModels.ts:~940` · `MeetingDetailPage.tsx:321` | ✅ |
| 2 | `can_add_agenda` 신설 | 같은 자리 `:323` — **선언이 없던 필드를 새로 받았다** | ✅ |
| 3 | `agenda.track` 신설 | `viewModels.ts:855 MeetingTrack` · `trackAgendas` | ✅ |
| 4 | `agenda.merged_from` 신설 | 타입만 (`:932`) — 계약대로 안 그린다 | ✅ |
| 5 | `line.from_lines` 신설 | 타입만 (`:879`) | ✅ |
| 6 | `source` 의 `ai` 은퇴 · `null` 허용 | `viewModels.ts` 타입 + `labels.ts` 에서 「AI 정리」 제거 + `meetingAgendaSourceText(source: string \| null)` | ✅ |
| 7 | 빠른 시작 `title` 이 `""` | `labels.ts agendaHead` 가 번호만 낸다 | ✅ |
| 8 | `agendas` 가 세 벌 · `order` 벌별 재시작 | 본문은 `trackAgendas` 로 걸렀다. **메모 칸 드롭다운·예약 모달·20 한도는 걸러지지 않았다** | ⚠ **F-1·F-2·F-3** |
| 9 | `export` 폴백 제거 | 화면은 URL 링크 하나라 할 일 없음 (`:822`) | ✅ (N/A) |
| 10 | PATCH `lines` 가 `{line_id,text}` | `api.ts:970` · 저장 전 경로 | ✅ |
| 11 | 원본 벌에 `lines` → 409 · 비-최종에 `concluded` → 409 | 줄 편집은 `lineEditing`(done·failed)에서만 열리고 `draftOf` 가 `"final"` 고정. **`concluded` 는 이 화면이 아예 PATCH 하지 않는다**(grep 확인) | ✅ |
| 12 | **SSE `ai_batch` 가 AI 벌만** | `:562` `aiTab && stream.batch` + `track==="ai"` 필터. 검사로 못박음(`MeetingLive.test.tsx:1093`) | ✅ |
| 13 | MCP inventory | 프론트 무관 | N/A |

내 백엔드 §5 가 **F-2 의 항목(`OQ-319`/§4.1-11 예약 이월)을 목록에 올리지 않았다** — 그 자리는
envelope 필드가 아니라 «세 벌이 한 배열로 온다» 의 파생이라 8번에 묶여 있었다. 다음 목록에는 갈라 적어야 한다.

---

## 5. 테스트 판정

```
npx tsc --noEmit  → 오류 0
npx vitest run --no-file-parallelism → 566 passed (566) · Errors 1
npx vite build    → ✓ built in 1.16s
```

### 5.1 새 검사 여덟이 «갈림 자체» 를 거나

**여덟 다 건다. 빈 단언이 하나도 없다.** 픽스처의 두 벌이 **서로 다른 제목·다른 줄**을 들어서
(`MeetingLive.test.tsx:1006 memoSide` / `:1012 aiSide`) 한 벌 시절 코드로는 통과할 수 없다.

- `:1019` — 탭을 넘기며 `getByText`/`queryByText` **양방향**으로 본다. 목록이 안 갈리면 반대쪽이 남아 실패한다
- `:1037` — `getAllByText(/^안건 1\./)` 가 **정확히 1개**. `order` 벌별 재시작 때문에 합치면 바로 깨진다
- `:1045` — 게이트를 `{memo:true, ai:false, final:false}` 로 주고 **AI 탭에서** 편집 자리 셋이 없음을 건다.
  불리언 하나이던 때 `Boolean(객체)` 가 늘 참이던 그 자리다
- `:1056` — `can_edit_agendas.memo=false` + `can_add_agenda.memo=true` 로 **두 게이트가 갈렸음**을 건다.
  한 필드만 읽는 구현으로는 통과 못 한다
- `:1093` — 배치를 실제로 `emit` 한 뒤 **메모 탭에 사람 벌이 남아 있음**을 건다. 갈아 끼우기 조건을 놓치면 깨진다
- `:1070`·`:1081`·`:1117` — 승격 자리 없음 · 결론 표시 없음 · 번호 두 번 안 붙음. 셋 다 음성 단정이 실질적이다

**다만 `:1117` 의 단정 범위 좁히기가 F-1 을 가렸다** — §2 F-1 참조.

### 5.2 고친 기존 테스트에 약화가 있나 — `git diff` 전수

**약화 0건.** 두 자리를 특히 봤다.

| 자리 | 무엇을 바꿨나 | 판정 |
|---|---|---|
| `MeetingLive` 픽스처를 두 벌로 (`agenda`/`aiAgenda`) | 0.4.x 픽스처는 **안건 하나에 `memo`·`ai` 줄을 같이** 매달았다. §4.2-9(「줄은 자기 벌의 안건에만 매달린다」)가 그 모양을 계약에서 지웠으므로 픽스처가 계약을 어기고 있었다. 가르지 않으면 새 검사가 실제로 아무것도 밟지 못한다 | **정당** |
| `MeetingAfter` 「출처 다섯 → 넷 + null」 | `source: "ai"` 케이스를 뺀 대신 **`expect(queryByText("AI 정리")).toBeNull()`** 과 **`source: null` 이면 자리가 안 선다**를 **새로 걸었다**. 단정이 하나 줄고 둘 늘었다 | **강화** |
| 전 파일 픽스처에 `track`·`title_placeholder`·`merged_from`·`from_lines` 추가, 게이트 객체화 | envelope 변경을 타입이 강제한 결과 | **기계적** |
| `MeetingDetail` 저장 검사 | `lines: ["…"]` → **`lines: [{ line_id: "l1", text: "…" }]`** — ⑥의 잠금이다 | **강화** |

### 5.3 실패 · 오류 분리

- **`Errors 1 error`** — `src/features/work/WorkViews.tsx:542` 의 `event.dataTransfer` 가 jsdom 에 없어 나는
  Unhandled Error. 발주서가 「원래 있던 것」이라 짚었고, `MyWorkPage.test.tsx` 단독 실행 **3회 모두**
  `20 passed + 1 error` 로 같은 모양이다. 회의와 무관하다.
- **⚠ 그 오류가 «테스트 실패» 로 계상될 때가 있다** — 내 첫 전체 실행은
  `Tests 1 failed | 565 passed`(그 오류가 `MyWorkPage.test.tsx` 의 칸반 검사에 붙었다)였고,
  두 번째 실행은 `566 passed`였다. **회의 파일은 두 실행 모두 전부 초록**이다.
  워커 보고의 `566 passed / 0 failed` 는 재현되지만, **`vitest` 종료 코드는 1** 이므로
  CI 에 걸면 이 오류부터 걷어야 한다(회의 작업과 별건).

---

## 6. 범위 · 커밋 위생

| 확인한 것 | 방법 | 결과 |
|---|---|---|
| 충돌 판정 UI (`OQ-308` · D-3) | `grep -rniE "merge_conflict\|conflict\|나란히\|side-by-side"` | **0건.** 걸린 것은 전부 409 저장 충돌(기존 자리)과 무관한 산문 |
| 원본 두 벌을 여는 자리 (`OQ-319`) | 탭·드로어·접힘·컨트롤 grep | **0건.** 사용자 결정과 일치 |
| 계보를 그렸나 | `grep merged_from\|from_lines` | **타입 두 줄뿐**, 화면 코드 0건 |
| `backend/` 수정 | `git show --stat 952f8f5 -- backend` | **0줄** |
| 코디가 고친 둘이 섞였나 | `git show --stat 952f8f5 -- …/shell.css …/glyphs.tsx …/shell` | **0줄.** 그 둘은 `5e7a41d` 에 이미 있고 셋째 커밋을 만들지 않은 판단이 옳다 |
| 세 벌 작업이 사이드바 커밋에 샜나 | `git show --stat a4d1c93 -- …/features/meetings …/lib` | **0줄** |
| 반대 방향 | `labels.ts` 의 `shellNav` | **샜다 → W-2** |
| 워크트리 | `git status --porcelain` | **비어 있다.** 내 probe 는 전부 지웠다 |

---

## 7. 코디가 가져갈 것

1. **F-1 을 먼저 닫아라** — `MeetingDetailPage.tsx:1052` 를 `agendas={trackAgendas}`(또는 memo 벌 목록)로.
   실회의에서 첫 배치가 돌면 바로 재현되고, 사람이 적은 메모가 이유 없이 실패한다.
   `MemoComposer.tsx:99` 의 번호도 `index+1` 대신 그 벌의 `order` 를 쓰는 것이 맞다.
2. **F-2** — `:1127` 을 `record.agendas.filter(a => a.track === "final" && !a.concluded)` 로 (§4.1-11).
3. **F-3** — `:1031` 을 `trackAgendas.length >= 20` 으로 (§4.0-3).
4. **W-1** — 409 검사에 「재저장 페이로드가 `line_id` 를 싣는다」 한 줄을 더해 잠가라.
5. **W-2** — 다음 커밋부터 라벨도 소속 작업의 커밋으로. 이미 선 둘은 되돌릴 일이 없으면 그대로 둬도 된다.
6. **W-3** — 「탭이 없는 창(공유)이 어느 벌을 보는가」를 스펙 한 줄로.
7. `vitest` 종료 코드 1(`WorkViews.tsx:542`)은 회의와 별건이지만 CI 전에 걷어야 한다.

*검수용 probe 셋(메모 칸 드롭다운 · 409 재저장 · 예약 모달)은 돌린 뒤 삭제했고 워크트리는 비어 있다.*

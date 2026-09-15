# 프론트 — 「최종 회의록만 회의록이다」 + 검수 FAIL 3

정본: `decision-final-is-the-note.md` (사용자 결정 2026-09-14)
워크트리: `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting-room` · 브랜치 `kknaksss/sc-meeting-room` · **미커밋**

## 한 줄

**합본을 넘기는 «경계» 가 둘이었다.** 하나는 상세 화면(`MeetingDetailPage`), 하나는 예약 모달의
「지난 회의 이어가기」(`BookingModal.applySuggestion`) — 두 번째는 브리프에 없던 자리다. 둘 다 막았다.

---

## ⑤ `agendas` 소비처 전수 — 어느 벌을 받아야 하는가

`grep -rn 'agendas' src --include='*.tsx' --include='*.ts'` 의 전수다 (테스트 제외).
**「합본」 이 닿으면 안 되는 자리**를 ⚠ 로 표시했다.

### A. 합본이 만들어지는 곳 (원본)

| 자리 | 무엇 | 판정 |
|---|---|---|
| `MeetingDetailPage.tsx:376` | `agendas` = `record.agendas` + `stream.agendas` 를 `agenda_id` 로 합친 것 | **원본.** 세 벌이 섞여 있다. 이 값을 «그대로» 받는 소비처가 있으면 안 된다 |
| `MeetingDetailPage.tsx:576` | **`byTrack` = 경계.** `{memo, ai, final}` 로 가른다 | 이 아래 소비처는 전부 여기서 꺼내 쓴다 |
| `lib/viewModels.ts:982` | `MeetingRecord.agendas` 타입 | 계약. 세 벌 합본이 맞다 |
| `lib/api.ts:906/950/975/982/992` | 안건 CRUD 경로 | 벌 축 없음. 그대로 |

### B. 상세 화면의 소비처 — 일곱 자리

| # | 자리 | 받아야 하는 벌 | 이번에 |
|---|---|---|---|
| 1 | `trackAgendas` (본문 안건 목록) | **지금 보는 벌** (`byTrack[shownTrack]`) | 그대로 (앞 판에서 고쳤다) |
| 2 | `aiTrackArrived` (AI 벌이 왔는가) | `byTrack.ai` | 그대로 |
| 3 | `saveNote()` 의 `changed` (PATCH 대상) | **`byTrack.final`** — 줄 편집은 최종의 일이다 (§8-9). 임시 벌로 나가면 409 | 그대로 + **테스트로 잠갔다** |
| 4 | `MemoComposer agendas=` (메모 대상 드롭다운) | ⚠ **`byTrack.memo`** — 메모는 사람 벌에만 매달린다 (§4.2-9). AI 안건을 고르면 **422** | **FAIL ②** |
| 5 | `[안건 추가]` 의 20 한도 | ⚠ **그 벌** (`trackAgendas.length`) — 합산이면 사람 벌 19개인데 죽는다 | **FAIL ③** |
| 6 | `BookingModal initialAgendas=` (다음 회의 예약) | ⚠ **`byTrack.final`** + `!concluded` | **FAIL ①** |
| 7 | `shownAgendas` (AI 배치 갈아 끼우기) | `stream.batch.agendas` 를 `track === "ai"` 로 한 번 더 거른다 | 그대로 |

### C. 상세 화면 «밖» — 브리프에 없던 두 번째 경계

| 자리 | 받아야 하는 벌 | 판정 |
|---|---|---|
| ⚠ `BookingModal.tsx:218` `applySuggestion()` | **`final`만** | **이번에 고쳤다.** 이 길은 `initialAgendas` 를 안 거친다 — `readMeeting(picked.meeting_id)` 의 응답을 «직접» 훑어서 결론 안 난 안건을 담는다. §B-6 을 고쳐도 이 길로 임시 두 벌이 다음 회의에 실려 간다. 실측의 「모달에 5개」는 **두 길 다** 낼 수 있는 증상이다 |
| `BookingModal` 의 다른 `agendas` (110·187·246·409·411·436) | 해당 없음 | 모달 «자기» 초안 목록(`AgendaDraft[]`)이다. 벌 축이 없는 값이라 거를 것이 없다. 436 의 `>= 20` 도 초안 한 벌이라 맞다 |
| `MemoComposer.tsx:39/40/99` | `memo` | 넘겨받은 것을 그대로 쓴다. 거르는 책임은 부르는 쪽(§B-4)이다 — 부품이 벌을 알 필요는 없다 |
| `stream.ts:37/46/111/151/155/173/241` | AI 배치 / 새 안건 프레임 | 서버가 낸 `track` 을 그대로 싣고 지운다. §B-7 과 §A 의 합본이 거른다 |
| `features/action/ActionMeetingCard.tsx:20` | 해당 없음 | 주석 한 줄. 코드 아니다 |

**결론: 합본이 닿으면 안 되는 자리는 다섯(B-3·4·5·6 · C-1)이고, 그중 넷이 상세 화면 한 파일 안이라
`byTrack` 하나로 한 번에 막힌다. 다섯 번째(C-1)만 다른 파일에서 따로 막아야 했다.**

---

## 고친 것

### ① 다음 회의 예약 — 최종 벌만

- `MeetingDetailPage` 의 `initialAgendas` 는 `byTrack.final.filter(!concluded)` (앞 판에서 이미)
- **`BookingModal.applySuggestion` 에 `agenda.track !== "final"` 거르기를 더했다** ← 이번 판
- `concluded` 만으로 못 거르는 이유를 코드 주석에 박았다: 결론 표시는 최종 벌에만 서므로(§4.0-5)
  임시 두 벌은 전부 `false` 로 통과한다

### ② 메모 대상 드롭다운 — 사람 벌만

`agendas={agendas}` → `agendas={byTrack.memo}`

### ③ 안건 20 한도 — 벌마다

`agendas.length >= 20` → `trackAgendas.length >= 20`

### ④ 진행 중 사람 벌 고치기·지우기 — **서버 값을 읽는다**

```
- const agendaAlways = canEditAgendas && (planned || cancelled);
+ const agendaAlways = canEditAgendas && shownTrack === "memo";
```

화면이 `planned || cancelled` 로 한 번 더 판단하던 것을 걷었다. 열지 말지는 **서버가 낸
`can_edit_agendas.memo` 하나**가 정한다 — 진행 중에도 참이면 열린다. 직접 판단하지 않는다.
(AI 벌은 서버가 언제나 거짓을 내므로 `shownTrack === "memo"` 는 «벌» 조건이지 «상태» 조건이 아니다.)

### ⑤ 경계 하나로 막기

```ts
const byTrack = {
  memo:  agendas.filter((a) => a.track === "memo"),
  ai:    agendas.filter((a) => a.track === "ai"),
  final: agendas.filter((a) => a.track === "final"),
};
```

**훅이 아니다.** 처음에 `useMemo` 로 짰다가 렌더가 통째로 깨졌다 (`Rendered more hooks than
during the previous render` → MeetingLive 5건 적색). 이 자리는 이른 `return`(454·464)보다 아래라
훅으로 두면 렌더마다 훅 개수가 달라진다. 게다가 `agendas`(376) 자체가 렌더마다 새로 만들어지는
배열이라 `useMemo` 가 아낄 것도 없었다. 평범한 계산으로 되돌렸고 그 이유를 주석에 남겼다.

---

## 테스트 — 여덟 개를 더했고 **전부 적색을 먼저 봤다**

| 파일 | 테스트 | 적색 확인 방법 |
|---|---|---|
| `MeetingList.test.tsx` | 「지난 회의 이어가기」도 최종 벌만 담는다 | `track !== "final"` 거르기를 뺐더니 적색 |
| `MeetingAfter.test.tsx` | [다음 회의 예약]은 최종 벌만 담는다 | (경계가 이미 서 있어 녹색. 잠금용) |
| `MeetingAfter.test.tsx` | 저장은 최종 벌 안건만 보낸다 | 〃 |
| `MeetingLive.test.tsx` | 메모 드롭다운에는 사람 벌만 뜬다 | `agendas={agendas}` 로 되돌렸더니 적색 |
| `MeetingLive.test.tsx` | 진행 중에도 사람 벌 안건을 고치고 지운다 | `&& (planned \|\| cancelled)` 를 되살렸더니 적색 |
| `MeetingDetail.test.tsx` | 20 한도는 벌마다 센다 (사람 19 + AI 5 + 최종 5) | `agendas.length >= 20` 으로 되돌렸더니 적색 |
| `MeetingDetail.test.tsx` | 그 벌이 20을 채우면 못 더한다 (한도 자체는 산다) | 한도를 지우면 적색 |
| `MeetingAfter.test.tsx` | **W-1:** 줄 셋 중 하나만 고쳐도 나머지 둘의 `line_id` 가 실린다 | `line_id` 를 패치에서 빼니 적색 |
| `MeetingAfter.test.tsx` | **W-1:** 409 로 갈아 끼운 뒤 다시 저장해도 서버가 준 `line_id` 가 실린다 | 〃 |

---

## 검증

| 게이트 | 결과 |
|---|---|
| `npx tsc --noEmit` | **통과** (종료 코드 0, 출력 없음) |
| `npx vitest run` | **50 파일 · 575 테스트 전부 통과** |
| `npx vite build` | **통과** (1.27s) |

**`vitest` 종료 코드는 여전히 1 이다** — `src/features/work/WorkViews.tsx:542` 의 `event.dataTransfer`
가 jsdom 에서 `undefined` 라 `MyWorkPage.test.tsx` 실행 중 Unhandled Error 하나가 난다.
**테스트는 575개 전부 녹색이고, 내가 만진 파일이 아니다. 지시대로 고치지 않았다.**

브라우저 육안 검증은 하지 않았다 — 사용자가 직접 한다.

---

## 하지 말라던 것

- 충돌 판정 UI (OQ-308) — 안 만들었다
- 원본 두 벌을 여는 자리 (OQ-319) — 탭·드로어·접히는 구획 어느 것도 안 더했다. 컨트롤 수 그대로다
- 계보 그리기 — 안 그렸다. `line_id` 는 **보내는 값**으로만 쓴다 (화면에 안 낸다)
- `backend/` — 한 줄도 안 건드렸다
- 사용자 로컬 스택 — 안 건드렸다
- `git add .` · push · PR — 안 했다

## 보고할 것 둘

1. **워크트리에 내 것이 아닌 미커밋 변경이 있다.** `Makefile` · `backend/` 8개 파일이
   `git status` 에 떠 있다 (`bootstrap/application.py` · `entrypoints/http.py` ·
   `modules/meetings/{application,finalize,policy}.py` · `schemas/ai_final_output.json` ·
   `platform/organization_access.py` · 백엔드 테스트 둘). **내가 만든 것이 아니고 건드리지 않았다.**
   커밋을 붙일 때 경로를 골라 담아야 한다.
2. **W-2 (커밋 위생):** `shellNav` 라벨이 세 벌 커밋 `952f8f5` 에 함께 들어갔다.
   **되돌리지 마라** — 사이드바 작업의 산출물이고 지금 화면이 그 이름으로 선다.
3. 내 미커밋 산출물: `frontend/src/features/meetings/{MeetingDetailPage,BookingModal}.tsx` ·
   테스트 넷 · `frontend/package.json`(e2e 스크립트 한 줄) · `frontend/scripts/meeting-three-tracks-e2e.mjs`(미추적)

## 남은 것 — 막혀 있다

**세 벌 e2e 재실행.** 사용자 스택의 uvicorn(pid 68882, 10:39 기동)이 커밋 `51ecceb`(13:46)보다
앞서서 응답에 `track`·`merged_from`·`from_lines` 가 없고 `can_add_agenda` 가 불리언이다.
**사용자가 API·`meeting_worker` 를 지금 코드로 다시 띄우면** 바로 돌릴 수 있다
(`npm run e2e:meeting-three-tracks`). 죽이거나 재시작하지 않았다.

---
---

# 이어 붙임 — 백엔드 `fa49c90` 이 새로 깨뜨린 계약 (§6-4·5·6)

백엔드 보고 §6 의 전수 여섯 중 **1~3 은 위에서 고쳤고, 아래가 남은 셋이다.**

## §6-4 — 「진행 중」 사람 벌 · 상태 재추론을 걷었다

**남은 자리가 하나 있었다.** `MeetingDetailPage.tsx:319`:

```
- const canEditNote = Boolean(meeting?.can_edit_note) && !live && !settling;
+ const canEditNote = Boolean(meeting?.can_edit_note);
```

서버의 `NOTE_EDITABLE_STATUSES` 는 **「종료 · 실패 · 취소」뿐**이라 「진행 중」·「정리 중」은
애초에 거짓이다 (`policy.py:24`). 화면이 한 번 더 재단하면 같은 규칙을 두 곳이 말하게 되고,
서버가 축을 옮길 때 화면이 조용히 어긋난다. **지금은 서버 값 하나만 읽는다.**

안건 쪽(`can_edit_agendas` · `can_add_agenda`)의 상태 재추론은 **위 판에서 이미 걷었다** —
`agendaAlways` 가 `canEditAgendas && shownTrack === "memo"` 다. 남은 상태 조건 둘은 재추론이 아니다:

| 자리 | 조건 | 왜 재추론이 아닌가 |
|---|---|---|
| `agendaAddOpen` | `&& !live` | **권한이 아니라 «자리» 판단**이다 (§4.1-6). 회의 중에 안건을 더하는 자리는 본문 칸이 아니라 메모 칸의 `[+ 새 안건]` 이다(§6-4). 권한은 그대로 서버의 `can_add_agenda` 가 정한다 |
| `lineEditing` | `&& (settled \|\| failedState)` | 줄 편집 화면이 서는 «자리» 다. 「취소됨」은 줄을 고칠 수 있어도 회의록이 비어 있어 안건 목록 화면이다 (§5.7) |

### ⚠ 보고 — 「진행 중 사람 벌 [수정]」은 **UI 자체가 없다** (어느 상태에서도)

서버가 `can_edit_agendas.memo` 로 여는 것은 **「안건 제목 고치기 · 안건 삭제」** 둘이다.

- **삭제(×)** — 진행 중 메모 탭에서 **선다.** 잠갔다 (아래 테스트).
- **제목 고치기** — **프론트에 그 컨트롤이 없다. 예정에도, 종료에도, 어디에도 없다.**
  `updateMeetingAgenda` 는 줄(`lines`)로만 불리고(`MeetingDetailPage.tsx:508`),
  `AgendaBlock` 에는 제목 입력 자리가 아예 없다. 서버 게이트만 열렸고 화면이 그 칸을 안 쓴다.

**만들지 않았다.** 시안에 그 컨트롤이 없고, 「컨트롤 하나도 더하지 마라」는 서 있는 제약이다.
**새 자리를 세우는 것은 디자인 결정이라 코디·디자이너의 몫으로 남긴다.**

참고로 본문 칸의 `[수정]` 단추는 진행 중 메모 탭에서 **의도적으로 서지 않는다** —
사람 벌은 편집 모드를 거치지 않고 ×가 늘 열려 있기 때문이다(예정 화면과 같은 결).
그래서 「[수정]이 안 선다」는 증상은 맞지만 원인은 게이트가 아니라 **제목 편집 UI의 부재**다.

## §6-5 — 승격 담당 후보를 회의 전용 경로로 갈아탔다

**실제로 쓰고 있던 것은 `getTaskAssignmentCandidates` 가 아니라
`getWorkRequestAssigneeCandidates`(`api.ts:385`) 였다.** 둘 다 **누른 사람의 권한 범위**로 좁히므로
(`organization_access.py:852` — "decision-capable peers whose current org scope overlaps the requester")
갈아타야 하는 것은 같다.

```ts
// lib/api.ts (신규)
export async function getMeetingPromotionCandidates(meetingId: string): Promise<Persona[]> {
  return request<Persona[]>(`/api/meetings/${meetingId}/promotion-candidates`);
}
```

- 승격 모달의 **담당 후보만** 갈아탔다.
- **참조(cc)는 그대로 `getWorkRequestCcCandidates` 다** — 그건 「내가 누구에게 보이느냐」라
  누른 사람의 범위가 맞다. 건드리지 않았다.
- **업무 관리 쪽 호출은 한 글자도 안 건드렸다** (`TodayPage.tsx` · `MyWorkPage.tsx` 그대로).
- 효과 의존성에 `meetingId` 를 더했다 — 회의를 옮겨 열면 그 회의의 후보를 다시 받아야 한다.

## §6-6 — `orderedAssignees` 정렬을 걷었다

`MeetingDetailPage.tsx:703` 의 참석자 끌어올리기 정렬을 지우고 한 줄 주석으로 남겼다.
**서버가 이미 참석자를 앞에 두고 낸다** — 두 곳이 같은 규칙을 말하면 서버가 순서를 바꿀 때 어긋난다.

픽스처도 그 모양으로 고쳤다: 이전에는 `[한서린, 정우성]` 을 주고 화면이 뒤집기를 기대했는데,
그 픽스처로는 **화면이 정렬해도 통과한다.** 이제 서버가 내는 대로 `[정우성(참석자), 한서린]` 을 주고
**나온 순서가 그대로인지**를 본다.

## 테스트 — 둘 더했다 (둘 다 적색 먼저 확인)

| 테스트 | 적색 확인 방법 |
|---|---|
| `MeetingAfter`: 승격 담당 후보는 회의 전용 경로에서 온다 — 업무 배정 후보를 쓰지 않는다 (회의 id 를 싣는다 · 업무 쪽 둘은 안 부른다 · **본인(이건학)이 목록에 있다** · 서버 순서 그대로) | ① 옛 경로로 되돌리니 적색 ② 화면이 다시 정렬하게 하니 적색 |
| `MeetingAfter`: 정리 중에는 어느 벌도 열리지 않는다 — 화면이 아니라 서버가 닫는다 | 게이트를 걷은 뒤 서버 값 하나로 닫히는지를 건다 |

이미 있던 것으로 나머지가 잠긴다: **「진행 중」에도 사람 벌 안건을 고치고 지운다**(× 가 선다) ·
**AI 벌엔 안 선다** (위 판에서 더했고 둘 다 적색 확인 완료).

## 검증

| 게이트 | 결과 |
|---|---|
| `npx tsc --noEmit` | **통과** |
| `npx vitest run` | **50 파일 · 577 테스트** — 세 번 돌렸고 **두 번은 577 전부 통과** |
| `npx vite build` | **통과** (1.17s) |

**흔들리는 파일 둘을 그대로 보고한다** — `features/work/Checklist.test.tsx` ·
`features/action/ActionCenter.test.tsx`. 병렬 실행에서 세 번 중 한 번 적색이고,
**둘만 따로 돌리면 51개 전부 통과한다**(확인함). **내가 만진 파일이 아니다.**

`vitest` 종료 코드 1 도 그대로다 (`WorkViews.tsx:542` dataTransfer — 지시대로 안 고쳤다).

브라우저 육안 검증은 하지 않았다 — 사용자가 직접 한다.

## 손댄 파일

- `src/lib/api.ts` — `getMeetingPromotionCandidates` 신규
- `src/features/meetings/MeetingDetailPage.tsx` — 위 셋
- 테스트 다섯 (`MeetingAfter`·`MeetingDetail`·`MeetingLive`·`MeetingMaterials`·`MeetingWorkspace`)
  — 새 api 목 등록 + 후보 픽스처 순서 + 새 테스트 둘

**`backend/` 무수정 · 로컬 스택 무접촉 · `git add .` 안 했다 · 커밋·push·PR 안 했다.**

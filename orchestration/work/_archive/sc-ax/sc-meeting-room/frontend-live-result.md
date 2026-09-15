# 회의 «중» 화면 5항목 — frontend 결과 보고

작업 워크트리 `ax-workspace/sc-meeting-room` · 브랜치 `kknaksss/sc-meeting-room` · 커밋/push/PR 없음.
이전 A~F 구현 위에서 이어 작업했다. **종료 후 범위는 한 줄도 손대지 않았다** (§7 보류 항목 참조).

---

## 1~5 결과

| | 항목 | 상태 |
|---|---|---|
| 1 | 하단 메모 입력줄 폭 + 보라 [기록] | **완료** |
| 2 | AI 요약 대기 문구 | **완료** |
| 3 | 스크립트 가독성 | **완료** |
| 4 | 진행 중 [+ 자료 첨부] | **변경 없음 — 계약이 막는다 (아래 근거)** |
| 5 | 회의 종료 버튼 | **완료(사용자 정정 반영: 빨간 solid 유지)** |

---

## 1. 하단 메모 입력줄 — 완료

**원인**: `footer` 가 두 겹이었다. 상세가 `<footer className="scax-note__composer">`(flex row)를 세우는데
`MemoComposer` 가 그 안에서 `<footer className="meeting-composer-foot">` 를 또 세웠고, 그 안쪽 것은
**flex 자식인데 자라지 않아** 내용 너비만큼만 섰다 — 그래서 칸이 왼쪽에 짧게 몰렸다(현재 화면 21).
여백도 `12/24` + `12/20` 두 겹이었다.

**고친 것**
- `MemoComposer` 의 안쪽 `footer` 를 걷고 `.scax-memo-composer{flex:1 1 auto;min-width:0}` 로 그 줄을 채운다.
- `Composer` 를 `__shell`(세로: 칸 + 실패 문장) / `__row`(가로: 칸 + 던지는 단추)로 갈랐다.
  `.composer{flex:1 1 auto;min-width:0}` 라 칸이 남는 폭을 다 먹고 단추만 제 폭을 지킨다.
- 던지는 자리를 `sendVariant="button"` 으로 열었다 — 시안 22 의 **보라 [기록]** 이 칸 «밖» 오른쪽에 선다.
  기본값 `"glyph"` 는 예전 그대로라 다른 호출부가 있어도 안 바뀐다(현재 호출부는 `MemoComposer` 하나).
- 문구는 `lib/labels` 의 `meetingScreen.recordMemo = "기록"`. ds 안에 하드코딩하지 않았다.

**지킨 것** — 대상 안건 `Select` 와 드롭다운 바닥의 **[+ 새 안건]** 은 칸 «안» 에 그대로다 (SPEC §6-4 · D45).
Enter 제출 · 빈 칸일 때 비활성 · 저장 실패 시 **친 것을 칸에 그대로 둠**(§6-7) · `can_write_memo` 권한 ·
`POST /agendas/{agendaId}/lines` 경로(§6-8) 전부 무수정. **시안의 하단 상태 데모 막대는 복제하지 않았다.**

**죽은 규칙** `.meeting-composer-foot` 는 호출부 0곳이 되어 걷었다.

## 2. AI 요약 대기 — 완료

**증상**: 「AI 요약」 탭이 AI 결과가 없을 때 사람이 쓴 안건 제목(출처 「직접 입력」)과 빈
「다음 할 일 / 후속업무 후보가 없습니다」 상자를 세워, 아무것도 안 나왔는데 정리된 것처럼 보였다(현재 화면 24).

**고친 것** — `aiTrackArrived` 를 도입하고 거짓인 동안 `meetingScreen.aiSummaryPending`
**「AI 요약이 곧 생성됩니다.」** 한 줄만 낸다(문구는 labels → prop).

```ts
const aiTrackArrived =
  Boolean(stream.batch) ||
  agendas.some(a => a.lines.some(l => l.track === "ai") || a.todos.some(t => t.provisional));
```

브리프가 짚은 두 함정을 그대로 피했다:
- **`stream.batch` 유무로만 판정하지 않는다.** 배치는 이 창이 붙어 있는 동안 온 것이라, 그것만 보면
  새로고침한 창에서 **이미 저장된 AI 요약이 숨는다.** 상세 응답이 실어 온 `track === "ai"` 줄과
  잠정 후보(`provisional`)까지 함께 본다 — 둘 다 §7.1 「적재」가 같은 트랜잭션으로 저장하는 것이다.
- **`source` 로 거르지 않는다.** AI 가 기존 안건(출처 「직접 입력」)에 줄만 붙인 경우도 유효한 결과다
  (§7.1). 출처로 걸렀다면 그 경우가 통째로 사라진다.

AI 트랙/메모 트랙 분리(§7.3)와 회의 중 후보의 **읽기 전용** 계약은 그대로다 — 승격·후보 빼기 자리를 만들지 않았다.
「메모」 탭은 이 판정에 끌려가지 않는다(적던 자리가 그대로 있다).

## 3. 스크립트 가독성 — 완료

**원인**: `LiveScript` 가 공용 `GutterList`(시각 | 화자 | 본문 **세 칸 가로**)를 썼다. 이 레일은 342 이고
앞 두 칸이 120 을 먼저 가져가 본문에 남는 폭이 200 이 안 됐다 — 두세 낱말마다 줄이 바뀌어 말이 토막났다(현재 화면 17).

**고친 것** — 줄을 «쌓는다». 폭을 못 늘리는 자리에서 **글자를 줄이는 대신 칸을 없앴다.**

```
00:15 · 화자 3                                   ← caption1 한 줄 (시각 assistive, 화자 medium)
이걸 보통 링키가 하고, 그리고 각 카카오톡 …      ← label2 / 일반 굵기 / 본문색 / 행간 1.62, 열 전체 폭
```

- 이름은 DS 가 이미 가진 `.scax-script-line*` 를 쓴다. 크기는 DS 램프 그대로 — **축소 없음.**
- 발언 간격 `--scax-space-400`(16).
- **캐릭터 가림 해소**: `.scax-script-list::after` 로 바닥 152px 을 비운다. 값은 셸이 문서형 화면에
  이미 쓰는 것과 같다(`shell.css` 의 `.scax-page-scroll`). 자료 탭은 건드리지 않는다.
- 지킨 것: 근거 점프(`active` 강조 + `scrollIntoView`) · 잠정 줄 흐림 · 메모/발화 구분 ·
  실시간 추가 · 스크롤 보존. **드래그 너비 조절은 구현하지 않았다**(미승인).

**⚠ 공용 스타일 영향 — 명시 보고**: 스크립트 줄은 진행 중과 **종료 후가 같은 부품**이라, 종료 화면의
스크립트 탭도 함께 쌓는 모양이 됐다. 종료 화면을 «따로» 고친 것이 아니고 낼 값·순서·동작은 그대로다.
되돌리려면 상태별로 갈라야 하는데 그것은 이번 승인 범위 밖이라 하지 않았다 — 코디 판단 필요.

**부수 효과**: `ds/GutterList.tsx` 와 `components.css` 의 `.gutter-*` 5종이 **호출부 0곳**이 됐다
(LiveScript 가 유일한 소비자였다). DS 자산이라 임의로 걷지 않고 남겨 두었다 — 은퇴 여부는 코디 판단.
meetings.css 가 갖고 있던 `.gutter-speaker` · `.gutter-body.muted` 둘만 걷었다(내 화면 소유 규칙).

## 4. 진행 중 [+ 자료 첨부] — 변경 없음 (계약이 막는다)

먼저 확인한 결과 **사용자 수정으로 해결된 것이 아니라, 애초에 계약이 금지하는 자리**였다.
지금 코드(`attendee && !live`)가 맞고 **아무것도 바꾸지 않았다.**

| 근거 | 내용 |
|---|---|
| SPEC §5.7-4 | 「[자료 첨부]는 **「진행 중」에 숨긴다** — 회의 중에 자료가 붙고 사라지면 보던 사람이 따라가지 못한다 (`X-117`)」 |
| backend `material_policy.py:32` | `can_attach = context.actor_is_attendee and current is not MeetingStatus.IN_PROGRESS` |
| backend `materials.py:195` | `if not access.can_attach:` → 거절 |

**시안 23 과 디자인 핸드오프(`workspace.v1.jsx`: 「첨부 단추는 상태와 무관하게 늘 선다」)가 SPEC·BE 와 어긋난다.**
단추를 세우면 눌러도 서버가 막으므로 «가짜 동작» 이 된다 — 세우지 않았다.

**미지원 계약 하나**: `can_attach` 는 서버가 «계산만» 하고 **어떤 응답에도 싣지 않는다**(`grep can_attach` →
backend 3곳, frontend 0곳). 그래서 지금 프론트는 서버 규칙을 `!live` 로 **거울처럼 따라 쓰는** 상태다.
envelope 로 판단하려면 BE 가 상세 또는 자료 응답에 `can_attach` 를 실어야 한다 — BE 요청 사항으로 올린다.
이번에는 **상태로 권한을 새로 추론하지 않았고** 기존 판단을 그대로 뒀다.
업로드 처리·모달·API 는 손대지 않았다(사용자 수정 보존).

## 5. 회의 종료 버튼 — 완료 (사용자 정정 반영)

브리프는 「검은 글자/채움 없는 형태」였고 한 번 `variant="text" tone="neutral"` 로 바꿨으나,
작업 중 **사용자가 「빨간색이 좋겠다」로 정정**하여 **DS `variant="solid" tone="danger"` 빨간 버튼으로 복원**했다.
종료 동작·확인·권한(`hosting`)은 처음부터 끝까지 무수정. 확장 아이콘 위치와 집중 모드도 그대로다.
새로 건 테스트도 **빨간 solid 를 잠그는 쪽**으로 바꿔 두어, 나중에 시안을 따라 되돌아가지 않게 했다.

---

## 변경 파일 (이번 태스크)

| 파일 | 무엇 |
|---|---|
| `features/meetings/MeetingDetailPage.tsx` | AI 대기 판정·렌더, 종료 버튼(복원) |
| `features/meetings/MemoComposer.tsx` | 껍데기 footer 제거, `sendVariant="button"` |
| `features/chat/Composer.tsx` | `__shell`/`__row` 분리, 라벨 단추 variant |
| `features/meetings/LiveScript.tsx` | 쌓는 줄로 재작성(GutterList 벗음) |
| `lib/labels.ts` | `aiSummaryPending` · `recordMemo` |
| `styles/workspace.css` | `.scax-memo-composer` · `.scax-note__pending` · `.scax-script-*` 재작성 |
| `styles/ax.css` | `.composer-shell` / `.composer-row` / `.composer{flex:1}` |
| `styles/meetings.css` | 죽은 규칙 3 제거 (`.meeting-composer-foot` · `.gutter-speaker` · `.gutter-body.muted`) |
| `features/meetings/MeetingLive.test.tsx` | 회귀 11건 추가 + 메모 단추 이름 5곳 |
| `features/meetings/MeetingAfter.test.tsx` | 스크립트 줄 선택자를 새 DOM 으로 |

`backend/` · `docs/` · `.design-sync/` · `frontend/ds-entry.tsx` **무수정.**
`.design-sync/NOTES.md` · `.design-sync/UPLOAD-BLOCKED-2026-09-14.md` 는 내 변경이 아니며 그대로 보존했다.
`AttachModal.tsx` 등 첨부 관련 파일은 **이번 태스크에서 한 줄도 만지지 않았다**(이전 태스크 변경만 남아 있다).

---

## 검증

```
cd frontend && npx tsc --noEmit                      → 오류 0
cd frontend && npx vitest run --no-file-parallelism  → 50 files / 543 passed / 0 failed
```
직전 기준 532 → **543** (+11: 회의 중 5항목 회귀).

**기본 병렬 실행은 숨기지 않고 보고한다** — `npx vitest run` 3회: `543 / 542+1실패 / 542+1실패`.
낙오한 것은 매번 **내가 안 만진** `features/work/Checklist.test.tsx` 의 서로 다른 테스트이고
(`git diff --stat -- frontend/src/features/work/` → 변경 0),
그 파일만 단독 실행하면 **3/3 전부 37 passed**. 직전 태스크에서도 파일만 바뀌며 같은 성격으로 났다.
→ 기존 부하 민감성으로 본다. 직렬 실행은 543 전량 통과.

### 새로 건 회귀 (MeetingLive.test.tsx)
1. 메모 칸이 그 줄을 채우고 [기록]이 칸 «밖» 오른쪽 · footer 가 하나 · 안건 선택과 [+ 새 안건] 유지
2. [기록]은 빈 칸에서 비활성 · 저장 실패 시 친 것이 칸에 그대로 남음
3. AI 트랙이 비면 정확한 문구만 · 사람이 쓴 안건과 빈 후보 상자 없음 · 메모 탭 무영향
4. 배치가 오면 AI 트랙으로 전환
5. **배치 없이 들어와도 저장된 AI 줄이 보임**(새로고침) · **출처가 「직접 입력」이어도 마찬가지**
6. 줄이 없어도 잠정 후보가 있으면 AI 트랙이 온 것
7. 발언이 「시각 · 화자」 한 줄 + 그 아래 본문(본문이 메타의 형제임을 확인 — 폭을 나눠 갖지 않는다)
8. 잠정/근거 강조 구분 유지
9. **「진행 중」에 [자료 첨부]가 서지 않는다** (§5.7-4 · BE `can_attach`)
10. [회의 종료]가 **빨간 solid** 이고 누르면 `endMeeting` 이 나감
11. 보기만 하는 창에는 [회의 종료] 없음

이탈 가드 잠금 2건(`MeetingWorkspace.test.tsx`)은 손대지 않았고 그대로 통과한다.
「없음」 단언으로 기능을 지운 곳은 없다 — 9번만 «없어야 한다» 이고 그것은 SPEC·BE 가 요구하는 부재다.

---

## 실제 브라우저 미검증 (명시)

사용자가 실제 회의 중 테스트를 직접 진행하므로 **쓰기성 브라우저 검증을 하지 않았다** —
회의 시작/종료·메모 저장·업로드 어느 것도 실행하지 않았다. dev server 도 띄우지 않았다.
따라서 아래는 **CSS·계약·단위 테스트 수준 근거**이고 눈으로 확인되지 않았다:
메모 줄의 실제 픽셀 폭과 [기록] 위치 · 스크립트 줄의 실제 줄바꿈과 캐릭터 가림 해소 ·
AI 대기 문구의 실제 자리 · 빨간 종료 버튼의 최종 모양.
전체 빌드 · acceptance-e2e · DB reset 은 하지 않았다.

## 코디 판단이 필요한 것

1. **종료 화면 스크립트가 함께 바뀐다** (3번의 공용 부품 영향). 되돌리려면 상태별 분기가 필요한데 미승인 범위다.
2. **`ds/GutterList.tsx` + `.gutter-*` 5종이 호출부 0곳**이 됐다. 은퇴 여부.
3. **BE 요청**: `can_attach` 를 상세/자료 응답에 실어 주면 프론트가 `!live` 거울 대신 envelope 로 판단할 수 있다.
4. 시안 23 · 디자인 핸드오프가 SPEC §5.7-4 와 어긋난다 — 시안 쪽 정정이 필요해 보인다(planner 보고 대상).

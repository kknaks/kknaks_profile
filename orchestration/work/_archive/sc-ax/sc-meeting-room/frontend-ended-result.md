# 종료 후 — 최종 회의록 생성 안내 · 후속 요청 모달 정리 (frontend 결과)

워크트리 `ax-workspace/sc-meeting-room` · 브랜치 `kknaksss/sc-meeting-room` · HEAD `9fbf4f5` · 커밋/push/PR 없음.
`backend/` 읽기만. `docs/` · `.design-sync/` · `frontend/ds-entry.tsx` · `.gitignore` 무수정(사용자 변경 그대로 보존).

| | 항목 | 상태 |
|---|---|---|
| 2 | 종료 후 생성 안내 (스피너 + 문구) | **완료** |
| 3 | 후속 요청 모달의 상태 \| 요청자 제거 | **완료** |

---

## 2. 종료 후 생성 안내 — 완료

**바꾼 것**: 「정리 중」의 회의록 칸이 스켈레톤 막대 일곱 줄이던 것을 **도는 원 + 「최종 회의록 생성 중입니다.」** 로 바꿨다.

**왜 스켈레톤이 틀린 부품이었나** — 스켈레톤은 「올 내용의 **모양을 아는**」 자리다(디자인 시스템 v2 `10 — STATE`:
실제와 같은 개수·같은 높이). 그런데 §8-5 는 합성이 **회의록을 처음부터 새로 짓는 일**이라고 말한다 —
안건도 줄도 새로 잡으므로 몇 줄이 될지 아무도 모른다. 막대 일곱 개는 «모양을 아는 척» 이었고,
실제로도 무엇을 기다리는지 말하지 않는 긴 회색 줄이 됐다(현재 화면 25).

**부품**: DS 에 스피너가 없어 `ds/Spinner.tsx` 를 더했다.
- 먼저 찾아본 결과 새 DS 에 `CircularCircular`(feedback)가 **있지만 우리 아카이브에는 `.d.ts` 만 있고
  구현(`CircularCircular.jsx`)이 없다** — 기하를 볼 수 없는 것을 베낄 수 없어, 값은 전부 `--scax-*`
  토큰으로 두고 가장 단순한 원으로 짰다(`.scax-spinner`: 트랙은 `--scax-color-line`, 도는 조각만
  `--scax-color-accent`). DS 원본이 들어오면 이 부품 «안» 만 갈아 끼우면 된다.
- **문구는 `lib/labels` 가 준다** — `meetingScreen.finalNoteGenerating`. ds 안에 하드코딩하지 않았다.
- 접근성: `role="status"` + `aria-busy="true"`, 도는 원은 `aria-hidden` 이고 **문장이 읽어 주는 말**이다.
  `prefers-reduced-motion` 이면 돌리지 않는다 — 기다리는 중이라는 사실은 문장이 말한다.

**회의 중 문구와 섞이지 않는다** — 이 자리는 `status === "summarizing"`(종료 뒤)이고,
「AI 요약이 곧 생성됩니다.」는 `aiPending`(회의 중 AI 요약 탭)이다. 두 조건은 서로 배타적이며 검사로 잠갔다.

**영원히 도는 원은 없다** — 프론트 타이머가 성공을 지어내지 않는다. 기존 폴링(`SETTLING_POLL_MS` 5초)이
상태를 다시 물어 §8-7 이면 진짜 회의록이 서고, §8-8 이면 실패 띠와 [다시 시도]가 선다. 어느 쪽이든
`settling` 이 거짓이 되어 이 자리가 스스로 걷힌다. **폴링·스트림 종료·재전사/합성 계약·재조회는 무수정.**

## 3. 후속 요청 모달 — 완료

**바꾼 것**: 회의록의 「다음 할 일」에서 [업무 생성]으로 여는 모달에서 **`상태 | 요청자` 표 전체 제거**(현재 화면 18·19).

**계약 근거** — SPEC §9-5(D40 · R-48): 「**요청자는 시스템(회의)이다.** 사람이 아니다 — 회의에서 나온
일이라 그 회의가 요청한 것으로 남는다. **누른 사람은 승격자(`promoted_by`)로 기록되고 참조로 붙는다.**」
그러니 그 자리에 누른 사람 이름을 「요청자」로 내던 것은 **계약과 어긋난 표시**였다. 상태도 언제나
「판단 대기」라 폼이 말해 줄 것이 없다.

**어떻게 갈랐나** — `CreateWorkModal` 에 **명시 prop `origin?: "meeting"`** 하나를 더했다.
- 제목·사람 이름·상태를 보고 「회의에서 온 것 같다」고 **추론하지 않는다.** 부르는 쪽이 명시로 넘긴다.
- **`size`/`narrow`(폭)로 가르지 않았다.** 폭은 「어떻게 보이나」이고 이것은 「무엇이 값인가」라 다른 축이다.
- 걷은 것은 둘: 상태 줄과 **읽기 전용** 요청자/담당자 줄. 담당자 **Select** 갈래는 건드리지 않았다 —
  조작이 사라지는 일은 없어야 한다.
- 두 줄을 걷으면 회의 모달(좁은 골격)에서는 그 표에 남는 줄이 하나도 없다(담당 후보·기한은 아래
  `.scax-field-row` 로 따로 선다). 빈 `<dl>` 은 여백만 남기므로 세우지 않는다(`metaGridShown`).

**표시만 걷었고 보내는 값은 하나도 바뀌지 않았다** — `onSubmitRequest`(승격 경로) · payload ·
`source_meeting_id`/`source_agenda_id` · 참조자 · 담당 선택 · 희망 기한 · 체크리스트 · 제출 흐름 ·
요청 성공 후 「요청됨」 표시 · 중복 방지 · 이탈 가드 · 실패 후 입력 보존 전부 그대로다.
**일반 업무 요청/일반 업무 생성 모달은 손대지 않았다**(호출부 셋 중 TodayPage·MyWorkPage 는 `origin` 미전달).

---

## 4. 이미 처리한 것 — 회귀만 확인

- **스크립트 가독성**: 앞 작업에서 공용 부품(`LiveScript`)이 바뀌며 종료 화면에도 적용됐다.
  재구현하지 않았고 회귀만 확인 — `MeetingAfter.test.tsx` 의 스크립트 검사 4건 통과.
- 첨부 업로드 · 진행 중 첨부 허용 · 회의 중 메모/AI 대기/빨간 종료 버튼 · quick-start 잠금: 무수정.
  이탈 가드 잠금 2건과 StrictMode quick-start 회귀도 이름을 지목해 따로 돌려 통과를 확인했다.

---

## 5. 변경 파일 (이번 태스크)

| 파일 | 무엇 |
|---|---|
| `frontend/src/ds/Spinner.tsx` **(신규)** | 도는 원 + 한 줄. `role=status`·`aria-busy`, 말은 호출부가 준다 |
| `frontend/src/styles/components.css` | `.scax-spinner*` + `@keyframes scax-spin` + reduced-motion |
| `frontend/src/features/meetings/MeetingDetailPage.tsx` | 「정리 중」 렌더 교체 |
| `frontend/src/features/work/WorkModals.tsx` | `origin` prop · `showOriginMeta` · `metaGridShown` |
| `frontend/src/lib/labels.ts` | `finalNoteGenerating` |
| `frontend/src/features/meetings/MeetingAfter.test.tsx` | 「정리 중」 검사 갱신 + 회귀 4건 |
| `frontend/src/features/work/CreateWork.test.tsx` | 회의/일반 갈림 검사 4건 |

## 6. 검증

```
cd frontend && npx tsc --noEmit                      → 오류 0
cd frontend && npx vitest run --no-file-parallelism  → 50 files / 555 passed / 0 failed  (3회 연속)
```
직전 기준 547 → **555** (+8).

### 검사가 진짜로 잡는지 확인 (RED)
`showOriginMeta` 를 임시로 항상 참으로 돌려 놓으니 **「상태 \| 요청자 두 줄이 서지 않는다」가 빨개졌고**,
되돌리니 초록이 됐다(확인 뒤 파일 복구 완료). 나머지 셋(필드 유지·제출값 유지·일반 요청 유지)은 그때도
초록이라 «갈림» 만 정확히 잡는다.

### 새로 건 회귀 8건
- `MeetingAfter.test.tsx` (4): 회의 중 문구와 안 섞임 · 정리 중 새로고침 · **시간만 밀어서는 안 바뀌고
  서버가 「종료」라고 해야 진짜 회의록으로 전환**(프론트 타이머가 성공을 지어내지 않는다) ·
  「실패」로 가면 사유와 [다시 시도]로 전환(영구 스피너 없음)
- `CreateWork.test.tsx` (4): 두 줄과 빈 표가 없음 · 나머지 필드 전부 유지 ·
  **실제 제출값이 그대로이고 일반 요청 경로로 새지 않음** · 회의가 아닌 요청에는 두 줄이 그대로

### ⚠ 내 새 검사 하나가 간헐로 빨개져 **고쳤다**
「정리 중에 새로고침해도 같은 안내가 선다」가 직렬 실행 1회에서 낙오했다. 원인은 내 단언이
`document.querySelector(".scax-skeleton")` 로 **문서 전체**를 봤기 때문이다 — 아직 자료를 불러오는
4칸(오른쪽 레일)의 스켈레톤이 걸렸다. 관심사인 **회의록 칸 안**으로 좁혔고, 그 파일만 5회 연속 21 통과,
전체 직렬 3회 연속 555 통과를 확인했다.

### 기본 병렬 (숨기지 않고 보고)
`npx vitest run` 3회 → `554+1 / 554+1 / 555`. 낙오한 것은 **내가 한 줄도 만지지 않은**
`features/work/Checklist.test.tsx` · `features/action/ActionCenter.test.tsx` 이고
(`git diff --stat` 으로 두 경로 변경 0 확인), 직전 세 태스크에서도 같은 두 파일이 매번 다른 테스트로
낙오했다(단독 실행은 항상 전량 통과). 기존 부하 민감성으로 본다. **직렬은 555 전량 통과.**

## 7. 실제 화면 미검증 — 명시

사용자가 실제 회의 e2e 를 직접 하므로 **회의를 만들거나 종료하지 않았고, 요청을 실제로 보내지 않았다.**
dev server 도 띄우지 않았다. 따라서 아래는 단위 테스트·계약 근거 수준이고 눈으로 확인되지 않았다:
스피너의 실제 크기·회전·여백, 「정리 중」 화면의 실제 전환 순간, 두 줄을 걷은 뒤 모달의 실제 간격.
전체 build · acceptance-e2e · DB reset 은 하지 않았다.

## 8. 미결

1. **완료 회의 정보 편집 진입점** — 시안 02 가 [수정]을 「예정」에만 두어 「완료」 회의의 정보 편집
   진입점이 없다. 사용자 결정이 아직 없어 **디자인을 발명하지 않았다.** API(`can_edit_info`)와
   `MeetingEditModal` 은 살아 있어 카드 조건 한 줄이면 되돌아온다.
2. **진행 중 첨부 허용** — SPEC §5.7-4 · BE `can_attach` 가 막고 시안 23 은 허용하는 어긋남이 그대로 남아 있다(범위 제외).
3. **`can_attach` envelope 미노출** — 프론트가 `!live` 로 서버 규칙을 거울처럼 따라 쓰는 상태(BE 요청 사항).
4. **`ds/GutterList.tsx` + `.gutter-*`** 가 호출부 0곳(앞 작업의 부수 효과). DS 자산이라 남겨 두었다.

# sc-meeting-room frontend — 회의 화면 시안 정합 결과 보고

## 상태: done (시각 검증은 사용자가 직접 — §시각 검증 참조)

---

## A~F 진행

| | 항목 | 상태 |
|---|---|---|
| A | DS 우선 · 공통 스크롤 | 완료 |
| B | 목록 잘림 · 생성/수정 | 완료 |
| C | 4칸 배치 · 회의 전 상세 | 완료 |
| D | 오른쪽 첨부/스크립트 열 | 완료 |
| E | 파일 첨부 · 공용 토스트 | 완료 |
| F | 캐릭터 말풍선 대비 | 완료 |

---

## 근본 원인 둘 (시안 근사가 아니라 원인을 고쳤다)

### 1. `box-sizing: border-box` 전역 리셋이 앱에서 «사라져» 있었다
바퀴 2 가 DS 원본 리셋 7줄을 잘라내며 「구 `styles.css` 가 이미 정해 두었다」는 이유를 달았는데,
바퀴 9-B 에서 그 파일이 지워지면서 **이 한 줄만 아무 데도 가지 못했다**
(`shell.css:5` 에 주석으로만 남아 있었다).

없으면 `width:100%` + padding + border 인 칸이 전부 부모보다 넓어진다. 그것이:
- 목록 카드가 레일 오른쪽에서 잘리던 것 (시안대비 03) — 카드 = 100% + 24 + 2
- 예약 모달의 가로 스크롤과 왼쪽 텍스트·라디오 잘림 (06)

→ `styles/shell.css` 에 되살렸다. h1~h4 리셋과 달리 **크기를 죽이지 않는다** — 넘치던 것을 칸 안에 들일 뿐.
`overflow` 를 숨겨 잘라낸 것이 아니라 폭 계산 자체를 고쳤다 (§6-A 요구).

### 2. 팝오버가 모달 «뒤» 에 그려지고 있었다
`.scax-popover{z-index:30}` 인데 `.modal-backdrop{z-index:50}` 이다. `Popover` 는 `document.body` 로
포털되므로 모달의 자손이 아니고, 쌓임 순서를 스스로 이겨야 한다. 그래서 생성 모달 안의
**지난 회의 셀렉터 · 날짜 캘린더 · 시작/종료 시간 칩이 열려 있는데도 안 보이고 눌리지도 않았다** (04·05).

→ `z-index:90` (모달 50 · 겹친 확인 60 · 자료 고르기 80 위, 최소 폭 안내 100 아래).
포털·클리핑·이벤트 경로는 이미 정상이었다 — 건드리지 않았다.

---

## 변경 파일

### 새로 만든 것 (2)
- `frontend/src/features/meetings/MeetingEditModal.tsx`
- `frontend/src/features/meetings/MeetingEditModal.test.tsx`

### 화면 (4)
- `features/meetings/MeetingDetailPage.tsx` — 머리 재구성 · 안건 상시 칸 · 4칸 재작성 (−457/+…, 순 감소)
- `features/meetings/MeetingListPage.tsx` — 카드 [수정] → 편집 모달
- `features/meetings/MeetingWorkspace.tsx` — `reloadToken` 배선
- `features/meetings/AttachModal.tsx` — 시안 12 구조 · 삭제 토스트

### DS (4)
- `ds/DropZone.tsx` · `ds/FileList.tsx` · `ds/Modal.tsx`(Toast `icon`) · `ds/icons/glyphs.tsx`

### 스타일·라벨 (9)
- `styles/shell.css` `components.css` `index.css` `meetings.css` `workspace.css` `product.css` `scax.css` `ax.css` · `lib/labels.ts`

### 테스트 (7)
`MeetingDetail` `MeetingAfter` `MeetingLive` `MeetingList` `MeetingMaterials` `MeetingWorkspace` + 새 `MeetingEditModal`

**`.design-sync/NOTES.md` 와 `.design-sync/UPLOAD-BLOCKED-2026-09-14.md` 는 내가 만든 것이 아니다** —
세션 중 다른 쪽에서 생겼다. 브리프대로 손대지 않았다. `backend/` · `docs/` · `frontend/ds-entry.tsx` 무수정.

---

## 항목별 구현

### A. DS 우선 · 스크롤
- 새 부품을 만들지 않았다. 있던 것을 시안에 맞춰 «넓혔다»: `SegmentedControl`(레일 탭) ·
  `DropZone`(시안 머리 한 줄) · `FileList`(글리프 + `__size`) · `Toast`(`icon`) · `Modal` · `Button` ·
  `DateField`/`TimeRangeField`/`PersonSearch`(편집 모달이 예약 모달과 같은 부품을 쓴다).
- DS 에 이미 규칙만 있고 마크업이 없던 것을 **되찾아 썼다** — `.scax-dropzone__head`/`__hint`/`__cursor`,
  `.scax-side-rail*`, `.scax-file-row__size`. 새로 지은 CSS 는 `.scax-side-rail__empty` 하나다.
- 구 `.btn`/`.field`/`.badge`/`.avatar` 재도입 0. 임의 hex 0.
- `ds/` 에 사람이 읽는 문구 0 — 새 prop(`drop`·`icon`·`pickLabel`)은 전부 호출부가 `lib/labels` 에서 넘긴다.
- **스크롤 막대**: `styles/scrollbar.css` 를 `index.css` 에 실었다(바퀴 1 D3 이 「바퀴 8 에서 풀면 된다」고
  남긴 줄이다). thumb/track 만 안 그리고 휠·터치·키보드는 그대로. 이 전역 규칙을 이기고 있던
  `.scax-scroll`/`.meeting-scroll` 의 hover 막대 12줄을 걷었다.

### B. 목록 · 생성/수정
- 카드 잘림 → box-sizing (위 §1). 선택 상태·구획·[더 보기] 그대로.
- 생성 모달 팝오버 → z-index (위 §2). 필수 입력·참석자·회의실·자정 넘는 예약 로직 **무수정**.
- **회의 정보 편집을 상세 연필 → 목록 카드 [수정] → 모달로 옮겼다** (시안 02).
  칸 다섯·「바뀐 것 없으면 저장 불가」·`updateMeetingInfo` patch 모양 **한 줄도 안 바꿨다**.
  권한은 모달이 `readMeeting` 으로 읽어 `can_edit_info` 로만 판정한다 — 행의 status 로 추론하지 않는다.
- **선택/편집 대상 어긋남 방지**: [수정]은 `stopPropagation` 후 «그 줄의 id» 로 모달을 열고
  **선택을 바꾸지 않는다**. 저장 뒤 목록을 다시 읽고, 고치던 회의를 «고르고 있었다면» 워크스페이스가
  `reloadToken` 으로 상세만 다시 읽게 한다(리마운트 아님 — 고치던 회의록 줄·스크롤을 잃지 않는다).
- **이탈 가드**: 잠금 2건 유지. 상세가 들고 있는 「저장 안 한 것」이 회의록 편집 하나로 줄어서
  테스트를 그 경로로 옮겼다(가드 자체·확인 전 이동 금지·확인 후 이동은 그대로 검사). 모달 닫기
  경로(× · Esc · 바깥 클릭)의 확인은 `MeetingEditModal.test.tsx` 가 새로 잠근다.

### C. 4칸 · 회의 전 상세
- `.scax-page-scroll--fixed` 의 좌우 40px 군더더기 여백 제거 → 칸이 시안처럼 맞닿는다.
  브라우저 chrome 을 앱 폭으로 계산한 곳은 없다(셸이 `100vh`/`min-width:1542px` 로 잡는다).
- 상세 머리: 「회의 정보」 라벨 + 연필 제거, **제목부터 시작**, 그 아래 메타 한 줄.
- 제목과 **같은 줄 오른쪽**에 `[확장 화살표][▷ 회의 시작]`. 보라 solid → 흰 면 + 1px 선(outlined)로
  내렸다 — 화면 맨 위 [빠른 시작](solid)과 결이 갈린다.
- 집중 모드 글리프: 네모+세로선(`left-side`) → **대각선 양방향 화살표**(`expand`/`collapse`).
  DS 원본(`design/components/icon/Icon.jsx:84~86`)에서 그대로 옮겼다 — 기하를 지어내지 않았다.
  실제 접기 기능은 그대로.
- 구분선은 칸 전체 너비(`.scax-note__body` border-top · `.scax-agenda-block` border-bottom),
  내용에는 시안의 안쪽 여백 24.
- **회의 전 안건**: 안건 목록 «바로 아래» 입력칸 + [안건 추가]가 **상시**로 선다(시안 10 ·
  `workspace.v1.jsx:221`). 예정/취소됨에서 [수정]이 하던 일이 「그 칸을 펴는 것」 하나였으므로
  단추를 내리고 칸을 열어 뒀다 — **안건 빼기(×)도 함께 상시**라 할 수 있는 일은 그대로다.
  완료·실패의 [수정]은 **그대로 둔다**(줄 편집은 명시 저장이 필요한 일이라 「고치는 중」 상태가
  화면에 남아야 한다). 권한은 여전히 `can_edit_agendas`/`can_edit_note` 가 정한다. API `addMeetingAgenda`
  ·`removeMeetingAgenda` 그대로.

### D. 오른쪽 열
- 열을 감싸던 카드(`.meeting-panel`, 1px 테두리 + 16 라운드, 짧은 고정 높이) 제거 →
  셸이 그은 세로 경계선으로 갈리고 화면 바닥까지 이어지는 `.scax-side-rail` 칸.
- 「자료」 밑줄 탭 → **회색 바탕 · 선택만 흰색**인 `SegmentedControl` [첨부|스크립트].
- 라운드는 세그먼티드 · 파일 줄 · 단추에만.
- 파일 줄: 시안의 `[문서 글리프] 이름 …… 크기 [×]` (DS `.scax-file-row__size` 복구).
- `[+ 자료 첨부]`는 **파일 목록 바로 다음 형제**. 파일이 없을 때도 칸 구조 유지 —
  열을 통째로 채우던 큰 빈 상태 카드 대신 한 줄(`.scax-side-rail__empty`).
- **스크립트 탭을 상태와 무관하게 세웠다.** 시안 주석이 「예정 회의는 스크립트가 비어 있을 뿐이다」라고
  직접 적었고, 계약도 그 말과 맞는다: `GET /api/meetings/{id}/transcript` 는 읽을 수 있는 회의면
  상태를 가리지 않고 빈 목록을 낸다(`backend/src/ax_workspace/modules/meetings/application.py:1049`).
  예전에는 예정·취소됨에 탭 자체가 없어 「아직 없다」와 「볼 수 없다」가 같은 모양이었다.
  **실제 데이터를 붙였고**(transcript 로딩 조건을 상태별에서 풀었다) 없으면 사실대로 빈 상태다.
  자료 탭은 여전히 참석자만(`viewer_relation`).

### E. 첨부 · 토스트
- 시안 12: 안내 문구 + **보라 [파일 추가]** 한 줄(`.scax-dropzone__head`), 그 **아래 같은 칸 «안»** 에
  파일 종류 글리프·이름·용량·삭제 × 행. 예전의 긴 [파일 선택] 단추와 칸 밖 목록을 걷었다.
- drag-over: 영역 전체 연보라 바닥 + 보라 점선(`--over`) + 집는 표시(`__cursor`) — 전부 DS 규칙.
- **지원 형식·크기는 계약을 따른다**: PDF · Markdown · 한 건 20MB
  (`backend/.../meetings/materials.py:31`). 시안에 URL 줄이 있지만 **만들지 않았다**.
  한도 문구(`attachLimit`)는 시안에 없어도 남겼다 — 지우면 화면이 계약보다 넓게 말한다.
- **공용 Toast**: 기존 `ds/Modal.tsx` 의 것을 확인하고 `icon` prop 만 더했다(새로 만들지 않았다).
  검은 바탕·둥근 모서리·흰 휴지통 글리프·문구, `role="status"`+`aria-live="polite"`.
  **복구하기/undo 는 넣지 않았다**(명시 제외). 토스트는 **선택 목록에서 실제로 빠진 뒤에만** 뜬다
  (이름이 없어 아무것도 안 빠지면 알림도 없다). 실패를 성공으로 표시하는 경로 없음 —
  서버 거절은 예전처럼 사유가 그 줄에 남고 `.scax-field__error` 로 따로 선다.
  기존 톤 글리프(check/circle-exclamation)는 크기 16 그대로 — 회귀 없음.
- 닫기 확인: 고른 파일이 **남아 있을 때만** 묻는다(다 빼면 안 묻는다 — 기존과 같다).
  문구를 `attachDiscardTitle` 로 갈라 **「고른 파일은 아직 첨부되지 않았습니다」** 라고 사실을 말한다
  (예약 모달과 공유하던 「입력 정보는 저장되지 않습니다」는 이 자리에서 무엇이 사라지는지 가린다).

### F. 말풍선
- 원인: `.scax-agent--ax .scax-agent__bubble small{color:var(--scax-color-ink-disabled)}` —
  `rgba(55,56,60,.16)` 을 **검은 면 위**에 둔 값이라 상태 문구와 점이 바닥에 묻혔다.
- `--scax-color-ink-inverse-assistive` (→ `--ax-ink-inverse-assistive` → DS 원시 램프 `--cool-neutral-70`,
  검정 대비 ≈6.9:1)를 더해 상태 줄과 쉬는 상태 점에 썼다. 나머지 상태 점 넷은 제 색이 있어 그대로.
  캐릭터 교체·가짜 상태 추가 없음.

---

## 죽은 CSS 정리 (저장소 관례대로 「호출부를 옮긴 부품은 자기 옛 CSS 를 데리고 나간다」)
호출부 0곳을 확인하고 뺐다: `.meeting-panel` · `.meeting-tabs`(+`.on`) · `.meeting-head-btn`(+`.icon`).
`.meeting-panel-center` · `.meeting-scroll` · `.meeting-surface` · `.meeting-meta-edit` · `.meeting-line-edit`
· `.meeting-row` · `.meeting-list` 는 아직 쓰는 마크업이 있어 남겼다.

---

## 검증

```
cd frontend && npx tsc --noEmit     → 오류 0
cd frontend && npx vitest run       → 50 files / 532 passed, 0 failed
```
기준선 524 → **532** (+8). 새 잠금 8 · 옮긴 잠금 여럿(수는 통합/분리로 상쇄).

### 새로 건 회귀 테스트
- `MeetingEditModal.test.tsx` (4) — 칸이 값으로 차 있다 · 안 바뀌면 저장 불가 ·
  `updateMeetingInfo` patch 계약 모양 + **[수정]이 선택을 바꾸지 않는다** ·
  고치던 채로 닫으면 묻는다 · `can_edit_info:false` 면 칸을 안 연다
- `MeetingMaterials.test.tsx` (+4) — 고른 파일이 드롭존 «안» 에 선다 · **실제로 빠진 뒤** 토스트(복구 없음,
  서버 호출 없음) · 남아 있을 때만 닫기 확인 · 첨부 칸 구조(카드 없음, [자료 첨부]가 목록 바로 다음 형제,
  빈 상태에서도 구조 유지)
- `MeetingList.test.tsx` (+2) — **box-sizing 전역 리셋이 살아 있다** · **막대는 안 그리되 스크롤은 산다**
  (`*{overflow` 가 없음을 함께 짚어 「숨겨서 해결」 회귀를 막는다)
- `MeetingDetail.test.tsx` — 「상태 여섯 어디서도 머리는 제목으로 시작한다」 ·
  「[회의 시작]·집중 모드가 제목과 같은 줄」 · 「예정은 [수정] 없이 안건 칸이 늘 선다(더하기·빼기 그대로)」 ·
  「예정에도 스크립트 탭이 서고 «아직 없다» 를 낸다」

### 고친(지운 것이 아니라 «옮긴») 기존 테스트
- 4칸 탭이 `button` → `role="tab"` (SegmentedControl). 텍스트 질의는 그대로.
- 상세 연필 잠금 4건 → `MeetingEditModal.test.tsx` 로 **이동**(같은 것을 검사한다). 「없음」 단언으로
  때우지 않았다.
- 공유받은 사람 검사 배열에서 `"회의 정보 수정"` 을 뺐다 — 그 자리가 이 화면에서 사라졌으므로
  여기서 세어 봐야 권한을 말해 주지 않는다(그 잠금은 새 파일이 든다).
- ⚠ `MeetingLive.test.tsx` 의 「ai.batch 가 읽던 자리를 지킨다」는 `.meeting-scroll`(첨부 칸)을 잡고 있었다 —
  **배치가 건드리지도 않는 칸이라 늘 통과하던 빈 검사였다.** 실제 대상인 `.scax-note__body` 로 겨눴다.
  이제 진짜로 `keepScroll`/`useLayoutEffect` 를 지난다.

### 확인한 API 근거 (backend 는 읽기만, 한 줄도 수정 안 함)
| 기능 | 경로 |
|---|---|
| 회의 정보 수정 | `PATCH /api/meetings/{id}` · `can_edit_info` (`lib/api.ts:920`) |
| 안건 추가/삭제 | `POST`/`DELETE /api/meetings/{id}/agendas[/{aid}]` · `can_edit_agendas` |
| 스크립트 | `GET /api/meetings/{id}/transcript` — 상태 무관, 빈 목록 (`application.py:1049`) |
| 자료 목록/첨부/삭제 | `GET`/`POST`/`DELETE .../materials` · `can_detach` |
| 첨부 형식·크기 | PDF · Markdown · 20MB (`materials.py:31`) |

컴포넌트 직접 `fetch` 0. envelope 외 권한 추론 0. 가짜 사람·파일·수치 0.
시안 01 의 하단 상태 데모 컨트롤·예시 데이터는 앱에 넣지 않았다.

---

## 미결 · 주의점 (코디 판단 필요)

1. **[중요] 「완료」 회의의 정보 편집 진입점이 사라진다.**
   시안 02 의 카드는 [수정]·[삭제]를 **「예정」에만** 둔다(「종료」 카드에는 조작 자리가 없다).
   시안을 그대로 따랐으므로, 예전에 연필이 열어 주던 **done 회의의 제목·일시·장소·참석자 편집
   진입점이 없어졌다** — API(`can_edit_info`)와 모달은 살아 있어 카드 조건 한 줄이면 되돌아온다.
   시안대로 둘지, 「예정 + 완료」로 넓힐지는 사용자 결정이 필요하다.

2. **`attachPick` 확정 문구 변경**: 「파일 선택」 → **「파일 추가」**(시안 12),
   `attachDrop` 「여기에 끌어다 놓거나」 → 「첨부할 파일을 끌어다 놓거나 추가하세요」.
   예전 문구는 뒤에 오던 단추에 말을 이어 붙이는 꼴이라 단추가 같은 줄 오른쪽으로 가면 끊긴다.
   기획 확정 문구집에 이 자리가 있으면 확인이 필요하다.

3. **탭 낱말**: `tabMaterials` 「자료」 → **「첨부」**(시안 08). 자료 «목록» 의 접근성 이름은
   「자료」로 남겼다(탭의 낱말과 목록의 이름은 다른 것이다).

4. **새 문구 2건** — `fileRemoved`(「파일이 삭제되었습니다.」, 시안 14 그대로) ·
   `attachDiscardTitle` · `cannotEditInfo` · `focus`/`exitFocus`. 확정 문구집에 자리가 없어 임시다.

5. **테스트 실행 안정성**: 전체 병렬 실행에서 **내가 안 만진 파일**(ActionCenter · MyWorkPage · App)의
   테스트 하나가 간헐적으로 타임아웃 낙오한다(매번 다른 파일, 단독 실행은 4/4 통과).
   기준선 실행에서도 `MyWorkPage.test.tsx` 발 unhandled error 가 1건 있었고, 이 파일들은
   내가 바꾼 부품(FileList·DropZone 은 meetings 전용, Toast 는 `icon` 경로만 추가)을 쓰지 않는다.
   → **기존 부하 민감성으로 본다.** `--no-file-parallelism` 으로는 **532/532 전량 통과**.

6. **시각 검증 — 미실시.** 로컬 프리뷰(vite 5176 + API 8000)를 띄우고 스크린샷을 찍으려 했으나
   **사용자가 「e2e 는 내가 직접 하겠다」고 해서 중단**했다. 띄운 dev server 는 껐고 임시 스크립트는 지웠다.
   따라서 아래는 **브라우저로 확인되지 않았다**: 네 칸의 실제 픽셀 너비·여백, 카드 잘림 해소,
   생성 모달 팝오버 실제 열림, 첨부 모달 drag-over 색, 토스트 위치, 말풍선 대비.
   근거는 CSS·계약·단위 테스트 수준이다. **사용자 확인 요망.**

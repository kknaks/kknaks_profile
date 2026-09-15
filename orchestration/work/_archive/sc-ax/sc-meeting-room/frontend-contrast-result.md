# 가독성 · 업무 요청 폼 · 자료 닫기 위치 — frontend 결과 보고

워크트리 `ax-workspace/sc-meeting-room` · 브랜치 `kknaksss/sc-meeting-room` · HEAD `794ef5e` · 커밋/push/PR 없음.
`backend/` · `docs/` · `.design-sync/` · `frontend/ds-entry.tsx` 및 사용자 기존 수정 무수정.

| | 항목 | 상태 |
|---|---|---|
| 2 | 회의 목록 글자 대비 | **완료** |
| 3-a | '요청할 업무' + 필수 `*` 한 줄 | **완료** |
| 3-b | 참조자·참고 업무·시작 단계 라벨 | **완료** |
| 3-c | 담당 후보 드롭다운 이름 | **완료** |
| 3-d | '참고 업무 연결' 버튼 | **완료** |
| 4 | 자료 미리보기 닫기 위치 | **완료** |

---

## 2. 회의 목록 글자 대비 — `styles/meetings.css`

날짜 · 「제목 없는 회의」 · 참석 인원 · 구획 머리(예정/지난)가 `--scax-color-ink-assistive`
(rgba(55,56,60,**.28**) — 흰 바탕 대비 **1.69:1**)라 묻혀 있었다(현재 화면 26).
넷 다 **`--scax-color-ink`** (DS 기본 본문 잉크)로 올렸다 → 측정값 **17.9:1**.

- **위계는 색이 아니라 크기·굵기가 진다** — 구획 머리 label2/medium, 날짜·메타 caption1,
  제목 body1/semibold 로 그대로다. 「제목 없는 회의」는 실제 제목(semibold)과 **medium 굵기**로 갈린다.
- **상태 배지의 의미색은 그대로** — 측정으로 확인: 실패 배지 `rgb(229,34,34)` / 연한 danger 바탕 유지.
- 선택(`--selected`)·hover 바탕 규칙은 손대지 않았다.

## 3. 업무 요청 폼

### a) 필수 `*` 가 다음 줄로 내려가던 것 — `WorkModals.tsx` · `styles/components.css`
**원인**: `.scax-field__label{display:flex}` 은 **블록**이라 라벨이 한 줄을 통째로 먹고, 형제인 `*` 가
다음 줄로 밀렸다(현재 화면 27). 감싸는 줄에 `.scax-field__label-row{display:flex;align-items:center;gap:4px}`
를 세워 둘이 나란히 선다. 측정: **라벨과 별표가 세로로 겹침(= 같은 줄) · 별표가 라벨 오른쪽 4px**.

**접근성** — 별표를 라벨 «안» 으로 넣지 않았다. 넣으면 접근 이름이 「요청할 업무 **\***」로 바뀌어
`getByLabelText("요청할 업무")` 가 깨지고 스크린리더가 별표를 읽는다. 대신
- 별표에 `aria-hidden` (눈으로만 읽는 표시)
- 입력칸에 **`aria-required="true"`** — 필수라는 사실을 프로그램으로 싣는다(전에는 시각 표시뿐이었다).

### b) 섹션 라벨 — `styles/screens-a.css`
`.cc-picker legend`(참조자 · 참고 업무 · 시작 단계)가 `ink-alt` 라 **바로 아래 안내 문구와 같은 결**이어서
제목으로 읽히지 않았다. `--scax-color-ink` 로 올렸다 → **17.9:1**.

### c) 담당 후보 드롭다운 이름 — `styles/meetings.css`
`.popover-item{color:ink-alt}` 이라 고를 수 있는 사람 이름이 꺼진 것처럼 보였다(현재 화면 28).
`--scax-color-ink` 로 올렸다 → **17.9:1**. **못 고르는 줄(`:disabled`)은 그대로 1.33:1** 로 회색이다.

### d) '참고 업무 연결' 버튼 — `WorkModals.tsx` · `styles/components.css`
**확인 결과 이 버튼에는 `disabled` 가 없다 — 늘 누를 수 있다.** 회색으로 보인 것은
`variant="text"`(`.scax-button--text-neutral{color:ink-alt}`) 때문이었다(현재 화면 30).
강제로 활성화한 것이 아니라 **이미 활성인 것을 활성으로 보이게** 했다:
- 호출부를 **`variant="outlined" tone="neutral"`** 로 올렸다 → 흰 면 + 1px 테두리 + `ink-neutral` 글자.
  측정: `color rgba(46,47,51,.88)` **9.14:1**, `background rgb(255,255,255)`, 테두리 있음 → 단추로 읽힌다.
- 함께 **`.scax-button--text-neutral` 의 글자색을 `ink-alt` → `--scax-color-ink-neutral`** 로 올렸다
  (테두리 단추와 같은 잉크 → 단추끼리 결이 갈리지 않는다). 「빼기」 같은 폼 안의 활성 조작이 여기 걸린다.

**「실제 disabled 일 때만 회색」을 브라우저로 확인했다** — `.scax-button:disabled`(특이도 0,2,0)가
`--text-neutral`(0,1,0)을 이긴다. 측정: 활성 글자 단추 **9.14:1** vs 진짜 disabled **1.33:1**.

> ⚠ **공용 DS 영향 — 보고 대상**: 이 한 줄은 앱 전역의 글자 단추 **호출부 69곳**에 닿는다
> (취소·닫기·빼기·로그아웃 등). 색만 한 단 진해지고 배치·동작·비활성 규칙은 그대로다.
> 일반 모달/일반 업무 요청의 **문구·제출 payload·담당 후보 목록·권한·시스템(회의) 요청자 기록**은 무수정.

**하지 않은 것**: placeholder(`선택`·`YYYY-MM-DD`)와 진짜 disabled, 안내 문구는 그대로 두었다.
앱 전체 무차별 CSS override 를 쓰지 않았고, 안내 문구 재작성도 하지 않았다.

## 4. 자료 미리보기 닫기 — `ds/Modal.tsx` · `styles/workspace.css`

**원인**: `flex:1 1 auto` 가 제목 `h3`(`.scax-drawer__title`)에 걸려 있었는데 **그 h3 의 부모가 flex 컨테이너가
아니었다.** 머리의 flex 자식은 제목을 감싼 `<div style={{minWidth:0}}>` 이고 그것이 자라지 않아 내용 폭만큼만
서서 `×` 가 파일명 바로 옆에 붙었다(현재 화면 29).

`.scax-drawer__head-lead{flex:1 1 auto;min-width:0}` 를 그 div 에 주고 닫기는 `flex:0 0 auto` 로 고정했다.
측정: **머리 오른쪽 520 · 닫기 오른쪽 500**(= 머리 padding 20px) · **제목 칸 폭 444** → 닫기가 오른쪽 끝이다.
제목의 기존 말줄임(`text-overflow:ellipsis`)은 그대로이고 이제 «남는 폭» 안에서 줄어든다.
닫기의 `aria-label`·`onClose`·Esc·드로어 동작 무수정. PDF 뷰어 내부 툴바·파일 내용·업로드는 손대지 않았다.

---

## 사용한 DS 토큰 / variant

| 쓴 것 | 어디에 |
|---|---|
| `--scax-color-ink` | 목록 날짜·제목없음·메타·구획머리 · 섹션 legend · 팝오버 항목 |
| `--scax-color-ink-neutral` | `.scax-button--text-neutral` 글자 |
| `--scax-color-ink-disabled` (기존) | 진짜 disabled — 건드리지 않았다 |
| `--scax-space-100` | `.scax-field__label-row` 간격 |
| `Button variant="outlined" tone="neutral"` | 참고 업무 연결 |

검정 hex 를 직접 박은 곳 없음. 구 `.btn`/`.field`/`.badge`/`.avatar` 재도입 없음. ds 안 문구 하드코딩 없음.

## 변경 파일

`frontend/src/ds/Modal.tsx` · `frontend/src/features/work/WorkModals.tsx` ·
`frontend/src/styles/meetings.css` · `frontend/src/styles/components.css` ·
`frontend/src/styles/screens-a.css` · `frontend/src/styles/workspace.css` ·
테스트 `frontend/src/ds/Overlays.test.tsx` · `frontend/src/features/work/CreateWork.test.tsx`

## 검증

```
cd frontend && npx tsc --noEmit                      → 오류 0
cd frontend && npx vitest run --no-file-parallelism  → 50 files / 558 passed / 0 failed
```
직전 555 → **558** (+3). 스타일을 그대로 베끼는 검사는 늘리지 않았고, **회귀 위험이 실제로 있는 셋만** 걸었다:
1. 필수 별표가 라벨과 같은 줄 · 접근 이름은 「요청할 업무」 그대로 · `aria-hidden` · `aria-required`
2. [참고 업무 연결]이 `disabled` 아님 + outlined variant + 눌러서 하던 일(연결 취소 전환) 그대로
3. 드로어 닫기가 머리의 마지막 자식이고 제목 칸 밖 · `onClose` 동작

**셋 다 RED 확인** — 바꾸기 전 마크업으로 되돌리니 셋 다 빨개졌고, 되돌린 뒤 초록(파일 복구 완료).

### 병렬 부하 실패 구분
직렬 반복 중 두 번, **내가 한 줄도 만지지 않은** 파일에서 각각 한 건이 낙오했다 —
`features/action/ActionCenter.test.tsx` · `features/work/TaskReferences.test.tsx`.
둘 다 단독 실행은 3/3 전량 통과이고 `git diff` 로 해당 경로 변경 0 을 확인했다.
직전 세 태스크에서도 같은 파일군이 매번 다른 테스트로 낙오한 기존 부하 민감성이다.
**깨끗한 직렬 실행 기준 558/558.**

## 시각 검증 — 정적 harness (실제 앱 아님)

**스크린샷**: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-ax-workspace-sc-meeting-room/d8eabb9c-1303-46da-a32a-eb9cf9d2e588/scratchpad/harness.png`
(스크래치패드 — 리포에 파일을 남기지 않았다. `git status` 로 새 파일 없음 확인.)

**한계 — 반드시 감안할 것**: 이것은 **실제 앱이 아니라 정적 harness** 다.
`styles/index.css` 의 `@import` 사슬을 그대로 펴서 **앱과 같은 CSS·같은 순서**로 싣고, 문제 구간의
마크업만 손으로 재현해 headless Chromium 에서 계산값을 읽었다. 확인된 것은 **색·대비·기하**뿐이다.
확인되지 **않은** 것: 실제 라우팅·데이터가 붙은 화면, 실제 드로어가 열릴 때의 폭과 긴 파일명의 말줄임,
상호작용(hover/focus) 상태, 실제 회의 목록의 다양한 상태 조합.
**실제 회의·업무·업로드를 생성하거나 변경하는 검증은 하지 않았고 dev server 도 띄우지 않았다.**

측정 결과(흰 바탕 대비):

| 대상 | 색 | 대비 |
|---|---|---|
| 날짜 · 제목없음 · 메타 · 구획머리 · legend · 팝오버 항목 | `rgb(23,23,25)` | **17.9:1** |
| 실패 배지 (의미색 유지) | `rgb(229,34,34)` | 4.58:1 |
| 참고 업무 연결 · 활성 글자 단추 | `rgba(46,47,51,.88)` | **9.14:1** |
| **진짜 disabled** (단추·팝오버 줄) | `rgba(55,56,60,.16)` | **1.33:1** (의도대로 회색) |

기하: 라벨·별표 세로 겹침(= 같은 줄), 별표가 라벨 오른쪽 4px · 드로어 머리 오른쪽 520 / 닫기 오른쪽 500.

## 미결 · 관찰

1. **드로어 닫기 `×` 글리프 자체가 매우 흐리다** — `rgba(55,56,60,.28)`, 대비 **1.69:1**.
   이번 브리프의 4번은 «위치» 만이라 **색은 건드리지 않았다.** 별도 판단이 필요하면 발주 바란다.
2. `.scax-button--text-neutral` 변경이 **앱 전역 글자 단추 69곳**에 닿는다(위 3-d). 의도한 범위이나
   일반 화면에서 위계가 한 단 평평해 보일 수 있어 눈으로 한 번 봐 주면 좋겠다.
3. 앞선 미결은 그대로다 — 완료 회의 정보 편집 진입점(사용자 결정 대기) · 진행 중 첨부 SPEC/시안 어긋남 ·
   `can_attach` envelope 미노출 · `ds/GutterList` 호출부 0곳.

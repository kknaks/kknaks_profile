# WORK-010 2루프 E2E 결과 보고 (frontend)

2루프 항목을 이 파일에 이어 적는다.

---

## E2E-1 · 업무 상세 「메타 정보」를 한 줄에 두 항목(2열)으로

### 상태: done
- 기준: HEAD `58e591a`.
- 커밋·push 하지 않았다. 서버·프론트를 띄우지 않았다(코디의 5176 스택은 HMR 로 반영된다).

### 변경 파일
| 파일 | 무엇 |
|---|---|
| `frontend/src/features/work/WorkModals.tsx` | 칸 10개를 `dl.meta-info__item` 상수로 꺼냈다(값이 없는 읽기 전용 칸은 `null`). `metaLine(key, left, right)` 가 짝으로 줄을 세운다. 내용·조건·핸들러는 한 글자도 안 바꾸고 자리만 옮겼다. |
| `frontend/src/styles/task-detail.css` | `.scax-td .meta-info` 스코프 4열 격자 · 말줄임 · 날짜 칸 폭 · 좁은 폭 규칙 |
| `frontend/src/features/work/TaskDetailDates.test.tsx` | 줄 단위 `lines()` 손잡이 · 짝/빈 칸 시험 6건(2건 고침 + 4건 신규) |
| `frontend/src/features/work/TaskDetailRelations.test.tsx` | 스코프 클래스 목록에 `meta-info__line`·`meta-info__item` 을 더했다 |

### 짝 · 빈 칸 규칙
| 줄 | 왼쪽 | 오른쪽 |
|---|---|---|
| 1 | 진행 상태 | 버전 |
| 2 | 담당 | 출처 (없으면 빈 칸) |
| 3 | 시작 예정일 | 실제 시작일 (없으면 빈 칸) |
| 4 | 마감일 | 실제 종료일 (없으면 빈 칸) |
| 5 | 결재 · 참조 — 둘 다 있으면 짝, 하나면 왼쪽 | |

- **칸이 서는 조건은 SPEC §2.10.2 그대로다.** 값이 없는 읽기 전용 칸(실제 날짜·결재·참조·출처, 읽기 전용의 예정 날짜)은 `null` 이다. 고칠 수 있는 화면의 시작 예정일·마감일은 비어 있어도 선다.
- **짝의 한쪽만 비면** 그 칸 자리에 `div.meta-info__item--empty[aria-hidden]` 가 들어간다. 열이 맞고, 화면 읽기에는 나오지 않는다.
  - 예: 읽기 전용에서 시작 예정일이 없고 실제 시작일만 있으면 줄 3이 `[빈 칸 | 실제 시작일]` 이다.
- **두 칸 모두 비면 줄이 서지 않는다** — `metaLine` 이 `null` 을 돌려준다.
- 값·저장·셀렉트·「마감일 초과」 배지·출처 「판단 보기」는 그대로다(관련 시험 전부 통과).

### 레이아웃 · 반응형
- 격자
  - `.meta-info__line` 은 2열(`minmax(0,1fr)` × 2)이다.
  - `.meta-info__item` 은 라벨 76px | 값 `minmax(0,1fr)` 이다(가장 긴 라벨 「시작 예정일」·「실제 종료일」이 한 줄에 든다).
  - 칸 사이와 줄 사이에 `line-weak` 구분선을 둔다. 겉 상자(선 · 모서리 12)는 공용 `.meta-grid` 와 같은 모양이다.
- 공용 `.meta-grid`(`components.css:527-534`)는 **건드리지 않았다.** 업무 상세는 이제 그 클래스를 쓰지 않는다.
  - 다른 사용처 3: `RelationGraphPage.tsx:337` · `WorkModals.tsx` 응답 대기 제안의 `meta-grid columns` · 요청 상세의 `meta-grid columns`
- **넘침**
  - 날짜 칸: `.date-field { width:100%; max-width:180px }` — 칸 안에 들고 칸이 좁으면 칸을 따른다(예전 자리에서는 dd 폭만큼 ~360px 로 늘었다).
  - 셀렉트 트리거·출처 링크·배지: `max-width:100%` + 말줄임.
  - `dd` 는 `min-width:0; overflow:hidden` 이다.
- **좁은 폭 기준 = `@media (max-width: 900px)`.** 기존 반응형 경계(`components.css:711` · 로그인 `screens-a.css`)와 같은 값이다.
  - 업무 상세 모달(880 + 겹 바깥 여백 24×2)이 화면보다 좁아지기 시작하는 자리다.
  - 그 아래에서는 한 줄에 한 칸이다(칸 사이 구분선은 위쪽 선으로 바뀌고, 빈 칸은 숨긴다).
  - 뷰포트 기준이다 — 모달 폭에 반응하는 컨테이너 쿼리는 이 저장소에 선례가 없어 쓰지 않았다.

### 기준선 vs 결과
- 기준선: 5 failed(`CreateWork` 4 · `CreateWorkLayout` 1)
- `npx vitest run --no-file-parallelism`: **Test Files 2 failed | 83 passed (85) · Tests 5 failed | 1309 passed (1314)** — 같은 5건이다. **새 실패 0.**
- `npx tsc --noEmit`: 0 · `make frontend-build`: 성공

### 남은 것
- 실제 폭에서의 모양(76px 라벨 · 날짜 180 · 셀렉트 말줄임 · 900px 아래 접힘)은 E2E 화면에서 확인해야 한다(jsdom 은 CSS 를 적용하지 않는다).

---

## E2E-2 · 메타 정보 날짜칸 두 개의 폭이 다르다

### 상태: done
- 미커밋 E2E-1 위에서 고쳤다. 커밋하지 않았고 서버를 띄우지 않았다.

### 원인 (코디 진단 확인)
- **감싸개가 달랐다 — 맞다.**
  - 마감일: `dd > span.meta-info__value`(flex 행, 배지 자리) 안의 `DateField`. 감싸개가 `dd`(flex 열, `align-items:flex-start`) 안에서 **내용 폭**으로 줄어, 그 안의 `width:100%` 가 내용 폭이 됐다(≈240).
  - 시작 예정일: `DateField` 가 `dd` 직속이라 **값 열 폭**으로 늘었다(≈360).
- **`.scax-td .meta-info .date-field { width:100%; max-width:180px }` 가 듣지 않았다.**
  - DateField 의 루트 클래스는 실제로 `div.date-field` 가 맞다(`ds/DateField.tsx` return, 안쪽 `.popover-root` > `button.select-trigger`).
  - 선택자와 명시도(0,3,0)만으로는 걸려야 하는 규칙이다. 화면에서 360 이 나왔다면 다음 둘 중 하나인데, jsdom 으로는 가를 수 없다.
    - 그 규칙이 실제 렌더에 닿지 않았다
    - 측정이 E2E-1 HMR 반영 전이었다
  - 그래서 그 규칙에 기대지 않고 **감싸개 하나가 폭을 정하도록** 바꿨다.

### 고친 것
- `WorkModals.tsx`
  - `dateCell(field, label, value, after?)` 로 두 날짜칸을 **같은 구조**로 그린다: `dd > span.meta-info__value > span.meta-info__date > div.date-field`(편집) / 날짜 글자(읽기 전용)
  - 「마감일 초과」 배지는 `after` 로 `.meta-info__date` **다음 형제**다(날짜칸 오른쪽 옆).
  - 실패·저장 중 문장(`FieldMessage`)은 감싸개 아래로 같은 자리다.
- `task-detail.css`
  - `.meta-info__value { display:flex; flex-wrap:wrap; align-items:center; gap:4px 8px; max-width:100% }` — 배지는 옆에 서고, 칸이 좁으면 아래 줄로 내려간다.
  - **`.meta-info__date { flex:0 1 140px; width:140px; min-width:0 }`** — 폭을 정하는 규칙은 이것 하나다. 칸이 좁으면 `flex-shrink` 로 칸을 따른다.
  - 안쪽 `.date-field` · `.date-field > .popover-root` · `.select-trigger` 는 `width:100%; max-width:none` 으로 그 폭을 채운다. 트리거 높이 30 · 13px 는 그대로다.
  - 옛 `.scax-td .meta-info .date-field { width:100%; max-width:180px }` 는 지웠다.

### 폭 값 — 140px
- 트리거 = 테두리 2 + 안여백 22(왼 12 · 오 10, `components.css:590`) + 「2026/10/13」(13px 숫자 10자 ≈ 75) + 간격 8 + 달력 아이콘 16 ≈ **123px**
- 여유 17px 를 더해 **140px** 이다.
- 빈 값일 때의 「YYYY/MM/DD」도 같은 글자 수라 들어간다.

### 검증
- 새 시험 2(`TaskDetailDates`)
  - 두 편집 날짜칸의 감싸개 체인이 같다(`meta-info__date` → `meta-info__value` → `DD`). 「마감일 초과」는 `.meta-info__date` 다음 형제다.
  - 읽기 전용 날짜 글자도 같은 감싸개 안이다.
- `npx vitest run --no-file-parallelism src/features/work`: **5 failed | 413 passed** — 실패 5 = 기준선 5(`CreateWork` 4 · `CreateWorkLayout` 1)이다. 새 실패 0.
- `npx tsc --noEmit`: 0
- 실제 폭(140 · 배지 줄바꿈)은 5176 화면에서 확인해야 한다(jsdom 은 CSS 를 적용하지 않는다).

### 변경 파일
`frontend/src/features/work/WorkModals.tsx` · `frontend/src/styles/task-detail.css` · `frontend/src/features/work/TaskDetailDates.test.tsx`

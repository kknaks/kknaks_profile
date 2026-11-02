# 리뷰 리포트 — strong-hajin-polish2 / frontend · WORK-009 Phase 2b (2026-10-02)

## 판정: WARN

WP 2b-1·2b-2 의 체크박스는 전부 코드로 섰고, 계약과 다르게 도는 자리(FAIL)는 없다. 시간대 처리가 맞다 — 날짜 문자열은 `Date` 를 거치지 않고, 시각만 `Intl`(Asia/Seoul)로 옮긴다. 브라우저 TZ 를 `America/Los_Angeles` 로 바꿔도 새 테스트가 통과한다. 워커가 보고한 숫자(`taskDateLabel` 36곳 · `formatDate(` 73곳)는 직접 다시 세어도 같다. 남은 것은 경미 5건이다. 그중 실물에서 눈에 띌 것은 둘이다 — 출처 줄의 글자 크기는 사실상 맞춰지지 않았고, 시각을 UTC 로 자르는 자리가 둘 남았다.

## 검수 범위

- 대상: `frontend/` 미커밋 변경만 — 수정 24파일 + 새 파일 2(`src/features/work/TaskDetailDates.test.tsx` · `src/lib/taskDates.test.ts`). +146 / −102. `backend/` 는 보지 않았다
- allowed_paths(발주서 §3 `frontend/src/`): 이탈 0
- 기준: WP `work-009-polish2.md` Phase 2b · P-4 · P-5 · SPEC-007 §2.2 · SPEC-001 U-17 · 발주서 · `fe-survey-report.md` §4·§5
- 실행한 검사
  - diff 전문 읽기
  - grep(`frontend/src`, 테스트 제외)
    - `기한` · `희망` · `} 마감` · `마감"`
    - `slice(0, 10)` · `split("T")` · `toLocaleDateString` · `toISOString` · `replaceAll("-"` · `toLocaleString`
    - `displaySeparator` · `type="date"` · `"date"`
    - `getMonth() + 1` · `월 ${` (포맷터 사본)
    - `taskDateLabel.*` · `formatDate(` 개수
    - `.origin-chip` · 글자 크기 토큰 실값
  - 테스트(직렬 `--no-file-parallelism`)
    - 새 테스트 3파일(`TZ=America/Los_Angeles`) → **20/20 통과**
    - 바뀐 테스트 14파일 → **469 통과 / 6 실패**. 5건은 기준선(CreateWork 시작일 4 · CreateWorkLayout 1)이다. 나머지 1건은 아래 「참고」
- tsc·build 는 다시 돌리지 않았다(워커가 보고했고, 검수는 동작 검증을 다시 하지 않는다)

## 위반 (FAIL 사유)

- 없음

## 경미 (WARN)

- **W1 `frontend/src/styles/task-detail.css:109`** — 출처 줄 글자 계층 맞춤이 **효과가 없다**. 새 규칙은 `p.origin-chip` 에 `font-size: 12px` 를 준다. 그런데 그 안의 자식은 전부 자기 클래스가 크기를 정한다.
  - 배지 `.scax-badge` — caption1 = 12px
  - 링크 `.scax-button--inline` — label2 = **13px** (`components.css:408`)
  - 링크가 없는 화면의 `small.t-meta` — **13px** (`components.css:460`)
  - p 자체에는 직접 글자 노드가 없다

  그래서 사실 줄(12px)과 출처 링크(13px)의 차이가 그대로 남는다. 간격(`--scax-space-200` = 8px)은 토큰이고 제대로 들어갔다. 다만 `12px` 은 토큰(`--scax-text-caption1-size`)이 아닌 리터럴이다. 바로 위 `.meta__facts` 가 쓰던 리터럴 패턴을 따른 것이긴 하다.
  - 근거: WP 2b-1 「글자 크기 12 / 12.5 차이도 같은 줄 계층으로 맞춘다」 · P-5. jsdom 테스트(`TaskDetailDates.test.tsx` 「출처 줄」)는 구조만 세고 CSS 는 보지 않는다 — 조용히 통과하는 자리다
  - 권장: `.scax-td .meta__facts + .origin-chip :is(.scax-button--inline, .t-meta)` 에 caption1 토큰을 주거나, 반대로 사실 줄을 label2 로 올린다(코디가 계층을 고른다)
- **W2 `frontend/src/features/action/ActionCenter.tsx:583` · `frontend/src/features/project/ProjectManageModal.tsx:78`** — 시각을 **UTC 날짜로 자르는 자리 둘이 남았다**.
  - `formatDate(detail.rounds[0].submitted_at.slice(0, 10))`(판단 상세 「첫 제출」) · `formatDate(row.valid_until.slice(0, 10))`
  - 이번 판에서 `formatDate` 가 시각을 서울 날짜로 옮기게 됐으므로(`labels.ts:189-193`), 이제는 `.slice(0, 10)` 이 오히려 그 처리를 막는다. 서울 00:00~09:00 에 낸 제출은 하루 앞 날짜로 보인다
  - 조사(`fe-survey §5` 「UTC 로 자르는 자리 3곳」) 중 「처리일」(`WorkTables.tsx`)은 포맷터 변경으로 같이 고쳐졌고, 이 둘만 남았다. 업무 날짜가 아니라 계약 밖이고 워커가 ⑧로 유지했다고 밝혔다. 다만 그 이유(업무 날짜 아님)는 「하루 밀림」을 정당화하지 못한다
  - 근거: WP 2b-1 「UTC 로 잘라 하루 밀리지 않는다(지금 「처리일」이 UTC 자름)」의 같은 결함 · 코디 판단 목록(⑤⑥)에 ⑧은 없다
  - 권장: 두 자리에서 `.slice(0, 10)` 만 지운다. `valid_until` 이 날짜 전용 값이면 결과가 같다
- **W3 `frontend/src/features/action/CommandConfirmationForm.tsx:97`** — 명령 확인 폼의 `field.type === 'date'` 가 **네이티브 `<input type="date">`** 다. 보이는 형식이 브라우저 로캘을 따른다(한국어 Chrome 은 `2026. 10. 06.`). 서버 편집 계약에 날짜 칸이 오는 AX 확인(예: 업무 수정의 `due_date`)에서는 OQ-Q ③(입력칸도 `2026/10/06`)이 닿지 않는다. 워커의 바꾼/유지한 자리 표(①~⑩)에도 이 자리가 없다 — **전수에서 빠진 자리**다
  - 근거: SPEC-001 U-17 「날짜 입력칸」 줄 · P-4
  - 권장: 그 분기를 `DateField`(기본 구분자 `/`)로 바꾸거나, 업무 날짜가 아니라고 판단해 유지 표에 올린다(코디 판단)
- **W4 어순이 섞인다 — `frontend/src/lib/labels.ts:1136-1137` · `frontend/src/features/work/WorkViews.tsx:153-155` · `:252-253`** — 마감일만 있는 업무는 「**마감일** 2026/10/06」(이름 앞), 시작일만 있는 업무는 「2026/10/01 **시작**」(이름 뒤)이다. 프로젝트 레일·캘린더 띠 라벨·내 업무 행에서 같은 목록 안에 두 어순이 나란히 선다. 「… 시작」 유지는 WP 2b-2 마지막에서 두 번째 체크박스와 사용자 결정이라 위반은 아니다. 실물에서 어색할 자리다
  - 근거: WP 2b-2 「「시작」 라벨이 시작 예정일을 뜻하는 자리는 그대로」 · 앞 판 「「… 마감」을 그 값의 이름으로 쓰지 않는다」(U-17)
  - 권장: 코디가 화면에서 보고 정한다. 맞추려면 「시작 2026/10/01」(이름 앞)이다
- **W5 `frontend/src/lib/labels.ts:78`** — `taskDateLabel.start`(「시작일」)를 정의만 하고 **아무 곳에서도 쓰지 않는다**(0곳). 만들기 창은 여전히 하드코딩 `"시작일"` 이다(`WorkModals.tsx:5369`·`:5378`). 같은 파일의 다른 날짜 라벨은 상수로 옮겼다. 죽은 상수가 남았고, 「라벨 상수 하나」 원칙이 이 자리만 비었다
  - 근거: reviewer rules 「한국어 문자열이 `labels.ts` 밖에 흩어지지 않았나」 · 같은 diff 의 패턴
  - 권장: 두 자리를 `taskDateLabel.start` 로 바꾼다

## 참고 (판정 제외)

- **`ActionCenter.test.tsx` 「prefills the revision form, shows the diff before sending…」** — 14파일을 한 번에 직렬로 돌렸을 때 **한 번 실패**했다. 같은 파일만 돌리면 세 번 다 통과했고, 5파일 묶음으로 다시 돌렸을 때는 재현되지 않았다. 이번 diff 가 바꾼 것은 라벨 문자열(「희망 기한」→「마감일」)과 기대 형식(`2026/09/30`)뿐이라 시점·부하에 따른 흔들림으로 본다. 기준선 5건 밖의 실패가 `make frontend-test` 에서 다시 나오면 그때 본다
- 기준선 실패 5건(날짜 의존 — CreateWork 시작일 4 · CreateWorkLayout 1)은 그대로다. 이번 diff 가 그 테스트들의 라벨 문자열을 바꿨지만, 실패 이유(오늘 날짜 의존)는 변하지 않았다

## 기존 부채 (이번 판정 제외)

- `ActionTaskCard.tsx:373-374` 서버 오류를 칸으로 매기는 정규식이 `/시작|start_date/` 를 먼저 본다. 그래서 「시작일은 마감일보다 …」 같은 서버 문장은 시작일 칸으로 간다. 이번 diff 는 `/마감일|기한|…/` 에 「마감일」만 더했다(워커 ⑨). 서버 라벨(「기한」 10자리)이 Phase 1 에서 「마감일」로 바뀌면 이 정규식 순서를 한 번 봐야 한다
- `shell/fixtures/requestInbox.ts:6` `conditions.note: "기한 협의"` — 테스트 픽스처라 화면에 나가지 않는다

## 확인한 것 (PASS 근거)

**1. 계약 충실도 — WP 체크박스별**

| WP | 코드 | 결과 |
|---|---|---|
| 2b-1 날짜 넷 순서 | `WorkModals.tsx:1982-1985` — 시작 예정일 → 실제 시작일 → 실제 종료일 → 마감일. 앞 「담당」 `:1976`, 뒤 결재·참조는 제자리 | ✔ |
| 2b-1 값 없는 칸 안 섬 | 네 줄 모두 `shown.<값> &&` 로 건다. 테스트 `TaskDetailDates.test.tsx` 시작 전 / 진행 중 / 완료 / 실제만 있는 경우 | ✔ |
| 2b-1 시각 → 서울 날짜 | `labels.ts:189-193` — `^\d{4}-\d{2}-\d{2}[T\s]\d` 에 맞으면 `isoDateInSeoul`(`Intl` `timeZone: "Asia/Seoul"`, `:218-223`), 아니면 문자열 그대로. **날짜 전용 `2026-10-06` 은 `Date` 를 거치지 않아 어느 TZ 에서도 밀리지 않는다**. 경계 테스트 — `taskDates.test.ts` 「UTC 15:00 이후는 다음 날」(`2026-10-05T15:00:00Z`→`10/06` · `14:59:59Z`→`10/05` · `+09:00` 오프셋), `TaskDetailDates.test.tsx` 「15:30Z → 10/06 · 14:59Z → 10/06」. LA TZ 로도 통과(실행 확인) | ✔ |
| 2b-1 편집 라벨 | `WorkModals.tsx:2021`·`:2032` `taskDateLabel.plannedStart`·`.due`. 편집 중에는 예정 둘이 사실 줄에서 빠지고 실제 둘은 남는다(`!metaEditing` 이 예정 둘에만 걸린다). 테스트 「편집」 | ✔ |
| 2b-1 출처 줄 간격 | `task-detail.css:109` — `.scax-td` 스코프로 덮고 전역 `.origin-chip`(`screens-a.css:437`)은 손대지 않았다. 간격 `--scax-space-200`(8px) 토큰. 인접 선택자 `+` 는 DOM 에서 사실 줄 바로 다음 형제여야 닿는다 — 테스트가 그 구조를 센다. 링크 문구 `source.title` 그대로(`:2003`) | ✔ 간격 / **W1** 글자 |
| 2b-2 「마감일」 라벨 전부 | 화면에 나가는 「기한」 하드코딩이 **0곳**이다(주석·테스트 픽스처·오류 매칭 정규식 제외). 칩 `labels.ts:304` `마감일 지남`. 배지 `WorkModals.tsx:1898`·`WorkViews.tsx:160` `마감일 초과`. 빈 값 `labels.ts:1099`·`:1135` `마감일 없음`. 표 머리 `WorkTables.tsx` 5곳. 요청 상세·수정·차이 `WorkModals.tsx:3861`·`:3961`·`:3984`·`:4077`. 판단 수정 `ActionCenter.tsx:54`. 수신함 `InboxRail.tsx:71`. 「희망 기한」·「… 마감」 0곳 | ✔ |
| 2b-2 DateField 입력 `2026/10/06` | `DateField.tsx:24` 기본 구분자 `/`. AX 카드는 `"."` 를 걷었다(`ActionTaskCard.tsx:140`). 회의·프로젝트 `"."` 유지(코디 판단 ⑥) | ✔ (W3 네이티브 입력 1곳 제외) |
| 2b-2 캘린더 거절 문구 날짜 | `labels.ts:1273` `calendarDeny.outOfRange` 가 `formatDate` → `2026/09/02~2026/09/04`. 테스트 `taskDates.test.ts` | ✔ |
| 2b-2 유지 — 만들기 창·캘린더 「시작일」 · 날 머리 | `WorkModals.tsx:5369`·`:5378` 「시작일」 · `labels.ts:1234` `createStartsOn` · `CalendarRail.tsx:61` 「10월 6일 월요일」 | ✔ |
| 2b-2 포맷터 하나 | `formatDate`(`labels.ts:189`) 하나 + 시각 전용 `formatDateTime`. 사본 grep(`getMonth()+1` · `월 ${`)은 회의 시각·캘린더 날 머리·주차뿐이다(업무 날짜 아님). AX 카드의 `.replaceAll("/", ".")` 사본을 걷었다(`ActionTaskCard.tsx:32`) | ✔ |
| 2b-2 업무 날짜 아닌 표시 불변 | 회의 시각(`meetingClock`·`meetingRange`)·시간 배정 칩(`scheduleChip`)·축 눈금은 바뀌지 않았다 | ✔ |
| 2b-2 테스트 문자열 함께 고침 | 바뀐 테스트 16파일 모두 라벨·형식 기대를 새 값으로 바꿨다. 기대를 지우거나 비운 단언은 없다 | ✔ |

**2. 전수 재계수** — `taskDateLabel.*` **36**(due 24 · plannedStart 4 · actualStart 1 · actualEnd 1 · overdue 2 · undated 2 · startAfterDue 2 · **start 0**) · `formatDate(` **73**(정의 제외, `grep -o`) — 워커 보고와 같다. 빠진 자리는 W2(UTC 자름 2) · W3(네이티브 날짜 입력 1)이다.

**3. 시간대** — 위 표 2b-1. `Intl` 방식이라 고정 오프셋 가정이 없다. 경계 테스트가 실제 경계(UTC 14:59:59 / 15:00)를 양쪽에서 짚는다.

**4. 조용히 통과하는 자리**
- 「시작」이 다른 뜻이 된 곳 — `HISTORY_FIELD_LABEL.start_date` 가 「시작 예정일」이 됐다(`WorkModals.tsx:166`, 상세 안의 이력이라 SPEC-007 이름이 맞다). 상세 검사 문장은 「시작 예정일은 마감일보다 늦을 수 없습니다」(`:1079`)다. 만들기 창·캘린더는 `startAfterDue` 「시작일은 …」으로 통일했다. 뜻이 바뀐 자리는 없다
- 빈 단언·오늘 의존 — 새 테스트는 고정 시각만 쓴다(`seoulToday` 의존 없음). 출처 줄 테스트가 CSS 를 보지 않는다는 점은 W1 에 적었다
- `MeetingDetailPage.tsx:1189`·`:1196` 회의 할 일의 `due_candidate` 를 `formatDate` 로 감쌌다. ISO 가 아닌 글자가 오면 그대로 낸다(`taskDates.test.ts` 「날짜가 아닌 글자는 그대로」)

**5. P-5** — 새 CSS 는 한 규칙이고 `.scax-td` 스코프다. 전역 `.origin-chip` 을 쓰는 다른 화면(없음 — `fe-survey §4-3` 「TaskDetailDrawer 한 곳」)으로 번지지 않는다. 임의 hex 0. `12px` 리터럴 1(W1).

## 사용자가 실물에서 만날 자리 (코디 화면 확인 목록)

1. **상세 사실 줄 길이** — 완료 업무는 「담당 · 시작 예정일 · 실제 시작일 · 실제 종료일 · 마감일 · 결재 · 참조」 일곱 칸이다. `.meta__facts` 가 `flex-wrap`(gap 6px 14px)이라 좁은 겹(드로어)에서 두세 줄로 접힌다. 날짜 칸 중간에서 끊기는지 본다
2. **출처 줄 글자 크기** — 사실 줄 12px 아래 링크 13px(W1). 간격 8px 이 들어간 뒤 크기 차이가 더 눈에 띌 수 있다
3. **표 머리 「마감일」** — 내 업무·AX 제안·보낸 업무·참조·조직 표의 셋째 칸이 두 글자에서 세 글자가 됐다. 칸 폭이 좁으면 머리가 접히는지 본다
4. **칩 「마감일 지남」·배지 「마감일 초과」** — 칩 바와 내 업무 행 오른쪽(`task-row-right`)이 한 글자씩 길어졌다. 칩 바 줄바꿈, 배지와 상태 글자의 겹침을 본다
5. **어순** — 같은 목록에 「마감일 2026/10/06」과 「2026/10/01 시작」이 섞인다(W4). 프로젝트 레일·캘린더 띠 툴팁·내 업무 행
6. **수신함 카드 메타** — 「요청자 · 마감일 2026/10/06」로 두 글자 늘었다. 좁은 레일에서 말줄임이 되는지 본다
7. **AX 카드 날짜 칸** — 1차에서 일부러 `2026.09.30` 이던 것이 `2026/09/30` 으로 바뀌었다(OQ-Q ③). 채팅 서랍 안 카드 모양이 그대로인지 본다
8. **판단 상세 「첫 제출」 날짜** — 서울 오전에 낸 제출이 하루 앞 날짜로 보인다(W2)
9. **명령 확인 폼 날짜 칸** — 브라우저 로캘 형식(`2026. 10. 06.`)으로 보인다(W3)

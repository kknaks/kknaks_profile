# WORK-004 프론트 3페이지 검수 보고

- 검수자: `@kknaks-reviewer` (read-only)
- 대상: 워크트리 `work-001-data-foundation` 의 **`app/front/` 미추적 신규 31파일 + `middleware.ts`**
  (`app/ontology-agent/` 는 WORK-002 진행 중 — 범위 제외, 열지 않았다)
- 기준: `roles/ontology-demo/frontend/rules.md` · SPEC-004 v0.1.0 · SPEC-003 v0.0.5 · SPEC-001
- 코디 재검증치(tsc 0 · build 라우트 5 · matcher 확인)를 전제로 **계약·규칙 준수만** 본다. 빌드는 돌리지 않았다.

## 판정: **PASS** — 위반 0건 · 경고 3건 · 승인 예외 4건 확인

파생 카운트·PII·토큰 스코프·mock 스위치·matcher 는 전항 통과다. 경고 3건은 전부
**실 API 전환(WORK-002·003) 시점에 드러날 계약 정합** 문제이고, 지금 화면 동작을 깨지 않는다.

---

## 1. 역할 규칙 (rules.md)

### globals.css·기존 파일 수정 0 — **diff 로 실증** ✓

`git status --porcelain -- app/front` 결과가 `??` 4건(신규 디렉토리 3 + `middleware.ts`)뿐이고
**`M` 이 한 건도 없다.** `globals.css` 는 추적 파일(`git ls-files` 확인)이며 변경 0 → **AC-3 성립**.
`package.json`·`package-lock.json` 도 무변경이다 — `answer-blocks.tsx:4-5` 가 쓰는
`react-markdown`·`remark-gfm` 은 **포트폴리오 기존 의존**(`package.json:12-13`)이라 추가가 없었다.
새 CSS 프레임워크·상태 라이브러리 0건 → **AC-23 성립**.
`middleware.ts` 는 신규 파일이다(`git log` 이력 없음) — 기존 파일 수정이 아니다.

### 파생 카운트 하드코딩 금지 — **전수 통과** ✓

SPEC-004 §4 「파생 카운트」 표 12항을 전건 대조했다.

| 표기 | 구현 | 근거 |
|---|---|---|
| 헤더 모니터링 탭 알림 배지 | `cards.filter(c => c.node_state === "알림").length` | `shell.tsx:59-61` |
| 기준일 배지 | `cards.as_of` | `shell.tsx:58,185` |
| 그래프 헤더 `노드 x/y · 엣지 x/y` | `visible.*.length` / `graph.*.length` | `monitoring-view.tsx:166-168` |
| 범례 판정별 개수 | `counts[verdict]` | `causal-graph.tsx:378` |
| KPI 카드 값·전일 대비·스파크·상태 | 전부 응답 필드 | `kpi-cards.tsx:74,128,144` |
| 「그 외 KPI」 내역 | `rest` 를 `node_state` 로 reduce | `kpi-cards.tsx:175-183` |
| 계층 탭 테이블 수 | `tablesByLayer[layer].length` | `data-view.tsx:158,189` |
| 표 헤더 `1–N / total` | `rangeLabel(offset, returned, total)` | `table-panel.tsx:69` · `encoding.ts:330` |
| 마스킹 바 컬럼 수·이름 | `masked_fields.length` · `.join` | `table-panel.tsx:87-89` |
| 드릴다운 「5 / N」 | `rows.length` / `drilldown.total` | `answer-blocks.tsx:216-219` |
| 예보 제목·본문·근거 | `item.title`·`message`·`edge.evidence` | `forecast-cards.tsx:40,62,65` |
| 인스펙터 판정·신뢰도·lag·근거 | 전부 `edge.*` | `edge-inspector.tsx:69-105` |

추가로 토글 라벨 `기각 {rejectedCount}` 도 `counts["기각"]` 파생이고(`monitoring-view.tsx:106,185`),
인스펙터 하단 기각 노트도 같은 값을 쓴다(`edge-inspector.tsx:132-135`).
JSX 텍스트에 박힌 카운트 리터럴을 정규식으로 훑어 **0건** 확인 → **AC-8 성립**.

### PII ✓

- 원값 0건. 마스킹 표기는 SPEC-001 §4 그대로만 등장한다(`김○○` · `010-****-1234` · `1990-**-**`).
- 폐기된 `19**-**-**` 표기(§7.2 D-1) **0건** — 정규식 확인.
- 픽스처도 원값을 두지 않고 **마스킹 표기를 생성**한다(`mock/tables.ts:439-447` — 성 1자 + `○○`,
  전화 뒤 4자리 난수, 생년 연도만). 리뷰 본문 픽스처의 직원명도 `○○ 실장님` 으로 이미 가려져 있다
  (`mock/tables.ts:126`).
- 언마스킹 UI·권한 UI **0개** — 검색 결과가 전부 「제공하지 않습니다」류 금지 문구다
  (`table-panel.tsx:89`, `mock/chat.ts:441`) → **AC-19·AC-20 성립**.

### 미니그래프 금지 · 스트리밍 금지 ✓

- `components/ontology/chat/` 안에 `CausalGraph` 참조·`viewBox 0 0 1130` 0건 → **AC-14 후단 성립**.
  `used_edges` 는 칩 + `/ontology/monitoring?edge=` 점프로만 표현된다(`answer-blocks.tsx:151-153`).
- `EventSource`·`WebSocket`·`ReadableStream` **0건**. 타이머는 `setInterval(…, 2000)` 하나뿐이고
  (`chat-view.tsx:70-75`, `client.ts:246`) `pending` 이 풀리면 `clearInterval` 된다(`:69,76`).
  스트리밍 흉내(커서 깜빡임·타이핑)도 두지 않았다.

### 토큰 컨테이너 스코프 ✓

`tokens.ts:20-175` 의 **모든 `--ont-*` 선언이 `[data-surface="ontology"]` 블록 안**이고,
`color-scheme: light` 재선언(`:23`)·`min-width` 컨테이너 스코프(`:160-174`)까지 계약대로다
(루트 `html`/`body` 에 `min-width` 없음 → **AC-4·AC-7 성립**).
컨테이너 밖으로 나가는 규칙은 `body:has([data-surface="ontology"])` 3건뿐이며 전부
**데모 표면이 문서에 있을 때만** 발동한다 — 포트폴리오 페이지의 색·서체는 변하지 않는다.
그중 2건이 승인 예외 ①(TopNav 가림)이고, 나머지 1건은 `body` 배경 지정(`:133-135`)으로 같은 조건부다.

`body > .topnav-wrap` / `body > footer` 자식 결합자가 실제로 먹는지 확인했다 —
루트 레이아웃이 두 컴포넌트를 `<Suspense>` 로만 감싸고(`app/layout.tsx:31-37`) Suspense 는 DOM 요소를
만들지 않으므로 둘 다 `body` 직계다(`components/shell/topnav.tsx:46` 의 `.topnav-wrap`,
`components/shell/footer.tsx:41` 의 `<footer>`). **선택자가 헛돌지 않는다** → **AC-2 성립**.

---

## 2. spec 준수

### SPEC-004 U-1~U-15 · AC 23항

전항 확인했다. 특기할 것만 적는다.

- **AC-10 좌표 자산** — `node-layout.ts:19-45` 의 25행을 SPEC-001 §4 표와 **전건 대조**했고
  `node_id`·x·y 가 **25/25 정확히 일치**한다. 좌표 없는 노드는 `missingCoords()` 로 뽑아
  배너로 드러낸다(`monitoring-view.tsx:105,127-132`) — 조용히 빠지지 않는다.
- **AC-9 그래프 1회 호출** — `useEffect(…, [])` 로 1회(`monitoring-view.tsx:59-73`), 툴바 토글은
  `filterGraph()` 순수 클라이언트 필터(`causal-graph.tsx:32-49`). 헤더·범례 카운트가 필터에 따라 함께 변한다.
- **AC-11 표기** — `node_type` 은 `NODE_TYPE_LABEL` 로만 노출되고(`encoding.ts:16-23`) 영문 enum 직접
  노출 0건, 엣지 판정은 번역 없이 정본 한글값 그대로다(`encoding.ts:46`, `edge-inspector.tsx:70`).
  인스펙터의 `kind` 영문 배지(`:88`)는 SPEC-003 §4 가 「인스펙터 배지가 이 값을 쓴다」고 정한 것이라 정상.
- **AC-12 메시지 5종** — `pending`(부분 텍스트 + `StepList`) · `done` · `failed`+다시 시도 ·
  `AI_TIMEOUT`(문구 분기 `timedOut`) · 컴포저 잠금(`send()` 의 `if (pending) return`, 409 미노출)
  전부 존재(`chat-view.tsx:347,374-433,90`).
- **AC-13·AC-16 답변 블록** — 6블록이 필드 유무로 조건부 렌더되고 빈 상자를 그리지 않는다
  (`answer-blocks.tsx:37,60,64,92,94,98`). 드릴다운은 5행 캡 + `total > 5` 일 때 「5 / N」 표시(`:183,216-219`).
  `used_edges` 빈 배열이면 규정 문구를 낸다(`:136-141`).
- **AC-17·AC-18 데이터 계층** — 픽스처 실측: **브론즈 16**(vegas·리뷰 + nexus 14, 행수가 SPEC-001 §4
  표와 전건 일치: 78,216 / 1,962 / 3 / 157 / 128 / 2,154 / 2,996 / 5,632 / 1,769 / 2,179 / 3,199 /
  323 / 24 / 287 / 858 / 0) · **실버 6** · **골드 5**(`gold_kpi_monthly` 포함).
  `LAYERS` 에 `ontology` 없음(`data-view.tsx:27`) → 데이터 화면에 온톨로지 계층 0.
- **AC-22 역추적** — `source_columns` → `parseTableRef()` → `dataHref()` 로 한 계층 아래로 링크가
  이어지고(`column-detail.tsx:118-125,183-198`), `flows_to[]` 로 위로도 이어진다(`:16-52`).
  매핑 표를 손으로 두지 않았다.
- **U-14 중립 바 카피** — 「실명·전화·생년월일은 이 계층으로 올라오지 않습니다 / 차트번호(chart_no)는
  계층 추적용으로 유지됩니다」(`table-panel.tsx:106-107`). 금지 문구(「환자 식별 정보는…」)를 쓰지 않았고
  `chart_no` 모순도 없다 → **D-2 정정 반영 확인**.
- **U-2 게이트** — 안내·실패 문구가 SPEC-003 U-1 과 **한 글자도 다르지 않다**(`gate-form.tsx:82,108`).
  시도 횟수·잠금·계정 안내 0건, 빈 입력 no-op(`:25`) → **AC-6 성립**.
- **AC-5 폰트** — `next/font/local` 로 로드(`layout.tsx:2,18-24`), 소스 전체에 `@import`·외부 URL
  **0건**(정규식 확인). 포트폴리오 Sans(Inter)는 건드리지 않고 데모 컨테이너에만 `--ont-font-sans` 를 건다.
- **AC-21 실시간 금지** — 「실시간」은 **주석 1곳**(`shell.tsx:161`, 금지를 설명하는 문장)에만 있고
  화면 카피에 0건. 세 화면 모두 기준일 배지를 갖고 타이틀 메타가 「일 1회 배치」다.

### SPEC-003 shape — 픽스처 vs spec JSON 예시 대조

- `/api/graph` — 픽스처가 **노드 25 · 엣지 27**, 판정 분포 **채택 4 · 자동 확정 14 · 선언 3 · 보류 3 ·
  기각 3** 으로 SPEC-001 §4 와 정확히 일치한다. `counts` 는 손으로 적지 않고 엣지 배열에서 파생
  (`mock/graph.ts:150-154`). `edge_id` 는 `<from>__<to>` 로 **픽스처(서버 대역)가 실어 주고**
  화면은 소비만 한다(`:118`). `lag: "2w"` 원형 보존 + `lag_days: 14` 병기(`:105-113`) → **AC-14 성립**.
  외생 3노드는 `from` 으로만 등장한다.
- `/api/forecast` — 2건이 SPEC-003 §4 예시와 **동일 값**이다(취소율→예약 `0d`/0·중간·`r=−0.583`,
  강남언니→신환 `2w`/14·낮음·`r=0.691 · n=30`). `title`·`message` 를 화면이 만들지 않는다 → **AC-15 정합**.
- 답변 객체 — §7.3 소재 그대로다: 패턴 A 전제 교정(`mock/chat.ts:77`), 패턴 B **기각
  `new_patients__sales_total` 을 `excluded_edges` 로 배제**하고 `payment_visits__sales_total` 경유
  (`:236-238,226`), 패턴 D 미관측(`used_edges: []` + `unknowns`, `:352,365`).
  **패턴 C(정량 추정)는 없다** → D-11 반영 확인.

### 라우트·URL 직렬화 ✓

`/ontology/{monitoring,chat,data}` + `/ontology` → 모니터링 redirect(`ontology/page.tsx:5`) →
**AC-1 성립**. 페이지 간 상태는 URL 쿼리뿐이고 전역 스토어가 없다.
`?edge=`·`?tier=&table=`·`&filters=`·`?q=` 네 파라미터가 §4 표대로 쓰인다. 테이블은 이름으로 식별
(`data-view.tsx:84`)하고 인덱스를 쓰지 않는다.

---

## 3. mock/실 API 스위치 · middleware matcher

- **스위치는 `client.ts` 한 곳뿐이다.** `isMockMode = ONTOLOGY_API_BASE.length === 0`(`client.ts:38-44`)
  이고 12개 메서드가 전부 그 분기 하나를 지난다. **`client.ts` 밖에서 `fetch(` 호출 0건**(정규식 확인) —
  화면 코드는 전환에 영향받지 않는다.
- **matcher 는 `/ontology/:path*` 한정**(`middleware.ts:38`). 포트폴리오 라우트(`/chat` 포함)는
  미들웨어를 지나지 않는다. `:path*` 가 0개 세그먼트도 매칭해 `/ontology` 자체도 가드된다.
  게이트는 **redirect 가 아니라 rewrite**(`:31`)라 URL 이 보존되고, 통과 후 `router.refresh()`
  (`gate-form.tsx:30`)만으로 원래 라우트로 복귀한다 — U-2 「원래 가려던 라우트로 복귀」를 리다이렉트
  파라미터 없이 푼 방식이 깔끔하다.

---

## 4. 경고 (WARN) — 위반 아님, 실 API 전환 전 처리 필요

### W1. 계약에 없는 필드 3종을 FE 타입이 신설했다

| 필드 | 위치 | 없으면 생기는 일 |
|---|---|---|
| `LayerTable.source_group` | `types.ts:169-173` | 브론즈 칩 그룹핑 키가 `table.table` 로 폴백(`data-view.tsx:76`)해 **1단 16칩 평면**이 된다 — U-13/AC-17 의 「원천 3칩 → nexus 2단 14칩」 구조가 사라진다 |
| `LayerRowsResponse.columns_note` | `types.ts:193-194` | 빈 컬럼 사유 문구가 기본값으로 대체(`table-panel.tsx:146`) — 승인 예외 ④ 의 표면이라 영향은 작다 |
| `ChatMessage.error_code` | `types.ts:311` | `AI_TIMEOUT` 과 `AI_FAILED` 를 **구분할 수단이 없어진다**(`chat-view.tsx:347`) — AC-12 의 5종 중 4번이 3번과 합쳐진다 |

셋 다 optional 이라 런타임은 무너지지 않고 degrade 한다. 다만 `types.ts:5-6` 이 스스로
*"필드를 늘리거나 이름을 바꾸지 않는다 — 없으면 지어내지 말고 spec 개정으로 올린다"* 라고 적어 둔
규칙을 이 파일이 어긴 모양새다. **코디 판단 필요** — (a) SPEC-003 `/api/layers/{layer}/tables` 에
`source_group`, `message` 에 `error_code` 를 등재하거나, (b) `source_group` 은 테이블명 접두
(`nexus_*`)에서 FE 가 파생하도록 바꾸는 편이 값싸다. `error_code` 는 대안이 없어 **spec 개정이 답**이다.

### W2. 토큰 hex 값이 두 곳에 있다

`encoding.ts:54-62`(`verdictStroke` 5색)와 `causal-graph.tsx:67,179,226-231`(`ARROW_COLORS`,
방향 배지 `#1E1E1E`, 개입 노드 `#F1F2FE`·`#7181F8`·`#4B52A8`, 속성 노드 `#F5F6F8`)이
리터럴 hex 를 쓴다. **현재 값은 `tokens.ts` 와 전건 일치**해 어긋난 곳은 없지만, SPEC-004 가
*"두 곳에 hex 를 두면 반드시 어긋난다"* 고 경고한 그 형태다. SVG `<marker>` 의 `fill` 은 `var()`
적용이 까다로워 정당한 예외로 보지만, `line`/`rect` 의 stroke·fill 은 `var(--ont-ink)` 등으로
환원 가능하다. 값 창작은 아니므로 규칙 위반은 아니다.

### W3. 「최근 7일」이 `window_days` 파생이 아니다

`monitoring-view.tsx:113` 의 타이틀 메타가 `"최근 7일 이상 빈도로 판정 · 일 1회 배치"` 상수다.
응답이 `window_days` 를 싣고(`types.ts:71`, 픽스처 `mock/kpi.ts:415`) 카드도 이미 `grain` 으로
캡션을 만드는데(`grainCaption`) 이 문구만 숫자를 품고 있다. §4 파생 표 전수 항목은 아니라
AC-8 위반은 아니지만, 같은 규율을 적용하는 편이 일관된다.

---

## 5. 승인된 예외 4건 — 확인만 (위반으로 세지 않음)

1. **TopNav CSS 가림** — `tokens.ts:129-135`. 조건부(`body:has(…)`)라 포트폴리오에 영향 0.
   선택자가 실제 DOM 과 맞는 것까지 확인했다(§1 토큰 스코프).
2. **woff2 커밋** — `app/(ontology)/fonts/PretendardVariable.woff2` 2.0MB. `next/font/local` 로만 쓰인다.
3. **`has_prev_period` 후속** — `types.ts:68-74` 에 필드가 없고 `PeriodStepper`(`monitoring-view.tsx:245-267`)가
   `hasNext` 만 받아 **◀ 화살표는 절대 비활성화되지 않는다.** 잔여 리스크를 정확히 적어 둔다:
   데이터 시작(2026-01) 이전으로 ◀ 를 누르면 `mockKpiCards` 가 미지의 기간을 **조용히 최신 기간으로
   되돌리므로**(`mock/kpi.ts:408`) 스테퍼 라벨이 갑자기 8월로 튄다. 실 API 도 같은 폴백이면 같은 증상이
   난다 — 후속 처리 시 이 경로를 함께 닫을 것.
4. **빈 컬럼 사유** — `mock/tables.ts:56-57` 의 `UNKNOWN_COLUMNS_NOTE` 가 「정본에 컬럼 목록이 없어
   비워 두었습니다 — 화면이 지어내지 않습니다」로, 지어내지 않는다는 사실을 화면이 말한다. 규율에 맞다.

---

## 6. 잔여 nit (비차단)

- `encoding.ts:185-189` `LAYER_NOTE_REF` 가 계층별 근거 기록을 상수 맵으로 갖는다. 계층 탭 우측
  라벨(`data-view.tsx:195`)만 이 상수를 쓰고, 표 헤더(`table-panel.tsx:64`)와 컬럼 상세
  (`column-detail.tsx:153`)는 응답 `note_ref` 를 쓴다 — 같은 표기의 출처가 둘이다. 상수 쪽을
  `tables[0].note_ref` 파생으로 바꾸면 U-15 의 「`note_ref` 파생」과 완전히 맞는다.
- `encoding.ts:266` 주석이 *"원값은 툴팁·인용이 갖는다"* 라고 적었는데 금액 툴팁은 구현돼 있지 않다
  (인용 블록에는 원값이 실린다). 주석 문장을 실제에 맞추면 된다.

---

## 7. 결론

세 화면이 **계약을 읽고 만든 코드**다. 특히 좌표 25행 전건 일치, 그래프 픽스처의 판정 분포
4·14·3·3·3, 브론즈 16테이블 행수 전건 일치, 예보 정본 수치 일치는 「시안을 옮긴 것」과
「정본을 옮긴 것」을 가르는 지점인데 전부 후자다. 파생 카운트는 JSX 리터럴 0건으로 실증되고,
PII 는 픽스처 생성 단계에서부터 마스킹 표기만 만든다.

**PASS.** W1(계약에 없는 필드 3종)만 실 API 전환 전에 코디가 spec 개정/대안을 정해 주면 되고,
W2·W3 과 nit 2건은 다음 커밋에 얹어도 무방하다. 재검수는 필요 없다.

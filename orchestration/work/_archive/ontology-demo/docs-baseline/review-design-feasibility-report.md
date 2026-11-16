# 디자인 핸드오프 실현 가능성 검토 — 페이지별 판정

- 검토자: `@kknaks-reviewer` (read-only)
- 일자: 2026-09-02
- 대상: `ontology-demo/reference/ontology_demo/design/` (README + 01~08 + `data/*.json` + `design/*.dc.html`)
- 대조: `20-spec/` SPEC-001·002·003·005(draft, 미커밋본) · `10-decision/` DEC-001~005 ·
  실환경 `app/front/`(Next.js 15 App Router)
- 리포지토리 파일은 한 건도 수정하지 않았다. 원천 데이터(`reference/ontology_demo/` 의
  design 폴더 밖)는 열지 않았다.

---

## 0. 전체 요약 표

| 페이지 | 판정 | 한 줄 근거 |
|---|---|---|
| 모니터링 | **FEASIBLE-WITH-CHANGES** | 레이아웃·상호작용은 전부 구현 가능. 다만 KPI 카드가 요구하는 값(전일 대비·스파크라인 7칸·단위·기간)과 인스펙터가 요구하는 값(kind·설명·원본 테이블 링크)이 `/api/kpi/cards`·`/api/graph` 응답에 **없다**. 노드 좌표의 SoT 도 계약에 없다 |
| 채팅 | **FEASIBLE-WITH-CHANGES** (가장 큰 폭) | 답변 6블록 중 **드릴다운 표·후속 질문 칩** 2개가 SPEC-005 답변 객체에 없다. 디자인에 **pending/로딩/실패/재시도 상태가 아예 없다**(SPEC-003 은 2초 폴링 전제). 우측 근거 그래프의 9노드·7엣지가 `edges.json` 과 불일치해 게이트 5-③(하이라이트 = `used_edges`)을 그대로는 만족할 수 없다 |
| 데이터 | **FEASIBLE-WITH-CHANGES** | 표·마스킹·계층 이동은 API 로 충분. 다만 브론즈 테이블 수(3 vs 16)·전 계층 행수·`noshow_rate` 계산식이 SPEC-001 과 어긋나고, 우측 "이 원본이 가는 곳"(하류 추적)과 컬럼 분포 바에 대응하는 API 가 없다 |
| **전 페이지 공통** | **FEASIBLE-WITH-CHANGES** | **접속 게이트 화면이 디자인 패키지에 전혀 없다**(디자인 8개 문서 grep 결과 0건). 토큰은 기존 `globals.css` 로 환원 불가 — 스코프된 신규 토큰 레이어가 불가피(C-2). 라우트 `/chat` 이 기존 포트폴리오 채팅과 충돌 |

**BLOCKED 은 한 건도 없다.** 모든 불일치가 「spec 개정」·「디자인 조정」·「구현 재량」
중 하나로 귀속되며, 착수를 막는 미지의 항목은 없다.

---

## 1. 모니터링 — FEASIBLE-WITH-CHANGES

### 1.1 데이터 실현성

**나오는 것** — 그래프(노드 25·엣지 27·판정·부호·시차·신뢰도·근거·사유)는
`/api/graph`(SPEC-003 §4 그래프)로 전부 온다. 노드 상태(`node_state` 정상/관찰/알림)와
`observed:false` 도 계약에 있다(SPEC-003 §4 KPI·그래프). 디자인
`03-graph-encoding.md` 의 인코딩 축(색=상태·모양=타입·선=판정·굵기=신뢰도)이 응답 필드와
1:1 대응한다.

**안 나오는 것** (KPI 카드 — `02-components.md` §KPI 메트릭 카드 · `04-screen-monitoring.md` §2):

| 디자인이 요구 | `/api/kpi/cards` 현재 응답 | 귀속 |
|---|---|---|
| 전일 대비 `+0.9%p` / `−7` | 없음 (`latest` 만) | **spec 개정** — `dod`·`dod_pct` 동봉(골드에 `_dod`·`_dod_pct` 가 이미 있다, SPEC-001 §4 골드) |
| 스파크라인 7칸 | 없음 | **spec 개정** 또는 **구현 재량** — `cards` 에 `spark:[7]` 을 싣거나 FE 가 `/api/kpi/series` 를 병행 호출. 후자면 카드 렌더가 2요청에 걸린다 |
| 단위 캡션(`%p`·`M`·`건`) | 없음 | **spec 개정** — `unit`·`format` 필드 |
| 「강남언니 리뷰 수 11 · −7(주간)」 | `cards` 에 grain 개념 없음. `gu_reviews` 는 `grain=weekly` 전용(SPEC-002 §4 `query_kpi` 허용 지표) | **spec 개정** — 카드마다 `grain` 을 실어야 한다. 일별 카드 행에 주별 지표가 하나 섞여 있다 |
| 기간 스테퍼 `< 2026년 8월 >` (§1 타이틀 행) | `cards` 는 `as_of` + `window_days:7` 고정, 기간 파라미터 없음 | **spec 개정**(카드에 기간 파라미터) 또는 **디자인 조정**(스테퍼를 데이터 화면에만 두거나 표시 전용) |
| 「그 외 KPI 12 **정상**」 | 파생 가능하나 **디자인 자체 데이터와 모순** | **디자인 조정** — `nodes.json` 은 kpi 17 중 alert 3 · watch 4 · normal 10 이다. 카드 5장(alert 3 + watch 1 + normal 1)을 빼면 남는 12 중 3건이 관찰이다. `08-rules-and-gates.md` §7(카운트는 데이터에서 파생)을 디자인이 스스로 어겼다. 라벨을 「그 외 KPI 12」로 바꾸고 내역을 파생시켜야 한다 |

**엣지 인스펙터** (`02-components.md` §엣지 인스펙터 · `04` §5):

| 디자인이 요구 | `/api/graph` edges | 귀속 |
|---|---|---|
| kind 배지(`causal`/`derivation`/…) | **없음** — SPEC-002 `trace_ontology` 응답엔 `kind` 가 있는데 SPEC-003 `/api/graph` 예시엔 빠졌다 | **spec 개정**(SPEC-003 §4 그래프에 `kind` 추가) |
| 설명 2줄(사람이 읽는 문장) | **없음** — `evidence`(수식)·`reason`(기각 사유)만 있다. `edges.json` 의 `note` 에 해당하는 필드가 계약에 없다 | **spec 개정** — `note`(설명) 추가. 기록 07 이 SoT |
| 「원본 데이터 보기」→ `/data` 해당 테이블 | 엣지·노드 → 테이블 매핑 필드 없음. SPEC-002 `trace_ontology` 의 노드엔 `source:"gold_kpi_daily.sales_total"` 이 있는데 `/api/graph` 노드엔 없다 | **spec 개정** — `/api/graph` 노드에 `source` 추가 |
| 「이 엣지로 질문하기」→ `/chat` 프리필 | 계약 불필요(FE 쿼리스트링) | **구현 재량** |

**예보 카드** (`04` §4 · `02-components.md` §예보 카드):

- `/api/forecast` 는 `rule`·`edge`·`trigger`·`target`·`horizon`·`risk`·`evidence`·`note`
  를 준다. 디자인이 요구하는 **제목**(「예약 위험」)·**본문 문장**·**근거 한 줄**
  (`r=0.412 n=163 · 신뢰도 높음`)은 조합해야 한다.
  - 제목·본문 → **구현 재량**(FE 조합) 또는 **spec 개정**(`title`·`message` 추가).
    근거 추적 앱이라 카피를 FE 에 흩는 것보다 서버가 주는 편이 낫다.
  - 근거 줄의 `r=…` → `forecast.edge` 에 `evidence` 가 없다. **spec 개정** 또는
    FE 가 `/api/graph` 와 조인(**구현 재량**).
- **수치 불일치**: 디자인 예보는 `취소율 → 예약 수 (−) · lag 1d · 신뢰도 높음 ·
  r=0.412 n=163`, SPEC-003 §4 예보 예시는 `lag "0" · horizon "동시점" · confidence "중간"`.
  강남언니→신환도 디자인 `lag 7d·신뢰도 중간`(04) / `높음`(edges.json) vs SPEC-003
  `lag "2주"·confidence "낮음"`. → **spec 개정 + 디자인 조정 양쪽**: 기록 07 을 SoT 로
  한 값 하나로 통일하고, 화면은 하드코딩하지 않는다.
- **lag 표기 형식이 세 곳에서 다르다**: `edges.json` `"0d"/"1d"/"7d"/"60d"` ·
  SPEC-002 `"0"` · SPEC-003 `"2주"`. → **spec 개정**(표기 형식 단일화. 화면 배지가
  이 문자열을 그대로 쓴다).

**기준일 배지** (`02-components.md` §기준일 배지) — 디자인은 `2026-08-31` 고정,
SPEC-003 `/api/kpi/cards.as_of` 예시는 `2026-08-30`, SPEC-002 검증은 데이터 범위를
`2026-01-07 ~ 2026-08-30` 이라 한다. → **디자인 조정**: 배지는 `as_of` 파생값이다
(디자인 08 §7 「카운트는 데이터에서 파생」의 같은 정신).

### 1.2 동작 실현성

- `07-interactions-state.md` §모니터링 상태의 전이 6종(엣지 클릭·hover·필터·기각 토글·
  미관측 토글·기간)은 전부 **클라이언트 상태**다. SPEC-003 계약과 충돌 없음. **FEASIBLE**.
- 기각 토글: SPEC-003 §4 는 「보류·기각은 `verdicts` 를 명시해야 온다」고 한다. 토글마다
  재요청할 필요는 없다 — 최초 1회 `verdicts=전체 5종` 으로 받아 클라이언트에서 거른다.
  헤더 카운트(`노드 25/25 · 엣지 24/27`)는 응답의 `counts` 로 파생된다. **구현 재량**.
- 디자인이 계약에 없는 즉시성·스트리밍을 전제하는 곳은 **모니터링에는 없다**.
  `08-rules-and-gates.md` §2(실시간 금지)가 SPEC-003 AC-12·DEC-005 D4 와 정확히 일치한다.

### 1.3 스택 실현성

- 그래프는 `viewBox 0 0 1130 560` 고정 좌표 SVG다. `07` §애니메이션도 「d3-force 를
  쓸 경우 좌표로 고정 후 정지」라고 못 박았으므로 **d3-force 는 사실상 불필요**하다
  (`package.json` 에 `d3-force@3` · `@types/d3-force` 존재 — 써도 되고 안 써도 된다).
  정적 SVG 렌더가 더 정확하다. **FEASIBLE**.
- **노드 좌표의 SoT 가 계약에 없다.** `/api/graph` 는 x/y 를 주지 않는다. `nodes.json`
  좌표를 FE 정적 자산으로 들고 가야 하는데, **id 체계가 다르다**:
  `nodes.json` = `reserv`·`cancelRate`·`newPat`·`gangnam`·`naver`·`payVisits` (camelCase),
  SPEC-002/003 예시 = `reservations`·`cancel_rate`·`new_patients`·`gu_reviews`·
  `payment_visits`·`sales`·`foreign_channel` (snake_case).
  → **spec 개정**: `node_id` 25종의 확정 목록을 SPEC-004(또는 SPEC-001)가 SoT 로 고정하고,
  좌표 자산을 그 id 로 재키잉한다. 매핑을 FE 에 손으로 두면 노드 하나가 조용히 사라진다.
- `support.js`(`x-dc` 커스텀 엘리먼트 + `{{ }}` 템플릿 런타임) 의존은 프로토타입 전용이다.
  README 가 이미 「구현에 필요 없다」고 명시했고, `.dc.html` 의 `data-dc-script` 블록을
  복사하지 않는 한 스펙에 스며들 경로가 없다. **위험 낮음** — 다만 SPEC-004 에
  「`.dc.html`·`support.js` 는 참조물이며 산출 코드의 의존이 아니다」를 한 줄 못 박기를 권한다.

---

## 2. 채팅 — FEASIBLE-WITH-CHANGES (변경 폭 최대)

### 2.1 데이터 실현성

`05-screen-chat.md` §답변 구조의 블록 6개를 SPEC-005 §4 답변 객체와 대조:

| # | 블록 | SPEC-005 대응 | 판정 |
|---|---|---|---|
| 1 | 상태 배지(전제 교정 / 답할 수 없음·미관측) | `premise_correction` · `unknowns` | ✅ 나온다 |
| 2 | 본문(수치 `<b>` 강조) | `answer` | ✅ (`react-markdown@10` 가용) |
| 3 | 근거 블록(테이블·컬럼·기간·**행 수**) | `citations[]` — `metric`·`grain`·`period`·`source{tool,table,column}` | ⚠️ **행 수 없음**. `query_kpi` 응답엔 `source.row_count` 가 있는데 `citations` 로 올라오지 않는다 → **spec 개정**(`citations[].row_count`) 또는 **디자인 조정**(행 수 제거) |
| 4 | `used_edges` 칩 | `used_edges[]` (from·to·verdict·sign·lag·confidence·role) | ✅ 칩 표기에 필요한 필드 전부 있음 |
| 5 | **드릴다운 표**(브론즈 마스킹 뷰 최대 5행 + 전체 보기) | **없다** | ❌ **spec 개정 필수**. SPEC-005 S-4 는 「답변에 마스킹된 원본 행이 실린다」고 서술하지만 §4 스키마에 행을 담을 필드가 없다. `drilldown:{table,view,columns,rows,masked_fields,total}` 추가, 또는 FE 가 `citations` 를 근거로 `/api/layers/bronze/…` 를 재호출하는 안(그러면 「무엇을 5행 보여줄지」의 필터를 답변이 알려줘야 한다 — 결국 필드가 필요하다) |
| 6 | **후속 질문 칩 2개** | **없다** | ❌ **spec 개정**(`followups: string[]`) 또는 **디자인 조정**(정적 칩으로 격하). 답변 맥락에서 나온 질문이어야 의미가 있으므로 spec 개정을 권한다 |

**빈 상태 시작 카드 4장** (`05` §빈 상태) — 「알림 상태 KPI에서 파생」은 `/api/kpi/cards`
로 가능하나, 카드의 **질문 문구**와 **메타**(「엣지 4개 · 브론즈 원본까지」)는 예측
불가능한 값이다. → **디자인 조정 또는 구현 재량**: 질문·메타는 정적 카피로 두되 dot·라벨만
알림 KPI 에서 파생. 3·4번 카드(프로모션·미관측)는 애초에 알림 KPI 파생이 아니다.

**답변 패턴 4종(`05` §43 「반드시 구현」)의 근거 데이터 검증** — 여기가 가장 아프다.
디자인 예문이 인용하는 엣지가 `edges.json` 의 정본과 어긋난다:

| 패턴 | 디자인이 인용한 엣지 | `edges.json` 정본 | 문제 |
|---|---|---|---|
| A 전제 교정 | 「노쇼율 → 신규 이탈 수 **채택** 엣지」 | 그런 엣지가 없다. 가장 가까운 것은 `noshows → churn` **보류(pending)·신뢰도 낮음** | **SPEC-005 §4 「`used_edges` ⊆ 확정(채택·산출0·외생)」·「보류는 인과 서술 금지」 위반**. 디자인 예문이 게이트 5-② 를 어긴다 → **디자인 조정 필수** |
| B 원인 추적 | 「**평균 할인율 → 노쇼율**(자동 확정, lag 1d)」 | `discount` 의 나가는 엣지는 `discount→ticket`(derived) · `discount→retention`(pending) 뿐. **해당 엣지 없음** | 없는 엣지를 인과 후보로 제시한다 → **디자인 조정** (또는 기록 07 이 실제로 그 엣지를 갖는지 확인 후 `edges.json` 정정) |
| B | 「요일 → 노쇼율 기각(p=0.51)」 | `dow→noshowRate` rejected `Granger p=0.51` | ✅ 일치. `excluded_edges` 로 정확히 표현된다 |
| C 정량 추정 | 「리뷰 10건↓ → 신환 약 3.4명↓」 → 「매출 −280만 원」 | 엣지 `gangnam→newPat`·`newPat→sales` 는 존재 ✅. 그러나 **계수(β)를 주는 도구·필드가 없다**. `evidence` 는 `r=0.287 n=32주` 문자열뿐 | **SPEC-005 §5 「집계를 에이전트가 하지 않는다」와 정면 충돌**. 에이전트가 곱셈으로 3.4명·280만 원을 만들면 규칙 위반이고, `citations` 의 「DB 재조회 일치」도 성립하지 않는다 → **spec 개정**(엣지에 계수·구간 필드 추가 + 추정치 산출 주체를 도구로 지정) **또는 디자인 조정**(정량 추정 문구 제거) |
| D 답할 수 없음 | 외국인 매출 비중은 답하고 유입 채널은 미관측 | `foreignCh` unobserved · `foreign_sales_share` 지표 존재 ✅ | ✅ `unknowns` + `used_edges: []` + 「엣지를 밟지 않았습니다」 문구까지 SPEC-005 §4(빈 배열, 생략 아님)와 정확히 맞는다 |

### 2.2 동작 실현성 — **가장 큰 구멍**

- **디자인에 진행 상태가 없다.** `Chat.dc.html`·`05`·`07` 전체에 로딩/pending/생각 중/
  실패/재시도/타임아웃에 해당하는 상태가 **한 건도 없다**(grep 0건). `07` §채팅 상태는
  `draft`·`turns`·`focus`·`hoverChip` 뿐이고, 전이는 「질문 매칭 → 답변 턴 추가」다 —
  **즉시 응답 전제**의 목업 상태 모델이다.
  SPEC-003 §4 채팅은 `pending` 동안 **2초 폴링**하며 `content`(부분 텍스트)와 `steps`
  (도구 단계)가 자라고, 180초 타임아웃·`AI_FAILED` 재시도·`CONVERSATION_BUSY` 컴포저
  잠금이 있다(SPEC-003 U-4 · S-6 · Case Matrix · AC-8/AC-10).
  → **디자인 조정 필수** — 다음 5개 상태의 시각 설계가 없다:
  1. assistant `pending` 버블(부분 텍스트 + `steps` 도구 단계 리스트)
  2. `failed` 버블 + 「다시 시도」 버튼
  3. `AI_TIMEOUT`(180초) 표시
  4. `CONVERSATION_BUSY` — 컴포저 잠금 상태
  5. `QUESTION_TOO_LONG`(1,000자) 컴포저 아래 문구
  좋은 소식: 디자인이 **스트리밍을 전제하지 않는다** — 계약(폴딩 + 2초 폴링)이 요구하는
  것보다 약한 전제이므로 계약과 충돌하지는 않는다. 부족할 뿐이다.
- **「새 대화」→ `turns=[]`** 는 새 `conversation` 생성으로 대응된다 ✅.
- **키워드 매칭**(`07` §「질문 매칭 키워드: 노쇼 / 리뷰·신환 / …」)은 목업 장치다.
  실제는 LLM 자유 대화(DEC-003 D3)다 → **디자인 조정**: `07` 채팅 상태 절을 폐기하고
  SPEC-003 의 `conversation`/`message` 모델로 대체한다.
- **접속 게이트**(SPEC-003 U-1: 「내부 공유용 데모입니다…」 입력 1칸)의 화면 설계가
  디자인 패키지에 **없다**(전 문서 grep 0건) → **디자인 조정**(게이트 화면 1개 추가)
  또는 **구현 재량**(토큰 안에서 최소 폼으로 구성). 어느 쪽이든 SPEC-004 가 문구·상태를
  받아야 한다.

### 2.3 스택 실현성

- 레이아웃(스레드 flex:1 + 우측 520 패널)·칩·버블 전부 인라인 style 로 재현 가능 ✅.
- `react-markdown@10` + `remark-gfm` 가용 — 본문 `<b>` 강조에 충분 ✅.
- **라우트 충돌**: `07` §라우팅은 `/chat` 인데 `app/front/app/chat/page.tsx` 가 이미
  포트폴리오 「채용담당자 채팅」이다(`app/front/app/chat/page.tsx:16`). `/monitoring`·
  `/data` 는 비어 있다. → **디자인 조정**(`07` 라우팅 표 갱신) — `/ontology/{monitoring,chat,data}`
  같은 접두 세그먼트를 권한다. DEC-004·SPEC-003 어디에도 경로가 고정돼 있지 않아 자유롭다.
- **루트 레이아웃 충돌**: `app/front/app/layout.tsx` 가 `TopNav`·`PageFooter` 를 전역
  주입한다. 디자인은 자체 h64 헤더 + 푸터 없음이다 → **구현 재량**: 라우트 그룹
  `app/(ontology)/layout.tsx` 로 셸을 분리한다.
- `07` §Responsive 의 **「루트에 `min-width:1280px`」은 그대로 적용하면 안 된다** —
  루트는 포트폴리오와 공유하고 `globals.css` 에 `@media (max-width:720px)` 반응형이
  이미 있다. → **디자인 조정/구현 재량**: 데모 레이아웃 컨테이너에만 스코프한다.

---

## 3. 데이터 — FEASIBLE-WITH-CHANGES

### 3.1 데이터 실현성

**나오는 것** — 표 본체(`columns`·`rows`·`total`·`returned`·`offset`·`masked_fields`)와
헤더 「1–14 / 78,216」은 `GET /api/layers/{layer}/{table}`(SPEC-003 §4 계층 조회)로 정확히
나온다 ✅. 「소리 없는 절단 금지」(SPEC-003 §5)가 디자인의 카운트 표기와 같은 정신이다.
계층 탭·테이블 칩·행 검색·기간은 `filters`·`limit`·`offset` 으로 충당된다 ✅.

**안 나오는 것**:

| 디자인이 요구 | 현재 계약 | 귀속 |
|---|---|---|
| 우측 「이 원본이 **가는 곳**」(`06` §우측 · `tables.json` `flowsTo`) | `lineage` 는 **상류**(`source_columns`)만 준다. 하류 추적 필드·엔드포인트가 없다 | **spec 개정** — `/api/layers/{layer}/tables` 응답에 `flows_to[]`, 또는 `lineage` 에 `downstream[]` |
| 컬럼 상세 **분포 바**(`02` §컬럼 상세 패널) | 값 분포를 주는 API 없음 | **spec 개정**(컬럼 분포 엔드포인트) 또는 **디자인 조정**(분포 바 제거). 데모 범위상 후자를 권한다 |
| 실버 글로서리 **규칙 ID**(G-014·G-021·G-008·G-031·G-040·G-050) | `lineage` 에 `note`·`note_ref` 는 있으나 `rule_id` 없음 | **spec 개정** — `lineage.columns[].rule_id`. 도구 쪽 `get_definition` 은 화면이 부르지 않는다 |
| 골드 **게이트 표기**(「게이트 G3 통과 · 분모 0일은 null 처리 후 ma7에서 제외」) | `lineage` 에 `formula`·`note`·`status_thresholds` 는 있으나 `gate` 필드 없음 | **spec 개정** — `lineage.columns[].gate` |
| **미확정 값 표기**(`06` §미확정 — 60일 미경과 코호트 `—`+「미확정」) | 응답에 확정/미확정 플래그 없음(`null` 만으로는 「관측 없음」과 구분 안 됨) | **spec 개정** — 행/셀 수준 `is_provisional`. SPEC-002 가 「관측 없음과 0 을 구분한다」를 이미 원칙으로 세웠으니 그 연장 |
| 계층 기록 링크(브론즈→02·실버→04·골드→05) | `note_ref` 존재 ✅ | 문제 없음 |

**행수·스키마 불일치 (전수)** — `tables.json` vs SPEC-001 §4:

| 테이블 | 디자인 | SPEC-001 | 귀속 |
|---|---|---|---|
| 브론즈 테이블 수 | **3** | **16** (vegas 1 + 리뷰 1 + nexus 14) | C-1 참조 |
| `silver_reservations` | 78,216 | **75,479** (중복 2,737 제거) | **디자인 조정** |
| `silver_catalog` | 2,481 | **6,198** | **디자인 조정** |
| `silver_promotions` | 42 | **73** | **디자인 조정** |
| `silver_mappings` | 318 | **9,689** | **디자인 조정** |
| `silver_branch_alias` | 26 | **11** | **디자인 조정** |
| `gold_kpi_daily` | 233 | **235** (2026-02-17 결측일 행 없음) | **디자인 조정** |
| `gold_kpi_weekly` | 35 | **34** | **디자인 조정** |
| `gold_promo_calendar` | 233 (일별) | **57** (프로모션 1건 = 1행, 그레인 자체가 다름) | **디자인 조정** — 화면 표의 그레인이 바뀐다 |
| `gold_retention_monthly` | 8 | 미상(SPEC-001 OQ-3) | **spec 개정** — 빌드 실측값 등재 |

**계산식·enum 불일치**:

- `tables.json` `gold.formulas.noshow_rate = "noshows / reservations"` vs
  SPEC-002 §4 `get_definition`·SPEC-003 `lineage` 예시 `"부도 ÷ (내원 + 부도), 취소는
  분모에서 제외"`. **분모가 다르다** → **디자인 조정**(기록 03/05 가 SoT).
- `tables.json` `silver.reservations.glossary.visit_status = "브론즈 6값을 내원·취소·**노쇼**
  3값으로 축약"` vs SPEC-001 §4 enum `내원 · 취소 · **부도**`. → **디자인 조정**(enum 값은
  화면에 그대로 나온다).
- `gold_kpi_daily` 컬럼 목록은 SPEC-002 허용 지표와 거의 일치하나, 디자인엔
  `new_patients_domestic`·`sales_foreign_est`·`visits_foreign_est`·
  `new_patients_foreign_est` 가 없다 → **디자인 조정**(표 컬럼 보강) 또는 **구현 재량**
  (화면 표시 컬럼을 부분집합으로 두되 「N개 컬럼 중 M개 표시」를 밝힌다 — 소리 없는 절단 금지).

### 3.2 동작 실현성

- `07` §데이터 상태(`tier`·`table`·`selectedRow`·`period`)와 전이 3종은 전부 클라이언트
  상태 + 조회 요청이다. 계약과 충돌 없음 ✅.
- 「골드 → 실버 → 브론즈 역추적이 항상 있어야 한다」(`08` §3 · `06` §우측)는 SPEC-001
  AC-9(드릴다운 성립)와 정확히 같은 요구다 ✅ — 다만 §3.1 의 하류/상류 API 보강이 전제다.
- `table: number`(계층 내 인덱스)로 테이블을 지목하는 상태 모델은 목록 순서에 의존한다
  → **구현 재량**: 테이블 **이름**을 키로 쓴다(브론즈 16종으로 늘면 인덱스가 깨진다).

### 3.3 스택 실현성

- 표는 `grid-template-columns` 를 컬럼 정의에서 생성(`02` §데이터 표) — App Router +
  인라인 style 로 무리 없음 ✅. sticky 헤더·overflow 컨테이너 모두 표준 CSS ✅.
- 한국어 값만 Pretendard 로 되돌리는 규칙 → 폰트 도입 문제(C-2)와 묶인다.

---

## 4. 공통 검토 포인트 판정 — C-1 ~ C-4

### C-1 테이블 수 불일치 — **판정: 디자인 조정 + spec 항목 추가**

- 사실관계: `tables.json` = 브론즈 **3** · 실버 6 · 골드 4 (13).
  SPEC-001 §4 = 브론즈 **16**(vegas 1 · 리뷰 1 · nexus 14) · 실버 6 · 골드 4 ·
  온톨로지 2 (총 28).
- 디자인의 「nexus 시술 카탈로그」 칩은 `format:"RDB · 14테이블"`, `rows:2481`,
  `columns:[code,category,name,listPrice,unit,active]` — **어느 브론즈 테이블과도 대응하지
  않는 합성 스키마**다. SPEC-001 의 nexus 14종은 `bronze_nexus_categories`(157) ·
  `bronze_nexus_procedure_products_ko`(2,996) 처럼 원형 그대로이고, 그 중 하나도 2,481행이
  아니다. 즉 화면 단순화가 아니라 **없는 테이블을 그린 것**이다.
- **권고안**: 브론즈를 「원천 3(vegas · 리뷰 · nexus)」의 **원천 축**으로 유지하되,
  nexus 를 고르면 두 번째 칩 행(또는 서브 칩 14개)이 열리는 **2단 선택**으로 간다.
  `02-components.md` 가 이미 「6개 이상이므로 탭이 아니라 칩 행」을 근거로 칩을 골랐으니
  14개도 같은 컴포넌트로 수용된다.
  - 계층 탭 카운트는 「브론즈 **16**」으로 파생시킨다(`08` §7).
  - 온톨로지 계층(`ontology_nodes`·`ontology_edges`)이 디자인에 **없다**. SPEC-003 은
    `{layer}` 에 `ontology` 를 포함한다 → **디자인 조정 또는 명시적 범위 배제**
    (그래프 화면이 이미 온톨로지를 보여주므로 데이터 화면에서 빼는 결정도 합당하다.
    다만 SPEC-004 가 「데이터 화면은 3계층만 다룬다」를 명시해야 한다).
- **정합 방법**: 칩 목록·행수·계층 카운트의 SoT 를 `/api/layers/{layer}/tables` 응답으로
  못 박는다. `tables.json` 은 **레이아웃 참조물**로 격하하고 값은 API 파생.

### C-2 토큰 충돌 — **판정: 기존 토큰으로 환원 불가. 스코프된 신규 토큰 레이어가 불가피**

핸드오프 제약(「`app/front/app/globals.css` 토큰 SSOT, 새 색·폰트 금지」)은 **현행
`globals.css` 를 보면 성립하지 않는다.** 근거:

- `app/front/app/globals.css:7-96` 의 `:root` 는 **dark-first 단일 테마**다
  (`color-scheme: dark`, `--bg-0:#0a0b0d`, `--fg-0:#f4f5f7`).
  `prefers-color-scheme`·`data-theme` 라이트 분기가 **없다**(grep 0건).
- 액센트는 **녹색** `oklch(0.78 0.14 145)`. 디자인 Primary 는 **보라-파랑** `#7181F8`.
- `01-tokens.md` 는 「단일 **라이트** 테마」를 선언한다. 두 시스템은 겹치는 지점이 없다.

**환원 가능 / 불가 목록**:

| 항목 | 기존 토큰 | 판정 |
|---|---|---|
| Mono 폰트 | `--font-mono` = next/font `JetBrains_Mono` | ✅ **환원 가능** (디자인 요구와 동일 서체) |
| 전환 시간 120ms | `--dur-1: 120ms` | ✅ 환원 가능 |
| 간격 4·8·12·16·20·24·32·64 | `--s-1 … --s-16` | ✅ 대부분 환원 가능 (**14px** 패널 gap, **9/10px** 만 신규) |
| 라운드 2·4·6·10 | `--r-1 … --r-4` | ⚠️ 부분 — 디자인의 **8·12·16** 이 없다 |
| **본문 색 전 계열**(Ink `#1E1E1E` · Body `#5F6470` · Label `#757575` · Muted `#9EA2AE` · Placeholder `#B3B3B3`) | dark 계열 `--fg-0..4` | ❌ **불가** — 명도 방향이 반대 |
| **서피스·보더 전 계열**(`#FFFFFF`·`#F9FAFB`·`#F5F6F8`·`#F1F2F5`·`#F8FAFF`·`#EBEBEB`·`#D9D9D9`·`#E5E7EA`) | `--bg-0..4`, `--line-1..3`(반투명 흰색) | ❌ **불가** |
| **Primary 3종**(`#7181F8`·`#5F71F5`·`#4B52A8`) | `--accent`(녹색) | ❌ **불가** — 색상환이 다르다 |
| **상태 4종 × 3값**(알림 `#E2685B`/`#FDEEEC`/`#A6382C`, 관찰 `#E3B93C`/`#FEF3C0`/`#8A6A11`, 정상, 미관측) | `--warn`·`--danger` 단일값(fill/text 파생 없음) | ❌ **불가** |
| **계층 배지 3종 × 4값**(브론즈·실버·골드) | 없음 | ❌ **불가** |
| **보조색**(Info `#33AAFF`, 알림/관찰 보더·연배경, 스파크라인 중간톤 3종) | 없음 | ❌ **불가** |
| **로고 그라디언트** `linear-gradient(135deg,#7181F8,#A6CDFF)` · 아바타 2종 | 없음 | ❌ **불가** — 그라디언트 토큰 자체가 없다 |
| **Sans = Pretendard Variable** (jsDelivr CDN) | `--font-sans` = next/font `Inter` | ❌ **신규 폰트**. 게다가 CDN `@import` 는 next/font 컨벤션과 어긋난다 |
| 섀도 4종(라이트용 `rgba(16,24,40,…)`) | `--shadow-card`/`--shadow-pop`(다크용 검정 40~60%) | ❌ **불가** |
| 타입 스케일(28/16/15/14/13/12/11) | `--t-h2:28` 외 대부분 불일치(`--t-body:15`) | ⚠️ 부분 |

**권고**:
1. `globals.css` 의 `:root` 를 **건드리지 않는다**(포트폴리오 전 페이지가 그 위에 서 있다).
2. 데모 라우트 그룹 레이아웃(`app/(ontology)/layout.tsx`)의 **컨테이너 스코프**에
   신규 토큰 세트를 선언한다 — 예: `[data-surface="ontology"] { --ont-ink: #1E1E1E; … }`.
   접두어(`--ont-`)로 전역 토큰과 이름 충돌을 막는다.
3. `color-scheme: light` 를 그 컨테이너에 재선언한다(전역이 `dark` 라 네이티브 위젯이
   샌다 — `globals.css:11-13` 주석이 지적한 문제의 정확한 역방향).
4. Pretendard 는 **next/font/local 또는 next/font/google 경로**로 도입한다(CDN `@import`
   금지). 도입 자체는 **사용자 승인이 필요한 결정**이다 — 포트폴리오 본문 서체(Inter)와
   다른 서체를 한 배포에 얹는 문제다.
5. **SPEC-004 가 「토큰 SSOT 는 globals.css」 제약을 「globals.css 를 수정하지 않고
   데모 스코프 토큰 레이어를 둔다」로 개정해야 한다.** 지금 문언 그대로는 디자인을
   구현할 수 없다.

### C-3 PII·게이트 — **판정: 어긋나는 곳 3건. spec 개정 1 · 디자인 조정 2**

| # | 대조 | 판정 |
|---|---|---|
| 1 | `08` §1 생년월일 마스킹 **`19**-**-**`** vs SPEC-001 §4 마스킹 표기 **`1990-**-**`**(「연도만 노출」) · SPEC-003 U-2 · SPEC-005 R-3 | ❌ **직접 충돌**. `08` 은 연도까지 가린다. → **디자인 조정**(SPEC-001 이 마스킹 표기의 SoT 라고 SPEC-001 §2 가 명시) |
| 2 | `tables.json` 브론즈 리뷰 `authorName*`(마스킹) vs SPEC-001 §4 마스킹 뷰 표 — `v_bronze_reviews` 가 가리는 것은 「**본문 내 직원 실명**」뿐, `authorName` 은 목록에 없다 | ⚠️ **spec 개정** — 리뷰 작성자명이 마스킹 대상인지 확정해야 한다(SPEC-001 OQ-5 와 인접하나 같은 질문은 아니다). 디자인은 이미 마스킹 전제로 그렸다 |
| 3 | `02` §마스킹 — 실버·골드 중립 바 문구 「**환자 식별 정보는 이 계층까지 올라오지 않습니다**」 vs SPEC-001 §4 「`chart_no` 는 **해시하지 않고 그대로** 반입·노출」, 디자인 자신의 `silver.reservations.columns` 에도 `chart_no` 가 있다 | ❌ **디자인 조정** — 카피가 자기 표와 모순된다. 「실명·전화·생년월일은 이 계층으로 올라오지 않습니다(차트번호는 추적용으로 유지)」류로 정정 |

**어긋나지 않는 것(확인)**:
- 마스킹 3컬럼(`patientName`·`phone`·`birthday`) 대상 = SPEC-001 §4 ✅
- **언마스킹 UI·권한 UI 없음** = DEC-002 · SPEC-001 §5(「원 테이블 직접 조회 경로를
  만들지 않는다」) ✅ — 디자인이 탈락안까지 기록해 둔 점이 계약과 같은 방향이다
- 노출 0건 게이트 = SPEC-001 AC-7 · SPEC-005 G3 ✅ (디자인은 카피·툴팁 예시·채팅
  예문에도 원값 금지를 명시 — SPEC-005 §4 Validation 의 PII 행과 동일)
- 실시간 금지·기준일 배지 = DEC-005 D4 · SPEC-003 AC-12 ✅
- 기각 엣지 보존 = SPEC-001 §4(「기각·보류도 행으로 남는다」) · SPEC-005 S-3 ✅
- 접속 게이트(env 비번 1개)의 **정책**은 충돌 없음. 다만 **화면이 없다**(§2.2).

### C-4 `used_edges` 하이라이트 — **판정: 하이브리드 설계는 옳으나, 우측 패널의 고정 9노드 축약은 게이트 5-③ 을 만족할 수 없다**

`05` §근거 그래프 패널 · `07` §used_edges 하이라이트가 채택한 하이브리드
(① 답변 안 엣지 칩 ② 우측 520px 패널에서 밟은 엣지 점등 ③ 칩 클릭 → 모니터링 점프)의
**구조는 SPEC-003·005 로 구현 가능하다**. 문제는 ② 의 데이터다.

**결함 1 — 축약 그래프의 노드·엣지가 정본과 다르다.**
`Chat.dc.html` 의 `NODES`/`EDGES`(9노드·7엣지)는 `data/edges.json` 의 부분집합이 아니다:

| 축약 그래프 엣지 | `edges.json` 정본 | 문제 |
|---|---|---|
| `noshowRate → churn` **adopted** | **없음**. `noshows → churn` 이 **pending** | 판정까지 뒤집혔다 |
| `cancelRate → churn` **pending** | **없음** | 없는 엣지 |
| `reviews → newPat` adopted | 노드 `reviews` 자체가 없다(정본은 `naver`·`gangnam` 분리) | 노드 합성 |
| `cancels→cancelRate`·`reserv→cancelRate`·`noshows→noshowRate`·`newPat→sales` | 존재 ✅ | 정상 |

→ **디자인 조정 필수**: 축약 그래프의 노드·엣지 집합을 `ontology_nodes`/`ontology_edges`
의 **진짜 부분집합**으로 다시 정의한다.

**결함 2 — 고정 축약으로는 게이트 5-③ 을 통과할 수 없다.**
SPEC-005 G5-③ 은 「**그래프 하이라이트 = `used_edges` (집합이 정확히 같을 것)**」이다.
`used_edges` 는 확정 엣지 21종(채택 4 + 산출0 14 + 외생 3) 중 무엇이든 될 수 있는데,
9노드 축약 그래프는 그 중 일부만 담는다. 답변이 축약 그래프에 없는 엣지를 밟는 순간
하이라이트 집합 ≠ `used_edges` 가 되어 **게이트가 깨진다**.

**해결안 2가지 (하나를 SPEC-004 가 택해야 한다)**:
- **(A) 동적 유도 부분그래프** — 우측 패널을 `used_edges` 의 induced subgraph 로 매 답변
  구성한다. 좌표는 `nodes.json` 의 전역 좌표를 부분집합에 맞춰 재정규화(bounding box
  fit). 고정 9노드 축약은 **빈 상태 전용**으로 격하. → 게이트 5-③ 자동 만족. **권장**.
- **(B) 게이트의 「하이라이트」를 모니터링 그래프로 한정** — 채팅 우측 패널은 요약
  뷰이며 게이트 대상이 아님을 SPEC-005 G5-③ 과 OQ-4 에 명시. 대신 축약 그래프에 담기지
  않은 엣지가 있을 때 「N개 중 M개 표시」를 밝혀야 한다(소리 없는 절단 금지).

**결함 3 — 엣지 식별자.**
`used_edges[]` 는 `(from, to)` 쌍만 갖는다(SPEC-005 §4). `edges.json` 27건에 `(from,to)`
중복은 **없으므로 쌍이 유효한 키다** — 다만 칩 클릭 → `/monitoring` 점프에 URL 로 실어야
하므로 **안정 `edge_id`** 를 두는 편이 낫다. → **spec 개정**(`/api/graph` edges 와
`used_edges` 에 `edge_id` 추가) 또는 **구현 재량**(`?from=…&to=…`).

**페이지 간 상태 공유 요구 (명시)**:
1. `/{monitoring}?edge=<edge_id>` — 채팅 칩 → 모니터링 인스펙터 선택 상태로 진입
   (`07` §교차 이동 3번). 전역 스토어 불필요, **URL 쿼리로 충분**.
2. `/{data}?tier=…&table=…&filters=…` — 채팅 드릴다운 표 → 데이터 페이지(필터 적용),
   모니터링 인스펙터 「원본 데이터 보기」 → 해당 테이블(`07` §교차 이동 1·4번).
   전제: 엣지 → 테이블 매핑(§1.1) · 드릴다운 필터의 직렬화 규약.
3. `/{chat}?q=…` — 인스펙터 「이 엣지로 질문하기」·데이터 「이 값 물어보기」 프리필
   (`07` §교차 이동 2·5번). 기존 포트폴리오 `/chat` 이 이미 `?q=` 를 쓰므로
   (`app/front/app/chat/page.tsx:13`) 같은 패턴을 그대로 따르면 된다.
4. **전역 상태는 필요 없다.** 세 페이지가 공유하는 것은 URL 파라미터와 세션 쿠키뿐이다.
   `used_edges` 를 페이지 간에 들고 다닐 필요는 없다 — 모니터링은 `edge_id` 하나만 받는다.

---

## 5. SPEC-004(화면 spec) 작성 시 들어가야 할 계약 항목

「이 항목이 SPEC-004 에 없으면 구현이 갈라진다」는 것만 추린다.

### 5.1 전 화면 공통

1. **라우트 확정** — `/chat` 충돌 해소. `app/(ontology)/{monitoring,chat,data}` 접두 세그먼트와
   기본 진입(`monitoring`)을 못 박는다.
2. **셸 계약** — 라우트 그룹 레이아웃이 포트폴리오 `TopNav`/`PageFooter` 를 대체한다는 명시.
3. **토큰 레이어 계약** — 「`globals.css` 를 수정하지 않는다 + 데모 스코프 토큰(`--ont-*`)
   + `color-scheme: light` 재선언」. C-2 의 **신규 토큰 전 목록**을 SPEC-004 가 SoT 로 갖는다.
4. **폰트 결정** — Pretendard 도입 여부와 방식(next/font, CDN 금지). 사용자 승인 항목.
5. **최소 폭 처리** — `min-width:1280px` 를 데모 컨테이너에 스코프. 안내 화면 문구.
6. **접속 게이트 화면** — SPEC-003 U-1 문구를 받는 화면 1개(입력·에러·성공 후 복귀).
7. **기준일 배지** = `as_of` 파생. 하드코딩 금지.
8. **파생 카운트 목록** — 하드코딩 금지 대상 전수: 헤더 탭 알림 배지 · 그래프 헤더
   `노드 x/y · 엣지 x/y` · 범례 판정별 개수 · 계층 탭 테이블 수 · 표 헤더 `1–N / total` ·
   「그 외 KPI」 카드. 각각의 **출처 API 필드**를 표로 지정.
9. **node_id 25종 확정 목록**과 좌표 자산(`viewBox 0 0 1130 560`)의 키 규약.
10. **엣지 `edge_id` 규약**과 URL 직렬화(`?edge=`·`?tier=&table=&filters=`).
11. **`.dc.html`/`support.js` 는 참조물이며 산출 코드의 런타임 의존이 아니다**(명시 1줄).

### 5.2 모니터링

12. KPI 카드가 필요로 하는 필드 계약: `dod`·`dod_pct`·`unit`·`grain`·`spark[7]`·정렬 규칙
    (알림→관찰→정상)·「그 외 KPI」 집계 규칙.
13. 그래프 인코딩 계약: 판정 5종 ↔ 선 스타일/화살촉, 신뢰도 ↔ 굵기(2.6/1.6/1),
    노드 타입 6종 ↔ 도형, 상태 4종 ↔ 색. **판정 라벨 표기 통일**(디자인 「선언」/「자동 확정」
    vs API `외생`/`산출0` — 어느 쪽을 화면 카피로 쓸지 확정).
14. 기각 토글의 데이터 획득 방식(1회 전체 fetch + 클라이언트 필터)과 카운트 연동.
15. 인스펙터 필드 계약: `kind`·설명(`note`)·`evidence`·액션 2종의 목적지.
16. 예보 카드 계약: 제목·본문·근거 줄의 생성 주체(서버 vs FE), `lag` 표기 형식,
    `risk` ↔ 카드 색(알림/관찰) 매핑.

### 5.3 채팅

17. **메시지 상태 5종의 화면 설계**: `pending`(부분 텍스트 + `steps`) · `done` ·
    `failed`+재시도 · `AI_TIMEOUT` · `CONVERSATION_BUSY`(컴포저 잠금). 2초 폴링 명시.
18. **답변 6블록 ↔ 답변 객체 필드 매핑표**(SPEC-005 §4 기준). 드릴다운·후속 질문의
    출처 필드를 확정(= SPEC-005 개정 요구).
19. **우측 근거 그래프 계약**: 동적 유도 부분그래프(A안) 채택 여부, 좌표 산출 규칙,
    빈 상태, 「N개 중 M개 표시」 문구, 게이트 5-③ 의 검증 대상 화면 지정(SPEC-005 OQ-4 를 닫는다).
20. 답변 패턴 4종의 **예문 정정** — A(보류 엣지를 채택으로 인용) · B(없는 엣지) ·
    C(계수 기반 추정)의 처리. C 는 「추정치를 낼 도구가 없으면 문구를 뺀다」가 기본값.
21. 컴포저 검증(1,000자)·전송 잠금·`?q=` 프리필.
22. 빈 상태 시작 카드 4장의 파생 규칙(무엇이 데이터 파생이고 무엇이 정적 카피인지).

### 5.4 데이터

23. 브론즈 16테이블의 표시 구조(원천 3 → nexus 2단 칩) + 계층 탭 카운트 파생.
24. 온톨로지 계층을 데이터 화면에서 다루는지 여부(다루지 않으면 명시적 배제).
25. `lineage` 가 화면에 주어야 할 필드: `rule_id`(G-0xx) · `gate` · `downstream/flows_to` ·
    `is_provisional`(미확정) — SPEC-003 개정 요구를 SPEC-004 가 촉발한다.
26. 표 컬럼의 부분 표시 규약(전 컬럼을 안 보여줄 때 그 사실을 표기).
27. 마스킹 바 문구 2종의 **최종 카피**(SPEC-003 U-2 문구와 디자인 `02` 문구 중 택일) +
    실버·골드 중립 바 문구 정정(`chart_no` 모순).
28. 「이 원본이 가는 곳」 항목의 클릭 목적지 규약(계층·테이블·필터).

### 5.5 SPEC-004 가 촉발하는 **타 spec 개정 요구** (요약)

| 대상 | 개정 항목 |
|---|---|
| SPEC-001 | 리뷰 `authorName` 마스킹 여부(C-3-2) · `gold_retention_monthly` 행수 확정 · `node_id` 25종 확정 목록 |
| SPEC-003 | `/api/kpi/cards` 에 `dod`·`dod_pct`·`unit`·`grain`·`spark`·기간 파라미터 · `/api/graph` 에 `kind`·`note`·노드 `source`·`edge_id` · `/api/forecast` 에 `title`/`message`/`edge.evidence` · `lineage` 에 `rule_id`·`gate`·`downstream`·`is_provisional` · `/api/layers/{layer}/tables` 에 `flows_to` · `lag` 표기 형식 통일 |
| SPEC-005 | 답변 객체에 `drilldown`·`followups` 추가 · `citations[].row_count` · 계수 기반 정량 추정의 허용 여부(§5 「집계를 에이전트가 하지 않는다」와의 관계) · G5-③ 의 검증 대상 화면 확정(OQ-4) |

---

## 6. 검토 한계

- 원천 데이터(`reference/ontology_demo/` 의 design 폴더 밖 bronze/·silver/ 등)는 PII 지침에
  따라 열지 않았다. 따라서 `tables.json`·`edges.json` 의 값이 **기록 02~07 과** 맞는지는
  검증하지 못했고, SPEC-001~005 의 서술값과만 대조했다.
- `20-spec/` 은 미커밋 draft 본을 읽었다(과제 지시대로). 커밋 시 값이 바뀌면 §3.1·§4 의
  행수 대조는 다시 봐야 한다.
- `.dc.html` 프로토타입은 브라우저로 실행하지 않고 소스로만 읽었다. 애니메이션·hover
  타이밍의 체감은 검토 대상에서 뺐다.
- 「기록 07」 원문을 보지 못했으므로, C-4 결함 1(축약 그래프의 없는 엣지)이 **디자인의
  창작**인지 **`edges.json` 의 누락**인지는 확정하지 못했다. 어느 쪽이든 두 파일이
  같아져야 한다는 결론은 바뀌지 않는다.

# SPEC — 피부 상담 목업 화면 2개 (charty-consult-mockup)

- 작성: planner 워커 · 2026-10-21 · 브리프 `spec-brief.md`
- 근거 문서: `_RESUME.md` · `research-report.md`(이하 R) · `assets-report.md`(이하 A)
- 근거 표기: 차티 `stg:<path>:줄`(= `CENTURION-CHARTY` origin/stg 461a48e, v1.8.0-rc.3, `frontend/src/` 생략) · 메디킷 `mk:<file>:줄`(1.4.0 설치본 `dist/`) · 원본 `har:measure` / `har:render` · 에셋 `A:<path>`(= `reference/2026-10-21-charty-poc/m3d-assets/`)
- 이 문서는 **스펙만** 정한다. 코드는 WP 순서대로 구현 워커 1명이 쓴다.

---

## 0. 한눈에

| 항목 | 값 |
|---|---|
| 앱 위치 | `reference/2026-10-21-charty-poc/web/` (Next.js App Router · TS) |
| 실행 | `npm run prepare:assets` → `npm run dev` → 같은 브라우저에서 `/screen` 탭 + `/tablet` 탭 |
| 화면 ① | `/screen` — 큰 스크린 1920×1080 가로. 좌 3D 얼굴 + 필터 / 우 분석 그래프 + 시술 플랜 + 최종 가격 |
| 화면 ② | `/tablet` — 상담사 태블릿 1180×820 가로. 차티 상담 화면 문법(가격표·선택 시술·할인·추천·체크리스트·차트·상담 텍스트) |
| 동기화 | `BroadcastChannel('charty-consult-mockup/v1')`. 태블릿이 상태의 주인, 스크린은 사본 |
| 데이터 | M3D 응답(HAR) → **어댑터** → 화면 모델 `SkinReport`. 가격표는 차티 데모 가격표 48건 |
| 3D | three.js + `@react-three/fiber` 9 + `@react-three/drei`. `Rgb.obj` 그대로, 텍스처 `_M.jpg` 3242×1621, 오버레이는 1장짜리 셰이더 합성 |
| 커밋 안 하는 것 | `web/public/m3d/**`(얼굴 텍스처·메시·측정 JSON 전부) · HAR · `m3d-assets/` — `.gitignore:86-91` 에 이미 있음 |

---

## 1. 화면 ① 큰 스크린 — `/screen`

### 1-1. 해상도 · 스테이지

- 설계 캔버스 **1920×1080 고정**. 실제 창 크기에 맞춰 `transform: scale()` 로 맞추고 남는 곳은 레터박스(배경 `--ms-gray-100`). 노트북 한 대로 탭 두 개를 띄워 시연해도 레이아웃이 깨지지 않게 하려는 것이다.
- 3D `<Canvas>` 는 `resize={{ offsetSize: true }}` 로 둔다(스케일 transform 이 측정값을 줄이지 않도록).
- 우상단 [전체화면] 버튼(`requestFullscreen`). 전체화면이 되면 버튼과 커서를 3초 뒤 숨긴다.
- 고객이 함께 보는 화면이라 **글자는 크게**: 본문 최소 `text-typo-heading-md-*`(16px), 점수 숫자 `text-typo-title-lg-600`(24px), 최종 가격 `text-typo-headline-lg-600`(40px). 10–12px 대 차티 소형 글씨(`text-[10px]` 등)는 화면 ①에서 쓰지 않는다.

### 1-2. 와이어

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│ [Charty 로고] 피부 상담     이건학 님 · 2026.10.16 측정            ● 상담사 화면 연결됨  10:42 [⛶] │ 64
├───────────────────────────────────────────────────┬──────────────────────────────────────────┤
│ A. 3D 뷰                         1040 × 944       │ B. 한눈에 보기                  856 × 372 │
│                                                   │ ┌ 레이더(4축) 320×320 ┐ ┌ 대분류 카드 2×2 ┐│
│                                                   │ │   염증·민감         │ │ 염증·민감 76 경도││
│                (3D 얼굴)                           │ │ 노화 ◇ 피부톤       │ │ 피부톤   68 중등도││
│                                                   │ │   피부결            │ │ 피부결 71.2 경도 ││
│                                                   │ └─────────────────────┘ │ 노화   68.3 중등도││
│                                                   │  한 줄 요약: "피부결과 붉은기는 …"         │
│ ┌ A2. 지금 보는 것 (좌하 플로팅 400w) ┐               ├──────────────────────────────────────────┤
│ │ 모공  68.8  [관리 시작]              │               │ C. 항목별 상태                  856 × 300 │
│ │ 흰 점 = 찾아낸 넓은 모공              │               │ 붉은기   ████████████░░  76  경도      │
│ │ 확장 모공 15.2% · 크기 450μm         │               │ 포르피린  점수 없음 · 5,470개            │
│ │ (주름 필터면 부위 맵 미니)            │               │ 색소 · 밝기 · 모공 · 피문 · 잔주름 · 굵은주름 │
│ └──────────────────────────────────────┘               │      (선택 필터와 이어진 행 강조)          │
│                                                   ├──────────────────────────────────────────┤
│ A1. 필터 바 (하단 72)                             │ D. 오늘의 시술 플랜              856 × 248 │
│ [자연광][잔주름][굵은주름][모공][붉은기][색소][피지 세균]│ 울쎄라 하안면 [정규가][10%] 2,200,000→1,980,000│
│                                                   │ 눈가 보톡스 120,000 · 리쥬란 HB 1회 [무료]  │
│                                                   │ ── 합계 VAT포함 2,310,000 · 10% 할인       │
│                                                   │    최종  2,079,000원   (40px)             │
└───────────────────────────────────────────────────┴──────────────────────────────────────────┘
```

- 구역 크기: 헤더 64 / 본문 1016(상하 패딩 16·좌우 24, 열 간격 24). 좌 A = 1040(≈54%), 우 B·C·D = 856(≈46%). 우측 세로는 B 372 · C 300 · D 248(간격 16·고정). D 가 넘치면 D 안에서만 스크롤.
- 배경: 페이지 `--ms-gray-100`, 각 구역은 메디킷 `Card padding="md"`(흰 바탕·`rounded-xl`·테두리). A 의 3D 캔버스 바탕은 `--ms-gray-800` 계열 어두운 단색(얼굴 사진 대비용).

### 1-3. 구성 요소 · 상태 · 상호작용

| 구역 | 구성 | 상태(읽는 값) | 상호작용 |
|---|---|---|---|
| 헤더 | 로고 · 「피부 상담」 · 고객명 · 측정일 · 연결 표시 · 시계 · 전체화면 | `report.customer`, `report.measuredAt`, `link.status` | 전체화면 버튼만 |
| A 3D 뷰 | §6 의 `FaceViewer` | `session.filter`, `session.cameraResetAt` | 드래그 회전 · 휠/핀치 확대(§6-4 범위). 더블클릭 = 정면 복귀 |
| A1 필터 바 | 필터 7개 칩(아이콘 + 한글명). 선택된 칩 primary 채움 | `session.filter` | 화면 ①에서 눌러도 바뀐다 → `filter:set` 을 태블릿에 보내고 태블릿 상태가 바뀐 뒤 스냅샷으로 돌아온다(§4). 손님이 직접 눌러 보는 경우를 위해 |
| A2 지금 보는 것 | 필터명 · 색 범례(“흰 선 = 찾아낸 잔주름”, “붉을수록 붉은기가 강한 곳”) · 이어진 항목 점수·등급 배지·쉬운 설명 1문장 · 측정치 2–3개 · 주름 필터일 때 **부위 맵 미니**(§2 G3) | `session.filter` → `FILTERS[filter].relatedItem` | 없음. `natural` 이면 카드 숨김 |
| B 한눈에 보기 | G1 레이더 · 대분류 카드 4 · 한 줄 요약 | `report.categories` | 카드 hover 없음(공동 시청 화면). `session.focusItem` 이 속한 대분류 카드 테두리 강조 |
| C 항목별 상태 | G2 막대 8행 | `report.items`, `session.filter`, `session.focusItem` | 없음. 강조 규칙: `focusItem` 우선, 없으면 현재 필터의 `relatedItem` |
| D 시술 플랜 | 체크된(`checked`) 카트 항목 목록 · 합계(VAT 별도/포함) · 할인율 · **최종(VAT 포함)** | `session.cart`, `session.discountRate`, `session.screen.showPrice` | 없음. 항목 추가 시 새 행 1.5초 primary-100 하이라이트, 금액은 300ms 숫자 트윈 |

빈 상태·예외:

| 경우 | 표시 |
|---|---|
| 카트 비었음 | D: “상담사가 시술을 고르면 여기에 보여요” |
| `showPrice=false` | D: 시술명·유형 배지만, 금액 열과 합계 줄을 감춘다(“가격은 상담사가 안내해 드려요”) |
| 태블릿 연결 끊김(5초 무응답) | 헤더 점 회색 + “상담사 화면 연결 대기”. 마지막 스냅샷은 그대로 보여 준다 |
| 3D 에셋 없음(`/m3d/manifest.json` 404) | A: “3D 에셋이 없습니다 — `npm run prepare:assets` 를 먼저 실행하세요”. 나머지 구역은 정상 |
| 측정 JSON 없음 | B·C: 같은 문구의 빈 상태. D 는 정상 |
| 3D 로딩 중 | A: 메디킷 `Loading` + “얼굴을 불러오는 중” (OBJ 20MB 파싱 1–3초) |

### 1-4. 가격 계산(화면 ①·② 공통, 차티와 같게)

차티 stg 계산을 그대로 옮긴다. 화면 ①은 계산하지 않고 공통 함수 결과를 그린다.

| 단계 | 식 | 근거 |
|---|---|---|
| 항목가 | `free ? 0 : discount>0 ? round(price×(1−discount/100)) : price` | `stg:features/pricing/utils/currency-format.ts:66-70` |
| 합계 | 체크된 항목(`checked !== false`)만 합 → `total`, `totalVat = round(total×1.1)` | `stg:features/pricing/utils/cart-utils.ts:4-16` |
| 최종 | `discountRate>0 ? round(totalVat×(1−rate/100)) : totalVat` (100% = 협찬 0원) | `stg:features/pricing/utils/cart-utils.ts:12-14`, `stg:features/pricing/components/cart-summary.tsx:86-100` |
| 표시 | 항목: 할인 있으면 정가 취소선 + 적용가, 무료면 「무료」 배지 + 정가 취소선 | `stg:features/pricing/components/cart.tsx:98-128` |

통화는 **KRW 고정**(차티의 통화 선택 `stg:features/pricing/components/pricing-panel.tsx:217-224` 은 옮기지 않는다).

---

## 2. 화면 ①의 그래프

메디킷·차티 모두 차트 라이브러리가 없다(R B-1, R A-3). **직접 SVG 컴포넌트 3개**를 만든다(의존성 0, 색은 CSS 변수). 라이브러리를 들이지 않는다.

### 2-1. 등급 4단계 — 기준 · 쉬운 이름 · 색

기준은 원본 리포트 안내문 「85점 이상 건강, 70–85 경도, 60–70 중등도, 60 이하 중도」(R C-1)를 **점수(score)로** 적용한다. HAR 값과 맞는지 확인했다(모공 68.8 → 중등도 = `har:measure` level 2, 레드존 76 → 경도 = level 1).

| 등급 키 | 점수 | 원본 이름 | 화면 이름(쉬운 말) | 차트 채움 | 배지(메디킷 `Badge`) |
|---|---|---|---|---|---|
| `good` | ≥ 85 | 건강 | **좋아요** | `--ms-primary` #6f21ff | `variant="primary"` + `className="bg-primary text-ms-white"` |
| `mild` | 70 ≤ s < 85 | 경도 | **조금 신경 써요** | `--ms-primary-500` #a290ff | `variant="primary"`(bg-primary-100 text-primary) |
| `moderate` | 60 ≤ s < 70 | 중등도 | **관리 시작** | `--ms-yellow` #fd9400 | `variant="warning"`(bg-yellow-100 text-yellow, `mk:index.js:837`) |
| `severe` | < 60 | 중도 | **집중 관리** | `--ms-red` #ff4e51 | `variant="danger"` |
| `none` | 점수 −1 | 무 | **점수 없음** | `--ms-gray-400` | `variant="neutral"` |

- 메디킷에 초록이 없다(success = primary, R A-2). 그래서 「좋음 = 브랜드색, 주의 = 따뜻한 색」으로 나눈다. 원본 4색(#29b99f 등)은 쓰지 않는다.
- 등급은 색만으로 전하지 않는다. 배지에 항상 글자를 같이 쓴다.

### 2-2. 그래프 목록

| # | 이름 | 위치 | 형태 | 데이터(`SkinReport`) | 원본 근거 |
|---|---|---|---|---|---|
| G1 | 종합 레이더 | B 좌 | 4축 레이더(염증·민감 / 피부톤 / 피부결 / 노화). 0–100, **바깥일수록 좋음**. 60·70·85 동심 다각형을 옅은 회색 점선으로 깔아 등급 띠를 보이고, 꼭짓점 점은 등급색 | `categories[].score` (76 · 68 · 71.2 · 68.3) | `har:measure` categories, R C-1 「종합분석」 |
| G1' | 대분류 카드 2×2 | B 우 | 이름 · 점수(24px) · 등급 배지 · 쉬운 설명 1문장 | 같은 값 | — |
| G2 | 항목별 막대 | C | 가로 막대 8행. 막대 길이 = 점수/100, 색 = 등급색, 60·70·85 세로 눈금선. 오른쪽에 점수 숫자 + 배지 | `items[]` — 붉은기 76 · 포르피린(점수 없음 → 막대 대신 “5,470개 · 얼굴의 30.6%”) · 색소 73 · 밝기 67 · 모공 68.8 · 피문 82.9 · 잔주름 83.8 · 굵은주름 65.6 | `har:measure` features |
| G3 | 주름 부위 맵 | A2(주름 필터일 때) | 정면 얼굴 실루엣 SVG(선화, 고정 좌표) 위에 부위 8개 점 + 점수 라벨. 점 색 = 등급색. 잔주름 필터면 잔주름 5부위 진하게·굵은주름 3부위 흐리게, 굵은주름 필터면 반대 | `wrinkleRegions[]` — 이마 92.8 · 미간 88.3 · 코뿌리 100 · 눈밑 79.5 · 눈가 90.7 · 눈물고랑 61.4 · 팔자 80.7 · 광대고랑 83.8 | `har:measure` basic_241·242 measures |

넣지 않는 것: 분포 히스토그램(`type:"distribution"` 11개 — 해석 난도가 높다, R C-3), LAB 좌표도·팬톤칩 12개, 좌/우 굵은주름 세부 곡률. 피부톤 코드는 B 의 한 줄 요약 옆에 **색 견본 칩 1개**(rgb `[155,108,76]` · “아몬드색”)로만 둔다.

### 2-3. 쉬운 설명 문구 규칙

문구는 `src/content/copy.ts` 한 파일에 모은다. 원본 analyze 의 설명문은 쓰지 않는다(공통 문구·빈 값·포르피린 내용 불일치, R C-3).

1. **진단·질환·치료 말 금지.** 「진단」→「피부 분석」, 「증상」→「고민」, 「치료」→「관리·시술」. 차티 차트 프롬프트 원칙과 같다(`stg:backend/app/service/chart/prompts.py` 「핵심 원칙」 2–4).
2. **전문 용어를 쉬운 이름으로.** 레드존→붉은기, 포르피린→피지 속 세균 흔적, 피문→피부결 골, 곡률→주름 깊이, 그레이스케일→밝기·칙칙함.
3. **한 문장 30자 안팎, 끝은 「~요」.** 숫자는 문장에 하나만(점수 또는 측정치).
4. **겁주지 않는다.** 「나쁨·심각」 대신 등급 이름(2-1)과 「관리하면 좋아져요」 꼴.
5. 문장 = `{쉬운 이름}{조사} {등급 문구}` + 항목별 뜻 1문장. 등급 문구: good 「좋은 상태예요」 / mild 「조금만 신경 쓰면 돼요」 / moderate 「지금부터 관리하면 좋아요」 / severe 「집중 관리가 필요해요」 / none 「점수는 나오지 않았어요」.
6. 조사는 메디킷 `withJosa` 로 붙인다(1.4.0 export).

항목별 사전(초안 — 구현 워커가 그대로 쓴다):

| 항목 키 | 쉬운 이름 | 뜻 1문장 |
|---|---|---|
| `redness` | 붉은기 | 피부 속 붉은 기운이 얼마나 퍼져 있는지예요 |
| `porphyrin` | 피지 속 세균 흔적 | 모공 속 피지에 생기는 세균 흔적의 양이에요 |
| `pigment` | 색소 | 기미·잡티처럼 갈색 색소가 얼마나 있는지예요 |
| `brightness` | 밝기 | 피부가 얼마나 맑고 환해 보이는지예요 |
| `pore` | 모공 | 넓어진 모공이 얼마나 있는지예요 |
| `dermatoglyph` | 피부결 | 피부 표면 골이 얼마나 고른지예요 |
| `fineWrinkle` | 잔주름 | 눈가·미간·이마의 가는 주름이에요 |
| `deepWrinkle` | 굵은 주름 | 팔자·눈물고랑처럼 깊게 팬 주름이에요 |

B 의 한 줄 요약 = 점수가 가장 낮은 대분류 2개를 골라 「{A}와 {B}부터 관리하면 좋아요」.

---

## 3. 화면 ② 상담사 태블릿 — `/tablet`

### 3-1. 해상도 · 근거 문법

- 설계 캔버스 **1180×820 고정**(iPad Air 가로), 화면 ①과 같은 scale-to-fit.
- 골격은 차티 상담 화면 데스크톱 배치를 따른다: 헤더 → 회색 세션 바 → 좌우 분할(좌: 상단 72px 띠 + 하단 가격 패널 | 우: 탭 패널) (`stg:pages/consultation/consultation-desktop.tsx:41-122`).
- ⚠ 차티 stg 는 1280px 미만(`stg:hooks/use-is-tablet.ts` — `max-width: 1279px`)이면 좌우 분할을 **위아래 쌓기**(좌 700px · 우 500px, 세로 스크롤)로 바꾼다(`stg:layouts/split-pane.tsx:24-34`). 1180 가로 태블릿에서 스크롤 없이 쓰려고 이 목업은 **좌우 분할을 유지**한다 → §11 정할 것 1.
- 글자 크기는 차티의 `max-xl:` 축소값(10–12px)을 그대로 쓴다. 손가락 터치 대상은 최소 32px 높이.

### 3-2. 와이어

```text
┌────────────────────────────────────────────────────────────────────────────────────────────┐
│ [Charty] 피부 상담 · 상담사                         10:42  메디솔브 피부과  [김상담] │ 50
├────────────────────────────────────────────────────────────────────────────────────────────┤
│ 이건학 님 · 2026.10.16 측정 · [첫방문 ▾]        ● 큰 화면 연결됨  [큰 화면 열기 ↗]  [가격 표시 ON] │ 40
├──────────────────────────────── 좌 700 ───────────────────────┬┬──────── 우 472 ──────────┤
│ 3D 필터 [자연광][잔주름][굵은주름][모공][붉은기][색소][피지 세균] [정면으로] ││ 피부분석|체크리스트|차트|상담 텍스트│ 72
├──────────────────────── 가격 패널 440 ────────┬┬─ 추천 260 ───┤│                          │
│ 시술 가격 [48]                                  ││ 추천 시술 [5]  ││  (탭 내용)                │
│ ┌ ProcedureList 220 ───┐┌ Cart 220 ─────────┐ ││ [보톡스][기기  ││                          │
│ │ 🔍 시술명 검색         ││ 선택 시술 [3] 전체해제│ ││  리프팅][레이저]││                          │
│ │ 보기 [추천 9][전체 48] ││ 눈가 보톡스   120,000│ ││ …             ││                          │
│ │ 시술 [전체][리프팅]…   ││ [할인없음▾][무료][삭제]│ ││ 보톡스         ││                          │
│ │ 유형 [전체][정규가]…   ││ …                   │ ││ 이유: 눈가·미간 ││                          │
│ │ 울쎄라 전체 얼굴       ││─────────────────────│ ││  잔주름         ││                          │
│ │  3,500,000 3,000,000   ││ 3/3건 선택           │ ││ 기대 효과 …    ││                          │
│ │ …                      ││ VAT별도 / VAT포함    │ ││ 금기 · 부작용 … ││                          │
│ │                        ││ 할인율 5 10 … 협찬100│ ││ [가격표에서 보기]││                          │
│ │                        ││ 최종(VAT포함) ……     │ ││               ││                          │
│ └────────────────────────┘└─────────────────────┘ ││               ││                          │
└────────────────────────────────────────────────────┴┴───────────────┴┴──────────────────────────┘
```

높이: 헤더 50 · 고객 바 40 · 본문 730(필터 띠 72 + 가격 영역 658). 분할 핸들 8px(차티와 같은 `w-2`, `stg:layouts/split-pane.tsx:44-53`). 핸들 드래그는 넣지 않고 고정폭으로 둔다(목업).

### 3-3. 구역별 기능 — 무엇을 본뜨나

| 구역 | 기능 | 본뜨는 차티 stg | 바뀌는 점 |
|---|---|---|---|
| 헤더 50 | 로고 · 화면명 「피부 상담 · 상담사」 · 시계 · 병원명 · 이름 pill | `stg:layouts/header.tsx:177-258` (50px 흰 헤더, `screenName` 슬롯 :195-199, 시계 :209, 이름 pill :230-234) | ServiceSwitcher·관리·결제 배지·크레딧·가이드·로그아웃 없음. 병원명·상담사명은 목 값 |
| 고객 바 40 | 고객명 · 측정일 · 상담 유형(첫방문/재방문/시술후) · 큰 화면 연결 표시 · [큰 화면 열기] · [가격 표시] 토글 | 세션 설정 바 `stg:pages/consultation/consultation-desktop.tsx:49-56` (`bg-ms-gray-100 border-b`) | 녹음 설정 대신 고객 맥락. 유형은 메디킷 `ComboBox`, 토글은 메디킷 `Toggle`. [큰 화면 열기] = `window.open('/screen','charty-screen')` |
| 필터 띠 72 | 3D 필터 7개 칩 + [정면으로] | 상태 패널 72px 슬롯 `stg:pages/consultation/consultation-desktop.tsx:100-106` | 녹음 컨트롤 대신 필터. 태블릿에는 3D 를 그리지 않는다(성능·발열) |
| 가격 패널 · 목록 | 검색 · 보기 [추천 n / 전체 48] · 대분류 칩 · 가격유형 칩 · 행 탭 = 카트 추가 · 정가 취소선 | `stg:features/pricing/components/pricing-panel.tsx:199-259` · `procedure-list.tsx:56-227` (탭→`addToCart` :189-193, 정가 취소선 :215-220, 감지됨/전체 토글 :79-103) · 정렬 가격 내림차순→이름 `pricing-panel.tsx:21-22` | 「감지됨」(녹취 감지) → **「추천」**(분석 기반 §3-4). 재방문이면 첫방문이벤트 숨김 규칙 그대로(`pricing-panel.tsx:58-66,84-88`) |
| 가격 패널 · 선택 시술 | 행 탭 = 체크 토글 · **항목 할인 5–50%** · **무료시술** · 삭제 · 전체선택/해제 · 전체삭제(할인율도 0) | `stg:features/pricing/components/cart.tsx:33-198` (할인 select :136-149, 무료 :151-160, 삭제 :161-166, 전체삭제 :56-66) | 같음. 네이티브 `<select>` 그대로 |
| 가격 패널 · 요약 | n/m건 선택 · VAT 별도/포함 · **전체 할인율 5–50% + 협찬 100%** · 최종(VAT 포함) | `stg:features/pricing/components/cart-summary.tsx:39-109` · 할인율 상수 `stg:features/pricing/constants/currencies.ts:22` | 환율 줄 없음 |
| 추천 260 | 추천 칩 · 칩 선택 시 이유 + 기대 효과·금기·부작용·시술 후 주의 카드 · [가격표에서 보기] | `stg:features/session/components/charty-recommendation.tsx:373-434`(헤더 「감지된 시술」 :375-384, 칩 :395-413) · 카드 `DetailSection` :106-230 | 헤더 「추천 시술」. 칩은 녹취 감지가 아니라 분석 규칙(§3-4). [가격표에서 보기] = 목록을 그 대분류로 거르고 보기=전체 |
| 우 탭 바 | 탭 4개, 활성 `border-b-2 border-primary text-primary` | `stg:features/chart/components/chart-toolbar.tsx:29-34,44-73` (자체 버튼 탭) | **「피부 분석」 탭을 맨 앞에 추가**(§11 정할 것 2). 진행 중 잠금(`lockNonChecklist`) 없음 |
| 탭 · 피부 분석 | 대분류 4 + 항목 8 목록(점수·배지·측정치 2개). 항목 탭 = 「큰 화면에서 강조」(`focusItem`) + 이어진 필터로 전환. 다시 탭 = 해제 | (차티에 없음 — 새 탭) | 상담사가 고객에게 설명할 항목을 고르는 리모컨 |
| 탭 · 체크리스트 | 필수 확인(그룹별 칩) 0/n · 상담 유형별 체크 · 카트 시술별 체크(부작용·사전·사후 색 구분) · 초기화 | `stg:features/session/components/consultation-checklist.tsx:11-406`(STATIC_CHECKS·GUIDE_CHECKS), `:408-600`(PROCEDURE_CHECKS), 렌더 `:814-1016` | 녹취 대신 **목 상담 텍스트에 같은 키워드 매칭**을 돌려 초기 체크를 채운다. 이후 수동 토글 |
| 탭 · 차트 | 차트 본문 미리보기 · [복사] · [편집]→[저장]/[취소] | 툴바 `stg:features/chart/components/chart-toolbar.tsx:75-122` · 가격 블록 `stg:features/chart/utils/build-pricing-summary.ts:9-40` | 본문은 템플릿 생성: 「■ 피부 분석 요약」(대분류·낮은 항목 3개) + 「■ 시술 가격 안내」(차티 형식 그대로). LLM 없음. 복사 시 `notify` 토스트 「복사되었습니다.」 |
| 탭 · 상담 텍스트 | 목 대화 12줄(상담사/고객 구분) | `stg:features/chart/components/chart-preview.tsx`(탭 `raw`) | 읽기 전용 |

### 3-4. 가격 조정 기능 — stg 확인 결과

| 기능 | stg 에 있나 | 근거 | 목업 |
|---|---|---|---|
| 항목별 할인율(5–50%, 5% 단위) | **있다** | `stg:features/pricing/components/cart.tsx:136-149`, store `setItemDiscount` `stg:stores/pricing-store.ts:77-82` | 넣는다 → ①에 반영 |
| 항목 무료 처리 | **있다** | `cart.tsx:151-160`, `pricing-store.ts:57-62` | 넣는다 |
| 전체 할인율(5–50%) + 협찬 100% | **있다** | `stg:features/pricing/components/cart-summary.tsx:60-79`, `stg:features/pricing/constants/currencies.ts:22` | 넣는다 |
| 체크 해제로 합계 제외 | **있다** | `cart.tsx:79`, `cart-utils.ts:4-6` | 넣는다(①에는 체크된 항목만) |
| 금액 직접 입력 | **상담 화면에는 없다.** 가격 편집 그리드(`pricing-edit-grid.tsx`)는 가격표 업로드 미리보기 화면(`/pricing/preview`)에서만 쓴다(`git grep` 결과 `pricing-preview-page.tsx` 만 import) | — | 넣지 않는다 → §11 정할 것 3 |

### 3-5. 목데이터 출처

| 목 | 출처 | 목업 파일 | 커밋 |
|---|---|---|---|
| 가격표 48건 | `stg:backend/app/seed_data/demo_pricing_v1.json`(「가격표_50건.xlsx 의 실제 유효 시술 48건」, 대분류 제모 10·리프팅 9·보톡스 7·레이저 6·필러 5·스킨케어 5·바디 4·부위별 2) | `src/data/mock/pricing.json` — 그대로 옮기고 `id: "p001"…` 만 덧붙인다 | ○ |
| 추천용 시술 설명 | `stg:backend/terminology/procedure-hub/taxonomy.json` `modality[]` 중 M1 보톡스 · M2 필러 · M4 스킨부스터 · M8 레이저 · M9 기기 리프팅 · M15 메디컬스킨케어의 `extracted` | `src/data/mock/taxonomy-subset.json` | ○ |
| 체크리스트 항목 | `stg:features/session/components/consultation-checklist.tsx:11-600` 상수 | `src/data/mock/checklist.ts` | ○ |
| 추천 규칙 | 목업용으로 이 스펙이 정한 규칙(아래). **의학적 근거가 아니다** — 파일 머리 주석에 적는다 | `src/data/recommend-rules.ts` | ○ |
| 상담 텍스트 12줄 | 새로 쓴다(눈가 주름·모공·예산·통증 걱정을 말하는 대화) | `src/data/mock/transcript.ts` | ○ |
| 병원명·상담사명 | 「메디솔브 피부과」 · 「김상담」(목 값) | `src/data/mock/session.ts` | ○ |
| 측정 수치 | HAR measure·render → 준비 스크립트 추출(§7) | `public/m3d/report/*.json` | ✗ (얼굴 데이터와 같이 로컬만) |

추천 규칙(`grade ∈ {moderate, severe}` 이거나 대분류 중 최저 점수 항목이면 발동, 점수 낮은 순 정렬):

| 분석 조건 | 추천 칩(taxonomy) | 이유 문구 | 「추천」 보기에 들어갈 가격표 행 |
|---|---|---|---|
| 잔주름 부위 중 점수 < 85 (눈밑 79.5) 또는 잔주름 mild 이상 | 보톡스(M1) | 「눈밑·눈가 잔주름」 | 보톡스 대분류 중 눈가·미간·이마·3부위 패키지·풀페이스 |
| 굵은주름 moderate (65.6, 눈물고랑 61.4) | 기기 리프팅(M9) · 필러(M2) | 「눈물고랑·팔자 굵은 주름」 | 리프팅 대분류(울쎄라·써마지·신스킨·고주파) · 필러 대분류 |
| 모공 moderate (68.8) | 스킨부스터(M4) · 레이저(M8) | 「넓어진 모공」 | 스킨케어 중 리쥬란 HB·스킨보톡스 · 레이저 중 제네시스 |
| 밝기 moderate (67) 또는 색소 mild 이상 | 레이저(M8) | 「칙칙함·색소」 | 피코토닝 · 르브란 · 올레이저 |
| 붉은기 mild 이상 (76) | 레이저(M8) | 「붉은기」 | 엑셀V |
| 포르피린 수량 ≥ 3,000 (5,470) | 메디컬스킨케어(M15) | 「피지·트러블 관리」 | 수소피부관리 |

HAR 값으로 돌리면 추천 칩 6개(보톡스·기기 리프팅·필러·스킨부스터·레이저·메디컬스킨케어), 「추천」 보기 행 약 20개가 나온다. 가격표에 팔자·눈물고랑 전용 필러 행은 없다(필러 5건이 코·입술·턱·패키지) — 대분류째로 보인다.

---

## 4. 동기화 · 라우트 · 초기 상태

### 4-1. 라우트

| 경로 | 화면 | 비고 |
|---|---|---|
| `/` | 시작 페이지 — [큰 화면 열기](새 창 `charty-screen`) · [상담사 화면 열기] 두 버튼과 사용법 3줄 | 서버 컴포넌트 가능 |
| `/screen` | 화면 ① | `'use client'` |
| `/tablet` | 화면 ② | `'use client'` |

두 화면 다 `src/app/(stage)/layout.tsx` 의 `Stage`(scale-to-fit)를 쓴다. 메디킷 1.4.0 번들에 `"use client"` 지시문이 없다(`dist/index.js` 0건) → 메디킷을 import 하는 파일은 전부 `'use client'` 아래에 둔다.

### 4-2. 원칙

- **태블릿이 상태의 주인.** `SessionState` 는 태블릿의 zustand store 에만 있고, 바뀔 때마다 **전체 스냅샷**을 보낸다. 상태가 작아서(카트 ≤ 20행) 차분 이벤트보다 단순하고 순서 문제가 없다.
- 화면 ①은 읽기 전용 사본. 유일한 역방향은 화면 ①의 필터 칩(`filter:set`)과 접속 인사(`screen:hello`).
- 받은 스냅샷의 `seq` 가 가진 것보다 작거나 같으면 버린다.
- 태블릿 상태는 `localStorage['charty-consult-mockup/session']` 에 저장해 새로고침해도 남긴다(읽기·쓰기 `try/catch`, 실패하면 초기 상태). 화면 ①은 저장하지 않는다.

### 4-3. 메시지 계약

채널 이름 `charty-consult-mockup/v1`. 모든 메시지는 봉투 하나:

```ts
type Envelope<T extends MsgType = MsgType> = {
  v: 1;
  type: T;
  from: 'tablet' | 'screen';
  senderId: string;   // 탭마다 crypto.randomUUID()
  at: number;         // Date.now()
  payload: Payloads[T];
};
```

| type | 방향 | payload | 받는 쪽 동작 |
|---|---|---|---|
| `screen:hello` | ① → ② | `{}` | 태블릿이 즉시 `state:snapshot` 회신 |
| `state:snapshot` | ② → ① | `{ seq: number; state: SessionState }` | `seq` 비교 후 교체 |
| `filter:set` | ① → ② | `{ filter: FilterKey }` | 태블릿 store `setFilter` → 새 스냅샷 송신 |
| `presence:ping` | ② → ①, 2초마다 | `{ seq: number }` | 화면 ①이 `presence:pong` 회신. 화면 ①은 마지막 ping 후 5초 지나면 「연결 대기」 |
| `presence:pong` | ① → ② | `{}` | 태블릿 고객 바 점: 5초 안 pong = 「큰 화면 연결됨」, 아니면 「큰 화면 없음」 |

`SessionState`:

```ts
interface SessionState {
  sessionId: string;
  consultType: 'first' | 'revisit' | 'post';
  filter: FilterKey;                 // 기본 'natural'
  focusItem: ItemKey | null;         // 피부 분석 탭에서 고른 항목
  cameraResetAt: number;             // [정면으로] 누른 시각. 바뀌면 화면 ① 카메라 초기화
  cart: CartItem[];
  discountRate: number;              // 0 | 5..50 | 100
  screen: { showPrice: boolean };    // 기본 true
}
interface CartItem {
  id: string;                        // 카트 행 id(같은 시술 두 번 담기 허용 — 차티와 같음, pricing-store.ts:49-52)
  procedureId: string;               // pricing.json 의 id
  name: string; category: string; subCategory: string | null;
  priceType: string;                 // '정규가' | '이벤트' | '첫방문이벤트' …
  price: number; originalPrice: number | null;
  discount: number;                  // 0 | 5..50
  free: boolean;
  checked: boolean;
}
```

화면 ①은 카트 행에 들어 있는 이름·가격만으로 그린다(가격표를 다시 찾지 않는다).

### 4-4. 초기 상태

| 값 | 초기 |
|---|---|
| `filter` | `'natural'` |
| `focusItem` | `null` |
| `cart` | `[]` |
| `discountRate` | `0` |
| `consultType` | `'first'` |
| `screen.showPrice` | `true` |
| 태블릿 탭 | 「피부 분석」 |
| 가격 목록 보기 | 「추천」 |

태블릿 고객 바에 [상담 초기화] 를 둔다(`ConfirmModal` → 위 초기 상태로 + 스냅샷 송신). 차티 [새 상담](`chart-toolbar.tsx:109-113`)에 해당.

---

## 5. 데이터 모델 · 어댑터 경계

### 5-1. 계층

```text
public/m3d/report/measure.json ─┐            (원본 M3D 응답 형태, 로컬만)
public/m3d/report/render.json  ─┤
                                 ▼
src/data/sources/m3d-mock-source.ts   fetch → 원본 타입(M3dMeasure, M3dRender)
                                 ▼
src/data/adapters/m3d.ts              fromM3d(measure, render, opts) → SkinReport   ← 경계
                                 ▼
src/domain/*.ts                        SkinReport · Grade · FilterDef (화면은 이것만 안다)
```

- 화면 코드는 `src/domain` 타입과 `useSkinReport()` 훅만 쓴다. `M3d*` 타입은 `src/data/` 밖으로 나가지 않는다.
- 진입 인터페이스:

```ts
interface SkinReportSource { load(): Promise<SkinReport>; }
// 지금: new M3dMockSource({ baseUrl: '/m3d/report', customer: { name: '이건학' } })
// 나중: 3D 스캔 업체 소스가 같은 인터페이스를 구현하고 자기 어댑터를 갖는다
```

- 고객 이름은 원본 `user` 를 읽지 않고 `opts.customer` 로 넣는다(원본에 실명·생년월일·회원번호가 있다, R C-2).

### 5-2. 화면 모델(`src/domain/skin-report.ts`)

```ts
type Grade = 'good' | 'mild' | 'moderate' | 'severe' | 'none';
type CategoryKey = 'inflammation' | 'tone' | 'texture' | 'aging';
type ItemKey = 'redness' | 'porphyrin' | 'pigment' | 'brightness'
             | 'pore' | 'dermatoglyph' | 'fineWrinkle' | 'deepWrinkle';
type RegionKey = 'TT' | 'MJ' | 'BG' | 'YD' | 'YW' | 'LG' | 'FL' | 'QJ';

interface SkinReport {
  customer: { name: string };
  measuredAt: string;                       // 'YYYY-MM-DD'
  categories: { key: CategoryKey; label: string; score: number | null; grade: Grade; items: ItemKey[] }[];
  items: {
    key: ItemKey; label: string;            // 쉬운 이름(copy.ts)
    score: number | null; grade: Grade;
    scoreNote?: string;                     // 점수 없음일 때 대신 보일 문장
    metrics: { key: string; label: string; value: number; unit: '' | '%' | 'μm' | 'mm' | '개'; display: string }[];
  }[];
  wrinkleRegions: { key: RegionKey; label: string; group: 'fine' | 'deep'; score: number; grade: Grade }[];
  tone: { name: string; code: string; rgb: [number, number, number] } | null;
  textures: TextureKey[];                   // 이 리포트에 있는 광원 텍스처
}
```

### 5-3. 어댑터 대응표(`fromM3d`)

| 화면 모델 | 원본 | 변환 |
|---|---|---|
| `categories` | measure `categories[]` — `basic_247`→inflammation · `basic_246`→tone · `basic_245`→texture · `basic_244`→aging | `score` 그대로, `-1`→`null` |
| `items` | measure `features[]` — `Red`→redness · `Porphyrin`→porphyrin · `Pigment`→pigment · `Grayscale`→brightness · `Pore`→pore · `Dermatograin`→dermatoglyph · `basic_241`→fineWrinkle · `basic_242`→deepWrinkle | `Pantone`·`SeasonColor` 는 items 에 넣지 않고 `tone` 으로 |
| `items[].metrics` | 항목별 화이트리스트(아래) | `ratio` 는 **×100 해서 %**(0.1523→15.2%) · `count` 는 천단위 콤마 · `extremum`/`intensity` 는 단위 없는 지수라 화면 ①에는 안 쓴다(태블릿만) |
| `wrinkleRegions` | `basic_241.measures[]`(BG·MJ·YD·YW·TT) · `basic_242.measures[]`(LG·FL·QJ) | `measure.score`. 좌/우 세부값은 버린다 |
| `tone` | `Pantone.measures[0].results` 의 `Skin_ID`(3R11) · `Skin_description`(아몬드색) · `rgb_value` | 원본 title(`描述词`·`rgb值`)은 안 쓴다 |
| `measuredAt` | render `date`(`2026/10/16`) | `-` 로 |
| `textures` | render `three_dimensional.mappings[].flag` | 매니페스트에 있는 것만 |
| `grade` | 위 `score` | §2-1 기준. `null`→`none` |

metrics 화이트리스트(label 은 어댑터가 한국어로 새로 붙인다 — 원본 title 미사용):

| 항목 | result id → 화면 label |
|---|---|
| redness | — (화면 ①은 점수만) · 태블릿: `red_max` 최댓값 · `red_peak` 대표값 |
| porphyrin | `porphyrin_count` 개수(개) · `porphyrin_percentage` 얼굴 중 비율(%) |
| pigment | 태블릿: `pigment_max` · `pigment_strength` |
| brightness | 태블릿: `grayscale_peak` · `grayscale_strength` |
| pore | `pore_big_ratio` 넓어진 모공 비율(%) · `pore_area_peak` 가장 많은 모공 크기(μm) · `pore_deep_ratio` 깊은 모공 비율(%) |
| dermatoglyph | `dermatograin_deep2_ratio` 깊은 골 비율(%) |
| fineWrinkle | 부위별 `wrinkles_*_length` 합 → 주름 길이 합(mm) |
| deepWrinkle | 부위 점수만(G3) |

### 5-4. 원본 품질 이슈 보정 — 규칙과 표시

| 이슈(R C-2) | 보정 | 화면 표시 |
|---|---|---|
| 중국어 미번역 title(`描述词`·`rgb值`·`红度`·`比例` 등) | 원본 title 을 **아예 쓰지 않고** 어댑터 사전의 한국어 label 만 쓴다. 사전에 없는 result 는 버린다 | 없음 |
| 굵은주름 좌/우가 id 와 title 이 반대 | id(`_right_`/`_left_`)를 기준으로 삼는다. 화면 ①은 좌/우를 아예 안 보인다 | 태블릿 피부 분석 탭에서 좌/우 값을 보일 때 ⓘ 툴팁 「원본 리포트의 좌우 표기와 다를 수 있어요」 → §11 정할 것 4 |
| 점수 −1(포르피린·팬톤·LAB) | `score:null`, `grade:'none'`. 대분류 점수는 원본 그대로(염증&민감 76) | 「점수 없음」 회색 배지 + `scoreNote`(포르피린: 「점수는 나오지 않았어요 · 5,470개 발견」) |
| ratio 의 `unit:"%"` 인데 값이 0~1 | ×100. 값이 정확히 1 인 굵은주름 `length_ratio` 는 쓰지 않는다 | % 로 |
| 포르피린 설명이 피부결 설명으로 들어감(analyze) | analyze 설명문 전부 미사용, `copy.ts` 사용 | 없음 |

### 5-5. 파일 구성

```text
web/
  src/
    app/ page.tsx · (stage)/layout.tsx · (stage)/screen/page.tsx · (stage)/tablet/page.tsx · globals.css · layout.tsx
    domain/     skin-report.ts · grade.ts · filters.ts · session.ts · pricing.ts(계산 함수)
    content/    copy.ts
    data/
      sources/  m3d-mock-source.ts · use-skin-report.ts
      adapters/ m3d.ts · m3d-types.ts · m3d.test.ts · __fixtures__/measure.sample.json · render.sample.json
      mock/     pricing.json · taxonomy-subset.json · checklist.ts · transcript.ts · session.ts
      recommend-rules.ts
    sync/       channel.ts · use-tablet-sync.ts · use-screen-sync.ts
    stores/     session-store.ts(태블릿) · screen-store.ts(화면 ① 사본)
    components/ stage/ · viewer/ · charts/ · screen/ · tablet/ · common/
  scripts/      prepare-assets.mjs
  public/m3d/   (생성물 — gitignore)
  e2e/          sync.spec.ts · viewer.spec.ts
```

`__fixtures__/*.sample.json` 은 **손으로 만든 가짜 값**(원본과 같은 형태, 숫자는 임의)이다. HAR 값은 커밋 파일에 들어가지 않는다.

---

## 6. 3D 뷰어 설계

### 6-1. 스택 — `@react-three/fiber` 를 쓴다

| 선택 | 이유 |
|---|---|
| `three` 0.18x + `@react-three/fiber` 9 + `@react-three/drei` 10 | React 19 대응판. 필터 상태(React)를 uniform 으로 넘기는 일이 대부분이라 선언형이 짧다. `OrbitControls`·`useProgress` 를 drei 로 받는다 |
| `next/dynamic(() => import('./face-viewer'), { ssr: false })` | WebGL 은 브라우저 전용 |

### 6-2. 로딩

- 메시: `useLoader(OBJLoader, '/m3d/mesh/Rgb.obj')`(`three/examples/jsm/loaders/OBJLoader.js`). `.mtl` 은 없다(A §4) — 로더 재질은 버리고 아래 셰이더로 갈아 끼운다.
- 그룹 안 첫 `Mesh` 의 geometry 하나만 쓴다. `geometry.computeBoundingBox()` 후 중심을 원점으로 옮긴다(`geometry.center()`). 단위는 미터, 얼굴 폭 약 0.21(A §4).
- 텍스처: `THREE.TextureLoader` 로만 읽는다(**`ImageBitmapLoader`·`createImageBitmap` 금지** — `flipY` 가 먹지 않는다).
- 로딩 순서: 매니페스트 → 메시 + 기본 텍스처(자연광) → 첫 화면 → 나머지 텍스처 4장·오버레이 3장을 백그라운드 선로딩. 필터 전환 때 기다림이 없게.

### 6-3. 합성 — 셰이더 1개

원본 M3D 뷰어도 텍스처 두 장을 셰이더로 섞는다(A §0-5, §4). 같은 방식으로 **재질 하나·드로우콜 하나**로 한다(겹친 메시 두 장 방식은 z-fighting 이 생긴다).

```glsl
// uniforms
uniform sampler2D uBase;      // 지금 광원 텍스처
uniform sampler2D uBasePrev;  // 직전 광원 텍스처(교체 페이드용)
uniform float     uMix;       // 0→1, 250ms
uniform sampler2D uOverlay;   // RGBA PNG(흰색 + 알파)
uniform float     uOverlayOn; // 0 | 1 (페이드 250ms)
uniform vec3      uOverlayColor;
varying vec2 vUv;
void main() {
  vec3 base = mix(texture2D(uBasePrev, vUv).rgb, texture2D(uBase, vUv).rgb, uMix);
  float a = texture2D(uOverlay, vUv).a * uOverlayOn;
  gl_FragColor = vec4(mix(base, uOverlayColor, a), 1.0);
}
```

- **조명 없음(unlit).** 텍스처가 이미 촬영 사진이라 빛을 더하면 색이 바뀐다.
- 색공간: 텍스처 `colorSpace = THREE.NoColorSpace`, `<Canvas flat linear>`. 셰이더가 사진 픽셀을 그대로 내보낸다(원본과 같은 색). sRGB 변환을 섞지 않는다.
- 필터링: `minFilter = LinearMipmapLinearFilter`, `anisotropy = gl.capabilities.getMaxAnisotropy()`. 3242×1621 은 2의 거듭제곱이 아니지만 WebGL2 에서 밉맵이 된다.
- 오버레이가 없는 필터는 `uOverlayOn=0`, `uOverlay` 에 1×1 투명 텍스처.

### 6-4. 좌표 · 카메라 주의점

| 항목 | 값 · 주의 |
|---|---|
| UV 상하 | OBJ `vt.v` = 1 − 이미지 v(A §6). three.js `TextureLoader` 기본 **`flipY = true` 가 정답**이다. 텍스처·오버레이 모두 기본값 유지, 코드에 `flipY` 를 건드리지 않는다 |
| 축 | y 위 · +z 정면 · x 음수 = 고객의 오른쪽(A §4). 카메라는 +z 에서 원점을 본다 |
| 좌우 | 화면에는 **마주 보는 시점**(고객의 오른쪽이 화면 왼쪽)으로 나온다. 거울 반전(`scale.x=-1`)을 하지 않는다 |
| 카메라 | `PerspectiveCamera fov 28`, 위치 `(0, 0, 0.55)` |
| OrbitControls | `enablePan=false` · `minDistance 0.28` · `maxDistance 0.9` · 좌우 `minAzimuthAngle -75°` `maxAzimuthAngle +75°` · 상하 `minPolarAngle 60°` `maxPolarAngle 120°` · `enableDamping` |
| 정면 복귀 | `session.cameraResetAt` 이 바뀌거나 캔버스 더블클릭 → 600ms 보간으로 기본 위치 |
| 면 방향 | 메시가 얼굴 앞면만 있으므로 `side: DoubleSide` 로 옆에서 봐도 구멍이 안 보이게 |

### 6-5. 필터 정의(`src/domain/filters.ts`)

연결은 A §5. 오버레이 필터의 바탕은 원본 분석 atlas 가 쓰는 냉광(`rgb_cool`)이다.

| FilterKey | 화면 이름 | 바탕 텍스처 | 오버레이 | 오버레이 색 | 이어진 항목 | 범례 문구 |
|---|---|---|---|---|---|---|
| `natural` | 자연광 | `natural`(Rgb) | — | — | — | — |
| `fineWrinkle` | 잔주름 | `cool`(RgbCool) | `fine-wrinkle`(wrinkle_mixed) | `--ms-primary-500` #a290ff | fineWrinkle | 보라 선 = 찾아낸 잔주름 |
| `deepWrinkle` | 굵은 주름 | `cool` | `deep-wrinkle`(rough_wrinkle_mask) | `--ms-yellow` #fd9400 | deepWrinkle | 주황 선 = 깊게 팬 주름 |
| `pore` | 모공 | `cool` | `pore`(pores) | `#ffffff` | pore | 흰 점 = 넓어진 모공 |
| `redness` | 붉은기 | `red-heat`(RedHeat · 염증 히트맵) | — | — | redness | 붉을수록 붉은기가 강한 곳 |
| `pigment` | 색소 | `brown-heat`(BrownHeat · 색소 히트맵) | — | — | pigment | 진할수록 색소가 많은 곳 |
| `porphyrin` | 피지 세균 | `uv`(Uv · 자외선) | — | — | porphyrin | 주황·붉게 빛나는 점 = 피지 속 세균 흔적 |

함몰·피문·노화 시뮬레이션·좌우 비교·등고선은 넣지 않는다(정해진 것).

---

## 7. 에셋 준비 스크립트 — `web/scripts/prepare-assets.mjs`

- 실행: `npm run prepare:assets`(= `node scripts/prepare-assets.mjs`). 의존: `sharp`(devDependency).
- 입력 위치: `M3D_SRC`(기본 `../m3d-assets`) · `M3D_HAR`(기본 `../m3d-ai-h5.migamedi.co.kr.har`).
- 출력: `public/m3d/` 를 지우고 다시 만든다(멱등). 입력 파일이 하나라도 없으면 무엇이 없는지 출력하고 종료 코드 1.

| 출력 | 입력 | 처리 |
|---|---|---|
| `mesh/Rgb.obj` | `A:obj/Rgb.obj` | 복사(20.4MB, 가공 없음) |
| `tex/natural.jpg` | `A:thumb/Rgb_M.jpg` | 복사 · 3242×1621 확인 |
| `tex/cool.jpg` | `A:thumb/RgbCool_M.jpg` | 같음 |
| `tex/red-heat.jpg` | `A:thumb/RedHeat_M.jpg` | 같음 |
| `tex/brown-heat.jpg` | `A:thumb/BrownHeat_M.jpg` | 같음 |
| `tex/uv.jpg` | `A:thumb/Uv_M.jpg` | 같음 |
| `overlay/fine-wrinkle.png` | `A:hd_ai/wrinkle_mixed.png`(9728×4864 L) | 아래 오버레이 처리 |
| `overlay/deep-wrinkle.png` | `A:hd_ai/rough_wrinkle_mask.png` | 같음 |
| `overlay/pore.png` | `A:hd_ai/pores.png` | 같음 |
| `report/measure.json` | HAR 에서 URL 경로가 `/api/skin/measure/results/render` 인 응답의 `data` | 그대로(측정 수치. 개인 식별 필드 없음) |
| `report/render.json` | HAR `/api/skin/report/render.v3` 응답의 `data` | **화이트리스트만**: `date`, `atlas[]`, `three_dimensional.mappings[].{flag,title}` |
| `manifest.json` | — | `{ generatedAt, mesh:{file,bytes}, textures:{key:{file,w,h}}, overlays:{key:{file,w,h,coverage}}, report:{measure,render} }` |

오버레이 처리(흰 선·점 마스크 → 투명 PNG):

1. L 채널을 읽어 `resize(3242, 1621, { kernel: 'lanczos3' })`.
2. 알파 = `min(255, L × gain)` (기본 `gain=3`, 축소로 옅어진 가는 선을 살린다). RGB = 흰색(255) — 색은 셰이더가 입힌다.
3. RGBA PNG(`compressionLevel 9`)로 저장. `coverage` = 알파 > 32 인 픽셀 비율을 매니페스트에 기록(모공 원본 4.4%, A §2 와 비교용).

개인정보 가드: `render.json`·`measure.json` 을 쓰기 전에 키 이름에 `hash`·`user`·`url`·`icon`·`scanner`·`unique` 가 남아 있으면 에러로 멈춘다. 끝에 `git check-ignore -q public/m3d` 를 돌려 무시되지 않으면 경고를 띄운다.

---

## 8. 메디킷 1.4.0 적용

### 8-1. 설치 · 설정

| 항목 | 값 | 근거 |
|---|---|---|
| 패키지 | `@medisolve-ai/medikit@1.4.0`(정확히 고정) · peer `react>=18` · `tailwindcss>=3` | `mk:package.json` |
| Tailwind | **3.4 고정**(`tailwindcss@^3.4` + `postcss` + `autoprefixer` + `postcss-import`). `create-next-app` 이 깔아 주는 v4 는 쓰지 않는다 — preset 이 v3 형식 | 차티 stg 도 3.4(R B-1) |
| `tailwind.config.ts` | `presets: [medikitPreset]`(`@medisolve-ai/medikit/tailwind`) · `content` 에 `./src/**/*.{ts,tsx}` + `./node_modules/@medisolve-ai/medikit/dist/**/*.{js,mjs}` | `stg:frontend/tailwind.config.ts:3-11`(이 줄만 레포 루트 기준) |
| `postcss.config.mjs` | `postcss-import` → `tailwindcss` → `autoprefixer` 순(`base.css` 안의 `@tailwind` 지시문을 처리하려면 import 가 먼저 인라인돼야 한다) | `mk:styles/base.css:7-9` |
| `globals.css` | 1행 `@import "../../node_modules/@medisolve-ai/medikit/dist/styles/base.css";` → `@tailwind base/components/utilities` → `:root` 차티 테마 | `stg:styles/index.css:1-31` |
| 차티 테마 | `:root { --ms-primary:#6f21ff; --ms-primary-100:#f4f3ff; --ms-primary-300:#e9e6ff; --ms-primary-500:#a290ff; --ms-primary-shadow:rgba(111,33,255,.3); --ms-primary-hover:#5a1acc; --ms-white:#ffffff; }` — `data-product` 속성은 안 쓴다 | `stg:styles/index.css:16-25` |
| solid 버튼 hover 보정 | 차티가 덧댄 hover 규칙을 그대로 옮긴다 | `stg:styles/index.css:37-` (PLAN-139-T-004) |
| 폰트 | Pretendard Variable — `pretendard` npm 패키지의 variable woff2 를 `next/font/local` 로 | `stg:styles/index.css:7-14` |
| body | `bg-slate-50` 대신 화면별 배경(① `--ms-gray-100`, ② 흰색) | — |

### 8-2. 쓸 메디킷 컴포넌트

| 컴포넌트 | 쓰는 곳 |
|---|---|
| `Button` | 시작 페이지 · 큰 화면 열기 · 정면으로 · 복사/편집/저장/취소 · 상담 초기화 · 전체화면 |
| `Badge` | 등급 배지(§2-1) · 개수 배지 |
| `Card` | 화면 ① 구역 틀 · 추천 상세 카드 틀 |
| `ComboBox` | 상담 유형(첫방문/재방문/시술후) · 차트 복사 대상(전체/내부 메모 제외, `chart-toolbar.tsx:82-95`) |
| `Toggle` | 고객 바 「가격 표시」 |
| `Tooltip*` | 좌/우 보정 ⓘ · 측정치 설명 |
| `Textarea` | 차트 편집 |
| `ConfirmModal` | 상담 초기화 확인 |
| `Loading` | 3D 로딩 · 측정 로딩 |
| `NotifyContainer` / `notify` | 복사 토스트 |
| `Divider` | 구획선 |
| `withJosa` · `formatNumber` | 문구 조사 · 금액 콤마 |

쓰지 않는 것: `Progress`(잔량 모델이라 점수 막대 뜻과 반대, R A-3) · `Tabs`(차티 상담 화면도 자체 버튼 탭, `chart-toolbar.tsx:53-66`) · `Header`·`Menu`(차티도 0건, R B-3).

### 8-3. 직접 만드는 것

| 부품 | 메모 |
|---|---|
| `Stage` | 고정 캔버스 scale-to-fit |
| `FaceViewer` · `FaceMaterial` | §6 |
| `FilterBar` | 화면 ①(큰 칩 56px) · 화면 ②(차티 칩 문법 `rounded-full text-[11px]`) 두 크기 |
| `RadarChart` · `ScoreBars` · `FaceRegionMap` | §2 SVG |
| `GradeBadge` | `Badge` 래핑 + §2-1 표 |
| `FocusCard` | 화면 ① A2 |
| `PlanPanel` | 화면 ① D |
| `AppHeader` · `CustomerBar` | 차티 `header.tsx` 문법을 옮긴 축소판 |
| `ProcedureList` · `Cart` · `CartSummary` · `RecommendationPanel` · `ChecklistPanel` · `ChartPanel` · `TranscriptPanel` · `AnalysisPanel` | 차티 자체 컴포넌트(메디킷에 없음)를 §3-3 근거대로 다시 쓴다. 차티 코드를 복사하지 말고 같은 클래스·구조로 새로 짠다(zustand·TanStack 의존 없이 목업 store 로) |
| `ConnectionDot` | 연결 표시 |

아이콘은 `lucide-react`(차티와 같음, R B-3).

---

## 9. WP 분할 (구현 워커 1명 · 순서대로)

각 WP 끝에 **그 WP 관련 확인만** 하고, 전체 확인(`npm run verify`)은 WP8 에서 한 번 한다.

| WP | 내용 | 완료 조건 |
|---|---|---|
| **WP1 뼈대** | `web/` 에 Next.js(최신 16.x, App Router, TS, ESLint) · Tailwind 3.4 · 메디킷 1.4.0 · 차티 테마 · Pretendard · 라우트 3개 빈 화면 · `Stage` · `package.json` 스크립트(`dev`·`build`·`lint`·`test`·`e2e`·`prepare:assets`·`verify`) | `npm run build` 통과 · `/` `/screen` `/tablet` 200 · 메디킷 `Button variant="solid" color="blue"` 배경이 `#6f21ff` · 창 크기를 바꿔도 1920×1080 캔버스가 비율 유지 |
| **WP2 에셋 · 목 데이터 준비** | `scripts/prepare-assets.mjs`(§7) · `src/data/mock/*`(§3-5 출처에서 옮김) | 스크립트 1회 실행으로 §7 표의 파일이 전부 생기고 매니페스트의 텍스처 w/h 가 3242/1621 · 두 번 돌려도 같은 결과 · 입력 하나를 지우면 종료 코드 1 · `git status` 에 `public/m3d` 아래 파일이 안 나옴 · `report/*.json` 에 가드 키 없음 |
| **WP3 데이터 계층** | domain 타입 · `grade.ts` · `copy.ts` · `m3d-types.ts` · `fromM3d` · `M3dMockSource` · `useSkinReport` · 가격 계산 함수 · 추천 규칙 · 단위 테스트(Vitest) | 테스트 통과: 등급 경계(84.9→mild, 85→good, 60→moderate, 59.9→severe, −1→none) · 가짜 픽스처로 대분류 4·항목 8·부위 8 생성 · `ratio` ×100 · 중국어 title 이 결과 어디에도 없음 · −1→null · 가격 계산이 §1-4 예(아래 AC-14)와 같음 · 실제 `public/m3d/report` 로 돌렸을 때 §2-2 의 숫자가 나옴 |
| **WP4 3D 뷰어** | §6 전부 + 화면 ① 좌측(A·A1) 단독 동작(로컬 상태) | 얼굴이 정면으로 뜬다 · 7개 필터가 전부 바뀐다 · 회전·확대 범위가 §6-4 · 오버레이 선이 사진의 주름 위치에 붙는다(눈 확인, 스크린샷 남김) · 에셋 없을 때 안내 문구 |
| **WP5 화면 ① 우측** | 헤더 · B(G1·G1') · C(G2) · A2(FocusCard·G3) · D(PlanPanel) — 목 `SessionState` 하나로 | §2 숫자가 화면에 보인다 · 등급 색이 §2-1 · 필터 바꾸면 A2 와 C 강조가 바뀐다 · 빈 카트·가격 숨김 상태가 §1-3 대로 |
| **WP6 화면 ②** | 헤더 · 고객 바 · 필터 띠 · 가격 패널(목록·카트·요약) · 추천 · 탭 4개 | §3-3 표의 기능이 전부 동작 · 가격 계산이 차티와 같음 · 추천 칩 6개 · 「추천」 보기 행이 규칙대로 · 재방문이면 첫방문이벤트 숨김 · 체크리스트 초기 체크가 목 상담 텍스트 키워드로 채워짐 |
| **WP7 동기화** | `channel.ts` · 태블릿 store → 스냅샷 송신 · 화면 ① 수신 · hello · filter:set · presence · localStorage 저장 | 두 탭에서 AC-5~AC-11 손 확인 · 태블릿 새로고침 후 카트 유지 · 화면 ① 새로고침 후 1초 안에 같은 상태 |
| **WP8 검증** | Playwright e2e(`e2e/sync.spec.ts` · `e2e/viewer.spec.ts`) · `npm run verify`(= lint + test + build + e2e) · 스크린샷 4장(① 자연광 · ① 모공 · ① 카트 3건+할인 · ②)을 `orchestration/work/charty-consult-mockup/screens/` 에 저장. 얼굴이 찍히므로 이 폴더를 `.gitignore` 에 추가(커밋 금지) | `npm run verify` 통과 · AC 전부 확인 표 작성 |

---

## 10. 수용 기준 (AC)

빌드 · 실행

1. `web/` 에서 `npm ci && npm run build` 가 **`public/m3d/` 가 없어도** 통과한다.
2. `npm run lint` · `npm run test` 가 통과한다.
3. `npm run prepare:assets` 1회로 §7 의 파일이 모두 생기고, `git status --porcelain` 에 `public/m3d/` · HAR · `m3d-assets/` 아래 경로가 하나도 나오지 않는다.
4. 커밋되는 파일(`git ls-files reference/2026-10-21-charty-poc/web`) 어디에도 HAR 의 리포트 hash·생년월일·회원번호·S3 URL 이 없다(`grep` 0건).

동기화(같은 브라우저, `/tablet` 탭 + `/screen` 탭)

5. 태블릿에서 시술 행을 누르면 **1초 안에** 화면 ① D 에 그 시술명과 금액이 보인다.
6. 태블릿에서 항목 할인(예 20%)·무료·체크 해제·삭제를 하면 1초 안에 화면 ① 의 행과 합계가 바뀐다.
7. 태블릿에서 전체 할인율 10% 를 누르면 1초 안에 화면 ① 최종 금액이 `round(totalVat × 0.9)` 로 바뀌고, 「협찬 100%」 면 0원이 된다.
8. 태블릿 필터 칩을 누르면 1초 안에 화면 ① 3D 텍스처가 바뀌고 해당 칩이 선택 표시된다. 화면 ①에서 필터 칩을 누르면 태블릿 칩도 1초 안에 따라 바뀐다.
9. 태블릿 「피부 분석」 탭에서 항목을 누르면 화면 ① C 의 그 행이 강조되고 필터가 이어진 필터로 바뀐다.
10. 화면 ① 탭을 새로고침하면 1초 안에 태블릿과 같은 상태(카트·할인·필터)로 돌아온다. 태블릿 탭을 새로고침해도 카트가 남는다.
11. 화면 ① 탭을 닫으면 5초 안에 태블릿 고객 바가 「큰 화면 없음」, 다시 열면 「큰 화면 연결됨」이 된다.
12. 「가격 표시」를 끄면 화면 ① D 에서 금액·합계가 사라지고 시술명은 남는다.

화면 · 데이터

13. 화면 ① 레이더 4축 값이 76 · 68 · 71.2 · 68.3, 막대 7개 값이 76 · 73 · 67 · 68.8 · 82.9 · 83.8 · 65.6 이고 색이 §2-1 등급표와 맞는다. 포르피린 행은 막대 대신 「점수 없음」과 5,470개를 보인다.
14. 가격 계산 예: 「눈가 보톡스」(120,000) 항목 할인 없음 + 「리쥬란 HB 1회」(200,000) 무료 + 「울쎄라 하안면」(2,200,000) 항목 10% → 합계 VAT 별도 2,100,000 · VAT 포함 2,310,000, 전체 할인 10% → 최종 2,079,000. 태블릿과 화면 ①이 같은 숫자를 보인다.
15. 화면 ①·② 어디에도 중국어(한자) 문자열과 「−1」 점수 표시가 없다(`/[一-鿿]/` 0건).
16. 굵은주름 좌/우 값을 보이는 곳(태블릿)에는 보정 ⓘ 안내가 있다. 화면 ①에는 좌/우 표기가 없다.
17. 화면 ① 문구에 「진단」「질환」「치료」「환자」가 없다.
18. 태블릿 가격 목록이 48건이고, 「추천」 보기는 §3-4 규칙의 행만 보인다. 상담 유형을 「재방문」으로 바꾸면 첫방문이벤트 행·칩이 사라진다.

3D

19. 화면 ① 첫 진입 시 3D 얼굴이 정면(+z)으로, 화면 기준 거울 반전 없이 뜬다.
20. 필터 7개가 각각 다른 그림을 만든다 — e2e 가 필터마다 캔버스 스크린샷을 찍어 서로 다름(픽셀 차 > 1%)을 확인한다.
21. 잔주름·굵은주름·모공 필터에서 오버레이가 사진 위 제자리에 붙는다(눈가·팔자 위치 눈 확인, 스크린샷 첨부). 위아래가 뒤집혀 있으면 실패.
22. 드래그로 좌우 ±75° 까지만 돌고, [정면으로](태블릿)·더블클릭(화면 ①)으로 정면에 돌아온다.
23. `public/m3d/` 가 없으면 화면 ① 3D 자리에 준비 스크립트 안내가 뜨고 페이지는 죽지 않는다.

문법 · 테마

24. 메디킷 1.4.0 이 `package.json` 에 정확한 버전으로 있고, primary 색이 `#6f21ff` 다(태블릿 활성 탭 밑줄·선택 칩).
25. 태블릿 우측 탭 바·가격 목록·선택 시술·할인 요약이 §3-3 의 stg 근거와 같은 구조(행 탭=추가, select 할인, 무료/삭제 버튼, 할인율 버튼 줄 + 협찬 100%)를 갖는다.

---

## 11. 정할 것 (planner 가 못 정한 것 — 기본값으로 진행 가능)

| # | 항목 | 왜 못 정했나 | 기본값 |
|---|---|---|---|
| 1 | 태블릿 레이아웃 — 차티 stg 태블릿(<1280)은 위아래 쌓기+스크롤(`stg:layouts/split-pane.tsx:24-34`), 목업은 좌우 분할 | 「차티 문법」과 「태블릿에서 한눈에」가 부딪힌다 | **좌우 분할**(§3-2) |
| 2 | 태블릿 우측에 「피부 분석」 탭 추가 | 차티 탭은 3개(`chart-toolbar.tsx:29-34`)인데 상담사가 고객에게 설명할 항목을 고를 자리가 따로 없다 | **추가, 맨 앞 탭** |
| 3 | 금액 직접 수정(정가 대신 임의 금액) | stg 상담 화면에 없다(§3-4). 넣으면 차티에 없는 기능을 보이는 셈 | **넣지 않는다**(할인 % · 무료 · 전체 할인만) |
| 4 | 굵은주름 좌/우 — id 와 title 중 무엇이 맞나 | 원본 값으로는 판별 근거가 없다(R C-2) | **id 기준** + 태블릿 ⓘ, 화면 ①은 좌/우 미표시 |
| 5 | 추천 규칙(§3-4 표) | 분석 → 시술 매핑은 의료 판단이라 planner 가 확정할 수 없다 | **표대로**, 파일 머리에 「목업용 · 의학적 근거 아님」 |

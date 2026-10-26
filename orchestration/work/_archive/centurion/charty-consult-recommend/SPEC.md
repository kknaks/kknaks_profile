# SPEC — 큰 화면 부위별 추천 시술 카드 (charty-consult-recommend)

- 작성: planner 워커 · 2026-10-26 · 브리프 `spec-brief.md`
- 정해진 것: `_RESUME.md` §2(다시 논의하지 않는다). 이 문서는 §2 를 화면·데이터·WP 로 푼다
- 직전 스펙: `_archive/centurion/charty-consult-mockup/SPEC.md`(이하 **구 SPEC**). 여기서 바꾸지 않은 것은 구 SPEC 그대로다
- 근거 표기: 코드 `web:<path>:줄`(= `reference/2026-10-21-charty-poc/web/`, 828948b) · 측정 원본 `measure:<feature>/<measure>`(= `web/public/m3d/report/measure.json`, 로컬) · Hub `hub:<endpoint>`(= `https://stg-procedure-hub.medisolveai.com/api/<endpoint>`, 2026-10-26 받아 확인)
- **스펙만** 정한다. 코드는 WP 순서대로 frontend 워커 1명이 쓴다. **태블릿 화면(`/tablet`)은 이번에 바꾸지 않는다**

---

## 0. 한눈에

| 항목 | 값 |
|---|---|
| 바뀌는 화면 | `/screen`(화면 ①)만. 1920×1080 고정 캔버스·`Stage` scale-to-fit 그대로 |
| 새 배치 | 얼굴(3D) 가운데 1024 폭 · **좌 3 / 우 3 부위 카드**(각 400 폭) · 카드 ↔ 얼굴 위 점을 **지시선**으로 |
| 빠지는 것 | 화면 ① 우측 B 한눈에 보기 · C 항목별 상태 · D 시술 플랜 + A2 지금 보는 것(→ 범례 한 줄로 축소) |
| 카드 | 6개: 이마/미간 · 눈가/눈밑 · 팔자/광대 · 볼/코 주변 · 모공/피부결 · 피지/트러블. 내용 = 부위명 + 대표 측정값·등급(작게) + 시술명 칩 |
| 점 | 이 고객 메시 표면의 고정 좌표 6개 → 매 프레임 화면 투영. 뒤로 돌거나 코에 가리면 점·선을 숨긴다 |
| 모달 | 시술명 칩 클릭 → 화면 ① 안에 모달(원리·효과 시작/지속·주의할 점·받으면 안 되는 경우·시술 후 관리·시술 시간/마취). 태블릿 동기화 없음 |
| 시술 정보 원천 | Procedure Hub stg **스냅샷** `web/src/data/hub/hub-snapshot.json`(커밋). 받는 스크립트 `npm run hub:snapshot` |
| 새 패키지 | 없음. 가림 판정 raycast 가속은 drei `<Bvh>`(drei 가 이미 `three-mesh-bvh ^0.8.3` 의존, `node_modules/three-mesh-bvh` 있음) |
| 「목업」 표기 | 화면 ① 범례 줄 끝 + 모달 바닥: 「목업 · 의학적 근거 아님」 |

---

## 1. 화면 ① 새 배치

### 1-1. 와이어 (1920×1080)

```text
┌──────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ [Charty] 피부 상담      이건학 님 · 2026.10.16 측정                     ● 상담사 화면 연결됨  10:42 [⛶] │ 64  (헤더 그대로)
├───────────────────┬──────────────────────────────────────────────────────────┬───────────────────────┤
│ L1 이마/미간  [좋아요]│ C. 3D 뷰 (어두운 바탕)                         1024 × 984  │ R1 피지/트러블 [점수 없음]│
│ 미간 88.3 · 이마 92.8 │                                                           │ 피지 속 세균 흔적        │
│ [보톡스]           ○─┼──────╮                                      ╭───────────┼─○ 점수 없음 · 5,470개   │
│        (흐림)        │       ╲          ●(이마 오른쪽)  ────────────╯           │ [PDT][아그네스]        │
│                     │        ●(미간)                                           │ [케미컬필링]  (흐림)    │
├─────────────────────┤                    (3D 얼굴)                             ├───────────────────────┤
│ L2 눈가/눈밑 [관리 시작]│        ●(왼눈 밑·바깥)                                  │ R2 볼/코 주변 [관리 시작]│
│ 눈물고랑 61.4 · 눈밑   ○─┼───────╯                         ●(오른 볼 중앙) ──────────┼─○ 밝기 67 · 색소 73 …   │
│ 79.5 · 눈가 90.7      │                                                          │ [V빔][IPL][엑셀V]      │
│ [보톡스][필러]        │                                                          │ [레이저토닝][피코토닝]   │
│ [스킨부스터][기기 리프팅]│                                                          │                       │
├─────────────────────┤        ●(왼 팔자)                                          ├───────────────────────┤
│ L3 팔자/광대 [조금 신경 써요]                                ●(오른 볼 아래) ──────────┼─○ R3 모공/피부결 [관리 시작]│
│ 팔자 80.7 · 광대고랑 ○─┼───────╯                                                  │ 모공 68.8 · 피부결 82.9 │
│ 83.8                 │  ┌ 범례: 흰 점 = 넓어진 모공 ·········· 목업 · 의학적 근거 아님 ┐│ [스킨보톡스][아그네스]  │
│ [필러][바이오스티뮬레이터/│  └──────────────────────────────────────────────────────┘│ [프락셔널레이저][니들RF]│
│  콜라겐부스터]        │  [자연광][잔주름][굵은주름][모공][붉은기][색소][피지 세균]  96 │                       │
└─────────────────────┴──────────────────────────────────────────────────────────┴───────────────────────┘
   x 24…424 (400)        x 448…1472 (1024)                                          x 1496…1896 (400)
```

- 구역: 헤더 64 / 본문 1016(상하 패딩 16 · 좌우 24 · 열 간격 24). `24 + 400 + 24 + 1024 + 24 + 400 + 24 = 1920`.
- 카드 열: 세로 3장, 간격 16 → 카드 높이 `(984 − 32) / 3 ≈ 317`(flex-1). 카드 = 메디킷 `Card padding="md"`(흰 바탕·`rounded-xl`·테두리).
- 가운데 C: 지금의 `ViewerArea`(`web:src/components/screen/viewer-area.tsx:16-27`) 그대로 — 어두운 바탕 `bg-ms-gray-800`, 3D 캔버스 = 위 `1024 × 888`, 아래 필터 바 96. **A2 FocusCard 자리**(좌하 플로팅 400w, `viewer-area.tsx:22`)에는 **범례 줄**(높이 40, 필터 바 바로 위, 좌우 24 여백)만 둔다: `FILTERS[filter].legend`(+ 오버레이 색 견본, `web:src/components/screen/focus-card.tsx:27-32` 와 같은 모양) · 오른쪽 끝 「목업 · 의학적 근거 아님」. `natural` 이면 범례 글자 없이 「목업 …」만.
- 지시선 SVG: 본문 전체(1920×1016, 헤더 아래)를 덮는 `position:absolute` 한 장, `pointer-events:none`. z 순서 = 카드·C 위, 모달 아래.
- 글자 크기(구 SPEC §1-1 원칙): 카드 부위명 `text-typo-title-lg-600`(24px) · 측정 줄 `text-typo-heading-md-400`(16px, 회색) · 칩 `text-typo-title-sm-500`(18px) · 등급 배지 `GradeBadge size="screen"`.

### 1-2. 카드 열 배치 — 왜 이 순서인가

지시선이 서로 엇갈리지 않게 **열 안 순서 = 점의 화면 높이 순서**로 둔다. 화면은 마주 보는 시점(고객의 오른쪽 = 화면 왼쪽, 구 SPEC §6-4)이다.

| 칸 | 카드 | 점이 놓일 곳(정면에서 본 화면 기준) |
|---|---|---|
| L1 | 이마/미간 | 미간 한가운데(코뿌리 바로 위) |
| L2 | 눈가/눈밑 | 화면 왼쪽 눈의 눈밑 바깥쪽(눈물고랑 끝) |
| L3 | 팔자/광대 | 화면 왼쪽 팔자 주름 가운데 |
| R1 | 피지/트러블 | 이마 화면 오른쪽(T존) |
| R2 | 볼/코 주변 | 화면 오른쪽 볼 중앙(광대 앞, 콧방울 옆) |
| R3 | 모공/피부결 | 화면 오른쪽 볼 아래(입꼬리 옆 볼) |

좌표 값 자체는 WP3 찍기 도구로 정한다(§3-2). 위 표는 찍을 자리의 지시다.

### 1-3. 빠지는 것 · 남는 것 — 컴포넌트·테스트 처리 (전수)

`grep` 결과(아래 import 는 `web:src/` 전체를 셌다):

| 파일 | 지금 쓰는 곳 | 처리 |
|---|---|---|
| `components/screen/overview-section.tsx` (B) | `screen-view.tsx:10,53` 만 | **삭제** |
| `components/screen/items-section.tsx` (C) | `screen-view.tsx:9,56` 만 | **삭제** |
| `components/screen/plan-panel.tsx` (D) | `screen-view.tsx:11,59` 만 | **삭제** |
| `components/screen/focus-card.tsx` (A2) | `screen-view.tsx:8,48` 만 | **삭제**(범례 줄은 `viewer-area.tsx` 안에 새로 그린다) |
| `components/charts/radar-chart.tsx` | `overview-section.tsx:2` 만 | **삭제** |
| `components/charts/score-bars.tsx` | `items-section.tsx:2` 만 | **삭제** |
| `components/charts/face-region-map.tsx` | `focus-card.tsx:1` 만 | **삭제** |
| `components/common/use-tween.ts` | `plan-panel.tsx:4` 만 | **삭제** |
| `components/common/grade-badge.tsx` | `score-bars` · `focus-card` · `overview` · **`tablet/analysis-panel.tsx:5`** | 남김(카드에서도 씀) |
| `content/copy.ts` `summaryLine`·`GRADE_PHRASE`·`gradeSentence` | overview · focus-card · `recommend-rules.test.ts:6` · 태블릿 | 남김(태블릿·테스트가 씀). 새 문구만 덧붙임 |
| `components/screen/screen-view.tsx` | `app/(stage)/screen/page.tsx` | **다시 씀**(§1-1 배치) |
| `components/screen/viewer-area.tsx` | `screen-view.tsx` | 고침: `focusCard` prop 제거 → 범례 줄 · `FaceViewer` 에 앵커 전달 |
| `components/screen/screen-header.tsx` | `screen-view.tsx` | 그대로 |
| `components/viewer/face-viewer.tsx` · `face-canvas.tsx` | 화면 ①만(태블릿은 3D 없음, 구 SPEC §3-3) | 고침: 앵커 투영·가림 판정·찍기 도구(§3) |
| `domain/session.ts` · `sync/*` · `stores/*` | 양쪽 | **그대로.** `SessionState.cart`·`discountRate`·`screen.showPrice` 는 스냅샷에 계속 실려 오지만 화면 ①은 더 안 읽는다 |

테스트 처리:

| 테스트 | 화면 ① 의존 | 처리 |
|---|---|---|
| `e2e/sync.spec.ts:25-68` AC-5·6·7·14 | `plan-row`·`plan-total`·`plan-total-vat`·`plan-final` | 화면 ① 단언 삭제, **태블릿 단언(`tablet-total`·`tablet-total-vat`·`tablet-final`)만 남겨** 이름을 「AC-14 — 태블릿 가격 계산」으로 |
| `sync.spec.ts:70-88` AC-8·9 | `bar-pore`·`bar-fineWrinkle`·`focus-card`·`region-map` | 필터 동기화 단언은 남기고, 강조 단언을 **카드 `data-state`** 로 바꾼다(§2-4, 새 AC-9) |
| `sync.spec.ts:90-107` AC-10 | `plan-row`·`plan-discount` | 화면 ① 쪽은 **필터 + 카드 `data-state`** 로 바꾼다. 태블릿 카트 유지 단언은 그대로 |
| `sync.spec.ts:109-119` AC-11 | 없음 | 그대로 |
| `sync.spec.ts:121-132` AC-12 가격 표시 | `plan-*` 전부 | **삭제**(화면 ①에 가격이 없다. §6 정할 것 4) |
| `sync.spec.ts:134-152` AC-18 | 태블릿만 | 그대로 |
| `sync.spec.ts:154-176` AC-15·16·17 | `score-bars` 대기 | 대기 대상을 `area-cards` 로. 나머지 그대로(모달은 닫힌 상태에서 검사 — §4-4) |
| `sync.spec.ts:178-194` fix1 W-3 | `bar-*`·`cat-inflammation`·`focus-card` | 카드 `data-state` 로 바꾼다(필터를 직접 바꾸면 `focusItem` 이 풀리고 카드 강조가 새 필터를 따른다) |
| `sync.spec.ts:196-222` fix1 W-1·W-2 | 태블릿만 | 그대로 |
| `e2e/viewer.spec.ts` AC-19·20·22 | 캔버스만(`canvasRaw` 는 `<canvas>` 픽셀만 읽어 SVG 지시선이 안 섞인다, `viewer.spec.ts:25-28`) | 그대로 |
| `viewer.spec.ts:109-118` AC-23 | `screen-plan` | `screen-plan` → `area-cards`(카드 6장이 보이고 측정 없음 문구) |
| `e2e/smoke.spec.ts` | 없음 | 그대로 |
| 단위 테스트 4개(`m3d.test.ts`·`recommend-rules.test.ts`·`checklist.test.ts`·`pricing.test.ts`) | 없음 | 그대로 |
| 새 테스트 | — | 단위 `domain/areas.test.ts` · `data/hub/hub-snapshot.test.ts` · `components/viewer/anchors.test.ts`, e2e `e2e/areas.spec.ts`(§5 AC) |

### 1-4. 예외 상태

| 경우 | 표시 |
|---|---|
| 측정 JSON 없음(`useSkinReport` → `missing`) | 카드 6장은 부위명·시술명 칩만, 측정 줄 자리에 「측정 데이터가 없습니다 — npm run prepare:assets …」(`COPY.reportMissing`), 전부 흐림(측정값 없음 규칙). 칩·모달은 동작 |
| 측정 로딩 중 | 측정 줄 자리에 메디킷 `Loading`(작게). 카드 상태 = 흐림 |
| 3D 에셋 없음 | C: 지금 문구 그대로(`viewer-missing`). 점·선 없음. 카드·모달 정상 |
| 앵커 파일이 다른 메시 기준(§3-3 가드) | 점·선 없음 + `console.warn` 1회. 카드·모달 정상 |
| 3D 로딩 중 | 점·선 없음(첫 프레임 뒤부터 그린다) |

---

## 2. 부위 카드 6개

### 2-1. 확정표 — 측정값 → 부위 → Hub 고민 항목 → 시술명

`_RESUME §2-1` 초안을 Hub 에 대 보고 확정한 표다. **목업용 매핑 · 의학적 근거 아님**(파일 머리 주석에 쓴다).

| 키 | 카드 | 근거 측정값(화면 모델 → 원본) | Hub 고민 항목(`hub:taxonomy` `problem[]`) | 시술명 칩(표시 이름 → Hub 노드) |
|---|---|---|---|---|
| `forehead` | 이마/미간 | `wrinkleRegions` TT 이마 · MJ 미간 · BG 코뿌리 ← `measure:basic_241/Wrinkles_TT·MJ·BG` | P2-1 표정주름: 이마주름 · 미간주름(→M1) | **보톡스** → `M1-3-1`(보톡스 › 용도별 › 주름) |
| `eye` | 눈가/눈밑 | YD 눈밑 · YW 눈가 ← `basic_241/Wrinkles_YD·YW` · LG 눈물고랑 ← `basic_242/Wrinkles_LG` | P2-1 눈가주름(→M1) · P2-3 잔주름(→M4·M8·M9) · P4-2 필러볼륨(→M2) | **보톡스** → `M1-3-1` · **필러** → `M2` · **스킨부스터** → `M4` · **기기 리프팅** → `M9` |
| `nasolabial` | 팔자/광대 | FL 팔자 · QJ 광대고랑 ← `basic_242/Wrinkles_FL·QJ` | P2-2 깊은주름: 팔자주름(→M2·M3) | **필러** → `M2` · **바이오스티뮬레이터/콜라겐부스터** → `M3` |
| `cheek` | 볼/코 주변 | `items` redness 붉은기 ← `Red` · pigment 색소 ← `Pigment` · brightness 밝기 ← `Grayscale` | P8-1 안면홍조: V빔 · IPL홍조 · P8-2 모세혈관확장: 엑셀V · P5-1 기미: 레이저토닝 · 피코토닝 · P5-2 주근깨/잡티: IPL | **V빔** → `M8-4-1`(레이저 › 혈관 › 브이빔) · **IPL** → `M8-3-1`(레이저 › IPL › IPL) · **엑셀V** → `M8-4-2`(레이저 › 혈관 › 엑셀브이) · **레이저토닝** → `M8-1-1` · **피코토닝** → `M8-1-2` |
| `poreTexture` | 모공/피부결 | pore 모공 ← `Pore` · dermatoglyph 피부결 ← `Dermatograin` | P7-1 피지과다형: 스킨보톡스 · 아그네스 · P7-2 탄력저하형: 프락셔널레이저 · 니들RF | **스킨보톡스** → `M1-3-5`(보톡스 › 용도별 › 스킨보톡스) · **아그네스** → `auto-M11-1775364775142`(니들RF › 니들RF 장비 › 아그네스) · **프락셔널레이저** → `M8-2`(레이저 › 프락셔널, 하위 분류) · **니들RF** → `M11` |
| `sebum` | 피지/트러블 | porphyrin 피지 속 세균 흔적 ← `Porphyrin`(**이번 데이터 점수 −1**) | P6-1 급성 여드름: PDT · P6-2 피지/모공: 아그네스 · 케미컬필링 | **PDT** → `auto-M15-1775364775173`(메디컬스킨케어 › 여드름 전용 › ALA-PDT) · **아그네스** → (위와 같은 노드) · **케미컬필링** → `M15-1-1`(메디컬스킨케어 › 케미컬필링 › AHA/BHA 필링) |

초안에서 바꾼 것(근거):

| 바꾼 것 | 왜 |
|---|---|
| 칩 이름 규칙: Hub 고민 항목 이름이 **시술명**이면 그대로(V빔·엑셀V·피코토닝…), **고민명**이면(이마주름·팔자주름·잔주름·필러볼륨) 그 항목의 `modality_ref` 시술 분류명(보톡스·필러…) | P2 항목은 `name` 이 고민(「팔자주름」)이고 `detail` 에 시술(「필러/바이오스티뮬레이터」)이 있다(`hub:taxonomy` `problem[P2].subcategories`) |
| IPL홍조(P8-1) + IPL(P5-2) → 칩 **IPL** 하나 | 둘 다 같은 Hub 노드 `M8-3-1` 로 간다. 같은 모달을 두 번 보이지 않는다 |
| 눈가/눈밑에서 P2-3 의 **레이저(M8) 제외** | P2-3 은 어떤 레이저인지 말하지 않는다 → 모달이 레이저 전체 설명이 된다. 레이저 칩은 볼/코 카드에 구체 이름으로 있다 → §6 정할 것 2 |
| 볼/코에서 P5-2 **피코레이저 제외** | Hub 에 「피코레이저」 노드가 없고(가까운 것: `M8-1-3 피코슈어` 제품, 하위 분류 「피코초(Picosecond)」) 어느 쪽인지 근거가 없다. 피코토닝과 같은 피코초 계열 → §6 정할 것 3 |
| 보톡스 → `M1` 이 아니라 **`M1-3-1` 주름**, 스킨보톡스 → `M1-3-5` | Hub `M1` 아래 「용도별」 하위 분류(`M1-3`)에 용도 단위 노드가 있고 각자 `extracted` 를 갖는다. 「보톡스 전체」보다 정확하다 |
| 케미컬필링 → `M15-1-1` AHA/BHA 필링 | P6-2 케미컬필링의 `detail` 이 「AHA/BHA」 — 같은 이름의 노드가 있다 |
| PDT → `ALA-PDT` | P6-1 PDT 의 `detail` 「감광제+LED」 = ALA(광감작제) + 광선. 「PDT블루라이트」보다 일치 |

### 2-2. 카드 점수 · 등급

| 값 | 규칙 |
|---|---|
| 대표 점수 | 그 카드 근거 측정값 중 **점수가 있는 것(≥0)의 최솟값**. 측정 줄 맨 앞에 굵게(「눈물고랑 **61.4**」) |
| 등급 | 대표 점수에 구 SPEC §2-1 기준(`web:src/domain/grade.ts:5-11` `gradeOf`). 점수 있는 측정값이 하나도 없으면 `none` |
| 측정 줄 | 대표 다음에 나머지를 점수 오름차순으로 「· 이름 점수」. 이름은 `REGION_LABEL`(`web:src/content/copy.ts:24-33`)·`ITEM_COPY.label`(`copy.ts:6-15`) |
| 점수 없음(`sebum`) | 「피지 속 세균 흔적 · 점수 없음 · 5,470개」 — 개수는 `porphyrin_count` metric(`porphyrinScoreNote`, `copy.ts:56-58` 와 같은 값) |

이 고객 값(`measure.json`)으로 계산하면:

| 카드 | 대표 | 등급 | 추천 필요? |
|---|---|---|---|
| 이마/미간 | 미간 88.3 (이마 92.8 · 코뿌리 100) | good 좋아요 | 아니오 → **흐림** |
| 눈가/눈밑 | 눈물고랑 61.4 (눈밑 79.5 · 눈가 90.7) | moderate 관리 시작 | 예 |
| 팔자/광대 | 팔자 80.7 (광대고랑 83.8) | mild 조금 신경 써요 | 예 |
| 볼/코 주변 | 밝기 67 (색소 73 · 붉은기 76) | moderate 관리 시작 | 예 |
| 모공/피부결 | 모공 68.8 (피부결 82.9) | moderate 관리 시작 | 예 |
| 피지/트러블 | 점수 없음 · 5,470개 | none 점수 없음 | 아니오 → **흐림** |

### 2-3. 강조 · 흐림 규칙

- **추천 필요(`needed`)** = 등급 ∈ {mild, moderate, severe}. good(「경도 미만」)·none(측정값 없음) = 불필요.
- **관련 항목(`highlight`)** = `session.focusItem ?? FILTERS[session.filter].relatedItem` — 지금 화면 ① 강조 규칙(`web:src/components/screen/screen-view.tsx:36`)을 그대로 쓴다. 태블릿 「피부 분석」 탭에서 항목을 고르면(`focusItem`) 그 항목이 우선.
- **항목 → 카드**:

| ItemKey | 카드 |
|---|---|
| `fineWrinkle` | 이마/미간 · 눈가/눈밑 |
| `deepWrinkle` | 눈가/눈밑(눈물고랑) · 팔자/광대 |
| `pore` · `dermatoglyph` | 모공/피부결 |
| `redness` · `pigment` · `brightness` | 볼/코 주변 |
| `porphyrin` | 피지/트러블 |

- **카드 상태**(`data-state`):
  - `strong` = `needed` 이고 (`highlight == null` 이거나 카드가 `highlight` 의 카드).
  - `dim` = 그 밖 전부. 시각: 카드 전체 `opacity: .35`, 지시선·점 `opacity: .3`. **칩은 흐려도 눌린다**(모달은 연다).
- **필터 일치 표시**(`data-match="true"`): `highlight != null` 이고 카드가 그 항목의 카드면, 상태와 상관없이 카드 테두리 `ring-2 ring-primary`. 그래서 「피지 세균」 필터처럼 일치 카드가 불필요(흐림)여도 어느 카드인지 보인다.
- `[전체]` = `natural`(필터 「자연광」) + `focusItem == null` → `highlight == null` → 필요한 카드 전부 strong. 칩 글자는 「자연광」 그대로(§6 정할 것 1).
- 전환: 상태가 바뀔 때 opacity 200ms.

이 고객 값으로 필터별 결과(AC 로 그대로 확인):

| 필터 | strong | dim | match 테두리 |
|---|---|---|---|
| 자연광 | 눈가 · 팔자 · 볼/코 · 모공 | 이마 · 피지 | 없음 |
| 잔주름 | 눈가 | 나머지 5 | 이마 · 눈가 |
| 굵은 주름 | 눈가 · 팔자 | 나머지 4 | 눈가 · 팔자 |
| 모공 | 모공 | 나머지 5 | 모공 |
| 붉은기 · 색소 | 볼/코 | 나머지 5 | 볼/코 |
| 피지 세균 | 없음 | 6장 전부 | 피지 |

### 2-4. 카드 마크업 계약(e2e 가 잡는 것)

| testid / 속성 | 위치 |
|---|---|
| `area-cards` · `area-col-left` · `area-col-right` | 본문(좌·우 열 + C + 지시선)을 감싸는 요소 · 왼쪽 열 · 오른쪽 열 |
| `area-card-<key>` + `data-state="strong|dim"` + `data-match="true|false"` + `data-grade` | 카드 |
| `area-score-<key>` + `data-value`(대표 점수, 없으면 빈 문자열) | 측정 줄 대표 |
| `area-chip` + `data-hub="<노드 id>"` + `data-name="<표시 이름>"` | 시술명 칩(`<button>`, 높이 ≥ 44) |
| `leader-<key>` + `data-visible="true|false"` · 점 `leader-dot-<key>` | 지시선 SVG `<g>` |

### 2-5. 파일

| 파일 | 내용 |
|---|---|
| `src/domain/areas.ts` | `AreaKey = 'forehead'|'eye'|'nasolabial'|'cheek'|'poreTexture'|'sebum'` · `AREAS`(§2-1 표의 측정값 연결·칩 목록 키) · `AREA_LAYOUT`(§1-2 칸) · `ITEM_AREAS`(§2-3 표) · `areaCards(report, session) → AreaCardModel[]`(점수·등급·needed·state·match). **순수 함수**, React 없음. 기존 `RegionKey`(주름 부위 TT…, `web:src/domain/skin-report.ts:14`)와 이름이 겹치지 않게 `Area` 를 쓴다 |
| `src/data/hub/hub-refs.json` | 칩 목록(손으로 씀, 커밋): `{ areas: { <AreaKey>: { problems: ["P2-1", …], chips: [{ label, hubId, problemItems: ["이마주름", …] }] } } }`. 스크립트(.mjs)와 앱(TS)이 함께 읽으려고 JSON |
| `src/data/hub/hub-snapshot.json` | §4-5 스냅샷(생성물, 커밋) |
| `src/data/hub/hub.ts` | 스냅샷 타입 · `hubNode(id)` · `modalSections(id)`(§4-2 필드 상향 대체) |
| `src/components/screen/area-card.tsx` · `area-column.tsx` · `leader-lines.tsx` · `procedure-modal.tsx` | 화면 부품 |
| `src/data/face-anchors.ts` | §3 앵커 6개(찍기 도구 산출물, 커밋) |

---

## 3. 3D 앵커 — 점·지시선

### 3-1. 좌표계

- 앵커 좌표 = **`geometry.center()` 뒤의 메시 로컬 좌표**(미터). 지금 메시는 그룹 안 첫 `Mesh` geometry 를 복제해 가운데로 옮긴 뒤 원점에 그린다(`web:src/components/viewer/face-canvas.tsx:48-57,128`) → 로컬 = 월드. 메시에 transform 을 더하지 않는 한 그대로 쓴다(더하면 `mesh.localToWorld`).
- 앵커 하나 = `{ key: AreaKey, p: [x,y,z], n: [nx,ny,nz] }` — `n` 은 찍은 삼각형의 면 법선(로컬, 정규화).

### 3-2. 좌표 정하는 법 — 개발용 찍기 도구 (WP3)

계산(UV·랜드마크로 자동 산출)은 쓰지 않는다. 이 고객 메시 하나에 6점이면 손으로 찍는 쪽이 빠르고 확실하다.

- 켜는 법: `/screen?anchors=edit`. `process.env.NODE_ENV === 'production'` 이면 무시(빌드 산출물에선 안 켜진다).
- 화면: 오른쪽 카드 열 위에 편집 패널(흰 카드) — 카드 6개 라디오 · 지금 값 표 · [복사] · [초기화].
- 동작: 라디오로 카드를 고르고 얼굴을 클릭 → r3f `onPointerDown` 의 `e.point`(월드=로컬)·`e.face.normal` 을 그 카드 앵커로 저장, 점이 즉시 그 자리에 뜬다. 드래그(회전)와 클릭을 가르려고 down→up 이동 4px 이하만 찍기로 본다.
- [복사] = `src/data/face-anchors.ts` 전체 본문(아래 형식, 소수 4자리)을 클립보드로. 워커가 파일에 붙여 넣고 커밋한다.

```ts
// src/data/face-anchors.ts — 찍기 도구(/screen?anchors=edit) 산출물. 이 고객 메시 기준 고정값.
export const FACE_ANCHORS = {
  meshBytes: 21369718,           // public/m3d/manifest.json mesh.bytes — 다른 메시면 점을 안 그린다
  points: [
    { key: 'forehead', p: [0.0012, 0.0431, 0.0987], n: [0.01, 0.31, 0.95] },
    // … 6개
  ],
} as const;
```

- 찍을 자리는 §1-2 표. 찍은 뒤 정면에서 스크린샷 1장(`orchestration/work/charty-consult-recommend/screens/anchors-front.png`, 얼굴이 찍히므로 이 폴더를 `.gitignore` 에 추가 — 커밋 금지).

### 3-3. 메시 가드

- `FaceViewer` 가 이미 읽는 매니페스트(`web:src/components/viewer/face-viewer.tsx:23-25`)의 `mesh.bytes` 와 `FACE_ANCHORS.meshBytes` 가 다르면 앵커를 끈다(점·선 없음, `console.warn('[anchors] mesh mismatch …')` 1회). 판정은 순수 함수 `anchorsUsable(manifest, anchors)` 로 빼서 단위 테스트한다.

### 3-4. 매 프레임 투영

- `Canvas` 안에 `<AnchorProjector>` 를 두고 `useFrame` 에서 6점을 계산한다. **React state 를 매 프레임 바꾸지 않는다** — 지시선 SVG 요소 ref 를 모듈 단위 레지스트리(또는 `useRef` 로 넘긴 객체)에 등록해 두고, `useFrame` 안에서 `setAttribute` 로 직접 고친다(r3f 관례, `face-canvas.tsx:2` 의 eslint 예외와 같은 이유).
- 화면 좌표: `ndc = p.clone().project(camera)` → 캔버스 px `cx = (ndc.x + 1)/2 · W`, `cy = (1 − ndc.y)/2 · H`. `W·H` = `gl.domElement.offsetWidth/offsetHeight` — `<Canvas resize={{ offsetSize: true }}>`(`face-canvas.tsx:193`)라 **설계 px**(Stage scale 이 안 섞임). `getBoundingClientRect` 는 쓰지 않는다(scale 된 값).
- 본문 좌표 = 캔버스 좌표 + 캔버스 원점(본문 기준 `x 448`, `y 16`). 지시선 SVG 도 본문 기준이라 같은 좌표계.
- 카드 쪽 끝점(고정, 본문 기준): 왼쪽 카드 = `(424, 카드 top + 40)`, 오른쪽 카드 = `(1496, 카드 top + 40)` — 카드 부위명 줄 높이. 카드 top 은 레이아웃 고정이라 상수로 둔다(카드 높이가 flex 로 정해지면 마운트 때 한 번 `offsetTop` 을 읽어 고정).
- 선 모양: `점 → 무릎(끝점 x ∓ 32, 끝점 y) → 끝점` 꺾은선(`<polyline>`), 2px, `--ms-primary`. 점 = 반지름 7 흰 원 + 2px primary 테두리, 카드 쪽 끝 = 반지름 4 primary 원.

### 3-5. 가림 판정

| 단계 | 규칙 |
|---|---|
| 뒷면 | `facing = n · normalize(cameraPos − p)`. `facing ≤ 0.10` 이면 숨김, `0.10–0.30` 사이는 opacity 를 선형으로 0→1(옆으로 돌 때 부드럽게 사라짐) |
| 가려짐(코·볼에 막힘) | 카메라 → p 로 raycast(`firstHitOnly`). 첫 교차 거리 < `|cameraPos − p| − 0.002`(2mm)면 숨김. 메시는 14만 면(`Rgb.obj` `f` 140,421줄)이라 BVH 없이 매 프레임 6줄은 무겁다 → 메시를 drei `<Bvh firstHitOnly>` 로 감싼다(새 패키지 없음) |
| 화면 밖 | `|ndc.x| > 1` 또는 `|ndc.y| > 1` 이면 숨김 |
| 깜빡임 방지 | 목표 opacity 로 매 프레임 `cur += (target − cur) · 0.25` |
| 결과 | 숨김 = 점·선 opacity 0(`data-visible="false"`), **카드는 그대로**(카드 상태와 무관). 최종 opacity = 가림 opacity × (카드 strong ? 1 : 0.3) |

### 3-6. 회전 · 확대 · 리셋

- 드래그 회전·휠 확대(구 SPEC §6-4 범위)·더블클릭/[정면으로] 600ms 복귀(`face-canvas.tsx:131-168`) 모두 카메라만 움직인다 → 투영을 매 프레임 다시 하므로 점은 피부에 붙어 따라간다. 별도 처리 없음.
- 필터 전환(텍스처 교체)은 점 위치와 무관.
- 첫 프레임 전(로딩 중)·`viewer-missing`·가드 불일치 → 지시선 SVG 를 그리지 않는다.

### 3-7. e2e 훅

`window.__faceViewer`(`face-canvas.tsx:27-38`)에 덧붙인다:

```ts
anchors: () => { key: AreaKey; x: number; y: number; visible: boolean; opacity: number }[]; // 본문 기준 설계 px
anchor3d: (key: AreaKey) => [number, number, number];
```

---

## 4. 시술명 모달

### 4-1. 열기 · 닫기

| 항목 | 값 |
|---|---|
| 여는 곳 | 화면 ① 카드의 시술명 칩. **화면 ①에 뜨고 태블릿과 동기화하지 않는다**(`_RESUME §3` 기본값 채택 — 화면 ① 상태는 지금도 로컬 상태가 카메라 하나뿐이고, 모달 하나 때문에 메시지 계약 `web:src/sync/channel.ts` 를 넓히지 않는다) |
| 그리는 곳 | `screen-view` 루트 안 `absolute inset-0` 오버레이. **메디킷 `Dialog`/`Modal` 을 쓰지 않는다** — 포털이 `body` 로 나가 `Stage` 의 `transform: scale()` 밖에 뜬다(`web:src/components/stage/stage.tsx:42-53`). 틀은 메디킷 `Card` · 닫기는 `Button` |
| 크기 | 1040 × 최대 880, 가운데. 바탕 `bg-ms-black/50` |
| 닫기 | ✕ 버튼 · 바탕 클릭 · `Esc` |
| 상태 | 한 번에 하나. 태블릿 스냅샷이 와도(필터 변경 등) 열린 채 유지. 같은 칩을 다시 눌러도 같은 모달 |
| testid | `procedure-modal` + `data-hub` · 닫기 `procedure-modal-close` · 섹션 `modal-sec-<key>` |

### 4-2. 표시 항목 ↔ Hub 필드

| 섹션 키 | 화면 제목 | Hub 필드(노드 `extracted`) | 비고 |
|---|---|---|---|
| (머리) | 칩 이름 + 경로 「레이저 › 혈관 › 브이빔」 | `modality.category` › `subcategory.label` › `item.name` | |
| `overview` | (부제 1–2줄) | `overview` | |
| `mechanism` | 어떻게 작용하나요 | `mechanism` | |
| `indications` | 이런 고민에 | `indications.primary`(최대 6) | `extended` 는 안 씀 |
| `onset` | 효과는 언제부터 · 얼마나 | `onset_duration.onset` 「시작」 · `peak`·`peak_effect` 「최대」 · `duration` 「지속」 · `maintenance` 「유지」 | 키가 노드마다 다르다(확인: `M1` `peak`, `M1-3-1` `peak_effect`, `M1-3-5` `maintenance`) |
| `procedure` | 시술 시간 · 마취 | `hub:procedure-profiles` 의 그 modality 프로필 `durationMin–durationMax`분 · `needsAnesthesia` | 마취 값 6종 → `none` 마취 없음 · `topical` 바르는 마취 · `topical_or_none` 바르는 마취(필요할 때) · `topical_or_block` 바르는 마취 또는 부분 마취 · `block` 부분 마취 · `block_or_sedation` 부분 마취 또는 수면 |
| `safety` | 알아 둘 반응 | `safety.common` 「흔한 반응」 · `uncommon` 「가끔」 · `serious` 「드문 부작용」 · `long_term` 「반복 시 주의」 · `note` 「참고」 | |
| `contraindications` | 받으면 안 되는 경우 | `contraindications.absolute` 「받으면 안 돼요」 · `relative` 「상담이 필요해요」 | **item 노드엔 이 필드가 없다**(아래 상향 대체) |
| `aftercare` | 시술 후 관리 | `aftercare`(번호 목록) | |
| (바닥) | 출처 줄 | 스냅샷 `meta` | 「출처: Procedure Hub(stg) · 2026-10-26 받음 · 목업 · 의학적 근거 아님」 |

- 알 수 없는 키가 스냅샷에 생기면 조용히 버리지 않는다 — `hub-snapshot.test.ts` 가 위 표에 없는 `onset_duration`·`safety` 하위 키를 찾으면 실패한다.
- 비어 있는 섹션은 그리지 않는다.
- 글자: 본문 18px(`text-typo-title-sm-400`), 섹션 제목 20px. 2열 그리드(왼쪽 원리·이런 고민에·효과·시술 시간 / 오른쪽 반응·받으면 안 되는 경우·시술 후 관리). 넘치면 모달 안 스크롤.

### 4-3. 시술명 단위 ↔ Hub 단위 어긋남 — 처리안

`_RESUME §3` 질문(「V빔 ↔ M8 레이저 전체」)의 답: **Hub 는 modality → subcategory → item 3단이고 item 이 자기 `extracted` 를 갖는다.** V빔 = `M8-4-1 브이빔`, 엑셀V = `M8-4-2`, IPL = `M8-3-1`, 레이저토닝 = `M8-1-1`, 피코토닝 = `M8-1-2`, 아그네스 = `auto-M11-…142`, 스킨보톡스 = `M1-3-5` 처럼 **시술명 단위 노드가 있다.** 단 item `extracted` 에는 `contraindications`·`related_techniques` 가 없다(8개 item 확인). subcategory 에는 `extracted` 가 없다.

→ **필드 단위 상향 대체**: 섹션마다 `item → (subcategory 는 건너뜀) → modality` 순으로 그 필드가 있는 가장 구체적인 노드를 쓴다. 상위에서 가져온 섹션은 제목 옆에 작게 「레이저 전체 기준」(= modality `category` + 「 전체 기준」).

| 칩 | 노드 단위 | 상위에서 오는 섹션 |
|---|---|---|
| V빔 · IPL · 엑셀V · 레이저토닝 · 피코토닝 | item | 받으면 안 되는 경우 → 레이저(M8) |
| 보톡스(눈가·이마) · 스킨보톡스 | item | 받으면 안 되는 경우 → 보톡스(M1) |
| 아그네스 | item | 받으면 안 되는 경우 → 니들RF(M11) |
| PDT · 케미컬필링 | item | 받으면 안 되는 경우 → 메디컬스킨케어(M15) |
| 프락셔널레이저 | subcategory `M8-2` | **전부** 레이저(M8) — 머리 경로는 「레이저 › 프락셔널」, 모든 섹션에 「레이저 전체 기준」 |
| 필러 · 스킨부스터 · 기기 리프팅 · 바이오스티뮬레이터/콜라겐부스터 · 니들RF | modality | 없음(그 자체가 modality) |
| (시술 시간 · 마취) | 언제나 modality(`procedure-profiles` 가 modality 단위 17개) | 칩이 item 이면 「레이저 전체 기준」 |

### 4-4. 원문 그대로 · 금지어

Hub 원문을 고쳐 쓰지 않는다(실제 API 값만, 요약·바꿔 쓰기 없음). 선택한 노드 원문에 「치료」「질환」「환자」가 들어 있다(예: `M8-4-1` overview 「혈관 병변과 색소 질환 치료를 위한…」, `M1` contraindications 「… 환자」). 구 SPEC AC-17(화면 ① 금지어 0건)은 **모달이 닫힌 화면 ①**(우리 문구)에만 적용하고, 모달은 바닥 출처 줄로 「Hub 원문」임을 밝힌다 → §6 정할 것 5. 한자는 선택 노드 원문에 0건(확인) — 모달도 한자 0건을 AC 로 건다.

### 4-5. Hub 스냅샷

| 항목 | 값 |
|---|---|
| 받는 범위 | `hub:taxonomy` 에서 `hub-refs.json` 이 가리키는 노드(서로 다른 16개: item 10 · subcategory 1(`M8-2`) · modality 5(M2·M3·M4·M9·M11)) **+ 그 노드들이 속한 modality 의 `extracted`·`category`**(상향 대체용: M1·M2·M3·M4·M8·M9·M11·M15) **+ 고민 항목 이름 확인용 `problem[]` 중 `hub-refs` 의 P 항목** · `hub:procedure-profiles` 에서 같은 modality 프로필 8개. 그 밖(제품·패키지·시술 간 금기 매트릭스·`products`)은 받지 않는다(카드는 조합·가격·제품 X) |
| 파일 | `web/src/data/hub/hub-snapshot.json`(**커밋** — Hub 시술 설명은 개인정보가 아니고, 구 SPEC 도 같은 출처의 `taxonomy-subset.json` 을 커밋했다). 예상 30–50KB |
| 형식 | `{ meta, modalities: { M8: { category, extracted, profile } }, nodes: { "M8-4-1": { level: "item", modalityId: "M8", path: ["레이저","혈관","브이빔"], extracted } , "M8-2": { level: "subcategory", modalityId: "M8", path: ["레이저","프락셔널"], extracted: null } }, problems: { "P8-1": { label: "안면홍조", items: ["V빔","IPL홍조","리쥬란+LDM"] } } }` |
| `meta` | `{ source: "https://stg-procedure-hub.medisolveai.com", endpoints: ["/api/taxonomy","/api/procedure-profiles"], fetchedAt: ISO, versions: { taxonomy: null, procedureProfiles: "3.3 (2026-07-26)" }, sha256: { taxonomy, procedureProfiles } }` — taxonomy 응답엔 version 필드가 없어 `null` + 응답 해시로 판본을 남긴다. 2026-10-26 확인값: procedure-profiles `version 3.3 · updated 2026-07-26`, taxonomy sha256 `7e92abcd…68f6`(받을 때마다 바뀔 수 있다) |
| 스크립트 | `web/scripts/fetch-hub.mjs`, `npm run hub:snapshot`. Node 내장 `fetch` 만(의존 0). ① 두 엔드포인트 GET ② `hub-refs.json` 의 `hubId` 마다 노드를 찾는다 — **하나라도 없으면 같은 이름 후보를 출력하고 종료 코드 1**(Hub 의 `auto-…` id 가 바뀌는 경우 대비) ③ 위 형식으로 쓰고 요약(노드 수·바이트·해시) 출력. 두 번 돌려 Hub 가 그대로면 `fetchedAt` 외 같은 결과 |
| 앱 | `import snapshot from '@/data/hub/hub-snapshot.json'` 정적 import. **실행 중 네트워크 요청 0**(시연 중 stg 의존 X) |
| 출처 표기 | 모달 바닥 출처 줄(§4-2). `fetchedAt` 날짜를 `YYYY-MM-DD` 로 |

---

## 5. 기존 추천과의 관계 — 공존

| 대상 | 이번 처리 | 이유 |
|---|---|---|
| `src/data/recommend-rules.ts` · `recommend-rules.test.ts` | **그대로**(공존) | 태블릿 추천 패널·「추천」 보기 행(`web:src/components/tablet/tablet-view.tsx:5`)이 쓴다. 태블릿은 이번에 안 바꾼다 |
| `src/data/mock/taxonomy-subset.json` | **그대로** | 같은 이유. 출처가 차티 stg 사본(구 SPEC §3-5)이라 새 스냅샷과 값이 다를 수 있다 → §6 정할 것 6 |
| `RecommendationPanel`(태블릿 추천 260) | 그대로 | |
| 새 카드 규칙(`domain/areas.ts`) | 별도 | 추천 규칙은 「항목 → modality 칩」, 카드는 「부위 → 시술명 노드」. 서로 import 하지 않는다. 둘 다 머리 주석 「목업용 · 의학적 근거 아님」 |

---

## 6. 정할 것 (planner 가 못 정한 것 — 기본값으로 진행 가능)

| # | 항목 | 왜 못 정했나 | 기본값 |
|---|---|---|---|
| 1 | 필터 칩 「자연광」을 「전체」로 바꿀까 | `_RESUME §2` 는 「[전체]」라 썼지만 필터 정의(`web:src/domain/filters.ts:17`)를 태블릿과 같이 쓴다. 이름을 바꾸면 태블릿 화면이 바뀐다 | **「자연광」 그대로**, 카드 규칙상 자연광 = 전체 |
| 2 | 눈가/눈밑에 P2-3 잔주름의 레이저(M8) 칩 | Hub 가 어떤 레이저인지 말하지 않아 모달이 「레이저 전체」가 된다 | **넣지 않는다**(보톡스·필러·스킨부스터·기기 리프팅 4개) |
| 3 | 볼/코에 P5-2 피코레이저 칩 | Hub 에 같은 이름 노드가 없고 후보(피코슈어 제품 / 「피코초」 하위 분류)를 고를 근거가 없다 | **넣지 않는다**(피코토닝으로 갈음) |
| 4 | 태블릿 「가격 표시」 토글 | 화면 ①에서 가격(D)이 빠져 토글이 아무 일도 안 한다. 태블릿은 안 바꾸는 범위 | **그대로 둔다**(동작 없는 토글). 다음 판에 태블릿 정리 때 뺀다 |
| 5 | 모달의 Hub 원문 속 「치료·질환·환자」 | 고쳐 쓰면 원문이 아니고, 두면 구 SPEC 금지어 원칙(AC-17)과 부딪힌다 | **원문 그대로 + 출처 줄**, 금지어 검사는 모달 닫힌 화면에만 |
| 6 | 태블릿 추천 설명(`taxonomy-subset.json`, 차티 사본)과 새 Hub 스냅샷이 둘 | 태블릿을 이번에 안 바꾸는 범위 | **공존**. 태블릿 정리 때 스냅샷 하나로 합친다 |
| 7 | 앵커 점 자리(§1-2) | 피부과 관점의 「대표 위치」는 판단 영역 | **§1-2 표대로**, 정면 스크린샷을 사용자 확인에 올린다 |

---

## 7. WP 분할 (frontend 워커 1명 · 순서대로)

각 WP 끝에 **그 WP 관련 시험만** 돌리고, 전체(`npm run verify`)는 WP6 에서 한 번. 사용자 dev 서버(3417)는 끄거나 재시작하지 않는다 — `playwright.config.ts` 가 `reuseExistingServer: true` 로 3417 을 그대로 쓴다. Next 16 dev 산출물은 `.next/dev` 로 분리돼 있어 `next build` 와 같이 돌 수 있다(확인: `web/.next/dev` 만 존재). 충돌하면 서버를 끄지 말고 코디에게 escalation.

| WP | 내용 | 완료 조건 |
|---|---|---|
| **WP1 Hub 스냅샷 · 카드 도메인** | `hub-refs.json`(§2-1) · `scripts/fetch-hub.mjs` · `npm run hub:snapshot` 1회 실행 → `hub-snapshot.json` · `data/hub/hub.ts`(`modalSections` 상향 대체) · `domain/areas.ts`(§2-2·2-3) · 단위 테스트 `areas.test.ts`·`hub-snapshot.test.ts` | `npm run test` 통과: AC-1~AC-6 · 스크립트를 존재하지 않는 `hubId` 로 돌리면 종료 코드 1 + 후보 출력 · 두 번 돌려 `fetchedAt` 외 diff 없음 |
| **WP2 화면 ① 배치 · 카드** | §1-1 배치 · `area-card`·`area-column` · 범례 줄 · §1-3 삭제 8파일 · e2e 고침(§1-3 표) | `npm run lint`·`test` 통과 · `e2e/sync.spec.ts`·`viewer.spec.ts` 의 고친 시험 통과 · AC-7~AC-11 · 1920×1080 스크린샷(자연광) 1장 |
| **WP3 앵커 찍기** | 찍기 도구(§3-2) · `face-anchors.ts` 6점 · 메시 가드(§3-3) · `anchors.test.ts` | 도구로 6점을 찍어 파일에 커밋 · 정면 스크린샷 `screens/anchors-front.png` · AC-15 단위 테스트 통과 · 프로덕션 빌드에서 `?anchors=edit` 가 안 켜짐 |
| **WP4 투영 · 지시선 · 가림** | `<AnchorProjector>` · `<Bvh>` · `leader-lines` · `__faceViewer.anchors/anchor3d` | AC-12~AC-14 · AC-16 · 회전 중 프레임 저하 없음(드래그하며 눈 확인 — DevTools Performance 에서 프레임 16ms 안팎) |
| **WP5 모달** | `procedure-modal`(§4) · 칩 연결 | AC-17~AC-21 · 모달 스크린샷 2장(V빔 · 프락셔널레이저 — 상향 대체 표기 확인) |
| **WP6 검증** | `e2e/areas.spec.ts` 정리 · `npm run verify`(lint + test + build + e2e) · AC 확인 표 · 스크린샷(자연광 · 모공 필터 · 30° 회전 · 모달)을 `orchestration/work/charty-consult-recommend/screens/` 에(gitignore) | `npm run verify` 통과 · §8 AC 전부 확인 표(번호 · 방법 · 결과) |

---

## 8. 수용 기준 (AC)

데이터 · 규칙(단위 테스트)

1. 이 고객 `measure.json` 으로 `areaCards` 를 돌리면 대표 점수·등급이 §2-2 표와 같다: 이마/미간 88.3 good · 눈가/눈밑 61.4 moderate · 팔자/광대 80.7 mild · 볼/코 67 moderate · 모공/피부결 68.8 moderate · 피지/트러블 `null` none(측정 JSON 없으면 skip — 기존 `recommend-rules.test.ts:13` 과 같은 방식). 손으로 만든 픽스처(`__fixtures__/measure.sample.json`)로도 같은 규칙(최솟값·−1 제외)이 돈다.
2. 필터 7개 × `focusItem=null` 에서 카드 `state`·`match` 가 §2-3 마지막 표와 칸마다 같다.
3. `focusItem='dermatoglyph'`(필터 무관)이면 모공/피부결만 strong, `focusItem='brightness'` 면 볼/코만 strong.
4. `hub-refs.json` 의 모든 `hubId` 가 `hub-snapshot.json` `nodes` 에 있고, 각 노드의 `modalityId` 가 `modalities` 에 있으며 `modalities[*].profile` 이 8개 모두 있다.
5. `modalSections('M8-4-1')` 의 `contraindications` 출처가 `M8`(상향), `mechanism` 출처가 `M8-4-1`. `modalSections('M8-2')` 는 모든 섹션 출처가 `M8`.
6. 스냅샷에 §4-2 표에 없는 `onset_duration`·`safety` 하위 키가 없다. 스냅샷 전체 문자열에 한자(`/[一-鿿]/`) 0건. `meta.fetchedAt`·`meta.sha256.taxonomy` 가 있다.

화면 · 카드(e2e, `/tablet` + `/screen` 두 탭)

7. 화면 ①에 카드 6장(`area-card-*`)이 §1-2 칸(L1–L3·R1–R3) 순서로 보이고, B·C·D 의 testid(`screen-overview`·`screen-items`·`screen-plan`·`focus-card`·`score-bars`)가 0개다.
8. 자연광(초기)에서 strong = 눈가·팔자·볼/코·모공, dim = 이마·피지. 각 카드에 부위명·대표 점수(`area-score-*` `data-value` = 61.4·80.7·67·68.8·88.3·빈 값)·등급 배지가 보이고, 피지 카드에 「점수 없음」과 「5,470개」가 보인다.
9. 태블릿에서 「모공」 필터를 누르면 1초 안에 화면 ①에서 **모공/피부결 카드만** `data-state="strong"` 이고 나머지 5장은 `dim`. 화면 ①에서 「피지 세균」을 누르면 6장 모두 `dim`, 피지 카드만 `data-match="true"`.
10. 태블릿 「피부 분석」에서 「피부결」 항목을 누르면 1초 안에 모공/피부결 카드만 strong. 그 뒤 화면 ①에서 「붉은기」 필터를 누르면 볼/코 카드만 strong(필터 직접 변경 시 `focusItem` 해제 — 기존 동작).
11. 화면 ① 탭을 새로고침하면 1초 안에 태블릿과 같은 필터·카드 상태로 돌아온다. 태블릿 카트(태블릿 화면)는 새로고침 뒤에도 남는다.

3D 앵커 · 지시선

12. 정면(초기)에서 점 6개가 모두 `data-visible="true"` 이고, 각 점의 화면 좌표(`__faceViewer.anchors()`)가 C 구역(본문 x 448–1472, y 16–904) 안이며, 지시선 6개가 서로 교차하지 않는다(e2e 가 선분 교차를 계산해 0건).
13. **얼굴을 돌리면 점이 피부에 붙어 이동한다**: 드래그로 약 30° 돌린 뒤, ① 각 visible 점의 좌표가 정면 때보다 10px 이상 움직였고 ② `leader-dot-<key>` 의 SVG `cx/cy` 가 `__faceViewer.project(anchor3d)` 를 본문 좌표로 바꾼 값과 1px 안에서 같다(점이 투영과 어긋나지 않음). 눈 확인 스크린샷에서 점이 찍은 자리(§1-2)에 붙어 있다.
14. 좌우 끝(±75°)까지 돌리면 먼 쪽 볼의 점(왼쪽 끝이면 R2·R3 쪽, 오른쪽 끝이면 L2·L3 쪽) 중 적어도 1개가 `data-visible="false"` 가 되고 그 지시선 opacity 가 0.05 미만이다. 이때 카드 6장은 그대로 보인다. 더블클릭으로 정면에 돌아오면 3초 안에 6개 모두 다시 visible.
15. `anchorsUsable` 은 매니페스트 `mesh.bytes` 가 `FACE_ANCHORS.meshBytes` 와 다르면 `false`(단위 테스트). e2e 에서 `**/m3d/manifest.json` 응답의 `mesh.bytes` 를 바꿔 끼우면 지시선 SVG 가 0개이고 카드 6장과 3D 는 정상이다.
16. dim 카드의 점·선 opacity 는 0.3 이하, strong 카드는 visible 일 때 0.9 이상이다.

모달

17. 「눈가/눈밑」 카드의 **보톡스** 칩을 누르면 화면 ① 안에 `procedure-modal`(`data-hub="M1-3-1"`)이 뜨고 「어떻게 작용하나요」(mechanism)·「알아 둘 반응」(safety)·「받으면 안 되는 경우」(contraindications, 옆에 「보톡스 전체 기준」)·「효과는 언제부터 · 얼마나」·「시술 시간 · 마취」(「10–15분」·「마취 없음」, 옆에 「보톡스 전체 기준」)가 보인다. 태블릿 화면은 아무것도 바뀌지 않는다.
18. 「볼/코 주변」의 **V빔** 칩 모달은 머리 경로 「레이저 › 혈관 › 브이빔」, 원리 섹션 본문이 `M8-4-1` 의 `mechanism` 과 같고, 「받으면 안 되는 경우」 옆에 「레이저 전체 기준」이 있다.
19. 「모공/피부결」의 **프락셔널레이저** 칩 모달은 머리 경로 「레이저 › 프락셔널」이고 보이는 모든 섹션 옆에 「레이저 전체 기준」이 있다.
20. 모달은 ✕ · 바탕 클릭 · `Esc` 로 닫힌다. 모달이 열린 채 태블릿에서 필터를 바꾸면 모달은 그대로 열려 있고 뒤의 카드 상태만 바뀐다. 모달 바닥에 「Procedure Hub(stg) · <받은 날짜> 받음 · 목업 · 의학적 근거 아님」이 보인다.
21. 모달이 열린 상태에서 페이지 네트워크 요청 중 `procedure-hub` 호스트로 가는 것이 0건이다(스냅샷만 읽음). 칩 19개(서로 다른 노드 16개 — 아그네스·보톡스·필러가 두 카드에 겹침)를 차례로 열어 모두 모달이 뜨고 한자가 0건이다.

회귀 · 범위

22. 태블릿 시험(AC-14 태블릿 가격 · AC-11 · AC-18 · fix1 W-1·W-2)이 고치지 않은 채 통과하고, `git diff --stat` 에 `src/components/tablet/`·`src/stores/`·`src/sync/`·`src/data/recommend-rules.ts`·`src/data/mock/` 아래 변경이 0줄이다.
23. 모달이 닫힌 화면 ①(필터 7개 각각)에 한자·「−1」·「진단·질환·치료·환자」·좌/우 표기가 없다(기존 AC-15·17 검사 그대로, 대기 대상만 `area-cards`).
24. `viewer.spec.ts` AC-19·20·22 가 고치지 않은 채 통과한다(지시선은 캔버스 픽셀에 안 섞인다).
25. `npm run build` 가 `public/m3d/` 없이 통과하고(구 AC-1), `git status --porcelain` 에 `public/m3d/`·`screens/` 아래 경로가 없다.

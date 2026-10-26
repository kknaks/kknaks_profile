# SPEC 검수 리포트 — charty-consult-recommend

- 검수: reviewer 워커(read-only) · 2026-10-26 · 대상 `SPEC.md`(446줄)
- 대조 기준: `_RESUME.md` §2 · 코드 `reference/2026-10-21-charty-poc/web/`(HEAD cecef3e) · `public/m3d/report/measure.json` · Hub stg `/api/taxonomy`·`/api/procedure-profiles`(2026-10-26 14:12 curl)

## 판정: **WARN** — 막는 결함(FAIL) 0 · 보완 권고 13

인용한 사실(측정 점수, Hub 노드 id·필드, 코드 줄 번호)은 **전부 실물과 맞는다**. 다만 아래 W-1~W-3은 frontend 발주 전에 SPEC에 한 줄씩 넣는 것을 권한다. 넣지 않으면 기존 e2e 1건이 깨지거나, 사용자가 정하지 않은 범위가 바뀐다. W-4 이하는 워커가 막히거나 같은 문장을 다르게 읽을 수 있는 자리다.

---

## 1. `_RESUME §2` 결정과의 일치

| 결정 | SPEC | 판정 |
|---|---|---|
| 얼굴 가운데 · 좌우 카드 · 지시선 · 점 | §0·§1-1(좌 3 / 우 3, 각 400 · 가운데 1024) · §3 | ✓ |
| 점 = 메시 고정 좌표 → 매 프레임 투영 · 가려지면 숨김/흐림 | §3-1·3-4·3-5 | ✓ |
| 카드 단위 = 부위 6개 | §2-1 키 6개 | ✓ |
| 카드 = 부위명 + 시술명만, 패키지·가격 X, 점수·등급은 작게 | §1-1 글자 크기(측정 줄 16px) · §2-4 · §4-5(제품·패키지 안 받음) | ✓ |
| 필터: 전체 = 모두 진하게 / 필터 = 해당 부위 강조 · 나머지 흐림 | §2-3 | ✓. 단 칩 이름은 「자연광」을 그대로 쓴다(§6-1 기본값, 일괄 승인 범위) |
| 추천이 필요 없는 부위는 흐림 | §2-3 `needed` | ✓ |
| 사진 없음 | 카드에 이미지 없음 | ✓ |
| 우측 패널 3개(B·C·D)는 큰 화면에서 빼고 태블릿에는 유지 | §1-3 · §0 「태블릿 안 바꿈」 · AC-22 | ✓ |
| 시술명 → 모달(Hub `extracted`) | §4 | ✓ |
| Hub 스냅샷(시연 중 stg 의존 X) | §4-5 · AC-21 | ✓ |
| 목업 · 의학적 근거 아님 표기 | §0 · §4-2 바닥 줄 | ✓ |
| **(결정 밖) A2 「지금 보는 것」 카드도 제거** | §0 · §1-3 `focus-card.tsx` 삭제 | **W-2** |

## 2. 인용 사실 실물 대조

### 2-1. measure.json 점수(§2-2 · AC-1 · AC-8) — 전부 일치

`python3`로 `features[].measures[]`를 덤프한 결과:

| 카드 | 원본 | SPEC |
|---|---|---|
| 이마/미간 | Wrinkles_MJ 88.3 · TT 92.8 · BG 100 | 88.3 good ✓ |
| 눈가/눈밑 | Wrinkles_LG 61.4 · YD 79.5 · YW 90.7 | 61.4 moderate ✓ |
| 팔자/광대 | Wrinkles_FL 80.7 · QJ 83.8 | 80.7 mild ✓ |
| 볼/코 | Grayscale 67 · Pigment 73 · Red 76 | 67 moderate ✓ |
| 모공/피부결 | Pore 68.8 · Dermatograin 82.9 | 68.8 moderate ✓ |
| 피지/트러블 | Porphyrin score −1 · porphyrin_count 5470 | null none · 5,470개 ✓ |

- 등급은 `src/domain/grade.ts:5-11` `gradeOf`로 다시 계산했다(≥85 good · ≥70 mild · ≥60 moderate) → §2-2 표와 같다.
- §2-3 필터별 strong/dim/match 표 7줄은 `ITEM_AREAS` 규칙과 위 등급으로 손으로 다시 계산했고, 칸마다 일치한다. AC-3(dermatoglyph → 모공만, brightness → 볼/코만)도 맞다.

### 2-2. Hub 노드 · 필드 — 전부 일치

- `tax.json`의 sha256은 `7e92abcd81b3…ee68f6`이고, SPEC §4-5에 적힌 값과 같다(Hub가 그 사이 바뀌지 않았다).
- `procedure-profiles`의 버전은 `3.3`, 갱신일은 `2026-07-26`이고, 프로필은 17개다 ✓.

| 노드 | 수준 | 경로(실물) | `extracted` 키 | contra |
|---|---|---|---|---|
| M1-3-1 | item | 보톡스 › 용도별 › 주름 | onset_duration{onset,peak_effect,duration} · safety{common,serious,long_term} | 없음 ✓ |
| M1-3-5 | item | 보톡스 › 용도별 › 스킨보톡스 | onset{onset,maintenance,duration} · safety{common} | 없음 ✓ |
| M8-4-1 | item | 레이저 › 혈관 › 브이빔 | onset{onset,duration} | 없음 ✓ |
| M8-4-2 | item | 레이저 › 혈관 › 엑셀브이 | 〃 | 없음 ✓ |
| M8-3-1 | item | 레이저 › IPL › IPL | 〃 | 없음 ✓ |
| M8-1-1 / M8-1-2 | item | 레이저 › 색소/토닝 › 레이저토닝 / 피코토닝 | 〃 | 없음 ✓ |
| auto-M11-1775364775142 | item | 니들RF › 니들RF 장비 › 아그네스 | 〃 | 없음 ✓ |
| auto-M15-1775364775173 | item | 메디컬스킨케어 › 여드름 전용 › ALA-PDT | 〃 | 없음 ✓ |
| M15-1-1 | item | 메디컬스킨케어 › 케미컬필링 › AHA/BHA 필링 | 〃 | 없음 ✓ |
| M8-2 | subcategory | 레이저 › 프락셔널 | **`extracted` 키 자체가 없음** ✓ | — |
| M2·M3·M4·M9·M11 | modality | — | 8키 전부(onset{onset,peak,duration} · safety{common,uncommon,serious}) | absolute·relative ✓ |
| 상향 대상 M1·M8·M15 | modality | — | 위와 같음 | ✓ |

- **노드 수:** 서로 다른 노드는 16개(item 10 · subcategory 1 · modality 5)이고, 칩은 19개다(보톡스·필러·아그네스가 두 번 나온다). SPEC §4-5와 AC-21의 수와 같다 ✓.
- **onset·safety 하위 키:** 선택한 노드의 하위 키를 모두 모으면 onset 쪽은 {onset, peak, peak_effect, duration, maintenance}, safety 쪽은 {common, uncommon, serious, long_term}이다. 둘 다 §4-2 표 안에 들어간다. 따라서 AC-6은 그대로 통과할 수 있다.
- **한자:** 선택한 item·modality의 `extracted` 전체(`related_techniques`, `indications.extended` 포함), problem 14개, 프로필 8개 어디에도 **0건**이다 ✓(AC-6, AC-21).
- **금지어:** 원문 속 「치료·질환·환자」는 M2·M4·M8-4-1 등 여러 노드에 있다. SPEC §4-4의 판단(모달은 원문 그대로 둔다)이 맞다.
- **프로필:** M1은 10–15분·none이다 → AC-17의 「10–15분 · 마취 없음」과 맞다 ✓. 마취 값은 6종이고, §4-2의 6종과 같다 ✓.
- **problem 항목:** P2-1 표정주름{이마·미간·눈가주름 → M1} · P2-2 팔자주름{M2,M3} · P2-3 잔주름{M4,M8,M9} · P4-2 필러볼륨{M2} · P5-1 레이저토닝·피코토닝 · P5-2 피코레이저·IPL · P6-1 PDT{감광제+LED} · P6-2 아그네스·케미컬필링{AHA/BHA} · P7-1 스킨보톡스·아그네스 · P7-2 프락셔널레이저·니들RF · P8-1 V빔·IPL홍조 · P8-2 엑셀V. §2-1 표와 「바꾼 것」 근거가 실물과 같다 ✓.
- **스냅샷 크기:** 선택한 노드의 `extracted`만 약 39KB, 프로필 8개가 약 6.5KB다. 압축 JSON이면 46KB 안팎으로 SPEC 예상(30–50KB)에 들어간다. 들여쓰기를 해서 저장하면 60KB 안팎이 될 수 있다(문제는 아니다).

### 2-3. 코드 인용 — 전부 일치

| SPEC 인용 | 실물 |
|---|---|
| `viewer-area.tsx:16-27`, `:22` A2 자리 | ✓ (22행 `absolute bottom-[112px] left-6 w-[400px]`) |
| `focus-card.tsx:27-32` 범례 견본 | ✓ |
| `screen-view.tsx:36` highlight 규칙 | ✓ |
| `face-canvas.tsx:48-57,128` geometry.center · `<mesh>` | ✓ |
| `face-canvas.tsx:27-38` `__faceViewer` · `:131-168` Controls · `:193` `resize={{offsetSize:true}}` · `:2` eslint 예외 | ✓ |
| `face-viewer.tsx:23-25` 매니페스트 로드 | ✓, `manifest.json mesh.bytes = 21369718` ✓ |
| `copy.ts:6-15` · `:24-33` · `:56-58` | ✓ |
| `grade.ts:5-11` · `filters.ts:17` · `skin-report.ts:14` | ✓ |
| `stage.tsx:42-53` transform scale | ✓ |
| `tablet-view.tsx:5` recommend import · `recommend-rules.test.ts:13` skipIf | ✓ |
| `Rgb.obj` 면 140,421 | `grep -c '^f '` = 140421 ✓ |
| drei `<Bvh>` · `three-mesh-bvh ^0.8.3` | `node_modules/@react-three/drei/core/Bvh.js` 있음 · bvh 0.8.3 ✓ |
| `.next/dev`만 있음 · `reuseExistingServer: true` | ✓ (`playwright.config.ts`) |
| 배치 산수 | 헤더 `h-16` = 64 ✓ · 24+400+24+1024+24+400+24 = 1920 ✓ · 본문 1016 − 32 = 984 ✓ |
| tsconfig `resolveJsonModule` (정적 JSON import) | `tsconfig.json:16` true ✓ |
| `screens/` gitignore | 아직 없다(`git check-ignore` 결과 없음). SPEC이 「추가」라고 쓴 대로 WP3에서 넣어야 한다 ✓ |

## 3. §1-3 「빠지는 것」 전수조사

빠지는 8개 파일의 import와 testid를 `src/`·`e2e/` 전체에서 grep으로 셌다.

| 대상 | grep으로 찾은 사용처 | SPEC 표 |
|---|---|---|
| overview-section / items-section / plan-panel / focus-card | `screen-view.tsx:8-11, 48,53,56,59`만 | ✓ |
| radar-chart / score-bars / face-region-map / use-tween | overview / items / focus-card / plan-panel 각 1곳만 | ✓ |
| grade-badge | score-bars · overview · focus-card · **tablet/analysis-panel.tsx:5** | ✓ 남김 |
| testid `focus-card` | `sync.spec.ts:83, 187` | ✓ |
| `score-bars` | `sync.spec.ts:156` | ✓ |
| `bar-*` | `sync.spec.ts:74,81,181,184,185,192,193` | ✓ |
| `region-map` | `sync.spec.ts:84` | ✓ |
| `cat-inflammation` | `sync.spec.ts:186` | ✓ (W-3 행) |
| `plan-row`/`plan-row-price`/`plan-total*`/`plan-final` | `sync.spec.ts:23,33,40,41,47,49,52,57,61,67` | ✓ |
| `plan-discount` | `sync.spec.ts:100` | ✓ |
| `plan-empty`/`plan-totals`/`plan-price-hidden` | `sync.spec.ts:123,126,128,129,131` (AC-12 삭제) | ✓ |
| `screen-plan` | `viewer.spec.ts:115` | ✓ |
| **`report-missing`** (`screen-view.tsx:26` `ReportPlaceholder`, 다시 쓰면서 사라짐) | **`viewer.spec.ts:116`** | **누락 → W-1** |
| `summaryLine`·`GRADE_PHRASE`·`gradeSentence` | summaryLine은 `recommend-rules.test.ts:6`, GRADE_PHRASE는 `copy.ts` 안(`porphyrinScoreNote` → 어댑터), gradeSentence는 **focus-card 한 곳뿐**. 태블릿에서 직접 쓰는 곳은 0이다 | 처리(남김)는 맞지만 근거 칸의 「태블릿」은 틀렸다 → W-9 |
| `summary-line`·`tone-chip`·`radar*`·`cat-*`(screen) testid | e2e에서는 `cat-inflammation`만 쓴다 | ✓ |

## 4. 권고(WARN) — 고칠 내용

| # | 자리 | 무엇이 문제인가 | 고칠 내용 |
|---|---|---|---|
| **W-1** | §1-3 테스트 표 AC-23 행 · §1-4 | `viewer.spec.ts:116`이 `report-missing`(`.first()`)에 「prepare:assets」가 있는지 검사한다. 이 testid는 지울 `ReportPlaceholder` 안에 있다. SPEC은 `screen-plan → area-cards`만 적었으므로, 그대로 구현하면 AC-23이 깨진다 | §1-4 「측정 JSON 없음」 행에 「측정 줄 요소에 `data-testid="report-missing"` 유지」를 덧붙인다. 또는 AC-23 행에 「`report-missing` → `area-card-*` 측정 줄 문구로 바꾼다」를 명시한다 |
| **W-2** | §0 「빠지는 것」 · §1-3 `focus-card.tsx` 삭제 | `_RESUME §2`가 뺀 것은 「우측 패널 3개」뿐이다. A2(지금 보는 것 — 항목 설명·지표·부위 지도)를 빼고 범례 한 줄로 줄이는 것은 결정 밖이고, §6 「정할 것」에도 없다. 그래서 일괄 승인 범위에 들었다고 볼 근거가 약하다 | 코디가 사용자에게 한 줄로 확인한다(A2를 뺄지). 유지한다면, 지시선이 왼쪽 아래 400×≈200 구역을 지나므로 A2를 가운데 아래로 옮겨야 한다. SPEC §6에 8번으로 올려 두는 것을 권한다 |
| **W-3** | §8 AC 번호 | 새 AC-1~25가 기존 테스트 이름(구 AC-5·6·7·14, AC-8·9, AC-15·16·17, AC-19·20·22, AC-23)과 번호가 겹친다. §1-3의 「새 AC-9」, §8 AC-22의 「AC-14 태블릿 가격」, AC-23의 「기존 AC-15·17」처럼 한 문서 안에서 두 번호 체계가 섞여 있다 | 새 AC에 접두어를 붙인다(예: `R-1`~`R-25`). 구 테스트는 「구 AC-n」으로 부른다. 새 e2e 이름도 접두어로 쓴다 |
| W-4 | WP3 찍기 | 워커는 터미널 에이전트라 얼굴을 눈으로 보며 클릭하기 어렵다. 정면 스크린샷을 보고 Playwright 좌표로 클릭할 수는 있지만, 방법이 적혀 있지 않다 | 찍기 도구에 e2e/스크립트용 훅을 더한다. 예: `__faceViewer.pickAt(cx, cy)` — 캔버스 px를 raycast해서 `{p, n}`을 반환한다. 워커는 정면 스크린샷 → 좌표 지정 → `pickAt` → 결과 스크린샷 확인 순서로 진행한다. 사람 확인(§6-7)은 지금처럼 스크린샷으로 한다 |
| W-5 | WP3 완료 조건 「프로덕션 빌드에서 `?anchors=edit`가 안 켜짐」 | Playwright가 3417 고정 + 사용자 dev 서버 재사용이라 e2e는 늘 development로 돈다. 확인 방법이 없다 | 판정을 순수 함수 `anchorEditEnabled(nodeEnv, search)`로 빼서 단위 테스트한다. 그리고 `next build` 산출물(`.next/static`)에 편집 패널 문구가 없음을 grep으로 확인한다 |
| W-6 | WP4 완료 조건 「DevTools Performance 16ms 안팎 눈 확인」 | 워커가 할 수 없다. e2e는 swiftshader라 수치가 의미 없다 | 측정할 수 있는 조건으로 바꾼다. 예: `AnchorProjector` useFrame 1회 소요를 `performance.now()`로 재서 `__faceViewer.anchorMs()`로 노출하고, 평균 2ms 미만인지 본다. 아니면 이 항목을 코디 실물 확인(3417)으로 넘긴다 |
| W-7 | §3-4·3-5 · AC-14·16 | ① 「무릎(끝점 x ∓ 32)」 부호가 모호하다(왼쪽 카드에서 −32면 카드 안쪽 392가 된다). ② `data-visible`이 목표값 기준인지, 스무딩된 현재값 기준인지 정해져 있지 않다(`cur += …·0.25`는 0에 닿지 않는다). ③ `__faceViewer.anchors().opacity`가 가림만 반영한 값인지, ×0.3을 곱한 최종값인지 정해져 있지 않다. AC-16이 이 값에 의존한다 | ① 「얼굴 쪽으로 32(왼쪽 +32 → x 456, 오른쪽 −32 → x 1464)」라고 쓴다. ② `data-visible = 목표 opacity > 0`. ③ `opacity`는 SVG에 실제로 적용한 최종값이라고 쓰고, 필요하면 `occlusion` 필드를 따로 둔다 |
| W-8 | WP1 「존재하지 않는 `hubId`로 돌리면 종료 코드 1」 | 커밋된 `hub-refs.json`을 고치지 않고 시험할 방법이 없다 | 스크립트에 `--refs <path>`(또는 `HUB_REFS` env)를 두고, 시험용 refs는 임시 파일로 준다고 명시한다 |
| W-9 | §1-3 copy.ts 행 | 근거 「태블릿이 씀」이 틀렸다(태블릿은 직접 import하지 않는다). `gradeSentence`는 focus-card 삭제 뒤 쓰는 곳이 0이 된다 | 근거를 「`summaryLine`: recommend-rules.test.ts · `GRADE_PHRASE`: porphyrinScoreNote(어댑터)」로 고친다. `gradeSentence`는 지우거나 「쓰는 곳 없음, 남김」으로 명시한다 |
| W-10 | §3-7 `__faceViewer` 확장 | `face-canvas.tsx:142-151` Controls effect가 객체를 **통째로 다시 만든다**(`applied`만 이어 받음). 앵커 훅을 다른 컴포넌트에서 붙이면 마운트 순서에 따라 지워진다 | 「anchors·anchor3d는 Controls effect의 객체 생성에 같이 넣거나, `Object.assign(window.__faceViewer, …)`로 덧붙이고 Controls도 기존 키를 보존하게 고친다」라고 명시한다 |
| W-11 | §2-3 match 테두리 | 흐림을 「카드 전체 `opacity .35`」로 주면 `ring-2`도 35%가 된다. 「피지 세균」 필터에서는 6장 모두 흐리므로, 일치 카드 테두리가 잘 안 보일 수 있다(실물 사용자 관점) | opacity는 카드 안 내용에 주고 테두리(ring)는 100%로 두라고 쓴다. 또는 AC-9 스크린샷 확인 항목에 넣는다 |
| W-12 | §1-1 카드 칩 | 400 폭 카드(패딩 md)에 18px 칩 「바이오스티뮬레이터/콜라겐부스터」(17자 ≈ 300px + 칩 패딩)가 들어간다. 한 줄에 겨우 맞거나 넘친다. 볼/코 카드는 칩 5개 × 높이 44로 3줄이다. 317 높이 안에 들어가기는 하지만(대략 280) 여유가 적다 | 「칩은 `flex-wrap`, 칩 하나가 넘치면 칩 안 줄바꿈 허용」을 쓰고, WP2 스크린샷에서 6장 모두 잘림이 없는지 완료 조건에 넣는다 |
| W-13 | AC-12 「지시선 6개 교차 0건」 | 찍는 자리(WP3)에 달린 조건이다. §1-2 높이 순서를 지키면 통과할 가능성이 높지만, 실패하면 워커가 SPEC 표 밖에서 자리를 바꾸게 된다 | 「교차가 나면 §1-2 칸 순서 안에서 점 자리를 옮겨 다시 찍는다(카드 칸 바꾸기 금지)」를 WP3에 적는다 |

## 5. WP · AC 따름성

- WP1~6의 순서(데이터 → 배치 → 앵커 → 투영 → 모달 → 검증)는 의존 순서와 맞고, 워커 1명이 그대로 따를 수 있다. WP마다 관련 시험만 돌리고, 전체 검증은 WP6에서 한 번 하는 방식도 규칙과 맞다.
- AC 25개 중 23개는 testid·속성·`__faceViewer` 값으로 검증할 수 있는 문장이다. 사람 눈이 들어가는 곳은 AC-13 끝 「눈 확인 스크린샷」과 WP4 프레임 확인 두 곳이고, W-6과 §6-7(사용자 확인)으로 처리하면 된다.
- 실물에서 만날 자리(1920×1080):
  - 모달은 1040×≤880이고 루트(1920×1080) 안 오버레이라 들어간다. 메디킷 Dialog 포털을 쓰지 않는 근거(`stage.tsx:42-53` scale)도 맞다.
  - 가장 긴 M8 노드도 섹션 항목이 3–5개라 2열에서 스크롤 없이 들어갈 가능성이 높다.
  - 투영 좌표는 `resize offsetSize` 기준 설계 px이다. 카메라 fov 28, 거리 0.55에서 30° 돌리면 미간 점도 100px 넘게 움직이므로, AC-13의 10px 기준은 여유가 있다.
  - 재질이 `DoubleSide`(`face-material.ts:46`)라 raycast가 뒷면에도 맞는다. 가림 판정이 보수적으로 되는 쪽이고 문제는 아니다.

## 6. 다음

W-1·W-2·W-3을 SPEC에 반영(또는 W-2는 사용자 확인)한 뒤 frontend를 발주하는 것을 권한다. W-4~W-13은 발주 브리프에 그대로 옮겨도 된다.

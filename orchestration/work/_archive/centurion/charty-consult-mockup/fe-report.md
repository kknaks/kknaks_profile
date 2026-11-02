# fe-report — charty-consult-mockup 구현 (frontend 워커)

- 브리프: 코디 dispatch ctx_bb3d20cdfe08 · task_0678a79d3617 · 정본 SPEC.md
- 앱: `reference/2026-10-21-charty-poc/web/`

## 진행 기록 (WP 마다 한 줄)

- WP1 뼈대 ✓ — Next 16.4.2 · Tailwind 3.4.19 · medikit 1.4.0 고정 · Pretendard local · `/` `/screen` `/tablet` · Stage. `npm run build` 통과, `e2e/smoke.spec.ts` 3건 통과(200 · solid blue = rgb(111,33,255) · 1280×720/1000×900/1920×1080 에서 16:9 유지)
- WP2 에셋·목데이터 ✓ — `scripts/prepare-assets.mjs` 1회로 §7 파일 12개 생성(텍스처 5장 모두 3242×1621) · 2회 실행 해시 동일(manifest generatedAt 제외) · `M3D_HAR=/nonexistent.har` 로 exit=1 · `git status --porcelain --untracked-files=all` 에 m3d/HAR 0줄 · report/*.json 가드 키 0. 목: pricing.json 48건 · taxonomy-subset.json 6종 · checklist.ts · transcript.ts · session.ts. ⚠ measure.data 최상위에 `hash`·`id` 가 있어 가드에 걸린다 → 측정 수치 키(type·version·results_version·categories·features)만 남김. ⚠ 데모 가격표에 첫방문이벤트 행이 0건(정규가·이벤트만)
- WP3 데이터 계층 ✓ — domain(skin-report·grade·filters·session·pricing) · copy.ts · m3d-types · fromM3d · M3dMockSource · useSkinReport · recommend-rules. `npx vitest run` 3파일 34건 통과(등급 경계 8 · 가짜 픽스처 8 · 실제 public/m3d 5(대분류 76/68/71.2/68.3 · 항목 · 부위 8 · 한자 0) · 가격 AC-14(2,100,000/2,310,000/2,079,000·협찬 0) · 첫방문 숨김(가짜 행) · 추천 칩 6). 실제값 테스트는 public/m3d 없으면 skip. 굵은주름 좌/우는 어댑터가 `sided` metric(태블릿 전용)으로만 남긴다
- WP4 3D 뷰어 ✓ — r3f 9 + drei OrbitControls · OBJLoader · ShaderMaterial 1개(바탕 페이드 + 오버레이 알파) · unlit · `<Canvas flat linear>` · NoColorSpace · flipY 기본. 얼굴 정면·정립 확인, 잔주름(미간·눈밑·이마)·굵은주름(팔자·마리오넷)·모공(얼굴 ROI, 눈 제외) 오버레이가 제자리 — `screens/overlay-*.png`. 보정 2건: ① 오버레이 색을 `setStyle(hex, LinearSRGB)` 로 넣어 linear 캔버스에서 색이 어두워지지 않게 ② 잔주름 원본(wrinkle_mixed)이 0.013% 로 성겨 1/3 축소 뒤 거의 사라짐 → 준비 스크립트에서 잔주름만 blur 2.5 + gain 8(나머지 gain 3 그대로). 회전 범위·정면 복귀는 WP8 e2e 로 확인
- WP5 화면 ① 우측 ✓ — 헤더 · B(레이더 G1 + 카드 2×2 + 한 줄 요약 + 피부톤 칩) · C(G2 막대 8행, 포르피린은 「5,470개 · 얼굴의 30.6%」+점수 없음 배지) · A2 FocusCard(+G3 부위 맵, 라벨 양옆 열) · D PlanPanel(행 하이라이트 · 300ms 트윈 · VAT 별도/포함 · 최종 40px). 목 SessionState(AC-14 카트 + 10%)로 눈 확인: 2,100,000 / 2,310,000 / 최종 2,079,000. 필터를 바꾸면 A2·C 강조·B 대분류 테두리가 따라 바뀜. 보정: 메디킷 `Button leftIcon` 이 lucide 아이콘에 size="sm" 을 주입해 svg 경고 → 아이콘을 children 으로. 빈 카트·가격 숨김은 WP7/8 동기화 e2e 로 확인
- WP6 화면 ② ✓ — 헤더 50 · 고객 바 40(유형 ComboBox · 연결 점 · 큰 화면 열기 · 가격 표시 Toggle · 상담 초기화 ConfirmModal) · 필터 띠 72 · 가격 패널 440(검색·보기 추천/전체·대분류·유형 칩·행 탭=추가 / 선택 시술: 행 탭=체크·select 할인·무료·삭제·전체선택/삭제 / 요약: n/m·VAT·할인율 줄+협찬 100%·최종) · 추천 260(칩 6 · 이유 · 기대효과/금기/부작용/시술 후 · 가격표에서 보기) · 우 탭 4(피부 분석 맨 앞 · 체크리스트 · 차트 · 상담 텍스트). Playwright 손 조작으로 AC-14 카트 → 태블릿 최종 2,079,000원. 추천 보기 25행(SPEC 「약 20」). 체크리스트 초기 체크 7/13(목 텍스트) · 단위 테스트 추가(36건 통과). 굵은 주름 좌/우 3줄에 ⓘ Tooltip
- WP7 동기화 ✓ — `sync/channel.ts`(봉투 v1 · 자기 메시지·같은 쪽 무시) · `use-tablet-sync`(localStorage 복원 → 변경마다 전체 스냅샷 · hello 회신 · filter:set · 2초 ping) · `use-screen-sync`(hello · seq 비교 · pong · 5초 무응답 = 대기) · `screen-store`. seq 규칙에 하나 덧붙임: sessionId 가 다르면(태블릿이 저장소를 잃고 새로 시작) seq 가 작아도 받는다. `e2e/sync.spec.ts` 7건 통과(dev 서버) — AC-5·6·7·8·9·10·11·12·14·15·16·17·18
- WP8 검증 ✓ — `npm run verify` exit 0: eslint 0 · vitest 4파일 36건 · next build · Playwright 14건(smoke 3 · sync 7 · viewer 4, `next start -p 3417`). AC-20 은 코디 결정 C 로 오버레이를 굵게 바꾼 뒤 통과(아래 전후 수치). 스크린샷 `screens/` 4장 + overlay 3장

---

## AC 확인 표

| AC | 결과 | 근거 |
|---|---|---|
| 1 | PASS | `public/m3d` 를 옮겨 둔 채 `npm ci && npm run build` 통과(Compiled successfully · 정적 5페이지) |
| 2 | PASS | `npm run lint` 0건 · `npm run test` 36 passed (verify 로그) |
| 3 | PASS | `npm run prepare:assets` 1회로 12파일 · `git status --porcelain --untracked-files=all` 에 public/m3d·HAR·m3d-assets·screens 0줄 |
| 4 | PASS | 커밋 대상(`git ls-files --others --exclude-standard -z web`) 전체에 HAR 의 리포트 hash·report id·user id·생년월일·회원번호(unique/display_unique)·스캐너 태그·`amazonaws`·`X-Amz` 8개 값 `grep -F` 0건(exit 1). 픽스처는 손으로 만든 값 |
| 5 | PASS | e2e `sync.spec` AC-5·6·7·14 — 행 추가 1초 안 큰 화면 행·120,000 |
| 6 | PASS | 같은 테스트 — 항목 20% → 1,760,000 · 무료 · 체크 해제(행 빠짐·합계 감소) · 삭제 · 무료 해제 |
| 7 | PASS | 같은 테스트 — 10% → 2,079,000 · 협찬 100% → 0 |
| 8 | PASS | `AC-8·9` — 태블릿 필터 → 큰 화면 칩·텍스처(viewer `data-applied`) · 큰 화면 칩 → 태블릿 칩 |
| 9 | PASS | `AC-8·9` — 피부 분석 잔주름 → C 행 강조 + 필터 fineWrinkle + A2 부위 맵 |
| 10 | PASS | `AC-10` — 큰 화면 새로고침 1초 안 카트·15%·필터 복원 · 태블릿 새로고침 후 카트 유지 |
| 11 | PASS | `AC-11` — 큰 화면 닫음 → 7초 한도 안 「큰 화면 없음」(ping 2초 + 5초 판정) · 다시 열면 「큰 화면 연결됨」 |
| 12 | PASS | `AC-12` — 가격 표시 OFF → 합계·행 금액 0개, 시술명 남음, 「가격은 상담사가 안내해 드려요」 · 빈 카트 문구 |
| 13 | PASS | vitest 실제값 `fromM3d — 실제 public/m3d/report`(76·68·71.2·68.3 / 76·73·67·68.8·82.9·83.8·65.6 / 포르피린 null·5,470개) · 색은 `GRADE_META`(§2-1) — `screens/1-screen-natural.png` |
| 14 | PASS | vitest `가격 계산(AC-14)` + e2e 태블릿 `2,100,000원/2,310,000원/2,079,000원` = 큰 화면 data-value 같음 |
| 15 | PASS | e2e `AC-15·16·17` — 큰 화면 필터 5개 · 태블릿 탭 4개 본문에 `/[一-鿿]/` 0 · `-1` 0 · vitest 「중국어 title 이 결과 어디에도 없다」 |
| 16 | PASS | 같은 테스트 — 태블릿 굵은 주름에 「좌/우」 + ⓘ 3개 · 큰 화면 본문에 좌/우 낱말 0 |
| 17 | PASS | 같은 테스트 — 큰 화면에 「진단·질환·치료·환자」 0 |
| 18 | PASS(데이터상 0건) | `AC-18` — 전체 48 · 추천 보기는 규칙 행만(사각턱·제모 없음, 칩 6) · 재방문에서 첫방문이벤트 행·칩 0. ⚠ 데모 가격표에 첫방문이벤트가 원래 0건이라 「사라짐」은 화면으로 못 보임 → 규칙은 vitest 「재방문 숨김(가짜 행)」으로 확인(코디 답: 기본값) |
| 19 | PASS | `viewer AC-19` — azimuth 0°·polar 90° · 투영 x(−0.05)<0, x(+0.05)>0(마주 보는 시점, 반전 없음) |
| 20 | PASS(보정 후) | `viewer AC-20` — 21쌍 모두 WebGL 캔버스 픽셀 차 >1%. 최소 쌍 잔주름↔굵은주름: **0.66% → 1.15%**(오버레이 굵게, 아래). 나머지 쌍 8.98–35.35% |
| 21 | PASS(눈 확인) | `screens/overlay-fine-wrinkle.png`(미간·눈밑·이마) · `overlay-deep-wrinkle.png`(팔자·마리오넷·눈물고랑) · `overlay-pore.png`(얼굴 ROI, 눈 제외) — 사진 위 제자리, 위아래 정상 |
| 22 | PASS | `viewer AC-22` — 양방향 드래그 후 |azimuth| 70–75°, polar 60–120° · 더블클릭·태블릿 [정면으로] 후 |azimuth|<1° |
| 23 | PASS | `viewer AC-23` — `/m3d/**` 404 → 「3D 에셋이 없습니다 — npm run prepare:assets…」 · D 정상 · pageerror 0 |
| 24 | PASS | `package.json` `"@medisolve-ai/medikit": "1.4.0"` · smoke e2e solid blue = rgb(111,33,255) · 활성 탭 `border-primary` · `screens/4-tablet.png` |
| 25 | PASS | 탭 바 4(자체 버튼·border-b-2) · 행 탭=추가 · select 할인 5–50 · 무료시술/삭제 · 할인율 버튼 줄 + 협찬 100% — `screens/4-tablet.png`, sync e2e 가 이 조작으로 돈다 |

## 스펙과 다르게 한 것 (이유)

1. **measure.json 최상위 키** — SPEC §7 은 「`data` 그대로」인데 `data` 최상위에 `hash`·`id`·`id_str` 가 있어 같은 §7 의 가드에 걸린다. 측정 수치 키(`type·version·results_version·categories·features`)만 남겼다.
2. **오버레이 처리** — SPEC 기본 gain 3. 잔주름(wrinkle_mixed 0.013%)이 1/3 축소 뒤 거의 사라져 잔주름 blur 2.5·gain 8 로 시작 → AC-20 에서 잔주름↔굵은주름 0.66% → **코디 결정 C**: 잔주름 blur 6·gain 14, 굵은주름 blur 5·gain 8 (pore 는 gain 3 그대로). coverage 잔주름 0.02→0.17%, 굵은주름 0.30→0.56%. 위치·색(보라 #a290ff / 주황 #fd9400)은 그대로. `OVERLAY_GAIN` 환경변수로 전체 덮어쓰기 가능
3. **오버레이 색 공간** — `<Canvas linear>` 에서 `Color.set()` 이 sRGB→linear 로 바꿔 색이 어두워져 `setStyle(hex, LinearSRGBColorSpace)` 로 넣었다(사진 픽셀과 같은 공간).
4. **globals.css** — SPEC 은 `@import base.css` → `@tailwind …` 이지만 base.css 가 이미 `@tailwind` 3줄을 품고 있어 두 벌이 되고 두 번째가 처리되지 않는다(Turbopack 경고). import 한 줄만 둔다. 결과 CSS 는 같다.
5. **화면 ① 세로 크기** — 와이어 A 944 / B·C·D 372·300·248 은 본문 1016−패딩 32 = 984 와 안 맞아, A 는 984 꽉, D 는 남는 높이(≈280)로 둠.
6. **대분류 카드 문장** — 「쉬운 설명 1문장」을 등급 문구(「조금만 신경 쓰면 돼요」 등)로 — 카드 폭에서 한 줄에 들어가게.
7. **굵은 주름 좌/우 값** — §5-3 「좌/우 세부값은 버린다」와 §5-4·§11-4 「태블릿에 좌/우 + ⓘ」가 부딪혀, 어댑터가 좌/우 **평균 곡률 점수**만 `sided`·`tabletOnly` metric 으로 남기고 태블릿에서만 보인다(id 기준).
8. **screen-store seq 규칙** — 「seq ≤ 가진 것이면 버림」에 「sessionId 가 다르면 받음」을 더했다(태블릿 저장소가 날아가 seq 가 1 부터 다시 시작할 때 큰 화면이 멈추지 않게).
9. **메디킷 Button `leftIcon`** — lucide 아이콘에 토큰 size("sm")를 주입해 svg 경고 → 아이콘을 children 으로.
10. **추천 보기 행 수** — 규칙대로 돌리면 25행(SPEC 「약 20」). 규칙 표 그대로라 줄이지 않았다.

## 남은 것 · 코디 확인 필요

- **gitignore 추가 필요(직접 안 고침)**: Next 16 이 `web/AGENTS.md`(dev 첫 실행 때 생성)·`web/tsconfig.tsbuildinfo`(build)·`web/next-env.d.ts` 를 자동으로 만든다. 앞의 둘은 지워 뒀지만 다시 돌리면 또 생긴다 → `reference/2026-10-21-charty-poc/web/AGENTS.md`·`*.tsbuildinfo` 무시 권장(next-env.d.ts 는 관례상 커밋). Playwright 산출물은 `node_modules/.cache/playwright` 로 보내 ignore 불필요.
- `reference/2026-10-21-charty-poc/테스트 보고서.html` 이 untracked 로 있다 — 내가 만든 파일 아님, 손대지 않음(코디 판단).
- `npm audit` 9건(2 moderate · 7 high) — 의존성 경고, 손대지 않음.
- AC-21·눈 확인 항목은 headless(swiftshader) 스크린샷 기준. 실제 큰 스크린·태블릿 기기 확인은 안 함.
- 3417 에 띄운 dev/start 서버는 모두 내렸다(`lsof` 0). git commit·push 안 함.

---

## 수정 1판 (fix1-instructions.md · review-report.md)

| # | 항목 | 결과 | 근거 |
|---|---|---|---|
| 1 | **F-1 AC-11** | 고침 | 태블릿만 판정 tick 500ms(`TABLET_LINK_TICK_MS`) · 무응답 4초(`TABLET_LINK_TIMEOUT_MS`) — `sync/channel.ts`, `use-tablet-sync.ts`(ping 2초와 tick 분리). 큰 화면 쪽은 SPEC 그대로 5초. e2e timeout 7s → **5s** 로 되돌림(`sync.spec.ts:113`), 통과 |
| | 최악 지연 계산 | | 큰 화면은 ping(2초 주기)마다 즉시 pong. 닫는 순간 t=0 에서 마지막 pong 은 t∈(−2, 0]초. 「없음」은 `now − lastPong ≥ 4초` 인 첫 tick → 최악은 마지막 pong 이 닫기 직전(≈0)일 때 4초 + tick 지연 최대 0.5초 = **4.5초 < 5초**. 최선은 2.0초. 정상 연결 중엔 pong 간격 2초 < 4초라 깜빡이지 않는다 |
| 2 | **잔주름 오버레이 얼룩** (AC-21) | 고침 | blur 를 없애고 **풀해상도 팽창 → max 축소**로 바꿈(`prepare-assets.mjs` `OVERLAY_DILATE_BY_KEY` · `maxPool`). 잔주름·굵은주름 모두 팽창 폭 15px(풀해상도, 축소 뒤 ≈5px), gain 3(기본값으로 복귀), 모공은 그대로. ⚠ libvips 형태 연산은 검정을 전경으로 봐서 흰 선을 굵히는 쪽이 `erode` 다(`dilate` 는 흰 선을 지움: 실측 0.013%→0%) — 코드 주석에 적음. 위치·색·범례 그대로, 이제 「선」으로 보임 |
| | AC-20 전후 | 통과 유지 | 잔주름↔굵은주름: 1판 원래 0.66% → 1판 blur 1.15% → **수정1 팽창 1.11%**(나머지 20쌍 8.9–35.4%). coverage 잔주름 0.17→0.12%, 굵은주름 0.56→0.55%. 전후 스크린샷 `screens/overlay-fine-wrinkle-before.png`·`overlay-deep-wrinkle-before.png`(blur) ↔ `overlay-fine-wrinkle.png`·`overlay-deep-wrinkle.png`(팽창) |
| 3 | **W-1 터치 32px** | 고침 | 할인 select·무료·삭제·전체선택/삭제 `h-8` · 할인율 버튼 `h-8 min-w-[36px]` · 보기/대분류/유형 칩 · 추천 칩 · 체크리스트 칩·초기화 · 차트 복사/편집/콤보 · 고객 바 버튼·콤보·Toggle(`!h-8`, scale 축소 제거) 모두 32px. 구조·문구·색은 그대로. 새 e2e `fix1 W-1·W-2` 가 19종 선택자 + 체크리스트 칩의 높이를 재서 31.5px 미만 0건 |
| 4 | **W-2** | 고침 | 피부 분석 대분류 4칸에 등급 배지(`analysis-cat-*` 안 `[data-grade]` 1개씩) · 항목 측정치 `slice(0, 2)`. 굵은 주름 좌/우 ⓘ 는 3 → 2개(AC-16 단언도 2로) |
| 5 | **W-3** | 고침 | `setFilter` 가 `focusItem: null` 을 함께 넣는다(`session-store.ts`). 큰 화면 `filter:set` 도 이 경로. 피부 분석 항목 탭(`toggleFocusItem`)은 필터와 강조를 같이 바꾸므로 그대로. 새 e2e `fix1 W-3`: 모공 강조 → 큰 화면에서 붉은기 → C 강조·B 테두리(염증·민감)·A2 가 모두 붉은기, 모공 강조·태블릿 선택 해제. 태블릿에서 바꿔도 같음 |
| 6 | **테스트 빈틈** | 고침 | AC-15 큰 화면 필터 **7개 전부** 순회 · 태블릿 탭 4개에 `-1` 검사 추가 · AC-16 큰 화면 정규식에 `좌\/우` 추가(`sync.spec.ts` AC-15·16·17) |

손대지 않은 것: W-6(추천 카드 원문) · F-2(코디 처리) · 그 밖의 리팩터.

### 확인

- 항목별 관련 테스트만 먼저: `viewer AC-20`(팽창 폭 9→1.01%·… 15 → 1.11% 로 정함) · `sync.spec` 9건
- 마지막 `npm run verify` **exit 0**: lint 0 · vitest 4파일 36 · build · Playwright **16 passed**(smoke 3 · sync 9 · viewer 4)
- 스크린샷 `screens/` 다시 찍음: 1~4 + overlay 3 + before 2. 3417 의 내가 띄운 dev/start 서버는 내림(`lsof` 0). 커밋 안 함
- `web/AGENTS.md`·`tsconfig.tsbuildinfo` 는 build 때 다시 생겼다 — 리뷰 기준 `.gitignore:87-94` 가 이미 덮는다

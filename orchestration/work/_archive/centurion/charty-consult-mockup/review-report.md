# review-report — charty-consult-mockup (reviewer · read-only)

- 기준: `SPEC.md` §9 WP · §10 AC 1~25 · §11 / `_RESUME.md` / `fe-brief.md` / `fe-report.md`(자기 보고는 근거로만 대조)
- 대상: `reference/2026-10-21-charty-poc/web/` (untracked 87파일) · `screens/` 7장
- 직접 돌린 것: `npx vitest run` → 4파일 36 passed(실데이터 테스트 skip 없이 돎) · `npm run lint` → 0건 · `npx tsc --noEmit` → exit 0
- 돌리지 않은 것: build · e2e · dev(브리프 제약). 그래서 AC-1·5~12·19~23 은 **e2e 코드와 구현 코드를 읽고** 판정했다. 실행 결과는 fe-report 의 말뿐이다

---

## 총평: **FAIL** — 고칠 것 1건(코드) + 코디가 커밋 전에 처리할 것 1건

| # | 무엇 | 누가 |
|---|---|---|
| F-1 | **AC-11**: 「5초 안에 큰 화면 없음」을 구현이 보장하지 못하고(최악 약 6초), e2e 는 기대값을 **7초**로 늘려서 통과했다 | 구현 워커 |
| F-2 | `reference/2026-10-21-charty-poc/테스트 보고서.html` 이 **gitignore 밖**인데 실명 「이건학」과 리포트 hash(`/h5?hash=…`)가 들어 있다. `git add reference/2026-10-21-charty-poc` 를 하면 같이 커밋된다 | 코디(.gitignore) |

이 둘을 빼면 남는 것은 WARN 뿐이다. 가격·동기화 핵심 로직은 차티 stg 와 같고, `web/` 커밋 대상에서는 개인정보가 나오지 않았다.

---

## 1. AC 1~25

| AC | 판정 | 근거 · 메모 |
|---|---|---|
| 1 | PASS(코드 확인) | `public/m3d` 를 import 하는 곳은 테스트 두 개뿐이고, 둘 다 fs + `describe.skipIf` 다(`src/data/adapters/m3d.test.ts:93-94`, `src/data/recommend-rules.test.ts:11-13`). 런타임은 fetch(`src/data/sources/m3d-mock-source.ts`). build 는 직접 돌리지 않았다 |
| 2 | PASS | 직접 실행: lint 0 · vitest 36 passed |
| 3 | PASS | `git check-ignore -v` 로 확인: `.gitignore:87-94` 가 m3d-assets·*.har·public/m3d·screens·AGENTS.md·*.tsbuildinfo·node_modules·.next 를 덮는다. porcelain 출력(web 87파일)에 m3d·HAR 경로 0 |
| 4 | PASS | HAR 에서 식별 키(hash·birth·unique·user_id·id·scanner·name …)의 값 201개를 뽑아 web 커밋 대상 87파일에 `grep -F` 를 돌렸다. 걸린 것은 `basic_241`·`Porphyrin`·`pore_big_ratio` 같은 **필드 이름**뿐이고 식별값은 0. `amazonaws`·`X-Amz`·리포트 hash 도 0. 픽스처 숫자는 실값과 다르다(예: Red 90 ↔ 실값 76), 손으로 만든 값이 맞다. ⚠ web 밖 파일은 F-2 |
| 5 | PASS(코드) | `e2e/sync.spec.ts:31-33` 시술명 + `data-value=120000`, timeout 1s |
| 6 | PASS(코드) | `sync.spec.ts:55-67` 할인 20% → 1,760,000 · 체크 해제 → 행 사라짐 · 합계 · 삭제 · 무료 해제 |
| 7 | PASS(코드) | `sync.spec.ts:46-52` 10% → 2,079,000 · 협찬 100% → 0. 계산식은 stg `cart-utils.ts:8-15` 와 같다 |
| 8 | PASS(코드) | `sync.spec.ts:72-78` 양방향. 큰 화면 → `filter:set` → 태블릿 `setFilter` → 스냅샷(`use-tablet-sync.ts:31`) |
| 9 | PASS(코드) | `sync.spec.ts:80-84`, `session-store.ts:106-110` |
| 10 | PASS(코드) | `sync.spec.ts:90-107`. 큰 화면은 seq 0 에서 시작하고 hello 를 받으면 태블릿이 즉시 스냅샷을 보낸다(`use-screen-sync.ts:27`, `use-tablet-sync.ts:30`) |
| 11 | **FAIL** | **F-1.** 태블릿은 `now` 를 ping 주기(2초)마다만 갱신하고(`use-tablet-sync.ts:36-39`) 판정은 `now - lastPong < 5000` 이다(`:49`). 마지막 pong 은 닫기 전 0~2초 안에 오므로, 닫은 뒤 「없음」이 뜨기까지 **4~6초**가 걸린다. 테스트는 `timeout: 7 * SEC`(`e2e/sync.spec.ts:113`)이고 제목에는 「5초 안에」라고 적혀 있다. 고칠 방향: 태블릿 판정 tick 을 500ms 로 하고 timeout 을 4초로 줄이면(ping 2초보다는 길게) 최악이 4.5초가 된다. 테스트 timeout 은 5초로 되돌린다 |
| 12 | PASS(코드) | `plan-panel.tsx:64,75-98`, `sync.spec.ts:121-132` |
| 13 | PASS | vitest 실데이터(직접 실행). 등급색은 `grade.ts:22-28` = SPEC §2-1 표. 스크린샷 1·2·3 에서 76/68/71.2/68.3 · 막대 7개 값 · 포르피린 「5,470개 · 얼굴의 30.6%」 + 「점수 없음」 배지를 눈으로 확인 |
| 14 | PASS | `pricing.test.ts:15-24`(직접 실행), `sync.spec.ts:35-48`. 스크린샷 3·4 에서 양쪽 2,100,000 / 2,310,000 / 2,079,000 확인 |
| 15 | PASS / 테스트 WARN | 코드: 어댑터가 원본 title 을 아예 안 읽는다(`m3d.ts:55` 화이트리스트, label 은 자체). 점수가 없으면 `''`·`–` 를 보인다(`grade.ts:33-35`). 화면 컴포넌트에 한자 0. ⚠ 테스트 빈틈: 큰 화면 필터 7개 중 5개만 돈다(redness·pigment 빠짐, `sync.spec.ts:158`). 태블릿은 한자만 보고 `-1` 은 안 본다(`:167-171`) |
| 16 | PASS / 테스트 WARN | 코드: 좌/우 metric 은 `tabletOnly`(`m3d.ts:127`)이고, 큰 화면 두 곳 모두 이를 걸러 낸다(`focus-card.tsx:13`, `score-bars.tsx:30`). ⓘ 는 `analysis-panel.tsx:56-65`. ⚠ 큰 화면 정규식 `/좌 |우 |왼쪽|오른쪽/`(`sync.spec.ts:165`)으로는 「좌/우」를 못 잡는다 — 느슨한 단언 |
| 17 | PASS | `src/components/screen`·`charts`·`copy.ts` 에서 금지어는 주석 1줄뿐(`copy.ts:2`). taxonomy 의 「치료·환자」는 태블릿 추천 카드에만 나온다(AC 범위 밖, 아래 W-6) |
| 18 | PASS(데이터상) | 규칙 행을 손으로 셌다: 보톡스 5 + 리프팅 7 + 필러 5 + 모공 3 + 칙칙함 3 + 엑셀V 1 + 수소 1 = **25**, fe-report 와 같다. 사각턱·턱선·실리프팅·인모드·제모는 빠진다. 재방문 숨김은 가짜 행 단위 테스트로만 확인됐다(`pricing.test.ts:53-65`) — 데모 가격표에 첫방문이벤트가 0건이라 화면으로는 보일 수 없다. 받아들일 만하다 |
| 19 | PASS(코드) | `viewer.spec.ts:44-54` azimuth·polar·투영 x 부호 |
| 20 | PASS(코드 · 보정 후) | `viewer.spec.ts:56-74` 21쌍 > 1%. 통과는 오버레이를 굵게 바꾼 결과다(아래 차이 2) |
| 21 | PASS(눈 확인) / WARN | `overlay-fine-wrinkle.png`: 미간·눈밑·이마 위치는 맞고 위아래도 정상. 다만 blur 6 탓에 **선이 아니라 얼룩 6~7개**로 보인다. 범례 「보라 선 = 찾아낸 잔주름」과 모양이 어긋난다 → 코디가 3417 에서 눈으로 확인할 것. 굵은주름(팔자·마리오넷)·모공(눈 제외 ROI)은 제자리다 |
| 22 | PASS(코드) | `viewer.spec.ts:76-107` ±75°, polar 60–120, 더블클릭 · 태블릿 [정면으로] |
| 23 | PASS(코드) | `viewer.spec.ts:109-118` 404 route · pageerror 0 |
| 24 | PASS | `package.json` `"@medisolve-ai/medikit": "1.4.0"` 고정. smoke e2e 가 rgb(111,33,255) 를 본다. 스크린샷 4 의 활성 탭 밑줄·선택 칩이 보라 |
| 25 | PASS | `cart.tsx:44-108`(행 탭=체크 · select 할인없음+5–50 · 무료시술/무료 해제 · 삭제), `cart-summary.tsx:36-57`(할인율 줄 + 협찬 100%, 다시 누르면 해제). stg `cart.tsx:136-149`·`cart-summary.tsx` 와 구조·문구·클래스가 같다 |

---

## 2. fe-report 「스펙과 다르게 한 것」 10건

| # | 판정 | 이유 |
|---|---|---|
| 1 measure.json 최상위 키 | 타당 | SPEC §7 안에서 「data 그대로」와 가드가 서로 부딪힌다. 수치 키 5개만 남겨도 어댑터가 쓰는 것은 다 있다(실파일 top keys 확인) |
| 2 오버레이 blur/gain | 타당 · WARN | AC-20 을 통과시키려고 코디가 결정 C 로 승인했다. 대가로 잔주름이 「선」이 아니라 「얼룩」이 됐다(AC-21 메모). 범례 문구를 「보라 = 잔주름이 모인 곳」으로 바꿀지는 코디가 판단 |
| 3 오버레이 색공간 | 타당 | linear 캔버스에서 hex 를 sRGB 로 해석하면 어두워진다. 사진 픽셀과 같은 공간으로 맞춘 것이다 |
| 4 globals.css @tailwind 중복 제거 | 타당 | base.css 가 이미 지시문을 갖고 있어 두 벌이 되는 것을 피했다. 결과는 같다 |
| 5 화면 ① 세로 크기 | 타당 | 와이어 수치끼리 합이 맞지 않는다(984 ≠ 944/372+300+248+간격). `screen-view.tsx:43-60` 은 B 372·C 300 고정, D 는 나머지 |
| 6 대분류 카드 문장 = 등급 문구 | 타당(경미) | SPEC 「쉬운 설명 1문장」을 좁게 읽었지만 §2-3 규칙 5 의 등급 문구다 |
| 7 굵은주름 좌/우 sided metric | 타당 | §5-3 「버린다」와 §5-4·§11-4 「태블릿에 좌/우 + ⓘ」가 충돌한다. 화면 ①에 새지 않는 것도 코드로 확인했다 |
| 8 screen-store sessionId 예외 | 타당 · WARN | 태블릿 저장소가 날아갔을 때 화면이 멈추지 않게 한다(`screen-store.ts:19`). 다만 sessionId 가 다른 태블릿 탭 두 개가 동시에 살아 있으면(그중 하나는 저장소 차단) 서로의 스냅샷을 번갈아 받는다. 목업 범위 밖이라 기록만 |
| 9 메디킷 Button leftIcon | 타당 | 경고 회피일 뿐 모양 차이는 없다 |
| 10 추천 25행(SPEC 「약 20」) | 타당 | 위 AC-18 손 계산과 같다. 규칙 표를 그대로 따르면 25다 |

---

## 3. 빠진 것 · 범위 밖

빠진 것(WARN, 모두 경미):

- **W-1 터치 대상 32px**(SPEC §3-1): 태블릿 할인 select·무료·삭제는 `h-6`(24px, `cart.tsx:82,95,104`)이고, 할인율 버튼·칩은 `py-0.5` 로 약 20px 이다. 차티 원본 크기를 따른 결과지만 SPEC 의 「최소 32px」은 지키지 못했다
- **W-2 피부 분석 탭 대분류**: SPEC 은 「점수·배지·측정치 2개」다. 대분류 4칸에는 배지가 없고(`analysis-panel.tsx:23-30`), 항목은 측정치를 3개까지 보인다(`:53`)
- **W-3 focusItem 이 남는 문제**: 피부 분석에서 항목(예 모공)을 고른 뒤 필터를 바꾸면, C 강조와 B 테두리는 계속 모공이고 A2 만 새 필터를 따른다(`screen-view.tsx:36`, SPEC 「focusItem 우선」 그대로). `setFilter` 할 때 `focusItem` 을 비울지는 코디가 판단

범위 밖으로 들어간 것: 없음. `chart-text.ts`·`checklist.ts`(domain)·`storage.ts`·`smoke.spec.ts` 는 SPEC 파일 목록에 없지만 SPEC 기능을 나눠 둔 것일 뿐이다. 금액 직접 입력은 없다(§11-3 지킴).

---

## 4. 개인정보

| 대상 | 판정 | 근거 |
|---|---|---|
| `web/` 커밋 대상 87파일 | PASS | AC-4 행. 얼굴 이미지 없음(`public/` 은 `charty-logo.svg` 하나, 폰트 woff2 하나) |
| `scripts/prepare-assets.mjs` 가드 | PASS | 가드 단어 6개(`:43`) · measure/render 화이트리스트(`:100-110`) · check-ignore 경고(`:184`) |
| `screens/` | PASS | `.gitignore:92` |
| **`reference/2026-10-21-charty-poc/테스트 보고서.html`** | **FAIL(F-2)** | gitignore 밖. 실명 1회, `https://m3d-ai-h5.migamedi.co.kr/h5?hash=<리포트 hash>` 1회. 구현 워커가 만든 파일이 아니다(fe-report 에도 그렇게 적혀 있다). 고칠 방향: `.gitignore` 에 `reference/2026-10-21-charty-poc/*.html` 을 넣거나 파일을 지운다 |
| work 문서(SPEC·report 류) | PASS | 리포트 hash 0. 걸린 것은 필드 이름뿐 |

---

## 5. 동기화 · 가격 경계

| 항목 | 판정 | 근거 |
|---|---|---|
| 항목가 반올림 · VAT · 최종 | PASS | `pricing.ts:30-50` 이 stg `currency-format.ts:66-70`·`cart-utils.ts:8-15` 와 한 줄씩 같다. 할인율 상수 = stg `currencies.ts:22`. 협찬 100% → `round(x*0)=0` |
| 할인 select 가 무료일 때 숨음 | PASS | `cart.tsx:78`(stg 와 같음). 무료 해제 뒤에는 이전 discount 가 남아 다시 적용된다 — stg 와 같은 동작 |
| 전체삭제 → 할인율 0 | PASS | `session-store.ts:104` |
| seq 단조 증가 · 새로고침 | PASS | 저장된 seq+1 로 hydrate(`use-tablet-sync.ts:15`). subscribe 는 ui 만 바뀐 것을 거른다(`:24`). 화면은 seq 0·'pending' 에서 시작한다 |
| 상담 초기화 | PASS | 새 sessionId 와 seq+1 → 화면이 받는다(`session-store.ts:119`) |
| sessionId 예외 | WARN | 위 차이 8 |
| 연결 판정 타이밍 | **FAIL** | AC-11 / F-1. 큰 화면 쪽은 1초 tick 이라 괜찮다(`use-screen-sync.ts:28,38`) |
| 재방문 전환 시 카트의 첫방문이벤트 제거 | PASS | `session-store.ts:113-117`(stg :58-66) |

---

## 6. 화면 문구

| 검사 | 판정 | 근거 |
|---|---|---|
| 「진단·질환·치료·환자」 — 화면 ① | PASS | 소스 grep 결과 주석 1줄뿐. 스크린샷 1~3 에도 없다 |
| 같은 낱말 — 태블릿 | W-6 | 추천 카드의 금기·부작용(taxonomy 원문)에 「치료 중인 사람」「고혈압 환자」 등이 있다(스크린샷 4). 상담사 화면이라 AC-17 범위 밖이지만, 고객이 태블릿을 같이 보는 장면이라면 문제가 될 수 있다 |
| 한자 | PASS | 소스에서 한자는 `__fixtures__` 원본 형태 재현과 테스트 단언에만 있다. 화면에 닿는 경로는 0 |
| `-1` | PASS | 점수가 없으면 `''`(점수 칸) 또는 `–`(대분류)로 보인다. 스크린샷에도 `-1` 은 없다 |

---

## 7. 코디에게

1. F-1 은 구현 워커에게 한 줄짜리로 되돌린다(tick 500ms · timeout 4s · e2e timeout 5s)
2. F-2 는 커밋 **전에** `.gitignore` 에 넣는다
3. 3417 실물 확인 때 볼 것: 잔주름 오버레이가 얼룩으로 보이는지(AC-21 · 차이 2), 태블릿 터치 크기(W-1)

---

## 재검수 (수정 1판 · `fix1-instructions.md` · fe-report 「수정 1판」)

- 직접 돌린 것: `npx vitest run` → 36 passed · `npm run lint` → 0건 · `npx tsc --noEmit` → exit 0
- 서버는 띄우지 않았다. e2e 는 코드로 읽었고, 화면은 새 스크린샷(12:50)으로 확인했다. 「verify exit 0 · Playwright 16 passed」는 fe-report 의 말이다

### 총평: **PASS**

| # | 항목 | 판정 | 근거 |
|---|---|---|---|
| 1 | **F-1 AC-11** | PASS | 판정 tick 을 ping 과 떼어 500ms 로 했다(`use-tablet-sync.ts:36-37`). 판정은 `now - lastPong < 4000`(`:48`, 상수 `channel.ts:62-63`). 최악 지연 계산은 내 계산과 같다: 마지막 pong p ≤ 닫은 시각 c → 첫 tick T 는 T ≤ p+4.5 ≤ c+4.5초 < 5초. 연결 중에는 pong 간격 2초 < 4초라 깜빡임이 없다. e2e timeout 도 `5 * SEC` 로 돌아왔다(`e2e/sync.spec.ts:113`). 큰 화면 쪽 5초(SPEC §4-3)는 그대로다 |
| 2 | **잔주름이 「선」으로 보이는가** (AC-21) | PASS | blur 를 없애고, 풀해상도에서 굵힌 뒤 칸별 최댓값으로 줄인다(`prepare-assets.mjs:128-160`, gain 3 복귀, 매니페스트 `dilate:15`). `overlay-fine-wrinkle.png`: 이마·미간·눈밑·눈가에 짧은 **선분**으로 보인다. 1판의 방울은 없어졌고 위치도 같다. `overlay-deep-wrinkle.png`: 팔자·마리오넷이 선으로 나온다. ⚠ 경미: 왼쪽 팔자 위에 옅은 주황 띠가 넓게 깔려 있다. 이것은 원본 마스크의 약한 값이 굵어진 것이다. 실물에서 거슬리면 알파 문턱으로 자를 일이지 이번 판정을 바꿀 것은 아니다. `erode` 를 「흰 선 굵히기」로 쓴 근거는 워커가 잰 값뿐인데, 스크린샷에서 선이 굵어진 것으로 결과가 확인된다. AC-20 은 잔주름↔굵은주름 1.11% > 1% 이고 여유가 얇다(워커 측정치) |
| 3 | **W-1 터치 32px** | PASS | `4-tablet.png` 에서 할인 select·무료·삭제·할인율 버튼(2열 그리드가 됨)·칩·필터·탭·고객 바가 모두 커졌다. e2e `fix1 W-1·W-2`(`sync.spec.ts:196-`)는 `data-scale=1` 을 먼저 확인한 뒤 19종 선택자와 체크리스트 칩의 실제 높이를 잰다. 31.5px 미만이 0건이어야 통과한다. 단언이 느슨하지 않다 |
| 4 | **W-2** | PASS | 대분류 4칸에 `GradeBadge` 가 들어갔다(`analysis-panel.tsx:24-30`, 스크린샷 확인). 측정치는 `slice(0, 2)`(`:56`). 그 결과 굵은주름 좌/우가 3줄에서 2줄로 줄었다(광대고랑 빠짐). SPEC 「측정치 2개」 그대로이고, AC-16 의 ⓘ 단언도 2개로 맞췄다(`sync.spec.ts:175`) |
| 5 | **W-3** | PASS | `setFilter` 가 `focusItem: null` 을 같이 넣는다(`session-store.ts:106`). 큰 화면 `filter:set` 도 같은 함수를 지난다(`use-tablet-sync.ts:31`). `toggleFocusItem` 은 그대로다. e2e `fix1 W-3`(`sync.spec.ts:178-194`)이 큰 화면과 태블릿 양쪽에서 C 강조·B 테두리·A2·태블릿 선택 해제를 확인한다 |
| 6 | **테스트 빈틈** | PASS | AC-15 가 큰 화면 필터 7개를 다 돈다(`sync.spec.ts:158`). 태블릿 4탭에 `-1` 단언을 넣었다(`:171`). AC-16 정규식에 `좌\/우` 가 들어갔다(`:165`) |

남은 것(판정 밖): W-6 은 코디 결정으로 그대로 둔다. F-2 는 코디가 처리했다고 들었고 여기서는 확인하지 않았다. 굵은주름의 옅은 띠는 실물 확인 때 본다.

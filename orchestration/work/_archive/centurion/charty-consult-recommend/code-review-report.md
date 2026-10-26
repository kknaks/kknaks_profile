# code-review-report — charty-consult-recommend (code reviewer, read-only)

- 기준: SPEC.md + fe-brief §2 + **layout-fix-brief.md(우선)** + _RESUME §2
- 대상: `git diff HEAD -- reference/` + untracked(`reference/2026-10-21-charty-poc/web/`, 이하 `web:`)
- 코드·문서는 고치지 않았다. e2e 는 3417 기존 서버 재사용으로만 돌렸다(서버를 끄거나 재시작하지 않았다). e2e 의 스크린샷 시험이 `screens/*.png` 를 다시 썼다(내용은 같은 화면이고 gitignore 대상이다)

## 판정: **FAIL** (FAIL 1 · WARN 6 · 참고 6) — 고칠 것은 한 줄

**F-1**: 리뷰어 e2e 실행에서 **R-13 이 실패했다**(`forehead cx` 오차 1.16px, 기준 < 1). 원인은 투영이 한 프레임 늦는 것이다. 회전 중 점이 피부에서 미끄러지는 실제 결함이기도 하고, `npm run verify` 를 불안정하게 만든다. 고치는 데는 한 줄이면 된다(§7 F-1).
그 밖의 기능 계약(R-1~R-12 · R-14~R-24)은 코드와 시험으로 확인했다. layout-fix 정정도 지켜졌다. 나머지는 시험이 약한 자리, R-25 미실행, 측정값 없음 상태의 칩 잘림 가능성, 그리고 사용자가 실물에서 만날 가독성 문제다.

## 1. 검증 명령

| 명령 | 결과 |
|---|---|
| `npm run lint` | 통과(출력 0) |
| `npm run test` | **7 파일 · 66 통과**. 실측 `measure.json` 이 있어서 `areas.test.ts` 「실제 측정값」 describe 가 skip 되지 않고 돌았다(`R-1 대표 점수 · 등급 ✓`) |
| `npx playwright test`(3417 재사용) | **31 통과 · 1 실패(R-13)** · 3.1분. 실패: `areas.spec.ts:197` `forehead cx` — `Expected < 1 · Received 1.1621636301061926`. 로그: `az -75.0 hidden sebum,cheek,poreTexture` · `az 75.0 hidden eye,nasolabial` · `anchorMs 평균 0.183ms`. 워커 실행(32/32)에서는 통과했으니 **불안정(flaky)**하다 |
| `npm run build` | 돌리지 않았다(브리프 §3) |

## 2. R-1 ~ R-25 대조 (코드·시험 직접 확인)

| R | 판정 | 근거 |
|---|---|---|
| R-1 | PASS | `web:src/domain/areas.test.ts:17-60`. 픽스처와 실측 둘 다 대표 점수·등급을 `toEqual` 로 단언한다. 최솟값은 `areas.ts:124-125`(`score>=0` 만, −1 제외). sebum `count 5470` 단언 |
| R-2 | PASS | `areas.test.ts:63-80` 필터 7 × strong/dim/match 를 §2-3 표와 전부 대조한다(빈 단언 없음) |
| R-3 | PASS | `areas.test.ts:82-85` 필터 7개 각각에서 focusItem 이 우선한다 |
| R-4 | PASS | `hub-snapshot.test.ts:10-22`: 칩 19 · 노드 16 · modality 8 · 프로필 필드 |
| R-5 | PASS | `hub-snapshot.test.ts:24-36`. 상향 대체 구현 `hub.ts:178-205`(item → modality, subcategory 는 extracted null 이라 건너뜀) |
| R-6 | PASS | `hub-snapshot.test.ts:45-58`. 직접 확인: 한자 0 · 이메일/전화 0 · URL 은 출처 1개뿐 |
| R-7 | PASS | `e2e/areas.spec.ts:30-56`. 좌3/우3 순서 · 오른쪽 열 testid 4개 visible · `focus-card` 0 · 패널 안 · 칩 bottom ≤ 카드 bottom · 칩 높이 ≥ 44 |
| R-8 | PASS | `areas.spec.ts:58-69` |
| R-9 · R-10 · R-11 | PASS | `areas.spec.ts:71-100`. `expectStrong` 이 6장 전부를 strong/dim 으로 단언한다 |
| R-12 | PASS | `areas.spec.ts:162-176`. 「C 구역」은 layout-fix §3 대로 캔버스 x 256–784 · y 0–848 로 다시 정했다. 교차는 polyline 의 모든 선분 쌍을 검사한다 |
| R-13 | **FAIL(F-1)** | `areas.spec.ts:178-205`. 리뷰어 실행에서 cx 오차 1.16px 로 실패했다. 이동량(>10px) 조건은 통과했다 |
| R-14 | **PASS(시험 약함 → W-1)** | `areas.spec.ts:207-229` |
| R-15 | PASS | 단위 `anchors.test.ts:6-11` + e2e `areas.spec.ts:231-249`(manifest 바꿔 끼움 → `leader-lines` 0 · 카드 6 · warn 1) |
| R-16 | PASS | `areas.spec.ts:251-264`: SVG `opacity` 속성 = `anchors().opacity`, `anchorMs < 2` |
| R-17 ~ R-21 | PASS | `areas.spec.ts:271-349`. R-17 은 태블릿 innerText 가 전후로 같은지 본다. R-21 은 칩 19개를 실제로 하나씩 연다 |
| R-22 | PASS | `git diff --stat HEAD` 변경 파일 10개 안에 `tablet/`·`stores/`·`sync/`·`recommend-rules.ts`·`data/mock/` 없음. `sync.spec.ts` AC-12(가격 표시)는 HEAD 그대로 |
| R-23 · R-24 | PASS | `sync.spec` AC-15·16·17 · `viewer.spec`(diff 0줄) HEAD 그대로 통과 |
| R-25 | **부분(W-3)** | `git status --porcelain -uall` 에 `m3d`·`screens`·이미지 0건. `.gitignore:97`(m3d) · `:99`(screens) 가 적용된다(`git check-ignore -v` 로 확인). **`public/m3d` 없이 빌드하는 시험은 아무도 돌리지 않았다** |

## 3. layout-fix 정정 — PASS

- 오른쪽 열 6파일(`overview-section`·`items-section`·`plan-panel`·`radar-chart`·`score-bars`·`use-tween`)은 `git diff --quiet HEAD` 로 **HEAD 와 같다**
- `screen-view.tsx` diff 는 추가만 있다(오른쪽 열 · `ReportPlaceholder` · `report-missing` 은 그대로). `viewer.spec.ts` 는 diff 0
- `sync.spec.ts` 는 focus-card/region-map 단언 2곳만 카드 `data-state`/`data-match` 로 바꿨다(:83-85 · :188-189). 대체 단언도 실제 조건을 건다
- 지운 것의 전수: HEAD 에서 `git grep` 해 보니 `face-region-map` 을 쓰는 곳은 `focus-card.tsx:1` 하나, `gradeSentence` 를 쓰는 곳은 `focus-card.tsx:3` 하나다. 그래서 **focus-card 전용만 지웠다.** 지금 트리에 남은 참조는 주석 1개와 R-7 의 「0개」 단언뿐이다. (SPEC §1-3 에는 `recommend-rules.test.ts:6` 이 `gradeSentence` 를 쓴다고 적혀 있지만 HEAD 에는 그런 줄이 없다. 지워도 문제없다)

## 4. 3D 투영 · 가림 · `__faceViewer` · 리렌더

- 매 프레임 React state 를 바꾸지 않는다. `anchor-projector.tsx:59-100` 은 `setAttribute` 만 쓰고, 임시 Vector3 는 `useMemo` 로 한 번만 만든다. `ms.list` 는 120개로 상한이 있다. ✓
- 가림 판정: 뒷면은 `facingOpacity`, 화면 밖과 raycast(`far=dist`, 2mm) 도 본다. drei `<Bvh firstHitOnly>` 로 감쌌다(`face-canvas.tsx:149`). 메시에 pointer 핸들러가 붙어 r3f 가 pointermove 마다 raycast 하지만 BVH 라서 부담이 적다. ✓
- `__faceViewer`: Controls(`face-canvas.tsx:184`)와 AnchorProjector(`anchor-projector.tsx:45`) 둘 다 `Object.assign` 으로 덧붙이고, `applied` 는 키가 있을 때만 쓴다(`:123`). 서로 덮어쓰지 않는다(W-10 ✓)
- LeaderLines 는 리렌더마다 ref 콜백으로 슬롯을 다시 등록한다. 이때 `cur`·`end` 를 이어 받으니 깜빡임은 없다 ✓

## 5. Hub 스냅샷 — PASS(참고 1)

- `meta`: source · endpoints · `fetchedAt 2026-10-26T05:19:51Z` · procedure-profiles `3.3 (2026-07-26)` · sha256 2개. 모달 바닥에 「Procedure Hub(stg) · 2026-10-26 받음 · 목업 · 의학적 근거 아님」(`hub.ts:213-216`, KST 날짜)
- 개인정보 0. 프로필은 5필드만 담았다. 제품·패키지·가격·금기 매트릭스는 없다
- 받지 않는 refs 를 주면 파일을 쓰기 **전에** 종료 코드 1 로 끝난다(`fetch-hub.mjs:67-74`). 그래서 스냅샷을 덮어쓰지 않는다 ✓
- 참고 N-1: 화면에 쓰지 않는 `indications.extended` · `related_techniques` 가 원문 그대로 남아 있다(1,775B). SPEC §4-2 에 「`extended` 안 씀」이라고 되어 있어 빼도 된다. 막는 문제는 아니다

## 6. 「목업 · 의학적 근거 아님」 · 태블릿 회귀 — PASS

- 이 문구는 범례 줄(`viewer-area.tsx:63`, `COPY.mockNote`) · 모달 바닥 · `areas.ts:1` · `hub-refs.json._note` 에 있다
- 태블릿 코드 diff 0. 가격 토글 → 화면 ① 플랜 가격은 HEAD 와 같다(`sync.spec` AC-12 그대로 통과)

## 7. FAIL · WARN — 고칠 것

**W-1 R-14 시험이 방향을 확인하지 않는다** — `e2e/areas.spec.ts:206,213-214`
`far` 를 「숨은 점이 있는 쪽」으로 고른다. 그래서 가까운 쪽 점이 숨어도 시험이 통과한다. 지금 동작은 맞다(로그 기준 −75° → sebum·cheek·poreTexture, +75° → eye·nasolabial). 하지만 시험이 그 조건을 단언하지 않는다.
→ 고칠 내용: `for (const [dx, far] of [[1300, <먼 쪽 키>], [-1300, <먼 쪽 키>]])` 처럼 드래그 방향마다 기대하는 쪽을 고정하고, `hidden ∩ far ≥ 1` 을 단언한다.

**F-1 (FAIL) 지시선 점이 한 프레임 늦다 → R-13 불안정** — `anchor-projector.tsx:59-66`
`tmp.ndc.project(camera)` 는 `camera.matrixWorldInverse` 를 쓴다. 그런데 이 값은 `gl.render` 안에서 갱신되므로, OrbitControls 가 이번 프레임에 바꾼 카메라가 아니라 지난 프레임의 행렬이다. 드래그 중에는 점이 피부보다 1프레임 뒤처져 미끄러져 보인다. R-13 은 `page.evaluate` 로 `project()` 를 부르는데, 이때는 렌더 뒤라 행렬이 이미 새것이다. 그래서 damping 이 아주 조금이라도 남아 있으면 SVG 점(옛 행렬)과 투영(새 행렬)이 벌어진다. 리뷰어 실행에서 1.16px 로 실패한 것이 이 경우다.
→ 고칠 내용: `AnchorProjector` 의 `useFrame` 첫 줄에 `camera.updateMatrixWorld()` 를 넣는다(OrbitControls 는 priority −1 이라 그 전에 끝난다). 고친 뒤 R-13 을 2–3회 반복해 통과하는지 확인한다(`npx playwright test e2e/areas.spec.ts -g R-13 --repeat-each 3`). 시험 기준(1px)은 바꾸지 않는다.

**W-3 R-25 「public/m3d 없이 build」 미실행**
fe-report 가 이미 밝혔다. 코디가 m3d 를 잠시 다른 곳으로 옮기고 `npm run build` 를 한 번 돌리거나, dev 서버와 겹치지 않는 시점에 확인해야 닫힌다.

**W-4 측정값 없음 상태에서 칩이 잘릴 수 있다** — `area-card.tsx:48`(`overflow-hidden`) · `:59-63`
측정 JSON 이 없으면 카드 6장마다 긴 `COPY.reportMissing`(「측정 데이터가 없습니다 — npm run prepare:assets 를 먼저 실행하세요」)이 안쪽 폭 208px 에 3–4줄로 들어간다. 이 자리 아래에 칩 2줄이 오면 카드 높이 약 267 을 넘을 수 있다(특히 눈가 4칩 · 볼/코 5칩 · 모공 4칩). W-12 의 「칩 잘림 0」 시험은 ready 상태에서만 돈다.
→ 고칠 내용: 카드 안 문구는 짧게(예: 「측정 데이터 없음」) 쓰고, 긴 안내는 오른쪽 열 `ReportPlaceholder` 에 이미 있으니 그쪽에 맡긴다(`viewer.spec` AC-23 은 `.first()` 라 그대로 통과한다). 아니면 이 상태에서도 칩 잘림을 e2e 로 단언한다. 시연 데이터에서는 이 상태가 나오지 않는다.

**W-5 흐린 지시선이 거의 안 보인다** — `anchor-projector.tsx:17`(`DIM 0.3`) · `leader-lines.tsx:68`(2px)
`screens/natural.png`·`filter-pore.png` 에서 보면, 흐린 카드의 선이 어두운 바탕과 흰 점 오버레이 위에서 사실상 사라진다. 「피지 세균」 필터에서는 선 6개가 모두 옅다. SPEC 수치(0.3)대로라 결함은 아니고 사용자 확인이 필요한 자리다. 대안: 흐린 선을 0.45 로 올리거나, 흐린 선에 dash 를 준다.

**W-6 모달 가독성** — `procedure-modal.tsx:58,101`(`text-ms-gray-500`) · `:84,110`
- 「◯◯ 전체 기준」이 흰 바탕 회색 16px 라 잘 안 보인다(`screens/modal-vbeam.png`)
- 오른쪽 열이 넘치면 「시술 후 관리」가 바닥에서 반쯤 잘린 채 보이는데, 스크롤된다는 신호(그림자·화살표)가 없다. 대형 화면은 터치·휠 사용이 드물어 닫힌 내용으로 오해할 수 있다. 대안: 모달 높이를 880까지 다 쓰거나(지금은 내용 높이), 아래 페이드를 둔다
- 「닫기」 버튼이 `size="m"` outlined 라 1920 화면에서 작다

**W-7 카드 하단 빈 공간 · 긴 지시선**(배치 결과, fe-report 에도 있음)
- 카드는 flex-1 로 약 267px 인데 내용은 위 55% 쯤이다. 이마/미간 · 피지 카드는 아래 절반이 비어 있다
- 이마/미간 선(L1 끝 → 미간)과 피지 선(R1 → 이마 오른쪽)이 정면에서도 눈썹·이마를 대각선으로 길게 가로지른다. 30°에서는 눈가 선이 눈 위를 지난다(`rotate-30.png`)
- 드래그 회전은 가운데 528px 안에서만 먹는다. 카드 사이 빈틈을 끌면 돌지 않는다

## 8. 참고 (고치지 않아도 됨)

- N-1 스냅샷에 쓰지 않는 필드가 있다(§5)
- N-2 `leader-lines.tsx:31-34` 가 렌더 중에 모듈 레지스트리(`slot.strong`)를 바꾼다. 동작은 하지만 render 부수효과다. ref 콜백(`reg`)이 같은 값을 이미 넣으므로 이 루프는 지워도 된다
- N-3 `procedure-modal.tsx:69-73`: `onClose` 가 `screen-view.tsx:74` 에서 인라인이라, 리렌더(태블릿 스냅샷)마다 keydown 리스너를 다시 붙인다. 문제는 없다
- N-4 `viewer-area.tsx:45` `panelOffset={[FACE_X0, 0]}` 이 렌더마다 새 배열이다. AnchorProjector 는 이 값을 deps 로 쓰지 않아 영향이 없다
- N-5 SPEC §2-5 의 `area-column.tsx` 는 파일로 만들지 않고 `viewer-area.tsx` 의 `Column` 으로 넣었다. 계약 testid(`area-col-left/right`)는 그대로다
- N-6 모달이 헤더까지 덮는다(`screen-root` 의 `absolute inset-0`). SPEC §4-1 「화면 ① 전체 위」와 맞다

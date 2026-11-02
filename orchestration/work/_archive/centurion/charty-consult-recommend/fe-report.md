# fe-report — charty-consult-recommend (frontend 워커)

- 범위: `reference/2026-10-21-charty-poc/web/` · 기준: SPEC.md + fe-brief §2 보정 + **layout-fix-brief.md(배치 정정, SPEC §0·§1 보다 우선)**
- 결과: WP1~WP6 완료 · **`npm run verify` 통과**(lint 0 · 단위 7파일 66 · build · e2e 32/32, 3417 dev 서버 재사용 · 끄거나 재시작하지 않음) · 커밋 안 함

## 진행 기록
- WP1 ✓ hub-refs.json(칩 19 · 노드 16) · `scripts/fetch-hub.mjs`(`npm run hub:snapshot`, `--refs`) · hub-snapshot.json 49,607B(taxonomy sha256 7e92abcd…ee68f6 — SPEC 값과 같음) · `data/hub/hub.ts` · `domain/areas.ts` · 단위 `areas.test.ts`·`hub-snapshot.test.ts` 통과(R-1~R-6). 잘못된 hubId refs → 종료 코드 1 + 후보 출력 · 두 번 실행 diff = `fetchedAt` 한 줄
- WP2 ✓ 화면 ① 배치(좌 400 · C 1024 · 우 400) · `area-card`·`area-column` · 범례 줄(`viewer-legend`, 「목업 · 의학적 근거 아님」) · 삭제 8파일 · `gradeSentence` 삭제(W-9) · e2e 고침(sync 8 · viewer AC-23) 12건 통과 · 새 `e2e/areas.spec.ts` R-7~R-11 통과(칩 잘림 없음·높이 ≥44 포함) · `screens/natural.png`·`filter-pore.png`
- **배치 정정(10-26 코디 `layout-fix-brief.md`)**: 오른쪽 열(한눈에 보기·항목별 상태·플랜)과 그것이 쓰는 6파일(`overview-section`·`items-section`·`plan-panel`·`radar-chart`·`score-bars`·`use-tween`)·`screen-view`·`sync.spec`·`viewer.spec` 을 HEAD 로 되돌림. `focus-card`·`face-region-map`(focus-card 전용)·`gradeSentence` 는 지운 채. 카드는 뷰어 패널 안 좌 3 / 우 3(열 폭 240 · 여백 16 · 간격 12), 3D 캔버스는 두 열 사이 x 256–784(528×888), 카메라 HOME 0.55 → 0.70
- WP2(재) ✓ `viewer-area` 안 카드 열 · `viewer-layout.ts`(좌표 상수) · 카드 = 부위명·등급·대표 점수 1개·칩(하위 지표 줄 뺌) · sync.spec focus-card/region-map 단언 2곳 → 카드 `data-state` · e2e sync 9 · viewer 4 · areas 6 통과 · `screens/natural.png`·`filter-pore.png` 갈아끼움
- WP3 ✓ 찍기 도구(`?anchors=edit`, `anchor-editor.tsx` — 라디오 6 · 값 표 · [복사] · [초기화]) · `__faceViewer.pickAt(cx, cy, key?)`(W-4) 로 정면 스크린샷 → 캔버스 px 6점 → `src/data/face-anchors.ts` · 메시 가드 `anchorsUsable` + `console.warn` 1회 · `anchorEditEnabled` 단위 테스트(W-5) · `next build` 후 `.next/static` 에 편집 패널 문구(「앵커 찍기 도구」·`anchor-pick-`) 0건 · `screens/anchors-front.png`
- WP4 ✓ `anchor-projector.tsx`(useFrame 에서 투영·뒷면·raycast 가림·스무딩, SVG 는 `setAttribute` 직접) · drei `<Bvh firstHitOnly>` · `leader-lines.tsx`(뷰어 패널 기준, 무릎 얼굴 쪽 32px) · `__faceViewer` 는 `Object.assign`(Controls 포함, W-10) — `anchors()`(opacity=최종 · occlusion=가림, W-7) · `anchor3d` · `anchorMs` · `canvasSize` · e2e R-12~R-16 통과 · `anchorMs` 평균 0.17ms(swiftshader) · `screens/rotate-30.png`(29.1°)
- WP5 ✓ `procedure-modal.tsx`(화면 ① 루트 `absolute inset-0` 오버레이 · 1040×≤880 · 2열 · ✕/바탕/Esc · 상향 표기 「◯◯ 전체 기준」 · 바닥 출처 줄) · 칩 연결 · e2e R-17~R-21 통과 · `screens/modal-vbeam.png`·`modal-fractional.png`
- WP6 ✓ `npm run verify` 한 번 — 통과(e2e 32: areas 16 · smoke 3 · sync 9 · viewer 4, 3.0분). 끝난 뒤 `next build` 가 바꾼 `next-env.d.ts` 는 되돌림

## R-1 ~ R-25 확인 표

좌표는 **뷰어 패널 기준 설계 px**(패널 왼쪽 위 원점, 1040×984). 「C 구역」 = 두 카드 열 사이 = 3D 캔버스 **x 256–784 · y 0–848**(범례 줄 위).

| R | 결과 | 근거 |
|---|---|---|
| R-1 | PASS | `areas.test.ts` — 실측 88.3 good · 61.4 moderate · 80.7 mild · 67 moderate · 68.8 moderate · null none(5,470개) + 픽스처(90 · 50 · 70 · 60 · 59.9 · null) |
| R-2 | PASS | `areas.test.ts` 필터 7개 × strong/dim/match 가 §2-3 표와 같음 |
| R-3 | PASS | `areas.test.ts` focusItem dermatoglyph → 모공만, brightness → 볼/코만(필터 7개 모두) |
| R-4 | PASS | `hub-snapshot.test.ts` — hubId 16 전부 nodes · modalityId 전부 modalities · 프로필 8 |
| R-5 | PASS | `modalSections('M8-4-1')` contraindications=M8 · mechanism=M8-4-1, `M8-2` 전부 M8 |
| R-6 | PASS | onset·safety 하위 키 §4-2 밖 0 · 한자 0 · `fetchedAt`·`sha256.taxonomy`(7e92abcd…ee68f6) |
| R-7 | PASS | e2e — 카드 6장이 `screen-viewer` 안 좌(이마·눈가·팔자)/우(피지·볼코·모공) · 오른쪽 열 `screen-overview`·`screen-items`·`screen-plan`·`score-bars` 보임 · `focus-card` 0 · 칩 잘림 0 · 칩 높이 ≥44 |
| R-8 | PASS | e2e — strong 4/dim 2 · `data-value` 61.4·80.7·67·68.8·88.3·'' · 피지 「점수 없음」「5,470개」 |
| R-9 | PASS | e2e — 태블릿 모공 → 모공만 strong · 화면 피지 세균 → 6장 dim · 피지만 match |
| R-10 | PASS | e2e — 피부결 항목 → 모공만 · 화면 붉은기 → 볼/코만 |
| R-11 | PASS | e2e — 화면 새로고침 뒤 굵은 주름 · 눈가·팔자 strong · 태블릿 카트 유지 |
| R-12 | PASS | e2e — 정면 6점 visible · C 구역 안 · 꺾은선 교차 0 · `screens/anchors-front.png` |
| R-13 | PASS | e2e — 29.1° 회전, 6점 모두 10px 넘게 이동 · SVG `cx/cy` = `project(anchor3d)`+캔버스 원점(256, 0) 1px 안 · `screens/rotate-30.png`(눈 확인: 점이 피부 자리에 붙어 있음) |
| R-14 | PASS | e2e — −75°: 숨음 sebum·cheek·poreTexture · +75°: 숨음 eye·nasolabial(opacity < 0.05, `data-visible=false`) · 카드 6장 보임 · 더블클릭 뒤 3초 안에 6개 visible |
| R-15 | PASS | 단위 `anchorsUsable` + e2e — manifest `mesh.bytes+1` → `leader-lines` 0 · 카드 6 · 3D ready · `[anchors]` warn 1회 |
| R-16 | PASS | e2e — dim(이마·피지) ≤ 0.3 · strong ≥ 0.9 · SVG `opacity` = `anchors().opacity` · `anchorMs` 평균 0.17ms(< 2ms, W-6) |
| R-17 | PASS | e2e — 눈가 보톡스 `M1-3-1` · 5섹션 · 받으면 안 되는 경우/시술 시간 「보톡스 전체 기준」 · 10–15분 · 마취 없음 · 태블릿 글자(시계 뺌) 그대로 |
| R-18 | PASS | e2e — 「레이저 › 혈관 › 브이빔」 · 원리 본문 = 스냅샷 M8-4-1 mechanism · 레이저 전체 기준 · `screens/modal-vbeam.png` |
| R-19 | PASS | e2e — 「레이저 › 프락셔널」 · 모든 섹션에 레이저 전체 기준 · `screens/modal-fractional.png` |
| R-20 | PASS | e2e — ✕ · 바탕 · Esc 닫힘 · 열린 채 태블릿 모공 → 모달 유지, 뒤 카드만 바뀜 · 출처 줄 「Procedure Hub(stg) · 2026-10-26 받음 · 목업 · 의학적 근거 아님」 |
| R-21 | PASS | e2e — 칩 19(노드 16) 차례로 열림 · 한자 0 · `procedure-hub` 요청 0 |
| R-22 | PASS | HEAD 대비 `src/components/tablet/`·`stores/`·`sync/`·`recommend-rules.ts`·`data/mock/` 변경 0줄. 태블릿 시험(AC-5·6·7·14 · AC-11 · AC-12 가격 표시 · AC-18 · fix1 W-1·W-2)은 HEAD 그대로 통과. 배치 정정 §3 대로 가격은 HEAD 동작 |
| R-23 | PASS | `sync.spec` AC-15·16·17(HEAD 그대로) — 모달 닫힌 화면 ① 필터 7개에서 한자·−1·금지어·좌/우 0 |
| R-24 | PASS | `viewer.spec` AC-19·20·22·23 HEAD 그대로 통과(AC-20 최소 차이 fine↔deep 1.33%) |
| R-25 | **부분** | `npm run build` 통과 · `git status --porcelain` 에 `public/m3d/`·`screens/` 없음. **`public/m3d` 없이 빌드는 못 돌렸다** — 읽기 전용이라 옮기지 못했고, 복사본 빌드는 Turbopack 이 node_modules 경로에서 거부했다. 대신 `src`·`next.config` 에서 `public/m3d` 를 빌드 때 import 하는 곳 0건(주석 3곳 · 런타임 fetch 만)을 grep 으로 확인 |

## 스펙과 다르게 한 것
1. **배치**: layout-fix-brief 대로 한다. 오른쪽 열과 그것이 쓰는 6파일은 HEAD 로 되살렸다. 카드는 뷰어 안 좌3/우3에 두고, 열 폭 240 · 바깥 여백 16 · 간격 12 · 카드 높이 약 267 이다. 카드에는 하위 지표 줄을 빼고 대표 점수 1개만 둔다
2. **3D 캔버스를 두 열 사이(528×888)로 좁혔다.** 처음엔 패널 전체(1040) 그대로 두고 카메라만 0.55 → 0.70 으로 물렸다. 그러자 얼굴이 캔버스에서 차지하는 비율이 줄어 `viewer.spec` AC-20(필터 그림 차이 > 1%)이 0.68% 로 떨어졌다. 시험은 고치지 않고 캔버스를 좁혀 1.33% 로 되돌렸다. 카메라 HOME 은 0.70(리셋 위치도 같음)
3. 지시선 카드 쪽 끝점 = 카드 top **+ 30**(SPEC +40). 카드 부위명 줄 가운데가 30이다
4. `__faceViewer.anchors()` 좌표는 본문이 아니라 **뷰어 패널 기준**이다. `pickAt(cx, cy, key?)` 는 key 를 주면 앵커로 저장한다. 덧붙인 키: `anchorFile()`([복사] 본문) · `canvasSize()`
5. 스냅샷 `profile` 은 화면에 쓰는 5필드만 담는다(id·name·durationMin·durationMax·needsAnesthesia, 원문 값 그대로). modality 단계 노드의 `extracted` 는 `modalities` 쪽에만 두고 `nodes` 에는 null 로 둔다(중복 제거). 결과 49,607B
6. `fetch-hub.mjs` 가 더 하는 일: 칩의 `problemItems` 이름이 Hub 고민 항목에 실제로 있는지 검사한다. 이름 후보가 없으면 id 앞부분이 같은 형제 노드를 후보로 낸다(예: `M8-4-999` → M8-4-1 브이빔 …)
7. `area-cards` testid 는 본문 전체가 아니라 **뷰어 안 두 카드 열을 감싼 요소**에 붙는다
8. `gradeSentence` 는 쓰는 곳이 없어져 지웠다(W-9). `face-region-map` 은 focus-card 전용이라 지운 채 둔다

## 남은 것
- 코디 실물(3417) 확인 두 가지: 회전 중 프레임을 눈으로 보는 것, 앵커 6점 자리를 사용자에게 확인받는 것(§6-7, `screens/anchors-front.png`)
- R-25 「m3d 없이 빌드」 실행(위)
- `.gitignore`(screens/) 는 코디가 이미 수정해 둔 상태 그대로다
- 「목업 · 의학적 근거 아님」 문구는 범례 줄과 모달 바닥에 있다

## 사용자가 실물에서 만날 만한 어색한 자리
- **얼굴이 이전보다 작다**(카메라 0.55 → 0.70). 드래그 회전은 가운데 528px 구역에서만 먹고, 카드 위를 끌면 돌지 않는다. 돌리면 볼이 카드 가장자리에서 잘린다
- 카드가 약 267px 높이인데 내용은 위쪽 절반 정도라 **카드 아래가 비어 보인다**(특히 이마/미간 · 피지/트러블)
- 흐린 카드(이마 · 피지)의 지시선은 opacity 0.3 이라 어두운 바탕에서 거의 안 보인다. 「피지 세균」 필터에서는 6장이 모두 흐려 선도 전부 옅다
- 피지 카드는 배지와 점수 줄이 둘 다 「점수 없음」이라 같은 말이 두 번 나온다
- 「바이오스티뮬레이터/콜라겐부스터」 칩은 두 줄로 꺾인다
- 30° 넘게 돌리면 지시선이 얼굴을 길게 가로지른다. 이마/미간 선은 정면에서도 왼쪽 눈썹 위를 지난다
- −75° 에서는 R1(피지 · 이마 T존) 점도 같이 숨는다
- 모달:
  - Hub 원문을 그대로 쓰므로 「치료 · 질환 · 환자」가 나온다(§6-5 기본값)
  - 프락셔널레이저는 모든 섹션이 「레이저 전체 기준」이다. 소개 문단도 레이저 전체 설명이라 프락셔널 이야기가 아니다
  - 「◯◯ 전체 기준」 글자는 회색이라 잘 안 보인다
  - 긴 노드(V빔 등)는 오른쪽 열을 스크롤해야 「시술 후 관리」가 보인다
- 태블릿 「가격 표시」 토글은 HEAD 대로 다시 동작한다(SPEC §6-4 무효)
- dev 서버에서는 왼쪽 아래에 Next 개발 표시(N)가 보인다. 빌드에서는 안 보인다
- e2e R-13 은 단계 회전이라 약 48초 걸린다

## 산출 파일
- 새로 만든 것:
  - `scripts/fetch-hub.mjs`
  - `src/data/hub/{hub-refs.json, hub-snapshot.json, hub.ts, hub-snapshot.test.ts}`
  - `src/domain/{areas.ts, areas.test.ts}`
  - `src/data/face-anchors.ts`
  - `src/components/screen/{area-card, leader-lines, procedure-modal}.tsx` · `viewer-layout.ts`
  - `src/components/viewer/{anchors.ts, anchors.test.ts, anchor-store.ts, anchor-projector.tsx, anchor-editor.tsx, use-anchor-edit.ts}`
  - `e2e/areas.spec.ts`
- 고친 것:
  - `package.json`(`hub:snapshot`)
  - `screen-view.tsx` · `viewer-area.tsx`
  - `face-canvas.tsx` · `face-viewer.tsx`
  - `copy.ts`(`mockNote` 추가 · `gradeSentence` 삭제)
  - `e2e/sync.spec.ts`(focus-card/region-map 단언 2곳)
- 지운 것: `focus-card.tsx` · `charts/face-region-map.tsx`
- `screens/`(gitignore): `natural.png` · `filter-pore.png` · `rotate-30.png` · `modal-vbeam.png` · `modal-fractional.png` · `anchors-front.png`

---

## 수정 1판 (code-review-report §7·§8 처리 · 2026-10-26)

| # | 결과 | 한 것 |
|---|---|---|
| F-1 | ✓ | `anchor-projector.tsx` useFrame 첫 줄에 `camera.updateMatrixWorld()`. OrbitControls(priority −1)가 옮긴 카메라 행렬로 같은 프레임에 투영한다. 시험 기준(1px)은 그대로. `--repeat-each 3` 3회 모두 통과(29.0° · 29.1° · 29.1°) |
| W-1 | ✓ | R-14 가 드래그 방향마다 먼 쪽을 고정한다. `+1300px → az < −70 · far = R2·R3(cheek·poreTexture)`, `−1300px → az > +70 · far = L2·L3(eye·nasolabial)`. 단언은 `hidden ∩ far ≥ 1`. 로그: `az -75.0 hidden sebum,cheek,poreTexture` · `az 75.0 hidden eye,nasolabial` |
| W-4 | ✓ | 측정값이 없을 때 카드 안 문구를 `COPY.reportMissingShort`(「측정 데이터 없음」)로 바꿨다. 긴 안내는 오른쪽 열 `ReportPlaceholder`(`report-missing`)가 맡는다. 카드 쪽 요소의 testid 는 `area-report-missing` 으로 바꿨다(아래 참고). 새 e2e 「W-4」: m3d 404 상태에서 카드 6장 짧은 문구 · 오른쪽 열에 prepare:assets 안내 · 6장 dim · 칩 잘림 0 |
| N-2 | ✓ | `leader-lines.tsx` 렌더 중에 레지스트리(`slot.strong`)를 바꾸던 루프를 지웠다. ref 콜백 `reg` 가 같은 값을 넣는다. R-16(dim ≤ 0.3 · strong ≥ 0.9)으로 확인 |
| W-5·W-6·W-7 | 손대지 않음 | 지시대로 2루프로 넘긴다 |

- **testid 를 바꾼 이유(W-4):** 카드에 `report-missing` 을 그대로 두면 `viewer.spec` AC-23 이 깨진다. AC-23 은 `getByTestId('report-missing').first()` 를 읽는데, DOM 순서상 뷰어(카드)가 오른쪽 열보다 앞이라 카드의 짧은 문구가 먼저 잡혀 FAIL 났다(1차 실행). 처음 W-1 에서 카드에 `report-missing` 을 둔 것은 오른쪽 열 `ReportPlaceholder` 가 지워졌기 때문이었다. 배치 정정으로 placeholder 가 되돌아왔으니 `report-missing` 은 원래 자리(placeholder)에만 둔다. 카드는 `area-report-missing` 을 쓴다. AC-23 은 고치지 않은 채 통과한다

### 명령 출력
```text
npm run lint   → exit 0 (경고 0)
npm run test   → Test Files 7 passed · Tests 66 passed
npx playwright test e2e/areas.spec.ts -g R-13 --repeat-each 3
  ✓ 1 R-13 (47.0s) azimuth 29.0° · visible 6
  ✓ 2 R-13 (52.6s) azimuth 29.1° · visible 6
  ✓ 3 R-13 (49.2s) azimuth 29.1° · visible 6
  3 passed (2.5m)
npx playwright test e2e/areas.spec.ts e2e/viewer.spec.ts
  areas 17(R-7~R-21 + W-4 + 스크린샷) · viewer 4(AC-19·20·22·23)
  21 passed (2.5m)
```
- 바꾼 파일: `src/components/viewer/anchor-projector.tsx` · `src/components/screen/leader-lines.tsx` · `src/components/screen/area-card.tsx` · `src/content/copy.ts` · `e2e/areas.spec.ts`
- 커밋 안 함 · 3417 서버 재사용(재시작 안 함). sync.spec 은 이번 범위 밖이라 돌리지 않았다

---

## 2루프 (사용자 눈 확인 피드백 + 검수 보류분 · 2026-10-26)

배치는 layout-fix-brief 그대로 두었다(오른쪽 3패널 유지 · 카드는 뷰어 안 좌3/우3).

### 항목별 결과

| # | 결과 | 한 것 · 근거 |
|---|---|---|
| U-1 카드 새 모양 · 탭 | ✓ | **머리**: 부위 확대 64px + 부위명·등급·대표 점수(세 줄). **시술 탭 한 줄**: 13px, h-32, 줄바꿈 없이 가로 스크롤하고 넘치면 오른쪽 끝을 흐린다. **고른 시술**: 사진 자리 56px + 이름(15px) + 간단 설명(13px, 3줄 말줄임) + 「Hub 원문 · ◯◯ 전체 기준」 + [자세히]. 카드마다 첫 탭이 기본 선택이다. 탭을 누르면 설명만 바뀌고 모달은 열리지 않는다. 선택 탭은 primary 채움으로 표시한다. [자세히]를 누르면 기존 `procedure-modal` 이 열린다. 흐린 카드에서도 둘 다 동작한다. e2e `U-1` · `R-17~R-21`(칩 → 탭+[자세히]) |
| 간단 설명 출처 | ✓ | `procedureSummary(hubId)` = 모달 머리 요약과 같은 값, 즉 노드의 `extracted.overview` 이다. item 에 없으면 modality 의 `extracted.overview` 로 상향 대체하고, 그때 「◯◯ 전체 기준」을 붙인다(예: 프락셔널레이저 → M8, `data-source="M8"`). 원문 그대로 3줄 CSS 말줄임이고 글자를 잘라 내지 않는다 |
| U-3 사진 자리 | ✓ | 회색 박스 + 그림 아이콘 + 「사진」. 데이터 자리는 `AreaChip.image?: string` 이다. `hub-refs.json` 칩에 `"image": "/경로"` 를 넣으면 그 사진을 그린다(지금은 없음). e2e `U-3·U-4` |
| U-4 부위 확대 사진 | ✓ | **UV**: 앵커 6점의 UV 를 `__faceViewer.anchorUv`(점 바깥 1cm 에서 법선 반대로 raycast → `hit.uv`)로 구해 `face-anchors.ts` 에 `uv` 로 같이 저장했다. **자르기**: `area-crop.tsx` 가 지금 필터 텍스처(`manifest.textures[FILTERS[f].texture]`)를 CSS `background-size/position` 으로 잘라 보인다. 이미지 px = (u·W, (1−v)·H)(three 기본 flipY), 반경 120 텍스처 px → 64px. **확인**: 자리가 맞는지 scratch 에서 sharp 로 잘라 봤다(미간·눈밑·팔자·이마 오른쪽·콧방울 옆 볼·입꼬리 옆 볼). 좌우는 텍스처와 화면이 같아 반전하지 않는다. 확인용 이미지는 지웠고, 잘라낸 이미지 파일은 저장·커밋하지 않았다. **오버레이 합성 ✓**: 주름·모공 필터는 오버레이 PNG 의 알파를 `mask-image` 로 써서 필터 색을 칠한다(셰이더와 같은 합성). **자리표시**: 측정 없음 · 에셋 없음 · `anchorsUsable=false` 면 회색 자리표시(`data-bg=""`, e2e `W-4`). e2e `U-3·U-4`: 6개 배경 지정, 모공 필터에서 `cool.jpg` + `pore.png`. 스크린샷 `loop2-crops.png` |
| U-2 카드 선택 | ✓ | 카드(빈 곳 포함)를 누르면 그 카드만 strong 이 되고 나머지는 dim(지시선 포함). 추천 불필요 카드도 고를 수 있다. 같은 카드를 다시 누르면 해제된다. 탭·[자세히]도 그 카드를 고른다(해제하지 않음). 화면 ① 필터를 누르면 해제되고, 태블릿에서 필터·항목이 바뀌어 와도 해제된다(고를 때의 `filter`·`focusItem` 을 같이 적어 두고 달라지면 무효). 3D 필터는 바꾸지 않고, 태블릿과 동기화하지 않는다. 고른 카드는 4px primary 외곽선 + `data-selected`. 단위 `areas.test.ts` U-2(필터 7개 × 카드 6) · e2e `U-2` · `loop2-card-selected.png` |
| W-5 흐린 선 | ✓ | dim 점·선 opacity 0.3 → **0.5**, 선은 **점선 `6 4`**. 「피지 세균」 필터(6장 dim)에서도 선이 보인다. R-16 기준을 0.45–0.55 + 점선으로 고쳤다 |
| W-6 모달 | ✓ | **표기**: 「◯◯ 전체 기준」을 회색 글씨에서 회색 바탕 배지(`ms-gray-200` · `ms-gray-800`)로 바꿨다. **스크롤 신호**: 내용이 넘치면 아래 페이드 + 「아래로 더 있어요」, 끝까지 내리면 사라진다(`modal-more`). **닫기**: `size="xl"`, 아이콘 24px. 함께 고친 버그: 1루프 모달 본문이 `h-full` 이라 스크롤이 안 되고 넘친 부분이 그냥 잘렸다 → `flex-1 min-h-0` 로 고쳤다. R-18 이 `modal-more` 를 단언한다. `loop2-modal.png` |
| W-7 여백 · 긴 선 | ✓ | **여백**: 새 카드 모양으로 카드 안이 차서 아래 빈 공간이 없다. **긴 선**: 맨 위 카드(L1 이마/미간 · R1 피지)는 지시선을 `'top'` 경로로 바꿨다. 카드 높이에서 얼굴 위 빈 곳을 가로로 지나 점 바로 위에서 수직으로 내려가므로 이마·눈썹을 대각선으로 가로지르지 않는다. 점이 무릎보다 카드 쪽에 오면(크게 돌린 경우) 원래 무릎 경로로 돌아간다. 카드 칸 순서와 앵커 자리는 그대로다. 단위 `anchors.test.ts` · R-12 교차 0 유지 |

### 스펙과 다르게 한 것 (2루프)
1. **카드 간단 설명의 금지어(코디 확정 A)**: 탭 19개 중 6개(V빔·IPL·엑셀V·피코토닝·프락셔널레이저·PDT)의 Hub overview 에 「치료」「질환」이 있어 구 AC-15·17(R-23)이 FAIL 났다. 원문은 그대로 두고 카드에 「Hub 원문」 출처를 표기했다. 금지어 검사(`sync.spec` AC-15·16·17)에서는 `area-summary` 만 숨기고 읽는다. 나머지 화면 ① 글자는 그대로 검사하고, 시험에 이유를 주석으로 남겼다. SPEC §6-5(모달)의 연장이다
2. **탭 높이 32px**(SPEC §2-4 칩 ≥ 44). 사용자가 「작은 글씨 한 줄」을 요청했고, 큰 화면은 터치가 드물다. R-7 은 「칩 높이 ≥44」 대신 「탭 한 줄 · 카드 안 잘림 0」을 단언한다
3. testid: 칩 `area-chip` → 탭 `area-tab`(+`data-selected`). 새로 둔 것: `area-tabs-<key>`(+`data-overflow`) · `area-desc-<key>`(`data-hub`) · `area-summary`(`data-source`) · `area-summary-source` · `area-summary-inherited` · `area-detail` · `area-photo-<key>`(`data-image`) · `area-crop-<key>`(`data-bg`·`data-overlay`) · 카드 `data-selected`
4. 카드 선택이 있으면 필터 일치 테두리(`data-match` ring) 대신 선택 외곽선만 그린다(`data-match` 값은 그대로 계산)
5. `__faceViewer.pickAt` 이 `uv` 도 돌려주고, `anchorUv(key)` 를 더했다. [복사] 본문에 `uv` 가 들어간다
6. 시험 쪽 고침: R-17 은 태블릿 「큰 화면 연결됨」이 켜진 뒤 기준 글자를 찍는다. 처음 실행에서 연결 표시가 늦게 켜져 한 번 실패했고, 고친 뒤 3회 반복 통과했다

### 사용자가 실물에서 만날 만한 어색한 자리 (2루프)
- **글자 크기**: 탭(13px)·설명(13px)·출처(11px)가 1920 큰 화면에서 꽤 작다. 요청대로 줄였지만 멀리서 읽기 어려울 수 있다
- **탭 넘침**: 눈가 4개 · 볼/코 5개 · 모공 4개는 가로 스크롤해야 끝 탭이 보인다. 끝 흐림으로만 알리고, 큰 화면에서 가로 스크롤은 손이 덜 간다
- **흐린 카드**: 내용 opacity .35 그대로라 흐린 카드의 확대 사진·설명이 연하다(이마 · 피지)
- **피지 카드**: 배지와 점수 줄에 「점수 없음」이 두 번 나온다
- **설명 문체**: Hub 원문이라 「…시술제」「…레이저」처럼 명사형으로 끝나고, 앞부분이 성분·원리 설명이라 상담 화면 말투와 다르다. 6개는 「치료·질환」이 들어간다(출처 표기로 처리)
- **확대 사진**: 64px · 반경 120 텍스처 px 라 피부결이 잘 보이는 정도다. 흐린 카드는 거의 베이지 판으로 보인다. 사진 자리(56px 회색)는 사진이 들어오기 전까지 빈 박스다
- **카드 클릭**: 카드 전체가 눌리므로 설명 글을 읽으려고 카드를 눌러도 선택이 바뀐다
- **'top' 경로 지시선**: 이마/미간 선은 이마 가운데를 수직으로 내려와 미간에 닿는다(이마를 세로로 지나긴 한다). 피지 선은 이마 오른쪽 위로 짧게 내려온다
- **닫기 버튼 xl**: 모달 머리 오른쪽에서 꽤 크다

### 명령 출력
```text
npm run lint                → exit 0 (경고 0)
npm run test                → Test Files 7 passed · Tests 74 passed
npx playwright test         → 36 passed (3.5m)   # 3417 재사용 · build 안 돌림
  areas 20(R-7~R-21 · W-4 · U-1 · U-2 · U-3·U-4 · 스크린샷) · smoke 3 · sync 9 · viewer 4
npx playwright test e2e/areas.spec.ts -g R-17 --repeat-each 3 → 3 passed
```
- 스크린샷 `screens/`:
  - 이번 판: `loop2-natural.png` · `loop2-filter-pore.png` · `loop2-card-selected.png` · `loop2-modal.png`(V빔 · 아래 안내) · `loop2-modal-fractional.png` · `loop2-crops.png`(부위 확대 6개)
  - 이번 실행에서 다시 찍힌 것: `anchors-front.png` · `rotate-30.png`
  - 1루프 그대로라 지금 화면과 다른 것: `natural.png` · `filter-pore.png` · `modal-*.png`
- 바꾼 파일:
  - 새로 만든 것: `src/components/screen/area-crop.tsx`
  - 고친 것: `area-card.tsx`(다시 씀) · `viewer-area.tsx` · `screen-view.tsx` · `leader-lines.tsx` · `procedure-modal.tsx` · `src/components/viewer/{anchors.ts, anchors.test.ts, anchor-store.ts, anchor-projector.tsx, face-canvas.tsx}` · `src/data/face-anchors.ts`(uv) · `src/data/hub/hub.ts`(`procedureSummary`) · `src/domain/{areas.ts, areas.test.ts}` · `src/app/globals.css` · `e2e/areas.spec.ts` · `e2e/sync.spec.ts`(금지어 검사에서 `area-summary` 제외)
- 커밋 안 함 · 3417 서버 끄거나 재시작하지 않음 · `public/m3d` 는 읽기만 했다

---

## 3루프 (카드 다듬기 · 사용자 실물 피드백 V-1~V-3 · 2026-10-26)

| # | 결과 | 한 것 |
|---|---|---|
| V-1 | ✓ | 카드 설명 아래 「Hub 원문」(`area-summary-source`)을 뺐다. 출처는 모달 아래 출처 줄에만 있다. 금지어 검사에서 `area-summary` 를 빼는 처리는 그대로 두고, `sync.spec` 주석만 고쳤다. e2e U-1 이 `area-summary-source` 0개를 단언한다 |
| V-2 | ✓ | [자세히]를 선택 시술 제목 줄 오른쪽으로 옮기고, 아래 출처/버튼 줄은 없앴다. 그 자리는 설명이 쓴다: 「◯◯ 전체 기준」이 없으면 3줄, 있으면 그 표기 1줄 + 2줄(말줄임). 4줄로 늘려 봤는데 카드 높이(약 267)에서 4번째 줄이 말줄임 없이 잘려서 3줄로 되돌렸다. 새 e2e `V-2·V-3`: 6장 모두 버튼과 제목의 세로 가운데 차이 < 6px · 버튼이 오른쪽 · 카드 안 잘림 0 |
| V-3 | ✓ | **틀:** 부위별로 반경·중심 이동을 정했다(아래 표). 반경 200·280·360 후보를 scratch 에서 잘라 비교해 골랐고, 미리보기 이미지는 지웠다. **썸네일:** 64 → **96px**. 이름·등급·점수 세 줄과 같이 들어가는 최대이고, 피지 점수 줄 「점수 없음 · 5,470개」는 두 덩이로 나눠 줄바꿈한다. **흐린 카드:** 사진만 opacity **0.75**, 글자·탭·설명은 그대로 .35. 흐림을 감싸는 요소 하나에 주면 opacity 가 곱해지므로 사진 칸만 따로 감쌌다(`area-crop-wrap-<key>`). e2e 로 사진 ≥ 88px · 반경 200대 · 흐린 카드(이마·피지) 사진 opacity ≥ 0.7 · 점수 줄 넘침 0 을 확인했다. `screens/loop3-crops.png` 로 6개 모두 알아볼 수 있음을 눈으로 확인했다 |

부위별 틀 — `area-crop.tsx` `CROP_FRAMES`, 텍스처 3242×1621 px 기준. dx/dy 는 앵커 UV 자리에서 옮긴 중심이고, + 는 이미지 오른쪽/아래다.

| 카드 | 반경 r | dx · dy | 이유(들어오는 것) |
|---|---|---|---|
| 이마/미간 | 260 | 0 · −90 | 미간에서 위로 올려 양 눈썹 사이 + 이마 아랫부분 |
| 눈가/눈밑 | 230 | −20 · −70 | 눈밑 점에서 위로 — 감은 눈 · 눈썹이 같이 |
| 팔자/광대 | 250 | +20 · 0 | 콧방울 옆 ~ 입가(코 · 윗입술) |
| 피지/트러블 | 280 | 0 · +40 | 이마 오른쪽 T존 — 머리선 ~ 눈썹 끝 |
| 볼/코 주변 | 260 | −30 · 0 | 콧방울 옆 볼 — 코 옆선 · 눈 아래가 같이 |
| 모공/피부결 | 250 | −30 · −10 | 입꼬리 옆 볼 — 입가 · 콧방울 |

함께 고친 것: 2루프의 피지 점수 줄이 넓어진 사진 때문에 카드 오른쪽 밖으로 넘쳤다. 「점수 없음」·「· 5,470개」를 각각 줄바꿈 금지 덩이로 두고 `min-w-0` 을 줬다.

### 어색한 자리 (3루프)
- **96px 썸네일:** 사진이 커져 이름 칸이 102px 로 줄었다. 부위명은 한 줄에 들어가지만, 피지 카드 점수 줄은 2줄이 될 수 있다(지금은 1줄에 들어감)
- **피지 사진:** 위쪽에 머리카락·검은 머리선이 들어온다. T존 자리라 피할 수 없다
- **오버레이 필터:** 모공·주름 필터에서는 넓어진 틀만큼 선·점이 촘촘히 겹쳐 보인다. 2루프처럼 텍스처 + mask 합성 그대로다
- **흐린 카드:** 사진만 진해서(0.75) 흐린 카드에서도 눈에 띈다. 의도한 것이지만 「흐림」 대비가 약해졌다

### 명령 출력
```text
npm run lint        → exit 0 (경고 0)
npm run test        → Test Files 7 passed · Tests 74 passed
npx playwright test e2e/areas.spec.ts → 21 passed (2.4m)   # 3루프 고침 중간
npx playwright test → 37 passed (3.6m)                       # 마지막 전체 1회 · 3417 재사용 · build 안 돌림
```
- 코디 안내(3417 이 외부 SIGTERM 으로 잠깐 내려갔다 다시 뜸): 전체 e2e 는 37/37 통과(exit 0)라 다시 돌리지 않았다. 끝난 뒤 `curl /screen` → 200 으로 서버가 떠 있는 것만 확인했고 서버는 건드리지 않았다
- 스크린샷: `screens/loop3-natural.png` · `loop3-crops.png`(이번 실행). `loop2-*` 는 2루프 화면 그대로다
- 바꾼 파일: `src/components/screen/area-card.tsx` · `area-crop.tsx`(`CROP_FRAMES`) · `viewer-area.tsx`(틀 연결) · `e2e/areas.spec.ts`(V-2·V-3 시험 · 스크린샷 이름 · U-1 단언) · `e2e/sync.spec.ts`(주석)
- 커밋 안 함 · 얼굴 크롭 파일 저장 안 함 · `public/m3d` 는 읽기만 했다

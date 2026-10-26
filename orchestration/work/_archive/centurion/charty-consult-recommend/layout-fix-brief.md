# frontend 정정 브리프 — 화면 ① 배치 (SPEC §0·§1 덮어씀)

10-26 사용자 정정: **화면 ① 기존 배치는 그대로 둔다. 추천 카드는 왼쪽 3D 패널 안에서 얼굴 좌우에 들어간다.**
이 문서가 SPEC §0·§1·§1-3·관련 AC 좌표보다 우선한다. 나머지(카드 규칙·앵커·모달·스냅샷·WP1)는 SPEC·fe-brief 그대로.

## 1. 배치
- 화면 ① 1920×1080 은 **커밋 HEAD 와 같은 구조**: 왼쪽 뷰어 패널 1040px + 오른쪽 열(한눈에 보기 372 · 항목별 상태 300 · 플랜 나머지)
- 뷰어 패널 안: 3D 얼굴 가운데 · **왼쪽 카드 열 3장 / 오른쪽 카드 열 3장**(칸 순서는 SPEC §1-2 그대로) · 아래 필터 바(96px) 그대로
  - 카드 열 폭 약 220px(패널 안쪽 여백 포함해 네가 정하라). 얼굴이 두 열 사이 가운데에 오게 카메라 거리/시야를 조정해도 된다(리셋 위치도 같이)
  - 카드는 어두운 패널 위 — 메디킷 Card 흰 바탕 유지 가능. 내용: **부위명 · 등급 배지 · 대표 점수 1개 · 시술 칩**. 하위 지표 줄은 공간이 안 되면 뺀다
  - 칩 잘림 없음(W-12) 그대로 완료 조건
- 지시선·점은 뷰어 패널 안에서만 그린다(카드 끝점 ↔ 투영 점)
- 「지금 보는 것」(focus-card) = **제거 유지**, 범례 한 줄(`viewer-legend`, 「목업 · 의학적 근거 아님」 포함)로 대체 — 사용자 기본값 동의
- 모달 = 화면 ① 전체 위 가운데(SPEC §4 그대로)

## 2. 되돌릴 것
- 오른쪽 열 3개와 그것이 쓰는 파일을 HEAD 에서 되살린다: `git checkout HEAD -- <path>` (커밋 아님 — 허용). 대상은 **grep 으로 전수**: `overview-section`·`items-section`·`plan-panel`·`radar-chart`·`score-bars`·`face-region-map`·`use-tween` 중 오른쪽 열이 쓰는 것 전부. focus-card 만 쓰던 것은 지운 채 둔다(`gradeSentence` 포함)
- `screen-view.tsx` 오른쪽 열·`ReportPlaceholder` 원상 복구(`report-missing` 유지)
- e2e `sync.spec.ts`·`viewer.spec.ts` 는 **HEAD 기준으로 되돌린 뒤** focus-card 관련 단언만 빼거나 고친다. 오른쪽 열 testid(`screen-overview`·`screen-items`·`screen-plan`·`score-bars` 등)는 다시 있어야 한다
- 태블릿 「가격 표시」 토글은 다시 동작한다(SPEC §6-4 무효)

## 3. AC 보정
- R-7: 카드 6장이 뷰어 패널(`screen-viewer`) 안 좌3·우3 순서로 있고, **오른쪽 열 testid 가 다시 있다**, `focus-card` 는 0개
- R-12 등 좌표 조건의 「C 구역」= 두 카드 열 사이 뷰어 영역(필터 바 위). 숫자는 네가 새 배치로 다시 정하고 리포트에 적어라
- R-22 등 가격 관련 AC 는 HEAD 동작대로(태블릿 토글 → 화면 ① 플랜 가격)

## 4. 진행
- 지금 WP2 를 이 배치로 다시 하고(스크린샷 `screens/natural.png`·`filter-pore.png` 갈아끼움), 그 뒤 WP3~WP6 원래대로
- fe-report 에 「배치 정정」 한 줄 기록. 완료 보고는 fe-brief §9 그대로

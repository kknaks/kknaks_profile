---
type: concept
id: surface-anchor-leader-line
title: 3D 표면 앵커를 화면 지시선으로
aliases:
  - 지시선
  - 콜아웃
  - 3D 앵커 투영
  - Vector3.project
  - updateMatrixWorld
  - 가림 판정
up:
  - 2026-10-26-charty-consult-recommend
tags:
  - frontend
  - threejs
  - webgl
---

# 3D 표면 앵커를 화면 지시선으로

회전하는 3D 모델의 **특정 지점**을 화면 옆 DOM 카드와 선으로 잇는 것. 점을 화면 좌표로 박으면 모델이 돌 때 점이 표면을 떠난다. **메시 위 3D 좌표를 저장하고 매 프레임 화면으로 투영**해야 점이 표면에 붙어 따라간다.

## 정의

1. **앵커 = 메시 표면의 점 + 법선 (+ UV)** — 사람이 화면을 클릭하면 raycast 로 표면 교점을 얻어 고정값으로 저장한다. 메시가 바뀌면 무효이므로 메시 크기 같은 지문으로 가드한다
2. **매 프레임 투영** — `useFrame` 에서 `p.clone().project(camera)` → NDC → 캔버스 px → 패널 좌표. SVG 는 React state 가 아니라 `setAttribute` 로 직접 고친다(프레임마다 리렌더 금지)
3. **카메라 행렬을 먼저 갱신한다** — `project()` 는 `camera.matrixWorldInverse` 를 쓰는데 이 값은 `gl.render` 안에서 갱신된다. 컨트롤이 이번 프레임에 카메라를 옮겼으면 투영은 **지난 프레임** 행렬로 계산된다 → `useFrame` 첫 줄 `camera.updateMatrixWorld()`
4. **가림** — 법선·시선 내적으로 뒷면을 먼저 거르고, 남은 점은 카메라→점 raycast 의 첫 교점이 점 자신인지로 판정. 메시가 크면 BVH(`<Bvh firstHitOnly>`)
5. **보이는지 판정은 목표값으로** — opacity 를 스무딩(`cur += (target − cur)·k`)하면 0 에 닿지 않는다. `visible` 은 목표 opacity > 0 으로 정의하고, 노출 값은 「SVG 에 실제 적용한 최종값」과 「가림만의 값」을 따로 둔다

## 경계와 오해

- **한 프레임 지연은 시험에서 flaky 로 나타난다** — 시험이 `page.evaluate` 로 투영을 다시 부르면 렌더 뒤라 행렬이 새것이다. 감쇠가 조금 남은 실행에서만 SVG 점(옛 행렬)과 어긋나 1px 기준을 넘는다. 기준을 늘리지 말고 원인을 고친다
- **터미널 에이전트는 화면을 보며 찍을 수 없다** — `pickAt(cx, cy)` 같은 좌표 → raycast 훅을 열어 두면 「스크린샷 → 좌표 지정 → 찍기 → 결과 스크린샷」으로 사람 없이 찍는다. 사람 확인은 정면 스크린샷 한 장
- **디버그 훅 객체를 여러 컴포넌트가 나눠 쓰면** — 한쪽이 객체를 통째로 다시 만들어 다른 쪽 키를 지운다. `Object.assign` 으로 덧붙이고 기존 키를 보존한다
- 지시선 교차는 앵커 자리와 카드 칸 순서에 달렸다 — 교차가 나면 칸을 바꾸지 말고 같은 칸 순서 안에서 점을 옮긴다

## 함께 보는 개념

- [[uv-atlas-overlay]] — 같은 앵커의 UV 로 텍스처를 잘라 카드 썸네일에
- [[viewport-aware-overlay]] — 화면 기준 DOM 오버레이 배치

## 출처

- [[2026-10-26-charty-consult-recommend]] §2 — 피부 상담 목업 부위 카드 지시선(`web/src/components/viewer/anchor-projector.tsx` · `code-review-report.md` F-1 · `spec-review-report.md` W-4·W-7·W-10)

# 도구 — OpenPencil 0.16.0 실측(2026-11-12)

- CLI: `bun ~/.bun/bin/openpencil …` (그냥 `openpencil` 은 node 20 에서 깨진다)
- 앱 모드(파일 인자 없음) = 사용자가 앱에 열어 둔 문서. `documents list` 로 대상 탭 · 경로를 먼저 확인
- `eval --stdin < 스크립트.js` 로 실행. 앱 모드 `figma` 에는 **`figma.variables` · `createTextStyle` · `createEffectStyle` 없음**
  - 변수: `figma.getLocalVariableCollections()` · `figma.getLocalVariables()` · `figma.createVariable(name, type, collectionId, value)`
  - 바인딩: `figma.bindVariable(nodeId, "fills/0/color", variableId)` (strokes 도 같은 꼴)
  - 컴포넌트: `figma.createComponentFromNode(node)` · `figma.combineAsVariants(components, parent)` (이름 `prop=value, prop=value`)
  - 폰트: Pretendard Regular/Medium/SemiBold 로드됨(`figma.loadFontAsync`)
- 저장: `bun ~/.bun/bin/openpencil documents save`
- 확인: `info <파일>` · `tree` · `find` · `lint`. **headless PNG(`export <파일>`)는 Pretendard 를 Inter 로 대체한다** — 배치 확인용으로만 쓰고 굵기 · 글자 폭 판정에 쓰지 않는다
- **eval 한 번이 20초를 넘으면 CLI 가 시간 초과**를 낸다(앱 쪽은 끝까지 돌지만 결과를 못 받는다). 렌더는 작은 스크립트 여러 번으로 나눈다
- 린트: `bun ~/.bun/bin/openpencil lint --json` (앱 모드) · `--rule <id>` · `--list-rules` · `--fix`(안전 수정: 색 변수 바인딩 · 정수 픽셀)

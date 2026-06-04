# Decision Index

규칙: `rules/product-doc-pipeline.md`

> baseline을 제품에 어떻게 적용할지 판단한 결정 목록과 아직 풀어야 할 질문을 관리한다. 원본 ADR-001~005에 대응한다.

## 결정 로그

| ID | Title | Status | Baseline | Result | Spec |
|---|---|---|---|---|---|
| MRT-DEC-001 | WebSocket을 통신 프로토콜로 선택 | accepted | MRT-BL-001 | WS 채택 | [MRT-SPEC-005](../20-spec/spec-005-websocket-protocol.md) |
| MRT-DEC-002 | CGWindowListCopyWindowInfo를 창 목록 수집에 사용 | accepted | MRT-BL-001 | CGWindowList 채택 | [MRT-SPEC-001](../20-spec/spec-001-window-list.md) |
| MRT-DEC-003 | 화면 캡처 대신 앱 아이콘만 표시 | accepted | MRT-BL-001 | 아이콘만 | [MRT-SPEC-004](../20-spec/spec-004-app-icon.md) |
| MRT-DEC-004 | Mac 헬퍼를 먼저 개발 | accepted | MRT-BL-001 | M→I→T 순서 | (work 순서 결정) |
| MRT-DEC-005 | Swifter를 Mac WebSocket 서버 라이브러리로 선택 | accepted | MRT-BL-001 | Swifter 채택 | [MRT-SPEC-005](../20-spec/spec-005-websocket-protocol.md) |

## 미결 사항

| ID | Question | Owner | Next |
|---|---|---|---|
| — | 없음 (모든 ADR accepted) | | |

# Spec Index

규칙: `rules/product-doc-pipeline.md`

> decision으로 확정된 내용을 기능 계약으로 구체화한 spec 목록. 모든 spec은 코드로 구현·배포되어 `implemented`다.

## Spec 목록

| ID | Title | Status | Decision | 의존 | Work |
|---|---|---|---|---|---|
| [MRT-SPEC-001](v1_0_1-spec-001-window-list.md) | 창 목록 수집 | implemented | MRT-DEC-002 | — | MRT-WORK-001, 005 |
| [MRT-SPEC-002](v1_0_1-spec-002-window-focus.md) | 창 활성화 | implemented | — | SPEC-001 | MRT-WORK-002, 005 |
| [MRT-SPEC-003](v1_0_1-spec-003-key-input.md) | 키 입력 (매크로) | implemented | — | — | MRT-WORK-003, 017, 005 |
| [MRT-SPEC-004](v1_0_1-spec-004-app-icon.md) | 앱 아이콘 수집 | implemented | MRT-DEC-003 | SPEC-001 | MRT-WORK-004, 005 |
| [MRT-SPEC-005](v1_0_1-spec-005-websocket-protocol.md) | WebSocket 통신 프로토콜 | implemented | MRT-DEC-001, 005 | SPEC-001·002·003·004 | MRT-WORK-005, 009 |
| [MRT-SPEC-006](v1_0_1-spec-006-permissions.md) | 권한 관리 | implemented | — | — | MRT-WORK-001, 006 |
| [MRT-SPEC-007](v1_0_1-spec-007-pairing.md) | 페어링 | implemented | — | SPEC-005 | MRT-WORK-007, 012 |

## 의존 관계

```
SPEC-001 (창 목록) ──► SPEC-002 (창 활성화)
   │                       │
   ├──► SPEC-004 (앱 아이콘)│
   │                       │
   └────┬────┬─────────────┘
        ▼    ▼
SPEC-003 (키 입력)   SPEC-005 (WebSocket 프로토콜)
                         │
SPEC-006 (권한)          ├──► SPEC-007 (페어링)
```

## 상태 정의

`implemented` = 기능 계약이 코드로 구현되고 릴리즈됨 (rules의 spec status).

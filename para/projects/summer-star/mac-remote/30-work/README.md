# Work Index

규칙: `para/projects/project.md`

> spec을 실제 구현 작업으로 내린 work 목록과 spec coverage. Mac 헬퍼(M1~M7) → iOS 앱(I1~I6) → 통합(T1~T3) + Hold 모드.

## Work 목록

| ID | Title | Type | Status | Progress | Covers Spec | 의존 | Release |
|---|---|---|---|---|---|---|---|
| [MRT-WORK-001](work-001-cli-prototype.md) | M1: CLI 프로토타입 (창 목록) | new-feature | done | 100 | SPEC-001, 006 | — | REL-001 |
| [MRT-WORK-002](work-002-window-focus.md) | M2: 창 활성화 | new-feature | done | 100 | SPEC-002 | WORK-001 | REL-001 |
| [MRT-WORK-003](work-003-key-input.md) | M3: 키 입력 | new-feature | done | 100 | SPEC-003 | WORK-001 | REL-001 |
| [MRT-WORK-004](work-004-app-icon.md) | M4: 앱 아이콘 추출 | new-feature | done | 100 | SPEC-004 | WORK-001 | REL-001 |
| [MRT-WORK-005](work-005-websocket-server.md) | M5: WebSocket 서버 | new-feature | done | 100 | SPEC-005 | WORK-001·002·003·004 | REL-001 |
| [MRT-WORK-006](work-006-menubar-app.md) | M6: 메뉴바 앱화 | new-feature | done | 100 | SPEC-006 | WORK-005 | REL-001 |
| [MRT-WORK-007](work-007-pairing-qr.md) | M7: 페어링 QR | new-feature | done | 100 | SPEC-007 | WORK-006 | REL-001 |
| [MRT-WORK-008](work-008-ios-setup.md) | I1: 프로젝트 셋업 (3탭) | new-feature | done | 100 | — | WORK-005 | REL-001 |
| [MRT-WORK-009](work-009-ws-client.md) | I2: WebSocket 클라이언트 | new-feature | done | 100 | SPEC-005 | WORK-008 | REL-001 |
| [MRT-WORK-010](work-010-window-list-ui.md) | I3: 창 목록 화면 | new-feature | done | 100 | SPEC-001, 002, 004 | WORK-009 | REL-001 |
| [MRT-WORK-011](work-011-macro-ui.md) | I4: 매크로 화면 | new-feature | done | 100 | SPEC-003 | WORK-009 | REL-001 |
| [MRT-WORK-012](work-012-settings-ui.md) | I5: 설정 화면 | new-feature | done | 100 | SPEC-006, 007 | WORK-009 | REL-001 |
| [MRT-WORK-013](work-013-status-handling.md) | I6: 상태 처리 | new-feature | done | 100 | SPEC-005 | WORK-009 | REL-001 |
| [MRT-WORK-017](work-017-hold-modifiers.md) | Hold 모드 (앱 스위처용) | new-feature | done | 100 | SPEC-003 | WORK-003·005·011 | REL-001 |
| [MRT-WORK-014](work-014-e2e-test.md) | T1: 엔드투엔드 테스트 | new-feature | done | 100 | 전체 | WORK-007·013 | REL-002 |
| [MRT-WORK-015](work-015-edge-cases.md) | T2: 엣지 케이스 대응 | new-feature | done | 100 | 전체 | WORK-014 | REL-002 |
| [MRT-WORK-016](work-016-polish.md) | T3: 다듬기 | new-feature | done | 100 | 전체 | WORK-015 | REL-002 |

## Spec Coverage

| Spec | Work | Coverage |
|---|---|---|
| SPEC-001 | WORK-001, 010 (+005 §계약) | Full |
| SPEC-002 | WORK-002, 010 (+005 §계약) | Full |
| SPEC-003 | WORK-003, 011, 017 (+005 §계약) | Full |
| SPEC-004 | WORK-004, 010 (+005 §계약) | Full |
| SPEC-005 | WORK-005(서버), 009(클라이언트), 013 | Full |
| SPEC-006 | WORK-001(확인), 006(안내), 012 | Full |
| SPEC-007 | WORK-007(QR생성), 012(QR스캔) | Full |

## 상태 정의

17개 work 전부 done — 제품은 1.0.1로 배포되어 운영 사용 중이다. T1~T3(WORK-014·015·016)는 실제 배포·실사용으로 충족됐다. App Store 심사 제출 절차는 `40-architecture/deploy/front/README.md` 런북을 따른다.

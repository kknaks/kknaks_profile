# Spec Index

규칙: `para/projects/project.md`

> decision으로 확정된 내용을 기능 계약으로 구체화한 spec 목록. 원본 `study_timelapse/medi_docs/current/spec/` 12건(spec-01~10, 12, 13, **spec-11 결번**)을 큐레이션 이관했다. 원본의 구현 본문(Swift/Python/TS)·옵션 deliberation 은 제외하고 계약 표면만 남겼으며, 각 spec 의 `구현 현황` 섹션에 실제 코드 grounding(file:line)을 남겼다.
> status 는 코드 상태 반영 — 대부분 `implemented`, 미구현 요소가 있는 2건은 `in_dev`(본문 Open Questions 에 gap 플래그).

## Spec 목록

| ID | Title | Status | Decision | 의존 | Work |
|---|---|---|---|---|---|
| [STL-SPEC-001](spec-001-recording-state-machine.md) | 녹화 세션 상태머신 | implemented | STL-DEC-004·005·006·007·008 | SPEC-002 | (예정) |
| [STL-SPEC-002](spec-002-capture-pipeline.md) | 캡처 파이프라인 (Native) | implemented | STL-DEC-004·005·007·008·009 | SPEC-001 | (예정) |
| [STL-SPEC-003](spec-003-subscription-state-machine.md) | 구독 5상태 머신 | implemented | STL-DEC-010·011 | SPEC-004·005·006 | (예정) |
| [STL-SPEC-004](spec-004-subscription-api.md) | 구독 API (Phase 1) | implemented | STL-DEC-010·012·013 | SPEC-003·005·006 | (예정) |
| [STL-SPEC-005](spec-005-subscription-data-model.md) | 구독 데이터 모델 | implemented | STL-DEC-010·011·012·013 | SPEC-003·004·006 | (예정) |
| [STL-SPEC-006](spec-006-revenuecat-integration.md) | RevenueCat 통합 API (Phase 2) | in_dev | STL-DEC-015·017·019·020·021·022 | SPEC-003·004·005·007·008 | (예정) |
| [STL-SPEC-007](spec-007-receipt-verification.md) | 영수증 검증 흐름 (Phase 2) | implemented | STL-DEC-015·017·021·022 | SPEC-006·003·005 | (예정) |
| [STL-SPEC-008](spec-008-mobile-revenuecat-integration.md) | Mobile RevenueCat SDK (Phase 2) | implemented | STL-DEC-013·016·018·022 | SPEC-006·004 | (예정) |
| [STL-SPEC-009](spec-009-auth-onboarding.md) | Auth & 온보딩 | in_dev | — | SPEC-003·008 | (예정) |
| [STL-SPEC-010](spec-010-session-domain.md) | 세션 도메인 (Session API) | implemented | — | SPEC-001·002·003·008 | (예정) |
| [STL-SPEC-012](spec-012-stats-domain.md) | Stats 도메인 (통계 API) | implemented | — | SPEC-003·008·010 | (예정) |
| [STL-SPEC-013](spec-013-users-api.md) | Users API | implemented | — | SPEC-003·004 | (예정) |

> **STL-SPEC-011 결번**: 원본 `spec/` 디렉토리에 `spec-11` 파일이 존재하지 않는다(STL-SPEC-011 미발급). 번호는 원본 spec 과 1:1 lineage 유지를 위해 보존(adr-03 결번과 동일 규약).

## 의존 관계

```
SPEC-001 (녹화 상태머신) ◄──► SPEC-002 (캡처 파이프라인)
        ▲
SPEC-010 (세션) ──┤
                  └──► SPEC-003 (구독 5상태) ──► SPEC-004 (구독 API) ──► SPEC-005 (데이터 모델)
                                                       │
SPEC-013 (Users) ──────────────────────────────────────┘
SPEC-006 (RevenueCat API) ──► SPEC-007 (영수증 검증)
        └──► SPEC-008 (Mobile SDK) ◄── SPEC-009 (Auth/온보딩)
SPEC-012 (Stats) ──► SPEC-010
```

## status 정의

- `implemented` = 기능 계약이 코드로 구현·배포됨 (10건)
- `in_dev` = 계약은 확정됐으나 일부 요소가 코드 미구현 (2건: SPEC-006 INITIAL_PURCHASE period_type 분기, SPEC-009 모바일 Apple Sign-In). 각 본문 Open Questions 참조.

## 미구현 gap 요약

| Spec | gap | 근거 |
|---|---|---|
| STL-SPEC-006 | `INITIAL_PURCHASE` period_type TRIAL/NORMAL 분기 미구현 (항상 pro) | `backend/app/schemas/subscription.py:14-23`, `subscription_handler.py:160-165` |
| STL-SPEC-009 | 모바일 Apple Sign-In 미연동 (BE 는 구현됨) | `frontend/mobile/app/login.tsx` Google 단독 |
| STL-SPEC-007 | verify rate-limit(5회/분) 미구현 (status 유지) | sync 만 30초 쿨다운 |
| STL-SPEC-012 | stats API timezone 미적용 (알려진 부채, status 유지) | `backend/app/api/v1/stats.py:26-33` |

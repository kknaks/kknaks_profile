# Work Index

규칙: `para/projects/project.md`

> 현재 구현, QA, 릴리즈 상태를 추적하는 map이다. 상세 work 실행 본문은 `30-work/` 아래 1 파일 = 1 work로 둔다.
> `Status Board`는 실행 상태의 owning view다. Spec Coverage는 work frontmatter `links.specs`를 spec 중심으로 펼친 derived view다.

최종 수정: 2026-10-03

Status 값: `todo`, `in_progress`, `blocked`, `review`, `done`

## Domain / Schema 관리 원칙

- Work는 구현 중 필요한 DDD 초안과 schema 가정을 적는 자리다.
- 실제 table schema, column, index, FK, migration 전문은 제품 코드/migration이 source of truth다.
- `30-work/`에는 aggregate boundary, 상태/invariant, migration 필요 여부, 코드 위치 후보만 적는다.
- 같은 invariant가 여러 work에 반복되거나 onboarding용 도메인 지도가 필요해지면 optional architecture 문서로 승격한다.
- SPEC에는 사용자/프론트/QA/외부 연동에 드러나는 resource, status, enum, API 계약만 환류한다.

## Status Board

| Phase | Work | Scope | Status | Owner | 예상 기간 | 목표 완료 | PR/Branch | Blocker | Next |
|---|---|---|---|---|---|---|---|---|---|
| 1–8 | [WORK-001 업무 생성·즉시 배정](work-001-task-creation.md) | SPEC-001/002의 W1 | review | kknaks | 미산정 | 미정 | `kknaksss/strong-hajin-work` | 사용자 E2E 미수행 | 사용자 E2E 확인 |
| 0–8 | [WORK-002 업무 v2·MyWork 개편](work-002-task-lifecycle-v2.md) | BE·FE 통합 | review | kknaks | 자동검증 완료 | 2026-09-17 목표 | `kknaksss/strong-hajin-work` | 자동검증 완료 · 브라우저 E2E 사용자 수행 · OQ-203·206 해당 경로 답 대기 | Node20 make verify·PG 77건·FE713건 완료 |
| 1–7 | [WORK-003 참조 읽음·선행업무·만들기 창 프레임](work-003-inbox-predecessor-and-create-frame.md) | SPEC-001의 D-19·D-20·D-21 | todo | kknaks | 미산정 | 미정 | `kknaksss/strong-hajin-work` | 없음 (OQ-M은 Phase 3의 한 조각만 gate) | WP 검수 → BE·FE 병렬 발주 |
| BE1–FE5 | [WORK-005 「프로젝트」 화면](work-005-projects.md) | SPEC-005 전절 (1루프 done · Phase 0 done · **2루프 BE-3→FE-4→FE-5 직렬**) | in_progress | kknaks | 미산정 | 미정 | `kknaksss/strong-hajin-projects` | 없음 | **2루프 BE-3 발주 예정** (인수조건 1루프 76 + **2루프 52**) |
| BE1–FE4 | [WORK-004 캘린더 시간 배정](work-004-calendar-scheduling.md) | SPEC-004 전절 (BE·FE 직렬 · 2루프) | in_progress | kknaks | 미산정 | 미정 | `kknaksss/strong-hajin-calendar` | 없음 | **1루프 넷 DONE**(`1c15d02`·`2a85176`·`c5b109d`·`aa8576b`) → **Phase BE-3 발주**(2루프 K19~K24) |

| 1–3 (2a·2b) | [WORK-010 운영 고도화 3차](work-010-polish3.md) | SPEC-007 §2.10 · SPEC-006 U-5 · R1·R2a·R3(WP 계약) | review | kknaks | 2일 | 2026-10-05 | Strong_hajin#11 (`202078b`) | macOS 실기·dmg | 운영 반영 |
| SHELL-0·BE1–3·FE·SHELL·INFRA | [WORK-011 외부 채널 연동·메시지함·프로필·카톡 수집](work-011-external-channels.md) | SPEC-008·009·006 전절 (초안 · 4차 검수 조건부 PASS 반영) | done | kknaks | 미산정 | 미정 | — | 없음 | BE-1·SHELL-0 발주됨 → BE-2 전 ★3 · BE-3 전 ★2 |
| 1–9 (6a·6b 분리) | [WORK-006 데스크톱 래퍼](work-006-tauri-wrapper.md) | SPEC-006 전절 · 10단계 | in_progress | kknaks | 미산정 | 미정 | `kknaksss/strong-hajin-projects` | 배포 결정·Windows 장비는 해당 단계에서 확인 | Phase 1 Claude 구현 중 |
| B-1–7 | [WORK-007 업무 상세 재설계](work-007-task-detail.md) | SPEC-007 전절 (**BE 셋 → FE 셋 직렬**) | todo | kknaks | 미산정 | 미정 | `kknaksss/strong-hajin-design` | 없음 (OQ-709 는 F-2 의 한 조각만 gate) | WP 검수 → **BE Phase B-1 발주** |
| 1 · 2 · 3a→3b | [WORK-008 운영 고도화 1차](work-008-polish.md) | 운영 요청 8건 + 회의 요약 · AX 탐색 (Phase 1~5, 6 취소) | done | kknaks | 2026-10-01~02 | 2026-10-02 | Strong_hajin#9 · k8s_infra_mac#7 | 없음 | 운영 반영 완료 — 다음 고도화는 회고 §7 |
| 1 · 2a · 2b · 3 | [WORK-009 운영 고도화 2차](work-009-polish2.md) | 운영 E2E 6건 — AX 초안 저장 · 관련 기록 탐색 · 채팅 단추 상태 · 업무 날짜 넷 | done | kknaks | 2026-10-02~03 | 2026-10-03 | Strong_hajin#10 · k8s_infra_mac#8 | 없음 | 운영 반영 — 다음 고도화는 회고 §7 |

## Work List

work 문서를 만들거나 상태, owner, branch, 다음 작업이 바뀌면 이 표를 갱신한다.

| ID | Title | Type | Owner | Status | Progress | File | Covers Spec |
|---|---|---|---|---|---|---|---|
| WORK-001 | 업무 생성·즉시 배정 | new-feature | kknaks | review | 90% | [work-001-task-creation.md](work-001-task-creation.md) | SPEC-001 · SPEC-002 |
| WORK-002 | 업무 v2·MyWork 개편 | new-feature | kknaks | review | 자동검증 완료 | [본문](work-002-task-lifecycle-v2.md) | SPEC-003 · SPEC-001 · SPEC-002 |
| WORK-003 | 참조 읽음·선행업무·만들기 창 프레임 | new-feature | kknaks | todo | 0% | [본문](work-003-inbox-predecessor-and-create-frame.md) | SPEC-001 |
| WORK-004 | 캘린더 시간 배정 | new-feature | kknaks | in_progress | 1루프 4/4 · 2루프 0/4 | [본문](work-004-calendar-scheduling.md) | SPEC-004 |

| WORK-006 | 데스크톱 래퍼 | new-feature | kknaks | in_progress | 0% | [본문](work-006-tauri-wrapper.md) | SPEC-006 |
| WORK-007 | 업무 상세 재설계 | new-feature | kknaks | todo | 0% | [본문](work-007-task-detail.md) | SPEC-007 |
| WORK-008 | 운영 고도화 1차 | improvement | kknaks | done | 100% | [본문](work-008-polish.md) | SPEC-001 · SPEC-002 · SPEC-005 · SPEC-007 |
| WORK-009 | 운영 고도화 2차 | improvement | kknaks | done | 100% | [본문](work-009-polish2.md) | SPEC-001 · SPEC-002 · SPEC-003 · SPEC-004 · SPEC-007 |
| WORK-011 | 외부 채널 연동·메시지함·프로필·카톡 수집 | new-feature | kknaks | done | 운영 반영 2026-10-06 · 후속 SH-IMP-006~015 | [본문](work-011-external-channels.md) | SPEC-008 · SPEC-009 · SPEC-006 |
| WORK-012 | 고도화 — WP1 운영 버그 · WP2 회의록 · WP3 AX 흐름 · WP4 메시지함→AX · SHELL | enhancement | kknaks | done | 운영 반영 2026-10-07(#16 `5c8345e` · 2루프 #17 `d2a06fa`) · dmg 서명·공증 · 운영 E2E | [본문](work-012-enhance.md) | SPEC-008 · SPEC-010 |
| WORK-013 | 알림 — P0 조사 · WP1 사건 채널(SSE) · WP2 생성·설정·판정·백필 · WP3 화면 · WP4 셸·수집기 | new-feature | kknaks | done | 운영 반영 2026-10-08(#18 `3321504`) · 추가 수정 2026-10-10(#19 `baf7daf`) · 사용자 E2E 통과 | [본문](work-013-notifications.md) | SPEC-011 · SPEC-006 · SPEC-008 · SPEC-009 |

## Spec Coverage

각 spec이 어느 work에서 구현되며 현재 진척이 어떤지 한눈에 보는 spec-centric view다. Covering Work의 Status를 종합한 derived view다.

| Spec | Covering Work | 구현 상태 |
|---|---|---|
| SPEC-001 | WORK-001 · WORK-002 · WORK-003 | W1 review. W2 미착수. 참조 읽음·선행업무·만들기 창 프레임은 WORK-003 todo |
| SPEC-002 | WORK-001 · WORK-002 | 신규 수락 제거·AX 확인 보존 review. 완료 승인·문의 미착수 |
| SPEC-003 | WORK-002 | 계획·BE·FE 구현 및 자동검증 완료, OQ-203·206 답 대기 |
| SPEC-004 | WORK-004 | v0.3.1 검수 PASS·커밋. **1루프 넷 DONE**, 2루프(`K19`~`K24`) 넷 todo — Phase BE-3 발주 대기 |

| SPEC-006 | WORK-006 | 계획 검수 종료. Phase 1 구현 중, 실기·설치 E2E는 내일 |
| SPEC-007 | WORK-007 | 계약 v0.2.0 검수 반영 완료. WP 작성 완료·구현 미착수(BE 셋 → FE 셋 직렬). **WORK-003 Phase 6 을 흡수한다** |

## Release Gate

### Scope

- [ ] 릴리즈 대상 spec이 정해졌다.
- [ ] 포함/제외 범위가 decision/spec과 맞다.

### Code

- [ ] 연결된 제품 PR이 merge됐다.
- [ ] 필요한 migration/환경변수/외부 설정이 반영됐다.

### Spec

- [ ] 필요한 `20-spec/README.md` / `20-spec/` 변경이 리뷰됐다.
- [ ] blocker open question이 없다.

### Baseline / UX

- [ ] 필요한 baseline artifact가 연결됐다.
- [ ] Known UX issue는 Product/Design이 승인했다.

### QA

- [ ] 필요한 QA case가 실행됐다.
- [ ] blocking fail이 없다.

### Approval

- [ ] Product
- [ ] QA
- [ ] Tech Lead
- [ ] 범위, 벤더 경로, 정책, 비용, 일정, 고객 약속이 바뀐 경우 Decision Owner

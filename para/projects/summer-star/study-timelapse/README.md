# study-timelapse

## 목적

Study Timelapse 제품을 운영하기 위한 SSOT다.

규칙: `para/projects/project.md`

## 현재 상태

| Area | Status | Next |
|---|---|---|
| Baseline | 미이관 | 필요 시 원본 PRD/리뷰 artifact 이관 |
| Decision | 21건 accepted (STL-DEC-001~022, 003 결번) | 미결 사항은 decision index에서 관리 |
| Spec | 12건 이관 (10 implemented / 2 in_dev, 011 결번) | SPEC-006 period_type, SPEC-009 Apple Sign-In gap 후속 |
| Work | STL-WORK-001 done, STL-WORK-002 todo, STL-WORK-003 todo | 기록 저장/통계 timezone fix 재현 테스트 후 구현 |

## 문서 맵

| Stage | Index |
|---|---|
| 00-baseline | `00-baseline/README.md` |
| 10-decision | `10-decision/README.md` |
| 20-spec | `20-spec/README.md` |
| 30-work | `30-work/README.md` |
| 40-architecture | `40-architecture/README.md` |

## 최근 로그

- 2026-06-20: STL-WORK-001 완료 — 앱 전반 영어 copy 통일 및 저장 후 back 보강
- 2026-06-21: STL-WORK-002 추가 — Mobile Apple Sign-In integration
- 2026-06-21: STL-WORK-003 추가 — session stats persistence/timezone bugfix
- 2026-06-09: STL-SPEC-001~013 이관, 10건 implemented / 2건 in_dev
- 2026-06-08: STL-DEC-001~022 이관, 21건 accepted

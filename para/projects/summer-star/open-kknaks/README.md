# open-kknaks

## 목적

Claude Code CLI를 Redis 기반 작업 큐와 PTY worker로 실행하는 Python library / CLI 제품의 SSOT다.

규칙: `para/projects/project.md`

## 현재 상태

| Area | Status | Next |
|---|---|---|
| Spec | Claude/Codex provider execution spec 구현 완료 | release note 유지 |
| Baseline | Codex headless 확장 아이디어 1건 | provider 확장 여부 결정 |
| Decision | Claude/Codex provider 기반 task 실행 모델 채택 | 후속 provider 필요 시 새 decision 작성 |
| Work | WORK-001~005 완료 | 후속 운영/확장 작업 분리 |
| Architecture | GitHub Actions 기반 PyPI 배포 절차 1건 | MCP smoke test 방식 결정 |
| Release | 2.0.2 배포 완료 | 다음 배포 시 `60-release/` 추가 |

## 문서 맵

| Stage | Index |
|---|---|
| 00-baseline | `00-baseline/README.md` |
| 10-decision | `10-decision/README.md` |
| 20-spec | `20-spec/README.md` |
| 30-work | `30-work/README.md` |
| 40-architecture | `40-architecture/README.md` |
| 60-release | `60-release/README.md` |
| log | `log.md` |

## 코드 기준

| Source | Path |
|---|---|
| Legacy repo | `/Users/kknaks/git/library/claude_code_pty/open_kknaks` |
| Package | `/Users/kknaks/git/library/claude_code_pty/open_kknaks/open_kknaks` |
| README | `/Users/kknaks/git/library/claude_code_pty/open_kknaks/README.md` |

## 최근 로그

- 2026-06-01: `OKK-REL-002` open-kknaks 2.0.2 PyPI release와 Claude/Codex 배포판 E2E 검증 완료.
- 2026-06-01: WORK-001~005 완료 상태 정리.
- 2026-05-31: 코드 레포에서 WORK-005 Demo와 E2E provider 실행 경로 갱신 완료.
- 2026-05-31: 코드 레포에서 WORK-004 Batch, CLI, MCP provider surface 갱신 완료.
- 2026-05-31: 코드 레포에서 WORK-003 Codex headless runner 구현 완료.
- 2026-05-29: `OKK-SPEC-009` Claude/Codex Runner Adapter 계약 초안 작성.
- 2026-05-29: Claude/Codex provider와 model 기반 task 실행 모델을 decision으로 채택.
- 2026-05-29: legacy 코드 기준으로 `20-spec/` 1차 작성.

# open-kknaks

## 목적

Claude Code CLI를 Redis 기반 작업 큐와 PTY worker로 실행하는 Python library / CLI 제품의 SSOT다.

규칙: `rules/product-doc-pipeline.md`

## 현재 상태

| Area | Status | Next |
|---|---|---|
| Spec | legacy 코드 기준 1차 스펙화 | API/README mismatch 검토 |
| Baseline | Codex headless 확장 아이디어 1건 | provider 확장 여부 결정 |
| Decision | Claude/Codex provider 기반 task 실행 모델 채택 | task/client/runner spec 반영 |
| Work | 만들지 않음 | spec 구체화 후 구현 작업으로 전환 |
| Architecture | GitHub Actions 기반 PyPI 배포 절차 1건 | MCP smoke test 방식 결정 |

## 문서 맵

| Stage | Index |
|---|---|
| 00-baseline | `00-baseline/README.md` |
| 10-decision | `10-decision/README.md` |
| 20-spec | `20-spec/README.md` |
| 40-architecture | `40-architecture/README.md` |
| log | `log.md` |

## 코드 기준

| Source | Path |
|---|---|
| Legacy repo | `/Users/kknaks/git/library/claude_code_pty/open_kknaks` |
| Package | `/Users/kknaks/git/library/claude_code_pty/open_kknaks/open_kknaks` |
| README | `/Users/kknaks/git/library/claude_code_pty/open_kknaks/README.md` |

## 최근 로그

- 2026-05-29: `OKK-SPEC-006` CLI 표면 계약을 provider-aware worker와 AgentClient 기준으로 업데이트.
- 2026-05-29: `OKK-SPEC-005` Batch 실행 계약을 provider task item과 parallel-only 기준으로 업데이트.
- 2026-05-29: `OKK-SPEC-002` Redis Broker 큐 계약을 provider task round-trip 기준으로 업데이트.
- 2026-05-29: provider 기반 실행 모델에 맞춰 `OKK-SPEC-001`, `OKK-SPEC-003`, `OKK-SPEC-004`를 draft로 업데이트.
- 2026-05-29: `OKK-SPEC-010` Codex Headless Runner 실행 계약 초안 작성.
- 2026-05-29: `OKK-SPEC-009` Claude/Codex Runner Adapter 계약 초안 작성.
- 2026-05-29: Claude/Codex provider와 model 기반 task 실행 모델을 decision으로 채택.
- 2026-05-29: legacy 코드 기준으로 `20-spec/` 1차 작성.

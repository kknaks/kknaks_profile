---
type: work
id: OKK-WORK-004
title: "Batch, CLI, MCP Provider 표면 갱신"
status: done
product: open-kknaks
work_type: breaking-change
owner: ""
roles:
  pm: ""
  design: ""
  fe: ""
  be: ""
  qa: ""
  ops: ""
progress: 100
created_at: 2026-05-29
updated_at: 2026-05-29
tags:
  - product/open-kknaks
  - doc/work
  - status/done
links:
  baselines: []
  decisions:
    - "[[decision-001-provider-based-task-execution|OKK-DEC-001]]"
  specs:
    - "[[spec-005-batch-execution|OKK-SPEC-005]]"
    - "[[spec-006-cli-surface|OKK-SPEC-006]]"
    - "[[spec-007-mcp-schema-server|OKK-SPEC-007]]"
    - "[[spec-008-middleware-and-operational-controls|OKK-SPEC-008]]"
  works:
    - "[[work-001-provider-task-model-client-broker|OKK-WORK-001]]"
    - "[[work-002-provider-worker-and-claude-adapter|OKK-WORK-002]]"
  related: []
---

# OKK-WORK-004 Batch, CLI, MCP Provider 표면 갱신

provider 구조가 들어간 뒤 batch API, CLI 출력/옵션, MCP schema-only 문구를 새 public contract에 맞춘다.

## Work Summary

| Field | Value |
|---|---|
| Type | breaking-change |
| Owner |  |
| Status | done |
| Progress | 100% |
| Branch/PR |  |
| Blocker | 없음 |
| Next | 통합 검토와 release note 정리 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM |  | public surface breaking change 확인 | done |
| Design |  | CLI 출력 정보 판단 | done |
| FE |  | 해당 없음 | n/a |
| BE |  | batch/cli/mcp 구현 | done |
| QA |  | public API/CLI/MCP 테스트 | done |
| Ops |  | CLI 운영 문서 영향 확인 | done |

## Scope

- Covers: OKK-SPEC-005, OKK-SPEC-006, OKK-SPEC-007, OKK-SPEC-008
- Out of scope: Task model/provider adapter core 구현, Codex parser 구현, MCP 실행형 server 승격

## Target Surface

- `/Users/kknaks/git/library/claude_code_pty/open_kknaks/open_kknaks/batch.py`
- `/Users/kknaks/git/library/claude_code_pty/open_kknaks/open_kknaks/cli/`
- `/Users/kknaks/git/library/claude_code_pty/open_kknaks/open_kknaks/mcp/server.py`
- `/Users/kknaks/git/library/claude_code_pty/open_kknaks/open_kknaks/middleware/`
- `/Users/kknaks/git/library/claude_code_pty/open_kknaks/tests/`

## Implementation Plan

| Step | Task | Owner | Status | Notes |
|---|---|---|---|---|
| 1 | `BatchRunner.submit_batch(items, queue)` signature 갱신 | BE | done | `mode` 제거 |
| 2 | batch item provider/model/options/provider_options/metadata 복사 | BE | done | item-level queue는 제외 |
| 3 | batch aggregate status 수정 | BE | done | running-only는 `running` |
| 4 | `wait_batch` timeout terminal-only 반환 수정 | BE | done | non-terminal snapshot 제외 |
| 5 | worker CLI `--provider` 추가 | BE | done | default `claude` |
| 6 | CLI status 출력에 provider/model 추가 | BE/Design | done | status, provider, model, queue, priority, error, cost |
| 7 | CLI cancel/status/result가 `AgentClient` 사용 | BE | done | `ClaudeClient` 제거 |
| 8 | MCP schema/guidance를 provider 구조로 갱신 | BE | done | schema-only 유지 |
| 9 | enqueue middleware hook 제외 유지 검증 | QA | done | public submit path 제외 |

## Data / API Notes

MCP는 실행형 queue server로 승격하지 않는다. 13개 tool schema는 유지하되, tool call은 실제 broker/client 작업을 하지 않고 schema-only 안내를 반환한다.

Batch는 sequential controller가 아니다. 모든 item은 독립 task로 enqueue되고 실행 순서는 broker priority와 worker concurrency가 결정한다.

## Acceptance Criteria

- [x] `submit_batch(items, queue="default")`에서 `mode` 인자가 제거된다.
- [x] batch item의 `provider`, `model`, `options`, `provider_options`, `metadata`, `context`가 생성 task에 복사된다.
- [x] 모든 batch task에 동일한 `batch_id`가 저장된다.
- [x] running-only batch aggregate가 `running`으로 계산된다.
- [x] `wait_batch` timeout 시 terminal task만 반환한다.
- [x] worker CLI에 `--provider`가 추가되고 기본값은 `claude`다.
- [x] task status CLI가 provider/model을 출력한다.
- [x] CLI task commands가 `AgentClient`를 사용한다.
- [x] MCP server는 Redis 연결 없이 13개 tool schema를 노출한다.
- [x] MCP tool call은 실제 queue mutation/query를 수행하지 않는다.
- [x] MCP schema와 guidance text가 `AgentClient`, provider/model/options/provider_options 기준이다.
- [x] enqueue middleware hook은 public `AgentClient.submit` path에서 제외된다.

## Test Plan

| Case | Owner | Status | Notes |
|---|---|---|---|
| Batch submit copies provider fields | QA | done | unit/integration |
| Batch mode removed | QA | done | API test |
| Batch running aggregate | QA | done | unit |
| Batch wait timeout terminal-only | QA | done | unit |
| Worker CLI provider option | QA | done | typer CliRunner |
| Task status shows provider/model | QA | done | CliRunner |
| CLI uses AgentClient | QA | done | import/behavior |
| MCP list_tools has 13 schemas | QA | done | mcp unit |
| MCP call_tool schema-only text | QA | done | mcp unit |
| Enqueue hooks not called by submit | QA | done | middleware regression |

## Done Criteria

- [x] 담당 role별 완료 상태가 갱신됐다.
- [x] 연결된 spec의 Work Handoff와 계약 섹션을 Acceptance Criteria에 반영했다.
- [x] 필요한 테스트/검증이 끝났다.
- [x] product `log.md`와 `30-work/README.md`가 갱신됐다.

## Open Issues

- 없음.

# Work Index

규칙: `rules/product-doc-pipeline.md`

> spec을 실제 구현 작업으로 내린 work 목록과 spec coverage를 관리한다.

## Work 목록

| ID | Title | Type | Owner | Status | Progress | Covers Spec | PR/Branch | Next |
|---|---|---|---|---|---|---|---|---|
| [OKK-WORK-001](work-001-provider-task-model-client-broker.md) | Provider Task Model, AgentClient, Broker 계약 구현 | breaking-change |  | done | 100% | OKK-SPEC-001, 002, 003, 009 |  | 완료 |
| [OKK-WORK-002](work-002-provider-worker-and-claude-adapter.md) | Provider Worker와 Claude Adapter 구현 | refactor |  | done | 100% | OKK-SPEC-004, 008, 009 |  | 완료 |
| [OKK-WORK-003](work-003-codex-headless-runner.md) | Codex Headless Runner 구현 | new-feature |  | done | 100% | OKK-SPEC-009, 010 |  | 완료 |
| [OKK-WORK-004](work-004-batch-cli-mcp-provider-surface.md) | Batch, CLI, MCP Provider 표면 갱신 | breaking-change |  | done | 100% | OKK-SPEC-005, 006, 007, 008 |  | 완료 |
| [OKK-WORK-005](work-005-demo-e2e-provider-surface.md) | Demo와 E2E Provider 실행 경로 갱신 | qa-enablement |  | done | 100% | OKK-SPEC-003, 006, 009, 010 |  | 완료 |
| [OKK-WORK-006](work-006-slack-knowledge-capture.md) | Slack Thread 기반 inbox·reference 지식 수집 | new-feature |  | in_progress | 90% | OKK-SPEC-011, 003, 008 | `feat/knowledge-graph` | 실제 Slack mention→thread smoke |

## Spec Coverage

| Spec | Work | Status |
|---|---|---|
| [OKK-SPEC-001](../20-spec/spec-001-task-model-and-lifecycle.md) | [OKK-WORK-001](work-001-provider-task-model-client-broker.md) | done |
| [OKK-SPEC-002](../20-spec/spec-002-redis-broker-queue-contract.md) | [OKK-WORK-001](work-001-provider-task-model-client-broker.md) | done |
| [OKK-SPEC-003](../20-spec/spec-003-python-client-and-streaming-api.md) | [OKK-WORK-001](work-001-provider-task-model-client-broker.md) | done |
| [OKK-SPEC-003](../20-spec/spec-003-python-client-and-streaming-api.md) | [OKK-WORK-005](work-005-demo-e2e-provider-surface.md) | done |
| [OKK-SPEC-004](../20-spec/spec-004-pty-worker-runtime.md) | [OKK-WORK-002](work-002-provider-worker-and-claude-adapter.md) | done |
| [OKK-SPEC-005](../20-spec/spec-005-batch-execution.md) | [OKK-WORK-004](work-004-batch-cli-mcp-provider-surface.md) | done |
| [OKK-SPEC-006](../20-spec/spec-006-cli-surface.md) | [OKK-WORK-004](work-004-batch-cli-mcp-provider-surface.md) | done |
| [OKK-SPEC-006](../20-spec/spec-006-cli-surface.md) | [OKK-WORK-005](work-005-demo-e2e-provider-surface.md) | done |
| [OKK-SPEC-007](../20-spec/spec-007-mcp-schema-server.md) | [OKK-WORK-004](work-004-batch-cli-mcp-provider-surface.md) | done |
| [OKK-SPEC-008](../20-spec/spec-008-middleware-and-operational-controls.md) | [OKK-WORK-002](work-002-provider-worker-and-claude-adapter.md), [OKK-WORK-004](work-004-batch-cli-mcp-provider-surface.md) | done |
| [OKK-SPEC-009](../20-spec/spec-009-claude-codex-runner-adapter.md) | [OKK-WORK-001](work-001-provider-task-model-client-broker.md), [OKK-WORK-002](work-002-provider-worker-and-claude-adapter.md), [OKK-WORK-003](work-003-codex-headless-runner.md) | done |
| [OKK-SPEC-010](../20-spec/spec-010-codex-headless-runner.md) | [OKK-WORK-003](work-003-codex-headless-runner.md) | done |
| [OKK-SPEC-009](../20-spec/spec-009-claude-codex-runner-adapter.md) | [OKK-WORK-005](work-005-demo-e2e-provider-surface.md) | done |
| [OKK-SPEC-010](../20-spec/spec-010-codex-headless-runner.md) | [OKK-WORK-005](work-005-demo-e2e-provider-surface.md) | done |
| [OKK-SPEC-011](../20-spec/spec-011-slack-knowledge-capture.md) | [OKK-WORK-006](work-006-slack-knowledge-capture.md) | in_progress |

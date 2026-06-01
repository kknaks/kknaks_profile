# Spec Index

규칙: `rules/product-doc-pipeline.md`

## Spec 목록

| ID | Title | Status | Decision | Coverage | Work |
|---|---|---|---|---|---|
| [OKK-SPEC-001](spec-001-task-model-and-lifecycle.md) | Task 모델과 생명주기 | draft | [OKK-DEC-001](../10-decision/decision-001-provider-based-task-execution.md) | `open_kknaks/task.py`, `open_kknaks/client.py`, `open_kknaks/worker/worker.py` | 없음 |
| [OKK-SPEC-002](spec-002-redis-broker-queue-contract.md) | Redis Broker 큐 계약 | draft | [OKK-DEC-001](../10-decision/decision-001-provider-based-task-execution.md) | `open_kknaks/broker/` | 없음 |
| [OKK-SPEC-003](spec-003-python-client-and-streaming-api.md) | Python Client와 Streaming API | draft | [OKK-DEC-001](../10-decision/decision-001-provider-based-task-execution.md) | `open_kknaks/client.py`, `AgentClient` | 없음 |
| [OKK-SPEC-004](spec-004-pty-worker-runtime.md) | PTY Worker 실행 계약 | draft | [OKK-DEC-001](../10-decision/decision-001-provider-based-task-execution.md) | `open_kknaks/worker/` | 없음 |
| [OKK-SPEC-005](spec-005-batch-execution.md) | Batch 실행 계약 | draft | [OKK-DEC-001](../10-decision/decision-001-provider-based-task-execution.md) | `open_kknaks/batch.py` | 없음 |
| [OKK-SPEC-006](spec-006-cli-surface.md) | CLI 표면 계약 | draft | [OKK-DEC-001](../10-decision/decision-001-provider-based-task-execution.md) | `open_kknaks/cli/` | 없음 |
| [OKK-SPEC-007](spec-007-mcp-schema-server.md) | MCP schema server 계약 | draft | [OKK-DEC-001](../10-decision/decision-001-provider-based-task-execution.md) | `open_kknaks/mcp/server.py` | 없음 |
| [OKK-SPEC-008](spec-008-middleware-and-operational-controls.md) | Middleware와 운영 제어 | stable | 없음 | `open_kknaks/middleware/` | 없음 |
| [OKK-SPEC-009](spec-009-claude-codex-runner-adapter.md) | Claude/Codex Runner Adapter 계약 | draft | [OKK-DEC-001](../10-decision/decision-001-provider-based-task-execution.md) | `open_kknaks/worker/`, runner adapter 후보 | 없음 |
| [OKK-SPEC-010](spec-010-codex-headless-runner.md) | Codex Headless Runner 실행 계약 | draft | [OKK-DEC-001](../10-decision/decision-001-provider-based-task-execution.md) | Codex runner adapter 후보 | 없음 |

## 읽는 순서

| Reader | Order |
|---|---|
| 라이브러리 사용자 | OKK-SPEC-003 -> OKK-SPEC-001 -> OKK-SPEC-002 |
| worker 운영자 | OKK-SPEC-004 -> OKK-SPEC-002 -> OKK-SPEC-008 |
| CLI 사용자 | OKK-SPEC-006 -> OKK-SPEC-001 |
| MCP 연동자 | OKK-SPEC-007 -> OKK-SPEC-003 |
| provider runner 구현 | OKK-SPEC-009 -> OKK-SPEC-010 -> OKK-SPEC-004 -> OKK-SPEC-001 |
| 구현 유지보수 | OKK-SPEC-001 -> OKK-SPEC-002 -> OKK-SPEC-004 -> OKK-SPEC-008 -> OKK-SPEC-009 -> OKK-SPEC-010 |

## Legacy 코드 기준 mismatch

| 항목 | 현재 코드 기준 |
|---|---|
| CLI/package naming | provider 구조 버전은 `AgentClient`와 provider-aware worker를 기준으로 하고 legacy `ClaudeClient`/`ClaudeWorker` 이름은 새 public contract에서 제외 |
| MCP tool 실행 | tool schema만 제공하고 실제 queue 작업은 수행하지 않음 |
| cancel semantics | client는 persisted status만 `cancelled`로 바꾸며 running process를 직접 종료하지 않음 |
| middleware enqueue hook | `before_enqueue`, `after_enqueue`는 정의되어 있으나 `ClaudeClient.submit`에서 호출되지 않음 |
| batch mode | legacy는 `mode` 인자를 받지만 sequential 제어가 없고, provider 구조 버전에서는 `mode`를 제거 |
| batch status/wait | legacy는 running-only batch를 `pending`으로 볼 수 있고 timeout 시 non-terminal snapshot도 반환할 수 있으나, provider 구조 버전은 running aggregate와 terminal-only timeout 반환을 요구 |
| non-JSON/stderr context | legacy Claude PTY parser는 non-JSON line을 publish/save하지 않으나, provider 구조 버전은 stream publish 없이 failure debug context 보존을 요구 |
| buffered drain | legacy executor의 종료 직후 remaining/flush line 처리 일부가 publish path를 타지 않을 수 있으나, provider 구조 버전은 remaining JSONL도 stream publish 대상 |
| pending cancel consumption | legacy client cancel은 marker만 저장하고 worker가 dequeue 후 `running`으로 덮어쓸 수 있으나, provider 구조 버전은 cancelled task skip/ack 처리 필요 |
| MCP schema wording | legacy MCP 안내는 Claude 중심 설명을 포함하므로 provider 구조 버전은 `AgentClient`와 provider fields 기준으로 갱신 |

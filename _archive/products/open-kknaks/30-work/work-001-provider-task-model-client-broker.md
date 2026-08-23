---
type: work
id: OKK-WORK-001
title: "Provider Task Model, AgentClient, Broker 계약 구현"
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
  baselines:
    - "[[OKK-BL-001-codex-headless-runner|OKK-BL-001]]"
  decisions:
    - "[[decision-001-provider-based-task-execution|OKK-DEC-001]]"
  specs:
    - "[[spec-001-task-model-and-lifecycle|OKK-SPEC-001]]"
    - "[[spec-002-redis-broker-queue-contract|OKK-SPEC-002]]"
    - "[[spec-003-python-client-and-streaming-api|OKK-SPEC-003]]"
    - "[[spec-009-claude-codex-runner-adapter|OKK-SPEC-009]]"
  works: []
  related: []
---

# OKK-WORK-001 Provider Task Model, AgentClient, Broker 계약 구현

provider 기반 실행 모델의 공통 데이터 계약을 먼저 구현한다. `Task`, Redis broker round-trip, public Python client를 `AgentClient` 기준으로 바꾼다.

## Work Summary

| Field | Value |
|---|---|
| Type | breaking-change |
| Owner |  |
| Status | done |
| Progress | 100% |
| Branch/PR |  |
| Blocker | 없음 |
| Next | OKK-WORK-003 Codex adapter 구현 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM |  | legacy public API 제거 범위 확인 | todo |
| Design |  | 해당 없음 | n/a |
| FE |  | 해당 없음 | n/a |
| BE |  | task/client/broker 구현 | done |
| QA |  | model/client/broker 테스트 | done |
| Ops |  | migration/release note 영향 확인 | todo |

## Scope

- Covers: OKK-SPEC-001, OKK-SPEC-002, OKK-SPEC-003, OKK-SPEC-009의 provider field/client/broker 계약
- Out of scope: 실제 Claude/Codex process 실행, CLI/MCP 표면 갱신, batch API 갱신

## Target Surface

- `/Users/kknaks/git/library/claude_code_pty/open_kknaks/open_kknaks/task.py`
- `/Users/kknaks/git/library/claude_code_pty/open_kknaks/open_kknaks/client.py`
- `/Users/kknaks/git/library/claude_code_pty/open_kknaks/open_kknaks/broker/`
- `/Users/kknaks/git/library/claude_code_pty/open_kknaks/open_kknaks/__init__.py`
- `/Users/kknaks/git/library/claude_code_pty/open_kknaks/tests/`

## Implementation Plan

| Step | Task | Owner | Status | Notes |
|---|---|---|---|---|
| 1 | provider constants module 추가 | BE | done | `PROVIDER_CLAUDE`, `PROVIDER_CODEX`, `SUPPORTED_PROVIDERS`, `DEFAULT_PROVIDER` |
| 2 | `Task`에 `provider`, `options`, `provider_options` 추가 | BE | done | default provider는 `claude` |
| 3 | legacy Claude task override fields 제거 또는 compatibility boundary 정리 | BE | done | public client kwargs와 Task legacy fields 제거 |
| 4 | Redis broker JSON round-trip 검증 | BE/QA | done | provider/options/provider_options 보존 |
| 5 | `AgentClient` public API 구현 | BE | done | `ClaudeClient`는 module alias만 임시 유지, root public export에서는 제외 |
| 6 | client cancel/status/result/stream 동작 유지 | BE/QA | done | cancel은 persisted marker |
| 7 | package root export와 tests 갱신 | BE/QA | done | legacy client tests를 `AgentClient` 기준으로 갱신 |

## Data / API Notes

`AgentClient.submit()`은 `provider`, `model`, `options`, `provider_options`, `metadata`를 받는다. Claude 전용 옵션은 public submit 인자에서 제거하고 `provider_options`로 전달한다.

알 수 없는 provider는 client enqueue 단계에서 조용히 보정하지 않는다. provider validation의 최종 방어선은 worker 실행 전 검증이다.

## Acceptance Criteria

- [x] `Task.provider` default가 `claude`다.
- [x] `Task.options`와 `Task.provider_options`가 dict로 저장된다.
- [x] Redis broker enqueue/dequeue/get/update에서 provider fields가 손실 없이 round-trip 된다.
- [x] `AgentClient`가 public client 이름으로 export된다.
- [x] `AgentClient.submit()`이 provider/model/options/provider_options 기반 task를 생성한다.
- [x] legacy `ClaudeClient`와 legacy Claude-specific submit kwargs가 public contract에서 제거된다.
- [x] `AgentClient.cancel()`은 task status를 `cancelled`로 저장하고 running process interrupt를 보장하지 않는다.
- [x] `AgentClient.result()`와 `stream()`의 timeout/filter semantics가 기존 계약을 유지한다.

## Test Plan

| Case | Owner | Status | Notes |
|---|---|---|---|
| Task default provider/options serialization | QA | done | unit |
| Redis broker provider field round-trip | QA | done | fakeredis/lua |
| AgentClient submit creates provider task | QA | done | client integration |
| AgentClient cancel persisted marker | QA | done | no process interrupt assertion |
| Legacy ClaudeClient import removal/update | QA | done | root export와 module alias 모두 제거 |

## Done Criteria

- [x] 담당 role별 완료 상태가 갱신됐다.
- [x] 연결된 spec의 Work Handoff와 계약 섹션을 Acceptance Criteria에 반영했다.
- [x] 필요한 테스트/검증이 끝났다.
- [x] product `log.md`와 `30-work/README.md`가 갱신됐다.

## Open Issues

- 없음.

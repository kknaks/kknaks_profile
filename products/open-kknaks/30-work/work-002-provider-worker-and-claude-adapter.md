---
type: work
id: OKK-WORK-002
title: "Provider Worker와 Claude Adapter 구현"
status: done
product: open-kknaks
work_type: refactor
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
    - "[[spec-004-pty-worker-runtime|OKK-SPEC-004]]"
    - "[[spec-008-middleware-and-operational-controls|OKK-SPEC-008]]"
    - "[[spec-009-claude-codex-runner-adapter|OKK-SPEC-009]]"
  works:
    - "[[work-001-provider-task-model-client-broker|OKK-WORK-001]]"
  related: []
---

# OKK-WORK-002 Provider Worker와 Claude Adapter 구현

legacy `ClaudeWorker`/`ClaudeCodeExecutor`의 동작을 보존하면서 worker 실행 계층을 provider-neutral adapter 구조로 분리한다.

## Work Summary

| Field | Value |
|---|---|
| Type | refactor |
| Owner |  |
| Status | done |
| Progress | 100% |
| Branch/PR |  |
| Blocker | 없음 |
| Next | OKK-WORK-003 Codex adapter 구현 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM |  | provider 범위와 breaking change 확인 | todo |
| Design |  | 해당 없음 | n/a |
| FE |  | 해당 없음 | n/a |
| BE |  | worker/adapter/middleware 구현 | done |
| QA |  | worker/executor regression 검증 | done |
| Ops |  | worker boot/health/logging 영향 확인 | todo |

## Scope

- Covers: OKK-SPEC-004, OKK-SPEC-008, OKK-SPEC-009의 worker flow와 Claude adapter 계약
- Out of scope: Codex adapter 상세 구현, public CLI/MCP 문구 갱신, batch API

## Target Surface

- `/Users/kknaks/git/library/claude_code_pty/open_kknaks/open_kknaks/worker/`
- `/Users/kknaks/git/library/claude_code_pty/open_kknaks/open_kknaks/config.py`
- `/Users/kknaks/git/library/claude_code_pty/open_kknaks/open_kknaks/middleware/`
- `/Users/kknaks/git/library/claude_code_pty/open_kknaks/tests/`

## Implementation Plan

| Step | Task | Owner | Status | Notes |
|---|---|---|---|---|
| 1 | runner adapter interface 추가 | BE | done | health/check/execute/cancel |
| 2 | worker provider selection 추가 | BE | done | unknown provider는 command 미실행 failed |
| 3 | legacy Claude executor를 Claude adapter로 감싸기 | BE | done | PTY 동작 보존 |
| 4 | `provider_options` 기반 Claude command build | BE | done | `_merge_config`가 provider_options만 반영 |
| 5 | `options.resume.session_id`, `options.cwd`, `options.timeout_sec` 반영 | BE | done | Claude config/task runtime field로 매핑 |
| 6 | pending cancel marker skip/ack 처리 | BE | done | dequeue 후 cancelled task 실행 방지 |
| 7 | remaining/flush JSONL publish 누락 수정 | BE | done | stream subscriber 누락 방지 |
| 8 | non-JSON stdout/stderr debug context 보존 | BE | done | stream publish는 하지 않음 |
| 9 | middleware process/boot/shutdown hook regression 검증 | QA | done | 전체 regression 통과 |

## Data / API Notes

public client cancel은 process interrupt가 아니다. worker 내부 shutdown/cancel과 adapter cancel은 process termination을 지원할 수 있지만 public cancel의 보장으로 노출하지 않는다.

Claude PTY stdout/stderr는 merged stream이다. non-JSON line은 공통 stream event로 publish하지 않고 failure diagnosis context로만 보존한다.

## Acceptance Criteria

- [x] worker가 task provider를 보고 runner adapter를 선택한다.
- [x] unknown provider는 CLI 실행 없이 task를 `failed`로 저장한다.
- [x] Claude adapter가 기존 `claude -p --output-format stream-json --verbose --include-partial-messages` 실행 계약을 유지한다.
- [x] Claude command는 legacy task fields가 아니라 `provider_options`와 common `options`에서 만들어진다.
- [x] `options.resume.session_id`가 Claude `--resume`으로 매핑된다.
- [x] pending task가 `cancelled` marker 상태면 worker가 실행하지 않고 ack한다.
- [x] PTY 종료 시 remaining/flush JSONL event도 stream publish path를 탄다.
- [x] non-JSON stdout/stderr는 stream event로 publish되지 않고 failure debug context에 보존된다.
- [x] middleware boot/process/shutdown hook 호출 순서가 유지된다.

## Test Plan

| Case | Owner | Status | Notes |
|---|---|---|---|
| Unknown provider fails without command | QA | done | fake adapter/worker |
| Claude command maps provider_options | QA | done | `_merge_config` unit |
| Resume maps to `--resume` | QA | done | `_merge_config` unit |
| Pending cancel skip/ack | QA | done | worker integration |
| Remaining JSONL publish | QA | done | executor parser test |
| Non-JSON stderr debug context | QA | done | failure test |
| Middleware order regression | QA | done | existing middleware tests 통과 |

## Done Criteria

- [ ] 담당 role별 완료 상태가 갱신됐다.
- [ ] 연결된 spec의 Work Handoff와 계약 섹션을 Acceptance Criteria에 반영했다.
- [ ] 필요한 테스트/검증이 끝났다.
- [ ] product `log.md`와 `30-work/README.md`가 갱신됐다.

## Open Issues

- 없음.

---
type: work
id: OKK-WORK-003
title: "Codex Headless Runner 구현"
status: done
product: open-kknaks
work_type: new-feature
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
    - "[[spec-009-claude-codex-runner-adapter|OKK-SPEC-009]]"
    - "[[spec-010-codex-headless-runner|OKK-SPEC-010]]"
  works:
    - "[[work-001-provider-task-model-client-broker|OKK-WORK-001]]"
    - "[[work-002-provider-worker-and-claude-adapter|OKK-WORK-002]]"
  related: []
---

# OKK-WORK-003 Codex Headless Runner 구현

`codex` provider adapter를 추가해 `codex exec --json`과 `codex exec resume` JSONL stream을 공통 `TaskResult`/`StreamEvent`로 변환한다.

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner |  |
| Status | done |
| Progress | 100% |
| Branch/PR |  |
| Blocker | 없음 |
| Next | OKK-WORK-004 Batch/CLI/MCP provider surface 갱신 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM |  | Codex 옵션 범위 확인 | todo |
| Design |  | 해당 없음 | n/a |
| FE |  | 해당 없음 | n/a |
| BE |  | Codex adapter/parser 구현 | done |
| QA |  | command/parser/failure 테스트 | done |
| Ops |  | codex binary/version/health 확인 | done |

## Scope

- Covers: OKK-SPEC-009의 `codex` adapter, OKK-SPEC-010 전체
- Out of scope: `codex exec review`, custom provider registry, OpenAI/local provider 추가

## Target Surface

- `/Users/kknaks/git/library/claude_code_pty/open_kknaks/open_kknaks/worker/`
- `/Users/kknaks/git/library/claude_code_pty/open_kknaks/open_kknaks/task.py`
- `/Users/kknaks/git/library/claude_code_pty/open_kknaks/tests/`

## Implementation Plan

| Step | Task | Owner | Status | Notes |
|---|---|---|---|---|
| 1 | Codex adapter class 추가 | BE | done | stdio subprocess 기반 |
| 2 | `codex exec --json` command builder 구현 | BE | done | new session |
| 3 | `resume.session`/`resume.last` command builder 구현 | BE | done | validation 포함 |
| 4 | provider_options allowlist validation 구현 | BE | done | unknown key fail |
| 5 | sandbox default `workspace-write` 적용 | BE | done | 명시 옵션만 override |
| 6 | stdout JSONL parser 구현 | BE | done | event/item mapping |
| 7 | stderr/non-JSON debug context 보존 | BE | done | stream publish 제외 |
| 8 | remaining JSONL drain/publish 구현 | BE | done | newline 없는 마지막 event |
| 9 | timeout/cancel/non-zero/auth failure 처리 | BE | done | TaskResult/failed mapping |
| 10 | Codex tests 추가 | QA | done | subprocess fake 중심 |

## Data / API Notes

`provider_options`는 자유 dict 입력이지만 Codex adapter는 알 수 없는 key를 fail-fast 처리한다. `json=true`는 공통 stream/result parsing을 위해 강제 기본값이다.

Codex `thread_id`는 공통 `TaskResult.session_id`와 `Task.result_session_id`에 저장한다.

## Acceptance Criteria

- [x] `provider="codex"` task가 Codex adapter로 실행된다.
- [x] new session command가 `codex exec --json` 형태로 생성된다.
- [x] `resume.mode=session`은 `codex exec resume <thread_id> --json`을 생성하고 `session_id` 누락 시 실패한다.
- [x] `resume.mode=last`는 `codex exec resume --last --json`을 생성한다.
- [x] `provider_options.sandbox` 기본값은 `workspace-write`다.
- [x] unknown `provider_options` key는 command 실행 전 validation failure가 된다.
- [x] stdout JSONL event가 공통 `StreamEvent`로 변환된다.
- [x] `thread.started.thread_id`가 `TaskResult.session_id`로 저장된다.
- [x] stderr/non-JSON line은 stream publish 대상이 아니며 debug context에 보존된다.
- [x] subprocess 종료 시 remaining JSONL도 parse/publish된다.
- [x] timeout, cancel, non-zero exit, auth failure가 task failure/cancel 계약대로 처리된다.
- [x] `codex exec review`는 구현하지 않는다.

## Test Plan

| Case | Owner | Status | Notes |
|---|---|---|---|
| New command build | QA | done | unit |
| Resume session/last command build | QA | done | unit |
| Unknown option validation | QA | done | unit |
| Sandbox default | QA | done | unit |
| JSONL event mapping | QA | done | parser unit |
| Thread id session result | QA | done | adapter unit |
| stderr/non-JSON debug context | QA | done | adapter failure |
| timeout/cancel/non-zero | QA | done | subprocess fake |

## Done Criteria

- [x] 담당 role별 완료 상태가 갱신됐다.
- [x] 연결된 spec의 Work Handoff와 계약 섹션을 Acceptance Criteria에 반영했다.
- [x] 필요한 테스트/검증이 끝났다.
- [x] product `log.md`와 `30-work/README.md`가 갱신됐다.

## Open Issues

- 없음.

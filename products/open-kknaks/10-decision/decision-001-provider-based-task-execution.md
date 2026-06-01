---
type: decision
id: OKK-DEC-001
title: "Provider 기반 task 실행 모델 도입"
status: accepted
product: open-kknaks
created_at: 2026-05-29
updated_at: 2026-05-29
tags:
  - product/open-kknaks
  - doc/decision
  - status/accepted
links:
  baselines:
    - "[[OKK-BL-001-codex-headless-runner|OKK-BL-001]]"
  decisions: []
  specs:
    - "[[spec-009-claude-codex-runner-adapter|OKK-SPEC-009]]"
    - "[[spec-010-codex-headless-runner|OKK-SPEC-010]]"
  works: []
  related: []
---

# OKK-DEC-001 Provider 기반 task 실행 모델 도입

`open-kknaks`는 Claude Code 전용 실행 큐가 아니라, task별로 `claude` 또는 `codex` headless runner와 model을 선택할 수 있는 agent queue로 확장한다.

## Context

- 관련 baseline: `OKK-BL-001 Codex headless runner 확장 아이디어`
- 문제/기회: Codex headless runner를 붙이려면 기존 Claude PTY 실행 계약과 다른 stdio/JSONL 실행 계약을 받아들여야 한다.
- 결정이 필요한 이유: Codex를 단순 예외 케이스로 붙이면 task, worker, stream, session 모델이 Claude 중심으로 굳어진다.

## Options

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| A | Claude Code 전용 queue 유지 | 현재 코드와 가장 가깝다 | Codex/OpenAI 확장 시 중복 구현이 커진다 | 단기 유지보수에는 유리 |
| B | Codex runner만 특수 케이스로 추가 | 빠르게 Codex를 붙일 수 있다 | worker와 task 모델에 provider 분기가 퍼진다 | 이후 OpenAI API 추가 시 다시 구조 변경 필요 |
| C | provider/model 기반 agent queue로 확장 | Claude와 Codex headless runner를 같은 queue 계약에 태울 수 있다 | task 모델과 runner 계층을 재정의해야 한다 | 채택 |

## Decision

- 채택: `Task`는 실행 대상 LLM을 `provider`와 `model`로 표현한다.
- 채택: Worker는 task의 `provider`를 보고 provider registry에서 runner adapter를 선택한다.
- 채택: 이번 범위의 provider 값은 `claude`, `codex`로 제한한다.
- 채택: 공통 실행 옵션은 `options`, provider별 실행 옵션은 `provider_options`에 분리한다.
- 채택: 세션 이어가기는 provider 공통 실행 개념으로 보고 `options.resume`에 둔다.
- 채택: `provider_options`는 1차 구현에서 자유 dict로 두고, 각 runner 내부에서 필요한 최소 검증만 수행한다.
- 채택: Codex runner의 기본 sandbox mode는 `workspace-write`로 둔다.
- 채택: Claude Code와 Codex CLI는 각각 runner adapter로 분리한다.
- 채택: 기존 Claude 사용자는 기본 provider를 `claude`로 두어 호환성을 유지한다.
- 채택: provider 구조가 들어가는 버전은 breaking change로 보고 legacy Claude task override 필드는 제거한다.
- 채택: provider-neutral Python client 이름은 `AgentClient`로 한다.
- 채택: public cancel 계약은 기존처럼 persisted status marker로 유지하고 running process interrupt는 보장하지 않는다.
- 채택: `AgentClient.submit()`은 enqueue middleware hook을 실행하지 않는다.
- 기각: Codex를 Claude runner 내부의 특수 모드로 넣지 않는다.
- 기각: `openai`, `ollama`, `lmstudio`, 사내 gateway 같은 범용/custom provider는 이번 스펙 범위에 포함하지 않는다.
- 제외: Codex review mode는 이번 목표에서 다루지 않는다.

## Rationale

- 판단 기준: queue 계약은 안정적으로 유지하고, 실행 방식 차이는 adapter 계층에 가둔다.
- 대안 대비 이유: Codex는 stdio/JSONL/thread 기반이고 Claude Code는 PTY/stream-json/session 기반이라 같은 runner에 넣기 어렵다.
- 리스크: 공통 옵션과 provider별 옵션의 경계가 명확하지 않으면 사용자 API가 흔들릴 수 있다.

## Target Layering

```text
Client
  -> Task(provider, model, prompt, options, provider_options)
  -> Broker Queue
  -> Worker
  -> Provider Registry
  -> Runner Adapter
      - ClaudeRunner
      - CodexRunner
  -> Event Normalizer
```

## Scope

- In:
  - task에 provider/model/options 개념 추가
  - 공통 `options`와 provider별 `provider_options` 경계 정의
  - Claude/Codex session resume을 공통 `options.resume` 계약으로 표현
  - worker의 runner 선택 책임을 provider registry로 분리
  - provider별 runner adapter 경계 정의
  - 공통 stream event와 provider-native payload 보존 정책 정의
- Out:
  - OpenAI API provider
  - custom provider registry
  - local provider
  - Codex review 자동화 작업 타입
  - provider별 인증 저장소 통합
  - multi-provider routing/fallback 정책
  - `danger-full-access` 기본 허용
- 영향을 받는 spec 후보:
  - `OKK-SPEC-001 Task 모델과 생명주기`
  - `OKK-SPEC-003 Python Client와 Streaming API`
  - `OKK-SPEC-004 PTY Worker 실행 계약`
  - `OKK-SPEC-009 Claude/Codex Runner Adapter 계약`
  - `OKK-SPEC-010 Codex Headless Runner 실행 계약`

## Open Questions

없음. 세부 validation 규칙은 spec에서 확정한다.

## Option Shape

공통 옵션은 runner 종류와 관계없이 worker가 해석할 수 있는 값이다.

```json
{
  "provider": "codex",
  "model": "gpt-5-codex",
  "prompt": "작업 내용",
  "options": {
    "cwd": "/repo",
    "timeout_sec": 600,
    "stream": true,
    "resume": {
      "mode": "new"
    }
  },
  "provider_options": {
    "sandbox": "workspace-write",
    "json": true
  }
}
```

초기 기준:

| Field | Owner | Examples |
|---|---|---|
| `options` | `open-kknaks` 공통 worker/client 계약 | `cwd`, `timeout_sec`, `stream`, `resume.mode`, `resume.session_id` |
| `provider_options` | provider runner adapter 계약 | Codex `sandbox`, `add_dir`, `profile`; Claude CLI 전용 flag |

`provider_options`는 초기 spec에서 provider별 typed schema를 강제하지 않는다. 실제 Claude/Codex 사용 중 반복되는 옵션이 안정되면 이후 spec에서 typed option으로 승격한다.

Codex runner의 기본 `provider_options.sandbox`는 `workspace-write`다. `read-only`는 사용자가 명시적으로 더 제한적인 실행을 원할 때 지정하고, `danger-full-access`는 기본값으로 사용하지 않는다.

### Option Comparison

아래 표는 이번 decision에서 다루는 headless 실행 옵션 후보 전체다. Claude 쪽은 legacy 구현의 `ClaudeConfig`와 executor command build 기준이고, Codex 쪽은 `CODEX_ANALYSIS.md`의 `codex exec` 옵션 기준이다. 최종 필드명과 validation은 spec에서 확정한다.

| 공통 옵션 (`options`) | Claude 전용 옵션 (`provider_options`) | Codex 전용 옵션 (`provider_options`) |
|---|---|---|
| `cwd`: 실행 working directory | `output_format`: 기본 `stream-json` | `json`: `--json`/`--experimental-json` |
| `timeout_sec`: task 실행 timeout | `verbose`: `--verbose` | `output_last_message`: `-o`, `--output-last-message` |
| `stream`: stream event 발행 여부 | `include_partial_messages`: `--include-partial-messages` | `output_schema`: `--output-schema` |
| `resume.mode`: `new`, `session`, `last` | `allowed_tools`: `--allowedTools` 반복 | `ephemeral`: `--ephemeral` |
| `resume.session_id`: 이어갈 session/thread id | `disallowed_tools`: `--disallowedTools` 반복 | `skip_git_repo_check`: `--skip-git-repo-check` |
| `prompt`: 실행 prompt | `permission_mode`: `--permission-mode` | `ignore_user_config`: `--ignore-user-config` |
| `model`: provider model override | `dangerously_skip_permissions`: `--dangerously-skip-permissions` | `ignore_rules`: `--ignore-rules` |
| `context`: task 추가 context | `add_dirs`: `--add-dir` 반복 | `strict_config`: `--strict-config` |
| `queue`: enqueue 대상 queue | `claude_bin`: worker/provider 설정에서만 허용 | `color`: `--color` |
| `priority`: queue priority |  | `sandbox`: `-s`, `--sandbox`; 기본 `workspace-write` |
| `metadata`: task metadata |  | `bypass_approvals_and_sandbox`: `--dangerously-bypass-approvals-and-sandbox`, `--yolo` |
|  |  | `bypass_hook_trust`: `--dangerously-bypass-hook-trust` |
|  |  | `profile`: `-p`, `--profile` |
|  |  | `profile_v2`: `--profile-v2` |
|  |  | `add_dirs`: `--add-dir` 반복 |
|  |  | `images`: `-i`, `--image` 반복 |
|  |  | `oss`: `--oss` |
|  |  | `local_provider`: `--local-provider` |
|  |  | `config`: `-c`, `--config key=value` 반복 |
|  |  | `enable`: `--enable` 반복 |
|  |  | `disable`: `--disable` 반복 |

이번 목표는 기존 Claude headless 실행과 유사한 큐 기반 실행 경험을 Codex headless에도 제공하는 것이다.

```json
{
  "provider": "claude",
  "model": "claude-sonnet-4",
  "prompt": "작업 내용",
  "options": {
    "cwd": "/repo",
    "timeout_sec": 600,
    "stream": true,
    "resume": {
      "mode": "new"
    }
  },
  "provider_options": {
    "output_format": "stream-json"
  }
}
```

```json
{
  "provider": "codex",
  "model": "gpt-5-codex",
  "prompt": "작업 내용",
  "options": {
    "cwd": "/repo",
    "timeout_sec": 600,
    "stream": true,
    "resume": {
      "mode": "session",
      "session_id": "codex-thread-id"
    }
  },
  "provider_options": {
    "json": true,
    "sandbox": "workspace-write"
  }
}
```

`options.resume`의 공통 의미:

| Mode | Meaning | Provider mapping |
|---|---|---|
| `new` | 새 세션으로 실행 | Claude/Codex 일반 headless 실행 |
| `session` | 지정한 세션을 이어서 실행 | Claude resume 값, Codex `codex exec resume <THREAD_ID>` |
| `last` | provider가 지원하는 최근 세션을 이어서 실행 | Codex `resume --last`; Claude는 지원 여부를 spec에서 확인 |

## Resulting Spec

| ID | Title | Action | File | Notes |
|---|---|---|---|---|
| [OKK-SPEC-001](../20-spec/spec-001-task-model-and-lifecycle.md) | Task 모델과 생명주기 | update | `spec-001-task-model-and-lifecycle.md` | provider/model/options 필드와 lifecycle 영향 반영 |
| [OKK-SPEC-003](../20-spec/spec-003-python-client-and-streaming-api.md) | Python Client와 Streaming API | update | `spec-003-python-client-and-streaming-api.md` | client submit API에서 provider/model 지정 방식 반영 |
| [OKK-SPEC-004](../20-spec/spec-004-pty-worker-runtime.md) | PTY Worker 실행 계약 | update | `spec-004-pty-worker-runtime.md` | Claude PTY worker와 provider runner 경계 재정의 |
| [OKK-SPEC-009](../20-spec/spec-009-claude-codex-runner-adapter.md) | Claude/Codex Runner Adapter 계약 | create | `spec-009-claude-codex-runner-adapter.md` | provider별 runner adapter 공통 계약 |
| [OKK-SPEC-010](../20-spec/spec-010-codex-headless-runner.md) | Codex Headless Runner 실행 계약 | create | `spec-010-codex-headless-runner.md` | Codex `exec --json` 실행과 resume/event mapping 계약 |

---
type: baseline
id: OKK-BL-001
title: "Codex headless runner 확장 아이디어"
status: accepted
product: open-kknaks
created_at: 2026-05-29
updated_at: 2026-05-29
tags:
  - product/open-kknaks
  - doc/baseline
  - status/raw
links:
  baselines: []
  decisions:
    - "[[decision-001-provider-based-task-execution|OKK-DEC-001]]"
  specs: []
  works: []
  related: []
---

# OKK-BL-001 Codex headless runner 확장 아이디어

## Raw

`open-kknaks`는 현재 Claude Code CLI를 Redis queue와 PTY worker로 실행한다.

`/Users/kknaks/git/library/claude_code_pty/open_kknaks/docs/legacy/CODEX_ANALYSIS.md`에는 Codex CLI의 headless 실행 방식이 정리되어 있다. 이 문서를 `open-kknaks`의 신규 확장 아이디어 원천으로 본다.

핵심 아이디어:

- Claude 전용 runner에 Codex headless runner/provider를 추가한다.
- Codex 실행 진입점은 `codex exec`다.
- Codex streaming은 `codex exec --json`의 stdout JSONL event stream을 사용한다.
- Codex session은 `thread.started.thread_id`를 저장하고 `codex exec resume <THREAD_ID>`로 이어간다.
- Codex는 PTY가 아니라 stdio 기반 실행을 우선 검토한다.
- `codex exec review`를 코드 리뷰 자동화 작업 타입으로 활용할 수 있다.

## Context

Codex와 Claude Code는 queue/broker/task 개념은 공유할 수 있지만 실행 계약은 다르다.

| 항목 | Claude Code runner | Codex runner 후보 |
|---|---|---|
| Headless entrypoint | `claude -p` | `codex exec` |
| Streaming output | `--output-format stream-json` | `--json` |
| Session id | Claude session id | Codex thread id |
| Resume | `--resume <id>` | `codex exec resume <id>` |
| Process model | PTY | stdio 우선 |
| Auth | Claude Code auth | `CODEX_API_KEY` 또는 `~/.codex/auth.json` |
| Working directory | worker config 중심 | `-C <DIR>` |

## Why It Matters

`open-kknaks`가 Claude Code 전용 queue에서 provider 기반 agent queue로 확장될 수 있다.

사용자는 task를 queue에 넣는 시점에 `claude` 또는 `codex` provider와 model을 선택할 수 있어야 한다. Worker는 provider/model 정보를 보고 실행 adapter를 선택하며, queue와 task lifecycle은 특정 headless CLI 계약에 묶이지 않아야 한다.

Codex는 JSONL event type이 풍부하고 thread id가 명시적으로 노출되므로, session resume, review automation, file-change tracking에 강점이 있다.

## Possible Direction

1. `open-kknaks`는 `claude`/`codex` provider와 model 기반 task 실행 모델로 확장한다.
2. Codex runner는 Claude PTY executor와 분리된 adapter로 설계한다.
3. Worker는 provider registry를 통해 task에 맞는 runner를 선택한다.
4. provider별 원본 event는 보존 가능하게 하되, 외부 stream 계약은 공통 event로 정규화한다.
5. `codex exec review`는 provider 구조가 잡힌 뒤 별도 work type으로 검토한다.

## Open Questions

- `Task` 모델의 provider/model/options 필드명을 spec에서 확정해야 한다.
- Codex 실행 기본 sandbox mode는 무엇으로 둘 것인가?

---
type: release
id: OKK-REL-002
title: "open-kknaks 2.0.2"
status: released
product: open-kknaks
version: "2.0.2"
released_at: 2026-06-01
summary: "Claude/Codex provider 기반 headless agent task queue release"
details:
  - "AgentClient provider/model/options/provider_options 계약 도입"
  - "Codex headless runner와 Docker examples E2E 경로 추가"
  - "PyPI 2.0.2 배포 및 Claude/Codex 배포판 E2E 검증 완료"
created_at: 2026-06-01
updated_at: 2026-06-01
tags:
  - product/open-kknaks
  - doc/release
  - status/released
links:
  baselines:
    - "[[OKK-BL-001-codex-headless-runner]]"
  decisions:
    - "[[decision-001-provider-based-task-execution]]"
  specs:
    - "[[spec-009-claude-codex-runner-adapter]]"
    - "[[spec-010-codex-headless-runner]]"
  works:
    - "[[work-001-provider-task-model-client-broker]]"
    - "[[work-002-provider-worker-and-claude-adapter]]"
    - "[[work-003-codex-headless-runner]]"
    - "[[work-004-batch-cli-mcp-provider-surface]]"
    - "[[work-005-demo-e2e-provider-surface]]"
  releases: []
  related: []
---

# OKK-REL-002 open-kknaks 2.0.2

## 요약

open-kknaks 2.0.2는 Claude 전용 PTY task queue를 Claude/Codex provider 기반 headless agent task queue로 확장한 release다.

라이브러리 사용자는 `AgentClient`에서 `provider`, `model`, 공통 `options`, provider별 `provider_options`를 지정해 Claude 또는 Codex 실행을 선택할 수 있다.

Docker examples는 PyPI 배포판 `open-kknaks==2.0.2`를 설치해 Claude/Codex worker 경유 E2E를 검증하는 경로를 제공한다.

## 상세 수정 사항

| Area | Change | Notes |
|---|---|---|
| Task model | `provider`, `model`, `options`, `provider_options` 계약 도입 | 기본 provider는 `claude` |
| Client API | `AgentClient` public API 도입 | legacy Claude-specific submit kwargs 제거 |
| Worker | provider adapter 기반 실행 경계 추가 | unknown provider는 실행 전 fail |
| Claude | 기존 Claude PTY 실행을 Claude adapter로 감쌈 | stream-json 계약 유지 |
| Codex | `codex exec --json` 기반 headless runner 추가 | JSONL parser, resume, sandbox, failure handling |
| Batch/CLI/MCP | provider-aware surface로 갱신 | batch item provider fields, worker `--provider`, schema guidance |
| Demo | FastAPI demo UI에 provider/model/options 입력 추가 | `/health`에서 Claude/Codex 상태 표시 |
| Docker examples | Claude/Codex toolchain과 auth mount 경로 정리 | `.claude-tools`, `.codex-tools`, `.codex-home` |
| README | PyPI 사용자 기준 setup/E2E 절차 정리 | Claude setup-token, Codex auth/config 주의사항 포함 |

## Breaking Changes

- root public export에서 legacy `ClaudeClient` 대신 `AgentClient` 사용을 기준으로 한다.
- public submit surface는 Claude 전용 kwargs 대신 `options`와 `provider_options`를 사용한다.
- Batch API는 provider task item 계약을 기준으로 동작한다.

## Migration Notes

- 기존 `ClaudeClient` 사용 코드는 `AgentClient`로 교체한다.
- Claude 전용 실행 옵션은 `provider_options`로 옮긴다.
- timeout, cwd, resume 같은 공통 실행 옵션은 `options`로 옮긴다.
- Codex provider는 `provider="codex"`와 필요한 `provider_options`를 지정한다.

## 검증

| Check | Result | Evidence |
|---|---|---|
| Release workflow | pass | GitHub Actions PyPI Release `v2.0.2` success |
| Unit/integration tests | pass | 232 tests passed in release workflow |
| Build | pass | `open_kknaks-2.0.2.tar.gz`, `open_kknaks-2.0.2-py3-none-any.whl` |
| PyPI publish | pass | PyPI latest version `2.0.2` 확인 |
| GitHub Release | pass | `https://github.com/kknaks/open_kknaks/releases/tag/v2.0.2` |
| Docker examples version | pass | app/worker container `open-kknaks==2.0.2` 확인 |
| Codex E2E | pass | result `codex pypi ok`, `exit_code=0` |
| Claude E2E | pass | result `claude pypi ok`, `exit_code=0` |

## 배포 정보

| Item | Value |
|---|---|
| Version | 2.0.2 |
| Released At | 2026-06-01 |
| Artifact | PyPI `open-kknaks==2.0.2` |
| Git Tag | `v2.0.2` |
| GitHub Release | `https://github.com/kknaks/open_kknaks/releases/tag/v2.0.2` |
| Deployment Target | PyPI, GitHub Release, examples Docker |

## Known Issues

- GitHub Actions에서 Node.js 20 action deprecation warning이 표시된다. 현재 release 동작에는 영향이 없다.

## Rollback

문제가 생기면 소비 프로젝트에서 `open-kknaks==2.0.1` 또는 검증된 이전 버전으로 pinning한다.

Docker examples에서는 `examples/Dockerfile.app`와 `examples/Dockerfile.worker`의 package version을 이전 버전으로 되돌린 뒤 image를 rebuild한다.

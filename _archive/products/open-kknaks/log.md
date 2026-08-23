# Product Log

| Date | Entry | Links |
|---|---|---|
| 2026-07-27 | OKK-SPEC-011 §4 Transport 개정 — bridge 실행 위치를 *별도 장기 실행 프로세스* → **kknaks_profile back 프로세스 내 백그라운드 태스크**로 변경. 종전 문장은 근거 없이 단정돼 있었고 실측상 분리가 사는 것이 없었다(포트 노출 0·같은 Dockerfile.back 이미지·slack-bolt 이미 back 의존성·AI 실행은 worker·`depends_on: back`). 분리 비용은 실재(`sys.path` 해킹·이름 충돌·env 이중관리로 `DATABASE_URL` 부재·repo 쓰기 마운트 2곳·**git push 소유권 분산**). §4 나머지 계약(진입점·인가·멱등성·스레드 세션)은 무변경. 근거 KDEV-DEC-013 / 실행 KDEV-WORK-012. | `20-spec/spec-011-slack-knowledge-capture.md` |
| 2026-07-02 | WORK-006 paper PDF·source security·reference reload fixture와 feature-flagged Slack bridge 배선 완료 — backend 303 passed | `30-work/work-006-slack-knowledge-capture.md` |
| 2026-07-02 | WORK-006 Socket Mode thread/session, AgentClient resume, source extractor, compose 배선 구현 — backend 298 passed | `30-work/work-006-slack-knowledge-capture.md` |
| 2026-07-02 | WORK-006 Phase 2 capture skill·schema validator·Markdown renderer·atomic writer 1차 구현 | `30-work/work-006-slack-knowledge-capture.md` |
| 2026-07-02 | WORK-006 Slack thread 기반 inbox/reference 지식 수집 구현 시작 | `30-work/work-006-slack-knowledge-capture.md` |
| 2026-07-02 | SPEC-011을 app mention + Socket Mode + Slack thread별 session·단일 노트 갱신 계약으로 보정 | `20-spec/spec-011-slack-knowledge-capture.md` |
| 2026-07-02 | Slack 텍스트·URL을 inbox/reference로 생성하는 지식 수집 계약 추가 | `20-spec/spec-011-slack-knowledge-capture.md` |
| 2026-07-02 | Slack 지식 수집 baseline을 accepted로 전환하고 SPEC-011에 연결 | `00-baseline/OKK-BL-002-slack-idea-knowledge-graph.md` |
| 2026-06-01 | `OKK-REL-002` open-kknaks 2.0.2 release note 작성 | `60-release/release-002-open-kknaks-2-0-2.md` |
| 2026-06-01 | open-kknaks 2.0.2 PyPI release 완료 및 배포판 examples Docker에서 Claude/Codex E2E 검증 완료 | `30-work/work-005-demo-e2e-provider-surface.md` |
| 2026-05-31 | 코드 레포에서 WORK-005 Demo와 E2E provider 실행 경로 갱신 완료 | `30-work/work-005-demo-e2e-provider-surface.md` |
| 2026-05-31 | WORK-005 Demo와 E2E provider 실행 경로 갱신 작업 시작 | `30-work/work-005-demo-e2e-provider-surface.md` |
| 2026-05-31 | 코드 레포에서 WORK-004 Batch, CLI, MCP provider surface 갱신 완료 | `30-work/work-004-batch-cli-mcp-provider-surface.md` |
| 2026-05-31 | 코드 레포에서 WORK-003 Codex headless runner 구현 완료 | `30-work/work-003-codex-headless-runner.md` |
| 2026-05-31 | 코드 레포에서 WORK-001 Task legacy Claude fields 제거와 options 기반 timeout/resume 전환 완료 | `30-work/work-001-provider-task-model-client-broker.md` |
| 2026-05-31 | 코드 레포에서 WORK-001 ClaudeClient alias와 legacy client 참조 제거 | `30-work/work-001-provider-task-model-client-broker.md` |
| 2026-05-29 | 코드 레포에서 WORK-002 provider worker와 Claude adapter 작업 완료 | `30-work/work-002-provider-worker-and-claude-adapter.md` |
| 2026-05-29 | 코드 레포에서 WORK-002 remaining JSONL stream publish와 non-JSON debug context 보존 구현 | `30-work/work-002-provider-worker-and-claude-adapter.md` |
| 2026-05-29 | 코드 레포에서 WORK-002 provider adapter 경계, unknown provider fail, pending cancel skip 1차 구현 | `30-work/work-002-provider-worker-and-claude-adapter.md` |
| 2026-05-29 | 코드 레포에서 WORK-001 provider constants, Task provider fields, AgentClient, broker round-trip 1차 구현 | `30-work/work-001-provider-task-model-client-broker.md` |
| 2026-05-29 | provider 기반 실행 모델 구현을 위한 work 4개 작성 | `30-work/README.md`, `30-work/work-001-provider-task-model-client-broker.md`, `30-work/work-002-provider-worker-and-claude-adapter.md`, `30-work/work-003-codex-headless-runner.md`, `30-work/work-004-batch-cli-mcp-provider-surface.md` |
| 2026-05-29 | legacy 코드 검증 결과를 반영해 batch, runner, Codex, MCP, middleware spec 보정 | `20-spec/spec-004-pty-worker-runtime.md`, `20-spec/spec-005-batch-execution.md`, `20-spec/spec-007-mcp-schema-server.md`, `20-spec/spec-008-middleware-and-operational-controls.md`, `20-spec/spec-009-claude-codex-runner-adapter.md`, `20-spec/spec-010-codex-headless-runner.md` |
| 2026-05-29 | CLI 표면 계약 spec을 provider-aware worker와 AgentClient 기준으로 업데이트 | `20-spec/spec-006-cli-surface.md` |
| 2026-05-29 | Batch 실행 계약 spec을 provider task item과 parallel-only 기준으로 업데이트 | `20-spec/spec-005-batch-execution.md` |
| 2026-05-29 | Redis Broker 큐 계약 spec을 provider task round-trip 기준으로 업데이트 | `20-spec/spec-002-redis-broker-queue-contract.md` |
| 2026-05-29 | provider 기반 실행 모델에 맞춰 task/client/worker 기존 spec을 draft로 업데이트 | `20-spec/spec-001-task-model-and-lifecycle.md`, `20-spec/spec-003-python-client-and-streaming-api.md`, `20-spec/spec-004-pty-worker-runtime.md` |
| 2026-05-29 | Codex Headless Runner 실행 계약 spec 추가 | `20-spec/spec-010-codex-headless-runner.md` |
| 2026-05-29 | Claude/Codex Runner Adapter 계약 spec 추가 | `20-spec/spec-009-claude-codex-runner-adapter.md` |
| 2026-05-29 | Claude/Codex provider와 model 기반 task 실행 모델을 decision으로 채택 | `10-decision/decision-001-provider-based-task-execution.md` |
| 2026-05-29 | PyPI package 배포 절차를 architecture deploy 문서로 추가 | `40-architecture/deploy/back/README.md` |
| 2026-05-29 | Codex headless runner 확장 아이디어를 baseline에 추가 | `00-baseline/OKK-BL-001-codex-headless-runner.md` |
| 2026-05-29 | legacy 코드 기준 open-kknaks spec 1차 작성 | `20-spec/README.md` |

# [backend] 실험 앱 CLI provider — Claude Code CLI · Codex CLI · 질문별 선택 · 일괄 실행 · Opus 자동 채점 (사용자 10-30)

(워크트리 `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` · 로컬 커밋만 · push 금지)
**지금 하고 있는 case3 시술 슬롯 수정을 먼저 끝내고** 이어서 이 작업.

## 근거
- 조사 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/cli-research.md`(§1 명령 꼴 · §2 측정 · §5 격리 · §6 구현 추천 · §7 막힘 B-1~B-7) — 그대로 따름
- 참고 설계(읽기만) `/Users/kknaks/git/toy_pr2/Strong_hajin/backend/src/ax_workspace/` platform/claude_cli.py · codex_cli.py · cli_process.py · modules/ax_execution/ai.py
- **실험은 CLI · 배포는 SDK**(사용자) — SDK provider 는 지우지 않고 셋 중 하나로

## 사용자 결정(10-30)
- provider = `sdk` · `claude-cli` · `codex-cli` — **질문마다 화면에서 선택**(세 케이스 모두 그 provider · Jev 는 그대로 TypeSafe API) · 기록 · 기록 표 · 열 머리에 provider · 모델 · effort
- **Claude CLI = Sonnet(`claude-sonnet-5-5`) · effort medium** · **Codex CLI = `gpt-5.6-terra` · effort medium** (둘 다 중간)
- **채점 = Opus(`claude-opus-5-5`) 자동**(Claude CLI) — CLI provider 판에서는 ① 이름 뽑기 · ② 채점 자동 켬 · SDK 판은 지금처럼 버튼(기본 끔) · 채점 원장 도구 = 로컬 stdio MCP(D-4 · SPEC W-3)
- 그 외 추천대로: 도구 루프 상한 = 없음 + 타임아웃 · `--max-budget-usd` + 도구 호출 수 기록(D-3) · ttft_kind(Claude 글자 · Codex 메시지) 구분 · 격리(§5 — 플래그 + 임시 cwd · Codex 전용 CODEX_HOME · 내장 도구 끔 · MCP 하나)
- **`ANTHROPIC_API_KEY` 는 사용자가 .env 에서 뺌**(sdk provider 는 그동안 「키 없음」) — 그래도 B-1 대로 CLI 자식 env 에서 그 키 · `CODEX_API_KEY` · `OPENAI_API_KEY` 를 **반드시 지우고**, 실행 앞에 인증 방식이 구독(OAuth · ChatGPT)인지 확인 · 아니면 그 열 오류(조용히 API 과금 금지)
- **일괄 실행(배치) 기능은 만들되 실행은 안 함** — 질문 리스트(`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-30-hub-evals/questions.md` 26) × provider 선택 · 순차 · 간격 · 재시도 · 이어 가기 · 진행 기록 · 한도 신호(`rate_limit_event`) 면 멈춤. **간격 · 재시도 · 한도 대응 값은 설정으로 두고 기본값은 비움 — 사용자가 구현 뒤 정함**(사용자 「한도는 구현부터 하고 정할게 · 질문도 구현부터」)

## 끝
- 모의 시험(실물 JSONL 꼴은 조사 §2 · 참고 설계 ingest 꼴로 픽스처) · ruff · 18210 재시작
- **실물 CLI 호출은 각 provider 1회만(짧은 질문 1개 · case3 만도 됨)** — §7 U-1~U-4(격리 · system/init · 도구 목록 · JSONL 꼴) 확인용 · 그 결과를 보고
- 결과 보고에 「SPEC-006 과 다른 점」 목록(코디가 SPEC 반영)
## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_56c4278e-4761-44d7-8d67-87ca697be965 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "backend 완료: 실험 앱 CLI provider" --body "claude-cli · codex-cli 실물 1회 결과 · 인증 = 구독 확인 · 시험 N passed · 커밋"
orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb --text "[worker_done] backend 완료 — 실험 앱 CLI provider. 상세는 인박스." --enter
```

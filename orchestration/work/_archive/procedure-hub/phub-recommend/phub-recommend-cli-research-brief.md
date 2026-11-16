# [researcher] hub-evals 를 CLI(Codex CLI · Claude Code CLI)로 돌릴 수 있나 — 조사 (read-only · 유료 호출 금지)

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 산출 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/cli-research.md` 하나.

## 왜(사용자 10-30)
hub-evals 실험(`SPEC-006.md` · 앱 `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals`)을 Anthropic API SDK 로 돌렸더니 실물 4질문에 $10 소진(질문당 $2+). 사용자: 「**실험은 CLI 로, 나중 배포는 SDK 로** · 비용이 너무 커 · **codex · claude 로 각각** 실험 · 실험 결과에 **코덱스는 terra, 클로드는 소넷** · **질문 리스트 전체**(`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/reference/2026-10-30-hub-evals/questions.md` 26) 돌려 볼 것 · CLI 로 갈 수 있는지 조사」.
사용자가 준 참고 설계(다른 레포에서 이미 쓰는 구조 — 요청 1건마다 headless 서브프로세스 · provider 설정 하나로 codex ↔ claude 전환 · 호출부는 모름 · MCP 서버 하나만 · 내장 도구 끔 · 사용자 설정 격리 · JSON schema 출력 · stdout JSONL 실시간 이벤트 · 실패 정규화): 실물 코드 `/Users/kknaks/git/toy_pr2/Strong_hajin/backend/src/ax_workspace/` 의 `modules/ax_execution/ai.py` · `bootstrap/settings.py` · `bootstrap/application.py` · `platform/codex_cli.py`(`_arguments` · `prepare_isolated_codex_home` · `_mcp_overrides`) · `platform/claude_cli.py`(`_isolation_arguments`) — **읽기만**.
설치 확인: `codex` · `claude` 둘 다 `/Users/kknaks/.nvm/versions/node/v20.20.0/bin/` 에 있음.

## 조사할 것(공식 문서 · 실제 `--help` · 로컬 버전 · 무료 확인만)
1. **우리 실험에 필요한 것을 CLI 가 다 되나** — 케이스별:
   - case1 · case2: 로컬 **Streamable HTTP MCP**(`http://127.0.0.1:18005/procedure-hub/raw-mcp/mcp` · `/gold-mcp/mcp`)를 붙여 도구 루프. Claude CLI `--mcp-config`(type http) · Codex CLI MCP 설정(http 지원 여부 · `-c` override 꼴)
   - case3: 도구 없이 1회 답(허브 결과를 프롬프트에 넣음)
   - ① 이름 뽑기 · ② 채점: JSON schema 출력(Claude `--json-schema` · Codex `--output-schema`) · 채점은 로컬 원장 도구 3(지금 앱 안 함수) → CLI 에선 MCP 로 줘야 하나
   - Jev 는 그대로 API(TypeSafe · 거의 공짜)
2. **측정이 되나**: stdout JSONL(Claude `stream-json` · Codex `--json`)에서 첫 텍스트 시각(ttft) · 도구 호출 시작/끝 · 왕복 수 · **토큰 · 비용 칸**이 나오나(구독이면 비용 대신 무엇) · **CLI 기동 오버헤드**(프로세스 시작 · 인증 · MCP 연결)를 단계로 따로 잴 수 있나 — 케이스 간 비교가 공정하려면
3. **모델**: Codex 의 「terra」가 무엇인지(모델 id · `codex -m` 값 · 로컬 `codex` 에서 고를 수 있나) · Claude CLI 에서 Sonnet 고르는 법(`--model` 값) · thinking/effort 를 세 케이스 같게 할 수 있나
4. **비용 · 한도**: 두 CLI 가 무엇으로 과금되나(구독 사용량 · API 키 중 어느 쪽 · 로컬이 지금 어느 쪽으로 로그인) · 질문 26 × 케이스 × (답 + 채점) 를 돌릴 때 구독 한도에 걸릴 위험 · 정책상 문제(개인 로컬 실험)
5. **격리**: 참고 설계의 격리(Codex 전용 CODEX_HOME · Claude 플래그 + 임시 cwd · 내장 도구 끔 · 설정 · CLAUDE.md · skills 차단)가 실험 공정성에 충분한가 · 사람 세션과 섞임
6. **실험 앱에 넣는 방법 추천**: SPEC-006 구조(case1 · 2 · 3 · 측정 · 기록 · 채점)를 그대로 두고 「LLM 호출 층」만 provider(sdk · claude-cli · codex-cli)로 바꾸는 꼴 · 참고 설계에서 가져올 것 · 버릴 것 · 화면 · 기록에 provider · 모델 표시 · 질문 리스트 전체 일괄 실행(배치) 기능
7. 막히는 것 · 사용자가 할 일 표
- **유료 호출 · 실제 질문 실행 금지**(`--help` · `--version` · 문서 · 설정 파일 읽기만 · 로그인 상태 확인은 출력에 계정 정보 안 남기게) · 키 · 실명 기록 금지

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_cb9563f9-3138-4945-b09d-9ddbeac86612 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "researcher 완료: CLI 실험 가능성 조사" --body "claude-cli 가능 N · codex-cli 가능 N · terra = ? · 막히는 것 N"
orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb --text "[worker_done] researcher 완료 — CLI 실험 가능성 조사. 상세는 인박스." --enter
```

## 추가(사용자 10-30)
- **질문마다 옵션으로 Claude / Codex 고르기** — 화면 질문 입력 옆 선택(claude-cli Sonnet · codex-cli terra · (sdk)) · 고른 provider 로 세 케이스 모두 돌림 · 기록 · 기록 표에 provider · 모델 표시 · 일괄 실행에도 provider 선택. §6 추천에 이 꼴로 넣을 것
- 전체 실험(26 × 두 provider)은 사용자가 나중에 직접 — 지금은 가능성 · 구현 계획까지
- **밤새 일괄 실행(코디가 돌림)**: 질문 26 × {Claude CLI Sonnet 1번 · Codex CLI terra 1번} · **채점 = Opus 자동**(① 이름 뽑기 · ② 채점 — Claude CLI 로 Opus) · 구독 기반 CLI 라 비용 부담 없음(사용자). 조사에 넣을 것: Opus 를 Claude CLI 로 부르는 꼴 · 일괄 실행 꼴(순차 · 질문 간 간격 · 실패 재시도 정책 · 중간에 끊겨도 이어서 · 진행 기록) · **구독 사용량 한도**(5시간 · 주간 한도에 걸리면 어떻게 멈추고 이어 가나) · 예상 소요 시간

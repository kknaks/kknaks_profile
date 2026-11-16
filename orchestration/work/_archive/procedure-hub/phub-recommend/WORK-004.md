---
type: work
id: WORK-004
title: "hub-evals 실험 앱 구현 — clinic_chat 뼈대 · 세 케이스 · 측정 · 기록 · 품질 두 층 · 화면 · 로컬 E2E"
status: todo
product: procedure-hub
feature: phub-recommend
work_type: new
owner: "backend 워커(+ frontend 워커 Phase 6)"
roles:
  pm: "코디네이터"
  design: ""
  fe: "frontend 워커"
  be: "backend 워커"
  qa: "reviewer_code 워커 · 코디(E2E) · 사용자(실물 실험)"
  ops: ""
progress: 0
created_at: 2026-10-30
updated_at: 2026-10-30
tags:
  - product/procedure-hub
  - feature/phub-recommend
  - doc/work
  - status/todo
links:
  spec: "orchestration/work/phub-recommend/SPEC-006.md"
  depends_on: "orchestration/work/phub-recommend/WORK-003.md(허브 골드 · 원장 MCP)"
---

# hub-evals 실험 앱 구현

> 검수 반영 2026-10-30(F-1 · W-1~W-7) — `review-spec006-report.md` · R-1~R-10 사용자 승인(10-30) · U-1 · U-2 사용자 완료 · 레포 세팅 사실(10-30)

SPEC-006 0.2.0 을 구현한다. 계약은 SPEC-006(앱)과 SPEC-005(허브 도구 스키마)가 갖고, 이 문서는 순서 · 파일 · 완료 조건 · 검증만 갖는다. 다르면 SPEC 을 따른다.

**비목표**: 허브 수정(SPEC-005 밖으로 손대지 않음) · 배포 · 여러 턴 · 얼굴 지도 · 병원 상품.

## Meta

- 레포: GitHub `kknaks/clinic_chat`(공개) · main `240c321`(`README.md` · `.gitignore` · `.env.example` 있음) · canonical `/Users/kknaks/git/clinic_chat` · **작업 워크트리 `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals`(브랜치 `kknaksss/hub-evals`)** — 여기서만 작업한다(SPEC-006 §2-3)
- **push 는 코디 승인 뒤**(공개 레포 — 데이터 · 키 · 환자 정보 검사 §Done 통과 확인 후). 그 전엔 로컬 커밋만
- 허브: `127.0.0.1:18005`(SPEC-005). **허브 골드는 아직 구현 중** — Phase 2~5 는 SPEC-005 도구 스키마로 만든 **모의 허브 MCP**로 시험하고, 실물 허브 대조는 WORK-003 완료 뒤 Phase 7
- 키: `ANTHROPIC_API_KEY` · `TYPESAFE_API_KEY` 는 사용자가 받아(U-1 · U-2 완료 10-30) 워크트리 `.env` 에 직접 넣는다. 워커는 `.env` 를 만들거나 · 덮거나 · 키를 묻거나 · 출력하지 않는다. `.env` 에 키가 없으면 모의로 뼈대 시험 · 실물 호출은 키가 들어온 뒤
- `.env` 는 워크트리에만 있는 ignored 파일 — 워크트리를 지우거나 옮길 때 먼저 `git status --ignored` 로 확인
- 사용자 포트 · 프로세스는 건드리지 않는다(3700 · 3800 · 8700 · 8800 · 54329 · `procedure-*`) · 실험 서버 18210
- 실명 · 키 · 원장 데이터 · 실행 기록을 레포에 넣지 않는다

## Work Summary

| Field | Value |
|---|---|
| Goal | 사용자가 로컬 화면에서 질문하면 세 케이스가 동시에 돌고 속도 · 답 · 흔적 · ① · ② · 사람 확인 · 기록이 나온다 |
| 완료 판정 | §Done Criteria — 두 단계: 「모의 완료」(모의 판 전부) → 「완료」(실물 E2E 1질문 뒤). **실물 없이 「완료」 금지** |

## Execution

- Phase 마다 **그 Phase 시험만**(`uv run pytest tests/<그 Phase> -q`). 전체 시험 · ruff 는 Phase 7 끝에 한 번
- Phase 끝마다 코디에게 heartbeat(phase) · 막히면 escalation · SPEC 과 다르게 해야 하면 `ask`

### Phase 1 — 레포 뼈대

- 워크트리 `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` 에서(clone 하지 않음) · `pyproject.toml`(anthropic[mcp] · mcp · typesafe-sdk · fastapi · uvicorn · sse 지원 · pydantic-settings · pytest · ruff — 버전 고정) · SPEC-006 §2-3 폴더 · `.gitignore` 는 main 것에 `.cache/` 한 줄만 더함 · `.env.example`(main 의 키 두 줄 + §2-4 나머지 이름 · 키 빈칸 · 사용자 경로 칸 빈칸) · `config.py`(pydantic-settings 가 루트 `.env` 를 읽음 — SPEC-006 §2-1 · `--env-file` 안 씀) · `README.md`(main 것에 §8 절차 · 데이터 · 키 규칙을 더함)
- `prompts/*.md` 초안(공통부 · 케이스별 · judge · extract) · 판 = sha 앞 12자
- MCP Streamable HTTP 클라이언트 import 경로를 고정한 MCP SDK 버전 문서로 확인해 `clients/hub_mcp.py` 머리 주석에 적음(jev-research §4)
- 시험 `tests/test_repo_rules.py`: `.env` · `*.jsonl` · 원장 파일 이름 21 · `semantic.json` 이 git 추적 목록에 없음 · 소스에 키 꼴 문자열(`sk-ant-` 등) 없음 · `.env.example` 의 `ANTHROPIC_API_KEY` · `TYPESAFE_API_KEY` 값 빈칸 · `.env.example` 에 사용자 홈 경로(`/Users/`) 없음

완료 조건: 시험 통과 · `.env` 를 둔 채 `uv run python -m clinic_chat.server`(SPEC-006 §8 명령 그대로 · `--env-file` 없이)가 빈 화면을 18210 에 냄 · 기동 확인 줄에 env 가 읽혔는지(키는 「있음 · 없음」만 · 값 출력 금지) · 워크트리 브랜치에 로컬 첫 커밋

### Phase 2 — case1 · case2(도구 루프)

- `tests/fake_hub/` 모의 허브 MCP 서버(Streamable HTTP · stateless · JSON) — 원장 3 · 골드 9 도구를 SPEC-005 §5-2~§5-10 · §5-12 입출력 스키마대로(값은 작은 고정 fixture · 가상 의학 문장 대신 「fixture」 표시 문자열)
- `loop.py`: Sonnet 스트림 · `tool_use` → MCP 호출(병렬은 결과를 한 메시지로) · 상한 `CASE_TOOL_LOOP_MAX` · 닿으면 `tool_choice none` 마지막 1번 · `between_tools` · effort high · 폴백 없음 · refusal 기록
- `case1.py`(원장 MCP) · `case2.py`(골드 MCP · `node_ids` 뽑기)
- 시험(모의 Anthropic 스트림 + 모의 허브): 도구 0 · 1 · 여러 번 · 병렬 · 상한 닿음 · refusal · MCP 오류 → `is_error` 결과 · thinking 칸이 `{"type": "between_tools"}` 하나뿐 · tool_choice 강제값 안 씀

완료 조건: 시험 통과 · (키 있으면) 모의 허브로 실물 Sonnet 1회씩 — 출력 원문

### Phase 3 — case3(허브 사전 → Jev → 골드 경로 → Sonnet)

- 시작 때 T9 vocab 캐시 · ① T1 resolve · ② Jev 한 요청(의도 Choice 12 · 슬롯 Choice · 255 넘는 슬롯은 ① 후보로 줄임 · 「해당 없음」 + 짝 Noul · 여러 고민 Noul · 순서 seed 섞기) · confidence · p_max · 1·2위 비 · `low_confidence`(< 0.3) · ③ 의도 → 도구 경로 표(SPEC-006 §3-4) · 필수 슬롯 없으면 되묻기 · ④ Sonnet 1회
- 시험(모의 Jev + 모의 허브): 의도마다 경로 1개 · 255 넘는 슬롯이 줄어 255 이하 · 선택지 순서 seed 재현 · 낮은 신뢰 표시 · I-12 허브 호출 0 · Jev 401 · 422 · 시간 초과 → 그 열만 오류
- Jev 요청 본문 꼴은 `typesafe-sdk` 문서 그대로(Choice `criteria` · `instructions`) — 실물 키 있을 때 1회 확인

완료 조건: 시험 통과 · (TypeSafe 키 있으면) 실물 Jev 1회 — 응답 `model` · `usage` · confidence 원문

### Phase 4 — 측정 · 기록

- `timing.py`: `t0` · `stages[]` · `ttft_ms`(첫 `text_delta` · thinking 제외) · `ttft_answer_ms` · `total_ms` · 왕복 · 단계별 토큰(Anthropic usage · Jev usage)
- `runs.py`: `runs.jsonl` 한 줄(SPEC-006 §4-2 · versions · settings · judge_order · seed) · `human_checks.jsonl` · 골드 `build_hash` · 원장 `raw_manifest_sha16` 은 도구 응답 머리에서 · `app_commit`
- 세 케이스 `gather` 동시 시작 · 한 열 오류여도 나머지 계속
- 시험: 모의 지연(가짜 시계)으로 stages · ttft 값 정확 · 세 케이스 같은 `t0` · 기록 줄이 꼴 · 키 · env 값이 기록에 없음

완료 조건: 시험 통과 · 모의 실행 기록 한 줄 예시(레포 밖 `RUNS_DIR`)

### Phase 5 — 품질 ① · ②

- ① `word_check.py`: 이름 뽑기(R-4 · 구조화 출력 · 사전 · 원장 안 줌) → 정규화(`normalize.py` = `semantic.json` `dictionary.resolve_rules.normalize` 그대로 — NFKC · 악센트 접기 · fold · 공백 · 괄호 · 전부 소문자 · 답 · 원장 · 사전에 같은 함수 · SPEC-006 §5-1) → `RAW_DIR` 21 파일 문자열 부분 일치 → 시맨틱 사전 `expr · variants` → `{name, norm, found, where[], via}` · 2자 미만 제외
- ② `raw_tools.py`: 채점용 원장 도구 3(`raw_list` · `raw_get` · `raw_search`)을 앱 안에 로컬 구현 — SPEC-005 §5-12 R1~R3 과 같은 계약 · `RAW_DIR` 로컬 파일 · 허브 원장 MCP 안 부름(R-10)
- ② `judge.py`: 세 답 seed 섞기 · A/B/C · `raw_tools.py` 원장 도구 3 을 Opus 도구로 · effort medium · 도구 루프 뒤 구조화 출력 · 항목 5 × 답 3 · 실패 근거 `{file, path, quote}` 를 원장 로컬 파일로 확인 → 없으면 `invalid`
- 시험: 정규화 표(**「한글로 시작 + 영문 대문자」 원장 문자열 하나 포함** — 예 「듀얼파장(알렉+다이오드 or 다이오드+Nd:YAG)」 에 답 이름 「Nd:YAG」 가 「있음」 · 「필러(HA/CaHA)」 에 「CaHA」 가 「있음」 · fold 「쳐짐」 → 「처짐」 · 괄호 지움) · 원장에 있는 이름 / 없는 이름 / 사전에만 있는 표기 · 가리기(채점 입력에 case 이름 · 도구 흔적 없음) · 근거 확인(맞는 경로 · 없는 quote → invalid) · seed 재현 · 로컬 원장 도구 3 의 입출력이 SPEC-005 §5-12 계약 꼴 · 채점 경로에서 허브 호출 0

완료 조건: 시험 통과 · (키 있으면) 모의 답 3개로 실물 Opus 채점 1회 원문

### Phase 6 — 화면

- `web/index.html · app.js · style.css`(SPEC-006 §6 와이어 · §4-3 SSE 계약) · 안내 줄(환자 정보 금지 · Jev 전송) · 3열 스트리밍 · 단계 막대(같은 눈금) · 흔적 접기 · ① · ② · 사람 확인 · 같은 질문 다시 ×3 · 기록 목록(누르면 기록에서 다시 그림)
- 시험: SSE 이벤트 → 화면 상태(모의 이벤트 재생) · 키 없는 케이스 「키 없음」 표시

완료 조건: 모의 서버로 브라우저에서 한 질문 끝까지(스크린샷 1장 · 레포 밖에 저장)

### Phase 7 — 로컬 E2E · 전체 검증

1. 모의 판 E2E: 모의 허브 · 모의 Anthropic · 모의 Jev 로 화면에서 질문 1 → 3열 · ① · ② · 기록 · 사람 확인
2. 전체 시험 · ruff 한 번
3. 실물 판(코디가 알림 — WORK-003 허브 골드 완성 · 키는 워크트리 `.env` 에 있음): **이것 없이 「완료」 아님**
   - 허브 실물 대조: 원장 MCP 3 · 골드 MCP 9 도구 목록 · 스키마가 모의와 같음(다르면 SPEC-005 를 따라 모의 · 코드 고침) · 채점용 로컬 원장 도구 3 이 허브 원장 MCP 와 같은 질의에 같은 결과
   - 실물 질문 1개(환자 정보 없음) — 세 열 실제 호출 · 기록 한 줄 · 서버 재시작 뒤 측정
4. 공개 레포 검사(`tests/test_repo_rules.py` + `git ls-files` 원문) → 코디에게 push 승인 요청

## Done Criteria

두 단계다. **실물 E2E 없이 「완료」로 보고하지 않는다** — 외부 서비스(Anthropic · TypeSafe · 허브 MCP) 경로는 실물 호출 1회가 완료 조건이다(검수 W-5).

### 「모의 완료」

- [ ] Phase 1~6 완료 조건 · Phase 7-1 · 7-2 · 7-4(출력 원문을 report 에)
- [ ] 모의 판 E2E PASS · 전체 시험 · ruff 통과
- [ ] 레포에 키 · 원장 · 시맨틱 · 실행 기록 · `.env` 없음(시험 + `git ls-files`)
- [ ] 세 케이스 같은 조건(모델 · `between_tools` · effort · 공통 프롬프트 판 · 같은 `t0`) 시험으로 확인
- [ ] SPEC-006 과 다르게 구현한 곳 0 — 있으면 목록 + `ask` 근거

### 「완료」(「모의 완료」 + 아래)

- [ ] Phase 7-3 실물 E2E 1질문 — 세 열 실제 호출(Anthropic · Jev · 허브 MCP) · 기록 줄 원문 · 허브 스키마 대조표 · 로컬 원장 도구 ↔ 허브 원장 MCP 대조
- [ ] push 는 코디 승인 뒤에만

## Rollback

로컬 레포라 커밋을 되돌린다. push 전이면 원격 영향 없음. 허브는 건드리지 않음.

## Open Issues

- SPEC-006 §7-3 R-1~R-10 — 결정됨(10-30 사용자 승인) · 값은 env · 프롬프트 파일로 조정 가능하게
- SPEC-006 §7-4 U-1 · U-2 완료(키는 사용자가 워크트리 `.env` 에) · U-4 는 실험 중 사용자
- SPEC-006 §7-5 L-1 실험 기록 저장 위치 — 사용자 답 대기 · 답 전까지 `runs/` · `*.jsonl` 커밋 안 함(지금 `.gitignore`)
- 허브 골드 미완 — 실물 대조는 WORK-003 완료 뒤

## Related

- SPEC-006 0.2.0 · SPEC-005(허브 도구 계약) · WORK-003 · `reference/2026-10-30-hub-evals/README.md` · `jev-research.md` · `_RESUME.md` §2 10-30

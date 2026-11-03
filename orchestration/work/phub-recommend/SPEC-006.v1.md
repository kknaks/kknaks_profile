---
type: spec
id: SPEC-006
title: "hub-evals 실험 앱 — 원장 MCP vs 골드 MCP vs 골드 + Jev · 로컬 프론트 질문 → 세 갈래 동시 실행 · 속도 · 품질 두 층 · 기록"
status: draft
product: procedure-hub
feature: phub-recommend
version: 0.2.0
created_at: 2026-10-30
updated_at: 2026-10-30
tags:
  - product/procedure-hub
  - feature/phub-recommend
  - doc/spec
  - status/draft
links:
  decisions:
    - "orchestration/work/phub-recommend/_RESUME.md §2 (10-30 「원장도 MCP 로」 · 「hub-evals 결정」 Q-1~Q-8 · 「최종 목표」 · 「hub-evals 는 골드 완성 뒤」 · DEC-001 D-08 · D-11)"
  sources:
    - "reference/2026-10-30-hub-evals/README.md"
    - "orchestration/work/phub-recommend/jev-research.md"
    - "orchestration/work/phub-recommend/SPEC-005.md §5 · §5-12"
  work:
    - "orchestration/work/phub-recommend/WORK-004.md"
---

# SPEC-006 — hub-evals 실험 앱

> 검수 반영 2026-10-30(F-1 · W-1~W-7) — `review-spec006-report.md` · R-1~R-10 사용자 승인(10-30) · U-1 · U-2 사용자 완료 · 레포 세팅 사실(10-30)

근거는 아래 정본만이다. 결정은 다시 논의하지 않는다. 이 스펙이 고른 값 R-1~R-10 은 10-30 사용자 승인으로 결정됐다(§7-3). 남은 열린 것은 §7-5 에만 둔다.

| 정본 | 이 스펙에서 |
|---|---|
| `reference/2026-10-30-hub-evals/README.md` | 세 케이스 · 속도 칸 · 품질 두 층 · 화면 와이어 · 기록 꼴 · 열린 것 O-1~O-9 |
| `jev-research.md` | Jev = TypeSafe System One(MCP 없음 · Choice 선택지 255 한도 · confidence · Python SDK) · Claude 로컬 MCP = Anthropic SDK + MCP 클라이언트 |
| `_RESUME.md` §2 10-30 | 원장도 MCP · Q-1~Q-8 · 최종 목표 · 레포 공개 · 데이터 · 키 env |
| `SPEC-005.md` | 허브 골드 도구 9(§5) · 원장 도구 3(§5-12) · 포트 · 경로 — **계약**. 허브는 아직 구현 중이라 실물 대조는 허브 완성 뒤 |
| `quality-eval-set.json` | 나중 회귀용 참고만 — 실험 질문은 사용자가 그때그때 입력(README §1) |

## 0. 요약

- 사용자가 로컬 화면에 질문 하나를 넣으면 case1(원장 MCP + Sonnet) · case2(골드 MCP + Sonnet) · case3(허브 사전 → Jev Choice 슬롯 → 골드 도구 → Sonnet 1회)가 **같은 시각에** 돈다
- 열마다: 속도(ttft · total · 단계별 · LLM 왕복 · 토큰) · 답 스트리밍 · 도구 호출 / Jev 슬롯 / 허브 경로 · ① 단어 검사(원장 대조 결정론) · ② Opus 채점(항목별 통과 · 실패 · 근거 인용 · 가리기) · 사람 확인 표시 · 기록 한 줄(jsonl)
- 앱은 공개 레포 `kknaks/clinic_chat` · 로컬 실행. 허브(SPEC-005)는 따로 떠 있는 서버이고 이 앱은 그 MCP · REST 를 부르기만 한다

| 절 | 내용 |
|---|---|
| §1 | 범위 · 경계 |
| §2 | 구성 · 레포 구조 · env |
| §3 | 세 케이스 흐름 · 같은 조건 |
| §4 | 속도 측정 · 기록 꼴 |
| §5 | 품질 두 층 |
| §6 | 화면 |
| §7 | 열린 것 처리표(README O-1~O-9 · Jev Q-1~Q-8 · R-1~R-10 결정 · 사용자 몫 · 남은 열린 것) |
| §8 | 사용자 실행 절차 |

---

## 1. 범위 · 경계

| 안 | 밖 |
|---|---|
| 실험 앱(서버 + 로컬 화면) · 세 케이스 실행 · 측정 · 채점 · 기록 | 허브 자체(SPEC-005 · 별도 서버) |
| 단건 질문(대화 이어가기 없음) | 여러 턴 · 얼굴 지도 패널 · 병원 상품(KOS) · 운영 지연 예산 판정(README §8) |
| 로컬 실행 | 배포 · 외부 공개 서버 · 허브를 밖으로 노출(jev-research §4 — Messages API MCP connector 안 씀) |

- **LLM 키는 env 로만**(D-11 · 10-30 「Claude 는 API 키 별도」). 문서 · 레포 · 기록 · 로그에 키를 쓰지 않는다
- **공개 레포 규칙**(10-30 「레포 kknaks/clinic_chat 공개 · 데이터 · 키는 env」): 레포에 원장 json · 시맨틱 · 실버 · 골드 파일 · 실행 기록(jsonl) · 허브 응답 캐시 · `.env` 를 넣지 않는다. 경로는 env 로 받는다. `.gitignore` 에 `.env` · `runs/` · `*.jsonl` · 캐시 폴더
- **환자 정보 금지**(10-30): 실험 질문에 환자 정보를 넣지 않는다 — 화면 입력칸 위에 안내 한 줄. Jev(TypeSafe · 미국)로 질문 + 노드 이름이 나간다는 사실도 같은 줄에(jev-research B-4)
- 허브 쪽 계약: 골드 MCP `http://127.0.0.1:18005/procedure-hub/gold-mcp/mcp` · 원장 MCP `…/procedure-hub/raw-mcp/mcp` · REST `…/procedure-hub/gold/*`(SPEC-005 §1-3 · §5-1 · §5-12). 도구 입력 · 출력 스키마는 SPEC-005 §5-2~§5-10 · §5-12 그대로 쓴다

## 2. 구성

### 2-1. 실험 서버

| 항목 | 값 | 근거 |
|---|---|---|
| 언어 | Python 3.12 · `uv` | jev-research §5 · 허브와 같은 도구 |
| Claude | 공식 Anthropic Python SDK(`anthropic[mcp]`) — **직접 루프**(Agent SDK · Messages API MCP connector 안 씀) | 10-30 Q-2 |
| 허브 MCP 연결 | 공식 MCP Python SDK `ClientSession` + Streamable HTTP 클라이언트 transport(정확한 import 경로는 고정한 SDK 버전 문서로 확인 — jev-research §4) · 도구 변환은 `anthropic.lib.tools.mcp.async_mcp_tool` 또는 같은 꼴의 직접 변환 | jev-research §4 · claude-api 스킬 `python/claude-api/tool-use.md` 「MCP Tool Conversion Helpers」 |
| Jev | `typesafe-sdk` `AsyncTypeSafeClient` · 모델 `jev-1.14.0` 고정 | 10-30 Q-6 · jev-research §1 |
| 웹 | FastAPI · uvicorn · SSE(서버 → 화면 스트림) · 127.0.0.1 에만 바인딩 | §7-3 R-1(결정됨) |
| 설정 읽기 | `pydantic-settings` — `config.py` 가 레포 루트 `.env` 를 직접 읽는다(`uv run` 은 `.env` 를 저절로 읽지 않으므로 `--env-file` 대신 이 방식 하나) · 환경 변수가 있으면 그것이 앞섬 | 검수 W-4 |
| 동시 실행 | `asyncio` — 세 케이스를 `gather` 로 같은 `t0` 에서 시작 | README §3 |

### 2-2. 프론트(로컬)

- **결정(R-1): 빌드 없는 정적 페이지 하나**(HTML + 바닐라 JS + `EventSource` · 서버가 정적 파일로 냄)
- 이유: 화면 하나(3열 + 기록 목록)뿐이고 로컬 실험용이다 · Node 빌드 체인이 없으면 실행 명령이 서버 하나로 끝난다 · SSE 는 브라우저 기본 `EventSource` 로 충분하다 · 공개 레포에 의존성이 적다
- 나중에 바꿀 경우(React · Vite 등)도 화면 계약(§6 · SSE 이벤트 §4-3)이 같으면 서버는 그대로

### 2-3. 레포 `kknaks/clinic_chat` 구조

10-30 실물(레포 세팅 끝): GitHub 공개 레포 · main `240c321`(「레포 시작」 — `README.md` · `.gitignore` · `.env.example` 만 있음).

| 자리 | 경로 |
|---|---|
| canonical(main) | `/Users/kknaks/git/clinic_chat` |
| 작업 워크트리 | `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` · 브랜치 `kknaksss/hub-evals`(main `240c321` 에서) |

- main 의 `.gitignore` 는 이미 `.env` · `.env.*`(`!.env.example`) · `runs/` · `data/` · `raw/` · `*.jsonl` · Python 캐시를 막는다 — Phase 1 은 `.cache/` 한 줄만 더한다
- main 의 `.env.example` 은 키 두 개(`ANTHROPIC_API_KEY` · `TYPESAFE_API_KEY`) 빈칸뿐 — Phase 1 이 §2-4 나머지 이름을 더한다

```
clinic_chat/
  .env.example            env 이름 · 키 값 빈칸 · 사용자 홈 경로 없음(§2-4)
  .gitignore              (main 에 있음) + .cache/
  pyproject.toml · uv.lock
  README.md               (main 에 있음) + 실행 절차(§8) · 데이터 · 키 규칙
  prompts/                common.md · case1.md · case2.md · case3.md · judge.md · extract.md (판 = 파일 sha 앞 12자)
  clinic_chat/
    config.py             env 읽기(pydantic-settings · 루트 .env)
    clients/anthropic_client.py · jev_client.py · hub_mcp.py(골드 · 원장 ClientSession) · hub_rest.py
    cases/case1.py · case2.py · case3.py · loop.py(case1 · 2 공통 도구 루프)
    timing.py             t0 · stages[] 기록기(perf_counter)
    quality/word_check.py · judge.py · normalize.py(resolve_rules.normalize) · raw_tools.py(채점용 로컬 원장 도구 R1~R3)
    runs.py               jsonl 쓰기 · 읽기 · human_checks
    server.py             FastAPI · SSE · 정적 파일
  web/index.html · app.js · style.css
  tests/                  모의 허브 MCP · 모의 Anthropic 스트림 · 모의 Jev(키 없이 도는 시험)
```

### 2-4. env(`.env` · git 제외 · 예시는 `.env.example`)

`.env.example` 규칙: **키 두 개(`ANTHROPIC_API_KEY` · `TYPESAFE_API_KEY`) 값은 빈칸 · 사용자 홈 경로(`/Users/…`)는 쓰지 않음**(사용자 경로 칸은 빈칸). 그 밖의 예시 값(모델 id · 허브 URL · `./runs` · 포트 · 상한 · 문턱)은 적는다. 키는 사용자가 워크트리 `.env` 에 직접 넣는다(U-1 · U-2 완료 10-30).

| 이름 | 뜻 | 예시 값(.env.example) |
|---|---|---|
| `ANTHROPIC_API_KEY` | Claude API 키(사용자) | 빈칸 |
| `TYPESAFE_API_KEY` | Jev 키(사용자) | 빈칸 |
| `TYPESAFE_DEFAULT_MODEL` | Jev 모델 | `jev-1.14.0` |
| `ANSWER_MODEL` · `JUDGE_MODEL` · `EXTRACT_MODEL` | 답 · 채점 · 이름 뽑기 모델 | `claude-sonnet-5-5` · `claude-opus-5-5` · `claude-opus-5-5`(R-4) |
| `HUB_GOLD_MCP_URL` · `HUB_RAW_MCP_URL` · `HUB_REST_URL` | 허브 주소 | `http://127.0.0.1:18005/procedure-hub/gold-mcp/mcp` · `…/raw-mcp/mcp` · `…/procedure-hub/gold` |
| `RAW_DIR` | ① 단어 검사 · ② 채점 원장 도구(§5-2)가 읽는 원장 21 폴더(레포 밖) | 빈칸(사용자 경로 — `.env` 에서 `…/PROCEDURE-HUB/phub-stg-2026-10-26` 꼴로 채움) |
| `SEMANTIC_JSON` | ① 정규화 규칙 · 표기 차이 확인용 시맨틱 사전(레포 밖) | 빈칸(사용자 경로 — `…/orchestration/work/phub-recommend/semantic.json` 꼴) |
| `RUNS_DIR` | 기록 폴더(레포 밖 또는 ignore 된 `runs/`) | `./runs` |
| `CLINIC_CHAT_PORT` | 실험 서버 포트 | `18210`(사용자 포트 3700 · 3800 · 8700 · 8800 · 54329 · 허브 18005 와 안 겹침) |
| `CASE_TOOL_LOOP_MAX` | case1 · 2 도구 루프 상한 | `12`(R-2) |
| `JEV_CONFIDENCE_MIN` | 낮은 신뢰 표시 문턱 | `0.3`(10-30 Q-5) |

## 3. 세 케이스 흐름

### 3-1. 같은 조건(세 케이스 공통)

| 항목 | 값 | 근거 |
|---|---|---|
| 답 모델 | `claude-sonnet-5-5` · 세 케이스 같음 | README §1 |
| thinking | **끔** = `thinking: {"type": "between_tools"}`(Sonnet 5.5 에서 `disabled` 는 400 — 가장 낮은 설정이 `between_tools` · 다른 칸 같이 보내면 400) | 10-30 Q-3 · claude-api 스킬(Sonnet 5.5 breaking change 1) |
| effort | `output_config.effort = "high"`(Sonnet 5.5 기본값을 명시 · `between_tools` 는 high 이하만 받음) · 세 케이스 같음 | R-3(결정됨) |
| tool_choice | `auto`(Sonnet 5.5 · Opus 5.5 는 강제 `any` · `tool` 이 400) | claude-api 스킬 |
| 폴백 | 쓰지 않음 — 폴백 모델이 답하면 「세 케이스 같은 모델」이 깨진다. `stop_reason == "refusal"` 이면 그 열에 거절로 기록 | README §1 「세 케이스 같은 모델」 |
| 프롬프트 | 공통부(`prompts/common.md` — 답 문장 지시) 같음 + 케이스별 부분(데이터 · 도구 설명만 다름) | README O-2 선택지 → R-5(결정됨) |
| 시작 | 같은 `t0` 에서 동시 시작 | README §3 |
| 스트리밍 | Sonnet 호출은 전부 `messages.stream` | — |
| 단건 | 대화 이어가기 없음 · 매 질문 새 대화 | README §1 |

### 3-2. case1 — 원장 MCP + Sonnet

- 도구 = 원장 MCP 3(`raw_list` · `raw_get` · `raw_search` — SPEC-005 §5-12) 그대로. 골드 · 시맨틱에 기대지 않음(10-30 「원장도 MCP 로」 · Q-1)
- 루프(`loop.py`): Sonnet 스트림 → `tool_use` 면 MCP 호출(병렬 호출은 모아 한 user 메시지로 결과 반환) → 다시 Sonnet → … `end_turn` 까지. 상한 `CASE_TOOL_LOOP_MAX` 번 Sonnet 호출 — 닿으면 `tool_choice: {"type": "none"}`(강제 금지 대상 아님 — none 은 허용)로 마지막 답 호출 1번 · 기록 `loop_capped: true`
- `trace.context` = 도구 호출 목록(README §6 의 「넣은 자료 설명」 자리)

### 3-3. case2 — 골드 MCP + Sonnet

- 도구 = 골드 MCP 9(SPEC-005 §5-1 T1~T9) 그대로 · 같은 `loop.py`
- `trace.tool_calls[]{tool, input, output_bytes, node_ids[], ms}` — `node_ids` = 결과 JSON 안의 정본 id(`{kind}:{키}` 꼴) 전부(README §6)
- 골드 응답의 `claude_contract`(SPEC-005 §5-0 · O-3)는 도구 결과에 들어 있는 그대로 Sonnet 에 간다(이 앱이 따로 덧붙이지 않음)

### 3-4. case3 — 앱 서버: 허브 사전 → Jev → 골드 도구 → Sonnet 1회

```
t0 ─▶ ① hub_resolve: T1 resolve(질문 전체)                      [허브 REST · 결정론]
      ② jev: 의도 Choice + 슬롯 Choice(한 요청에 병렬)           [Jev 1회 · 255 넘는 슬롯만 2단]
      ③ hub_path: 의도별 골드 도구 경로 1번                       [허브 REST]
      ④ claude: Sonnet 1회(③ 결과 + 낮은 신뢰 슬롯 표시)         [스트리밍]
```

| 단계 | 규칙 | 근거 |
|---|---|---|
| 시작 때 1회 | T9 vocab(고민 · 부위 · 목적 · 확인 조건 · 기법 · 계열 · 의도 · 메뉴)을 받아 캐시 · 질문당 단계에서 뺌(기록엔 `hub_list: "cache"`) | 10-30 Q-7 · SPEC-005 §5-10 |
| ① 사전 검색 | T1 resolve(질문 전체) → `candidates` · `menu_candidates` · `unmatched`. **질문마다 늘 부른다** — 시술 · 제품 슬롯(255 넘음)은 ① 후보 없이는 Choice 선택지를 만들 수 없고, 질문이 시술 슬롯을 말하는지는 ① 을 해 봐야 안다(Q-4). 255 이하 슬롯만 쓰는 질문에도 부르므로 그 시간은 `stages[]` 의 `hub_resolve` 로 따로 남겨 `jev` · `hub_path` · `claude` 와 나눠 비교한다(검수 W-7) | SPEC-005 §5-2 · 10-30 Q-4 |
| ② 의도 | Choice 하나 — 선택지 = 의도 12(SPEC-005 §5-1 의도 열 · gold-research 의도 I-01~I-12) · `criteria` 설명 = 의도 이름 · 예시 질문 | D-08 · gold-research §3 |
| ② 슬롯 | 슬롯마다 Choice 하나 — 슬롯 = T9 vocab 종류(고민 · 부위 · 목적 · 확인 조건 · 기법 · 계열 · 메뉴) + 시술 · 제품. **중증도 슬롯은 없다** — 허브 vocab(SPEC-005 §5-10)에 중증도 종류가 없고, 7단계가 중증도를 하위 고민으로 옮겼다(R18 · J12 — 주름 초기 · 경미 → P2-3 잔주름 · 중기 · 중등도 · 심화 · 중증 → P2-2 깊은주름 · `step7-concerns.md`) — D-08 의 「중증도」는 고민 슬롯이 덮는다(검수 W-6). 선택지 = vocab 노드(이름 + 동의어 몇 개를 설명으로 · 한국어만). **선택지가 255 를 넘는 슬롯**(시술 · 제품: 단위 시술 162 + 제품 354 + 계열 27)은 ① 의 후보로 줄인 뒤 Choice(10-30 Q-4) · 「해당 없음」 선택지 + 짝 Noul(「질문이 이 슬롯 값을 말하나」) | 10-30 Q-4 · jev-research §2-3 |
| ② 여러 고민 | Choice 는 하나만 고른다 → R-6(① 후보 고민마다 Noul) | jev-research §2-3 |
| ② 선택지 순서 | 섞고 seed 기록(앞쪽 기울기) | jev-research §2-3 「순서 또는 seed 기록」 → R-7 |
| ② 신뢰도 | 슬롯 · 의도마다 `confidence` · `p_max` · 1·2위 비 기록 · `confidence < 0.3` 이면 `low_confidence` 표시 | 10-30 Q-5 · jev-research §2-2 |
| ③ 경로 | **의도 → 도구 = SPEC-005 §6-1 의도 → 도구 대응 그대로**(① T1 은 이미 부름). 이 스펙에 옮겨 적은 꼴: I-01 → T2 recommend(`concerns` · `site` · `cc` — T1 `candidates` 의 concern · site 만) · I-02 · I-03 · I-04 · I-05 · I-10 → T3 procedure_card(의도별 `sections`) · I-06 → T6 compare · I-07 · I-08 → T4 pair_check(**I-07 자기 쌍 = 같은 id 두 번** — SPEC-005 §5-5) · I-09 → T5 check_conditions(**확인 조건 노드가 안 잡히는 질문(「통증 민감」 꼴)은 T3 `sections=overview,ops`**) · I-11 → T7 combos(`menu_candidates` 는 여기만 · 질문 말이 라벨이면 `menu` · 아니면 `concern`) · I-12 가격 → 허브 도구 없음(연결 층 · 이 실험 밖 — Sonnet 에 「가격 정보 없음」만 줌). SPEC-005 §6-1 이 바뀌면 그쪽을 따른다(검수 W-2) | SPEC-005 §6-1 · §5-1 · §5-5 · gold-research §3 |
| ③ 필수 슬롯 없음 | 그 의도의 필수 슬롯(SPEC-005 도구 필수 입력)이 비면 도구를 부르지 않고 「되묻기 필요」로 Sonnet 에 넘김 | D-08 「신뢰도 낮은 슬롯은 되묻기」 |
| ④ Sonnet | 1회 · 도구 없음 · 입력 = 질문 + ③ 결과 JSON + 슬롯 표(낮은 신뢰 표시 포함) | README §2 |

- 기록 `trace.jev{model, intent{choice, confidence, p_max, ratio}, slots{…}, noul{…}, option_order_seed, usage}` · `trace.hub{resolve, path, tool, input, node_ids[]}`
- Jev 실패(401 · 422 · 429/529 재시도 끝 · 시간 초과): 그 열을 오류로 기록하고 다른 두 열은 계속(jev-research §2-4)

## 4. 속도 측정 · 기록 꼴

### 4-1. 속도 칸

| 칸 | 정의 |
|---|---|
| `t0` | 서버가 질문을 받은 시각(세 케이스 같은 값 · `perf_counter` 기준) |
| `ttft_ms` | `t0` → 그 케이스 Sonnet 스트림의 **첫 `text_delta`** 도착(thinking 델타 제외 · 어느 바퀴든 처음 나온 글자) — 10-30 Q-3 |
| `ttft_answer_ms` | `t0` → 마지막 Sonnet 호출(답 바퀴)의 첫 `text_delta` — case2 는 도구 바퀴 앞 글이 있을 수 있어 같이 남김 |
| `total_ms` | `t0` → 답 스트림 끝 |
| `stages[]` | `{name, start_ms, end_ms, tokens?}` — case1 · 2: `claude#n` · `tool:<이름>#n` / case3: `hub_resolve` · `jev` · `hub_path` · `claude` (`start_ms` · `end_ms` 는 `t0` 기준) |
| `llm_round_trips` | Sonnet 호출 수(+ case3 는 `jev_calls` 따로) |
| `tokens` | 단계별 Anthropic `usage`(input · output · cache_creation · cache_read) · Jev `usage.input_tokens` |

- 단건 값은 편차가 크다 — 결론은 쌓인 기록의 경향으로 본다(README §3). 「같은 질문 다시」 버튼(§6 · R-8)

### 4-2. 기록 꼴(한 질문 = `runs/runs.jsonl` 한 줄)

README §6 꼴에 아래를 더한다.

```json
{
  "run_id": "…", "asked_at": "…", "question": "…",
  "versions": {
    "answer_model": "claude-sonnet-5-5", "judge_model": "claude-opus-5-5", "extract_model": "…",
    "jev_model": "jev-1.14.0",
    "prompts": {"common": "<sha12>", "case1": "…", "case2": "…", "case3": "…", "judge": "…", "extract": "…"},
    "gold_build_hash": "<골드 응답 머리 build.build_hash>",
    "raw_manifest_sha16": "<원장 MCP 응답 머리 raw.dir_manifest_sha16>",
    "app_commit": "<clinic_chat git sha>"
  },
  "settings": {"thinking": "between_tools", "effort": "high", "tool_loop_max": 12, "jev_confidence_min": 0.3, "jev_option_order_seed": 0},
  "cases": {"case1": {"answer": "…", "stop_reason": "…", "loop_capped": false, "error": null,
                      "timing": {"ttft_ms": 0, "ttft_answer_ms": 0, "total_ms": 0, "stages": [], "llm_round_trips": 0},
                      "tokens": {}, "trace": {}, "word_check": {}, "judge": {}}, "case2": {}, "case3": {}},
  "judge_order": ["case2", "case1", "case3"], "judge_seed": 0
}
```

- 사람 확인은 `runs/human_checks.jsonl` 에 따로 덧붙임(`{run_id, case, verdict: "맞음|틀림", item?, note, at}`) — 기록 줄은 고치지 않는다
- 기록에 키 · 환경 변수 값을 넣지 않는다

### 4-3. 서버 ↔ 화면 계약(SSE)

`POST /api/ask {question}` → `{run_id}` · `GET /api/runs/{run_id}/events`(SSE) 이벤트: `stage{case, name, start_ms, end_ms}` · `text{case, delta}` · `trace{case, …}` · `case_done{case, timing, tokens}` · `word_check{case, …}` · `judge{cases…}` · `run_done{run_id}` · `error{case?, message}` / `GET /api/runs?limit=` 기록 목록 · `POST /api/runs/{run_id}/human_check` · `POST /api/runs/{run_id}/rerun`

## 5. 품질 두 층

세 열이 모두 끝나면 ① → ② 순서로 자동(README §5).

### 5-1. ① 단어 검사(결정론 판정)

| 단계 | 규칙 | 근거 |
|---|---|---|
| 이름 뽑기 | LLM 추출(R-4 — `claude-opus-5-5` · effort `low` · 구조화 출력 `output_config.format` 으로 `{names: [{text, kind: 시술\|제품\|장비\|부위\|성분}]}`) · 답 원문만 입력 · **시맨틱 사전 · 원장을 주지 않음**(지어낸 이름을 놓치지 않게) | README §4 ① 1 · O-4 |
| 정규화 | **`semantic.json` `dictionary.resolve_rules.normalize` 그대로** — NFKC → 라틴 악센트 접기(NFKD 결합 부호 제거 · NFC) → 입력 접기 `fold`(「쳐짐」 → 「처짐」) → 공백 제거 → 괄호 `strip_chars`(`()[]`) 지움(안 글자는 남김) → **전부 소문자**. 답에서 뽑은 이름 · 원장 문자열 · 사전 `expr` · `variants` 에 **같은 함수 하나**를 쓴다(`fold` · `strip_chars` 는 `SEMANTIC_JSON` 에서 읽음 — 문서 = 코드). 「영문으로 시작하면 소문자」(README §4 ① 2 · 3단계 lexicon 문구)는 쓰지 않는다 — 한글로 시작하고 영문 대문자가 섞인 원장 문자열(실물 290개 · 예 「필러(HA/CaHA)」 · 「…Nd:YAG)」)이 소문자로 안 바뀌어 거짓 「없는 이름」이 나기 때문(검수 F-1) | `semantic.json` `dictionary.resolve_rules`(note: 사전은 이 규칙 하나) · `semantic.md` §4 · `semantic-build.py:55-63` |
| 대조 | 원장 21 파일의 모든 문자열 값(정규화 뒤)에 그 이름이 부분 문자열로 있나 → 없으면 시맨틱 사전 `dictionary.expressions[].expr · variants[]`(정규화 뒤)와 같은가 | README §4 ① 3 |
| 출력 | 이름마다 `{name, norm, found, where[] (원장 파일 · 경로 · 최대 3), via: "원장\|사전"}` · 열마다 `not_found` 수 | README §4 ① 4 |
| 결정론 | 대조는 결정론 · 뽑기 결과(LLM)는 기록에 그대로 남겨 다시 대조 가능 | — |

- 2자 미만 이름은 대조에서 뺌(부분 일치 거짓 「있음」 방지) — R-4
- 원장은 `RAW_DIR` 로컬 파일을 직접 읽는다(허브 원장 MCP 를 부르지 않음 — 채점 경로가 실험 대상 서버에 기대지 않게) · 시작 때 21 파일 해시를 기록 `raw_manifest_sha16` 과 같은 식으로 셈

### 5-2. ② Opus 채점

| 항목 | 묻는 것 | 값 |
|---|---|---|
| 정확성(관계 · 숫자) | 시술 ↔ 부위 ↔ 고민 관계 · 간격 · 용량 숫자가 원천과 맞나 | 통과 · 실패 · 해당 없음 |
| 안전 정보 | 추천한 시술의 금기 · 주의를 같이 말했나(10-26) | 〃 |
| 후보 처리 | 뜻이 갈리는 말을 단정하지 않고 고르거나 되물었나(10-27) | 〃 |
| 불확실 표시 | 근거 약 · 정보 없음을 「안전함」 · 「확실함」처럼 말하지 않았나 | 〃 |
| 질문에 답함 | 물은 것에 답했나 · 새지 않았나 | 〃 |

- 항목 = README §4 ② 5개 그대로(O-5 → R-9 「5개 그대로 시작」). 「지어낸 말」은 ① 몫
- **가리기**: 세 답을 seed 로 섞어 A · B · C 로만 보여 줌 · case 이름 · 도구 흔적 · 속도 안 보임 · `judge_order` · `judge_seed` 기록
- **기준 자료(O-3 → R-10 = B 원장)**: Opus 에 원장 도구 3(`raw_list` · `raw_get` · `raw_search`)을 준다 — 원장 전체를 넣지 않고 필요한 곳만 찾아 읽음(README 의 B 「크기 문제」를 도구로 풂) · 골드 결과는 주지 않음(C 는 case2 · 3 에 유리)
- **원장 도구는 앱 안 로컬 구현**(`quality/raw_tools.py`): SPEC-005 §5-12 R1~R3 과 같은 이름 · 입력 · 출력 계약 · `RAW_DIR` 로컬 원장 파일을 읽는다 · 허브 원장 MCP 를 부르지 않는다 — ① 과 같은 이유(채점 경로가 실험 대상 서버에 기대지 않게 · 기준 하나 · 검수 W-3). case1 이 쓰는 허브 원장 MCP 와 계약이 같은지는 WORK-004 Phase 7 실물 대조에서 확인
- **근거 인용 필수**: 실패마다 `{item, answer: A|B|C, claim, evidence: {file, path, quote}}`. 앱이 `quote` 가 그 경로 원문에 실제로 있는지 원장 로컬 파일로 확인 → 없으면 그 실패는 `invalid`(무효 · 화면에 회색)
- 호출: `claude-opus-5-5` · thinking 기본(Opus 5.5 는 못 끔) · effort `medium` 명시(기본값) · `tool_choice: auto` · 도구 루프(상한 `CASE_TOOL_LOOP_MAX`) 뒤 마지막 응답을 구조화 출력(`output_config.format`)으로 받음
- **사람 확인**: 열마다 「맞음 · 틀림」 + 메모(README §4 「처음 몇 건은 사용자가 채점관 검수」) — §4-2 `human_checks.jsonl`

## 6. 화면

README §5 와이어 그대로 + 질문 기록 목록.

```
┌────────────────────────────────────────────────────────────┐
│ ⚠ 환자 정보 넣지 말 것 · 질문과 노드 이름이 Jev(미국)로 나감   │
│ 질문 [                                          ] [보내기] │
├──────────────────┬──────────────────┬──────────────────────┤
│ case1 원장 MCP   │ case2 골드 MCP   │ case3 골드 + Jev     │
│ ⏱ 첫 글자 / 전체 │ ⏱ 첫 글자 / 전체 │ ⏱ 첫 글자 / 전체     │
│ ▓▓ ▓ ▓▓ 왕복     │ ▓▓ ▓ ▓▓ ▓▓ 왕복  │ ▏hub ▓ jev ▏hub ▓▓ claude │
├──────────────────┼──────────────────┼──────────────────────┤
│ [답변 스트리밍]  │ [답변 스트리밍]  │ [답변 스트리밍]      │
├──────────────────┼──────────────────┼──────────────────────┤
│ ▸ 원장 도구 N    │ ▸ 도구 호출 N    │ ▸ Jev 의도 · 슬롯    │
│   입력 · 결과    │   입력 · 결과    │   confidence(낮음 ⚠) │
│   토큰 수        │   쓴 노드 id     │ ▸ 허브 경로 · 노드 id│
├──────────────────┼──────────────────┼──────────────────────┤
│ ① 없는 이름 N    │ ① 없는 이름 N    │ ① 없는 이름 N        │
│ ② 항목별 ●/✕     │ ② 항목별 ●/✕     │ ② 항목별 ●/✕         │
│   (실패 근거)    │                  │                      │
│ [사람 확인 ✓✗]   │ [사람 확인 ✓✗]   │ [사람 확인 ✓✗]       │
└──────────────────┴──────────────────┴──────────────────────┘
  [같은 질문 다시 ×3]
  ↓ 질문 기록 — 한 줄씩: 시각 · 질문 · 열별 total_ms · 없는 이름 수 · ② 통과 수 · 사람 확인 · 판(골드 해시 앞 8자)
```

- 단계 막대 = `stages[]` 를 `t0` 기준 가로 시간축으로(열마다 같은 눈금)
- 기록 줄을 누르면 그 질문의 3열을 기록에서 다시 그림(다시 호출 안 함)
- 얼굴 지도 패널 없음(README §5)

## 7. 열린 것 처리표

### 7-1. README 열린 것 O-1~O-9

| # | 무엇 | 처리 | 근거 · 값 |
|---|---|---|---|
| O-1 | case1 원장 넣는 방식 | **결정됨** — 원장 MCP 도구 3 | 10-30 Q-1 · 「원장도 MCP 로」 |
| O-2 | 세 케이스 시스템 프롬프트 | **결정됨** — R-5 | README 선택지 「답 문장 지시는 같게 · 데이터 · 도구 설명만 다르게」 |
| O-3 | Opus 기준 자료 | **결정됨** — R-10(B 원장 — 앱 안 로컬 원장 도구로) | README 「논의에선 B 기본」 |
| O-4 | ① 이름 뽑기 방법 | **결정됨** — R-4(LLM 추출 · Opus 5.5) | README 선택지 |
| O-5 | 품질 항목 최종 목록 | **결정됨** — R-9(5개 그대로) | README §4 ② |
| O-6 | Jev 호출 꼴 | **결정됨** — 이 스펙 §3-4(의도 12 · 슬롯 = SPEC-005 vocab · 도구 입력) · 세부 값 R-6 · R-7 | SPEC-005 §5 · Q-4 · Q-5 · Q-7 |
| O-7 | 허브 도구 목록 · 의도별 경로 | **결정됨** — SPEC-005 §5(도구 9 · 경로) · §5-12(원장 3) | SPEC-005 |
| O-8 | 화면 · 실행 위치 | **결정됨** — 레포 `kknaks/clinic_chat`(공개 · §2-3 경로) · 스택 R-1 | 10-30 |
| O-9 | 모델 키 | **결정됨** — 사용자 보유 · env 로만 · Claude 는 API 키 별도 | D-11 · 10-30 |

### 7-2. Jev 조사 Q-1~Q-8(10-30 사용자 「응」 — 전부 결정됨)

| # | 결정 | 이 스펙 |
|---|---|---|
| Q-1 | case1 = 원장 MCP | §3-2 |
| Q-2 | Anthropic Python SDK + MCP 클라이언트 직접 루프 | §2-1 |
| Q-3 | ttft = 첫 텍스트 델타 · thinking 끔(세 케이스 같게) | §3-1 · §4-1 |
| Q-4 | 255 넘으면 허브 사전 검색으로 후보 줄인 뒤 Choice | §3-4 |
| Q-5 | 되묻기 문턱 0.3 시작 · 기록 보고 조정 | §3-4 · env `JEV_CONFIDENCE_MIN` |
| Q-6 | `jev-1.14.0` 고정 | §2-1 · env |
| Q-7 | 노드 목록 앱 시작 1회 캐시 | §3-4 |
| Q-8 | 영어 병기 안 함(처음) | §3-4 슬롯 설명 한국어만 |

### 7-3. R-1~R-10 — 결정됨(10-30 사용자 승인)

이 스펙이 추천한 값을 사용자가 10-30 한 번에 승인했다. 다시 논의하지 않는다(값 조정은 기록을 보고 사용자가 정함).

| # | 무엇 | 결정 | 이유 |
|---|---|---|---|
| R-1 | 서버 · 화면 스택 | FastAPI + SSE + 빌드 없는 정적 페이지 | 화면 하나 · 로컬 · 실행 명령 하나 · 의존성 적음 |
| R-2 | case1 · 2 도구 루프 상한 | Sonnet 호출 12번 · 닿으면 `tool_choice none` 으로 마지막 답 1번 + `loop_capped` | 무한 루프 · 비용 막기 · 셈은 기록으로 조정 |
| R-3 | Sonnet effort | `high`(모델 기본값 명시) · 세 케이스 같음 | `between_tools` 가 high 이하만 받음 · 기본값이면 따로 고른 것이 없음 |
| R-4 | ① 이름 뽑기 | `claude-opus-5-5` · effort low · 구조화 출력 · 2자 미만 제외 | 이미 정해진 채점 모델 — 새 모델을 들이지 않음 · 답 모델(Sonnet)과 달라 자기 답 편들기 없음 |
| R-5 | 프롬프트 | 공통부 같음 + 케이스별 데이터 · 도구 설명만 | README O-2 선택지 |
| R-6 | 여러 고민 슬롯 | 고민 Choice 1 + ① 후보 고민마다 Noul(0.5 이상이면 더함) | Choice 는 하나만 고름(jev-research §2-3 문서 패턴) |
| R-7 | Jev 선택지 순서 | seed 로 섞고 기록 | 앞쪽 기울기(jev-research §2-3) |
| R-8 | 같은 질문 다시 | 버튼 · 3회 · 중간값 표시 | README §3 「필요하면 재실행 버튼(중간값)」 |
| R-9 | 품질 항목 | README 5개 그대로 시작 | O-5 |
| R-10 | Opus 기준 자료 | B 원장 — 원장 도구 3 을 Opus 에 줌 · **도구는 앱 안 로컬 구현**(SPEC-005 §5-12 R1~R3 과 같은 계약 · `RAW_DIR` 로컬 원장 파일 · 허브 원장 MCP 안 부름) | README 「B 기본」 · 크기 문제를 도구 조회로 풂 · C 는 골드 쪽에 유리 · ① 과 같이 채점이 실험 대상 서버에 기대지 않게(검수 W-3 · 코디 판단) |

### 7-4. 사용자 몫

| # | 무엇 | 왜 사용자만 |
|---|---|---|
| U-1 | Jev 콘솔 접근 · 키 발급(`console.typesafe.ai`) · 조직 rate limit 확인 | **완료(10-30)** — 키 받음 · 사용자가 워크트리 `.env` 에 직접 넣음 |
| U-2 | Anthropic API 키를 `.env` 에 넣기(충전된 API 키 · 구독 아님) | **완료(10-30)** — 키 받음 · 사용자가 워크트리 `.env` 에 직접 넣음 |
| U-3 | R-1~R-10 승인 · 바꿈 | **완료(10-30)** — 승인(§7-3) |
| U-4 | 실험 중 사람 확인 표시 · 문턱(0.3) 조정 판단 | README §4 · 10-30 Q-5 「기록 보고 조정」 — 실험하면서 |

### 7-5. 남은 열린 것

| # | 무엇 | 선택지 | 지금 |
|---|---|---|---|
| L-1 | 실험 기록(`runs.jsonl` · `human_checks.jsonl`) 저장 위치 | (가) 레포 안 `runs/` 폴더 · 커밋 안 함 / (나) 레포에 커밋 | **사용자 답 대기** — 답 전까지 지금 `.gitignore`(`runs/` · `*.jsonl` 막음) 그대로 = (가) 꼴로 둔다. (나) 로 정해지면 공개 레포 규칙(§1 · 환자 정보 · 키)과 `.gitignore` 를 같이 고친다 |

## 8. 사용자 실행 절차

전제: 허브 골드(SPEC-005 · WORK-003)가 완성돼 로컬에서 뜬다 · U-1 · U-2 끝(10-30 — 키는 사용자가 워크트리 `.env` 에 직접).

```bash
# 1) 허브(18005) — SPEC-005 코드 레포
cd /Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend
docker compose -f graph-local.compose.yml up -d
uv run --env-file envs/.env.gold uvicorn app.graph_main:app --host 127.0.0.1 --port 18005
curl -s 127.0.0.1:18005/procedure-hub/gold/health          # 발행 빌드 id · 원장 manifest 21/21

# 2) 실험 앱(18210) — clinic_chat 작업 워크트리(브랜치 kknaksss/hub-evals)
cd /Users/kknaks/orca/workspaces/clinic_chat/hub-evals
cp .env.example .env        # .env 가 이미 있으면 건너뜀 · ANTHROPIC_API_KEY · TYPESAFE_API_KEY · RAW_DIR · SEMANTIC_JSON 채움(.env 는 커밋 안 됨)
uv sync
uv run python -m clinic_chat.server   # config.py(pydantic-settings)가 루트 .env 를 읽음 — --env-file 필요 없음

# 3) 화면
open http://127.0.0.1:18210
```

- 첫 질문: 환자 정보 없는 일반 질문 하나를 넣고 [보내기] — 세 열이 같이 흐르고, 셋 다 끝나면 ① → ② 가 자동으로 붙고, 아래 기록 목록에 한 줄이 생긴다
- 서버 기동 때 확인 줄: 허브 골드 · 원장 MCP 연결 · vocab 캐시 셈 · 모델 id(`client.models.list()` 로 한 번 — jev-research §4) · 키가 없으면 그 케이스만 「키 없음」으로 비활성

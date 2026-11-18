---
type: spec
id: SPEC-004
title: "상담 채팅 1판 — CLI 세션 기억(`--session-id` → `--resume`) · htmx 화면(얼굴 점 · 시술 리스트 · 채팅) · 대화 장부 · 이어 묻기 뼈대"
status: draft
product: procedure-hub
feature: phub-gold-jev
version: 0.1.0
created_at: 2026-11-17
updated_at: 2026-11-17
tags:
  - product/procedure-hub
  - feature/phub-gold-jev
  - doc/spec
  - status/draft
links:
  decisions:
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-17 — 「CLI 실행기 = 앱이 직접 띄움」 · 「채팅 조사 뒤 사용자 결정」(U-1 · U-3 · U-4 · U-6 · U-7 · U-8 · U-9 · 상담 플로우는 따로) · 「이번 세션 목표 = 상담 채팅」 · 「Procedure Hub 데이터는 공개 정보」 · 「답 프롬프트 확정(C-1)은 채팅(상담) 단계로 넘김」 · 「테스트 답은 빠짐없이(사용자)」 의 「짧게는 상담 단계에서」)"
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-16 — 「테스트 ≠ 상담」(L0 · L1 · L2 · 대화 장부 · 여러 턴 맥락) · 「LLM 에는 필요한 것만」 · 「원칙: 폭은 빠짐없이, 깊이만 Jev 판단」 · 「안전 정보를 처음부터 붙이지 않는다」 · 「D8 LLM = 지금은 CLI 구독 · DB화 때 SDK」)"
    - "orchestration/work/phub-gold-jev/spec-chat-instructions.md (「정해진 것」 — 코디가 위 _RESUME §2 행과 조사 코디 기본값 C-1 ~ C-9 를 풀어 적은 지시서 · 보조 근거)"
  sources:
    - "orchestration/work/phub-gold-jev/research-chat.md (§0 ~ §7 — 사실 · 셈 · 파일:줄 · 「확인 안 됨」 8)"
    - "orchestration/work/phub-gold-jev/SPEC-001-hub-gold-mcp.md (0.6.0 — §4-5 `concern_candidates` · §4-0 · §5-9 HG1 · HG3)"
    - "orchestration/work/phub-gold-jev/SPEC-002-chat-eval.md (0.6.0 — §3-1 · §3-2a · §3-5 · §3-6 · §3-7 · §4 · §5 · §6 · §7)"
    - "clinic_chat 워크트리 phub-gold-jev (HEAD 6303e18 · 읽기만) — clinic_chat/{llm/cli.py,llm/cli_process.py,llm/auth.py,columns/col_b.py,columns/base.py,walk/,clients/,progress.py,runs.py,prompts.py,config.py,web/server.py} · prompts/ · pyproject.toml · README.md · tests/fake_cli"
    - "PROCEDURE-HUB 워크트리 phub-gold-jev (HEAD 85c28af · 읽기만) — backend/app/modules/gold/{repository.py,memory.py}"
    - "orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model/silver/{site,concern_site,procedure_case,concern}.csv (gitignore · 로컬)"
    - "로컬 CLI `claude --help`(2.1.322) · open_kknaks docs/legacy/CLAUDE_CODE_ANALYSIS.md §2 · §4 (옵션 정리 — 꼴 참고만)"
  related:
    - "orchestration/work/phub-gold-jev/SPEC-001-hub-gold-mcp.md"
    - "orchestration/work/phub-gold-jev/SPEC-002-chat-eval.md"
    - "orchestration/work/phub-gold-jev/SPEC-003-hub-gold-db.md"
---

# SPEC-004 — 상담 채팅 1판

경로 접두어: `$W` = 이 폴더 · `$A` = clinic_chat 워크트리 `phub-gold-jev`(읽기만 · 구현은 여기에 이어서) · `$H` = PROCEDURE-HUB 워크트리 `phub-gold-jev`(읽기만) · `$SM` = `orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model`(gitignore · 로컬).
「조사」 = `$W/research-chat.md` · 「지시서」 = `$W/spec-chat-instructions.md` · 「재셈」 = 이 워커가 `$SM/silver` 의 CSV 와 로컬 `claude --help` 로 다시 본 값(부록 B · §3-1).
줄마다 상태를 적었다: **결정** = `_RESUME` §2 에 행이 있다 · **기본값** = 조사 §0-2 「나」 의 코디 기본값(C-1 ~ C-9) · **제안** = 이 워커의 제안(코디 · 사용자가 정한다 — §11).
이 문서에는 비밀값 · 키 · 내부 주소가 없다. 화면에 보일 문장도 없다(§4-5).

## 0. 요약

| 무엇 | 이 스펙이 정하는 것 |
|---|---|
| 목표 | 「한 턴 = 고민 → 시술 리스트 + 얼굴 점 + 짧은 답」 과 「이어 묻기(장부 맥락)」 의 **뼈대**. 상담 플로우(단계 · 시술을 눌렀을 때 · 상세 목록 자리)는 0.2 |
| 화면 | 새 화면 · 서버사이드 렌더링 + htmx · 왼쪽 위 얼굴 SVG + 부위 점 · 왼쪽 아래 시술 리스트 · 오른쪽 채팅 · `127.0.0.1:18222`(18220 시험 화면은 그대로) |
| LLM | 앱이 `claude -p` 를 직접 띄운다 · Sonnet · 첫 턴 `--session-id <앱 UUID>` → 다음 턴 `--resume <같은 UUID>` · 도구 없음 · stream-json. SDK 는 갈아 끼울 자리(인터페이스)만 |
| 재료 | 시험 앱의 B 흐름 그대로(맨 앞 Jev 판단 → 허브 폭 → 깊이 → 틀린 말 검사) · LLM 에는 필요한 칸만 · **턴마다 새로 읽은 것만** 그 턴 메시지에 |
| 시술 리스트 | 앱이 허브 `concern_candidates` 행으로 **결정론**으로 짓는다(LLM 답 문장이 아니다) · 계열 묶음 · 층 표시 · LLM 보다 먼저 그린다 |
| 얼굴 | 손으로 새로 그린 SVG · 부위 코드마다 0 ~ 1 비율 좌표(코드 안의 표) · 좌우 짝은 점 둘 · 얼굴 밖 · 넓은 부위는 얼굴 아래 라벨 · 점 기준 = 고민 부위(`concern_site`) |
| 장부 | 앱 메모리 + 파일 한 줄씩 — 턴 · session_id · 고른 대상 · 읽은 재료 id · 답 · 시간 |
| 허브에 필요한 것 | `concern_candidates` 응답 머리에 고민 부위 코드 목록 — **SPEC-001 0.7 이 닫는다**(여기는 필요만 적는다 — §6-3) |
| 범위 밖 | 상담 플로우 · SDK 모듈 · API 키 · 배포 · 몸통 그림 · 채점 — §1-3 |

## 1. 목적 · 범위

### 1-1. 목적

연결 시험은 「질문 하나에서 연결된 정보가 빠짐없이 보이나」 였다(단일 턴 · `_RESUME` §2 11-16 「테스트 ≠ 상담」). 11-17 결정으로 그 다음을 연다 — **같은 길 찾기(gold + Jev) 위에 여러 턴 상담 화면을 얹는다**(`_RESUME` §2 11-17 「이번 세션 목표 = 상담 채팅」). 이번 판은 한 턴의 뼈대와 이어 묻기의 뼈대까지다.

### 1-2. 정해진 것(다시 묻지 않는다)

지시서 「정해진 것」 을 옮긴다. 「조사」 칸은 근거가 된 조사 절이다.

| # | 정해진 것 | 근거 | 이 문서에서 |
|---|---|---|---|
| D-1 | 화면 = 서버사이드 렌더링 + htmx · 왼쪽 위 얼굴 · 왼쪽 아래 시술 리스트 · 오른쪽 채팅 | `_RESUME` §2 11-17 「이번 세션 목표 = 상담 채팅」 | §4 |
| D-2 | 새 화면 · 포트 18222 · 18220 시험 화면은 그대로 | 기본값 C-7 · 조사 §4-2 | §2 · §4-1 |
| D-3 | Jinja2 를 의존에 더한다 · htmx 는 로컬 파일로 고정 | 기본값 C-8 · C-9 · 조사 §4-3 | §2-3 |
| D-4 | LLM = CLI 먼저 · SDK 모듈은 배포 전(이 판 범위 밖 — 갈아 끼울 자리만) | `_RESUME` §2 11-17 「채팅 조사 뒤 사용자 결정」 U-1 | §3 · §3-6 |
| D-5 | 앱이 CLI 를 직접 띄운다(open_kknaks 안 씀) | `_RESUME` §2 11-17 「CLI 실행기 = 앱이 직접 띄움」 | §3-2 |
| D-6 | 모델 Sonnet | 같은 행 U-4 | §3-2 |
| D-7 | CLI 옵션: `--session-id` 첫 턴 → `--resume` · `--no-session-persistence` 뺌 · `--system-prompt-file` · `--fallback-model haiku` · `--effort low` · `--max-turns 1` · 도구 전부 막음 · stream-json + partial + verbose · `--continue` · `--mcp-config` · `--max-budget-usd` 안 씀 · `--json-schema` 보류 · `--bare` 주의 | `_RESUME` §2 11-17 「CLI 실행기」 행 | §3-2 |
| D-8 | 대화 장부 = 앱 메모리 + 파일 한 줄씩(`runs.jsonl` 꼴) — 턴 · session_id · 고른 대상 · 읽은 재료 id · 답 · 시간 | 기본값 C-2 · 조사 §1-5 | §5-1 |
| D-9 | 재료 = B 흐름(gold + Jev 가 맨 앞에서 판단 · 허브 폭 · LLM 에는 필요한 칸만) | `_RESUME` §2 11-16 「길 찾기 재설계 진행」 · 「LLM 에는 필요한 것만」 | §4-2 |
| D-10 | 턴마다 새로 읽은 것만 그 턴 메시지에(덧붙이기) | 기본값 C-1 · 조사 §1-2 | §5-3 |
| D-11 | 시술 리스트는 앱이 허브 행으로 결정론으로 짓는다(계열 묶음 · 층 표시) · 채팅 답은 짧게 · 리스트를 다시 읊지 않는다 | 지시서 · 기본값 C-3 · 조사 §2-3 | §6-1 · §7 |
| D-12 | 얼굴 = 손 SVG(새로 그림 · 벡터) · 좌표는 코드(표)에 · 부위 코드마다 0 ~ 1 비율 좌표 · 좌우 짝은 점 둘 | `_RESUME` §2 11-17 U-6 · 기본값 C-6 | §8 |
| D-13 | 얼굴 밖 · 넓은 부위(얼굴 전체 · 전신 · 등 · 허벅지 …)는 얼굴 아래 라벨 | 같은 행 U-8 | §8-3 |
| D-14 | 점 기준 = 고민 부위(`concern_site`) | 지시서 | §6-2 |
| D-15 | 원본 PNG 는 레포에 두지 않는다(밑그림 참고용) | 같은 행 U-7 | §8-1 |
| D-16 | 근거 꼬리(답 줄 ↔ 재료 줄) 유지 · 화면에서만 숨김 | 같은 행 U-9 | §4-4 · §7-3 |
| D-17 | 화면 문구는 짓지 않는다(빈 자리 표시 · 사용자 몫) | 지시서 | §4-5 |
| D-18 | 상담 플로우(짧게 → 깊게의 단계 · 시술을 눌렀을 때 · 상세 턴 목록 자리)는 사용자가 따로 준다 — U-5 · U-10 은 그때 | 같은 행 「상담플로우는 별도로」 | §10 O-1 |
| D-19 | 허브가 고민 → 부위를 응답에 안 내는 것은 SPEC-001 0.7 이 닫는다 | 지시서 · 기본값 C-5 | §6-3 |
| D-20 | 이어 묻는 턴의 대상 = 장부의 앞 턴 대상을 Jev 대상 후보에 함께 | 기본값 C-4 · 조사 §5-2 | §5-2 |
| D-21 | open-kknaks 규칙은 이 앱과 무관 | 같은 행 U-3(코디) | §3-6 |
| D-22 | API 키는 SDK 때 | 같은 행 U-2 | §1-3 |
| D-23 | Procedure Hub 데이터(원장 · silver · gold)는 공개 정보 — 부위 코드 · 이름을 이 문서 · 앱 레포에 적어도 된다 | `_RESUME` §2 11-17 「Procedure Hub 데이터는 공개 정보」 | 부록 B |

### 1-3. 범위 밖

| 무엇 | 왜 · 어디서 |
|---|---|
| 상담 플로우(L0 → L1 → L2 의 단계 · 시술을 눌렀을 때 · 상세 턴의 긴 목록 자리) | D-18 — 0.2 |
| SDK 모듈 · API 키 · 프롬프트 캐싱 설계 | D-4 · D-22 — 배포 전 |
| 배포 · 여러 사람 동시 사용 · 구독 로그인으로 여러 사람이 쓰는 것의 약관 | 조사 §7-3 「확인 안 됨」 — 이 판은 로컬 한 사람 |
| 몸통 두 패널 | `_RESUME` §2 11-17 「몸통 두 패널은 이번엔 안 씀」 |
| 채점 · 세 열 비교 · 속도 탭 | 시험 화면(18220)의 것 — 손대지 않는다 |
| 허브 코드 변경 | SPEC-001 0.7 |
| 답 프롬프트 문구 확정 | 사용자(C-1) — 이 판은 초안 파일의 자리와 뼈대까지(§7) |

## 2. 구조

### 2-1. 원칙

| # | 규칙 | 상태 |
|---|---|---|
| ST1 | 상담은 **새 패키지** `clinic_chat/consult/` 다. 시험 앱의 열 · runner · 화면(`columns/col_a.py` · `col_c.py` · `runner.py` · `batch.py` · `web/` · `quality/` · `evalset/` · `report.py` · `speed.py`)은 **고치지 않는다** | 결정(D-2) · 자리 이름은 제안 |
| ST2 | 길 찾기는 **같은 코드**를 쓴다 — `columns/col_b.py` 의 `walk()`(`$A/clinic_chat/columns/col_b.py:161`)와 `walk/` 전부 · `clients/hub_rest.py` · `clients/jev_client.py`. 상담용으로 걷기를 다시 짓지 않는다 | 결정(D-9) |
| ST3 | 함께 쓰는 코드에 손대는 곳은 **선택 인자 둘뿐**이고 기본값이 지금 동작이다(§5-2 CR2 의 `carry` · §5-3 AP2 의 줄 번호 시작) — 시험 앱의 답 키 · 기록 · 시험 214 건이 그대로 통과해야 한다 | 제안 |
| ST4 | 앱 코드는 사용자에게 보일 문장을 갖지 않는다 — 문장은 `prompts/` 에만(`col_b.py:11` 과 같은 규칙) · 화면 문구는 빈 자리(§4-5) | 결정(D-17) |
| ST5 | 상담 설정은 `config.py` 의 `Settings` 에 칸을 더한다(이름은 §2-4 — 제안) · 지금 칸의 뜻 · 기본값은 바꾸지 않는다 | 제안 |

### 2-2. 모듈 자리(제안)

| 자리 | 무엇 | 새로 / 함께 |
|---|---|---|
| `clinic_chat/consult/__main__.py` · `server.py` | FastAPI 앱 · 라우트(§4-1) · 18222 | 새로 |
| `clinic_chat/consult/turn.py` | 한 턴 흐름(§4-2) — 걷기 → 리스트 · 부위 → LLM → 장부 | 새로 |
| `clinic_chat/consult/ledger.py` | 대화 장부(§5-1) — 메모리 + `turns.jsonl` | 새로(`runs.py` `RunStore` 의 덧붙이기 꼴을 따름) |
| `clinic_chat/consult/carry.py` | 이어 묻기 — 앞 턴 대상 → 후보(§5-2) | 새로 |
| `clinic_chat/consult/material.py` | 상담 재료 — 새로 읽은 줄만 · 줄 번호 이어감 · 목록 요약 줄(§5-3) | 새로(`walk/material.py` 의 `build` · `to_lines` 를 부른다) |
| `clinic_chat/consult/listing.py` | 시술 리스트 짓기(§6-1) | 새로 |
| `clinic_chat/consult/sites.py` · `face_coords.py` | 고민 부위 → 점 · 라벨(§6-2) · 좌표표(§8-2) | 새로 |
| `clinic_chat/consult/templates/` · `static/` | Jinja2 조각 · 얼굴 SVG · htmx 파일 · CSS | 새로 |
| `clinic_chat/llm/chat.py` | 대화 LLM 인터페이스(§3-6) | 새로 |
| `clinic_chat/llm/chat_cli.py` | CLI 구현(§3) — `--session-id` / `--resume` | 새로 |
| `prompts/consult/` | 상담 지시 초안 · 상담용 Jev 지시(§7-2) | 새로 |
| `clinic_chat/llm/cli_process.py` | `run_cli` · `child_env` · `StopRun` | 함께(안 고침) |
| `clinic_chat/llm/auth.py` | 구독 인증 확인(10분 캐시) | 함께(안 고침) |
| `clinic_chat/llm/cli.py` | `ClaudeIngest`(stream-json → 답 · 토큰 · 시간) · `DISALLOWED_TOOLS` · `USAGE_KEYS` | 함께(안 고침 — `claude_args` 는 `--no-session-persistence` · `--system-prompt` 가 박혀 있어(`cli.py:80-84`) 상담은 자기 인자 함수를 따로 갖는다) |
| `clinic_chat/columns/col_b.py` | `walk()` · `judgement()` · `split_tail()` · `_TailFilter` · `TAIL_MARK` | 함께(`walk()` 에 선택 인자 하나 — CR2) |
| `clinic_chat/walk/` | 전부 | 함께(`front()` · `material.build()` 에 선택 인자 하나씩 — CR2 · AP2) |
| `clinic_chat/clients/` · `progress.py` · `timing.py` · `prompts.py` · `runs.py`(`now_iso` · `app_commit`) | 그대로 | 함께(안 고침) |

- `_TailFilter` 는 밑줄 이름이다 — 상담이 가져다 쓰려면 이름을 드러내거나(`__all__`) 같은 꼴을 상담 쪽에 둔다. 동작은 같아야 한다(표식이 조각 둘에 걸쳐도 흘리지 않음 — `col_b.py:307-332`).
- 세션 id 는 `ClaudeIngest` 가 지금 읽지 않는다(`cli.py:159-163` `_init` 은 모델 · 판 · 인증만). 상담 실행기는 init 줄의 세션 id 를 **자기가 준 값과 대조**한다(CL7).

### 2-3. 의존(제안 — 판 번호는 WORK 에서 고정)

| 무엇 | 지금 | 이 판 |
|---|---|---|
| `jinja2` | `uv.lock` 에 없음(조사 §4-3) | 직접 의존에 더함(D-3) |
| `python-multipart` | `uv.lock` 에 딸려 옴(0.0.33) · 직접 의존 아님 | 폼 본문을 받으므로 직접 의존에 적는다 |
| `sse-starlette` | 딸려 옴(3.7.0) · 직접 의존 아님 | 쓰지 않는다 — 시험 화면처럼 `StreamingResponse` 로 SSE 를 낸다(`web/server.py:82-86` `to_sse` 꼴) |
| htmx · htmx SSE 확장 | 없음 | 로컬 파일 둘을 `consult/static/` 에 고정(D-3) · 판 번호 · 라이선스 글은 WP-0 에서 확인해 함께 둔다(조사 §4-3 「확인 안 됨」) |
| `anthropic` | 없음 | **더하지 않는다**(D-4) |

### 2-4. 설정 칸(이름 · 기본값 전부 제안 — C-10)

| env | 기본 | 뜻 |
|---|---|---|
| `CHAT_PORT` | `18222` | 상담 화면 포트(D-2) |
| `CHAT_MODEL` | `sonnet` | `--model`(D-6) |
| `CHAT_FALLBACK_MODEL` | `haiku` | `--fallback-model`(D-7) |
| `CHAT_EFFORT` | `low` | `--effort`(D-7) |
| `CHAT_TURN_TIMEOUT_SEC` | `120` | 한 턴의 CLI 시간 한도(CL11) — 시험 앱의 `CLI_TIMEOUT_SEC` 600 은 상담에 길다 |
| `CHAT_CLI_CWD` | 시스템 임시 폴더 아래 고정 이름 하나 | CLI 를 띄우는 **고정 cwd**(CL9) |
| `CHAT_MAX_TURNS` | `20` | 한 대화의 턴 한도(CL13) |
| `CHAT_CARRY_TURNS` | `1` | 이어 묻기에서 되짚는 앞 턴 수(CR1) |
| `CHAT_DIR` | `RUNS_DIR` 아래 `consult` | 장부 파일 자리(LG2) — `runs/` 는 gitignore(`$A/.gitignore`) |

- CLI 동시 한도는 지금 칸 `CLI_MAX_CONCURRENT`(기본 1 — `config.py:33`)를 그대로 쓴다(CL12).

## 3. CLI 기억

### 3-1. 사실(조사 · 재셈)

| # | 사실 | 출처 |
|---|---|---|
| F1 | 기억은 CLI 가 쓴 로컬 파일 `~/.claude/projects/<인코딩된 cwd>/<session-id>.jsonl` 에 있다 — 같은 기계에서만 · 턴마다 프로세스를 새로 띄운다 | 조사 §1-1 |
| F2 | 지금 앱은 `--no-session-persistence` 로 세션을 남기지 않고(`$A/clinic_chat/llm/cli.py:82`) 실행마다 임시 cwd 를 만들었다 지운다(`:314` · `:331`) — 그대로는 resume 이 안 된다 | 조사 §1-1 · 코드 |
| F3 | 세션은 id 로 찾으므로 cwd 가 달라도 이어진다(2.1.223 이상 · 이 기계 2.1.322) — 공식 문서의 말이고 **이 조사는 실측하지 않았다** | 조사 §1-1 |
| F4 | 추론은 CLI 로 끄지 못한다 — 가장 낮은 effort 로만 | 조사 §1-1(앱 실물 확인) |
| F5 | 로컬 `claude --help` 에 줄이 있는 옵션: `--session-id <uuid>`(「must be a valid UUID」) · `-r, --resume` · `--fork-session` · `--no-session-persistence` · `--fallback-model` · `--effort`(low · medium · high · xhigh · max) · `--system-prompt` · `--setting-sources` · `--tools` · `--disallowedTools` · `--disable-slash-commands` · `--strict-mcp-config` · `--permission-mode` · `--include-partial-messages` · `--json-schema` · `--max-budget-usd` · `-c, --continue` · `--bare` | 재셈(`claude --help` · 2.1.322) |
| F6 | **`--max-turns` 는 로컬 `claude --help` 에 줄이 없다.** `--system-prompt-file` 도 자기 줄이 없고 `--bare` 설명 안에 `--system-prompt[-file]` 로만 나온다. 둘 다 옵션 정리 문서(§4 「실행 제한」 · 「시스템 프롬프트」)에는 있다 — **이 판(2.1.322)이 받는지는 확인 안 됨** | 재셈 · open_kknaks `docs/legacy/CLAUDE_CODE_ANALYSIS.md` §4 |
| F7 | `--system-prompt-snapshot <on\|off>`(기본 on): 시스템 프롬프트를 대화의 첫 요청에서 기록하고 **그 뒤 요청 · resume 은 뒤 실행이 다른 글을 줘도 기록을 그대로 보낸다**(대화가 압축될 때까지) — help 글이고 실측은 아니다 | 재셈(`claude --help`) |
| F8 | `--bare` 는 구독 로그인을 읽지 않는다(「OAuth and keychain are never read」) — 구독으로 도는 이 판에서는 **쓰지 않는다** | 재셈 · 조사 §1-1 「앞으로의 위험」 |
| F9 | 시험 앱 기록(v06 37 줄 중앙): 첫 글자 2,320ms 가운데 LLM 쪽 약 1.8초(프로세스 띄움 포함) · `cache_read` 4,074 · `cache_creation` 9,171 토큰. resume 을 걸었을 때의 값 · resume 때 앞 대화가 캐시로 읽히는 조건은 **확인 안 됨** | 조사 §1-1 · §6 |

### 3-2. 명령 꼴

| # | 규칙 | 상태 |
|---|---|---|
| CL1 | 앱이 `claude -p` 를 서브프로세스로 직접 띄운다 — `run_cli`(`$A/clinic_chat/llm/cli_process.py:54`) 그대로 · 프롬프트는 stdin · 자식 env 는 `child_env()`(API 키 꼴 env 를 지움 — `cli_process.py:20-37`) · 실행 앞에 구독 인증 확인(`llm/auth.py`) | 결정(D-5) |
| CL2 | **첫 턴** 인자(순서는 뜻 없음):<br>`claude -p --session-id <UUID> --model sonnet --fallback-model haiku --effort low --max-turns 1 --system-prompt-file <상담 지시 파일> --setting-sources "" --tools "" --disallowedTools <목록> --disable-slash-commands --strict-mcp-config --permission-mode bypassPermissions --output-format stream-json --verbose --include-partial-messages` | 결정(D-7) · 격리 인자는 지금 꼴(`cli.py:80-84`) |
| CL3 | **다음 턴** = CL2 에서 `--session-id <UUID>` 를 `--resume <같은 UUID>` 로만 바꾼다. 나머지 인자는 글자 그대로 같다(모델 · effort · 시스템 프롬프트 파일을 대화 도중에 바꾸지 않는다) | 결정(D-7) · 「글자 그대로」 는 제안(조사 §0-2 U-4 「대화 단위로 고정」) |
| CL4 | 안 쓰는 것: `--no-session-persistence`(뺌) · `--continue` · `--mcp-config` · `--max-budget-usd` · `--bare`(F8). `--json-schema` 는 보류 | 결정(D-7) |
| CL5 | 「도구 전부 막음」 = `--tools ""` + `--disallowedTools`(`cli.py:36` 의 목록) + `--strict-mcp-config`(MCP 설정을 주지 않으므로 MCP 0) + `--disable-slash-commands` + `--setting-sources ""`. stream-json 에 도구 호출이 보이면 그 턴은 오류로 닫는다(CL10) | 결정(D-7) · 검사는 제안 |
| CL6 | `<UUID>` = 앱이 대화를 시작할 때 만든 UUID4(F5 — 유효한 UUID 여야 한다). 대화 id(`conv_id`)와 **따로** 둔다 — 세션을 못 쓰게 됐을 때 대화 기록은 남기고 세션만 버릴 수 있게 | 결정(D-7 「앱 UUID」) · 따로 둠은 제안 |
| CL7 | stream-json 의 init 줄에서 세션 id · 모델 · 인증 종류를 읽는다 — 세션 id 가 준 값과 다르면 그 턴은 오류 · 구독이 아니면 멈춘다(`cli.py:164-167` 과 같은 검사) | 제안 |
| CL8 | F6 — **WORK 의 첫 걸음(E1)에서 `--max-turns 1` · `--system-prompt-file` 을 이 판 CLI 가 받는지 본다.** 안 받으면 구현하지 말고 코디에게 올린다(결정된 옵션이므로 워커가 바꾸지 않는다). 올릴 때 함께 적을 사실: `--system-prompt <글>` 은 지금 앱이 쓰는 꼴이다(`cli.py:80`) | 제안 |

### 3-3. cwd · 세션 파일

| # | 규칙 | 상태 |
|---|---|---|
| CL9 | 상담 실행기는 **고정 cwd 하나**에서 띄운다(`CHAT_CLI_CWD`) — 대화 · 턴이 달라도 같은 폴더 · 턴 뒤에 지우지 않는다(없으면 만든다 · 안은 비어 있다). 까닭: 세션 파일 자리가 cwd 에 매인다(F1). cwd 가 턴마다 달라도 이어진다는 것(F3)은 실측 전이므로 **거기에 기대지 않는다** | 제안 |
| CL9-1 | 고정 cwd 는 **레포 밖**이다(앱 레포 · 프로필 레포 · 허브 레포의 아래가 아니다) — CLI 가 위 폴더의 지침 파일을 찾아 올라가는 길을 닫는다. 시험 앱이 시스템 임시 폴더를 쓰는 것과 같은 까닭이다(`cli.py:5`) | 제안 |
| CL9-2 | 세션 파일(`~/.claude/projects/…`)은 사용자 홈의 CLI 자료다 — **앱이 지우지 않는다.** 보관 기간은 확인 안 됨(조사 §7-2). 대화 글이 그 파일에 평문으로 남는다는 것을 README 에 적는다 | 제안 |
| CL9-3 | 장부에는 세션 파일 경로를 적지 않는다(홈 경로) — 세션 id 와 cwd 설정 이름만 | 제안 |

### 3-4. session_id 수명

| 상태 | 뜻 | 다음 턴 |
|---|---|---|
| `new` | UUID 를 만들었고 아직 성공한 턴이 없다 | `--session-id <UUID>` |
| `open` | 성공한 턴이 하나 이상 | `--resume <UUID>` |
| `broken` | 이 세션을 더는 믿지 않는다 | 띄우지 않는다(CL10) |

| # | 규칙 | 상태 |
|---|---|---|
| CL10 | **실패 처리** — ① `new` 에서 실패(인증 · 종료 코드 · 시간 초과 · 도구 호출 보임): 그 UUID 를 버리고 **새 UUID** 로 `new` 그대로(같은 UUID 를 다시 `--session-id` 로 주지 않는다 — 반쯤 쓰인 세션 파일이 있을 수 있다) ② `open` 에서 답이 끝나기 전에 실패(시간 초과 · 중단 · 종료 코드): 세션 `broken` — 세션 파일에 답 없는 질문이 남았을 수 있고 그 뒤 `--resume` 의 동작은 **확인 안 됨** ③ `open` 에서 띄우기 전 실패(인증 · 줄 서기 중 취소): 세션은 `open` 그대로 · 그 턴만 오류 | 제안 |
| CL10-1 | `broken` 대화는 **끝난 대화**다 — 그 턴은 오류로 장부에 남고 화면은 새 대화를 시작하는 길만 연다(문구는 빈 자리). 장부로 새 세션을 다시 세우는 길(앞 턴의 메시지 · 답을 새 세션에 다시 싣기)은 SDK 경계와 같은 꼴이라 이 판에서 하지 않는다 — **사용자 결정 U-11** | 제안 |
| CL11 | 시간 한도 = `CHAT_TURN_TIMEOUT_SEC`. 넘으면 프로세스 그룹째 끝낸다(`run_cli` 가 이미 그렇게 한다 — `cli_process.py:83-97`) | 제안 |
| CL12 | **동시 한도** — ① 한 대화에 한 번에 한 턴(대화마다 잠금 — 같은 세션 파일을 두 프로세스가 쓰지 않게. 앞 턴이 도는 중에 온 턴은 받지 않고 오류 조각) ② 앱 전체 CLI 동시 수 = `CLI_MAX_CONCURRENT`(세마포어 — `cli.py:291-298` 꼴). 줄 서는 중이면 `step` 이벤트로 알린다 | 제안 |
| CL13 | 한 대화의 턴 수가 `CHAT_MAX_TURNS` 에 닿으면 그 대화는 더 받지 않는다(새 대화). 까닭: 재료가 턴마다 쌓여 입력이 자란다(조사 §1-2 (가) — 한 턴 중앙 13,247 토큰) · CLI 가 긴 대화를 압축하면 시스템 프롬프트 기록 · 앞 재료가 어떻게 되는지 **확인 안 됨**(F7) | 제안 · 값은 임시 |
| CL14 | 대화가 시작될 때의 허브 `build.gold_hash` 를 장부에 적는다. 뒤 턴의 허브 응답 `build` 가 다르면 그 대화는 끝난 대화다(앞 턴 재료의 줄이 다른 판의 것) | 제안 |

### 3-5. 결과 꼴

상담 실행기의 결과는 지금 `cli.run` 의 결과(`cli.py:100-104` `new_result`)에서 상담에 필요한 것만 든다.

| 칸 | 뜻 |
|---|---|
| `answer_raw` | CLI 가 낸 답 그대로(꼬리째) |
| `error` | `null` 또는 `{kind, stage, detail}` |
| `tokens` | `input_tokens` · `output_tokens` · `cache_creation_input_tokens` · `cache_read_input_tokens`(`cli.py:38` `USAGE_KEYS`) |
| `observed_model` · `observed_models` | init 줄 · result 줄의 모델(대체 모델로 넘어갔는지 여기서 본다) |
| `thinking_seen` | 추론 블록이 보였나 |
| `stop_reason` · `timing{ttft_ms, total_ms}` | 그대로 |
| `llm{kind: "cli", session_id, mode: "new" \| "resume", model, effort, cli_version, returncode}` | 이 턴을 어떻게 띄웠나 |

### 3-6. SDK 로 갈아 끼울 경계

| # | 규칙 | 상태 |
|---|---|---|
| SD1 | 한 턴 흐름(§4-2)은 `clinic_chat/llm/chat.py` 의 **인터페이스 하나**만 부른다: 「대화 상태 · 이번 턴 user 메시지 · 시스템 지시 파일 → §3-5 결과」 + 글자 조각은 `progress.emit("delta")`. CLI 구현(`chat_cli.py`)만 이 판에서 짓는다 | 결정(D-4 「갈아 끼울 자리만」) · 꼴은 제안 |
| SD2 | 인터페이스는 **앞 대화를 받는 인자를 가진다**(장부의 앞 턴 user 메시지 · 답 목록). CLI 구현은 그 인자를 쓰지 않는다(세션이 들고 있다) · SDK 구현은 그것을 `messages` 로 보낸다(조사 §1-1 「서버에 기억이 없다」) | 제안 |
| SD3 | 그래서 장부는 **이 판부터** 턴마다 「LLM 에 실은 user 메시지 글자 그대로」 와 「답 꼬리째」 를 남긴다(§5-1 LG3) — SDK 로 바꿀 때 장부 꼴이 안 바뀐다. 조사 §1-2: 앞부분이 글자 그대로 같아야 캐시가 선다 | 제안 |
| SD4 | 대화에 남는 답 = **꼬리째**다. CLI 세션은 낸 답을 그대로 들고 있어 고를 수 없다 — SDK 때도 같은 꼴로 맞춘다(조사 §1-2 「한 가지로 고정」) | 제안 |
| SD5 | API 키 · `anthropic` 의존 · 캐시 표시 자리 · 추론 설정은 이 판에서 정하지 않는다(O-4). CLI 자식에게는 키 env 를 계속 지운다(`cli_process.py:20-26`) | 결정(D-22) |

## 4. 한 턴 흐름

### 4-1. 라우트(경로 이름은 제안 — C-11)

| 라우트 | 무엇 | 돌려주는 것 |
|---|---|---|
| `GET /` | 새 대화 화면 — `conv_id` 를 만들고 세 칸의 빈 틀을 그린다 | HTML 한 장 |
| `GET /c/{conv_id}` | 그 대화 화면 — 장부의 턴들(질문 · 답 본문)과 마지막 리스트 · 점을 다시 그린다 | HTML 한 장 |
| `POST /c/{conv_id}/turns` | 폼 `text` — 턴을 띄운다 | HTML 조각: 내 말풍선 + 빈 답 말풍선(이 턴의 SSE 에 붙는 자리) |
| `GET /c/{conv_id}/turns/{n}/events` | 그 턴의 SSE(§4-3) | `text/event-stream` — 자료는 HTML 조각 |
| `GET /face-check` | 좌표 확인용 — 좌표표의 점을 전부 켠 얼굴 한 장(§8-4) | HTML 한 장 |
| `GET /static/…` | htmx 파일 · CSS | 파일 |

- JSON 을 내는 라우트는 없다(화면은 조각만 받는다 — D-1). 기록을 보는 길은 장부 파일이다(§5-1).
- 늦게 붙거나 끊겼다 다시 붙은 구독자는 처음부터 / 받은 번호 다음부터 받는다 — 시험 화면의 `Live` · `resume_from`(`$A/clinic_chat/web/server.py:52-64` · `:89-95`) 꼴을 따른다.

### 4-2. 단계

| # | 단계 | 무엇 | 근거 |
|---|---|---|---|
| TF1 | 받기 | 글이 비었거나 대화가 `broken` · 턴 한도(CL13) · 앞 턴이 도는 중(CL12)이면 오류 조각. 아니면 턴 번호를 매기고 `POST` 가 곧바로 「내 말풍선 + 빈 답 말풍선」 을 돌려준다 | 조사 §4-3 「한 턴의 꼴」 1 |
| TF2 | 걷기 | `walk(question, deps, carry=…)` — 단계 ① 맨 앞 판단(resolve · coverage · Jev 한 요청) → ② 허브 폭 → ③ 깊이 → ④ 재료 · 틀린 말 검사 → 종료 상태. **시험 앱 B 와 같은 함수**다(ST2). 이어 묻기의 앞 턴 대상만 `carry` 로 더 준다(§5-2) | D-9 · `col_b.py:161-225` |
| TF3 | 리스트 · 부위 | 걷기가 끝나면(LLM 을 기다리지 않고) 앱이 읽은 `concern_candidates` 응답으로 시술 리스트(§6-1)와 부위(§6-2)를 짓고 **`list` · `sites` 이벤트를 먼저 보낸다** | 지시서 「리스트 · 점은 LLM 전에」 · 조사 §5-1 |
| TF4 | 재료 | 이번 턴에 **새로 읽은 줄만** 턴 메시지로 짓는다(§5-3) — 앱 판정(JSON) → 자료 → 질문 순서(`col_b.py:272-283` `prompt_pages` 와 같은 순서 · 질문이 맨 뒤) | D-10 · 조사 §1-2 |
| TF5 | LLM | §3 의 실행기 한 번. 글자 조각은 꼬리 표식 앞까지만 `delta` 이벤트로 흘린다(`_TailFilter`) | D-16 |
| TF6 | 맺기 | 답에서 꼬리를 떼고(`split_tail` — `col_b.py:286-304`) 본문만 `done` 이벤트로 말풍선에 넣는다 · 장부에 한 줄 쓴다(§5-1) · 세션 상태를 옮긴다(§3-4) | D-8 · D-16 |

- 걷기 안의 허브 · Jev 오류는 시험 앱과 같이 「실행 중단」 으로 끝나고(`col_b.py:210-217`), **그 상태에서도 TF5 를 부른다** — 입력 = 종료 상태 + 사유 코드 + 빈 재료(`col_b.py:7` · `_RESUME` §2 11-16 「WORK 검수 뒤(코디)」 W2-1). 앱이 대신 문장을 짓지 않는다(ST4).
- 「범위 밖」 · 「입구 없음」 · 「실행 중단」 에서는 `list` · `sites` 를 보내지 않는다(왼쪽 칸은 앞 턴 것 그대로).
- 시간 어림(조사 §5-1 — 실측 아님): 걷기 끝까지 약 0.5 ~ 0.7초(v06 중앙 Jev 424ms · 허브 72ms) → 리스트 · 점 → 첫 글자 약 2.3초.

### 4-3. 이벤트

SSE 한 줄기(턴 하나)에 아래 이벤트가 차례로 온다. `id:` = 이벤트 번호(다시 붙기용).

| 이벤트 | 언제 | 자료(HTML 조각) | 받는 자리(id — 제안) |
|---|---|---|---|
| `step` | 단계가 바뀔 때(걷기의 `progress.emit("step")` — `col_b.py:167` · `:179` · `:193` · `:198` + LLM 줄 서기 · 시작) | 단계 코드만 든 빈 표시(`data-step`) — 글 없음 | 이 턴 답 말풍선의 상태 자리 |
| `list` | TF3 | 시술 리스트 조각 통째(§6-1) | `#procedure-list` |
| `sites` | TF3 | 얼굴 점 층 + 얼굴 아래 라벨 조각 통째(§6-2) | `#face-marks` |
| `delta` | TF5 — 글자 조각마다 | HTML 이스케이프한 글자 | 이 턴 답 말풍선 본문 **끝에 덧붙임** |
| `done` | TF6 | 답 본문 조각 통째(꼬리 없음) · 종료 상태 코드(`data-end-state`) | 이 턴 답 말풍선 본문 **통째 바꿈** · 줄기를 닫는다 |
| `error` | 어느 단계든 턴이 못 끝났을 때 | 오류 종류 코드만 든 빈 표시(`data-error`) | 이 턴 답 말풍선 · 줄기를 닫는다 |

| # | 규칙 | 상태 |
|---|---|---|
| EV1 | 순서: `list` · `sites` 는 **첫 `delta` 보다 먼저**다(둘 사이 순서는 `list` → `sites`) · `done` 또는 `error` 가 마지막이고 둘 중 하나만 온다 | 결정(지시서) |
| EV2 | 조각 셋(리스트 · 점 · 말풍선)을 한 줄기에서 갈아 끼우는 htmx 길은 둘이다 — (가) 이벤트 이름마다 받는 자리를 두는 길(SSE 확장의 이벤트 이름 맞춤) (나) 조각 안의 자리 밖 바꾸기(`hx-swap-oob`). **어느 쪽이 서는지는 조사가 확인하지 않았다**(조사 §4-3 「확인 안 됨」 ①) — WP-0 의 빈 화면 확인(E0)에서 정한다. 이 스펙이 고정하는 것은 **이벤트 이름 · 조각 · 받는 자리 id** 까지다 | 제안 |
| EV3 | 점은 SVG 안 요소를 낱개로 갈아 끼우지 않고 **`#face-marks` 통째**로 바꾼다 — SVG 안 요소를 조각으로 갈아 끼울 때 제대로 그려지는지 확인 안 됨(조사 §4-3 ②). E0 에서 통째 바꾸기가 서는지 본다 | 제안 |
| EV4 | 글자 조각 · 이름 · 값은 전부 HTML 이스케이프해서 보낸다(Jinja2 자동 이스케이프 켬 — 답에 `<` 가 올 수 있다 · 조사 §4-3) | 결정(D-3 의 까닭) |
| EV5 | `delta` 는 **이어 붙이기 전용**이다 — 받은 뒤 `done` 이 본문을 통째 바꾸므로 다시 붙은 구독자가 조각을 놓쳐도 끝 꼴은 같다 | 제안 |

### 4-4. 근거 꼬리

- 답 꼬리(`<<<근거>>>` 뒤 「답 줄: 재료 줄 번호」 — `col_b.py:42-43`)는 상담에서도 LLM 이 쓴다(D-16). 앱은 떼어 장부 `answer_lines[]` 로 남기고, **화면에는 표식 뒤를 한 글자도 흘리지 않는다**(`delta` 는 `_TailFilter` · `done` 은 `split_tail` 의 본문).
- 꼬리가 없거나 꼴이 깨졌으면 답은 그대로이고 `answer_lines` = `null` 이다(`col_b.py:8-9` 와 같음). 화면은 달라지지 않는다.
- 줄 번호는 **대화 전체에서 이어진다**(§5-3 AP2) — 꼬리가 앞 턴에 실은 줄 번호를 가리켜도 장부에서 gid 로 되짚힌다.

### 4-5. 화면 문구 — 빈 자리

앱 · 템플릿은 사람에게 보일 문장을 갖지 않는다(D-17). 템플릿에는 **자리와 값만** 있다. 자리마다 `data-slot` 이름을 달아 사용자가 채울 곳을 센다.

| 자리(`data-slot`) | 무엇이 들어갈 곳 |
|---|---|
| `page-title` | 화면 제목 |
| `face-title` · `list-title` · `chat-title` | 세 칸의 제목 |
| `input-placeholder` · `send-label` | 입력칸 안내 · 보내기 단추 글 |
| `list-empty` · `face-empty` | 리스트 · 점이 없을 때 |
| `list-section-modality-only` · `list-section-unreached` | 리스트의 두 따로 묶음 머리(§6-1 PL5) |
| `label-area-title` | 얼굴 아래 라벨 줄의 머리 |
| `step-<코드>` | 단계 표시 글(걷는 중 · 답 쓰는 중 …) |
| `error-<종류>` | 오류 글 · 새 대화를 여는 길의 글 |
| `turn-limit` | 턴 한도에 닿았을 때 |

- 값으로 그리는 것(문구가 아니다): 시술 이름 · 계열 이름 · 층 값(`reach` 의 gold 값 그대로) · 부위 이름 · 내 질문 · LLM 답.
- 빈 자리는 비어 보이는 그대로 둔다(자리 이름을 화면에 찍지 않는다 — 확인용 화면 `/face-check` 만 코드 값을 보인다).

## 5. 장부 · 이어 묻기 · 재료 덧붙이기

### 5-1. 대화 장부

| # | 규칙 | 상태 |
|---|---|---|
| LG1 | 장부 = 앱 메모리(`conv_id` → 대화) + 파일. 턴 하나가 끝나면(성공 · 오류 모두) **한 줄**을 덧붙인다 · 쓴 줄은 고치지 않는다(`runs.py:1` 과 같은 규칙) | 결정(D-8) |
| LG2 | 파일 = `CHAT_DIR/turns.jsonl`(한 파일 · 대화가 섞여 있다 — `conv_id` · `turn` 으로 가린다). 시험 기록 `runs.jsonl` 과 **섞지 않는다**(꼴이 다르다 — 질문 하나가 아니라 턴 하나) | 제안 |
| LG3 | 한 줄의 칸은 아래 표다. 결정된 여섯(턴 · session_id · 고른 대상 · 읽은 재료 id · 답 · 시간)은 굵게 | 결정(굵은 것) · 나머지는 제안 |
| LG4 | 서버를 다시 띄운 뒤 같은 `conv_id` 로 오면 파일에서 그 대화의 줄을 되읽어 메모리를 세운다(세션 파일은 디스크에 그대로다 — F1). 마지막 줄이 오류로 끝난 대화는 §3-4 의 상태를 그 줄에서 읽는다 | 제안(조사 §1-5 「파일에서 되읽어야」) |
| LG5 | 장부에는 키 · 홈 경로 · 세션 파일 경로를 적지 않는다(CL9-3). 질문 · 답 원문은 적는다(로컬 · gitignore) | 제안 |

| 칸 | 뜻 |
|---|---|
| `conv_id` · **`turn`** · `asked_at` | 대화 · 턴 번호(1 부터) · 시각 |
| `question` | 이번 턴 글 그대로 |
| **`llm.session_id`** · `llm.mode` · `llm.model` · `llm.effort` · `llm.observed_model` · `llm.cli_version` | §3-5 |
| `session_state` | 이 턴 뒤의 `new` · `open` · `broken` |
| **`targets[]`** | 고른 대상 — `{table, code, name, by}`(`by` = `target` · `named` · `uncertain_kept` · `noul` · `carried`) |
| `carried[]` | 이번 턴에 후보로 넣은 앞 턴 대상 — `{table, code, from_turn, noul, decision}`(§5-2) |
| `kinds[]` · `end_state` · `reason` | 읽은 정보 종류 · 종료 상태 · 사유 코드 |
| `trace` | 시험 앱 B 의 trace 그대로(`col_b.py:378-401` `b_trace` — `front` · `entry` · `breadth` · `visited` · `gates` …) |
| **`material.new_lines[]`** | 이번 턴에 새로 실은 줄 — `{n, gid, gold_table, silver_table, silver_id, evidence_kind, kind, range, layer}`(`walk/material.py:184` 의 줄 꼴) 또는 목록 요약 줄 `{n, summary: true, gids[]}`(§5-3 AP4) |
| `material.seen_lines[]` | 이번 턴 조회가 다시 읽었지만 앞 턴에 이미 실은 줄 번호 |
| `material.next_n` | 다음 턴의 줄 번호 시작 |
| `list` | 이번 턴 리스트(§6-1) — 보냈으면 그 자료 · 안 보냈으면 `null` |
| `sites` | 이번 턴 점 · 라벨(§6-2) — 같은 꼴 |
| `llm_user_message` | LLM 에 실은 user 메시지 **글자 그대로**(SD3) |
| **`answer`** · `answer_raw` · `answer_lines` | 꼬리 뗀 본문 · 꼬리째 · 꼬리에서 읽은 「답 줄 ↔ 재료 줄」 |
| **`timing`** | `first_list_ms`(누른 뒤 → `list` 보냄) · `ttft_ms`(누른 뒤 → 첫 `delta`) · `total_ms` · `parts{jev_ms, hub_ms, llm_ms}` |
| `tokens` · `thinking_seen` | §3-5 |
| `build` · `prompts{consult, jev_front}` · `commits{app}` | 허브 `gold_hash` · 프롬프트 파일 sha256 · 앱 커밋 |
| `error` | `null` 또는 `{kind, stage, detail}` |

### 5-2. 이어 묻기 — 앞 턴 대상을 Jev 후보에

지금 단계 ① 의 대상 후보는 **이번 글에서 글자로 맞은 것뿐**이다(`$A/clinic_chat/walk/front.py:203-216` · SPEC-002 §3-1 CD1). 앞 턴을 이어 가리키는 글(「그중 …」)은 글자만으로 앞 턴 맥락이 안 잡힌다(조사 §5-2).

| # | 규칙 | 상태 |
|---|---|---|
| CR1 | **든 후보** = 장부에서 「대상이 있는」 가장 가까운 앞 턴 `CHAT_CARRY_TURNS` 개의 `targets[]`. 종료 상태가 「범위 밖」 · 「입구 없음」 · 「실행 중단」 인 턴은 건너뛴다 | 결정(D-20) · 몇 턴인지는 제안 |
| CR2 | `walk()` · `front()` 에 선택 인자 `carry`(기본 없음 = 지금 동작)를 더한다. `front()` 는 resolve 후보 **뒤에** 든 후보를 붙여 한 번에 묻는다 — coverage 도 함께(Jev 호출 수가 늘지 않는다 · `front.py:217-228`). 이번 글에서 이미 맞은 것과 같은 (표, 코드)는 든 후보로 다시 넣지 않는다 | 제안 |
| CR3 | Jev 에 주는 후보 설명에서 든 후보는 `matched` = `null` · `carried_from` = 앞 턴 번호다(「이번 글에 글자로 없다 · 앞 턴의 대상이다」 를 Jev 가 알게) | 제안 |
| CR4 | **든 후보는 Jev 가 yes 일 때만 대상이다** — 사이 값 · no 는 뺀다(`carried[].decision` = `dropped`). 「글에 통째로 든 이름은 점수와 무관하게 대상」(TG3)과 「사이 값은 넘김」(TG2)은 **글에 있는 이름의 규칙**이라 든 후보에 걸지 않는다 — 덮인 조각을 yes 일 때만 대상으로 하는 것(`front.py:306-307`)과 같은 꼴 | 제안(`_RESUME` §2 11-17 「덮인 조각 규칙」 의 꼴을 따름) |
| CR5 | 든 후보로 대상이 된 것은 `targets[].by` = `carried` · `read_as{by: "carry", from_turn}` 이다 — 재료 표지로 LLM 에 가서 답이 「앞에서 말한 그 대상으로 읽었다」 를 밝힐 수 있다(공통 지시 9 번의 재료) | 제안 |
| CR6 | 이번 글에 후보가 0 이고 든 후보만 있을 때: 든 후보를 후보로 삼아 같은 요청을 한다(입구 고르기 TG4 는 든 후보도 0 일 때만). 든 후보가 전부 `dropped` 면 지금의 입구 고르기 길로 간다 | 제안 |
| CR7 | 상담용 Jev 지시는 시험 것(`prompts/jev/front.md`)을 고치지 않고 **따로 둔다**(§7-2) — 든 후보를 읽는 법 한 줄이 더 든다. 시험 프롬프트의 확인 기록(sha — `prompts.py:76-90`)이 깨지지 않게 | 제안 |

- **이 판이 하지 않는 것**: 앞 턴 **리스트의 후보**(시술 수십 개)를 후보에 넣어 「그중 필러」 를 「그 고민의 리스트에 있던 필러 계열 시술」 로 좁히는 것. 조사 §5-2 는 이것이 없으면 「필러 전체의 효과 기간」 을 답하게 된다고 적었다. 좁히는 규칙(앞 턴 리스트 ∩ 이번 대상)은 「짧게 → 깊게」 의 단계와 한 몸이라 상담 플로우(0.2)에서 정한다 — **사용자 결정 U-12**.

### 5-3. 재료 덧붙이기

| # | 규칙 | 상태 |
|---|---|---|
| AP1 | 턴 메시지에는 **이번 턴에 새로 읽은 행만** 싣는다. 대화가 이미 실은 행(gid)은 다시 싣지 않는다 — 대화마다 「실은 gid → 줄 번호」 장부를 든다 | 결정(D-10) |
| AP2 | 줄 번호 `n` 은 **대화 전체에서 이어진다**(1 턴 1 ~ k → 2 턴 k+1 ~). 지금은 한 질문 안에서 1 부터다(`walk/material.py:167` `enumerate(…, 1)`) — `build()` 에 시작 번호 선택 인자(기본 1 = 지금 동작)를 더한다 | 제안(조사 §1-2 「줄 번호를 대화 전체에서 이어 붙여야」) |
| AP3 | 이번 턴 조회가 **다시 읽은 앞 턴 줄**은 줄 번호만 「앱 판정」 의 `seen_lines[]` 로 준다(칸을 다시 싣지 않는다) — LLM 이 앞 대화의 어느 줄이 이번 질문의 재료인지 안다. 표지가 달라졌어도(예: 좁힌 조회의 표지) 다시 싣지 않는다 — 장부에만 남는 한계다 | 제안 |
| AP4 | **고민 → 리스트 턴의 `concern_candidates` 행**은 줄마다 싣지 않고 **목록 요약 줄**로 싣는다: 계열 하나에 한 줄 `{n, 계열 이름, 시술 수, 층 값들(reach), 고민 맞춤 값들(concern_match), 원리 이름들(mechanism_name)}` + 머리에 윗고민에서 물려받았는지(`inherited_from`). 시술 이름 줄은 **싣지 않는다** — 리스트가 화면에 전부 있고, 없는 것은 답이 읊지 못한다 | 기본값 C-3(조사 §2-3 「② 가 더 단단하다」) · 요약 줄의 칸은 제안 |
| AP5 | 요약 줄도 줄 번호를 갖고 장부에 `gids[]`(그 계열 묶음의 행 gid 전부)를 남긴다 — 답 꼬리 → 요약 줄 → gid → `g_evidence` → silver → `source_ref` 로 근거 되짚기가 그대로 선다 | 제안 |
| AP6 | AP4 는 SPEC-002 §3-6 FT2(「종류마다 싣는 칸 고정」)를 **상담에서만** 바꾸는 것이다(조사 §2-2 끝 줄). 그 밖의 종류 · 턴은 SPEC-002 §3-2a 「LLM 에 싣는 칸」 그대로다 — 틀린 말 막기에 필요한 칸 · 표지도 그대로 간다 | 제안 |
| AP7 | 「이름 목록」(SPEC-002 §3-7-1 CP2 · FT8)은 상담 재료에 **싣지 않고** `answer_check` 도 돌리지 않는다 — 「목록을 줄이지 않는다」 는 시험 전용이다(`_RESUME` §2 11-17 「테스트 답은 빠짐없이」 · 조사 §2-1) | 제안 |
| AP8 | 쪽 나눔(FT4)은 이 판에서 하지 않는다 — 한 턴 메시지가 `ANSWER_INPUT_MAX_TOKENS` 를 넘으면 「실행 중단」(사유 `FT5` — `col_b.py:419-422` 와 같은 길). 한 세션에 쪽마다 따로 물을 수 없다(`--max-turns 1` · 답이 대화에 쌓인다) | 제안 |

- 「앱 판정」 은 지금 꼴(`col_b.py:252-269` `judgement`)에 `seen_lines[]` · `turn` 을 더한 JSON 이다. `offered`(더 볼 수 있는 정보)는 그대로 간다 — 「필요할 때 깊게」 의 되묻기 재료다(조사 §2-1 `col_b.md` 7 번).

## 6. 시술 리스트 · 부위

### 6-1. 시술 리스트(앱 결정론)

| # | 규칙 | 상태 |
|---|---|---|
| PL1 | 리스트는 이번 턴 걷기가 읽은 **`concern_candidates` 응답**(목적 `read` 인 조회)으로만 짓는다. LLM 답 · Jev 점수는 리스트에 닿지 않는다 | 결정(D-11) |
| PL2 | 행 = 시술 하나(`groups[]` 의 `procedure_code` 로 묶음 — 후보가 케이스 · 제품이어도 **시술 이름**으로 · 공통 지시 7 번). 행의 값: `procedure_name` · 층 = 그 시술 묶음들의 `reach[]` 합집합(gold 값 그대로) · `concern_match[]` 합집합(「직접」 · 「하위 고민」) | 결정(D-11) · 조사 §2-3 |
| PL3 | 계열 묶음 = 후보별 profile 의 `modality_name`(걷기가 이미 읽는다 — SPEC-002 §3-2a `indication` 행 「후보마다 `facets` profile」). 계열 이름이 빈 시술은 빈 계열 묶음 하나에 모은다(이름을 지어 붙이지 않는다) | 결정(D-11) |
| PL4 | 순서 = 허브가 낸 순서(묶음의 첫 행 gid — SPEC-001 §4-5) 그대로: 계열은 처음 나온 순서 · 계열 안 시술도 처음 나온 순서. 앱이 순위를 매기지 않는다(공통 지시 8 번) | 제안 |
| PL5 | `modality_only[]`(「계열 층만」)와 `unreached[]` 는 **시술 행에 섞지 않고**(SPEC-001 §4-5) 리스트 아래 **따로 묶음 둘**로 그린다 — 「계열 층만」 = 계열 이름 · 「그 밖」 = `candidate_name` + `reach`. 버리지 않는다(「폭은 빠짐없이」) — **사용자 결정 U-13** | 제안 |
| PL6 | 윗고민에서 물려받은 응답(`inherited_from` ≠ `null` — SPEC-001 §5-9 HG1)이면 리스트 머리에 「어느 고민의 것인가」 를 값으로 단다(윗고민 이름 · 몇 단 위) | 제안 |
| PL7 | 고민 대상이 둘 이상이면 고민마다 리스트 하나(머리 = 고민 이름) · 한 조각에 차례로 | 제안 |
| PL8 | 이번 턴에 `concern_candidates` 를 읽지 않았으면 `list` 이벤트를 **보내지 않는다** — 왼쪽 아래 칸은 가장 최근 리스트 그대로다. 상세 턴에서 그 칸을 무엇으로 쓸지는 U-10(0.2) | 제안 |
| PL9 | 리스트 행에는 `data-procedure-code` 를 단다(0.2 의 「시술을 눌렀을 때」 가 걸릴 자리) — 이 판에서 누르는 동작은 없다 | 제안 |

- 장부 `list` = `{concerns: [{concern_code, concern_name, inherited_from, modalities: [{modality_name, procedures: [{procedure_code, procedure_name, reach[], concern_match[], gids[]}]}], modality_only: [{modality_name, gids[]}], unreached: [{candidate_name, reach, gid}], counts}]}` — 리스트의 모든 행이 gid 로 되짚힌다.
- 미리 본 값(조사 §5-1 — 허브를 부르지 않고 CSV 로 셈): 고민 하나에서 행 74 → 후보 묶음 37 · 시술 15 · 「계열 층만」 7 · 못 닿음 2.

### 6-2. 부위 → 점 · 라벨

| # | 규칙 | 상태 |
|---|---|---|
| SI1 | 점의 재료 = 허브가 `concern_candidates` 응답 머리에 내는 **고민 부위 코드 목록**(§6-3). 앱은 silver CSV 를 직접 읽지 않는다(DB 판에서 못 쓰는 길 — 조사 §0-2 C-5) | 결정(D-14 · D-19) |
| SI2 | 모으는 고민 = 물은 고민 + **읽은 행의 `concern_code`**(하위 고민으로 펼쳐진 행 — 대분류는 자기 부위가 없고 하위 소분류가 부위를 가진다 · 조사 §3-4) | 제안 |
| SI3 | 부위 코드 하나를 좌표표(§8-2)에서 찾아: `point` → 점 하나 · `pair` → 점 둘 · `area` · `line` · `none` · **표에 없는 코드**(몸 부위) → 얼굴 아래 라벨(부위 이름 = 허브가 낸 값) | 결정(D-12 · D-13) |
| SI4 | 같은 부위가 여러 고민에서 나와도 점 · 라벨은 한 번 | 제안 |
| SI5 | 부위가 0 이면 빈 `sites` 조각을 보낸다(앞 턴 점을 지운다) — 리스트는 이번 고민 것인데 점만 앞 고민 것으로 남지 않게. 부위 없는 고민이 많다(260 가운데 175 — 조사 §3-4) | 제안 |
| SI6 | 점에는 `data-site-code` 를 단다(확인 · 0.2 용). 점 옆에 글을 그리지 않는다 | 제안 |
| SI7 | 질문에 든 부위 이름(resolve 의 부위 후보) · 시술 쪽 부위(케이스 · 상품)는 **이 판의 점 재료가 아니다** — 점 기준은 고민 부위 하나다(D-14). 시술을 눌렀을 때의 부위는 U-5(0.2) | 결정(D-14 · D-18) |

- 장부 `sites` = `{dots: [{site_code, shape, concern_codes[], csi_ids[]}], labels: [{site_code, site_name, why: "area" | "line" | "none" | "off_face"}]}`.

### 6-3. 허브에 필요한 것(계약은 SPEC-001 0.7 이 닫는다)

지금 허브는 고민 → 부위 코드를 어느 응답에도 내지 않는다 — `sites_of_concern` 은 저장소에 있고(`$H/backend/app/modules/gold/repository.py:217-219`) 부르는 곳이 없다(조사 §3-4). 이 스펙은 「`concern_candidates` 응답 머리에 고민 부위 코드 목록이 온다」 고 **가정**하고, 필요만 적는다. 칸 이름 · 꼴은 SPEC-001 0.7 이 정한다.

| # | 필요 |
|---|---|
| HN1 | 응답 머리에 (고민 코드, 부위 코드) 쌍의 목록 — 물은 고민과, **응답 행에 나오는 `concern_code`**(하위 고민) 전부에 대해 |
| HN2 | 쌍마다 부위 이름과 묶임 id(`concern_site.id`) — 라벨에 이름을 쓰고, 점을 silver 행으로 되짚는다 |
| HN3 | 물은 고민의 행이 0 이어도(윗고민 행을 물려받은 응답 — HG1) **물은 고민 자신의 부위**는 낸다 |
| HN4 | `site` 거르개 · 쪽 넘김과 무관하게 같은 목록(머리 값 — 첫 쪽에) |

- 허브 0.7 이 서기 전에는 `sites` 가 빈 꼴이다(점 0 · 라벨 0). 앱이 다른 길(이름이 같은 넷 · `case_site_name` 글자)로 메우지 않는다 — 조사 §3-4 「일반 고민은 지금 계약으로 못 닿는다」.
- 앱 단위 시험은 가짜 허브(`$A/tests/fake_hub.py`)에 그 머리 칸을 실어 돈다 — 칸 이름은 0.7 이 정한 뒤 맞춘다(WORK 순서 = SPEC-001 0.7 → 이 스펙의 부위 WP).

## 7. 상담 프롬프트 기반

문구 확정은 사용자다(C-1 — `_RESUME` §2 11-17 「답 프롬프트 확정(C-1)은 채팅(상담) 단계로 넘김」). 이 스펙은 **파일 자리와 뼈대**까지만 정하고 문장을 쓰지 않는다. 구현은 초안 파일로 하고 e2e 때 사용자가 고친다.

### 7-1. 시험 프롬프트에서 남길 것 · 뺄 것(조사 §2-1 그대로)

| 시험 파일 | 남김 | 고침 | 뺌 |
|---|---|---|---|
| `prompts/common.md` | 1(자료에 있는 것만) · 2(id · 코드 안 넣음) · 3(틀린 말 일곱 줄) · 4(종료 상태 구분) · 5 앞(다루지 않는 것) · 6 앞(묻지 않은 것 안 붙임) · 7(시술 이름 · 층) · 8(우열 안 함) · 9(어느 개념으로 읽었나) · 10(모범 답 꼴 + 「짧게」 를 되살림) · 11(층 밝힘) | 역할 줄(질문 하나 → 여러 턴 상담) · 5 뒤(「각각 빠짐없이」 → 각각 말하되 깊이는 단계대로) · 6 뒤(「그 폭을 빠짐없이」 → 긴 목록 자리는 U-10) | 12(목록을 줄이지 않는다) |
| `prompts/col_b.md` | 3(자료 꼴 + 「여러 턴에 걸쳐 자료가 온다」 를 더함) · 4(표지) · 5 의 「목록에 있다고 값을 지어 말하지 않는다」 · 6(0.6 표지) · 7(`offered` = 되묻기 재료) · 8 ~ 14(종료 상태별) · 15(`scope_gap`) · 18(답 꼬리 — D-16) | — | 5 의 「`value` 는 전부 답에」(이름 목록을 안 싣는다 — AP7) |
| `prompts/judge.md` | — | — | 전부(채점 지시) |

### 7-2. 파일 자리(제안)

| 파일 | 무엇 | 누가 읽나 |
|---|---|---|
| `prompts/consult/system.md` | 상담 지시 — 대화 내내 **글자 그대로 고정** | CLI `--system-prompt-file`(CL2) |
| `prompts/consult/jev_front.md` | 상담용 맨 앞 판단 지시(영어 — D10) = 시험 `prompts/jev/front.md` + 든 후보 읽는 법(CR7) | `walk.front`(상담일 때) |

- 시험 프롬프트 파일(`prompts/common.md` · `col_*.md` · `judge.md` · `jev/*.md`)은 **고치지 않는다** — 확인 기록 sha 와 18220 이 그대로다.
- 턴 메시지의 틀(「앱 판정」 · 「자료」 · 「질문」 머리)은 지금처럼 코드에 있다(`col_b.py:273-274`) — 사람에게 보일 문장이 아니다.

### 7-3. 뼈대(조사 §2-5)

| # | 규칙 | 상태 |
|---|---|---|
| PM1 | `system.md` 의 절: ① 역할 한 줄(여러 턴 상담) ② 규칙(§7-1 「남김」 · 「고침」) ③ 화면 규칙 — 「시술 목록은 화면에 있다 · 이름을 늘어놓지 않는다」 · 「짧게 · 물은 것만 · 되묻기로 끝」 ④ 자료 읽는 법(§7-1 `col_b.md` 「남김」 + 줄 번호가 대화 전체에서 이어짐 · `seen_lines` · 목록 요약 줄 읽는 법) ⑤ 답 꼬리 | 뼈대는 조사 §2-5 · 문구는 사용자 |
| PM2 | `system.md` 에 시각 · 대화 id · 세션 id · 사용자 정보를 넣지 않는다(대화마다 글자가 같아야 한다 — SDK 캐시 조건 · 조사 §1-2) | 제안 |
| PM3 | 대화가 시작될 때의 `system.md` sha256 을 장부에 적는다. 대화 도중 파일이 바뀌어도 그 대화는 첫 턴의 기록을 그대로 쓰는 것으로 읽힌다(F7 — help 글) — E1 에서 본다 | 제안 |
| PM4 | 리스트를 다시 읊지 않게 하는 손잡이는 둘 다 건다: 지시(PM1 ③)와 재료(AP4 — 이름 줄을 안 실음) | 기본값 C-3 |
| PM5 | 초안 파일 머리에 「초안 — 사용자 확인 전」 주석을 단다(`prompts/common.md:1` 과 같은 꼴). 상담 프롬프트의 확인 기록(sha 대조)은 이 판에서 만들지 않는다 | 제안 |

## 8. 얼굴 SVG · 좌표표

### 8-1. 그림

| # | 규칙 | 상태 |
|---|---|---|
| FC1 | 얼굴 = **손으로 새로 그린 SVG**(선 그림 · path). 밑그림 = 사용자 PNG `~/Downloads/미니멀 인체 해부학 삼면도.png` 의 왼쪽 패널 — **읽기만 · 레포에 두지 않는다**(PNG · 그것을 기계로 뽑은 것 모두) | 결정(D-12 · D-15) |
| FC2 | `viewBox` = `0 0 590 1060` — 밑그림 왼쪽 패널 안쪽의 크기(약 590 × 1060 — 조사 §3-1). 좌표표의 비율이 이 상자 기준이다 | 제안 |
| FC3 | 그림 파일 = `clinic_chat/consult/templates/_face.svg`(Jinja2 조각 — 선 그림 층 + 점 층 `#face-marks` 가 한 SVG 안). 선의 세부(눈동자 · 눈썹 결)는 줄인다(조사 §0-2 U-6 「위험」) | 제안 |
| FC4 | 민머리 정면 한 장이다 — 두피 · 정수리 · 헤어라인은 정면에 자리가 있고, 귀 뒤는 `site` 에 없다(조사 §3-2) | 사실 |

### 8-2. 좌표표

| # | 규칙 | 상태 |
|---|---|---|
| FC5 | 표 = 코드 안의 사전 `clinic_chat/consult/face_coords.py`: `site_code → {shape, points}` · `shape` ∈ `point` · `pair` · `area` · `line` · `none` · `points` = `[[x, y], …]`(0 ~ 1 · FC2 상자 기준 · `point` 1 개 · `pair` 2 개 · 나머지 0 개) | 결정(D-12) · 꼴은 조사 §3-3 |
| FC6 | 표에 **얼굴 · 머리 · 목 부위 60 을 전부** 적는다(분류 = 부록 B). 몸 부위 29 는 표에 넣지 않는다 — 「표에 없는 코드 = 얼굴 밖」(SI3) | 제안 |
| FC7 | 이 판에 좌표를 찍는 것 = `point` 17 + `pair` 27 = **44 부위**(점 71 개). 고민 부위로 지금 실제로 쓰이는 것은 그 가운데 25(`point` 11 · `pair` 14 — 재셈)지만, 시술 부위(U-5)가 열리면 다시 찍지 않게 한 번에 찍는다 | 제안 |
| FC8 | `area` 8 · `line` 4 · `none` 4 는 좌표 없이 **라벨**이다(D-13 「넓은 부위」). `line` 넷은 묶인 고민 · 케이스 · 상품이 전부 0 이라 이 판에서 그려질 일이 없다(부록 B) | 결정(D-13) · `line` 은 제안 |
| FC9 | 좌표표는 gold · silver 가 아니라 **앱의 화면 자료**다(그림에 묶인 값 — 조사 §3-3). 부위 이름은 표에 적지 않는다(이름은 허브가 낸 값) — 표의 주석으로만 | 제안 |
| FC10 | 시험: 표의 코드가 `SITE-` 꼴 · 60 개 · `shape` 별 수 = 17 · 27 · 8 · 4 · 4 · `points` 길이 = `shape` 와 맞음 · 값이 0 ~ 1 · `pair` 는 두 점이 좌우(x 가 0.5 양쪽) | 제안 |

### 8-3. 라벨

- 얼굴 아래 한 줄에 부위 이름을 값으로 늘어놓는다(D-13). 순서 = 허브가 낸 순서.
- 미리 본 수(재셈): 고민 부위 51 종 가운데 얼굴 쪽 31 = 점 25 + 라벨 6(`area` 5 · `none` 1) · 몸 20 = 전부 라벨. 「얼굴」 처럼 넓은 부위가 자주 나온다(조사 §0-2 U-8 「위험」) — 점이 안 뜨고 라벨만 뜨는 턴이 흔할 수 있다.

### 8-4. 누가 찍고 누가 확인하나

| 차례 | 누가 | 무엇 |
|---|---|---|
| 1 | 구현 워커 | 밑그림에 눈금을 얹어 보고 SVG 를 새로 그린다 · 44 부위 좌표 **초안**을 찍는다. 조사 §3-3 의 예 값은 「눈으로 어림한 값 — 찍은 값이 아니다」 이므로 그대로 쓰지 않는다 |
| 2 | 구현 워커 | `/face-check` — 점을 전부 켜고 점마다 부위 코드를 보이는 확인용 한 장(코드 값이므로 문구가 아니다) |
| 3 | 코디 | 18222 를 띄운다(워커는 서버 · 포트를 띄우지 않는다) |
| 4 | 사용자 | 화면에서 눈으로 본다 — 어긋난 부위 코드를 말한다 |
| 5 | 구현 워커 | 그 코드의 좌표만 고친다 |

## 9. 시험 · 실물 확인

### 9-1. 단위 시험(외부 호출 0 — 가짜 CLI · 가짜 허브 · 가짜 Jev)

시험 앱의 가짜들을 쓴다(`$A/tests/fake_cli/` · `fake_hub.py` · `fake_jev.py`).

| # | 무엇 | 기대 |
|---|---|---|
| T1 | 첫 턴 인자 | `--session-id <UUID4>` 가 있고 `--resume` · `--no-session-persistence` · `--continue` · `--mcp-config` · `--max-budget-usd` · `--bare` 가 없다 · CL2 의 나머지 인자가 전부 있다 |
| T2 | 둘째 턴 인자 | `--resume <같은 UUID>` · `--session-id` 없음 · 나머지 인자가 첫 턴과 글자 그대로 같다 |
| T3 | 세션 상태 | 성공 `new` → `open` · `new` 에서 실패하면 다음 시도의 UUID 가 다르다 · `open` 에서 답 중 실패하면 `broken` 이고 다음 턴을 띄우지 않는다(CL10) |
| T4 | 대화 잠금 | 같은 대화에 턴 둘이 겹치면 둘째는 오류 조각 · CLI 는 한 번만 뜬다(CL12) |
| T5 | 자식 env | 키 꼴 env 가 자식에게 없다(`child_env` — 지금 시험과 같은 검사) |
| T6 | 이벤트 순서 | `list` → `sites` → 첫 `delta` → `done`(EV1) · 「범위 밖」 턴에는 `list` · `sites` 가 없다 |
| T7 | 꼬리 숨김 | 표식이 조각 둘에 걸쳐 와도 `delta` · `done` 어디에도 표식 뒤 글이 없다 · 장부 `answer_lines` 는 있다 |
| T8 | 이스케이프 | 답 · 이름에 `<` 가 있어도 조각에 태그로 들지 않는다(EV4) |
| T9 | 리스트 | `groups[]` → 시술 행 · 계열 묶음 · 층 합집합 · `modality_only[]` · `unreached[]` 가 시술 행에 없다 · 순서 = 허브 순서 · 행마다 gid(PL1 ~ PL5) |
| T10 | 부위 | `point` → 점 1 · `pair` → 점 2 · `area` · `none` · 표에 없는 코드 → 라벨 · 같은 부위 한 번 · 부위 0 → 빈 조각(SI3 ~ SI5) |
| T11 | 좌표표 | FC10 |
| T12 | 든 후보 | 앞 턴 대상이 후보에 붙는다 · yes 만 대상(`by` = `carried`) · 사이 값 · no 는 `dropped` · 이번 글에 같은 것이 있으면 다시 안 넣는다 · Jev 요청 수가 안 늘어난다(CR2 ~ CR5) |
| T13 | `carry` 없음 = 지금 동작 | `carry` 를 안 주면 `front()` 결과 · trace 가 지금과 같다 — **시험 앱의 지금 시험 전부 통과**(ST3) |
| T14 | 재료 덧붙이기 | 둘째 턴 메시지에 첫 턴 gid 가 없다 · 줄 번호가 이어진다 · 다시 읽은 줄은 `seen_lines` 에만 · `build()` 시작 번호를 안 주면 지금과 같다(AP1 ~ AP3) |
| T15 | 목록 요약 줄 | 고민 → 리스트 턴 메시지에 시술 이름 줄이 없다 · 계열마다 한 줄 · 장부에 그 줄의 `gids[]` 가 있다(AP4 · AP5) |
| T16 | 장부 | 턴마다 한 줄 · LG3 의 굵은 칸 여섯이 있다 · 서버를 다시 세운 뒤 같은 `conv_id` 로 줄을 되읽어 `open` 상태 · 다음 줄 번호가 이어진다(LG4) |
| T17 | 문구 0 | 템플릿 · `consult/` 코드에 한글 문장이 없다(주석 · `data-slot` 이름 빼고) — grep 시험 |
| T18 | 시험 화면 무변경 | `clinic_chat/web/` · `prompts/common.md` · `col_*.md` · `judge.md` · `jev/*.md` 의 sha 가 그대로다 |

### 9-2. 실물 확인

| # | 무엇 | 누가 | 보는 것 |
|---|---|---|---|
| E0 | htmx 빈 화면(외부 호출 0) | 구현 워커가 짓고 **코디가 띄움** | 가짜 턴 하나로 조각 셋이 한 줄기에서 갈아 끼워지는가 — EV2 의 두 길 가운데 서는 쪽 · `#face-marks` 통째 바꾸기가 SVG 로 그려지는가(EV3) · htmx · SSE 확장의 판 번호 · 라이선스 글(조사 §7-4) |
| E1 | **CLI 3턴 실측**(구독 · 회사 자료 없는 짧은 글) | 구현 워커(안 되면 코디) | ① `--max-turns 1` · `--system-prompt-file` 을 받는가(CL8) ② 둘째 · 셋째 턴이 첫 턴의 내용을 아는가(기억 이어짐) ③ 턴마다 첫 글자 ms · 전체 ms(조사 §7-1) ④ 턴마다 `cache_read` · `cache_creation` 토큰(resume 때 앞 대화가 캐시로 읽히는가 — 조사 §7-2) ⑤ 세션 파일이 고정 cwd 의 프로젝트 폴더에 생기는가 ⑥ 턴마다 `thinking_seen` · `observed_model` ⑦ 둘째 턴에 시스템 프롬프트 파일을 바꿔 줘도 첫 턴 기록이 유지되는가(F7) |
| E2 | 중단 뒤 resume(구독) | 구현 워커 | 답이 흐르는 중에 프로세스를 끝낸 세션에 `--resume` 을 걸면 어떻게 되는가 — CL10 ② 의 「`broken`」 이 지나치게 보수적인지의 재료(결과는 보고만 · 규칙은 코디가 바꾼다) |
| E3 | 실물 3턴(허브 18105 · Jev · CLI) | 구현 워커(안 되면 코디) | 조사 §5 의 세 턴 꼴(고민 → 그중 한 계열 → 다른 계열과 차이) — 턴마다 `first_list_ms` · `ttft_ms` · `total_ms` · 든 후보의 Noul · 결정 · 새 줄 수 · `seen_lines` 수 · 종료 상태. **답의 옳고 그름은 이 판의 기준이 아니다**(플로우 · 프롬프트가 초안) — 수와 배관만 |
| E4 | 화면 e2e | **코디가 18222 를 띄우고 사용자가 확인** | 리스트 · 점이 답보다 먼저 뜨는가 · 답이 리스트를 다시 읊지 않는가 · 꼬리가 화면에 없는가 · `/face-check` 좌표(§8-4) · 빈 자리 목록(§4-5) |

- E1 ~ E3 는 구독 CLI · Jev 를 실제로 부른다 — 「실물 호출 없이 끝났다고 하지 않는다」(코디 규칙). 워커는 18222 · 18220 · 18105 를 띄우거나 내리지 않는다.
- E1 · E2 는 고정 cwd(레포 밖)에서만 돌리고 사용자 홈의 세션 파일을 지우지 않는다(CL9-2).

### 9-3. 끝 조건

1. T1 ~ T18 통과 · 시험 앱의 지금 시험 전부 통과 · ruff.
2. E0 ~ E3 의 값이 보고에 있다(E1 ① 이 「안 받음」 이면 거기서 멈추고 코디에게).
3. E4 — 사용자 확인.

## 10. 열린 것

| # | 무엇 | 상태 · 추천 |
|---|---|---|
| O-1 | **상담 플로우** — 「짧게 → 깊게」 의 단계(L0 목록 / L1 개요 / L2 상세) · 시술을 눌렀을 때 · 상세 턴의 긴 목록 자리 | 사용자가 따로 준다(D-18) — 0.2. 조사 U-5(시술 부위 = 케이스 부위 추천) · U-10(왼쪽 아래 칸을 「지금 턴의 목록」 으로 — 추천)은 그때 |
| O-2 | SPEC-001 0.7 — 고민 부위 칸의 이름 · 꼴 | 별도 문서(D-19). 이 스펙의 필요 = §6-3 HN1 ~ HN4 |
| O-3 | 중단된 세션의 `--resume` 동작 · 긴 대화의 압축 · 세션 파일 보관 기간 · resume 때 캐시 조건 | 확인 안 됨(조사 §7-2) — E1 · E2 가 재료를 낸다. 그때까지 CL10 ② · CL13 은 보수적인 쪽 |
| O-4 | **SDK 모듈** — API 키 · `anthropic` 의존 · 캐시 표시 자리 · 추론 설정 · 모델 고르기 | 배포 전(D-4 · D-22). 경계 = §3-6 |
| O-5 | **`--bare`** — 공식 문서: `-p` 의 기본이 될 예정이고 bare 는 구독 로그인을 읽지 않는다(조사 §1-1) | 지금은 안 쓴다(CL4). CLI 판을 올릴 때마다 E1 을 다시 돈다 — 판 번호를 장부에 남기는 까닭(`llm.cli_version`) |
| O-6 | `--max-turns` · `--system-prompt-file` 을 이 판 CLI 가 받는가 | 확인 안 됨(F6) — E1 ①. 안 받으면 코디가 정한다 |
| O-7 | `--fallback-model haiku` 로 넘어간 턴의 처리 — 대화 도중 모델이 바뀌면 그 뒤 답 · 캐시가 어떻게 되는가 | 이 판은 기록만(`observed_model`). 값을 본 뒤 |
| O-8 | 구독 로그인으로 여러 사람이 쓰는 것 | 확인 안 됨(조사 §7-3) — 이 판은 로컬 한 사람. 배포 전에 닫는다 |
| O-9 | 상담 품질을 재는 법(물은 것만 · 불확실 표시 · 근거 추적) | 이 판 범위 밖. `judge.md` 의 두 항목은 그대로 쓸 수 있다(조사 §2-1) |
| O-10 | 같은 gid 를 다른 표지로 다시 읽었을 때(AP3 의 한계) · 한 턴 메시지가 한도를 넘을 때의 쪽 나눔(AP8) | 플로우(0.2)에서 상세 턴 꼴과 함께 |
| O-11 | 고민과 부위가 같은 이름으로 함께 잡힐 때 허브 응답 행 수(조사 §7-5) | 확인 안 됨 — E3 의 첫 턴에서 수를 본다 |

## 11. WORK 전에 정할 것

### 11-1. 사용자 결정(추천 붙임)

| # | 무엇 | 선택지 | 추천 |
|---|---|---|---|
| U-11 | 세션을 못 쓰게 됐을 때(`broken`) | (a) 그 대화는 끝 — 새 대화만 연다 (b) 장부로 새 세션을 다시 세워 잇는다(앞 턴 메시지 · 답을 새 세션에 다시 실음) | **(a)** — (b)는 SDK 경계와 같은 일이라 SDK 때 함께. 로컬 한 사람 · 턴 한도 20 에서는 드물다 |
| U-12 | 이 판의 이어 묻기 범위 | (a) 앞 턴 **대상**만 후보로(§5-2) — 「그중 필러」 를 앞 턴 리스트로 좁히는 것은 플로우(0.2) (b) 앞 턴 **리스트의 시술**까지 후보로 넣어 이 판에서 좁힌다 | **(a)** — 좁히는 규칙은 「짧게 → 깊게」 단계와 한 몸이다. (b)는 후보가 수십 개 늘어 Jev 요청이 는다(32 개 묶음) |
| U-13 | 「계열 층만」 · 「그 밖(시술 코드 없는 행)」 을 리스트에 | (a) 시술 행 아래 따로 묶음 둘로 전부 보인다 (b) 시술 행만 그리고 둘은 기록에만 | **(a)** — 「폭은 빠짐없이」. 묶음 머리 글은 빈 자리 |

### 11-2. 코디 기본값(바꿀 것만)

| # | 무엇 | 기본값 |
|---|---|---|
| C-10 | 설정 칸 이름 · 값 | §2-4 표 — 턴 시간 한도 120초 · 턴 한도 20 · 되짚는 앞 턴 1 · CLI 동시 수는 지금 칸 그대로(1) |
| C-11 | 모듈 · 라우트 · 파일 이름 | §2-2 · §4-1 · §7-2 |
| C-12 | 고정 cwd | 레포 밖 · 시스템 임시 폴더 아래 고정 이름 하나(CL9) |
| C-13 | 든 후보는 yes 일 때만 대상 | CR4 |
| C-14 | 고민 → 리스트 턴의 재료 = 목록 요약 줄(계열 · 시술 수 · 층 · 고민 맞춤 · 원리 이름) | AP4 |
| C-15 | 상담 재료에 이름 목록을 안 싣고 `answer_check` 를 안 돌린다 | AP7 |
| C-16 | 좌표는 44 부위를 한 번에 · `viewBox` 590 × 1060 | FC2 · FC7 |
| C-17 | 부위 0 이면 앞 턴 점을 지운다 | SI5 |
| C-18 | WORK 순서 | SPEC-001 0.7(허브 부위 칸) → WP-0(E0 빈 화면 · E1 CLI 3턴) → 실행기 · 장부 → 한 턴 흐름 · 리스트 → 부위 · 얼굴 → 이어 묻기 → E3 · E4 |

## 부록 A. 결정 행 → 이 문서

`_RESUME` §2 의 결정 행과 조사 코디 기본값이 이 문서의 어느 줄에 앉았는지다. 「줄」 은 이 파일의 줄 번호다.

| 결정 | 규칙 | 줄 |
|---|---|---|
| 11-17 「CLI 실행기 = 앱이 직접 띄움」 — 앱이 직접 | CL1 | 187 |
| 같은 행 — `--session-id` 첫 턴 · 옵션 전부 | CL2 | 188 |
| 같은 행 — `--resume` | CL3 | 189 |
| 같은 행 — 안 쓰는 것 · `--json-schema` 보류 · `--bare` 주의 | CL4 · O-5 | 190 · 558 |
| 같은 행 — 도구 전부 막음 | CL5 | 191 |
| 11-17 「채팅 조사 뒤 사용자 결정」 U-1 CLI 먼저 · SDK 는 배포 전 | SD1 · O-4 | 240 · 557 |
| 같은 행 U-2 키는 SDK 때 | SD5 | 244 |
| 같은 행 U-3 open-kknaks 무관 | D-21 | 88 |
| 같은 행 U-4 Sonnet | D-6 · CL2 | 73 · 188 |
| 같은 행 U-6 벡터로 새로 그림 · 좌표는 코드에 | FC1 · FC5 | 473 · 482 |
| 같은 행 U-7 원본 PNG 는 레포에 안 둠 | FC1 | 473 |
| 같은 행 U-8 얼굴 밖 · 넓은 부위는 얼굴 아래 라벨 | SI3 · FC8 | 413 · 485 |
| 같은 행 U-9 근거 꼬리 유지 · 화면에서만 숨김 | TF5 · TF6 · T7 | 270 · 271 · 518 |
| 같은 행 「상담 플로우는 따로」(U-5 · U-10) | O-1 | 554 |
| 11-17 「이번 세션 목표 = 상담 채팅」 — 화면 세 칸 · htmx | D-1 · EV2 | 68 · 293 |
| 같은 행 — 고민 → 시술 검색 → 리스트 → 부위에 점 | TF2 · TF3 | 267 · 268 |
| 11-17 「Procedure Hub 데이터는 공개 정보」 | D-23 | 90 |
| 11-17 「답 프롬프트 확정(C-1)은 채팅(상담) 단계로」 | PM1 | 461 |
| 11-17 「테스트 답은 빠짐없이」 — 「짧게」 는 상담에서 | AP7 · PM1 | 383 · 461 |
| 11-16 「테스트 ≠ 상담」 — 대화 장부 · 여러 턴 맥락 | LG1 · CR1 | 329 · 363 |
| 11-16 「LLM 에는 필요한 것만」 | AP6 | 382 |
| 11-16 「원칙: 폭은 빠짐없이」 | PL5 | 398 |
| 기본값 C-1 덧붙이기만 | AP1 | 377 |
| 기본값 C-2 장부 = 메모리 + 파일 한 줄씩 | LG1 · LG3 | 329 · 331 |
| 기본값 C-3 첫 턴에 이름 줄을 안 실음 | AP4 · PM4 | 380 · 464 |
| 기본값 C-4 앞 턴 대상을 Jev 후보에 | CR1 · CR2 | 363 · 364 |
| 기본값 C-5 허브에 고민 부위 칸(SPEC-001 판 올림) | SI1 · HN1 | 411 · 427 |
| 기본값 C-6 좌우 짝은 점 둘 | SI3 · FC5 | 413 · 482 |
| 기본값 C-7 새 모듈 + 포트 18222 | ST1 · D-2 | 110 · 69 |
| 기본값 C-8 Jinja2 · C-9 htmx 로컬 파일 | D-3 | 70 |
| 지시서 — 리스트는 앱 결정론 · 계열 묶음 · 층 표시 | PL1 · PL2 · PL3 | 394 · 395 · 396 |
| 지시서 — 리스트 · 점은 LLM 전에 | TF3 · EV1 | 268 · 292 |
| 지시서 — 점 기준 = 고민 부위 | SI1 · SI7 | 411 · 417 |
| 지시서 — 화면 문구는 짓지 않는다 | ST4 · T17 | 113 · 528 |

## 부록 B. 얼굴 · 머리 · 목 부위 60 의 분류

분류(꼴)는 조사 §3-2 의 **초안**이다 — 조사 워커가 그림을 보고 붙였고 사용자 눈 확인 전이다. 「고민」 = 그 부위에 묶인 `concern_site` 행 수(재셈 — 조사 표와 60 행 전부 같다). 이 판의 화면 = `point` · `pair` 는 점, 나머지는 라벨.

| 꼴 | 수 | 고민이 묶인 것 | 부위 코드(굵은 것 = 고민이 묶임) |
|---|---|---|---|
| `point`(한 점) | 17 | 11 | **SITE-014** · **SITE-015** · **SITE-035** · **SITE-036** · **SITE-037** · SITE-040 · SITE-041 · SITE-057 · SITE-060 · **SITE-062** · SITE-064 · **SITE-069** · **SITE-072** · SITE-073 · **SITE-077** · **SITE-079** · **SITE-084** |
| `pair`(좌우 — 점 둘) | 27 | 14 | **SITE-016** · **SITE-018** · **SITE-019** · **SITE-024** · **SITE-025** · SITE-026 · SITE-027 · SITE-028 · **SITE-029** · **SITE-030** · SITE-031 · SITE-032 · SITE-033 · SITE-034 · SITE-039 · **SITE-046** · **SITE-051** · SITE-055 · **SITE-056** · **SITE-067** · **SITE-075** · **SITE-076** · **SITE-086** · SITE-089 · SITE-090 · SITE-091 · SITE-120 |
| `area`(영역 — 라벨) | 8 | 5 | **SITE-007** · **SITE-011** · **SITE-013** · SITE-045 · SITE-058 · **SITE-083** · **SITE-087** · SITE-088 |
| `line`(선 — 라벨) | 4 | 0 | SITE-065 · SITE-080 · SITE-081 · SITE-085 |
| `none`(정면에 안 보임 — 라벨) | 4 | 1 | SITE-043 · SITE-044 · **SITE-070** · SITE-071 |
| 합 | 60 | 31 | |

- 재셈(`$SM/silver/site.csv` 89 행 · `concern_site.csv` 95 행): 고민이 묶인 부위 51 종 = 얼굴 쪽 31 + 몸 20 · 부위가 묶인 고민 85(부위 1 개 83 · 3 개 1 · 9 개 1) — 조사 §3-4 와 같다.
- 몸 부위 가운데 고민이 묶인 20(전부 라벨): SITE-001 · SITE-092 · SITE-093 · SITE-095 · SITE-097 · SITE-098 · SITE-100 · SITE-101 · SITE-102 · SITE-103 · SITE-105 · SITE-106 · SITE-110 · SITE-112 · SITE-114 · SITE-115 · SITE-116 · SITE-117 · SITE-118 · SITE-119.
- `parent_code` 로 「얼굴 안의 부위」 를 고를 수 없다(부모가 있는 부위 21 / 89 — 조사 §3-2) — 그래서 표가 손으로 가른 목록이다.

## 변경 기록

### 0.1.0 — 2026-11-17 · 처음 씀

- 상담 채팅 1판: 구조(§2) · CLI 기억(§3) · 한 턴 흐름과 이벤트(§4) · 장부 · 이어 묻기 · 재료 덧붙이기(§5) · 시술 리스트 · 부위(§6) · 프롬프트 기반(§7) · 얼굴 SVG · 좌표표(§8) · 시험 T1 ~ T18 · 실물 확인 E0 ~ E4(§9).
- 열린 것 O-1 ~ O-11 · 사용자 결정 U-11 ~ U-13 · 코디 기본값 C-10 ~ C-18.
- 이 워커가 새로 본 사실: 로컬 CLI(2.1.322) `--help` 에 `--max-turns` 줄이 없고 `--system-prompt-file` 은 `--bare` 설명 안에만 나온다(F6) · `--system-prompt-snapshot` 의 help 글(F7).

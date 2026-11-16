# 운영(prod) 서버 claude CLI 사용처 실측 — read-only 조사

- 조사 시각: 2026-11-13 10:49~11:20 KST (UTC 01:49~02:20)
- 조사자: mediness `infra` 워커 (task_e6c0675bfacb / ctx_c4bbb1a04fe2)
- 방법: `git show origin/main:` 코드 전수 grep + `ssh medi-me` → `/opt/homebrew/bin/kubectl` (ns `mediness-prod`) exec·logs·psql(`default_transaction_read_only=on`) + `gh api` 로 `k8s_infra_mac/charts/mediness`
- 쓰기 0건: 코드·클러스터·DB·GitOps 레포 모두 변경 없음. 비밀값은 「있음/없음」으로만 적었다.

---

## 0. 결론 먼저 — 이미 장애 중이다

**prod 의 claude 경로는 지금 전부 죽어 있다.** 2026-11-10 06:03 KST 브리프부터 worker 의 claude 호출이 매번
`Your organization has disabled Claude subscription access for Claude Code · Use an Anthropic API key instead, or ask your admin to enable access`
로 실패한다(prod·dev 공통, `CLAUDE_CODE_OAUTH_TOKEN` 구독 인증이 조직 차원에서 막힘). 따라서 「claude 를 쓰는 경로」는
곧 「**지금 고장 난 경로**」다. codex 경로(회의록 v2·랜딩 채팅)는 같은 시간대에 정상 동작 중이다.

## 1. 요약 표 (prod, origin/main `67b6a7dc` 기준)

| # | 경로 | 실행 위치(pod) | 운영 현재 provider (근거) | codex 전환 방법 | 근거 발췌 |
|---|---|---|---|---|---|
| **A** | AX 비서 (action_runtime 드라이버 — `ax_task_draft`·`decision_draft`·`catalog_turn`·`catalog_final_audit`·`incident_triage`) | **back** 프로세스가 `claude -p` 를 직접 spawn | **claude, 켜져 있음** (env `ACTION_RUNTIME_LLM_DRIVER=claude`, `llm_calls` 원장 전량 claude). 11-07 이후 원장 행 0건 → 11-10 이후는 **실패 추정**(아래 §7 「확인 못 함」) | **env 만으로 안 된다 — 인프라 변경 필요(코드 수정은 불요).** ① back 컨테이너에 `codex` 실행 파일 없음 → `/opt/codex` hostPath ro 마운트 + PATH 추가(차트). ② back 에 codex 인증 없음(`CODEX_HOME` 미설정, `OPENAI_API_KEY` 없음, back 은 uid 1001 appuser) → appuser 가 읽을 수 있는 `CODEX_HOME`+`auth.json` 또는 `OPENAI_API_KEY` 주입. ③ 그 뒤 `mediness-secret` 의 `ACTION_RUNTIME_LLM_DRIVER=codex-unsafe-tools` + back 재시작 | back: `command -v codex` → `codex:none`; `CODEX_HOME=unset`; env `ACTION_RUNTIME_LLM_DRIVER=claude`; `llm_calls`: claude/f 801행, 최종 `2026-11-07 02:51 UTC` |
| **B** | 결정 게이트 `decision_gate._default_ai_call` (Slack 의사결정 intake AI 추천) | back 이 제출 → **worker** 큐 `mediness-brief` | **claude, 배선은 켜져 있으나 유휴.** 조건 `SLACK_DECISION_BOT_TOKEN` 있음 + `LLM_VENDOR=open_kknaks` → `main.py:95` 실 AI 게이트 활성. 단 `decision_intake` 최종 행 2026-08-03 → 3개월 넘게 트리거 없음 | **코드 수정 필요.** `provider` 기본값 `"claude"` 고정 + `model=settings.meeting_llm_batch`(`claude-sonnet-4-6`) + claude 전용 `provider_options`(`system_prompt`·`max_turns`·`mcp_config`·`allowed_tools`) — codex 는 이 키 집합을 거부(회의록 v2 가 별도 codex plan 빌더를 둔 이유, `meeting_extractor_client.py:258` 주석) | env: `SLACK_DECISION_BOT_TOKEN=<있음>`, `LLM_VENDOR=open_kknaks`; DB: decision_intake 2026-08 4건이 마지막 |
| B′ | `pipeline_ingest_consumer._default_analyze` (B 재사용) | back → worker | **꺼져 있음.** `PIPELINE_INGEST_ENABLED` 미설정 → 기본 `False` → 컨슈머 미기동 | (켜지 않는 한 무관) B 를 고치면 같이 고쳐짐 | env 에 `PIPELINE_INGEST*` 없음; `config.py:426 pipeline_ingest_enabled=False`; `pipeline_change_proposal` 0행 |
| **C** | 데일리 브리프 `brief/synthesizer.py:556` (매일 06:00 KST 스케줄러) | back(스케줄러) → **worker** 큐 `mediness-brief` | **claude, 켜져 있음 → 11-10 부터 매일 실패.** 스케줄러 무조건 등록(`main.py` `build_scheduler()`), `llm_vendor` 검사 없음(dev 는 `LLM_VENDOR=mock` 인데도 claude 로 제출되어 같은 에러로 실패) | **코드 수정 필요.** `provider="claude"` 하드코딩 + claude 전용 options(`mcp_config`·`allowed_tools`·`max_turns`·`system_prompt`) + claude 모델명 | `brief_run` 11-10·11·12·13 FAILED, error `"Your organization has disabled Claude subscription access…"`; 11-03~11-09 PUBLISHED |
| **D** | 주간회의록 `weekly_report_pipeline.py:515` (금 09:00 KST) | back(스케줄러) → **worker** 큐 `mediness-brief` | **claude, 켜져 있음 → 오늘(11-13 금) 실패.** version_summary 4콜 전부 실패, 보고서는 AI 요약 없이 `draft` 로 생성됨 | **코드 수정 필요.** `provider="claude"` 하드코딩, `provider_options={"system_prompt",…,"max_turns":1,"effort":"low"}`, claude 모델명 | back 로그 `2026-11-13 00:00:02 [WARNING] weekly_report_pipeline: weekly version_summary 콜 실패 … RuntimeError('weekly AI 응답 비정상 — status=failed')` ×4; worker 로그 동시각 `task.failed error='Your organization has disabled Claude subscription access…'` ×4 |
| **E** | 회의록 v2 (`meeting_v2_extractor` warmup·batch·final) | back → **worker** 큐 `mediness-meeting-v2` | **codex, 정상 동작.** `MEETING_LLM_PROVIDER` 미설정 → 기본 `codex`. claude 차단 이후인 11-13 01:39~01:50 UTC 에도 task.done exit_code=0 연속 | 이미 codex. 조치 불요 | worker 로그 `queue=mediness-meeting-v2 … task.done … exit_code=0` (11-13 6건); `meeting_v2` 11-09 주 ended 9건 중 8건 llm_session_id 보유 |
| **F** | 랜딩 채팅 `landing_chat/submission.py:212` | back → **worker** 큐 `mediness-landing-chat` | **codex.** 코드 고정 `provider="codex"` | 이미 codex | `landing_chat_turns` done 493 / failed 1, 최신 usage 에 `reasoning_output_tokens` 키(codex 어댑터 형식) |
| (G) | 회의록 v1 `meeting_extractor.py` | — | **꺼져 있음(코드 사망).** 함수 `get_client()` 만 v2 가 재사용, v1 submit 경로는 호출처 없음(WP-045 v1 라이브 제거) | 무관 | `git grep` 결과 v1 모듈 import 처는 v2·seed·pipeline_ingest(`loads_json_robust`) 뿐 |

**claude 를 실제로 쓰는(=지금 고장 난) 운영 경로: A · C · D (+ 트리거 오면 B).**
- env 만으로 codex 전환 가능한 경로: **없다.** A 는 인프라(마운트+인증)만 필요하고 코드는 불요, B·C·D 는 코드 수정 필요.

---

## 2. 배포 버전

| deployment | 이미지 태그 | origin/main | pod 시작 |
|---|---|---|---|
| back | `mediness-back:67b6a7dc1e05e0e82c43405b407a3af2e1f3605e-arm64` | **= origin/main HEAD** `67b6a7dc` (Merge PR #152 from dev, 2026-09-23 12:24 KST) | 2026-09-23T03:43:54Z |
| worker | `mediness-worker:67b6a7dc…-arm64` | 동일 | 2026-09-23T03:43:24Z |
| mcp | `mediness-mcp:67b6a7dc…-arm64` | 동일 | 2026-09-23T03:43:24Z |
| front | `mediness-front:67b6a7dc…-arm64` | 동일 | 2026-09-23T03:43:24Z |
| (sts) postgres | `pgvector/pgvector:pg16` | — | — |
| (sts) redis | `redis:7-alpine` | — | — |

CronJob 없음. 스케줄은 back 프로세스 안 APScheduler.

## 3. deployment 별 CLI 유무 / 마운트

| pod | uid | PATH 선두 | `claude` | `codex` | `/opt/claude` | `/opt/codex` | CODEX_HOME / 인증 |
|---|---|---|---|---|---|---|---|
| back | 1001 appuser | `/opt/claude/bin:…` | `/opt/claude/bin/claude` (2.1.220) | **없음** | ro hostPath | **없음** | `CODEX_HOME` unset, `OPENAI_API_KEY` 없음 |
| worker | 0 root | `/opt/codex/bin:/opt/claude/bin:…` | `/opt/claude/bin/claude` (2.1.220) | `/opt/codex/bin/codex` (codex-cli 0.146.0) | ro hostPath | ro hostPath | `CODEX_HOME=/root/.codex` (PVC `worker-codex`), `auth.json` **있음** |
| mcp | 1001 appuser | — | 없음 | 없음 | 없음 | 없음 | — |
| front | — | — | 없음 | 없음 | 없음 | 없음 | — |

근거(발췌):
```
== back
PATH=/opt/claude/bin:/usr/local/bin:...
/opt/claude/bin/claude
codex:none
CODEX_HOME=unset
2.1.220 (Claude Code)
sh: 1: codex: not found
mounts=/mediness() ... /opt/claude(true)   volumes: claude-bin:/opt/claude
== worker
PATH=/opt/codex/bin:/opt/claude/bin:...
/opt/claude/bin/claude
/opt/codex/bin/codex
CODEX_HOME=/root/.codex   (ls → auth.json, sessions, ...)
mounts=/root/.claude() /opt/claude(true) /root/.codex() /opt/codex(true)
volumes: claude:worker-claude claude-bin:/opt/claude codex:worker-codex codex-bin:/opt/codex
```
참고: back pod 는 lima-worker-1 에 떠 있고, 같은 노드에서 worker 가 `/opt/codex` hostPath 를 이미 쓰고 있다 → 노드에 바이너리는 있다(values-prod 주석: 「노드 /opt/codex 는 41-codex.sh 로 worker-1·2 설치 완료」).

## 4. env 표 (prod)

envFrom 은 세 deployment 모두 `configMapRef mediness-config` + `secretRef mediness-secret(optional)`.

| 키 | back | worker | mcp | 출처 |
|---|---|---|---|---|
| `LLM_VENDOR` | `open_kknaks` | `open_kknaks` | `open_kknaks` | configmap (차트 `back.llmVendor`) |
| `MEDINESS_LLM_VENDOR` | 미설정 | 미설정 | 미설정 | — (config 에 env_prefix 없음 → 쓰이지 않는 키) |
| `MEETING_LLM_PROVIDER` | **미설정** → 코드 기본 `codex` | 미설정 | 미설정 | — |
| `MEETING_CODEX_MODEL` | 미설정 → `landing_chat_model` 기본 `gpt-5.6-terra` | 미설정 | 미설정 | — |
| `ACTION_RUNTIME_LLM_DRIVER` | `claude` | `claude` | `claude` | **secret `mediness-secret`** (차트 아님) |
| `ACTION_RUNTIME_CLAUDE_MODEL` | `sonnet` | `sonnet` | `sonnet` | secret |
| `ACTION_RUNTIME_LLM_TIMEOUT_SECONDS` | `60` | `60` | `60` | secret |
| `OPEN_KKNAKS_QUEUE` | `mediness-meeting,mediness-meeting-v2,mediness-brief,mediness-landing-chat` | 동일 | 동일 | configmap |
| `STT_VENDOR` | `elevenlabs` | 동일 | 동일 | configmap |
| `CODEX_HOME` | 미설정 | `/root/.codex` | 미설정 | deployment env |
| `PIPELINE_INGEST_ENABLED` | 미설정(→False) | — | — | — |
| `CLAUDE_CODE_OAUTH_TOKEN` | 있음 | 있음 | 있음 | secret |
| `ANTHROPIC_API_KEY` | 없음 | 없음 | 없음 | — |
| `ANTHROPIC_AUTH_TOKEN` | 없음 | 없음 | 없음 | — |
| `OPENAI_API_KEY` | 없음 | 없음 | 없음 | — |
| codex 자격증명 파일 | 없음 (`CODEX_HOME` 없음, `/root/.codex` 권한 없음) | `$CODEX_HOME/auth.json` 있음 | 없음 | worker PVC |
| `SLACK_DECISION_BOT_TOKEN` | 있음 | 있음 | 있음 | secret |
| 그 외 `*PROVIDER*`·`*VENDOR*`·`*DRIVER*`·`*LLM*` | 없음 | 없음 | 없음 | — |

## 5. 실제 호출 흔적

### 5-1. `llm_calls` 원장 (경로 A 전용 — 쓰는 곳은 `action_runtime/llm/driver.py` 의 `_meter` 하나)

```
select provider, estimated, count(*), max(created_at) from llm_calls where created_at > now() - interval '7 days' group by 1,2;
 provider | estimated | count |              max
----------+-----------+-------+-------------------------------
 claude   | f         |     3 | 2026-11-07 02:51:16.383432+00
(1 row)
```
전체 기간:
```
 provider | estimated |       purpose       |      model      | count |              min              |              max
----------+-----------+---------------------+-----------------+-------+-------------------------------+-------------------------------
 claude   | f         | ax_task_draft       | claude-sonnet-5 |   505 | 2026-08-12 04:48:40+00 | 2026-11-07 02:50:17+00
 claude   | f         | catalog_final_audit | claude-sonnet-5 |    61 | 2026-07-31 04:56:49+00 | 2026-11-03 02:01:44+00
 claude   | f         | catalog_turn        | claude-sonnet-5 |   201 | 2026-07-31 04:56:38+00 | 2026-11-03 02:01:37+00
 claude   | f         | decision_draft      | claude-sonnet-5 |    23 | 2026-08-14 08:51:44+00 | 2026-11-07 02:51:16+00
 claude   | f         | incident_triage     | claude-sonnet-5 |    11 | 2026-08-13 06:50:11+00 | 2026-08-13 06:52:45+00
```
codex 행(`estimated=t`) 은 한 번도 없다 → 경로 A 는 운영에서 codex 로 돈 적이 없다.
최근 AX 트리거: 11-07 02:49(api), 11-07 02:50(ax_decision_draft_api), **11-09 08:32(meeting_modal) — 대응 원장 행 없음.**

### 5-2. worker 로그 (`kubectl logs deploy/worker --since=96h`, 239줄)

큐별 task 수: `mediness-meeting-v2` 107 / `mediness-brief` 8.
```
2026-11-09 21:03:21 [error] task.failed error='Your organization has disabled Claude subscription access for Claude Code · Use an Anthropic API key instead, ...'   ← 브리프(C) 06:03 KST
2026-11-10 21:03:35 [error] task.failed (동일)
2026-11-11 21:03:41 [error] task.failed (동일)
2026-11-12 21:03:23 [error] task.failed (동일)
2026-11-13 00:00:00 task.start prompt='너는 주간회의록의 버전별 진행 요약 에이전트다…' queue=mediness-brief
2026-11-13 00:00:02 [error] task.failed (동일)  ×4                                ← 주간보고(D) 09:00 KST
2026-11-13 01:39:13 task.start prompt='당신은 회의록 작성 도우미입니다…' queue=mediness-meeting-v2
2026-11-13 01:39:19 task.done cost_usd=0.0 duration_ms=0 exit_code=0           ← 회의록 v2(E) codex 정상 (이후 01:50 까지 5건 더 exit_code=0)
```
worker 로그에는 provider 필드가 찍히지 않는다. claude/codex 판정은 큐→코드의 provider 값 + 성공/실패 패턴으로 했다.

### 5-3. 경로별 DB 흔적

```
brief_run (C):  11-13·11-12·11-11·11-10 FAILED  error {"llm":{"status":"failed","error_msg":"Your organization has disabled Claude subscription access…"}}
                11-03~11-09 PUBLISHED / 11-02 FAILED ("You've hit your session limit")
weekly_report (D): 2026-W47 snapshot 20 status=draft generated 2026-11-13 00:00 UTC (AI 요약 4콜 실패 상태로 생성)
decision_intake (B): 최종 2026-08-03 (2026-08 4건, 07 54건, 06 10건) — 이후 0건
pipeline_change_proposal (B′): 0 rows
meeting_v2 (E): 매주 5~10건 ended, 대부분 llm_session_id 보유 (11-09 주 9건 중 8건)
landing_chat_turns (F): done 493 (최종 2026-11-07), failed 1
```

## 6. 후보 목록 밖에서 새로 찾은 것

`git grep -nE 'provider=|create_subprocess_exec|subprocess|\.submit\(' origin/main -- back/ mcp/` 전수 + `"claude"`·`AgentClient(`·`make_claude_client` 추가 grep 결과:

1. **회의록 v2 의 claude 분기** — `meeting_v2_extractor.py` warmup/batch 는 `settings.meeting_llm_provider != "codex"` 이면 claude 로 간다(`meeting_extractor_client.OpenKknaksAdapter.submit` 의 기본 `provider="claude"`). prod 는 기본값 codex 라 해당 없음. 단, 누가 `MEETING_LLM_PROVIDER` 를 다른 값으로 넣으면 claude 로 돌아간다.
2. **`make_claude_client()` 게이트** — 회의록 v2 도 `LLM_VENDOR=open_kknaks` 여야 실호출(`mock` 이면 MockClaudeClient). dev 가 `mock` 이라 dev 회의록은 LLM 을 아예 안 탄다.
3. **회의록 v1 `meeting_extractor.py`** — 사망 코드(호출처 없음). 무관.
4. **`landing_chat/runtime.py:50`** — F 의 실제 제출 지점(`provider=plan.provider` = `"codex"`).
5. **`action_runtime_v2.py:2576 provider=row.provider`** — 원장 조회 응답 직렬화일 뿐 호출 아님.
6. `docs_sync.py`·`publish/git_client.py`·`search_service.py` 의 subprocess 는 git/rg — LLM 무관.
7. **스크립트(운영 미실행)**: `back/scripts/brief_synthesize_smoke.py:313`, `back/scripts/warmup_local_check.py:77` 가 `provider="claude"` — 수동 스모크용, 서버 경로 아님.
8. **mcp 서비스**: LLM 호출 없음(claude/codex/AgentClient 참조 0건, CLI 도 없음).
9. **문서 드리프트**: `DEPLOY.md §4-4` 절차는 docker-compose 시절(`.env.prod` → GH Secret → 재배포) 기준이다. 현재 prod 는 k8s 이고 `ACTION_RUNTIME_LLM_DRIVER` 는 클러스터 secret `mediness-secret` 에 있다(차트 configmap 아님). 또 §4-4 의 전제(서버 컨테이너 PATH 에 codex)는 **prod back 에서 충족되지 않는다.**

## 7. dev (`mediness-dev`) — prod 와 다른 점만

- 이미지: `b840254a…-dev-arm64` (dev 브랜치, main 보다 앞섬 — WP-131)
- `LLM_VENDOR=mock` → 결정 게이트(B)는 더미, 회의록 v2(E)는 MockClaudeClient(LLM 미호출). `LLM_LOCAL_MODEL=google/gemma-4-26b-a4b-qat` 추가.
- **브리프(C)는 dev 에서도 claude 로 제출되어 같은 에러로 실패**(`brief_run` 11-11~11-13 FAILED) → C 는 `llm_vendor` 와 무관하게 claude 를 탄다는 실증.
- `llm_calls`: 최근 7일 0행, 전체 claude/f 73행(최종 2026-09-01).
- CLI 구성은 prod 와 같다: back 에 claude 만, codex 없음. worker 는 둘 다 있고 `auth.json` 있음.
- env `ACTION_RUNTIME_*` 는 prod 와 같은 값(secret).

## 8. 확인 못 한 것과 이유

1. **경로 A 가 11-10 이후 실제로 실패하는지 — 확인 못 함.** 11-07 이후 `llm_calls` 행이 없고(11-09 meeting_modal 트리거 1건은 대응 행 없음), back 로그는 APScheduler 스팸 탓에 `--since=168h` 로도 **2026-11-12 20:04 UTC 이후 약 6시간분만 남아** 그 사이 AX 호출 흔적이 없다. back 과 worker 는 같은 secret 의 같은 `CLAUDE_CODE_OAUTH_TOKEN` 을 쓰므로 **같은 에러로 실패할 것이 강하게 추정**되지만, 실제 `claude -p` 를 back 에서 돌려 보는 것은 LLM 호출(외부 부작용)이라 read-only 범위 밖으로 보고 하지 않았다. 확인하려면 AX 발화 1회 후 back 로그의 `claude CLI 실패 (1): …` 를 보면 된다.
2. **결정 게이트(B) 활성 로그** — `decision intake AI gate (C6 real AI) enabled` 기동 로그는 pod 가 9-23 기동이라 로그가 이미 로테이션되어 없다. 활성 판정은 env(`SLACK_DECISION_BOT_TOKEN` 있음, `LLM_VENDOR=open_kknaks`) + `main.py:88-124` 코드로 했다.
3. **worker 의 claude 인증 출처** — worker 는 `CLAUDE_CODE_OAUTH_TOKEN` env 와 PVC `/root/.claude` 를 둘 다 가진다. 어느 쪽이 실제로 쓰였는지는 확인하지 않았다(결과적으로 둘 다 같은 조직 정책에 막힌 것으로 보인다).
4. **back 에 codex 인증을 어떻게 줄지** — worker 의 `CODEX_HOME` PVC(`worker-codex`)는 RWO 일 가능성이 높고 root 소유라 back(appuser) 재사용 가능 여부는 확인하지 않았다. values-prod 주석도 「CODEX_HOME 을 공유하지 마라(세션 충돌·토큰 refresh 무효화)」고 경고한다.
5. **`mediness-secret` 의 프로비저닝 경로**(누가 어디서 갱신하는지) — 범위 밖이라 보지 않았다.

## 9. 핫픽스 설계자에게 넘기는 요점 (설계 아님, 사실 정리)

- 고장 범위: **A(AX 비서)·C(데일리 브리프)·D(주간보고 AI 요약)**, 그리고 Slack 결정 intake 가 들어오면 **B**.
- A: 코드 수정 없이 **차트(back 에 `/opt/codex` 마운트 + PATH + codex 인증) + secret 값 `codex-unsafe-tools`** 로 전환 가능. DEPLOY §4-4 의 보안 대가(임의 파일 읽기·에이전트 스폰 잔존)가 그대로 따라온다.
- B·C·D: 모두 worker 큐 `mediness-brief` 로 제출되고 worker 에는 codex·인증이 이미 있다 → **인프라는 준비됨, 코드만 바꾸면 된다**(provider 하드코딩, claude 전용 `provider_options`, claude 모델명 `meeting_llm_batch=claude-sonnet-4-6`). 회의록 v2 의 `meeting_v2_submission.build_submission`/`compose_prompt` 가 기존 codex 제출 선례다.
- E·F: 이미 codex, 정상.
- 대안(코드 무변경): Anthropic API 키(`ANTHROPIC_API_KEY`)를 secret 에 넣으면 claude 경로 전체가 되살아날 가능성이 있다(에러 문구가 그 방법을 안내함). 단 이는 비용 구조가 바뀌는 결정이라 사용자 판단 사항이다. 검증하지 않았다.

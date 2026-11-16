# [backend_hotfix] WP-133 — 서버 LLM claude → codex 전환 핫픽스 (B·C·D, main)

너는 **mediness `backend_hotfix` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스/orchestration/roles/mediness/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- 이 워크트리의 `AGENTS.md`(있으면)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/llm-codex-hotfix-hotfix`
base 브랜치: `origin/main` (= prod 배포본 `67b6a7dc`) → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

너는 앞 맥락이 없다. 이 브리프와 WP-133 이 입력의 전부다.

## 1. SSOT — 먼저 읽을 것

- **WP-133 (계약·빌드 계획의 정본)**: `/Users/kknaks/orca/workspaces/mediness-mediness/llm-codex-hotfix-spec/products/mediness/30-work/work-133-server-llm-codex-hotfix.md` — 대응표·결과 파싱 표·Phase 1~2 를 **그대로** 구현한다. 여기 없는 건 발명하지 마라.
- 운영 실측 리포트(배경): `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스/orchestration/work/llm-codex-hotfix/survey-prod-claude-usage.md`

**기대는 개념** — 해당 없음. 원칙: **선례 `back/app/services/meeting_v2_submission.py` · `meeting_v2_extractor.py:449-471` 의 모양을 그대로 따른다.**

## 2. 배경 / 무엇을 바꾸나

2026-11-10 부터 조직 차단으로 서버의 claude 호출이 전부 실패한다. 결정 게이트(B)·데일리 브리프(C)·주간보고(D)의 worker 제출을 codex 로 바꾼다. worker 에는 codex·인증이 이미 있어 **코드만** 바꾼다.

**사용자 결정(2026-11-13) — WP-133 보다 우선한다:**
- **테스트를 작성·수정·실행하지 않는다.** WP-133 Phase 1 「검증 — 단위」, Phase 2 「기존 테스트 보존·신규 테스트」 「검증」 항목은 **이번 판에서 하지 않는다.** 기존 테스트가 codex 기본값 때문에 깨지는 것은 알고 둔다(CI 가 테스트를 돌리지 않는다).
- Phase 3(운영 실물 호출)은 **배포 후 코디네이터가** 한다 — 너는 운영(ssh·kubectl)에 손대지 않는다.
- Open Issues ① 설정 키 배치는 **ⓐ 공용 키 한 벌**(B·C·D 공통 — 같은 큐 `mediness-brief` 를 쓰는 서버 콜 묶음)로 간다. 값은 WP 그대로(provider 기본 `codex`, codex 모델 키 기본 `""` → `landing_chat_model`, MCP url·server key 는 `meeting_v2_mcp_url`·`meeting_v2_mcp_server_key` 와 같은 값).

## 3. 계약

WP-133 대응표 그대로. 핵심:
- provider 설정값(기본 codex). `codex` 면 선례 모양으로 조립, 아니면 **현 claude 인자 그대로**(되돌리기 경로 보존 — claude 분기 코드를 지우지 마라).
- codex 조립: `sandbox="read-only"` · `skip_git_repo_check=True` · `config` `-c` 리스트(`model_reasoning_effort` · `approval_policy="never"` · 표면 축소 4줄 · MCP 쓰는 경로만 `mcp_servers.<key>.url/http_headers/enabled_tools` + 툴별 `approval_mode="approve"`) · `compose_prompt(system, user)` · 모델 해석값이 비면 `None`(키 제외).
- `enabled_tools` 는 **접두어(`mcp__mediness__`) 뗀 이름.** B = `gate_tools.ALLOWED_TOOL_NAMES` 7종, C = `read_file_tool`·`list_dir_tool`·`repo_search_tool`·`get_metadata_tool`, D = MCP 없음.
- effort: B `low` · C `medium` · D `low`. `options.timeout_sec`·`queue` 는 그대로.
- **compose 후 최종 프롬프트 바이트 로그** 한 줄(B·C·D 공통). `http_headers` 는 로그·에러에서 redact(선례 `redact_config_overrides`).

## 4. 먼저 읽을 핵심 파일

- `back/app/services/meeting_v2_submission.py` — 선례 조립(`build_submission`·`compose_prompt`·`redact_config_overrides`)
- `back/app/services/meeting_v2_extractor.py:440-550` — provider 분기 선례
- `back/app/services/decision_gate.py:651-736` — B
- `back/app/services/pipeline_ingest_consumer.py:159-169` — B′ (수정 없음, partial 호환만 확인)
- `back/app/services/brief/synthesizer.py:530-612` — C
- `back/app/services/weekly_report_pipeline.py:498-525` — D
- `back/app/config.py:255-300` — 선례 설정 키

## 5. allowed_paths — 이 밖은 건드리지 마라

- `back/app/` 만 (역할상 `back/`·`mcp/` 허용이지만 이번 판은 `back/app/` 로 좁힌다 — 테스트·스크립트·mcp 수정 금지)

## 6. 구현 단계

1. WP-133 Phase 1 — 공용 codex 조립 함수 + 설정 키(ⓐ) + 바이트 로그 + redact.
2. WP-133 Phase 2 — B·C·D 제출 지점을 provider 분기로 전환. B′ 는 손대지 않고 partial 인자가 codex 분기에서 깨지지 않는지만 코드로 확인.
3. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스/orchestration/work/llm-codex-hotfix/be-hotfix-report.md` 작성: 변경 파일·지점별 전/후 제출 인자 요약·설정 키 이름과 기본값·env 로 되돌리는 법·Phase 3 에서 코디가 볼 로그 문구(바이트 로그 키워드).

## 7. 범위 제약 — 하지 말 것

- 테스트 작성·수정·실행 금지(사용자 결정). 스택 기동·docker·운영 접속 금지.
- A(AX 비서 `action_runtime/llm/driver.py`)·`DEPLOY.md`·`agent/`·mcp 수정 금지.
- claude 분기 삭제 금지. open-kknaks 라이브러리 수정 금지.
- 커밋·push·PR 금지.

## 8. 검증

```
cd back && python -m py_compile <네가 고친 .py 파일들>          → 에러 0
cd back && python -c "import app.services.decision_gate, app.services.brief.synthesizer, app.services.weekly_report_pipeline, app.config"   → import 에러 0 (back 의 venv 가 있으면 그 python 으로)
git -C /Users/kknaks/orca/workspaces/mediness-app/llm-codex-hotfix-hotfix status --short   → back/app/ 밖 변경 0
grep 으로 codex 분기 조립 결과에 system_prompt·max_turns·allowed_tools·disallowed_tools·mcp_config·json_schema 키가 없는지 코드 대조
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_4d39f44d-7335-41dc-bd4a-b274304b05d9 --from term_ffb55a13-10b5-4db8-902e-149e4df17ee5 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend_hotfix 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_4d39f44d-7335-41dc-bd4a-b274304b05d9 \
  --text "[worker_done] backend_hotfix 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_4d39f44d-7335-41dc-bd4a-b274304b05d9 --text "[질문] backend_hotfix: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)

# [reviewer_code_hotfix] WP-133 핫픽스 코드 검수 — B·C·D codex 전환 (read-only)

너는 **mediness `reviewer_code` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스/orchestration/roles/mediness/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/llm-codex-hotfix-hotfix`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

⚠ 이 워크트리에 backend_hotfix 워커의 **미커밋 산출물**이 있다(수정 4 + 신규 `back/app/services/server_llm_submission.py`). 검수 대상이다 — **고치지 마라.** 너는 앞 맥락이 없다.

## 1. SSOT — 먼저 읽을 것

- **WP-133 (계약 정본)**: `/Users/kknaks/orca/workspaces/mediness-mediness/llm-codex-hotfix-spec/products/mediness/30-work/work-133-server-llm-codex-hotfix.md` — 대응표·결과 파싱 표·Phase 1~2
- 구현 브리프(사용자 결정 포함): `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스/orchestration/work/llm-codex-hotfix/llm-codex-hotfix-be-hotfix-brief.md` §2·§3
- 워커 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스/orchestration/work/llm-codex-hotfix/be-hotfix-report.md`

## 2. 배경

조직 차단으로 서버 claude 호출이 전부 실패 중. B(결정 게이트)·C(데일리 브리프)·D(주간보고)를 codex 로 바꾸는 main 핫픽스다. **사용자 결정: 테스트 작성·실행 생략**(기존 claude 단정 테스트가 깨지는 건 알고 둔다 — 지적하지 마라). 수용은 배포 후 운영 실물 호출로 한다.

## 3. 계약

해당 없음 (BE 단독). 기준은 WP-133 대응표.

## 4. 검수 항목 (`git diff origin/main` + untracked)

1. **선례 일치** — `server_llm_submission.py` 의 조립이 `meeting_v2_submission.py`(`build_submission`·`_config_overrides`·`compose_prompt`·`redact_config_overrides`)와 같은 모양인가. TOML 따옴표·`enabled_tools` 형식·툴별 `approval_mode` 키 경로가 선례와 글자 단위로 같은가.
2. **codex 분기에 claude 전용 키 0** — `system_prompt`·`max_turns`·`effort`·`mcp_config`·`allowed_tools`·`disallowed_tools`·`json_schema` 가 codex 제출 provider_options 에 실리지 않는가(B·C·D 각각).
3. **claude 분기 보존** — `SERVER_LLM_PROVIDER=claude` 일 때 B·C·D 제출 인자가 `origin/main` 의 구 인자와 **바이트 동일**한가(provider 값만 설정값으로 바뀐 것 외).
4. **경로별 값** — B: 7종 allowlist(접두어 없음)·effort low·timeout 그대로 / C: 4종·medium·600 / D: MCP 없음·low·300. queue 그대로. 모델 해석값 빈 값 → None.
5. **B′ 호환** — `pipeline_ingest_consumer` 의 partial(`max_turns`·`timeout_sec`)이 codex 분기에서 깨지지 않는가.
6. **결과 처리 불변** — 각 경로의 `task.status`·결과 파싱·에러 처리·redact(C `_redact_tokens`)가 그대로인가. codex 경로의 프롬프트가 system+user 합성으로 바뀐 것 외에 동작 변화가 없는가.
7. **비밀 유출** — `internal_auth_secret` 이 로그·에러·DB 에 평문으로 남는 경로가 없는가(바이트 로그의 redact 포함).
8. **런타임 위험** — import 순환(config ↔ server_llm_submission ↔ meeting_v2_submission), 잘못된 속성명, async 오용 등 테스트 없이 배포될 때 터질 지점을 코드 읽기로 찾아라. 필요하면 `python -m py_compile`·import 1회는 해도 된다(pytest 금지).
9. 범위 — `back/app/` 밖 변경 0, A(`action_runtime/llm/driver.py`)·mcp·테스트 무수정.
10. **실물에서 만날 자리** — 배포 후 첫 실호출에서 사람이 볼 이상 징후(예: 브리프 본문 펜스, 프롬프트 바이트 E2BIG 근접)를 짚어라.

## 5. allowed_paths — 이 밖은 건드리지 마라

- read-only. 산출물은 리포트 1개: `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스/orchestration/work/llm-codex-hotfix/review-code-report.md`

## 6. 구현 단계

1. SSOT 읽기 → 2. diff 대조 → 3. 리포트(판정 PASS/WARN/FAIL · 위반 목록 파일:줄 + 근거 + 수정 제안 · 실물 체크포인트).

## 7. 범위 제약 — 하지 말 것

- 파일 수정 금지. pytest·스택 기동·운영 접속 금지. 테스트 미작성은 지적 대상이 아니다(사용자 결정).

## 8. 검증

```
리뷰는 read-only — 코드를 고치지 않고 테스트도 돌리지 않는다. git diff origin/main...HEAD + git diff + untracked 로 범위를 산정하고, 판정(PASS/WARN/FAIL)과 위반 목록(파일:줄 + 근거 규칙)을 리포트에 남긴다
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_4d39f44d-7335-41dc-bd4a-b274304b05d9 --from term_d626f8c9-8298-4e5c-9a9f-a33f6c117839 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_code_hotfix 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_4d39f44d-7335-41dc-bd4a-b274304b05d9 \
  --text "[worker_done] reviewer_code_hotfix 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_4d39f44d-7335-41dc-bd4a-b274304b05d9 --text "[질문] reviewer_code_hotfix: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)

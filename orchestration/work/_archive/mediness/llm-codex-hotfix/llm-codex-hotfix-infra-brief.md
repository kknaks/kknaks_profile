
# [infra] 운영 배포 기준 — 서버가 claude CLI 를 어디서 쓰는지 실측 (read-only 조사)

너는 **mediness `infra` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스/orchestration/roles/mediness/infra/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/llm-codex-hotfix`
base 브랜치: `origin/dev` — **이번 판은 조사만 한다. 코드·설정을 바꾸지 않는다.**
운영(prod)은 `main` 에서 배포된다. 코드를 볼 때는 `git show origin/main:<경로>` 로 main 을 기준으로 본다.

너는 앞 맥락이 없다. 이 브리프만으로 일한다.

## 1. SSOT — 먼저 읽을 것

- `git show origin/main:DEPLOY.md` — 특히 §4-4 「AX LLM 드라이버 전환 (claude → codex)」
- `git show origin/main:back/app/config.py` — `llm_vendor`(85행 근처) · `meeting_llm_provider`(264행) · `action_runtime_llm_driver`(496행)
- `git show origin/main:back/Dockerfile.worker` — worker 가 claude/codex 실행 파일을 노드 마운트로 받는 방식

**기대는 개념** — 해당 없음. 대신 원칙: **설정값은 코드 기본값이 아니라 실제 떠 있는 파드에서 읽은 값이 정답이다.**

## 2. 배경 / 무엇을 알아내나

사용자가 서버의 LLM 호출을 **claude → codex 로 핫픽스 전환**하려 한다. 코디가 코드만 보고 claude 를 부르는
서버 경로를 아래 6개로 추렸지만, **운영 env 로 무엇이 실제로 켜져 있는지는 아무도 확인하지 않았다.**
네 일은 **운영(prod) 배포 기준으로 지금 claude 를 실제로 쓰는 경로를 전부** 가려내는 것이다.

코디가 코드에서 찾은 서버 쪽 후보 (origin/main):

| # | 경로 | 코드상 claude 여부를 가르는 값 |
|---|---|---|
| A | AX 비서 파싱·분류 — `back/app/services/action_runtime/llm/driver.py` (back 프로세스 안에서 `claude -p` 직접 spawn) | env `ACTION_RUNTIME_LLM_DRIVER` (기본 `claude`) |
| B | 결정 게이트 `decision_gate.py:651 _default_ai_call` + 이를 재사용하는 `pipeline_ingest_consumer.py _default_analyze` | 코드 고정 `provider="claude"` · `llm_vendor=="open_kknaks"` 일 때만 실호출(`main.py:95`) |
| C | 브리프 합성 `services/brief/synthesizer.py:556` | 코드 고정 `provider="claude"` |
| D | 주간 보고 `services/weekly_report_pipeline.py:515` | 코드 고정 `provider="claude"` |
| E | 회의록 v2 `meeting_v2_extractor.py:449,511` | env `MEETING_LLM_PROVIDER` (기본 `codex`) |
| F | 랜딩 채팅 `landing_chat/submission.py:212` | 코드 고정 `provider="codex"` |

사용자 PC 데몬 `agent/` 는 **범위 밖**이다(개인 로컬). 보지 마라.

후보 목록을 믿지 말고 **전수조사**하라 — `git grep -nE 'provider=|create_subprocess_exec|subprocess|\.submit\(' origin/main -- back/ mcp/` 로 호출처를 직접 세고, 목록 밖에서 claude 를 부르는 곳이 있으면 추가하라.

## 3. 계약

해당 없음 (조사).

## 4. 조사 대상 — 운영 실물

접속은 `ssh medi-me`, kubectl 은 **절대경로** `/opt/homebrew/bin/kubectl` (비대화 ssh 는 PATH 가 최소). namespace `mediness-prod`.
GitOps 레포 `MediSolveAIDev/k8s_infra_mac` 의 `charts/mediness`(values-prod.yaml · worker.yaml) 도 참고 — `gh` 로 읽어라.

알아낼 것:

1. **배포 버전** — prod 각 deployment 의 이미지 태그 sha 가 `origin/main` 의 어느 커밋인지.
2. **deployment 목록** — back · worker · mcp · 그 외 무엇이 떠 있는지. 각각 **claude / codex 실행 파일이 PATH 에 있는지**(`kubectl exec ... -- sh -c 'command -v claude; command -v codex'`), `/opt/claude` 마운트 여부.
3. **env 값** — 각 deployment 에서 아래 키의 **값**(비밀이 아닌 것) / **존재 여부만**(비밀):
   - 값: `LLM_VENDOR` · `MEDINESS_LLM_VENDOR` · `MEETING_LLM_PROVIDER` · `MEETING_CODEX_MODEL` · `ACTION_RUNTIME_LLM_DRIVER` · `ACTION_RUNTIME_CLAUDE_MODEL` · `CODEX_HOME` · 그 외 `*PROVIDER*`·`*VENDOR*`·`*DRIVER*`·`*LLM*` 키 전부
   - 존재 여부만: `CLAUDE_CODE_OAUTH_TOKEN` · `ANTHROPIC_API_KEY` · `ANTHROPIC_AUTH_TOKEN` · `OPENAI_API_KEY` · codex 자격증명 파일(`$CODEX_HOME/auth.json` 등)
4. **실제 호출 흔적** — read-only 로만:
   - DB `llm_calls` 원장: `select provider, estimated, count(*), max(created_at) from llm_calls where created_at > now() - interval '7 days' group by 1,2;` (스키마가 다르면 컬럼을 확인하고 맞춰라)
   - worker 로그(`kubectl logs` 최근 분량)에서 provider 별 task 실행 흔적 — claude / codex 가 각각 어느 경로(회의·게이트·브리프·주간보고·랜딩)에서 돌았는지
   - 경로 B·C·D 가 운영에서 **실제로 켜져 있는지**(스케줄러 등록·트리거 조건·feature flag). 꺼져 있으면 claude 를 안 쓰는 것이다.
5. 각 경로별 결론: **운영에서 지금 claude 를 쓰나 / codex 를 쓰나 / 꺼져 있나**, 그리고 codex 로 바꾸려면 **env 변경만으로 되나 / 코드 수정이 필요하나**.
6. (참고) 같은 1~4 를 `mediness-dev` 에도 짧게 — prod 와 다른 점만.

## 5. allowed_paths — 이 밖은 건드리지 마라

- **read-only.** mediness-app 레포·GitOps 레포·클러스터·DB 어디에도 쓰기 금지.
- 산출물은 **리포트 파일 1개만**: `/Users/kknaks/orca/workspaces/kknaks_profile/메디니스/orchestration/work/llm-codex-hotfix/survey-prod-claude-usage.md`

## 6. 구현 단계

1. §1 문서 읽기 → §2 전수 grep 으로 후보 확정
2. §4 의 1~4 실측
3. 리포트 작성 — 형식:
   - 요약 표: 경로 | 실행 위치(pod) | 운영 현재 provider(근거) | codex 전환 방법(env/코드) | 근거(명령·출력 발췌)
   - 배포 sha · deployment별 CLI 유무 · env 표(비밀은 「있음/없음」)
   - `llm_calls` 집계 결과 원문
   - 후보 목록 밖에서 새로 찾은 것
   - 확인 못 한 것과 이유 (추측으로 메우지 마라 — 「확인 못 함」이라고 적는다)

## 7. 범위 제약 — 하지 말 것

- **비밀값을 출력·리포트에 남기지 마라.** 토큰·키는 존재 여부만. `env` 전체를 찍지 말고 `grep` 으로 키를 골라 비밀 키는 `sed 's/=.*/=<있음>/'` 처리.
- 파드 재시작·rollout·exec 로 쓰기·DB 쓰기·env 변경·ArgoCD sync 금지.
- 코드 수정·커밋·PR 금지. 핫픽스 설계·구현은 이번 판이 아니다.
- `agent/`(사용자 PC 데몬) 조사 금지.

## 8. 검증

```
리포트의 모든 「운영에서 claude 사용」 판정에 근거(명령 + 출력 발췌)가 붙어 있는지 스스로 대조.
grep -nE '(sk-|sk-ant-|eyJ)[A-Za-z0-9_-]{10,}' <리포트>  → 0 건이어야 한다 (비밀값 유출 검사)
```

- 확인 못 한 항목은 이유와 함께 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_4d39f44d-7335-41dc-bd4a-b274304b05d9 --from term_dd2f12cb-195c-40ee-ae67-7cadfce68bf3 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "infra 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_4d39f44d-7335-41dc-bd4a-b274304b05d9 \
  --text "[worker_done] infra 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_4d39f44d-7335-41dc-bd4a-b274304b05d9 --text "[질문] infra: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)

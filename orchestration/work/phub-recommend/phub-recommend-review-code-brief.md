
# [reviewer_code] Hub 데이터 그래프 + REST · MCP 구현 검수 (WORK-001 Phase 1~7)

너는 **procedure-hub `reviewer_code` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend`
base 브랜치: `origin/release/v1.2.0` → 최종 PR 대상 `release/v1.2.0` (PR 은 코디네이터가 올린다)

backend 워커가 끝낸 워크트리다. read-only — 파일을 고치지 말고, 브랜치 · 커밋도 건드리지 마라.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/SPEC-001.md` (v0.2.1) · `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/WORK-001.md` ← 계약
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/DEC-001.md` ← D-05 · D-06 · D-12 · D-13c
- 레포 기준: 워크트리 `AGENTS.md`(첫 줄 `/Users/marin/...` 무시) · `.agents/skills/be-reviewer/` · `.agents/skills/task-checker/`
- backend 워커 완료 보고: 코디가 dispatch 때 이 아래 §3 에 붙인다

## 2. 배경

사용자가 다음 날 이 브랜치를 로컬에서 E2E 한다. 이 검수가 코드 쪽 마지막 게이트다.

## 3. 계약 · 워커 보고

backend 완료 보고 요약(2026-10-26):
- 수정 기존 파일: `backend/app/model/__init__.py`(graph import 1문) · `pyproject.toml`(mcp>=2.3,<3 · httpx runtime) · `uv.lock`(mcp 2.3.0, 전이 idna 3.11→3.20)
- 신규: `app/graph_main.py` · `app/modules/graph/*` · `app/router/graph.py` · `app/schema/graph.py` · `app/swagger_docs/graph.py` · `app/model/graph.py` · `alembic/versions/b202610260001_graph_schema.py` · `scripts/graph_{ingest,build,e2e_check}.py` · `graph-local.compose.yml` · `envs/graph.env.example` · `docs/graph-local.md` · `tests/conftest.py`(**신규 — SPEC 허용 목록에 있는지, 기존 테스트에 영향 없는지 확인**) · `tests/graph_support.py` · `tests/test_graph_*.py` · `tests/integration/test_graph_stg_snapshot.py` · `tests/fixtures/graph/*.json`
- 워커 실측: 노드 941 · 엣지 1,504 · conflict 7 · E2E 76/76 · pytest 422 passed · alembic up/down/up diff 0
- **워커가 SPEC 밖에서 고른 것(판정 대상)**: ① procedure.attributes.group_id 를 노드 id 로 ② minimum_intervals 원천 문자열을 `cited_source` 로 ③ procedure_relation 주장에 `kind` 추가 ④ search limit ≤100 · neighbors limit ≤1000 ⑤ validation build=latest 처리(보고 잘림 — 코드에서 확인)

## 4. 볼 것

1. **SPEC 대조** — 노드 · 엣지 규칙(특히 §3.3 세 규칙 · CC 동률 · subgraph direction · safety 포함 규칙 R1) · 응답 shape · 검증 코드 · 발행 규칙이 SPEC 과 같은가
2. **DEC 경계** — 모델 · LLM 호출 0(D-12), 레거시 · canonical 모델 · 서비스 import 0(D-13c), 큐레이션 비병합, 정규화 완전 일치 외 매칭 0
3. **기존 앱 회귀** — 기존 파일 수정이 SPEC 허용 목록(`app/model/__init__.py` · `pyproject.toml` · `uv.lock`) 안인가. 기존 공개 API 계약 테스트가 그대로인가. 새 마이그레이션이 기존 baseline 위에 단일 head 인가
4. **레포 규칙** — be-reviewer 기준(계층 · DI · 트랜잭션 · 예외)
5. **테스트** — stg 를 부르지 않는가, SPEC E2E 기대값을 fixture 로 고정한 테스트가 있는가
6. **사용자가 실물에서 만날 자리** — 로컬 실행 문서대로 따라 하면 막히는 곳 · 응답이 이상해 보일 곳

## 5. allowed_paths

- 생성: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/review-code-report.md` **1개만**(코디 워크트리 쪽 절대경로). 코드 워크트리에는 아무것도 만들지 않는다

## 6. 구현 단계

1. `git -C <워크트리> diff origin/release/v1.2.0...HEAD` + `git status --short`(미커밋 · untracked 포함)로 범위를 센다
2. 위 축마다 지적을 `파일:줄 + 근거(SPEC 절 · DEC D · 스킬 규칙)`. FAIL / WARN 구분
3. 맨 위 종합 판정과 FAIL 목록

## 7. 범위 제약

- 코드 수정 · 테스트 실행 · 서버 기동 금지(read-only). 사용자 포트 · 컨테이너 금지
- 취향 지적 금지

## 8. 검증

```
git diff <base>...HEAD + untracked 로 범위 산정. 각 지적에 파일:줄 + 근거(SPEC 절 · WP · AGENTS.md 스킬 be-reviewer/fe-convention-reviewer 기준). 판정 FAIL/WARN/PASS. 「사용자가 실물에서 만날 자리」를 따로 모은다
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_92a9e861-40e9-4ab0-bec1-e792cb83801e --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_code 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_92a9e861-40e9-4ab0-bec1-e792cb83801e \
  --text "[worker_done] reviewer_code 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_92a9e861-40e9-4ab0-bec1-e792cb83801e --text "[질문] reviewer_code: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)

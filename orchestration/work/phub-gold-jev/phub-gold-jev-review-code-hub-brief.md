# [reviewer_code] 허브 코드 검수 — WORK-001 구현

너는 **procedure-hub `reviewer_code` 워커**다(read-only). **앞 판의 맥락이 없다.** 역할 문서(절대경로): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/roles/procedure-hub/reviewer/role.md`(+ 같은 폴더 파일) · 레포 `AGENTS.md` · `.agents/skills/be-reviewer`.

검수 워크트리: `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(branch `kknaksss/phub-gold-jev` · base `origin/release/v1.2.0` · 커밋 없음 — 변경은 작업 트리에만). **파일을 고치지 마라 · stash · checkout 금지.**

`P=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온` · `W=$P/orchestration/work/phub-gold-jev` · `SM=$P/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model`

## 읽을 것

- 계약: `$W/SPEC-001-hub-gold-mcp.md`(0.4.1) · `$W/WORK-001-hub.md`(0.2.0) · `$W/_RESUME.md` §2
- 구현 보고 요지: 변경 = `backend/app/modules/gold/*` 18 · `router/gold.py` · `swagger_docs/gold.py` · `gold_main.py` · 시험 8 · `pyproject.toml` · `uv.lock` · `envs/.env.example` · `README.md`. 주의점: WORK §6 단계 1(T4 입구) 문구와 다르게 entry_text ∪ question 으로 · mcp 2.3.0 은 ToolError 대신 is_error · 쪽 밖 목록은 첫 쪽에만 · offer 대상 쪽 행 중복(layer 다름) · GOLD_MCP_RESULT_MAX_CHARS 1,000,000

## 볼 것

1. `git diff origin/release/v1.2.0` + untracked 로 범위 산정 — allowed_paths(`backend/`) 밖 0 · 기존 코드(`app.main` · core · alembic · Dockerfile) 변경 0 · CSV 커밋 0.
2. SPEC-001 계약 대조 — 도구 8 입력 · 출력 필드(부록 A) · 오류 · cursor · 응답 머리 · 계층(repository 만 바꾸면 DB 로) · 허브에 LLM 없음 · **폭이 줄어드는 자리 0**(limit = 쪽 크기 · 상한 · 상위 N 없음).
3. 구현 보고 주의점 ②~⑩ 각각이 SPEC 과 부딪히나(⑤ 행 중복은 SPEC 규칙상 맞는지 · 접어야 하는지).
4. 시험 — 직접 한 번 돌려라: `cd backend && DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest -q tests/test_gold_*.py`(데이터 env 없이) 와 README 「gold 로컬 실행 · 검증」 절의 데이터 env 판 1회. 수치를 리포트에.
5. 실서버 확인은 **코디가 18105 에 띄워 둔 것**으로만(띄우거나 내리지 마라): REST 몇 개 · MCP 1개.
6. be-reviewer 기준(계층 · 예외 · 의존). 「사용자가 실물에서 만날 자리」(앱 · 다른 서비스가 부를 때 헷갈릴 것)를 따로 모아라.
7. 공개 레포 아님(회사 레포)이지만 비밀값 · 회사 데이터 본문이 코드 · 시험에 하드코딩됐는지 grep.

## 산출

`$W/review-code-hub.md` 1개만. 판정 PASS/WARN/FAIL + 지적 표(파일:줄 · 심각도 · 근거 SPEC 절 · 고칠 방향).

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_95e86b96-831a-4d31-aa96-58649a80d244 --from term_c52e6fee-ee18-4782-8089-3b74e08db13d \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_code 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_95e86b96-831a-4d31-aa96-58649a80d244 \
  --text "[worker_done] reviewer_code 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_95e86b96-831a-4d31-aa96-58649a80d244 --text "[질문] reviewer_code: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)

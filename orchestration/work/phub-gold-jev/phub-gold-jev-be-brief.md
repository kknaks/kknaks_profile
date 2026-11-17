# [backend] 허브 — 새 gold 메모리 적재 · 도구 8 · REST · MCP (WORK-001 전체)

너는 **procedure-hub `backend` 워커**다. **앞 판의 맥락이 하나도 없다** — 아래 「읽을 것」만으로 일한다. 먼저 역할 문서를 읽어라(절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/roles/procedure-hub/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- 코드 레포 규칙: 작업 워크트리의 `AGENTS.md`(첫 줄이 가리키는 `/Users/marin/AGENTS.md` 는 이 머신에 없다 — 무시) · `.agents/skills/be-reviewer` · `backend/README.md` 「검증」 절

작업 워크트리: `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev` (branch `kknaksss/phub-gold-jev`, base `origin/release/v1.2.0`) — 이 워크트리는 너 혼자 쓴다.

## 1. SSOT — 먼저 읽을 것

`P=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온` · `W=$P/orchestration/work/phub-gold-jev` · `SM=$P/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model`(로컬 데이터 · 읽기만)

- `$W/WORK-001-hub.md`(0.2.0) ← **구현 계획. WP-1 → WP-4 순서 · 완료 조건 · 검증 명령 그대로**
- `$W/SPEC-001-hub-gold-mcp.md`(0.4.1) ← **계약. 여기 없는 건 발명하지 마라.** 부록 A = 출력 필드 ↔ CSV 헤더
- `$W/_RESUME.md` §2 ← 결정(DB 없음 · repository 만 바꾸면 DB 로 갈 수 있게 · 허브에 LLM 없음 · 로컬 시험까지)
- 옛 틀(읽기만 · `git show HEAD:`): `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend` — WORK-001 이 가리키는 파일:줄만

**코디 확정(WORK 검수 뒤)**: WORK-001 의 N1-1 은 제안 (a) 로 간다.

**기대는 개념**: `$P/para/areas/concept/cs/artifact-traceability.md` — 모든 응답 행이 gid → g_evidence → silver → source_ref 로 되짚힘.

## 2. 배경

새 silver 57 · gold 15 를 허브에 처음부터 연결한다. 허브는 결정론 조회만(LLM 없음). 앱(clinic_chat · 다른 워커가 병행)이 REST(걷기)와 MCP(LLM 직접)로 부른다.

## 3. 계약

SPEC-001 §4(도구 8) · 부록 A 그대로. 앱 워커는 이 계약만 보고 클라이언트를 짓는다 — **계약을 바꾸고 싶으면 코디에게 먼저 물어라**(아래 §9 질문).

## 4. 먼저 읽을 핵심 파일

WORK-001 각 WP 의 「옛 틀에서 가져올 것」 · 「만들 파일」 표.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `backend/` 안에서 WORK-001 이 정한 새 파일 · 의존 추가(`pyproject.toml` · `uv.lock`)만. 기존 앱 코드(`app/main.py` 등)는 WORK-001 이 고치라고 한 곳만.
- **gold · silver CSV 를 레포에 복사 · 커밋하지 마라** — 데이터는 env 경로로(WORK-001 §데이터 env). 회사 데이터 본문을 테스트 기대값으로 하드코딩하지 마라(데이터 env 없으면 skip).

## 6. 구현 단계

WORK-001 WP-1 → WP-2 → WP-3 → WP-4. **WP-3(로컬 서버 18105 에서 health · 도구 응답)이 끝나면 완료 보고 전에 코디에게 한 줄 알려라**(§9 의 (2) 방식으로 `[진행] backend: WP-3 서버 준비 — 실행 명령 <…>`) — 앱 워커가 실물 연결을 시작한다. 그 뒤 WP-4 를 이어 간다.

## 7. 범위 제약 — 하지 말 것

- 커밋 · push · PR 금지(코디 몫). stg · 배포 · 개발/운영 DB · 사용자 포트(18005 · 18210 등) 금지 — 너의 로컬 확인은 18105 에서 띄웠다가 **끝나면 내린다**.
- SPEC · WORK 문서를 고치지 마라(구멍은 보고).
- 옛 PR #31 워크트리 · 옛 gold 모듈을 import 하지 마라(틀만 옮겨 다시 쓴다).

## 8. 검증

```
cd backend && uv run ruff check <네가 만진 파일> · DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest -q <네가 만들거나 고친 테스트 파일만> (tests/integration 제외) — 각 1회, 통과하면 반복하지 마라. 마이그레이션을 만들었으면 alembic 이 빈 DB 에 올라가는지 확인. 사용자 포트·프로세스·개발/운영 DB 를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending 으로 보고
```

- 데이터 env 를 준 판으로 WP-4 의 37 문항 되짚기 · T1 ~ T14 결과 수치를 보고한다.
- 로컬 서버를 실제로 띄워 도구 8 을 REST · MCP 로 각 1회 이상 불러 응답 머리(`build.gold_hash`)가 `8accbb21…` 인지 확인 → 내린다.
- 끝에 `git -C <워크트리> status --porcelain` 로 변경 범위 보고.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_95e86b96-831a-4d31-aa96-58649a80d244 --from term_1841b11d-7f4e-4206-98a2-eab5c34cc5ae \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_95e86b96-831a-4d31-aa96-58649a80d244 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_95e86b96-831a-4d31-aa96-58649a80d244 --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)

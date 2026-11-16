
# [backend] WORK-001 Phase 1~7 — Hub 데이터 그래프 + REST · MCP 조회 tool (로컬 E2E 1차)

너는 **procedure-hub `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend`
base 브랜치: `origin/release/v1.2.0` → 최종 PR 대상 `release/v1.2.0` (PR 은 코디네이터가 올린다)

이 워크트리는 너 혼자 쓴다. 브랜치 `kknaksss/phub-recommend` 는 **로컬 전용** — 커밋 · push 하지 마라(회사 org 레포).

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/SPEC-001.md` ← **계약의 SoT. 여기 없는 건 발명하지 마라.**
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/WORK-001.md` ← Phase 순서 · 완료 기준 · 테스트 · 검증 명령. 이대로 간다
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/review-spec-001-report.md` ← 문서 검수 결과. **코디가 반영 지시를 §3 에 적는다 — §3 가 SPEC 보다 우선**
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/DEC-001.md` ← 결정 배경(D-12 Hub 에 LLM 없음 · D-13c 레거시/canonical 미접촉)
- 레포 규칙: 워크트리 루트 `AGENTS.md`(첫 줄 `/Users/marin/AGENTS.md` 는 다른 머신 경로 — 무시) · `.agents/skills/be-reviewer/` · `backend/README.md`

**기대는 개념** — `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/areas/concept/db/medallion-architecture.md` — 레이어 사이 의존 방향(골드/tool 은 브론즈 원본을 직접 읽지 않는다)을 코드 구조로 지킨다

## 2. 배경

Procedure Hub 위에 결정론 데이터 그래프(브론즈 → 실버 → 시맨틱 → 발행)와 읽기 전용 조회 tool(REST + MCP)을 세운다. 사용자가 **다음 날 로컬에서 E2E** 한다. LLM 은 이번 범위에 없다.

## 3. 계약 — 문서 검수 반영 지시

- 문서 검수 2회(`review-spec-001-report.md` FAIL 7 → `review-spec-001-v2-report.md` F1~F7 PASS · 회귀 R1) 를 거쳐 **SPEC-001 v0.2.1 · WORK-001 이 최종본**이다. R1 · WARN-n 반영은 코디가 diff 로 확인했다
- 추가 지시 없음 — **SPEC 그대로** 구현한다. 두 리포트는 「왜 이렇게 됐나」를 볼 때만 참고
- 기대값(노드 941 · 엣지 1,504 · procedure_relation 106 · conflict 7 · S-1 16/34 …)은 2026-10-26 stg 응답 기준이다. Phase 7 실측에서 stg 가 바뀌어 숫자가 다르면 **규칙을 바꾸지 말고** 차이와 원인을 보고한다

## 4. 먼저 읽을 핵심 파일

- SPEC-001 · WORK-001 이 가리키는 파일:줄 전부(관례 원본)
- `backend/tests/test_public_api_contract.py` — 기존 공개 API 동결. 깨면 안 된다

## 5. allowed_paths — 이 밖은 건드리지 마라

- `backend/` (SPEC-001 「위치」 절이 정한 새 파일 + 그 절이 허용한 기존 파일 수정만 — `app/model/__init__.py` import · `pyproject.toml` · `uv.lock`)
- 레거시 · canonical 모델 · 서비스 · 라우터 · 기존 마이그레이션은 **수정 금지**

## 6. 구현 단계

WORK-001 Phase 1 → 7 순서. Phase 마다 그 Phase 의 테스트만 돌리고 넘어간다. **전체 검증은 Phase 7 끝에 1회.**
Phase 7 실측: `phub-graph-` 접두 컨테이너로 PostgreSQL 55434 · API 18005 를 띄워 stg 적재 → 빌드 → 발행 → E2E 시나리오 S-1~S-7 을 REST 와 MCP 로 각 1회. 결과 수치를 보고에 넣고, **끝나면 API 프로세스는 내린다**(DB 컨테이너 · 볼륨은 남겨 둔다 — 코디가 재확인한다).

## 7. 범위 제약 — 하지 말 것

- 커밋 · push · PR 금지. 브랜치 전환 금지
- 사용자 포트 · 컨테이너(3700 · 3800 · 8700 · 8800 · 54329 · `procedure-*` · `interpret-pwa-*` · `strong-hajin-*`)를 건드리지 않는다
- 개발 · 운영 DB 접속 금지. stg 는 Phase 7 적재 1회(GET)만
- 모델 호출(LLM · Jev) 코드 금지(D-12)
- SPEC 과 실물이 다르면 혼자 고치지 말고 질문으로 묻는다(§9 질문 방식)

## 8. 검증

```
cd backend && uv run ruff check <네가 만진 파일> · DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest -q <네가 만들거나 고친 테스트 파일만> (tests/integration 제외) — 각 1회, 통과하면 반복하지 마라. 마이그레이션을 만들었으면 alembic 이 빈 DB 에 올라가는지 확인. 사용자 포트·프로세스·개발/운영 DB 를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending 으로 보고
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
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_92a9e861-40e9-4ab0-bec1-e792cb83801e \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_92a9e861-40e9-4ab0-bec1-e792cb83801e --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)

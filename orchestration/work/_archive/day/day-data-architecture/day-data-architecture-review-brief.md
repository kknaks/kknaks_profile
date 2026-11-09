
# [reviewer] Delivery #224 백엔드 뼈대 — 코드 검수

너는 **day `reviewer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-data-architecture`
base 브랜치: `origin/v2-dev` → 최종 PR 대상 `v2-dev` (PR 은 코디네이터가 올린다)

**읽기 전용 검수다.** 같은 워크트리에 backend 워커가 만든 미커밋 변경(`git status` — `AGENTS.md` 수정 · 나머지 신규)이 있다. 고치지 마라 — 지적만 한다. 너는 앞 맥락이 없다 — 아래 순서대로 읽어라.

## 1. SSOT — 먼저 읽을 것

- **계약 = GitHub Delivery Issue #224** — `gh issue view 224 -R MediSolveAIDev/CENTURION_DAY` (「바뀌는 것」 · 「이번에 하지 않는 것」 · 완료 조건 A1 ~ A5). **여기 없는 건 발명하지 마라.**
- 레포 규칙 = `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-data-architecture/AGENTS.md`(워크트리 판 · `git diff AGENTS.md` 로 바뀐 곳도 본다) — 구조 · 계층 · 백엔드 안전 · 테스트 · 작업 규칙
- 시스템 결정 = `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/system/README.md` — taskiq + Redis 브로커 · `DB_SCHEMA` 로 환경 분리(dev `day_dev` / prod `day_prod`) · DB 1개(CREATE DATABASE 권한 없음)
- 구현 리포트 = `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/backend-224-report.md` — 워커가 주장하는 것. **주장을 믿지 말고 코드로 확인해라.** 「이슈 · 코디가 확인할 것」 1 ~ 8 은 판정을 내려라(받아들임 / 고칠 것).
- 기대는 개념: 해당 없음

## 2. 배경 / 무엇을 바꾸나

DAY v2 를 빈 `v2-dev` 위에 처음 세운 뼈대다 — 서버 · 설정 · DB 연결 · alembic · taskiq 자리 · import 경계 테스트. 다음 Delivery(#225 데이터 모델 · #226 KOS 연동 · #227 로그인)가 이 위에 쌓이므로, **지금 잘못 놓인 자리는 뒤 세 개가 그대로 물려받는다.** 그 관점으로 본다.

## 3. 계약

처음 생기는 외부 계약: 헬스체크 경로(`/health/live` · `/health/ready`) · task name(`day.ping`) · 큐 이름 · 진입점. AGENTS.md 「API 경로 · task name · migration 은 외부 계약」.

## 4. 먼저 읽을 핵심 파일 · 대조할 본

- 워크트리 전체: `git -C <워크트리> status` · 신규 파일 전부
- centurion(모양 본 · 읽기만): `git -C /Users/kknaks/git/centurion show origin/main:<경로>` — `backend/runtime/main.py` · `backend/common/config.py` · `backend/common/db/session.py` · `model_base.py` · `backend/migrations/centurion/env.py` · `backend/linky/tasks/broker.py` · `deploy/compose.local.yaml` · `docs/development/backend-reliability.md` · `testing-strategy.md`

## 5. allowed_paths — 이 밖은 건드리지 마라

- `(read-only — 리포 파일 수정 금지. 산출물은 브리프가 지정한 리포트 파일 1개뿐)`

## 6. 볼 것

1. **계약 대조** — A1 ~ A5 · 「바뀌는 것」 각 줄 · 「하지 않는 것」을 넘지 않았는지(업무 테이블 · KOS · 로그인 · 화면이 새어 들어왔는지).
2. **DB_SCHEMA** — `MetaData(schema)` · alembic `version_table_schema` · `search_path` · 테스트 스키마가 **같은 한 값**에서 오는지. 스키마 이름이 SQL 에 그대로 들어가는 자리의 검증. `APP_ENV` ↔ `DB_SCHEMA` 가드. 스키마가 없을 때(첫 migrate) 누가 만드는지 · 관리형 DB 권한(CREATE SCHEMA 는 되나 CREATE DATABASE 없음)과 맞는지.
3. **경계 테스트** — 진짜로 깨지는지(예외 `migrations` 가 정당한지 · 너무 넓지 않은지). 검사기가 놓치는 import 형태가 있는지.
4. **자리** — `Base` 를 `common/db` 에 둔 것 · 브로커를 `common/tasks` 에 둔 것이 AGENTS.md 트리(`day/db.py` 에 Base/세션 · `day/tasks/`)와 어긋나는지, #225 · #226 이 물려받을 때 문제인지.
5. **백엔드 안전** — 세션 수명 · lifespan 정리 · timeout · 동기 I/O · 비밀값 노출(로그 · 헬스 응답 · 예외 문구) · `SecretStr`.
6. **테스트** — 실제 PostgreSQL · Redis 로 도는지, 테스트가 `day_dev` 를 건드리지 않는지, skip 이 조용히 통과를 만들지 않는지(인프라 없을 때 skip 5개가 CI 에서 「통과」로 보일 위험).
7. **비밀값** — 커밋 대상에 실제 값 0. `.gitignore` 가 `deploy/local.env` 를 막는지.

직접 돌려 봐도 된다: `scripts/test.sh -q` · `uv run ruff check backend`. compose 를 띄우면 **포트 11040 · 11042 · 11043** 만, 끝나면 `down`(볼륨은 둔다). 사용자 포트 · 컨테이너는 건드리지 마라.

## 7. 범위 제약 — 하지 말 것

- 파일 수정 · 커밋 · push · PR 금지. 산출물은 리포트 1개.
- 계약에 없는 기능을 「있어야 한다」로 FAIL 주지 마라 — 범위 밖이면 WARN 이나 「다음 Delivery 몫」으로.

## 8. 검증

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-224-report.md` — 판정(PASS · WARN · FAIL) · 지적마다 파일:줄 + 근거(Issue 항목 · AGENTS.md 절) + 고칠 방향 · 리포트 「코디가 확인할 것」 1 ~ 8 판정 · 직접 돌린 명령과 수치.

```
각 지적에 파일:줄 + 근거(SPEC 절 · DEC D-번호). 판정 FAIL · WARN · PASS. 「조용히 통과하는 자리」를 따로 본다
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
  --to term_70b6f193-86a2-4c1d-8965-4e2220cef9b3 --from term_ad2a4487-a45e-4f07-bd10-b6fa67936898 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: #224 코드 검수" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_70b6f193-86a2-4c1d-8965-4e2220cef9b3 \
  --text "[worker_done] reviewer 완료 — #224 코드 검수. 리포트 work/day-data-architecture/review-224-report.md" --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_70b6f193-86a2-4c1d-8965-4e2220cef9b3 --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)

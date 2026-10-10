# [backend] 알림 구현 — WORK-013 Phase WP1-BE (이후 Phase 는 지시서로 이어 받는다)

너는 **strong-hajin `backend` 워커**다. 이 워크트리에서 조사(`be-survey-report.md`)를 한 그 워커일 수 있다 — 이제 **구현**이다. 맥락이 없으면 아래를 먼저 읽어라:

- 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/roles/strong-hajin/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- 코드 레포 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-notify/AGENTS.md`
- 조사 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/be-survey-report.md`

경로 약어: `P/` = `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/summer-star/strong-hajin/` · `W/` = `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/`

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-notify` (branch `kknaksss/strong-hajin-notify`, base `origin/main` `d2a06fa`)

⚠ frontend 워커가 같은 워크트리에서 **P0 조사(읽기 전용)** 중이다 — `frontend/` 는 건드리지 마라

## 1. SSOT — 계약 (여기 없는 것은 발명하지 마라)

- **실행 계획 — 이번 판의 할 일 목록**: `P/30-work/work-013-notifications.md` **「Phase WP1-BE」 절**(계약 체크박스 · 완료 조건 · 시험) + 「이 판의 원칙」 P-1~P-10 + 「Code Surface — 전수 grep 개수표」 의 **WP1 표**(닿는 곳 전부)
- **계약**: `P/20-spec/spec-011-notifications.md`(v0.2.2) **§4.1** · `P/20-spec/spec-008-external-channels.md`(v0.7.0) §4.4
- 결정: `P/10-decision/decision-010-notifications.md`

**기대는 개념** — `para/areas/concept/cs/server-sent-events.md` · `back/per-user-fanout.md` · `back/application-event.md`(같은 레포 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/areas/concept/`) — SSE 재연결·이어 받기 · 회원별 팬아웃 · 같은 트랜잭션 게시를 이대로

## 2. 무엇을 하나

WORK-013 「Phase WP1-BE」 의 계약 체크박스를 **전부** 구현하고 그 절의 「시험」 을 더한다. Code Surface WP1 표가 센 자리를 **전부** 닿아라 — 표 밖에서 같은 심볼·패턴을 쓰는 곳을 찾으면 그것도 고치고 보고에 적어라(빠진 자리가 다음 판 FAIL 이다).

**먼저 기준선을 잰다** — 아무것도 고치기 전에 §5 의 시험을 한 번 돌려 기존 실패(있으면)를 `W/be-baseline.md` 에 적는다.

## 3. allowed_paths — 이 밖은 건드리지 마라

- `backend/` · `docker-compose.yml` · `Makefile`
- 리포트: `W/be-wp1-report.md` · `W/be-baseline.md` (W/ 에는 이 두 파일만)

문서(`P/`)는 고치지 마라 — 계약이 부족하거나 틀렸으면 **[질문]** 으로 묻는다(추측으로 메우지 마라).

## 4. 하지 말 것

- 커밋·push·PR 금지 — 변경은 워크트리에 남긴다
- **사용자 포트·프로세스를 건드리지 마라**(8001 · 5176 · 54329) · 로컬 스택을 띄우지 마라 · 운영 접속 금지
- 범위 밖(WORK-013 다른 Phase · DEC-010 범위 밖) 금지

## 5. 검증 — **관련 시험만** (사용자 지시 2026-10-08)

- WORK-013 「Phase WP1-BE」 의 **「시험」 줄에 적힌 Makefile 타겟·파일만** 돌린다(P-8). **전체 스위트(`make test-unit` · `make test-contract` · `make test-postgres` 를 거르지 않고 통째로) 금지 · `make verify` 금지 · `uv run pytest` 직접 호출 금지** — 전체는 E2E 직전에 코디가 한 번 돈다
- 격리 PostgreSQL 이 필요하면 사용자 54329 가 아닌 **별도 컨테이너·포트**로
- 기존 실패는 기준선과 분리해 보고

## 6. 리포트 `W/be-wp1-report.md`

계약 체크박스별 구현 위치(파일:줄) · Code Surface 표 대비 닿은 자리 개수(표 밖에서 더 찾은 것 포함) · 새 시험 목록 · 검증 명령과 수치(통과/실패) · 미결·주의점

## 7. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 코디handle 은 세션 재연결로 바뀐다.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_aa9fb9af-eed1-45ee-baad-95e52082321d --from <네 워커handle — preamble 에 있다> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: WP1-BE" \
  --body "리포트 경로 / 계약 체크박스 n/n / 검증 수치 / 미결"

# (2) 직접 주입
orca terminal send --terminal term_aa9fb9af-eed1-45ee-baad-95e52082321d \
  --text "[worker_done] backend WP1-BE 완료 — <한 줄 요약>. 리포트 be-wp1-report.md" --enter
```

- 막히면: `orca terminal send --terminal term_aa9fb9af-eed1-45ee-baad-95e52082321d --text "[질문] backend: <질문>" --enter`

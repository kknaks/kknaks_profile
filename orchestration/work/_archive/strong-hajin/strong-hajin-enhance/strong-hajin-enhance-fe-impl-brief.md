# [frontend] 고도화 구현 — WORK-012 Phase WP1-FE (이후 Phase 는 지시서로 이어 받는다)

너는 **strong-hajin `frontend` 워커**다. 너는 이 워크트리에서 조사(`fe-survey-report.md`)를 한 그 워커다 — 이제 **구현**이다. 맥락이 없으면 아래를 먼저 읽어라:

- 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-2/orchestration/roles/strong-hajin/frontend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- 코드 레포 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-enhance/AGENTS.md`
- 네 조사 리포트: `W/fe-survey-report.md`

경로 약어: `P/` = `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-2/para/projects/summer-star/strong-hajin/` · `W/` = `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-2/orchestration/work/strong-hajin-enhance/`

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-enhance` (branch `kknaksss/strong-hajin-enhance`, base `origin/main` `f0ad522`)

⚠ backend 워커가 `backend/` 에서 병렬 작업 중 — 건드리지 마라. 005·014 의 서버 계약은 WORK-012 WP1-BE 절에 고정돼 있다(같은 판에 BE 가 구현) — 그 계약대로 소비하라

## 1. SSOT — 계약 (여기 없는 것은 발명하지 마라)

- **실행 계획 — 이번 판의 할 일 목록**: `P/30-work/work-012-enhance.md` **「Phase WP1-FE」 절**(계약 체크박스 · 완료 조건 · 시험) + 「Code Surface — 전수 grep 개수표」 의 WP1 표(닿는 곳 전부)
- **계약**: `P/20-spec/spec-010-meeting-ax-enhance.md` · `P/20-spec/spec-008-external-channels.md`(v0.6.0) — Phase 절이 가리키는 절
- 결정: `P/10-decision/decision-009-enhance.md` (닫힌 OQ 포함)

**기대는 개념** — 해당 없음.

## 2. 무엇을 하나

WORK-012 「Phase WP1-FE」 의 계약 체크박스를 **전부** 구현하고 그 절의 「시험」 을 더한다. Code Surface 표가 센 자리를 **전부** 닿아라 — 표 밖에서 같은 심볼·패턴을 쓰는 곳을 찾으면 그것도 고치고 보고에 적어라(빠진 자리가 다음 판 FAIL 이다).

**먼저 기준선을 잰다** — 아무것도 고치기 전에 아래 §5 시험을 한 번 돌려 기존 실패(있으면)를 `W/fe-baseline.md` 에 적는다. 이후 「기존 실패」 와 「이번 실패」 를 가른다.

## 3. allowed_paths — 이 밖은 건드리지 마라

- `frontend/` (단, `frontend/src-tauri/` 는 이번 판 아님 — SHELL Phase 에서 따로)
- 리포트: `W/fe-wp1-report.md` · `W/fe-baseline.md` (이 두 파일만 W/ 에 쓴다)

문서(`P/`)는 고치지 마라 — 계약이 부족하거나 틀렸으면 **[질문]** 으로 묻는다(추측으로 메우지 마라).

## 4. 하지 말 것

- 커밋·push·PR 금지 — 변경은 워크트리에 남긴다
- **사용자 포트·프로세스를 건드리지 마라**(8001 · 5176 · 54329) · 로컬 스택을 띄우지 마라(E2E 는 코디가 한다) · 운영 접속 금지
- 범위 밖(WORK-012 다른 Phase · DEC-009 범위 밖)을 하지 마라

## 5. 검증

`make frontend-test` · `make frontend-build` — 통과할 때까지 고친다. 기존 실패는 기준선과 분리해 보고한다.

## 6. 리포트 `W/fe-wp1-report.md`

계약 체크박스별 구현 위치(파일:줄) · Code Surface 표 대비 닿은 자리 개수(표 밖에서 더 찾은 것 포함) · 새 시험 목록 · 검증 수치(통과/실패 수) · 미결·주의점

## 7. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 코디handle 은 세션 재연결로 바뀐다 — 확실하지 않으면 코디에게 [질문] 으로 묻지 말고 preamble 값을 따르라.

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_367ca23a-f846-44c0-afc7-07b6655df214 --from <네 워커handle — preamble 에 있다> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: WP1-FE" \
  --body "리포트 경로 / 계약 체크박스 n/n / 검증 수치 / 미결"

# (2) 직접 주입
orca terminal send --terminal term_367ca23a-f846-44c0-afc7-07b6655df214 \
  --text "[worker_done] frontend WP1-FE 완료 — <한 줄 요약>. 리포트 fe-wp1-report.md" --enter
```

- 막히면: `orca terminal send --terminal term_367ca23a-f846-44c0-afc7-07b6655df214 --text "[질문] frontend: <질문>" --enter`

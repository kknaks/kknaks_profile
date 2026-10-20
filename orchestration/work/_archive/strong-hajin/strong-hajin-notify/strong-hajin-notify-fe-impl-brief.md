# [frontend] 알림 구현 — WORK-013 Phase WP1-FE (이후 Phase 는 지시서로 이어 받는다)

너는 **strong-hajin `frontend` 워커**다. 이 워크트리에서 조사(`fe-survey-report.md`)와 P0(`p0-report.md`)를 한 그 워커일 수 있다 — 이제 **구현**이다. 맥락이 없으면 먼저 읽어라:

- 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/roles/strong-hajin/frontend/role.md` (+ 같은 폴더 문서) · 코드 레포 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-notify/AGENTS.md`
- 조사 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/fe-survey-report.md` · 서버 쪽 구현 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/be-wp1-report.md`(WP1-BE 가 이미 구현했다 — 계약의 실물)

경로 약어: `P/` = `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/projects/summer-star/strong-hajin/` · `W/` = `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/`
작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-notify` (branch `kknaksss/strong-hajin-notify`)

⚠ backend 의 WP1-BE 변경이 워크트리에 있다(코드 검수 중) — `backend/` 는 건드리지 마라

## 1. SSOT
- **할 일**: `P/30-work/work-013-notifications.md` **「Phase WP1-FE」 절** + 「이 판의 원칙」 P-1~P-10 + Code Surface **WP1 표의 화면 줄 전부**
- **계약**: `P/20-spec/spec-011-notifications.md`(v0.2.2) **§4.1**(연결 수명 — 첫/둘째 `ready` · `resync` · 백오프 · `?last_event_id=` · `/api/auth/me` 로 세션 가르기 · 10회 멈춤 + 5분 느린 재시도 · 한 연결 다시 읽기 한 번) · `spec-008` §4.4
- **기대는 개념** — `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/para/areas/concept/cs/server-sent-events.md`

## 2. 무엇을 하나
WP1-FE 계약 체크박스를 **전부** 구현하고 그 절의 「시험」 을 더한다. Code Surface WP1 표의 화면 자리(`useInboxStream(` · `new WebSocket` · `inboxStreamUrl` · 허브 · `onReconnect` · 세션 상실 · WS 시험 대역 등)를 **전부** 닿아라 — 표 밖에서 같은 심볼을 찾으면 고치고 보고. **회의 WS(`features/meetings/stream.ts`)는 건드리지 마라.**
먼저 기준선: §5 시험을 고치기 전에 한 번 돌려 기존 실패를 `W/fe-baseline.md` 에.

## 3. allowed_paths
- `frontend/` (단 `frontend/src-tauri/` 는 이번 Phase 아님)
- 리포트 `W/fe-wp1-report.md` · `W/fe-baseline.md`

## 4. 하지 말 것
- 커밋·push·PR 금지 · 사용자 포트·프로세스(8001 · 5176 · 54329) 금지 · 로컬 스택 띄우기 금지 · 운영 접속 금지 · 문서(`P/`) 수정 금지(모자라면 [질문])

## 5. 검증 — **관련 시험만** (사용자 지시)
- WP1-FE 「시험」 줄의 **고른 vitest 파일만** `cd frontend && npx vitest run <파일들>` + 타입 `npx tsc --noEmit`. **전체 `make frontend-test` · `make verify` 금지** — 전체는 E2E 직전 코디가 한 번

## 6. 리포트 `W/fe-wp1-report.md`
체크박스별 구현 위치(파일:줄) · Code Surface 대비 닿은 자리 수 · 새/바뀐 시험 · 검증 명령과 수치 · 미결

## 7. 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**
```bash
orca orchestration send \
  --to term_aa9fb9af-eed1-45ee-baad-95e52082321d --from <네 워커handle — preamble 에 있다> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: WP1-FE" \
  --body "리포트 경로 / 계약 체크박스 n/n / 검증 수치 / 미결"
orca terminal send --terminal term_aa9fb9af-eed1-45ee-baad-95e52082321d \
  --text "[worker_done] frontend WP1-FE 완료 — <한 줄 요약>. 리포트 fe-wp1-report.md" --enter
```
- 막히면: `orca terminal send --terminal term_aa9fb9af-eed1-45ee-baad-95e52082321d --text "[질문] frontend: <질문>" --enter`

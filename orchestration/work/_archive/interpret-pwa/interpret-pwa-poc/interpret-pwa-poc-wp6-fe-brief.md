# [frontend] interpret-pwa WORK-001 WP6-FE — 묶음 수정(시안 · D-18~D-21 · 리뷰 FAIL/WARN)

너는 **interpret-pwa `frontend` 워커**다. 역할 문서(절대경로): `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/roles/interpret-pwa/frontend/role.md` (+ 같은 폴더 rules · skills · tools · workflow)

작업 워크트리: `/Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-poc` · base `origin/main` (커밋 없음 · 1루프 변경이 워크트리에 그대로 있다 — 그 위에 고친다)
⚠ 다른 워커가 같은 워크트리에서 병렬 작업 중 — `back/` · 루트 compose · env 예시 · `design/`(시안 — 읽기만) 는 건드리지 마라. `.env` 는 열지 마라(코드가 읽는 것은 괜찮다).

## 1. SSOT

- `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md` **0.3.0** ← 계약 정본. 변경 이력에서 0.3.0 이 바꾼 절부터 읽어라
- `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/30-work/work-001-interpret-pwa.md` **WP6-FE 행** ← 범위 · 완료 조건 · 부분 검증 명령. 이 행이 이번 일의 전부다
- `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/10-decision/decision-001-interpret-pwa.md` D-18 ~ D-21
- 근거 자료: `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-poc/review-code-report.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-poc/e2e-feedback-batch-1.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-poc/live-check-2026-10-26.json` · `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-poc/design-report.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-poc/design-r2-report.md`
- **시안이 화면 정본**(D-20): `/Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-poc/design/` (README · `project/*.dc.html` 17화면). 화면마다 시안과 스크린샷 대조 — 다른 곳은 리포트에 표로
- ccc 테마: `git -C /Users/kknaks/git/toy_pr2/cc-prototype show origin/main:procedure/front/app/styles/ceramique-theme.css` + `<html data-product="ceramique">`
- 실발화 1회: 키가 루트 `.env` 에 있다 — back 은 WP6-BE 가 같이 고치는 중이니 확인 때 back 을 띄울 일이 있으면 backend 와 포트가 겹치지 않게 순서를 리포트에 남겨라(8800 이 이미 떠 있으면 그걸 쓴다 · 네가 띄운 것만 내린다)

## 2. allowed_paths

- `front/**`

## 3. 검증

- WORK-001 WP6-FE 행의 부분 검증 명령 1회씩. 전체 검증은 WP7 에서 코디가 한다
- 사용자 포트(3600 · 8600 · 3700 · 8700)는 건드리지 않는다. 네가 띄운 프로세스는 끝나면 내린다

## 4. 하지 말 것

- 커밋 · push · PR · 범위 밖 수정 · 키 · 계정값 출력

## 5. 완료 보고 — 문구 변경 금지

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-poc/wp6-fe-report.md` (rules.md 형식). 끝나면 두 명령 모두:

```bash
orca orchestration send --to term_ce3ec37d-8f58-4bca-9420-d55b08c591e2 --from <네 워커handle> --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> --subject "frontend 완료: WP6-FE <한 줄>" --body "변경 파일 / 요약 / 검증 수치 / 미결"
orca terminal send --terminal term_ce3ec37d-8f58-4bca-9420-d55b08c591e2 --text "[worker_done] frontend WP6-FE 완료 — <한 줄>. 상세는 인박스." --enter
```
코디 핸들은 보고 직전 `orca terminal list --json` 에서 제목 'Interpretation PWA with terminology integration' 으로 확인하고 다르면 그쪽으로.
막히면: `orca terminal send --terminal <코디handle> --text "[질문] frontend: <질문>" --enter`

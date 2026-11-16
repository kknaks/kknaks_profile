# [frontend] interpret-pwa WORK-001 WP10 — 우리 용어집 시드(D-33)

너는 interpret-pwa frontend 워커다(역할: `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/roles/interpret-pwa/frontend/role.md`). 워크트리 `/Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-poc` (main d0a91a7 = 배포본). 커밋 · push 금지 · `.env` 열지 마라.
SSOT: `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md` **0.4.0 §4**(+ 변경 이력) · `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/30-work/work-001-interpret-pwa.md` **WP10 행**(범위 · 완료 조건 · 부분 검증) · DEC-001 D-33
- back WP9 와 병렬 — 메뉴 API 모양은 SPEC §4 정본(rows{id,category,ko,koAliases,term,aliases,reviewed}). back 이 아직이면 그 모양 목업으로 시험
allowed_paths: front/**. 다른 워커가 같은 워크트리에서 병렬 — 남의 폴더 건드리지 마라.
리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-poc/wp9-fe-report.md`(파일명 고정). 완료 두 채널 — 코디 handle 은 보고 직전 `orca terminal list --json` 에서 제목에 'Interpretation PWA' 가 든 것(지금 term_b9fdf879-633c-469b-bbfe-e0a25fae3193):
`orca orchestration send --to <코디> --from <너> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "frontend 완료: WP10 <한 줄>" --body "…"` + `orca terminal send --terminal <코디> --text "[worker_done] frontend WP10 완료 — <한 줄>" --enter`

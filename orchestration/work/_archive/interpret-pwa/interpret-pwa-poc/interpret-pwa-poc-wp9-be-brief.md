# [backend] interpret-pwa WORK-001 WP9 — 우리 용어집 시드(D-33)

너는 interpret-pwa backend 워커다(역할: `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/roles/interpret-pwa/backend/role.md`). 워크트리 `/Users/kknaks/orca/workspaces/interpret-pwa/interpret-pwa-poc` (main d0a91a7 = 배포본). 커밋 · push 금지 · `.env` 열지 마라.
SSOT: `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/20-spec/spec-001-interpret-pwa.md` **0.4.0 §4**(+ 변경 이력) · `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/para/projects/summer-star/interpret-pwa/30-work/work-001-interpret-pwa.md` **WP9 행**(범위 · 완료 조건 · 부분 검증) · DEC-001 D-33
- 처분(코디 · 2026-10-27): ① zh-Hant context 재료 = 시드 zh-Hant entry(t2s) — 채택 ② 괄호 분해 규칙 SPEC 그대로 ③ **첫 시드에 써마지FLX 의 ko_aliases 에 「써마지」**(출처 note: 사용자 지적 2026-10-26) ④ 시드 깨지면 기동 실패 ⑤ zh-Hant 한도 ⑬ 실측 → 18832 보다 작으면 기본값을 고치고 리포트에
- 실물: 키는 레포 루트 .env(값 출력 금지). 써마지 · 울쎄라 정방향(ko → zh · zh-Hant · en) · 역방향(zh 「热玛吉」「超声刀」 발화 → ko) 포함
allowed_paths: back/** · .env.example. 다른 워커가 같은 워크트리에서 병렬 — 남의 폴더 건드리지 마라.
리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-poc/wp9-be-report.md`(파일명 고정). 완료 두 채널 — 코디 handle 은 보고 직전 `orca terminal list --json` 에서 제목에 'Interpretation PWA' 가 든 것(지금 term_b9fdf879-633c-469b-bbfe-e0a25fae3193):
`orca orchestration send --to <코디> --from <너> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "backend 완료: WP9 <한 줄>" --body "…"` + `orca terminal send --terminal <코디> --text "[worker_done] backend WP9 완료 — <한 줄>" --enter`
